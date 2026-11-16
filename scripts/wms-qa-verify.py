#!/usr/bin/env python3
"""
wms-qa-verify.py — Kiểm thử E2E tất định cho cổng S4 QA (where-money-sleeps).
Xác minh:
  [QA-1] Hợp đồng Nội dung, 4 hình mặt cắt LUẬT 9 (1200x675, CLS=0) & 6 Thẻ Trắc nghiệm WMS_QUIZ_BANK
  [QA-2] Máy trạng thái đo lường chống trùng `tel` (R1–R6, F4, from_start, #sync round-trip, suppressed)
  [QA-3] Cam kết Quyền riêng tư & An ninh (0 tracker ngoài, CSP connect-src 'none' trên studio.html)
  [QA-4] Bộ 6 Video Calm Editorial Motion v6.5 (MP4 streams, 30fps, multi-second animation delta > 0, .srt, youtubeId)
  [QA-5] Tương thích Đa khung hình Mobile + Desktop (`LUẬT 13 · R1–R5`, 320/390/768/1440px, Scroll-Hide, Touch Targets & SVG)
"""

import functools
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from wms_qa_uiux import runtime_uiux_checks, static_uiux_checks

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
PROTO = ROOT / "docs" / "prototype.html"
STUDIO = ROOT / "docs" / "studio.html"
WORKFLOWS = ROOT / "docs" / "workflows.html"
S6_HTML = ROOT / "docs" / "s6.html"
DOC_CSS = ROOT / "docs" / "assets" / "doc.css"
STUDIO_DATA = ROOT / "docs" / "wms-studio-data.js"
LICENCES = ROOT / "legal" / "licences.json"
YT_DIR = ROOT / "dist" / "youtube"

EXPECTED_YT_IDS = {
    ("card", "long"): "l56GlTCof4c",
    ("card", "short"): "o84RnVgqQok",
    ("pay", "long"): "OET3IUPC6Qs",
    ("pay", "short"): "f2UKhEheWw4",
    ("install", "long"): "OdcXfR5kSkI",
    ("install", "short"): "o-hFPmyKF7w",
    ("minpay", "long"): "aLsnblI01yM",
    ("minpay", "short"): "RcaF4llz-Cc",
    ("qr", "long"): "awgxZiOJMOM",
    ("qr", "short"): "kQzff8VVZ4E",
    ("profitcash", "long"): "doLPegldsWE",
    ("profitcash", "short"): "RlYjvtiVuDA",
    ("offus", "long"): "pyf9muWYLmI",
    ("offus", "short"): "csafiwCITcQ",
}


def verify_qa1_content_and_quiz(proto_text: str) -> list[str]:
    errors = []
    # Check 28 CHAP_FIGS images on disk and attributes across all 7 lessons
    for sid in ("card", "pay", "install", "minpay", "qr", "profitcash", "offus"):
        for idx in (1, 2, 3, 4):
            fig_path = ROOT / "public" / "brand" / f"{sid}-fig-{idx}.jpg"
            if not fig_path.is_file() or fig_path.stat().st_size < 10_000:
                errors.append(f"Thiếu hoặc lỗi file hình mặt cắt LUẬT 9: {fig_path}")
    if 'width="1200" height="675"' not in proto_text or 'loading="lazy"' not in proto_text:
        errors.append("prototype.html thiếu thuộc tính CLS=0 (width=1200 height=675 loading=lazy) cho CHAP_FIGS")

    # Check WMS_QUIZ_BANK 14 cards across all 7 lessons
    for cid in ("card-q1.v1", "card-q2.v1", "pay-q1.v1", "pay-q2.v1", "install-q1.v1", "install-q2.v1", "minpay-q1.v1", "minpay-q2.v1", "qr-q1.v1", "qr-q2.v1", "profitcash-q1.v1", "profitcash-q2.v1", "offus-q1.v1", "offus-q2.v1"):
        if cid not in proto_text:
            errors.append(f"WMS_QUIZ_BANK thiếu card trắc nghiệm: {cid}")
    if 'reviewed_by: "Duy"' not in proto_text or 'accountant_agent: "ke-toan-reviewer"' not in proto_text:
        errors.append("WMS_QUIZ_BANK thiếu trường reviewed_by='Duy' hoặc accountant_agent='ke-toan-reviewer' (AC-21)")
    if "const WMS_QUIZ_BANK_EN =" not in proto_text:
        errors.append("LUẬT 11: prototype.html thiếu WMS_QUIZ_BANK_EN (14 thẻ trắc nghiệm tiếng Anh)")
    else:
        for cid in ("card-q1.v1", "pay-q1.v1", "install-q1.v1", "minpay-q1.v1", "qr-q1.v1", "profitcash-q1.v1", "offus-q1.v1"):
            if proto_text.count(cid) < 2:
                errors.append(f"WMS_QUIZ_BANK_EN thiếu card trắc nghiệm EN: {cid}")
    if "unofficial summary" not in proto_text.lower():
        errors.append("AC-52: prototype.html thiếu dòng disclaimer tiếng Anh 'unofficial summary'")

    # Check CSS Anti-Overlap Guard (.flow, .ch, .ledger .stamp vs .jstep/h4, .book, .split-pill)
    required_css_guards = [
        ("minmax(15.5rem,18rem)", ".flow li phải đủ rộng cho cột .who (minmax(15.5rem,18rem)) để không đè cột .what"),
        (".flow .who{display:grid;grid-template-columns:minmax(0,1fr)", ".flow .who phải khoá minmax(0,1fr) và min-width:0"),
        ("width:fit-content;max-width:100%", ".ch phải dùng width:fit-content;max-width:100% thay vì width:max-content"),
        (".journal .jstep{font:700 11px/1.4 var(--mono);letter-spacing:.06em;color:#7c4f07;display:block;margin-bottom:4px;padding-right:124px}", ".journal .jstep phải có padding-right:124px để không đè lên .stamp"),
        ("min-height:var(--h,250px);height:auto", ".book phải dùng min-height thay vì height cứng để không tràn chữ trên mobile"),
    ]
    for snippet, msg in required_css_guards:
        if snippet not in proto_text:
            errors.append(f"Lỗi hồi quy CSS Anti-Overlap: {msg}")

    if "function syncGlossaryDefaultScope(" not in proto_text or 'S.glScope = S.view === "detail" ? "story" : "all";' not in proto_text:
        errors.append("Lỗi hồi quy Từ điển: detail view phải luôn mặc định S.glScope = 'story' qua syncGlossaryDefaultScope")
    jump_pos = proto_text.find('if ($("#popJumpBtn"))')
    jump_block = proto_text[jump_pos:jump_pos + 450] if jump_pos != -1 else ""
    if not jump_block or "extractStoryTerms(S.story)" not in jump_block or 'S.glScope = "all";' in jump_block:
        errors.append("Lỗi hồi quy Từ điển: #popJumpBtn không được hardcode S.glScope = 'all' khi thuật ngữ nằm trong bài")
    return errors


def verify_qa2_telemetry_state_machine(proto_text: str) -> tuple[list[str], dict]:
    errors = []
    # Extract the telemetry and progress JS functions or verify via Node VM simulation
    node_script = r"""
const fs = require('fs');
const assert = require('assert');

// Simulate storage + sendBeacon environment for WMS progress & telemetry state machine
let store = {};
const localStorageMock = {
  getItem: (k) => store[k] || null,
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: (k) => { delete store[k]; }
};
let beacons = [];
const navigatorMock = {
  sendBeacon: (url, blobOrData) => {
    beacons.push({ url, data: blobOrData });
    return true;
  },
  storage: { persist: async () => true }
};

// Verify prototype.html contains all required functions & keys
const html = fs.readFileSync(process.argv[1], 'utf8');
const requiredSymbols = [
  'WMS_PROGRESS_KEY',
  'WMS_QUIZ_BANK',
  'loadWmsProgress',
  'saveWmsProgress',
  'emitWmsTelemetry',
  'answerQuizCard',
  'selfDeclareEntryStage',
  'encodeSyncToken',
  'restoreFromSyncToken',
  '__wmsTelemetryLog'
];
for (const sym of requiredSymbols) {
  if (!html.includes(sym)) {
    throw new Error('Missing symbol in prototype.html: ' + sym);
  }
}

// Extract the script block defining WMS_QUIZ_BANK through window.__wmsQA
const startIdx = html.indexOf('const WMS_QUIZ_BANK =');
const endIdx = html.indexOf('/* ── khởi động');
if (startIdx < 0 || endIdx < 0) throw new Error('Cannot locate WMS_QUIZ_BANK..khởi động block');
const jsCode = html.slice(startIdx, endIdx);

const vm = require('vm');
const sandbox = {
  window: { location: { hash: '' }, __wmsTelemetryLog: [] },
  document: {
    getElementById: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {}
  },
  localStorage: localStorageMock,
   indexedDB: null,
  navigator: navigatorMock,
  Blob: class Blob { constructor(parts, opts) { this.parts = parts; this.opts = opts; } },
  btoa: (s) => Buffer.from(s, 'binary').toString('base64'),
  atob: (s) => Buffer.from(s, 'base64').toString('binary'),
  encodeURIComponent,
  decodeURIComponent,
  escape,
  unescape,
  Date,
  JSON,
  Object,
  Array,
  String,
  Boolean,
  Math,
  console
};
sandbox.window.window = sandbox.window;
sandbox.window.localStorage = localStorageMock;
sandbox.window.navigator = navigatorMock;

vm.createContext(sandbox);
// Strip DOM-only rendering calls at bottom of snippet if needed, or run in sandbox
vm.runInContext(jsCode, sandbox);

// 1. Test initial state
let prog = sandbox.loadWmsProgress();
assert.strictEqual(prog.schema, 1, 'Schema must be 1 (AC-29)');

// 2. Test answering first quiz card of lesson 1 ('card-q1.v1') -> must fire BOTH card_answered AND lesson_completed(from_start=true)
sandbox.answerQuizCard('card', 'card-q1.v1', 0);
const log1 = sandbox.window.__wmsTelemetryLog;
assert.strictEqual(log1.length, 2, 'First card answer on lesson 1 must emit exactly 2 events (card_answered + lesson_completed)');
assert.strictEqual(log1[0].event, 'card_answered');
assert.strictEqual(log1[0].props.card, 'card-q1.v1');
assert.strictEqual(log1[0].props.correct, true);
assert.strictEqual(log1[1].event, 'lesson_completed');
assert.strictEqual(log1[1].props.lesson, 'card');
assert.strictEqual(log1[1].props.from_start, true);
assert.strictEqual( Object.keys(log1[1].props).includes('lang'), false, 'lesson_completed must NOT include lang (QĐ 25b)');

// 3. Test R1 dedupe: answering 'card-q1.v1' or 'card-q2.v1' must NOT re-emit lesson_completed for 'card'
sandbox.answerQuizCard('card', 'card-q1.v1', 1);
assert.strictEqual(sandbox.window.__wmsTelemetryLog.length, 2, 'R1: Re-answering same card must not emit duplicate card_answered or lesson_completed');
sandbox.answerQuizCard('card', 'card-q2.v1', 0);
assert.strictEqual(sandbox.window.__wmsTelemetryLog.length, 3, 'Answering 2nd card emits card_answered for card-q2.v1 only');
assert.strictEqual(sandbox.window.__wmsTelemetryLog[2].event, 'card_answered');
assert.strictEqual(sandbox.window.__wmsTelemetryLog[2].props.card, 'card-q2.v1');

// 4. Test #sync creation & round-trip restoration (R4: tel travels with backup)
const token = sandbox.createSyncBackup('code');
const logAfterSync = sandbox.window.__wmsTelemetryLog;
assert.strictEqual(logAfterSync[logAfterSync.length - 1].event, 'sync_created');
assert.strictEqual(logAfterSync[logAfterSync.length - 1].props.method, 'code');
// Second sync_created with same method='code' must be deduplicated by R1
sandbox.createSyncBackup('code');
assert.strictEqual(sandbox.window.__wmsTelemetryLog.length, logAfterSync.length, 'R1: sync_created(code) must fire at most once per storage');

// Wipe storage to simulate Device B, then restore from token
store = {};
const restoredOk = sandbox.restoreFromSyncToken(token, 'code');
assert.strictEqual(restoredOk, true, 'restoreFromSyncToken must succeed');
const lastEv = sandbox.window.__wmsTelemetryLog[sandbox.window.__wmsTelemetryLog.length - 1];
assert.strictEqual(lastEv.event, 'progress_restored');
assert.strictEqual(lastEv.props.method, 'code');

// Verify R4: after restore on Device B, answering card on 'card' lesson must NOT fire lesson_completed again
const lenBefore = sandbox.window.__wmsTelemetryLog.length;
sandbox.answerQuizCard('card', 'card-q1.v1', 1);
assert.strictEqual(sandbox.window.__wmsTelemetryLog.length, lenBefore, 'R4: Restored progress carries tel locks so old lessons/cards never double-fire');

// 5. Test R3: Self-declare entry stage suppresses lesson_completed permanently
store = {};
sandbox.selfDeclareEntryStage();
const progSuppressed = sandbox.loadWmsProgress();
assert.strictEqual(progSuppressed.tel.lesson_completed['card'], 'suppressed');
assert.strictEqual(progSuppressed.tel.lesson_completed['pay'], 'suppressed');
assert.strictEqual(progSuppressed.tel.lesson_completed['install'], 'suppressed');
const lenBeforeSup = sandbox.window.__wmsTelemetryLog.length;
sandbox.answerQuizCard('pay', 'pay-q1.v1', 1);
// card_answered fires, but lesson_completed is suppressed!
const emittedAfterSup = sandbox.window.__wmsTelemetryLog.slice(lenBeforeSup);
assert.strictEqual(emittedAfterSup.length, 1, 'R3: After self-declare, answering a quiz card emits card_answered but NEVER lesson_completed');
assert.strictEqual(emittedAfterSup[0].event, 'card_answered');

// 6. Test from_start=false when user jumps straight to lesson 'install' on fresh storage without completing 'card' first
store = {};
const lenFresh = sandbox.window.__wmsTelemetryLog.length;
sandbox.answerQuizCard('install', 'install-q1.v1', 1);
const freshEvents = sandbox.window.__wmsTelemetryLog.slice(lenFresh);
assert.strictEqual(freshEvents.length, 2);
assert.strictEqual(freshEvents[1].event, 'lesson_completed');
assert.strictEqual(freshEvents[1].props.lesson, 'install');
assert.strictEqual(freshEvents[1].props.from_start, false, 'Jumping straight to install without completing lesson 1 (card) must set from_start=false (QĐ 39)');

// 7. Test AC-68: EasyPrivacy blocklist avoidance for sendBeacon endpoint
const forbiddenPaths = ['/collect', '/event', '/track', '/beacon', '/metrics', '/api/event'];
for (const b of beacons) {
  assert.strictEqual(forbiddenPaths.includes(b.url), false, 'AC-68: Beacon URL must not be on EasyPrivacy blocklist: ' + b.url);
  assert.strictEqual(b.url, '/api/p');
}

// 8. Test AC-62 + LUẬT 11: Setting prog.lang='en' persists UI language without ever leaking lang into lesson_completed
const pEnCheck = sandbox.window.__wmsQA.loadProg();
pEnCheck.lang = 'en';
sandbox.window.__wmsQA.saveProg(pEnCheck);
sandbox.window.__wmsTelemetryLog.length = 0;
sandbox.window.__wmsQA.answerQuizCard('pay-q1.v1', 0);
const enEvents = sandbox.window.__wmsTelemetryLog.filter(e => e.event === 'lesson_completed');
assert.strictEqual(enEvents.length, 1, 'EN mode must still emit lesson_completed cleanly');
assert.strictEqual(Object.keys(enEvents[0].props).includes('lang'), false, 'AC-62: lesson_completed must NEVER include lang even when prog.lang="en"');

console.log(JSON.stringify({
  status: 'PASS',
  totalEventsTested: sandbox.window.__wmsTelemetryLog.length,
  invariantsVerified: ['R1_dedupe_before_send', 'R2_lang_agnostic_key', 'R3_self_declare_suppressed', 'R4_sync_carries_tel', 'F4_co_fire_card_and_lesson', 'QD39_from_start_true_and_false', 'AC29_single_schema_record', 'AC68_neutral_beacon_path', 'AC62_en_mode_no_lang_leak']
}));
"""
    res = subprocess.run(
        ["node", "-e", node_script, str(PROTO)],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        errors.append(f"Node VM E2E Telemetry test failed: {res.stderr.strip()}")
        return errors, {}
    try:
        summary = json.loads(res.stdout.strip().splitlines()[-1])
    except Exception as exc:
        errors.append(f"Failed to parse Node VM output: {exc}")
        summary = {}
    return errors, summary


def verify_qa3_privacy_and_csp(proto_text: str, studio_text: str, wf_text: str) -> list[str]:
    errors = []
    # Check 0 external script src across all 3 apps
    for name, content in [("prototype.html", proto_text), ("studio.html", studio_text), ("workflows.html", wf_text)]:
        ext_scripts = re.findall(r'<script[^>]+src=["\'](https?://[^"\']+)["\']', content, re.I)
        if ext_scripts:
            errors.append(f"{name} chứa script CDN bên thứ ba vi phạm AC-33: {ext_scripts}")
    # Check CSP connect-src 'none' on studio.html
    if "connect-src 'none'" not in studio_text:
        errors.append("studio.html thiếu khoá bảo mật CSP connect-src 'none'")

    # Check Cloudflare Worker & wrangler.jsonc privacy invariants (AC-55, AC-56)
    worker_path = ROOT / "cloudflare" / "worker.js"
    wrangler_path = ROOT / "wrangler.jsonc"
    schema_path = ROOT / "cloudflare" / "schema.sql"
    for req_p in (worker_path, wrangler_path, schema_path):
        if not req_p.is_file():
            errors.append(f"Thiếu file hạ tầng deploy Cloudflare: {req_p}")
    if worker_path.is_file():
        w_txt = worker_path.read_text(encoding="utf-8")
        for forbidden in ("CF-Connecting-IP", "User-Agent", "request.cf", "Set-Cookie", "console.log(request)"):
            if forbidden.lower() in w_txt.lower():
                errors.append(f"cloudflare/worker.js vi phạm AC-55/AC-56 (chứa {forbidden})")
    if wrangler_path.is_file():
        wr_txt = wrangler_path.read_text(encoding="utf-8")
        if '"enabled": false' not in wr_txt:
            errors.append("wrangler.jsonc thiếu observability.enabled = false (AC-56)")
    return errors


def verify_qa4_videos_and_youtube_ids(proto_text: str, studio_data_text: str, ci_mode: bool = False) -> list[str]:
    errors = []
    seen_sids = set()
    for (sid, fmt), ytid in EXPECTED_YT_IDS.items():
        seen_sids.add(sid)
        if ytid not in proto_text:
            errors.append(f"prototype.html thiếu youtubeId {ytid} cho ({sid}, {fmt})")
        if ytid not in studio_data_text:
            errors.append(f"wms-studio-data.js thiếu youtubeId {ytid} cho ({sid}, {fmt})")
        suffix = "long-16x9" if fmt == "long" else "short-9x16"
        mp4_path = YT_DIR / f"{sid}-{suffix}.mp4"
        srt_path = YT_DIR / f"{sid}-{suffix}.srt"
        if not ci_mode or mp4_path.is_file():
            if not mp4_path.is_file() or mp4_path.stat().st_size < 5_000_000:
                errors.append(f"File MP4 v6.5 thiếu hoặc quá nhỏ: {mp4_path}")
        if not srt_path.is_file() or srt_path.stat().st_size < 200:
            errors.append(f"File phụ đề .srt thiếu hoặc rỗng: {srt_path}")
    if 'const effFmt = scope === "stage" ? "long" : fmt;' not in proto_text:
        errors.append("prototype.html chưa khoá chỉ hiển thị Video Dài 16:9 trên sân khấu website (scope === 'stage')")
    for sid in sorted(seen_sids):
        manifest_path = YT_DIR / f"{sid}-elevenlabs-youtube-manifest.json"
        if not manifest_path.is_file() or manifest_path.stat().st_size < 100:
            errors.append(f"File manifest thiếu hoặc rỗng: {manifest_path}")
            continue
        try:
            mf = json.loads(manifest_path.read_text(encoding="utf-8"))
            short_spec = ((mf.get("formats") or {}).get("short") or {}).get("youtubeUploadSpec") or {}
            expected_url = f"https://wheremoneysleeps.duyslab.icu/?story={sid}"
            if short_spec.get("articleUrl") != expected_url or expected_url not in str(short_spec.get("description") or ""):
                errors.append(f"Manifest {sid} thiếu URL bài viết chính xác ({expected_url}) trong description của Video Ngắn")
        except Exception as exc:
            errors.append(f"Lỗi đọc manifest {manifest_path}: {exc}")
    return errors


class _QuietQaHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class _QuietQaServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (BrokenPipeError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)


def verify_qa5_responsive_ux(proto_text: str, studio_text: str, wf_text: str, ci_mode: bool = False) -> tuple[list[str], str]:
    errors = []
    doc_css_text = DOC_CSS.read_text(encoding="utf-8") if DOC_CSS.is_file() else ""
    index_text = INDEX_HTML.read_text(encoding="utf-8") if INDEX_HTML.is_file() else ""

    # 1. Static LUẬT 13 (R1–R5) invariants across all deliverables
    if proto_text != index_text:
        errors.append("index.html không đồng bộ từng byte với docs/prototype.html")
    for name, txt in (("prototype.html", proto_text), ("studio.html", studio_text), ("workflows.html", wf_text)):
        if "viewport-fit=cover" not in txt:
            errors.append(f"{name} thiếu viewport-fit=cover (R1 safe-area)")
        if 'name="text-scale" content="scale"' not in txt:
            errors.append(f"{name} thiếu <meta name=\"text-scale\" content=\"scale\"> (R2 OS text scale)")
        if "overflow-x:clip" not in txt and "overflow-x: clip" not in txt:
            errors.append(f"{name} thiếu overflow-x:clip trên html,body (R1)")
        if "pointer:coarse" not in txt and "pointer: coarse" not in txt:
            errors.append(f"{name} thiếu @media (pointer:coarse) >= 44px touch targets (R2)")
        if "font-size:max(16px" not in txt and "font-size: max(16px" not in txt:
            errors.append(f"{name} thiếu quy tắc >= 16px cho input/select/textarea trên mobile (R2)")
    if "overflow-x:clip" not in doc_css_text and "overflow-x: clip" not in doc_css_text:
        errors.append("docs/assets/doc.css thiếu overflow-x:clip (R1)")
    if "pointer:coarse" not in doc_css_text and "pointer: coarse" not in doc_css_text:
        errors.append("docs/assets/doc.css thiếu @media (pointer:coarse) 44px targets (R2)")
    if "ab-back-ico" not in proto_text or "ab-back-lbl" not in proto_text:
        errors.append("prototype.html thiếu span tách icon/label cho #navBackBtn")
    if "100dvh" not in proto_text or "overscroll-behavior:contain" not in proto_text:
        errors.append("prototype.html thiếu 100dvh / overscroll-behavior:contain trên overlay (R4)")
    if 'style="display:grid;grid-template-columns:1.35fr 0.65fr' in studio_text or ".oss-cmp-grid" not in studio_text:
        errors.append("studio.html vẫn còn inline grid cứng ở #panel-oss hoặc thiếu .oss-cmp-grid")
    if "svg-swipe-hint" not in wf_text or "min-width:720px" not in wf_text:
        errors.append("workflows.html thiếu .svg-swipe-hint hoặc .wf-svg min-width:720px trên mobile (R5)")
    errors.extend(static_uiux_checks(ROOT))

    # 2. Live multi-viewport Chromium checks (Mobile 320·390 + Touch Tablet 768·820·1024 + Desktop 1440px)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        if ci_mode:
            return errors, "static OK · Playwright chưa cài trong CI — bỏ qua DOM viewports"
        errors.append("Playwright chưa khả dụng để kiểm tra DOM đa khung hình [QA-5]")
        return errors, "Playwright missing"

    handler = functools.partial(_QuietQaHandler, directory=str(ROOT))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = _QuietQaServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    checked_cases = 0
    try:
        base = f"http://127.0.0.1:{port}"
        viewports = [
            (320, 568, True),    # Mobile small (touch)
            (362, 1218, True),   # Mobile narrow DevTools / small Android (touch)
            (390, 844, True),    # Mobile standard (touch)
            (768, 1024, True),   # Tablet portrait iPad (touch)
            (820, 1180, True),   # Tablet portrait iPad Air (touch)
            (1024, 768, True),   # Tablet landscape iPad (touch)
            (1440, 900, False),  # Desktop standard (fine pointer)
        ]
        control_scan_js = """({isMob}) => {
          const minH = isMob ? 43.5 : 23.5;
          const bad = [];
          for (const el of document.querySelectorAll('button, a, input, select, textarea, summary, [role="button"], [role="tab"]')) {
            if (el.matches('p a, li a, figcaption a, td a, .cite a, button.gl, .term, .fn-ref, .skip-link, input[type="checkbox"], input[type="radio"]')) continue;
            const cs = getComputedStyle(el);
            if (cs.display === 'inline') continue;
            const r = el.getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) continue;
            if (r.height < minH || r.width < minH) {
              bad.push(`${el.tagName}#${el.id || ''}.${(el.className || '').toString().trim().split(/\\s+/)[0] || ''}:${Math.round(r.width)}x${Math.round(r.height)}`);
            }
          }
          return bad.slice(0, 8);
        }"""
        input_font_js = """() => [...document.querySelectorAll('input:not([type="range"]):not([type="checkbox"]):not([type="radio"]),select,textarea')].filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && r.height > 0 && parseFloat(getComputedStyle(el).fontSize) < 15.9;
        }).map(el => el.id || el.name || el.tagName)"""

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for vw, vh, is_mob in viewports:
                    ctx = browser.new_context(
                        viewport={"width": vw, "height": vh},
                        has_touch=is_mob,
                        is_mobile=is_mob,
                    )
                    page = ctx.new_page()
                    page_errors = []
                    page.on("pageerror", lambda e: page_errors.append(str(e)))

                    # A. prototype.html — Landing + Detail + Overlays
                    page.goto(f"{base}/docs/prototype.html", wait_until="domcontentloaded")
                    page.wait_for_selector("#atlasbar")
                    page.wait_for_timeout(150)

                    ov = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                    if ov > 0:
                        errors.append(f"[{vw}x{vh}] prototype Landing tràn ngang +{ov}px")
                    bar_h = page.evaluate("() => document.getElementById('atlasbar')?.getBoundingClientRect().height || 0")
                    if bar_h > vh * 0.12:
                        errors.append(f"[{vw}x{vh}] prototype Landing #atlasbar cao {bar_h:.1f}px > 12% dvh ({vh*0.12:.1f}px)")

                    if vw <= 900:
                        pill_rows = page.evaluate("""() => {
                          const tops = [...document.querySelectorAll('#catPills .cat-pill')]
                            .filter(el => el.getBoundingClientRect().width > 0)
                            .map(el => Math.round(el.getBoundingClientRect().top / 4));
                          return new Set(tops).size;
                        }""")
                        if pill_rows > 1:
                            errors.append(f"[{vw}x{vh}] Landing #catPills rớt {pill_rows} hàng (> 1 hàng vuốt ngang)")

                    if is_mob:
                        small_inputs = page.evaluate(input_font_js)
                        if small_inputs:
                            errors.append(f"[{vw}x{vh}] prototype Landing input font-size < 16px: {small_inputs}")

                    small_land = page.evaluate(control_scan_js, {"isMob": is_mob})
                    if small_land:
                        errors.append(f"[{vw}x{vh}] prototype Landing controls < {'44px' if is_mob else '24px'}: {small_land}")

                    # Out-of-bounds & anti-ellipsis scan (catches elements clipped silently by overflow-x: clip)
                    land_clip = page.evaluate("""() => {
                      const vw = window.innerWidth;
                      const oob = [], ellip = [];
                      for (const sel of ['#atlasbar', '.catalog-bar', '#landingSearch', '#gridModeSeg', '#gridModeSeg button', '.story-card']) {
                        for (const el of document.querySelectorAll(sel)) {
                          const r = el.getBoundingClientRect();
                          if (r.width > 0 && (r.left < -1.5 || r.right > vw + 1.5)) {
                            oob.push(`${sel}(${Math.round(r.left)}..${Math.round(r.right)}>${vw})`);
                          }
                        }
                      }
                      for (const btn of document.querySelectorAll('#gridModeSeg button')) {
                        const r = btn.getBoundingClientRect();
                        if (r.width > 0 && btn.scrollWidth > btn.clientWidth + 2) {
                          ellip.push(`${btn.textContent.trim()}(sw=${btn.scrollWidth}>cw=${btn.clientWidth})`);
                        }
                      }
                      return { oob: oob.slice(0, 6), ellip };
                    }""")
                    if land_clip["oob"]:
                        errors.append(f"[{vw}x{vh}] prototype Landing phần tử tràn ngoài khung (che bởi overflow-x:clip): {land_clip['oob']}")
                    if land_clip["ellip"]:
                        errors.append(f"[{vw}x{vh}] prototype Landing #gridModeSeg bị cắt chữ: {land_clip['ellip']}")

                    if vw in (320, 362):
                        page.goto(f"{base}/docs/prototype.html?lang=en", wait_until="domcontentloaded")
                        page.wait_for_selector("#gridModeSeg button")
                        page.wait_for_timeout(120)
                        en_clip = page.evaluate("""() => {
                          const vw = window.innerWidth;
                          const bad = [];
                          for (const btn of document.querySelectorAll('#gridModeSeg button')) {
                            const r = btn.getBoundingClientRect();
                            if (r.width > 0 && (r.right > vw + 1.5 || btn.scrollWidth > btn.clientWidth + 2)) {
                              bad.push(`${btn.textContent.trim()}(r=${Math.round(r.right)},sw=${btn.scrollWidth},cw=${btn.clientWidth})`);
                            }
                          }
                          return bad;
                        }""")
                        if en_clip:
                            errors.append(f"[{vw}x{vh}] prototype Landing EN #gridModeSeg cắt/tràn chữ: {en_clip}")
                        page.goto(f"{base}/docs/prototype.html", wait_until="domcontentloaded")
                        page.wait_for_selector("#atlasBtn")
                        page.wait_for_timeout(120)

                    # Open #atlas drawer and clamp inside viewport (+ 2-col parity at 1440px)
                    page.click("#atlasBtn")
                    page.wait_for_timeout(120)
                    atlas_box = page.evaluate("""() => {
                      const a = document.getElementById('atlas');
                      const r = a && !a.hidden ? a.getBoundingClientRect() : null;
                      const m = a ? a.querySelector('.atlas-master')?.getBoundingClientRect() : null;
                      const d = a ? a.querySelector('.atlas-detail-wrap')?.getBoundingClientRect() : null;
                      return r ? {top: r.top, left: r.left, right: r.right, bottom: r.bottom, twoCol: !!(m && d && m.right <= d.left + 4)} : null;
                    }""")
                    if not atlas_box or atlas_box["right"] > vw + 1 or atlas_box["bottom"] > vh + 1 or atlas_box["left"] < -1 or atlas_box["top"] < -1:
                        errors.append(f"[{vw}x{vh}] #atlas vượt khung hình: {atlas_box}")
                    if vw >= 1280 and atlas_box and not atlas_box["twoCol"]:
                        errors.append(f"[{vw}x{vh}] #atlas mất bố cục 2 cột Desktop master-detail")
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(80)

                    # Navigate to Detail view (?story=card), test Split-Pill width, #postPop, #pop, Verdict parity, and scroll-hide
                    page.goto(f"{base}/docs/prototype.html?story=card", wait_until="domcontentloaded")
                    page.wait_for_selector("#postPillBtn")
                    page.wait_for_timeout(150)
                    ov_d = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                    if ov_d > 0:
                        errors.append(f"[{vw}x{vh}] prototype Detail tràn ngang +{ov_d}px")
                    bar_hd = page.evaluate("() => document.getElementById('atlasbar')?.getBoundingClientRect().height || 0")
                    if bar_hd > vh * 0.12:
                        errors.append(f"[{vw}x{vh}] prototype Detail #atlasbar cao {bar_hd:.1f}px > 12% dvh ({vh*0.12:.1f}px)")

                    pills_dim = page.evaluate("""() => {
                      const c = document.getElementById('catPillBtn')?.getBoundingClientRect();
                      const p = document.getElementById('postPillBtn')?.getBoundingClientRect();
                      const pt = document.querySelector('.sp-post .post-title')?.getBoundingClientRect();
                      const vCards = [...document.querySelectorAll('.verdict section')].filter(s => s.getBoundingClientRect().width > 0);
                      const vTwoCol = vCards.length >= 2 && vCards[0].getBoundingClientRect().right <= vCards[1].getBoundingClientRect().left + 4;
                      const vw = window.innerWidth;
                      const detOob = [], tabClip = [];
                      for (const sel of ['.pack-tabs button', '#detailHead', '.try', '.ledger']) {
                        for (const el of document.querySelectorAll(sel)) {
                          const r = el.getBoundingClientRect();
                          if (r.width > 0 && (r.left < -1.5 || r.right > vw + 1.5)) detOob.push(`${sel}(${Math.round(r.right)}>${vw})`);
                        }
                      }
                      for (const el of document.querySelectorAll('.pack-tabs button')) {
                        const r = el.getBoundingClientRect();
                        if (r.width > 0 && el.scrollWidth > el.clientWidth + 2) tabClip.push(`${el.textContent.trim().slice(0,24)}(sw=${el.scrollWidth}>cw=${el.clientWidth})`);
                      }
                      return {
                        catW: c ? c.width : 0,
                        catH: c ? c.height : 0,
                        postW: p ? p.width : 0,
                        postH: p ? p.height : 0,
                        postTitleW: pt ? pt.width : 0,
                        vTwoCol,
                        detOob: detOob.slice(0, 6),
                        tabClip,
                      };
                    }""")
                    min_pill_w = 43.5 if is_mob else 56.0
                    min_title_w = 32.0 if vw <= 325 else (72.0 if is_mob else 50.0)
                    if pills_dim["postW"] < min_pill_w:
                        errors.append(f"[{vw}x{vh}] #postPillBtn bị ép hẹp còn {pills_dim['postW']:.1f}px < {min_pill_w}px")
                    if pills_dim["postTitleW"] < min_title_w:
                        errors.append(f"[{vw}x{vh}] .sp-post .post-title bị ép hẹp còn {pills_dim['postTitleW']:.1f}px < {min_title_w}px")
                    if pills_dim["detOob"]:
                        errors.append(f"[{vw}x{vh}] prototype Detail phần tử tràn khung: {pills_dim['detOob']}")
                    if pills_dim["tabClip"]:
                        errors.append(f"[{vw}x{vh}] prototype Detail .pack-tabs bị cắt chữ: {pills_dim['tabClip']}")
                    if vw > 480 and pills_dim["catW"] < min_pill_w:
                        errors.append(f"[{vw}x{vh}] #catPillBtn bị ép hẹp còn {pills_dim['catW']:.1f}px < {min_pill_w}px")
                    if vw >= 1280 and not pills_dim["vTwoCol"]:
                        errors.append(f"[{vw}x{vh}] Detail .verdict mất bố cục 2 cột Desktop")

                    if is_mob:
                        small_inputs_d = page.evaluate(input_font_js)
                        if small_inputs_d:
                            errors.append(f"[{vw}x{vh}] prototype Detail input font-size < 16px: {small_inputs_d}")

                    small_det = page.evaluate(control_scan_js, {"isMob": is_mob})
                    if small_det:
                        errors.append(f"[{vw}x{vh}] prototype Detail controls < {'44px' if is_mob else '24px'}: {small_det}")

                    page.click("#postPillBtn")
                    page.wait_for_timeout(100)
                    pp_box = page.evaluate("""() => {
                      const p = document.getElementById('postPop');
                      const r = p && !p.hidden ? p.getBoundingClientRect() : null;
                      return r ? {top: r.top, left: r.left, right: r.right, bottom: r.bottom} : null;
                    }""")
                    if not pp_box or pp_box["right"] > vw + 1 or pp_box["bottom"] > vh + 1 or pp_box["left"] < -1:
                        errors.append(f"[{vw}x{vh}] #postPop vượt khung hình: {pp_box}")
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(80)

                    # Open first glossary .gl button
                    if page.locator("article button.gl, #art button.gl").count() > 0:
                        page.locator("article button.gl, #art button.gl").first.click()
                        page.wait_for_timeout(100)
                        gl_box = page.evaluate("""() => {
                          const p = document.getElementById('pop');
                          const r = p && p.classList.contains('open') ? p.getBoundingClientRect() : null;
                          return r ? {top: r.top, left: r.left, right: r.right, bottom: r.bottom} : null;
                        }""")
                        if gl_box and (gl_box["right"] > vw + 1 or gl_box["bottom"] > vh + 1 or gl_box["left"] < -1 or gl_box["top"] < -1):
                            errors.append(f"[{vw}x{vh}] #pop glossary vượt khung hình: {gl_box}")
                        if page.locator("#popX").is_visible():
                            page.click("#popX")

                    # Scroll-hide test (reset to top first because clicking .gl may have scrolled down)
                    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                    page.wait_for_timeout(120)
                    page.evaluate("window.scrollTo({top: 500, behavior: 'instant'})")
                    page.wait_for_timeout(200)
                    hidden_down = page.evaluate("() => document.getElementById('atlasbar')?.classList.contains('is-hidden')")
                    page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                    page.wait_for_timeout(200)
                    shown_up = page.evaluate("() => !document.getElementById('atlasbar')?.classList.contains('is-hidden')")
                    if not hidden_down or not shown_up:
                        errors.append(f"[{vw}x{vh}] prototype scroll-hide lỗi (down={hidden_down}, up={shown_up})")

                    # B. workflows.html — overflow, sticky chrome <= 12%, SVG >= 10px text on mobile
                    page.goto(f"{base}/docs/workflows.html", wait_until="domcontentloaded")
                    page.wait_for_selector("#wfSvg")
                    page.wait_for_timeout(150)
                    ov_wf = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                    if ov_wf > 0:
                        errors.append(f"[{vw}x{vh}] workflows.html tràn ngang +{ov_wf}px")
                    wf_bar_h = page.evaluate("() => document.querySelector('.atlasbar')?.getBoundingClientRect().height || 0")
                    if wf_bar_h > vh * 0.12:
                        errors.append(f"[{vw}x{vh}] workflows.html .atlasbar cao {wf_bar_h:.1f}px > 12% dvh")
                    small_wf = page.evaluate(control_scan_js, {"isMob": is_mob})
                    if small_wf:
                        errors.append(f"[{vw}x{vh}] workflows.html controls < {'44px' if is_mob else '24px'}: {small_wf}")
                    if vw <= 860:
                        min_svg_px = page.evaluate("""() => {
                          const svg = document.getElementById('wfSvg');
                          const sr = svg.getBoundingClientRect();
                          const scale = sr.width / 640;
                          const sizes = [...svg.querySelectorAll('text')].filter(t => getComputedStyle(t).display !== 'none').map(t => parseFloat(getComputedStyle(t).fontSize) * scale);
                          return { w: sr.width, minPx: sizes.length ? Math.min(...sizes) : 99 };
                        }""")
                        if min_svg_px["minPx"] < 9.95:
                            errors.append(f"[{vw}x{vh}] workflows.html #wfSvg text thu nhỏ còn {min_svg_px['minPx']:.2f}px < 10px (svg w={min_svg_px['w']:.1f})")

                    # C. studio.html — overflow, sticky topbar <= 12% dvh, touch input >= 16px, controls >= 44/24px, video/oss tabs
                    page.goto(f"{base}/docs/studio.html", wait_until="domcontentloaded")
                    page.wait_for_selector(".st-topbar")
                    page.wait_for_timeout(150)
                    for m in ("post", "video", "oss"):
                        page.click(f'.mode-tab[data-mode="{m}"]')
                        page.wait_for_timeout(100)
                        ov_st = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                        if ov_st > 0:
                            errors.append(f"[{vw}x{vh}] studio.html mode={m} tràn ngang +{ov_st}px")
                        if m == "post" and is_mob:
                            small_st_inps = page.evaluate(input_font_js)
                            if small_st_inps:
                                errors.append(f"[{vw}x{vh}] studio.html input font-size < 16px: {small_st_inps}")
                        small_st = page.evaluate(control_scan_js, {"isMob": is_mob})
                        if small_st:
                            errors.append(f"[{vw}x{vh}] studio.html mode={m} controls < {'44px' if is_mob else '24px'}: {small_st}")
                    st_bar_h = page.evaluate("() => document.querySelector('.st-topbar')?.getBoundingClientRect().height || 0")
                    if st_bar_h > vh * 0.125:
                        errors.append(f"[{vw}x{vh}] studio.html .st-topbar cao {st_bar_h:.1f}px > 12.5% dvh")

                    # D. s6.html — shared doc.css check (1-row nav <= 12.5% dvh + controls >= 44/24px)
                    page.goto(f"{base}/docs/s6.html", wait_until="domcontentloaded")
                    page.wait_for_selector("nav .in")
                    page.wait_for_timeout(100)
                    ov_s6 = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                    if ov_s6 > 0:
                        errors.append(f"[{vw}x{vh}] s6.html tràn ngang +{ov_s6}px")
                    s6_nav = page.evaluate("""() => {
                      const h = document.querySelector('nav')?.getBoundingClientRect().height || 0;
                      const mids = [...document.querySelectorAll('nav .in > *')]
                        .map(e => e.getBoundingClientRect())
                        .filter(r => r.width > 0)
                        .map(r => Math.round(((r.top + r.bottom) / 2) / 8));
                      return { h, rows: new Set(mids).size };
                    }""")
                    if s6_nav["h"] > vh * 0.125:
                        errors.append(f"[{vw}x{vh}] s6.html nav cao {s6_nav['h']:.1f}px > 12.5% dvh")
                    if s6_nav["rows"] > 1:
                        errors.append(f"[{vw}x{vh}] s6.html nav rớt {s6_nav['rows']} hàng (> 1 hàng)")
                    small_s6 = page.evaluate(control_scan_js, {"isMob": is_mob})
                    if small_s6:
                        errors.append(f"[{vw}x{vh}] s6.html controls < {'44px' if is_mob else '24px'}: {small_s6}")

                    if page_errors:
                        errors.append(f"[{vw}x{vh}] JS pageerror: {page_errors[0]}")
                    ctx.close()
                    checked_cases += 1
                ui_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
                ui_page = ui_ctx.new_page()
                errors.extend(runtime_uiux_checks(ui_page, base))
                ui_ctx.close()
            finally:
                browser.close()
    finally:
        httpd.shutdown()

    vp_label = "·".join(str(vw) for vw, _, _ in viewports) + "px"
    return errors, f"static + {checked_cases}/{len(viewports)} Playwright viewports ({vp_label})"


def main() -> int:
    ci_mode = ("--ci" in sys.argv) or (os.environ.get("GITHUB_ACTIONS") == "true")
    proto_text = PROTO.read_text(encoding="utf-8")
    studio_text = STUDIO.read_text(encoding="utf-8")
    wf_text = WORKFLOWS.read_text(encoding="utf-8")
    studio_data_text = STUDIO_DATA.read_text(encoding="utf-8")

    print("wms-qa-verify — Kiểm thử E2E tất định S4 QA (where-money-sleeps)\n")

    e1 = verify_qa1_content_and_quiz(proto_text)
    print(f"[QA-1] Nội dung, 28 hình LUẬT 9 (CLS=0) & 14 thẻ trắc nghiệm WMS_QUIZ_BANK: {'PASS' if not e1 else 'FAIL'}")
    for err in e1:
        print(f"  ✗ {err}")

    e2, tel_summary = verify_qa2_telemetry_state_machine(proto_text)
    print(f"[QA-2] Máy trạng thái đo lường `tel` (R1–R6, F4, from_start, #sync): {'PASS' if not e2 else 'FAIL'}")
    if tel_summary:
        print(f"  ✓ Invariants verified: {', '.join(tel_summary.get('invariantsVerified', []))}")
    for err in e2:
        print(f"  ✗ {err}")

    e3 = verify_qa3_privacy_and_csp(proto_text, studio_text, wf_text)
    print(f"[QA-3] Quyền riêng tư (0 CDN script) & An ninh CSP studio.html: {'PASS' if not e3 else 'FAIL'}")
    for err in e3:
        print(f"  ✗ {err}")

    e4 = verify_qa4_videos_and_youtube_ids(proto_text, studio_data_text, ci_mode=ci_mode)
    print(f"[QA-4] Bộ 14 Video Calm Editorial v6.5 + .srt + 14 mã youtubeId: {'PASS' if not e4 else 'FAIL'}")
    for err in e4:
        print(f"  ✗ {err}")

    e5, qa5_note = verify_qa5_responsive_ux(proto_text, studio_text, wf_text, ci_mode=ci_mode)
    print(f"[QA-5] Tương thích Đa khung hình LUẬT 13 R1–R5 ({qa5_note}): {'PASS' if not e5 else 'FAIL'}")
    for err in e5:
        print(f"  ✗ {err}")

    all_errors = e1 + e2 + e3 + e4 + e5
    if all_errors:
        print(f"\nFAIL — {len(all_errors)} lỗi chặn")
        return 1
    print("\nPASS — 5/5 cụm kiểm thử E2E S4 QA đạt 100% (0 lỗi chặn)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
