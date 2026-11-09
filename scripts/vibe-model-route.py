#!/usr/bin/env python3
"""
vibe-model-route.py — Bộ phân loại độ phức tạp (T0..T4) & định tuyến model tất định cho xưởng Vibe.

Áp dụng cho cả thư mục gốc Vibe/ và mọi repo con bên trong Vibe/.
Chấm điểm trên 4 trục (mỗi trục 0..2, tổng S = 0..8):
  - Ambiguity (A)        : 0 = đã có khuôn/script cứng | 1 = có hợp đồng, tự quyết chi tiết | 2 = ý tưởng mở 0→1
  - Domain_Risk (R)      : 0 = sửa nhỏ dễ đảo ngược   | 1 = chạm logic/state nhiều file   | 2 = Pháp lý / Kế toán TT99 / Spec S1 / Core UI
  - Taste_Originality (T): 0 = cơ học/kỹ thuật thuần  | 1 = cần câu chữ/UI mượt theo mẫu  | 2 = sáng tạo Design 0→1 chống mùi AI / khảo cứu sâu
  - Scope (Sc)           : 0 = 1–2 file               | 1 = 3–6 file (1 lát cắt / 1 bài)  | 2 = xuyên toàn repo / đa phòng ban

Cách dùng:
  python3 -I scripts/vibe-model-route.py --task "Thiết kế lại toàn bộ UI/UX chống mùi AI" --stage S2
  python3 -I scripts/vibe-model-route.py --ambiguity 1 --risk 2 --taste 1 --scope 1 --stage S3 --prefer claude
  python3 -I scripts/vibe-model-route.py --preset vibe-post-locked
  python3 -I scripts/vibe-model-route.py --list-presets
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

PRESETS: dict[str, dict] = {
    "dedupe-check": {
        "desc": "Gộp trùng DEDUPE, chạy vibe-check.sh, check-story.py, đếm chữ, cân Nợ/Có",
        "stage": "ANY",
        "scores": (0, 0, 0, 0),
        "force_t0": True,
    },
    "s0-sweep": {
        "desc": "S0 Discovery — Pha 1 SWEEP đa mũi độc lập quét thông tin & đối thủ",
        "stage": "S0",
        "scores": (1, 0, 0, 1),
    },
    "s0-refute": {
        "desc": "S0 Discovery — Pha 3 REFUTE (phản biện giết ứng viên + fix_if_any)",
        "stage": "S0",
        "scores": (2, 2, 1, 1),
        "prefer": "claude",
    },
    "s0-judge-legal": {
        "desc": "S0 Discovery — Pha 4 JUDGE + LEGAL-SCREEN (vào vbpl.vn/Công báo bằng trình duyệt thật)",
        "stage": "S0",
        "scores": (2, 2, 0, 2),
        "prefer": "gemini",
    },
    "s1-spec-prd": {
        "desc": "S1 Spec — Viết PRD.md, ACCEPTANCE, SUCCESS-CRITERIA, TRACKING-PLAN, LEGAL-REVIEW",
        "stage": "S1",
        "scores": (2, 2, 1, 1),
        "prefer": "claude",
    },
    "s1-t3-reconstruct": {
        "desc": "S1/S2 T3 Tái lập — Dựng lại kết luận từ nguồn gốc bằng họ model ngược với người viết",
        "stage": "S1",
        "scores": (1, 2, 0, 2),
        "prefer": "gemini",
    },
    "s1-html-summary": {
        "desc": "S1/S2 Review HTML — Chưng cất tài liệu quyết định docs/*.html (≤ 520 từ)",
        "stage": "S1",
        "scores": (0, 1, 1, 1),
    },
    "s2-design-0to1": {
        "desc": "S2 Design — Định hình ngôn ngữ thiết kế 0→1 chống mùi AI (Taste Distillation / Core UI)",
        "stage": "S2",
        "scores": (2, 2, 2, 2),
    },
    "s2-design-extend": {
        "desc": "S2 Design — Mở rộng màn hình / component theo Design System đã khoá",
        "stage": "S2",
        "scores": (0, 1, 1, 1),
    },
    "s3-build-slice": {
        "desc": "S3 Build — Code lát cắt dọc theo PRD & mockup đã duyệt + viết test TDD",
        "stage": "S3",
        "scores": (0, 1, 1, 1),
    },
    "vibe-post-locked": {
        "desc": "S3 Content — Lên bài mới (/vibe-post) theo khuôn Diorama v3.0 + C9 đã khoá",
        "stage": "S3",
        "scores": (0, 2, 1, 1),
    },
    "vibe-post-new-standard": {
        "desc": "S1/S3 Content — Đúc bài mẫu đầu tiên khi nâng cấp chuẩn nội dung mới (như C9 3A)",
        "stage": "S1",
        "scores": (1, 2, 2, 1),
    },
    "ke-toan-review": {
        "desc": "Phòng Kế toán — Soát K1–K4 (số học + TT 99/2025 + khái niệm + người mới hiểu sai)",
        "stage": "S3",
        "scores": (0, 2, 1, 2),
    },
    "s4-browser-qa": {
        "desc": "S4 QA — Lái trình duyệt thật kiểm tra console, network, a11y, LCP",
        "stage": "S4",
        "scores": (0, 1, 0, 1),
    },
    "s4-deep-review": {
        "desc": "S4 QA — Code review, security review & đối chiếu ACCEPTANCE.md (khác họ với Dev S3)",
        "stage": "S4",
        "scores": (1, 2, 0, 2),
        "prefer": "gemini",
    },
}


@dataclass(frozen=True)
class RouteDecision:
    tier: str
    score: int
    breakdown: dict[str, int]
    primary_family: str
    primary_model: str
    primary_cli_id: str
    effort: str
    fallback_model: str
    cross_check_model: str
    subagent_model_arg: str
    relative_cost: str
    claude_cmd: str
    agy_cmd: str
    rationale: str
    downgrade_rule: str


def infer_scores(task: str, stage: str, fail_count: int) -> tuple[int, int, int, int, bool]:
    t = task.lower()
    st = (stage or "").upper()

    # T0 deterministic check
    if any(k in t for k in ("vibe-check", "check-story", "dedupe", "gộp trùng", "đếm từ", "word count", "chmod")):
        return (0, 0, 0, 0, True)

    amb = 0
    risk = 0
    taste = 0
    scope = 0

    # Ambiguity
    if any(k in t for k in ("0->1", "0→1", "ý tưởng mới", "từ đầu", "refactor toàn bộ", "chưa rõ", "khám phá", "discovery")):
        amb = 2
    elif any(k in t for k in ("prd", "spec", "kiến trúc", "설계", "design", "pipeline", "nâng cấp", "phương án")):
        amb = 1

    # Risk
    if any(k in t for k in ("kế toán", "tt 99", "tt99", "pháp lý", "legal", "licences", "sổ cái", "ledger", "refute", "phản biện", "security", "c9", "hợp đồng")):
        risk = 2
    elif any(k in t for k in ("build", "feature", "component", "api", "state", "test", "qa", "bài viết", "vibe-post")):
        risk = 1

    # Taste & Originality
    if any(k in t for k in ("quá là ai", "mùi ai", "kurzgesagt", "taste", "diorama", "core design system", "refactor toàn bộ ui", "độc bản", "0→1")):
        taste = 2
    elif any(k in t for k in ("ui", "ux", "mockup", "html", "css", "animation", "kịch bản", "video", "khảo cứu", "văn phong", "brand-voice")):
        taste = 1

    # Scope
    if any(k in t for k in ("toàn bộ", "tất cả repo", "xưởng", "all repos", "pipeline", "3 bài", "multi-category")):
        scope = 2
    elif any(k in t for k in ("bài", "story", "slice", "stage", "module", "trang")):
        scope = 1

    # Stage baseline adjustments
    if st == "S0" and "sweep" in t:
        return (1, 0, 0, 1, False)
    if st == "S2" and taste == 2 and amb >= 1:
        amb = max(amb, 2)
        risk = max(risk, 2)
        scope = max(scope, 1)

    # Escalation on repeated failure
    if fail_count == 1:
        amb = min(2, amb + 1)
        risk = min(2, risk + 1)
    elif fail_count >= 2:
        amb, risk, taste, scope = 2, 2, 2, max(1, scope)

    if amb + risk + taste + scope == 0:
        scope = 1  # default non-script task is at least T1
    return (amb, risk, taste, scope, False)


def build_decision(
    amb: int,
    risk: int,
    taste: int,
    scope: int,
    force_t0: bool = False,
    prefer: str = "auto",
) -> RouteDecision:
    s = 0 if force_t0 else (amb + risk + taste + scope)
    bd = {"ambiguity": amb, "risk": risk, "taste": taste, "scope": scope}

    if force_t0 or s == 0:
        return RouteDecision(
            tier="T0",
            score=0,
            breakdown=bd,
            primary_family="script",
            primary_model="Python / Bash Script",
            primary_cli_id="python3 / bash",
            effort="n/a",
            fallback_model="haiku",
            cross_check_model="n/a (tất định)",
            subagent_model_arg="flash_lite",
            relative_cost="0.0x (0 token)",
            claude_cmd="# CẤM gọi LLM cho T0 — chạy trực tiếp script: bash scripts/vibe-check.sh <app>",
            agy_cmd="# CẤM gọi LLM cho T0 — chạy trực tiếp script: python3 -I scripts/check-story.py",
            rationale="Tác vụ tất định (gộp trùng, đếm từ, cân Nợ/Có, kiểm đường dẫn). Dùng script 100% chính xác và tốn 0 token.",
            downgrade_rule="Giữ nguyên ở T0.",
        )

    if s <= 2:
        use_gemini = prefer in ("auto", "gemini") and taste == 0
        return RouteDecision(
            tier="T1",
            score=s,
            breakdown=bd,
            primary_family="gemini" if use_gemini else "claude",
            primary_model="Gemini 3.8 Flash" if use_gemini else "Claude Haiku 4.5",
            primary_cli_id="gemini-3.8-flash-medium" if use_gemini else "haiku",
            effort="low",
            fallback_model="sonnet",
            cross_check_model="Script T0 (vibe-check / check-story)",
            subagent_model_arg="flash",
            relative_cost="0.3x – 1.0x",
            claude_cmd='claude -p --model haiku --effort low --fallback-model sonnet "<prompt>"',
            agy_cmd='agy -p --model gemini-3.8-flash-medium --effort low "<prompt>"',
            rationale="Task độ phức tạp thấp (SWEEP thông tin, đọc DOM/log trình duyệt, sửa cơ học/đồng bộ file). Flash/Haiku nhanh gấp 4x và rẻ gấp 3–10x.",
            downgrade_rule="Nếu fail 1 lần ⇒ nâng lên T2 (Claude Sonnet / Gemini 4 Argon Medium).",
        )

    if s <= 4:
        use_claude = prefer in ("auto", "claude") or taste >= 1
        return RouteDecision(
            tier="T2",
            score=s,
            breakdown=bd,
            primary_family="claude" if use_claude else "gemini",
            primary_model="Claude Sonnet 5.5" if use_claude else "Gemini 4 Argon (Medium)",
            primary_cli_id="sonnet" if use_claude else "gemini-4-argon-medium",
            effort="high" if s == 4 else "medium",
            fallback_model="opus",
            cross_check_model="Gemini 4 Argon (Medium/High)" if use_claude else "Claude Sonnet 5.5",
            subagent_model_arg="inherit",
            relative_cost="2.0x – 3.5x",
            claude_cmd=f'claude -p --model sonnet --effort {"high" if s == 4 else "medium"} --fallback-model opus "<prompt>"',
            agy_cmd='agy -p --model gemini-4-argon-medium --effort medium "<prompt>"',
            rationale="Ngựa thồ chủ lực (S3 Build theo spec, viết test, lên bài mới theo khuôn C9 đã khoá, tóm tắt HTML ≤520 từ). Đủ thông minh mà không đốt giá 5x–10x của Opus/Fable.",
            downgrade_rule="Các bước kiểm tra cú pháp/số học bên trong task phải đẩy xuống T0 (script). Nếu fail 2 lần ⇒ nâng lên T3 (Opus / Argon High).",
        )

    if s <= 6:
        use_claude = prefer in ("auto", "claude") and (taste >= 1 or amb >= 1)
        return RouteDecision(
            tier="T3",
            score=s,
            breakdown=bd,
            primary_family="claude" if use_claude else "gemini",
            primary_model="Claude Opus 5.5" if use_claude else "Gemini 4 Argon (High)",
            primary_cli_id="opus" if use_claude else "gemini-4-argon-high",
            effort="high",
            fallback_model="sonnet",
            cross_check_model="Gemini 4 Argon (High) [cross-vendor]" if use_claude else "Claude Opus 5.5 [cross-vendor]",
            subagent_model_arg="pro",
            relative_cost="5.0x",
            claude_cmd='claude -p --model opus --effort high --fallback-model sonnet "<prompt>"',
            agy_cmd='agy -p --model gemini-4-argon-high --effort high "<prompt>"',
            rationale="Task đòi hỏi suy luận đa tầng, phản biện REFUTE, soát kế toán TT 99/2025, viết PRD S1 hoặc đúc bài khảo cứu mẫu đầu tiên. Bắt buộc kiểm chéo khác họ model (Opus ↔ Argon High).",
            downgrade_rule="KHOÁ-RỒI-HẠ: Ngay khi mẫu đầu tiên/hợp đồng đã được duyệt và có script kiểm, hạ các lần chạy lặp lại sau xuống T2 (Sonnet).",
        )

    # T4 (s >= 7)
    return RouteDecision(
        tier="T4",
        score=s,
        breakdown=bd,
        primary_family="claude",
        primary_model="Claude Fable 5 (Frontier Taste & 0→1)",
        primary_cli_id="fable",
        effort="high",
        fallback_model="opus,sonnet",
        cross_check_model="Gemini 4 Argon (High) + chrome-devtools-mcp [cross-vendor]",
        subagent_model_arg="pro",
        relative_cost="10.0x (CẢNH BÁO CHI PHÍ CAO)",
        claude_cmd='claude -p --model fable --effort high --fallback-model opus,sonnet "<prompt>"',
        agy_cmd='agy -p --model claude-opus-5-5-high --effort high "<prompt>"',
        rationale="Đỉnh cao 0→1 (S2 Design Direction chống mùi AI, Taste Distillation, hoặc gỡ bế tắc sau khi T3 thất bại 2 lần). Chỉ Fable mới đủ độ tinh tế để tạo ngôn ngữ thiết kế độc bản.",
        downgrade_rule="BẮT BUỘC KHOÁ-RỒI-HẠ: Fable chỉ đúc engine/design system 1 lần duy nhất. CẤM dùng Fable chạy hàng loạt hoặc sửa lặt vặt sau khi đã có khuôn (hạ về Sonnet T2).",
    )


def format_tag(d: RouteDecision) -> str:
    b = d.breakdown
    return (
        f"[Route: {d.tier} · S={d.score}/8 "
        f"(A={b['ambiguity']}, R={b['risk']}, T={b['taste']}, Sc={b['scope']}) · "
        f"Primary={d.primary_model} ({d.effort}) · CrossCheck={d.cross_check_model}]"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Bộ phân loại task (T0..T4) và định tuyến model cho xưởng Vibe.")
    ap.add_argument("--preset", choices=sorted(PRESETS.keys()), help="Chọn mẫu công việc có sẵn trong xưởng")
    ap.add_argument("--list-presets", action="store_true", help="Liệt kê toàn bộ mẫu định tuyến có sẵn")
    ap.add_argument("--task", default="", help="Mô tả ngắn công việc (để tự suy điểm nếu không truyền 4 trục)")
    ap.add_argument("--stage", default="", help="Stage hiện tại (S0..S6)")
    ap.add_argument("--ambiguity", type=int, choices=(0, 1, 2), help="Độ mơ hồ (0..2)")
    ap.add_argument("--risk", type=int, choices=(0, 1, 2), help="Độ nhạy cảm / rủi ro nghiệp vụ (0..2)")
    ap.add_argument("--taste", type=int, choices=(0, 1, 2), help="Đòi hỏi Gu thẩm mỹ & sáng tạo độc bản (0..2)")
    ap.add_argument("--scope", type=int, choices=(0, 1, 2), help="Quy mô phối hợp (0..2)")
    ap.add_argument("--fail-count", type=int, default=0, help="Số lần model bậc thấp đã thất bại liên tiếp trên task này")
    ap.add_argument("--prefer", choices=("auto", "claude", "gemini"), default="auto", help="Ưu tiên họ model khi đồng hạng")
    ap.add_argument("--json", action="store_true", help="Xuất JSON máy đọc")
    args = ap.parse_args()

    if args.list_presets:
        print(f"{'PRESET':<24} {'STAGE':<6} {'TIER':<5} {'ĐIỂM':<8} MÔ TẢ")
        print("─" * 95)
        for k, v in PRESETS.items():
            a, r, t, sc = v["scores"]
            dec = build_decision(a, r, t, sc, v.get("force_t0", False), v.get("prefer", "auto"))
            print(f"{k:<24} {v['stage']:<6} {dec.tier:<5} S={dec.score}/8    {v['desc']} → {dec.primary_model}")
        return 0

    force_t0 = False
    prefer = args.prefer
    if args.preset:
        p = PRESETS[args.preset]
        amb, risk, taste, scope = p["scores"]
        force_t0 = p.get("force_t0", False)
        if prefer == "auto":
            prefer = p.get("prefer", "auto")
    elif all(x is not None for x in (args.ambiguity, args.risk, args.taste, args.scope)):
        amb, risk, taste, scope = args.ambiguity, args.risk, args.taste, args.scope
    elif args.task:
        amb, risk, taste, scope, force_t0 = infer_scores(args.task, args.stage, args.fail_count)
    else:
        ap.error("Cần truyền --preset, hoặc --task, hoặc đủ 4 trục (--ambiguity --risk --taste --scope).")
        return 2

    if args.fail_count > 0 and not args.task:
        if args.fail_count == 1:
            amb, risk = min(2, amb + 1), min(2, risk + 1)
        else:
            amb, risk, taste, scope = 2, 2, 2, max(1, scope)
        force_t0 = False

    dec = build_decision(amb, risk, taste, scope, force_t0, args.prefer)

    if args.json:
        out = asdict(dec)
        out["route_tag"] = format_tag(dec)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(format_tag(dec))
    print(f"  · Bậc phức tạp   : {dec.tier} (Điểm S = {dec.score}/8: Ambiguity={amb}, Risk={risk}, Taste={taste}, Scope={scope})")
    print(f"  · Model chính    : {dec.primary_model} [CLI: {dec.primary_cli_id} · effort: {dec.effort}]")
    print(f"  · Dự phòng       : --fallback-model {dec.fallback_model}")
    print(f"  · Kiểm chéo      : {dec.cross_check_model}")
    print(f"  · Hệ số chi phí  : {dec.relative_cost}")
    print(f"  · Lệnh Claude    : {dec.claude_cmd}")
    print(f"  · Lệnh AGY       : {dec.agy_cmd}")
    print(f"  · Lý do chọn     : {dec.rationale}")
    print(f"  · Luật hạ cấp    : {dec.downgrade_rule}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
