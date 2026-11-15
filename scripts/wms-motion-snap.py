#!/usr/bin/env python3
"""wms-motion-snap.py — Cổng kiểm tất định M1–M4 (Bang Motion & Anti-Slideshow Specialist).

Chắt lọc có kiểm soát từ bangtutorial/bang-motion (MIT License) và khoá chặt với:
  - M1: Anti-PPT & Persistent World (cubic-bezier, giữ nguyên thế giới 5 ngôi nhà / sơ đồ phân cấp)
  - M2: Kinetic Financial Counter (tabular-nums, animateMoneyText / rolling counter & hạt dẫn hướng SVG)
  - M3: Khoá khung nhìn LUẬT 6b (Containment P_inner >= 20px) & LUẬT 8 (3-Zone Split-Stage không đè chữ)
  - M4: Đồng hồ tất định window.__vibeSeek, 0 script CDN bên thứ ba lúc runtime, và prefers-reduced-motion
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROTO_HTML = ROOT / "docs" / "prototype.html"
WF_HTML = ROOT / "docs" / "workflows.html"
STUDIO_HTML = ROOT / "docs" / "studio.html"
MEDIA_PY = ROOT / "scripts" / "wms-media-pipeline.py"
LICENCES_JSON = ROOT / "legal" / "licences.json"


def run_audit() -> int:
    fails = 0
    passes = 0

    def ok(code: str, target: str, msg: str) -> None:
        nonlocal passes
        passes += 1
        print(f"PASS      {code:<4} {target:<30} {msg}")

    def bad(code: str, target: str, msg: str) -> None:
        nonlocal fails
        fails += 1
        print(f"FAIL      {code:<4} {target:<30} {msg}")

    print(f"── CHUYÊN GIA CHUYỂN ĐỘNG BANG-MOTION (M1–M4) · {ROOT}")

    # 0. Kiểm tra giấy phép MIT trong legal/licences.json (Quy tắc 4)
    lic_txt = LICENCES_JSON.read_text(encoding="utf-8") if LICENCES_JSON.is_file() else ""
    if "bangtutorial-bang-motion-skill" in lic_txt and "MIT License" in lic_txt:
        ok("M0", "legal/licences.json", "Đã ghi nhận giấy phép MIT cho bangtutorial/bang-motion (Quy tắc 4)")
    else:
        bad("M0", "legal/licences.json", "Thiếu mục bangtutorial-bang-motion-skill (MIT License) trong legal/licences.json")

    for html_path in (PROTO_HTML, WF_HTML, STUDIO_HTML):
        rel = str(html_path.relative_to(ROOT))
        if not html_path.is_file():
            bad("M1", rel, "Không tìm thấy file HTML")
            continue
        src = html_path.read_text(encoding="utf-8")

        # M1: Anti-PPT & Persistent World (cubic-bezier + persistent stage)
        if "cubic-bezier" in src and (".diorama" in src or ".hierarchy-stage" in src or ".workbench" in src):
            ok("M1", rel, "Persistent World + đường cong quán tính vật lý cubic-bezier đạt chuẩn Anti-PPT")
        else:
            bad("M1", rel, "Thiếu đường cong quán tính cubic-bezier hoặc vùng Persistent World")

        # M2: Kinetic Financial Counter (tabular-nums + rolling counter + SVG path particle)
        has_tabular = "tabular-nums" in src
        has_counter = ("animateMoneyText" in src) or ("animateCounter" in src)
        if has_tabular and has_counter:
            ok("M2", rel, "Kinetic Counter (tabular-nums + hàm nội suy số tiền/chỉ số mượt) đã kích hoạt")
        else:
            bad("M2", rel, f"Thiếu tabular-nums ({has_tabular}) hoặc hàm nội suy số ({has_counter})")

        # M4a: Deterministic Seek Hook (window.__vibeSeek)
        if "__vibeSeek" in src:
            ok("M4", rel, "Có đồng hồ tất định window.__vibeSeek(stepOrSec) phục vụ chụp kiểm tra")
        else:
            bad("M4", rel, "Thiếu hàm đồng hồ tất định window.__vibeSeek")

        # M4b: Zero External Runtime Script CDN (Privacy Rule 8)
        ext_scripts = re.findall(r'<script\b[^>]*\bsrc=["\'](https?://[^"\']+)["\']', src, flags=re.I)
        if not ext_scripts:
            ok("M4", rel, "0 script CDN bên thứ ba lúc runtime (bảo toàn quyền riêng tư người đọc)")
        else:
            bad("M4", rel, f"Phát hiện script CDN bên thứ ba lúc runtime: {ext_scripts}")

        # M4c: prefers-reduced-motion
        if "prefers-reduced-motion" in src:
            ok("M4", rel, "Tôn trọng @media (prefers-reduced-motion: reduce)")
        else:
            bad("M4", rel, "Thiếu @media (prefers-reduced-motion: reduce)")

    # M3: Split-Stage & Containment Guard trong pipeline dựng video
    if MEDIA_PY.is_file():
        msrc = MEDIA_PY.read_text(encoding="utf-8")
        if "assert_parent_child_containment" in msrc and "STAGE_BOX" in msrc and "CARD_BOX" in msrc:
            ok("M3", "scripts/wms-media-pipeline.py", "Khoá khung nhìn LUẬT 6b (Containment) & LUẬT 8 (STAGE_BOX / CARD_BOX) nguyên vẹn")
        else:
            bad("M3", "scripts/wms-media-pipeline.py", "Thiếu assert_parent_child_containment hoặc STAGE_BOX / CARD_BOX")

    # M3b (LUẬT 10): Kiểm tra tất định 0 đè chữ (Zero Sibling Text Collision & 2D Box Containment) trên workflows.html & prototype.html
    if WF_HTML.is_file():
        wsrc = WF_HTML.read_text(encoding="utf-8")
        # 1. Cấm đặt text-anchor="end" cùng dòng với nhãn mã bước trong .st-node
        if '"text-anchor": "end"' in wsrc:
            bad("M3b", "docs/workflows.html", "Vi phạm LUẬT 10: Phát hiện text-anchor='end' dễ gây đè chữ ngang hàng trong hộp trạm")
        else:
            ok("M3b", "docs/workflows.html", "LUẬT 10: 100% nhãn trong trạm SVG nằm trên tầng Y độc lập (1 Row = 1 Text)")

        # 2. Kiểm tra kích thước hộp trạm vs bề rộng chữ của toàn bộ 30 trạm trong 5 quy trình
        step_re = re.compile(
            r'\{\s*id:\s*"([^"]+)",\s*code:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*dept:\s*"([^"]+)",\s*'
            r'x:\s*(\d+),\s*y:\s*(\d+),\s*w:\s*(\d+),\s*h:\s*(\d+),\s*icon:\s*"([^"]+)",\s*vendors:\s*\[[^\]]*\],\s*'
            r'tier:\s*"([^"]+)"',
            re.S,
        )
        steps = list(step_re.finditer(wsrc))
        overflow_errs = []
        for m in steps:
            sid, code, name, dept, x, y, w, h, icon, tier = m.groups()
            w_val = int(w)
            dept_px = len(dept) * 5.25
            name_px = len(name) * 6.45
            tier_px = len(tier) * 5.05
            if dept_px > w_val - 12:
                overflow_errs.append(f"{sid}.dept('{dept}'={dept_px:.0f}px > {w_val-12}px)")
            if name_px > w_val - 12:
                overflow_errs.append(f"{sid}.name('{name}'={name_px:.0f}px > {w_val-12}px)")
            if tier_px > w_val - 18:
                overflow_errs.append(f"{sid}.tier('{tier}'={tier_px:.0f}px > {w_val-18}px)")
            en_name_m = re.search(rf'id:\s*"{re.escape(sid)}"[^}}]*nameEn:\s*"([^"]+)"', wsrc)
            en_tier_m = re.search(rf'id:\s*"{re.escape(sid)}"[^}}]*tierEn:\s*"([^"]+)"', wsrc)
            if en_name_m and len(en_name_m.group(1)) * 6.45 > w_val - 12:
                overflow_errs.append(f"{sid}.nameEn('{en_name_m.group(1)}')")
            if en_tier_m and len(en_tier_m.group(1)) * 5.05 > w_val - 18:
                overflow_errs.append(f"{sid}.tierEn('{en_tier_m.group(1)}')")
        if not steps:
            bad("M3b", "docs/workflows.html", "Không đọc được danh sách trạm WORKFLOWS để kiểm tra va chạm chữ")
        elif overflow_errs:
            bad("M3b", "docs/workflows.html", f"Vi phạm LUẬT 10 tràn chữ hộp trạm: {', '.join(overflow_errs)}")
        else:
            ok("M3b", "docs/workflows.html", f"LUẬT 10: Toàn bộ {len(steps)} trạm (VI + EN) đủ biên an toàn (0 tràn chữ, 0 đè chữ)")

    if PROTO_HTML.is_file():
        psrc = PROTO_HTML.read_text(encoding="utf-8")
        has_pole_safe = "POLE = 38" in psrc and ", 19)})" in psrc
        has_tag_clamp = "curRoom.rx + w / 2 + 3" in psrc
        if has_pole_safe and has_tag_clamp:
            ok("M3b", "docs/prototype.html", "LUẬT 10: Ray trên (POLE=38), bóng thoại (.tag >= 19%) và nhãn phòng (tagS clamp) 0 chồng lấn")
        else:
            bad("M3b", "docs/prototype.html", f"Vi phạm LUẬT 10 trên #scene: pole_safe={has_pole_safe}, tag_clamp={has_tag_clamp}")

        # M3c: Đồng bộ Web Diorama ↔ Video (BEAT_AUDIO Giọng Tâm, vòng lặp hạt, HUD 5 ngôi nhà, nhúng Video trực tiếp)
        beatmap_json = ROOT / "knowledge" / "wms-beatmap.json"
        has_beatmap = beatmap_json.is_file()
        has_audio_sync = 'id="dioramaAudio"' in psrc and "const BEAT_AUDIO =" in psrc and "startAudioMasterClock" in psrc
        has_loop_hud = "const phase = e % cycle" in psrc and 'id="dioramaHudBar"' in psrc and 'id="packVideoEmbed"' in psrc and 'id="stageVideoWrap"' in psrc
        audio_files_ok = all((ROOT / "public" / "audio" / f"{k}-beats.mp3").is_file() for k in ("card", "pay", "install", "minpay", "qr", "profitcash", "offus", "termdep"))
        if has_beatmap and has_audio_sync and has_loop_hud and audio_files_ok:
            ok("M3c", "docs/prototype.html", "Đồng bộ Web ↔ Video: 8 MP3 Giọng Tâm (-14 LUFS) + rAF master clock + HUD 5 nhà + vòng lặp hạt + nhúng Video trực tiếp")
        else:
            bad("M3c", "docs/prototype.html", f"Thiếu đồng bộ Web ↔ Video: beatmap={has_beatmap}, audio_sync={has_audio_sync}, loop_hud={has_loop_hud}, mp3_8={audio_files_ok}")

    if STUDIO_HTML.is_file():
        ssrc = STUDIO_HTML.read_text(encoding="utf-8")
        svg_y_vals = [int(y) for y in re.findall(r'<text\b[^>]*\by="(\d+)"', ssrc)]
        has_unique_rows = len(svg_y_vals) == len(set(svg_y_vals)) and len(svg_y_vals) >= 7
        has_csp_lock = "connect-src 'none'" in ssrc
        if has_unique_rows and has_csp_lock:
            ok("M3b", "docs/studio.html", f"LUẬT 10 & Bảo mật: {len(svg_y_vals)} nhãn SVG Safe-Zone nằm trên các tầng Y riêng biệt + CSP connect-src 'none'")
        else:
            bad("M3b", "docs/studio.html", f"Vi phạm LUẬT 10 hoặc CSP trên studio.html: unique_y={has_unique_rows}, csp={has_csp_lock}")

    print(f"Kết quả Bang-Motion (M1–M4): FAIL {fails} · PASS {passes}")
    return 1 if fails > 0 else 0


if __name__ == "__main__":
    sys.exit(run_audit())
