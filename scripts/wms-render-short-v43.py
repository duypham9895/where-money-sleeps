#!/usr/bin/env python3
"""
render_smooth_short_video.py — Bộ dựng Video & Audio Chuyển Tiếp Mượt (Broadcast-Grade v4.3 Split-Stage)
cho Where Money Sleeps (`install-short-9x16.mp4`, `card-short-9x16.mp4`, `pay-short-9x16.mp4`):

1. VOICE & AUDIO CONTINUITY (Chuyển tiếp âm thanh mượt, không đứt gãy):
   - Sử dụng bản thu `eleven_v3` LIỀN MẠCH 1 LẦN ĐỌC (`{slug}_short_continuous_v3.json`)
     với giọng Signature Giọng Tâm (`JwqRvOqFdGeQNu7UjKjw`) -> giữ nguyên 1 hơi thở, 1 âm sắc.
   - Chèn thêm khoảng thở êm 0.36s (cross-faded room tone bridge) tại ranh giới chuyển cảnh.
   - Trộn 6 hiệu ứng âm thanh chuyển cảnh tinh tế ở mức `-22 dBFS` trên nền Analog Night-Watch Room Tone (`-33 dBFS`), chuẩn hoá `-14 LUFS`.

2. VISUAL CONTINUITY & 3-ZONE SPLIT-STAGE (LUẬT 1–8):
   - ZONE 1 (y=36..354): Header + Thanh 5 ngôi nhà (22px inner padding).
   - ZONE 2 (STAGE_BOX = 48, 368, 1032, 1280): Sân khấu Mặt cắt & Live 30fps Animation độc lập 100% (0px chồng lấn).
   - ZONE 3 (CARD_BOX = 48, 1294, 1032, 1734): Khung Script & Công thức gọn ở dưới, hiển thị trọn vẹn lời bình + tô sáng từng từ.
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


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


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


# ── CẤU HÌNH ĐA BÀI VIẾT (`install`, `card`, `pay`) ─────────────────────────

STORY_CONFIGS: dict[str, dict] = {
    "install": {
        "plates": [
            "public/brand/install-short-plate-1.jpg",
            "public/brand/install-short-plate-2.jpg",
            "public/brand/install-short-plate-3.jpg",
            "public/brand/install-short-plate-4.jpg",
        ],
        "crop_windows": [
            (0, 380, 1080, 1380),
            (0, 380, 1080, 1380),
            (0, 380, 1080, 1380),
            (0, 820, 1080, 1820),
        ],
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("CỬA HÀNG", "Nơi bán máy"),
            ("CÔNG TY", "Tài chính"),
            ("NGÂN HÀNG", "Của bạn"),
            ("NGÂN HÀNG", "Cửa hàng"),
        ],
        "conduit_top": "LUỒNG HỒ SƠ & HỢP ĐỒNG (CHỈ LÀ THÔNG TIN · 0 ĐỒNG)",
        "conduit_bot": "LUỒNG TIỀN GIẢI NGÂN & TRẢ GÓP (TIỀN THẬT QUA NGÂN HÀNG)",
        "scenes": [
            (0, {0, 1}, ("wire", 0, 1), "TẠI QUẦY BÁN HÀNG  ·  LỜI HỨA TRẢ GÓP 0%", "Mua máy 12.000.000 đ  ·  Trả góp 0% trong 12 tháng"),
            (1, {1, 2}, ("wire", 1, 2), "DUYỆT HỒ SƠ VAY  ·  CHUYỂN GIAO KHOẢN NỢ", "Hợp đồng vay chuyển thẳng về Công ty tài chính"),
            (2, {1, 2, 4}, ("pipe", 2, 4, 1), "GIẢI NGÂN QUA NGÂN HÀNG  ·  KHOẢN HỤT 600.000 Đ", "12.000.000 đ  −  600.000 đ (5%)  =  11.400.000 đ thực nhận"),
            (2, {0, 2, 3}, ("pipe", 0, 3, 2), "TRẢ GÓP 12 KỲ  ·  LÃI SUẤT THỰC TẾ", "1.000.000 đ × 12 tháng  —  Lãi ngầm ~0,8%/tháng (~10%/năm)"),
            (3, {1, 2}, ("none",), "BÀI TOÁN GIÁ BÁN  ·  AI GÁNH PHẦN CHÊNH?", "Trả thẳng & trả góp cùng giá  —  Cửa hàng chịu 600.000 đ"),
            (3, {0, 1, 2, 3, 4}, ("none",), "ĐIỂM MẤU CHỐT  ·  CÂU HỎI TRƯỚC KHI KÝ", "Luôn hỏi: Trả thẳng một lần thì giá bao nhiêu?"),
        ],
    },
    "card": {
        "plates": [
            "public/brand/card-short-plate-1.jpg",
            "public/brand/card-short-plate-2.jpg",
            "public/brand/card-short-plate-3.jpg",
            "public/brand/card-short-plate-4.jpg",
        ],
        "crop_windows": [
            (0, 280, 1080, 1460),
            (0, 280, 1080, 1460),
            (0, 280, 1080, 1460),
            (0, 280, 1080, 1460),
        ],
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("QUÁN QUEN", "Nơi ăn uống"),
            ("NGÂN HÀNG", "Của quán"),
            ("TỔ CHỨC THẺ", "Chuyển mạch"),
            ("NGÂN HÀNG", "Của bạn"),
        ],
        "conduit_top": "LUỒNG XÉT DUYỆT & ĐỐI CHIẾU (CHỈ LÀ THÔNG TIN · 0 ĐỒNG)",
        "conduit_bot": "LUỒNG QUYẾT TOÁN & HOÀN TIỀN (TIỀN THẬT QUA NGÂN HÀNG)",
        "scenes": [
            (0, {0, 4}, ("wire", 4, 0), "QUẸT THẺ 10 TRIỆU  ·  TIỀN HOÀN 100.000 Đ", "Nhận +100.000 đ tiền hoàn (1%)  —  Ai đang trả khoản này?"),
            (0, {0, 1, 4}, ("wire", 1, 3, 4), "LÚC CHẠM THẺ  ·  GIỮ CHỖ TRÊN HẠN MỨC", "Tạm khoá hạn mức 10.000.000 đ  ·  Chưa có đồng tiền nào chạy"),
            (1, {1, 2, 4}, ("pipe", 4, 2, 1), "QUYẾT TOÁN T+2  ·  PHÍ NHẬN THẺ 2,2%", "Quán thực nhận 9.780.000 đ  ·  Bị trừ 220.000 đ phí MDR"),
            (1, {2, 3, 4}, ("pipe", 2, 4), "CHIA PHÍ 3 BÊN  ·  INTERCHANGE VỀ NGÂN HÀNG BẠN", "220.000 đ = 150.000 đ Interchange + 60.000 đ + 10.000 đ"),
            (2, {0, 4}, ("pipe", 0, 4), "CUỐI KỲ SAO KÊ  ·  NGUỒN CHI TIỀN HOÀN", "Ngân hàng thu 150.000 đ từ quán  ·  Trích trả bạn 100.000 đ"),
            (3, {0, 1, 2, 3, 4}, ("none",), "ĐIỂM MẤU CHỐT  ·  VÒNG TRÒN GIÁ MÓN ĂN", "Phí nhận thẻ nằm trong giá món  —  Tiền của bạn đi một vòng"),
        ],
    },
    "pay": {
        "plates": [
            "public/brand/pay-short-plate-1.jpg",
            "public/brand/pay-short-plate-2.jpg",
            "public/brand/pay-short-plate-3.jpg",
            "public/brand/pay-short-plate-4.jpg",
        ],
        "crop_windows": [
            (0, 200, 1080, 1580),
            (0, 200, 1080, 1580),
            (0, 200, 1080, 1580),
            (0, 200, 1080, 1580),
        ],
        "house_nodes": [
            ("CÔNG TY", "Nơi trả lương"),
            ("NGÂN HÀNG", "Trả lương"),
            ("BẠN", "Người nhận"),
            ("ĐỒNG NGHIỆP", "500 tài khoản"),
            ("KHỐI CHO VAY", "Của ngân hàng"),
        ],
        "conduit_top": "LUỒNG LỆNH CHI LƯƠNG & GHI SỔ (CHỈ LÀ THÔNG TIN · 0 ĐỒNG)",
        "conduit_bot": "LUỒNG VỐN HUY ĐỘNG & CHO VAY (VỐN GỘP TRONG NGÂN HÀNG)",
        "scenes": [
            (0, {0, 1, 2}, ("wire", 0, 1, 2), "TIN NHẮN LƯƠNG VỀ  ·  15.000.000 Đ GHI CÓ", "Tài khoản +15.000.000 đ  ·  0 đồng tiền mặt phải di chuyển"),
            (0, {0, 1, 2}, ("wire", 0, 1, 2), "CHUYỂN KHOẢN CÙNG NGÂN HÀNG  ·  CƠ CHẾ ON-US", "Sửa 2 dòng sổ: Bớt nợ Công ty 15tr  ·  Tăng nợ Bạn 15tr"),
            (1, {1, 2, 3}, ("pipe", 3, 1), "SỐ DƯ NẰM YÊN (CASA)  ·  500 ĐỒNG NGHIỆP", "500 người × 5.000.000 đ = 2,5 tỷ đồng nằm chờ (lãi ~0,1%/năm)"),
            (1, {1, 3, 4}, ("pipe", 1, 4), "CHI PHÍ VỐN RẺ  ·  CHÊNH LỆCH GẤP 50 LẦN", "Trả lãi CASA ~2,5 triệu/năm  vs  Kỳ hạn 5% tốn 125 triệu/năm"),
            (2, {0, 1, 4}, ("wire", 1, 0), "ĐỔI BẢNG LƯƠNG LẤY ƯU ĐÃI  ·  MẶC CẢ DOANH NGHIỆP", "Ngân hàng có nguồn vốn rẻ  ·  Công ty nhận ưu đãi phí & lãi vay"),
            (3, {0, 1, 2, 3, 4}, ("none",), "ĐIỂM MẤU CHỐT  ·  SỐ DƯ LÀ KHOẢN NGÂN HÀNG NỢ BẠN", "Tiền lương ngủ trong sổ ngân hàng và sinh lời cho người khác"),
        ],
    },
}

SLATE_LEAK_RE = re.compile(
    r"(\bCẢNH\s*\d|\bSCENE\s*\d|\bMỐC\s*\d|\bÝ\s*\d+\s*/\s*\d+|\bKỲ\s*\d+\s*/\s*\d+|Chữ\s+to|SFX\s*gợi\s*ý|dây\s+điện|dây\s+tín\s+hiệu|ống\s+ngầm|ống\s+quyết\s+toán|[→⇒➜➔←↔])",
    re.IGNORECASE,
)

NUMBER_RE = re.compile(
    r"(\b(?:mười|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|không|trăm|nghìn|triệu|tỷ|phần|trăm|phẩy|kỳ|tháng)\b|\d+[.,]?\d*%?)",
    re.IGNORECASE,
)


def assert_broadcast_overlay_clean(texts: list[str]) -> None:
    for txt in texts:
        m = SLATE_LEAK_RE.search(str(txt or ""))
        if m:
            raise RuntimeError(
                f"FAIL [B4 Broadcast Polish]: Lộ nhãn kịch bản nội bộ '{m.group(0)}' trong chuỗi hiển thị: {txt!r}"
            )


def precompute_scene_layouts(
    scene_meta: list[dict],
    scene_cfg_list: list[tuple],
    f_callout: ImageFont.FreeTypeFont,
    f_vo: ImageFont.FreeTypeFont,
    f_vo_bold: ImageFont.FreeTypeFont,
    max_w: int,
) -> None:
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))
    space_w = max(11.0, dummy.textlength(" ", font=f_vo_bold) + 2.5)
    line_h = 36
    phrase_gap = 8

    overlay_audit_strings: list[str] = []

    for s_idx, sm in enumerate(scene_meta):
        _, _, _, kicker, headline = scene_cfg_list[s_idx]
        overlay_audit_strings.extend([kicker, headline])
        sm["kicker"] = kicker

        c_words = headline.split()
        c_lines: list[str] = []
        cur_c = ""
        for w in c_words:
            test = (cur_c + " " + w).strip()
            if dummy.textlength(test, font=f_callout) <= max_w:
                cur_c = test
            else:
                if cur_c:
                    c_lines.append(cur_c)
                cur_c = w
        if cur_c:
            c_lines.append(cur_c)
        sm["callout_lines"] = c_lines[:2]

        cur_y = 0
        for p_idx, phr in enumerate(sm["phrases"]):
            lines: list[list[dict]] = []
            cur_line: list[dict] = []
            cur_w = 0.0
            for wm in phr["words"]:
                w_str = wm["word"]
                overlay_audit_strings.append(w_str)
                is_num = bool(NUMBER_RE.search(w_str))
                w_font = f_vo_bold if is_num else f_vo
                ww = dummy.textlength(w_str, font=w_font)
                item = {
                    "word": w_str,
                    "w": ww,
                    "t0": wm["t0"],
                    "t1": wm["t1"],
                    "is_num": is_num,
                    "p_idx": p_idx,
                }
                if cur_line and (cur_w + space_w + ww > max_w - 22):
                    lines.append(cur_line)
                    cur_line = [item]
                    cur_w = ww
                else:
                    if cur_line:
                        cur_w += space_w + ww
                    else:
                        cur_w = ww
                    cur_line.append(item)
            if cur_line:
                lines.append(cur_line)

            phr["y0"] = cur_y
            placed_words: list[dict] = []
            for l_idx, ln in enumerate(lines):
                rx = 20.0
                ry = cur_y + l_idx * line_h
                for item in ln:
                    item_copy = dict(item)
                    item_copy["rx"] = rx
                    item_copy["ry"] = ry
                    placed_words.append(item_copy)
                    rx += item["w"] + space_w
            phr["placed_words"] = placed_words
            phr["y1"] = cur_y + len(lines) * line_h
            cur_y = phr["y1"] + phrase_gap

    assert_broadcast_overlay_clean(overlay_audit_strings)


# Bất biến Hình học 3 Vùng Tách Biệt Không Đè Nhau (LUẬT 6b & LUẬT 8: Non-Overlapping 3-Zone Split-Stage)
HEADER_BOX = (48, 36, 1032, 168)
CONDUIT_PARENT_BOX = (48, 180, 1032, 354)
HOUSE_BW = 172
HOUSE_BH = 50
HOUSE_GAP = 20
HOUSE_XS = [70 + HOUSE_BW // 2 + i * (HOUSE_BW + HOUSE_GAP) for i in range(5)]  # [156, 348, 540, 732, 924]
WIRE_Y = 222
NODE_Y = 267
PIPE_Y = 312

STAGE_BOX = (48, 368, 1032, 1280)
CARD_BOX = (48, 1294, 1032, 1734)


def assert_parent_child_containment(
    scene_meta: list[dict],
    house_nodes: list[tuple[str, str]],
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))

    if not (HEADER_BOX[3] + 10 <= CONDUIT_PARENT_BOX[1] and CONDUIT_PARENT_BOX[3] + 12 <= STAGE_BOX[1] and STAGE_BOX[3] + 12 <= CARD_BOX[1]):
        raise RuntimeError(
            f"FAIL [LUẬT 8 Zone Overlap]: Các vùng giao diện chồng lấn nhau: "
            f"Header={HEADER_BOX}, Conduit={CONDUIT_PARENT_BOX}, Stage={STAGE_BOX}, Card={CARD_BOX}"
        )

    px0, py0, px1, py1 = CONDUIT_PARENT_BOX
    min_h_pad = 20
    min_v_pad = 12

    for i, hx in enumerate(HOUSE_XS):
        cx0 = hx - HOUSE_BW // 2
        cx1 = hx + HOUSE_BW // 2
        cy0 = NODE_Y - HOUSE_BH // 2
        cy1 = NODE_Y + HOUSE_BH // 2
        if cx0 < px0 + min_h_pad or cx1 > px1 - min_h_pad:
            raise RuntimeError(
                f"FAIL [B4 Box Containment]: Hộp con thứ {i} ({house_nodes[i][0]}) tràn ngang khung cha "
                f"(child x={cx0}..{cx1} vs parent x={px0}..{px1}, cần lề trong >= {min_h_pad}px)"
            )
        if cy0 < WIRE_Y + min_v_pad or cy1 > PIPE_Y - min_v_pad:
            raise RuntimeError(
                f"FAIL [B4 Box Containment]: Hộp con thứ {i} tràn dọc vào đường luồng "
                f"(child y={cy0}..{cy1} vs wire_y={WIRE_Y}, pipe_y={PIPE_Y})"
            )
        l1, l2 = house_nodes[i]
        tw1 = dummy.textlength(l1, font=fonts["node_top"])
        tw2 = dummy.textlength(l2, font=fonts["node_sub"])
        if tw1 > HOUSE_BW - 20 or tw2 > HOUSE_BW - 20:
            raise RuntimeError(
                f"FAIL [B4 Box Containment]: Chữ trong hộp con thứ {i} ({l1} / {l2}) quá rộng ({max(tw1, tw2):.1f}px > {HOUSE_BW - 20}px)"
            )

    card_x0, card_top, card_x1, card_bot = CARD_BOX
    for s_idx, sm in enumerate(scene_meta):
        kicker_w = int(dummy.textlength(sm["kicker"], font=fonts["badge"])) + 34
        if 80 + kicker_w > card_x1 - 24:
            raise RuntimeError(f"FAIL [B4 Box Containment]: Kicker cảnh {s_idx} tràn ngang khung Card")
        cy = card_top + 74
        for ln in sm["callout_lines"]:
            lw = dummy.textlength(ln, font=fonts["callout"])
            if 80 + lw > card_x1 - 24:
                raise RuntimeError(f"FAIL [B4 Box Containment]: Callout cảnh {s_idx} tràn ngang khung Card ({80 + lw:.1f} > {card_x1 - 24})")
            cy += 36
        div_y = cy + 6
        base_wx = 80
        base_wy = div_y + 12
        for phr in sm["phrases"]:
            for pw in phr["placed_words"]:
                wx1 = base_wx + pw["rx"] + pw["w"] + 6
                wy1 = base_wy + pw["ry"] + 30
                if wx1 > card_x1 - 20:
                    raise RuntimeError(
                        f"FAIL [B4 Box Containment]: Từ '{pw['word']}' ở cảnh {s_idx} tràn ngang khung Card ({wx1:.1f} > {card_x1 - 20})"
                    )
                if wy1 > card_bot - 14:
                    raise RuntimeError(
                        f"FAIL [B4 Box Containment]: Từ '{pw['word']}' ở cảnh {s_idx} tràn đáy khung Card ({wy1:.1f} > {card_bot - 14})"
                    )


def draw_stage_pill(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill_rgba: tuple[int, int, int, int],
    outline_rgba: tuple[int, int, int, int],
    text_rgba: tuple[int, int, int, int],
) -> None:
    tw = draw.textlength(text, font=font)
    pw = tw + 28
    ph = 36
    x0 = max(STAGE_BOX[0] + 20, min(STAGE_BOX[2] - 20 - pw, cx - pw / 2))
    y0 = max(STAGE_BOX[1] + 16, min(STAGE_BOX[3] - 16 - ph, cy - ph / 2))
    draw.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=10, fill=fill_rgba, outline=outline_rgba, width=2)
    draw.text((x0 + 14, y0 + 7), text, font=font, fill=text_rgba)


def draw_particles_along_segment(
    draw: ImageDraw.ImageDraw,
    p0: tuple[float, float],
    p1: tuple[float, float],
    t: float,
    speed: float,
    offsets: tuple[float, ...],
    outer_rgba: tuple[int, int, int, int],
    inner_rgba: tuple[int, int, int, int],
) -> None:
    for off in offsets:
        u = smoothstep(0.0, 1.0, (t * speed + off) % 1.0)
        px = lerp(p0[0], p1[0], u)
        py = lerp(p0[1], p1[1], u)
        draw.ellipse((px - 11, py - 11, px + 11, py + 11), fill=outer_rgba)
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=inner_rgba)


def draw_stage_live_animation(
    story_slug: str,
    draw: ImageDraw.ImageDraw,
    s_idx: int,
    t: float,
    s_prog: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    f_tag = fonts["stage_tag"]
    sx0, sy0, sx1, sy1 = STAGE_BOX

    if story_slug == "install":
        if s_idx == 0:
            pulse = 0.5 + 0.5 * math.sin(t * 4.2)
            r_glow = int(18 + 8 * pulse)
            pt_shop, pt_top = (425, 960), (510, 600)
            draw.ellipse((pt_shop[0] - r_glow, pt_shop[1] - r_glow, pt_shop[0] + r_glow, pt_shop[1] + r_glow), outline=(255, 209, 102, int(190 * pulse + 50)), width=3)
            draw_particles_along_segment(draw, pt_shop, pt_top, t, 0.55, (0.0, 0.33, 0.66), (245, 166, 35, 110), (255, 230, 150, 250))
            draw_stage_pill(draw, 540, 412, "CÂU HỎI: AI TRẢ TIỀN LÃI CHO 12 THÁNG CHỜ ĐỢI?", f_tag, (14, 20, 32, 230), (245, 166, 35, 225), (255, 209, 102, 255))
            draw_stage_pill(draw, 460, 1165, "QUẦY CỬA HÀNG: MÁY 12.000.000 Đ  ·  TỜ RƠI GHI 0% × 12 KỲ", f_tag, (14, 20, 32, 230), (72, 187, 120, 225), (154, 240, 180, 255))
        elif s_idx == 1:
            draw_particles_along_segment(draw, (420, 965), (675, 680), t, 0.65, (0.0, 0.33, 0.66), (245, 166, 35, 115), (255, 236, 160, 255))
            draw_stage_pill(draw, 640, 420, "CÔNG TY TÀI CHÍNH: CHỦ NỢ MỚI (GIỮ HỢP ĐỒNG 12.000.000 Đ)", f_tag, (14, 20, 32, 232), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 395, 1195, "QUẦY CỬA HÀNG: ĐÃ GIAO MÁY  ·  CHƯA NHẬN ĐỒNG TIỀN NÀO", f_tag, (14, 20, 32, 232), (80, 210, 190, 225), (175, 248, 236, 255))
        elif s_idx == 2:
            p_vault, p_junc, p_shop_tray, p_fee_tray = (650, 650), (535, 765), (390, 1015), (575, 975)
            draw_particles_along_segment(draw, p_vault, p_shop_tray, t, 0.60, (0.0, 0.33, 0.66), (72, 187, 120, 115), (154, 240, 180, 255))
            draw_particles_along_segment(draw, p_junc, p_fee_tray, t, 0.55, (0.0, 0.50), (245, 166, 35, 130), (255, 215, 110, 255))
            draw_stage_pill(draw, 345, 1195, "CỬA HÀNG THỰC NHẬN: +11.400.000 Đ (95%)", f_tag, (14, 20, 32, 235), (72, 187, 120, 240), (154, 240, 180, 255))
            draw_stage_pill(draw, 745, 1125, "GIỮ LẠI: −600.000 Đ (LÃI 5%)", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
        elif s_idx == 3:
            bar_x0, bar_y0, bar_x1, bar_y1 = sx0 + 36, sy0 + 22, sx1 - 36, sy0 + 82
            draw.rounded_rectangle((bar_x0, bar_y0, bar_x1, bar_y1), radius=12, fill=(14, 20, 32, 232), outline=(245, 166, 35, 210), width=2)
            active_months = min(12, max(1, int(s_prog * 13.0)))
            cell_w = (bar_x1 - bar_x0 - 24) / 12.0
            for m_i in range(12):
                cx0 = bar_x0 + 12 + m_i * cell_w + 3
                cx1 = cx0 + cell_w - 6
                is_paid = m_i < active_months
                c_fill = (72, 187, 120, 235) if is_paid else (38, 50, 72, 190)
                draw.rounded_rectangle((cx0, bar_y0 + 12, cx1, bar_y1 - 12), radius=6, fill=c_fill)
                m_lbl = f"T{m_i+1}"
                mw = draw.textlength(m_lbl, font=fonts["node_sub"])
                draw.text(((cx0 + cx1 - mw) / 2, bar_y0 + 21), m_lbl, font=fonts["node_sub"], fill=(12, 18, 28, 255) if is_paid else (175, 188, 205, 220))
            draw_stage_pill(draw, 540, 1200, "TRẢ THẲNG 11.400.000 Đ  vs  TRẢ GÓP 12.000.000 Đ  =  LÃI THỰC TẾ ~10%/NĂM", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
        elif s_idx == 4:
            pulse = 0.5 + 0.5 * math.sin(t * 3.5)
            draw_stage_pill(draw, 330, 615, "TRẢ THẲNG GIẢM 600K: BẠN TRẢ LÃI", f_tag, (14, 20, 32, 235), (245, 166, 35, int(190 + 60 * pulse)), (255, 209, 102, 255))
            draw_stage_pill(draw, 745, 665, "MỘT GIÁ CHUNG: CỬA HÀNG GÁNH 600K", f_tag, (14, 20, 32, 235), (72, 187, 120, int(190 + 60 * (1.0 - pulse))), (154, 240, 180, 255))
            draw_stage_pill(draw, 540, 1205, "SỔ KẾ TOÁN: 600.000 Đ CHI PHÍ HỖ TRỢ LÃI SUẤT KHÔNG HỀ BIẾN MẤT", f_tag, (14, 20, 32, 235), (245, 166, 35, 225), (244, 239, 230, 255))
        else:
            draw_stage_pill(draw, 540, 595, "12.000.000 Đ (GHI BÁN)  −  11.400.000 Đ (THỰC NHẬN)  =  600.000 Đ TIỀN LÃI", f_tag, (14, 20, 32, 238), (245, 166, 35, 245), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "CÂU HỎI DUY NHẤT CẦN HỎI: “TRẢ THẲNG MỘT LẦN THÌ GIÁ BAO NHIÊU?”", f_tag, (14, 20, 32, 238), (72, 187, 120, 245), (154, 240, 180, 255))

    elif story_slug == "card":
        if s_idx == 0:
            draw_particles_along_segment(draw, (650, 660), (430, 960), t, 0.55, (0.0, 0.33, 0.66), (245, 166, 35, 115), (255, 230, 150, 255))
            draw_stage_pill(draw, 540, 412, "HOÁ ĐƠN 10.000.000 Đ  ·  HOÀN TIỀN +100.000 Đ (1%)", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "CÂU HỎI: 100.000 Đ TIỀN HOÀN NÀY ĐƯỢC TRÍCH TỪ ĐÂU?", f_tag, (14, 20, 32, 235), (72, 187, 120, 235), (154, 240, 180, 255))
        elif s_idx == 1:
            draw_particles_along_segment(draw, (430, 960), (520, 620), t, 0.65, (0.0, 0.33, 0.66), (245, 166, 35, 115), (255, 236, 160, 255))
            draw_stage_pill(draw, 640, 420, "NGÂN HÀNG CỦA BẠN: GIỮ CHỖ 10.000.000 Đ TRÊN HẠN MỨC", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 440, 1205, "QUẦY QUÁN QUEN: CHƯA CÓ ĐỒNG TIỀN THẬT NÀO CHẠY VỀ KÉT", f_tag, (14, 20, 32, 235), (80, 210, 190, 235), (175, 248, 236, 255))
        elif s_idx == 2:
            draw_particles_along_segment(draw, (670, 660), (370, 990), t, 0.60, (0.0, 0.33, 0.66), (72, 187, 120, 120), (154, 240, 180, 255))
            draw_particles_along_segment(draw, (550, 780), (455, 955), t, 0.50, (0.0, 0.50), (245, 166, 35, 130), (255, 215, 110, 255))
            draw_stage_pill(draw, 355, 1205, "QUÁN THỰC NHẬN: +9.780.000 Đ (SAU T+2)", f_tag, (14, 20, 32, 235), (72, 187, 120, 240), (154, 240, 180, 255))
            draw_stage_pill(draw, 760, 1130, "PHÍ NHẬN THẺ (MDR 2,2%): −220.000 Đ", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
        elif s_idx == 3:
            draw_particles_along_segment(draw, (455, 955), (670, 660), t, 0.60, (0.0, 0.33, 0.66), (245, 166, 35, 125), (255, 224, 130, 255))
            draw_stage_pill(draw, 540, 415, "NGÂN HÀNG CỦA BẠN NHẬN: +150.000 Đ PHÍ INTERCHANGE (1,5%)", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "NGÂN HÀNG CỦA QUÁN GIỮ 60.000 Đ  ·  PHÍ MẠNG THẺ 10.000 Đ", f_tag, (14, 20, 32, 236), (80, 210, 190, 235), (175, 248, 236, 255))
        elif s_idx == 4:
            draw_particles_along_segment(draw, (410, 980), (675, 670), t, 0.60, (0.0, 0.50), (72, 187, 120, 120), (154, 240, 180, 255))
            draw_particles_along_segment(draw, (675, 670), (370, 995), t, 0.55, (0.25, 0.75), (245, 166, 35, 130), (255, 224, 130, 255))
            draw_stage_pill(draw, 630, 415, "THU INTERCHANGE 150.000 Đ  ·  TRÍCH HOÀN TIỀN 100.000 Đ", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 460, 1205, "BẠN TRẢ ĐỦ 10.000.000 Đ DƯ NỢ SAO KÊ  ·  NHẬN LẠI 100.000 Đ", f_tag, (14, 20, 32, 236), (72, 187, 120, 240), (154, 240, 180, 255))
        else:
            pulse = 0.5 + 0.5 * math.sin(t * 3.5)
            draw_stage_pill(draw, 540, 415, "QUÁN ĐỊNH GIÁ CHUNG: PHÍ NHẬN THẺ 2,2% NẰM TRONG GIÁ MÓN", f_tag, (14, 20, 32, 238), (245, 166, 35, int(195 + 55 * pulse)), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "TIỀN HOÀN 100.000 Đ RẤT CÓ THỂ LÀ TIỀN CỦA CHÍNH BẠN ĐI MỘT VÒNG", f_tag, (14, 20, 32, 238), (72, 187, 120, 245), (154, 240, 180, 255))

    elif story_slug == "pay":
        if s_idx == 0:
            draw_particles_along_segment(draw, (320, 815), (535, 700), t, 0.65, (0.0, 0.50), (245, 166, 35, 120), (255, 230, 150, 255))
            draw_particles_along_segment(draw, (535, 700), (710, 835), t, 0.65, (0.25, 0.75), (245, 166, 35, 120), (255, 230, 150, 255))
            draw_stage_pill(draw, 540, 412, "BÁO GHI CÓ +15.000.000 Đ  ·  KÉT TIỀN NGÂN HÀNG VẪN ĐÓNG KÍN", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "KHÔNG MỘT ĐỒNG TIỀN THẬT NÀO RỜI KHỎI TOÀ NHÀ NGÂN HÀNG", f_tag, (14, 20, 32, 235), (72, 187, 120, 235), (154, 240, 180, 255))
        elif s_idx == 1:
            draw_particles_along_segment(draw, (320, 815), (535, 700), t, 0.60, (0.0, 0.33, 0.66), (245, 166, 35, 125), (255, 236, 160, 255))
            draw_stage_pill(draw, 350, 420, "CÔNG TY: −15.000.000 Đ", f_tag, (14, 20, 32, 235), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 730, 420, "TÀI KHOẢN BẠN: +15.000.000 Đ", f_tag, (14, 20, 32, 235), (72, 187, 120, 240), (154, 240, 180, 255))
            draw_stage_pill(draw, 540, 1205, "CÙNG NGÂN HÀNG (ON-US): CHỈ ĐỔI TÊN CHỦ NỢ TRÊN SỔ CÁI", f_tag, (14, 20, 32, 235), (80, 210, 190, 235), (175, 248, 236, 255))
        elif s_idx == 2:
            for x_ray in (340, 460, 610, 730):
                draw_particles_along_segment(draw, (x_ray, 720), (x_ray, 980), t, 0.55, (0.0, 0.50), (72, 187, 120, 115), (154, 240, 180, 255))
            draw_stage_pill(draw, 540, 412, "500 ĐỒNG NGHIỆP × 5.000.000 Đ = 2,5 TỶ ĐỒNG SỐ DƯ NẰM YÊN (CASA)", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "LÃI TIỀN GỬI KHÔNG KỲ HẠN RẤT THẤP: VÍ DỤ ~0,1% / NĂM", f_tag, (14, 20, 32, 236), (72, 187, 120, 240), (154, 240, 180, 255))
        elif s_idx == 3:
            draw_stage_pill(draw, 355, 420, "CASA 0,1%: ~2,5 TRIỆU / NĂM", f_tag, (14, 20, 32, 236), (72, 187, 120, 240), (154, 240, 180, 255))
            draw_stage_pill(draw, 730, 420, "KỲ HẠN 5%: ~125 TRIỆU / NĂM", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "NGUỒN VỐN RẺ GẤP 50 LẦN: LÝ DO NGÂN HÀNG MUỐN GIỮ BẢNG LƯƠNG", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
        elif s_idx == 4:
            draw_particles_along_segment(draw, (370, 620), (740, 770), t, 0.60, (0.0, 0.50), (245, 166, 35, 120), (255, 230, 150, 255))
            draw_stage_pill(draw, 540, 412, "BÊN CHO VAY CỦA NGÂN HÀNG: DÙNG BỂ VỐN RẺ ĐỂ CHO VAY LÃI CAO HƠN", f_tag, (14, 20, 32, 236), (245, 166, 35, 240), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "CÔNG TY NHẬN ƯU ĐÃI PHÍ DỊCH VỤ HOẶC LÃI VAY (TUỲ HỢP ĐỒNG)", f_tag, (14, 20, 32, 236), (72, 187, 120, 240), (154, 240, 180, 255))
        else:
            draw_stage_pill(draw, 540, 412, "SỐ DƯ TRÊN ĐIỆN THOẠI = KHOẢN NGÂN HÀNG ĐANG NỢ BẠN", f_tag, (14, 20, 32, 238), (245, 166, 35, 245), (255, 209, 102, 255))
            draw_stage_pill(draw, 540, 1205, "ĐÊM NAY, SỐ DƯ NẰM YÊN CỦA BẠN ĐANG LÀM VIỆC CHO AI?", f_tag, (14, 20, 32, 238), (72, 187, 120, 245), (154, 240, 180, 255))


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

    p_idx, active_set, flow_spec, kicker, _ = story_cfg["scenes"][s_idx]
    frame_rgba = locked_stage_bgs[p_idx].copy()

    dyn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dyn)

    f_node_top = fonts["node_top"]
    f_node_sub = fonts["node_sub"]
    f_badge = fonts["badge"]
    f_callout = fonts["callout"]
    f_vo = fonts["vo"]
    f_vo_bold = fonts["vo_bold"]

    house_xs = HOUSE_XS
    wire_y = WIRE_Y
    node_y = NODE_Y
    pipe_y = PIPE_Y

    draw.line([(house_xs[0], wire_y), (house_xs[-1], wire_y)], fill=(245, 166, 35, 125), width=3)
    draw.line([(house_xs[0], pipe_y), (house_xs[-1], pipe_y)], fill=(72, 187, 120, 135), width=5)

    flow_kind = flow_spec[0]
    if flow_kind in ("wire", "pipe") and len(flow_spec) >= 3:
        nodes_seq = flow_spec[1:]
        y_line = wire_y if flow_kind == "wire" else pipe_y
        outer_c = (245, 166, 35, 95) if flow_kind == "wire" else (72, 187, 120, 95)
        inner_c = (255, 224, 130, 245) if flow_kind == "wire" else (154, 240, 180, 245)
        n_segs = len(nodes_seq) - 1
        for offset in (0.0, 0.33, 0.66):
            p_cyc = (t * 0.72 + offset) % 1.0
            seg_f = p_cyc * n_segs
            seg_i = min(n_segs - 1, int(math.floor(seg_f)))
            seg_u = smoothstep(0.0, 1.0, seg_f - seg_i)
            px = lerp(house_xs[nodes_seq[seg_i]], house_xs[nodes_seq[seg_i + 1]], seg_u)
            draw.ellipse((px - 10, y_line - 10, px + 10, y_line + 10), fill=outer_c)
            draw.ellipse((px - 5, y_line - 5, px + 5, y_line + 5), fill=inner_c)

    house_nodes = story_cfg["house_nodes"]
    for i, hx in enumerate(house_xs):
        is_act = i in active_set
        fill_col = (245, 166, 35, 248) if is_act else (22, 31, 46, 215)
        out_col = (255, 224, 140, 255) if is_act else (90, 108, 135, 210)
        top_col = (14, 20, 32, 255) if is_act else (232, 238, 246, 245)
        sub_col = (28, 38, 56, 240) if is_act else (164, 178, 198, 225)
        bw, bh = HOUSE_BW, HOUSE_BH
        draw.rounded_rectangle(
            (hx - bw // 2, node_y - bh // 2, hx + bw // 2, node_y + bh // 2),
            radius=12,
            fill=fill_col,
            outline=out_col,
            width=2,
        )
        line1, line2 = house_nodes[i]
        tw1 = draw.textlength(line1, font=f_node_top)
        tw2 = draw.textlength(line2, font=f_node_sub)
        draw.text((hx - tw1 / 2, node_y - 19), line1, font=f_node_top, fill=top_col)
        draw.text((hx - tw2 / 2, node_y + 2), line2, font=f_node_sub, fill=sub_col)

    draw_stage_live_animation(story_slug, draw, s_idx, t, s_prog, fonts)

    card_x0, card_top, card_x1, card_bot = CARD_BOX
    draw.rounded_rectangle(
        (card_x0, card_top, card_x1, card_bot),
        radius=24,
        fill=(12, 18, 30, 242),
        outline=(245, 166, 35, 215),
        width=3,
    )

    seg_total_w = W - 160
    seg_gap = 10
    seg_w = (seg_total_w - seg_gap * 5) / 6.0
    for s_i in range(6):
        sx0 = 80 + s_i * (seg_w + seg_gap)
        sx1 = sx0 + seg_w
        if s_i < s_idx:
            draw.rounded_rectangle((sx0, card_top + 15, sx1, card_top + 20), radius=3, fill=(245, 166, 35, 235))
        elif s_i == s_idx:
            draw.rounded_rectangle((sx0, card_top + 15, sx1, card_top + 20), radius=3, fill=(65, 80, 105, 180))
            fill_x = sx0 + seg_w * s_prog
            draw.rounded_rectangle((sx0, card_top + 15, max(sx0 + 8, fill_x), card_top + 20), radius=3, fill=(255, 209, 102, 255))
        else:
            draw.rounded_rectangle((sx0, card_top + 15, sx1, card_top + 20), radius=3, fill=(65, 80, 105, 145))

    phrases = sm["phrases"]
    active_p_float = 0.0
    active_p_idx = 0
    for p_i, phr in enumerate(phrases):
        if t >= phr["t0"] - 0.25:
            active_p_idx = p_i
            trans_w = smoothstep(phr["t0"] - 0.25, phr["t0"] + 0.12, t) if p_i > 0 else 1.0
            active_p_float = (p_i - 1) + trans_w if p_i > 0 else 0.0

    kicker_w = int(draw.textlength(kicker, font=f_badge)) + 34
    draw.rounded_rectangle((80, card_top + 30, 80 + kicker_w, card_top + 64), radius=9, fill=(245, 166, 35, 245))
    draw.text((97, card_top + 37), kicker, font=f_badge, fill=(14, 20, 32, 255))

    cy = card_top + 74
    for ln in sm["callout_lines"]:
        draw.text((80, cy), ln, font=f_callout, fill=(255, 209, 102, 255))
        cy += 36

    div_y = cy + 6
    draw.line([(80, div_y), (W - 80, div_y)], fill=(245, 166, 35, 110), width=2)

    base_wx = 80
    base_wy = div_y + 12

    p_low = int(math.floor(active_p_float))
    p_high = min(len(phrases) - 1, p_low + 1)
    p_frac = active_p_float - p_low
    bar_y0 = base_wy + lerp(phrases[p_low]["y0"], phrases[p_high]["y0"], p_frac)
    bar_y1 = base_wy + lerp(phrases[p_low]["y1"], phrases[p_high]["y1"], p_frac) - 5
    draw.rounded_rectangle((base_wx, bar_y0 + 2, base_wx + 6, max(bar_y0 + 14, bar_y1)), radius=3, fill=(255, 209, 102, 255))

    for p_i, phr in enumerate(phrases):
        if p_i == active_p_idx:
            p_focus = 1.0
        elif p_i < active_p_idx:
            p_focus = 0.84
        else:
            p_focus = lerp(0.60, 1.0, smoothstep(phr["t0"] - 0.35, phr["t0"] + 0.05, t))

        for pw in phr["placed_words"]:
            wx = base_wx + pw["rx"]
            wy = base_wy + pw["ry"]
            w_t0 = pw["t0"]
            w_t1 = pw["t1"]
            ww = pw["w"]
            w_str = pw["word"]
            is_num = pw["is_num"]

            use_font = f_vo_bold if is_num else f_vo

            ramp_in = smoothstep(w_t0 - 0.07, w_t0 + 0.01, t)
            ramp_out = smoothstep(w_t1 - 0.01, w_t1 + 0.11, t)
            w_act = max(0.0, min(1.0, ramp_in * (1.0 - ramp_out)))
            w_spoken = ramp_in

            if w_act > 0.02:
                pad_x, pad_y = 5, 2
                pill_alpha = int(68 * w_act)
                draw.rounded_rectangle(
                    (wx - pad_x, wy - pad_y, wx + ww + pad_x, wy + 28 + pad_y),
                    radius=7,
                    fill=(245, 166, 35, pill_alpha),
                )

            unspoken_r, unspoken_g, unspoken_b = 195 * p_focus, 192 * p_focus, 184 * p_focus
            if is_num:
                spoken_r, spoken_g, spoken_b = 255 * p_focus, 209 * p_focus, 102 * p_focus
            else:
                spoken_r, spoken_g, spoken_b = 244 * p_focus, 239 * p_focus, 230 * p_focus

            base_r = lerp(unspoken_r, spoken_r, w_spoken)
            base_g = lerp(unspoken_g, spoken_g, w_spoken)
            base_b = lerp(unspoken_b, spoken_b, w_spoken)

            final_r = int(lerp(base_r, 255.0, w_act))
            final_g = int(lerp(base_g, 222.0, w_act))
            final_b = int(lerp(base_b, 128.0, w_act))

            draw.text((wx, wy), w_str, font=use_font, fill=(final_r, final_g, final_b, 255))

    return Image.alpha_composite(frame_rgba, dyn).convert("RGB")


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
    plate_paths = [ROOT / p for p in story_cfg["plates"]]
    crop_windows = story_cfg["crop_windows"]

    sx0, sy0, sx1, sy1 = STAGE_BOX
    stage_w, stage_h = sx1 - sx0, sy1 - sy0

    stage_mask = Image.new("L", (stage_w, stage_h), 0)
    ImageDraw.Draw(stage_mask).rounded_rectangle((0, 0, stage_w - 1, stage_h - 1), radius=22, fill=255)

    stage_plates: list[Image.Image] = []
    for p_i, pp in enumerate(plate_paths):
        im_full = Image.open(pp).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
        crop_box = crop_windows[p_i]
        im_stage = im_full.crop(crop_box).resize((stage_w, stage_h), Image.Resampling.LANCZOS)
        stage_plates.append(im_stage)

    fonts = {
        "brand": get_font(20, bold=True),
        "title": get_font(28, bold=True),
        "node_top": get_font(17, bold=True),
        "node_sub": get_font(14, bold=False),
        "pipe_lbl": get_font(16, bold=True),
        "stage_tag": get_font(18, bold=True),
        "badge": get_font(18, bold=True),
        "callout": get_font(29, bold=True),
        "vo": get_font(26, bold=False),
        "vo_bold": get_font(26, bold=True),
        "footer": get_font(20, bold=False),
    }

    precompute_scene_layouts(scene_meta, story_cfg["scenes"], fonts["callout"], fonts["vo"], fonts["vo_bold"], W - 160)

    static_chrome = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sv_draw = ImageDraw.Draw(static_chrome)

    sv_draw.rounded_rectangle(HEADER_BOX, radius=20, fill=(14, 20, 32, 235), outline=(245, 166, 35, 160), width=2)
    sv_draw.text((74, 48), "WHERE MONEY SLEEPS  ·  MẶT CẮT DÒNG TIỀN 5 NGÔI NHÀ", font=fonts["brand"], fill=(245, 166, 35, 255))

    short_title = story["videoScript"]["short"]["title"]
    t_words = short_title.split()
    t_lines: list[str] = []
    cur_t = ""
    for w in t_words:
        test = (cur_t + " " + w).strip()
        if sv_draw.textlength(test, font=fonts["title"]) <= W - 156:
            cur_t = test
        else:
            t_lines.append(cur_t)
            cur_t = w
    if cur_t:
        t_lines.append(cur_t)
    ty = 80
    for ln in t_lines[:2]:
        sv_draw.text((74, ty), ln, font=fonts["title"], fill=(244, 239, 230, 255))
        ty += 36

    assert_parent_child_containment(scene_meta, story_cfg["house_nodes"], fonts)

    sv_draw.rounded_rectangle(CONDUIT_PARENT_BOX, radius=18, fill=(12, 18, 29, 232), outline=(80, 102, 132, 135), width=2)
    sv_draw.text((70, 190), story_cfg["conduit_top"], font=fonts["pipe_lbl"], fill=(245, 166, 35, 220))
    sv_draw.text((70, 322), story_cfg["conduit_bot"], font=fonts["pipe_lbl"], fill=(72, 187, 120, 225))

    sv_draw.rounded_rectangle(STAGE_BOX, radius=22, fill=None, outline=(245, 166, 35, 150), width=2)
    sv_draw.text((64, H - 64), "WHERE MONEY SLEEPS  ·  ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  SỐ LIỆU VÍ DỤ MINH HOẠ CƠ CHẾ", font=fonts["footer"], fill=(165, 175, 190, 210))

    locked_stage_bgs: list[Image.Image] = []
    for sp in stage_plates:
        bg_canvas = Image.new("RGBA", (W, H), (9, 13, 22, 255))
        bg_canvas.paste(sp, (sx0, sy0), stage_mask)
        bg_canvas = Image.alpha_composite(bg_canvas, static_chrome)
        locked_stage_bgs.append(bg_canvas)

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

    TRANS_HALF = 0.48
    t0_wall = time.time()
    black_rgb = Image.new("RGB", (W, H), (10, 14, 23))

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


def run_for_story(wmp, stories: dict, sfx_map: dict[str, bytes], slug: str) -> None:
    story = stories[slug]
    brand_audit = wmp.step_5_0_brand_safety_audit(slug, story)
    print(f"\n=== [{slug.upper()}.SHORT — Broadcast-Grade v4.3 Split-Stage] ===")
    print(f"[0/3 Brand Safety Specialist PASS] B1–B4 sạch ({brand_audit['scenesAudited']} cảnh, 0 tên riêng/thương hiệu)")
    scenes = story["videoScript"]["short"]["scenes"]

    cont_path = CACHE_DIR / f"{slug}_short_continuous_v3.json"
    if not cont_path.is_file():
        raise RuntimeError(f"Missing {cont_path}")
    cont_data = json.loads(cont_path.read_text(encoding="utf-8"))

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
    parser.add_argument("--story", default="install", choices=["install", "card", "pay", "all"])
    args = parser.parse_args()

    wmp = load_pipeline_module()
    wmp.load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing ELEVENLABS_API_KEY")

    stories = wmp.extract_stories((ROOT / "docs/prototype.html").read_text(encoding="utf-8"))
    sfx_map = ensure_sfx_cached(api_key)

    target_slugs = ["card", "pay"] if args.story == "all" else [args.story]
    for slug in target_slugs:
        run_for_story(wmp, stories, sfx_map, slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
