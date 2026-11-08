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
import importlib.util
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "docs/prototype.html"
LICENCES_JSON = ROOT / "legal/licences.json"
ENV_FILE = ROOT / ".env"
CACHE_DIR = ROOT / ".cache/elevenlabs"
DIST_DIR = ROOT / "dist/youtube"

YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
VALID_EMBED_STATUS = {"pending_upload", "uploaded_unlisted", "uploaded_private", "uploaded_public"}
VALID_VIDEO_MODES = ("hybrid", "elevenlabs-full", "programmatic")
DEFAULT_VOICE_SPEC = "eleven_flash_v2_5:vi_editorial"
DEFAULT_VIDEO_MODEL = "veo-3.1-fast-generate-001"
DEFAULT_YT_HANDLE = "@WhereMoneySleeps"
DEFAULT_YT_URL = "https://www.youtube.com/@WhereMoneySleeps"


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


def run_check_env() -> int:
    """Kiểm tra sẵn sàng của `.env`, ElevenLabs API Key và YouTube OAuth (`@WhereMoneySleeps`)."""
    load_dotenv()
    lic = verify_elevenlabs_licence()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    video_model = os.environ.get("ELEVENLABS_VIDEO_MODEL", DEFAULT_VIDEO_MODEL).strip()
    video_mode = os.environ.get("WMS_VIDEO_MODE", "hybrid").strip()
    yt_handle = os.environ.get("YOUTUBE_CHANNEL_HANDLE", DEFAULT_YT_HANDLE).strip()
    yt_url = os.environ.get("YOUTUBE_CHANNEL_URL", DEFAULT_YT_URL).strip()
    yt_secret = ROOT / os.environ.get("YOUTUBE_CLIENT_SECRET_FILE", ".secrets/youtube_client_secret.json")
    yt_token = ROOT / os.environ.get("YOUTUBE_TOKEN_FILE", ".secrets/youtube_token.json")

    print("=== KIỂM TRA CẤU HÌNH PIPELINE BƯỚC 5 (QĐ 56) ===")
    print(f"  [PASS] Giấy phép ElevenLabs (legal/licences.json): {lic.get('id')} ({lic.get('status')})")
    print(f"  [PASS] Kênh YouTube đích: {yt_handle} ({yt_url})")
    print(f"  [INFO] Chế độ dựng Video (5B): video_mode={video_mode!r} · model={video_model!r}")
    if ENV_FILE.is_file():
        print(f"  [PASS] File .env: đã tạo tại {ENV_FILE.relative_to(ROOT)}")
    else:
        print(f"  [WAIT] File .env: chưa tạo (chạy `cp .env.example .env` trong where-money-sleeps/)")

    if api_key:
        masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"  [PASS] ELEVENLABS_API_KEY: đã khai báo ({masked})")
    else:
        print("  [WAIT] ELEVENLABS_API_KEY: chưa điền trong .env")

    if yt_secret.is_file():
        print(f"  [PASS] YouTube OAuth client_secret: {yt_secret.relative_to(ROOT)}")
    else:
        print(f"  [WAIT] YouTube OAuth client_secret: chưa đặt file tại {yt_secret.relative_to(ROOT)}")

    if yt_token.is_file():
        print(f"  [PASS] YouTube OAuth refresh token: {yt_token.relative_to(ROOT)}")
    else:
        print(f"  [INFO] YouTube OAuth refresh token: sẽ tự sinh ở lần đăng nhập đầu tiên ({yt_token.relative_to(ROOT)})")
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


def scene_cache_key(voice_spec: str, fmt: str, idx: int, vo: str, on_screen: str) -> str:
    payload = json.dumps(
        {"voice": voice_spec, "fmt": fmt, "idx": idx, "vo": vo.strip(), "onScreen": on_screen.strip()},
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


def step_5a_5b_manifest(story_key: str, story: dict, mode: str, video_mode: str = "hybrid") -> dict:
    """5A (ElevenLabs TTS with-timestamps + SFX) & 5B (ElevenLabs /v1/flows/video + Diorama v3.0 16:9/9:16)."""
    load_dotenv()
    lic = verify_elevenlabs_licence()
    vid = story.get("videoScript") or {}
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    video_model = os.environ.get("ELEVENLABS_VIDEO_MODEL", DEFAULT_VIDEO_MODEL).strip()
    yt_handle = os.environ.get("YOUTUBE_CHANNEL_HANDLE", DEFAULT_YT_HANDLE).strip()
    yt_url = os.environ.get("YOUTUBE_CHANNEL_URL", DEFAULT_YT_URL).strip()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    formats_out = {}
    for fmt in ("long", "short"):
        fobj = vid.get(fmt) or {}
        voice_spec = str(fobj.get("elevenlabsVoiceId") or DEFAULT_VOICE_SPEC).strip()
        model_id, _, voice_id = voice_spec.partition(":")
        if not voice_id:
            voice_id = model_id
            model_id = "eleven_flash_v2_5"
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

            use_el_video = video_mode == "elevenlabs-full" or (
                video_mode == "hybrid" and (i == 0 or i == len(scenes) - 1)
            )
            scene_plan.append(
                {
                    "sceneIndex": i,
                    "time": sc.get("time"),
                    "beat": sc.get("beat"),
                    "sha256CacheKey": ck,
                    "cached": cache_file.is_file(),
                    "elevenlabsTtsEndpoint": f"/v1/text-to-speech/{voice_id}/with-timestamps",
                    "elevenlabsModelId": model_id,
                    "elevenlabsVideoEndpoint": "/v1/flows/video" if use_el_video else None,
                    "elevenlabsVideoModelId": video_model if use_el_video else None,
                    "visualPrompt": visual,
                    "sfxEndpoint": "/v1/sound-generation" if sfx_prompt else None,
                    "sfxPrompt": sfx_prompt,
                    "voWords": len(vo.split()),
                }
            )

        resolution = "1920x1080" if fmt == "long" else "1080x1920"
        aspect = "16:9" if fmt == "long" else "9:16"
        mp4_name = f"{story_key}-{fmt}-{aspect.replace(':', 'x')}.mp4"
        formats_out[fmt] = {
            "title": fobj.get("title"),
            "aspectRatio": aspect,
            "resolution": resolution,
            "videoMode": video_mode,
            "elevenlabsVideoApi": {
                "createEndpoint": "POST https://api.elevenlabs.io/v1/flows/video",
                "statusEndpoint": "GET https://api.elevenlabs.io/v1/flows/video/:generation_id",
                "modelId": video_model,
                "requiredScope": "Image & Video (Flows)",
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
        "schemaVersion": "1.1-qd56",
        "story": story_key,
        "storyStatus": story.get("status"),
        "youtubeChannel": {
            "handle": yt_handle,
            "url": yt_url,
        },
        "licenceCheck": {
            "id": lic.get("id"),
            "licence": lic.get("licence"),
            "status": lic.get("status"),
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
    ap.add_argument("--check-env", action="store_true", help="Kiểm tra file .env, ELEVENLABS_API_KEY và YouTube OAuth")
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
        default="hybrid",
        help="Chế độ dựng hình ảnh video 5B (hybrid | elevenlabs-full | programmatic)",
    )
    ap.add_argument("--bind-long-id", default=None, help="Gán mã YouTube Video ID 11 ký tự cho bản Dài 16:9 và nhúng vào bài")
    ap.add_argument("--bind-short-id", default=None, help="Gán mã YouTube Video ID 11 ký tự cho bản Shorts 9:16 và nhúng vào bài")
    ap.add_argument(
        "--embed-status",
        choices=sorted(VALID_EMBED_STATUS),
        default=None,
        help="Trạng thái nhúng YouTube (pending_upload | uploaded_unlisted | uploaded_private | uploaded_public)",
    )
    args = ap.parse_args()

    if args.check_env:
        return run_check_env()

    if not args.story:
        ap.error("Cần truyền `--story <slug>` (hoặc `--check-env` để kiểm tra cấu hình)")

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
    if args.story not in stories:
        print(f"LỖI: Không tìm thấy bài '{args.story}' trong STORIES", file=sys.stderr)
        return 1

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
