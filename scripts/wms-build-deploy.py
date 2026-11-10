#!/usr/bin/env python3
"""
wms-build-deploy.py — Đóng gói bản phát hành tĩnh `dist/site/` cho Cloudflare Workers Static Assets + `/api/p`.
Đảm bảo:
  - `dist/site/index.html` (và `dist/site/prototype.html`) lấy từ `docs/prototype.html`, chuẩn hoá đường dẫn ảnh `public/brand/`.
  - Sao chép đầy đủ 28 hình mặt cắt LUẬT 9 (`public/brand/*-fig-*.jpg`), `studio.html`, `wms-studio-data.js`, `workflows.html` và `legal/licences.json`.
  - Sinh file `dist/site/_headers` khoá bảo mật HTTP (`nosniff`, `no-referrer`, `CSP`).
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PUBLIC_BRAND = ROOT / "public" / "brand"
LEGAL = ROOT / "legal" / "licences.json"
OUT = ROOT / "dist" / "site"

LESSONS = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")


def build_site() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "public" / "brand").mkdir(parents=True, exist_ok=True)
    (OUT / "legal").mkdir(parents=True, exist_ok=True)

    # 1. Build index.html & prototype.html from docs/prototype.html
    proto_src = (DOCS / "prototype.html").read_text(encoding="utf-8")
    proto_dist = proto_src.replace('src="../public/brand/', 'src="public/brand/')
    (OUT / "index.html").write_text(proto_dist, encoding="utf-8")
    (OUT / "prototype.html").write_text(proto_dist, encoding="utf-8")

    # 2. Copy studio.html, wms-studio-data.js, workflows.html
    for name in ("studio.html", "wms-studio-data.js", "workflows.html"):
        src_file = DOCS / name
        if src_file.is_file():
            txt = src_file.read_text(encoding="utf-8").replace("../public/brand/", "public/brand/")
            (OUT / name).write_text(txt, encoding="utf-8")

    # 3. Copy all brand figures & plates
    copied_figs = 0
    for img in sorted(PUBLIC_BRAND.glob("*")):
        if img.is_file() and img.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".svg"):
            shutil.copy2(img, OUT / "public" / "brand" / img.name)
            copied_figs += 1

    # Verify all 28 LUẬT 9 figures exist in dist/site/public/brand
    for sid in LESSONS:
        for idx in (1, 2, 3, 4):
            fig = OUT / "public" / "brand" / f"{sid}-fig-{idx}.jpg"
            if not fig.is_file() or fig.stat().st_size < 10_000:
                print(f"FAIL: Thiếu hình mặt cắt LUẬT 9 trong gói deploy: {fig}", file=sys.stderr)
                return 1

    # 4. Copy legal/licences.json
    if LEGAL.is_file():
        shutil.copy2(LEGAL, OUT / "legal" / "licences.json")

    # 5. Write Cloudflare Static Assets _headers
    headers_txt = (
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: no-referrer\n"
        "  X-Frame-Options: DENY\n"
        "\n"
        "/studio.html\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'none'; frame-src https://www.youtube-nocookie.com https://www.youtube.com; object-src 'none'; base-uri 'none'\n"
    )
    (OUT / "_headers").write_text(headers_txt, encoding="utf-8")

    total_bytes = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(
        f"[wms-build-deploy PASS] Đã đóng gói dist/site/ ({total_bytes / (1024 * 1024):.2f} MB · "
        f"{copied_figs} ảnh public/brand · 7 bài học · index.html + studio.html + workflows.html + _headers)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(build_site())
