#!/usr/bin/env python3
"""
wms-build-deploy.py — Đóng gói bản phát hành tĩnh `dist/site/` cho Cloudflare Workers Static Assets + `/api/p`.
Đảm bảo:
  - `dist/site/index.html` (và `dist/site/prototype.html`) lấy từ `docs/prototype.html`, chuẩn hoá đường dẫn ảnh `public/brand/`.
  - Sao chép đầy đủ 28 hình mặt cắt LUẬT 9 (`public/brand/*-fig-*.jpg`), 7 file âm thanh `public/audio/*-beats.mp3`,
    `studio.html`, `wms-studio-data.js`, `workflows.html`, các trang cổng `s0.html..s6.html`, `assets/doc.{css,js}`,
    `favicon.svg` + `favicon.ico` và `legal/licences.json`.
  - Sinh file `dist/site/_headers` khoá bảo mật HTTP (`nosniff`, `no-referrer`, `CSP` chặn 100% script bên thứ ba).
"""

import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PUBLIC_BRAND = ROOT / "public" / "brand"
PUBLIC_AUDIO = ROOT / "public" / "audio"
LEGAL_DIR = ROOT / "legal"
GATES_DIR = ROOT / "gates"
YT_DIR = ROOT / "dist" / "youtube"
OUT = ROOT / "dist" / "site"

LESSONS = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")


def _rewrite_doc_refs(text: str) -> str:
    return (
        text.replace("../public/brand/", "public/brand/")
        .replace("../public/audio/", "public/audio/")
        .replace("../gates/", "gates/")
        .replace("../dist/youtube/", "dist/youtube/")
        .replace("../legal/", "legal/")
        .replace('<a href="index.html">S0 Discovery</a>', '<a href="s0.html">S0 Discovery</a>')
    )


def _write_favicons(out_dir: Path) -> None:
    svg_txt = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="14" fill="#0d1320"/>'
        '<circle cx="32" cy="32" r="21" fill="none" stroke="#f5a524" stroke-width="3.5"/>'
        '<path d="M23 24h18M23 32h18M23 40h12" stroke="#f5f1e8" stroke-width="3.5" stroke-linecap="round"/>'
        '<circle cx="41" cy="40" r="3" fill="#10b981"/>'
        "</svg>\n"
    )
    (out_dir / "favicon.svg").write_text(svg_txt, encoding="utf-8")

    # Minimal valid 16x16 32-bit BGRA ICO in pure Python (0 external dependencies in CI)
    w, h = 16, 16
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            dx, dy = x - 7.5, y - 7.5
            r2 = dx * dx + dy * dy
            if 28 <= r2 <= 46:
                pixels.extend((36, 165, 245, 255))  # Gold ring (#f5a524 in BGRA)
            elif r2 < 28:
                pixels.extend((32, 19, 13, 255))    # Archival navy (#0d1320 in BGRA)
            else:
                pixels.extend((0, 0, 0, 0))
    and_mask = bytes(4 * h)
    bmp_header = struct.pack("<IIIHHIIIIII", 40, w, h * 2, 1, 32, 0, len(pixels) + len(and_mask), 0, 0, 0, 0)
    ico_data = bmp_header + bytes(pixels) + and_mask
    ico_dir = struct.pack("<HHHBBBBHHII", 0, 1, 1, w, h, 0, 0, 1, 32, len(ico_data), 22)
    (out_dir / "favicon.ico").write_bytes(ico_dir + ico_data)


def build_site() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "public" / "brand").mkdir(parents=True, exist_ok=True)
    (OUT / "public" / "audio").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "legal").mkdir(parents=True, exist_ok=True)
    (OUT / "gates").mkdir(parents=True, exist_ok=True)
    (OUT / "dist" / "youtube").mkdir(parents=True, exist_ok=True)

    # 1. Build index.html & prototype.html from docs/prototype.html
    proto_src = (DOCS / "prototype.html").read_text(encoding="utf-8")
    proto_dist = _rewrite_doc_refs(proto_src)
    (OUT / "index.html").write_text(proto_dist, encoding="utf-8")
    (OUT / "prototype.html").write_text(proto_dist, encoding="utf-8")

    # 2. Dynamically copy ALL docs/*.html & docs/*.js (plus docs/index.html -> s0.html)
    copied_docs = 2
    for src_file in sorted(DOCS.glob("*.html")):
        if src_file.name in ("prototype.html", "index.html"):
            continue
        txt = _rewrite_doc_refs(src_file.read_text(encoding="utf-8"))
        (OUT / src_file.name).write_text(txt, encoding="utf-8")
        copied_docs += 1

    for src_js in sorted(DOCS.glob("*.js")):
        txt = _rewrite_doc_refs(src_js.read_text(encoding="utf-8"))
        (OUT / src_js.name).write_text(txt, encoding="utf-8")
        copied_docs += 1

    if (DOCS / "index.html").is_file():
        s0_txt = _rewrite_doc_refs((DOCS / "index.html").read_text(encoding="utf-8"))
        (OUT / "s0.html").write_text(s0_txt, encoding="utf-8")
        copied_docs += 1

    if (DOCS / "assets").is_dir():
        for asset in sorted((DOCS / "assets").glob("*")):
            if asset.is_file():
                shutil.copy2(asset, OUT / "assets" / asset.name)

    _write_favicons(OUT)

    # 3. Copy all brand figures & plates
    copied_figs = 0
    for img in sorted(PUBLIC_BRAND.glob("*")):
        if img.is_file() and img.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".svg"):
            shutil.copy2(img, OUT / "public" / "brand" / img.name)
            copied_figs += 1

    # 3b. Copy all ElevenLabs studio beat audio files & manifest
    copied_audio = 0
    if PUBLIC_AUDIO.is_dir():
        for aud in sorted(PUBLIC_AUDIO.glob("*")):
            if aud.is_file() and aud.suffix.lower() in (".mp3", ".json"):
                shutil.copy2(aud, OUT / "public" / "audio" / aud.name)
                copied_audio += 1

    # Verify all 28 LUẬT 9 figures & 7 ElevenLabs beat MP3s exist in dist/site/public/
    for sid in LESSONS:
        for idx in (1, 2, 3, 4):
            fig = OUT / "public" / "brand" / f"{sid}-fig-{idx}.jpg"
            if not fig.is_file() or fig.stat().st_size < 10_000:
                print(f"FAIL: Thiếu hình mặt cắt LUẬT 9 trong gói deploy: {fig}", file=sys.stderr)
                return 1
        mp3 = OUT / "public" / "audio" / f"{sid}-beats.mp3"
        if not mp3.is_file() or mp3.stat().st_size < 50_000:
            print(f"FAIL: Thiếu file âm thanh Giọng Tâm ElevenLabs trong gói deploy: {mp3}", file=sys.stderr)
            return 1

    # 4. Copy all legal documents (licences.json, tt99-phu-luc-ii.secondary.json, VanBanGoc PDF)
    copied_legal = 0
    if LEGAL_DIR.is_dir():
        for lf in sorted(LEGAL_DIR.iterdir()):
            if lf.is_file() and not lf.name.startswith("."):
                shutil.copy2(lf, OUT / "legal" / lf.name)
                copied_legal += 1

    # 4b. Copy gate markdown records (gates/**/*.md) so references from docs/s6.html etc. resolve live
    copied_gates = 0
    if GATES_DIR.is_dir():
        for gf in sorted(GATES_DIR.rglob("*.md")):
            if gf.is_file():
                rel = gf.relative_to(GATES_DIR)
                dest = OUT / "gates" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                gate_txt = gf.read_text(encoding="utf-8").replace("../../../", "../../../../../")
                dest.write_text(gate_txt, encoding="utf-8")
                copied_gates += 1

    # 4c. Copy subtitle (.srt) & manifest files from dist/youtube/ (excluding bulky video/audio binaries)
    copied_yt = 0
    if YT_DIR.is_dir():
        for yf in sorted(YT_DIR.iterdir()):
            if yf.is_file() and (yf.suffix.lower() == ".srt" or yf.name.endswith("-manifest.json")):
                shutil.copy2(yf, OUT / "dist" / "youtube" / yf.name)
                copied_yt += 1

    # Verify required pages & core resources exist in bundle
    required_paths = (
        "index.html",
        "prototype.html",
        "workflows.html",
        "studio.html",
        "wms-studio-data.js",
        "duyslab-overview.html",
        "landing-detail-mockups.html",
        "mockup-option-a.html",
        "mockup-option-b.html",
        "llm-quiz.html",
        "studio-mockups.html",
        "s0.html",
        "s1.html",
        "s2.html",
        "s3.html",
        "s4.html",
        "s5.html",
        "s6.html",
        "legal/licences.json",
        "legal/tt99-phu-luc-ii.secondary.json",
        "gates/06-iterate/TRIAGE.md",
        "gates/06-iterate/READOUT.md",
        "dist/youtube/card-long-16x9.srt",
        "public/audio/beats-manifest.json",
    )
    for rel_req in required_paths:
        req_file = OUT / rel_req
        if not req_file.is_file() or req_file.stat().st_size == 0:
            print(f"FAIL: Thiếu tài nguyên bắt buộc trong gói deploy: {req_file}", file=sys.stderr)
            return 1

    # 5. Write Cloudflare Static Assets _headers (enforce AC-33/AC-36 zero 3rd-party scripts across all pages)
    headers_txt = (
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: DENY\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data: blob: https://i.ytimg.com; media-src 'self' blob:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-src https://www.youtube-nocookie.com https://www.youtube.com; object-src 'none'; base-uri 'none'\n"
        "\n"
        "/public/audio/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "\n"
        "/studio.html\n"
        "  Referrer-Policy: no-referrer\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; script-src 'self' 'unsafe-inline'; connect-src 'none'; frame-src https://www.youtube-nocookie.com https://www.youtube.com; object-src 'none'; base-uri 'none'\n"
    )
    (OUT / "_headers").write_text(headers_txt, encoding="utf-8")

    total_bytes = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(
        f"[wms-build-deploy PASS] Đã đóng gói dist/site/ ({total_bytes / (1024 * 1024):.2f} MB · "
        f"{copied_docs} trang/JS · {copied_figs} ảnh public/brand · {copied_audio} audio · "
        f"{copied_legal} legal · {copied_gates} gates .md · {copied_yt} yt .srt/manifest · 7 bài học)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(build_site())
