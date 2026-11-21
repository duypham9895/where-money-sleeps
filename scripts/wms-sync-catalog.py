#!/usr/bin/env python3
"""
wms-sync-catalog.py — Đồng bộ tất định các catalog từ docs/prototype.html & beats-manifest.json:
  1. cloudflare/worker.js  (ALLOWED_LESSONS, ALLOWED_CARDS, SEO_CATALOG.stories)
  2. legal/licences.json   (vieneu-tts-local-apache2.audio_files, youtube-channel-brand-art-gemini.brand_files)
  3. knowledge/wms-beatmap.json
  4. README.md             (Published Stories count & rows)

Chế độ `--verify` kiểm tra mọi file đồng bộ đủ & khớp mà không ghi đĩa (exit != 0 nếu lệch).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROTO_PATH = ROOT / "docs" / "prototype.html"
MANIFEST_PATH = ROOT / "public" / "audio" / "beats-manifest.json"
WORKER_PATH = ROOT / "cloudflare" / "worker.js"
LICENCES_PATH = ROOT / "legal" / "licences.json"
BEATMAP_PATH = ROOT / "knowledge" / "wms-beatmap.json"
README_PATH = ROOT / "README.md"


def _load_check_story():
    spec = importlib.util.spec_from_file_location("check_story", ROOT / "scripts" / "check-story.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Không nạp được scripts/check-story.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _find_matching_brace(text: str, open_idx: int, open_ch: str = "{", close_ch: str = "}") -> int:
    """Tìm vị trí ngoặc đóng khớp với open_idx, bỏ qua chuỗi JS và comment //, /* */."""
    depth = 0
    i = open_idx
    n = len(text)
    in_str: str | None = None
    in_line_comment = False
    in_block_comment = False
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
        elif in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 1
        elif in_str is not None:
            if ch == "\\":
                i += 1
            elif ch == in_str:
                in_str = None
        else:
            if ch == "/" and nxt == "/":
                in_line_comment = True
                i += 1
            elif ch == "/" and nxt == "*":
                in_block_comment = True
                i += 1
            elif ch in ('"', "'", "`"):
                in_str = ch
            elif ch == open_ch:
                depth += 1
            elif ch == close_ch:
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise ValueError(f"Không tìm thấy dấu `{close_ch}` tương ứng tại offset {open_idx}")


def _extract_js_top_entries(block_body: str) -> list[tuple[str, str]]:
    """Tách các cặp (key, full_entry_text) cấp 1 bên trong thân một object literal JS."""
    entries: list[tuple[str, str]] = []
    i = 0
    n = len(block_body)
    key_re = re.compile(r'^\s*(?:"([^"]+)"|\'([^\']+)\'|([A-Za-z0-9_$]+))\s*:\s*\{')
    while i < n:
        sub = block_body[i:]
        m = key_re.match(sub)
        if not m:
            nxt_nl = block_body.find("\n", i)
            if nxt_nl == -1:
                break
            i = nxt_nl + 1
            continue
        key = m.group(1) or m.group(2) or m.group(3)
        brace_open = i + m.end() - 1
        brace_close = _find_matching_brace(block_body, brace_open, "{", "}")
        entry_start = i + len(sub) - len(sub.lstrip("\r\n"))
        entries.append((key, block_body[entry_start : brace_close + 1].rstrip()))
        i = brace_close + 1
        while i < n and block_body[i] in " \t,":
            i += 1
        while i < n and block_body[i] in "\r\n":
            i += 1
    return entries


def _js_quote(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def _format_seo_entry(slug: str, s_vi: dict[str, Any], s_en: dict[str, Any]) -> str:
    yt_long = (s_vi.get("videoScript") or {}).get("long", {}).get("youtubeId") or ""
    vi_title = f"{s_vi['title']} — Where Money Sleeps"
    vi_desc = s_vi["teaser"]
    vi_alt = s_vi["title"]

    en_title = f"{s_en['title']} — Where Money Sleeps"
    en_desc = s_en["teaser"].strip()
    if "unofficial summary" not in en_desc.lower():
        if not en_desc.endswith((".", "!", "?")):
            en_desc += "."
        en_desc = f"{en_desc} (Unofficial summary of Circular 99/2025/TT-BTC.)"
    en_alt = s_en["title"]

    safe_key = slug if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", slug) else _js_quote(slug)
    return "\n".join(
        [
            f"    {safe_key}: {{",
            f"      ytLong: {_js_quote(yt_long)},",
            "      vi: {",
            f"        title: {_js_quote(vi_title)},",
            f"        desc: {_js_quote(vi_desc)},",
            f"        imgAlt: {_js_quote(vi_alt)}",
            "      },",
            "      en: {",
            f"        title: {_js_quote(en_title)},",
            f"        desc: {_js_quote(en_desc)},",
            f"        imgAlt: {_js_quote(en_alt)}",
            "      }",
            "    }",
        ]
    )


def _sync_worker(
    worker_text: str,
    published_slugs: list[str],
    stories: dict[str, Any],
    stories_en: dict[str, Any],
    quiz_bank: dict[str, Any],
) -> tuple[str, list[str]]:
    issues: list[str] = []

    expected_cards: list[str] = []
    for slug in published_slugs:
        for q in quiz_bank.get(slug, []):
            qid = q.get("id")
            if qid:
                expected_cards.append(str(qid))

    lessons_body = "\n" + ",\n".join(f"  {_js_quote(s)}" for s in published_slugs) + "\n"
    lessons_re = re.compile(r"(const ALLOWED_LESSONS = new Set\(\[)([\s\S]*?)(\]\);)")
    m_less = lessons_re.search(worker_text)
    if not m_less:
        raise ValueError("Không thấy ALLOWED_LESSONS trong cloudflare/worker.js")
    cur_lessons = re.findall(r'"([^"]+)"', m_less.group(2))
    if cur_lessons != published_slugs:
        issues.append(f"worker.js ALLOWED_LESSONS lệch: {cur_lessons} != {published_slugs}")
    new_worker = worker_text[: m_less.start(2)] + lessons_body + worker_text[m_less.end(2) :]

    cards_body = "\n" + ",\n".join(f"  {_js_quote(c)}" for c in expected_cards) + "\n"
    cards_re = re.compile(r"(const ALLOWED_CARDS = new Set\(\[)([\s\S]*?)(\]\);)")
    m_cards = cards_re.search(new_worker)
    if not m_cards:
        raise ValueError("Không thấy ALLOWED_CARDS trong cloudflare/worker.js")
    cur_cards = re.findall(r'"([^"]+)"', m_cards.group(2))
    if cur_cards != expected_cards:
        issues.append(f"worker.js ALLOWED_CARDS lệch ({len(cur_cards)} != {len(expected_cards)})")
    new_worker = new_worker[: m_cards.start(2)] + cards_body + new_worker[m_cards.end(2) :]

    seo_m = re.search(r"\bstories:\s*\{", new_worker)
    if not seo_m:
        raise ValueError("Không thấy SEO_CATALOG.stories trong cloudflare/worker.js")
    open_brace = seo_m.end() - 1
    close_brace = _find_matching_brace(new_worker, open_brace, "{", "}")
    inner_seo = new_worker[open_brace + 1 : close_brace]
    existing_entries = _extract_js_top_entries(inner_seo)
    existing_map = {k: body for k, body in existing_entries}

    rendered_entries: list[str] = []
    for slug in published_slugs:
        yt_long = (stories[slug].get("videoScript") or {}).get("long", {}).get("youtubeId") or ""
        if slug in existing_map:
            block = existing_map[slug]
            yt_m = re.search(r'ytLong:\s*"([^"]*)"', block)
            has_unoff = "unofficial summary" in block.lower()
            if yt_m and yt_m.group(1) == yt_long and has_unoff:
                rendered_entries.append(block)
                continue
            issues.append(f"worker.js SEO_CATALOG.stories[{slug}] lệch ytLong hoặc thiếu unofficial summary")
        else:
            issues.append(f"worker.js SEO_CATALOG.stories thiếu bài `{slug}`")
        rendered_entries.append(_format_seo_entry(slug, stories[slug], stories_en[slug]))

    new_seo_inner = "\n" + ",\n".join(rendered_entries) + "\n  "
    new_worker = new_worker[: open_brace + 1] + new_seo_inner + new_worker[close_brace:]
    return new_worker, issues


def _sync_licences(
    lic_data: dict[str, Any],
    published_slugs: list[str],
    stories: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    updated = json.loads(json.dumps(lic_data))
    assets = updated.get("assets", [])

    el_asset = next((a for a in assets if a.get("id") == "elevenlabs-commercial-tts-sfx"), None)
    vn_asset = next((a for a in assets if a.get("id") == "vieneu-tts-local-apache2"), None)
    brand_asset = next((a for a in assets if a.get("id") == "youtube-channel-brand-art-gemini"), None)
    if el_asset is None or vn_asset is None or brand_asset is None:
        raise ValueError("legal/licences.json thiếu asset bắt buộc (elevenlabs / vieneu / brand)")

    el_files = {str(x.get("file")) for x in el_asset.get("audio_files", []) if isinstance(x, dict)}
    cur_vn_list = [str(x.get("file")) for x in vn_asset.get("audio_files", []) if isinstance(x, dict)]
    cur_vn_set = set(cur_vn_list)

    expected_vn: list[str] = list(cur_vn_list)
    for slug in published_slugs:
        rel_audio = f"public/audio/{slug}-beats.mp3"
        disk_exists = (ROOT / rel_audio).is_file()
        vs = stories[slug].get("videoScript") or {}
        voice = str(vs.get("long", {}).get("elevenlabsVoiceId") or "")
        is_vieneu = voice.startswith("vieneu:") or (disk_exists and rel_audio not in el_files)
        if disk_exists and rel_audio not in el_files and is_vieneu:
            if rel_audio not in cur_vn_set:
                issues.append(f"legal/licences.json thiếu audio VieNeu `{rel_audio}`")
                expected_vn.append(rel_audio)
                cur_vn_set.add(rel_audio)
        elif not disk_exists and is_vieneu:
            issues.append(f"Thiếu file audio trên đĩa `{rel_audio}` cho bài published `{slug}`")

    for p in sorted((ROOT / "public" / "audio").glob("*-beats.mp3")):
        rel = p.relative_to(ROOT).as_posix()
        if rel not in el_files and rel not in cur_vn_set:
            issues.append(f"File `{rel}` trên đĩa chưa khai báo trong legal/licences.json")
            expected_vn.append(rel)
            cur_vn_set.add(rel)

    vn_asset["audio_files"] = [{"file": f} for f in expected_vn]

    cur_brand = list(brand_asset.get("brand_files", []))
    cur_brand_set = set(cur_brand)
    brand_dir = ROOT / "public" / "brand"
    if brand_dir.is_dir():
        for p in sorted(brand_dir.iterdir()):
            if not p.is_file() or p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".avif", ".svg"}:
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel not in cur_brand_set:
                issues.append(f"legal/licences.json thiếu brand image `{rel}`")
                cur_brand.append(rel)
                cur_brand_set.add(rel)
    brand_asset["brand_files"] = cur_brand
    return updated, issues


def _build_beatmap(
    existing_beatmap: dict[str, Any],
    published_slugs: list[str],
    stories: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    out: dict[str, Any] = {}
    for slug in published_slugs:
        s = stories[slug]
        m = manifest.get(slug)
        if not m:
            issues.append(f"public/audio/beats-manifest.json thiếu entry `{slug}`")
            if slug in existing_beatmap:
                out[slug] = existing_beatmap[slug]
            continue
        vs = s.get("videoScript") or {}
        yt_long = vs.get("long", {}).get("youtubeId")
        yt_short = vs.get("short", {}).get("youtubeId")
        s_beats = s.get("beats", [])
        m_beats = m.get("beats", [])
        if len(s_beats) != len(m_beats):
            issues.append(f"Số beat lệch giữa STORIES[{slug}] ({len(s_beats)}) và beats-manifest ({len(m_beats)})")
        merged_beats = []
        for idx, b in enumerate(s_beats):
            mb = m_beats[idx] if idx < len(m_beats) else {}
            merged_beats.append(
                {
                    "beat": b.get("beat", idx),
                    "when": b.get("when", ""),
                    "title": b.get("title", ""),
                    "lit": b.get("lit", []),
                    "msgs": b.get("msgs", []),
                    "tags": b.get("tags", {}),
                    "t0": mb.get("t0"),
                    "t1": mb.get("t1"),
                }
            )
        entry = {
            "story": slug,
            "title": s.get("title", ""),
            "audioSrc": m.get("src", f"public/audio/{slug}-beats.mp3"),
            "duration": m.get("duration"),
            "youtubeLongId": yt_long,
            "youtubeShortId": yt_short,
            "beats": merged_beats,
        }
        if existing_beatmap.get(slug) != entry:
            issues.append(f"knowledge/wms-beatmap.json lệch ở bài `{slug}`")
        out[slug] = entry
    extra_keys = set(existing_beatmap.keys()) - set(published_slugs)
    if extra_keys:
        issues.append(f"knowledge/wms-beatmap.json còn khoá thừa: {sorted(extra_keys)}")
    return out, issues


def _mechanism_summary(s_vi: dict[str, Any], s_en: dict[str, Any]) -> str:
    txt = re.sub(r"\s+", " ", str(s_en.get("teaser") or s_vi.get("teaser") or "")).strip()
    txt = re.sub(r"\s*\(Unofficial summary[^)]*\)\.?\s*$", "", txt, flags=re.IGNORECASE).strip()
    txt = txt.rstrip(".")
    return txt.replace("|", "\\|")


def _sync_readme(
    readme_text: str,
    published_slugs: list[str],
    stories: dict[str, Any],
    stories_en: dict[str, Any],
    categories: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    issues: list[str] = []
    lines = readme_text.splitlines(keepends=True)

    published_set = set(published_slugs)
    live_cats = 0
    for cat in categories:
        if any(t.get("story") in published_set for t in cat.get("topics", [])):
            live_cats += 1
    expected_heading = f"## Published Stories ({live_cats} Categories · {len(published_slugs)} Lessons Live — VI ⇄ EN)"

    start_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("## Published Stories"):
            start_idx = idx
            break
    if start_idx is None:
        raise ValueError("Không thấy mục `## Published Stories` trong README.md")

    cur_heading = lines[start_idx].rstrip("\r\n")
    if cur_heading != expected_heading:
        issues.append(f"README.md heading lệch: `{cur_heading}` != `{expected_heading}`")

    end_idx = start_idx + 1
    while end_idx < len(lines):
        if lines[end_idx].startswith("## ") or lines[end_idx].strip() == "---":
            break
        end_idx += 1

    existing_rows: dict[str, str] = {}
    row_re = re.compile(r"^\|\s*`([^`]+)`\s*\|")
    for line in lines[start_idx + 1 : end_idx]:
        m = row_re.match(line)
        if m:
            existing_rows[m.group(1)] = line.rstrip("\r\n")

    table_rows: list[str] = []
    for slug in published_slugs:
        s_vi = stories[slug]
        s_en = stories_en[slug]
        vs = s_vi.get("videoScript") or {}
        yt_long = vs.get("long", {}).get("youtubeId") or ""
        yt_short = vs.get("short", {}).get("youtubeId") or ""
        yt_cell = f"`{yt_long}` · `{yt_short}`"
        if slug in existing_rows:
            row = existing_rows[slug]
            if yt_long in row and yt_short in row:
                table_rows.append(row)
                continue
            issues.append(f"README.md hàng `{slug}` thiếu YouTube ID hiện tại ({yt_long}, {yt_short})")
            parts = [p.strip() for p in re.split(r"(?<!\\)\|", row.strip("|"))]
            if len(parts) >= 4:
                parts[-1] = yt_cell
                table_rows.append("| " + " | ".join(parts) + " |")
                continue
        else:
            issues.append(f"README.md thiếu hàng cho bài published `{slug}`")
        mech = _mechanism_summary(s_vi, s_en)
        table_rows.append(f"| `{slug}` | {s_vi['name'].replace('|', '/')} | {mech} | {yt_cell} |")

    trailing_blank = "\n" if end_idx < len(lines) else ""
    new_block = (
        expected_heading
        + "\n\n"
        + "| Story | Title | Mechanism & Focus | YouTube (16:9 & Shorts · v7.2) |\n"
        + "|---|---|---|---|\n"
        + "\n".join(table_rows)
        + "\n"
        + trailing_blank
    )
    new_readme = "".join(lines[:start_idx]) + new_block + "".join(lines[end_idx:])
    return new_readme, issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync Where Money Sleeps catalogs from docs/prototype.html")
    ap.add_argument("--verify", action="store_true", help="Kiểm tra lệch đồng bộ, không ghi file")
    args = ap.parse_args()

    cs = _load_check_story()
    html = PROTO_PATH.read_text(encoding="utf-8")
    stories = cs.extract(html, "STORIES")
    stories_en = cs.extract(html, "STORIES_EN")
    categories = cs.extract(html, "CATEGORIES")
    quiz_bank = cs.extract(html, "WMS_QUIZ_BANK")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    published_slugs = [slug for slug, s in stories.items() if s.get("status") == "published"]

    worker_old = WORKER_PATH.read_text(encoding="utf-8")
    worker_new, worker_issues = _sync_worker(worker_old, published_slugs, stories, stories_en, quiz_bank)

    lic_old_text = LICENCES_PATH.read_text(encoding="utf-8")
    lic_old = json.loads(lic_old_text)
    lic_new, lic_issues = _sync_licences(lic_old, published_slugs, stories)

    beatmap_old_text = BEATMAP_PATH.read_text(encoding="utf-8")
    beatmap_old = json.loads(beatmap_old_text)
    beatmap_new, beatmap_issues = _build_beatmap(beatmap_old, published_slugs, stories, manifest)

    readme_old = README_PATH.read_text(encoding="utf-8")
    readme_new, readme_issues = _sync_readme(readme_old, published_slugs, stories, stories_en, categories)

    all_issues = worker_issues + lic_issues + beatmap_issues + readme_issues

    if args.verify:
        if all_issues:
            print("[FAIL] wms-sync-catalog.py --verify phát hiện lệch:", file=sys.stderr)
            for item in all_issues:
                print(f"  - {item}", file=sys.stderr)
            return 1
        print(f"[PASS] wms-sync-catalog.py --verify: {len(published_slugs)} bài published đồng bộ đầy đủ.")
        return 0

    changed: list[str] = []
    if worker_new != worker_old:
        WORKER_PATH.write_text(worker_new, encoding="utf-8")
        changed.append("cloudflare/worker.js")
    lic_new_text = json.dumps(lic_new, ensure_ascii=False, indent=2) + "\n"
    if lic_new_text != lic_old_text and lic_issues:
        LICENCES_PATH.write_text(lic_new_text, encoding="utf-8")
        changed.append("legal/licences.json")
    beatmap_new_text = json.dumps(beatmap_new, ensure_ascii=False, indent=2) + "\n"
    if beatmap_new_text != beatmap_old_text:
        BEATMAP_PATH.write_text(beatmap_new_text, encoding="utf-8")
        changed.append("knowledge/wms-beatmap.json")
    if readme_new != readme_old:
        README_PATH.write_text(readme_new, encoding="utf-8")
        changed.append("README.md")

    if changed:
        print(f"[OK] Đã đồng bộ: {', '.join(changed)}")
    else:
        print(f"[OK] Không có thay đổi ({len(published_slugs)} bài published đã khớp).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
