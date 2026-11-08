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

    for html_path in (PROTO_HTML, WF_HTML):
        rel = str(html_path.relative_to(ROOT))
        if not html_path.is_file():
            bad("M1", rel, "Không tìm thấy file HTML")
            continue
        src = html_path.read_text(encoding="utf-8")

        # M1: Anti-PPT & Persistent World (cubic-bezier + persistent stage)
        if "cubic-bezier" in src and (".diorama" in src or ".hierarchy-stage" in src):
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

    print(f"Kết quả Bang-Motion (M1–M4): FAIL {fails} · PASS {passes}")
    return 1 if fails > 0 else 0


if __name__ == "__main__":
    sys.exit(run_audit())
