#!/usr/bin/env python3
"""
wms-build-deploy.py — Đóng gói bản phát hành tĩnh `dist/site/` cho Cloudflare Workers Static Assets + `/api/p`.
Đảm bảo:
  - Tách nội dung chi tiết (`article` & `videoScript` đầy đủ) sang `dist/site/data/stories/<slug>.json`
    và thay `STORIES`/`STORIES_EN` trong HTML phát hành bằng bản khung nhẹ giữ nguyên từ khoá tìm sâu.
  - Sao chép self-hosted fonts `public/fonts/`, `public/manifest.webmanifest`, 84 ảnh mặt cắt `.jpg/.webp/.avif`,
    7 file audio `public/audio/*-beats.mp3`, các trang Studio/Workflows/cổng S0–S6 và `legal/licences.json`.
  - Sinh `robots.txt`, `sitemap.xml`, `feed.xml` (VI), `feed-en.xml` (EN), `sw.js` (PWA offline) và `_headers`.
"""

import html as _html
import importlib.util
import json
import re
import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PUBLIC_BRAND = ROOT / "public" / "brand"
PUBLIC_AUDIO = ROOT / "public" / "audio"
PUBLIC_FONTS = ROOT / "public" / "fonts"
MANIFEST_SRC = ROOT / "public" / "manifest.webmanifest"
LEGAL_DIR = ROOT / "legal"
GATES_DIR = ROOT / "gates"
YT_DIR = ROOT / "dist" / "youtube"
OUT = ROOT / "dist" / "site"

LESSONS = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")
SITE_ORIGIN = "https://wheremoneysleeps.duyslab.icu"
TERM_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def _load_js_literal_cls():
    spec = importlib.util.spec_from_file_location("check_story_mod", ROOT / "scripts" / "check-story.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.JSLiteral


def _rewrite_doc_refs(text: str) -> str:
    return (
        text.replace("../public/brand/", "public/brand/")
        .replace("../public/audio/", "public/audio/")
        .replace("../public/fonts/", "public/fonts/")
        .replace("../public/manifest.webmanifest", "public/manifest.webmanifest")
        .replace("../gates/", "gates/")
        .replace("../dist/youtube/", "dist/youtube/")
        .replace("../legal/", "legal/")
        .replace('<a href="index.html">S0 Discovery</a>', '<a href="s0.html">S0 Discovery</a>')
    )


def _walk_strings(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        out: list[str] = []
        for item in obj:
            out.extend(_walk_strings(item))
        return out
    if isinstance(obj, dict):
        out = []
        for val in obj.values():
            out.extend(_walk_strings(val))
        return out
    return []


def _extract_stub(slug: str, story: dict) -> dict:
    article = story.get("article") or {}
    lay = article.get("lay") or {}
    pro = article.get("pro") or {}
    sections = lay.get("sections") or []
    lay_words = sum(len(" ".join(sec.get("paras") or []).split()) for sec in sections)

    raw_texts = _walk_strings(story.get("beats") or []) + _walk_strings(article)
    terms: set[str] = set()
    for txt in raw_texts:
        for m in TERM_RE.finditer(txt):
            key = (m.group(2) or m.group(1) or "").strip().lower()
            if key:
                terms.add(key)

    accts: set[str] = set()
    acct_names: set[str] = set()
    for b in story.get("beats") or []:
        led = b.get("ledger") or {}
        for row in led.get("rows") or []:
            if len(row) > 1 and row[1]:
                accts.add(str(row[1]).strip())
            if len(row) > 2 and row[2]:
                acct_names.add(str(row[2]).strip())
    for jr in pro.get("journal") or []:
        for row in jr.get("rows") or []:
            if len(row) > 1 and row[1]:
                accts.add(str(row[1]).strip())
            if len(row) > 2 and row[2]:
                acct_names.add(str(row[2]).strip())

    vid = story.get("videoScript") or {}
    vid_stub = {}
    for fmt in ("long", "short"):
        fobj = vid.get(fmt) or {}
        vid_stub[fmt] = {
            "title": fobj.get("title", ""),
            "youtubeId": fobj.get("youtubeId", ""),
            "embedStatus": fobj.get("embedStatus", "pending_upload"),
            "elevenlabsVoiceId": fobj.get("elevenlabsVoiceId", ""),
            **({"angle": fobj["angle"]} if "angle" in fobj else {}),
            **({"hookNote": fobj["hookNote"]} if "hookNote" in fobj else {}),
            "scenes": [
                {
                    "time": sc.get("time", ""),
                    "beat": sc.get("beat"),
                    **({"chapter": sc["chapter"]} if sc.get("chapter") else {}),
                }
                for sc in (fobj.get("scenes") or [])
            ],
        }

    search_bits: list[str] = []
    for sec in sections:
        if sec.get("h"):
            search_bits.append(str(sec["h"]))
    for mech in pro.get("mechanics") or []:
        if mech.get("h"):
            search_bits.append(str(mech["h"]))
    for jr in pro.get("journal") or []:
        if jr.get("book"):
            search_bits.append(str(jr["book"]))
    for acc in sorted(accts):
        search_bits.append(f"TK {acc} Account {acc} {acc}")
    for nm in sorted(acct_names):
        search_bits.append(nm)

    stub = {
        "name": story.get("name", ""),
        "title": story.get("title", ""),
        "teaser": story.get("teaser", ""),
        "category": story.get("category") or story.get("cat") or "",
        "status": story.get("status", "draft"),
        "approvedBy": story.get("approvedBy", ""),
        "approvedAt": story.get("approvedAt", ""),
        "houses": story.get("houses") or [],
        "beats": story.get("beats") or [],
        "videoScript": vid_stub,
        "_splitPack": True,
        "_layWords": lay_words,
        "_secCount": len(sections) or 5,
        "_terms": sorted(terms),
        "_accts": sorted(accts),
        "_acctNames": sorted(acct_names),
        "_q": " ".join(search_bits),
    }
    if "review" in story:
        stub["review"] = story["review"]
    return stub


def _safe_inline_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _split_stories_for_dist(proto_dist: str, out_dir: Path) -> tuple[str, dict, dict]:
    JSLiteral = _load_js_literal_cls()
    data_dir = out_dir / "data" / "stories"
    data_dir.mkdir(parents=True, exist_ok=True)

    spans = {}
    parsed = {}
    for var_name in ("STORIES", "STORIES_EN"):
        m = re.search(rf"\bconst\s+{var_name}\s*=\s*", proto_dist)
        if not m:
            raise ValueError(f"Không tìm thấy const {var_name} = trong HTML build")
        parser = JSLiteral(proto_dist, m.end())
        val = parser.value()
        parsed[var_name] = val
        spans[var_name] = (m.end(), parser.i)

    vi_stories = parsed["STORIES"]
    en_stories = parsed["STORIES_EN"]
    vi_stubs = {}
    en_stubs = {}
    for slug in vi_stories:
        v_obj = vi_stories[slug]
        e_obj = en_stories.get(slug) or {}
        pack = {
            "vi": {"article": v_obj.get("article"), "videoScript": v_obj.get("videoScript")},
            "en": {"article": e_obj.get("article"), "videoScript": e_obj.get("videoScript")},
        }
        (data_dir / f"{slug}.json").write_text(
            json.dumps(pack, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
        )
        vi_stubs[slug] = _extract_stub(slug, v_obj)
        if slug in en_stories:
            en_stubs[slug] = _extract_stub(slug, e_obj)

    # Replace spans from right to left so offsets stay valid
    out_html = proto_dist
    rep_pairs = [
        (spans["STORIES"][0], spans["STORIES"][1], _safe_inline_json(vi_stubs)),
        (spans["STORIES_EN"][0], spans["STORIES_EN"][1], _safe_inline_json(en_stubs)),
    ]
    for s_idx, e_idx, replacement in sorted(rep_pairs, key=lambda x: x[0], reverse=True):
        out_html = out_html[:s_idx] + replacement + out_html[e_idx:]
    return out_html, vi_stories, en_stories


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

    w, h = 16, 16
    pixels = bytearray()
    for y in range(h):
        for x in range(w):
            dx, dy = x - 7.5, y - 7.5
            r2 = dx * dx + dy * dy
            if 28 <= r2 <= 46:
                pixels.extend((36, 165, 245, 255))
            elif r2 < 28:
                pixels.extend((32, 19, 13, 255))
            else:
                pixels.extend((0, 0, 0, 0))
    and_mask = bytes(4 * h)
    bmp_header = struct.pack("<IIIHHIIIIII", 40, w, h * 2, 1, 32, 0, len(pixels) + len(and_mask), 0, 0, 0, 0)
    ico_data = bmp_header + bytes(pixels) + and_mask
    ico_dir = struct.pack("<HHHBBBBHHII", 0, 1, 1, w, h, 0, 0, 1, 32, len(ico_data), 22)
    (out_dir / "favicon.ico").write_bytes(ico_dir + ico_data)


def _write_seo_files(out_dir: Path) -> None:
    robots_txt = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /studio\n"
        "Disallow: /studio.html\n"
        "Disallow: /wms-studio-data.js\n"
        "Disallow: /studio-mockups.html\n"
        "Disallow: /landing-detail-mockups.html\n"
        "Disallow: /mockup-\n"
        "Disallow: /gates/\n\n"
        f"Sitemap: {SITE_ORIGIN}/sitemap.xml\n"
    )
    (out_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")

    url_blocks = []
    home_alts = (
        f'    <xhtml:link rel="alternate" hreflang="vi" href="{SITE_ORIGIN}/"/>\n'
        f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_ORIGIN}/?lang=en"/>\n'
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_ORIGIN}/"/>'
    )
    for loc in (f"{SITE_ORIGIN}/", f"{SITE_ORIGIN}/?lang=en"):
        url_blocks.append(f"  <url>\n    <loc>{loc}</loc>\n{home_alts}\n    <priority>1.0</priority>\n  </url>")
    for sid in LESSONS:
        alts = (
            f'    <xhtml:link rel="alternate" hreflang="vi" href="{SITE_ORIGIN}/?story={sid}&amp;lang=vi"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_ORIGIN}/?story={sid}&amp;lang=en"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_ORIGIN}/?story={sid}"/>'
        )
        for lang in ("vi", "en"):
            url_blocks.append(
                f"  <url>\n    <loc>{SITE_ORIGIN}/?story={sid}&amp;lang={lang}</loc>\n{alts}\n    <priority>0.8</priority>\n  </url>"
            )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(url_blocks)
        + "\n</urlset>\n"
    )
    (out_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")


def _write_atom_feeds(out_dir: Path, vi_stories: dict, en_stories: dict) -> None:
    for lang, catalog, fname, feed_title, subtitle in (
        (
            "vi",
            vi_stories,
            "feed.xml",
            "Where Money Sleeps — Đường đi thật của dòng tiền (VI)",
            "Giải phẫu giao dịch hằng ngày qua 5 ngôi nhà và bút toán kép Thông tư 99/2025/TT-BTC.",
        ),
        (
            "en",
            en_stories,
            "feed-en.xml",
            "Where Money Sleeps — Where Your Money Actually Goes (EN)",
            "Everyday money flows across five stops and Circular 99/2025/TT-BTC ledgers (unofficial summary).",
        ),
    ):
        dates = [str((catalog.get(s) or {}).get("approvedAt") or "2026-11-18") for s in LESSONS]
        updated = max(dates) if dates else "2026-11-18"
        entries = []
        for sid in LESSONS:
            st = catalog.get(sid) or {}
            title = _html.escape(str(st.get("title") or sid))
            teaser = str(st.get("teaser") or "")
            if lang == "en" and "unofficial summary" not in teaser.lower():
                teaser = f"{teaser} (Unofficial summary of Circular 99/2025/TT-BTC.)"
            summary = _html.escape(teaser)
            link = f"{SITE_ORIGIN}/?story={sid}&amp;lang={lang}"
            dt = str(st.get("approvedAt") or "2026-11-18")
            entries.append(
                f"  <entry>\n"
                f"    <id>{link}</id>\n"
                f"    <title>{title}</title>\n"
                f'    <link href="{link}" rel="alternate" type="text/html"/>\n'
                f"    <updated>{dt}T00:00:00Z</updated>\n"
                f"    <summary>{summary}</summary>\n"
                f"  </entry>"
            )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<feed xmlns="http://www.w3.org/2005/Atom">\n'
            f"  <id>{SITE_ORIGIN}/{fname}</id>\n"
            f"  <title>{_html.escape(feed_title)}</title>\n"
            f"  <subtitle>{_html.escape(subtitle)}</subtitle>\n"
            f'  <link href="{SITE_ORIGIN}/{fname}" rel="self" type="application/atom+xml"/>\n'
            f'  <link href="{SITE_ORIGIN}/?lang={lang}" rel="alternate" type="text/html"/>\n'
            f"  <updated>{updated}T00:00:00Z</updated>\n"
            f"  <author><name>Where Money Sleeps</name><uri>{SITE_ORIGIN}</uri></author>\n"
            + "\n".join(entries)
            + "\n</feed>\n"
        )
        (out_dir / fname).write_text(xml, encoding="utf-8")


def _write_service_worker(out_dir: Path) -> None:
    sw_js = """/* Service Worker for Where Money Sleeps — zero PII, zero tracking, offline reader cache */
const CACHE_PAGES = "wms-pages-v1";
const CACHE_DATA = "wms-data-v1";
const CACHE_STATIC = "wms-static-v1";
const MAX_STATIC_ENTRIES = 120;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_PAGES).then((cache) => cache.addAll(["/", "/public/manifest.webmanifest", "/favicon.svg"])).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  const keep = new Set([CACHE_PAGES, CACHE_DATA, CACHE_STATIC]);
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => !keep.has(k)).map((k) => caches.delete(k)))).then(() => self.clients.claim())
  );
});

async function trimCache(name, maxItems) {
  const cache = await caches.open(name);
  const keys = await cache.keys();
  while (keys.length > maxItems) {
    await cache.delete(keys.shift());
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith("/api/")) return;

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).then((resp) => {
        if (resp && resp.status === 200) {
          const copy = resp.clone();
          caches.open(CACHE_PAGES).then((c) => c.put(req, copy));
        }
        return resp;
      }).catch(async () => (await caches.match(req)) || (await caches.match("/")))
    );
    return;
  }

  if (url.pathname.startsWith("/data/stories/")) {
    event.respondWith(
      caches.open(CACHE_DATA).then(async (cache) => {
        const cached = await cache.match(req);
        const net = fetch(req).then((resp) => {
          if (resp && resp.status === 200) cache.put(req, resp.clone());
          return resp;
        }).catch(() => cached);
        return cached || net;
      })
    );
    return;
  }

  if (url.pathname.startsWith("/public/fonts/") || url.pathname.startsWith("/public/brand/") || url.pathname.startsWith("/assets/")) {
    event.respondWith(
      caches.open(CACHE_STATIC).then(async (cache) => {
        const cached = await cache.match(req);
        if (cached) return cached;
        const resp = await fetch(req);
        if (resp && resp.status === 200) {
          cache.put(req, resp.clone()).then(() => trimCache(CACHE_STATIC, MAX_STATIC_ENTRIES));
        }
        return resp;
      })
    );
  }
});
"""
    (out_dir / "sw.js").write_text(sw_js, encoding="utf-8")


def build_site() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "public" / "brand").mkdir(parents=True, exist_ok=True)
    (OUT / "public" / "audio").mkdir(parents=True, exist_ok=True)
    (OUT / "public" / "fonts").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "legal").mkdir(parents=True, exist_ok=True)
    (OUT / "gates").mkdir(parents=True, exist_ok=True)
    (OUT / "dist" / "youtube").mkdir(parents=True, exist_ok=True)

    # 1. Build split data packs + lightweight index.html & prototype.html from docs/prototype.html
    proto_src = (DOCS / "prototype.html").read_text(encoding="utf-8")
    proto_dist = _rewrite_doc_refs(proto_src)
    proto_slim, vi_stories, en_stories = _split_stories_for_dist(proto_dist, OUT)
    (OUT / "index.html").write_text(proto_slim, encoding="utf-8")
    (OUT / "prototype.html").write_text(proto_slim, encoding="utf-8")

    # 2. Copy all remaining docs/*.html, docs/*.js, assets/, self-hosted fonts & manifest
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

    copied_fonts = 0
    if PUBLIC_FONTS.is_dir():
        for ff in sorted(PUBLIC_FONTS.iterdir()):
            if ff.is_file() and ff.suffix.lower() in (".woff2", ".css"):
                shutil.copy2(ff, OUT / "public" / "fonts" / ff.name)
                copied_fonts += 1
    if MANIFEST_SRC.is_file():
        shutil.copy2(MANIFEST_SRC, OUT / "public" / "manifest.webmanifest")

    _write_favicons(OUT)
    _write_seo_files(OUT)
    _write_atom_feeds(OUT, vi_stories, en_stories)
    _write_service_worker(OUT)

    # 3. Copy web-used brand figures (.jpg + .webp + .avif) & audio MP3s
    copied_figs = 0
    for img in sorted(PUBLIC_BRAND.glob("*")):
        if not img.is_file() or img.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".avif", ".svg"):
            continue
        if "-short-plate-" in img.name or img.name.startswith(("youtube-avatar-", "youtube-banner-")):
            continue
        shutil.copy2(img, OUT / "public" / "brand" / img.name)
        copied_figs += 1

    copied_audio = 0
    if PUBLIC_AUDIO.is_dir():
        for aud in sorted(PUBLIC_AUDIO.glob("*")):
            if aud.is_file() and aud.suffix.lower() in (".mp3", ".json"):
                shutil.copy2(aud, OUT / "public" / "audio" / aud.name)
                copied_audio += 1

    for sid in LESSONS:
        for idx in (1, 2, 3, 4):
            for ext in ("jpg", "webp", "avif"):
                fig = OUT / "public" / "brand" / f"{sid}-fig-{idx}.{ext}"
                if not fig.is_file() or fig.stat().st_size < 4_000:
                    print(f"FAIL: Thiếu hình mặt cắt LUẬT 9 ({ext}) trong gói deploy: {fig}", file=sys.stderr)
                    return 1
        mp3 = OUT / "public" / "audio" / f"{sid}-beats.mp3"
        if not mp3.is_file() or mp3.stat().st_size < 50_000:
            print(f"FAIL: Thiếu file âm thanh Giọng Tâm ElevenLabs trong gói deploy: {mp3}", file=sys.stderr)
            return 1
        pack_f = OUT / "data" / "stories" / f"{sid}.json"
        if not pack_f.is_file() or pack_f.stat().st_size < 10_000:
            print(f"FAIL: Thiếu JSON tách bài học: {pack_f}", file=sys.stderr)
            return 1

    # 4. Copy public legal metadata, gates/**/*.md, subtitle .srt & manifests
    copied_legal = 0
    if LEGAL_DIR.is_dir():
        for lf in sorted(LEGAL_DIR.iterdir()):
            if lf.is_file() and not lf.name.startswith(".") and lf.name != "VanBanGoc_TT 99.2025-btc.pdf":
                shutil.copy2(lf, OUT / "legal" / lf.name)
                copied_legal += 1

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

    copied_yt = 0
    if YT_DIR.is_dir():
        for yf in sorted(YT_DIR.iterdir()):
            if yf.is_file() and (yf.suffix.lower() == ".srt" or yf.name.endswith("-manifest.json")):
                shutil.copy2(yf, OUT / "dist" / "youtube" / yf.name)
                copied_yt += 1

    required_paths = (
        "index.html", "prototype.html", "workflows.html", "studio.html", "wms-studio-data.js",
        "duyslab-overview.html", "landing-detail-mockups.html", "mockup-option-a.html", "mockup-option-b.html",
        "llm-quiz.html", "studio-mockups.html", "s0.html", "s1.html", "s2.html", "s3.html", "s4.html",
        "s5.html", "s6.html", "legal/licences.json", "legal/tt99-phu-luc-ii.secondary.json",
        "gates/06-iterate/TRIAGE.md", "gates/06-iterate/READOUT.md", "dist/youtube/card-long-16x9.srt",
        "public/audio/beats-manifest.json", "public/fonts/wms-fonts.css", "public/manifest.webmanifest",
        "robots.txt", "sitemap.xml", "feed.xml", "feed-en.xml", "sw.js",
    )
    for rel_req in required_paths:
        req_file = OUT / rel_req
        if not req_file.is_file() or req_file.stat().st_size == 0:
            print(f"FAIL: Thiếu tài nguyên bắt buộc trong gói deploy: {req_file}", file=sys.stderr)
            return 1

    # 5. Write _headers (no Google Fonts origin, immutable fonts/audio, long cache brand/assets, /studio CSP handled cleanly by Worker)
    headers_txt = (
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: DENY\n"
        "  Content-Security-Policy: default-src 'self'; img-src 'self' data: blob: https://i.ytimg.com; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; font-src 'self' data:; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-src https://www.youtube-nocookie.com https://www.youtube.com; object-src 'none'; base-uri 'none'\n"
        "\n"
        "/public/audio/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "\n"
        "/public/fonts/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "\n"
        "/public/brand/*\n"
        "  Cache-Control: public, max-age=604800, stale-while-revalidate=2592000\n"
        "\n"
        "/assets/*\n"
        "  Cache-Control: public, max-age=604800, stale-while-revalidate=2592000\n"
        "\n"
        "/data/stories/*\n"
        "  Cache-Control: public, max-age=3600, stale-while-revalidate=86400\n"
        "\n"
        "/sw.js\n"
        "  Cache-Control: public, max-age=0, must-revalidate\n"
    )
    (OUT / "_headers").write_text(headers_txt, encoding="utf-8")

    total_bytes = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    idx_kb = (OUT / "index.html").stat().st_size / 1024
    print(
        f"[wms-build-deploy PASS] Đã đóng gói dist/site/ ({total_bytes / (1024 * 1024):.2f} MB · "
        f"index.html={idx_kb:.1f} KB · {copied_docs} trang/JS · {copied_fonts} font · "
        f"{copied_figs} ảnh public/brand · {copied_audio} audio · 7 JSON split packs)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(build_site())
