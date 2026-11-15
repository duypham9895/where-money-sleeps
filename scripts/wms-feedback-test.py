#!/usr/bin/env python3
"""
wms-feedback-test.py — Bộ 12 test-case E2E kiểm thử tính năng "Hộp thư Góp ý & Đề xuất bài viết mới"
và nút icon Sao chép Email (`hello@duypham.me`) bằng Playwright Chromium.

Chạy:
  /opt/homebrew/Caskroom/miniforge/base/bin/python3 -I scripts/wms-feedback-test.py
  /opt/homebrew/Caskroom/miniforge/base/bin/python3 -I scripts/wms-feedback-test.py --artifacts
"""

import argparse
import functools
import http.server
import socketserver
import sys
import threading
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/edwardpham/.gemini/antigravity/brain/e0b64418-4798-42c0-83f6-ec92206aaefd")

SPECS = {
    "docs_a": {
        "copy_btn": "#ftCopyEmailBtn",
        "kind_btn": "#siteFooter [data-fb-kind]",
        "chip_btn": "#fbQuickChips [data-fb-tpl]",
        "msg": "#fbMessage",
        "email": "#fbEmail",
        "submit": "#fbSubmitBtn",
        "status": "#fbStatus",
        "mailto": "#fbMailtoLink",
        "ctx": "#fbCtxBanner",
        "detail_btn": "#labDetailBtn",
        "landing_btn": "#labLandingBtn",
        "check_dedup": True,
        "ctx_hidden_on_landing": True,
        "has_dock": True,
        "expected_dt": 5,
        "err_el": "#fbMessageError",
        "tab_sel": ".fb-mode-btn",
    },
    "docs_b": {
        "copy_btn": "#copyEmailBtnB",
        "kind_btn": "#siteFooter [data-fb-kind]",
        "chip_btn": "#siteFooter [data-fb-chip]",
        "msg": "#fbMessageB",
        "email": "#fbEmailB",
        "submit": "#fbCopyDraftBtnB",
        "status": "#fbStatusB",
        "mailto": "#fbMailtoLinkB",
        "ctx": "#fbCtxBannerB",
        "detail_btn": "#labDetailBtn",
        "landing_btn": "#labLandingBtn",
        "check_dedup": False,
        "ctx_hidden_on_landing": False,
        "has_dock": True,
        "expected_dt": 5,
        "err_el": "#fbMsgErrB",
        "tab_sel": ".fb-tab",
    },
    "art_a": {
        "copy_btn": "#copyEmailBtnA",
        "kind_btn": "#siteFooter [data-fb-kind]",
        "chip_btn": "#siteFooter [data-fb-chip]",
        "msg": "#fbMessageA",
        "email": "#fbEmailA",
        "submit": "#fbSubmitBtnA",
        "status": "#fbStatusA",
        "mailto": "#fbMailtoLinkA",
        "ctx": "#fbCtxBannerA",
        "detail_btn": "#vDetBtn",
        "landing_btn": "#vLandBtn",
        "check_dedup": False,
        "ctx_hidden_on_landing": False,
        "has_dock": False,
        "expected_dt": 4,
        "err_el": "#fbMsgErrA",
        "tab_sel": ".fb-tab",
    },
    "art_b": {
        "copy_btn": "#copyEmailBtnB",
        "kind_btn": "#siteFooterB [data-fb-kind]",
        "chip_btn": "#siteFooterB [data-fb-chip]",
        "msg": "#fbMessageB",
        "email": "#fbEmailB",
        "submit": "#fbCopyDraftBtnB",
        "status": "#fbStatusB",
        "mailto": "#fbMailtoLinkB",
        "ctx": "#fbCtxBannerB",
        "detail_btn": "#vDetBtn",
        "landing_btn": "#vLandBtn",
        "check_dedup": False,
        "ctx_hidden_on_landing": False,
        "has_dock": False,
        "expected_dt": 4,
        "err_el": "#fbMsgErrB",
        "tab_sel": ".fb-tab",
    },
}

CLIPBOARD_SPY_SCRIPT = """
(() => {
  window.__copiedLog = [];
  const fakeClipboard = {
    writeText: async (text) => {
      window.__copiedLog.push(String(text));
      return undefined;
    }
  };
  try {
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      get: () => fakeClipboard
    });
  } catch (_) {}
})();
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def start_ephemeral_server(directory: Path):
    handler = functools.partial(QuietHandler, directory=str(directory))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port


def run_suite_on_target(browser, name: str, url: str, spec: dict) -> list[str]:
    failures = []

    def check(tc_id: str, cond: bool, msg: str):
        if not cond:
            failures.append(f"[{name} · {tc_id}] {msg}")

    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_init_script(CLIPBOARD_SPY_SCRIPT)
    page = ctx.new_page()
    page.set_default_timeout(5000)

    console_errs = []
    page_errs = []
    page.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errs.append(str(e)))

    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(120)

    # TC-01: Copy Email icon idle state
    tc01 = page.evaluate("""(sel) => {
      const btn = document.querySelector(sel);
      if (!btn) return null;
      const icoCopy = btn.querySelector('svg.ico-copy');
      const icoCheck = btn.querySelector('svg.ico-check');
      const toast = btn.querySelector('.ft-copy-toast');
      return {
        copiedAttr: btn.dataset.copied,
        aria: btn.getAttribute('aria-label') || '',
        title: btn.getAttribute('title') || '',
        borderTop: getComputedStyle(btn).borderTopWidth,
        copyVisible: icoCopy ? getComputedStyle(icoCopy).display !== 'none' : false,
        checkHidden: icoCheck ? getComputedStyle(icoCheck).display === 'none' : false,
        toastHidden: toast ? getComputedStyle(toast).display === 'none' : false,
        rawText: btn.innerText.trim(),
      };
    }""", spec["copy_btn"])
    check("TC-01", tc01 is not None, f"Missing copy button {spec['copy_btn']}")
    if tc01:
        check("TC-01", tc01["copiedAttr"] == "false", f"Expected initial data-copied='false', got {tc01['copiedAttr']}")
        check("TC-01", "hello@duypham.me" in tc01["aria"] and "hello@duypham.me" in tc01["title"], f"Missing email aria/title: {tc01}")
        check("TC-01", tc01["copyVisible"] and tc01["checkHidden"] and tc01["toastHidden"], f"Icon idle visibility wrong: {tc01}")
        check("TC-01", tc01["borderTop"] == "0px", f"Copy btn borderTopWidth={tc01['borderTop']} != 0px")
        check("TC-01", tc01["rawText"] == "", f"Unexpected visible text on icon button: {tc01['rawText']!r}")

    # TC-02: Copy Email click -> clipboard write, check icon + toast shown, auto-reset after 2s
    page.click(spec["copy_btn"])
    page.wait_for_timeout(100)
    tc02_active = page.evaluate("""(sel) => {
      const btn = document.querySelector(sel);
      const icoCopy = btn.querySelector('svg.ico-copy');
      const icoCheck = btn.querySelector('svg.ico-check');
      const toast = btn.querySelector('.ft-copy-toast');
      return {
        log: window.__copiedLog,
        copiedAttr: btn.dataset.copied,
        aria: btn.getAttribute('aria-label') || '',
        copyHidden: icoCopy ? getComputedStyle(icoCopy).display === 'none' : false,
        checkVisible: icoCheck ? getComputedStyle(icoCheck).display !== 'none' : false,
        toastText: toast && getComputedStyle(toast).display !== 'none' ? toast.textContent.trim() : '',
      };
    }""", spec["copy_btn"])
    check("TC-02", tc02_active["log"] == ["hello@duypham.me"], f"Clipboard spy mismatch: {tc02_active['log']}")
    check("TC-02", tc02_active["copiedAttr"] == "true" and tc02_active["copyHidden"] and tc02_active["checkVisible"], f"Copied state UI wrong: {tc02_active}")
    check("TC-02", tc02_active["toastText"] == "Đã chép" and "Đã sao chép" in tc02_active["aria"], f"Copied feedback text/aria wrong: {tc02_active}")

    page.wait_for_timeout(2150)
    tc02_reset = page.evaluate("""(sel) => {
      const btn = document.querySelector(sel);
      return { copiedAttr: btn.dataset.copied, aria: btn.getAttribute('aria-label') || '' };
    }""", spec["copy_btn"])
    check("TC-02", tc02_reset["copiedAttr"] == "false" and "Sao chép email" in tc02_reset["aria"], f"Copy icon did not auto-reset: {tc02_reset}")

    # TC-03: Mode tabs switcher (topic <-> feedback) updates aria-pressed & mailto subject
    fb_btn = page.locator(f"{spec['kind_btn']}[data-fb-kind='feedback']")
    topic_btn = page.locator(f"{spec['kind_btn']}[data-fb-kind='topic']")
    fb_btn.click()
    page.wait_for_timeout(60)
    mailto_fb = urllib.parse.unquote(page.get_attribute(spec["mailto"], "href") or "")
    check("TC-03", fb_btn.get_attribute("aria-pressed") == "true" and topic_btn.get_attribute("aria-pressed") == "false", "Mode tabs aria-pressed did not toggle to feedback")
    check("TC-03", "Góp ý" in mailto_fb, f"Mailto subject did not switch to feedback: {mailto_fb}")
    topic_btn.click()
    page.wait_for_timeout(60)
    mailto_top = urllib.parse.unquote(page.get_attribute(spec["mailto"], "href") or "")
    check("TC-03", topic_btn.get_attribute("aria-pressed") == "true" and "Đề xuất bài viết mới" in mailto_top, f"Mailto subject did not switch back to topic: {mailto_top}")

    # TC-04: Quick chips populate textarea, clear errors, update mailto, and Option A deduplicates repeat clicks
    first_chip = page.locator(spec["chip_btn"]).first
    first_chip.click()
    page.wait_for_timeout(50)
    msg_after_chip = page.input_value(spec["msg"])
    check("TC-04", len(msg_after_chip.strip()) >= 8, f"Quick chip did not fill textarea: {msg_after_chip!r}")
    check("TC-04", page.get_attribute(spec["msg"], "aria-invalid") == "false", "aria-invalid should be false after quick chip")
    mailto_chip = urllib.parse.unquote(page.get_attribute(spec["mailto"], "href") or "")
    check("TC-04", msg_after_chip.strip()[:20] in mailto_chip, "Quick chip content missing from mailto href")
    if spec["check_dedup"]:
        first_chip.click()
        page.wait_for_timeout(40)
        check("TC-04", page.input_value(spec["msg"]) == msg_after_chip, "Option A duplicated identical chip text on repeat click")

    # Reset form inputs cleanly for validation tests
    page.fill(spec["msg"], "")
    page.fill(spec["email"], "")

    # TC-05: Empty submit blocked + focus + #fbStatus untouched
    page.click(spec["submit"])
    page.wait_for_timeout(60)
    err_visible = page.evaluate("""(sel) => {
      const el = document.querySelector(sel);
      return el ? (!el.hidden && getComputedStyle(el).display !== 'none' && el.textContent.trim().length > 0) : false;
    }""", spec["err_el"])
    st_empty = page.evaluate("""(sel) => {
      const el = document.querySelector(sel);
      return !el || el.hidden || el.textContent.trim() === '';
    }""", spec["status"])
    focused_id = page.evaluate("() => document.activeElement ? document.activeElement.id : ''")
    check("TC-05", page.get_attribute(spec["msg"], "aria-invalid") == "true" and err_visible, "Empty submit failed to flag invalid + visible error")
    check("TC-05", focused_id == page.locator(spec["msg"]).get_attribute("id"), f"Empty submit focus={focused_id}, expected textarea")
    check("TC-05", st_empty, "Status banner should stay hidden/empty after invalid submit")

    # TC-06: Short message (< 8 chars) including padded whitespace fails, then recovers live at >= 8 chars
    page.fill(spec["msg"], "1234567")
    page.click(spec["submit"])
    page.wait_for_timeout(60)
    check("TC-06", page.get_attribute(spec["msg"], "aria-invalid") == "true", "7-char message was not rejected on submit")
    page.fill(spec["msg"], "  12345  ")
    page.click(spec["submit"])
    page.wait_for_timeout(60)
    check("TC-06", page.get_attribute(spec["msg"], "aria-invalid") == "true", "Whitespace-padded 5-char message bypassed minlength=8 on submit")
    page.fill(spec["msg"], "12345678")
    page.wait_for_timeout(60)
    check("TC-06", page.get_attribute(spec["msg"], "aria-invalid") == "false", "aria-invalid did not recover live once input reached 8 chars")

    # TC-07: Whitespace-only message (10 spaces) trimmed & rejected
    page.fill(spec["msg"], "          ")
    page.click(spec["submit"])
    page.wait_for_timeout(60)
    check("TC-07", page.get_attribute(spec["msg"], "aria-invalid") == "true", "10-space message was not rejected")

    # TC-08: Invalid email rejected -> empty email allows anonymous submission
    page.fill(spec["msg"], "Muốn đọc bài về phí chuyển tiền quốc tế.")
    page.fill(spec["email"], "khong-phai-email")
    page.click(spec["submit"])
    page.wait_for_timeout(60)
    check("TC-08", page.get_attribute(spec["email"], "aria-invalid") == "true", "Invalid email format was not rejected")
    page.fill(spec["email"], "")
    page.click(spec["submit"])
    page.wait_for_timeout(80)
    st_anon = page.evaluate("""(sel) => {
      const el = document.querySelector(sel);
      return el ? (!el.hidden && el.textContent.trim()) : '';
    }""", spec["status"])
    check("TC-08", page.get_attribute(spec["email"], "aria-invalid") == "false" and len(st_anon) > 0, f"Anonymous submit with empty email failed: {st_anon!r}")

    # TC-09 & TC-10: Valid submit with reply email + HTML XSS payload + mailto dynamic href
    payload = "Kiểm thử <b id='xssTag'>XSS</b> phí MDR 2,2%"
    page.evaluate("() => { window.__xssTriggered = false; }")
    page.fill(spec["msg"], payload)
    page.fill(spec["email"], "duy.qa@duypham.me")
    page.click(spec["submit"])
    page.wait_for_timeout(100)
    st_text = page.locator(spec["status"]).inner_text().strip()
    xss_nodes = page.locator("#xssTag").count()
    mailto_full = urllib.parse.unquote(page.get_attribute(spec["mailto"], "href") or "")
    check("TC-09", len(st_text) > 0 and xss_nodes == 0, f"Valid submit/XSS safety failed: status={st_text!r} xss={xss_nodes}")
    check("TC-09", page.evaluate("() => window.__xssTriggered") is False, "XSS script marker triggered")
    check("TC-10", "mailto:hello@duypham.me" in mailto_full and "duy.qa@duypham.me" in mailto_full and "phí MDR 2,2%" in mailto_full, f"Mailto href missing email/body: {mailto_full}")

    # TC-11: Context banner updates Landing -> Detail view and injects story context into mailto
    if spec["ctx_hidden_on_landing"]:
        check("TC-11", page.locator(spec["ctx"]).is_hidden(), "Option A #fbCtxBanner should start hidden on Landing")
    page.click(spec["detail_btn"])
    page.wait_for_timeout(120)
    ctx_det = page.locator(spec["ctx"])
    ctx_txt = ctx_det.inner_text().strip() if not ctx_det.is_hidden() else ""
    mailto_det = urllib.parse.unquote(page.get_attribute(spec["mailto"], "href") or "")
    check("TC-11", (not ctx_det.is_hidden()) and len(ctx_txt) > 10, f"Context banner did not update/show on Detail view: {ctx_txt!r}")
    check("TC-11", "card" in mailto_det or "10 triệu" in mailto_det or "quẹt thẻ" in mailto_det, f"Detail story context missing in mailto: {mailto_det}")

    # Switch back to Landing for clean layout geometry checks
    page.click(spec["landing_btn"])
    page.wait_for_timeout(80)

    # TC-12: De-boxing & responsive geometry (1440x900 + 390x844)
    for vp_w, vp_h in [(1440, 900), (390, 844)]:
        page.set_viewport_size({"width": vp_w, "height": vp_h})
        page.wait_for_timeout(80)
        geom = page.evaluate("""(hasDock) => {
          const sw = document.documentElement.scrollWidth;
          const cw = document.documentElement.clientWidth;
          const dtCount = document.querySelectorAll('dl.ft-dir dt').length;
          const borderCheck = [
            '.ft-link', '.ft-copy-btn', '.ft-copy', '.fb-chip',
            '#fbMailtoLink', '#fbMailtoLinkA', '#fbMailtoLinkB'
          ].map(s => {
            const el = document.querySelector(s);
            return el ? [s, getComputedStyle(el).borderTopWidth] : null;
          }).filter(Boolean);
          const dock = hasDock ? document.querySelector('.ux-lab-dock') : null;
          return {
            sw, cw, dtCount, borderCheck,
            dockPos: dock ? getComputedStyle(dock).position : null,
          };
        }""", spec["has_dock"])
        check("TC-12", geom["sw"] <= geom["cw"], f"{vp_w}x{vp_h} overflow: scrollWidth={geom['sw']} > clientWidth={geom['cw']}")
        check("TC-12", geom["dtCount"] == spec["expected_dt"], f"{vp_w}x{vp_h} dl.ft-dir dt={geom['dtCount']} != {spec['expected_dt']}")
        for sel_b, bw in geom["borderCheck"]:
            check("TC-12", bw == "0px", f"{vp_w}x{vp_h} {sel_b} borderTopWidth={bw} != 0px")
        if spec["has_dock"]:
            check("TC-12", geom["dockPos"] == "static", f"{vp_w}x{vp_h} .ux-lab-dock position={geom['dockPos']} != static")

    check("TC-09", not console_errs and not page_errs, f"Console/Page errors: console={console_errs} page={page_errs}")
    ctx.close()
    return failures


def main():
    parser = argparse.ArgumentParser(description="E2E functional tests for WMS footer copy icon and feedback form.")
    parser.add_argument("--artifacts", action="store_true", help="Also run suite on Brain HTML artifacts if present.")
    args = parser.parse_args()

    httpd, port = start_ephemeral_server(ROOT)
    base = f"http://127.0.0.1:{port}"
    proto_spec = {
        **SPECS["docs_a"],
        "detail_btn": "#heroStartBtn",
        "landing_btn": "#navBackBtn",
        "has_dock": False,
    }
    targets = [
        ("proto", f"{base}/docs/prototype.html", proto_spec),
        ("docs-option-a", f"{base}/docs/mockup-option-a.html", SPECS["docs_a"]),
        ("docs-landing-detail", f"{base}/docs/landing-detail-mockups.html", SPECS["docs_a"]),
        ("docs-option-b", f"{base}/docs/mockup-option-b.html", SPECS["docs_b"]),
    ]
    if args.artifacts:
        art_a = BRAIN_DIR / "mockup-option-a.html"
        art_b = BRAIN_DIR / "mockup-option-b.html"
        if art_a.is_file():
            targets.append(("artifact-a", f"file://{art_a}", SPECS["art_a"]))
        if art_b.is_file():
            targets.append(("artifact-b", f"file://{art_b}", SPECS["art_b"]))

    all_failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for tname, turl, tspec in targets:
            errs = run_suite_on_target(browser, tname, turl, tspec)
            if errs:
                print(f"FAIL [{tname}]: {len(errs)} assertion(s) failed")
                for e in errs:
                    print(f"  - {e}")
                all_failures.extend(errs)
            else:
                print(f"PASS [{tname}]: TC-01..TC-12 all passed")
        browser.close()

    httpd.shutdown()
    if all_failures:
        print(f"\nSUMMARY: {len(all_failures)} failure(s) across {len(targets)} target(s)")
        return 1
    print(f"\nSUMMARY: PASS — {len(targets) * 12}/{len(targets) * 12} test cases passed ({len(targets)} targets x TC-01..TC-12)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
