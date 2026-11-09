#!/usr/bin/env python3
# wms-hook-guard.sh — PreToolUse hook cho Gemini / Antigravity, NẰM TRONG repo where-money-sleeps.
#
# Vì sao có bản riêng: repo này có .git riêng. Mở Antigravity thẳng ở đây, hoặc clone riêng repo,
# thì Vibe/scripts/vibe-hook-guard.sh không đi theo. Bản này làm mọi việc bản xưởng làm, cộng cổng WMS-R4.
#
# Trả "decision": "force_ask" (bắt hộp hỏi Duy, bỏ qua cache Always Allow) khi:
#   1. Payload không đọc được                     — FAIL-CLOSED (bản xưởng thì cho qua)
#   2. run_command: git push · gh pr merge · gh release · vercel · netlify · wrangler (kể cả rtk/npx)
#   3. run_command chứa mẫu "đã duyệt" hoặc status "published" (sed/python ghi thẳng dữ liệu)
#   4. Ghi file (mọi tool có khoá đường dẫn/nội dung): số lần "đã duyệt" hoặc status "published"
#      trong text MỚI nhiều hơn text CŨ. "Đã duyệt" = đúng ngữ nghĩa C7 của check-story.py:
#      approvedBy không rỗng và không chứa "demo". Bỏ qua file .md (tài liệu chứa ví dụ).
#   5. PIPELINE.md: giá trị `pointer:` đổi (bất kỳ hướng nào) hoặc thêm dòng APPROVE/DUYỆT S0–S6.
#
# KHÔNG bắt được (ghi ở AGENT-CMS-PIPELINE §0): hoán đổi approvedBy giữa hai bài (số lần không đổi),
# lệnh shell ghi file mà chuỗi mẫu không nằm trong lệnh, và mọi thứ nếu Antigravity không chạy hook.
# Tên tool / tên khoá tham số của Antigravity: CHƯA XÁC MINH — vì vậy đọc nhiều tên khoá.

import json
import pathlib
import re
import sys

SHIP = re.compile(
    r"(?:^|[;&|]\s*)(?:rtk\s+(?:proxy\s+)?)?(?:npx\s+)?"
    r"(?:git\s+push|gh\s+pr\s+merge|gh\s+release|vercel|netlify|wrangler|youtube-upload|yt-upload|wms-youtube-upload)\b"
)
APPROVED = re.compile(r"""["'`]?approvedBy["'`]?\s*[:=]\s*(["'`])(.*?)\1""")
PUBLISHED = re.compile(r"""["'`]?status["'`]?\s*[:=]\s*["'`]published["'`]""")
UPLOADED_PUBLIC = re.compile(r"""["'`]?embedStatus["'`]?\s*[:=]\s*["'`]uploaded_public["'`]""")
APPROVE_LINE = re.compile(r"\b(?:APPROVE|DUYỆT)\s+S[0-6]\b")
POINTER = re.compile(r"^pointer:\s*(\S+)", re.M)

PATH_KEYS = ("Path", "TargetFile", "AbsolutePath", "File", "path", "file_path")
NEW_KEYS = ("Replacement", "Content", "CodeContent", "ReplacementContent", "content", "new_string")
OLD_KEYS = ("Target", "TargetContent", "old_string")
CHUNK_KEYS = ("ReplacementChunks", "Chunks", "edits")
WRITE_TOOLS = {"edit_file", "write_file", "write_to_file", "replace_file_content", "multi_replace_file_content"}


def out(decision: str, reason: str = "") -> None:
    d = {"decision": decision}
    if reason:
        d["reason"] = reason
    print(json.dumps(d, ensure_ascii=False))
    sys.exit(0)


def approved_count(text: str) -> int:
    return sum(1 for m in APPROVED.finditer(text) if m.group(2).strip() and "demo" not in m.group(2).lower())


def published_count(text: str) -> int:
    return len(PUBLISHED.findall(text))


def uploaded_public_count(text: str) -> int:
    return len(UPLOADED_PUBLIC.findall(text))


def texts(args: dict) -> tuple[str, str]:
    """Tách text MỚI và text CŨ theo tên khoá — không gom đệ quy mù (gom mù trộn Target vào 'mới')."""
    new = [args[k] for k in NEW_KEYS if isinstance(args.get(k), str)]
    old = [args[k] for k in OLD_KEYS if isinstance(args.get(k), str)]
    for ck in CHUNK_KEYS:
        for ch in args.get(ck) or []:
            if isinstance(ch, dict):
                new += [ch[k] for k in NEW_KEYS if isinstance(ch.get(k), str)]
                old += [ch[k] for k in OLD_KEYS if isinstance(ch.get(k), str)]
    return "\n".join(new), "\n".join(old)


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        tc = payload.get("toolCall") or {}
        name = str(tc.get("name") or "")
        args = tc.get("args") or {}
        if not isinstance(args, dict):
            raise TypeError("args không phải object")
    except Exception as e:  # noqa: BLE001 — fail-closed có chủ đích
        out("force_ask", f"CỔNG WMS: không đọc được payload hook ({e!r}) — hỏi Duy thay vì cho qua.")

    if name == "run_command":
        cmd = str(args.get("CommandLine") or args.get("command") or "")
        if SHIP.search(cmd.strip()):
            out("force_ask", "CỔNG SHIP WMS: lệnh đẩy code / phát hành ra ngoài cần Duy xác nhận trực tiếp.")
        if approved_count(cmd) or published_count(cmd) or uploaded_public_count(cmd):
            out("force_ask", "CỔNG DUYỆT WMS-R4 / QĐ 56: lệnh shell ghi approvedBy / status \"published\" / embedStatus \"uploaded_public\". Chỉ Duy đăng bài.")
        out("allow")

    path_str = next((str(args[k]) for k in PATH_KEYS if args.get(k)), "")
    new_text, old_text = texts(args)
    if not path_str and not new_text:
        out("allow")                                 # tool không ghi file
    # Tool GHI FILE đã biết tên mà không đọc ra được nội dung mới ⇒ tên khoá lạ ⇒ không được đoán là vô hại.
    # (Tool lạ chỉ có khoá đường dẫn — thường là tool đọc — vẫn cho qua, để không hỏi oan mỗi lần đọc file.)
    is_pipeline = pathlib.PurePath(path_str).name == "PIPELINE.md"
    if name in WRITE_TOOLS and not new_text and (is_pipeline or not path_str.endswith(".md")):
        out("force_ask", f"CỔNG WMS: {name} không có khoá nội dung nào guard đọc được — hỏi Duy thay vì cho qua.")

    p = pathlib.Path(path_str) if path_str else None
    try:
        disk = p.read_text(errors="replace") if p is not None and p.is_file() else ""
    except OSError:
        disk = ""                                    # không đọc được đĩa ⇒ coi như file mới: so với rỗng (nghiêng về hỏi)
    if not old_text and name in ("write_file", "write_to_file"):
        old_text = disk                              # ghi đè cả file: cái cũ là file trên đĩa

    # 4 — cổng duyệt bài (WMS-R4) chạy TRƯỚC nhánh PIPELINE, cho mọi file trừ .md
    if not path_str.endswith(".md"):
        if approved_count(new_text) > approved_count(old_text):
            out("force_ask", "CỔNG DUYỆT WMS-R4: ghi approvedBy (đã duyệt). Agent không được tự duyệt — chỉ Duy.")
        if published_count(new_text) > published_count(old_text):
            out("force_ask", "CỔNG DUYỆT WMS-R4: đặt status \"published\". Agent để \"review\"; chỉ Duy đăng.")
        if uploaded_public_count(new_text) > uploaded_public_count(old_text):
            out("force_ask", "CỔNG DUYỆT WMS-R4 / QĐ 56: đặt embedStatus \"uploaded_public\". Agent chỉ được để \"pending_upload\", \"uploaded_unlisted\", hoặc \"uploaded_private\"; chỉ Duy mở công khai.")

    # 5 — cổng con trỏ
    if pathlib.PurePath(path_str).name == "PIPELINE.md" and "templates/app/PIPELINE.md" not in path_str:
        m_old = POINTER.search(old_text) or POINTER.search(disk)
        m_new = POINTER.search(new_text)
        if m_new and (not m_old or m_new.group(1) != m_old.group(1)):
            frm = m_old.group(1) if m_old else "?"
            out("force_ask", f"CỔNG DUYỆT (Quy tắc 1): đổi pointer PIPELINE.md {frm} → {m_new.group(1)}. Chỉ Duy.")
        if len(APPROVE_LINE.findall(new_text)) > len(APPROVE_LINE.findall(old_text or disk)):
            out("force_ask", "CỔNG DUYỆT (Quy tắc 1): ghi dòng APPROVE/DUYỆT vào PIPELINE.md. Chỉ Duy duyệt stage.")

    out("allow")


if __name__ == "__main__":
    main()
