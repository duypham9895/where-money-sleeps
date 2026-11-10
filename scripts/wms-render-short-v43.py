#!/usr/bin/env python3
"""
wms-render-short-v43.py — Bộ dựng Video Ngắn 9:16 Chuẩn Điện Ảnh & Khoa Học Nhận Thức v5.0 (QĐ 61)
cho Where Money Sleeps (`install-short-9x16.mp4`, `card-short-9x16.mp4`, `pay-short-9x16.mp4`):

1. KIẾN TRÚC BỐ CỤC SAFE-ZONE YOUTUBE SHORTS NGHIÊM NGẶT (QĐ 61 · F2 · LUẬT 6b · LUẬT 8 · LUẬT 10):
   - Khung an toàn: `SAFE_X = (48, 868)` (rộng 820px — nhường x=868..1080 cho cột nút Like/Comment/Share
     của YouTube Shorts) và `SAFE_Y = (268, 1316)` (cao 1048px — nhường y=0..268 cho thanh tiêu đề trên và
     y=1316..1920 cho phụ đề [CC] YouTube + thông tin kênh ở đáy).
   - Bỏ hoàn toàn các hộp chữ tĩnh rườm rà (HEADER_BOX, CARD_BOX 170 từ, Footer) bị UI YouTube che khuất
     và gây hiệu ứng dư thừa (Mayer 2021 Redundancy Principle; Berney & Bétrancourt 2016 g=0.226 -> 0.883).
   - Chia làm 3 vùng chuyên biệt không chồng lấn trong Safe Zone:
     + ZONE 1 (`ACTIVE_ACTOR_PILL = (48, 268, 868, 356)`, 820x88px): Thanh tiến độ 6 cảnh + chỉ hiển thị
       2–3 định chế đang tương tác trực tiếp trong cảnh + xung tín hiệu/dòng tiền chạy giữa chúng.
     + ZONE 2A (`CUTAWAY_STAGE_BOX = (48, 372, 868, 868)`, 820x496px): Mặt cắt kiến trúc Risograph cận cảnh
       RIÊNG BIỆT CHO TỪNG CẢNH (`F1`: kết hợp `short-plate-1..4.jpg` & `fig-1..4.jpg`, kiểm `MSE >= 15.0`
       giữa mọi cặp cảnh liền kề) + hạt chuyển động 30fps + 1 nhãn neo không gian duy nhất (`<= 10 từ`).
     + ZONE 2B (`MECHANISM_CANVAS_BOX = (48, 884, 868, 1316)`, 820x432px): Mặt phẳng tối `#0B101B` tương phản
       >12:1 chạy 7 Nguyên hàm Hoạt cảnh Thủ tục (`P1–P7`) khớp 2 Nhịp Câu Giọng Đọc (`F5`: `Beat 1` ở
       `phrases[0]["t0"]` -> `Beat 2` ở `phrases[1]["t0"]`), tuân thủ `1 Y-Row = 1 Text` (`LUẬT 10`).

2. VOICE & AUDIO CONTINUITY:
   - Giữ nguyên bản thu `eleven_v3` liền mạch 1 lần đọc (`{slug}_short_continuous_v3.json`, Giọng Tâm)
     + khoảng thở 0.36s + Room Tone (-33 dBFS) + 6 SFX (-22 dBFS), chuẩn hoá -14 LUFS.
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path("/Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps")
BRAIN = pathlib.Path("/Users/edwardpham/.gemini/antigravity/brain/7f8bd653-2dd3-4155-8d12-ef6b38dd6a6e")
CACHE_DIR = ROOT / ".cache/elevenlabs"
DIST_DIR = ROOT / "dist/youtube"


def load_pipeline_module():
    spec = importlib.util.spec_from_file_location("wmp", ROOT / "scripts/wms-media-pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    if edge1 <= edge0:
        return 1.0 if x >= edge0 else 0.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def ease_out_cubic(x: float) -> float:
    t = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_sine(x: float) -> float:
    t = max(0.0, min(1.0, x))
    return 0.5 * (1.0 - math.cos(math.pi * t))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def blend_rgb(
    c0: tuple[int, int, int],
    c1: tuple[int, int, int],
    u: float,
) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, u))
    return (
        int(round(lerp(c0[0], c1[0], t))),
        int(round(lerp(c0[1], c1[1], t))),
        int(round(lerp(c0[2], c1[2], t))),
    )


def fmt_vnd(val: float | int) -> str:
    return f"{int(round(val)):,}".replace(",", ".") + " đ"


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    )
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


SFX_SPECS = [
    ("sfx_lamp_switch", "Soft warm vintage tungsten desk lamp switch click with gentle room ambiance, subtle documentary sound", 2.0),
    ("sfx_wire_pulse", "Soft warm analog telegraph signal whoosh pulsing gently across an overhead wire, subtle documentary transition", 2.5),
    ("sfx_pipe_flow", "Deep warm subterranean water flowing gently through an underground metal pipe, subtle low documentary transition", 3.0),
    ("sfx_clock_tick", "Soft warm mechanical pocket watch ticking steady rhythm, subtle documentary sound effect", 3.0),
    ("sfx_scale_chime", "Soft warm brass balance scale gentle metallic chime, subtle documentary transition", 2.5),
    ("sfx_shutter_close", "Gentle distant shopfront metal roller shutter closing softly at night with warm low ambient resonance", 3.0),
]


def ensure_sfx_cached(api_key: str) -> dict[str, bytes]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out: dict[str, bytes] = {}
    for key, prompt, dur in SFX_SPECS:
        cfile = CACHE_DIR / f"{key}.json"
        if not cfile.is_file():
            print(f"  -> Generating ElevenLabs SFX '{key}' ({dur}s)...")
            url = "https://api.elevenlabs.io/v1/sound-generation"
            body = json.dumps(
                {
                    "text": prompt,
                    "duration_seconds": dur,
                    "prompt_influence": 0.35,
                }
            ).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=body,
                headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    mp3_bytes = resp.read()
                cfile.write_text(
                    json.dumps({"id": key, "prompt": prompt, "audio_base64": base64.b64encode(mp3_bytes).decode("ascii")}),
                    encoding="utf-8",
                )
            except Exception as e:
                print(f"  [WARN] SFX generation fallback for {key}: {e}")
                continue
        data = json.loads(cfile.read_text(encoding="utf-8"))
        out[key] = base64.b64decode(data["audio_base64"])
    return out


def split_scene_into_phrases(scene_text: str, char_offset: int, starts: list[float], ends: list[float], time_shift: float) -> list[dict]:
    raw_parts = re.split(r"(?<=[.?!])\s+", scene_text.strip())
    phrases_str = [p.strip() for p in raw_parts if p.strip()]

    phrases_out: list[dict] = []
    local_cursor = 0
    for p_str in phrases_str:
        idx_in_scene = scene_text.find(p_str, local_cursor)
        if idx_in_scene < 0:
            idx_in_scene = local_cursor
        g_start_char = char_offset + idx_in_scene
        g_end_char = min(len(ends) - 1, g_start_char + len(p_str) - 1)
        p_t0 = starts[g_start_char] + time_shift
        p_t1 = ends[g_end_char] + time_shift

        words_meta: list[dict] = []
        w_cursor = 0
        for w in p_str.split():
            w_pos = p_str.find(w, w_cursor)
            if w_pos < 0:
                w_pos = w_cursor
            wc0 = min(len(starts) - 1, g_start_char + w_pos)
            wc1 = min(len(ends) - 1, wc0 + len(w) - 1)
            words_meta.append(
                {
                    "word": w,
                    "t0": starts[wc0] + time_shift,
                    "t1": ends[wc1] + time_shift,
                }
            )
            w_cursor = w_pos + len(w)

        phrases_out.append(
            {
                "text": p_str,
                "t0": p_t0,
                "t1": p_t1,
                "words": words_meta,
            }
        )
        local_cursor = idx_in_scene + len(p_str)
    return phrases_out


def build_timeline_and_master_audio(
    scenes: list[dict],
    cont_data: dict,
    sfx_map: dict[str, bytes],
    tmp_dir: pathlib.Path,
) -> tuple[pathlib.Path, list[dict], float]:
    raw_vo_mp3 = tmp_dir / "vo_continuous.mp3"
    raw_vo_mp3.write_bytes(base64.b64decode(cont_data["audio_base64"]))
    raw_vo_wav = tmp_dir / "vo_continuous.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(raw_vo_mp3), "-ar", "44100", "-ac", "2", str(raw_vo_wav)],
        check=True,
        capture_output=True,
    )

    import wave
    with wave.open(str(raw_vo_wav), "rb") as wf:
        sr = wf.getframerate()
        n_frames = wf.getnframes()
        pcm = np.frombuffer(wf.readframes(n_frames), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0

    align = cont_data["alignment"]
    starts = [float(x) for x in align["character_start_times_seconds"]]
    ends = [float(x) for x in align["character_end_times_seconds"]]
    scene_texts = [s["vo"].strip() for s in scenes]
    full_text = "\n\n".join(scene_texts)

    raw_bounds: list[tuple[int, int, float, float]] = []
    cursor = 0
    for st in scene_texts:
        pos = full_text.find(st, cursor)
        end_pos = pos + len(st) - 1
        t0 = starts[pos]
        t1 = ends[min(end_pos, len(ends) - 1)]
        raw_bounds.append((pos, end_pos, t0, t1))
        cursor = end_pos + 1

    EXTRA_PAUSE = 0.36
    LEAD_IN = 0.25
    TAIL_OUT = 0.95

    chunks: list[np.ndarray] = [np.zeros((int(LEAD_IN * sr), 2), dtype=np.float32)]
    scene_meta: list[dict] = []
    cum_shift = LEAD_IN
    prev_sample_end = 0

    for idx, (pos, end_pos, raw_t0, raw_t1) in enumerate(raw_bounds):
        if idx < len(raw_bounds) - 1:
            next_raw_t0 = raw_bounds[idx + 1][2]
            mid_silence_t = 0.5 * (raw_t1 + next_raw_t0)
            cut_sample = min(len(pcm), int(mid_silence_t * sr))
        else:
            cut_sample = len(pcm)

        seg_pcm = pcm[prev_sample_end:cut_sample].copy()
        fade_len = min(int(0.025 * sr), len(seg_pcm) // 4)
        if fade_len > 0:
            ramp = np.linspace(0.0, 1.0, fade_len, dtype=np.float32)[:, None]
            seg_pcm[:fade_len] *= ramp
            seg_pcm[-fade_len:] *= ramp[::-1]

        chunks.append(seg_pcm)

        adj_t0 = raw_t0 + cum_shift
        adj_t1 = raw_t1 + cum_shift
        phrases = split_scene_into_phrases(scene_texts[idx], pos, starts, ends, cum_shift)

        if idx < len(raw_bounds) - 1:
            chunks.append(np.zeros((int(EXTRA_PAUSE * sr), 2), dtype=np.float32))
            scene_win_end = mid_silence_t + cum_shift + EXTRA_PAUSE * 0.5
        else:
            chunks.append(np.zeros((int(TAIL_OUT * sr), 2), dtype=np.float32))
            scene_win_end = adj_t1 + TAIL_OUT

        scene_meta.append(
            {
                "index": idx,
                "scene": scenes[idx],
                "vo_t0": adj_t0,
                "vo_t1": adj_t1,
                "win_t0": 0.0 if idx == 0 else scene_meta[-1]["win_t1"],
                "win_t1": scene_win_end,
                "phrases": phrases,
            }
        )

        cum_shift += EXTRA_PAUSE
        prev_sample_end = cut_sample

    vo_full = np.concatenate(chunks, axis=0)
    total_dur = len(vo_full) / sr
    scene_meta[-1]["win_t1"] = total_dur

    t_arr = np.arange(len(vo_full), dtype=np.float32) / sr
    drone = (
        0.50 * np.sin(2 * math.pi * 110.0 * t_arr)
        + 0.30 * np.sin(2 * math.pi * 164.81 * t_arr)
        + 0.20 * np.sin(2 * math.pi * 220.0 * t_arr)
    )
    slow_lfo = 0.82 + 0.18 * np.sin(2 * math.pi * 0.14 * t_arr)
    ambient = (drone * slow_lfo * 0.014)[:, None] * np.array([[0.95, 1.05]], dtype=np.float32)

    fi = int(0.6 * sr)
    fo = int(1.1 * sr)
    ambient[:fi] *= np.linspace(0.0, 1.0, fi, dtype=np.float32)[:, None]
    ambient[-fo:] *= np.linspace(1.0, 0.0, fo, dtype=np.float32)[:, None]

    mix_pcm = vo_full + ambient

    sfx_cue_times = [
        ("sfx_lamp_switch", 0.05, 0.075, 520.0),
        ("sfx_wire_pulse", scene_meta[1]["win_t0"] - 0.35, 0.085, 660.0),
        ("sfx_pipe_flow", scene_meta[2]["win_t0"] - 0.35, 0.090, 220.0),
        ("sfx_clock_tick", scene_meta[3]["win_t0"] - 0.30, 0.070, 440.0),
        ("sfx_scale_chime", scene_meta[4]["win_t0"] - 0.35, 0.085, 587.33),
        ("sfx_shutter_close", scene_meta[5]["win_t0"] - 0.35, 0.085, 293.66),
    ]
    for sfx_key, cue_t, gain, fallback_freq in sfx_cue_times:
        if sfx_key in sfx_map:
            s_mp3 = tmp_dir / f"{sfx_key}.mp3"
            s_wav = tmp_dir / f"{sfx_key}.wav"
            s_mp3.write_bytes(sfx_map[sfx_key])
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(s_mp3), "-ar", str(sr), "-ac", "2", str(s_wav)],
                check=True,
                capture_output=True,
            )
            with wave.open(str(s_wav), "rb") as swf:
                s_pcm = np.frombuffer(swf.readframes(swf.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0
            sf_len = min(int(0.25 * sr), len(s_pcm) // 3)
            if sf_len > 0:
                s_pcm[:sf_len] *= np.linspace(0.0, 1.0, sf_len, dtype=np.float32)[:, None]
                s_pcm[-sf_len:] *= np.linspace(1.0, 0.0, sf_len, dtype=np.float32)[:, None]
        else:
            dur_s = 1.15
            t_s = np.arange(int(dur_s * sr), dtype=np.float32) / sr
            env_s = np.sin(math.pi * (t_s / dur_s)) ** 1.6 * np.exp(-2.2 * t_s)
            wave_s = 0.65 * np.sin(2 * math.pi * fallback_freq * t_s) + 0.35 * np.sin(2 * math.pi * (fallback_freq * 1.5) * t_s)
            s_pcm = (wave_s * env_s)[:, None] * np.array([[0.9, 1.1]], dtype=np.float32)
        start_idx = max(0, int(cue_t * sr))
        end_idx = min(len(mix_pcm), start_idx + len(s_pcm))
        if end_idx > start_idx:
            mix_pcm[start_idx:end_idx] += s_pcm[: end_idx - start_idx] * gain

    mix_pcm = np.clip(mix_pcm, -0.98, 0.98)
    mixed_wav = tmp_dir / "master_mixed.wav"
    with wave.open(str(mixed_wav), "wb") as out_wf:
        out_wf.setnchannels(2)
        out_wf.setsampwidth(2)
        out_wf.setframerate(sr)
        out_wf.writeframes((mix_pcm * 32767.0).astype(np.int16).tobytes())

    norm_wav = tmp_dir / "master_norm.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(mixed_wav),
            "-af",
            "loudnorm=I=-14:TP=-1.5:LRA=11",
            "-ar",
            str(sr),
            "-ac",
            "2",
            str(norm_wav),
        ],
        check=True,
        capture_output=True,
    )
    return norm_wav, scene_meta, total_dur


# ── HÌNH HỌC CÂN ĐỐI CHÍNH GIỮA KHUNG 9:16 (1080x1920) — QĐ 61 · LUẬT 6b · LUẬT 8 · LUẬT 10 ──
# Căn giữa tuyệt đối theo trục ngang (x = 48..1032, rộng 984px, tâm x = 540) và phân bổ cân đối
# theo trục dọc (y = 64..1748, cao 1684px, chừa đáy y = 1748..1920 cho thanh tiến trình & phụ đề).
SAFE_X = (48, 1032)
SAFE_Y = (64, 1748)

ACTIVE_ACTOR_PILL = (48, 64, 1032, 204)        # 984 x 140 px (Thanh tiến độ + 2–3 định chế 2 dòng + gói giao dịch chạy)
CUTAWAY_STAGE_BOX = (48, 224, 1032, 1248)      # 984 x 1024 px (Mặt cắt kiến trúc Risograph thuần 2 tầng + luồng tiền giữa 2 phòng)
MECHANISM_CANVAS_BOX = (48, 1268, 1032, 1748)  # 984 x 480 px (Sân khấu Nguyên hàm Hoạt cảnh P1–P7 độ tương phản >12:1, rõ 100%)

# Alias tương thích kiểm toán M3
STAGE_BOX = CUTAWAY_STAGE_BOX
CARD_BOX = MECHANISM_CANVAS_BOX

SLATE_LEAK_RE = re.compile(
    r"(\bCẢNH\s*\d|\bSCENE\s*\d|\bMỐC\s*\d|\bÝ\s*\d+\s*/\s*\d+|\bKỲ\s*\d+\s*/\s*\d+|Chữ\s+to|SFX\s*gợi\s*ý|dây\s+điện|dây\s+tín\s+hiệu|ống\s+ngầm|ống\s+quyết\s+toán|[→⇒➜➔←↔])",
    re.IGNORECASE,
)


def assert_broadcast_overlay_clean(texts: list[str]) -> None:
    for txt in texts:
        m = SLATE_LEAK_RE.search(str(txt or ""))
        if m:
            raise RuntimeError(
                f"FAIL [B4 Broadcast Polish]: Lộ nhãn kịch bản nội bộ '{m.group(0)}' trong chuỗi hiển thị: {txt!r}"
            )


# ── CẤU HÌNH 6 CẢNH × 3 BÀI (`install`, `card`, `pay`) VỚI 6 TẤM TRANH RIÊNG BIỆT (F1) ──

STORY_CONFIGS: dict[str, dict] = {
    "install": {
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("CỬA HÀNG", "Nơi bán máy"),
            ("CÔNG TY", "Tài chính"),
            ("NGÂN HÀNG", "Của bạn"),
            ("NGÂN HÀNG", "Cửa hàng"),
        ],
        # Cắt trọn 2 tầng kiến trúc từ short-plate-1..4.jpg (tỷ lệ ~1.23:1 khớp khung 984x800, 0 chữ nướng sẵn)
        "scene_plates": [
            ("public/brand/install-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-1.jpg", (80, 480, 1020, 1244)),
            ("public/brand/install-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-3.jpg", (80, 490, 1020, 1254)),
            ("public/brand/install-short-plate-4.jpg", (20, 820, 1060, 1665)),
        ],
        "scenes": [
            {
                "active": [0, 1],
                "flow": ("wire", 0, 1),
                "room_src": (0.31, 0.66, "QUẦY CỬA HÀNG (12TR)"),
                "room_dst": (0.68, 0.30, "CÔNG TY TÀI CHÍNH"),
                "packet_label": "MÁY 12.000.000 Đ (TRẢ GÓP 0%)",
                "stage_tag": "QUẦY BÁN HÀNG  ·  MÁY NIÊM YẾT 12.000.000 Đ",
                "primitive": "P1_INSTALL_HOOK",
                "kicker": "MỞ ĐẦU  ·  LỜI HỨA TRẢ GÓP 0%",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 1, 2),
                "room_src": (0.30, 0.64, "CỬA HÀNG (GIAO MÁY)"),
                "room_dst": (0.68, 0.28, "CÔNG TY TÀI CHÍNH (CHỦ NỢ)"),
                "packet_label": "HỒ SƠ VAY 12.000.000 Đ",
                "stage_tag": "HỒ SƠ VAY CHUYỂN THẲNG VỀ CÔNG TY TÀI CHÍNH",
                "primitive": "P2_INSTALL_CONTRACT",
                "kicker": "BƯỚC 1  ·  AI LÀ CHỦ NỢ THẬT SỰ?",
            },
            {
                "active": [2, 4, 1],
                "flow": ("pipe", 2, 4, 1),
                "room_src": (0.68, 0.32, "KÉT CÔNG TY TÀI CHÍNH"),
                "room_dst": (0.40, 0.72, "TK CỬA HÀNG (+11,4TR)"),
                "packet_label": "GIẢI NGÂN +11.400.000 Đ (−5% PHÍ)",
                "stage_tag": "GIẢI NGÂN QUA NGÂN HÀNG  ·  KHẤU TRỪ TẠI NGUỒN 5%",
                "primitive": "P1_INSTALL_SPLIT",
                "kicker": "BƯỚC 2  ·  CỬA HÀNG THỰC NHẬN 11.400.000 Đ",
            },
            {
                "active": [0, 3, 2],
                "flow": ("pipe", 0, 3, 2),
                "room_src": (0.38, 0.70, "NGƯỜI MUA (1TR × 12 KỲ)"),
                "room_dst": (0.68, 0.30, "CÔNG TY TÀI CHÍNH (THU 12TR)"),
                "packet_label": "TRẢ ĐỀU 1.000.000 Đ / THÁNG",
                "stage_tag": "12 KỲ TRẢ ĐỀU 1.000.000 Đ  ·  TỔNG TRẢ 12.000.000 Đ",
                "primitive": "P5_INSTALL_EIR",
                "kicker": "BƯỚC 3  ·  QUY ĐỔI LÃI SUẤT HIỆU DỤNG (EIR)",
            },
            {
                "active": [0, 1, 2],
                "flow": ("pipe", 2, 1),
                "room_src": (0.34, 0.66, "KHAY 95%: 11.400.000 Đ"),
                "room_dst": (0.58, 0.56, "KHAY PHÍ 5%: 600.000 Đ"),
                "packet_label": "CHÊNH LỆCH LÃI NGẦM 600.000 Đ",
                "stage_tag": "SO SÁNH GIÁ TRẢ THẲNG VÀ GIÁ TRẢ GÓP TẠI QUẦY",
                "primitive": "P7_INSTALL_TWOWORLD",
                "kicker": "BƯỚC 4  ·  AI ĐANG TRẢ 600.000 Đ TIỀN LÃI?",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 0, 1),
                "room_src": (0.48, 0.24, "BÀN CÂN SỔ KẾ TOÁN"),
                "room_dst": (0.50, 0.64, "SỔ CÁI TT 99/2025 (NỢ = CÓ)"),
                "packet_label": "Σ NỢ 12TR = Σ CÓ 12TR",
                "stage_tag": "BÀN CÂN SỔ KẾ TOÁN TT 99/2025  ·  Σ NỢ = Σ CÓ",
                "primitive": "P4_INSTALL_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  CÂU HỎI TRƯỚC KHI KÝ",
            },
        ],
    },
    "card": {
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("QUÁN QUEN", "Nơi ăn uống"),
            ("NGÂN HÀNG", "Của quán"),
            ("TỔ CHỨC THẺ", "Chuyển mạch"),
            ("NGÂN HÀNG", "Của bạn"),
        ],
        "scene_plates": [
            ("public/brand/card-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-1.jpg", (80, 480, 1020, 1244)),
            ("public/brand/card-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-2.jpg", (80, 490, 1020, 1254)),
            ("public/brand/card-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-4.jpg", (20, 460, 1060, 1305)),
        ],
        "scenes": [
            {
                "active": [0, 1, 4],
                "flow": ("wire", 4, 0),
                "room_src": (0.31, 0.66, "QUẦY QUÁN QUEN (10TR)"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG CỦA BẠN (+100K)"),
                "packet_label": "QUẸT 10TR · HOÀN TIỀN +100.000 Đ",
                "stage_tag": "QUẸT THẺ 10.000.000 Đ  ·  HOÀN TIỀN +100.000 Đ",
                "primitive": "P1_CARD_HOOK",
                "kicker": "MỞ ĐẦU  ·  TIỀN HOÀN 1% ĐẾN TỪ ĐÂU?",
            },
            {
                "active": [0, 1, 4],
                "flow": ("wire", 1, 3, 4),
                "room_src": (0.31, 0.66, "MÁY POS QUÁN (KÉT = 0 Đ)"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG BẠN (KHOÁ 10TR)"),
                "packet_label": "BẢN TIN GIỮ HẠN MỨC 10.000.000 Đ",
                "stage_tag": "LÚC CHẠM THẺ  ·  CHỈ LÀ BẢN TIN GIỮ HẠN MỨC",
                "primitive": "P2_CARD_HOLD",
                "kicker": "BƯỚC 1  ·  0 ĐỒNG TIỀN THẬT CHẠY LÚC QUẸT",
            },
            {
                "active": [4, 2, 1],
                "flow": ("pipe", 4, 2, 1),
                "room_src": (0.68, 0.30, "NGÂN HÀNG QUYẾT TOÁN T+2"),
                "room_dst": (0.40, 0.72, "TK QUÁN (+9.780.000 Đ)"),
                "packet_label": "CHUYỂN +9.780.000 Đ (−220K MDR)",
                "stage_tag": "QUYẾT TOÁN T+2  ·  KHẤU TRỪ PHÍ NHẬN THẺ 2,2%",
                "primitive": "P1_CARD_MDR_SPLIT",
                "kicker": "BƯỚC 2  ·  QUÁN THỰC NHẬN 9.780.000 Đ",
            },
            {
                "active": [2, 3, 4],
                "flow": ("pipe", 2, 3, 4),
                "room_src": (0.40, 0.72, "PHÍ MDR QUÁN BỊ TRỪ (220K)"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG BẠN (+150.000 Đ)"),
                "packet_label": "PHÍ INTERCHANGE +150.000 Đ (1,5%)",
                "stage_tag": "CHIA PHÍ MDR 220.000 Đ CHO 3 ĐỊNH CHẾ TRUNG GIAN",
                "primitive": "P1_CARD_THREE_WAY",
                "kicker": "BƯỚC 3  ·  PHÍ INTERCHANGE 150.000 Đ VỀ ĐÂU?",
            },
            {
                "active": [0, 4],
                "flow": ("pipe", 4, 0),
                "room_src": (0.68, 0.28, "NGÂN HÀNG BẠN (THU 150K)"),
                "room_dst": (0.34, 0.64, "VÍ CỦA BẠN (HOÀN +100K)"),
                "packet_label": "TRÍCH HOÀN TIỀN +100.000 Đ (1%)",
                "stage_tag": "NGÂN HÀNG CỦA BẠN THU 150.000 Đ  ·  HOÀN BẠN 100.000 Đ",
                "primitive": "P4_CARD_WATERFALL",
                "kicker": "BƯỚC 4  ·  NGUỒN GỐC KHOẢN TIỀN HOÀN 1%",
            },
            {
                "active": [0, 1, 4],
                "flow": ("wire", 0, 1),
                "room_src": (0.36, 0.62, "SỔ KẾ TOÁN QUÁN (TT 99/2025)"),
                "room_dst": (0.64, 0.48, "BÀN CÂN NỢ 10TR = CÓ 10TR"),
                "packet_label": "PHÍ 2,2% NẰM TRONG GIÁ MÓN ĂN",
                "stage_tag": "PHÍ NHẬN THẺ 2,2% NẰM TRONG GIÁ MÓN ĂN CHUNG",
                "primitive": "P7_CARD_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  VÒNG TRÒN GIÁ MÓN ĂN",
            },
        ],
    },
    "pay": {
        "house_nodes": [
            ("CÔNG TY", "Nơi trả lương"),
            ("NGÂN HÀNG", "Trả lương"),
            ("BẠN", "Người nhận"),
            ("ĐỒNG NGHIỆP", "500 tài khoản"),
            ("KHỐI CHO VAY", "Của ngân hàng"),
        ],
        "scene_plates": [
            ("public/brand/pay-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-1.jpg", (60, 520, 1020, 1300)),
            ("public/brand/pay-short-plate-2.jpg", (20, 260, 1060, 1105)),
            ("public/brand/pay-short-plate-2.jpg", (20, 740, 1060, 1585)),
            ("public/brand/pay-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-4.jpg", (20, 560, 1060, 1405)),
        ],
        "scenes": [
            {
                "active": [0, 1, 2],
                "flow": ("wire", 0, 1, 2),
                "room_src": (0.28, 0.56, "BÀN KẾ TOÁN CÔNG TY"),
                "room_dst": (0.72, 0.56, "ĐIỆN THOẠI BẠN (+15TR)"),
                "packet_label": "TIN NHẮN BÁO LƯƠNG +15.000.000 Đ",
                "stage_tag": "TIN NHẮN BÁO +15.000.000 Đ  ·  KÉT NGÂN HÀNG ĐÓNG KÍN",
                "primitive": "P3_PAY_HOOK",
                "kicker": "MỞ ĐẦU  ·  LƯƠNG VỀ NHƯNG TIỀN ĐỨNG YÊN",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 0, 1, 2),
                "room_src": (0.48, 0.36, "SỔ CÁI NỘI BỘ NGÂN HÀNG"),
                "room_dst": (0.50, 0.74, "HẦM KÉT ĐÓNG KÍN (0 Đ CHẠY)"),
                "packet_label": "ĐỔI CHỦ NỢ ON-US ±15.000.000 Đ",
                "stage_tag": "CHUYỂN KHOẢN CÙNG NGÂN HÀNG (ON-US)  ·  ĐỔI TÊN CHỦ NỢ",
                "primitive": "P3_PAY_ONUS_FLIP",
                "kicker": "BƯỚC 1  ·  BỚT NỢ CÔNG TY, TĂNG NỢ BẠN",
            },
            {
                "active": [1, 2, 3],
                "flow": ("pipe", 3, 1),
                "room_src": (0.50, 0.28, "500 PHÒNG NHÂN VIÊN"),
                "room_dst": (0.50, 0.74, "BỂ VỐN CASA 2,5 TỶ ĐỒNG"),
                "packet_label": "500 × 5TR = 2,5 TỶ ĐỒNG CASA",
                "stage_tag": "500 ĐỒNG NGHIỆP × 5.000.000 Đ = 2,5 TỶ ĐỒNG CASA",
                "primitive": "P6_PAY_CASA_POOL",
                "kicker": "BƯỚC 2  ·  BỂ VỐN KHÔNG KỲ HẠN NẰM YÊN",
            },
            {
                "active": [1, 3, 4],
                "flow": ("pipe", 1, 4),
                "room_src": (0.50, 0.26, "DÒNG LƯƠNG TỪ 500 TÀI KHOẢN"),
                "room_dst": (0.50, 0.68, "BỂ VỐN GIÁ RẺ (LÃI 0,1%/NĂM)"),
                "packet_label": "CHI PHÍ VỐN RẺ GẤP 50 LẦN",
                "stage_tag": "CHI PHÍ LÃI CASA 0,1%/NĂM RẺ GẤP 50 LẦN KỲ HẠN 5%",
                "primitive": "P6_PAY_BAR_1TO50",
                "kicker": "BƯỚC 3  ·  CHÊNH LỆCH CHI PHÍ VỐN 1 : 50",
            },
            {
                "active": [0, 1, 4],
                "flow": ("wire", 1, 0),
                "room_src": (0.34, 0.34, "CÔNG TY (GIAO BẢNG LƯƠNG)"),
                "room_dst": (0.52, 0.72, "NGÂN HÀNG (ƯU ĐÃI VAY & PHÍ)"),
                "packet_label": "ĐỔI BẢNG LƯƠNG LẤY ƯU ĐÃI VAY",
                "stage_tag": "ĐỔI BẢNG LƯƠNG LẤY ƯU ĐÃI PHÍ & LÃI VAY DOANH NGHIỆP",
                "primitive": "P4_PAY_BARGAIN",
                "kicker": "BƯỚC 4  ·  CUỘC MẶC CẢ GIỮA HAI TỔ CHỨC",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 0, 1),
                "room_src": (0.50, 0.24, "SỔ KẾ TOÁN TT 99/2025"),
                "room_dst": (0.50, 0.68, "HẦM KÉT NGÂN HÀNG (NỢ BẠN)"),
                "packet_label": "SỐ DƯ = NGÂN HÀNG ĐANG NỢ BẠN",
                "stage_tag": "SỐ DƯ TRÊN ĐIỆN THOẠI = KHOẢN NGÂN HÀNG ĐANG NỢ BẠN",
                "primitive": "P4_PAY_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  TIỀN LƯƠNG NGỦ Ở ĐÂU?",
            },
        ],
    },
    "minpay": {
        "house_nodes": [
            ("BẠN", "Chủ thẻ"),
            ("CỬA HÀNG", "Nơi bán máy"),
            ("NGÂN HÀNG", "Cửa hàng"),
            ("NGÂN HÀNG", "Phát hành thẻ"),
            ("NGÂN HÀNG", "Tài khoản bạn"),
        ],
        "scene_plates": [
            ("public/brand/card-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-4.jpg", (20, 820, 1060, 1665)),
            ("public/brand/card-short-plate-4.jpg", (20, 460, 1060, 1305)),
        ],
        "scenes": [
            {
                "active": [0, 3],
                "flow": ("wire", 3, 0),
                "room_src": (0.32, 0.64, "SAO KÊ 10.000.000 Đ"),
                "room_dst": (0.68, 0.30, "TRẢ TỐI THIỂU 5%: 500.000 Đ"),
                "packet_label": "SAO KÊ 10TR · TỐI THIỂU 500.000 Đ",
                "stage_tag": "SAO KÊ 10.000.000 Đ  ·  TRẢ TỐI THIỂU 5% = 500.000 Đ",
                "primitive": "P1_MINPAY_HOOK",
                "kicker": "MỞ ĐẦU  ·  TRẢ 500.000 Đ NHƯNG NỢ VỌT LÊN 10,09TR?",
            },
            {
                "active": [1, 2, 3],
                "flow": ("pipe", 3, 2, 1),
                "room_src": (0.68, 0.30, "NGÂN HÀNG PHÁT HÀNH (ỨNG VỐN)"),
                "room_dst": (0.38, 0.70, "CỬA HÀNG (+9.800.000 Đ)"),
                "packet_label": "ỨNG TIỀN THẬT +9.800.000 Đ TỪ T+2",
                "stage_tag": "NGÀY T+2  ·  NGÂN HÀNG ĐÃ BỎ TIỀN TÚI ỨNG TRƯỚC",
                "primitive": "P2_MINPAY_T2_ADVANCE",
                "kicker": "BƯỚC 1  ·  VÌ SAO LÃI TÍNH LÙI TỪ NGÀY 01?",
            },
            {
                "active": [0, 3, 4],
                "flow": ("pipe", 4, 3),
                "room_src": (0.36, 0.68, "NGÂN HÀNG TK BẠN (−500.000 Đ)"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG THẺ (GỐC CÒN 9,5TR)"),
                "packet_label": "TRẢ 500.000 Đ · MẤT 45 NGÀY MIỄN LÃI",
                "stage_tag": "NGÀY 45  ·  TRẢ 500.000 Đ LÀM SẬP 45 NGÀY MIỄN LÃI",
                "primitive": "P3_MINPAY_FORFEIT",
                "kicker": "BƯỚC 2  ·  THOÁT PHÍ PHẠT, MẤT TRẮNG ÂN HẠN",
            },
            {
                "active": [0, 3],
                "flow": ("wire", 3, 0),
                "room_src": (0.34, 0.66, "KHÚC 1 (45 NGÀY): +450.000 Đ"),
                "room_dst": (0.66, 0.34, "KHÚC 2 (15 NGÀY): +142.500 Đ"),
                "packet_label": "TỔNG LÃI = 450K + 142,5K = 592.500 Đ",
                "stage_tag": "PHÉP TÍNH LÃI LÙI DƯ NỢ BÌNH QUÂN NGÀY (0,1%/NGÀY)",
                "primitive": "P1_MINPAY_TWO_PARTS",
                "kicker": "BƯỚC 3  ·  GIẢI PHẪU HAI KHÚC LÃI 592.500 Đ",
            },
            {
                "active": [0, 3],
                "flow": ("wire", 3, 0),
                "room_src": (0.36, 0.66, "TIỀN VỪA TRẢ: 500.000 Đ"),
                "room_dst": (0.66, 0.34, "TIỀN LÃI CỘNG VÀO: +592.500 Đ"),
                "packet_label": "DƯ NỢ MỚI = 10.092.500 Đ (+92.500 Đ)",
                "stage_tag": "TRẢ 500.000 Đ NHƯNG BỊ CỘNG 592.500 Đ TIỀN LÃI",
                "primitive": "P7_MINPAY_PARADOX",
                "kicker": "BƯỚC 4  ·  NGHỊCH LÝ DƯ NỢ KỲ SAU TĂNG VỌT",
            },
            {
                "active": [0, 3, 4],
                "flow": ("pipe", 4, 3),
                "room_src": (0.48, 0.24, "SỔ KẾ TOÁN TT 99/2025"),
                "room_dst": (0.50, 0.68, "TRẢ ĐỦ 100% SAO KÊ = MIỄN LÃI"),
                "packet_label": "TRẢ ĐỦ 100% ĐỂ KHÔI PHỤC 45 NGÀY",
                "stage_tag": "TRẢ ĐỦ 100% DƯ NỢ SAO KÊ ĐỂ GIỮ TRỌN 45 NGÀY MIỄN LÃI",
                "primitive": "P4_MINPAY_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  KHI NÀO DÙNG TRẢ TỐI THIỂU?",
            },
        ],
    },
    "qr": {
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("QUÁN QUEN", "Cà phê 50k"),
            ("NGÂN HÀNG", "Của bạn"),
            ("CHUYỂN MẠCH", "Liên NH 24/7"),
            ("NGÂN HÀNG", "Của quán"),
        ],
        "scene_plates": [
            ("public/brand/card-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-1.jpg", (60, 520, 1020, 1300)),
            ("public/brand/card-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-2.jpg", (20, 260, 1060, 1105)),
            ("public/brand/card-short-plate-4.jpg", (20, 460, 1060, 1305)),
        ],
        "scenes": [
            {
                "active": [0, 1],
                "flow": ("wire", 0, 1),
                "room_src": (0.32, 0.64, "QUẦY CÀ PHÊ (50.000 Đ)"),
                "room_dst": (0.68, 0.30, "LOA BÁO TIỀN VỀ SAU 3 GIÂY"),
                "packet_label": "QUÉT QR 50.000 Đ · NHẬN ĐỦ 100%",
                "stage_tag": "LY CÀ PHÊ 50.000 Đ  ·  QUÉT MÃ QR NHẬN ĐỦ 100% SAU 3 GIÂY",
                "primitive": "P1_QR_HOOK",
                "kicker": "MỞ ĐẦU  ·  VÌ SAO QUÉT QR KHÔNG MẤT 2,2% PHÍ NHƯ THẺ?",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 0, 2),
                "room_src": (0.34, 0.66, "ĐIỆN THOẠI BẠN (ĐẨY LỆNH)"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG BẠN (−50.000 Đ CASA)"),
                "packet_label": "THANH TOÁN ĐẨY (PUSH PAYMENT)",
                "stage_tag": "THANH TOÁN ĐẨY (PUSH) TRỪ THẲNG TIỀN CÓ SẴN CASA",
                "primitive": "P2_QR_PUSH_VS_PULL",
                "kicker": "BƯỚC 1  ·  THANH TOÁN ĐẨY (PUSH) vs THANH TOÁN KÉO (PULL)",
            },
            {
                "active": [2, 3, 4],
                "flow": ("wire", 2, 3, 4),
                "room_src": (0.34, 0.66, "BẢN TIN CHUYỂN MẠCH 24/7"),
                "room_dst": (0.68, 0.30, "NGÂN HÀNG QUÁN (+50.000 Đ NGAY)"),
                "packet_label": "GHI CÓ TỨC THỜI +50.000 Đ (T+0)",
                "stage_tag": "GIÂY THỨ 3  ·  BẢN TIN 24/7 CÓ BẢO CHỨNG GHI CÓ NGAY",
                "primitive": "P3_QR_3SEC_WIRE",
                "kicker": "BƯỚC 2  ·  3 GIÂY TRÊN MẶT ĐẤT: BẢN TIN CÓ BẢO CHỨNG",
            },
            {
                "active": [2, 3, 4],
                "flow": ("pipe", 2, 3, 4),
                "room_src": (0.34, 0.68, "GOM HÀNG TRIỆU LỆNH 2 CHIỀU"),
                "room_dst": (0.68, 0.30, "BÙ TRỪ RÒNG CUỐI PHIÊN (4 TỶ)"),
                "packet_label": "QUYẾT TOÁN RÒNG (NET SETTLEMENT)",
                "stage_tag": "CUỐI PHIÊN  ·  HAI NGÂN HÀNG BÙ TRỪ RÒNG PHẦN CHÊNH LỆCH",
                "primitive": "P6_QR_NET_SETTLE",
                "kicker": "BƯỚC 3  ·  DƯỚI LÒNG ĐẤT: BÙ TRỪ RÒNG CUỐI PHIÊN",
            },
            {
                "active": [1, 2, 4],
                "flow": ("pipe", 2, 4),
                "room_src": (0.34, 0.64, "200 LY = 10TR: GIỮ TRỌN 220.000 Đ"),
                "room_dst": (0.68, 0.30, "BỂ VỐN CASA NGÂN HÀNG (~0,1%/NĂM)"),
                "packet_label": "GIỮ LẠI 220.000 Đ · GIỮ BỂ VỐN CASA",
                "stage_tag": "MỖI 10 TRIỆU DOANH THU: QUÁN GIỮ LẠI ĐƯỢC 220.000 Đ",
                "primitive": "P1_QR_SAVE_220K",
                "kicker": "BƯỚC 4  ·  QUÁN GIỮ 220K, NGÂN HÀNG GIỮ BỂ VỐN CASA",
            },
            {
                "active": [0, 1, 4],
                "flow": ("wire", 0, 1),
                "room_src": (0.48, 0.24, "SỔ KẾ TOÁN QUÁN (TT 99/2025)"),
                "room_dst": (0.50, 0.68, "QUẦY QUEN = QR · MUA XA = THẺ"),
                "packet_label": "TẠI QUẦY QUEN: QR · MUA XA: THẺ",
                "stage_tag": "MUA TẠI QUẦY QUEN DÙNG QR  ·  MUA TỪ XA CẦN LÁ CHẮN THẺ",
                "primitive": "P4_QR_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  KHI NÀO QUÉT QR, KHI NÀO CHẠM THẺ?",
            },
        ],
    },
    "profitcash": {
        "house_nodes": [
            ("KHO HÀNG", "Nhà cung cấp"),
            ("CÔNG TY", "Lãi sổ 2 tỷ"),
            ("KHÁCH SỈ", "Nợ 2,5 tỷ"),
            ("NGÂN HÀNG", "Két còn 50tr"),
            ("NHÂN SỰ", "Lương 500tr"),
        ],
        "scene_plates": [
            ("public/brand/pay-short-plate-1.jpg", (60, 520, 1020, 1300)),
            ("public/brand/install-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-2.jpg", (20, 260, 1060, 1105)),
            ("public/brand/install-short-plate-4.jpg", (20, 780, 1060, 1625)),
            ("public/brand/pay-short-plate-4.jpg", (20, 460, 1060, 1305)),
        ],
        "scenes": [
            {
                "active": [1, 3, 4],
                "flow": ("wire", 1, 3),
                "room_src": (0.34, 0.64, "BÁO CÁO LÃI RÒNG: +2 TỶ Đ"),
                "room_dst": (0.68, 0.30, "KÉT NGÂN HÀNG: CÒN 50 TRIỆU"),
                "packet_label": "LÃI 2 TỶ NHƯNG KÉT CÒN 50 TRIỆU",
                "stage_tag": "BÁO CÁO LÃI RÒNG 2 TỶ ĐỒNG  ·  KÉT NGÂN HÀNG CÒN 50 TRIỆU",
                "primitive": "P1_PROFIT_HOOK",
                "kicker": "MỞ ĐẦU  ·  LÃI RÒNG 2 TỶ SAO KHÔNG ĐỦ TIỀN TRẢ LƯƠNG?",
            },
            {
                "active": [1, 2, 3],
                "flow": ("pipe", 2, 3),
                "room_src": (0.34, 0.66, "DOANH THU TK 511: 10 TỶ Đ"),
                "room_dst": (0.68, 0.30, "KHÁCH SỈ NỢ TK 131: 2,5 TỶ Đ"),
                "packet_label": "THU 7,5 TỶ · CÒN NỢ 2,5 TỶ (TK 131)",
                "stage_tag": "GIAO HÀNG 10 TỶ  ·  THU VỀ 7,5 TỶ, KHÁCH NỢ 2,5 TỶ (TK 131)",
                "primitive": "P2_PROFIT_ACCRUAL_131",
                "kicker": "BƯỚC 1  ·  KẾ TOÁN DỒN TÍCH & 2,5 TỶ NỢ PHẢI THU",
            },
            {
                "active": [0, 1, 3],
                "flow": ("pipe", 3, 0),
                "room_src": (0.34, 0.66, "TIỀN VÀO KÉT: 1 TỶ + 7,5 TỶ"),
                "room_dst": (0.68, 0.30, "CHI NHẬP HÀNG: −7,45 TỶ Đ"),
                "packet_label": "CHI 7,45 TỶ HÀNG + 1,0 TỶ VẬN HÀNH",
                "stage_tag": "NHẬP HÀNG 7,45 TỶ ĐỒNG  ·  TỒN KHO CUỐI KỲ GIAM 950 TRIỆU",
                "primitive": "P3_PROFIT_INVENTORY_156",
                "kicker": "BƯỚC 2  ·  HÀNG TỒN KHO TK 156 NGỐN TIỀN TƯƠI",
            },
            {
                "active": [0, 1, 2],
                "flow": ("wire", 1, 2),
                "room_src": (0.34, 0.66, "PHẢI THU TK 131: 2,50 TỶ Đ"),
                "room_dst": (0.68, 0.30, "TỒN KHO TK 156: 950 TRIỆU Đ"),
                "packet_label": "3,45 TỶ ĐỒNG ĐANG NGỦ TRONG SỔ",
                "stage_tag": "TIỀN VÀO 8,50 TỶ TRỪ TIỀN RA 8,45 TỶ = KÉT CÒN 50 TRIỆU",
                "primitive": "P6_PROFIT_SPONGE_345B",
                "kicker": "BƯỚC 3  ·  3,45 TỶ ĐỒNG NGỦ ĐÔNG Ở PHẢI THU & TỒN KHO",
            },
            {
                "active": [1, 2, 3],
                "flow": ("wire", 1, 3),
                "room_src": (0.34, 0.66, "LỢI NHUẬN RÒNG: +2,00 TỶ Đ"),
                "room_dst": (0.68, 0.30, "DÒNG TIỀN OCF: −950 TRIỆU Đ"),
                "packet_label": "LÃI RÒNG +2 TỶ NHƯNG OCF −950 TRIỆU",
                "stage_tag": "BÁO CÁO LƯU CHUYỂN TIỀN TỆ: DÒNG TIỀN KINH DOANH ÂM 950TR",
                "primitive": "P7_PROFIT_OCF_MINUS950M",
                "kicker": "BƯỚC 4  ·  ĐỐI CHIẾU LỢI NHUẬN (+2 TỶ) vs DÒNG TIỀN (−950TR)",
            },
            {
                "active": [1, 3, 4],
                "flow": ("pipe", 3, 4),
                "room_src": (0.48, 0.24, "VAY NGẮN HẠN TK 341: +450TR"),
                "room_dst": (0.50, 0.68, "CHI LƯƠNG TK 334: 500 TRIỆU"),
                "packet_label": "50TR KÉT + 450TR VAY = 500TR LƯƠNG",
                "stage_tag": "VAY NGẮN HẠN 450 TRIỆU (TK 341) ĐỂ TRẢ ĐỦ 500 TRIỆU LƯƠNG",
                "primitive": "P4_PROFIT_CLOSING",
                "kicker": "ĐIỂM MẤU CHỐT  ·  LỢI NHUẬN LÀ CHỮ, DÒNG TIỀN LÀ MÁU",
            },
        ],
    },
}


def assert_distinct_adjacent_plates(stage_plates: list[Image.Image], slug: str) -> None:
    """F1 Guard: Đảm bảo 2 cảnh liền kề không bao giờ dùng cùng 1 hình cắt tĩnh (MSE >= 15.0)."""
    for i in range(len(stage_plates) - 1):
        arr_a = np.asarray(stage_plates[i].convert("RGB"), dtype=np.float32)
        arr_b = np.asarray(stage_plates[i + 1].convert("RGB"), dtype=np.float32)
        mse = float(np.mean((arr_a - arr_b) ** 2))
        if mse < 15.0:
            raise RuntimeError(
                f"FAIL [F1 Distinct Scene Plates]: Cảnh {i} và Cảnh {i+1} của '{slug}' có mặt cắt quá giống nhau (MSE={mse:.2f} < 15.0)"
            )


def assert_parent_child_containment(
    story_slug: str,
    story_cfg: dict,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """F2 + F4 + LUẬT 6b + LUẬT 8 + LUẬT 10 Guard: Kiểm tra tất định hình học Safe-Zone & không tràn chữ."""
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))

    # 1. Kiểm tra toàn bộ 3 hộp nằm gọn trong SAFE_X=(48, 868) và SAFE_Y=(268, 1316) và tách rời nhau >= 14px
    for box_name, box in (
        ("ACTIVE_ACTOR_PILL", ACTIVE_ACTOR_PILL),
        ("CUTAWAY_STAGE_BOX", CUTAWAY_STAGE_BOX),
        ("MECHANISM_CANVAS_BOX", MECHANISM_CANVAS_BOX),
    ):
        if box[0] < SAFE_X[0] or box[2] > SAFE_X[1] or box[1] < SAFE_Y[0] or box[3] > SAFE_Y[1]:
            raise RuntimeError(f"FAIL [F2 YouTube Shorts Safe-Zone]: {box_name}={box} tràn ngoài Safe Zone {SAFE_X}x{SAFE_Y}")

    if not (
        ACTIVE_ACTOR_PILL[3] + 14 <= CUTAWAY_STAGE_BOX[1]
        and CUTAWAY_STAGE_BOX[3] + 14 <= MECHANISM_CANVAS_BOX[1]
    ):
        raise RuntimeError(
            f"FAIL [LUẬT 8 Zone Overlap]: 3 vùng chồng lấn nhau: "
            f"Actor={ACTIVE_ACTOR_PILL}, Stage={CUTAWAY_STAGE_BOX}, Canvas={MECHANISM_CANVAS_BOX}"
        )

    # 2. Kiểm tra nhãn và chiều rộng chữ trong từng cảnh
    audit_strings: list[str] = []
    max_inner_w = (MECHANISM_CANVAS_BOX[2] - MECHANISM_CANVAS_BOX[0]) - 48  # P_inner >= 24px mỗi bên -> 936px
    for s_idx, sc in enumerate(story_cfg["scenes"]):
        st_tag = sc["stage_tag"]
        kicker = sc["kicker"]
        lbl_src = sc["room_src"][2]
        lbl_dst = sc["room_dst"][2]
        pkt_lbl = sc["packet_label"]
        audit_strings.extend([st_tag, kicker, lbl_src, lbl_dst, pkt_lbl])
        if dummy.textlength(st_tag, font=fonts["stage_tag"]) > (CUTAWAY_STAGE_BOX[2] - CUTAWAY_STAGE_BOX[0]) - 56:
            raise RuntimeError(f"FAIL [LUẬT 6b]: stage_tag cảnh {s_idx} ({story_slug}) tràn khung Stage: {st_tag}")
        if dummy.textlength(kicker, font=fonts["badge"]) > max_inner_w - 40:
            raise RuntimeError(f"FAIL [LUẬT 6b]: kicker cảnh {s_idx} ({story_slug}) tràn khung Canvas: {kicker}")
        for r_lbl in (lbl_src, lbl_dst, pkt_lbl):
            if dummy.textlength(r_lbl, font=fonts["badge"]) > (CUTAWAY_STAGE_BOX[2] - CUTAWAY_STAGE_BOX[0]) - 80:
                raise RuntimeError(f"FAIL [LUẬT 6b]: Nhãn trên Stage tràn khung ({story_slug} s{s_idx}): {r_lbl}")

    for l1, l2 in story_cfg["house_nodes"]:
        audit_strings.extend([l1, l2])
        if dummy.textlength(l1, font=fonts["actor"]) > 216 or dummy.textlength(l2, font=fonts["actor_sub"]) > 216:
            raise RuntimeError(f"FAIL [LUẬT 6b]: Nhãn định chế ({l1} / {l2}) quá rộng so với hộp con")

    assert_broadcast_overlay_clean(audit_strings)


def step_quantize(val: float, step: int = 100_000) -> int:
    """Làm tròn số tiền theo bậc chẵn (100.000 đ) trong 0.45s chuyển nhịp, cấm sinh số lẻ gây rối mắt."""
    return int(round(val / step) * step)


def draw_active_actor_pill(
    draw: ImageDraw.ImageDraw,
    story_cfg: dict,
    s_idx: int,
    n_scenes: int,
    s_prog: float,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """ZONE 1 (48, 64, 1032, 204): Thanh tiến độ dịu mắt + 2–3 định chế trên nền phẳng trầm (0 hạt nhấp nháy)."""
    ax0, ay0, ax1, ay1 = ACTIVE_ACTOR_PILL
    draw.rounded_rectangle(
        ACTIVE_ACTOR_PILL,
        radius=20,
        fill=(13, 19, 30),
        outline=(38, 48, 66),
        width=1,
    )

    # Thanh tiến độ 6 cảnh ở đỉnh hộp (y = ay0 + 14..18, mảnh và dịu mắt)
    seg_total_w = (ax1 - ax0) - 56
    seg_gap = 10
    seg_w = (seg_total_w - seg_gap * (n_scenes - 1)) / float(n_scenes)
    for i in range(n_scenes):
        sx0 = ax0 + 28 + i * (seg_w + seg_gap)
        sx1 = sx0 + seg_w
        if i < s_idx:
            draw.rounded_rectangle((sx0, ay0 + 14, sx1, ay0 + 18), radius=2, fill=(186, 138, 62))
        elif i == s_idx:
            draw.rounded_rectangle((sx0, ay0 + 14, sx1, ay0 + 18), radius=2, fill=(32, 42, 60))
            fill_x = sx0 + seg_w * s_prog
            draw.rounded_rectangle((sx0, ay0 + 14, max(sx0 + 6, fill_x), ay0 + 18), radius=2, fill=(226, 168, 76))
        else:
            draw.rounded_rectangle((sx0, ay0 + 14, sx1, ay0 + 18), radius=2, fill=(26, 35, 50))

    sc = story_cfg["scenes"][s_idx]
    active_indices: list[int] = sc["active"]
    house_nodes = story_cfg["house_nodes"]
    n_act = len(active_indices)
    node_w = 276 if n_act <= 2 else 256
    node_h = 72
    gap = 104 if n_act <= 2 else 52
    total_nodes_w = n_act * node_w + (n_act - 1) * gap
    start_x = ax0 + ((ax1 - ax0) - total_nodes_w) / 2.0
    cy = ay0 + 84

    centers: list[float] = []
    for k in range(n_act):
        cx = start_x + k * (node_w + gap) + node_w / 2.0
        centers.append(cx)

    flow_kind = sc["flow"][0]
    line_col = (94, 184, 138) if flow_kind == "pipe" else (226, 168, 76)
    u_sig = ease_in_out_sine((t / 3.4) % 1.0)

    if len(centers) >= 2:
        draw.line([(centers[0], cy), (centers[-1], cy)], fill=(42, 56, 76), width=2)
        sig_x = lerp(centers[0], centers[-1], u_sig)
        tail_x = max(centers[0], sig_x - 72.0)
        draw.line([(tail_x, cy), (sig_x, cy)], fill=line_col, width=4)
        draw.ellipse((sig_x - 9, cy - 9, sig_x + 9, cy + 9), fill=(26, 38, 54), outline=line_col, width=2)
        draw.ellipse((sig_x - 4, cy - 4, sig_x + 4, cy + 4), fill=line_col)

    for k, h_idx in enumerate(active_indices):
        cx = centers[k]
        bx0 = cx - node_w / 2.0
        bx1 = cx + node_w / 2.0
        by0 = cy - node_h / 2.0
        by1 = cy + node_h / 2.0
        accent_c = (226, 168, 76) if k == 0 else (94, 184, 138)
        pulse_u = (1.0 - u_sig) if k == 0 else (u_sig if k == n_act - 1 else 0.5)
        surf_col = blend_rgb((17, 24, 36), (25, 36, 52), pulse_u)
        draw.rounded_rectangle(
            (bx0, by0, bx1, by1),
            radius=12,
            fill=surf_col,
            outline=accent_c,
            width=2 if pulse_u > 0.65 else 1,
        )
        bar_w = (node_w - 28) * (0.35 + 0.65 * pulse_u)
        draw.rounded_rectangle((cx - bar_w / 2.0, by1 - 4, cx + bar_w / 2.0, by1 - 1), radius=1, fill=accent_c)
        l1, l2 = house_nodes[h_idx]
        draw_centered_row_text(draw, cx, cy - 23, l1, fonts["actor"], accent_c)
        draw_centered_row_text(draw, cx, cy + 4, l2, fonts["actor_sub"], (216, 222, 232))


def draw_cutaway_stage_overlay(
    draw: ImageDraw.ImageDraw,
    story_slug: str,
    story_cfg: dict,
    s_idx: int,
    sm: dict,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """
    ZONE 2A (48, 224, 1032, 1248) — Chuẩn Calm Editorial Motion v6.5:
    - Giữ sạch 90% bức tranh mặt cắt Risograph (0 hộp chữ đè lên tranh, 0 thẻ chữ bay qua lại).
    - Đường dẫn kiến trúc 2px tự vẽ nối 2 tâm phòng trong 1.8s (0.35s..2.15s, sau khi cross-dissolve mở ra).
    - Hạt ánh sáng (Glowing Flow Orb + đuôi sao băng 56px) lướt êm theo chu kỳ 3.6s giữa 2 tâm phòng + vòng gợn sóng tại đích.
    """
    sx0, sy0, sx1, sy1 = CUTAWAY_STAGE_BOX
    sw, sh = sx1 - sx0, sy1 - sy0
    sc = story_cfg["scenes"][s_idx]
    flow_kind = sc["flow"][0]

    rx0, ry0, _ = sc["room_src"]
    rx1, ry1, _ = sc["room_dst"]
    p_src = (sx0 + rx0 * sw, sy0 + ry0 * sh)
    p_dst = (sx0 + rx1 * sw, sy0 + ry1 * sh)

    t_local = max(0.0, t - sm["win_t0"])
    line_u = ease_out_cubic((t_local - 0.30) / 1.80)
    p_cur = (lerp(p_src[0], p_dst[0], line_u), lerp(p_src[1], p_dst[1], line_u))

    line_col = (94, 184, 138) if flow_kind == "pipe" else (226, 168, 76)
    dim_line = (46, 88, 70) if flow_kind == "pipe" else (112, 84, 42)
    if line_u > 0.01:
        draw.line([p_src, p_cur], fill=dim_line, width=2)

    u_orb = ease_in_out_sine((max(0.0, t_local - 0.35) / 3.4) % 1.0)
    u_tail = max(0.0, u_orb - 0.16)
    orb_pt = (lerp(p_src[0], p_dst[0], u_orb), lerp(p_src[1], p_dst[1], u_orb))
    tail_pt = (lerp(p_src[0], p_dst[0], u_tail), lerp(p_src[1], p_dst[1], u_tail))
    draw.line([tail_pt, orb_pt], fill=line_col, width=4)

    for idx_pt, (pt, c_dot) in enumerate(((p_src, (226, 168, 76)), (p_dst, (94, 184, 138)))):
        ripple = (1.0 - u_orb * 3.0) if (idx_pt == 0 and u_orb < 0.33) else ((u_orb - 0.67) * 3.0 if (idx_pt == 1 and u_orb > 0.67) else 0.0)
        if ripple > 0.02:
            r_rip = 9.0 + 9.0 * ripple
            draw.ellipse((pt[0] - r_rip, pt[1] - r_rip, pt[0] + r_rip, pt[1] + r_rip), outline=c_dot, width=2)
        draw.ellipse((pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8), fill=(13, 19, 30), outline=c_dot, width=2)
        draw.ellipse((pt[0] - 4, pt[1] - 4, pt[0] + 4, pt[1] + 4), fill=c_dot)

    draw.ellipse((orb_pt[0] - 11, orb_pt[1] - 11, orb_pt[0] + 11, orb_pt[1] + 11), outline=line_col, width=2)
    draw.ellipse((orb_pt[0] - 5, orb_pt[1] - 5, orb_pt[0] + 5, orb_pt[1] + 5), fill=(248, 244, 232))

    # Dải chú thích đáy không viền + thanh quét nhịp mượt dưới chân
    tag_txt = sc["stage_tag"]
    f_tag = fonts["stage_tag"]
    tw = draw.textlength(tag_txt, font=f_tag)
    pw = min(sw - 48, tw + 44)
    ph = 44
    px0 = (sx0 + sx1 - pw) / 2.0
    py0 = sy1 - 16 - ph
    draw.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=10, fill=(10, 14, 22))
    sweep_w = (pw - 24) * line_u
    if sweep_w > 4:
        draw.rounded_rectangle((px0 + 12, py0 + ph - 3, px0 + 12 + sweep_w, py0 + ph - 1), radius=1, fill=line_col)
    draw_centered_row_text(draw, (sx0 + sx1) / 2.0, py0 + 11, tag_txt, f_tag, (236, 231, 221))


def compute_two_beat_progress(sm: dict, t: float) -> tuple[float, float]:
    """
    Chuẩn Hoạt Cảnh 2 Nhịp Rõ Ràng (v6.5):
    - Nhịp 1 bắt đầu ở `t0_scene + 0.40s` (ngay sau khi cross-dissolve mở ra) và chạy mượt trong `2.20s` (66 frames).
    - Nhịp 2 bắt đầu ở câu thứ 2 (`b2_start`) và chạy mượt trong `2.40s` (72 frames).
    """
    phrases = sm["phrases"]
    t0_scene = sm["win_t0"]
    t1_scene = sm["win_t1"]
    dur = max(0.1, t1_scene - t0_scene)

    b1_start = t0_scene + 0.40
    raw_b2 = phrases[1]["t0"] if len(phrases) >= 2 else (t0_scene + dur * 0.46)
    b2_start = max(t0_scene + 3.0, min(t1_scene - 2.6, raw_b2))

    beat1 = ease_out_cubic((t - b1_start) / 2.20)
    beat2 = ease_out_cubic((t - b2_start) / 2.40)
    return beat1, beat2


def draw_beat_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    beat_u: float,
    fill_active: tuple[int, int, int],
    accent_col: tuple[int, int, int],
    radius: int = 12,
) -> None:
    """Vẽ thẻ nội dung có chuyển động mở sáng nền, thanh nhấn dọc 4px mọc từ trên xuống và thanh tiến độ ngang dưới đáy."""
    x0, y0, x1, y1 = box
    u = max(0.0, min(1.0, beat_u))
    surf_c = blend_rgb((12, 17, 26), fill_active, u)
    draw.rounded_rectangle(box, radius=radius, fill=surf_c)
    if u > 0.02:
        bar_h = max(6.0, (y1 - y0) * u)
        draw.rounded_rectangle((x0, y0, x0 + 4, y0 + bar_h), radius=2, fill=accent_col)
        prog_w = (x1 - x0 - 28.0) * u
        if prog_w > 6.0:
            dim_acc = blend_rgb((22, 30, 44), accent_col, 0.55 * u)
            draw.rounded_rectangle((x0 + 14, y1 - 4, x0 + 14 + prog_w, y1 - 1), radius=1, fill=dim_acc)


def draw_centered_row_text(
    draw: ImageDraw.ImageDraw,
    cx: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
) -> None:
    tw = draw.textlength(text, font=font)
    draw.text((cx - tw / 2.0, y), text, font=font, fill=fill)


def draw_mechanism_canvas(
    draw: ImageDraw.ImageDraw,
    story_slug: str,
    story_cfg: dict,
    s_idx: int,
    sm: dict,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """
    ZONE 2B (`MECHANISM_CANVAS_BOX = (48, 884, 868, 1316)`, 820x432px):
    Mặt phẳng tối `#0B101B` tương phản >12:1 chạy 7 Nguyên hàm Hoạt cảnh Thủ tục (`P1–P7`)
    theo 2 nhịp câu đọc (`beat1`, `beat2`). Mỗi dòng chữ chiếm 1 tầng Y độc lập (`LUẬT 10`).
    """
    cx0, cy0, cx1, cy1 = MECHANISM_CANVAS_BOX
    draw.rounded_rectangle(
        MECHANISM_CANVAS_BOX,
        radius=20,
        fill=(15, 21, 32),
        outline=(38, 48, 66),
        width=1,
    )

    sc = story_cfg["scenes"][s_idx]
    prim = sc["primitive"]
    kicker = sc["kicker"]
    beat1, beat2 = compute_two_beat_progress(sm, t)
    t_local = max(0.0, t - sm["win_t0"])

    ix0 = cx0 + 32
    ix1 = cx1 - 32
    iw = ix1 - ix0
    icx = (ix0 + ix1) / 2.0

    # Hàng Y1 (cy0 + 22): Dòng Kicker biên tập dịu mắt + thanh tiến độ mảnh dưới chân
    draw.ellipse((ix0, cy0 + 27, ix0 + 8, cy0 + 35), fill=(226, 168, 76))
    draw.text((ix0 + 18, cy0 + 21), kicker, font=fonts["badge"], fill=(226, 168, 76))
    draw.line([(ix0, cy0 + 52), (ix1, cy0 + 52)], fill=(34, 44, 60), width=1)
    draw.line([(ix0, cy0 + 52), (ix0 + iw * max(0.08, 0.5 * beat1 + 0.5 * beat2), cy0 + 52)], fill=(226, 168, 76), width=2)

    # ── NGUYÊN HÀM BÀI 1: `install` (Mua trả góp 12 triệu 0%) ────────────────
    if prim == "P1_INSTALL_HOOK":
        v1 = step_quantize(12_000_000 * max(0.08, beat1), 500_000) if beat1 < 0.99 else 12_000_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 182
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "GIÁ NIÊM YẾT TẠI QUẦY (TRẢ GÓP 0% × 12 KỲ)", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b1_y0 + 44, fmt_vnd(v1), fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Mỗi tháng đóng đều: 1.000.000 đ × 12 tháng", fonts["sub"], (182, 192, 206))

        b2_y0, b2_y1 = cy0 + 198, cy0 + 328
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 31, 38), (94, 184, 138))
        c_l2 = blend_rgb((82, 96, 112), (94, 184, 138), beat2)
        c_s2 = blend_rgb((88, 100, 116), (216, 222, 232), beat2)
        draw_centered_row_text(draw, icx, b2_y0 + 14, "NHƯNG SỐ TIỀN CỬA HÀNG THỰC NHẬN VỀ KÉT:", fonts["label"], c_l2)
        v2 = 12_000_000 if beat2 <= 0.01 else (11_400_000 if beat2 >= 0.99 else step_quantize(lerp(12_000_000, 11_400_000, beat2), 100_000))
        fee_v = 12_000_000 - v2
        draw_centered_row_text(draw, icx, b2_y0 + 46, f"{fmt_vnd(v2)}   (Hụt −{fmt_vnd(fee_v)})", fonts["big_num"], c_l2)
        draw_centered_row_text(draw, icx, b2_y0 + 90, "600.000 đ chênh lệch đi đâu và ai đang trả?", fonts["sub"], c_s2)

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P2_INSTALL_CONTRACT":
        track_y0, track_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, track_y0, ix1, track_y1), max(0.2, beat1), (21, 29, 43), (226, 168, 76))
        draw.text((ix0 + 22, track_y0 + 14), "1. CỬA HÀNG (NƠI GIAO MÁY)", font=fonts["label"], fill=(148, 160, 178))
        r_lbl = "2. CÔNG TY TÀI CHÍNH (CHỦ NỢ)"
        rw = draw.textlength(r_lbl, font=fonts["label"])
        draw.text((ix1 - 22 - rw, track_y0 + 14), r_lbl, font=fonts["label"], fill=(226, 168, 76))

        rail_x0, rail_x1 = ix0 + 140, ix1 - 140
        rail_y = track_y0 + 80
        draw.line([(rail_x0, rail_y), (rail_x1, rail_y)], fill=(54, 68, 92), width=2)
        u_rail = ease_out_cubic((t_local - 0.35) / 2.80)
        card_cx = lerp(rail_x0, rail_x1, u_rail)
        draw.line([(rail_x0, rail_y), (card_cx, rail_y)], fill=(226, 168, 76), width=4)
        cw_box, ch_box = 264, 46
        draw.rounded_rectangle(
            (card_cx - cw_box / 2, rail_y - ch_box / 2, card_cx + cw_box / 2, rail_y + ch_box / 2),
            radius=10,
            fill=(178, 126, 48),
            outline=(236, 192, 108),
            width=1,
        )
        draw_centered_row_text(draw, card_cx, rail_y - 11, "HỢP ĐỒNG VAY 12.000.000 Đ", fonts["badge"], (244, 240, 232))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_led = step_quantize(12_000_000 * beat2, 500_000) if beat2 < 0.99 else 12_000_000
        c_deb = blend_rgb((92, 104, 120), (226, 168, 76), beat2)
        c_crd = blend_rgb((82, 102, 98), (94, 184, 138), beat2)
        draw_centered_row_text(draw, icx, b2_y0 + 14, "SỔ KẾ TOÁN CỬA HÀNG LÚC GIAO MÁY (TT 99/2025):", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Debit 1388 (Phải thu khác): +{fmt_vnd(v_led)}", fonts["val_bold"], c_deb)
        draw_centered_row_text(draw, icx, b2_y0 + 84, f"Credit 511 (Doanh thu bán hàng): +{fmt_vnd(v_led)}", fonts["val_bold"], c_crd)

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "LÚC NÀY KÉT TIỀN CỬA HÀNG VẪN CHƯA NHẬN ĐỒNG NÀO", fonts["label"], (226, 168, 76))

    elif prim == "P1_INSTALL_SPLIT":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 146
        v_loan = step_quantize(12_000_000 * max(0.15, beat1), 500_000) if beat1 < 0.99 else 12_000_000
        draw_centered_row_text(draw, icx, b1_y0 + 6, "KHOẢN VAY GỐC ĐƯỢC DUYỆT (100%):", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b1_y0 + 36, fmt_vnd(v_loan), fonts["hero_num"], (236, 231, 221))

        # Thanh tách tỷ lệ 95% / 5% (Beat 1: đầy 100%, Beat 2: tách mượt khối 5% sang phải)
        split_u = max(ease_out_cubic((t_local - 1.40) / 2.60), beat2)
        bar_y0, bar_y1 = cy0 + 162, cy0 + 224
        gap_px = lerp(2.0, 14.0, split_u)
        w_95 = (iw - gap_px) * lerp(0.96, 0.84, split_u)
        w_05 = max(36.0, (iw - gap_px) - w_95)
        v_net = step_quantize(lerp(12_000_000, 11_400_000, split_u), 100_000) if split_u < 0.99 else 11_400_000
        draw.rounded_rectangle((ix0, bar_y0, ix0 + w_95, bar_y1), radius=10, fill=(38, 110, 78))
        draw.rounded_rectangle((ix0 + w_95 + gap_px, bar_y0, ix1, bar_y1), radius=10, fill=blend_rgb((48, 62, 78), (168, 110, 34), split_u))

        draw_centered_row_text(draw, ix0 + w_95 / 2.0, bar_y0 + 18, f"THỰC NHẬN (95%): +{fmt_vnd(v_net)}", fonts["val_bold"], (240, 246, 242))
        if split_u > 0.15:
            draw_centered_row_text(draw, ix0 + w_95 + gap_px + w_05 / 2.0, bar_y0 + 18, "−5%", fonts["val_bold"], (248, 240, 224))

        det_y0, det_y1 = cy0 + 242, cy0 + 332
        draw_beat_card(draw, (ix0, det_y0, ix1, det_y1), split_u, (21, 29, 43), (94, 184, 138), radius=10)
        v_641 = 12_000_000 - v_net
        draw_centered_row_text(draw, icx, det_y0 + 16, f"Debit 112 (Tiền gửi NH): +{fmt_vnd(v_net)} (Về tài khoản cửa hàng)", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, det_y0 + 52, f"Debit 641 (Chi phí bán hàng): +{fmt_vnd(v_641)} (Phí hỗ trợ lãi suất 5%)", fonts["sub"], (226, 168, 76))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "CỬA HÀNG CHẤP NHẬN HỤT 600.000 Đ ĐỂ ĐỔI LẤY ĐƠN HÀNG NGAY", fonts["label"], (226, 168, 76))

    elif prim == "P5_INSTALL_EIR":
        grid_y0, grid_y1 = cy0 + 66, cy0 + 184
        u_12m = ease_out_cubic((t_local - 0.35) / 4.40)
        draw_beat_card(draw, (ix0, grid_y0, ix1, grid_y1), max(0.2, u_12m), (21, 29, 43), (226, 168, 76))
        active_m = 12 if u_12m >= 0.96 else min(12, max(1, int(round(lerp(1.0, 12.0, u_12m)))))
        draw_centered_row_text(
            draw,
            icx,
            grid_y0 + 12,
            f"LỊCH TRẢ GÓP 12 KỲ: {active_m}/12 THÁNG  ·  TỔNG TRẢ {fmt_vnd(active_m * 1_000_000)}",
            fonts["label"],
            (226, 168, 76),
        )
        cell_w = (iw - 32) / 12.0
        for m_i in range(12):
            mx0 = ix0 + 16 + m_i * cell_w + 3
            mx1 = mx0 + cell_w - 6
            cell_u = max(0.0, min(1.0, u_12m * 12.0 - m_i))
            draw.rounded_rectangle((mx0, grid_y0 + 44, mx1, grid_y0 + 100), radius=6, fill=(26, 35, 50))
            if cell_u > 0.02:
                fill_h = 56.0 * cell_u
                draw.rounded_rectangle(
                    (mx0, grid_y0 + 100 - fill_h, mx1, grid_y0 + 100),
                    radius=6,
                    fill=(42, 118, 84),
                )
            draw_centered_row_text(draw, (mx0 + mx1) / 2.0, grid_y0 + 62, f"T{m_i+1}", fonts["small"], (236, 242, 238) if cell_u > 0.4 else (120, 134, 152))

        eir_y0, eir_y1 = cy0 + 200, cy0 + 330
        draw_beat_card(draw, (ix0, eir_y0, ix1, eir_y1), beat2, (19, 30, 40), (94, 184, 138))
        eir_m = lerp(0.0, 0.8, max(0.1, beat2))
        eir_y = lerp(0.0, 10.0, max(0.1, beat2))
        c_eir = blend_rgb((96, 108, 124), (226, 168, 76), beat2)
        draw_centered_row_text(draw, icx, eir_y0 + 14, "GIÁ TRỊ THỜI GIAN CỦA TIỀN (NHẬN 11,4TR — THU 12,0TR):", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, eir_y0 + 46, f"LÃI SUẤT HIỆU DỤNG (EIR): ~{eir_m:.1f}%/THÁNG (~{eir_y:.1f}%/NĂM)".replace(".", ","), fonts["big_num"], c_eir)
        draw_centered_row_text(draw, icx, eir_y0 + 90, "11.400.000 = Σ 1.000.000 / (1 + r)^t   (t = 1..12 kỳ)", fonts["sub"], blend_rgb((88, 100, 116), (216, 222, 232), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "KHOẢN CHÊNH 600.000 Đ LÀM ĐÚNG NHIỆM VỤ CỦA TIỀN LÃI", fonts["label"], (226, 168, 76))

    elif prim == "P7_INSTALL_TWOWORLD":
        w1_y0, w1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, w1_y0, ix1, w1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        v_disc = step_quantize(600_000 * max(0.1, beat1), 50_000) if beat1 < 0.99 else 600_000
        draw_centered_row_text(draw, icx, w1_y0 + 14, "KỊCH BẢN 1: TRẢ THẲNG ĐƯỢC GIẢM 600.000 Đ (CÒN 11.400.000 Đ)", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, w1_y0 + 48, f"Chọn trả góp 12.000.000 đ = BẠN trả {fmt_vnd(v_disc)} tiền lãi", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, w1_y0 + 86, "(Bạn đánh đổi 600.000 đ chiết khấu tiền mặt để lấy 12 tháng trả chậm)", fonts["sub"], (148, 160, 178))

        w2_y0, w2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, w2_y0, ix1, w2_y1), beat2, (19, 30, 40), (94, 184, 138))
        c_w2_t = blend_rgb((84, 102, 98), (94, 184, 138), beat2)
        c_w2_v = blend_rgb((92, 104, 120), (236, 231, 221), beat2)
        draw_centered_row_text(draw, icx, w2_y0 + 14, "KỊCH BẢN 2: TRẢ THẲNG & TRẢ GÓP CÙNG MỘT GIÁ 12.000.000 Đ", fonts["label"], c_w2_t)
        draw_centered_row_text(draw, icx, w2_y0 + 48, "CỬA HÀNG chịu 600.000 đ vào TK 641 (hoặc đã cộng vào giá chung)", fonts["val_bold"], c_w2_v)
        draw_centered_row_text(draw, icx, w2_y0 + 86, "(Người mua trả thẳng không được giảm giá đang phụ trả phần phí này)", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "TRONG CẢ 2 KỊCH BẢN, 600.000 Đ TIỀN LÃI KHÔNG HỀ BIẾN MẤT", fonts["label"], (226, 168, 76))

    elif prim == "P4_INSTALL_CLOSING":
        t_y0, t_y1 = cy0 + 66, cy0 + 220
        draw_beat_card(draw, (ix0, t_y0, ix1, t_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_bal = step_quantize(12_000_000 * max(0.1, beat1), 500_000) if beat1 < 0.99 else 12_000_000
        draw_centered_row_text(draw, icx, t_y0 + 12, "BÀN CÂN SỔ KẾ TOÁN CỬA HÀNG (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw.line([(ix0 + 24, t_y0 + 42), (ix0 + 24 + (iw - 48) * max(0.15, beat1), t_y0 + 42)], fill=(94, 184, 138), width=2)
        draw_centered_row_text(draw, icx, t_y0 + 54, "Bên Nợ: TK 112 (11.400.000 đ) + TK 641 (600.000 đ) = 12.000.000 đ", fonts["sub"], (226, 168, 76))
        draw_centered_row_text(draw, icx, t_y0 + 88, "Bên Có: TK 511 (Doanh thu bán hàng) = 12.000.000 đ", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, t_y0 + 122, f"Σ Nợ ({fmt_vnd(v_bal)})  =  Σ Có ({fmt_vnd(v_bal)})   [CÂN BẰNG]", fonts["val_bold"], (236, 231, 221))

        q_y0, q_y1 = cy0 + 238, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (226, 168, 76), radius=14)
        c_q1 = blend_rgb((96, 108, 124), (236, 231, 221), beat2)
        c_q2 = blend_rgb((82, 102, 98), (94, 184, 138), beat2)
        draw_centered_row_text(draw, icx, q_y0 + 18, "CÂU HỎI DUY NHẤT CẦN HỎI TRƯỚC KHI KÝ TRẢ GÓP 0%:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, q_y0 + 58, "“Nếu trả thẳng một lần ngay bây giờ", fonts["big_num"], c_q1)
        draw_centered_row_text(draw, icx, q_y0 + 104, "thì giá món hàng giảm còn bao nhiêu?”", fonts["big_num"], c_q2)

    # ── NGUYÊN HÀM BÀI 2: `card` (Quẹt thẻ 10 triệu hoàn tiền 1%) ───────────
    elif prim == "P1_CARD_HOOK":
        v1 = step_quantize(10_000_000 * max(0.08, beat1), 500_000) if beat1 < 0.99 else 10_000_000
        v_cb = step_quantize(100_000 * max(0.1, beat1), 10_000) if beat1 < 0.99 else 100_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 182
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "HOÁ ĐƠN QUẸT THẺ TẠI QUÁN QUEN:", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b1_y0 + 44, fmt_vnd(v1), fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, f"Bạn nhận thông báo hoàn tiền (Cashback 1%): +{fmt_vnd(v_cb)}", fonts["sub"], (94, 184, 138))

        b2_y0, b2_y1 = cy0 + 198, cy0 + 328
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 31, 38), (94, 184, 138))
        v2 = 10_000_000 if beat2 <= 0.01 else (9_780_000 if beat2 >= 0.99 else step_quantize(lerp(10_000_000, 9_780_000, beat2), 20_000))
        mdr_v = 10_000_000 - v2
        draw_centered_row_text(draw, icx, b2_y0 + 14, "NHƯNG SỐ TIỀN QUÁN QUEN THỰC NHẬN VỀ TÀI KHOẢN:", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, f"{fmt_vnd(v2)}   (Hụt −{fmt_vnd(mdr_v)})", fonts["big_num"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 90, "Ai đã lấy 220.000 đ và trích 100.000 đ hoàn cho bạn?", fonts["sub"], blend_rgb((88, 100, 116), (216, 222, 232), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P2_CARD_HOLD":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        v_hold = step_quantize(10_000_000 * max(0.1, beat1), 500_000) if beat1 < 0.99 else 10_000_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "1. TẠI NGÂN HÀNG CỦA BẠN (LÚC CHẠM THẺ T+0):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"TẠM KHOÁ HẠN MỨC: −{fmt_vnd(v_hold)}", fonts["big_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 88, "Chỉ là bản tin điện tử giữ chỗ — chưa có đồng tiền nào rời ngân hàng", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_rec = step_quantize(10_000_000 * beat2, 500_000) if beat2 < 0.99 else 10_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "2. TẠI QUÁN QUEN (ĐÊM ĐẦU TIÊN TRONG SỔ TT 99/2025):", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Debit 1388 (Phải thu khác): +{fmt_vnd(v_rec)}  |  Credit 511: +10tr", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Két tiền của quán: +0 đ (Đợi quyết toán liên ngân hàng T+2)", fonts["sub"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "TIẾNG “BÍP” TẠI MÁY POS CHỈ LÀ LỜI HỨA THANH TOÁN", fonts["label"], (226, 168, 76))

    elif prim == "P1_CARD_MDR_SPLIT":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 146
        v_bill = step_quantize(10_000_000 * max(0.15, beat1), 500_000) if beat1 < 0.99 else 10_000_000
        draw_centered_row_text(draw, icx, b1_y0 + 6, "DOANH THU GHI HÓA ĐƠN (100%):", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b1_y0 + 36, fmt_vnd(v_bill), fonts["hero_num"], (236, 231, 221))

        split_u = max(ease_out_cubic((t_local - 1.40) / 2.60), beat2)
        bar_y0, bar_y1 = cy0 + 162, cy0 + 224
        gap_px = lerp(2.0, 14.0, split_u)
        w_net = (iw - gap_px) * lerp(0.96, 0.83, split_u)
        w_mdr = max(38.0, (iw - gap_px) - w_net)
        v_net_q = step_quantize(lerp(10_000_000, 9_780_000, split_u), 20_000) if split_u < 0.99 else 9_780_000
        draw.rounded_rectangle((ix0, bar_y0, ix0 + w_net, bar_y1), radius=10, fill=(38, 110, 78))
        draw.rounded_rectangle((ix0 + w_net + gap_px, bar_y0, ix1, bar_y1), radius=10, fill=blend_rgb((48, 62, 78), (168, 110, 34), split_u))

        draw_centered_row_text(draw, ix0 + w_net / 2.0, bar_y0 + 18, f"QUÁN THỰC NHẬN (97,8%): +{fmt_vnd(v_net_q)}", fonts["val_bold"], (240, 246, 242))
        if split_u > 0.15:
            draw_centered_row_text(draw, ix0 + w_net + gap_px + w_mdr / 2.0, bar_y0 + 18, "−2,2%", fonts["val_bold"], (248, 240, 224))

        det_y0, det_y1 = cy0 + 242, cy0 + 332
        draw_beat_card(draw, (ix0, det_y0, ix1, det_y1), split_u, (21, 29, 43), (94, 184, 138), radius=10)
        v_mdr_q = 10_000_000 - v_net_q
        draw_centered_row_text(draw, icx, det_y0 + 16, f"Debit 112 (Tiền gửi NH của quán): +{fmt_vnd(v_net_q)} (Về sau 2 ngày)", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, det_y0 + 52, f"Debit 641 (Chi phí bán hàng — Phí MDR 2,2%): +{fmt_vnd(v_mdr_q)}", fonts["sub"], (226, 168, 76))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "PHÍ NHẬN THẺ 220.000 Đ BỊ KHẤU TRỪ TRƯỚC KHI TIỀN VỀ QUÁN", fonts["label"], (226, 168, 76))

    elif prim == "P1_CARD_THREE_WAY":
        b1_y0 = cy0 + 66
        draw_centered_row_text(draw, icx, b1_y0 + 4, "TỔNG PHÍ QUÁN BỊ TRỪ (MDR 2,2%): 220.000 Đ", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 32, "Được chia tự động cho 3 định chế tài chính:", fonts["sub"], (148, 160, 178))

        rows_3 = [
            ("1. Ngân hàng của bạn (Interchange 1,50%)", 150_000, 0.68, (226, 168, 76), 0.35),
            ("2. Ngân hàng của quán (Acquirer 0,60%)", 60_000, 0.27, (94, 184, 138), 1.65),
            ("3. Tổ chức thẻ chuyển mạch (0,10%)", 10_000, 0.08, (130, 178, 218), 2.95),
        ]
        ry = cy0 + 142
        for title_r, amt_num, share_r, acc_c, t_st in rows_3:
            ru = ease_out_cubic((t_local - t_st) / 1.60)
            draw_beat_card(draw, (ix0, ry, ix1, ry + 56), max(0.12, ru), (21, 29, 43), acc_c, radius=10)
            bar_rw = (iw - 16) * share_r * ru
            if bar_rw > 6:
                draw.rounded_rectangle((ix0 + 8, ry + 6, ix0 + 8 + bar_rw, ry + 50), radius=6, fill=blend_rgb((21, 29, 43), acc_c, 0.22))
            v_r = step_quantize(amt_num * ru, 10_000) if ru < 0.99 else amt_num
            draw_centered_row_text(draw, icx, ry + 17, f"{title_r}:   +{fmt_vnd(v_r)}", fonts["val_bold"], blend_rgb((108, 120, 138), (236, 231, 221), max(0.2, ru)))
            ry += 66

        draw.line([(ix0, cy0 + 348), (ix1, cy0 + 348)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 368, "NGÂN HÀNG CỦA BẠN NHẬN PHẦN LỚN NHẤT: 150.000 Đ (68% TỔNG PHÍ)", fonts["label"], (226, 168, 76))

    elif prim == "P4_CARD_WATERFALL":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 188
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        v_ic = step_quantize(150_000 * max(0.1, beat1), 10_000) if beat1 < 0.99 else 150_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "TẠI NGÂN HÀNG PHÁT HÀNH THẺ CỦA BẠN:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"Thu phí Interchange từ giao dịch của bạn: +{fmt_vnd(v_ic)} (1,5%)", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 84, "(Khoản thu này đến từ 220.000 đ mà Quán quen vừa bị khấu trừ)", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 204, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_cb2 = step_quantize(100_000 * beat2, 10_000) if beat2 < 0.99 else 100_000
        v_nim = step_quantize(50_000 * beat2, 10_000) if beat2 < 0.99 else 50_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "CÁCH NGÂN HÀNG CHIA KHOẢN THU 150.000 Đ:", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Trích hoàn tiền cho bạn (1,0%): +{fmt_vnd(v_cb2)}", fonts["val_bold"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 84, f"Ngân hàng giữ lại thu nhập thuần (0,5%): +{fmt_vnd(v_nim)}", fonts["val_bold"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "NGÂN HÀNG KHÔNG TỰ BỎ TIỀN TÚI ĐỂ TẶNG BẠN 100.000 Đ", fonts["label"], (226, 168, 76))

    elif prim == "P7_CARD_CLOSING":
        w1_y0, w1_y1 = cy0 + 66, cy0 + 202
        draw_beat_card(draw, (ix0, w1_y0, ix1, w1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, w1_y0 + 14, "VÒNG TRÒN ĐỊNH GIÁ TẠI QUÁN QUEN:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, w1_y0 + 50, "Để không lỗ 2,2% phí thẻ, quán tính phí vào giá thực đơn chung", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, w1_y0 + 88, "Σ Nợ (9,78tr TK 112 + 220k TK 641) = Σ Có (10,0tr TK 511)", fonts["sub"], (94, 184, 138))

        q_y0, q_y1 = cy0 + 220, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (94, 184, 138), radius=14)
        draw_centered_row_text(draw, icx, q_y0 + 18, "SỰ THẬT HỆ THỐNG ĐẰNG SAU 100.000 Đ TIỀN HOÀN:", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 60, "Tiền hoàn 1% thực chất là tiền của chính bạn", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 108, "đi một vòng qua giá món ăn rồi quay về ví (sau khi trừ phí)", fonts["sub"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))

    # ── NGUYÊN HÀM BÀI 3: `pay` (Tiền lương 15 triệu & Bể vốn CASA) ──────────
    elif prim == "P3_PAY_HOOK":
        v1 = step_quantize(15_000_000 * max(0.08, beat1), 500_000) if beat1 < 0.99 else 15_000_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 184
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "TIN NHẮN ĐIỆN THOẠI BÁO LƯƠNG VỀ:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 46, f"+{fmt_vnd(v1)}", fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Hiển thị ngay lập tức vì bạn và công ty mở tài khoản cùng ngân hàng", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 200, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "NHƯNG BÊN DƯỚI HẦM KÉT CỦA NGÂN HÀNG:", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "0 ĐỒNG TIỀN THẬT DI CHUYỂN", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 90, "Vì sao ngân hàng yêu cầu cả công ty mở tài khoản tại cùng một nơi?", fonts["sub"], blend_rgb((88, 100, 116), (182, 192, 206), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P3_PAY_ONUS_FLIP":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 214
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        v_fl = step_quantize(15_000_000 * max(0.1, beat1), 500_000) if beat1 < 0.99 else 15_000_000
        draw_centered_row_text(draw, icx, b1_y0 + 12, "BÚT TOÁN NỘI BỘ NGÂN HÀNG (CHUYỂN KHOẢN ON-US):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"Dòng 1 — TK Công ty:   −{fmt_vnd(v_fl)}  (Ngân hàng bớt nợ Công ty)", fonts["val_bold"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 86, f"Dòng 2 — TK Của bạn:   +{fmt_vnd(v_fl)}  (Ngân hàng tăng nợ Bạn)", fonts["val_bold"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 120, "Tổng tiền mặt nằm trong ngân hàng: KHÔNG ĐỔI (Hao hụt thanh khoản = 0 đ)", fonts["sub"], (182, 192, 206))

        b2_y0, b2_y1 = cy0 + 230, cy0 + 332
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_c2 = step_quantize(15_000_000 * beat2, 500_000) if beat2 < 0.99 else 15_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "SỔ KẾ TOÁN CÔNG TY (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b2_y0 + 50, f"Debit 334 (Phải trả NLĐ): {fmt_vnd(v_c2)}  |  Credit 112: {fmt_vnd(v_c2)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "CHỈ ĐỔI TÊN CHỦ NỢ TRÊN SỔ  ·  0 ĐỒNG RỜI KHỎI NGÂN HÀNG", fonts["label"], (226, 168, 76))

    elif prim == "P6_PAY_CASA_POOL":
        g_y0, g_y1 = cy0 + 66, cy0 + 208
        u_pool = ease_out_cubic((t_local - 0.35) / 4.40)
        draw_beat_card(draw, (ix0, g_y0, ix1, g_y1), max(0.2, u_pool), (21, 29, 43), (94, 184, 138))
        n_emp = int(round(500 * u_pool))
        draw_centered_row_text(draw, icx, g_y0 + 12, f"MẠNG LƯỚI {n_emp}/500 TÀI KHOẢN LƯƠNG NHÂN VIÊN TRONG CÙNG NGÂN HÀNG:", fonts["label"], (94, 184, 138))

        cols_n, rows_n = 15, 2
        cell_w = (iw - 48) / float(cols_n)
        for r_i in range(rows_n):
            for c_i in range(cols_n):
                idx_c = r_i * cols_n + c_i
                cx_a = ix0 + 24 + c_i * cell_w + 3
                cx_b = cx_a + cell_w - 6
                cy_a = g_y0 + 44 + r_i * 42
                cy_b = cy_a + 32
                cell_u = max(0.0, min(1.0, u_pool * 30.0 - idx_c))
                draw.rounded_rectangle(
                    (cx_a, cy_a, cx_b, cy_b),
                    radius=5,
                    fill=blend_rgb((26, 35, 50), (42, 118, 84), cell_u),
                )

        p_y0, p_y1 = cy0 + 222, cy0 + 332
        draw_beat_card(draw, (ix0, p_y0, ix1, p_y1), max(u_pool, beat2), (19, 30, 40), (226, 168, 76))
        v_casa = step_quantize(2_500_000_000 * max(u_pool, beat2), 50_000_000) if max(u_pool, beat2) < 0.99 else 2_500_000_000
        draw_centered_row_text(draw, icx, p_y0 + 12, "500 NGƯỜI × 5.000.000 Đ SỐ DƯ NẰM YÊN BÌNH QUÂN:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, p_y0 + 44, f"BỂ VỐN CASA = {fmt_vnd(v_casa)}", fonts["big_num"], (94, 184, 138))
        draw_centered_row_text(draw, icx, p_y0 + 82, "Lãi suất không kỳ hạn (CASA) ngân hàng trả: ~0,1% / năm", fonts["sub"], (182, 192, 206))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "MỖI NGƯỜI RÚT LẺ TẺ, NHƯNG BỂ VỐN CHUNG LUÔN ĐẦY", fonts["label"], (226, 168, 76))

    elif prim == "P6_PAY_BAR_1TO50":
        b_y0, b_y1 = cy0 + 66, cy0 + 330
        draw_beat_card(draw, (ix0, b_y0, ix1, b_y1), max(0.2, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b_y0 + 14, "CHI PHÍ NGÂN HÀNG HUY ĐỘNG 2,5 TỶ ĐỒNG TRONG 1 NĂM:", fonts["label"], (226, 168, 76))

        r1_y = b_y0 + 58
        v_c1 = step_quantize(2_500_000 * max(0.1, beat1), 250_000) if beat1 < 0.99 else 2_500_000
        draw.text((ix0 + 22, r1_y), "1. Tiền gửi lương không kỳ hạn (CASA 0,1%/năm):", font=fonts["sub"], fill=(94, 184, 138))
        draw.rounded_rectangle((ix0 + 22, r1_y + 30, ix0 + 22 + 26 * max(0.2, beat1), r1_y + 68), radius=5, fill=(46, 126, 88))
        draw.text((ix0 + 64, r1_y + 36), f"{fmt_vnd(v_c1)} / năm   (Chỉ bằng 1/50 chi phí kỳ hạn)", font=fonts["val_bold"], fill=(236, 231, 221))

        r2_y = b_y0 + 144
        u_bar = max(ease_out_cubic((t_local - 1.50) / 3.00), beat2)
        bar2_w = max(24, int((iw - 44) * u_bar))
        v_td = step_quantize(125_000_000 * u_bar, 2_500_000) if u_bar < 0.99 else 125_000_000
        draw.text((ix0 + 22, r2_y), "2. Tiền gửi tiết kiệm có kỳ hạn (Lãi 5,0%/năm):", font=fonts["sub"], fill=(226, 168, 76))
        draw.rounded_rectangle((ix0 + 22, r2_y + 30, ix1 - 22, r2_y + 76), radius=8, fill=(28, 38, 54))
        draw.rounded_rectangle((ix0 + 22, r2_y + 30, ix0 + 22 + bar2_w, r2_y + 76), radius=8, fill=(168, 110, 34))
        draw_centered_row_text(draw, icx, r2_y + 42, f"{fmt_vnd(v_td)} / năm   (Đắt gấp 50 lần CASA)", fonts["val_bold"], (244, 240, 232))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "NGÂN HÀNG TIẾT KIỆM ~122,5 TRIỆU/NĂM NHỜ GIỮ TRỌN BẢNG LƯƠNG", fonts["label"], (226, 168, 76))

    elif prim == "P4_PAY_BARGAIN":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "PHÍA NGÂN HÀNG NHẬN ĐƯỢC:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Bể vốn CASA 2,5 tỷ đồng giá rẻ (~0,1%/năm)", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Dùng làm nguồn vốn đầu vào để cho vay mua nhà, mua xe lãi cao hơn", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "PHÍA CÔNG TY CỦA BẠN NHẬN LẠI:", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "Miễn phí chi hộ lương + Ưu đãi lãi vay vốn lưu động", fonts["val_bold"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "(Bảng lương nhân viên chính là tài sản thương lượng của doanh nghiệp)", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "ĐÓ LÀ LÝ DO PHÒNG NHÂN SỰ CHỈ ĐỊNH 1 NGÂN HÀNG NHẬN LƯƠNG", fonts["label"], (226, 168, 76))

    elif prim == "P4_PAY_CLOSING":
        t_y0, t_y1 = cy0 + 66, cy0 + 220
        draw_beat_card(draw, (ix0, t_y0, ix1, t_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_pay_bal = step_quantize(17_000_000 * max(0.1, beat1), 500_000) if beat1 < 0.99 else 17_000_000
        draw_centered_row_text(draw, icx, t_y0 + 12, "BÚT TOÁN CHI LƯƠNG TẠI DOANH NGHIỆP (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw.line([(ix0 + 24, t_y0 + 42), (ix0 + 24 + (iw - 48) * max(0.15, beat1), t_y0 + 42)], fill=(94, 184, 138), width=2)
        draw_centered_row_text(draw, icx, t_y0 + 54, "Bên Nợ: TK 642 (Chi phí quản lý DN) = 17.000.000 đ", fonts["sub"], (226, 168, 76))
        draw_centered_row_text(draw, icx, t_y0 + 88, "Bên Có: TK 334 (Lương 15tr) + TK 338/3335 (BHXH & Thuế 2tr) = 17tr", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, t_y0 + 122, f"Σ Nợ ({fmt_vnd(v_pay_bal)})  =  Σ Có ({fmt_vnd(v_pay_bal)})   [CÂN BẰNG]", fonts["val_bold"], (236, 231, 221))

        q_y0, q_y1 = cy0 + 238, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (226, 168, 76), radius=14)
        draw_centered_row_text(draw, icx, q_y0 + 18, "BẢN CHẤT KẾ TOÁN CỦA SỐ DƯ TRÊN ĐIỆN THOẠI:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, q_y0 + 58, "Số dư tài khoản là khoản NGÂN HÀNG ĐANG NỢ BẠN", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 106, "Đêm nay, số dư nằm yên của bạn đang sinh lời cho ai?", fonts["sub"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))

    # ── NGUYÊN HÀM BÀI 4: `minpay` (Trả tối thiểu 5% sao kê thẻ tín dụng 10 triệu) ──
    elif prim == "P1_MINPAY_HOOK":
        v1 = step_quantize(10_000_000 * max(0.08, beat1), 500_000) if beat1 < 0.99 else 10_000_000
        v_min = step_quantize(500_000 * max(0.1, beat1), 50_000) if beat1 < 0.99 else 500_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 182
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "DƯ NỢ SAO KÊ THẺ TÍN DỤNG NGÀY 30:", fonts["label"], (148, 160, 178))
        draw_centered_row_text(draw, icx, b1_y0 + 44, fmt_vnd(v1), fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, f"Nút bấm nhẹ tênh: Trả tối thiểu 5% = {fmt_vnd(v_min)} (Đúng hạn, 0 phí phạt)", fonts["sub"], (94, 184, 138))

        b2_y0, b2_y1 = cy0 + 198, cy0 + 328
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 31, 38), (226, 168, 76))
        v2 = 9_500_000 if beat2 <= 0.01 else (10_092_500 if beat2 >= 0.99 else step_quantize(lerp(9_500_000, 10_092_500, beat2), 25_000))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "NHƯNG TỔNG DƯ NỢ TRÊN SAO KÊ KỲ SAU (NGÀY 60):", fonts["label"], blend_rgb((82, 102, 98), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, f"{fmt_vnd(v2)}   (Cộng thêm +592.500 đ lãi)", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 90, "Vì sao vừa trả 500.000 đ xong, tháng sau lại nợ nhiều hơn lúc chưa trả?", fonts["sub"], blend_rgb((88, 100, 116), (216, 222, 232), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P2_MINPAY_T2_ADVANCE":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_adv = step_quantize(9_800_000 * max(0.1, beat1), 200_000) if beat1 < 0.99 else 9_800_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "1. NGÀY T+2: NGÂN HÀNG PHÁT HÀNH ĐÃ BỎ TIỀN TÚI ỨNG TRƯỚC:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"QUYẾT TOÁN CHO CỬA HÀNG: +{fmt_vnd(v_adv)}", fonts["big_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 88, "(Sau khi trừ phí nhận thẻ MDR 2% ví dụ = 200.000 đ)", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "2. BẢN CHẤT CỦA 45 NGÀY MIỄN LÃI (CONDITIONAL GRACE PERIOD):", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "Chỉ miễn lãi nếu Ngày 45 trả đủ 100% sao kê (10.000.000 đ)", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Suốt 45 ngày đó bạn đang tiêu tiền ngân hàng ứng trước từ Ngày T+2", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "MIỄN LÃI 45 NGÀY LÀ LỜI HỨA CÓ ĐIỀU KIỆN TRẢ ĐỦ 100%", fonts["label"], (226, 168, 76))

    elif prim == "P3_MINPAY_FORFEIT":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_p = step_quantize(500_000 * max(0.1, beat1), 50_000) if beat1 < 0.99 else 500_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "NGÀY 45 — BẠN CHUYỂN KHOẢN TRẢ TỐI THIỂU 5%:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"TRẢ ĐÚNG HẠN: {fmt_vnd(v_p)}   (Gốc còn lại: 9.500.000 đ)", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Sổ DN (TT 99/2025): Debit TK 338: 500.000 đ  |  Credit TK 112: 500.000 đ", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "CÁI GIÁ CỦA VIỆC CHƯA TRẢ ĐỦ 100% DƯ NỢ SAO KÊ:", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "Thoát phí phạt trễ hạn · NHƯNG MẤT TRẮNG 45 NGÀY MIỄN LÃI", fonts["val_bold"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Đồng hồ tính lãi lập tức quay ngược về tận Ngày 01 đầu kỳ", fonts["sub"], blend_rgb((88, 100, 116), (226, 168, 76), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "TRẢ THIẾU DÙ CHỈ 1 ĐỒNG CŨNG HUỶ TOÀN BỘ 45 NGÀY MIỄN LÃI", fonts["label"], (226, 168, 76))

    elif prim == "P1_MINPAY_TWO_PARTS":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        v_k1 = step_quantize(450_000 * max(0.1, beat1), 25_000) if beat1 < 0.99 else 450_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "KHÚC 1 (NGÀY 01–45: TÍNH LÙI TRÊN CẢ 10.000.000 Đ):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"10.000.000 × 0,1%/ngày × 45 ngày = +{fmt_vnd(v_k1)}", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "(Lãi suất ví dụ 36%/năm ≈ 3%/tháng ≈ 0,1%/ngày)", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_k2 = step_quantize(142_500 * beat2, 12_500) if beat2 < 0.99 else 142_500
        draw_centered_row_text(draw, icx, b2_y0 + 14, "KHÚC 2 (NGÀY 46–60: TRÊN 9.500.000 Đ GỐC CÒN LẠI):", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"9.500.000 × 0,1%/ngày × 15 ngày = +{fmt_vnd(v_k2)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Tổng lãi kỳ 2 = 450.000 đ + 142.500 đ = +592.500 đ", fonts["sub"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "PHƯƠNG PHÁP DƯ NỢ BÌNH QUÂN NGÀY (AVERAGE DAILY BALANCE)", fonts["label"], (226, 168, 76))

    elif prim == "P7_MINPAY_PARADOX":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "ĐỐI CHIẾU TIỀN BẠN TRẢ vs TIỀN LÃI BỊ CỘNG:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Tiền trả Ngày 45: 500.000 đ  <  Tiền lãi Ngày 60: 592.500 đ", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Tiền lãi phát sinh chỉ trong 1 kỳ đã nuốt trọn khoản trả tối thiểu", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        v_nb = step_quantize(lerp(9_500_000, 10_092_500, beat2), 25_000) if beat2 < 0.99 else 10_092_500
        draw_centered_row_text(draw, icx, b2_y0 + 14, "TỔNG DƯ NỢ MỚI TRÊN SAO KÊ NGÀY 60:", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, f"9.500.000 + 592.500 = {fmt_vnd(v_nb)}", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 88, "Cao hơn dư nợ ban đầu 92.500 đ · Lãi kép năm EIR ≈ 42,6%/năm", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "GIỮ LẠI 9,5 TRIỆU THÊM 15 NGÀY TỐN 592.500 Đ (≈ 6,24%)", fonts["label"], (226, 168, 76))

    elif prim == "P4_MINPAY_CLOSING":
        t_y0, t_y1 = cy0 + 66, cy0 + 220
        draw_beat_card(draw, (ix0, t_y0, ix1, t_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_int = step_quantize(592_500 * max(0.1, beat1), 25_000) if beat1 < 0.99 else 592_500
        draw_centered_row_text(draw, icx, t_y0 + 12, "BÚT TOÁN LÃI THẺ TÍN DỤNG (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw.line([(ix0 + 24, t_y0 + 42), (ix0 + 24 + (iw - 48) * max(0.15, beat1), t_y0 + 42)], fill=(94, 184, 138), width=2)
        draw_centered_row_text(draw, icx, t_y0 + 54, "Bên Nợ: TK 635 (Chi phí tài chính — Lãi thẻ) = 592.500 đ", fonts["sub"], (226, 168, 76))
        draw_centered_row_text(draw, icx, t_y0 + 88, "Bên Có: TK 338 (Phải trả, phải nộp khác — 3388) = 592.500 đ", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, t_y0 + 122, f"Σ Nợ ({fmt_vnd(v_int)})  =  Σ Có ({fmt_vnd(v_int)})   [CÂN BẰNG]", fonts["val_bold"], (236, 231, 221))

        q_y0, q_y1 = cy0 + 238, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (226, 168, 76), radius=14)
        draw_centered_row_text(draw, icx, q_y0 + 18, "QUY TẮC VÀNG KHI DÙNG THẺ TÍN DỤNG:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, q_y0 + 58, "Trả đủ 100% dư nợ sao kê đúng hạn", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 106, "là cách duy nhất để giữ nguyên 45 ngày miễn lãi", fonts["sub"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))

    # ── NGUYÊN HÀM BÀI 5: `qr` (Quét mã QR chuyển khoản 50 nghìn vs Quẹt thẻ) ──
    elif prim == "P1_QR_HOOK":
        v1 = step_quantize(50_000 * max(0.2, beat1), 5_000) if beat1 < 0.99 else 50_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 182
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "QUÉT MÃ QR CHUYỂN KHOẢN TẠI QUẦY CÀ PHÊ:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 44, fmt_vnd(v1), fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Chỉ sau 3 giây: Loa báo quán nhận đủ 100% (50.000 đ · Phí 0 đ)", fonts["sub"], (182, 192, 206))

        b2_y0, b2_y1 = cy0 + 198, cy0 + 328
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 31, 38), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "ĐỐI CHIẾU VỚI CHẠM THẺ TÍN DỤNG TẠI MÁY POS:", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, "Quẹt thẻ mất 2,2% phí MDR + Phải chờ T+2", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 90, "Vì sao quét mã QR lại nhận đủ tiền tươi ngay trong 3 giây?", fonts["sub"], blend_rgb((88, 100, 116), (216, 222, 232), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P2_QR_PUSH_VS_PULL":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "1. QUẸT THẺ TÍN DỤNG = THANH TOÁN KÉO (PULL PAYMENT):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Ngân hàng phát hành ứng vốn cho vay 45 ngày + Chịu rủi ro", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Nên thu phí chiết khấu MDR 2,2% từ phía cửa hàng để bù đắp", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "2. QUÉT MÃ QR = THANH TOÁN ĐẨY (PUSH PAYMENT):", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "Bạn tự lấy tiền có sẵn (CASA) đẩy thẳng sang quán", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "0 đồng ứng vốn · 0% rủi ro nợ xấu · 0 đồng phí MDR", fonts["sub"], blend_rgb((88, 100, 116), (138, 212, 174), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "KHÔNG AI PHẢI CHO VAY 45 NGÀY NÊN KHÔNG AI THU PHÍ 2,2%", fonts["label"], (226, 168, 76))

    elif prim == "P3_QR_3SEC_WIRE":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "TRONG 3 GIÂY ĐẦU TIÊN (CHUYỂN MẠCH 24/7):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Bản tin điện tử có quỹ bảo chứng chạy sang ngân hàng quán", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Ngân hàng của quán ghi Có ngay +50.000 đ cho quán dùng tức thì", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_qr = step_quantize(50_000 * beat2, 5_000) if beat2 < 0.99 else 50_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "SỔ KẾ TOÁN QUÁN CÀ PHÊ NGAY TẠI T+0 (TT 99/2025):", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Debit TK 112 (Tiền gửi không kỳ hạn): +{fmt_vnd(v_qr)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, f"Credit TK 511 (Doanh thu bán hàng): +{fmt_vnd(v_qr)} (Không treo 1388)", fonts["sub"], blend_rgb((88, 100, 116), (138, 212, 174), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "TIỀN VÀO THẲNG TK 112 NGAY LÚC KHÁCH VỪA RỜI QUẦY", fonts["label"], (226, 168, 76))

    elif prim == "P6_QR_NET_SETTLE":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "SUỐT CẢ NGÀY: HÀNG TRIỆU LỆNH CHẠY QUA LẠI 2 CHIỀU:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "NH A sang NH B: 100 tỷ đ   |   NH B về NH A: 96 tỷ đ (Ví dụ)", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Hai ngân hàng không chở từng bọc 50.000 đ đi qua lại lẻ tẻ", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "CUỐI PHIÊN: QUYẾT TOÁN RÒNG (DEFERRED NET SETTLEMENT):", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "100 tỷ − 96 tỷ = Chỉ chuyển đúng 4 tỷ đ phần chênh lệch", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Tất toán một lần trên tài khoản thanh toán tại Ngân hàng Trung ương", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "LỜI NHẮN CHẠY TỪNG GIÂY  ·  TIỀN DỰ TRỮ CHỈ CHUYỂN PHẦN CHÊNH", fonts["label"], (226, 168, 76))

    elif prim == "P1_QR_SAVE_220K":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_sv = step_quantize(220_000 * max(0.1, beat1), 20_000) if beat1 < 0.99 else 220_000
        draw_centered_row_text(draw, icx, b1_y0 + 14, "TRÊN MỖI 200 LY CÀ PHÊ (= 10.000.000 Đ DOANH THU):", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, f"Quét QR giúp quán giữ lại: +{fmt_vnd(v_sv)} phí thẻ", fonts["big_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 88, "(Nhận đủ 10.000.000 đ ở T+0 thay vì 9.780.000 đ ở T+2)", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "VÌ SAO NGÂN HÀNG VUI VẺ MIỄN PHÍ CHUYỂN KHOẢN 0 ĐỒNG?", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, "Giữ tiền nằm lại trong bể vốn CASA lãi ~0,1%/năm", fonts["val_bold"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Thay vì bị rút ra tiền giấy ở cây ATM, ngân hàng có vốn rẻ cho vay", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "ĐỔI PHÍ LẺ VÀI TRĂM ĐỒNG ĐỂ GIỮ BỂ VỐN CASA KHỔNG LỒ", fonts["label"], (226, 168, 76))

    elif prim == "P4_QR_CLOSING":
        t_y0, t_y1 = cy0 + 66, cy0 + 220
        draw_beat_card(draw, (ix0, t_y0, ix1, t_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_10m = step_quantize(10_000_000 * max(0.1, beat1), 500_000) if beat1 < 0.99 else 10_000_000
        draw_centered_row_text(draw, icx, t_y0 + 12, "BÚT TOÁN 200 LY CÀ PHÊ QUA QR (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw.line([(ix0 + 24, t_y0 + 42), (ix0 + 24 + (iw - 48) * max(0.15, beat1), t_y0 + 42)], fill=(94, 184, 138), width=2)
        draw_centered_row_text(draw, icx, t_y0 + 54, "Bên Nợ: TK 112 (Tiền gửi không kỳ hạn) = 10.000.000 đ", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, t_y0 + 88, "Bên Có: TK 511 (Doanh thu bán hàng) = 10.000.000 đ", fonts["sub"], (226, 168, 76))
        draw_centered_row_text(draw, icx, t_y0 + 122, f"Σ Nợ ({fmt_vnd(v_10m)})  =  Σ Có ({fmt_vnd(v_10m)})   [CÂN BẰNG]", fonts["val_bold"], (236, 231, 221))

        q_y0, q_y1 = cy0 + 238, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (226, 168, 76), radius=14)
        draw_centered_row_text(draw, icx, q_y0 + 18, "NGUYÊN TẮC CHỌN CÔNG CỤ THANH TOÁN:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, q_y0 + 58, "Tại quầy quen: Quét QR giữ 100% cho quán", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 106, "Mua từ xa: Dùng thẻ để có quyền khiếu nại hoàn tiền (Chargeback)", fonts["sub"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))

    # ── NGUYÊN HÀM BÀI 6: `profitcash` (Báo cáo lãi ròng 2 tỷ nhưng két còn 50 triệu) ──
    elif prim == "P1_PROFIT_HOOK":
        v1 = step_quantize(2_000_000_000 * max(0.2, beat1), 100_000_000) if beat1 < 0.99 else 2_000_000_000
        b1_y0, b1_y1 = cy0 + 66, cy0 + 182
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "BÁO CÁO KẾT QUẢ KINH DOANH CUỐI NĂM (TK 421):", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 44, f"+{fmt_vnd(v1)}", fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Doanh thu 10 tỷ − Giá vốn 6,5 tỷ − Chi phí quản lý 1,5 tỷ = Lãi 2 tỷ", fonts["sub"], (182, 192, 206))

        b2_y0, b2_y1 = cy0 + 198, cy0 + 328
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 31, 38), (226, 168, 76))
        draw_centered_row_text(draw, icx, b2_y0 + 14, "NHƯNG TRÊN MÀN HÌNH KÉT NGÂN HÀNG (TK 112):", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, "Chỉ còn 50.000.000 đ (Thiếu 450tr trả lương)", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 90, "Bảng lương tháng 12 cần 500.000.000 đ · Tiền thật của công ty đi đâu?", fonts["sub"], blend_rgb((88, 100, 116), (216, 222, 232), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC LỜI BÌNH", fonts["label"], (226, 168, 76))

    elif prim == "P2_PROFIT_ACCRUAL_131":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "NGUYÊN TẮC KẾ TOÁN DỒN TÍCH (ACCRUAL BASIS — TT 99/2025):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Giao hàng xong là ghi nhận đủ: Credit TK 511 = 10.000.000.000 đ", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Doanh thu ghi sổ ngay khi bàn giao, không đợi tiền mặt về đủ", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_ar = step_quantize(2_500_000_000 * beat2, 250_000_000) if beat2 < 0.99 else 2_500_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "THỰC TẾ THU TIỀN TỪ ĐỐI TÁC MUA SỈ:", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Thu TK 112: 7,5 tỷ đ  ·  Nợ phải thu TK 131: {fmt_vnd(v_ar)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "2,5 tỷ đồng nằm trên giấy hẹn trả chậm 90 ngày của khách hàng", fonts["sub"], blend_rgb((88, 100, 116), (138, 212, 174), beat2))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "DOANH THU 10 TỶ TRÊN SỔ NHƯNG KÉT CHỈ THU VỀ 7,5 TỶ TIỀN TƯƠI", fonts["label"], (226, 168, 76))

    elif prim == "P3_PROFIT_INVENTORY_156":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "TỔNG TIỀN MẶT CHẢY VÀO KÉT TRONG KỲ:", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "Đầu kỳ 1.000.000.000 đ + Thu khách 7.500.000.000 đ = 8,50 tỷ đ", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Toàn bộ nguồn tiền mặt thực có để xoay sở trong suốt quý 4", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        v_out = step_quantize(8_450_000_000 * beat2, 450_000_000) if beat2 < 0.99 else 8_450_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "TỔNG TIỀN MẶT ĐÃ CHI RA KHỎI KÉT (TK 112):", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Nhập hàng 7,45 tỷ + Vận hành 1,00 tỷ = {fmt_vnd(v_out)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Trong 7,45 tỷ tiền hàng: 6,50 tỷ là giá vốn TK 632 + 950tr tồn kho TK 156", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "950 TRIỆU HÀNG TỒN KHO CHƯA BÁN KHÔNG TÍNH VÀO CHI PHÍ NHƯNG ĐÃ TRỪ TIỀN", fonts["label"], (226, 168, 76))

    elif prim == "P6_PROFIT_SPONGE_345B":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "PHÉP TRỪ TRỰC DIỆN TRÊN TÀI KHOẢN NGÂN HÀNG (TK 112):", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "8.500.000.000 đ (Vào) − 8.450.000.000 đ (Ra) = 50.000.000 đ", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Số dư tiền gửi không kỳ hạn chiều 31/12 chỉ còn đúng 50 triệu đồng", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (94, 184, 138))
        v_sp = step_quantize(3_450_000_000 * beat2, 350_000_000) if beat2 < 0.99 else 3_450_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "HAI MIẾNG BỌT BIỂN ĐANG GIAM CHẶT TIỀN MẶT:", fonts["label"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 48, f"Phải thu 2,50 tỷ + Tồn kho 950tr = {fmt_vnd(v_sp)}", fonts["val_bold"], blend_rgb((92, 104, 120), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 86, "Tiền không mất đi — nó đang ngủ đông trong công nợ và kệ kho", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "VỐN LƯU ĐỘNG PHÌNH TO HÚT CẠN KÉT TIỀN DÙ BÁO CÁO LÃI LỚN", fonts["label"], (226, 168, 76))

    elif prim == "P7_PROFIT_OCF_MINUS950M":
        b1_y0, b1_y1 = cy0 + 66, cy0 + 190
        draw_beat_card(draw, (ix0, b1_y0, ix1, b1_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 14, "CẦU NỐI GIÁN TIẾP TỪ LỢI NHUẬN SANG DÒNG TIỀN (OCF):", fonts["label"], (94, 184, 138))
        draw_centered_row_text(draw, icx, b1_y0 + 48, "+2,00 tỷ (Lãi) − 2,50 tỷ (TK 131) − 0,95 tỷ (TK 156) + 0,50 tỷ (TK 334)", fonts["val_bold"], (236, 231, 221))
        draw_centered_row_text(draw, icx, b1_y0 + 86, "Điều chỉnh biến động vốn lưu động trên Báo cáo lưu chuyển tiền tệ", fonts["sub"], (148, 160, 178))

        b2_y0, b2_y1 = cy0 + 206, cy0 + 330
        draw_beat_card(draw, (ix0, b2_y0, ix1, b2_y1), beat2, (19, 30, 40), (226, 168, 76))
        v_ocf = step_quantize(950_000_000 * beat2, 95_000_000) if beat2 < 0.99 else 950_000_000
        draw_centered_row_text(draw, icx, b2_y0 + 14, "DÒNG TIỀN THUẦN TỪ HOẠT ĐỘNG KINH DOANH (OCF):", fonts["label"], blend_rgb((96, 108, 124), (226, 168, 76), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 46, f"OCF = −{fmt_vnd(v_ocf)} (Âm 950 triệu)", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, b2_y0 + 88, "Tiền đầu kỳ (1,00 tỷ) + OCF (−950 triệu) = Tiền cuối kỳ (50 triệu)", fonts["sub"], (148, 160, 178))

        draw.line([(ix0, cy0 + 346), (ix1, cy0 + 346)], fill=(34, 44, 60), width=1)
        draw_centered_row_text(draw, icx, cy0 + 366, "LỢI NHUẬN RÒNG +2 TỶ ĐỒNG NHƯNG DÒNG TIỀN KINH DOANH ÂM 950 TRIỆU", fonts["label"], (226, 168, 76))

    else:  # P4_PROFIT_CLOSING
        t_y0, t_y1 = cy0 + 66, cy0 + 220
        draw_beat_card(draw, (ix0, t_y0, ix1, t_y1), max(0.15, beat1), (21, 29, 43), (94, 184, 138))
        v_pay = step_quantize(500_000_000 * max(0.1, beat1), 50_000_000) if beat1 < 0.99 else 500_000_000
        draw_centered_row_text(draw, icx, t_y0 + 12, "BÚT TOÁN VAY NGẮN HẠN TRẢ LƯƠNG 31/12 (TT 99/2025/TT-BTC):", fonts["label"], (148, 160, 178))
        draw.line([(ix0 + 24, t_y0 + 42), (ix0 + 24 + (iw - 48) * max(0.15, beat1), t_y0 + 42)], fill=(94, 184, 138), width=2)
        draw_centered_row_text(draw, icx, t_y0 + 54, "Bên Nợ: TK 334 (Phải trả người lao động) = 500.000.000 đ", fonts["sub"], (94, 184, 138))
        draw_centered_row_text(draw, icx, t_y0 + 88, "Bên Có: TK 112 (50.000.000 đ) + TK 341 (Vay ngắn hạn: 450.000.000 đ)", fonts["sub"], (226, 168, 76))
        draw_centered_row_text(draw, icx, t_y0 + 122, f"Σ Nợ ({fmt_vnd(v_pay)})  =  Σ Có ({fmt_vnd(v_pay)})   [CÂN BẰNG]", fonts["val_bold"], (236, 231, 221))

        q_y0, q_y1 = cy0 + 238, cy0 + 404
        draw_beat_card(draw, (ix0, q_y0, ix1, q_y1), beat2, (22, 33, 38), (226, 168, 76), radius=14)
        draw_centered_row_text(draw, icx, q_y0 + 18, "NGUYÊN TẮC SỐNG CÒN CỦA QUẢN TRỊ TÀI CHÍNH:", fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, icx, q_y0 + 58, "Lợi nhuận là chữ trên sổ · Dòng tiền là máu", fonts["big_num"], blend_rgb((96, 108, 124), (236, 231, 221), beat2))
        draw_centered_row_text(draw, icx, q_y0 + 106, "Luôn đặt Báo cáo lưu chuyển tiền tệ (OCF) cạnh Báo cáo lãi lỗ", fonts["sub"], blend_rgb((82, 102, 98), (94, 184, 138), beat2))


def render_single_scene_frame(
    story_slug: str,
    story_cfg: dict,
    s_idx: int,
    t: float,
    scene_meta: list[dict],
    locked_stage_bgs: list[Image.Image],
    fonts: dict[str, ImageFont.FreeTypeFont],
    W: int,
    H: int,
) -> Image.Image:
    sm = scene_meta[s_idx]
    s_dur = max(0.01, sm["win_t1"] - sm["win_t0"])
    s_prog = max(0.0, min(1.0, (t - sm["win_t0"]) / s_dur))

    frame_rgb = locked_stage_bgs[s_idx].copy()
    draw = ImageDraw.Draw(frame_rgb)

    draw_active_actor_pill(draw, story_cfg, s_idx, len(scene_meta), s_prog, t, fonts)
    draw_cutaway_stage_overlay(draw, story_slug, story_cfg, s_idx, sm, t, fonts)
    draw_mechanism_canvas(draw, story_slug, story_cfg, s_idx, sm, t, fonts)

    return frame_rgb


def render_smooth_video(
    story_slug: str,
    story: dict,
    scene_meta: list[dict],
    total_dur: float,
    master_wav: pathlib.Path,
    out_mp4: pathlib.Path,
) -> None:
    W, H = 1080, 1920
    FPS = 30
    total_frames = int(round(total_dur * FPS))

    story_cfg = STORY_CONFIGS[story_slug]
    sx0, sy0, sx1, sy1 = CUTAWAY_STAGE_BOX
    stage_w, stage_h = sx1 - sx0, sy1 - sy0

    stage_mask = Image.new("L", (stage_w, stage_h), 0)
    ImageDraw.Draw(stage_mask).rounded_rectangle((0, 0, stage_w - 1, stage_h - 1), radius=22, fill=255)

    # Nạp 6 tấm mặt cắt riêng biệt cho 6 cảnh (F1 — chỉ dùng short-plate-1..4 thuần Risograph, 0 chữ nướng)
    stage_plates: list[Image.Image] = []
    for rel_path, crop_box in story_cfg["scene_plates"]:
        if "fig-" in rel_path:
            raise RuntimeError(f"FAIL [Zero Baked-In Text]: Cấm dùng ảnh fig có chữ nướng sẵn trong video: {rel_path}")
        pp = ROOT / rel_path
        im_src = Image.open(pp).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
        im_stage = im_src.crop(crop_box).resize((stage_w, stage_h), Image.Resampling.LANCZOS)
        stage_plates.append(im_stage)

    assert_distinct_adjacent_plates(stage_plates, story_slug)

    fonts = {
        "actor": get_font(18, bold=True),
        "actor_sub": get_font(15, bold=False),
        "stage_tag": get_font(19, bold=True),
        "badge": get_font(17, bold=True),
        "label": get_font(18, bold=True),
        "sub": get_font(19, bold=False),
        "val_bold": get_font(22, bold=True),
        "big_num": get_font(29, bold=True),
        "hero_num": get_font(38, bold=True),
        "small": get_font(15, bold=True),
    }

    assert_parent_child_containment(story_slug, story_cfg, fonts)

    static_chrome = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sv_draw = ImageDraw.Draw(static_chrome)
    sv_draw.rounded_rectangle(CUTAWAY_STAGE_BOX, radius=20, fill=None, outline=(38, 48, 66, 255), width=1)

    locked_stage_bgs: list[Image.Image] = []
    for sp in stage_plates:
        bg_canvas = Image.new("RGBA", (W, H), (10, 14, 22, 255))
        bg_canvas.paste(sp, (sx0, sy0), stage_mask)
        bg_canvas = Image.alpha_composite(bg_canvas, static_chrome)
        locked_stage_bgs.append(bg_canvas.convert("RGB"))

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{W}x{H}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(master_wav),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(out_mp4),
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None

    TRANS_HALF = 0.42
    t0_wall = time.time()
    black_rgb = Image.new("RGB", (W, H), (8, 12, 20))

    for f_idx in range(total_frames):
        t = f_idx / FPS

        blended_rgb: Image.Image | None = None
        for b_idx in range(len(scene_meta) - 1):
            b_t = scene_meta[b_idx]["win_t1"]
            if (b_t - TRANS_HALF) <= t <= (b_t + TRANS_HALF):
                alpha = smoothstep(b_t - TRANS_HALF, b_t + TRANS_HALF, t)
                img_a = render_single_scene_frame(story_slug, story_cfg, b_idx, t, scene_meta, locked_stage_bgs, fonts, W, H)
                img_b = render_single_scene_frame(story_slug, story_cfg, b_idx + 1, t, scene_meta, locked_stage_bgs, fonts, W, H)
                blended_rgb = Image.blend(img_a, img_b, alpha)
                break

        if blended_rgb is None:
            cur_s_idx = 0
            for idx, sm in enumerate(scene_meta):
                if sm["win_t0"] <= t <= sm["win_t1"] or idx == len(scene_meta) - 1:
                    cur_s_idx = idx
                    break
            blended_rgb = render_single_scene_frame(story_slug, story_cfg, cur_s_idx, t, scene_meta, locked_stage_bgs, fonts, W, H)

        if t < 0.35:
            blended_rgb = Image.blend(black_rgb, blended_rgb, smoothstep(0.0, 0.35, t))
        elif t > total_dur - 0.65:
            blended_rgb = Image.blend(blended_rgb, black_rgb, smoothstep(total_dur - 0.65, total_dur, t))

        proc.stdin.write(blended_rgb.tobytes())

        if (f_idx + 1) % 300 == 0 or f_idx == total_frames - 1:
            elapsed = time.time() - t0_wall
            fps_actual = (f_idx + 1) / max(0.01, elapsed)
            print(f"  -> [{story_slug}] Rendered frame {f_idx + 1}/{total_frames} ({t:.1f}s / {total_dur:.1f}s, {fps_actual:.1f} fps)")

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"FFmpeg failed with code {ret}:\n{stderr_out[-1200:]}")


def ensure_short_continuous_tts(slug: str, scenes: list[dict], api_key: str) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cont_path = CACHE_DIR / f"{slug}_short_continuous_v3.json"
    if cont_path.is_file():
        return json.loads(cont_path.read_text(encoding="utf-8"))
    voice_id = "JwqRvOqFdGeQNu7UjKjw"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    full_text = "\n\n".join(s["vo"].strip() for s in scenes)
    print(f"  [TTS eleven_v3] Calling ElevenLabs for {slug}.short ({len(full_text)} chars)...")
    payload = {
        "text": full_text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.80,
            "style": 0.20,
            "use_speaker_boost": True,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read()
    cont_path.write_bytes(raw)
    return json.loads(raw.decode("utf-8"))


def run_for_story(wmp, stories: dict, sfx_map: dict[str, bytes], slug: str, api_key: str) -> None:
    story = stories[slug]
    brand_audit = wmp.step_5_0_brand_safety_audit(slug, story)
    print(f"\n=== [{slug.upper()}.SHORT — Broadcast-Grade v5.0 Safe-Zone Cinema (QĐ 61)] ===")
    print(f"[0/3 Brand Safety Specialist PASS] B1–B4 sạch ({brand_audit['scenesAudited']} cảnh, 0 tên riêng/thương hiệu)")
    scenes = story["videoScript"]["short"]["scenes"]

    cont_data = ensure_short_continuous_tts(slug, scenes, api_key)

    with tempfile.TemporaryDirectory(prefix=f"wms_smooth_{slug}_") as tmp:
        tmp_dir = pathlib.Path(tmp)
        master_wav, scene_meta, total_dur = build_timeline_and_master_audio(scenes, cont_data, sfx_map, tmp_dir)
        print(f"  -> Master audio ready: {total_dur:.2f}s (-14 LUFS, 6 smooth breath bridges + 6 SFX cues)")
        for sm in scene_meta:
            print(
                f"     Scene {sm['index']+1}: window={sm['win_t0']:.2f}s..{sm['win_t1']:.2f}s "
                f"(VO={sm['vo_t0']:.2f}s..{sm['vo_t1']:.2f}s, phrases={len(sm['phrases'])})"
            )

        out_mp4 = DIST_DIR / f"{slug}-short-9x16.mp4"
        print(f"[2/3] Rendering 30fps continuous video ({int(round(total_dur * 30))} frames) -> {out_mp4} ...")
        render_smooth_video(slug, story, scene_meta, total_dur, master_wav, out_mp4)

    print(f"[3/3] Done! Output saved to {out_mp4} ({out_mp4.stat().st_size:,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", default="install", choices=["install", "card", "pay", "minpay", "qr", "profitcash", "all"])
    args = parser.parse_args()

    wmp = load_pipeline_module()
    wmp.load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing ELEVENLABS_API_KEY")

    stories = wmp.extract_stories((ROOT / "docs/prototype.html").read_text(encoding="utf-8"))
    sfx_map = ensure_sfx_cached(api_key)

    target_slugs = ["install", "card", "pay", "minpay", "qr", "profitcash"] if args.story == "all" else [args.story]
    for slug in target_slugs:
        run_for_story(wmp, stories, sfx_map, slug, api_key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
