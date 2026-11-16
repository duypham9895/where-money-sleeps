#!/usr/bin/env python3
"""
wms_qa_uiux.py — Kiểm định Tĩnh & Playwright Runtime cho Holistic UI/UX (`LUẬT 13 · U1–U7`).
Gồm: metric fallback fonts, contrast AA Light/Dark/Paper/Charcoal, SC 1.4.11 UI border contrast,
zero-FOUC color-scheme, Scoped Vestibular Dampening, Skip-Link + :focus-visible, và VNI/Telex IME guard.
"""
from __future__ import annotations

import re
from pathlib import Path

DOC_PAGES = [
    "s1.html", "s2.html", "s3.html", "s4.html", "s5.html",
    "s6.html", "index.html", "duyslab-overview.html", "llm-quiz.html",
]
MOCKUP_PAGES = [
    "landing-detail-mockups.html", "mockup-option-a.html", "mockup-option-b.html",
    "mockup-mobile-a.html", "mockup-mobile-b.html", "studio-mockups.html",
]
ALL_STORIES = ["card", "pay", "install", "minpay", "qr", "profitcash", "offus"]

_CONTRAST_JS = """(specs) => {
  const parseRgba = (s) => {
    let m = (s || "").match(/color\\(srgb\\s+([^)]+)\\)/i);
    if (m) {
      const p = m[1].replace(/\\//g, " ").trim().split(/\\s+/).map(Number);
      return [(p[0] || 0) * 255, (p[1] || 0) * 255, (p[2] || 0) * 255, p.length >= 4 && !Number.isNaN(p[3]) ? p[3] : 1];
    }
    m = (s || "").match(/rgba?\\(([^)]+)\\)/i);
    if (!m) return [0, 0, 0, 0];
    const p = m[1].replace(/\\//g, " ").trim().split(/[\\s,]+/).map(Number);
    return [p[0] || 0, p[1] || 0, p[2] || 0, p.length >= 4 && !Number.isNaN(p[3]) ? p[3] : 1];
  };
  const blend = (top, bot) => {
    const a = top[3];
    return [top[0]*a + bot[0]*(1-a), top[1]*a + bot[1]*(1-a), top[2]*a + bot[2]*(1-a), 1];
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b);
  };
  const ratio = (c1, c2) => {
    const l1 = lum(c1), l2 = lum(c2);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  };
  const bgChain = (el, stopBeforeSelf) => {
    const chain = [];
    for (let cur = stopBeforeSelf ? el.parentElement : el; cur; cur = cur.parentElement) chain.push(cur);
    chain.reverse();
    let acc = [255, 255, 255, 1];
    for (const node of chain) {
      const c = parseRgba(getComputedStyle(node).backgroundColor);
      if (c[3] > 0) acc = blend(c, acc);
    }
    return acc;
  };
  const out = [];
  for (const sp of specs) {
    const el = document.querySelector(sp.sel);
    if (!el) continue;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (r.width <= 0 || r.height <= 0 || cs.visibility === "hidden" || cs.display === "none") continue;
    if (sp.mode === "border") {
      const bc = parseRgba(cs.borderTopColor);
      const pbg = bgChain(el, true);
      const bbg = blend(bc, pbg);
      out.push({ sel: sp.sel, mode: "border", cr: ratio(bbg, pbg), minCr: 3.0 });
    } else {
      const ownBg = bgChain(el, false);
      const fg = blend(parseRgba(cs.color), ownBg);
      const fs = parseFloat(cs.fontSize) || 16;
      const fw = parseInt(cs.fontWeight, 10) || 400;
      const isLarge = fs >= 24 || (fs >= 18.66 && fw >= 700);
      out.push({ sel: sp.sel, mode: "text", cr: ratio(fg, ownBg), minCr: isLarge ? 3.0 : 4.5 });
    }
  }
  return out;
}"""


def static_uiux_checks(root_dir: Path) -> list[str]:
    errs: list[str] = []
    docs = root_dir / "docs"
    proto = (docs / "prototype.html").read_text(encoding="utf-8")
    wf = (docs / "workflows.html").read_text(encoding="utf-8")
    studio = (docs / "studio.html").read_text(encoding="utf-8")

    for name, src in [("prototype.html", proto), ("workflows.html", wf), ("studio.html", studio)]:
        for tok in ['name="color-scheme"', 'name="text-scale" content="scale"', "viewport-fit=cover",
                    ".skip-link", 'id="mainContent"', ":focus-visible", "prefers-reduced-motion"]:
            if tok not in src:
                errs.append(f"{name} thiếu {tok} (U1–U7)")
        if src.find("<script>") == -1 or src.find("<script>") > src.find("<style>"):
            errs.append(f"{name} thiếu synchronous zero-FOUC <script> trước <style> (U4)")
        if "light-dark(" in src or "overflow-clip-margin" in src:
            errs.append(f"{name} dùng CSS không an toàn (light-dark() / overflow-clip-margin)")
        rm_pos = src.find("@media (prefers-reduced-motion")
        if rm_pos != -1 and ".01ms" in src[rm_pos:rm_pos + 500]:
            errs.append(f"{name} vẫn còn nuclear 0.01ms !important trong prefers-reduced-motion (U5)")

    for tok in ['"Newsreader Fallback"', '"Be Vietnam Pro Fallback"', "tabular-nums lining-nums",
                "bindComposedInput", "isComposing", "compositionend", "#atlasQ", "#landingSearch", "#glSearch"]:
        if tok not in proto:
            errs.append(f"prototype.html thiếu {tok}")
    scene_m = re.search(r"/\*SCENECSS:START.*?SCENECSS:END\*/", proto, flags=re.S)
    font_rem_re = re.compile(r"""font(?:-size)?\s*[:=]\s*["']?[^;}'">]*(?:\d+(?:\.\d+)?|\.\d+)r?em\b""")
    if scene_m and font_rem_re.search(scene_m.group(0)):
        errs.append("prototype.html SCENECSS chứa font-size rem|em bị cấm")
    for svg_m in re.finditer(r"<svg\b[^>]*>.*?</svg>", proto + wf, flags=re.S):
        if "viewBox=" in svg_m.group(0) and font_rem_re.search(svg_m.group(0)):
            errs.append("SVG <svg viewBox> chứa font-size rem|em bị cấm")
            break

    if '"Newsreader Fallback"' not in wf or not re.search(r"\.fact-cell\s+\.val\{[^}]*var\(--sans\)", wf):
        errs.append("workflows.html thiếu font fallback hoặc .fact-cell .val chưa dùng var(--sans)")
    for tok in ["wms-studio-theme", "--ok-fill", "--flag-fill", "Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700", "font-size: 0.875rem"]:
        if tok not in studio:
            errs.append(f"studio.html thiếu {tok}")
    if re.search(r"html,\s*body\s*\{[^}]*font-size:\s*14px", studio):
        errs.append("studio.html vẫn đặt font-size:14px lên html (làm lệch 1rem)")

    for pg in DOC_PAGES:
        txt = (docs / pg).read_text(encoding="utf-8")
        for tok in ["viewport-fit=cover", 'name="text-scale"', 'name="color-scheme"', "vibe-doc-theme", "wght@400;500;600;700;800"]:
            if tok not in txt:
                errs.append(f"docs/{pg} thiếu {tok}")
        if "wght@400;500;650" in txt:
            errs.append(f"docs/{pg} vẫn còn font axis wght@400;500;650")

    for pg in MOCKUP_PAGES:
        txt = (docs / pg).read_text(encoding="utf-8")
        for tok in ["viewport-fit=cover", 'name="text-scale" content="scale"', 'name="color-scheme"', ":focus-visible", "prefers-reduced-motion"]:
            if tok not in txt:
                errs.append(f"docs/{pg} thiếu {tok} (U1–U7)")
        if txt.find("<script>") == -1 or txt.find("<script>") > txt.find("<style>"):
            errs.append(f"docs/{pg} thiếu synchronous zero-FOUC <script> trước <style> (U4)")
        rm_pos = txt.find("@media (prefers-reduced-motion")
        if rm_pos != -1 and ".01ms" in txt[rm_pos:rm_pos + 500]:
            errs.append(f"docs/{pg} vẫn còn nuclear 0.01ms !important trong prefers-reduced-motion (U5)")
        if re.search(r"html\s*\{[^}]*font-size\s*:", txt) or re.search(r"html,\s*body\s*\{[^}]*font-size:\s*1[49]px", txt):
            errs.append(f"docs/{pg} vẫn ép font-size trên html (làm lệch 1rem)")

    expected_html = {"prototype.html", "workflows.html", "studio.html", *DOC_PAGES, *MOCKUP_PAGES}
    actual_html = {p.name for p in docs.glob("*.html")}
    if actual_html != expected_html:
        missing_cov = sorted(actual_html - expected_html)
        extra_cov = sorted(expected_html - actual_html)
        if missing_cov:
            errs.append(f"docs/ có trang HTML chưa phủ kiểm tra UI/UX: {missing_cov}")
        if extra_cov:
            errs.append(f"docs/ thiếu trang HTML khai báo trong UI/UX gate: {extra_cov}")
    return errs


def runtime_uiux_checks(page, base_url: str) -> list[str]:
    errs: list[str] = []
    targets = [
        ("prototype-light-landing", f"{base_url}/docs/prototype.html?theme=light", "#landingSearch", [
            {"sel": ".hero h1"}, {"sel": ".hero-kicker"}, {"sel": ".ab-brand"}, {"sel": ".sp-caret"},
            {"sel": "#landingSearch", "mode": "border"},
        ]),
        ("prototype-dark-landing", f"{base_url}/docs/prototype.html?theme=dark", "#landingSearch", [
            {"sel": ".hero h1"}, {"sel": ".hero-kicker"}, {"sel": ".ab-brand"}, {"sel": ".sp-caret"},
            {"sel": "#landingSearch", "mode": "border"},
        ]),
        ("workflows-light", f"{base_url}/docs/workflows.html?theme=light", ".hero h1", [
            {"sel": ".hero h1"}, {"sel": ".hero-kicker"}, {"sel": ".fact-cell .lbl"}, {"sel": ".fact-cell .val"}, {"sel": ".tldr-tag"},
        ]),
        ("workflows-dark", f"{base_url}/docs/workflows.html?theme=dark", ".hero h1", [
            {"sel": ".hero h1"}, {"sel": ".hero-kicker"}, {"sel": ".fact-cell .lbl"}, {"sel": ".fact-cell .val"}, {"sel": ".tldr-tag"},
        ]),
        ("studio-paper", f"{base_url}/docs/studio.html?theme=paper&story=install&mode=post", ".btn-primary", [
            {"sel": ".btn-primary"}, {"sel": ".ac-kicker"}, {"sel": ".ac-badge"}, {"sel": ".gate-pill-btn"},
            {"sel": "#storySelect", "mode": "border"}, {"sel": ".ac-note-input", "mode": "border"},
        ]),
        ("studio-charcoal", f"{base_url}/docs/studio.html?theme=charcoal&story=install&mode=post", ".btn-primary", [
            {"sel": ".btn-primary"}, {"sel": ".ac-kicker"}, {"sel": ".ac-badge"}, {"sel": ".gate-pill-btn"},
            {"sel": "#storySelect", "mode": "border"}, {"sel": ".ac-note-input", "mode": "border"},
        ]),
    ]
    story_specs = [
        {"sel": ".detail-cat-chip"},
        {"sel": ".detail-teaser"},
        {"sel": ".journal .jstep"},
        {"sel": ".yt-play"},
        {"sel": ".verdict h5"},
        {"sel": ".verdict p"},
    ]
    for slug in ALL_STORIES:
        targets.append((f"story-{slug}-light", f"{base_url}/docs/prototype.html?story={slug}&theme=light", ".detail-cat-chip", story_specs))
        targets.append((f"story-{slug}-dark", f"{base_url}/docs/prototype.html?story={slug}&theme=dark", ".detail-cat-chip", story_specs))

    for label, url, wait_sel, specs in targets:
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector(wait_sel)
        page.wait_for_timeout(100)
        for res in page.evaluate(_CONTRAST_JS, specs):
            if res["cr"] < res["minCr"]:
                errs.append(f"[{label}] {res['sel']} ({res['mode']}) contrast {res['cr']:.2f} < {res['minCr']:.1f}")

    for vw, vh in [(1280, 800), (320, 568)]:
        page.set_viewport_size({"width": vw, "height": vh})
        for pg in MOCKUP_PAGES:
            dark_param = "charcoal" if pg == "studio-mockups.html" else "dark"
            page.goto(f"{base_url}/docs/{pg}?theme={dark_param}", wait_until="domcontentloaded")
            page.wait_for_timeout(60)
            chk = page.evaluate("""() => ({
              ov: document.documentElement.scrollWidth - window.innerWidth,
              cs: getComputedStyle(document.documentElement).colorScheme || ""
            })""")
            if chk["ov"] > 0:
                errs.append(f"[{pg}@{vw}x{vh}] tràn ngang +{chk['ov']}px")
            if "dark" not in chk["cs"]:
                errs.append(f"[{pg}@{vw}x{vh}] ?theme={dark_param} colorScheme không đồng bộ dark: {chk['cs']!r}")
    page.set_viewport_size({"width": 1280, "height": 800})

    for label, url in [
        ("prototype", f"{base_url}/docs/prototype.html"),
        ("workflows", f"{base_url}/docs/workflows.html"),
        ("studio", f"{base_url}/docs/studio.html"),
    ]:
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#skipLink")
        page.keyboard.press("Tab")
        sk = page.evaluate("""() => {
          const el = document.activeElement;
          const cs = el ? getComputedStyle(el) : null;
          const r = el ? el.getBoundingClientRect() : {height: 0};
          return { id: el ? el.id : "", outline: cs ? cs.outlineStyle : "none", h: r.height };
        }""")
        if sk["id"] != "skipLink" or sk["outline"] == "none" or sk["h"] < 43.5:
            errs.append(f"[{label}] Tab skip-link check failed: {sk}")

    page.goto(f"{base_url}/docs/prototype.html", wait_until="domcontentloaded")
    page.wait_for_selector("#landingSearch")
    ime = page.evaluate("""() => {
      const inp = document.querySelector("#landingSearch");
      const countCards = () => [...document.querySelectorAll("#storyList .story-card")].filter(c => getComputedStyle(c).display !== "none").length;
      const n0 = countCards();
      inp.focus();
      inp.dispatchEvent(new CompositionEvent("compositionstart", { bubbles: true, data: "t" }));
      inp.value = "zzzz_vni_test";
      inp.dispatchEvent(new InputEvent("input", { bubbles: true, isComposing: true }));
      const during = countCards();
      inp.dispatchEvent(new CompositionEvent("compositionend", { bubbles: true, data: "zzzz_vni_test" }));
      const after = countCards();
      inp.value = "";
      inp.dispatchEvent(new InputEvent("input", { bubbles: true, isComposing: false }));
      return { n0, during, after, reset: countCards() };
    }""")
    if ime["n0"] == 0 or ime["during"] != ime["n0"] or ime["after"] != 0 or ime["reset"] != ime["n0"]:
        errs.append(f"[prototype] VNI/Telex isComposing IME guard failed: {ime}")
    return errs


def run_holistic_uiux_checks(page, root_dir: Path, base_url: str | None = None) -> list[str]:
    errs = static_uiux_checks(root_dir)
    if page is not None and base_url:
        errs.extend(runtime_uiux_checks(page, base_url))
    return errs
