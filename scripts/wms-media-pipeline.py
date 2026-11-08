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
import hashlib
import http.server
import importlib.util
import json
import os
import pathlib
import re
import shutil
import sys
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
DEFAULT_VOICE_SPEC = "eleven_flash_v2_5:vi_editorial"
DEFAULT_VEO_MODEL = "veo-3.1-generate-preview"
DEFAULT_VEO_FAST_MODEL = "veo-3.1-fast-generate-preview"
DEFAULT_YT_HANDLE = "@WhereMoneySleeps"
DEFAULT_YT_URL = "https://www.youtube.com/@WhereMoneySleeps"
DEFAULT_REF_IMAGES = [
    "public/brand/youtube-banner-2560x1440-safezone.jpg",
    "public/brand/youtube-avatar-1024x1024.png",
]


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
    redirect_uri = f"http://localhost:{port}"
    scopes = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"

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
    captured: dict[str, str] = {}

    class OAuthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
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

    print("=== ĐĂNG NHẬP OAUTH 2.0 CHO KÊNH @WhereMoneySleeps ===")
    print(f"1. Mở URL sau trên trình duyệt (chọn đúng tài khoản quản lý kênh @WhereMoneySleeps):\n   {auth_url}\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass
    print(f"2. Đang chờ Google gọi ngược về {redirect_uri} ...")
    with http.server.HTTPServer(("127.0.0.1", port), OAuthHandler) as httpd:
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


def step_5c_upload_youtube(story_key: str, story: dict, fmt: str, mp4_path: pathlib.Path) -> str:
    """
    5C — Đẩy file `.mp4` lên kênh `@WhereMoneySleeps` qua YouTube Data API v3 Resumable Upload.
    Bắt buộc đặt `privacyStatus = "unlisted"` khi `story.status != "published"` (WMS-R4 / QĐ 56).
    Trả về `youtubeId` 11 ký tự.
    """
    if not mp4_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file video để upload: {mp4_path}")
    access_token = get_youtube_access_token()
    fobj = (story.get("videoScript") or {}).get(fmt) or {}
    scenes = fobj.get("scenes") or []
    raw_title = str(fobj.get("title") or story.get("title") or story_key).strip()
    title = f"{raw_title} #Shorts" if fmt == "short" and "#Shorts" not in raw_title else raw_title
    chapters = build_youtube_chapters(scenes, raw_title)
    desc = (
        f"{story.get('teaser', '')}\n\n"
        f"Bài viết tương tác đầy đủ (Mặt cắt Kiến trúc Đêm Diorama v3.0 & Sổ kế toán TT 99/2025):\n"
        f"Where Money Sleeps ({DEFAULT_YT_HANDLE})\n\n"
        f"Mục lục chương:\n{chapters}\n\n"
        f"---\n"
        f"Lưu ý: Số liệu trong video là ví dụ minh hoạ để thấy cơ chế vận hành, không phải lời khuyên tài chính.\n"
        f"Audio generated by ElevenLabs · Visuals & Accounting Diorama by Where Money Sleeps."
    )
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
    with urllib.request.urlopen(init_req, timeout=60) as init_resp:
        upload_url = init_resp.headers.get("Location")
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
    m_vs = re.search(r"\bvideoScript\s*:\s*\{", src[m_story.start() :])
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


def build_youtube_chapters(scenes: list[dict], story_title: str) -> str:
    lines = [f"0:00 Mở đầu — {story_title}"]
    for idx, sc in enumerate(scenes):
        t0 = parse_start_mmss(sc.get("time", ""))
        beat = sc.get("beat")
        label = "Hook mở đầu" if idx == 0 else ("Cảnh kết" if idx == len(scenes) - 1 else f"Đoạn {int(beat) + 1}" if isinstance(beat, int) else f"Cảnh {idx + 1}")
        if t0 != "0:00":
            lines.append(f"{t0} {label}")
    return "\n".join(lines)


def step_5a_5b_manifest(story_key: str, story: dict, mode: str, video_mode: str = "veo-hybrid") -> dict:
    """5A (ElevenLabs TTS with-timestamps + SFX) & 5B (Google Veo 3.1 Video + FFmpeg Diorama/TT99 Overlay 16:9/9:16)."""
    load_dotenv()
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
            model_id = "eleven_flash_v2_5"
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
                # Gọi ElevenLabs /v1/text-to-speech/{voice_id}/with-timestamps
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
                body = json.dumps(
                    {
                        "text": vo,
                        "model_id": model_id,
                        "previous_text": prev_text,
                        "next_text": next_text,
                    }
                ).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
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
                "provider": "ElevenLabs API (Text to Speech with-timestamps + Sound Effects)",
                "requiredKeyScopes": ["Text to Speech", "Sound Effects", "Voices (Read)", "Pronunciation Dictionaries"],
                "cacheDir": ".cache/elevenlabs/",
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
                "categoryId": "27",
                "defaultLanguage": "vi",
                "privacyStatus": "unlisted" if story.get("status") != "published" else "public",
                "selfDeclaredMadeForKids": False,
                "containsSyntheticMedia": True,
                "chaptersDescription": build_youtube_chapters(scenes, str(fobj.get("title") or story.get("title") or "")),
            },
            "scenes": scene_plan,
        }

    manifest = {
        "schemaVersion": "1.2-qd56-elevenlabs-google-veo",
        "story": story_key,
        "storyStatus": story.get("status"),
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
            fobj["embedStatus"] = target_status
        if not fobj.get("elevenlabsVoiceId"):
            fobj["elevenlabsVoiceId"] = DEFAULT_VOICE_SPEC

    new_vs_json = json.dumps(vid, ensure_ascii=False, indent=1)
    updated_src = src[:start] + new_vs_json + src[end:]
    html_path.write_text(updated_src, encoding="utf-8")
    return (
        vid["long"].get("youtubeId", ""),
        vid["short"].get("youtubeId", ""),
        vid["long"].get("embedStatus", "pending_upload"),
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

    if not args.story:
        ap.error("Cần truyền `--story <slug>` (hoặc `--check-env` / `--auth-youtube`)")

    src = args.html.read_text(encoding="utf-8")
    stories = extract_stories(src)
    if args.story not in stories:
        print(f"LỖI: Không tìm thấy bài '{args.story}' trong STORIES", file=sys.stderr)
        return 1

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
