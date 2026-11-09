#!/usr/bin/env python3
"""
wms-render-long-v43.py — Bộ dựng Video Dài 16:9 Chuẩn Điện Ảnh & Khoa Học Nhận Thức v5.0 (QĐ 61)
cho Where Money Sleeps (`install-long-16x9.mp4`, `card-long-16x9.mp4`, `pay-long-16x9.mp4` — 1920x1080, 30fps):

1. KIẾN TRÚC BỐ CỤC SAFE-ZONE YOUTUBE 16:9 NGHIÊM NGẶT (QĐ 61 · F2 · LUẬT 6b · LUẬT 8 · LUẬT 10):
   - Khung an toàn: `SAFE_X = (64, 1856)` (rộng 1792px) và `SAFE_Y = (44, 828)` (cao 784px).
   - Chừa trống hoàn toàn dải đáy `y = 830..1080` (250px) cho phụ đề `[CC]` của YouTube (`y = 850..960`)
     và thanh tua / điều khiển Player (`y = 960..1080`) -> 0% chữ hay đồ thị bị đè!
   - Xoá hoàn toàn bức tường chữ Karaoke 180–329 từ ở nửa phải (tránh hiệu ứng dư thừa Mayer 2021).
   - Thanh định chế trên cùng: `ACTIVE_ACTOR_BAR = (64, 44, 1856, 124)` (1792x80px) hiển thị thanh tiến độ
     11–12 cảnh + 5 định chế với đèn chiếu sáng chủ thể đang tương tác + hạt xung chạy giữa chúng.

2. BA CHẾ ĐỘ SÂN KHẤU ĐỘNG (`Mode L-A`, `Mode L-B`, `Mode L-C`) & XÂY DỰNG TUẦN TỰ 4 NHỊP (`Beat 1..4`):
   - `Mode L-A` (`Full-Stage Cinema`, cho cảnh Mở đầu, Chuyển cảnh thế giới và Kết luận):
     + Trái (`64..1124`, 1060x688px): Mặt cắt kiến trúc Risograph 16:9 sắc nét + hạt 30fps + 1 nhãn neo không gian.
     + Phải (`1148..1856`, 708x688px): 4 thẻ tiêu điểm xuất hiện tuần tự theo 4 câu giọng đọc (`Beat 1..4`).
   - `Mode L-B` (`Asymmetric 55/45 Cutaway + 4-Beat Progressive Ledger & Mechanism Canvas`):
     + Trái (`CUTAWAY_STAGE_BOX = (64, 140, 1020, 828)`, 956x688px): Mặt cắt cận cảnh riêng biệt (`F1`).
     + Phải (`MECHANISM_CANVAS_BOX = (1044, 140, 1856, 828)`, 812x688px): Xây dựng tuần tự 4 nhịp
       (`Beat 1: Quy mô gốc` -> `Beat 2: Nguyên hàm P1/P2/P3` -> `Beat 3: Sổ cái kép T-Account TT 99/2025 P4`
       -> `Beat 4: Quy tắc chốt`).
   - `Mode L-C` (`Full-Width Analytical Stage`, `(64, 140, 1856, 828)`, 1792x688px):
     + Sân khấu phân tích định lượng toàn chiều ngang cho `P5` (Đường cong chiết khấu dòng tiền 12 kỳ & EIR),
       `P6` (Lưới CASA & Cột 1:50), `P7` (So sánh song song 2 thế giới), và `P9` (Triptych 3 tình huống ngoại lệ).
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
import wave

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

    sfx_cycle = [
        "sfx_lamp_switch",
        "sfx_wire_pulse",
        "sfx_wire_pulse",
        "sfx_clock_tick",
        "sfx_pipe_flow",
        "sfx_clock_tick",
        "sfx_scale_chime",
        "sfx_scale_chime",
        "sfx_wire_pulse",
        "sfx_clock_tick",
        "sfx_shutter_close",
        "sfx_shutter_close",
    ]
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


# ── HÌNH HỌC SAFE-ZONE YOUTUBE 16:9 (1920x1080) — QĐ 61 · LUẬT 6b · LUẬT 8 · LUẬT 10 ──
# Chừa hoàn toàn dải đáy y = 890..1080 (190px) cho phụ đề [CC] YouTube và thanh tua Player!
SAFE_X = (64, 1856)
SAFE_Y = (36, 884)

ACTIVE_ACTOR_BAR = (64, 36, 1856, 132)       # 1792 x 96 px (Thanh tiến độ + 5 định chế 2 dòng rõ nét)
HOUSE_BW = 280
HOUSE_BH = 56
HOUSE_GAP = 72
# 5 * 280 + 4 * 72 = 1688px trong khung 1792px -> lề trong 52px mỗi bên (116..1804)
HOUSE_XS = [116 + HOUSE_BW // 2 + i * (HOUSE_BW + HOUSE_GAP) for i in range(5)]
NODE_Y = 92

# Mode L-A (Full-Stage Cinema: 896px Trái Mặt cắt tỉ lệ 1.22:1 + 872px Phải 4 Thẻ Nhịp)
LA_STAGE_BOX = (64, 148, 960, 884)            # 896 x 736 px (khớp tỉ lệ gốc 1040x845 = 1.23:1, 0 méo hình)
LA_BEATS_BOX = (984, 148, 1856, 884)          # 872 x 736 px (rộng rãi cho 4 thẻ nhịp)

# Mode L-B (Cutaway 896px + 4-Beat Progressive Ledger & Mechanism Canvas 872px)
CUTAWAY_STAGE_BOX = (64, 148, 960, 884)       # 896 x 736 px
MECHANISM_CANVAS_BOX = (984, 148, 1856, 884)  # 872 x 736 px

# Mode L-C (Full-Width Analytical Stage: 1792 x 736 px)
LC_FULL_BOX = (64, 148, 1856, 884)           # 1792 x 736 px

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


# ── CẤU HÌNH BÀI DÀI 16:9 (`install`, `card`, `pay`) ─────────────────────────

LONG_STORY_CONFIGS: dict[str, dict] = {
    "install": {
        "house_nodes": [
            ("BẠN", "Người mua"),
            ("CỬA HÀNG", "Nơi bán máy"),
            ("CÔNG TY", "Tài chính"),
            ("NGÂN HÀNG", "Của bạn"),
            ("NGÂN HÀNG", "Cửa hàng"),
        ],
        "plates_pool": [
            ("public/brand/install-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-1.jpg", (40, 430, 1040, 1255)),
            ("public/brand/install-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-2.jpg", (40, 430, 1040, 1255)),
            ("public/brand/install-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-3.jpg", (40, 430, 1040, 1255)),
            ("public/brand/install-short-plate-4.jpg", (20, 780, 1060, 1625)),
            ("public/brand/install-short-plate-4.jpg", (40, 790, 1040, 1615)),
        ],
        "scenes": [
            # 0: Mode L-A (Mở đầu)
            {
                "mode": "L-A",
                "plate_idx": 0,
                "active": {0, 1},
                "flow": ("wire", 0, 1),
                "kicker": "MỞ ĐẦU  ·  BÀI TOÁN 12 TRIỆU TRẢ GÓP 0%",
                "stage_tag": "QUẦY BÁN HÀNG  ·  MÁY NIÊM YẾT 12.000.000 Đ (0% × 12 KỲ)",
                "beats": [
                    ("1. GIÁ NIÊM YẾT TẠI QUẦY", "12.000.000 đ  ·  Chia đều 12 tháng × 1.000.000 đ"),
                    ("2. LỜI HỨA TRÊN TỜ RƠI", "Lãi suất ghi trên hợp đồng: 0% / năm"),
                    ("3. SỰ THẬT TẠI KÉT CỬA HÀNG", "Cửa hàng chỉ thực nhận về: 11.400.000 đ (Hụt 600.000 đ)"),
                    ("4. CÂU HỎI TRUNG TÂM", "600.000 đ chênh lệch đi đâu và ai đang trả khoản này?"),
                ],
                "rule": "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC TRỌN LỜI BÌNH",
            },
            # 1: Mode L-B (Bước 1 - Gửi hồ sơ điện tử)
            {
                "mode": "L-B",
                "plate_idx": 1,
                "active": {0, 1, 2},
                "flow": ("wire", 0, 1, 2),
                "kicker": "BƯỚC 1  ·  GỬI HỒ SƠ ĐIỆN TỬ TẠI QUẦY",
                "stage_tag": "LUỒNG HỒ SƠ XÉT DUYỆT  ·  0 ĐỒNG TIỀN MẶT DI CHUYỂN",
                "scale_title": "GIÁ TRỊ HỒ SƠ VAY ĐƯỢC KHỞI TẠO:",
                "scale_val": 12_000_000,
                "mech_type": "P2_CONTRACT",
                "mech_left": "Cửa hàng (Nơi lập hồ sơ)",
                "mech_right": "Công ty tài chính (Xét duyệt)",
                "mech_badge": "HỒ SƠ VAY 12.000.000 Đ",
                "ledger_title": "TRẠNG THÁI SỔ KẾ TOÁN LÚC CHỜ DUYỆT (T+0):",
                "debit_line": "Chưa phát sinh bút toán thu tiền mặt (Két = 0 đ)",
                "credit_line": "Hồ sơ tín dụng đang định danh bạn với Công ty tài chính",
                "rule": "CỬA HÀNG CHỈ LÀ ĐIỂM TIẾP NHẬN HỒ SƠ, KHÔNG PHẢI NGƯỜI CHO VAY",
            },
            # 2: Mode L-A (Bước 2 - Xác lập hợp đồng tín dụng)
            {
                "mode": "L-A",
                "plate_idx": 2,
                "active": {0, 1, 2},
                "flow": ("wire", 1, 2),
                "kicker": "BƯỚC 2  ·  XÁC LẬP HỢP ĐỒNG TÍN DỤNG",
                "stage_tag": "CHỦ NỢ HỢP PHÁP CỦA BẠN LÀ CÔNG TY TÀI CHÍNH",
                "beats": [
                    ("1. BÊN BÁN HÀNG HÓA", "Cửa hàng giao chiếc máy 12.000.000 đ cho bạn đem về"),
                    ("2. BÊN CHO VAY TIỀN", "Công ty tài chính đứng tên chủ nợ trên hợp đồng 12 kỳ"),
                    ("3. TÁCH BIỆT NGHĨA VỤ", "Dù máy hỏng hay đổi trả, hợp đồng vay vẫn độc lập"),
                    ("4. QUYỀN ĐÒI NỢ 12 THÁNG", "Nằm trọn tại Công ty tài chính ngay khi bạn ký tên"),
                ],
                "rule": "BẠN ĐANG NỢ CÔNG TY TÀI CHÍNH 12.000.000 Đ, KHÔNG NỢ CỬA HÀNG",
            },
            # 3: Mode L-B (Bước 3 - Đêm đầu tiên trong sổ kế toán)
            {
                "mode": "L-B",
                "plate_idx": 3,
                "active": {1, 2},
                "flow": ("none",),
                "kicker": "BƯỚC 3  ·  ĐÊM ĐẦU TIÊN TRONG SỔ KẾ TOÁN",
                "stage_tag": "SỔ KẾ TOÁN CỬA HÀNG (TT 99/2025): GHI NHẬN PHẢI THU KHÁC",
                "scale_title": "DOANH THU GHI NHẬN TRÊN HOÁ ĐƠN:",
                "scale_val": 12_000_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Két tiền mặt / Ngân hàng (TK 111/112):  +0 đ",
                "mech_line2": "Khoản phải thu khác (TK 1388):  +12.000.000 đ",
                "ledger_title": "BÚT TOÁN KÉP TẠI CỬA HÀNG (TT 99/2025/TT-BTC):",
                "debit_line": "Debit 1388 (Phải thu khác): +12.000.000 đ",
                "credit_line": "Credit 511 (Doanh thu bán hàng): +12.000.000 đ",
                "rule": "Σ NỢ (12.000.000 Đ) = Σ CÓ (12.000.000 Đ)  ·  TIỀN ĐANG NGỦ TRONG SỔ",
            },
            # 4: Mode L-B (Bước 4 - Giải ngân hụt 600.000 đ)
            {
                "mode": "L-B",
                "plate_idx": 4,
                "active": {1, 2, 4},
                "flow": ("pipe", 2, 4, 1),
                "kicker": "BƯỚC 4  ·  GIẢI NGÂN HỤT 600.000 Đ (T+1)",
                "stage_tag": "GIẢI NGÂN QUA NGÂN HÀNG  ·  KHẤU TRỪ TẠI NGUỒN 5%",
                "scale_title": "SỐ TIỀN THỰC TẾ CHUYỂN VỀ TÀI KHOẢN CỬA HÀNG:",
                "scale_val": 11_400_000,
                "mech_type": "P1_SPLIT",
                "split_ratio": 0.95,
                "split_left_lbl": "THỰC NHẬN (95%): 11.400.000 Đ",
                "split_right_lbl": "PHÍ 5%: 600K",
                "ledger_title": "BÚT TOÁN TẤT TOÁN CÔNG NỢ (TT 99/2025/TT-BTC):",
                "debit_line": "Debit 112: +11.400.000 đ  ·  Debit 641 (Phí 5%): +600.000 đ",
                "credit_line": "Credit 1388 (Xoá phải thu khác): −12.000.000 đ",
                "rule": "600.000 Đ ĐƯỢC HẠCH TOÁN VÀO CHI PHÍ BÁN HÀNG (TK 641) CỦA CỬA HÀNG",
            },
            # 5: Mode L-C (Bước 5 - 12 kỳ trả đều 1.000.000 đ)
            {
                "mode": "L-C",
                "plate_idx": 5,
                "active": {0, 2, 3},
                "flow": ("pipe", 0, 3, 2),
                "kicker": "BƯỚC 5  ·  LỊCH TRẢ ĐỀU 12 KỲ × 1.000.000 Đ",
                "lc_type": "P5_LADDER_12M",
                "headline": "CÔNG TY TÀI CHÍNH BỎ RA 11.400.000 Đ NGÀY ĐẦU  ·  THU VỀ 12.000.000 Đ QUA 12 THÁNG",
                "sub_left": "Vốn giải ngân thực tế (T+1): 11.400.000 đ",
                "sub_right": "Tổng thu từ người mua (12 kỳ): 12.000.000 đ (+600.000 đ)",
                "rule": "KHOẢN CHÊNH 600.000 Đ LÀ PHẦN BÙ ĐẮP GIÁ TRỊ THỜI GIAN CỦA TIỀN & RỦI RO TÍN DỤNG",
            },
            # 6: Mode L-C (Bước 6 - Quy đổi lãi suất thực tế EIR / IRR)
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 2, 3},
                "flow": ("pipe", 0, 3, 2),
                "kicker": "BƯỚC 6  ·  QUY ĐỔI LÃI SUẤT HIỆU DỤNG (EIR / IRR)",
                "lc_type": "P5_EIR_FORMULA",
                "headline": "PHƯƠNG TRÌNH CHIẾT KHẤU DÒNG TIỀN:  11.400.000 = Σ [ 1.000.000 / (1 + r)^t ]   (t = 1..12)",
                "card1_title": "TRẢ CUỐI MỖI KỲ (ORDINARY ANNUITY)",
                "card1_big": "r ≈ 0,80%/tháng  (EIR ≈ 10,0%/năm)",
                "card1_sub": "Nhận 11,4 triệu hôm nay, trả 1 triệu vào cuối mỗi tháng từ T1 đến T12",
                "card2_title": "ĐÓNG KỲ ĐẦU NGAY LÚC MUA (ANNUITY DUE)",
                "card2_big": "r ≈ 0,95%/tháng  (EIR ≈ 12,0%/năm)",
                "card2_sub": "Vì kỳ đầu trả ngay tại quầy nên vốn vay thực chất chỉ còn 10,4 triệu trong 11 tháng",
                "rule": "LÃI SUẤT DANH NGHĨA 0% NHƯNG CHI PHÍ VỐN NGẦM TƯƠNG ĐƯƠNG ~10% – 12% / NĂM",
            },
            # 7: Mode L-B (Bước 7 - Ai thật sự trả 600.000 đ?)
            {
                "mode": "L-B",
                "plate_idx": 5,
                "active": {0, 1, 2},
                "flow": ("none",),
                "kicker": "BƯỚC 7  ·  AI THẬT SỰ GÁNH 600.000 Đ?",
                "stage_tag": "ĐẶT 2 KỊCH BẢN GIÁ BÁN LÊN BÀN CÂN TẠI QUẦY",
                "scale_title": "CHI PHÍ HỖ TRỢ LÃI SUẤT 5% CẦN PHÂN BỔ:",
                "scale_val": 600_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Kịch bản 1 (Trả thẳng giảm 600k): BẠN trả lãi",
                "mech_line2": "Kịch bản 2 (Một giá chung 12tr): CỬA HÀNG chịu phí",
                "ledger_title": "SO SÁNH VỚI QUẸT THẺ THÔNG THƯỜNG (MDR 2,2%):",
                "debit_line": "Quẹt thẻ thường: Cửa hàng chỉ mất 264.000 đ (2,2%)",
                "credit_line": "Trả góp 0%: Cửa hàng mất 600.000 đ (5,0% — gấp đôi)",
                "rule": "NẾU MỘT GIÁ CHUNG, NGƯỜI MUA TRẢ THẲNG ĐANG PHỤ TRẢ PHÍ CHO NGƯỜI TRẢ GÓP",
            },
            # 8: Mode L-C (Bước 8 - So sánh trả góp qua Thẻ tín dụng)
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 3},
                "flow": ("wire", 0, 3),
                "kicker": "BƯỚC 8  ·  SO SÁNH: CÔNG TY TÀI CHÍNH vs THẺ TÍN DỤNG",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "HAI CƠ CHẾ TRẢ GÓP 0% PHỔ BIẾN TRÊN THỊ TRƯỜNG",
                "card1_title": "KÊNH 1: QUA CÔNG TY TÀI CHÍNH",
                "card1_big": "Cửa hàng bị trừ 5% (600.000 đ)",
                "card1_sub": "Hồ sơ vay mới · Chủ nợ là Công ty tài chính · EIR ngầm ~10%/năm",
                "card2_title": "KÊNH 2: QUA THẺ TÍN DỤNG NGÂN HÀNG",
                "card2_big": "Phí chuyển đổi 3% (360.000 đ)",
                "card2_sub": "Trừ trên hạn mức thẻ sẵn có · EIR ~5,8%/năm (hoặc ~17%/năm nếu mất thêm giảm giá 600k)",
                "rule": "LUÔN CỘNG CẢ “PHÍ CHUYỂN ĐỔI THẺ” LẪN “KHOẢN GIẢM GIÁ BỊ MẤT” ĐỂ RA CHI PHÍ THẬT",
            },
            # 9: Mode L-C (Bước 9 - 3 Tình huống ngoại lệ)
            {
                "mode": "L-C",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("pipe", 0, 3, 2),
                "kicker": "BƯỚC 9  ·  3 TÌNH HUỐNG NGOẠI LỆ KHI KẾ HOẠCH LỆCH",
                "lc_type": "P9_TRIPTYCH",
                "headline": "ĐIỀU GÌ XẢY RA KHI BẠN TẤT TOÁN SỚM, TRỄ HẠN HOẶC ĐỔI TRẢ HÀNG?",
                "col1_title": "1. TẤT TOÁN SỚM Ở THÁNG 4",
                "col1_big": "Không hoàn lại 600.000 đ",
                "col1_sub": "Vẫn phải trả đủ 8.000.000 đ gốc còn lại + phí tất toán sớm · EIR vọt lên ~1,48%/tháng",
                "col2_title": "2. TRỄ HẠN THANH TOÁN KỲ 5",
                "col2_big": "Phí phạt 150.000 đ + Lãi phạt",
                "col2_sub": "Ưu đãi 0% chấm dứt ngay cho kỳ quá hạn và ảnh hưởng trực tiếp lịch sử tín dụng",
                "col3_title": "3. ĐỔI TRẢ MÁY TẠI CỬA HÀNG",
                "col3_big": "2 giao dịch hoàn toàn tách rời",
                "col3_sub": "Cửa hàng phải hoàn tiền để thanh lý hợp đồng vay tại Công ty tài chính trước",
                "rule": "ĐỌC KỸ ĐIỀU KHOẢN TẤT TOÁN SỚM & PHÍ TRỄ HẠN TRƯỚC KHI ĐẶT BÚT KÝ",
            },
            # 10: Mode L-A (Kết luận)
            {
                "mode": "L-A",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("none",),
                "kicker": "KẾT LUẬN  ·  TIỀN LÃI CHỈ ĐỔI CHỖ ĐỨNG",
                "stage_tag": "12.000.000 Đ (GHI BÁN) − 11.400.000 Đ (THỰC NHẬN) = 600.000 Đ",
                "beats": [
                    ("1. BẢN CHẤT KẾ TOÁN", "Σ Nợ (11,4tr TK 112 + 600k TK 641) = Σ Có (12,0tr TK 511)"),
                    ("2. KHI NÀO CÓ LỢI CHO BẠN?", "Khi giá trả thẳng & trả góp bằng hệt nhau và bạn trả đúng hạn 100%"),
                    ("3. KHI NÀO THÀNH BẪY?", "Khi mất chiết khấu tiền mặt lớn hoặc cộng thêm phí chuyển đổi/bảo hiểm"),
                    ("4. CÂU HỎI BỎ TÚI", "“Nếu trả thẳng một lần ngay bây giờ thì giá giảm còn bao nhiêu?”"),
                ],
                "rule": "ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  WHERE MONEY SLEEPS",
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
        "plates_pool": [
            ("public/brand/card-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-1.jpg", (40, 430, 1040, 1255)),
            ("public/brand/card-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-2.jpg", (40, 430, 1040, 1255)),
            ("public/brand/card-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-3.jpg", (40, 430, 1040, 1255)),
            ("public/brand/card-short-plate-4.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-4.jpg", (40, 430, 1040, 1255)),
        ],
        "scenes": [
            {
                "mode": "L-A",
                "plate_idx": 0,
                "active": {0, 1, 4},
                "flow": ("wire", 4, 0),
                "kicker": "MỞ ĐẦU  ·  QUẸT THẺ 10 TRIỆU HOÀN TIỀN 100.000 Đ",
                "stage_tag": "HOÁ ĐƠN 10.000.000 Đ  ·  HOÀN TIỀN +100.000 Đ  ·  QUÁN NHẬN 9.780.000 Đ",
                "beats": [
                    ("1. TRẢI NGHIỆM CỦA BẠN", "Chạm thẻ thanh toán 10.000.000 đ, nhận ngay +100.000 đ hoàn tiền (1%)"),
                    ("2. THỰC TẾ TẠI QUÁN QUEN", "Hai ngày sau (T+2), tài khoản quán chỉ nhận về 9.780.000 đ"),
                    ("3. KHOẢN HỤT 220.000 Đ", "Phí chấp nhận thẻ (MDR 2,2%) bị khấu trừ tự động tại nguồn"),
                    ("4. CÂU HỎI TRUNG TÂM", "220.000 đ được chia cho những ai và liên quan gì tới 100.000 đ của bạn?"),
                ],
                "rule": "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC TRỌN LỜI BÌNH",
            },
            {
                "mode": "L-B",
                "plate_idx": 1,
                "active": {0, 1, 3, 4},
                "flow": ("wire", 1, 3, 4),
                "kicker": "BƯỚC 1  ·  HAI GIÂY ĐẦU TIÊN SAU CÚ CHẠM THẺ (AUTH)",
                "stage_tag": "BẢN TIN CẤP PHÉP (AUTHORIZATION)  ·  0 ĐỒNG TIỀN THẬT DI CHUYỂN",
                "scale_title": "HẠN MỨC TÍN DỤNG TẠM KHOÁ (AUTH HOLD):",
                "scale_val": 10_000_000,
                "mech_type": "P2_CONTRACT",
                "mech_left": "Máy POS Quán quen",
                "mech_right": "Ngân hàng phát hành thẻ",
                "mech_badge": "BẢN TIN GIỮ CHỖ 10.000.000 Đ",
                "ledger_title": "TRẠNG THÁI LÚC QUẸT THẺ XONG (T+0):",
                "debit_line": "Ngân hàng của bạn: Phong toả 10.000.000 đ hạn mức khả dụng",
                "credit_line": "Két tiền Quán quen: +0 đ (Chỉ nhận tờ biên lai in nhiệt)",
                "rule": "TIẾNG “BÍP” TẠI QUẦY CHỈ LÀ LỜI HỨA THANH TOÁN, CHƯA PHẢI TIỀN VỀ KÉT",
            },
            {
                "mode": "L-A",
                "plate_idx": 2,
                "active": {1, 2, 3, 4},
                "flow": ("wire", 1, 2, 3, 4),
                "kicker": "BƯỚC 2  ·  ĐÊM ĐỐI SOÁT LÔ GIAO DỊCH (CLEARING)",
                "stage_tag": "ĐỐI SOÁT CUỐI NGÀY QUA TỔ CHỨC THẺ CHUYỂN MẠCH",
                "beats": [
                    ("1. GOM LÔ CUỐI NGÀY (BATCH)", "Máy POS của quán gửi toàn bộ biên lai trong ngày về Ngân hàng của quán"),
                    ("2. ĐỐI CHIẾU LIÊN NGÂN HÀNG", "Tổ chức thẻ chuyển mạch phân loại giao dịch theo từng ngân hàng phát hành"),
                    ("3. SỔ KẾ TOÁN QUÁN ĐÊM ĐẦU", "Debit 1388 (Phải thu khác): 10.000.000 đ  |  Credit 511: 10.000.000 đ"),
                    ("4. ĐỢI QUYẾT TOÁN T+2", "Tiền thật vẫn chưa chạy qua tài khoản ngân hàng của quán"),
                ],
                "rule": "TRONG 48 GIỜ ĐẦU, 10.000.000 Đ NẰM Ở MỤC PHẢI THU KHÁC (TK 1388)",
            },
            {
                "mode": "L-B",
                "plate_idx": 3,
                "active": {1, 2, 4},
                "flow": ("pipe", 4, 2, 1),
                "kicker": "BƯỚC 3  ·  QUYẾT TOÁN T+2 & KHẤU TRỪ PHÍ MDR 2,2%",
                "stage_tag": "QUÁN THỰC NHẬN 9.780.000 Đ  ·  KHẤU TRỪ 220.000 Đ TẠI NGUỒN",
                "scale_title": "SỐ TIỀN VỀ TÀI KHOẢN QUÁN QUEN (T+2):",
                "scale_val": 9_780_000,
                "mech_type": "P1_SPLIT",
                "split_ratio": 0.978,
                "split_left_lbl": "THỰC NHẬN (97,8%): 9.780.000 Đ",
                "split_right_lbl": "MDR 2,2%: 220K",
                "ledger_title": "BÚT TOÁN NHẬN TIỀN TẠI QUÁN (TT 99/2025/TT-BTC):",
                "debit_line": "Debit 112: +9.780.000 đ  ·  Debit 641 (Phí MDR): +220.000 đ",
                "credit_line": "Credit 1388 (Xoá phải thu khác): −10.000.000 đ",
                "rule": "Σ NỢ (9.780.000 + 220.000) = Σ CÓ (10.000.000 Đ) — CÂN BẰNG TUYỆT ĐỐI",
            },
            {
                "mode": "L-B",
                "plate_idx": 4,
                "active": {2, 3, 4},
                "flow": ("pipe", 2, 3, 4),
                "kicker": "BƯỚC 4  ·  GIẢI PHẪU 220.000 Đ PHÍ MDR ĐI VỀ ĐÂU?",
                "stage_tag": "CHIA PHÍ MDR 2,2% CHO 3 ĐỊNH CHẾ TRUNG GIAN",
                "scale_title": "TỔNG PHÍ CHẤP NHẬN THẺ (MDR 2,2%):",
                "scale_val": 220_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "1. Phí Interchange về Ngân hàng của bạn (1,50%): +150.000 đ",
                "mech_line2": "2. Ngân hàng quán (0,60%): +60.000 đ  ·  Tổ chức thẻ (0,10%): +10.000 đ",
                "ledger_title": "NGUỒN THU CỦA NGÂN HÀNG PHÁT HÀNH THẺ:",
                "debit_line": "Ngân hàng của bạn nhận 150.000 đ (68% tổng phí MDR)",
                "credit_line": "Trích 100.000 đ hoàn cho bạn  ·  Giữ lại +50.000 đ lãi thuần",
                "rule": "TIỀN HOÀN 100.000 Đ ĐƯỢC TRÍCH TỪ 150.000 Đ PHÍ INTERCHANGE THU CỦA QUÁN",
            },
            {
                "mode": "L-C",
                "plate_idx": 5,
                "active": {0, 4},
                "flow": ("pipe", 4, 0),
                "kicker": "BƯỚC 5  ·  CHU KỲ MIỄN LÃI 45 NGÀY & DÒNG TIỀN HOÀN",
                "lc_type": "P5_EIR_FORMULA",
                "headline": "DÒNG TIỀN GIỮA BẠN VÀ NGÂN HÀNG PHÁT HÀNH THẺ Ở CUỐI KỲ SAO KÊ",
                "card1_title": "NẾU BẠN TRẢ ĐỦ 100% DƯ NỢ ĐÚNG HẠN",
                "card1_big": "Trả 10.000.000 đ  ·  Nhận hoàn +100.000 đ",
                "card1_sub": "Chi phí thực của bạn = 9.900.000 đ + Tận dụng vốn miễn lãi tới 45 ngày",
                "card2_title": "KẾT QUẢ CỦA NGÂN HÀNG PHÁT HÀNH THẺ",
                "card2_big": "Thu 150.000 đ − Chi 100.000 đ = +50.000 đ",
                "card2_sub": "Ngân hàng vẫn lãi ròng 50.000 đ trên giao dịch mà không tốn tiền túi",
                "rule": "HOÀN TIỀN LÀ CƠ CHẾ CHIA SẺ PHÍ INTERCHANGE ĐỂ KHUYẾN KHÍCH BẠN QUẸT THẺ",
            },
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {2, 3, 4},
                "flow": ("pipe", 4, 3, 2),
                "kicker": "BƯỚC 6  ·  BÙ TRỪ ĐA PHƯƠNG LIÊN NGÂN HÀNG (NETTING)",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "VÌ SAO HÀNG TRIỆU GIAO DỊCH THẺ CHỈ CẦN MỘT LỆNH CHUYỂN TIỀN RÒNG CUỐI NGÀY?",
                "card1_title": "NẾU CHUYỂN TỪNG GIAO DỊCH RIÊNG LẺ (GROSS)",
                "card1_big": "Hàng triệu lệnh chuyển tiền chồng chéo",
                "card1_sub": "Tốn thanh khoản dự trữ khổng lồ giữa các ngân hàng thương mại",
                "card2_title": "CƠ CHẾ BÙ TRỪ RÒNG ĐA PHƯƠNG (MULTILATERAL NETTING)",
                "card2_big": "Gom chênh lệch ròng 1 lần / ngày",
                "card2_sub": "Chỉ phần chênh lệch ròng cuối ngày mới chạy qua tài khoản tại Ngân hàng Nhà nước",
                "rule": "ĐÓ LÀ LÝ DO QUÁN QUEN PHẢI ĐỢI T+1 HOẶC T+2 MỚI NHẬN ĐƯỢC TIỀN THẬT",
            },
            {
                "mode": "L-B",
                "plate_idx": 5,
                "active": {0, 1, 4},
                "flow": ("none",),
                "kicker": "BƯỚC 7  ·  VÒNG TRÒN GIÁ MÓN ĂN & TRỢ CẤP CHÉO",
                "stage_tag": "KHI QUÁN QUEN CỘNG 2,2% PHÍ THẺ VÀO GIÁ THỰC ĐƠN CHUNG",
                "scale_title": "PHÍ NHẬN THẺ NẰM TRONG HOÁ ĐƠN 10 TRIỆU:",
                "scale_val": 220_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Khách quẹt thẻ: Chịu giá cao hơn nhưng được hoàn lại 100.000 đ (1%)",
                "mech_line2": "Khách trả tiền mặt/chuyển khoản: Chịu cùng mức giá nhưng hoàn 0 đ",
                "ledger_title": "HIỆU ỨNG TRỢ CẤP CHÉO TRONG BÁN LẺ:",
                "debit_line": "Người trả tiền mặt đang gián tiếp tài trợ phí thẻ",
                "credit_line": "Người dùng thẻ nhận lại một phần tiền của chính mình",
                "rule": "KHÔNG CÓ KHOẢN HOÀN TIỀN NÀO TỪ TRÊN TRỜI RƠI XUỐNG",
            },
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 1, 2, 4},
                "flow": ("wire", 0, 2, 1),
                "kicker": "BƯỚC 8  ·  SO SÁNH: THẺ QUỐC TẾ vs THẺ NỘI ĐỊA NAPAS vs MÃ QR",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "VÌ SAO NHIỀU QUÁN NHỎ THÍCH NHẬN QUÉT MÃ QR CHUYỂN KHOẢN HƠN THẺ TÍN DỤNG?",
                "card1_title": "QUẸT THẺ TÍN DỤNG (MDR ~1,8% – 2,5%)",
                "card1_big": "Mất 220.000 đ / đơn 10 triệu  ·  Chờ T+2",
                "card1_sub": "Đổi lại khách có hạn mức tín dụng 45 ngày và hoàn tiền 1% từ Interchange",
                "card2_title": "CHUYỂN KHOẢN MÃ QR / THẺ NỘI ĐỊA (0% – 0,4%)",
                "card2_big": "Phí cực thấp hoặc 0 đ  ·  Tiền về ngay T+0",
                "card2_sub": "Không có nguồn phí Interchange 1,5% nên ngân hàng rất ít hoàn tiền mặt",
                "rule": "MỨC HOÀN TIỀN CỦA THẺ TỶ LỆ THUẬN VỚI MỨC PHÍ MDR MÀ CỬA HÀNG PHẢI CHỊU",
            },
            {
                "mode": "L-C",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("pipe", 0, 4),
                "kicker": "BƯỚC 9  ·  3 TÌNH HUỐNG NGOẠI LỆ: HOÀN ĐƠN, PHỤ THU & TRỄ HẠN",
                "lc_type": "P9_TRIPTYCH",
                "headline": "ĐIỀU GÌ XẢY RA KHI HOÀN HUỶ GIAO DỊCH, QUÁN THU PHỤ PHÍ, HOẶC BẠN CHỈ TRẢ TỐI THIỂU?",
                "col1_title": "1. HOÀN ĐƠN HÀNG (REFUND)",
                "col1_big": "Thu hồi 100.000 đ tiền hoàn",
                "col1_sub": "Ngân hàng ghi nợ lại khoản Cashback đã cấp; quán thường không được hoàn lại toàn bộ phí xử lý",
                "col2_title": "2. QUÁN THU PHỤ PHÍ QUẸT THẺ 2%",
                "col2_big": "Lỗ ròng −120.000 đ",
                "col2_sub": "Trả thêm 200.000 đ phụ phí chỉ để nhận 100.000 đ hoàn tiền là bài toán lỗ ngay tại quầy",
                "col3_title": "3. CHỈ ĐÓNG TỐI THIỂU 5% CUỐI KỲ",
                "col3_big": "Lãi thẻ 28%–36%/năm tính từ ngày quẹt",
                "col3_sub": "Mất toàn bộ ân hạn miễn lãi; chỉ 1 tháng trả chậm sẽ nuốt sạch tiền hoàn của cả năm",
                "rule": "THẺ HOÀN TIỀN CHỈ CÓ LỢI KHI KHÔNG BỊ PHỤ THU VÀ BẠN TRẢ ĐỦ 100% ĐÚNG HẠN",
            },
            {
                "mode": "L-A",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("none",),
                "kicker": "KẾT LUẬN  ·  ĐỌC THẤU ĐƯỜNG ĐI CỦA 220.000 Đ",
                "stage_tag": "10.000.000 Đ = 9.780.000 Đ (QUÁN NHẬN) + 100.000 Đ (HOÀN BẠN) + 120.000 Đ (PHÍ HỆ THỐNG)",
                "beats": [
                    ("1. BẢN CHẤT KẾ TOÁN", "Σ Nợ (9,78tr TK 112 + 220k TK 641) = Σ Có (10,0tr TK 511)"),
                    ("2. NGUỒN GỐC CASHBACK", "Trích từ 150.000 đ phí Interchange mà ngân hàng của bạn thu từ quán"),
                    ("3. KHI NÀO NÊN DÙNG?", "Khi quán niêm yết 1 giá duy nhất, không phụ thu thẻ, và bạn trả đủ 100% sao kê"),
                    ("4. CÂU HỎI BỎ TÚI", "“Quẹt thẻ có phụ phí không, và trả tiền mặt có được chiết khấu không?”"),
                ],
                "rule": "ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  WHERE MONEY SLEEPS",
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
        "plates_pool": [
            ("public/brand/pay-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-1.jpg", (40, 430, 1040, 1255)),
            ("public/brand/pay-short-plate-2.jpg", (20, 260, 1060, 1105)),
            ("public/brand/pay-short-plate-2.jpg", (20, 720, 1060, 1565)),
            ("public/brand/pay-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-3.jpg", (40, 430, 1040, 1255)),
            ("public/brand/pay-short-plate-4.jpg", (20, 420, 1060, 1265)),
            ("public/brand/pay-short-plate-4.jpg", (40, 430, 1040, 1255)),
        ],
        "scenes": [
            # Bài pay có 12 cảnh
            {
                "mode": "L-A",
                "plate_idx": 0,
                "active": {0, 1, 2},
                "flow": ("wire", 0, 1, 2),
                "kicker": "MỞ ĐẦU  ·  LƯƠNG VỀ 15 TRIỆU NHƯNG TIỀN ĐỨNG YÊN",
                "stage_tag": "TIN NHẮN BÁO +15.000.000 Đ  ·  KÉT NGÂN HÀNG KHÔNG HỀ MỞ",
                "beats": [
                    ("1. TIN NHẮN LƯƠNG VỀ", "Điện thoại báo tài khoản tăng +15.000.000 đ ngay trong 1 giây"),
                    ("2. YÊU CẦU NGÀY NHẬN VIỆC", "Phòng nhân sự đề nghị mọi nhân viên mở tài khoản cùng 1 ngân hàng"),
                    ("3. SỰ THẬT DƯỚI HẦM KÉT", "Không một đồng tiền mặt hay dự trữ nào rời khỏi ngân hàng đó"),
                    ("4. CÂU HỎI TRUNG TÂM", "Ngân hàng được lợi gì khi giữ cả công ty lẫn 500 nhân viên ở cùng một nơi?"),
                ],
                "rule": "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC TRỌN LỜI BÌNH",
            },
            {
                "mode": "L-B",
                "plate_idx": 1,
                "active": {0, 1},
                "flow": ("wire", 0, 1),
                "kicker": "BƯỚC 1  ·  HẠCH TOÁN BẢNG LƯƠNG TẠI DOANH NGHIỆP",
                "stage_tag": "SỔ KẾ TOÁN CÔNG TY (TT 99/2025): CHI PHÍ LƯƠNG & KHẤU TRỪ",
                "scale_title": "TỔNG CHI PHÍ LƯƠNG GHI NHẬN (VÍ DỤ):",
                "scale_val": 17_000_000,
                "mech_type": "P1_SPLIT",
                "split_ratio": 0.882,
                "split_left_lbl": "THỰC LĨNH (TK 334): 15.000.000 Đ",
                "split_right_lbl": "BHXH & THUẾ: 2TR",
                "ledger_title": "BÚT TOÁN TÍNH LƯƠNG (TT 99/2025/TT-BTC):",
                "debit_line": "Debit 642 (Chi phí quản lý DN): +17.000.000 đ",
                "credit_line": "Credit 334: 15.000.000 đ  ·  Credit 338/3335: 2.000.000 đ",
                "rule": "TRƯỚC GIỜ BẤM NÚT CHI LƯƠNG, 15.000.000 Đ LÀ KHOẢN CÔNG TY ĐANG NỢ BẠN (TK 334)",
            },
            {
                "mode": "L-B",
                "plate_idx": 2,
                "active": {0, 1, 2},
                "flow": ("wire", 0, 1, 2),
                "kicker": "BƯỚC 2  ·  CƠ CHẾ CHUYỂN KHOẢN NỘI BỘ (ON-US BOOK TRANSFER)",
                "stage_tag": "CÙNG MỘT NGÂN HÀNG: CHỈ ĐỔI TÊN CHỦ NỢ TRÊN SỔ CÁI",
                "scale_title": "LỆNH CHI LƯƠNG THỰC LĨNH:",
                "scale_val": 15_000_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Dòng 1 — TK Tiền gửi Công ty:  −15.000.000 đ (Ngân hàng bớt nợ Công ty)",
                "mech_line2": "Dòng 2 — TK Tiền gửi Của bạn:  +15.000.000 đ (Ngân hàng tăng nợ Bạn)",
                "ledger_title": "BÚT TOÁN TẤT TOÁN LƯƠNG TẠI CÔNG TY (TT 99/2025):",
                "debit_line": "Debit 334 (Xoá nợ phải trả NLĐ): −15.000.000 đ",
                "credit_line": "Credit 112 (Tiền gửi ngân hàng): −15.000.000 đ",
                "rule": "TỔNG NGUỒN VỐN TRONG NGÂN HÀNG KHÔNG ĐỔI (HAO HỤT THANH KHOẢN = 0 Đ)",
            },
            {
                "mode": "L-A",
                "plate_idx": 3,
                "active": {1, 2},
                "flow": ("none",),
                "kicker": "BƯỚC 3  ·  SỐ DƯ TRÊN ĐIỆN THOẠI THỰC CHẤT LÀ GÌ?",
                "stage_tag": "ĐỐI XỨNG BẢNG CÂN ĐỐI KẾ TOÁN GIỮA BẠN VÀ NGÂN HÀNG",
                "beats": [
                    ("1. DƯỚI GÓC NHÌN CỦA BẠN", "15.000.000 đ trên màn hình là Tài sản thanh khoản (Tiền gửi không kỳ hạn)"),
                    ("2. DƯỚI GÓC NHÌN NGÂN HÀNG", "15.000.000 đ đó nằm ở cột NỢ PHẢI TRẢ (Ngân hàng đang nợ bạn)"),
                    ("3. KHÔNG PHẢI HỘP GIỮ HỘ", "Ngân hàng không cất riêng cọc tiền 15 triệu mang tên bạn trong két"),
                    ("4. CAM KẾT THANH KHOẢN", "Ngân hàng cam kết trả tiền ngay khi bạn rút hoặc quét QR chuyển đi"),
                ],
                "rule": "SỐ DƯ TÀI KHOẢN LÀ KHOẢN NỢ KHÔNG KỲ HẠN MÀ NGÂN HÀNG ĐANG NỢ BẠN",
            },
            {
                "mode": "L-B",
                "plate_idx": 4,
                "active": {1, 2, 3},
                "flow": ("pipe", 3, 1),
                "kicker": "BƯỚC 4  ·  500 ĐỒNG NGHIỆP TẠO THÀNH BỂ VỐN CASA 2,5 TỶ",
                "stage_tag": "500 TÀI KHOẢN × 5.000.000 Đ SỐ DƯ BÌNH QUÂN = 2,5 TỶ ĐỒNG",
                "scale_title": "QUY MÔ BỂ VỐN KHÔNG KỲ HẠN (CASA POOL):",
                "scale_val": 2_500_000_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Mỗi cá nhân rút tiêu lẻ tẻ theo nhịp sinh hoạt khác nhau",
                "mech_line2": "Phần đáy bể vốn bình quân (~5 triệu/người) luôn nằm yên trong ngân hàng",
                "ledger_title": "CHI PHÍ TRẢ LÃI KHÔNG KỲ HẠN (CASA ~0,1%/NĂM):",
                "debit_line": "Lãi trả cho mỗi tài khoản 5 triệu: ~5.000 đ / năm",
                "credit_line": "Tổng lãi trả cho cả 500 tài khoản (2,5 tỷ): ~2.500.000 đ / năm",
                "rule": "LUẬT SỐ ĐÔNG BIẾN TIỀN LƯƠNG NGẮN HẠN THÀNH NGUỒN VỐN ỔN ĐỊNH CHO NGÂN HÀNG",
            },
            {
                "mode": "L-C",
                "plate_idx": 5,
                "active": {1, 3, 4},
                "flow": ("pipe", 1, 4),
                "kicker": "BƯỚC 5  ·  CHÊNH LỆCH CHI PHÍ VỐN 1 : 50 (CASA vs KỲ HẠN)",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "SO SÁNH CHI PHÍ NGÂN HÀNG HUY ĐỘNG 2,5 TỶ ĐỒNG TRONG 1 NĂM",
                "card1_title": "NGUỒN 1: BỂ VỐN LƯƠNG KHÔNG KỲ HẠN (CASA 0,1%/NĂM)",
                "card1_big": "Chi phí lãi: ~2.500.000 đ / năm",
                "card1_sub": "Rẻ gấp 50 lần so với tiền gửi có kỳ hạn · Giúp ngân hàng hạ mạnh giá vốn đầu vào (COF)",
                "card2_title": "NGUỒN 2: TIỀN GỬI TIẾT KIỆM CÓ KỲ HẠN (LÃI 5,0%/NĂM)",
                "card2_big": "Chi phí lãi: ~125.000.000 đ / năm",
                "card2_sub": "Đắt hơn 122.500.000 đ/năm cho cùng một quy mô vốn 2,5 tỷ đồng",
                "rule": "TỶ LỆ CASA CAO LÀ CHÌA KHOÁ GIÚP NGÂN HÀNG TỐI ƯU BIÊN LÃI RÒNG (NIM)",
            },
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {1, 3, 4},
                "flow": ("pipe", 1, 4),
                "kicker": "BƯỚC 6  ·  BIÊN LÃI RÒNG (NIM) & DỰ TRỮ THANH KHOẢN",
                "lc_type": "P5_EIR_FORMULA",
                "headline": "TỪ BỂ VỐN CASA 2,5 TỶ ĐỒNG ĐẾN KHOẢN CHO VAY TÍN DỤNG NGOÀI NỀN KINH TẾ",
                "card1_title": "PHẦN GIỮ LẠI ĐỆM THANH KHOẢN (VÍ DỤ ~20%)",
                "card1_big": "500.000.000 đ sẵn sàng đáp ứng rút tiền",
                "card1_sub": "Đảm bảo bất kỳ lúc nào bạn quét QR hay rút ATM đều có tiền ngay lập tức",
                "card2_title": "PHẦN PHÂN BỔ CHO VAY (VÍ DỤ 2,0 TỶ @ 9%/NĂM)",
                "card2_big": "Thu lãi ~180tr − Trả CASA 2,5tr = +177,5tr",
                "card2_sub": "Chênh lệch dùng bù đắp chi phí vận hành hệ thống 24/7 và dự phòng rủi ro tín dụng",
                "rule": "TIỀN LƯƠNG NẰM YÊN CỦA BẠN ĐANG THỨC ĐỂ SINH LỜI TRONG CÁC KHOẢN VAY KHÁC",
            },
            {
                "mode": "L-B",
                "plate_idx": 5,
                "active": {0, 1, 4},
                "flow": ("wire", 1, 0),
                "kicker": "BƯỚC 7  ·  CUỘC MẶC CẢ GIỮA NGÂN HÀNG VÀ DOANH NGHIỆP",
                "stage_tag": "ĐỔI TRỌN GÓI BẢNG LƯƠNG LẤY ƯU ĐÃI DỊCH VỤ & LÃI VAY",
                "scale_title": "GIÁ TRỊ BỂ VỐN LƯƠNG DOANH NGHIỆP MANG LẠI:",
                "scale_val": 2_500_000_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Ngân hàng nhận: Dòng tiền CASA 2,5 tỷ đều đặn + Tệp 500 khách hàng cá nhân",
                "mech_line2": "Doanh nghiệp nhận: Miễn phí chi lương tự động + Ưu đãi lãi vay vốn lưu động",
                "ledger_title": "VÌ SAO PHÒNG NHÂN SỰ CHỈ ĐỊNH 1 NGÂN HÀNG?",
                "debit_line": "Giảm lỗi vận hành khi chạy bảng lương hàng trăm người",
                "credit_line": "Tối ưu chi phí tài chính cho doanh nghiệp trong hợp đồng tổng thể",
                "rule": "BẢNG LƯƠNG NHÂN VIÊN LÀ MỘT TÀI SẢN ĐÀM PHÁN GIỮA CÔNG TY VÀ NGÂN HÀNG",
            },
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 1, 2},
                "flow": ("pipe", 0, 1, 2),
                "kicker": "BƯỚC 8  ·  SO SÁNH: CHI LƯƠNG NỘI BỘ (ON-US) vs LIÊN NGÂN HÀNG (OFF-US)",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "ĐIỀU GÌ XẢY RA NẾU NHÂN VIÊN NHẬN LƯƠNG Ở MỘT NGÂN HÀNG KHÁC?",
                "card1_title": "CÙNG NGÂN HÀNG (ON-US BOOK TRANSFER)",
                "card1_big": "Hao hụt vốn của ngân hàng = 0 đ",
                "card1_sub": "Chỉ đổi tên chủ nợ trên sổ nội bộ · Ngân hàng giữ trọn 100% số dư CASA",
                "card2_title": "KHÁC NGÂN HÀNG (OFF-US INTERBANK)",
                "card2_big": "Chảy máu thanh khoản thực sự ra ngoài",
                "card2_sub": "Ngân hàng trả lương phải chuyển tiền dự trữ thật sang ngân hàng của bạn qua hệ thống bù trừ",
                "rule": "GIỮ CHÂN NGƯỜI NHẬN LƯƠNG Ở LẠI LÀ MỤC TIÊU SỐNG CÒN CỦA NGÂN HÀNG CHI LƯƠNG",
            },
            {
                "mode": "L-C",
                "plate_idx": 7,
                "active": {1, 2, 4},
                "flow": ("wire", 1, 2),
                "kicker": "BƯỚC 9  ·  BÁN CHÉO SẢN PHẨM TRÊN TỆP TÀI KHOẢN LƯƠNG",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "VÌ SAO NGÂN HÀNG BIẾT CHÍNH XÁC HẠN MỨC THẺ TÍN DỤNG & THẤU CHI CỦA BẠN?",
                "card1_title": "DỮ LIỆU DÒNG TIỀN THU NHẬP THẬT (VERIFIED INCOME)",
                "card1_big": "Lịch sử lương 6–12 tháng chính xác 100%",
                "card1_sub": "Ngân hàng không cần thẩm định giấy tờ phức tạp vì nắm rõ ngày giờ và quy mô lương về",
                "card2_title": "HỆ SINH THÁI BÁN CHÉO (CROSS-SELLING)",
                "card2_big": "Thẻ tín dụng · Vay thấu chi · Vay mua nhà",
                "card2_sub": "Chi phí tìm kiếm khách hàng (CAC) gần như bằng 0 nhờ gói trả lương doanh nghiệp",
                "rule": "TÀI KHOẢN LƯƠNG LÀ CÁNH CỬA ĐẦU TIÊN ĐƯA BẠN VÀO HỆ SINH THÁI TÍN DỤNG",
            },
            {
                "mode": "L-C",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("pipe", 2, 1),
                "kicker": "BƯỚC 10  ·  3 TÌNH HUỐNG NGOẠI LỆ VỀ TÀI KHOẢN LƯƠNG",
                "lc_type": "P9_TRIPTYCH",
                "headline": "ĐIỀU GÌ XẢY RA KHI BẠN CHUYỂN TIỀN ĐI NGAY, NGHỈ VIỆC, HOẶC DÙNG THẤU CHI LƯƠNG?",
                "col1_title": "1. CHUYỂN HẾT LƯƠNG SANG NGÂN HÀNG KHÁC",
                "col1_big": "Bể vốn CASA giảm thực chất",
                "col1_sub": "Ngân hàng chi lương mất nguồn vốn 0,1% ngay lập tức qua kênh chuyển mạch liên ngân hàng",
                "col2_title": "2. KHI BẠN NGHỈ VIỆC / ĐỔI CÔNG TY",
                "col2_big": "Tài khoản hết ưu đãi gói Payroll",
                "col2_sub": "Các tài khoản không còn dòng lương đổ về có thể phát sinh phí duy trì nếu số dư thấp",
                "col3_title": "3. VAY THẤU CHI QUA TÀI KHOẢN LƯƠNG",
                "col3_big": "Vay lại chính bể vốn với lãi 12%–18%/năm",
                "col3_sub": "Ngân hàng tự động khấu trừ gốc và lãi ngay giây đầu tiên khi kỳ lương tháng sau vừa báo về",
                "rule": "HIỂU RÕ CƠ CHẾ ĐỂ CHỦ ĐỘNG QUẢN LÝ SỐ DƯ NGAY KHI LƯƠNG VỪA VỀ TÀI KHOẢN",
            },
            {
                "mode": "L-A",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("none",),
                "kicker": "KẾT LUẬN  ·  ĐÁNH THỨC TIỀN LƯƠNG ĐANG NGỦ",
                "stage_tag": "Σ NỢ (17,0TR TK 642) = Σ CÓ (15,0TR TK 334 + 2,0TR TK 338/3335) — TT 99/2025",
                "beats": [
                    ("1. BẢN CHẤT KẾ TOÁN", "Số dư trên điện thoại là khoản Nợ không kỳ hạn mà ngân hàng đang nợ bạn"),
                    ("2. SỨC MẠNH CỦA SỐ ĐÔNG", "Hàng trăm tài khoản lương tạo nên bể vốn CASA 0,1%/năm rẻ gấp 50 lần kỳ hạn"),
                    ("3. KHI NÀO CÓ LỢI CHO BẠN?", "Khi tận dụng miễn phí chuyển khoản 24/7 và tách riêng phần tiết kiệm sinh lời"),
                    ("4. CÂU HỎI BỎ TÚI", "“Sau chi tiêu tháng này, bao nhiêu tiền lương đang ngủ ở mức 0,1%/năm?”"),
                ],
                "rule": "ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  WHERE MONEY SLEEPS",
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
        "plates_pool": [
            ("public/brand/card-short-plate-1.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-2.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/card-short-plate-3.jpg", (20, 420, 1060, 1265)),
            ("public/brand/install-short-plate-4.jpg", (20, 780, 1060, 1625)),
            ("public/brand/card-short-plate-4.jpg", (20, 460, 1060, 1305)),
            ("public/brand/install-short-plate-1.jpg", (20, 420, 1060, 1265)),
        ],
        "scenes": [
            # 0: Mode L-A (Mở đầu: Con số 500 nghìn dễ chịu trên sao kê 10 triệu)
            {
                "mode": "L-A",
                "plate_idx": 0,
                "active": {0, 3},
                "flow": ("wire", 3, 0),
                "kicker": "MỞ ĐẦU  ·  SAO KÊ 10 TRIỆU & NÚT BẤM TRẢ TỐI THIỂU 5%",
                "stage_tag": "SAO KÊ THẺ TÍN DỤNG 10.000.000 Đ  ·  TỐI THIỂU 5% = 500.000 Đ",
                "beats": [
                    ("1. DƯ NỢ SAO KÊ KỲ ĐẦU", "10.000.000 đ  ·  Hạn thanh toán: Ngày 45"),
                    ("2. LỰA CHỌN NHẸ TÊNH", "Trả tối thiểu 5% = 500.000 đ (Đúng hạn, 0 phí phạt)"),
                    ("3. CÚ SỐC SAO KÊ KỲ SAU", "Dư nợ Ngày 60 vọt lên: 10.092.500 đ (+592.500 đ lãi)"),
                    ("4. CÂU HỎI TRUNG TÂM", "Vì sao vừa trả 500.000 đ mà lại bị cộng 592.500 đ tiền lãi?"),
                ],
                "rule": "VÍ DỤ MINH HOẠ CƠ CHẾ  ·  BẬT PHỤ ĐỀ [CC] ĐỂ ĐỌC TRỌN LỜI BÌNH",
            },
            # 1: Mode L-B (Ngày 01: Quẹt thẻ 10 triệu và lời hứa 45 ngày)
            {
                "mode": "L-B",
                "plate_idx": 1,
                "active": {0, 1, 2, 3},
                "flow": ("wire", 1, 2, 3),
                "kicker": "NGÀY 01  ·  QUẸT THẺ 10 TRIỆU & LỜI HỨA 45 NGÀY",
                "stage_tag": "GIỮ CHỖ HẠN MỨC 10.000.000 Đ  ·  0 ĐỒNG TIỀN THẬT DI CHUYỂN",
                "scale_title": "GIÁ TRỊ GIAO DỊCH QUẸT THẺ NGÀY 01:",
                "scale_val": 10_000_000,
                "mech_type": "P2_CONTRACT",
                "mech_left": "Cửa hàng (Quẹt máy POS)",
                "mech_right": "Ngân hàng phát hành (Giữ hạn mức)",
                "mech_badge": "GIỮ HẠN MỨC 10.000.000 Đ",
                "ledger_title": "SỔ KẾ TOÁN DOANH NGHIỆP CHỦ THẺ (TT 99/2025):",
                "debit_line": "Bên Nợ: TK 642 (Chi phí quản lý DN) = 10.000.000 đ",
                "credit_line": "Bên Có: TK 338 (Phải trả khác — 3388) = 10.000.000 đ",
                "rule": "CHƯA CÓ TIỀN RỜI TK 112  ·  MỞ KỲ ÂN HẠN TỐI ĐA 45 NGÀY",
            },
            # 2: Mode L-B (Ngày T+2: Ngân hàng đã bỏ tiền túi ứng trước)
            {
                "mode": "L-B",
                "plate_idx": 2,
                "active": {1, 2, 3},
                "flow": ("pipe", 3, 2, 1),
                "kicker": "NGÀY T+2  ·  NGÂN HÀNG PHÁT HÀNH BỎ TIỀN TÚI ỨNG TRƯỚC",
                "stage_tag": "QUYẾT TOÁN LIÊN NGÂN HÀNG T+2  ·  CỬA HÀNG NHẬN 9.800.000 Đ",
                "scale_title": "TIỀN THẬT NGÂN HÀNG ỨNG TRƯỚC TỪ T+2:",
                "scale_val": 9_800_000,
                "mech_type": "P1_SPLIT",
                "split_left_lbl": "Cửa hàng thực nhận (98%): 9.800.000 đ",
                "split_right_lbl": "MDR 2%: 200k",
                "ledger_title": "VÌ SAO NGÂN HÀNG CÓ CĂN CỨ TÍNH LÃI TỪ ĐẦU KỲ?",
                "debit_line": "Ngân hàng phát hành đã xuất tiền thật trả cửa hàng từ Ngày T+2",
                "credit_line": "Miễn lãi 45 ngày là ưu đãi có điều kiện phải trả đủ 100% ở Ngày 45",
                "rule": "SUỐT HƠN 1 THÁNG ĐÓ BẠN ĐANG TIÊU TIỀN NGÂN HÀNG ỨNG TRƯỚC",
            },
            # 3: Mode L-C (Ngày 30: Sao kê chốt sổ và hai con đường)
            {
                "mode": "L-C",
                "plate_idx": 3,
                "active": {0, 3},
                "flow": ("wire", 3, 0),
                "kicker": "NGÀY 30  ·  CHỐT SAO KÊ 10 TRIỆU & HAI CON ĐƯỜNG",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "HAI LỰA CHỌN TRÊN TỜ SAO KÊ CHO HẠN THANH TOÁN NGÀY 45",
                "card1_title": "CON ĐƯỜNG A: TRẢ ĐỦ 100% DƯ NỢ SAO KÊ",
                "card1_big": "Thanh toán 10.000.000 đ : Lãi = 0 đ",
                "card1_sub": "Giữ trọn vẹn 45 ngày miễn lãi · Hạn mức thẻ khôi phục đầy đủ cho kỳ sau",
                "card2_title": "CON ĐƯỜNG B: TRẢ TỐI THIỂU 5% DƯ NỢ",
                "card2_big": "Thanh toán 500.000 đ : Mất 45 ngày miễn lãi",
                "card2_sub": "Thoát phí phạt trễ hạn & không bị nợ quá hạn, nhưng bị tính lãi lùi về Ngày 01",
                "rule": "ĐIỀU KIỆN MIỄN LÃI ĐÒI HỎI THANH TOÁN ĐỦ 100% DƯ NỢ SAO KÊ ĐÚNG HẠN",
            },
            # 4: Mode L-B (Ngày 45: Trả 500 nghìn — thoát phạt nhưng bật đồng hồ lãi lùi)
            {
                "mode": "L-B",
                "plate_idx": 4,
                "active": {0, 3, 4},
                "flow": ("pipe", 4, 3),
                "kicker": "NGÀY 45  ·  TRẢ 500 NGHÌN & CÔNG TẮC HUỶ HỒI TỐ",
                "stage_tag": "TRẢ 500.000 Đ ĐÚNG HẠN  ·  NỢ GỐC CÒN LẠI 9.500.000 Đ",
                "scale_title": "SỐ TIỀN BẠN CHUYỂN TRẢ Ở NGÀY 45 (5%):",
                "scale_val": 500_000,
                "mech_type": "P3_FLIP",
                "mech_line1": "Đạt được: Phí phạt trễ hạn = 0 đ · Giữ nhóm nợ tiêu chuẩn",
                "mech_line2": "Đánh đổi: Mất trắng 45 ngày miễn lãi · Tính lãi lùi từ Ngày 01",
                "ledger_title": "BÚT TOÁN TRẢ TỐI THIỂU TRÊN SỔ DOANH NGHIỆP (TT 99/2025):",
                "debit_line": "Bên Nợ: TK 338 (Phải trả khác — giảm gốc thẻ) = 500.000 đ",
                "credit_line": "Bên Có: TK 112 (Tiền gửi không kỳ hạn) = 500.000 đ",
                "rule": "NỢ GỐC TRÊN TK 338 GIẢM CÒN 9.500.000 Đ NHƯNG ĐỒNG HỒ LÃI QUAY VỀ NGÀY 01",
            },
            # 5: Mode L-B (Ngày 60: Giải phẫu hai khúc tiền lãi 450.000 và 142.500)
            {
                "mode": "L-B",
                "plate_idx": 5,
                "active": {0, 3},
                "flow": ("wire", 3, 0),
                "kicker": "NGÀY 60  ·  GIẢI PHẪU HAI KHÚC LÃI 450.000 Đ & 142.500 Đ",
                "stage_tag": "DƯ NỢ BÌNH QUÂN NGÀY (ADB)  ·  TỔNG LÃI = 592.500 Đ",
                "scale_title": "TỔNG TIỀN LÃI CỘNG VÀO SAO KÊ NGÀY 60:",
                "scale_val": 592_500,
                "mech_type": "P3_FLIP",
                "mech_line1": "Khúc 1 (Ngày 01–45): 10.000.000 × 0,1%/ngày × 45 ngày = 450.000 đ",
                "mech_line2": "Khúc 2 (Ngày 46–60): 9.500.000 × 0,1%/ngày × 15 ngày = 142.500 đ",
                "ledger_title": "GHI NHẬN CHI PHÍ LÃI THẺ TÍN DỤNG KỲ 2 (TT 99/2025):",
                "debit_line": "Bên Nợ: TK 635 (Chi phí tài chính — lãi thẻ) = 592.500 đ",
                "credit_line": "Bên Có: TK 338 (Phải trả khác — cộng vào sao kê) = 592.500 đ",
                "rule": "TỔNG DƯ NỢ MỚI TRÊN TK 338 = 9.500.000 + 592.500 = 10.092.500 Đ",
            },
            # 6: Mode L-C (Cái giá thật của 15 ngày giữ lại 9,5 triệu)
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 3},
                "flow": ("wire", 3, 0),
                "kicker": "PHÂN TÍCH  ·  CÁI GIÁ THẬT CỦA 15 NGÀY TRÌ HOÃN",
                "lc_type": "P5_EIR_FORMULA",
                "headline": "ĐỐI CHIẾU QUYẾT ĐỊNH KINH TẾ TẠI NGÀY 45 (VÍ DỤ LÃI 36%/NĂM)",
                "card1_title": "CHI PHÍ BIÊN CỦA 15 NGÀY GIỮ LẠI 9.500.000 Đ",
                "card1_big": "592.500 đ / 9.500.000 đ = 6,24%",
                "card1_sub": "Bạn mất 592.500 đ tiền lãi chỉ để cầm 9.500.000 đ thêm đúng 15 ngày (Ngày 45–60)",
                "card2_title": "LÃI SUẤT THỰC TẾ NĂM KHI LÃI NHẬP GỐC (EIR)",
                "card2_big": "(1 + 3%)^12 − 1 ≈ 42,6% / năm",
                "card2_sub": "Cao hơn đáng kể so với mức lãi suất danh nghĩa 36%/năm ghi trên biểu phí",
                "rule": "TRẢ 500.000 Đ XONG, DƯ NỢ KỲ SAU (10.092.500 Đ) CAO HƠN LÚC CHƯA TRẢ 92.500 Đ",
            },
            # 7: Mode L-C (Khi giao dịch mới cũng mất quyền miễn lãi)
            {
                "mode": "L-C",
                "plate_idx": 6,
                "active": {0, 1, 3},
                "flow": ("wire", 1, 3),
                "kicker": "HIỆU ỨNG DÂY CHUYỀN  ·  GIAO DỊCH MỚI MẤT QUYỀN MIỄN LÃI",
                "lc_type": "P7_TWOWORLD_COMPARE",
                "headline": "ĐIỀU GÌ XẢY RA KHI BẠN QUẸT THÊM MÓN MỚI Ở KỲ THỨ HAI?",
                "card1_title": "KHI THẺ LUÔN TRẢ ĐỦ 100% SAO KÊ",
                "card1_big": "Món quẹt mới có 45 ngày miễn lãi",
                "card1_sub": "Mỗi giao dịch mua hàng mới đều được cấp đường băng ân hạn miễn lãi riêng",
                "card2_title": "KHI THẺ ĐANG CÒN DƯ NỢ CHUYỂN KỲ",
                "card2_big": "Món quẹt mới chịu lãi 0,1%/ngày ngay lập tức",
                "card2_sub": "Bộ đếm ân hạn miễn lãi bị khoá cho tới khi toàn bộ dư nợ sao kê về 0 đồng",
                "rule": "KHÔNG NÊN QUẸT THÊM GIAO DỊCH MỚI TRÊN CHIẾC THẺ ĐANG TRẢ TỐI THIỂU",
            },
            # 8: Mode L-C (Thiếu 10.000 đồng số lẻ và bẫy rút tiền mặt)
            {
                "mode": "L-C",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("wire", 3, 0),
                "kicker": "NGOẠI LỆ  ·  3 TÌNH HUỐNG DỄ SẬP BẪY NHẤT KHI DÙNG THẺ",
                "lc_type": "P9_TRIPTYCH",
                "headline": "THIẾU 10.000 ĐỒNG SỐ LẺ, RÚT TIỀN MẶT ATM VÀ LÃI PHẦN ĐUÔI",
                "col1_title": "1. TRẢ 9.990.000 Đ (THIẾU 10.000 Đ)",
                "col1_big": "Vẫn mất 450.150 đ tiền lãi",
                "col1_sub": "Trả thiếu 10.000 đ số lẻ vẫn làm huỷ 45 ngày miễn lãi trên toàn bộ 10.000.000 đ đầu kỳ",
                "col2_title": "2. RÚT TIỀN MẶT TẠI CÂY ATM",
                "col2_big": "Phí rút ~4% + Lãi ngày từ giây đầu",
                "col2_sub": "Giao dịch rút tiền mặt thẻ tín dụng hoàn toàn không có bất kỳ ngày ân hạn miễn lãi nào",
                "col3_title": "3. LÃI PHẦN ĐUÔI (TRAILING INTEREST)",
                "col3_big": "Phát sinh từ Ngày 60 đến ngày trả",
                "col3_sub": "Cần kiểm tra sao kê kỳ 3 để tất toán nốt tiền lãi của những ngày chờ thanh toán kỳ 2",
                "rule": "LUÔN KIỂM TRA SỐ LẺ ĐẾN HÀNG ĐƠN VỊ ĐỒNG KHI THANH TOÁN SAO KÊ THẺ",
            },
            # 9: Mode L-A (Kết luận: Câu hỏi trước khi bấm nút trả tối thiểu)
            {
                "mode": "L-A",
                "plate_idx": 7,
                "active": {0, 1, 2, 3, 4},
                "flow": ("pipe", 4, 3),
                "kicker": "KẾT LUẬN  ·  KHI NÀO DÙNG PHAO CỨU HỘ TRẢ TỐI THIỂU?",
                "stage_tag": "TẤT TOÁN 100% DƯ NỢ SAO KÊ (10.092.500 Đ) ĐỂ KHÔI PHỤC 45 NGÀY MIỄN LÃI",
                "beats": [
                    ("1. BẢN CHẤT CỦA TRẢ TỐI THIỂU 5%", "Phao cứu hộ tránh phí phạt trễ hạn & nợ xấu khi kẹt tiền mặt thật sự"),
                    ("2. CÁI GIÁ PHẢI ĐÁNH ĐỔI", "Mất trắng 45 ngày miễn lãi: trả 500.000 đ nhưng chịu 592.500 đ lãi lùi"),
                    ("3. HẠCH TOÁN KẾ TOÁN TT 99/2025", "Ghi nhận chi phí lãi vào Debit TK 635 / Credit TK 338 (592.500 đ)"),
                    ("4. CÁCH KHÔI PHỤC MIỄN LÃI", "Thanh toán dứt điểm 100% dư nợ sao kê để đưa TK 338 về 0 đồng"),
                ],
                "rule": "ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU?  ·  WHERE MONEY SLEEPS",
            },
        ],
    },
}


def step_quantize(val: float, step: int = 100_000) -> int:
    return int(round(val / step) * step)


def compute_four_beat_progress(sm: dict, t: float) -> tuple[float, float, float, float]:
    """
    Chuẩn Hoạt Cảnh 4 Nhịp Rõ Ràng (v6.5) cho bài dài 16:9:
    - Nhịp 1 bắt đầu ở `t0 + 0.40s` (ngay sau khi cross-dissolve mở ra).
    - Mỗi nhịp (`b1, b2, b3, b4`) chuyển động mượt trong `2.40s` (72 frames) thay vì 0.45s.
    """
    phrases = sm["phrases"]
    t0 = sm["win_t0"]
    t1 = sm["win_t1"]
    dur = max(0.1, t1 - t0)

    if len(phrases) >= 4:
        starts = [max(t0 + 0.40, phrases[0]["t0"]), phrases[1]["t0"], phrases[2]["t0"], phrases[3]["t0"]]
    elif len(phrases) == 3:
        starts = [max(t0 + 0.40, phrases[0]["t0"]), phrases[1]["t0"], phrases[2]["t0"], t0 + dur * 0.72]
    elif len(phrases) == 2:
        starts = [max(t0 + 0.40, phrases[0]["t0"]), t0 + dur * 0.28, phrases[1]["t0"], t0 + dur * 0.72]
    else:
        starts = [t0 + 0.40, t0 + dur * 0.26, t0 + dur * 0.50, t0 + dur * 0.74]

    b1 = ease_out_cubic((t - starts[0]) / 2.20)
    b2 = ease_out_cubic((t - starts[1]) / 2.40)
    b3 = ease_out_cubic((t - starts[2]) / 2.40)
    b4 = ease_out_cubic((t - starts[3]) / 2.40)
    return b1, b2, b3, b4


def assert_parent_child_containment(
    story_slug: str,
    story_cfg: dict,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Kiểm chứng tất định F2 (YouTube Long Safe-Zone y <= 828) + LUẬT 6b + LUẬT 8 + LUẬT 10."""
    dummy = ImageDraw.Draw(Image.new("RGBA", (16, 16)))

    for box_name, box in (
        ("ACTIVE_ACTOR_BAR", ACTIVE_ACTOR_BAR),
        ("LA_STAGE_BOX", LA_STAGE_BOX),
        ("LA_BEATS_BOX", LA_BEATS_BOX),
        ("CUTAWAY_STAGE_BOX", CUTAWAY_STAGE_BOX),
        ("MECHANISM_CANVAS_BOX", MECHANISM_CANVAS_BOX),
        ("LC_FULL_BOX", LC_FULL_BOX),
    ):
        if box[0] < SAFE_X[0] or box[2] > SAFE_X[1] or box[1] < SAFE_Y[0] or box[3] > SAFE_Y[1]:
            raise RuntimeError(
                f"FAIL [F2 YouTube 16:9 Safe-Zone]: {box_name}={box} tràn ngoài Safe Zone {SAFE_X}x{SAFE_Y} (y phải <= 828 để tránh [CC])"
            )

    if not (
        ACTIVE_ACTOR_BAR[3] + 14 <= CUTAWAY_STAGE_BOX[1]
        and CUTAWAY_STAGE_BOX[2] + 20 <= MECHANISM_CANVAS_BOX[0]
        and LA_STAGE_BOX[2] + 20 <= LA_BEATS_BOX[0]
    ):
        raise RuntimeError("FAIL [LUẬT 8 16:9 Zone Overlap]: Các khung giao diện chồng lấn nhau!")

    audit_strings: list[str] = []
    for l1, l2 in story_cfg["house_nodes"]:
        audit_strings.extend([l1, l2])
        if dummy.textlength(l1, font=fonts["actor"]) > HOUSE_BW - 24 or dummy.textlength(l2, font=fonts["small"]) > HOUSE_BW - 24:
            raise RuntimeError(f"FAIL [LUẬT 6b Top Actor Bar]: {l1}/{l2} tràn hộp HOUSE_BW={HOUSE_BW}")

    for s_i, sc in enumerate(story_cfg["scenes"]):
        for k, v in sc.items():
            if isinstance(v, str):
                audit_strings.append(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, tuple):
                        audit_strings.extend(str(x) for x in item)
        mode = sc["mode"]
        if mode == "L-A":
            iw_la = (LA_BEATS_BOX[2] - LA_BEATS_BOX[0]) - 52
            if dummy.textlength(sc["kicker"], font=fonts["badge"]) + 28 > iw_la - 16:
                raise RuntimeError(f"FAIL [LUẬT 6b L-A kicker]: scene {s_i} {sc['kicker']!r}")
            if dummy.textlength(sc["rule"], font=fonts["label"]) > iw_la - 28:
                raise RuntimeError(f"FAIL [LUẬT 6b L-A rule]: scene {s_i} {sc['rule']!r}")
            for bt, bd in sc["beats"]:
                if dummy.textlength(bt, font=fonts["label"]) > iw_la - 36 or dummy.textlength(bd, font=fonts["val_bold"]) > iw_la - 36:
                    raise RuntimeError(f"FAIL [LUẬT 6b L-A beat]: scene {s_i} {bt!r} / {bd!r}")
        elif mode == "L-B":
            iw_lb = (MECHANISM_CANVAS_BOX[2] - MECHANISM_CANVAS_BOX[0]) - 56
            kw = dummy.textlength(sc["kicker"], font=fonts["badge"]) + 28
            bw = dummy.textlength("NHỊP 4 / 4", font=fonts["badge"]) + 24
            if kw + bw + 16 > iw_lb:
                raise RuntimeError(f"FAIL [LUẬT 10 L-B header]: scene {s_i} kicker={sc['kicker']!r} ({kw:.0f}px) + badge ({bw:.0f}px) > {iw_lb}px")
            if dummy.textlength(sc["rule"], font=fonts["label"]) > iw_lb - 32:
                raise RuntimeError(f"FAIL [LUẬT 6b L-B rule]: scene {s_i} {sc['rule']!r} ({dummy.textlength(sc['rule'], font=fonts['label']):.0f}px > {iw_lb - 32}px)")
            for k_line in ("debit_line", "credit_line", "mech_line1", "mech_line2"):
                if k_line in sc and dummy.textlength(sc[k_line], font=fonts["val_bold"]) > iw_lb - 36:
                    raise RuntimeError(f"FAIL [LUẬT 6b L-B {k_line}]: scene {s_i} {sc[k_line]!r}")
        elif mode == "L-C":
            iw_lc = (LC_FULL_BOX[2] - LC_FULL_BOX[0]) - 72
            if dummy.textlength(sc["headline"], font=fonts["big_num"]) > iw_lc - 32:
                raise RuntimeError(f"FAIL [LUẬT 6b L-C headline]: scene {s_i} {sc['headline']!r}")
            if dummy.textlength(sc["rule"], font=fonts["label"]) > iw_lc - 32:
                raise RuntimeError(f"FAIL [LUẬT 6b L-C rule]: scene {s_i} {sc['rule']!r}")

    assert_broadcast_overlay_clean(audit_strings)


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


def draw_top_actor_bar(
    draw: ImageDraw.ImageDraw,
    story_cfg: dict,
    s_idx: int,
    n_scenes: int,
    s_prog: float,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """ACTIVE_ACTOR_BAR = (64, 36, 1856, 132): Thanh tiến độ dịu mắt + 5 định chế trên nền phẳng trầm (0 hạt nhấp nháy, 0 tô đặc cam chói)."""
    bx0, by0, bx1, by1 = ACTIVE_ACTOR_BAR
    draw.rounded_rectangle(ACTIVE_ACTOR_BAR, radius=16, fill=(13, 19, 30), outline=(38, 48, 66), width=1)

    seg_total_w = (bx1 - bx0) - 56
    seg_gap = 6
    seg_w = (seg_total_w - seg_gap * (n_scenes - 1)) / float(n_scenes)
    for i in range(n_scenes):
        sx0 = bx0 + 28 + i * (seg_w + seg_gap)
        sx1 = sx0 + seg_w
        if i < s_idx:
            draw.rounded_rectangle((sx0, by0 + 8, sx1, by0 + 12), radius=2, fill=(186, 138, 62))
        elif i == s_idx:
            draw.rounded_rectangle((sx0, by0 + 8, sx1, by0 + 12), radius=2, fill=(32, 42, 60))
            fill_x = sx0 + seg_w * s_prog
            draw.rounded_rectangle((sx0, by0 + 8, max(sx0 + 6, fill_x), by0 + 12), radius=2, fill=(226, 168, 76))
        else:
            draw.rounded_rectangle((sx0, by0 + 8, sx1, by0 + 12), radius=2, fill=(24, 32, 46))

    sc = story_cfg["scenes"][s_idx]
    active_set = sc["active"]
    flow_spec = sc["flow"]
    flow_kind = flow_spec[0]
    u_sig = ease_in_out_sine((t / 3.6) % 1.0)

    draw.line([(HOUSE_XS[0], NODE_Y), (HOUSE_XS[-1], NODE_Y)], fill=(38, 50, 68), width=2)

    if flow_kind in ("wire", "pipe") and len(flow_spec) >= 3:
        nodes_seq = flow_spec[1:]
        line_c = (94, 184, 138) if flow_kind == "pipe" else (226, 168, 76)
        for seg_i in range(len(nodes_seq) - 1):
            p0 = (float(HOUSE_XS[nodes_seq[seg_i]]), float(NODE_Y))
            p1 = (float(HOUSE_XS[nodes_seq[seg_i + 1]]), float(NODE_Y))
            draw.line([p0, p1], fill=line_c, width=2)
            sig_x = lerp(p0[0], p1[0], u_sig)
            tail_x = lerp(p0[0], p1[0], max(0.0, u_sig - 0.18))
            draw.line([(tail_x, NODE_Y), (sig_x, NODE_Y)], fill=line_c, width=4)
            draw.ellipse((sig_x - 8, NODE_Y - 8, sig_x + 8, NODE_Y + 8), fill=(18, 28, 42), outline=line_c, width=2)
            draw.ellipse((sig_x - 3, NODE_Y - 3, sig_x + 3, NODE_Y + 3), fill=line_c)

    house_nodes = story_cfg["house_nodes"]
    for i, hx in enumerate(HOUSE_XS):
        is_act = i in active_set
        fill_col = (22, 31, 46) if is_act else (15, 22, 34)
        out_col = (226, 168, 76) if is_act else None
        txt1_col = (226, 168, 76) if is_act else (112, 126, 146)
        txt2_col = (236, 231, 221) if is_act else (94, 108, 128)
        draw.rounded_rectangle(
            (hx - HOUSE_BW // 2, NODE_Y - HOUSE_BH // 2, hx + HOUSE_BW // 2, NODE_Y + HOUSE_BH // 2),
            radius=10,
            fill=fill_col,
            outline=out_col,
            width=1 if is_act else 0,
        )
        l1, l2 = house_nodes[i]
        draw_centered_row_text(draw, float(hx), NODE_Y - 21, l1, fonts["actor"], txt1_col)
        draw_centered_row_text(draw, float(hx), NODE_Y + 3, l2, fonts["small"], txt2_col)


def paste_stage_plate(
    canvas: Image.Image,
    plate_img: Image.Image,
    box: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    resized = plate_img.resize((w, h), Image.Resampling.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=20, fill=255)
    canvas.paste(resized, (x0, y0), mask)


def draw_cutaway_stage_decor(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    story_cfg: dict,
    sc: dict,
    sm: dict,
    s_idx: int,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """
    Chuẩn Calm Editorial Motion v6.5 cho Mặt cắt 16:9:
    - Giữ 90% bức tranh mặt cắt Risograph sạch bóng UI (0 hộp chữ đè lên tranh).
    - Đường mảnh 2px tự vẽ trong 1.8s nối 2 tâm phòng + hạt sáng (Glowing Flow Orb + đuôi sao băng) lướt êm theo chu kỳ 3.6s.
    - 1 dải chú thích đáy không viền kèm thanh quét nhịp.
    """
    sx0, sy0, sx1, sy1 = box
    sw, sh = sx1 - sx0, sy1 - sy0
    draw.rounded_rectangle(box, radius=20, fill=None, outline=(38, 48, 66), width=1)

    flow_spec = sc["flow"]
    flow_kind = flow_spec[0]
    p_src = (sx0 + sw * 0.40, sy0 + sh * 0.72)
    p_dst = (sx0 + sw * 0.68, sy0 + sh * 0.30)

    t_local = max(0.0, t - sm["win_t0"])
    line_u = ease_out_cubic((t_local - 0.30) / 1.80)
    p_cur = (lerp(p_src[0], p_dst[0], line_u), lerp(p_src[1], p_dst[1], line_u))

    line_col = (94, 184, 138) if flow_kind == "pipe" else (226, 168, 76)
    dim_line = (46, 88, 70) if flow_kind == "pipe" else (112, 84, 42)
    if line_u > 0.01:
        draw.line([p_src, p_cur], fill=dim_line, width=2)

    u_orb = ease_in_out_sine((max(0.0, t_local - 0.35) / 3.6) % 1.0)
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

    tag_txt = sc.get("stage_tag", "")
    if tag_txt:
        tw = draw.textlength(tag_txt, font=fonts["stage_tag"])
        pw = min(sw - 40, tw + 40)
        ph = 42
        px0 = (sx0 + sx1 - pw) / 2.0
        py0 = sy1 - 16 - ph
        draw.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=10, fill=(10, 14, 22))
        sweep_w = (pw - 24) * line_u
        if sweep_w > 4:
            draw.rounded_rectangle((px0 + 12, py0 + ph - 3, px0 + 12 + sweep_w, py0 + ph - 1), radius=1, fill=line_col)
        draw_centered_row_text(draw, (sx0 + sx1) / 2.0, py0 + 11, tag_txt, fonts["stage_tag"], (236, 231, 221))


def render_mode_la(
    draw: ImageDraw.ImageDraw,
    sc: dict,
    beats_prog: tuple[float, float, float, float],
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Mode L-A (Calm Editorial v6.5): Trái = Mặt cắt 1060x688; Phải = 4 Dải Nhịp Tonal mở sáng tuần tự 2.4s/nhịp."""
    bx0, by0, bx1, by1 = LA_BEATS_BOX
    draw.rounded_rectangle(LA_BEATS_BOX, radius=18, fill=(15, 21, 32), outline=(44, 56, 76), width=1)

    ix0, ix1 = bx0 + 26, bx1 - 26
    iw = ix1 - ix0
    icx = (ix0 + ix1) / 2.0

    kicker = sc["kicker"]
    kw = draw.textlength(kicker, font=fonts["badge"]) + 28
    draw.rounded_rectangle((ix0, by0 + 20, ix0 + kw, by0 + 50), radius=6, fill=(226, 168, 76))
    draw.text((ix0 + 14, by0 + 25), kicker, font=fonts["badge"], fill=(10, 14, 22))

    cards = sc["beats"]
    cy = by0 + 68
    for idx_b, (c_title, c_desc) in enumerate(cards[:4]):
        prog_b = beats_prog[idx_b]
        is_green = idx_b in (2, 3)
        bar_c = (94, 184, 138) if is_green else (226, 168, 76)
        surf_c = blend_rgb((13, 19, 29), (21, 29, 43), prog_b)
        title_c = blend_rgb((92, 104, 122), (138, 212, 174) if is_green else (226, 168, 76), prog_b)
        desc_c = blend_rgb((104, 116, 134), (236, 231, 221), prog_b)

        draw.rounded_rectangle((ix0, cy, ix1, cy + 112), radius=10, fill=surf_c)
        if prog_b > 0.02:
            bar_h = max(6.0, 88.0 * prog_b)
            draw.rounded_rectangle((ix0, cy + 12, ix0 + 4, cy + 12 + bar_h), radius=2, fill=bar_c)
            sweep_w = (iw - 36.0) * prog_b
            if sweep_w > 6.0:
                draw.rounded_rectangle((ix0 + 18, cy + 105, ix0 + 18 + sweep_w, cy + 108), radius=1, fill=blend_rgb((21, 29, 43), bar_c, 0.55 * prog_b))
        draw.text((ix0 + 18, cy + 18), c_title, font=fonts["label"], fill=title_c)
        draw.text((ix0 + 18, cy + 54), c_desc, font=fonts["val_bold"], fill=desc_c)
        cy += 126

    # Dải quy tắc chốt ở đáy (Tonal strip + Hairline 1px)
    draw.line([(ix0, by1 - 84), (ix1, by1 - 84)], fill=(44, 56, 76), width=1)
    draw.rounded_rectangle((ix0, by1 - 74, ix1, by1 - 18), radius=8, fill=blend_rgb((13, 19, 29), (21, 29, 43), beats_prog[3]))
    draw_centered_row_text(draw, icx, by1 - 55, sc["rule"], fonts["label"], (226, 168, 76))


def render_mode_lb(
    draw: ImageDraw.ImageDraw,
    sc: dict,
    beats_prog: tuple[float, float, float, float],
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """
    Mode L-B (Calm Editorial v6.5): Phải = MECHANISM_CANVAS_BOX (1044, 140, 1856, 828) (812x688px)
    4 dải Tonal Surface mở sáng tuần tự 2.4s/nhịp + thanh tách/trượt/bút toán động mượt mà.
    """
    cx0, cy0, cx1, cy1 = MECHANISM_CANVAS_BOX
    draw.rounded_rectangle(MECHANISM_CANVAS_BOX, radius=18, fill=(15, 21, 32), outline=(44, 56, 76), width=1)

    ix0, ix1 = cx0 + 28, cx1 - 28
    iw = ix1 - ix0
    icx = (ix0 + ix1) / 2.0
    b1, b2, b3, b4 = beats_prog

    kicker = sc["kicker"]
    kw = draw.textlength(kicker, font=fonts["badge"]) + 28
    draw.rounded_rectangle((ix0, cy0 + 20, ix0 + kw, cy0 + 50), radius=6, fill=(226, 168, 76))
    draw.text((ix0 + 14, cy0 + 25), kicker, font=fonts["badge"], fill=(10, 14, 22))

    # DẢI 1 (cy0 + 66..190): Quy mô gốc & Số tiền đếm mượt 2.2s
    s1_y0, s1_y1 = cy0 + 66, cy0 + 190
    draw.rounded_rectangle((ix0, s1_y0, ix1, s1_y1), radius=10, fill=(21, 29, 43))
    bar1_h = max(8.0, (s1_y1 - s1_y0 - 28.0) * max(0.15, b1))
    draw.rounded_rectangle((ix0, s1_y0 + 14, ix0 + 4, s1_y0 + 14 + bar1_h), radius=2, fill=(226, 168, 76))
    draw_centered_row_text(draw, icx, s1_y0 + 16, sc["scale_title"], fonts["label"], (148, 160, 178))
    val_anim = step_quantize(float(sc["scale_val"]) * max(0.08, b1), 100_000) if b1 < 0.99 else int(sc["scale_val"])
    draw_centered_row_text(draw, icx, s1_y0 + 54, fmt_vnd(val_anim), fonts["hero_num"], (236, 231, 221))

    # DẢI 2 (cy0 + 204..382): Nguyên hàm Cơ chế (P1_SPLIT / P2_CONTRACT / P3_FLIP)
    s2_u = max(0.0, min(1.0, b2))
    s2_y0, s2_y1 = cy0 + 204, cy0 + 382
    draw.rounded_rectangle((ix0, s2_y0, ix1, s2_y1), radius=10, fill=blend_rgb((13, 19, 29), (21, 29, 43), s2_u))
    if s2_u > 0.02:
        bar2_h = max(8.0, (s2_y1 - s2_y0 - 28.0) * s2_u)
        draw.rounded_rectangle((ix0, s2_y0 + 14, ix0 + 4, s2_y0 + 14 + bar2_h), radius=2, fill=(94, 184, 138))

    c_lbl2 = blend_rgb((88, 100, 118), (148, 160, 178), s2_u)
    c_val2 = blend_rgb((102, 114, 132), (236, 231, 221), s2_u)
    c_acc2 = blend_rgb((102, 114, 132), (226, 168, 76), s2_u)
    c_grn2 = blend_rgb((92, 112, 104), (138, 212, 174), s2_u)

    m_type = sc["mech_type"]
    if m_type == "P1_SPLIT":
        draw_centered_row_text(draw, icx, s2_y0 + 14, "TÁCH DÒNG TIỀN TỶ LỆ THẬT TẠI NGUỒN:", fonts["label"], c_lbl2)
        u_sp = max(0.15 * b1, s2_u)
        gap_px = lerp(2.0, 14.0, s2_u)
        w_left = (iw - 36 - gap_px) * lerp(0.95, 0.74, s2_u)
        bx_bar0 = ix0 + 18
        bx_bar1 = ix1 - 18
        by_bar0, by_bar1 = s2_y0 + 52, s2_y0 + 120
        draw.rounded_rectangle((bx_bar0, by_bar0, bx_bar0 + w_left, by_bar1), radius=8, fill=blend_rgb((20, 38, 34), (32, 88, 68), u_sp))
        draw.rounded_rectangle((bx_bar0 + w_left + gap_px, by_bar0, bx_bar1, by_bar1), radius=8, fill=blend_rgb((28, 26, 24), (146, 98, 36), s2_u))
        draw_centered_row_text(draw, bx_bar0 + w_left / 2.0, by_bar0 + 23, sc["split_left_lbl"], fonts["val_bold"], c_val2)
        if s2_u > 0.12:
            draw_centered_row_text(draw, (bx_bar0 + w_left + gap_px + bx_bar1) / 2.0, by_bar0 + 23, sc["split_right_lbl"], fonts["label"], c_acc2)
        draw_centered_row_text(draw, icx, s2_y0 + 138, "Khoản khấu trừ được giữ lại tự động trước khi tiền về tài khoản", fonts["sub"], c_lbl2)

    elif m_type == "P2_CONTRACT":
        draw.text((ix0 + 20, s2_y0 + 16), f"1. {sc['mech_left']}", font=fonts["label"], fill=c_lbl2)
        r_txt = f"2. {sc['mech_right']}"
        rw = draw.textlength(r_txt, font=fonts["label"])
        draw.text((ix1 - 20 - rw, s2_y0 + 16), r_txt, font=fonts["label"], fill=c_acc2)
        rail_x0, rail_x1 = ix0 + 140, ix1 - 140
        rail_y = s2_y0 + 94
        draw.line([(rail_x0, rail_y), (rail_x1, rail_y)], fill=(56, 72, 96), width=2)
        u_rail = max(0.25 * b1, s2_u)
        cx_card = lerp(rail_x0, rail_x1, u_rail)
        draw.line([(rail_x0, rail_y), (cx_card, rail_y)], fill=(226, 168, 76), width=4)
        cw_b, ch_b = 276, 48
        draw.rounded_rectangle((cx_card - cw_b / 2, rail_y - ch_b / 2, cx_card + cw_b / 2, rail_y + ch_b / 2), radius=8, fill=blend_rgb((64, 72, 86), (226, 168, 76), u_rail))
        draw_centered_row_text(draw, cx_card, rail_y - 10, sc["mech_badge"], fonts["badge"], (10, 14, 22))
        draw_centered_row_text(draw, icx, s2_y0 + 138, "Bản tin / Hợp đồng điện tử xác lập nghĩa vụ pháp lý", fonts["sub"], c_lbl2)

    else:  # P3_FLIP
        draw_centered_row_text(draw, icx, s2_y0 + 16, "ĐỐI CHIẾU HAI VẾ TRÊN SỔ KẾ TOÁN:", fonts["label"], c_lbl2)
        draw.rounded_rectangle((ix0 + 18, s2_y0 + 50, ix1 - 18, s2_y0 + 102), radius=8, fill=(15, 21, 32))
        w_f1 = (iw - 44) * max(0.15 * b1, s2_u)
        draw.rounded_rectangle((ix0 + 22, s2_y0 + 96, ix0 + 22 + w_f1, s2_y0 + 99), radius=1, fill=(226, 168, 76))
        draw_centered_row_text(draw, icx, s2_y0 + 63, sc["mech_line1"], fonts["val_bold"], c_acc2)
        draw.rounded_rectangle((ix0 + 18, s2_y0 + 112, ix1 - 18, s2_y0 + 164), radius=8, fill=(15, 21, 32))
        draw.rounded_rectangle((ix0 + 22, s2_y0 + 158, ix0 + 22 + w_f1, s2_y0 + 161), radius=1, fill=(94, 184, 138))
        draw_centered_row_text(draw, icx, s2_y0 + 125, sc["mech_line2"], fonts["val_bold"], c_grn2)

    # DẢI 3 (cy0 + 396..576): Bảng Bút toán Kép T-Account TT 99/2025/TT-BTC
    s3_u = max(0.0, min(1.0, b3))
    s3_y0, s3_y1 = cy0 + 396, cy0 + 576
    draw.rounded_rectangle((ix0, s3_y0, ix1, s3_y1), radius=10, fill=blend_rgb((13, 19, 29), (21, 29, 43), s3_u))
    if s3_u > 0.02:
        bar3_h = max(8.0, (s3_y1 - s3_y0 - 28.0) * s3_u)
        draw.rounded_rectangle((ix0, s3_y0 + 14, ix0 + 4, s3_y0 + 14 + bar3_h), radius=2, fill=(94, 184, 138))
    c_lbl3 = blend_rgb((88, 100, 118), (148, 160, 178), s3_u)
    c_deb3 = blend_rgb((102, 114, 132), (226, 168, 76), s3_u)
    c_crd3 = blend_rgb((92, 112, 104), (138, 212, 174), s3_u)

    draw_centered_row_text(draw, icx, s3_y0 + 14, sc["ledger_title"], fonts["label"], c_lbl3)
    draw.line([(ix0 + 24, s3_y0 + 46), (ix1 - 24, s3_y0 + 46)], fill=(38, 50, 68), width=1)
    if s3_u > 0.02:
        draw.line([(ix0 + 24, s3_y0 + 46), (ix0 + 24 + (iw - 48) * s3_u, s3_y0 + 46)], fill=(94, 184, 138), width=2)
    draw_centered_row_text(draw, icx, s3_y0 + 62, sc["debit_line"], fonts["val_bold"], c_deb3)
    draw_centered_row_text(draw, icx, s3_y0 + 104, sc["credit_line"], fonts["val_bold"], c_crd3)
    draw_centered_row_text(draw, icx, s3_y0 + 144, "Nguyên tắc bút toán kép: Σ Phát sinh Nợ = Σ Phát sinh Có", fonts["sub"], c_lbl3)

    # DẢI 4 (cy0 + 592..666): Quy tắc chốt ở đáy hộp
    s4_u = max(0.0, min(1.0, b4))
    s4_y0, s4_y1 = cy0 + 592, cy0 + 666
    draw.line([(ix0, s4_y0 - 6), (ix1, s4_y0 - 6)], fill=(44, 56, 76), width=1)
    draw.rounded_rectangle((ix0, s4_y0, ix1, s4_y1), radius=8, fill=blend_rgb((13, 19, 29), (21, 29, 43), s4_u))
    draw_centered_row_text(draw, icx, s4_y0 + 26, sc["rule"], fonts["label"], blend_rgb((104, 116, 134), (226, 168, 76), s4_u))


def render_mode_lc(
    draw: ImageDraw.ImageDraw,
    sc: dict,
    beats_prog: tuple[float, float, float, float],
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Mode L-C (Calm Editorial v6.5): Sân khấu phân tích định lượng toàn chiều ngang LC_FULL_BOX = (64, 140, 1856, 828)."""
    fx0, fy0, fx1, fy1 = LC_FULL_BOX
    draw.rounded_rectangle(LC_FULL_BOX, radius=18, fill=(15, 21, 32), outline=(44, 56, 76), width=1)

    ix0, ix1 = fx0 + 36, fx1 - 36
    iw = ix1 - ix0
    icx = (ix0 + ix1) / 2.0
    b1, b2, b3, b4 = beats_prog

    kicker = sc["kicker"]
    kw = draw.textlength(kicker, font=fonts["badge"]) + 32
    draw.rounded_rectangle((ix0, fy0 + 22, ix0 + kw, fy0 + 52), radius=6, fill=(226, 168, 76))
    draw.text((ix0 + 16, fy0 + 27), kicker, font=fonts["badge"], fill=(10, 14, 22))

    draw_centered_row_text(draw, icx, fy0 + 74, sc["headline"], fonts["big_num"], (236, 231, 221))

    lc_type = sc["lc_type"]
    if lc_type == "P5_LADDER_12M":
        # Biểu đồ 12 cột dòng tiền trả góp 1.000.000 đ/tháng + chiết khấu giá trị hiện tại PV mọc tuần tự
        chart_y0, chart_y1 = fy0 + 132, fy0 + 472
        draw.rounded_rectangle((ix0, chart_y0, ix1, chart_y1), radius=12, fill=(21, 29, 43))
        u_12 = max(b1 * 0.45, b2, b3)
        col_w = (iw - 64) / 12.0
        for m_i in range(12):
            cx_a = ix0 + 32 + m_i * col_w + 8
            cx_b = cx_a + col_w - 16
            col_u = max(0.0, min(1.0, u_12 * 12.0 - m_i))
            pv_ratio = 1.0 / ((1.0 + 0.008) ** (m_i + 1))
            full_h = 210
            pv_h = int(full_h * pv_ratio * max(0.15, col_u))
            by_bot = chart_y1 - 54
            by_top_nom = by_bot - full_h
            by_top_pv = by_bot - pv_h
            draw.rounded_rectangle((cx_a, by_top_nom, cx_b, by_bot), radius=6, fill=(32, 44, 62))
            if col_u > 0.02:
                draw.rounded_rectangle((cx_a, by_top_pv, cx_b, by_bot), radius=6, fill=(52, 124, 96))
            draw_centered_row_text(draw, (cx_a + cx_b) / 2.0, by_top_nom - 26, "1,0tr", fonts["small"], (226, 168, 76))
            draw_centered_row_text(draw, (cx_a + cx_b) / 2.0, by_bot + 14, f"Kỳ {m_i+1}", fonts["label"], (236, 231, 221) if col_u > 0.4 else (112, 124, 142))

        # 2 dải Tonal đối xứng dưới biểu đồ
        sub_y0, sub_y1 = fy0 + 490, fy0 + 584
        half_w = (iw - 24) / 2.0
        draw.rounded_rectangle((ix0, sub_y0, ix0 + half_w, sub_y1), radius=10, fill=blend_rgb((13, 19, 29), (21, 29, 43), max(0.2, b2)))
        draw.rounded_rectangle((ix0, sub_y0 + 14, ix0 + 4, sub_y0 + 14 + (sub_y1 - sub_y0 - 28) * max(0.2, b2)), radius=2, fill=(94, 184, 138))
        draw_centered_row_text(draw, ix0 + half_w / 2.0, sub_y0 + 34, sc["sub_left"], fonts["val_bold"], (138, 212, 174))

        draw.rounded_rectangle((ix0 + half_w + 24, sub_y0, ix1, sub_y1), radius=10, fill=blend_rgb((13, 19, 29), (21, 29, 43), max(0.2, b3)))
        draw.rounded_rectangle((ix0 + half_w + 24, sub_y0 + 14, ix0 + half_w + 28, sub_y0 + 14 + (sub_y1 - sub_y0 - 28) * max(0.2, b3)), radius=2, fill=(226, 168, 76))
        draw_centered_row_text(draw, ix0 + half_w + 24 + half_w / 2.0, sub_y0 + 34, sc["sub_right"], fonts["val_bold"], (226, 168, 76))

    elif lc_type in ("P5_EIR_FORMULA", "P7_TWOWORLD_COMPARE"):
        half_w = (iw - 28) / 2.0
        c1_x0, c1_x1 = ix0, ix0 + half_w
        c2_x0, c2_x1 = ix0 + half_w + 28, ix1
        cy_top, cy_bot = fy0 + 138, fy0 + 576

        u1 = max(0.15, b1)
        draw.rounded_rectangle((c1_x0, cy_top, c1_x1, cy_bot), radius=14, fill=blend_rgb((13, 19, 29), (21, 29, 43), u1))
        draw.rounded_rectangle((c1_x0, cy_top + 20, c1_x0 + 4, cy_top + 20 + (cy_bot - cy_top - 40) * u1), radius=2, fill=(226, 168, 76))
        draw.rounded_rectangle((c1_x0 + 24, cy_bot - 6, c1_x0 + 24 + (half_w - 48) * u1, cy_bot - 2), radius=2, fill=blend_rgb((21, 29, 43), (226, 168, 76), 0.55 * u1))
        draw_centered_row_text(draw, (c1_x0 + c1_x1) / 2.0, cy_top + 48, sc["card1_title"], fonts["label"], (226, 168, 76))
        draw_centered_row_text(draw, (c1_x0 + c1_x1) / 2.0, cy_top + 144, sc["card1_big"], fonts["hero_num"], (236, 231, 221))
        draw_centered_row_text(draw, (c1_x0 + c1_x1) / 2.0, cy_top + 258, sc["card1_sub"], fonts["sub"], (148, 160, 178))

        u2 = max(0.0, min(1.0, max(b2, b3)))
        draw.rounded_rectangle((c2_x0, cy_top, c2_x1, cy_bot), radius=14, fill=blend_rgb((13, 19, 29), (21, 29, 43), u2))
        if u2 > 0.02:
            draw.rounded_rectangle((c2_x0, cy_top + 20, c2_x0 + 4, cy_top + 20 + (cy_bot - cy_top - 40) * u2), radius=2, fill=(94, 184, 138))
            draw.rounded_rectangle((c2_x0 + 24, cy_bot - 6, c2_x0 + 24 + (half_w - 48) * u2, cy_bot - 2), radius=2, fill=blend_rgb((21, 29, 43), (94, 184, 138), 0.55 * u2))
        draw_centered_row_text(draw, (c2_x0 + c2_x1) / 2.0, cy_top + 48, sc["card2_title"], fonts["label"], blend_rgb((96, 112, 128), (138, 212, 174), u2))
        draw_centered_row_text(draw, (c2_x0 + c2_x1) / 2.0, cy_top + 144, sc["card2_big"], fonts["hero_num"], blend_rgb((104, 116, 134), (138, 212, 174), u2))
        draw_centered_row_text(draw, (c2_x0 + c2_x1) / 2.0, cy_top + 258, sc["card2_sub"], fonts["sub"], blend_rgb((88, 100, 118), (148, 160, 178), u2))

    else:  # P9_TRIPTYCH (3 cột Triptych mở sáng tuần tự b1 -> b2 -> b3)
        col_w = (iw - 48) / 3.0
        cy_top, cy_bot = fy0 + 138, fy0 + 576
        cols_data = [
            (sc["col1_title"], sc["col1_big"], sc["col1_sub"], max(0.15, b1), (226, 168, 76)),
            (sc["col2_title"], sc["col2_big"], sc["col2_sub"], b2, (214, 118, 92)),
            (sc["col3_title"], sc["col3_big"], sc["col3_sub"], b3, (94, 184, 138)),
        ]
        for idx_c, (ctitle, cbig, csub, cprog, rgb_c) in enumerate(cols_data):
            cx_a = ix0 + idx_c * (col_w + 24)
            cx_b = cx_a + col_w
            ccx = (cx_a + cx_b) / 2.0
            cu = max(0.0, min(1.0, cprog))
            draw.rounded_rectangle((cx_a, cy_top, cx_b, cy_bot), radius=12, fill=blend_rgb((13, 19, 29), (21, 29, 43), cu))
            if cu > 0.02:
                bar_cw = (col_w - 40) * cu
                draw.rounded_rectangle((ccx - bar_cw / 2.0, cy_top, ccx + bar_cw / 2.0, cy_top + 4), radius=2, fill=rgb_c)
            draw_centered_row_text(draw, ccx, cy_top + 44, ctitle, fonts["label"], blend_rgb((96, 110, 128), rgb_c, cu))
            draw_centered_row_text(draw, ccx, cy_top + 134, cbig, fonts["big_num"], blend_rgb((104, 116, 134), (236, 231, 221), cu))
            words_s = csub.split()
            mid_w = len(words_s) // 2
            l_a = " ".join(words_s[:mid_w])
            l_b = " ".join(words_s[mid_w:])
            draw_centered_row_text(draw, ccx, cy_top + 236, l_a, fonts["sub"], blend_rgb((88, 100, 118), (148, 160, 178), cu))
            draw_centered_row_text(draw, ccx, cy_top + 272, l_b, fonts["sub"], blend_rgb((88, 100, 118), (148, 160, 178), cu))

    # Dải quy tắc chốt ở đáy sân khấu L-C
    draw.line([(ix0, fy1 - 86), (ix1, fy1 - 86)], fill=(44, 56, 76), width=1)
    draw.rounded_rectangle((ix0, fy1 - 76, ix1, fy1 - 18), radius=8, fill=blend_rgb((13, 19, 29), (21, 29, 43), max(0.2, b4)))
    draw_centered_row_text(draw, icx, fy1 - 57, sc["rule"], fonts["label"], (226, 168, 76))


def render_single_scene_frame(
    story_cfg: dict,
    s_idx: int,
    t: float,
    scene_meta: list[dict],
    scene_bgs: list[Image.Image],
    fonts: dict[str, ImageFont.FreeTypeFont],
    W: int,
    H: int,
) -> Image.Image:
    sm = scene_meta[s_idx]
    s_dur = max(0.01, sm["win_t1"] - sm["win_t0"])
    s_prog = max(0.0, min(1.0, (t - sm["win_t0"]) / s_dur))
    beats_prog = compute_four_beat_progress(sm, t)

    sc = story_cfg["scenes"][min(s_idx, len(story_cfg["scenes"]) - 1)]
    mode = sc["mode"]

    base_rgb = scene_bgs[s_idx].copy()
    draw = ImageDraw.Draw(base_rgb)

    draw_top_actor_bar(draw, story_cfg, s_idx, len(scene_meta), s_prog, t, fonts)

    if mode == "L-A":
        draw_cutaway_stage_decor(draw, LA_STAGE_BOX, story_cfg, sc, sm, s_idx, t, fonts)
        render_mode_la(draw, sc, beats_prog, fonts)
    elif mode == "L-B":
        draw_cutaway_stage_decor(draw, CUTAWAY_STAGE_BOX, story_cfg, sc, sm, s_idx, t, fonts)
        render_mode_lb(draw, sc, beats_prog, fonts)
    else:
        render_mode_lc(draw, sc, beats_prog, fonts)

    return base_rgb


def render_smooth_long_video(
    story_slug: str,
    story: dict,
    scene_meta: list[dict],
    total_dur: float,
    master_wav: pathlib.Path,
    out_mp4: pathlib.Path,
) -> None:
    W, H = 1920, 1080
    FPS = 30
    total_frames = int(round(total_dur * FPS))

    story_cfg = LONG_STORY_CONFIGS[story_slug]
    plates_loaded: list[Image.Image] = []
    for rel_path, crop_box in story_cfg["plates_pool"]:
        if "fig-" in rel_path:
            raise RuntimeError(f"FAIL [Zero Baked-In Text]: Cấm dùng ảnh fig có chữ nướng sẵn: {rel_path}")
        pp = ROOT / rel_path
        im_src = Image.open(pp).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
        plates_loaded.append(im_src.crop(crop_box))

    # Pre-bake nền cảnh RGB cho từng scene trước vòng lặp để tăng tốc >5x (không tốn alpha_composite mỗi frame)
    scene_bgs: list[Image.Image] = []
    for s_idx in range(len(scene_meta)):
        sc = story_cfg["scenes"][min(s_idx, len(story_cfg["scenes"]) - 1)]
        mode = sc["mode"]
        plate_img = plates_loaded[sc["plate_idx"] % len(plates_loaded)]
        bg_c = Image.new("RGBA", (W, H), (10, 14, 22, 255))
        if mode == "L-A":
            paste_stage_plate(bg_c, plate_img, LA_STAGE_BOX)
        elif mode == "L-B":
            paste_stage_plate(bg_c, plate_img, CUTAWAY_STAGE_BOX)
        scene_bgs.append(bg_c.convert("RGB"))

    fonts = {
        "actor": get_font(16, bold=True),
        "stage_tag": get_font(17, bold=True),
        "badge": get_font(16, bold=True),
        "label": get_font(17, bold=True),
        "sub": get_font(18, bold=False),
        "val_bold": get_font(20, bold=True),
        "big_num": get_font(25, bold=True),
        "hero_num": get_font(34, bold=True),
        "small": get_font(15, bold=True),
    }

    assert_parent_child_containment(story_slug, story_cfg, fonts)

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

    TRANS_HALF = 0.45
    t0_wall = time.time()
    black_rgb = Image.new("RGB", (W, H), (8, 12, 20))

    for f_idx in range(total_frames):
        t = f_idx / FPS

        blended_rgb: Image.Image | None = None
        for b_idx in range(len(scene_meta) - 1):
            b_t = scene_meta[b_idx]["win_t1"]
            if (b_t - TRANS_HALF) <= t <= (b_t + TRANS_HALF):
                alpha = smoothstep(b_t - TRANS_HALF, b_t + TRANS_HALF, t)
                img_a = render_single_scene_frame(story_cfg, b_idx, t, scene_meta, scene_bgs, fonts, W, H)
                img_b = render_single_scene_frame(story_cfg, b_idx + 1, t, scene_meta, scene_bgs, fonts, W, H)
                blended_rgb = Image.blend(img_a, img_b, alpha)
                break

        if blended_rgb is None:
            cur_s_idx = 0
            for idx, sm in enumerate(scene_meta):
                if sm["win_t0"] <= t <= sm["win_t1"] or idx == len(scene_meta) - 1:
                    cur_s_idx = idx
                    break
            blended_rgb = render_single_scene_frame(story_cfg, cur_s_idx, t, scene_meta, scene_bgs, fonts, W, H)

        if t < 0.35:
            blended_rgb = Image.blend(black_rgb, blended_rgb, smoothstep(0.0, 0.35, t))
        elif t > total_dur - 0.65:
            blended_rgb = Image.blend(blended_rgb, black_rgb, smoothstep(total_dur - 0.65, total_dur, t))

        proc.stdin.write(blended_rgb.tobytes())

        if (f_idx + 1) % 900 == 0 or f_idx == total_frames - 1:
            elapsed = time.time() - t0_wall
            fps_actual = (f_idx + 1) / max(0.01, elapsed)
            print(f"  -> [{story_slug}.long] Rendered frame {f_idx + 1}/{total_frames} ({t:.1f}s / {total_dur:.1f}s, {fps_actual:.1f} fps)")

    proc.stdin.close()
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"FFmpeg failed with code {ret}:\n{stderr_out[-1200:]}")


def ensure_long_continuous_tts(slug: str, scenes: list[dict], api_key: str) -> pathlib.Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    merged_cache = CACHE_DIR / f"{slug}_long_continuous_v3.json"
    if merged_cache.is_file():
        return merged_cache

    split_idx = len(scenes) // 2
    part1_text = "\n\n".join(s["vo"].strip() for s in scenes[:split_idx])
    part2_text = "\n\n".join(s["vo"].strip() for s in scenes[split_idx:])

    def call_tts_part(part_name: str, text: str) -> dict:
        part_cache = CACHE_DIR / f"{slug}_long_{part_name}_v3.json"
        if part_cache.is_file():
            return json.loads(part_cache.read_text(encoding="utf-8"))
        print(f"  [TTS Continuous Long {part_name}] Calling ElevenLabs eleven_v3 ({len(text)} chars)...")
        url = "https://api.elevenlabs.io/v1/text-to-speech/JwqRvOqFdGeQNu7UjKjw/with-timestamps"
        payload = {
            "text": text,
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
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=240) as resp:
            raw = resp.read().decode("utf-8")
        part_cache.write_text(raw, encoding="utf-8")
        return json.loads(raw)

    d1 = call_tts_part("part1", part1_text)
    d2 = call_tts_part("part2", part2_text)

    with tempfile.TemporaryDirectory(prefix=f"wms_stitch_{slug}_") as tmp:
        tmp_dir = pathlib.Path(tmp)
        mp3_1 = tmp_dir / "p1.mp3"
        mp3_2 = tmp_dir / "p2.mp3"
        wav_1 = tmp_dir / "p1.wav"
        wav_2 = tmp_dir / "p2.wav"
        mp3_1.write_bytes(base64.b64decode(d1["audio_base64"]))
        mp3_2.write_bytes(base64.b64decode(d2["audio_base64"]))
        subprocess.run(["ffmpeg", "-y", "-i", str(mp3_1), "-ar", "44100", "-ac", "1", str(wav_1)], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-i", str(mp3_2), "-ar", "44100", "-ac", "1", str(wav_2)], check=True, capture_output=True)

        with wave.open(str(wav_1), "rb") as w1:
            sr = w1.getframerate()
            pcm1 = np.frombuffer(w1.readframes(w1.getnframes()), dtype=np.int16)
        with wave.open(str(wav_2), "rb") as w2:
            pcm2 = np.frombuffer(w2.readframes(w2.getnframes()), dtype=np.int16)

        dur1 = len(pcm1) / sr
        bridge_s = 0.40
        bridge_samples = np.zeros(int(sr * bridge_s), dtype=np.int16)
        merged_pcm = np.concatenate([pcm1, bridge_samples, pcm2])

        merged_wav = tmp_dir / "merged.wav"
        with wave.open(str(merged_wav), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(merged_pcm.tobytes())

        merged_mp3 = tmp_dir / "merged.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(merged_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(merged_mp3)],
            check=True,
            capture_output=True,
        )
        merged_b64 = base64.b64encode(merged_mp3.read_bytes()).decode("ascii")

    a1 = d1["alignment"]
    a2 = d2["alignment"]
    offset = dur1 + bridge_s
    merged_chars = list(a1["characters"]) + ["\n", "\n"] + list(a2["characters"])
    merged_starts = list(a1["character_start_times_seconds"]) + [dur1, dur1 + 0.20] + [
        round(t + offset, 4) for t in a2["character_start_times_seconds"]
    ]
    merged_ends = list(a1["character_end_times_seconds"]) + [dur1 + 0.20, offset] + [
        round(t + offset, 4) for t in a2["character_end_times_seconds"]
    ]
    merged_obj = {
        "audio_base64": merged_b64,
        "alignment": {
            "characters": merged_chars,
            "character_start_times_seconds": merged_starts,
            "character_end_times_seconds": merged_ends,
        },
    }
    merged_cache.write_text(json.dumps(merged_obj, ensure_ascii=False), encoding="utf-8")
    return merged_cache


def run_for_story(wmp, stories: dict, sfx_map: dict[str, bytes], slug: str) -> None:
    story = stories[slug]
    brand_audit = wmp.step_5_0_brand_safety_audit(slug, story)
    print(f"\n=== [{slug.upper()}.LONG 16:9 — Broadcast-Grade v5.0 3-Mode Cinema (QĐ 61)] ===")
    print(f"[0/3 Brand Safety Specialist PASS] B1–B4 sạch ({brand_audit['scenesAudited']} cảnh, 0 tên riêng/thương hiệu)")
    scenes = story["videoScript"]["long"]["scenes"]

    wmp.load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    cont_path = ensure_long_continuous_tts(slug, scenes, api_key)
    cont_data = json.loads(cont_path.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory(prefix=f"wms_smooth_long_{slug}_") as tmp:
        tmp_dir = pathlib.Path(tmp)
        master_wav, scene_meta, total_dur = build_timeline_and_master_audio(scenes, cont_data, sfx_map, tmp_dir)
        print(f"  -> Master audio ready: {total_dur:.2f}s (-14 LUFS, {len(scene_meta)} scenes)")
        out_mp4 = DIST_DIR / f"{slug}-long-16x9.mp4"
        print(f"[2/3] Rendering 30fps 16:9 video ({int(round(total_dur * 30))} frames) -> {out_mp4} ...")
        render_smooth_long_video(slug, story, scene_meta, total_dur, master_wav, out_mp4)

    print(f"[3/3] Done! Output saved to {out_mp4} ({out_mp4.stat().st_size:,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", default="install", choices=["install", "card", "pay", "minpay", "all"])
    args = parser.parse_args()

    wmp = load_pipeline_module()
    stories = wmp.extract_stories((ROOT / "docs/prototype.html").read_text(encoding="utf-8"))
    sfx_map = load_cached_sfx()

    target_slugs = ["install", "card", "pay", "minpay"] if args.story == "all" else [args.story]
    for slug in target_slugs:
        run_for_story(wmp, stories, sfx_map, slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
