#!/usr/bin/env python3
"""
wms-sync-fonts.py — Đóng gói self-hosted web fonts (SIL OFL 1.1) & ảnh mặt cắt WebP/AVIF.
Loại bỏ kết nối ngoài tới fonts.googleapis.com / fonts.gstatic.com.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import sys
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT / "public" / "fonts"
BRAND_DIR = ROOT / "public" / "brand"
DEFAULT_LESSONS = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")


def load_lessons() -> tuple[str, ...]:
    proto = ROOT / "docs" / "prototype.html"
    if not proto.is_file():
        return DEFAULT_LESSONS
    spec = importlib.util.spec_from_file_location("check_story_mod", ROOT / "scripts" / "check-story.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    stories = mod.extract(proto.read_text(encoding="utf-8"), "STORIES")
    return tuple(stories.keys()) or DEFAULT_LESSONS

CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
FONT_CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Be+Vietnam+Pro:wght@400;500;600;700;800"
    "&family=Fraunces:opsz,wght@9..144,400..700"
    "&family=JetBrains+Mono:wght@400..700"
    "&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600"
    "&display=swap"
)
ALLOWED_SUBSETS = {"vietnamese", "latin-ext", "latin"}


def _slug_name(family: str, style: str, weight: str, subset: str, url: str) -> str:
    fam = re.sub(r"[^a-z0-9]+", "", family.lower())
    w = re.sub(r"[^0-9]+", "-", weight.strip()).strip("-") or "400"
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
    return f"{fam}-{style}-{w}-{subset}-{h}.woff2"


def sync_fonts() -> tuple[list[str], dict[str, str]]:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(FONT_CSS_URL, headers={"User-Agent": CHROME_UA})
    raw_css = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")

    block_re = re.compile(r"/\*\s*([a-z0-9-]+)\s*\*/\s*@font-face\s*\{([^}]+)\}", re.S)
    css_parts = [
        "/* Self-hosted SIL OFL 1.1 Web Fonts (Be Vietnam Pro, Newsreader, Fraunces, JetBrains Mono) */"
    ]
    kept_files: set[str] = set()
    preloads: dict[str, str] = {}

    for subset, body in block_re.findall(raw_css):
        if subset not in ALLOWED_SUBSETS:
            continue
        fam_m = re.search(r"font-family:\s*'([^']+)'", body)
        sty_m = re.search(r"font-style:\s*([a-z]+)", body)
        wgt_m = re.search(r"font-weight:\s*([^;]+)", body)
        url_m = re.search(r"src:\s*url\((https://[^)]+\.woff2)\)", body)
        if not (fam_m and url_m):
            continue
        fam = fam_m.group(1)
        style = sty_m.group(1) if sty_m else "normal"
        weight = wgt_m.group(1).strip() if wgt_m else "400"
        remote_url = url_m.group(1)
        fname = _slug_name(fam, style, weight, subset, remote_url)
        dest = FONTS_DIR / fname
        if not dest.is_file() or dest.stat().st_size == 0:
            data = urllib.request.urlopen(
                urllib.request.Request(remote_url, headers={"User-Agent": CHROME_UA}), timeout=20
            ).read()
            dest.write_bytes(data)
        kept_files.add(fname)

        if fam == "Be Vietnam Pro" and subset == "vietnamese" and weight == "400":
            preloads["be_vietnam_pro_400_vi"] = fname
        if fam == "Newsreader" and subset == "vietnamese" and style == "normal":
            preloads["newsreader_vi"] = fname

        local_body = body.replace(remote_url, f"./{fname}")
        css_parts.append(f"/* {subset} */\n@font-face {{{local_body}}}")

    for old in FONTS_DIR.glob("*.woff2"):
        if old.name not in kept_files:
            old.unlink()

    (FONTS_DIR / "wms-fonts.css").write_text("\n".join(css_parts) + "\n", encoding="utf-8")
    return sorted(kept_files), preloads


def sync_editorial_formats(lessons: tuple[str, ...] | None = None) -> tuple[int, int, int, tuple[str, ...]]:
    active = lessons if lessons is not None else load_lessons()
    jpg_bytes = webp_bytes = avif_bytes = 0
    count = 0
    for sid in active:
        for idx in (1, 2, 3, 4):
            jpg = BRAND_DIR / f"{sid}-fig-{idx}.jpg"
            if not jpg.is_file():
                raise FileNotFoundError(f"Missing figure JPG: {jpg}")
            jpg_bytes += jpg.stat().st_size
            webp = BRAND_DIR / f"{sid}-fig-{idx}.webp"
            avif = BRAND_DIR / f"{sid}-fig-{idx}.avif"
            with Image.open(jpg) as im:
                rgb = im.convert("RGB")
                if not webp.is_file() or webp.stat().st_mtime < jpg.stat().st_mtime:
                    rgb.save(webp, format="WEBP", quality=82, method=6)
                if not avif.is_file() or avif.stat().st_mtime < jpg.stat().st_mtime:
                    rgb.save(avif, format="AVIF", quality=68)
            webp_bytes += webp.stat().st_size
            avif_bytes += avif.stat().st_size
            count += 1
    return count, jpg_bytes, webp_bytes + avif_bytes, active


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts-only", action="store_true")
    ap.add_argument("--images-only", action="store_true")
    args = ap.parse_args()

    if not args.images_only:
        files, preloads = sync_fonts()
        total_kb = sum((FONTS_DIR / f).stat().st_size for f in files) / 1024
        print(f"[fonts] {len(files)} .woff2 files ({total_kb:.1f} KB); preloads={preloads}")
    if not args.fonts_only:
        cnt, jpg_b, next_b, active = sync_editorial_formats()
        webp_b = sum((BRAND_DIR / f"{s}-fig-{i}.webp").stat().st_size for s in active for i in (1, 2, 3, 4))
        avif_b = sum((BRAND_DIR / f"{s}-fig-{i}.avif").stat().st_size for s in active for i in (1, 2, 3, 4))
        print(
            f"[images] {cnt} figures: JPG={jpg_b/1024/1024:.2f} MB · "
            f"WebP={webp_b/1024/1024:.2f} MB · AVIF={avif_b/1024/1024:.2f} MB"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
