#!/usr/bin/env python3
"""
render_smooth_long_video.py — Bộ dựng Video Dài 16:9 (1920x1080, 30fps, Broadcast-Grade v4.3 Split-Stage)
cho Where Money Sleeps (`install-long-16x9.mp4` — 11 cảnh, ~8m30s):

1. VOICE & AUDIO CONTINUITY:
   - Sử dụng `install_long_continuous_v3.json` (Giọng Tâm `eleven_v3:JwqRvOqFdGeQNu7UjKjw`)
   - Khoảng thở êm 0.36s giữa 11 cảnh + nền Analog Night-Watch Room Tone (-33 dBFS) + 11 điểm nhấn SFX (-22 dBFS), chuẩn hoá -14 LUFS.

2. 16:9 3-ZONE SPLIT-STAGE (LUẬT 1–8 — Zero Stage Occlusion):
   - ZONE 1 (Top Header & 5-House Conduit Bar, x=40..1880, y=24..242):
     + HEADER_BOX = (40, 24, 1880, 102)
     + CONDUIT_PARENT_BOX = (40, 114, 1880, 242) chứa 5 hộp con (HOUSE_BW=280, HOUSE_BH=36, HOUSE_GAP=80, lề trong ngang 60px, dọc 12px).
   - ZONE 2 (Left Visual & Live 30fps Animation Stage, STAGE_BOX = (40, 256, 980, 1016), 940x760px):
     + Hiển thị trọn vẹn mặt cắt kiến trúc + chuyển động hạt 30fps, bút toán TT 99/2025, thanh 12 kỳ trả góp, công thức EIR.
   - ZONE 3 (Right Script & Equation Dock, CARD_BOX = (1000, 256, 1880, 1016), 880x760px):
     + Tách biệt hoàn toàn bên phải STAGE_BOX (khoảng cách ngang 20px, chồng lấn 0px), hiển thị toàn bộ lời bình của cảnh + tô sáng từng từ.
"""

from __future__ import annotations

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

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path("/Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps")
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


def load_cached_sfx() -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for key in ("sfx_lamp_switch", "sfx_wire_pulse", "sfx_pipe_flow", "sfx_clock_tick", "sfx_scale_chime", "sfx_shutter_close"):
        cfile = CACHE_DIR / f"{key}.json"
        if cfile.is_file():
            data = json.loads(cfile.read_text(encoding="utf-8"))
            out[key] = base64.b64decode(data["audio_base64"])
    return out


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
    LEAD_IN = 0.30
    TAIL_OUT = 1.00

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

    sfx_cycle = ["sfx_lamp_switch", "sfx_wire_pulse", "sfx_wire_pulse", "sfx_clock_tick", "sfx_pipe_flow", "sfx_clock_tick", "sfx_scale_chime", "sfx_scale_chime", "sfx_wire_pulse", "sfx_clock_tick", "sfx_shutter_close"]
    for idx, sm in enumerate(scene_meta):
        sfx_key = sfx_cycle[idx % len(sfx_cycle)]
        cue_t = 0.05 if idx == 0 else sm["win_t0"] - 0.35
        if sfx_key in sfx_map:
            s_mp3 = tmp_dir / f"{sfx_key}_{idx}.mp3"
            s_wav = tmp_dir / f"{sfx_key}_{idx}.wav"
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
            start_idx = max(0, int(cue_t * sr))
            end_idx = min(len(mix_pcm), start_idx + len(s_pcm))
            if end_idx > start_idx:
                mix_pcm[start_idx:end_idx] += s_pcm[: end_idx - start_idx] * 0.08

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


# ── CẤU HÌNH 11 CẢNH BÀI DÀI `install` (1920x1080 Split-Stage) ──────────────

HOUSE_NODES = [
    ("BẠN", "Người mua"),
    ("CỬA HÀNG", "Nơi bán máy"),
    ("CÔNG TY", "Tài chính"),
    ("NGÂN HÀNG", "Của bạn"),
    ("NGÂN HÀNG", "Cửa hàng"),
]

LONG_SCENE_CONFIG = [
    # (plate_idx, active_set, flow_spec, kicker, headline, stage_top_pill, stage_bot_pill)
    (
        0,
        {0, 1},
        ("wire", 0, 1),
        "MỞ ĐẦU  ·  BÀI TOÁN 12 TRIỆU TRẢ GÓP 0%",
        "Mua máy 12.000.000 đ  ·  12 kỳ × 1.000.000 đ  ·  Ai trả 600.000 đ tiền lãi?",
        "MÁY 12.000.000 Đ  ·  TỜ RƠI GHI 0% TRONG 12 KỲ",
        "CÂU HỎI TRUNG TÂM: AI TRẢ 600.000 Đ TIỀN LÃI SAU QUẦY?",
    ),
    (
        0,
        {0, 1, 2},
        ("wire", 1, 2),
        "BƯỚC 1  ·  GỬI HỒ SƠ ĐIỆN TỬ TẠI QUẦY",
        "Hồ sơ trả góp gửi thẳng về Công ty tài chính  ·  Chưa có đồng tiền nào chạy",
        "LUỒNG THÔNG TIN XÉT DUYỆT: 0 ĐỒNG TIỀN MẶT",
        "ĐIỂM ĐẾN CỦA HỒ SƠ: CÔNG TY TÀI CHÍNH Ở CUỐI PHỐ",
    ),
    (
        1,
        {0, 1, 2},
        ("wire", 2, 1, 0, 2),
        "BƯỚC 2  ·  XÁC LẬP HỢP ĐỒNG TÍN DỤNG",
        "Bạn ký nhận nợ 12.000.000 đ với Công ty tài chính, không phải Cửa hàng",
        "CÔNG TY TÀI CHÍNH: CHỦ NỢ HỢP PHÁP CỦA BẠN",
        "CỬA HÀNG CHỈ BÁN MÁY  ·  RỦI RO ĐÒI NỢ THUỘC CÔNG TY TÀI CHÍNH",
    ),
    (
        1,
        {1, 2},
        ("none",),
        "BƯỚC 3  ·  ĐÊM ĐẦU TIÊN TRONG SỔ KẾ TOÁN",
        "Bút toán tại Cửa hàng: Debit 1388 / Credit 511 — 12.000.000 đ (Phải thu khác)",
        "SỔ CỬA HÀNG (TT 99/2025): DEBIT 1388 / CREDIT 511 — 12.000.000 Đ",
        "KÉT TIỀN TRỐNG: TIỀN MUA MÁY ĐANG NGỦ TRONG MỘT DÒNG SỔ",
    ),
    (
        2,
        {1, 2, 4},
        ("pipe", 2, 4, 1),
        "BƯỚC 4  ·  GIẢI NGÂN HỤT 600.000 Đ (T+1)",
        "12.000.000 đ − 600.000 đ (hỗ trợ lãi suất 5%) = 11.400.000 đ thực nhận",
        "CỬA HÀNG THỰC NHẬN: +11.400.000 Đ VÀO TÀI KHOẢN NGÂN HÀNG",
        "KHOẢN HỤT 600.000 Đ (5%): CHI PHÍ HỖ TRỢ LÃI SUẤT CỬA HÀNG CHỊU",
    ),
    (
        2,
        {0, 2, 3},
        ("pipe", 0, 3, 2),
        "BƯỚC 5  ·  MƯỜI HAI KỲ TRẢ ĐỀU 1.000.000 Đ",
        "12 tháng × 1.000.000 đ = 12.000.000 đ cho món hàng giá trả thẳng 11.400.000 đ",
        "UỶ QUYỀN TRÍCH NỢ: 1.000.000 Đ / THÁNG × 12 KỲ = 12.000.000 Đ",
        "CHÊNH LỆCH 600.000 Đ LÀM ĐÚNG NHIỆM VỤ CỦA TIỀN LÃI",
    ),
    (
        2,
        {0, 2, 3},
        ("pipe", 0, 3, 2),
        "BƯỚC 6  ·  QUY ĐỔI LÃI SUẤT THỰC TẾ (EIR / IRR)",
        "11.400.000 = Σ 1.000.000 / (1 + r)^t  —  EIR ~0,8%/tháng (~10%/năm)",
        "CÔNG THỨC CHIẾT KHẤU DÒNG TIỀN: r ≈ 0,80%/THÁNG (~10,0%/NĂM)",
        "NẾU ĐÓNG KỲ ĐẦU NGAY LÚC MUA: EIR TĂNG LÊN ~0,95%/THÁNG (~12%/NĂM)",
    ),
    (
        3,
        {1, 2},
        ("none",),
        "BƯỚC 7  ·  AI THẬT SỰ TRẢ 600.000 Đ?",
        "Trả thẳng rẻ hơn: bạn trả lãi  ·  Một giá chung: cửa hàng hoặc mọi người mua trả",
        "QUẸT THẺ THƯỜNG (MDR 2,2%): MẤT 264.000 Đ  vs  TRẢ GÓP 0%: 600.000 Đ",
        "NẾU MỘT GIÁ CHUNG: NGƯỜI MUA TRẢ THẲNG CŨNG GÓP PHẦN LÃI NÀY",
    ),
    (
        3,
        {0, 3},
        ("wire", 0, 3),
        "BƯỚC 8  ·  SO SÁNH TRẢ GÓP 0% QUA THẺ TÍN DỤNG",
        "Phí chuyển đổi 3% (360.000 đ)  —  EIR ~5,8%/năm (hoặc ~17%/năm nếu mất giảm giá)",
        "TRẢ GÓP QUA THẺ TÍN DỤNG: CHỦ NỢ LÀ NGÂN HÀNG PHÁT HÀNH THẺ",
        "PHÍ CHUYỂN ĐỔI 3% = 360.000 Đ  ·  EIR ~0,47%/THÁNG (~5,8%/NĂM)",
    ),
    (
        2,
        {0, 1, 2, 3, 4},
        ("pipe", 0, 3, 2),
        "BƯỚC 9  ·  KHI KẾ HOẠCH LỆCH: TẤT TOÁN SỚM & TRỄ HẠN",
        "Trả hết tháng 4: dư nợ 8.000.000 đ (EIR ~1,48%/tháng)  ·  Trễ kỳ 5: phạt 150.000 đ",
        "TẤT TOÁN SỚM THÁNG 4: KHÔNG ĐƯỢC GIẢM 600.000 Đ ĐÃ KHẤU TRỪ ĐẦU KỲ",
        "TRẢ LẠI MÁY: CỬA HÀNG KHÔNG TỰ XOÁ ĐƯỢC HỢP ĐỒNG VAY",
    ),
    (
        3,
        {0, 1, 2, 3, 4},
        ("none",),
        "KẾT LUẬN  ·  TIỀN LÃI CHỈ ĐỔI CHỖ ĐỨNG",
        "12.000.000 đ vs 11.400.000 đ  —  Luôn hỏi: Trả thẳng thì giá bao nhiêu?",
        "12.000.000 Đ (GHI BÁN)  −  11.400.000 Đ (THỰC NHẬN)  =  600.000 Đ TIỀN LÃI",
        "CÂU HỎI DUY NHẤT TRƯỚC KHI KÝ: “TRẢ THẲNG THÌ GIÁ BAO NHIÊU?”",
    ),
]

SLATE_LEAK_RE = re.compile(
    r"(\bCẢNH\s*\d|\bSCENE\s*\d|\bMỐC\s*\d|\bÝ\s*\d+\s*/\s*\d+|\bKỲ\s*\d+\s*/\s*\d+|Chữ\s+to|SFX\s*gợi\s*ý|dây\s+điện|dây\s+tín\s+hiệu|ống\s+ngầm|ống\s+quyết\s+toán|[→⇒➜➔←↔])",
    re.IGNORECASE,
)

NUMBER_RE = re.compile(
    r"(\b(?:mười|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|không|trăm|nghìn|triệu|tỷ|phần|trăm|phẩy|kỳ|tháng)\b|\d+[.,]?\d*%?)",
    re.IGNORECASE,
)

# Bất biến Hình học 16:9 (1920x1080) — LUẬT 6b & LUẬT 8 (3 Vùng Không Chồng Lấn)
HEADER_BOX = (40, 20, 1880, 96)
CONDUIT_PARENT_BOX = (40, 108, 1880, 236)
HOUSE_BW = 280
HOUSE_BH = 36
HOUSE_GAP = 80
# 5 * 280 + 4 * 80 = 1720px trong khung cha 1840px (40..1880) -> lề trong 60px mỗi bên (100..1820)
HOUSE_XS = [100 + HOUSE_BW // 2 + i * (HOUSE_BW + HOUSE_GAP) for i in range(5)]  # [240, 600, 960, 1320, 1680]
WIRE_Y = 142
NODE_Y = 172
PIPE_Y = 202

# ZONE 2 (Sân khấu Mặt cắt Trái) & ZONE 3 (Khung Script Phải) — Cách nhau 20px, 0px chồng lấn!
STAGE_BOX = (40, 250, 980, 1018)
CARD_BOX = (1000, 250, 1880, 1018)

PLATE_CROP_WINDOWS = [
    (0, 380, 1080, 1380),
    (0, 380, 1080, 1380),
    (0, 380, 1080, 1380),
    (0, 820, 1080, 1820),
]


def assert_broadcast_overlay_clean(texts: list[str]) -> None:
    for txt in texts:
        m = SLATE_LEAK_RE.search(str(txt or ""))
        if m:
            raise RuntimeError(
                f"FAIL [B4 Broadcast Polish]: Lộ nhãn kịch bản nội bộ '{m.group(0)}' trong chuỗi hiển thị: {txt!r}"
            )


def precompute_scene_layouts(
    scene_meta: list[dict],
    f_callout: ImageFont.FreeTypeFont,
    f_vo: ImageFont.FreeTypeFont,
    f_vo_bold: ImageFont.FreeTypeFont,
    max_w: int,
) -> None:
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))
    space_w = max(8.5, dummy.textlength(" ", font=f_vo_bold) + 2.0)
    line_h = 29
    phrase_gap = 5

    overlay_audit_strings: list[str] = []

    for s_idx, sm in enumerate(scene_meta):
        _, _, _, kicker, headline, top_pill, bot_pill = LONG_SCENE_CONFIG[s_idx]
        overlay_audit_strings.extend([kicker, headline, top_pill, bot_pill])
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
                rx = 18.0
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


def assert_parent_child_containment(
    scene_meta: list[dict],
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))

    # Kiểm chứng LUẬT 8 trên khung 16:9: Zone 1 ở trên, Zone 2 (Trái) và Zone 3 (Phải) tách biệt hoàn toàn
    if not (
        HEADER_BOX[3] + 10 <= CONDUIT_PARENT_BOX[1]
        and CONDUIT_PARENT_BOX[3] + 12 <= STAGE_BOX[1]
        and CONDUIT_PARENT_BOX[3] + 12 <= CARD_BOX[1]
        and STAGE_BOX[2] + 16 <= CARD_BOX[0]
    ):
        raise RuntimeError(
            f"FAIL [LUẬT 8 16:9 Zone Overlap]: Các vùng giao diện chồng lấn nhau: "
            f"Header={HEADER_BOX}, Conduit={CONDUIT_PARENT_BOX}, Stage={STAGE_BOX}, Card={CARD_BOX}"
        )

    px0, py0, px1, py1 = CONDUIT_PARENT_BOX
    for i, hx in enumerate(HOUSE_XS):
        cx0 = hx - HOUSE_BW // 2
        cx1 = hx + HOUSE_BW // 2
        cy0 = NODE_Y - HOUSE_BH // 2
        cy1 = NODE_Y + HOUSE_BH // 2
        if cx0 < px0 + 20 or cx1 > px1 - 20:
            raise RuntimeError(f"FAIL [B4 Box Containment]: Hộp con thứ {i} tràn ngang khung cha")
        if cy0 < WIRE_Y + 10 or cy1 > PIPE_Y - 10:
            raise RuntimeError(f"FAIL [B4 Box Containment]: Hộp con thứ {i} tràn dọc vào đường luồng")

    card_x0, card_top, card_x1, card_bot = CARD_BOX
    for s_idx, sm in enumerate(scene_meta):
        kicker_w = int(dummy.textlength(sm["kicker"], font=fonts["badge"])) + 32
        if card_x0 + 28 + kicker_w > card_x1 - 20:
            raise RuntimeError(f"FAIL [B4 Box Containment]: Kicker cảnh {s_idx} tràn ngang khung Card")
        cy = card_top + 68
        for ln in sm["callout_lines"]:
            lw = dummy.textlength(ln, font=fonts["callout"])
            if card_x0 + 28 + lw > card_x1 - 20:
                raise RuntimeError(f"FAIL [B4 Box Containment]: Callout cảnh {s_idx} tràn ngang khung Card")
            cy += 30
        div_y = cy + 6
        base_wx = card_x0 + 28
        base_wy = div_y + 10
        for phr in sm["phrases"]:
            for pw in phr["placed_words"]:
                wx1 = base_wx + pw["rx"] + pw["w"] + 5
                wy1 = base_wy + pw["ry"] + 24
                if wx1 > card_x1 - 18:
                    raise RuntimeError(
                        f"FAIL [B4 Box Containment]: Từ '{pw['word']}' ở cảnh {s_idx} tràn ngang khung Card ({wx1:.1f} > {card_x1 - 18})"
                    )
                if wy1 > card_bot - 12:
                    raise RuntimeError(
                        f"FAIL [B4 Box Containment]: Từ '{pw['word']}' ở cảnh {s_idx} tràn đáy khung Card ({wy1:.1f} > {card_bot - 12})"
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
    pw = tw + 26
    ph = 34
    x0 = max(STAGE_BOX[0] + 16, min(STAGE_BOX[2] - 16 - pw, cx - pw / 2))
    y0 = max(STAGE_BOX[1] + 14, min(STAGE_BOX[3] - 14 - ph, cy - ph / 2))
    draw.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=9, fill=fill_rgba, outline=outline_rgba, width=2)
    draw.text((x0 + 13, y0 + 7), text, font=font, fill=text_rgba)


def draw_stage_live_animation_long(
    draw: ImageDraw.ImageDraw,
    s_idx: int,
    t: float,
    s_prog: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    f_tag = fonts["stage_tag"]
    sx0, sy0, sx1, sy1 = STAGE_BOX
    cx_mid = (sx0 + sx1) / 2.0

    _, _, _, _, _, top_pill, bot_pill = LONG_SCENE_CONFIG[s_idx]

    # Vẽ hạt chuyển động 30fps trên mặt cắt kiến trúc (tọa độ quy đổi trong STAGE_BOX 940x760)
    if s_idx in (0, 1):
        p0, p1 = (sx0 + 360, sy0 + 490), (sx0 + 450, sy0 + 195)
        for off in (0.0, 0.33, 0.66):
            u = smoothstep(0.0, 1.0, (t * 0.55 + off) % 1.0)
            px, py = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
            draw.ellipse((px - 10, py - 10, px + 10, py + 10), fill=(245, 166, 35, 115))
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(255, 230, 150, 255))
    elif s_idx in (2, 3, 8):
        p0, p1 = (sx0 + 360, sy0 + 495), (sx0 + 600, sy0 + 260)
        for off in (0.0, 0.33, 0.66):
            u = smoothstep(0.0, 1.0, (t * 0.60 + off) % 1.0)
            px, py = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
            draw.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(245, 166, 35, 115))
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(255, 236, 160, 255))
    elif s_idx in (4, 9):
        p_vault, p_shop, p_fee = (sx0 + 580, sy0 + 230), (sx0 + 335, sy0 + 540), (sx0 + 510, sy0 + 505)
        for off in (0.0, 0.33, 0.66):
            u = smoothstep(0.0, 1.0, (t * 0.62 + off) % 1.0)
            px, py = lerp(p_vault[0], p_shop[0], u), lerp(p_vault[1], p_shop[1], u)
            draw.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(72, 187, 120, 120))
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(154, 240, 180, 255))
        u_f = smoothstep(0.0, 1.0, (t * 0.55) % 1.0)
        fx, fy = lerp(p_vault[0], p_fee[0], u_f), lerp(p_vault[1], p_fee[1], u_f)
        draw.ellipse((fx - 10, fy - 10, fx + 10, fy + 10), fill=(245, 166, 35, 130))
        draw.ellipse((fx - 5, fy - 5, fx + 5, fy + 5), fill=(255, 215, 110, 255))
    elif s_idx in (5, 6):
        bar_x0, bar_y0, bar_x1, bar_y1 = sx0 + 24, sy0 + 62, sx1 - 24, sy0 + 114
        draw.rounded_rectangle((bar_x0, bar_y0, bar_x1, bar_y1), radius=10, fill=(14, 20, 32, 232), outline=(245, 166, 35, 210), width=2)
        active_months = min(12, max(1, int(s_prog * 13.0)))
        cell_w = (bar_x1 - bar_x0 - 20) / 12.0
        for m_i in range(12):
            cx0 = bar_x0 + 10 + m_i * cell_w + 2
            cx1 = cx0 + cell_w - 4
            is_paid = m_i < active_months
            c_fill = (72, 187, 120, 235) if is_paid else (38, 50, 72, 190)
            draw.rounded_rectangle((cx0, bar_y0 + 10, cx1, bar_y1 - 10), radius=5, fill=c_fill)
            m_lbl = f"T{m_i+1}"
            mw = draw.textlength(m_lbl, font=fonts["node_sub"])
            draw.text(((cx0 + cx1 - mw) / 2, bar_y0 + 17), m_lbl, font=fonts["node_sub"], fill=(12, 18, 28, 255) if is_paid else (175, 188, 205, 220))

    draw_stage_pill(draw, cx_mid, sy0 + 34, top_pill, f_tag, (14, 20, 32, 236), (245, 166, 35, 235), (255, 209, 102, 255))
    draw_stage_pill(draw, cx_mid, sy1 - 34, bot_pill, f_tag, (14, 20, 32, 236), (72, 187, 120, 235), (154, 240, 180, 255))


def render_single_scene_frame(
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

    p_idx, active_set, flow_spec, kicker, _, _, _ = LONG_SCENE_CONFIG[s_idx]
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
    draw.line([(house_xs[0], pipe_y), (house_xs[-1], pipe_y)], fill=(72, 187, 120, 135), width=4)

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
            draw.ellipse((px - 9, y_line - 9, px + 9, y_line + 9), fill=outer_c)
            draw.ellipse((px - 4, y_line - 4, px + 4, y_line + 4), fill=inner_c)

    for i, hx in enumerate(house_xs):
        is_act = i in active_set
        fill_col = (245, 166, 35, 248) if is_act else (22, 31, 46, 215)
        out_col = (255, 224, 140, 255) if is_act else (90, 108, 135, 210)
        top_col = (14, 20, 32, 255) if is_act else (232, 238, 246, 245)
        sub_col = (28, 38, 56, 240) if is_act else (164, 178, 198, 225)
        bw, bh = HOUSE_BW, HOUSE_BH
        draw.rounded_rectangle(
            (hx - bw // 2, node_y - bh // 2, hx + bw // 2, node_y + bh // 2),
            radius=10,
            fill=fill_col,
            outline=out_col,
            width=2,
        )
        line1, line2 = HOUSE_NODES[i]
        combined = f"{line1} · {line2}"
        tw = draw.textlength(combined, font=f_node_top)
        draw.text((hx - tw / 2, node_y - 10), combined, font=f_node_top, fill=top_col if is_act else (232, 238, 246, 245))

    draw_stage_live_animation_long(draw, s_idx, t, s_prog, fonts)

    card_x0, card_top, card_x1, card_bot = CARD_BOX
    draw.rounded_rectangle(
        (card_x0, card_top, card_x1, card_bot),
        radius=22,
        fill=(12, 18, 30, 242),
        outline=(245, 166, 35, 215),
        width=3,
    )

    n_scenes = len(scene_meta)
    seg_total_w = (card_x1 - card_x0) - 56
    seg_gap = 6
    seg_w = (seg_total_w - seg_gap * (n_scenes - 1)) / float(n_scenes)
    for s_i in range(n_scenes):
        sx0 = card_x0 + 28 + s_i * (seg_w + seg_gap)
        sx1 = sx0 + seg_w
        if s_i < s_idx:
            draw.rounded_rectangle((sx0, card_top + 14, sx1, card_top + 19), radius=2, fill=(245, 166, 35, 235))
        elif s_i == s_idx:
            draw.rounded_rectangle((sx0, card_top + 14, sx1, card_top + 19), radius=2, fill=(65, 80, 105, 180))
            fill_x = sx0 + seg_w * s_prog
            draw.rounded_rectangle((sx0, card_top + 14, max(sx0 + 6, fill_x), card_top + 19), radius=2, fill=(255, 209, 102, 255))
        else:
            draw.rounded_rectangle((sx0, card_top + 14, sx1, card_top + 19), radius=2, fill=(65, 80, 105, 145))

    phrases = sm["phrases"]
    active_p_float = 0.0
    active_p_idx = 0
    for p_i, phr in enumerate(phrases):
        if t >= phr["t0"] - 0.25:
            active_p_idx = p_i
            trans_w = smoothstep(phr["t0"] - 0.25, phr["t0"] + 0.12, t) if p_i > 0 else 1.0
            active_p_float = (p_i - 1) + trans_w if p_i > 0 else 0.0

    kicker_w = int(draw.textlength(kicker, font=f_badge)) + 32
    draw.rounded_rectangle((card_x0 + 28, card_top + 28, card_x0 + 28 + kicker_w, card_top + 60), radius=8, fill=(245, 166, 35, 245))
    draw.text((card_x0 + 44, card_top + 35), kicker, font=f_badge, fill=(14, 20, 32, 255))

    cy = card_top + 68
    for ln in sm["callout_lines"]:
        draw.text((card_x0 + 28, cy), ln, font=f_callout, fill=(255, 209, 102, 255))
        cy += 30

    div_y = cy + 6
    draw.line([(card_x0 + 28, div_y), (card_x1 - 28, div_y)], fill=(245, 166, 35, 110), width=2)

    base_wx = card_x0 + 28
    base_wy = div_y + 10

    p_low = int(math.floor(active_p_float))
    p_high = min(len(phrases) - 1, p_low + 1)
    p_frac = active_p_float - p_low
    bar_y0 = base_wy + lerp(phrases[p_low]["y0"], phrases[p_high]["y0"], p_frac)
    bar_y1 = base_wy + lerp(phrases[p_low]["y1"], phrases[p_high]["y1"], p_frac) - 4
    draw.rounded_rectangle((base_wx, bar_y0 + 2, base_wx + 5, max(bar_y0 + 12, bar_y1)), radius=2, fill=(255, 209, 102, 255))

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
                pad_x, pad_y = 4, 2
                pill_alpha = int(68 * w_act)
                draw.rounded_rectangle(
                    (wx - pad_x, wy - pad_y, wx + ww + pad_x, wy + 23 + pad_y),
                    radius=6,
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


def render_smooth_long_video(
    story: dict,
    scene_meta: list[dict],
    total_dur: float,
    master_wav: pathlib.Path,
    out_mp4: pathlib.Path,
) -> None:
    W, H = 1920, 1080
    FPS = 30
    total_frames = int(round(total_dur * FPS))

    plate_paths = [
        ROOT / "public/brand/install-short-plate-1.jpg",
        ROOT / "public/brand/install-short-plate-2.jpg",
        ROOT / "public/brand/install-short-plate-3.jpg",
        ROOT / "public/brand/install-short-plate-4.jpg",
    ]
    sx0, sy0, sx1, sy1 = STAGE_BOX
    stage_w, stage_h = sx1 - sx0, sy1 - sy0

    stage_mask = Image.new("L", (stage_w, stage_h), 0)
    ImageDraw.Draw(stage_mask).rounded_rectangle((0, 0, stage_w - 1, stage_h - 1), radius=22, fill=255)

    stage_plates: list[Image.Image] = []
    for p_i, pp in enumerate(plate_paths):
        im_full = Image.open(pp).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
        crop_box = PLATE_CROP_WINDOWS[p_i]
        im_stage = im_full.crop(crop_box).resize((stage_w, stage_h), Image.Resampling.LANCZOS)
        stage_plates.append(im_stage)

    fonts = {
        "brand": get_font(17, bold=True),
        "title": get_font(25, bold=True),
        "node_top": get_font(15, bold=True),
        "node_sub": get_font(13, bold=False),
        "pipe_lbl": get_font(14, bold=True),
        "stage_tag": get_font(16, bold=True),
        "badge": get_font(16, bold=True),
        "callout": get_font(22, bold=True),
        "vo": get_font(20, bold=False),
        "vo_bold": get_font(20, bold=True),
        "footer": get_font(17, bold=False),
    }

    card_inner_w = (CARD_BOX[2] - CARD_BOX[0]) - 56
    precompute_scene_layouts(scene_meta, fonts["callout"], fonts["vo"], fonts["vo_bold"], card_inner_w)
    assert_parent_child_containment(scene_meta, fonts)

    static_chrome = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sv_draw = ImageDraw.Draw(static_chrome)

    sv_draw.rounded_rectangle(HEADER_BOX, radius=16, fill=(14, 20, 32, 235), outline=(245, 166, 35, 160), width=2)
    sv_draw.text((64, 30), "WHERE MONEY SLEEPS  ·  MẶT CẮT DÒNG TIỀN 5 NGÔI NHÀ (BẢN PHÂN TÍCH ĐẦY ĐỦ)", font=fonts["brand"], fill=(245, 166, 35, 255))
    long_title = story["videoScript"]["long"]["title"]
    sv_draw.text((64, 55), long_title, font=fonts["title"], fill=(244, 239, 230, 255))

    sv_draw.rounded_rectangle(CONDUIT_PARENT_BOX, radius=16, fill=(12, 18, 29, 232), outline=(80, 102, 132, 135), width=2)
    sv_draw.text((64, 115), "LUỒNG HỒ SƠ & HỢP ĐỒNG (CHỈ LÀ THÔNG TIN · 0 ĐỒNG)", font=fonts["pipe_lbl"], fill=(245, 166, 35, 220))
    sv_draw.text((64, 212), "LUỒNG TIỀN GIẢI NGÂN & TRẢ GÓP (TIỀN THẬT QUA NGÂN HÀNG)", font=fonts["pipe_lbl"], fill=(72, 187, 120, 225))

    sv_draw.rounded_rectangle(STAGE_BOX, radius=22, fill=None, outline=(245, 166, 35, 150), width=2)
    sv_draw.text((48, H - 42), "WHERE MONEY SLEEPS  ·  ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  SỐ LIỆU VÍ DỤ MINH HOẠ CƠ CHẾ", font=fonts["footer"], fill=(165, 175, 190, 210))

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
                img_a = render_single_scene_frame(b_idx, t, scene_meta, locked_stage_bgs, fonts, W, H)
                img_b = render_single_scene_frame(b_idx + 1, t, scene_meta, locked_stage_bgs, fonts, W, H)
                blended_rgb = Image.blend(img_a, img_b, alpha)
                break

        if blended_rgb is None:
            cur_s_idx = 0
            for idx, sm in enumerate(scene_meta):
                if sm["win_t0"] <= t <= sm["win_t1"] or idx == len(scene_meta) - 1:
                    cur_s_idx = idx
                    break
            blended_rgb = render_single_scene_frame(cur_s_idx, t, scene_meta, locked_stage_bgs, fonts, W, H)

        if t < 0.35:
            blended_rgb = Image.blend(black_rgb, blended_rgb, smoothstep(0.0, 0.35, t))
        elif t > total_dur - 0.65:
            blended_rgb = Image.blend(blended_rgb, black_rgb, smoothstep(total_dur - 0.65, total_dur, t))

        proc.stdin.write(blended_rgb.tobytes())

        if (f_idx + 1) % 900 == 0 or f_idx == total_frames - 1:
            elapsed = time.time() - t0_wall
            fps_actual = (f_idx + 1) / max(0.01, elapsed)
            print(f"  -> [install.long] Rendered frame {f_idx + 1}/{total_frames} ({t:.1f}s / {total_dur:.1f}s, {fps_actual:.1f} fps)")

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"FFmpeg failed with code {ret}:\n{stderr_out[-1200:]}")


def main() -> int:
    wmp = load_pipeline_module()
    stories = wmp.extract_stories((ROOT / "docs/prototype.html").read_text(encoding="utf-8"))
    story = stories["install"]
    brand_audit = wmp.step_5_0_brand_safety_audit("install", story)
    print(f"=== [INSTALL.LONG 16:9 — Broadcast-Grade v4.3 Split-Stage] ===")
    print(f"[0/3 Brand Safety Specialist PASS] B1–B4 sạch ({brand_audit['scenesAudited']} cảnh, 0 tên riêng/thương hiệu)")
    scenes = story["videoScript"]["long"]["scenes"]

    cont_path = CACHE_DIR / "install_long_continuous_v3.json"
    if not cont_path.is_file():
        raise RuntimeError(f"Missing {cont_path}")
    cont_data = json.loads(cont_path.read_text(encoding="utf-8"))
    sfx_map = load_cached_sfx()

    with tempfile.TemporaryDirectory(prefix="wms_smooth_long_") as tmp:
        tmp_dir = pathlib.Path(tmp)
        master_wav, scene_meta, total_dur = build_timeline_and_master_audio(scenes, cont_data, sfx_map, tmp_dir)
        print(f"  -> Master audio ready: {total_dur:.2f}s (-14 LUFS, 11 scenes)")
        out_mp4 = DIST_DIR / "install-long-16x9.mp4"
        print(f"[2/3] Rendering 30fps 16:9 video ({int(round(total_dur * 30))} frames) -> {out_mp4} ...")
        render_smooth_long_video(story, scene_meta, total_dur, master_wav, out_mp4)

    print(f"[3/3] Done! Output saved to {out_mp4} ({out_mp4.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
