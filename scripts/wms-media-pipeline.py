#!/usr/bin/env python3
"""
wms-media-pipeline.py — Pipeline tự động Bước 5 (QĐ 56) cho Where Money Sleeps:
  5A. Build Audio + Timestamp + SFX từ ElevenLabs API (/v1/text-to-speech/{voice_id}/with-timestamps
      & /v1/sound-generation) có bộ nhớ đệm SHA-256 (.cache/elevenlabs/).
  5B. Hợp nhất Video Diorama v3.0 2 định dạng:
      - YouTube Dài 16:9 (1920×1080, 8–10 phút)
      - YouTube Shorts 9:16 (1080×1920, 60–90 giây)
      chuẩn âm lượng phát sóng YouTube (-14 LUFS, true peak <= -1.0 dBTP).
  5C. Upload lên YouTube qua YouTube Data API v3 (videos.insert):
      - Khi bài đang ở `status: "review"` (chưa được Duy duyệt đăng), BẮT BUỘC đặt
        `privacyStatus = "unlisted"` (hoặc `"private"`), TUYỆT ĐỐI CẤM `"public"`.
      - Nhờ `"unlisted"`, video nhận ngay `youtubeId` 11 ký tự và nhúng xem thử được
        trực tiếp trong bài viết ở chế độ `?preview=1` mà không lộ công khai trên kênh.
  5D. Nhúng ngược `youtubeId` + `embedStatus` vào `STORIES[<khoá>].videoScript.long`
      và `STORIES[<khoá>].videoScript.short` trong `docs/prototype.html` để trình phát
      YouTube (`youtube-nocookie.com/embed/<youtubeId>`) hiển thị ngay trong bài viết.

Cách gọi:
  python3 -I scripts/wms-media-pipeline.py --story <slug> --mode dry-run
  python3 -I scripts/wms-media-pipeline.py --story <slug> --mode live
  python3 -I scripts/wms-media-pipeline.py --story <slug> --bind-long-id <11char> --bind-short-id <11char> --embed-status uploaded_unlisted
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import http.server
import importlib.util
import json
import os
import pathlib
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "docs/prototype.html"
LICENCES_JSON = ROOT / "legal/licences.json"
ENV_FILE = ROOT / ".env"
CACHE_DIR = ROOT / ".cache/elevenlabs"
VEO_CACHE_DIR = ROOT / ".cache/google-veo"
DIST_DIR = ROOT / "dist/youtube"

YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
VALID_EMBED_STATUS = {"pending_upload", "uploaded_unlisted", "uploaded_private", "uploaded_public"}
VALID_VIDEO_MODES = ("veo-hybrid", "veo-full", "elevenlabs-hybrid", "programmatic")
DEFAULT_VOICE_SPEC = "eleven_v3:JwqRvOqFdGeQNu7UjKjw"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.5,
    "similarity_boost": 0.80,
    "style": 0.20,
    "use_speaker_boost": True,
}
DEFAULT_VEO_MODEL = "veo-3.1-generate-preview"
DEFAULT_VEO_FAST_MODEL = "veo-3.1-fast-generate-preview"
DEFAULT_YT_HANDLE = "@WhereMoneySleeps"
DEFAULT_YT_URL = "https://www.youtube.com/@WhereMoneySleeps"
DEFAULT_SITE_BASE_URL = "https://wheremoneysleeps.duyslab.icu"
DEFAULT_REF_IMAGES = [
    "public/brand/youtube-banner-2560x1440-safezone.jpg",
    "public/brand/youtube-avatar-1024x1024.png",
]

# LUẬT 6b + LUẬT 8 + M3 (Bang-Motion Split-Stage & Parent-Child Containment Guard — QĐ 59 Phương án B: Zone 2 80% Kinetic Stage + Compact Formula Bar + YouTube CC .srt)
HEADER_BOX = (48, 36, 1032, 184)
CONDUIT_PARENT_BOX = (48, 198, 1032, 354)
STAGE_BOX = (48, 368, 1032, 1496)
CARD_BOX = (48, 1512, 1032, 1734)


def assert_parent_child_containment(
    parent_box: tuple[int, int, int, int],
    child_boxes: list[tuple[int, int, int, int]],
    pad_x: int = 20,
    pad_y: int = 12,
) -> None:
    """LUẬT 6b + M3: Đảm bảo mọi hộp con nằm gọn trong hộp cha với lề trong tối thiểu."""
    px0, py0, px1, py1 = parent_box
    for idx, (cx0, cy0, cx1, cy1) in enumerate(child_boxes):
        if cx0 < px0 + pad_x or cx1 > px1 - pad_x or cy0 < py0 + pad_y or cy1 > py1 - pad_y:
            raise AssertionError(
                f"Vi phạm LUẬT 6b/M3: child_box[{idx}]={(cx0, cy0, cx1, cy1)} tràn ngoài parent_box={parent_box} (pad=({pad_x},{pad_y}))"
            )
    if STAGE_BOX[3] + 12 > CARD_BOX[1]:
        raise AssertionError(f"Vi phạm LUẬT 8/M3: STAGE_BOX {STAGE_BOX} đè lên CARD_BOX {CARD_BOX}")


def load_dotenv(env_path: pathlib.Path = ENV_FILE) -> None:
    """Nạp biến môi trường từ file `.env` nếu có (không ghi đè biến đã set sẵn trên shell)."""
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def normalize_youtube_secrets(yt_secret: pathlib.Path, yt_token: pathlib.Path) -> None:
    """Tự động phát hiện nếu file OAuth client_secret (`installed`/`web`) được lưu nhầm tên thành youtube_token.json."""
    if yt_token.is_file() and not yt_secret.is_file():
        try:
            data = json.loads(yt_token.read_text(encoding="utf-8"))
            if isinstance(data, dict) and ("installed" in data or "web" in data):
                yt_secret.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(yt_token), str(yt_secret))
        except Exception:
            pass


def run_auth_youtube(port: int = 8765) -> int:
    """Chạy luồng OAuth 2.0 loopback (`http://localhost:<port>`) để lấy `refresh_token` cho kênh `@WhereMoneySleeps`."""
    load_dotenv()
    yt_secret = ROOT / os.environ.get("YOUTUBE_CLIENT_SECRET_FILE", ".secrets/youtube_client_secret.json")
    yt_token = ROOT / os.environ.get("YOUTUBE_TOKEN_FILE", ".secrets/youtube_token.json")
    normalize_youtube_secrets(yt_secret, yt_token)
    if not yt_secret.is_file():
        print(f"LỖI: Không tìm thấy {yt_secret.relative_to(ROOT)}", file=sys.stderr)
        return 1

    raw = json.loads(yt_secret.read_text(encoding="utf-8"))
    cfg = raw.get("installed") or raw.get("web") or {}
    client_id = cfg.get("client_id", "")
    client_secret = cfg.get("client_secret", "")
    auth_uri = cfg.get("auth_uri", "https://accounts.google.com/o/oauth2/auth")
    token_uri = cfg.get("token_uri", "https://oauth2.googleapis.com/token")
    scopes = "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube.force-ssl"
    captured: dict[str, str] = {}

    class OAuthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            q = urllib.parse.parse_qs(parsed.query)
            if "code" in q:
                captured["code"] = q["code"][0]
                body = "<html><meta charset='utf-8'><body style='font-family:sans-serif;padding:2rem'><h2>Đã kết nối kênh @WhereMoneySleeps thành công!</h2><p>Bạn có thể đóng tab này và quay lại cửa sổ dòng lệnh.</p></body></html>"
                self.send_response(200)
            else:
                captured["error"] = q.get("error", ["unknown"])[0]
                body = f"<html><meta charset='utf-8'><body><h2>Lỗi OAuth: {captured['error']}</h2></body></html>"
                self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

        def log_message(self, format, *args):  # noqa: A002
            return

    httpd: http.server.HTTPServer | None = None
    last_err: OSError | None = None
    for candidate_port in (port, *range(8766, 8776), 0):
        try:
            httpd = http.server.HTTPServer(("127.0.0.1", candidate_port), OAuthHandler)
            break
        except OSError as exc:
            if exc.errno == errno.EADDRINUSE:
                last_err = exc
                continue
            raise
    if httpd is None:
        raise last_err or OSError(errno.EADDRINUSE, "Không tìm được cổng localhost trống cho OAuth")

    with httpd:
        actual_port = httpd.server_port
        redirect_uri = f"http://localhost:{actual_port}"
        params = urllib.parse.urlencode(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": scopes,
                "access_type": "offline",
                "prompt": "consent",
            }
        )
        auth_url = f"{auth_uri}?{params}"

        print("=== ĐĂNG NHẬP OAUTH 2.0 CHO KÊNH @WhereMoneySleeps ===")
        print(f"1. Mở URL sau trên trình duyệt (chọn đúng tài khoản quản lý kênh @WhereMoneySleeps):\n   {auth_url}\n", flush=True)
        try:
            webbrowser.open(auth_url)
        except Exception:
            pass
        print(f"2. Đang chờ Google gọi ngược về {redirect_uri} (tối đa 180s) ...", flush=True)
        deadline = time.monotonic() + 180.0
        while "code" not in captured and "error" not in captured:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                captured["error"] = "timeout"
                break
            httpd.timeout = remaining
            httpd.handle_request()

    if "code" not in captured:
        print(f"LỖI: Không nhận được mã uỷ quyền OAuth ({captured.get('error', 'timeout')})", file=sys.stderr)
        return 1

    token_body = urllib.parse.urlencode(
        {
            "code": captured["code"],
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        token_uri,
        data=token_body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        tok_data = json.loads(resp.read().decode("utf-8"))

    saved = {
        "access_token": tok_data.get("access_token"),
        "refresh_token": tok_data.get("refresh_token"),
        "token_uri": token_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": scopes.split(),
    }
    yt_token.parent.mkdir(parents=True, exist_ok=True)
    yt_token.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    print(f"[PASS] Đã lưu YouTube OAuth refresh token vào {yt_token.relative_to(ROOT)}")
    return 0


def get_youtube_access_token() -> str:
    """Lấy `access_token` mới nhất từ `.secrets/youtube_token.json` (tự động chạy `--auth-youtube` nếu chưa có)."""
    load_dotenv()
    yt_token = ROOT / os.environ.get("YOUTUBE_TOKEN_FILE", ".secrets/youtube_token.json")
    if not yt_token.is_file():
        rc = run_auth_youtube()
        if rc != 0 or not yt_token.is_file():
            raise RuntimeError("Chưa hoàn tất uỷ quyền OAuth 2.0 cho YouTube")

    tok = json.loads(yt_token.read_text(encoding="utf-8"))
    if tok.get("refresh_token") and tok.get("client_id") and tok.get("client_secret"):
        refresh_body = urllib.parse.urlencode(
            {
                "client_id": tok["client_id"],
                "client_secret": tok["client_secret"],
                "refresh_token": tok["refresh_token"],
                "grant_type": "refresh_token",
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            tok.get("token_uri", "https://oauth2.googleapis.com/token"),
            data=refresh_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            refreshed = json.loads(resp.read().decode("utf-8"))
        if refreshed.get("access_token"):
            tok["access_token"] = refreshed["access_token"]
            yt_token.write_text(json.dumps(tok, indent=2) + "\n", encoding="utf-8")
    return str(tok.get("access_token") or "")


def step_5_0_brand_safety_audit(story_key: str, story: dict) -> dict:
    """
    5.0 — Brand Safety & Zero Proper Noun Specialist (`brand-safety-reviewer`, B1..B4).
    Chạy bắt buộc TRƯỚC 5A (ElevenLabs TTS), 5B (Render Video) và 5C (YouTube Upload).
    Nếu phát hiện bất kỳ tên riêng / thương hiệu / ngân hàng / mạng thẻ / công cụ AI hậu trường nào
    trong lời bình `vo`, chữ trên màn hình `onScreen`, mô tả cảnh `visual`, 5 ngôi nhà `houses` hoặc metadata YouTube,
    lập tức tung RuntimeError để chặn trước khi tốn quota hoặc đẩy lên YouTube.
    """
    brand_re = re.compile(
        r"\b(Vietcombank|Techcombank|VPBank|ACB|BIDV|VietinBank|MBBank|TPBank|Sacombank|VIB|"
        r"Agribank|HDBank|SHB|MSB|OCB|SeABank|LPBank|Eximbank|NamABank|Cake|Timo|"
        r"MoMo|ZaloPay|VNPay|Viettel\s*Money|ShopeePay|Payoo|OnePay|AirPay|Moca|"
        r"Visa|Mastercard|JCB|Amex|American\s+Express|UnionPay|NAPAS|VietQR|SWIFT|"
        r"FE\s*Credit|Home\s*Credit|HD\s*Saison|Shinhan\s*Finance|Mirae\s*Asset|Lotte\s*Finance|"
        r"Fundiin|Kredivo|Atome|Ree-Pay|Kaypay|"
        r"Shopee|Lazada|Tiki|TikTok|Reels|Facebook|Instagram|"
        r"Thế\s+Giới\s+Di\s+Động|FPT\s+Shop|Điện\s+Máy\s+Xanh|CellphoneS|Bách\s+Hoá\s+Xanh|"
        r"WinMart|Circle\s*K|Highlands|Starbucks|Phúc\s+Long|Grab|Be|Gojek|"
        r"Apple|iPhone|MacBook|Samsung|Xiaomi|Oppo|Sony|"
        r"ElevenLabs|Google|Veo|Gemini|OpenAI|ChatGPT|Claude|Anthropic|Sora|Runway|Midjourney|CapCut|"
        r"Stripe|PayPal|Adyen|Square|Klarna|Affirm|Afterpay|"
        r"Hermanson|Maher|Quán\s+Nhà\s+Liên)\b",
        re.I,
    )

    violations: list[str] = []

    def _scan_text(label: str, text: str) -> None:
        m = brand_re.search(str(text or ""))
        if m:
            violations.append(f"{label}: chứa tên riêng/thương hiệu cấm '{m.group(0)}' (B1/B2)")

    # B1/B2/B3: Quét cấp độ bài và 5 ngôi nhà
    _scan_text(f"STORIES.{story_key}.title", story.get("title", ""))
    _scan_text(f"STORIES.{story_key}.sub", story.get("sub", ""))
    _scan_text(f"STORIES.{story_key}.teaser", story.get("teaser", ""))
    houses = story.get("houses") or []
    for h_idx, h in enumerate(houses):
        if isinstance(h, dict):
            _scan_text(f"STORIES.{story_key}.houses[{h_idx}].name", h.get("name", ""))
            _scan_text(f"STORIES.{story_key}.houses[{h_idx}].sub", h.get("sub", ""))

    # B1/B2/B4: Quét toàn bộ videoScript.long & videoScript.short + YouTube metadata
    vid = story.get("videoScript") or {}
    checked_scenes = 0
    for fmt in ("long", "short"):
        fobj = vid.get(fmt) or {}
        vtitle = str(fobj.get("title") or "").strip()
        _scan_text(f"videoScript.{fmt}.title", vtitle)
        _scan_text(f"videoScript.{fmt}.hookNote", fobj.get("hookNote", ""))
        _scan_text(f"videoScript.{fmt}.angle", fobj.get("angle", ""))
        if len(vtitle.split()) < 8 or re.match(r"^\s*\d+(?:[.,]\d+)?\s*%", vtitle):
            violations.append(
                f"videoScript.{fmt}.title ({vtitle!r}): chưa đủ 3 điểm neo ngữ cảnh tự thân (B4)"
            )
        scenes = fobj.get("scenes") or []
        for s_idx, sc in enumerate(scenes):
            if not isinstance(sc, dict):
                continue
            checked_scenes += 1
            _scan_text(f"videoScript.{fmt}.scenes[{s_idx}].vo", sc.get("vo", ""))
            _scan_text(f"videoScript.{fmt}.scenes[{s_idx}].onScreen", sc.get("onScreen", ""))
            _scan_text(f"videoScript.{fmt}.scenes[{s_idx}].visual", sc.get("visual", ""))
            _scan_text(f"videoScript.{fmt}.scenes[{s_idx}].chapter", sc.get("chapter", ""))
        chapters_txt = build_youtube_chapters(scenes, vtitle or str(story.get("title") or ""))
        _scan_text(f"videoScript.{fmt}.youtubeChapters", chapters_txt)

    if violations:
        joined = "\n  - ".join(violations)
        raise RuntimeError(
            f"FAIL [Brand Safety & Zero Proper Noun Specialist B1–B4] trên bài '{story_key}':\n  - {joined}"
        )

    return {
        "specialist": "brand-safety-reviewer",
        "rule": "LUẬT 4 (VOICE-AND-PROSODY-SPEC.md §5)",
        "checks": ["B1_zero_commercial_proper_nouns", "B2_fourth_wall_tool_immunity", "B3_canonical_5house_archetypes", "B4_frame_and_metadata_audit"],
        "status": "PASS",
        "scenesAudited": checked_scenes,
        "properNounsFound": 0,
    }


def step_5_0b_financial_specialist_audit(story_key: str, story: dict) -> dict:
    """
    5.0b — Financial Domain, Banking Mechanics & Regulatory Intelligence Specialist (`tai-chinh-reviewer`, F1..F4).
    Chạy bắt buộc TRƯỚC 5A (ElevenLabs TTS), 5B (Render Video) và 5C (YouTube Upload).
    Đối chiếu trực tiếp với `knowledge/finance-kb.json` qua `scripts/wms-finance-kb.py`:
      - F1: Cơ chế ngân hàng, thanh toán & tín dụng (Wire vs Pipe vs Book).
      - F2: Toán tài chính (IRR/EIR, MDR, khấu trừ lương, Σ Nợ = Σ Có).
      - F3: Tính thời sự pháp quy (TT 99/2025/TT-BTC, độ tươi kho tri thức ≤ 30 ngày).
      - F4: Độ khớp xuyên suốt Bài viết ↔ Video (Long 16:9 & Short 9:16).
    """
    import importlib.util

    fkb_script = ROOT / "scripts" / "wms-finance-kb.py"
    kb_file = ROOT / "knowledge" / "finance-kb.json"
    if not fkb_script.is_file() or not kb_file.is_file():
        raise RuntimeError(f"Thiếu bộ kiểm định Chuyên gia Tài chính: {fkb_script} hoặc {kb_file}")

    spec = importlib.util.spec_from_file_location("wms_finance_kb", fkb_script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Không nạp được module {fkb_script}")
    fkb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fkb)

    kb = json.loads(kb_file.read_text(encoding="utf-8"))
    cs = fkb._load_check_story_module()
    tt99 = cs.load_tt99()

    fresh_rows = fkb.check_kb_freshness(kb)
    res = fkb.verify_story_finance(story_key, story, kb, tt99)
    all_rows = fresh_rows + res["rows"]
    fails = [f"[{code}] {where}: {msg}" for lv, code, where, msg in all_rows if lv == "FAIL"]
    if fails:
        joined = "\n  - ".join(fails)
        raise RuntimeError(
            f"FAIL [Financial Specialist tai-chinh-reviewer F1–F4] trên bài '{story_key}':\n  - {joined}"
        )

    return {
        "specialist": "tai-chinh-reviewer",
        "kbFile": "knowledge/finance-kb.json",
        "kbLastCrawledAt": kb.get("lastCrawledAt"),
        "checks": [
            "F1_banking_payment_credit_mechanics",
            "F2_financial_math_irr_eir_ledger",
            "F3_regulatory_freshness_tt99_2025",
            "F4_cross_format_post_to_video_fidelity",
        ],
        "status": "PASS",
        "details": [msg for lv, code, where, msg in res["rows"] if lv == "PASS"],
    }


def step_5c_upload_youtube(story_key: str, story: dict, fmt: str, mp4_path: pathlib.Path) -> str:
    """
    5C — Đẩy file `.mp4` lên kênh `@WhereMoneySleeps` qua YouTube Data API v3 Resumable Upload.
    Bắt buộc chạy `step_5_0_brand_safety_audit` và `step_5_0b_financial_specialist_audit` trước khi đẩy
    và đặt `privacyStatus = "unlisted"` khi `story.status != "published"` (WMS-R4 / QĐ 56).
    Trả về `youtubeId` 11 ký tự.
    """
    if not mp4_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file video để upload: {mp4_path}")
    brand_audit = step_5_0_brand_safety_audit(story_key, story)
    print(
        f"[5.0 Brand Safety Specialist PASS] B1–B4 sạch ({brand_audit['scenesAudited']} cảnh, "
        f"0 tên riêng/thương hiệu) trước khi upload {mp4_path.name}"
    )
    fin_audit = step_5_0b_financial_specialist_audit(story_key, story)
    print(
        f"[5.0b Financial Specialist PASS] F1–F4 sạch (KB: {fin_audit['kbLastCrawledAt']}) trước khi upload {mp4_path.name}"
    )
    access_token = get_youtube_access_token()
    fobj = (story.get("videoScript") or {}).get(fmt) or {}
    scenes = fobj.get("scenes") or []
    raw_title = str(fobj.get("title") or story.get("title") or story_key).strip()
    title = f"{raw_title} #Shorts" if fmt == "short" and "#Shorts" not in raw_title else raw_title
    desc = build_youtube_description(story_key, story, fmt)
    privacy = "unlisted" if story.get("status") != "published" else "unlisted"
    meta_body = json.dumps(
        {
            "snippet": {
                "title": title[:100],
                "description": desc,
                "tags": ["WhereMoneySleeps", "TaiChinhCaNhan", "KeToan", "TraGop0PhanTram", "Shorts" if fmt == "short" else "Explainer"],
                "categoryId": "27",
                "defaultLanguage": "vi",
                "defaultAudioLanguage": "vi",
            },
            "status": {
                "privacyStatus": privacy,
                "embeddable": True,
                "publicStatsViewable": True,
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
            },
        },
        ensure_ascii=False,
    ).encode("utf-8")

    mp4_bytes = mp4_path.read_bytes()
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    init_req = urllib.request.Request(
        init_url,
        data=meta_body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(len(mp4_bytes)),
            "X-Upload-Content-Type": "video/mp4",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(init_req, timeout=60) as init_resp:
            upload_url = init_resp.headers.get("Location")
    except urllib.error.HTTPError as exc:
        err_raw = exc.read().decode("utf-8", errors="replace")
        if "uploadLimitExceeded" in err_raw:
            raise RuntimeError(
                f"YouTube Data API v3 trả về 'uploadLimitExceeded' (kênh {DEFAULT_YT_HANDLE} đã chạm trần 10 video/24h của YouTube cho kênh mới). "
                f"File video đã render sẵn tại {mp4_path.relative_to(ROOT)} ({len(mp4_bytes):,} bytes); "
                "hãy bật Intermediate/Advanced Features trong YouTube Studio (Settings -> Channel -> Feature eligibility) hoặc chạy lại lệnh upload sau khi hạn mức 24h mở lại."
            ) from exc
        raise RuntimeError(f"YouTube Data API v3 trả về HTTP {exc.code}: {err_raw}") from exc
    if not upload_url:
        raise RuntimeError("YouTube Data API v3 không trả về Location header cho Resumable Upload")

    print(f"[5C Upload] Đang đẩy {mp4_path.relative_to(ROOT)} ({len(mp4_bytes):,} bytes) lên {DEFAULT_YT_HANDLE} (privacy={privacy!r})...")
    up_req = urllib.request.Request(
        upload_url,
        data=mp4_bytes,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "video/mp4",
            "Content-Length": str(len(mp4_bytes)),
        },
        method="PUT",
    )
    with urllib.request.urlopen(up_req, timeout=300) as up_resp:
        res_data = json.loads(up_resp.read().decode("utf-8"))
    yt_id = str(res_data.get("id") or "").strip()
    if not YT_ID_RE.match(yt_id):
        raise RuntimeError(f"YouTube trả về video ID không hợp lệ: {yt_id!r}")
    print(f"[5C Upload PASS] Đã tải lên thành công: https://youtu.be/{yt_id} (privacyStatus={privacy!r})")
    return yt_id


def run_check_env() -> int:
    """Kiểm tra sẵn sàng của `.env`, ElevenLabs API Key (Audio), Google Veo 3.1 (Video) và YouTube OAuth (`@WhereMoneySleeps`)."""
    load_dotenv()
    lic_el = verify_elevenlabs_licence()
    lic_veo = verify_google_veo_licence()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    veo_model = os.environ.get("GOOGLE_VEO_MODEL", DEFAULT_VEO_MODEL).strip()
    video_mode = os.environ.get("WMS_VIDEO_MODE", "veo-hybrid").strip()
    yt_handle = os.environ.get("YOUTUBE_CHANNEL_HANDLE", DEFAULT_YT_HANDLE).strip()
    yt_url = os.environ.get("YOUTUBE_CHANNEL_URL", DEFAULT_YT_URL).strip()
    yt_secret = ROOT / os.environ.get("YOUTUBE_CLIENT_SECRET_FILE", ".secrets/youtube_client_secret.json")
    yt_token = ROOT / os.environ.get("YOUTUBE_TOKEN_FILE", ".secrets/youtube_token.json")
    normalize_youtube_secrets(yt_secret, yt_token)

    print("=== KIỂM TRA CẤU HÌNH PIPELINE BƯỚC 5 (QĐ 56: ElevenLabs Audio + Google Veo 3.1 Video -> YouTube) ===")
    print(f"  [PASS] Giấy phép Audio ElevenLabs (legal/licences.json): {lic_el.get('id')} ({lic_el.get('licence')})")
    print(f"  [PASS] Giấy phép Video Google Veo (legal/licences.json): {lic_veo.get('id')} ({lic_veo.get('licence')})")
    print(f"  [PASS] Kênh YouTube đích: {yt_handle} ({yt_url})")
    print(f"  [INFO] Chế độ dựng Video (5B): video_mode={video_mode!r} · veo_model={veo_model!r}")
    if ENV_FILE.is_file():
        print(f"  [PASS] File .env: đã tạo tại {ENV_FILE.relative_to(ROOT)}")
    else:
        print(f"  [WAIT] File .env: chưa tạo (chạy `cp .env.example .env` trong where-money-sleeps/)")

    if api_key:
        masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"  [PASS] ELEVENLABS_API_KEY (5A Audio: TTS + SFX): đã khai báo ({masked})")
    else:
        print("  [WAIT] ELEVENLABS_API_KEY (5A Audio: chỉ cần quyền Text to Speech + Sound Effects): chưa điền trong .env")

    if gemini_key:
        g_masked = gemini_key[:6] + "..." + gemini_key[-4:] if len(gemini_key) > 12 else "***"
        print(f"  [PASS] GEMINI_API_KEY (5B Video: Google Veo 3.1 Ultra quota): đã khai báo ({g_masked})")
    else:
        print("  [WAIT] GEMINI_API_KEY (5B Video: Google Veo 3.1): chưa điền trong .env")

    if yt_secret.is_file():
        raw_sec = json.loads(yt_secret.read_text(encoding="utf-8"))
        proj = (raw_sec.get("installed") or raw_sec.get("web") or {}).get("project_id", "unknown")
        print(f"  [PASS] YouTube OAuth client_secret: {yt_secret.relative_to(ROOT)} (project_id={proj!r})")
    else:
        print(f"  [WAIT] YouTube OAuth client_secret: chưa đặt file tại {yt_secret.relative_to(ROOT)}")

    if yt_token.is_file():
        print(f"  [PASS] YouTube OAuth refresh token: {yt_token.relative_to(ROOT)}")
    else:
        print(
            f"  [INFO] YouTube OAuth refresh token: chưa sinh ({yt_token.relative_to(ROOT)}) — "
            "chạy `python3 -I scripts/wms-media-pipeline.py --auth-youtube` để uỷ quyền kênh @WhereMoneySleeps 1 lần"
        )
    return 0


def _load_check_story():
    spec = importlib.util.spec_from_file_location("check_story", ROOT / "scripts/check-story.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Không nạp được scripts/check-story.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extract_stories(src: str) -> dict:
    """Trích object JS `const STORIES = {...}` từ HTML bằng JSLiteral của check-story.py."""
    mod = _load_check_story()
    return mod.extract(src, "STORIES")


def find_story_videoscript_span(src: str, story_key: str) -> tuple[dict, int, int]:
    """Tìm vị trí khối JSON `videoScript:{...}` của `story_key` trong HTML để ghi ngược ở Bước 5D."""
    m_stories = re.search(r"\bconst\s+STORIES\s*=\s*\{", src)
    base = m_stories.start() if m_stories else 0
    story_pat = re.compile(rf"(?:^\s*|[,{{]\s*)(?:[\"']?{re.escape(story_key)}[\"']?)\s*:\s*\{{", re.M)
    m_story = story_pat.search(src, base)
    if not m_story:
        raise KeyError(f"Không tìm thấy bài '{story_key}' trong STORIES")
    m_vs = re.search(r'(?:["\']?videoScript["\']?)\s*:\s*\{', src[m_story.start() :])
    if not m_vs:
        raise ValueError(f"Không tìm thấy `videoScript` trong bài '{story_key}'")
    start = m_story.start() + m_vs.end() - 1
    depth, in_str, esc = 0, False, False
    for i in range(start, len(src)):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    raw = src[start : i + 1]
                    return json.loads(raw), start, i + 1
    raise ValueError(f"Khối videoScript của '{story_key}' không đóng ngoặc nhọn")


def verify_elevenlabs_licence() -> dict:
    """Kiểm tra mục giấy phép thương mại ElevenLabs trong legal/licences.json (Quy tắc 4)."""
    if not LICENCES_JSON.is_file():
        raise RuntimeError(f"Thiếu {LICENCES_JSON} — Quy tắc 4 bắt buộc kiểm giấy phép trước khi build media")
    data = json.loads(LICENCES_JSON.read_text(encoding="utf-8"))
    for asset in data.get("assets", []):
        if asset.get("id") == "elevenlabs-commercial-tts-sfx":
            return asset
    raise RuntimeError(
        "legal/licences.json thiếu mục `id: \"elevenlabs-commercial-tts-sfx\"` — không được gọi ElevenLabs API"
    )


def verify_google_veo_licence() -> dict:
    """Kiểm tra mục giấy phép thương mại Google Veo 3.1 trong legal/licences.json (Quy tắc 4)."""
    if not LICENCES_JSON.is_file():
        raise RuntimeError(f"Thiếu {LICENCES_JSON} — Quy tắc 4 bắt buộc kiểm giấy phép trước khi build video")
    data = json.loads(LICENCES_JSON.read_text(encoding="utf-8"))
    for asset in data.get("assets", []):
        if asset.get("id") == "google-veo-video-generation":
            return asset
    raise RuntimeError(
        "legal/licences.json thiếu mục `id: \"google-veo-video-generation\"` — không được gọi Google Veo API"
    )


def scene_cache_key(voice_spec: str, fmt: str, idx: int, vo: str, on_screen: str) -> str:
    payload = json.dumps(
        {"voice": voice_spec, "fmt": fmt, "idx": idx, "vo": vo.strip(), "onScreen": on_screen.strip()},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def veo_scene_cache_key(veo_model: str, aspect: str, idx: int, visual: str) -> str:
    payload = json.dumps(
        {"model": veo_model, "aspectRatio": aspect, "idx": idx, "visual": visual.strip()},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_start_mmss(time_range: str) -> str:
    m = re.match(r"^\s*(\d+:\d{2})\s*[–-]\s*(\d+:\d{2})", str(time_range or ""))
    return m.group(1) if m else "0:00"


def build_article_url(story_key: str) -> str:
    base = os.environ.get("WMS_SITE_BASE_URL", DEFAULT_SITE_BASE_URL).strip().rstrip("/")
    return f"{base}/?story={urllib.parse.quote(story_key)}"


def build_youtube_chapters(scenes: list[dict], story_title: str) -> str:
    lines = [f"0:00 Mở đầu — {story_title}"]
    for idx, sc in enumerate(scenes):
        t0 = parse_start_mmss(sc.get("time", ""))
        beat = sc.get("beat")
        label = "Hook mở đầu" if idx == 0 else ("Cảnh kết" if idx == len(scenes) - 1 else f"Đoạn {int(beat) + 1}" if isinstance(beat, int) else f"Cảnh {idx + 1}")
        if t0 != "0:00":
            lines.append(f"{t0} {label}")
    return "\n".join(lines)


def build_youtube_description(story_key: str, story: dict, fmt: str) -> str:
    vid = story.get("videoScript") or {}
    fobj = vid.get(fmt) or {}
    scenes = fobj.get("scenes") or []
    raw_title = str(fobj.get("title") or story.get("title") or story_key).strip()
    chapters = build_youtube_chapters(scenes, raw_title)
    article_url = build_article_url(story_key)
    long_yt_id = str((vid.get("long") or {}).get("youtubeId") or "").strip()
    long_line = f"▶ Xem Video bài giảng đầy đủ (16:9): https://youtu.be/{long_yt_id}\n" if (fmt == "short" and long_yt_id) else ""
    return (
        f"📖 Đọc bài khảo cứu đầy đủ & Sổ kế toán kép tại: {article_url}\n"
        f"{long_line}\n"
        f"{story.get('teaser', '')}\n\n"
        f"Mục lục chương:\n{chapters}\n\n"
        f"---\n"
        f"Bài khảo cứu tương tác đầy đủ (Video 16:9 + Sổ kế toán TT 99/2025 + Máy tính dòng tiền): {article_url}\n"
        f"Kênh: Where Money Sleeps ({DEFAULT_YT_HANDLE})\n"
        f"Lưu ý: Mọi con số và tình huống trong video là ví dụ minh hoạ để thấy cơ chế vận hành của dòng tiền và bút toán kế toán, không nhắc tới bất kỳ đơn vị hay thương hiệu cụ thể nào và không phải lời khuyên tài chính.\n"
        f"Where Money Sleeps — Đêm nay, tiền của bạn ngủ ở đâu?"
    )


def step_5c_update_youtube_description(
    story_key: str,
    story: dict,
    fmt: str,
    privacy_status: str | None = None,
) -> str:
    """Cập nhật snippet.description (kèm URL chính xác của bài viết) và status.privacyStatus trên YouTube qua videos.update."""
    step_5_0_brand_safety_audit(story_key, story)
    vid = story.get("videoScript") or {}
    fobj = vid.get(fmt) or {}
    yt_id = str(fobj.get("youtubeId") or "").strip()
    if not YT_ID_RE.match(yt_id):
        raise ValueError(f"Bài '{story_key}' ({fmt}) chưa có youtubeId hợp lệ để cập nhật description")
    if privacy_status == "public" and story.get("status") != "published":
        raise PermissionError(f"CỔNG WMS-R4: Bài '{story_key}' chưa ở status='published', cấm bật public")
    access_token = get_youtube_access_token()
    raw_title = str(fobj.get("title") or story.get("title") or story_key).strip()
    title = f"{raw_title} #Shorts" if fmt == "short" and "#Shorts" not in raw_title else raw_title
    desc = build_youtube_description(story_key, story, fmt)
    payload: dict = {
        "id": yt_id,
        "snippet": {
            "title": title[:100],
            "description": desc,
            "tags": ["WhereMoneySleeps", "TaiChinhCaNhan", "KeToan", "TraGop0PhanTram", "Shorts" if fmt == "short" else "Explainer"],
            "categoryId": "27",
            "defaultLanguage": "vi",
            "defaultAudioLanguage": "vi",
        },
    }
    part_q = "snippet"
    if privacy_status in ("public", "unlisted", "private"):
        payload["status"] = {
            "privacyStatus": privacy_status,
            "embeddable": True,
            "publicStatsViewable": True,
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        }
        part_q = "snippet,status"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part={part_q}",
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
        out_id = str(res_data.get("id") or yt_id).strip()
        out_priv = str((res_data.get("status") or {}).get("privacyStatus") or privacy_status or "unchanged")
        print(f"[5C Update Desc PASS] {story_key} ({fmt} · {out_id} · privacy={out_priv}) -> {build_article_url(story_key)}")
        return out_id
    except urllib.error.HTTPError as exc:
        err_raw = exc.read().decode("utf-8", errors="replace")
        if exc.code == 403 and ("insufficientPermissions" in err_raw or "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in err_raw):
            print(
                f"[5C Update Desc INFO] {story_key} ({fmt} · {yt_id}): Đã ghi description chuẩn kèm URL {build_article_url(story_key)} vào manifest. "
                "Để cập nhật trực tiếp video cũ đã tải lên trên YouTube qua videos.update, chạy 1 lần `python3 -I scripts/wms-media-pipeline.py --auth-youtube` để cấp thêm scope `youtube` (mọi video upload mới qua `videos.insert` đã tự động đính kèm URL này ngay từ đầu)."
            )
            return yt_id
        raise RuntimeError(f"YouTube videos.update trả về HTTP {exc.code}: {err_raw}") from exc


def step_5c_upload_youtube_captions(
    story_key: str,
    story: dict,
    fmt: str,
    srt_path: pathlib.Path | None = None,
) -> str:
    """Tải phụ đề chuẩn `.srt` (tiếng Việt) lên video YouTube qua YouTube Data API v3 Captions API (cần scope youtube.force-ssl)."""
    vid = story.get("videoScript") or {}
    fobj = vid.get(fmt) or {}
    yt_id = str(fobj.get("youtubeId") or "").strip()
    if not YT_ID_RE.match(yt_id):
        return ""
    suffix = "short-9x16.srt" if fmt == "short" else "long-16x9.srt"
    target_srt = srt_path or (DIST_DIR / f"{story_key}-{suffix}")
    if not target_srt.is_file():
        print(f"  [WARN] Chưa thấy file phụ đề {target_srt.relative_to(ROOT)} để upload cho {story_key} ({fmt})")
        return yt_id

    access_token = get_youtube_access_token()
    existing_caption_id = ""
    try:
        list_req = urllib.request.Request(
            f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={urllib.parse.quote(yt_id)}",
            headers={"Authorization": f"Bearer {access_token}"},
            method="GET",
        )
        with urllib.request.urlopen(list_req, timeout=30) as resp:
            caps_data = json.loads(resp.read().decode("utf-8"))
        for item in caps_data.get("items") or []:
            snip = item.get("snippet") or {}
            if snip.get("language") == "vi" and str(snip.get("trackKind") or "").lower() != "asr":
                existing_caption_id = str(item.get("id") or "").strip()
                break
    except urllib.error.HTTPError as exc:
        err_raw = exc.read().decode("utf-8", errors="replace")
        if exc.code == 403 and ("insufficientPermissions" in err_raw or "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in err_raw):
            print(
                f"  [WARN] Token hiện tại thiếu scope youtube.force-ssl cho Captions API ({story_key} {fmt} · {yt_id}); "
                "chạy `--auth-youtube` 1 lần để cấp quyền."
            )
            return yt_id
        raise RuntimeError(f"YouTube captions.list trả về HTTP {exc.code}: {err_raw}") from exc

    snippet_meta: dict = {
        "snippet": {
            "videoId": yt_id,
            "language": "vi",
            "name": "Tiếng Việt (Chuẩn khớp lời bình)",
            "isDraft": False,
        }
    }
    method = "POST"
    if existing_caption_id:
        snippet_meta = {"id": existing_caption_id, "snippet": {"name": "Tiếng Việt (Chuẩn khớp lời bình)", "isDraft": False}}
        method = "PUT"

    boundary = f"wms_cap_{os.urandom(12).hex()}"
    meta_bytes = json.dumps(snippet_meta, ensure_ascii=False).encode("utf-8")
    srt_bytes = target_srt.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + meta_bytes + (
        f"\r\n--{boundary}\r\n"
        f"Content-Type: application/x-subrip; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + srt_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    up_req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(up_req, timeout=60) as resp:
            cap_res = json.loads(resp.read().decode("utf-8"))
        cap_id = str(cap_res.get("id") or existing_caption_id or "").strip()
        print(f"[5C Captions PASS] {story_key} ({fmt} · {yt_id} · {method}) <- {target_srt.name} (captionId={cap_id})")
        return yt_id
    except urllib.error.HTTPError as exc:
        err_raw = exc.read().decode("utf-8", errors="replace")
        if exc.code == 403 and ("insufficientPermissions" in err_raw or "ACCESS_TOKEN_SCOPE_INSUFFICIENT" in err_raw):
            print(
                f"  [WARN] Token hiện tại thiếu scope youtube.force-ssl cho Captions API ({story_key} {fmt} · {yt_id}); "
                "chạy `--auth-youtube` 1 lần để cấp quyền."
            )
            return yt_id
        raise RuntimeError(f"YouTube captions.{method.lower()} trả về HTTP {exc.code}: {err_raw}") from exc


def step_5a_5b_manifest(story_key: str, story: dict, mode: str, video_mode: str = "veo-hybrid") -> dict:
    """5.0 (Brand Safety Specialist B1-B4 & Financial Specialist F1-F4) -> 5A (ElevenLabs TTS with-timestamps + SFX) & 5B (Locked-Stage Diorama v3.0 Video 16:9/9:16)."""
    load_dotenv()
    brand_audit = step_5_0_brand_safety_audit(story_key, story)
    print(
        f"[5.0 Brand Safety Specialist PASS] B1–B4 sạch trên '{story_key}' "
        f"({brand_audit['scenesAudited']} cảnh, 0 tên riêng/thương hiệu có thật)"
    )
    fin_audit = step_5_0b_financial_specialist_audit(story_key, story)
    print(
        f"[5.0b Financial Specialist PASS] F1–F4 sạch trên '{story_key}' "
        f"(KB: {fin_audit['kbLastCrawledAt']})"
    )
    lic_el = verify_elevenlabs_licence()
    lic_veo = verify_google_veo_licence()
    vid = story.get("videoScript") or {}
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    veo_model = os.environ.get("GOOGLE_VEO_MODEL", DEFAULT_VEO_MODEL).strip()
    veo_fast_model = os.environ.get("GOOGLE_VEO_FAST_MODEL", DEFAULT_VEO_FAST_MODEL).strip()
    yt_handle = os.environ.get("YOUTUBE_CHANNEL_HANDLE", DEFAULT_YT_HANDLE).strip()
    yt_url = os.environ.get("YOUTUBE_CHANNEL_URL", DEFAULT_YT_URL).strip()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    VEO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    formats_out = {}
    for fmt in ("long", "short"):
        fobj = vid.get(fmt) or {}
        voice_spec = str(fobj.get("elevenlabsVoiceId") or DEFAULT_VOICE_SPEC).strip()
        model_id, _, voice_id = voice_spec.partition(":")
        if not voice_id:
            voice_id = model_id
            model_id = "eleven_v3"
        resolution = "1920x1080" if fmt == "long" else "1080x1920"
        aspect = "16:9" if fmt == "long" else "9:16"
        scenes = fobj.get("scenes") or []
        scene_plan = []
        for i, sc in enumerate(scenes):
            vo = str(sc.get("vo") or "").strip()
            visual = str(sc.get("visual") or "").strip()
            on_screen = str(sc.get("onScreen") or "").strip()
            prev_text = str(scenes[i - 1].get("vo") or "").strip() if i > 0 else ""
            next_text = str(scenes[i + 1].get("vo") or "").strip() if i + 1 < len(scenes) else ""
            ck = scene_cache_key(voice_spec, fmt, i, vo, on_screen)
            cache_file = CACHE_DIR / f"{ck}.json"
            sfx_match = re.search(r"SFX(?:\s*gợi ý)?:\s*([^·\n]+)", on_screen, flags=re.I)
            sfx_prompt = sfx_match.group(1).strip() if sfx_match else ""

            if mode == "live" and api_key and not cache_file.is_file():
                # Gọi ElevenLabs /v1/text-to-speech/{voice_id}/with-timestamps (eleven_v3 expressive prosody)
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
                tts_payload: dict = {
                    "text": vo,
                    "model_id": model_id,
                    "voice_settings": DEFAULT_VOICE_SETTINGS,
                }
                if not model_id.startswith("eleven_v3"):
                    tts_payload["previous_text"] = prev_text
                    tts_payload["next_text"] = next_text
                body = json.dumps(tts_payload, ensure_ascii=False).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=90) as resp:
                    cache_file.write_bytes(resp.read())

            use_veo = video_mode in ("veo-hybrid", "veo-full")
            scene_veo_model = (
                veo_model if (i == 0 or i == len(scenes) - 1 or fmt == "short") else veo_fast_model
            ) if use_veo else None
            veo_ck = veo_scene_cache_key(scene_veo_model or "none", aspect, i, visual) if use_veo else None
            veo_clip_file = VEO_CACHE_DIR / f"{veo_ck}.mp4" if veo_ck else None

            scene_plan.append(
                {
                    "sceneIndex": i,
                    "time": sc.get("time"),
                    "beat": sc.get("beat"),
                    "sha256CacheKey": ck,
                    "cached": cache_file.is_file(),
                    "elevenlabsTtsEndpoint": f"/v1/text-to-speech/{voice_id}/with-timestamps",
                    "elevenlabsModelId": model_id,
                    "googleVeoVideo": {
                        "enabled": use_veo,
                        "sdkMethod": "google.genai.Client().models.generate_videos",
                        "modelId": scene_veo_model,
                        "aspectRatio": aspect,
                        "referenceImages": DEFAULT_REF_IMAGES,
                        "sha256CacheKey": veo_ck,
                        "cachedMp4": bool(veo_clip_file and veo_clip_file.is_file()),
                        "dioramaHudOverlay": video_mode == "veo-hybrid",
                    } if use_veo else None,
                    "visualPrompt": visual,
                    "sfxEndpoint": "/v1/sound-generation" if sfx_prompt else None,
                    "sfxPrompt": sfx_prompt,
                    "voWords": len(vo.split()),
                }
            )

        mp4_name = f"{story_key}-{fmt}-{aspect.replace(':', 'x')}.mp4"
        formats_out[fmt] = {
            "title": fobj.get("title"),
            "aspectRatio": aspect,
            "resolution": resolution,
            "videoMode": video_mode,
            "videoGenerator": {
                "provider": "Google Veo 3.1 (Google AI Ultra / Gemini API) + FFmpeg Diorama/TT99 Overlay",
                "sdk": "google-genai (client.models.generate_videos)",
                "heroModelId": veo_model,
                "bodyModelId": veo_fast_model,
                "referenceImages": DEFAULT_REF_IMAGES,
                "cacheDir": ".cache/google-veo/",
            },
            "audioGenerator": {
                "provider": "ElevenLabs API (Single-Take Continuous eleven_v3 TTS with-timestamps + Sound Effects + Warm Room Tone Bed)",
                "synthesisMode": "single_take_continuous_with_breath_bridges",
                "continuousCacheFile": f".cache/elevenlabs/{story_key}_{fmt}_continuous_v3.json",
                "breathBridgeSeconds": 0.36,
                "roomToneBedDbfs": -33.0,
                "transitionSfxDbfs": -22.0,
                "requiredKeyScopes": ["Text to Speech", "Sound Effects", "Voices (Read)", "Pronunciation Dictionaries"],
                "cacheDir": ".cache/elevenlabs/",
            },
            "visualTransitionEngine": {
                "version": "4.3-broadcast-split-stage-30fps",
                "stageMotion": "0px_pan_1.00x_zoom_locked_stage",
                "stageLayout": "3_zone_non_overlapping_split_stage_luat_8",
                "fps": 30,
                "crossDissolveSeconds": 0.96,
                "easing": "cubic_smoothstep",
                "captionMode": "phrase_by_phrase_constant_weight_pill_highlight",
                "liveConduitAnimation": True,
            },
            "loudnessTarget": "-14 LUFS (true peak <= -1.0 dBTP)",
            "elevenlabsVoiceId": voice_spec,
            "youtubeId": fobj.get("youtubeId", ""),
            "embedStatus": fobj.get("embedStatus", "pending_upload"),
            "outputMp4": str((DIST_DIR / mp4_name).relative_to(ROOT)),
            "youtubeUploadSpec": {
                "api": "YouTube Data API v3 — videos.insert (part=snippet,status)",
                "channelHandle": yt_handle,
                "channelUrl": yt_url,
                "articleUrl": build_article_url(story_key),
                "categoryId": "27",
                "defaultLanguage": "vi",
                "privacyStatus": "unlisted" if story.get("status") != "published" else "public",
                "embeddable": True,
                "publicStatsViewable": True,
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
                "chaptersDescription": build_youtube_chapters(scenes, str(fobj.get("title") or story.get("title") or "")),
                "description": build_youtube_description(story_key, story, fmt),
            },
            "scenes": scene_plan,
        }

    manifest = {
        "schemaVersion": "1.4-qd56-locked-stage-brand-and-financial-specialists",
        "story": story_key,
        "storyStatus": story.get("status"),
        "brandSafetyAudit": brand_audit,
        "financialSpecialistAudit": fin_audit,
        "youtubeChannel": {
            "handle": yt_handle,
            "url": yt_url,
        },
        "licenceCheck": {
            "audio": {
                "id": lic_el.get("id"),
                "licence": lic_el.get("licence"),
            },
            "video": {
                "id": lic_veo.get("id"),
                "licence": lic_veo.get("licence"),
            },
        },
        "formats": formats_out,
    }
    manifest_path = DIST_DIR / f"{story_key}-elevenlabs-youtube-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def step_5d_embed_into_post(
    html_path: pathlib.Path,
    story_key: str,
    long_yt_id: str | None,
    short_yt_id: str | None,
    embed_status: str | None,
) -> tuple[str, str, str]:
    """
    5D — Ghi ngược `youtubeId` và `embedStatus` vào `STORIES[<story>].videoScript.{long,short}`
    trong `docs/prototype.html` để trình phát YouTube nhúng thẳng vào bài viết.
    """
    src = html_path.read_text(encoding="utf-8")
    stories = extract_stories(src)
    if story_key not in stories:
        raise KeyError(f"Không tìm thấy bài '{story_key}' trong STORIES của {html_path}")
    st = stories[story_key]
    vid, start, end = find_story_videoscript_span(src, story_key)
    if not isinstance(vid.get("long"), dict) or not isinstance(vid.get("short"), dict):
        raise ValueError(f"Bài '{story_key}' thiếu videoScript.long hoặc videoScript.short")

    target_status = embed_status or vid["long"].get("embedStatus") or "pending_upload"
    if target_status not in VALID_EMBED_STATUS:
        raise ValueError(f"embedStatus không hợp lệ: {target_status!r} (chỉ nhận {sorted(VALID_EMBED_STATUS)})")
    if st.get("status") != "published" and target_status == "uploaded_public":
        raise PermissionError(
            f"CỔNG WMS-R4 / QĐ 56: Bài '{story_key}' đang ở status='{st.get('status')}' (chưa được Duy duyệt đăng). "
            "CẤM đặt embedStatus='uploaded_public'. Chỉ được dùng 'uploaded_unlisted', 'uploaded_private', hoặc 'pending_upload'."
        )

    for fmt, new_id in (("long", long_yt_id), ("short", short_yt_id)):
        fobj = vid[fmt]
        if new_id is not None:
            clean_id = new_id.strip()
            if clean_id and not YT_ID_RE.match(clean_id):
                raise ValueError(
                    f"youtubeId cho {fmt} ({clean_id!r}) phải rỗng hoặc đúng 11 ký tự chuẩn YouTube (^[A-Za-z0-9_-]{{11}}$)"
                )
            fobj["youtubeId"] = clean_id
        if embed_status is not None:
            fobj["embedStatus"] = target_status if fobj.get("youtubeId") else "pending_upload"
        if not fobj.get("elevenlabsVoiceId"):
            fobj["elevenlabsVoiceId"] = DEFAULT_VOICE_SPEC

    new_vs_json = json.dumps(vid, ensure_ascii=False, indent=1)
    updated_src = src[:start] + new_vs_json + src[end:]
    html_path.write_text(updated_src, encoding="utf-8")
    return (
        vid["long"].get("youtubeId", ""),
        vid["short"].get("youtubeId", ""),
        vid["short"].get("embedStatus") if vid["short"].get("youtubeId") else vid["long"].get("embedStatus", "pending_upload"),
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Pipeline Bước 5 (QĐ 56): ElevenLabs TTS/SFX/Video -> Render Video -> Upload YouTube -> Embed vào bài viết."
    )
    ap.add_argument("--html", type=pathlib.Path, default=DEFAULT_HTML, help="Đường dẫn tới docs/prototype.html")
    ap.add_argument("--check-env", action="store_true", help="Kiểm tra file .env, ELEVENLABS_API_KEY, GEMINI_API_KEY và YouTube OAuth")
    ap.add_argument("--auth-youtube", action="store_true", help="Mở trình duyệt đăng nhập OAuth 2.0 1 lần để lấy refresh_token cho @WhereMoneySleeps")
    ap.add_argument("--story", default=None, help="Khoá bài viết trong STORIES (vd: card, pay, install)")
    ap.add_argument(
        "--mode",
        choices=("dry-run", "live"),
        default="dry-run",
        help="dry-run: kiểm giấy phép + xuất manifest ElevenLabs/YouTube; live: gọi API khi có ELEVENLABS_API_KEY",
    )
    ap.add_argument(
        "--video-mode",
        choices=VALID_VIDEO_MODES,
        default="veo-hybrid",
        help="Chế độ dựng hình ảnh video 5B (veo-hybrid | veo-full | elevenlabs-hybrid | programmatic)",
    )
    ap.add_argument("--bind-long-id", default=None, help="Gán mã YouTube Video ID 11 ký tự cho bản Dài 16:9 và nhúng vào bài")
    ap.add_argument("--bind-short-id", default=None, help="Gán mã YouTube Video ID 11 ký tự cho bản Shorts 9:16 và nhúng vào bài")
    ap.add_argument("--upload-short", action="store_true", help="Upload dist/youtube/<story>-short-9x16.mp4 lên @WhereMoneySleeps (unlisted) và tự động nhúng youtubeId vào bài viết")
    ap.add_argument("--upload-long", action="store_true", help="Upload dist/youtube/<story>-long-16x9.mp4 lên @WhereMoneySleeps (unlisted) và tự động nhúng youtubeId vào bài viết")
    ap.add_argument("--update-youtube-desc", action="store_true", help="Cập nhật description chứa URL chính xác của bài viết lên YouTube cho video ngắn (và dài)")
    ap.add_argument("--upload-captions", action="store_true", help="Tải phụ đề .srt lên YouTube qua Captions API (cần scope youtube.force-ssl)")
    ap.add_argument("--all-stories", action="store_true", help="Chạy cho toàn bộ 7 bài trong STORIES")
    ap.add_argument(
        "--embed-status",
        choices=sorted(VALID_EMBED_STATUS),
        default=None,
        help="Trạng thái nhúng YouTube (pending_upload | uploaded_unlisted | uploaded_private | uploaded_public)",
    )
    args = ap.parse_args()

    if args.check_env:
        return run_check_env()

    if args.auth_youtube:
        return run_auth_youtube()

    src = args.html.read_text(encoding="utf-8")
    stories = extract_stories(src)

    if args.all_stories:
        priv_map = {
            "uploaded_public": "public",
            "uploaded_unlisted": "unlisted",
            "uploaded_private": "private",
        }
        target_priv = priv_map.get(args.embed_status or "")
        for sk in list(stories.keys()):
            if args.embed_status is not None:
                step_5d_embed_into_post(args.html, sk, None, None, args.embed_status)
                src = args.html.read_text(encoding="utf-8")
                stories = extract_stories(src)
            if args.update_youtube_desc:
                step_5c_update_youtube_description(sk, stories[sk], "short", privacy_status=target_priv)
                step_5c_update_youtube_description(sk, stories[sk], "long", privacy_status=target_priv)
            if args.upload_captions:
                step_5c_upload_youtube_captions(sk, stories[sk], "short")
                step_5c_upload_youtube_captions(sk, stories[sk], "long")
            step_5a_5b_manifest(sk, stories[sk], args.mode, args.video_mode)
        return 0

    if not args.story:
        ap.error("Cần truyền `--story <slug>` (hoặc `--all-stories` / `--check-env` / `--auth-youtube`)")

    if args.story not in stories:
        print(f"LỖI: Không tìm thấy bài '{args.story}' trong STORIES", file=sys.stderr)
        return 1

    if args.update_youtube_desc:
        step_5c_update_youtube_description(args.story, stories[args.story], "short")
        step_5c_update_youtube_description(args.story, stories[args.story], "long")
    if args.upload_captions:
        step_5c_upload_youtube_captions(args.story, stories[args.story], "short")
        step_5c_upload_youtube_captions(args.story, stories[args.story], "long")

    if args.upload_short:
        mp4_short = DIST_DIR / f"{args.story}-short-9x16.mp4"
        yt_short_id = step_5c_upload_youtube(args.story, stories[args.story], "short", mp4_short)
        args.bind_short_id = yt_short_id
        if args.embed_status is None:
            args.embed_status = "uploaded_unlisted"

    if args.upload_long:
        mp4_long = DIST_DIR / f"{args.story}-long-16x9.mp4"
        yt_long_id = step_5c_upload_youtube(args.story, stories[args.story], "long", mp4_long)
        args.bind_long_id = yt_long_id
        if args.embed_status is None:
            args.embed_status = "uploaded_unlisted"

    if args.bind_long_id is not None or args.bind_short_id is not None or args.embed_status is not None:
        long_id, short_id, st_now = step_5d_embed_into_post(
            args.html, args.story, args.bind_long_id, args.bind_short_id, args.embed_status
        )
        print(
            f"[5D Embed] Đã nhúng vào bài '{args.story}' trong {args.html.relative_to(ROOT)}: "
            f"long.youtubeId={long_id!r}, short.youtubeId={short_id!r}, embedStatus={st_now!r}"
        )
        src = args.html.read_text(encoding="utf-8")
        stories = extract_stories(src)

    manifest = step_5a_5b_manifest(args.story, stories[args.story], args.mode, args.video_mode)
    long_cfg = manifest["formats"]["long"]
    short_cfg = manifest["formats"]["short"]
    print(
        f"[5A-5C Pipeline] Bài '{args.story}' (status={manifest['storyStatus']!r}, channel={manifest['youtubeChannel']['handle']}, videoMode={args.video_mode}): "
        f"Dài {len(long_cfg['scenes'])} cảnh ({long_cfg['aspectRatio']}, voice={long_cfg['elevenlabsVoiceId']}, "
        f"embed={long_cfg['embedStatus']}, yt={long_cfg['youtubeId'] or 'chưa gán'}) | "
        f"Ngắn {len(short_cfg['scenes'])} cảnh ({short_cfg['aspectRatio']}, embed={short_cfg['embedStatus']}, "
        f"yt={short_cfg['youtubeId'] or 'chưa gán'}) -> dist/youtube/{args.story}-elevenlabs-youtube-manifest.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
