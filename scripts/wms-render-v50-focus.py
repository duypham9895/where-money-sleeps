#!/usr/bin/env python3
"""
wms-render-v50-focus.py — Prototype v5.1 (Zero Zone 3 · 100% Unified Single-Focus Stage)

Sửa triệt để hai lỗi từ phản hồi thực tế:
1. XOÁ HOÀN TOÀN Zone 3 (`SUBTITLE_BOX` / hộp chạy chữ ở đáy màn hình):
   - Không đốt phụ đề chạy từng từ vào đáy video (không phân tâm, không cắt giữa câu).
   - Tự động xuất file phụ đề rời `.srt` (`dist/youtube/card-short-9x16.srt`, `card-long-16x9.srt`)
     để người xem chủ động bật nút [CC] trên YouTube khi muốn đọc lời thoại chi tiết.
2. HỢP NHẤT SÂN KHẤU `Zone 2` THÀNH 1 TÂM ĐIỂM DUY NHẤT (Zero Split-Attention):
   - Gỡ bỏ hoàn toàn cấu trúc hộp-lồng-hộp và bỏ dòng mô tả dài cạnh tranh mắt nhìn.
   - Bên trong `STAGE_BOX` chỉ có một mặt phẳng duy nhất gồm 3 tầng thoáng mắt:
     + Tầng trên: 1 Tiêu đề ngắn cực to (`<= 6 từ`) đổi mượt theo 2 nhịp chính của lời bình (`Beat 1 -> Beat 2`).
     + Tâm điểm giữa: Tối đa 2–4 định chế 2D tối giản có nhãn trực tiếp to rõ + hoạt cảnh nhịp thở/vầng sáng
       trên chủ thể đang hoạt động (chủ thể phụ làm mờ ~28%) + luồng hạt/tiền xu/xung điện chạy 30fps.
     + Tầng dưới: 1 Con số đếm động (`kinetic counter`) hoặc thanh tỷ lệ trực quan duy nhất.
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
import unicodedata
import wave
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _resolve_main_root(repo_root: pathlib.Path = ROOT) -> pathlib.Path:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--git-common-dir"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            gd = pathlib.Path(res.stdout.strip())
            resolved = gd.resolve() if gd.is_absolute() else (repo_root / gd).resolve()
            if resolved.name == ".git":
                return resolved.parent
    except Exception:
        pass
    return repo_root


def _resolve_shared_dir(rel_path: str) -> pathlib.Path:
    cand = ROOT / rel_path
    if cand.exists() and (not cand.is_dir() or any(cand.iterdir())):
        return cand
    return _resolve_main_root(ROOT) / rel_path


CACHE_DIR = _resolve_shared_dir(".cache/elevenlabs")
TTS_CACHE_DIR = _resolve_shared_dir(".cache/tts")
DIST_DIR = ROOT / "dist/youtube"

# ── BẢNG MÀU GIẤY ẤM & MỰC IN TƯƠNG PHẢN CAO ────────────────────────────────
PAPER_BG = (245, 239, 226)       # #F5EFE2 giấy kem ấm
PAPER_CARD = (252, 249, 242)     # #FCF9F2 mặt sân khấu sáng nhẹ
PAPER_FLOOR = (246, 241, 229)    # #F6F1E5 vùng sàn tầng dưới sân khấu (0 dùng khung viền đen lồng)
PAPER_SOFT = (233, 224, 206)     # #E9E0CE nền phụ dịu
INK = (30, 29, 26)               # #1E1D1A mực đen ấm
INK_MUTED = (104, 98, 88)        # #686258 chữ phụ

AMBER = (214, 146, 30)           # Tín hiệu wire / giữ hạn mức / nhấn chính
AMBER_LIGHT = (248, 226, 178)
GREEN = (38, 130, 88)            # Tiền thật chảy về két / tiền hoàn
GREEN_LIGHT = (206, 236, 220)
CORAL = (208, 66, 62)            # Khấu trừ phí MDR / chi phí
CORAL_LIGHT = (249, 214, 212)
NAVY = (38, 72, 118)             # Ngân hàng của bạn / tiêu đề tổng kết
TEAL = (40, 102, 112)            # Ngân hàng của quán / bù trừ
TERRACOTTA = (196, 86, 52)       # Quán quen / vòng tròn giá
GOLD = (242, 188, 62)            # Đồng tiền vàng & điểm sáng

# ── BỐ CỤC ĐỐI XỨNG TUYỆT ĐỐI TÂM (W/2, H/2) · ZERO ZONE 3 ──────────────────
LAYOUT_SHORT = {
    "W": 1080,
    "H": 1920,
    "HUD_BOX": (72, 390, 1008, 506),     # 936 x 116 px | lề trái=phải=72, lề trên=dưới=390, tâm (540, 960)
    "STAGE_BOX": (72, 530, 1008, 1530),  # 936 x 1000 px | dải đáy 390px đối xứng hoàn hảo
}

LAYOUT_LONG = {
    "W": 1920,
    "H": 1080,
    "HUD_BOX": (96, 116, 1824, 200),     # 1728 x 84 px | lề trái=phải=96, lề trên=dưới=116, tâm (960, 540)
    "STAGE_BOX": (96, 224, 1824, 964),   # 1728 x 740 px | lề trên=dưới=116
}

SLATE_LEAK_RE = re.compile(
    r"(\bCẢNH\s*\d|\bSCENE\s*\d|\bMỐC\s*\d|\bÝ\s*\d+\s*/\s*\d+|\bKỲ\s*\d+\s*/\s*\d+|"
    r"Chữ\s+to|SFX\s*gợi\s*ý|dây\s+điện|dây\s+tín\s+hiệu|ống\s+ngầm|ống\s+quyết\s+toán|[→⇒➜➔←↔])",
    re.IGNORECASE,
)


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


def dim_color(c: tuple[int, int, int], focus: float, bg: tuple[int, int, int] = PAPER_CARD) -> tuple[int, int, int]:
    """Làm mờ màu về nền sân khấu khi thực thể không phải tâm điểm (focus ~ 0.25 -> 1.0)."""
    return blend_rgb(bg, c, max(0.24, min(1.0, focus)))


def fmt_vnd(val: float | int) -> str:
    return f"{int(round(val)):,}".replace(",", ".") + " đ"


def step_quantize(val: float, step: int = 50_000) -> int:
    return int(round(val / step) * step)


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", str(text or ""))


def get_font(size: int, weight: str = "bold") -> ImageFont.FreeTypeFont:
    candidates_map = {
        "heavy": [
            "/Library/Fonts/SF-Pro-Rounded-Heavy.otf",
            "/Library/Fonts/SF-Pro-Display-Heavy.otf",
            "/Library/Fonts/SF-Pro-Rounded-Bold.otf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ],
        "bold": [
            "/Library/Fonts/SF-Pro-Rounded-Bold.otf",
            "/Library/Fonts/SF-Pro-Display-Bold.otf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ],
        "regular": [
            "/Library/Fonts/SF-Pro-Rounded-Semibold.otf",
            "/Library/Fonts/SF-Pro-Display-Medium.otf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ],
    }
    for path in candidates_map.get(weight, candidates_map["bold"]):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def assert_broadcast_overlay_clean(texts: list[str]) -> None:
    for txt in texts:
        m = SLATE_LEAK_RE.search(str(txt or ""))
        if m:
            raise RuntimeError(f"FAIL [B4 Broadcast Polish]: Lộ nhãn nội bộ '{m.group(0)}' trong: {txt!r}")


# ── TÁCH CỤM PHỤ ĐỀ CHO FILE .SRT RỜI (YOUTUBE [CC], KHÔNG ĐỐT VÀO VIDEO) ───

def split_scene_into_phrases(
    scene_text: str,
    char_offset: int,
    starts: list[float],
    ends: list[float],
    time_shift: float,
) -> list[dict]:
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
            if w not in ("—", "-", "–", "..."):
                words_meta.append(
                    {
                        "word": nfc(w.replace("...", "").strip()),
                        "t0": starts[wc0] + time_shift,
                        "t1": ends[wc1] + time_shift,
                    }
                )
            w_cursor = w_pos + len(w)

        phrases_out.append(
            {
                "text": nfc(p_str),
                "t0": p_t0,
                "t1": p_t1,
                "words": [wm for wm in words_meta if wm["word"]],
            }
        )
        local_cursor = idx_in_scene + len(p_str)
    return phrases_out


def build_srt_chunks(scene_meta: list[dict], max_words: int = 8) -> None:
    """Tạo cụm phụ đề gọn gàng theo từng câu/ngắt phẩy để xuất file `.srt` cho YouTube [CC]."""
    for sm in scene_meta:
        all_words: list[dict] = []
        for ph in sm["phrases"]:
            all_words.extend(ph["words"])

        chunks: list[dict] = []
        cur: list[dict] = []

        def flush_cur() -> None:
            nonlocal cur
            if not cur:
                return
            chunks.append(
                {
                    "words": cur,
                    "t0": cur[0]["t0"],
                    "t1": max(cur[0]["t0"] + 0.20, cur[-1]["t1"]),
                    "text": " ".join(w["word"] for w in cur),
                }
            )
            cur = []

        for w in all_words:
            if cur and len(cur) + 1 > max_words:
                flush_cur()
            cur.append(w)
            w_str = w["word"]
            if w_str.endswith((".", "?", "!", ":", ";")) or (w_str.endswith(",") and len(cur) >= 4):
                flush_cur()

        flush_cur()

        for ci in range(len(chunks)):
            if ci > 0 and chunks[ci]["t0"] < chunks[ci - 1]["t1"]:
                mid = 0.5 * (chunks[ci - 1]["t1"] + chunks[ci]["t0"])
                chunks[ci - 1]["t1"] = max(chunks[ci - 1]["t0"] + 0.10, mid)
                chunks[ci]["t0"] = chunks[ci - 1]["t1"] + 0.01

        sm["srt_chunks"] = chunks


def _fmt_srt_ts(sec: float) -> str:
    ms_total = max(0, int(round(sec * 1000)))
    h = ms_total // 3_600_000
    rem = ms_total % 3_600_000
    m = rem // 60_000
    rem %= 60_000
    s = rem // 1000
    ms = rem % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def export_srt_subtitles(scene_meta: list[dict], srt_path: pathlib.Path) -> pathlib.Path:
    """Xuất file `.srt` chuẩn YouTube [CC] từ alignment timestamp của Giọng Tâm."""
    lines: list[str] = []
    cue_num = 1
    prev_end = 0.0
    for sm in scene_meta:
        for ch in sm.get("srt_chunks", []):
            t0 = max(prev_end, float(ch["t0"]))
            t1 = max(t0 + 0.25, float(ch["t1"]))
            prev_end = t1 + 0.005
            lines.append(str(cue_num))
            lines.append(f"{_fmt_srt_ts(t0)} --> {_fmt_srt_ts(t1)}")
            lines.append(nfc(ch["text"]))
            lines.append("")
            cue_num += 1
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    srt_path.write_text("\n".join(lines), encoding="utf-8")
    return srt_path


# ── HỆ NHÂN VẬT & ĐỊNH CHẾ 2D SẮC NÉT (2x SUPERSAMPLED VECTOR SPRITES) ──────

ARCHETYPES: dict[int, dict[str, Any]] = {
    0: {"name": "BẠN", "sub": "Chủ thẻ", "accent": NAVY, "bg": (222, 232, 245)},
    1: {"name": "QUÁN QUEN", "sub": "Nơi bán", "accent": TERRACOTTA, "bg": (248, 228, 218)},
    2: {"name": "NH CỦA QUÁN", "sub": "Acquirer", "accent": TEAL, "bg": (218, 236, 238)},
    3: {"name": "TỔ CHỨC THẺ", "sub": "Chuyển mạch", "accent": AMBER, "bg": (250, 236, 206)},
    4: {"name": "NH CỦA BẠN", "sub": "Issuer", "accent": GREEN, "bg": (218, 238, 226)},
}


def _poly_ink(
    d: ImageDraw.ImageDraw,
    pts: list[tuple[float, float]],
    fill: tuple[int, int, int],
    sw: int,
    outline: tuple[int, int, int] = INK,
) -> None:
    d.polygon(pts, fill=fill)
    if sw > 0:
        d.line(pts + [pts[0]], fill=outline, width=sw, joint="curve")


def draw_archetype_vector(
    d: ImageDraw.ImageDraw,
    actor_id: int,
    W: int,
    H: int,
    accent: tuple[int, int, int],
    fill_bg: tuple[int, int, int],
    inner_only: bool = True,
) -> None:
    """Vẽ minh hoạ nhân vật & định chế 2D mỹ thuật nhiều lớp trên canvas 4x supersampled."""
    sw = max(10, W // 38)
    sw_fine = max(5, sw // 2)
    cx, cy = W / 2.0, H / 2.0
    pad = int(round(sw * 1.4))

    # Nền huy hiệu 2 tầng bên trong vòng tròn: bầu trời sáng dịu + bệ sàn kiến trúc
    d.ellipse((pad, pad, W - pad, H - pad), fill=fill_bg)
    glow_r = W * 0.34
    d.ellipse(
        (cx - glow_r, H * 0.44 - glow_r, cx + glow_r, H * 0.44 + glow_r),
        fill=blend_rgb(fill_bg, PAPER_CARD, 0.56),
    )
    floor_y = int(round(H * 0.755))
    d.rectangle((pad, floor_y, W - pad, H - pad), fill=blend_rgb(fill_bg, PAPER_SOFT, 0.72))
    d.line([(pad, floor_y), (W - pad, floor_y)], fill=blend_rgb(INK, fill_bg, 0.55), width=sw_fine)

    if actor_id == 0:
        # BẠN (Chủ thẻ): Chân dung cân đối, tóc gọn gàng, áo blazer Navy + sơ mi trắng + thẻ chip EMV
        hcx = W * 0.455
        # Bờ vai & áo blazer Navy
        d.pieslice(
            (hcx - W * 0.30, H * 0.54, hcx + W * 0.30, H * 1.12),
            180,
            360,
            fill=NAVY,
            outline=INK,
            width=sw,
        )
        # Vạt sơ mi chữ V + cà vạt đỏ gạch ở giữa ngực
        _poly_ink(
            d,
            [(hcx - W * 0.085, H * 0.56), (hcx + W * 0.085, H * 0.56), (hcx, H * 0.78)],
            PAPER_CARD,
            sw_fine,
        )
        _poly_ink(
            d,
            [
                (hcx - W * 0.022, H * 0.61),
                (hcx + W * 0.022, H * 0.61),
                (hcx + W * 0.032, H * 0.77),
                (hcx, H * 0.81),
                (hcx - W * 0.032, H * 0.77),
            ],
            TERRACOTTA,
            max(3, sw_fine - 1),
        )
        # Cổ & hai tai ấm áp
        neck_w, neck_top, neck_bot = W * 0.056, H * 0.49, H * 0.59
        d.rounded_rectangle(
            (hcx - neck_w, neck_top, hcx + neck_w, neck_bot),
            radius=sw_fine,
            fill=(238, 198, 168),
            outline=INK,
            width=sw_fine,
        )
        hcy = H * 0.365
        hrx, hry = W * 0.138, H * 0.148
        ear_r = W * 0.032
        d.ellipse((hcx - hrx - ear_r * 0.6, hcy - ear_r, hcx - hrx + ear_r * 0.8, hcy + ear_r), fill=(242, 204, 174), outline=INK, width=sw_fine)
        d.ellipse((hcx + hrx - ear_r * 0.8, hcy - ear_r, hcx + hrx + ear_r * 0.6, hcy + ear_r), fill=(242, 204, 174), outline=INK, width=sw_fine)

        # Mái tóc sau gáy & phom tóc gọn gàng
        hair_col = (36, 32, 30)
        d.ellipse((hcx - hrx * 1.12, hcy - hry * 1.24, hcx + hrx * 1.12, hcy + hry * 0.35), fill=hair_col, outline=INK, width=sw)
        # Khuôn mặt
        d.ellipse((hcx - hrx, hcy - hry, hcx + hrx, hcy + hry), fill=(252, 229, 205), outline=INK, width=sw)
        # Tóc mái rẽ ngôi lệch mềm mại
        _poly_ink(
            d,
            [
                (hcx - hrx * 1.02, hcy - hry * 0.15),
                (hcx - hrx * 0.96, hcy - hry * 0.85),
                (hcx - hrx * 0.10, hcy - hry * 1.12),
                (hcx + hrx * 0.88, hcy - hry * 0.86),
                (hcx + hrx * 1.00, hcy - hry * 0.24),
                (hcx + hrx * 0.55, hcy - hry * 0.55),
                (hcx - hrx * 0.15, hcy - hry * 0.42),
                (hcx - hrx * 0.68, hcy - hry * 0.58),
            ],
            hair_col,
            sw_fine,
        )
        # Chân mày, đôi mắt có chấm sáng trắng, má hồng & nụ cười
        eye_dx = hrx * 0.40
        eye_y = hcy + hry * 0.04
        er = max(5, int(W * 0.017))
        d.arc((hcx - eye_dx - er * 1.5, eye_y - hry * 0.28, hcx - eye_dx + er * 1.5, eye_y - hry * 0.06), 195, 345, fill=INK, width=sw_fine)
        d.arc((hcx + eye_dx - er * 1.5, eye_y - hry * 0.28, hcx + eye_dx + er * 1.5, eye_y - hry * 0.06), 195, 345, fill=INK, width=sw_fine)
        for ex in (hcx - eye_dx, hcx + eye_dx):
            d.ellipse((ex - er, eye_y - er, ex + er, eye_y + er), fill=INK)
            sp_r = max(2, er // 3)
            d.ellipse((ex - er * 0.45, eye_y - er * 0.45, ex - er * 0.45 + sp_r * 2, eye_y - er * 0.45 + sp_r * 2), fill=PAPER_CARD)
        chk_rx, chk_ry = W * 0.028, H * 0.016
        d.ellipse((hcx - hrx * 0.62 - chk_rx, hcy + hry * 0.28 - chk_ry, hcx - hrx * 0.62 + chk_rx, hcy + hry * 0.28 + chk_ry), fill=(244, 186, 168))
        d.ellipse((hcx + hrx * 0.62 - chk_rx, hcy + hry * 0.28 - chk_ry, hcx + hrx * 0.62 + chk_rx, hcy + hry * 0.28 + chk_ry), fill=(244, 186, 168))
        d.arc((hcx - hrx * 0.34, hcy + hry * 0.22, hcx + hrx * 0.34, hcy + hry * 0.62), 20, 160, fill=INK, width=sw_fine)

        # Thẻ Tín dụng Vàng Kim + Chip EMV + Sóng Contactless ở góc phải dưới
        cw0, cy0, cw1, cy1 = W * 0.50, H * 0.555, W * 0.855, H * 0.775
        d.rounded_rectangle((cw0, cy0 + sw_fine, cw1, cy1 + sw_fine), radius=sw, fill=blend_rgb(NAVY, INK, 0.45))
        d.rounded_rectangle((cw0, cy0, cw1, cy1), radius=sw, fill=GOLD, outline=INK, width=sw)
        # Dải trang trí góc trên thẻ
        d.rectangle((cw0 + sw, cy0 + (cy1 - cy0) * 0.16, cw1 - sw, cy0 + (cy1 - cy0) * 0.34), fill=NAVY)
        # Con chip EMV 4 ô vuông rõ nét
        ch_x0, ch_y0 = cw0 + W * 0.042, cy0 + (cy1 - cy0) * 0.48
        ch_w, ch_h = W * 0.072, H * 0.056
        d.rounded_rectangle((ch_x0, ch_y0, ch_x0 + ch_w, ch_y0 + ch_h), radius=sw_fine // 2, fill=(252, 232, 168), outline=INK, width=max(3, sw_fine - 1))
        d.line([(ch_x0 + ch_w / 2, ch_y0), (ch_x0 + ch_w / 2, ch_y0 + ch_h)], fill=INK, width=max(2, sw_fine // 2))
        d.line([(ch_x0, ch_y0 + ch_h / 2), (ch_x0 + ch_w, ch_y0 + ch_h / 2)], fill=INK, width=max(2, sw_fine // 2))
        # 3 vạch sóng contactless
        wcx, wcy = cw1 - W * 0.068, cy0 + (cy1 - cy0) * 0.66
        for wr in (W * 0.024, W * 0.042, W * 0.060):
            d.arc((wcx - wr, wcy - wr, wcx + wr, wcy + wr), -48, 48, fill=INK, width=max(3, sw_fine // 2))

    elif actor_id == 1:
        # QUÁN QUEN (Nơi bán): Mặt tiền tiệm chỉnh chu + mái hiên sọc lượn sóng + cửa gỗ + đèn quầy + POS cầm tay
        bx0, by0, bx1, by1 = W * 0.19, H * 0.285, W * 0.77, H * 0.775
        # Bệ đá & thân tiệm kem sáng
        d.rounded_rectangle((bx0 - W * 0.025, by1 - H * 0.04, bx1 + W * 0.025, by1 + H * 0.025), radius=sw_fine, fill=(92, 82, 74), outline=INK, width=sw_fine)
        d.rounded_rectangle((bx0, by0, bx1, by1), radius=sw_fine, fill=PAPER_CARD, outline=INK, width=sw)
        # Bảng hiệu phía trên mái hiên
        d.rounded_rectangle((bx0 + W * 0.05, by0 - H * 0.068, bx1 - W * 0.05, by0 + H * 0.015), radius=sw_fine, fill=TERRACOTTA, outline=INK, width=sw)
        d.line([(bx0 + W * 0.12, by0 - H * 0.026), (bx1 - W * 0.12, by0 - H * 0.026)], fill=PAPER_CARD, width=sw_fine)

        # Cửa gỗ pano trái + tay nắm đồng
        dx0, dy0, dx1, dy1 = bx0 + W * 0.055, H * 0.49, bx0 + W * 0.215, by1
        d.rounded_rectangle((dx0, dy0, dx1, dy1), radius=sw_fine // 2, fill=(154, 78, 48), outline=INK, width=sw_fine)
        d.rectangle((dx0 + W * 0.028, dy0 + H * 0.032, dx1 - W * 0.028, dy0 + H * 0.125), fill=(182, 102, 66), outline=INK, width=max(3, sw_fine // 2))
        d.ellipse((dx1 - W * 0.04, (dy0 + dy1) * 0.52, dx1 - W * 0.018, (dy0 + dy1) * 0.52 + W * 0.022), fill=GOLD, outline=INK, width=2)

        # Ô kính lớn bên phải với đèn thả ấm và vệt sáng kính
        wx0, wy0, wx1, wy1 = bx0 + W * 0.255, H * 0.49, bx1 - W * 0.055, H * 0.695
        d.rounded_rectangle((wx0, wy0, wx1, wy1), radius=sw_fine // 2, fill=(204, 232, 238), outline=INK, width=sw_fine)
        d.polygon([(wx0 + W * 0.04, wy1 - sw_fine), (wx0 + W * 0.11, wy0 + sw_fine), (wx0 + W * 0.15, wy0 + sw_fine), (wx0 + W * 0.08, wy1 - sw_fine)], fill=PAPER_CARD)
        lmp_x = (wx0 + wx1) * 0.48
        d.line([(lmp_x, wy0), (lmp_x, wy0 + H * 0.048)], fill=INK, width=max(3, sw_fine // 2))
        _poly_ink(d, [(lmp_x - W * 0.035, wy0 + H * 0.078), (lmp_x + W * 0.035, wy0 + H * 0.078), (lmp_x + W * 0.015, wy0 + H * 0.044), (lmp_x - W * 0.015, wy0 + H * 0.044)], AMBER, max(3, sw_fine // 2))
        d.rounded_rectangle((wx0 - W * 0.015, wy1, wx1 + W * 0.015, wy1 + H * 0.03), radius=sw_fine // 2, fill=(138, 92, 58), outline=INK, width=sw_fine)

        # Mái hiên lượn sóng 6 múi nổi bật
        ax0, ax1 = bx0 - W * 0.032, bx1 + W * 0.032
        ay0, ay1 = H * 0.30, H * 0.415
        n_seg = 6
        seg_w = (ax1 - ax0) / n_seg
        # Bóng đổ mềm dưới mái hiên
        d.rectangle((bx0 + sw_fine, ay1, bx1 - sw_fine, ay1 + H * 0.035), fill=blend_rgb(PAPER_CARD, INK, 0.18))
        for si in range(n_seg):
            sx0 = ax0 + si * seg_w
            sx1 = sx0 + seg_w
            sc_col = TERRACOTTA if si % 2 == 0 else PAPER_CARD
            _poly_ink(d, [(sx0 + seg_w * 0.06, ay0), (sx1 - seg_w * 0.06, ay0), (sx1, ay1), (sx0, ay1)], sc_col, sw_fine)
            sc_r = seg_w * 0.5
            d.pieslice((sx0, ay1 - sc_r * 0.55, sx1, ay1 + sc_r * 0.55), 0, 180, fill=sc_col, outline=INK, width=sw_fine)

        # Máy POS cầm tay & tờ biên lai nhô lên ở góc phải dưới
        px0, py0, px1, py1 = W * 0.625, H * 0.555, W * 0.825, H * 0.825
        # Tờ hoá đơn trắng ở khe trên
        d.rounded_rectangle((px0 + W * 0.038, py0 - H * 0.065, px1 - W * 0.038, py0 + H * 0.03), radius=sw_fine // 2, fill=PAPER_CARD, outline=INK, width=sw_fine)
        d.line([(px0 + W * 0.062, py0 - H * 0.032), (px1 - W * 0.062, py0 - H * 0.032)], fill=INK_MUTED, width=max(3, sw_fine // 2))
        d.rounded_rectangle((px0, py0, px1, py1), radius=sw, fill=(44, 48, 60), outline=INK, width=sw)
        d.rounded_rectangle((px0 + W * 0.028, py0 + H * 0.028, px1 - W * 0.028, py0 + H * 0.125), radius=sw_fine // 2, fill=(168, 240, 198), outline=INK, width=max(3, sw_fine // 2))
        # Dấu tick trên màn hình POS
        d.line([(px0 + W * 0.068, py0 + H * 0.078), (px0 + W * 0.092, py0 + H * 0.102), (px1 - W * 0.056, py0 + H * 0.052)], fill=GREEN, width=sw_fine, joint="curve")
        # Phím bấm POS gọn gàng
        for kr in range(2):
            for kc in range(3):
                kx0 = px0 + W * 0.034 + kc * W * 0.048
                ky0 = py0 + H * 0.15 + kr * H * 0.038
                d.rounded_rectangle((kx0, ky0, kx0 + W * 0.036, ky0 + H * 0.025), radius=3, fill=PAPER_SOFT if kr == 0 else (GOLD if kc == 2 else (120, 130, 146)))

    elif actor_id == 2:
        # NH CỦA QUÁN (Acquirer): Toà nhà Ngân hàng Thương mại hiện đại + 4 cột + khiên thanh toán
        bx0, bx1 = W * 0.185, W * 0.785
        ped_top, ent_y, body_bot = H * 0.19, H * 0.34, H * 0.74
        # Bậc tam cấp nền vững chãi
        d.rounded_rectangle((bx0 - W * 0.045, body_bot, bx1 + W * 0.045, body_bot + H * 0.04), radius=sw_fine // 2, fill=(214, 206, 190), outline=INK, width=sw_fine)
        d.rounded_rectangle((bx0 - W * 0.065, body_bot + H * 0.038, bx1 + W * 0.065, body_bot + H * 0.078), radius=sw_fine // 2, fill=(184, 176, 160), outline=INK, width=sw_fine)
        # Thân nhà chính
        d.rectangle((bx0, ent_y, bx1, body_bot), fill=(240, 234, 222), outline=INK, width=sw)
        # Cửa kính vòm giữa & các ô cửa sổ kính xanh dịu
        d.rounded_rectangle((cx - W * 0.062, H * 0.54, cx + W * 0.03, body_bot), radius=sw_fine, fill=(58, 128, 138), outline=INK, width=sw_fine)
        d.line([(cx - W * 0.016, H * 0.54), (cx - W * 0.016, body_bot)], fill=INK, width=max(3, sw_fine // 2))
        # 4 trụ cột đứng cân đối có đầu & chân cột
        col_xs = [bx0 + W * 0.055, bx0 + W * 0.185, bx1 - W * 0.185, bx1 - W * 0.055]
        cw = W * 0.032
        for col_x in col_xs:
            d.rectangle((col_x - cw, ent_y + H * 0.045, col_x + cw, body_bot), fill=TEAL, outline=INK, width=sw_fine)
            d.line([(col_x, ent_y + H * 0.06), (col_x, body_bot - H * 0.015)], fill=blend_rgb(TEAL, PAPER_CARD, 0.35), width=max(2, sw_fine // 2))
            d.rounded_rectangle((col_x - cw * 1.35, ent_y + H * 0.025, col_x + cw * 1.35, ent_y + H * 0.052), radius=3, fill=PAPER_CARD, outline=INK, width=max(3, sw_fine // 2))
        # Dầm ngang & mái tam giác cổ điển
        d.rounded_rectangle((bx0 - W * 0.045, ent_y - H * 0.01, bx1 + W * 0.045, ent_y + H * 0.038), radius=sw_fine // 2, fill=PAPER_CARD, outline=INK, width=sw)
        _poly_ink(d, [(cx - W * 0.016, ped_top), (bx0 - W * 0.05, ent_y), (bx1 + W * 0.05, ent_y)], TEAL, sw)
        _poly_ink(d, [(cx - W * 0.016, ped_top + H * 0.042), (bx0 + W * 0.04, ent_y - H * 0.015), (bx1 - W * 0.07, ent_y - H * 0.015)], PAPER_CARD, sw_fine)
        # Huy hiệu khiên thanh toán góc phải dưới
        scx, scy = W * 0.72, H * 0.67
        sr = W * 0.118
        d.ellipse((scx - sr, scy - sr, scx + sr, scy + sr), fill=PAPER_CARD, outline=INK, width=sw)
        d.ellipse((scx - sr * 0.74, scy - sr * 0.74, scx + sr * 0.74, scy + sr * 0.74), fill=TEAL, outline=INK, width=sw_fine)
        d.line([(scx - sr * 0.36, scy), (scx - sr * 0.08, scy + sr * 0.28), (scx + sr * 0.38, scy - sr * 0.26)], fill=GOLD, width=sw, joint="curve")

    elif actor_id == 3:
        # TỔ CHỨC THẺ (Chuyển mạch): Trung tâm Switch & Server đối xứng + 4 cổng kết nối + mũi tên chuyển mạch ⇄
        # 4 thanh đường ray kết nối 4 hướng tới cổng định tuyến
        for px, py in [(W * 0.145, cy), (W * 0.855, cy), (cx, H * 0.145), (cx, H * 0.855)]:
            d.line([(cx, cy), (px, py)], fill=INK, width=sw)
            d.line([(cx, cy), (px, py)], fill=AMBER, width=sw_fine)
            pr = W * 0.042
            d.ellipse((px - pr, py - pr, px + pr, py + pr), fill=GOLD, outline=INK, width=sw_fine)

        # Khối tủ chuyển mạch công nghệ Navy + Gold
        sx0, sy0, sx1, sy1 = W * 0.23, H * 0.24, W * 0.77, H * 0.76
        d.rounded_rectangle((sx0, sy0, sx1, sy1), radius=sw * 1.4, fill=NAVY, outline=INK, width=sw)
        d.rounded_rectangle((sx0 + sw, sy0 + sw, sx1 - sw, sy1 - sw), radius=sw, fill=(24, 46, 80), outline=blend_rgb(NAVY, GOLD, 0.55), width=max(3, sw_fine // 2))

        # 2 cột server blade đối xứng trái/phải với đèn LED hoạt động
        for rx0, rx1 in [(sx0 + W * 0.045, sx0 + W * 0.195), (sx1 - W * 0.195, sx1 - W * 0.045)]:
            for ri in range(4):
                ry0 = sy0 + H * 0.07 + ri * H * 0.098
                d.rounded_rectangle((rx0, ry0, rx1, ry0 + H * 0.068), radius=sw_fine // 2, fill=(16, 26, 44), outline=blend_rgb(NAVY, PAPER_CARD, 0.35), width=max(2, sw_fine // 2))
                lr = max(4, int(W * 0.013))
                lx = rx0 + W * 0.025
                ly = ry0 + H * 0.034
                l_col = GREEN if (ri % 2 == 0) else GOLD
                d.ellipse((lx - lr, ly - lr, lx + lr, ly + lr), fill=l_col)
                d.line([(rx0 + W * 0.052, ly), (rx1 - W * 0.022, ly)], fill=(78, 108, 152), width=max(3, sw_fine // 2))

        # Vòng tròn lõi trung tâm chuyển mạch với 2 mũi tên đảo chiều trên/dưới
        hr = W * 0.135
        d.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), fill=PAPER_CARD, outline=INK, width=sw)
        d.ellipse((cx - hr * 0.78, cy - hr * 0.78, cx + hr * 0.78, cy + hr * 0.78), fill=AMBER_LIGHT, outline=AMBER, width=sw_fine)
        ay_top, ay_bot = cy - hr * 0.25, cy + hr * 0.25
        ax_l, ax_r = cx - hr * 0.44, cx + hr * 0.44
        aw = hr * 0.20
        d.line([(ax_l, ay_top), (ax_r - aw * 0.4, ay_top)], fill=INK, width=sw_fine)
        d.polygon([(ax_r + aw * 0.3, ay_top), (ax_r - aw * 0.7, ay_top - aw * 0.75), (ax_r - aw * 0.7, ay_top + aw * 0.75)], fill=INK)
        d.line([(ax_r, ay_bot), (ax_l + aw * 0.4, ay_bot)], fill=NAVY, width=sw_fine)
        d.polygon([(ax_l - aw * 0.3, ay_bot), (ax_l + aw * 0.7, ay_bot - aw * 0.75), (ax_l + aw * 0.7, ay_bot + aw * 0.75)], fill=NAVY)

    else:
        # NH CỦA BẠN (Issuer): Toà nhà Ngân hàng Phát hành Lục bảo cổ điển + 4 cột cẩm thạch + Cửa Két Hạn Mức
        bx0, bx1 = W * 0.175, W * 0.765
        ped_top, ent_y, body_bot = H * 0.185, H * 0.335, H * 0.74
        # Bậc tam cấp đá
        d.rounded_rectangle((bx0 - W * 0.04, body_bot, bx1 + W * 0.04, body_bot + H * 0.038), radius=sw_fine // 2, fill=(224, 218, 204), outline=INK, width=sw_fine)
        d.rounded_rectangle((bx0 - W * 0.06, body_bot + H * 0.036, bx1 + W * 0.06, body_bot + H * 0.075), radius=sw_fine // 2, fill=(192, 184, 168), outline=INK, width=sw_fine)
        # Tường chính màu xanh lục bảo sâu
        d.rectangle((bx0, ent_y, bx1, body_bot), fill=GREEN, outline=INK, width=sw)
        # Cổng vòm trung tâm bên trong
        d.rounded_rectangle((bx0 + W * 0.21, H * 0.50, bx0 + W * 0.37, body_bot), radius=sw, fill=(24, 72, 50), outline=INK, width=sw_fine)
        # 4 trụ cột cẩm thạch trắng kem nổi bật
        col_xs = [bx0 + W * 0.06, bx0 + W * 0.18, bx1 - W * 0.18, bx1 - W * 0.06]
        cw = W * 0.030
        for col_x in col_xs:
            d.rectangle((col_x - cw, ent_y + H * 0.04, col_x + cw, body_bot), fill=PAPER_CARD, outline=INK, width=sw_fine)
            d.line([(col_x, ent_y + H * 0.06), (col_x, body_bot - H * 0.02)], fill=PAPER_SOFT, width=max(3, sw_fine // 2))
            d.rounded_rectangle((col_x - cw * 1.35, ent_y + H * 0.02, col_x + cw * 1.35, ent_y + H * 0.048), radius=3, fill=(238, 232, 218), outline=INK, width=max(2, sw_fine // 2))
        # Dầm ngang & Mái tam giác Ngân hàng có huy chương vàng
        bcx = (bx0 + bx1) / 2.0
        d.rounded_rectangle((bx0 - W * 0.04, ent_y - H * 0.01, bx1 + W * 0.04, ent_y + H * 0.034), radius=sw_fine // 2, fill=PAPER_CARD, outline=INK, width=sw)
        _poly_ink(d, [(bcx, ped_top), (bx0 - W * 0.045, ent_y), (bx1 + W * 0.045, ent_y)], GREEN, sw)
        _poly_ink(d, [(bcx, ped_top + H * 0.042), (bx0 + W * 0.045, ent_y - H * 0.015), (bx1 - W * 0.045, ent_y - H * 0.015)], GREEN_LIGHT, sw_fine)
        d.ellipse((bcx - W * 0.025, ped_top + H * 0.068, bcx + W * 0.025, ped_top + H * 0.118), fill=GOLD, outline=INK, width=max(3, sw_fine // 2))

        # Cửa Két Sắt Tín dụng thép + tay quay 6 chấu vàng kim góc phải dưới
        vcx, vcy = W * 0.695, H * 0.665
        vr = W * 0.148
        d.ellipse((vcx - vr, vcy - vr, vcx + vr, vcy + vr), fill=(162, 170, 178), outline=INK, width=sw)
        d.ellipse((vcx - vr * 0.72, vcy - vr * 0.72, vcx + vr * 0.72, vcy + vr * 0.72), fill=(54, 62, 74), outline=INK, width=sw_fine)
        # Tay quay 6 chấu vàng kim
        for k in range(3):
            ang = k * math.pi / 3.0 + math.pi / 6.0
            sp_len = vr * 0.58
            d.line(
                [(vcx - sp_len * math.cos(ang), vcy - sp_len * math.sin(ang)), (vcx + sp_len * math.cos(ang), vcy + sp_len * math.sin(ang))],
                fill=GOLD,
                width=sw_fine + 2,
            )
        d.ellipse((vcx - vr * 0.24, vcy - vr * 0.24, vcx + vr * 0.24, vcy + vr * 0.24), fill=GOLD, outline=INK, width=sw_fine)

    if not inner_only:
        d.ellipse((pad, pad, W - pad, H - pad), outline=INK, width=sw)


class SpriteBank:
    """Cache 4x-supersampled RGBA sprite hạ xuống 2x sắc nét cho nhịp thở 30fps mượt và tốc độ cao."""

    def __init__(self, size: int):
        self.size = size
        self.hi_bright: dict[int, Image.Image] = {}
        self.dim_icons: dict[int, Image.Image] = {}
        hi4_sz = size * 4
        hi2_sz = size * 2
        sw4 = max(10, hi4_sz // 38)
        pad4 = int(round(sw4 * 1.4))

        # Mặt nạ cắt huy hiệu tròn tại 4x đảm bảo đường cắt biên siêu mịn
        clip_mask = Image.new("L", (hi4_sz, hi4_sz), 0)
        ImageDraw.Draw(clip_mask).ellipse((pad4, pad4, hi4_sz - pad4, hi4_sz - pad4), fill=255)
        empty4 = Image.new("RGBA", (hi4_sz, hi4_sz), (0, 0, 0, 0))

        for aid, cfg in ARCHETYPES.items():
            scene4 = Image.new("RGBA", (hi4_sz, hi4_sz), (0, 0, 0, 0))
            draw_archetype_vector(ImageDraw.Draw(scene4), aid, hi4_sz, hi4_sz, cfg["accent"], cfg["bg"], inner_only=True)
            master4 = Image.composite(scene4, empty4, clip_mask)

            # Viền đôi huy hiệu đồng bộ ở mặt trên cùng (lót kem sáng bên trong + viền mực #1E1D1A)
            bd = ImageDraw.Draw(master4)
            bd.ellipse((pad4 + sw4 // 2, pad4 + sw4 // 2, hi4_sz - pad4 - sw4 // 2, hi4_sz - pad4 - sw4 // 2), outline=PAPER_CARD, width=max(5, sw4 // 2))
            bd.ellipse((pad4, pad4, hi4_sz - pad4, hi4_sz - pad4), outline=INK, width=sw4)

            self.hi_bright[aid] = master4.resize((hi2_sz, hi2_sz), Image.Resampling.LANCZOS)

            bright = master4.resize((size, size), Image.Resampling.LANCZOS)
            arr = np.asarray(bright, dtype=np.float32)
            bg_rgb = np.array([PAPER_CARD[0], PAPER_CARD[1], PAPER_CARD[2]], dtype=np.float32)
            lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
            grey = np.stack([lum, lum, lum], axis=-1)
            faded_rgb = 0.28 * (0.45 * arr[..., :3] + 0.55 * grey) + 0.72 * bg_rgb
            dim_arr = arr.copy()
            dim_arr[..., :3] = np.clip(faded_rgb, 0, 255)
            self.dim_icons[aid] = Image.fromarray(dim_arr.astype(np.uint8), mode="RGBA")

    def get_scaled(self, actor_id: int, focused: bool, scale: float = 1.0) -> Image.Image:
        if not focused:
            return self.dim_icons[actor_id]
        target_sz = max(32, int(round(self.size * scale)))
        return self.hi_bright[actor_id].resize((target_sz, target_sz), Image.Resampling.BILINEAR)


# ── DỮ LIỆU KỊCH BẢN HÌNH ẢNH BÀI `card` (SHORT 6 CẢNH · LONG 11 CẢNH) ───────

SHORT_STEP_CARDS: list[tuple[str, str]] = [
    ("BƯỚC 1", "Quẹt thẻ"),
    ("BƯỚC 2", "Quyết toán"),
    ("BƯỚC 3", "Chia phí"),
    ("BƯỚC 4", "Hoàn tiền"),
    ("BƯỚC 5", "Giá món"),
]

SHORT_SCENES: list[dict[str, Any]] = [
    {
        "is_hook": True,
        "step": "MỞ ĐẦU · CÂU HỎI ĐẶT RA",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_left": "HOÁ ĐƠN: 10.000.000 đ",
        "hud_right": "HOÀN TIỀN: +100.000 đ",
        "beat_headlines": (
            ("QUẸT 10 TRIỆU, HOÀN 100.000đ", "100.000đ", GREEN),
            ("AI ĐANG TRẢ KHOẢN TIỀN NÀY?", "AI", AMBER),
        ),
        "actors": [
            {"id": 0, "tag": "QUẸT 10 TRIỆU", "beat": 1},
            {"id": 4, "tag": "HOÀN +100.000 đ", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "CÂU DẪN · TRƯỚC KHI VÀO 5 BƯỚC GIẢI MÃ", "prop": "coin"},
        "hook_data": {
            "left_title": "HOÁ ĐƠN QUẸT THẺ",
            "left_amt": "10.000.000 đ",
            "left_sub": "Tại Quán quen",
            "left_actor": 0,
            "left_accent": NAVY,
            "right_title": "TIỀN HOÀN VỀ VÍ",
            "right_amt": "+100.000 đ",
            "right_sub": "Hoàn tiền 1% (Cashback)",
            "right_actor": 4,
            "right_accent": GREEN,
            "hook_kicker": "NGHỊCH LÝ CẦN GIẢI MÃ",
            "hook_line1": "NGHE NHƯ MÓN QUÀ TẶNG THÊM",
            "hook_line2": "NHƯNG AI THẬT SỰ TRẢ 100.000 Đ NÀY?",
            "hook_sub": "Cùng bóc tách từng bước từ lúc chạm thẻ đến lúc chia tiền",
        },
        "focal": {
            "type": "HERO_NUM",
            "target_val": 100_000,
            "prefix": "+",
            "suffix": " đ",
            "color": GREEN,
            "pill": "BẮT ĐẦU NGAY · BƯỚC 1/5: QUẸT THẺ TẠI QUẦY",
        },
    },
    {
        "step": "BƯỚC 1/5 · QUẸT THẺ TẠI QUẦY",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_right": "HẠN MỨC: TẠM KHOÁ",
        "beat_headlines": (
            ("CHƯA CÓ ĐỒNG NÀO CHẠY", "CHƯA", AMBER),
            ("TIỀN THẬT VẪN NẰM YÊN", "NẰM YÊN", AMBER),
        ),
        "actors": [
            {"id": 1, "tag": "KÉT QUÁN: 0 đ", "beat": 1},
            {"id": 4, "tag": "GIỮ CHỖ HẠN MỨC", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 1/5 · LỆNH GIỮ CHỖ 10.000.000 đ", "prop": "lock"},
        "focal": {
            "type": "HERO_NUM",
            "fixed_text": "0 đ",
            "color": AMBER,
            "pill": "CHỈ KHOÁ TẠM TRÊN HẠN MỨC 10 TRIỆU",
        },
    },
    {
        "step": "BƯỚC 2/5 · QUYẾT TOÁN 2 NGÀY",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "PHÍ: -220.000 đ",
        "beat_headlines": (
            ("SAU 2 NGÀY TIỀN MỚI VỀ", "2 NGÀY", GREEN),
            ("TRỪ NGAY 220.000đ PHÍ THẺ", "220.000đ", CORAL),
        ),
        "actors": [
            {"id": 4, "tag": "XUẤT VỐN 10TR", "beat": 1},
            {"id": 1, "tag": "NHẬN 9.780.000 đ", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 2/5 · QUYẾT TOÁN TIỀN THẬT SAU T+2", "prop": "clock"},
        "focal": {
            "type": "SPLIT_BAR",
            "left_lbl": "Quán nhận: 9.780.000 đ",
            "right_lbl": "Phí: −220K",
            "ratio": 0.72,
            "pill": "97,8% VỀ KÉT QUÁN · 2,2% PHÍ NHẬN THẺ",
        },
    },
    {
        "step": "BƯỚC 3/5 · CHIA 220.000 Đ PHÍ THẺ",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "INTERCHANGE: 150K",
        "beat_headlines": (
            ("150.000đ VỀ NGÂN HÀNG BẠN", "150.000đ", GREEN),
            ("PHẦN NHỎ CHIA HAI BÊN", "CHIA", TEAL),
        ),
        "actors": [
            {"id": 4, "tag": "NHẬN +150K", "beat": 1},
            {"id": 2, "tag": "GIỮ +60K", "beat": 2},
            {"id": 3, "tag": "PHÍ +10K", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 3/5 · CHIA 3 KHOẢN TỪ 220.000 đ PHÍ", "prop": "split"},
        "focal": {
            "type": "THREE_SLICE",
            "slices": [
                ("NH bạn (Interchange)", "150.000 đ", 0.56, GREEN),
                ("NH quán", "60.000 đ", 0.27, TEAL),
                ("Thẻ", "10.000 đ", 0.17, AMBER),
            ],
            "pill": "NGÂN HÀNG PHÁT HÀNH THẺ HƯỞNG PHẦN LỚN NHẤT",
        },
    },
    {
        "step": "BƯỚC 4/5 · TRÍCH HOÀN 100.000 Đ",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "HOÀN: +100.000 đ",
        "beat_headlines": (
            ("BẠN TRẢ ĐỦ 10.000.000đ", "10.000.000đ", NAVY),
            ("TRÍCH 150K HOÀN BẠN 100K", "100K", GREEN),
        ),
        "actors": [
            {"id": 4, "tag": "THU 150K TỪ QUÁN", "beat": 1},
            {"id": 0, "tag": "HOÀN BẠN +100K", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 4/5 · TRÍCH TỪ 150.000 đ INTERCHANGE", "prop": "coin"},
        "focal": {
            "type": "SPLIT_BAR",
            "left_lbl": "Hoàn bạn: +100.000 đ",
            "right_lbl": "Giữ: +50K",
            "ratio": 0.67,
            "pill": "NGUỒN TIỀN HOÀN LẤY TỪ PHÍ QUÁN TRẢ",
        },
    },
    {
        "step": "BƯỚC 5/5 · CỘNG PHÍ VÀO GIÁ MÓN",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "ĐI HẾT 1 VÒNG",
        "beat_headlines": (
            ("QUÁN CỘNG PHÍ VÀO GIÁ MÓN", "GIÁ MÓN", TERRACOTTA),
            ("TIỀN BẠN ĐI MỘT VÒNG", "MỘT VÒNG", TERRACOTTA),
        ),
        "actors": [
            {"id": 1, "tag": "GIÁ MÓN +2,2%", "beat": 1},
            {"id": 0, "tag": "NHẬN LẠI TIỀN MÌNH", "beat": 2},
        ],
        "flow": {"kind": "loop", "label": "BƯỚC 5/5 · VÒNG TRÒN GIÁ MÓN VÀ TIỀN HOÀN", "prop": "loop"},
        "focal": {
            "type": "HERO_NUM",
            "fixed_text": "1 VÒNG KHÉP KÍN",
            "color": TERRACOTTA,
            "pill": "KHÔNG CÓ MÓN QUÀ MIỄN PHÍ NÀO TỪ THẺ",
        },
    },
]

LONG_SCENES: list[dict[str, Any]] = [
    {
        "is_hook": True,
        "step": "MỞ ĐẦU · CÂU HỎI ĐẶT RA",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_left": "HOÁ ĐƠN: 10.000.000 đ",
        "hud_right": "KÉT QUÁN ĐÊM NAY: 0 đ",
        "archetype": "HOOK_STAGE",
        "beat_headlines": (
            ("22:47 TỐI, HOÁ ĐƠN 10.000.000đ", "10.000.000đ", AMBER),
            ("CHƯA CÓ ĐỒNG NÀO RỜI ĐI", "CHƯA", AMBER),
        ),
        "phrase_beats": [
            ("22:47 TỐI, HOÁ ĐƠN 10.000.000đ", "10.000.000đ", AMBER),
            ("MÁY POS DUYỆT TRONG 2 GIÂY", "2 GIÂY", GREEN),
            ("NHƯNG KÉT QUÁN VẪN LÀ 0đ", "0đ", CORAL),
            ("10 TRIỆU ĐANG NGỦ Ở ĐÂU?", "Ở ĐÂU?", AMBER),
        ],
        "actors": [
            {"id": 0, "tag": "CHẠM THẺ 10.000.000 đ", "beat": 1},
            {"id": 1, "tag": "KÉT QUÁN: 0 đ", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "CÂU DẪN · TRƯỚC KHI VÀO 10 BƯỚC GIẢI MÃ", "prop": "wire"},
        "hook_data": {
            "left_title": "BỀ MẶT LÚC 22:47 TỐI",
            "left_amt": "10.000.000 đ",
            "left_sub": "Chạm thẻ · Máy POS báo duyệt sau 2 giây",
            "left_actor": 0,
            "left_accent": AMBER,
            "right_title": "SỰ THẬT TRONG KÉT QUÁN",
            "right_amt": "0 đ",
            "right_sub": "Chưa có đồng tiền thật nào rời ngân hàng",
            "right_actor": 1,
            "right_accent": CORAL,
            "hook_kicker": "NGHỊCH LÝ ĐÊM T+0 (22:47 TỐI)",
            "hook_line1": "ĐIỆN THOẠI ĐÃ BÁO TRỪ 10.000.000 Đ — NHƯNG KÉT QUÁN VẪN LÀ 0 Đ",
            "hook_sub": "Tiền thật đang ngủ ở đâu? Cùng giải mã tuần tự qua 10 bước ngay sau đây",
        },
        "focal": {
            "type": "HERO_NUM",
            "fixed_text": "0 đ",
            "color": AMBER,
            "pill": "BẮT ĐẦU NGAY · BƯỚC 1/10: CHẠM THẺ & GIỮ CHỖ HẠN MỨC",
        },
        "arch_data": {
            "left": {
                "kicker": "BỀ MẶT BẠN THẤY",
                "actor_id": 0,
                "big": "10.000.000 đ",
                "sub": "Hoá đơn quẹt thẻ thành công",
                "tag1": "Máy POS in biên lai tức thì",
                "tag2": "Tưởng tiền đã sang ví quán",
                "accent": AMBER,
            },
            "right": {
                "kicker": "TRONG KÉT QUÁN ĐÊM NAY",
                "actor_id": 1,
                "big": "0 đ",
                "sub": "Chưa có đồng tiền thật nào về",
                "tag1": "Quán chỉ mới giữ lời hứa trả",
                "tag2": "Phải chờ tới T+2 mới có tiền",
                "accent": CORAL,
            },
            "bridge": "VS",
        },
    },
    {
        "step": "BƯỚC 1/10 · CHẠM THẺ & GIỮ CHỖ",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_right": "TẠM KHOÁ 10.000.000 đ",
        "archetype": "GAUGE_AND_LOCK",
        "beat_headlines": (
            ("ĐÂY LÀ LỆNH GIỮ CHỖ", "GIỮ CHỖ", AMBER),
            ("CHƯA GHI DƯ NỢ SỔ THẺ", "CHƯA", AMBER),
        ),
        "phrase_beats": [
            ("LỆNH GIỮ CHỖ AUTHORIZATION HOLD", "GIỮ CHỖ", AMBER),
            ("KHOÁ TẠM 10 TRIỆU HẠN MỨC", "10 TRIỆU", AMBER),
            ("CHƯA TRỪ TIỀN, CHƯA TÍNH LÃI", "CHƯA", GREEN),
            ("HUỶ NGAY SẼ GỠ KHOÁ NGAY", "GỠ KHOÁ", TEAL),
        ],
        "actors": [
            {"id": 0, "tag": "KHOÁ HẠN MỨC 10TR", "beat": 1},
            {"id": 4, "tag": "DÁN NHÃN CHỜ", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 1/10 · AUTHORIZATION HOLD (TẠM GIỮ HẠN MỨC)", "prop": "lock"},
        "focal": {
            "type": "HOLD_GAUGE",
            "left_lbl": "Tạm khoá giữ chỗ: 10.000.000 đ",
            "right_lbl": "Hạn mức còn lại",
            "ratio": 0.36,
            "pill": "HUỶ BỮA NGAY LÚC NÀY CÓ THỂ GỠ GIỮ CHỖ NGAY",
        },
        "arch_data": {
            "gauge_title": "THANH HẠN MỨC THẺ TÍN DỤNG CỦA BẠN",
            "locked_lbl": "Tạm khoá giữ chỗ: 10.000.000 đ",
            "free_lbl": "Hạn mức còn lại chưa tiêu",
            "ratio": 0.38,
            "mode": "LOCK",
            "card_left": ("TRẠNG THÁI QUYỀN TIÊU", "Đã khoá −10.000.000 đ", "Không thể quẹt trùng số hạn mức này", AMBER),
            "card_right": ("TRẠNG THÁI SỔ NỢ THẺ", "Dư nợ thực: 0 đ", "Chưa chốt sao kê · Chưa phát sinh lãi", GREEN),
        },
    },
    {
        "step": "BƯỚC 2/10 · XÉT DUYỆT QUA 4 BÊN",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_right": "MÃ CẤP PHÉP OK",
        "archetype": "RELAY_PIPELINE",
        "beat_headlines": (
            ("BẢN TIN CHẠY QUA BỐN BÊN", "BỐN BÊN", NAVY),
            ("TỔ CHỨC THẺ KHÔNG CHO VAY", "KHÔNG", AMBER),
        ),
        "phrase_beats": [
            ("BẢN TIN CHẠY QUA 4 BÊN", "4 BÊN", NAVY),
            ("TỔ CHỨC THẺ CHỈ TRUYỀN TIN", "TRUYỀN TIN", AMBER),
            ("NGÂN HÀNG DUYỆT QUA 3 CỔNG", "3 CỔNG", GREEN),
            ("NGÂN HÀNG BẠN LÀ CHỦ NỢ", "CHỦ NỢ", NAVY),
        ],
        "actors": [
            {"id": 1, "tag": "POS GỬI LỆNH", "beat": 1},
            {"id": 2, "tag": "ACQUIRER CHUYỂN", "beat": 1},
            {"id": 3, "tag": "GIỮ LUẬT CHƠI", "beat": 2},
            {"id": 4, "tag": "DUYỆT 3 BƯỚC", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 2/10 · XÉT DUYỆT TRONG VÀI GIÂY", "prop": "wire"},
        "focal": {
            "type": "CHECKLIST_3",
            "items": ["1. Thẻ thật hợp lệ", "2. Còn đủ hạn mức", "3. Không gian lận"],
            "pill": "NGÂN HÀNG CỦA BẠN MỚI LÀ BÊN CHO BẠN VAY",
        },
        "arch_data": {"sub_mode": "CHECKLIST"},
    },
    {
        "step": "BƯỚC 3/10 · GHI SỔ PHẢI THU (T+0)",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_right": "PHẢI THU: 10.000.000 đ",
        "archetype": "LEDGER_BOARD",
        "beat_headlines": (
            ("TIỀN NGỦ TRONG KHOẢN PHẢI THU", "PHẢI THU", AMBER),
            ("QUÁN KHÔNG ĐÒI NỢ BẠN", "KHÔNG", GREEN),
        ),
        "phrase_beats": [
            ("ĐÊM T+0: TIỀN NGỦ TRONG SỔ", "TRONG SỔ", AMBER),
            ("GHI NỢ TK 1388 PHẢI THU", "TK 1388", AMBER),
            ("GHI CÓ TK 511 DOANH THU", "TK 511", GREEN),
            ("QUÁN ĐÒI NGÂN HÀNG, KHÔNG BẠN", "NGÂN HÀNG", TEAL),
        ],
        "actors": [
            {"id": 1, "tag": "GIỮ LỜI HỨA 10TR", "beat": 1},
            {"id": 2, "tag": "CAM KẾT TRẢ QUÁN", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 3/10 · GHI SỔ PHẢI THU ĐÊM T+0 (CHUẨN TT 99/2025)", "prop": "ledger"},
        "focal": {
            "type": "T_ACCOUNT",
            "debit": "Bên Nợ · TK 1388 (Phải thu NH quán): +10.000.000 đ",
            "credit": "Bên Có · TK 511 (Doanh thu bán hàng): +10.000.000 đ",
            "pill": "ĐÊM NAY CHƯA CÓ TIỀN TRONG KÉT",
        },
        "arch_data": {
            "active_day": 0,
            "days": [("ĐÊM T+0", "Ghi sổ phải thu"), ("NGÀY T+1", "Đối chiếu Clearing"), ("NGÀY T+2", "Tiền thật về két")],
            "debit_title": "BÊN NỢ (DEBIT) · TÀI SẢN TĂNG",
            "debit_rows": [("TK 1388 · Phải thu NH của quán", "+10.000.000 đ", "Quyền đòi tiền từ ngân hàng thanh toán", AMBER)],
            "credit_title": "BÊN CÓ (CREDIT) · DOANH THU TĂNG",
            "credit_rows": [("TK 511 · Doanh thu bán hàng", "+10.000.000 đ", "Đã phục vụ xong bữa tối cho khách", GREEN)],
            "balance_lbl": "Σ NỢ = Σ CÓ = 10.000.000 đ",
        },
    },
    {
        "step": "BƯỚC 4/10 · CHỐT CA & ĐỐI CHIẾU",
        "ket": 0,
        "ket_pct": 0.0,
        "hud_right": "NGÀY GHI SỔ SAO KÊ",
        "archetype": "GAUGE_AND_LOCK",
        "beat_headlines": (
            ("GOM HOÁ ĐƠN CHỐT CA ĐÊM", "CHỐT CA", NAVY),
            ("ĐỐI CHIẾU SỐ, CHƯA CHUYỂN TIỀN", "CHƯA", AMBER),
        ),
        "phrase_beats": [
            ("CUỐI CA: GOM LÔ HOÁ ĐƠN", "GOM LÔ", NAVY),
            ("NGÀY QUẸT THẺ KHÁC GHI SỔ", "KHÁC", AMBER),
            ("ĐỐI CHIẾU SỐ QUA MẠNG THẺ", "ĐỐI CHIẾU", TEAL),
            ("TIỀN THẬT VẪN CHƯA RỜI KÉT", "CHƯA RỜI", CORAL),
        ],
        "actors": [
            {"id": 2, "tag": "GOM LÔ CUỐI NGÀY", "beat": 1},
            {"id": 3, "tag": "SO KHỚP DỮ LIỆU", "beat": 1},
            {"id": 4, "tag": "GHI NỢ THẺ BẠN", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 4/10 · DANH SÁCH ĐỐI CHIẾU CLEARING", "prop": "wire"},
        "focal": {
            "type": "SPLIT_BAR",
            "left_lbl": "Ngày giao dịch (Lúc quẹt thẻ)",
            "right_lbl": "Ngày ghi sổ (Lúc đối chiếu)",
            "ratio": 0.50,
            "pill": "MỚI SO KHỚP SỐ LIỆU — TIỀN THẬT VẪN CHƯA CHẠY",
        },
        "arch_data": {
            "gauge_title": "TIẾN TRÌNH CHỐT LÔ & ĐỐI CHIẾU SỔ (CLEARING T+1)",
            "locked_lbl": "Ngày giao dịch (Lúc quẹt thẻ T+0)",
            "free_lbl": "Ngày ghi sổ sao kê (Đối chiếu T+1)",
            "ratio": 0.50,
            "mode": "SPLIT_TIME",
            "card_left": ("TRÊN SAO KÊ CỦA BẠN", "Lệch 1 ngày giữa 2 cột", "Ngày giao dịch ≠ Ngày ghi sổ", NAVY),
            "card_right": ("TRONG KÉT CỦA QUÁN", "Tiền mặt thực nhận: 0 đ", "Mới khớp con số, chưa chuyển tiền", AMBER),
        },
    },
    {
        "step": "BƯỚC 5/10 · QUYẾT TOÁN 2 NGÀY (T+2)",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "QUÁN NHẬN 9.780.000 đ",
        "archetype": "LEDGER_BOARD",
        "beat_headlines": (
            ("NGÂN HÀNG BẠN ỨNG TIỀN TRƯỚC", "ỨNG TIỀN", GREEN),
            ("QUÁN NHẬN 9.780.000đ SAU T+2", "9.780.000đ", GREEN),
        ),
        "phrase_beats": [
            ("NGÀY T+2: TIỀN THẬT BẮT ĐẦU", "TIỀN THẬT", GREEN),
            ("NGÂN HÀNG BẠN ỨNG 9,85 TRIỆU", "9,85 TRIỆU", TEAL),
            ("KÉT QUÁN NHẬN VỀ 9.780.000đ", "9.780.000đ", GREEN),
            ("KHẤU TRỪ 220.000đ PHÍ DỌC ĐƯỜNG", "220.000đ", CORAL),
        ],
        "actors": [
            {"id": 4, "tag": "ỨNG TRƯỚC 9,85TR", "beat": 1},
            {"id": 2, "tag": "NHẬN & TRẢ QUÁN", "beat": 1},
            {"id": 1, "tag": "KÉT VÀO +9,78TR", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 5/10 · TIỀN THẬT CHẠY SAU 2 NGÀY (T+2)", "prop": "clock"},
        "focal": {
            "type": "T_ACCOUNT",
            "debit": "Nợ TK 112: +9.780.000 đ  +  Nợ TK 641 (Phí): +220.000 đ",
            "credit": "Có TK 1388 (Xoá khoản phải thu đêm trước): −10.000.000 đ",
            "pill": "LỜI HỨA ĐÊM QUA ĐÃ THÀNH TIỀN — THIẾU ĐÚNG PHẦN PHÍ",
        },
        "arch_data": {
            "active_day": 2,
            "days": [("ĐÊM T+0", "Ghi sổ TK 1388"), ("NGÀY T+1", "Khớp lô Clearing"), ("NGÀY T+2", "Tiền về két 9,78tr")],
            "debit_title": "BÊN NỢ (DEBIT) · TIỀN VỀ & CHI PHÍ",
            "debit_rows": [
                ("TK 112 · Tiền gửi NH quán", "+9.780.000 đ", "Tiền thật thực nhận (97,8%)", GREEN),
                ("TK 641 · Chi phí nhận thẻ", "+220.000 đ", "Phí MDR 2,2% bị khấu trừ", CORAL),
            ],
            "credit_title": "BÊN CÓ (CREDIT) · XOÁ KHOẢN PHẢI THU",
            "credit_rows": [("TK 1388 · Phải thu NH của quán", "−10.000.000 đ", "Lời hứa đêm T+0 đã tất toán đủ", TEAL)],
            "balance_lbl": "9.780.000 đ + 220.000 đ = 10.000.000 đ",
        },
    },
    {
        "step": "BƯỚC 6/10 · CHIA 220.000 Đ PHÍ THẺ",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "CHIA 3 TỪ 1 HOÁ ĐƠN",
        "archetype": "WATERFALL_SPLIT",
        "beat_headlines": (
            ("220.000đ PHÍ THẺ CHIA LÀM BA", "220.000đ", CORAL),
            ("150.000đ CHẢY VỀ NGÂN HÀNG BẠN", "150.000đ", GREEN),
        ),
        "phrase_beats": [
            ("GIẢI PHẪU 220.000đ PHÍ THẺ MDR", "220.000đ", CORAL),
            ("150.000đ VỀ NGÂN HÀNG BẠN", "150.000đ", GREEN),
            ("60.000đ VỀ NGÂN HÀNG QUÁN", "60.000đ", TEAL),
            ("10.000đ PHÍ MẠNG CHUYỂN MẠCH", "10.000đ", AMBER),
        ],
        "actors": [
            {"id": 4, "tag": "INTERCHANGE +150K", "beat": 1},
            {"id": 2, "tag": "NH QUÁN +60K", "beat": 2},
            {"id": 3, "tag": "TỔ CHỨC THẺ +10K", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 6/10 · PHÂN BỔ 220.000 đ PHÍ NHẬN THẺ (MDR)", "prop": "split"},
        "focal": {
            "type": "THREE_SLICE",
            "slices": [
                ("NH của bạn (Interchange 1,5%)", "150.000 đ", 0.64, GREEN),
                ("NH quán (0,6%)", "60.000 đ", 0.24, TEAL),
                ("Thẻ (0,1%)", "10.000 đ", 0.12, AMBER),
            ],
            "pill": "BA BÊN ĐỀU ĐƯỢC TRẢ TỪ CÙNG MỘT HOÁ ĐƠN 10 TRIỆU",
        },
        "arch_data": {
            "top_left": ("Két quán thực nhận (97,8%)", "9.780.000 đ", GREEN),
            "top_right": ("Phí MDR cắt lại (2,2%)", "220.000 đ", CORAL),
            "top_ratio": 0.72,
            "buckets": [
                {"title": "1. NH CỦA BẠN", "sub": "Phí Interchange (1,5%)", "amt": "150.000 đ", "note": "Bù rủi ro ứng vốn & miễn lãi", "color": GREEN, "actor_id": 4},
                {"title": "2. NH CỦA QUÁN", "sub": "Phí Acquirer (0,6%)", "amt": "60.000 đ", "note": "Vận hành máy POS & tài khoản", "color": TEAL, "actor_id": 2},
                {"title": "3. TỔ CHỨC THẺ", "sub": "Phí Scheme (0,1%)", "amt": "10.000 đ", "note": "Phí đường ray chuyển mạch", "color": AMBER, "actor_id": 3},
            ],
        },
    },
    {
        "step": "BƯỚC 7/10 · BÙ TRỪ RÒNG CUỐI NGÀY",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "CHUYỂN RÒNG 6.895.000 đ",
        "archetype": "RELAY_PIPELINE",
        "beat_headlines": (
            ("KHÔNG CHUYỂN TIỀN TỪNG HOÁ ĐƠN", "KHÔNG", TEAL),
            ("CỘNG TRỪ RÒNG CHỈ 6.895.000đ", "6.895.000đ", TEAL),
        ),
        "phrase_beats": [
            ("HÀNG TRIỆU GIAO DỊCH MỖI NGÀY", "HÀNG TRIỆU", NAVY),
            ("KHÔNG CHUYỂN LẺ TỪNG HOÁ ĐƠN", "KHÔNG", AMBER),
            ("BÙ TRỪ ĐA PHƯƠNG CUỐI NGÀY", "BÙ TRỪ", TEAL),
            ("CHỈ CHUYỂN RÒNG 6.895.000đ", "6.895.000đ", GREEN),
        ],
        "actors": [
            {"id": 4, "tag": "NỢ QUÁN 9.850.000 đ", "beat": 1},
            {"id": 3, "tag": "BÙ TRỪ RÒNG 6,895TR", "beat": 2},
            {"id": 2, "tag": "NỢ LẠI 2.955.000 đ", "beat": 1},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 7/10 · CHỈ CHUYỂN CHÊNH LỆCH RÒNG CUỐI NGÀY", "prop": "coin"},
        "focal": {
            "type": "HERO_NUM",
            "target_val": 6_895_000,
            "prefix": "",
            "suffix": " đ",
            "color": TEAL,
            "pill": "BÙ TRỪ: 9.850.000 đ − 2.955.000 đ = 6.895.000 đ",
        },
        "arch_data": {
            "sub_mode": "NETTING_3",
            "net_cols": [
                ("PHẢI TRẢ NH QUÁN", "9.850.000 đ", "Từ hoá đơn của bạn", AMBER),
                ("PHẢI THU NGƯỢC LẠI", "−2.955.000 đ", "Từ giao dịch chiều ngược", CORAL),
                ("LỆNH CHUYỂN RÒNG", "= 6.895.000 đ", "Chỉ đi 1 lệnh duy nhất", GREEN),
            ],
        },
    },
    {
        "step": "BƯỚC 8/10 · TRẢ SAO KÊ & HOÀN 100K",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "HOÀN +100.000 đ",
        "archetype": "TWIN_SHOWDOWN",
        "beat_headlines": (
            ("CUỐI KỲ BẠN TRẢ ĐỦ 10TR", "10TR", NAVY),
            ("TIỀN HOÀN TỪ PHÍ INTERCHANGE 150K", "150K", GREEN),
        ),
        "phrase_beats": [
            ("CUỐI KỲ: BẠN TRẢ ĐỦ 10TR", "10TR", NAVY),
            ("NGÂN HÀNG HOÀN BẠN 100.000đ", "100.000đ", GREEN),
            ("TRÍCH TỪ 150.000đ PHÍ QUÁN TRẢ", "150.000đ", AMBER),
            ("TIỀN HOÀN CHỈ ĐI MỘT VÒNG", "MỘT VÒNG", TERRACOTTA),
        ],
        "actors": [
            {"id": 0, "tag": "TRẢ ĐỦ 10.000.000 đ", "beat": 1},
            {"id": 4, "tag": "THU 150K · HOÀN +100K", "beat": 2},
        ],
        "flow": {"kind": "pipe", "label": "BƯỚC 8/10 · THANH TOÁN SAO KÊ & CHIA TIỀN HOÀN", "prop": "coin"},
        "focal": {
            "type": "SPLIT_BAR",
            "left_lbl": "Hoàn cho bạn: +100.000 đ",
            "right_lbl": "NH giữ: +50.000 đ",
            "ratio": 0.67,
            "pill": "QUÁN CỘNG PHÍ VÀO GIÁ — TIỀN HOÀN ĐI 1 VÒNG",
        },
        "arch_data": {
            "left": {
                "kicker": "NGUỒN THU CỦA NGÂN HÀNG BẠN",
                "actor_id": 4,
                "big": "+150.000 đ",
                "sub": "Thu phí Interchange từ quán quen",
                "tag1": "Bạn thanh toán đủ 10.000.000 đ",
                "tag2": "Quán đã gánh 220.000 đ phí MDR",
                "accent": AMBER,
            },
            "right": {
                "kicker": "CHIA LẠI TIỀN HOÀN CHO BẠN",
                "actor_id": 0,
                "big": "+100.000 đ",
                "sub": "Trích từ chính 150.000 đ phí trên",
                "tag1": "Bạn nhận hoàn 1% (+100.000 đ)",
                "tag2": "Ngân hàng giữ phần dư +50.000 đ",
                "accent": GREEN,
            },
            "bridge": "TRÍCH TỪ",
        },
    },
    {
        "step": "BƯỚC 9/10 · XỬ LÝ KHI CÓ SỰ CỐ",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "XỬ LÝ SỰ CỐ",
        "archetype": "FULL_TRIPTYCH_3",
        "beat_headlines": (
            ("BA CÁCH XỬ LÝ SỰ CỐ", "BA CÁCH", CORAL),
            ("TIỀN VỀ KÉT VẪN BỊ TRỪ", "BỊ TRỪ", CORAL),
        ),
        "phrase_beats": [
            ("BA KỊCH BẢN KHI GẶP LỖI", "BA KỊCH BẢN", CORAL),
            ("1. REVERSAL: HUỶ NGAY TRONG CA", "REVERSAL", GREEN),
            ("2. REFUND: QUÁN HOÀN SAU T+2", "REFUND", AMBER),
            ("3. CHARGEBACK: KHIẾU NẠI CƯỠNG CHẾ", "CHARGEBACK", CORAL),
        ],
        "actors": [
            {"id": 1, "tag": "QUÁN HUỶ / HOÀN ĐƠN", "beat": 1},
            {"id": 0, "tag": "BẠN KHIẾU NẠI GIAO DỊCH", "beat": 2},
        ],
        "flow": {"kind": "wire", "label": "BƯỚC 9/10 · REVERSAL · REFUND · CHARGEBACK", "prop": "wire"},
        "focal": {
            "type": "TRIPTYCH_3",
            "cols": [
                ("1. REVERSAL", "Huỷ trong ca", "Gỡ giữ chỗ · 0 đ chạy"),
                ("2. REFUND", "Quán hoàn tiền", "Tiền chạy ngược lại"),
                ("3. CHARGEBACK", "Bạn khiếu nại", "NH trừ lại tiền quán"),
            ],
            "pill": "TUỲ AI KHỞI XƯỚNG MÀ ĐƯỜNG ĐI TIỀN KHÁC NHAU",
        },
        "arch_data": {
            "cards": [
                {
                    "num": "CON ĐƯỜNG 01",
                    "title": "REVERSAL",
                    "sub": "Huỷ ngay trong ca đêm T+0",
                    "when": "Trước khi chốt lô Clearing",
                    "flow": "Gỡ khoá hạn mức tức thì",
                    "impact": "0 đ tiền thật dịch chuyển",
                    "color": GREEN,
                },
                {
                    "num": "CON ĐƯỜNG 02",
                    "title": "REFUND",
                    "sub": "Quán chủ động hoàn sau T+2",
                    "when": "Sau khi tiền đã về két quán",
                    "flow": "Phát lệnh chuyển trả ngược",
                    "impact": "Mất 3–7 ngày làm việc",
                    "color": AMBER,
                },
                {
                    "num": "CON ĐƯỜNG 03",
                    "title": "CHARGEBACK",
                    "sub": "Bạn khiếu nại qua Ngân hàng",
                    "when": "Giao dịch gian lận / sai hàng",
                    "flow": "Tổ chức thẻ phân xử bắt buộc",
                    "impact": "Trừ ngược tiền + phạt phí quán",
                    "color": CORAL,
                },
            ],
        },
    },
    {
        "step": "BƯỚC 10/10 · VÒNG TRÒN GIÁ & KẾT",
        "ket": 9_780_000,
        "ket_pct": 0.978,
        "hud_right": "DƯ NỢ VỀ 0 đ",
        "archetype": "WATERFALL_SPLIT",
        "beat_headlines": (
            ("KHÔNG CÓ AI MIỄN PHÍ", "MIỄN PHÍ", NAVY),
            ("AI ĐÃ TRẢ PHÍ TRONG GIÁ?", "AI", TERRACOTTA),
        ),
        "phrase_beats": [
            ("TỔNG KẾT ĐƯỜNG ĐI 10.000.000đ", "10.000.000đ", NAVY),
            ("QUÁN THỰC NHẬN 9.780.000đ", "9.780.000đ", GREEN),
            ("HỆ THỐNG THẺ GIỮ 120.000đ", "120.000đ", TEAL),
            ("100.000đ HOÀN LẠI VÍ BẠN", "100.000đ", AMBER),
        ],
        "actors": [
            {"id": 1, "tag": "THỰC NHẬN 9,78TR", "beat": 1},
            {"id": 4, "tag": "CHIA 220K PHÍ MDR", "beat": 1},
            {"id": 0, "tag": "NHẬN HOÀN +100K", "beat": 2},
        ],
        "flow": {"kind": "loop", "label": "BƯỚC 10/10 · ĐÊM ĐẦU TK 1388 · T+2 VỀ KÉT · HOÀN 100K", "prop": "loop"},
        "focal": {
            "type": "HERO_NUM",
            "target_val": 10_000_000,
            "prefix": "",
            "suffix": " đ",
            "color": NAVY,
            "pill": "9.780.000 đ VỀ QUÁN  +  220.000 đ PHÍ  =  10.000.000 đ",
        },
        "arch_data": {
            "top_left": ("Tổng tiền bạn trả cuối kỳ (100%)", "10.000.000 đ", NAVY),
            "top_right": ("Tổng phí dịch chuyển (2,2%)", "220.000 đ", TERRACOTTA),
            "top_ratio": 0.72,
            "buckets": [
                {"title": "1. VỀ KÉT QUÁN QUEN", "sub": "Doanh thu thực nhận (97,8%)", "amt": "9.780.000 đ", "note": "Nhận vào ngày T+2 sau trừ phí", "color": GREEN, "actor_id": 1},
                {"title": "2. HỆ THỐNG THẺ & NH", "sub": "Phần giữ ròng (1,2%)", "amt": "120.000 đ", "note": "NH bạn 50K · NH quán 60K · Thẻ 10K", "color": TEAL, "actor_id": 3},
                {"title": "3. HOÀN LẠI CHO BẠN", "sub": "Cashback 1% từ phí quán", "amt": "100.000 đ", "note": "Quán tính vào giá bán mọi khách", "color": AMBER, "actor_id": 0},
            ],
        },
    },
]


# ── HÀM VẼ THÀNH PHẦN (HUD GỌN · SÂN KHẤU 1 TÂM ĐIỂM HỢP NHẤT · 0 ZONE 3) ──────

def make_parchment_canvas(W: int, H: int) -> Image.Image:
    base = Image.new("RGB", (W, H), PAPER_BG)
    draw = ImageDraw.Draw(base)
    dot_col = (229, 221, 204)
    step = 44
    cx, cy = W // 2, H // 2
    max_kx = (cx - 16) // step
    max_ky = (cy - 16) // step
    for ky in range(-max_ky, max_ky + 1):
        y = cy + ky * step
        for kx in range(-max_kx, max_kx + 1):
            x = cx + kx * step
            draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=dot_col)
    return base


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    cx: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> None:
    s = nfc(text)
    tw = draw.textlength(s, font=font)
    draw.text((cx - tw / 2.0, y), s, font=font, fill=fill)


def draw_highlighted_headline(
    draw: ImageDraw.ImageDraw,
    cx: float,
    y: float,
    headline: str,
    hi_substr: str,
    hi_color: tuple[int, int, int],
    font: ImageFont.FreeTypeFont,
) -> None:
    """Vẽ 1 dòng tiêu đề cực lớn căn giữa, tô màu đúng 1 cụm từ khoá không làm lệch vị trí chữ."""
    full_s = nfc(headline)
    hi_s = nfc(hi_substr)
    total_w = draw.textlength(full_s, font=font)
    x0 = cx - total_w / 2.0

    pos = full_s.find(hi_s) if hi_s else -1
    if pos < 0:
        draw.text((x0, y), full_s, font=font, fill=INK)
        return

    before = full_s[:pos]
    mid = full_s[pos : pos + len(hi_s)]
    after = full_s[pos + len(hi_s) :]
    if before:
        draw.text((x0, y), before, font=font, fill=INK)
    x_mid = x0 + draw.textlength(before, font=font)
    draw.text((x_mid, y), mid, font=font, fill=hi_color)
    if after:
        x_after = x0 + draw.textlength(before + mid, font=font)
        draw.text((x_after, y), after, font=font, fill=INK)


def draw_crafted_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int],
    width: int = 2,
    is_active: bool = False,
    accent: tuple[int, int, int] | None = None,
    inner_glow: bool = True,
) -> None:
    """Vẽ thẻ UI/UX chuẩn Bento: bóng đổ dọc 2 lớp đối xứng X, viền sáng nội bộ & thanh nhấn đỉnh."""
    x0, y0, x1, y1 = box
    if is_active:
        draw.rounded_rectangle((x0, y0 + 7, x1, y1 + 7), radius=radius, fill=(230, 223, 208))
        draw.rounded_rectangle((x0, y0 + 4, x1, y1 + 4), radius=radius, fill=(214, 205, 188))
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    if inner_glow and (x1 - x0) > 28 and (y1 - y0) > 28:
        ins = max(3, width + 1)
        hi_col = blend_rgb(fill, (255, 255, 255), 0.72)
        draw.rounded_rectangle((x0 + ins, y0 + ins, x1 - ins, y1 - ins), radius=max(2, radius - ins), outline=hi_col, width=1)
    if is_active and accent is not None and (x1 - x0) > 160 and (y1 - y0) > 64:
        bar_w = min(92.0, (x1 - x0) * 0.22)
        bcx = (x0 + x1) / 2.0
        by = y0 + max(5, width + 2)
        draw.rounded_rectangle((bcx - bar_w / 2.0, by, bcx + bar_w / 2.0, by + 4), radius=2, fill=accent)


def _draw_centered_bbox_text(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> None:
    s = nfc(text)
    sb = draw.textbbox((0, 0), s, font=font)
    draw.text((cx - (sb[0] + sb[2]) / 2.0, cy - (sb[1] + sb[3]) / 2.0), s, font=font, fill=fill)


def draw_hud(
    draw: ImageDraw.ImageDraw,
    hud_box: tuple[int, int, int, int],
    sc: dict[str, Any],
    s_idx: int,
    n_scenes: int,
    s_prog: float,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
    is_short: bool,
) -> None:
    hx0, hy0, hx1, hy1 = hud_box
    hcx = (hx0 + hx1) / 2.0
    draw_crafted_card(draw, hud_box, radius=18, fill=PAPER_CARD, outline=INK, width=3, is_active=True, accent=None)

    # Hiệu ứng đếm két quán khi bước sang T+2 (s_idx == 2 Short hoặc s_idx == 5 Long)
    if sc["ket"] > 0 and ((is_short and s_idx == 2) or (not is_short and s_idx == 5)):
        u = ease_out_cubic(min(1.0, t_local / 2.4))
        disp_ket = step_quantize(sc["ket"] * u, step=10_000) if u < 0.99 else sc["ket"]
    else:
        disp_ket = sc["ket"]

    n_steps = max(1, n_scenes - 1)
    cur_step = s_idx
    left_metric = nfc(sc.get("hud_left") or f"KÉT QUÁN: {fmt_vnd(disp_ket)}")

    if is_short:
        if cur_step == 0:
            # Màn MỞ ĐẦU (Hook): 0 số bước 1..5 — chỉ 1 nhãn MỞ ĐẦU căn giữa + 2 viên số nghịch lý
            step_txt = nfc(sc["step"])
            tw = draw.textlength(step_txt, font=fonts["hud_title"])
            pw = tw + 36
            draw.rounded_rectangle(
                (hcx - pw / 2.0, hy0 + 12, hcx + pw / 2.0, hy0 + 46),
                radius=15,
                fill=AMBER_LIGHT,
                outline=AMBER,
                width=2,
            )
            _draw_centered_bbox_text(draw, hcx, hy0 + 29, step_txt, fonts["hud_title"], INK)

            pill_top, pill_bot = hy0 + 58, hy0 + 98
            lp_box = (hx0 + 24, pill_top, int(hcx - 8), pill_bot)
            rp_box = (int(hcx + 8), pill_top, hx1 - 24, pill_bot)
            l_bg = GREEN_LIGHT if disp_ket > 0 else PAPER_FLOOR
            l_bd = GREEN if disp_ket > 0 else PAPER_SOFT
            draw_crafted_card(draw, lp_box, radius=12, fill=l_bg, outline=l_bd, width=2, is_active=False, inner_glow=disp_ket > 0)
            draw_crafted_card(draw, rp_box, radius=12, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=2, is_active=False, inner_glow=False)

            l_col = GREEN if disp_ket > 0 else (INK if sc.get("hud_left") else INK_MUTED)
            draw_centered_text(draw, (lp_box[0] + lp_box[2]) / 2.0, pill_top + 8, left_metric, fonts["hud_val"], l_col)
            r_txt = nfc(sc["hud_right"])
            draw_centered_text(draw, (rp_box[0] + rp_box[2]) / 2.0, pill_top + 8, r_txt, fonts["hud_sub"], GREEN if "+100" in r_txt else INK)
        else:
            # Màn BƯỚC 1..5: Thanh lộ trình 5 bước cố định kèm tên ngắn xuyên suốt mọi màn
            cw, cg = 170, 11
            tot_w = 5 * cw + 4 * cg  # 894 px (căn đối xứng tuyệt đối qua x=540)
            x0_start = int(round(hcx - tot_w / 2.0))
            cy_top, cy_bot = hy0 + 14, hy1 - 14
            conn_y = (cy_top + cy_bot) / 2.0

            for ci in range(4):
                rx_prev_end = x0_start + ci * (cw + cg) + cw
                rx_next_start = x0_start + (ci + 1) * (cw + cg)
                c_col = GREEN if (ci + 1) < cur_step else PAPER_SOFT
                draw.line([(rx_prev_end, conn_y), (rx_next_start, conn_y)], fill=c_col, width=3)

            step_cards = sc.get("step_cards", SHORT_STEP_CARDS)
            for step_i in range(1, 6):
                st_tag, st_lbl = step_cards[step_i - 1]
                rx0 = x0_start + (step_i - 1) * (cw + cg)
                rx1 = rx0 + cw
                rcx = (rx0 + rx1) / 2.0

                if step_i == cur_step:
                    draw.rounded_rectangle((rx0, cy_top + 4, rx1, cy_bot + 4), radius=14, fill=(214, 205, 188))
                    draw.rounded_rectangle((rx0, cy_top, rx1, cy_bot), radius=14, fill=AMBER_LIGHT, outline=INK, width=3)
                    draw.rounded_rectangle((rx0 + 14, cy_top + 7, rx1 - 14, cy_top + 35), radius=10, fill=AMBER, outline=INK, width=2)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 21, st_tag, fonts["card_kicker"], INK)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 61, st_lbl, fonts["bubble_sm"], INK)
                elif step_i < cur_step:
                    draw.rounded_rectangle((rx0, cy_top, rx1, cy_bot), radius=14, fill=GREEN_LIGHT, outline=GREEN, width=2)
                    draw.rounded_rectangle((rx0 + 14, cy_top + 7, rx1 - 14, cy_top + 35), radius=10, fill=GREEN)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 21, f"XONG B{step_i}", fonts["card_kicker"], PAPER_CARD)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 61, st_lbl, fonts["bubble_sm"], GREEN)
                else:
                    draw.rounded_rectangle((rx0, cy_top, rx1, cy_bot), radius=14, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=1)
                    draw.rounded_rectangle((rx0 + 14, cy_top + 7, rx1 - 14, cy_top + 35), radius=10, fill=PAPER_SOFT)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 21, st_tag, fonts["card_kicker"], INK_MUTED)
                    _draw_centered_bbox_text(draw, rcx, cy_top + 61, st_lbl, fonts["bubble_sm"], INK_MUTED)

    else:
        # 16:9 1 hàng: Hook (cur_step == 0) không vẽ khay 1..10; Step 1..10 có hộp BƯỚC i/10 nổi bật + khay 1..10
        hcy = (hy0 + hy1) / 2.0
        step_txt = nfc(sc["step"])
        tw = draw.textlength(step_txt, font=fonts["hud_title"])
        if cur_step == 0:
            draw.rounded_rectangle(
                (hx0 + 24, hcy - 18, hx0 + 24 + tw + 28, hcy + 18),
                radius=14,
                fill=AMBER_LIGHT,
                outline=AMBER,
                width=2,
            )
            _draw_centered_bbox_text(draw, hx0 + 24 + (tw + 28) / 2.0, hcy, step_txt, fonts["hud_title"], INK)
        else:
            draw.rounded_rectangle(
                (hx0 + 20, hcy - 19, hx0 + 20 + tw + 28, hcy + 19),
                radius=14,
                fill=AMBER_LIGHT,
                outline=INK,
                width=3,
            )
            _draw_centered_bbox_text(draw, hx0 + 20 + (tw + 28) / 2.0, hcy, step_txt, fonts["hud_title"], INK)

            seg_area_w = 346
            seg_gap = 4
            seg_w = (seg_area_w - seg_gap * (n_steps - 1)) / float(n_steps)
            sx_start = hcx - seg_area_w / 2.0
            draw.rounded_rectangle((sx_start - 8, hcy - 17, sx_start + seg_area_w + 8, hcy + 17), radius=12, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=1)
            for step_i in range(1, n_steps + 1):
                px0 = sx_start + (step_i - 1) * (seg_w + seg_gap)
                px1 = px0 + seg_w
                py_top, py_bot = hcy - 13, hcy + 13
                if step_i > cur_step:
                    draw.rounded_rectangle((px0, py_top, px1, py_bot), radius=8, fill=PAPER_SOFT)
                    txt_col = INK_MUTED
                elif step_i < cur_step:
                    draw.rounded_rectangle((px0, py_top, px1, py_bot), radius=8, fill=GREEN)
                    txt_col = PAPER_CARD
                else:
                    draw.rounded_rectangle((px0, py_top, px1, py_bot), radius=8, fill=AMBER, outline=INK, width=2)
                    txt_col = INK
                _draw_centered_bbox_text(draw, (px0 + px1) / 2.0, hcy, str(step_i), fonts["slice_lbl"], txt_col)

        sep_lbl = "  ·  "
        cb_lbl = nfc(sc["hud_right"])
        f_r = fonts["hud_val"]
        w_ket = draw.textlength(left_metric, font=f_r)
        w_sep = draw.textlength(sep_lbl, font=f_r)
        w_cb = draw.textlength(cb_lbl, font=f_r)
        max_rw = hx1 - 28 - (hcx + 181 + 20)
        if (w_ket + w_sep + w_cb) > max_rw:
            f_r = fonts["hud_title"]
            w_ket = draw.textlength(left_metric, font=f_r)
            w_sep = draw.textlength(sep_lbl, font=f_r)
            w_cb = draw.textlength(cb_lbl, font=f_r)
        rx_start = hx1 - 28 - (w_ket + w_sep + w_cb)
        l_col = GREEN if disp_ket > 0 else (INK if sc.get("hud_left") else INK_MUTED)
        draw.text((rx_start, hcy - 12), left_metric, font=f_r, fill=l_col)
        draw.text((rx_start + w_ket, hcy - 12), sep_lbl, font=f_r, fill=INK_MUTED)
        draw.text((rx_start + w_ket + w_sep, hcy - 12), cb_lbl, font=f_r, fill=INK)


def draw_actor_node(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    sprites: SpriteBank,
    actor_cfg: dict[str, Any],
    cx: float,
    cy: float,
    focus_u: float,
    t_local: float,
    actor_idx: int,
    fonts: dict[str, ImageFont.FreeTypeFont],
    compact: bool = False,
) -> None:
    """Vẽ 1 định chế 2D chỉnh chu với vầng sáng nhịp thở 30fps, bong bóng liền mũi nhọn & bệ tên 2 tầng."""
    aid = actor_cfg["id"]
    arch = ARCHETYPES[aid]
    is_bright = focus_u >= 0.55
    base_sz = sprites.size

    breath = 1.0 + 0.032 * math.sin(2.0 * math.pi * 0.72 * t_local + actor_idx * 0.9) if is_bright else 1.0
    sp = sprites.get_scaled(aid, focused=is_bright, scale=breath)
    cur_sz = sp.width

    if is_bright:
        pulse = 0.5 + 0.5 * math.sin(2.0 * math.pi * 1.1 * t_local + actor_idx)
        outer_r = base_sz // 2 + 14 + int(round(4 * pulse))
        halo_col = blend_rgb(PAPER_CARD, arch["accent"], 0.18 + 0.12 * pulse)
        draw.ellipse((cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r), fill=halo_col)
        ring_r = base_sz // 2 + 7 + int(round(2 * pulse))
        draw.ellipse((cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r), outline=arch["accent"], width=4)
        # Hai chấm định vị đối xứng ngang trên vòng halo
        tk_r = 4
        draw.ellipse((cx - ring_r - tk_r, cy - tk_r, cx - ring_r + tk_r, cy + tk_r), fill=PAPER_CARD, outline=arch["accent"], width=2)
        draw.ellipse((cx + ring_r - tk_r, cy - tk_r, cx + ring_r + tk_r, cy + tk_r), fill=PAPER_CARD, outline=arch["accent"], width=2)

    canvas.paste(sp, (int(round(cx - cur_sz / 2.0)), int(round(cy - cur_sz / 2.0))), sp)

    # 1. Bong bóng hành động phía trên có mũi nhọn liền viền sắc nét
    tag_txt = nfc(actor_cfg["tag"])
    f_tag = fonts["bubble_sm"] if compact else fonts["bubble"]
    tw = draw.textlength(tag_txt, font=f_tag)
    pw = tw + (22 if compact else 28)
    ph = 36 if compact else 40
    by1 = cy - base_sz / 2.0 - 16
    by0 = by1 - ph
    bx0, bx1 = cx - pw / 2.0, cx + pw / 2.0
    b_fill = arch["bg"] if is_bright else dim_color(arch["bg"], 0.28)
    b_outline = INK if is_bright else dim_color(INK, 0.28)
    b_txt = INK if is_bright else dim_color(INK, 0.34)
    if is_bright:
        draw.rounded_rectangle((bx0, by0 + 4, bx1, by1 + 4), radius=13, fill=(224, 216, 200))
        draw.polygon([(cx - 10, by1 + 2), (cx + 10, by1 + 2), (cx, by1 + 12)], fill=b_outline)
    draw.rounded_rectangle((bx0, by0, bx1, by1), radius=13, fill=b_fill, outline=b_outline, width=3 if is_bright else 2)
    draw.polygon([(cx - 8, by1 - 2), (cx + 8, by1 - 2), (cx, by1 + 9)], fill=b_fill)
    if is_bright:
        draw.line([(cx - 8, by1), (cx, by1 + 9), (cx + 8, by1)], fill=b_outline, width=3, joint="curve")
    draw_centered_text(draw, cx, by0 + (7 if compact else 8), tag_txt, f_tag, b_txt)

    # 2. Bệ tên định chế 2 tầng (LUẬT 10: mỗi nhãn 1 hàng Y riêng biệt)
    name_txt = nfc(actor_cfg.get("name") or arch["name"])
    f_name = fonts["actor_name_sm"] if compact else fonts["actor_name"]
    nw = draw.textlength(name_txt, font=f_name)
    npw = max(nw + 24, 118 if compact else 136)
    nph = 34 if compact else 38
    ny0 = cy + base_sz / 2.0 + 12
    ny1 = ny0 + nph
    nx0, nx1 = cx - npw / 2.0, cx + npw / 2.0
    n_fill = INK if is_bright else dim_color(INK, 0.36)
    if is_bright:
        draw.rounded_rectangle((nx0, ny0 + 3, nx1, ny1 + 3), radius=11, fill=(220, 212, 196))
    draw.rounded_rectangle((nx0, ny0, nx1, ny1), radius=11, fill=n_fill)
    if is_bright:
        draw.rounded_rectangle((nx0 + 2, ny0 + 2, nx1 - 2, ny1 - 2), radius=9, outline=blend_rgb(INK, PAPER_CARD, 0.25), width=1)
    draw_centered_text(draw, cx, ny0 + (5 if compact else 6), name_txt, f_name, PAPER_CARD)

    sub_txt = nfc(actor_cfg.get("sub") or arch["sub"])
    sub_w = draw.textlength(sub_txt, font=fonts["actor_sub"]) + 20
    sub_y0 = ny1 + 5
    draw.rounded_rectangle(
        (cx - sub_w / 2.0, sub_y0, cx + sub_w / 2.0, sub_y0 + 23),
        radius=10,
        fill=PAPER_FLOOR if is_bright else dim_color(PAPER_FLOOR, 0.55),
        outline=PAPER_SOFT if is_bright else dim_color(PAPER_SOFT, 0.5),
        width=1,
    )
    draw_centered_text(
        draw,
        cx,
        sub_y0 + 3,
        sub_txt,
        fonts["actor_sub"],
        INK_MUTED if is_bright else dim_color(INK_MUTED, 0.35),
    )


def draw_flow_segment(
    draw: ImageDraw.ImageDraw,
    p0: tuple[float, float],
    p1: tuple[float, float],
    flow_cfg: dict[str, Any],
    t_local: float,
    is_loop_reverse_arc: bool = False,
) -> None:
    """Vẽ đường dẫn tín hiệu / dòng tiền có cổng nối, vỏ ống & hoạt cảnh 30fps."""
    kind = flow_cfg["kind"]
    col = GREEN if kind == "pipe" else (TERRACOTTA if kind == "loop" else AMBER)
    span = p1[0] - p0[0]
    if span < 28:
        return

    if kind == "wire":
        # Đường ray nền + xung nét đứt
        draw.line([p0, (p1[0] - 6, p1[1])], fill=PAPER_SOFT, width=5)
        steps = 12
        for si in range(0, steps, 2):
            u0 = si / steps
            u1 = min(1.0, (si + 1.15) / steps)
            draw.line(
                [(lerp(p0[0], p1[0], u0), lerp(p0[1], p1[1], u0)), (lerp(p0[0], p1[0], u1), lerp(p0[1], p1[1], u1))],
                fill=col,
                width=5,
            )
        draw.ellipse((p0[0] - 6, p0[1] - 6, p0[0] + 6, p0[1] + 6), fill=PAPER_CARD, outline=col, width=3)
        ax, ay = p1[0] - 8, p1[1]
        draw.polygon([(ax + 12, ay), (ax - 5, ay - 9), (ax - 5, ay + 9)], fill=col)

        for pi in range(3):
            u = ((t_local * 0.55) + pi / 3.0) % 1.0
            px = lerp(p0[0] + 8, p1[0] - 10, u)
            py = p0[1]
            r = 8 if pi == 0 else 6
            draw.ellipse((px - r - 3, py - r - 3, px + r + 3, py + r + 3), fill=AMBER_LIGHT)
            draw.ellipse((px - r, py - r, px + r, py + r), fill=col, outline=INK, width=2)
            draw.ellipse((px - 2, py - 2, px + 2, py + 2), fill=PAPER_CARD)

    elif kind == "pipe":
        # Vỏ ống 2 lớp + cổng đầu ống + đồng xu đúc nổi chạy 30fps
        draw.line([p0, (p1[0] - 6, p1[1])], fill=blend_rgb(PAPER_SOFT, col, 0.24), width=16)
        draw.line([(p0[0], p0[1] - 8), (p1[0] - 8, p1[1] - 8)], fill=blend_rgb(INK, PAPER_CARD, 0.62), width=1)
        draw.line([(p0[0], p0[1] + 8), (p1[0] - 8, p1[1] + 8)], fill=blend_rgb(INK, PAPER_CARD, 0.62), width=1)
        draw.line([p0, (p1[0] - 4, p1[1])], fill=col, width=5)
        draw.ellipse((p0[0] - 7, p0[1] - 7, p0[0] + 7, p0[1] + 7), fill=PAPER_CARD, outline=col, width=3)
        ax, ay = p1[0] - 8, p1[1]
        draw.polygon([(ax + 13, ay), (ax - 6, ay - 10), (ax - 6, ay + 10)], fill=col)

        for ci in range(2):
            u = ((t_local * 0.42) + ci * 0.5) % 1.0
            ox = lerp(p0[0] + 12, p1[0] - 14, ease_in_out_sine(u))
            oy = p0[1]
            draw.ellipse((ox - 13, oy - 13, ox + 13, oy + 13), fill=GOLD, outline=INK, width=3)
            draw.ellipse((ox - 8, oy - 8, ox + 8, oy + 8), outline=(255, 232, 152), width=1)
            draw.ellipse((ox - 5, oy - 5, ox + 5, oy + 5), fill=GREEN)

    else:
        mid_y = p0[1]
        h_off = 26
        pts_top = []
        pts_bot = []
        for si in range(25):
            u = si / 24.0
            ang = math.pi * u
            pts_top.append((lerp(p0[0], p1[0], u), mid_y - math.sin(ang) * h_off - 6))
            pts_bot.append((lerp(p1[0], p0[0], u), mid_y + math.sin(ang) * h_off + 6))
        draw.line(pts_top, fill=TERRACOTTA, width=4)
        draw.line(pts_bot, fill=GREEN, width=4)
        draw.ellipse((p0[0] - 5, mid_y - 11, p0[0] + 5, mid_y - 1), fill=PAPER_CARD, outline=TERRACOTTA, width=2)
        draw.ellipse((p1[0] - 5, mid_y + 1, p1[0] + 5, mid_y + 11), fill=PAPER_CARD, outline=GREEN, width=2)
        draw.polygon([(p1[0] + 6, mid_y - 6), (p1[0] - 10, mid_y - 14), (p1[0] - 10, mid_y + 2)], fill=TERRACOTTA)
        draw.polygon([(p0[0] - 6, mid_y + 6), (p0[0] + 10, mid_y - 2), (p0[0] + 10, mid_y + 14)], fill=GREEN)

        u1 = (t_local * 0.45) % 1.0
        tx = lerp(p0[0], p1[0], u1)
        ty = mid_y - math.sin(math.pi * u1) * h_off - 6
        draw.ellipse((tx - 11, ty - 11, tx + 11, ty + 11), fill=CORAL, outline=INK, width=2)

        u2 = (t_local * 0.45 + 0.5) % 1.0
        bx = lerp(p1[0], p0[0], u2)
        by = mid_y + math.sin(math.pi * u2) * h_off + 6
        draw.ellipse((bx - 11, by - 11, bx + 11, by + 11), fill=GOLD, outline=INK, width=2)


def draw_prop_badge(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    prop_kind: str,
    t_local: float,
    font_small: ImageFont.FreeTypeFont,
    show_label: bool = True,
) -> None:
    """Vẽ icon trực quan siêu gọn trên khoảng trống giữa track (T+2 clock hoặc khoá giữ chỗ)."""
    if prop_kind == "clock":
        r = 22
        draw.ellipse((cx - r, cy - r + 2, cx + r, cy + r + 2), fill=(224, 216, 200))
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=PAPER_CARD, outline=INK, width=3)
        draw.ellipse((cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4), outline=PAPER_SOFT, width=1)
        ang = t_local * 2.4 - math.pi / 2.0
        draw.line([(cx, cy), (cx + math.cos(ang) * 13, cy + math.sin(ang) * 13)], fill=GREEN, width=3)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=INK)
        if show_label:
            draw_centered_text(draw, cx, cy + r + 5, "T+2", font_small, GREEN)
    elif prop_kind == "lock":
        draw.arc((cx - 10, cy - 22, cx + 10, cy - 2), 180, 360, fill=INK, width=4)
        draw.rounded_rectangle((cx - 14, cy - 11, cx + 14, cy + 12), radius=5, fill=AMBER, outline=INK, width=3)
        draw.ellipse((cx - 3, cy - 2, cx + 3, cy + 4), fill=INK)


def draw_focal_floor(
    draw: ImageDraw.ImageDraw,
    fbox: tuple[int, int, int, int],
    focal: dict[str, Any],
    beat2_u: float,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
    phrase_idx: int,
    is_short: bool,
) -> None:
    """
    Vẽ tầng dưới ngay trong lòng Sân khấu thống nhất (KHÔNG dùng khung viền đen lồng hộp).
    Dùng ô trưng bày sáng tinh tế (Display Well) làm nổi bật 1 con số/thanh tỷ lệ trực quan duy nhất.
    """
    fx0, fy0, fx1, fy1 = fbox
    fw = fx1 - fx0
    fcx = (fx0 + fx1) / 2.0

    draw.rounded_rectangle(fbox, radius=20, fill=PAPER_FLOOR)
    draw.line([(fx0 + 24, fy0), (fx1 - 24, fy0)], fill=PAPER_SOFT, width=3)

    py0 = fy1 - (54 if is_short else 52)
    py1 = py0 + 38

    # Ô trưng bày trung tâm giúp con số hoặc thanh đo có chiều sâu UI/UX chỉnh chu mà vẫn rất thoáng
    well_box = (fx0 + 24, fy0 + 18, fx1 - 24, py0 - 16)
    draw_crafted_card(draw, well_box, radius=18, fill=PAPER_CARD, outline=PAPER_SOFT, width=2, is_active=False, inner_glow=True)

    ftype = focal["type"]
    mid_y = (well_box[1] + well_box[3]) / 2.0

    if ftype == "HERO_NUM":
        if "target_val" in focal:
            u = ease_out_cubic(min(1.0, max(0.0, t_local - 0.15) / 1.45))
            tval = focal["target_val"]
            cur_v = step_quantize(tval * u, step=5_000 if tval <= 200_000 else 100_000) if u < 0.99 else tval
            num_txt = f"{focal.get('prefix', '')}{int(cur_v):,}".replace(",", ".") + focal.get("suffix", "")
        else:
            num_txt = nfc(focal["fixed_text"])

        f_num = fonts["focal_hero"]
        if draw.textlength(num_txt, font=f_num) > fw - 96:
            f_num = fonts["focal_big"]
        sb = draw.textbbox((0, 0), num_txt, font=f_num)
        num_h = sb[3] - sb[1]
        num_y = mid_y - num_h * 0.62 - 14
        draw_centered_text(draw, fcx, num_y, num_txt, f_num, focal["color"])
        # Thanh nhấn mảnh đối xứng bên dưới đáy thực tế của con số lớn
        acc_w = min(156.0, max(84.0, draw.textlength(num_txt, font=f_num) * 0.34))
        acc_y = num_y + sb[3] + 18
        draw.rounded_rectangle((fcx - acc_w / 2.0, acc_y, fcx + acc_w / 2.0, acc_y + 6), radius=3, fill=focal["color"])
        draw.ellipse((fcx - acc_w / 2.0 - 14, acc_y, fcx - acc_w / 2.0 - 8, acc_y + 6), fill=PAPER_SOFT)
        draw.ellipse((fcx + acc_w / 2.0 + 8, acc_y, fcx + acc_w / 2.0 + 14, acc_y + 6), fill=PAPER_SOFT)

    elif ftype in ("SPLIT_BAR", "HOLD_GAUGE"):
        bar_x0, bar_x1 = fx0 + (48 if is_short else 72), fx1 - (48 if is_short else 72)
        bar_h = 74 if is_short else 76
        bar_y0, bar_y1 = int(mid_y - bar_h / 2) - 8, int(mid_y + bar_h / 2) - 8
        bw = bar_x1 - bar_x0
        anim_u = ease_out_cubic(min(1.0, max(0.08, t_local / 1.1)))
        ratio = focal["ratio"]
        cur_ratio = lerp(0.5, ratio, anim_u) if ftype == "SPLIT_BAR" else lerp(0.08, ratio, anim_u)
        split_x = int(bar_x0 + bw * ratio)
        fill_split_x = int(bar_x0 + bw * cur_ratio)
        c_left = AMBER if ftype == "HOLD_GAUGE" else GREEN
        c_right = PAPER_SOFT if ftype == "HOLD_GAUGE" else CORAL

        # Máng đỡ bao ngoài thanh đo
        draw.rounded_rectangle((bar_x0 - 7, bar_y0 - 7, bar_x1 + 7, bar_y1 + 7), radius=18, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=2)
        draw.rounded_rectangle((bar_x0, bar_y0, max(bar_x0 + 40, fill_split_x - 4), bar_y1), radius=14, fill=c_left, outline=INK, width=2)
        draw.rounded_rectangle((split_x + 4, bar_y0, bar_x1, bar_y1), radius=14, fill=c_right, outline=INK, width=2)
        if anim_u > 0.65:
            alpha_t = smoothstep(0.65, 1.0, anim_u)
            l_col = blend_rgb(c_left, PAPER_CARD, alpha_t)
            draw_centered_text(draw, (bar_x0 + split_x - 4) / 2.0, bar_y0 + (bar_h - 28) // 2, nfc(focal["left_lbl"]), fonts["bar_lbl"], l_col)
        r_col = INK if ftype == "HOLD_GAUGE" else PAPER_CARD
        draw_centered_text(draw, (split_x + 4 + bar_x1) / 2.0, bar_y0 + (bar_h - 28) // 2, nfc(focal["right_lbl"]), fonts["bar_lbl"], r_col)

        # Thước chia 3 vạch đối xứng bên dưới thanh đo
        ry = bar_y1 + 22
        draw.line([(bar_x0, ry), (bar_x1, ry)], fill=PAPER_SOFT, width=2)
        for tx in (bar_x0, (bar_x0 + bar_x1) / 2.0, bar_x1):
            draw.line([(tx, ry - 5), (tx, ry + 5)], fill=blend_rgb(INK_MUTED, PAPER_CARD, 0.35), width=2)

    elif ftype == "THREE_SLICE":
        bar_x0, bar_x1 = fx0 + (48 if is_short else 72), fx1 - (48 if is_short else 72)
        bar_h = 92 if is_short else 88
        bar_y0, bar_y1 = int(mid_y - bar_h / 2) - 6, int(mid_y + bar_h / 2) - 6
        bw = bar_x1 - bar_x0
        anim_u = ease_out_cubic(min(1.0, max(0.08, t_local / 1.1)))
        draw.rounded_rectangle((bar_x0 - 7, bar_y0 - 7, bar_x1 + 7, bar_y1 + 7), radius=18, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=2)
        cur_x = float(bar_x0)
        for idx, (lbl, amt, share, col) in enumerate(focal["slices"]):
            sw_full = bw * share - 6
            sw_px = max(24.0, sw_full * lerp(0.25, 1.0, anim_u))
            draw.rounded_rectangle((cur_x, bar_y0, cur_x + sw_px, bar_y1), radius=14, fill=col, outline=INK, width=2)
            if anim_u > 0.65:
                draw_centered_text(draw, cur_x + sw_full / 2.0, bar_y0 + 13, nfc(lbl), fonts["slice_lbl"], PAPER_CARD)
                draw_centered_text(draw, cur_x + sw_full / 2.0, bar_y0 + 44, nfc(amt), fonts["bar_lbl"], PAPER_CARD)
            cur_x += sw_full + 8

    elif ftype == "T_ACCOUNT":
        pill_w = fw - 120
        px0 = fx0 + 60
        row_h = 46
        draw.rounded_rectangle((px0, mid_y - 50, px0 + pill_w, mid_y - 50 + row_h), radius=12, fill=AMBER_LIGHT, outline=AMBER, width=2)
        draw_centered_text(draw, fcx, mid_y - 40, nfc(focal["debit"]), fonts["bar_lbl"], INK)

        c_bg = blend_rgb(PAPER_CARD, GREEN_LIGHT, 0.35 + 0.65 * beat2_u)
        c_bd = blend_rgb(PAPER_SOFT, GREEN, 0.35 + 0.65 * beat2_u)
        c_ink = INK if beat2_u > 0.25 else INK_MUTED
        draw.rounded_rectangle((px0, mid_y + 8, px0 + pill_w, mid_y + 8 + row_h), radius=12, fill=c_bg, outline=c_bd, width=2)
        draw_centered_text(draw, fcx, mid_y + 18, nfc(focal["credit"]), fonts["bar_lbl"], c_ink)

    elif ftype in ("CHECKLIST_3", "TRIPTYCH_3"):
        cols = focal.get("items") or focal.get("cols")
        n = len(cols)
        gap = 20
        cw = (fw - 120 - gap * (n - 1)) / float(n)
        for ci, item in enumerate(cols):
            cx0 = fx0 + 60 + ci * (cw + gap)
            cx1 = cx0 + cw
            is_hi = (ci == (phrase_idx % n)) if ftype == "TRIPTYCH_3" else (t_local >= ci * 4.0)
            bg_c = AMBER_LIGHT if (is_hi and ftype == "TRIPTYCH_3") else (GREEN_LIGHT if is_hi else PAPER_CARD)
            bd_c = INK if is_hi else dim_color(INK, 0.35)
            draw.rounded_rectangle((cx0, mid_y - 42, cx1, mid_y + 44), radius=14, fill=bg_c, outline=bd_c, width=3 if is_hi else 2)
            if isinstance(item, tuple):
                draw_centered_text(draw, (cx0 + cx1) / 2.0, mid_y - 30, nfc(item[0]), fonts["bar_lbl"], INK if is_hi else INK_MUTED)
                draw_centered_text(draw, (cx0 + cx1) / 2.0, mid_y + 6, nfc(item[2]), fonts["actor_sub"], INK if is_hi else INK_MUTED)
            else:
                draw_centered_text(draw, (cx0 + cx1) / 2.0, mid_y - 12, nfc(item), fonts["bar_lbl"], INK if is_hi else INK_MUTED)

    # 1 Thẻ tóm tắt cực gọn duy nhất (pill <= 9 từ) ngay dưới ô trưng bày
    pill_txt = nfc(focal["pill"])
    pw = min(fw - 48, draw.textlength(pill_txt, font=fonts["focal_pill"]) + 36)
    draw.rounded_rectangle((fcx - pw / 2.0, py0 + 3, fcx + pw / 2.0, py1 + 3), radius=19, fill=(228, 220, 204))
    draw.rounded_rectangle((fcx - pw / 2.0, py0, fcx + pw / 2.0, py1), radius=19, fill=PAPER_CARD, outline=PAPER_SOFT, width=2)
    draw_centered_text(draw, fcx, py0 + 8, pill_txt, fonts["focal_pill"], INK)


# ── ĐẠO DIỄN 5 KHUÔN HÌNH VIDEO DÀI 16:9 (v6.0 ANTI-MONOTONY) ────────────────

def draw_takeaway_pill(
    draw: ImageDraw.ImageDraw,
    fcx: float,
    py0: int,
    max_w: float,
    text: str,
    font: ImageFont.FreeTypeFont,
) -> None:
    pill_txt = nfc(text)
    pw = min(max_w, draw.textlength(pill_txt, font=font) + 40)
    py1 = py0 + 38
    draw.rounded_rectangle((fcx - pw / 2.0, py0 + 3, fcx + pw / 2.0, py1 + 3), radius=19, fill=(228, 220, 204))
    draw_crafted_card(draw, (fcx - pw / 2.0, py0, fcx + pw / 2.0, py1), radius=19, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=2, is_active=False, inner_glow=True)
    draw_centered_text(draw, fcx, py0 + 7, pill_txt, font, INK)


def draw_long_twin_showdown(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    sprites: SpriteBank,
    sc: dict[str, Any],
    beat4_idx: int,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Khuôn hình 1: Bàn cân đối xứng 2 thế giới qua trục x=960 (Bề mặt vs Sự thật)."""
    ad = sc["arch_data"]
    if sc.get("ket", 0) > 0:
        focus_seq = [(1.0, 0.30), (0.32, 1.0), (1.0, 0.32), (1.0, 1.0)]
    else:
        focus_seq = [(1.0, 0.30), (1.0, 0.32), (0.32, 1.0), (1.0, 1.0)]
    f_left, f_right = focus_seq[min(3, beat4_idx)]

    cards = [
        ((124, 388, 892, 878), ad["left"], f_left, 0),
        ((1028, 388, 1796, 878), ad["right"], f_right, 1),
    ]
    for box, cfg, fu, idx in cards:
        x0, y0, x1, y1 = box
        cx = (x0 + x1) / 2.0
        is_bright = fu >= 0.7
        acc = cfg["accent"]
        bg_card = blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.45) if is_bright else blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.15)
        bd_col = acc if is_bright else dim_color(INK, 0.32)
        draw_crafted_card(draw, box, radius=22, fill=bg_card, outline=bd_col, width=4 if is_bright else 2, is_active=is_bright, accent=acc)

        # 1. Kicker pill
        k_txt = nfc(cfg["kicker"])
        kw = draw.textlength(k_txt, font=fonts["card_kicker"]) + 32
        k_fill = blend_rgb(PAPER_CARD, acc, 0.18 if is_bright else 0.08)
        draw.rounded_rectangle((cx - kw / 2.0, y0 + 18, cx + kw / 2.0, y0 + 50), radius=16, fill=k_fill, outline=dim_color(acc, fu), width=2)
        draw_centered_text(draw, cx, y0 + 24, k_txt, fonts["card_kicker"], dim_color(INK, max(0.45, fu)))

        # 2. Sprite định chế với halo định vị tinh tế
        aid = cfg["actor_id"]
        breath = 1.0 + 0.03 * math.sin(2.0 * math.pi * 0.72 * t_local + idx) if is_bright else 1.0
        sp = sprites.get_scaled(aid, focused=is_bright, scale=0.84 * breath)
        scy = y0 + 130
        if is_bright:
            r_h = int(sp.width * 0.56)
            draw.ellipse((cx - r_h, scy - r_h, cx + r_h, scy + r_h), fill=blend_rgb(PAPER_CARD, acc, 0.20), outline=dim_color(acc, 0.42), width=2)
        canvas.paste(sp, (int(round(cx - sp.width / 2.0)), int(round(scy - sp.height / 2.0))), sp)

        # 3. Con số lớn & mô tả (1 hàng Y = 1 dòng chữ)
        big_txt = nfc(cfg["big"])
        f_big = fonts["focal_big"]
        draw_centered_text(draw, cx, y0 + 218, big_txt, f_big, dim_color(acc, max(0.35, fu)))
        draw_centered_text(draw, cx, y0 + 286, nfc(cfg["sub"]), fonts["bar_lbl"], dim_color(INK_MUTED, max(0.45, fu)))

        # 4. Hai thanh chi tiết bên trong thẻ
        for ti, tkey in enumerate(("tag1", "tag2")):
            ty0 = y0 + 336 + ti * 60
            ty1 = ty0 + 44
            tbox = (x0 + 40, ty0, x1 - 40, ty1)
            t_fill = PAPER_CARD if is_bright else dim_color(PAPER_FLOOR, 0.6)
            t_bd = dim_color(acc, 0.45 if is_bright else 0.22)
            draw.rounded_rectangle(tbox, radius=12, fill=t_fill, outline=t_bd, width=2)
            draw_centered_text(draw, cx, ty0 + 9, nfc(cfg[tkey]), fonts["hud_sub"], dim_color(INK, max(0.42, fu)))

    # Cầu nối giữa hai thẻ tại đúng x=960
    by = 633
    draw_flow_segment(draw, (894, by), (1026, by), sc["flow"], t_local)
    br_txt = nfc(ad["bridge"])
    br_w = max(76, draw.textlength(br_txt, font=fonts["hud_title"]) + 28)
    draw.rounded_rectangle((960 - br_w / 2.0, by - 19, 960 + br_w / 2.0, by + 25), radius=16, fill=(214, 206, 190))
    draw.rounded_rectangle((960 - br_w / 2.0, by - 22, 960 + br_w / 2.0, by + 22), radius=16, fill=INK, outline=PAPER_CARD, width=3)
    draw_centered_text(draw, 960, by - 13, br_txt, fonts["hud_title"], PAPER_CARD)


def draw_long_gauge_and_lock(
    draw: ImageDraw.ImageDraw,
    sc: dict[str, Any],
    beat4_idx: int,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Khuôn hình 2: Thanh khoá/đối chiếu khổng lồ tầng trên + 2 thẻ trạng thái đối xứng tầng dưới."""
    ad = sc["arch_data"]
    mode = ad["mode"]
    if mode == "LOCK":
        seq = [(1.0, 0.35, 0.35), (0.90, 1.0, 0.35), (0.72, 0.35, 1.0), (1.0, 0.90, 1.0)]
    else:
        seq = [(1.0, 0.40, 0.40), (0.85, 1.0, 0.35), (0.85, 0.35, 1.0), (0.90, 0.55, 1.0)]
    f_top, f_l, f_r = seq[min(3, beat4_idx)]

    tbox = (124, 388, 1796, 616)
    draw_crafted_card(draw, tbox, radius=20, fill=PAPER_FLOOR, outline=INK if f_top >= 0.8 else dim_color(INK, 0.4), width=3, is_active=True, accent=None)
    draw_centered_text(draw, 960, 408, nfc(ad["gauge_title"]), fonts["hud_title"], INK)

    bx0, bx1 = 176, 1744
    by0, by1 = 460, 554
    bw = bx1 - bx0
    anim_u = ease_out_cubic(min(1.0, max(0.12, t_local / 1.2)))
    ratio = ad["ratio"]
    cur_ratio = lerp(0.18, ratio, anim_u) if mode == "LOCK" else lerp(0.28, ratio, anim_u)
    split_x = int(bx0 + bw * ratio)
    fill_split_x = int(bx0 + bw * cur_ratio)

    c_left = AMBER if mode == "LOCK" else NAVY
    c_right = PAPER_SOFT if mode == "LOCK" else TEAL
    # Máng thanh đo UI bao ngoài
    draw.rounded_rectangle((bx0 - 8, by0 - 8, bx1 + 8, by1 + 8), radius=20, fill=PAPER_CARD, outline=PAPER_SOFT, width=2)
    draw.rounded_rectangle((bx0, by0, max(bx0 + 60, fill_split_x - 8), by1), radius=16, fill=c_left, outline=INK, width=3)
    draw.rounded_rectangle((split_x + 8, by0, bx1, by1), radius=16, fill=c_right, outline=INK, width=3)

    if anim_u > 0.55:
        draw_centered_text(draw, (bx0 + split_x - 8) / 2.0, by0 + 32, nfc(ad["locked_lbl"]), fonts["bar_lbl"], PAPER_CARD)
    r_txt_col = INK if mode == "LOCK" else PAPER_CARD
    draw_centered_text(draw, (split_x + 8 + bx1) / 2.0, by0 + 32, nfc(ad["free_lbl"]), fonts["bar_lbl"], r_txt_col)

    # Huy hiệu ổ khoá hoặc đồng hồ tại giao điểm
    badge_cy = (by0 + by1) / 2.0
    draw.ellipse((split_x - 27, badge_cy - 24, split_x + 27, badge_cy + 30), fill=(214, 206, 190))
    draw.ellipse((split_x - 27, badge_cy - 27, split_x + 27, badge_cy + 27), fill=PAPER_CARD, outline=INK, width=3)
    draw.ellipse((split_x - 22, badge_cy - 22, split_x + 22, badge_cy + 22), outline=PAPER_SOFT, width=1)
    draw_prop_badge(draw, split_x, badge_cy + (3 if mode == "LOCK" else 0), "lock" if mode == "LOCK" else "clock", t_local, fonts["slice_lbl"], show_label=False)

    sub_hint = nfc(
        ad.get("sub_hint")
        or ("100% HẠN MỨC THẺ TÍN DỤNG CỦA BẠN" if mode == "LOCK" else "QUY TRÌNH XỬ LÝ TỪ LÚC QUẸT THẺ ĐẾN SAO KÊ")
    )
    draw_centered_text(draw, 960, 576, sub_hint, fonts["actor_sub"], INK_MUTED)

    bottom_cards = [
        ((124, 636, 944, 878), ad["card_left"], f_l),
        ((976, 636, 1796, 878), ad["card_right"], f_r),
    ]
    for box, (kicker, big_st, desc, acc), fu in bottom_cards:
        x0, y0, x1, y1 = box
        cx = (x0 + x1) / 2.0
        is_hi = fu >= 0.85
        fill_c = PAPER_CARD if is_hi else dim_color(PAPER_FLOOR, 0.75)
        bd_c = acc if is_hi else dim_color(INK, 0.35)
        draw_crafted_card(draw, box, radius=20, fill=fill_c, outline=bd_c, width=4 if is_hi else 2, is_active=is_hi, accent=acc)

        kw = draw.textlength(nfc(kicker), font=fonts["card_kicker"]) + 32
        draw.rounded_rectangle((cx - kw / 2.0, y0 + 20, cx + kw / 2.0, y0 + 52), radius=16, fill=blend_rgb(PAPER_CARD, acc, 0.2 if is_hi else 0.08), outline=dim_color(acc, fu), width=2)
        draw_centered_text(draw, cx, y0 + 26, nfc(kicker), fonts["card_kicker"], dim_color(INK, max(0.45, fu)))
        draw_centered_text(draw, cx, y0 + 82, nfc(big_st), fonts["card_title"], dim_color(acc, max(0.38, fu)))
        draw_centered_text(draw, cx, y0 + 156, nfc(desc), fonts["bar_lbl"], dim_color(INK, max(0.42, fu)))


def draw_long_ledger_board(
    draw: ImageDraw.ImageDraw,
    sc: dict[str, Any],
    beat4_idx: int,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Khuôn hình 4: Trục thời gian 3 ngày + Bảng cân đối Chữ T Kế Toán chuẩn TT 99/2025."""
    ad = sc["arch_data"]
    days = ad["days"]
    act_day = ad["active_day"]

    # 1. Trục thời gian 3 mốc (y=390..458) đối xứng qua x=960
    day_boxes = [(148, 390, 588, 458), (740, 390, 1180, 458), (1332, 390, 1772, 458)]
    for di in range(2):
        ax0, ax1 = day_boxes[di][2] + 12, day_boxes[di + 1][0] - 12
        ay = 424
        draw.line([(ax0, ay), (ax1 - 10, ay)], fill=AMBER if di < act_day else PAPER_SOFT, width=4)
        draw.ellipse((ax0 - 4, ay - 4, ax0 + 4, ay + 4), fill=PAPER_CARD, outline=AMBER if di < act_day else PAPER_SOFT, width=2)
        draw.polygon([(ax1, ay), (ax1 - 14, ay - 8), (ax1 - 14, ay + 8)], fill=AMBER if di < act_day else PAPER_SOFT)

    for di, ((dlbl, dsub), dbox) in enumerate(zip(days, day_boxes)):
        is_cur = di == act_day
        is_past = di < act_day
        dcx = (dbox[0] + dbox[2]) / 2.0
        fill_d = AMBER_LIGHT if (is_cur and act_day == 0) else (GREEN_LIGHT if is_cur else (PAPER_CARD if is_past else PAPER_FLOOR))
        bd_d = INK if is_cur else dim_color(INK, 0.35)
        if is_cur:
            draw.rounded_rectangle((dbox[0], dbox[1] + 4, dbox[2], dbox[3] + 4), radius=16, fill=(224, 216, 200))
        draw_crafted_card(draw, dbox, radius=16, fill=fill_d, outline=bd_d, width=3 if is_cur else 2, is_active=False, inner_glow=is_cur)
        draw_centered_text(draw, dcx, dbox[1] + 9, nfc(dlbl), fonts["hud_title"], INK if is_cur else dim_color(INK_MUTED, 0.6))
        draw_centered_text(draw, dcx, dbox[1] + 38, nfc(dsub), fonts["actor_sub"], INK if is_cur else dim_color(INK_MUTED, 0.55))

    # 2. Bảng Sổ Cái Chữ T (y=476..878)
    board = (124, 476, 1796, 878)
    draw_crafted_card(draw, board, radius=20, fill=PAPER_FLOOR, outline=INK, width=3, is_active=True, accent=None)

    draw.line([(144, 544), (1776, 544)], fill=INK, width=3)
    draw.line([(960, 490), (960, 804)], fill=INK, width=3)

    fu_debit = 1.0 if beat4_idx >= 1 else 0.55
    fu_credit = 1.0 if beat4_idx >= 2 else 0.35

    draw.rounded_rectangle((144, 490, 944, 536), radius=12, fill=blend_rgb(PAPER_CARD, AMBER_LIGHT, 0.9 if fu_debit >= 0.8 else 0.35))
    draw_centered_text(draw, 544, 501, nfc(ad["debit_title"]), fonts["hud_title"], INK if fu_debit >= 0.8 else INK_MUTED)

    draw.rounded_rectangle((976, 490, 1776, 536), radius=12, fill=blend_rgb(PAPER_CARD, GREEN_LIGHT, 0.9 if fu_credit >= 0.8 else 0.35))
    draw_centered_text(draw, 1376, 501, nfc(ad["credit_title"]), fonts["hud_title"], INK if fu_credit >= 0.8 else INK_MUTED)

    def _draw_t_rows(rows: list[tuple], col_x0: int, col_x1: int, fu: float) -> None:
        is_hi = fu >= 0.85
        n_r = len(rows)
        if n_r == 1:
            code, amt, note, acc = rows[0]
            rbox = (col_x0 + 18, 570, col_x1 - 18, 782)
            rcx = (rbox[0] + rbox[2]) / 2.0
            draw_crafted_card(draw, rbox, radius=16, fill=PAPER_CARD if is_hi else dim_color(PAPER_CARD, 0.55), outline=acc if is_hi else dim_color(INK, 0.3), width=3 if is_hi else 2, is_active=is_hi, accent=acc)
            draw_centered_text(draw, rcx, 594, nfc(code), fonts["bar_lbl"], dim_color(INK, max(0.45, fu)))
            draw_centered_text(draw, rcx, 646, nfc(amt), fonts["focal_big"], dim_color(acc, max(0.38, fu)))
            draw_centered_text(draw, rcx, 728, nfc(note), fonts["hud_sub"], dim_color(INK_MUTED, max(0.45, fu)))
        else:
            for ri, (code, amt, note, acc) in enumerate(rows[:2]):
                ry0 = 560 + ri * 122
                ry1 = ry0 + 108
                rbox = (col_x0 + 18, ry0, col_x1 - 18, ry1)
                draw_crafted_card(draw, rbox, radius=16, fill=PAPER_CARD if is_hi else dim_color(PAPER_CARD, 0.55), outline=acc if is_hi else dim_color(INK, 0.3), width=3 if is_hi else 2, is_active=False, inner_glow=is_hi)
                draw.text((rbox[0] + 24, ry0 + 18), nfc(code), font=fonts["bar_lbl"], fill=dim_color(INK, max(0.45, fu)))
                amt_w = draw.textlength(nfc(amt), font=fonts["ledger_amt"])
                draw.text((rbox[2] - 24 - amt_w, ry0 + 13), nfc(amt), font=fonts["ledger_amt"], fill=dim_color(acc, max(0.38, fu)))
                draw.text((rbox[0] + 24, ry0 + 62), nfc(note), font=fonts["actor_sub"], fill=dim_color(INK_MUTED, max(0.45, fu)))

    _draw_t_rows(ad["debit_rows"], 144, 944, fu_debit)
    _draw_t_rows(ad["credit_rows"], 976, 1776, fu_credit)

    bal_hi = beat4_idx >= 3
    bal_txt = nfc(ad["balance_lbl"])
    bw = min(900, draw.textlength(bal_txt, font=fonts["hud_val"]) + 56)
    draw_crafted_card(draw, (960 - bw / 2.0, 816, 960 + bw / 2.0, 862), radius=16, fill=GREEN_LIGHT if bal_hi else PAPER_CARD, outline=GREEN if bal_hi else PAPER_SOFT, width=3 if bal_hi else 2, is_active=False, inner_glow=bal_hi)
    draw_centered_text(draw, 960, 825, bal_txt, fonts["hud_val"], GREEN if bal_hi else INK_MUTED)


def draw_long_waterfall_split(
    draw: ImageDraw.ImageDraw,
    sc: dict[str, Any],
    beat4_idx: int,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Khuôn hình 5A: Thác phân rã từ thanh tổng có máng đỡ xuống 3 bể định chế đối xứng."""
    ad = sc["arch_data"]
    bx0, bx1 = 152, 1768
    by0, by1 = 388, 474
    bw = bx1 - bx0
    anim_u = ease_out_cubic(min(1.0, max(0.15, t_local / 1.1)))
    ratio = ad["top_ratio"]
    split_x = int(bx0 + bw * ratio)
    fill_x = int(bx0 + bw * lerp(0.5, ratio, anim_u))

    tl_lbl, tl_amt, tl_col = ad["top_left"]
    tr_lbl, tr_amt, tr_col = ad["top_right"]

    draw.rounded_rectangle((bx0 - 7, by0 - 7, bx1 + 7, by1 + 7), radius=20, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=2)
    draw.rounded_rectangle((bx0, by0, max(bx0 + 80, fill_x - 6), by1), radius=16, fill=tl_col, outline=INK, width=3)
    draw.rounded_rectangle((split_x + 6, by0, bx1, by1), radius=16, fill=tr_col, outline=INK, width=3)
    if anim_u > 0.55:
        draw_centered_text(draw, (bx0 + split_x - 6) / 2.0, by0 + 13, nfc(tl_lbl), fonts["slice_lbl"], PAPER_CARD)
        draw_centered_text(draw, (bx0 + split_x - 6) / 2.0, by0 + 40, nfc(tl_amt), fonts["ledger_amt"], PAPER_CARD)
    draw_centered_text(draw, (split_x + 6 + bx1) / 2.0, by0 + 13, nfc(tr_lbl), fonts["slice_lbl"], PAPER_CARD)
    draw_centered_text(draw, (split_x + 6 + bx1) / 2.0, by0 + 40, nfc(tr_amt), fonts["ledger_amt"], PAPER_CARD)

    # Nhánh thác dẫn xuống 3 bể đối xứng (x=394, 960, 1526) kèm khớp nối kỹ thuật
    bucket_boxes = [(136, 536, 652, 878), (702, 536, 1218, 878), (1268, 536, 1784, 878)]
    top_hub_x = 960 if ad["top_right"][0].startswith("Tổng phí") else (split_x + 6 + bx1) / 2.0
    joints: list[tuple[float, tuple[int, int, int]]] = []
    for bi, b in enumerate(bucket_boxes):
        bcx = (b[0] + b[2]) / 2.0
        col = ad["buckets"][bi]["color"]
        is_focus = (beat4_idx == 0) or (beat4_idx == bi + 1)
        l_col = col if is_focus else dim_color(col, 0.35)
        draw.line([(top_hub_x, by1 + 2), (top_hub_x, 504), (bcx, 504), (bcx, 532)], fill=l_col, width=4)
        draw.polygon([(bcx, 534), (bcx - 8, 520), (bcx + 8, 520)], fill=l_col)
        joints.append((bcx, l_col))

        if is_focus and beat4_idx > 0:
            u = (t_local * 0.65) % 1.0
            px = lerp(top_hub_x, bcx, smoothstep(0.0, 0.7, u))
            py = 504 if 0.2 <= u <= 0.8 else (lerp(by1 + 2, 504, u / 0.2) if u < 0.2 else lerp(504, 530, (u - 0.8) / 0.2))
            draw.ellipse((px - 7, py - 7, px + 7, py + 7), fill=GOLD, outline=INK, width=2)

    for jx, jcol in joints:
        draw.ellipse((jx - 5, 499, jx + 5, 509), fill=PAPER_CARD, outline=jcol, width=2)
    draw.ellipse((top_hub_x - 6, 498, top_hub_x + 6, 510), fill=PAPER_CARD, outline=INK, width=2)

    for bi, (bk, box) in enumerate(zip(ad["buckets"], bucket_boxes)):
        x0, y0, x1, y1 = box
        cx = (x0 + x1) / 2.0
        acc = bk["color"]
        fu = 0.72 if beat4_idx == 0 else (1.0 if beat4_idx == bi + 1 else 0.32)
        is_hi = fu >= 0.85
        draw_crafted_card(draw, box, radius=20, fill=PAPER_CARD if fu >= 0.6 else dim_color(PAPER_FLOOR, 0.7), outline=acc if is_hi else dim_color(INK, 0.35), width=4 if is_hi else 2, is_active=is_hi, accent=None)

        draw.rounded_rectangle((x0 + 12, y0 + 12, x1 - 12, y0 + 62), radius=14, fill=dim_color(acc, fu))
        draw_centered_text(draw, cx, y0 + 24, nfc(bk["title"]), fonts["hud_title"], PAPER_CARD)

        draw_centered_text(draw, cx, y0 + 96, nfc(bk["sub"]), fonts["bar_lbl"], dim_color(INK_MUTED, max(0.45, fu)))
        draw_centered_text(draw, cx, y0 + 150, nfc(bk["amt"]), fonts["focal_big"], dim_color(acc, max(0.38, fu)))
        draw.line([(x0 + 36, y0 + 236), (x1 - 36, y0 + 236)], fill=PAPER_SOFT, width=2)

        nbox = (x0 + 20, y0 + 258, x1 - 20, y1 - 20)
        draw.rounded_rectangle(nbox, radius=14, fill=PAPER_FLOOR if fu >= 0.6 else PAPER_CARD, outline=dim_color(acc, 0.35 if is_hi else 0.18), width=2)
        draw_centered_text(draw, cx, y0 + 278, nfc(bk["note"]), fonts["hud_sub"], dim_color(INK, max(0.42, fu)))


def draw_long_full_triptych(
    draw: ImageDraw.ImageDraw,
    sc: dict[str, Any],
    beat4_idx: int,
    fonts: dict[str, ImageFont.FreeTypeFont],
) -> None:
    """Khuôn hình 5B: 3 cột đứng đối xứng cỡ đại (1. Reversal | 2. Refund | 3. Chargeback)."""
    ad = sc["arch_data"]
    cols_boxes = [(136, 388, 652, 878), (702, 388, 1218, 878), (1268, 388, 1784, 878)]
    for ci, (card, box) in enumerate(zip(ad["cards"], cols_boxes)):
        x0, y0, x1, y1 = box
        cx = (x0 + x1) / 2.0
        acc = card["color"]
        fu = 0.78 if beat4_idx == 0 else (1.0 if beat4_idx == ci + 1 else 0.32)
        is_hi = fu >= 0.85

        draw_crafted_card(draw, box, radius=22, fill=PAPER_CARD if fu >= 0.6 else dim_color(PAPER_FLOOR, 0.75), outline=acc if is_hi else dim_color(INK, 0.35), width=4 if is_hi else 2, is_active=is_hi, accent=acc)

        kw = draw.textlength(nfc(card["num"]), font=fonts["card_kicker"]) + 32
        draw.rounded_rectangle((cx - kw / 2.0, y0 + 22, cx + kw / 2.0, y0 + 56), radius=16, fill=dim_color(acc, fu))
        draw_centered_text(draw, cx, y0 + 28, nfc(card["num"]), fonts["card_kicker"], PAPER_CARD)

        draw_centered_text(draw, cx, y0 + 78, nfc(card["title"]), fonts["card_title"], dim_color(acc, max(0.4, fu)))
        draw_centered_text(draw, cx, y0 + 128, nfc(card["sub"]), fonts["bar_lbl"], dim_color(INK_MUTED, max(0.45, fu)))

        rows = [
            ("KHI NÀO?", card["when"], PAPER_FLOOR, INK),
            ("CƠ CHẾ?", card["flow"], PAPER_FLOOR, INK),
            ("TIỀN THẬT", card["impact"], blend_rgb(PAPER_CARD, acc, 0.16 if fu >= 0.6 else 0.06), acc),
        ]
        for ri, (rk, rv, rbg, rtxt_col) in enumerate(rows):
            ry0 = y0 + 178 + ri * 98
            ry1 = ry0 + 84
            draw.rounded_rectangle((x0 + 24, ry0, x1 - 24, ry1), radius=14, fill=rbg, outline=dim_color(acc if ri == 2 else PAPER_SOFT, max(0.4, fu)), width=2)
            draw_centered_text(draw, cx, ry0 + 12, rk, fonts["actor_sub"], dim_color(INK_MUTED, max(0.48, fu)))
            draw_centered_text(draw, cx, ry0 + 42, nfc(rv), fonts["hud_sub"], dim_color(rtxt_col, max(0.45, fu)))


def draw_hook_stage(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    sprites: SpriteBank,
    sc: dict[str, Any],
    beat2_u: float,
    beat4_idx: int,
    t_local: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
    is_short: bool,
) -> None:
    """
    Khuôn hình MỞ ĐẦU (HOOK_STAGE — Scene 0):
    Chỉ làm nhiệm vụ câu dẫn đặt vấn đề (0 ô BƯỚC 1..5, 0 bộ đếm bước) để người xem
    nắm gọn nghịch lý trước khi bước sang màn BƯỚC 1/5 (hoặc BƯỚC 1/10).
    """
    hd = sc["hook_data"]

    if is_short:
        # 1. HAI THẺ NGHỊCH LÝ ĐỐI XỨNG QUA X=540 (y=706..1056)
        cards = [
            ((104, 706, 514, 1056), "left", 1.0 - 0.12 * beat2_u),
            ((566, 706, 976, 1056), "right", 0.52 + 0.48 * beat2_u),
        ]
        for (x0, y0, x1, y1), side, fu in cards:
            cx = (x0 + x1) / 2.0
            acc = hd[f"{side}_accent"]
            is_bright = fu >= 0.68
            bg_c = blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.35) if is_bright else blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.12)
            bd_c = acc if is_bright else dim_color(INK, 0.38)
            draw_crafted_card(draw, (x0, y0, x1, y1), radius=22, fill=bg_c, outline=bd_c, width=4 if is_bright else 2, is_active=is_bright, accent=acc)

            k_txt = nfc(hd[f"{side}_title"])
            kw = draw.textlength(k_txt, font=fonts["card_kicker"]) + 28
            draw.rounded_rectangle((cx - kw / 2.0, y0 + 20, cx + kw / 2.0, y0 + 50), radius=15, fill=blend_rgb(PAPER_CARD, acc, 0.18), outline=acc, width=2)
            _draw_centered_bbox_text(draw, cx, y0 + 35, k_txt, fonts["card_kicker"], INK)

            aid = hd[f"{side}_actor"]
            breath = 1.0 + 0.025 * math.sin(2.0 * math.pi * 0.72 * t_local) if is_bright else 1.0
            sp = sprites.get_scaled(aid, focused=True, scale=0.78 * breath)
            scy = y0 + 132
            r_h = int(sp.width * 0.56)
            draw.ellipse((cx - r_h, scy - r_h, cx + r_h, scy + r_h), fill=blend_rgb(PAPER_CARD, acc, 0.18), outline=dim_color(acc, 0.45), width=2)
            canvas.paste(sp, (int(round(cx - sp.width / 2.0)), int(round(scy - sp.height / 2.0))), sp)

            amt_txt = nfc(hd[f"{side}_amt"])
            f_amt = fonts["focal_big"]
            if draw.textlength(amt_txt, font=f_amt) > (x1 - x0 - 32):
                f_amt = fonts["ledger_amt"]
            draw_centered_text(draw, cx, y0 + 224, amt_txt, f_amt, acc)
            draw_centered_text(draw, cx, y0 + 292, nfc(hd[f"{side}_sub"]), fonts["bar_lbl"], INK_MUTED)

        # Huy hiệu dấu hỏi (?) đối xứng tại đúng (540, 881)
        by = 881
        draw.line([(514, by), (566, by)], fill=AMBER, width=5)
        draw.ellipse((540 - 26, by - 23, 540 + 26, by + 29), fill=(214, 206, 190))
        draw.ellipse((540 - 26, by - 26, 540 + 26, by + 26), fill=INK, outline=PAPER_CARD, width=3)
        _draw_centered_bbox_text(draw, 540, by, "?", fonts["card_title"], GOLD)

        # 2. THẺ NGHỊCH LÝ MỞ ĐẦU (KHÔNG VẼ LỘ TRÌNH BƯỚC Ở MÀN HOOK) (y=1088..1412)
        q_box = (104, 1088, 976, 1412)
        draw_crafted_card(draw, q_box, radius=22, fill=PAPER_FLOOR, outline=AMBER, width=3, is_active=True, accent=AMBER)

        hk_txt = nfc(hd["hook_kicker"])
        hkw = draw.textlength(hk_txt, font=fonts["card_kicker"]) + 32
        draw.rounded_rectangle((540 - hkw / 2.0, 1112, 540 + hkw / 2.0, 1146), radius=16, fill=AMBER_LIGHT, outline=AMBER, width=2)
        _draw_centered_bbox_text(draw, 540, 1129, hk_txt, fonts["card_kicker"], INK)

        l1_txt = nfc(hd["hook_line1"])
        f_l1 = fonts["card_title"] if draw.textlength(l1_txt, font=fonts["card_title"]) <= 824 else fonts["hud_val"]
        _draw_centered_bbox_text(draw, 540, 1188, l1_txt, f_l1, INK)

        l2_txt = nfc(hd["hook_line2"])
        f_l2 = fonts["card_title"] if draw.textlength(l2_txt, font=fonts["card_title"]) <= 824 else fonts["hud_val"]
        _draw_centered_bbox_text(draw, 540, 1244, l2_txt, f_l2, CORAL)

        draw.line([(184, 1296), (896, 1296)], fill=PAPER_SOFT, width=2)

        hs_txt = nfc(hd["hook_sub"])
        f_hs = fonts["hud_sub"] if draw.textlength(hs_txt, font=fonts["hud_sub"]) <= 824 else fonts["actor_sub"]
        _draw_centered_bbox_text(draw, 540, 1348, hs_txt, f_hs, NAVY)

        draw_takeaway_pill(draw, 540, 1438, 840, sc["focal"]["pill"], fonts["focal_pill"])
        return

    # VIDEO DÀI 16:9 HOOK_STAGE (Bố cục dẫn nhập thuần túy — 0 vẽ khay lộ trình 10 bước ở màn mở đầu)
    focus_seq = [(1.0, 0.35), (1.0, 0.35), (0.38, 1.0), (1.0, 1.0)]
    f_left, f_right = focus_seq[min(3, beat4_idx)]
    cards = [
        ((124, 388, 892, 712), "left", f_left, 0),
        ((1028, 388, 1796, 712), "right", f_right, 1),
    ]
    for (x0, y0, x1, y1), side, fu, idx in cards:
        cx = (x0 + x1) / 2.0
        acc = hd[f"{side}_accent"]
        is_bright = fu >= 0.7
        bg_c = blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.45) if is_bright else blend_rgb(PAPER_CARD, PAPER_FLOOR, 0.15)
        bd_c = acc if is_bright else dim_color(INK, 0.32)
        draw_crafted_card(draw, (x0, y0, x1, y1), radius=22, fill=bg_c, outline=bd_c, width=4 if is_bright else 2, is_active=is_bright, accent=acc)

        k_txt = nfc(hd[f"{side}_title"])
        kw = draw.textlength(k_txt, font=fonts["card_kicker"]) + 32
        draw.rounded_rectangle((cx - kw / 2.0, y0 + 18, cx + kw / 2.0, y0 + 50), radius=16, fill=blend_rgb(PAPER_CARD, acc, 0.18 if is_bright else 0.08), outline=dim_color(acc, fu), width=2)
        _draw_centered_bbox_text(draw, cx, y0 + 34, k_txt, fonts["card_kicker"], dim_color(INK, max(0.45, fu)))

        aid = hd[f"{side}_actor"]
        breath = 1.0 + 0.03 * math.sin(2.0 * math.pi * 0.72 * t_local + idx) if is_bright else 1.0
        sp = sprites.get_scaled(aid, focused=is_bright, scale=0.78 * breath)
        scy = y0 + 126
        if is_bright:
            r_h = int(sp.width * 0.56)
            draw.ellipse((cx - r_h, scy - r_h, cx + r_h, scy + r_h), fill=blend_rgb(PAPER_CARD, acc, 0.20), outline=dim_color(acc, 0.42), width=2)
        canvas.paste(sp, (int(round(cx - sp.width / 2.0)), int(round(scy - sp.height / 2.0))), sp)

        draw_centered_text(draw, cx, y0 + 204, nfc(hd[f"{side}_amt"]), fonts["focal_big"], dim_color(acc, max(0.38, fu)))
        draw_centered_text(draw, cx, y0 + 268, nfc(hd[f"{side}_sub"]), fonts["bar_lbl"], dim_color(INK_MUTED, max(0.45, fu)))

    # Cầu nối giữa hai thẻ tại đúng x=960, y=550
    by = 550
    draw_flow_segment(draw, (894, by), (1026, by), sc["flow"], t_local)
    br_txt = "NHƯNG"
    br_w = max(84, draw.textlength(br_txt, font=fonts["hud_title"]) + 28)
    draw.rounded_rectangle((960 - br_w / 2.0, by - 19, 960 + br_w / 2.0, by + 25), radius=16, fill=(214, 206, 190))
    draw.rounded_rectangle((960 - br_w / 2.0, by - 22, 960 + br_w / 2.0, by + 22), radius=16, fill=INK, outline=PAPER_CARD, width=3)
    _draw_centered_bbox_text(draw, 960, by, br_txt, fonts["hud_title"], PAPER_CARD)

    # Băng nghịch lý mở đầu (y=736..878)
    draw_crafted_card(draw, (124, 736, 1796, 878), radius=20, fill=PAPER_FLOOR, outline=AMBER, width=3, is_active=True, accent=AMBER)
    hl1 = nfc(hd["hook_line1"])
    f_hl1 = fonts["hud_val"] if draw.textlength(hl1, font=fonts["hud_val"]) <= 1600 else fonts["hud_title"]
    _draw_centered_bbox_text(draw, 960, 774, hl1, f_hl1, INK)
    hs_l = nfc(hd["hook_sub"])
    f_hsl = fonts["hud_sub"] if draw.textlength(hs_l, font=fonts["hud_sub"]) <= 1600 else fonts["actor_sub"]
    _draw_centered_bbox_text(draw, 960, 832, hs_l, f_hsl, NAVY)


def render_v51_frame(
    layout: dict[str, Any],
    parchment_bg: Image.Image,
    sprites: SpriteBank,
    scenes_cfg: list[dict[str, Any]],
    scene_meta: list[dict],
    s_idx: int,
    t: float,
    fonts: dict[str, ImageFont.FreeTypeFont],
    is_short: bool,
) -> Image.Image:
    sm = scene_meta[s_idx]
    sc = scenes_cfg[min(s_idx, len(scenes_cfg) - 1)]
    s_dur = max(0.01, sm["win_t1"] - sm["win_t0"])
    s_prog = max(0.0, min(1.0, (t - sm["win_t0"]) / s_dur))
    t_local = max(0.0, t - sm["win_t0"])

    phrases = sm["phrases"]
    b2_start = phrases[len(phrases) // 2]["t0"] if len(phrases) >= 2 else (sm["win_t0"] + s_dur * 0.45)
    beat2_u = smoothstep(b2_start - 0.15, b2_start + 0.35, t)

    phrase_idx = 0
    for pi, ph in enumerate(phrases):
        if t >= ph["t0"]:
            phrase_idx = pi

    canvas = parchment_bg.copy()
    draw = ImageDraw.Draw(canvas)

    draw_hud(draw, layout["HUD_BOX"], sc, s_idx, len(scenes_cfg), s_prog, t_local, fonts, is_short)

    # Mặt phẳng Sân khấu Zone 2 duy nhất — lề trong đối xứng hoàn hảo trái=phải, bóng đổ dọc 0px lệch ngang
    stx0, sty0, stx1, sty1 = layout["STAGE_BOX"]
    st_cx = (stx0 + stx1) / 2.0
    st_pad = 24 if is_short else 28
    draw_crafted_card(draw, layout["STAGE_BOX"], radius=28, fill=PAPER_CARD, outline=INK, width=4, is_active=True, accent=None)

    # TẦNG 1 TRONG SÂN KHẤU: 1 Headline ngắn & bự (<= 6 từ)
    band_top = sty0 + st_pad
    band_bot = sty0 + (150 if is_short else 144)
    draw.rounded_rectangle((stx0 + st_pad, band_top, stx1 - st_pad, band_bot), radius=20, fill=PAPER_FLOOR, outline=PAPER_SOFT, width=1)

    flow_cfg = sc["flow"]
    kind = flow_cfg["kind"]
    f_col = GREEN if kind == "pipe" else (TERRACOTTA if kind == "loop" else AMBER)
    f_bg = GREEN_LIGHT if kind == "pipe" else (CORAL_LIGHT if kind == "loop" else AMBER_LIGHT)
    flow_lbl = nfc(flow_cfg["label"])
    fl_w = draw.textlength(flow_lbl, font=fonts["flow_lbl"]) + 32
    fl_y = band_top + (12 if is_short else 10)
    fl_bd = INK if s_idx >= 1 else f_col
    draw.rounded_rectangle((st_cx - fl_w / 2.0, fl_y, st_cx + fl_w / 2.0, fl_y + 32), radius=16, fill=f_bg, outline=fl_bd, width=2)
    draw_centered_text(draw, st_cx, fl_y + 5, flow_lbl, fonts["flow_lbl"], INK)

    if not is_short and "phrase_beats" in sc:
        # Video Dài 16:9 dùng 4 nhịp bồi đồng bộ từng câu nói (đổi mỗi ~9–11s)
        n_ph = max(1, len(phrases))
        beat4_idx = min(3, int((phrase_idx * 4) / n_ph)) if n_ph >= 4 else min(3, int(s_prog * 4.0))
        bh_text, bh_hi, bh_col = sc["phrase_beats"][beat4_idx]
        hl_font = fonts["headline"]
        if draw.textlength(nfc(bh_text), font=hl_font) > (stx1 - stx0 - 2 * st_pad - 24):
            hl_font = fonts["headline_sm"]
        draw_highlighted_headline(draw, st_cx, band_top + 48, bh_text, bh_hi, bh_col, hl_font)

        # 4 thanh nhịp micro căn ĐÚNG TÂM x=960
        dot_w, dot_gap = 28, 10
        tot_dw = 4 * dot_w + 3 * dot_gap
        dx0 = st_cx - tot_dw / 2.0
        dy0 = band_bot - 14
        for di in range(4):
            px0 = dx0 + di * (dot_w + dot_gap)
            d_fill = bh_col if di == beat4_idx else (GREEN if di < beat4_idx else PAPER_SOFT)
            draw.rounded_rectangle((px0, dy0, px0 + dot_w, dy0 + 6), radius=3, fill=d_fill)

        # TẦNG 2+3 VIDEO DÀI 16:9: Điều phối qua HOOK_STAGE (Mở đầu) + 6 Khuôn Hình Đạo Diễn
        archetype = sc["archetype"]
        if archetype == "HOOK_STAGE":
            draw_hook_stage(canvas, draw, sprites, sc, beat2_u, beat4_idx, t_local, fonts, is_short=False)
        elif archetype == "TWIN_SHOWDOWN":
            draw_long_twin_showdown(canvas, draw, sprites, sc, beat4_idx, t_local, fonts)
        elif archetype == "GAUGE_AND_LOCK":
            draw_long_gauge_and_lock(draw, sc, beat4_idx, t_local, fonts)
        elif archetype == "LEDGER_BOARD":
            draw_long_ledger_board(draw, sc, beat4_idx, t_local, fonts)
        elif archetype == "WATERFALL_SPLIT":
            draw_long_waterfall_split(draw, sc, beat4_idx, t_local, fonts)
        elif archetype == "FULL_TRIPTYCH_3":
            draw_long_full_triptych(draw, sc, beat4_idx, fonts)
        else:
            # RELAY_PIPELINE: dây chuyền 3-4 định chế chạy spotlight 4 nhịp + tầng dưới 3 hộp
            actors = sc["actors"]
            n_act = len(actors)
            actor_y = sty0 + 278
            margin_x = 340 if n_act <= 2 else (240 if n_act == 3 else 190)
            span_x = (stx1 - margin_x) - (stx0 + margin_x)
            centers = [(stx0 + margin_x + (span_x * i) / float(n_act - 1), actor_y) for i in range(n_act)]
            offset_r = sprites.size * 0.57
            for i in range(n_act - 1):
                draw_flow_segment(draw, (centers[i][0] + offset_r, actor_y), (centers[i + 1][0] - offset_r, actor_y), flow_cfg, t_local)

            active_a = min(n_act - 1, beat4_idx) if n_act == 4 else min(n_act - 1, max(0, beat4_idx - 1))
            for i, a_cfg in enumerate(actors):
                f_u = 1.0 if (i == active_a or beat4_idx == 3 and i == n_act - 1) else 0.30
                draw_actor_node(canvas, draw, sprites, a_cfg, centers[i][0], centers[i][1], f_u, t_local, i, fonts, compact=False)

            ad = sc.get("arch_data", {})
            if ad.get("sub_mode") == "NETTING_3":
                net_cols = ad["net_cols"]
                gap = 28
                cw = (1672 - gap * 2) / 3.0
                for ci, (ntitle, namt, nsub, ncol) in enumerate(net_cols):
                    cx0 = 124 + ci * (cw + gap)
                    cx1 = cx0 + cw
                    ncx = (cx0 + cx1) / 2.0
                    is_hi = (beat4_idx == ci + 1) or (beat4_idx == 0 and ci == 0)
                    bg_c = blend_rgb(PAPER_CARD, ncol, 0.16) if is_hi else PAPER_FLOOR
                    bd_c = ncol if is_hi else dim_color(INK, 0.35)
                    draw_crafted_card(draw, (cx0, 690, cx1, 876), radius=18, fill=bg_c, outline=bd_c, width=3 if is_hi else 2, is_active=is_hi, accent=ncol)
                    draw_centered_text(draw, ncx, 712, nfc(ntitle), fonts["card_kicker"], INK if is_hi else INK_MUTED)
                    draw_centered_text(draw, ncx, 748, nfc(namt), fonts["ledger_amt"], ncol if is_hi else dim_color(ncol, 0.45))
                    draw_centered_text(draw, ncx, 816, nfc(nsub), fonts["actor_sub"], INK_MUTED)
            else:
                # 3 Cổng kiểm duyệt
                items = sc["focal"]["items"]
                gap = 28
                cw = (1672 - gap * 2) / 3.0
                for ci, item in enumerate(items):
                    cx0 = 124 + ci * (cw + gap)
                    cx1 = cx0 + cw
                    ncx = (cx0 + cx1) / 2.0
                    is_hi = (beat4_idx >= 2) or (t_local >= ci * 3.5)
                    draw_crafted_card(draw, (cx0, 704, cx1, 868), radius=18, fill=GREEN_LIGHT if is_hi else PAPER_FLOOR, outline=GREEN if is_hi else dim_color(INK, 0.35), width=3 if is_hi else 2, is_active=is_hi, accent=GREEN)
                    draw_centered_text(draw, ncx, 738, f"CỔNG 0{ci + 1}", fonts["card_kicker"], GREEN if is_hi else INK_MUTED)
                    draw_centered_text(draw, ncx, 782, nfc(item), fonts["bar_lbl"], INK if is_hi else INK_MUTED)

        # Thẻ tóm tắt đáy cố định tại cùng độ cao cho 100% các cảnh Long
        draw_takeaway_pill(draw, st_cx, sty1 - st_pad - 38, 1620, sc["focal"]["pill"], fonts["focal_pill"])
        return canvas

    # SHORT 9:16: Tách riêng HOOK_STAGE (Cảnh 0 Mở đầu) và Bố cục 3 tầng Step-by-Step (Bước 1..5)
    bh_idx = 1 if beat2_u >= 0.5 else 0
    bh_text, bh_hi, bh_col = sc["beat_headlines"][bh_idx]
    hl_font = fonts["headline"]
    if draw.textlength(nfc(bh_text), font=hl_font) > (stx1 - stx0 - 2 * st_pad - 24):
        hl_font = fonts["headline_sm"]
    draw_highlighted_headline(draw, st_cx, band_top + 58, bh_text, bh_hi, bh_col, hl_font)

    if sc.get("is_hook"):
        draw_hook_stage(canvas, draw, sprites, sc, beat2_u, 0, t_local, fonts, is_short=True)
        return canvas

    actors = sc["actors"]
    n_act = len(actors)
    compact_act = n_act >= 3
    actor_y = sty0 + 372
    margin_x = 160 if n_act >= 3 else 230
    span_x = (stx1 - margin_x) - (stx0 + margin_x)
    centers = [(st_cx if n_act == 1 else (stx0 + margin_x + (span_x * i) / float(n_act - 1)), actor_y) for i in range(n_act)]

    offset_r = sprites.size * 0.57
    for i in range(n_act - 1):
        draw_flow_segment(
            draw,
            (centers[i][0] + offset_r, actor_y),
            (centers[i + 1][0] - offset_r, actor_y),
            flow_cfg,
            t_local,
        )

    if n_act == 2 and flow_cfg.get("prop") in ("clock", "lock"):
        draw_prop_badge(draw, st_cx, actor_y - 54, flow_cfg["prop"], t_local, fonts["actor_sub"])

    for i, a_cfg in enumerate(actors):
        if a_cfg["beat"] == 1:
            f_u = 1.0 - 0.65 * beat2_u
        else:
            f_u = 0.28 + 0.72 * beat2_u
        draw_actor_node(
            canvas,
            draw,
            sprites,
            a_cfg,
            centers[i][0],
            centers[i][1],
            f_u,
            t_local,
            i,
            fonts,
            compact=compact_act,
        )

    floor_top = sty0 + 572
    floor_box = (stx0 + st_pad, floor_top, stx1 - st_pad, sty1 - st_pad)
    draw_focal_floor(draw, floor_box, sc["focal"], beat2_u, t_local, fonts, phrase_idx, True)

    return canvas


# ── AUDIO TIMELINE & KIỂM ĐỊNH TOÁN HỌC / HÌNH HỌC TẤT ĐỊNH ──────────────────

def load_cached_sfx() -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for key in ("sfx_lamp_switch", "sfx_wire_pulse", "sfx_pipe_flow", "sfx_clock_tick", "sfx_scale_chime", "sfx_shutter_close"):
        cf = CACHE_DIR / f"{key}.json"
        if cf.is_file():
            out[key] = base64.b64decode(json.loads(cf.read_text(encoding="utf-8"))["audio_base64"])
    return out


def build_master_audio(
    scenes: list[dict],
    cont_data: dict,
    sfx_map: dict[str, bytes],
    tmp_dir: pathlib.Path,
) -> tuple[pathlib.Path, list[dict], float]:
    raw_mp3 = tmp_dir / "vo_raw.mp3"
    raw_mp3.write_bytes(base64.b64decode(cont_data["audio_base64"]))
    raw_wav = tmp_dir / "vo_raw.wav"
    subprocess.run(["ffmpeg", "-y", "-i", str(raw_mp3), "-ar", "44100", "-ac", "2", str(raw_wav)], check=True, capture_output=True)

    with wave.open(str(raw_wav), "rb") as wf:
        sr = wf.getframerate()
        pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0

    align = cont_data["alignment"]
    starts = [float(x) for x in align["character_start_times_seconds"]]
    ends = [float(x) for x in align["character_end_times_seconds"]]
    scene_texts = [s["vo"].strip() for s in scenes]
    full_text = "\n\n".join(scene_texts)

    raw_bounds: list[tuple[int, int, float, float]] = []
    cursor = 0
    for st in scene_texts:
        pos = full_text.find(st, cursor)
        if pos < 0:
            raise RuntimeError(f"Alignment mismatch near: {st[:40]!r}")
        end_pos = pos + len(st) - 1
        raw_bounds.append((pos, end_pos, starts[pos], ends[min(end_pos, len(ends) - 1)]))
        cursor = end_pos + 1

    EXTRA_PAUSE = 0.36
    LEAD_IN = 0.25
    TAIL_OUT = 0.90

    chunks: list[np.ndarray] = [np.zeros((int(LEAD_IN * sr), 2), dtype=np.float32)]
    scene_meta: list[dict] = []
    cum_shift = LEAD_IN
    prev_end = 0

    for idx, (pos, end_pos, raw_t0, raw_t1) in enumerate(raw_bounds):
        if idx < len(raw_bounds) - 1:
            mid_t = 0.5 * (raw_t1 + raw_bounds[idx + 1][2])
            cut_s = min(len(pcm), int(mid_t * sr))
        else:
            cut_s = len(pcm)

        seg = pcm[prev_end:cut_s].copy()
        fade_n = min(int(0.025 * sr), len(seg) // 4)
        if fade_n > 0:
            ramp = np.linspace(0.0, 1.0, fade_n, dtype=np.float32)[:, None]
            seg[:fade_n] *= ramp
            seg[-fade_n:] *= ramp[::-1]
        chunks.append(seg)

        adj_t0 = raw_t0 + cum_shift
        adj_t1 = raw_t1 + cum_shift
        phrases = split_scene_into_phrases(scene_texts[idx], pos, starts, ends, cum_shift)

        if idx < len(raw_bounds) - 1:
            chunks.append(np.zeros((int(EXTRA_PAUSE * sr), 2), dtype=np.float32))
            win_end = mid_t + cum_shift + EXTRA_PAUSE * 0.5
        else:
            chunks.append(np.zeros((int(TAIL_OUT * sr), 2), dtype=np.float32))
            win_end = adj_t1 + TAIL_OUT

        scene_meta.append(
            {
                "index": idx,
                "scene": scenes[idx],
                "vo_t0": adj_t0,
                "vo_t1": adj_t1,
                "win_t0": 0.0 if idx == 0 else scene_meta[-1]["win_t1"],
                "win_t1": win_end,
                "phrases": phrases,
            }
        )
        cum_shift += EXTRA_PAUSE
        prev_end = cut_s

    vo_full = np.concatenate(chunks, axis=0)
    total_dur = len(vo_full) / sr
    scene_meta[-1]["win_t1"] = total_dur

    t_arr = np.arange(len(vo_full), dtype=np.float32) / sr
    drone = 0.5 * np.sin(2 * math.pi * 110.0 * t_arr) + 0.3 * np.sin(2 * math.pi * 164.81 * t_arr) + 0.2 * np.sin(2 * math.pi * 220.0 * t_arr)
    ambient = (drone * (0.82 + 0.18 * np.sin(2 * math.pi * 0.14 * t_arr)) * 0.012)[:, None] * np.array([[0.95, 1.05]], dtype=np.float32)
    mix = vo_full + ambient

    sfx_keys = list(sfx_map.keys())
    if sfx_keys:
        for idx, sm in enumerate(scene_meta):
            skey = sfx_keys[idx % len(sfx_keys)]
            cue_t = 0.05 if idx == 0 else sm["win_t0"] - 0.30
            s_mp3 = tmp_dir / f"{skey}_{idx}.mp3"
            s_wav = tmp_dir / f"{skey}_{idx}.wav"
            s_mp3.write_bytes(sfx_map[skey])
            subprocess.run(["ffmpeg", "-y", "-i", str(s_mp3), "-ar", str(sr), "-ac", "2", str(s_wav)], check=True, capture_output=True)
            with wave.open(str(s_wav), "rb") as swf:
                spcm = np.frombuffer(swf.readframes(swf.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0
            s0 = max(0, int(cue_t * sr))
            s1 = min(len(mix), s0 + len(spcm))
            if s1 > s0:
                mix[s0:s1] += spcm[: s1 - s0] * 0.075

    mix = np.clip(mix, -0.98, 0.98)
    raw_mix_wav = tmp_dir / "mix_raw.wav"
    with wave.open(str(raw_mix_wav), "wb") as owf:
        owf.setnchannels(2)
        owf.setsampwidth(2)
        owf.setframerate(sr)
        owf.writeframes((mix * 32767.0).astype(np.int16).tobytes())

    norm_wav = tmp_dir / "master_norm.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(raw_mix_wav), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(sr), "-ac", "2", str(norm_wav)],
        check=True,
        capture_output=True,
    )
    return norm_wav, scene_meta, total_dur


def load_fonts(is_short: bool) -> dict[str, ImageFont.FreeTypeFont]:
    return {
        "hud_title": get_font(20 if is_short else 22, "heavy"),
        "hud_lbl": get_font(19 if is_short else 21, "bold"),
        "hud_val": get_font(21 if is_short else 24, "heavy"),
        "hud_sub": get_font(19 if is_short else 22, "bold"),
        "flow_lbl": get_font(17 if is_short else 19, "bold"),
        "headline": get_font(40 if is_short else 42, "heavy"),
        "headline_sm": get_font(34 if is_short else 38, "heavy"),
        "bubble": get_font(21 if is_short else 22, "bold"),
        "bubble_sm": get_font(18 if is_short else 20, "bold"),
        "actor_name": get_font(20 if is_short else 21, "heavy"),
        "actor_name_sm": get_font(17 if is_short else 20, "heavy"),
        "actor_sub": get_font(17 if is_short else 18, "regular"),
        "focal_hero": get_font(62 if is_short else 66, "heavy"),
        "focal_big": get_font(48 if is_short else 52, "heavy"),
        "ledger_amt": get_font(32 if is_short else 36, "heavy"),
        "card_title": get_font(28 if is_short else 34, "heavy"),
        "card_kicker": get_font(17 if is_short else 18, "heavy"),
        "bar_lbl": get_font(21 if is_short else 24, "bold"),
        "slice_lbl": get_font(17 if is_short else 19, "bold"),
        "focal_pill": get_font(20 if is_short else 22, "bold"),
    }


def _collect_strings(obj: Any, out: list[str]) -> None:
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_strings(v, out)
    elif isinstance(obj, (list, tuple)):
        for it in obj:
            _collect_strings(it, out)


def assert_v51_containment(
    layout: dict[str, Any],
    scenes_cfg: list[dict[str, Any]],
    scene_meta: list[dict],
    fonts: dict[str, ImageFont.FreeTypeFont],
    sprite_sz: int,
    is_short: bool,
    wmp_mod: Any = None,
) -> None:
    """Kiểm toán hình học tất định trước khi render: Zero Zone 3, Đối xứng Tâm (W/2, H/2), Anti-Monotony, LUẬT 6b/8/10 & B1-B4."""
    if "SUBTITLE_BOX" in layout:
        raise RuntimeError("FAIL [Zero Zone 3]: Vẫn còn định nghĩa SUBTITLE_BOX trong layout")

    W, H = layout["W"], layout["H"]
    hud, stg = layout["HUD_BOX"], layout["STAGE_BOX"]
    if hud[3] + 20 > stg[1]:
        raise RuntimeError(f"FAIL [LUẬT 8]: HUD_BOX {hud} và STAGE_BOX {stg} quá sát nhau (<20px)")
    if (hud[0] + hud[2]) != W or (stg[0] + stg[2]) != W or hud[0] != (W - hud[2]) or stg[0] != (W - stg[2]):
        raise RuntimeError(f"FAIL [Symmetry X]: Khối HUD/STAGE không đối xứng trục X={W/2}: hud={hud}, stg={stg}")
    if hud[1] != (H - stg[3]):
        raise RuntimeError(f"FAIL [Symmetry Y]: Lề trên ({hud[1]}) != lề dưới ({H - stg[3]}): hud={hud}, stg={stg}")

    dummy = ImageDraw.Draw(Image.new("RGBA", (32, 32)))
    audit_texts: list[str] = []
    st_pad = 24 if is_short else 28
    floor_w = (stg[2] - stg[0]) - 2 * st_pad

    # Chống đơn điệu: 0 được phép có 2 cảnh liên tiếp trùng archetype trên Video Dài 16:9
    if not is_short:
        for i in range(len(scenes_cfg) - 1):
            if scenes_cfg[i].get("archetype") == scenes_cfg[i + 1].get("archetype"):
                raise RuntimeError(
                    f"FAIL [Anti-Monotony]: Hai cảnh liên tiếp s{i} và s{i+1} trùng archetype '{scenes_cfg[i].get('archetype')}'"
                )

    for s_idx, sc in enumerate(scenes_cfg):
        audit_texts.append(sc["step"])
        if sc.get("hud_left"):
            audit_texts.append(sc["hud_left"])
        audit_texts.append(sc["hud_right"])
        audit_texts.append(sc["flow"]["label"])

        left_hud_txt = nfc(sc.get("hud_left") or f"KÉT QUÁN: {fmt_vnd(sc['ket'])}")

        if is_short:
            if s_idx == 0:
                pill_w = ((hud[0] + hud[2]) / 2.0 - 8) - (hud[0] + 24)
                if dummy.textlength(left_hud_txt, font=fonts["hud_val"]) > pill_w - 28:
                    raise RuntimeError(f"FAIL [HUD Short L]: Chữ tràn pill trái ở s{s_idx}: {left_hud_txt!r}")
                if dummy.textlength(nfc(sc["hud_right"]), font=fonts["hud_sub"]) > pill_w - 28:
                    raise RuntimeError(f"FAIL [HUD Short R]: Chữ tràn pill phải ở s{s_idx}: {sc['hud_right']!r}")
            else:
                for st_tag, st_lbl in sc.get("step_cards", SHORT_STEP_CARDS):
                    audit_texts.extend((st_tag, st_lbl))
                    if dummy.textlength(nfc(st_tag), font=fonts["card_kicker"]) > 142:
                        raise RuntimeError(f"FAIL [HUD Short Stepper Tag]: Tràn thẻ: {st_tag!r}")
                    if dummy.textlength(nfc(st_lbl), font=fonts["bubble_sm"]) > 152:
                        raise RuntimeError(f"FAIL [HUD Short Stepper Lbl]: Tràn thẻ: {st_lbl!r}")
            if sc.get("is_hook") and "hook_data" in sc:
                hd = sc["hook_data"]
                _collect_strings(hd, audit_texts)
                for side in ("left", "right"):
                    if dummy.textlength(nfc(hd[f"{side}_title"]), font=fonts["card_kicker"]) > 370:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Title tràn thẻ {side}: {hd[f'{side}_title']!r}")
                    if dummy.textlength(nfc(hd[f"{side}_amt"]), font=fonts["ledger_amt"]) > 378:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Số tràn thẻ {side}: {hd[f'{side}_amt']!r}")
                    if dummy.textlength(nfc(hd[f"{side}_sub"]), font=fonts["bar_lbl"]) > 378:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Sub tràn thẻ {side}: {hd[f'{side}_sub']!r}")
                if dummy.textlength(nfc(hd["hook_kicker"]), font=fonts["card_kicker"]) > 760:
                    raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Kicker tràn thẻ: {hd['hook_kicker']!r}")
                if dummy.textlength(nfc(hd["hook_line1"]), font=fonts["hud_val"]) > 824:
                    raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Line1 tràn thẻ: {hd['hook_line1']!r}")
                if dummy.textlength(nfc(hd["hook_line2"]), font=fonts["hud_val"]) > 824:
                    raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Line2 tràn thẻ: {hd['hook_line2']!r}")
                if dummy.textlength(nfc(hd["hook_sub"]), font=fonts["actor_sub"]) > 824:
                    raise RuntimeError(f"FAIL [LUẬT 6b Hook]: Sub hook tràn thẻ: {hd['hook_sub']!r}")
        else:
            seg_left = W / 2.0 - 181.0
            seg_right = W / 2.0 + 181.0
            step_pad = 56
            step_end = hud[0] + step_pad + dummy.textlength(nfc(sc["step"]), font=fonts["hud_title"])
            right_lbl = nfc(f"{left_hud_txt}  ·  {sc['hud_right']}")
            w_r_best = dummy.textlength(right_lbl, font=fonts["hud_title"])
            right_start = hud[2] - 28 - w_r_best
            if step_end + 20 > seg_left:
                raise RuntimeError(f"FAIL [HUD Long L]: Tiêu đề chạm khay bước ở s{s_idx} ({step_end:.0f} > {seg_left - 20:.0f})")
            if s_idx >= 1 and right_start - 20 < seg_right:
                raise RuntimeError(f"FAIL [HUD Long R]: Nhãn phải chạm khay bước ở s{s_idx} ({right_start:.0f} < {seg_right + 20:.0f})")

            # Kiểm tra đủ 4 phrase_beats (<= 6 từ) & toàn bộ chữ trong arch_data
            pbeats = sc.get("phrase_beats") or []
            if len(pbeats) != 4:
                raise RuntimeError(f"FAIL [v6.0 4-Beat]: Cảnh Long s{s_idx} phải có đúng 4 phrase_beats (hiện có {len(pbeats)})")
            for pb_i, (hl_txt, _, _) in enumerate(pbeats):
                audit_texts.append(hl_txt)
                n_words = len([w for w in hl_txt.split() if w not in ("·", "—", "-")])
                if n_words > 6:
                    raise RuntimeError(f"FAIL [PhraseBeat <= 6 words]: s{s_idx}.pb{pb_i} có {n_words} từ: {hl_txt!r}")
                if dummy.textlength(nfc(hl_txt), font=fonts["headline_sm"]) > (stg[2] - stg[0] - 2 * st_pad - 24):
                    raise RuntimeError(f"FAIL [LUẬT 6b]: phrase_beat tràn Sân khấu ở s{s_idx}.pb{pb_i}: {hl_txt!r}")

            if sc.get("archetype") == "HOOK_STAGE" and "hook_data" in sc:
                hd = sc["hook_data"]
                _collect_strings(hd, audit_texts)
                for side in ("left", "right"):
                    if dummy.textlength(nfc(hd[f"{side}_title"]), font=fonts["card_kicker"]) > 700:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook Long]: Title tràn thẻ {side}")
                    if dummy.textlength(nfc(hd[f"{side}_amt"]), font=fonts["focal_big"]) > 700:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook Long]: Số tràn thẻ {side}")
                    if dummy.textlength(nfc(hd[f"{side}_sub"]), font=fonts["bar_lbl"]) > 700:
                        raise RuntimeError(f"FAIL [LUẬT 6b Hook Long]: Sub tràn thẻ {side}")
                if dummy.textlength(nfc(hd["hook_kicker"]), font=fonts["card_kicker"]) > 1520:
                    raise RuntimeError("FAIL [LUẬT 6b Hook Long]: hook_kicker tràn thẻ")
                if dummy.textlength(nfc(hd["hook_line1"]), font=fonts["hud_title"]) > 1600:
                    raise RuntimeError("FAIL [LUẬT 6b Hook Long]: hook_line1 tràn băng")
                if dummy.textlength(nfc(hd["hook_sub"]), font=fonts["actor_sub"]) > 1600:
                    raise RuntimeError("FAIL [LUẬT 6b Hook Long]: hook_sub tràn băng")

            ad = sc.get("arch_data") or {}
            _collect_strings(ad, audit_texts)
            arch = sc.get("archetype")
            if arch == "TWIN_SHOWDOWN":
                for side in ("left", "right"):
                    cfg = ad[side]
                    for txt, fnt, lim in [
                        (cfg["kicker"], fonts["card_kicker"], 700),
                        (cfg["big"], fonts["focal_big"], 700),
                        (cfg["sub"], fonts["bar_lbl"], 700),
                        (cfg["tag1"], fonts["hud_sub"], 640),
                        (cfg["tag2"], fonts["hud_sub"], 640),
                    ]:
                        if dummy.textlength(nfc(txt), font=fnt) > lim:
                            raise RuntimeError(f"FAIL [LUẬT 6b Twin]: Tràn thẻ {side} ở s{s_idx}: {txt!r}")
            elif arch == "GAUGE_AND_LOCK":
                bw = 1568
                split_px = bw * ad["ratio"]
                if dummy.textlength(nfc(ad["locked_lbl"]), font=fonts["bar_lbl"]) > split_px - 68:
                    raise RuntimeError(f"FAIL [LUẬT 6b Gauge L]: Tràn thanh trái ở s{s_idx}: {ad['locked_lbl']!r}")
                if dummy.textlength(nfc(ad["free_lbl"]), font=fonts["bar_lbl"]) > (bw - split_px) - 68:
                    raise RuntimeError(f"FAIL [LUẬT 6b Gauge R]: Tràn thanh phải ở s{s_idx}: {ad['free_lbl']!r}")
                for side in ("card_left", "card_right"):
                    kicker, big_st, desc, _ = ad[side]
                    for txt, fnt in [(kicker, fonts["card_kicker"]), (big_st, fonts["card_title"]), (desc, fonts["bar_lbl"])]:
                        if dummy.textlength(nfc(txt), font=fnt) > 776:
                            raise RuntimeError(f"FAIL [LUẬT 6b GaugeCard]: Tràn thẻ ở s{s_idx}: {txt!r}")
            elif arch == "LEDGER_BOARD":
                for row_key in ("debit_rows", "credit_rows"):
                    rows = ad[row_key]
                    for code, amt, note, _ in rows:
                        if len(rows) > 1:
                            cw_req = dummy.textlength(nfc(code), font=fonts["bar_lbl"]) + dummy.textlength(nfc(amt), font=fonts["ledger_amt"])
                            if cw_req > 700:
                                raise RuntimeError(f"FAIL [LUẬT 6b Ledger]: Tràn dòng 2 cột ở s{s_idx}: {code!r} + {amt!r}")
                        elif dummy.textlength(nfc(code), font=fonts["bar_lbl"]) > 720 or dummy.textlength(nfc(note), font=fonts["hud_sub"]) > 720:
                            raise RuntimeError(f"FAIL [LUẬT 6b Ledger]: Tràn dòng ở s{s_idx}: {code!r}")
            elif arch == "WATERFALL_SPLIT":
                for bk in ad["buckets"]:
                    for txt, fnt, lim in [
                        (bk["title"], fonts["hud_title"], 470),
                        (bk["sub"], fonts["bar_lbl"], 476),
                        (bk["amt"], fonts["focal_big"], 476),
                        (bk["note"], fonts["hud_sub"], 458),
                    ]:
                        if dummy.textlength(nfc(txt), font=fnt) > lim:
                            raise RuntimeError(f"FAIL [LUẬT 6b Waterfall]: Tràn bể ở s{s_idx}: {txt!r}")
            elif arch == "FULL_TRIPTYCH_3":
                for card in ad["cards"]:
                    for txt, fnt, lim in [
                        (card["title"], fonts["card_title"], 476),
                        (card["sub"], fonts["bar_lbl"], 476),
                        (card["when"], fonts["hud_sub"], 448),
                        (card["flow"], fonts["hud_sub"], 448),
                        (card["impact"], fonts["hud_sub"], 448),
                    ]:
                        if dummy.textlength(nfc(txt), font=fnt) > lim:
                            raise RuntimeError(f"FAIL [LUẬT 6b Triptych]: Tràn cột ở s{s_idx}: {txt!r}")
            elif arch == "RELAY_PIPELINE":
                if ad.get("sub_mode") == "NETTING_3":
                    for nt, na, ns, _ in ad["net_cols"]:
                        if dummy.textlength(nfc(na), font=fonts["ledger_amt"]) > 498 or dummy.textlength(nfc(ns), font=fonts["actor_sub"]) > 498:
                            raise RuntimeError(f"FAIL [LUẬT 6b Netting]: Tràn cột ở s{s_idx}: {na!r}")
                else:
                    for item in sc["focal"].get("items", []):
                        if dummy.textlength(nfc(item), font=fonts["bar_lbl"]) > 500:
                            raise RuntimeError(f"FAIL [LUẬT 6b Checklist]: Tràn ô cổng ở s{s_idx}: {item!r}")

        for b_idx, (hl_txt, hi_sub, _) in enumerate(sc["beat_headlines"]):
            audit_texts.append(hl_txt)
            n_words = len([w for w in hl_txt.split() if w not in ("·", "—", "-")])
            if n_words > 6:
                raise RuntimeError(f"FAIL [Headline <= 6 words]: s{s_idx}.beat{b_idx+1} có {n_words} từ: {hl_txt!r}")
            if dummy.textlength(nfc(hl_txt), font=fonts["headline_sm"]) > (stg[2] - stg[0] - 2 * st_pad - 24):
                raise RuntimeError(f"FAIL [LUẬT 6b]: Headline tràn Sân khấu ở s{s_idx}.beat{b_idx+1}: {hl_txt!r}")

        if is_short or sc.get("archetype") == "RELAY_PIPELINE":
            actors = sc["actors"]
            n_act = len(actors)
            compact_act = is_short and n_act >= 3
            f_tag = fonts["bubble_sm"] if compact_act else fonts["bubble"]
            f_name = fonts["actor_name_sm"] if compact_act else fonts["actor_name"]
            margin_x = (160 if n_act >= 3 else 230) if is_short else (340 if n_act <= 2 else (240 if n_act == 3 else 190))
            span_x = (stg[2] - margin_x) - (stg[0] + margin_x)
            prev_r_bubble = -1e9
            prev_r_badge = -1e9
            for ai, a in enumerate(actors):
                a_name = a.get("name") or ARCHETYPES[a["id"]]["name"]
                a_sub = a.get("sub") or ARCHETYPES[a["id"]]["sub"]
                audit_texts.extend((a["tag"], a_name, a_sub))
                cx = (stg[0] + stg[2]) / 2.0 if n_act == 1 else (stg[0] + margin_x + (span_x * ai) / float(n_act - 1))
                pw = dummy.textlength(nfc(a["tag"]), font=f_tag) + (22 if compact_act else 28)
                npw = max(dummy.textlength(nfc(a_name), font=f_name) + 24, 118 if compact_act else 136)
                half_w = max(pw, npw, sprite_sz) / 2.0
                if cx - half_w < stg[0] + 16 or cx + half_w > stg[2] - 16:
                    raise RuntimeError(f"FAIL [LUẬT 6b]: Actor {ai} tràn mép sân khấu ở s{s_idx}")
                if (cx - pw / 2.0) < prev_r_bubble + 14:
                    raise RuntimeError(f"FAIL [LUẬT 10]: Bong bóng actor {ai} đè nhau ở s{s_idx}: {a['tag']!r}")
                if (cx - npw / 2.0) < prev_r_badge + 14:
                    raise RuntimeError(f"FAIL [LUẬT 10]: Nhãn tên actor {ai} đè nhau ở s{s_idx}")
                prev_r_bubble = cx + pw / 2.0
                prev_r_badge = cx + npw / 2.0

        focal = sc["focal"]
        _collect_strings(focal, audit_texts)
        if dummy.textlength(nfc(focal["pill"]), font=fonts["focal_pill"]) > floor_w - 48:
            raise RuntimeError(f"FAIL [LUẬT 6b]: Pill tóm tắt tràn sàn ở s{s_idx}: {focal['pill']!r}")
        inner_bw = floor_w - (56 if is_short else 144)
        if focal["type"] in ("SPLIT_BAR", "HOLD_GAUGE"):
            lw_req = dummy.textlength(nfc(focal["left_lbl"]), font=fonts["bar_lbl"])
            rw_req = dummy.textlength(nfc(focal["right_lbl"]), font=fonts["bar_lbl"])
            if lw_req > inner_bw * focal["ratio"] - 20:
                raise RuntimeError(f"FAIL [LUẬT 6b]: Thanh trái tràn ở s{s_idx}: {focal['left_lbl']!r}")
            if rw_req > inner_bw * (1.0 - focal["ratio"]) - 20:
                raise RuntimeError(f"FAIL [LUẬT 6b]: Thanh phải tràn ở s{s_idx}: {focal['right_lbl']!r}")
        elif focal["type"] == "THREE_SLICE":
            for lbl, amt, share, _ in focal["slices"]:
                sw_px = inner_bw * share - 6
                if dummy.textlength(nfc(lbl), font=fonts["slice_lbl"]) > sw_px - 10:
                    raise RuntimeError(f"FAIL [LUẬT 6b]: Nhãn slice tràn ở s{s_idx}: {lbl!r} ({sw_px:.0f}px)")
                if dummy.textlength(nfc(amt), font=fonts["bar_lbl"]) > sw_px - 10:
                    raise RuntimeError(f"FAIL [LUẬT 6b]: Số slice tràn ở s{s_idx}: {amt!r} ({sw_px:.0f}px)")

    for sm in scene_meta:
        for ch in sm.get("srt_chunks", []):
            audit_texts.append(ch["text"])

    assert_broadcast_overlay_clean(audit_texts)

    # Tái sử dụng step_5_0_brand_safety_audit từ wmp để soát tên riêng thương hiệu B1-B4
    if wmp_mod is not None and hasattr(wmp_mod, "step_5_0_brand_safety_audit"):
        clean_title = "Quẹt thẻ mười triệu đồng thanh toán và bù trừ liên ngân hàng"
        synth_scenes = [{"vo": txt, "onScreen": txt, "visual": ""} for txt in audit_texts]
        wmp_mod.step_5_0_brand_safety_audit(
            "card_overlay_audit",
            {"title": clean_title, "videoScript": {"long": {"title": clean_title, "scenes": synth_scenes}, "short": {"title": clean_title, "scenes": []}}},
        )


def _resolve_audio_cache(story_key: str, fmt_name: str, voice_id: str = "") -> pathlib.Path | None:
    el_path = CACHE_DIR / f"{story_key}_{fmt_name}_continuous_v3.json"
    tts_path = TTS_CACHE_DIR / f"{story_key}_{fmt_name}_continuous.json"
    order = (tts_path, el_path) if voice_id.startswith("vieneu:") else (el_path, tts_path)
    for cand in order:
        if cand.is_file():
            return cand
    return None


def _hydrate_color(val: Any) -> Any:
    palette = {
        "PAPER_BG": PAPER_BG,
        "PAPER_CARD": PAPER_CARD,
        "PAPER_FLOOR": PAPER_FLOOR,
        "PAPER_SOFT": PAPER_SOFT,
        "INK": INK,
        "INK_MUTED": INK_MUTED,
        "AMBER": AMBER,
        "AMBER_LIGHT": AMBER_LIGHT,
        "GREEN": GREEN,
        "GREEN_LIGHT": GREEN_LIGHT,
        "CORAL": CORAL,
        "CORAL_LIGHT": CORAL_LIGHT,
        "NAVY": NAVY,
        "TEAL": TEAL,
        "TERRACOTTA": TERRACOTTA,
        "GOLD": GOLD,
    }
    if isinstance(val, str) and val in palette:
        return palette[val]
    if isinstance(val, list) and len(val) == 3 and all(isinstance(x, int) for x in val):
        return (val[0], val[1], val[2])
    return val


def _hydrate_scenes_list(scenes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for raw in scenes:
        sc = json.loads(json.dumps(raw))
        if "step_cards" in sc and isinstance(sc["step_cards"], list):
            sc["step_cards"] = [(a, b) for a, b in sc["step_cards"]]
        if "beat_headlines" in sc and isinstance(sc["beat_headlines"], list):
            sc["beat_headlines"] = tuple((a, b, _hydrate_color(c)) for a, b, c in sc["beat_headlines"])
        if "phrase_beats" in sc and isinstance(sc["phrase_beats"], list):
            sc["phrase_beats"] = [(a, b, _hydrate_color(c)) for a, b, c in sc["phrase_beats"]]
        hd = sc.get("hook_data")
        if isinstance(hd, dict):
            for k in ("left_accent", "right_accent"):
                if k in hd:
                    hd[k] = _hydrate_color(hd[k])
        foc = sc.get("focal")
        if isinstance(foc, dict):
            if "color" in foc:
                foc["color"] = _hydrate_color(foc["color"])
            if "slices" in foc and isinstance(foc["slices"], list):
                foc["slices"] = [(lbl, amt, share, _hydrate_color(col)) for lbl, amt, share, col in foc["slices"]]
            for ck in ("cols", "items"):
                if isinstance(foc.get(ck), list):
                    foc[ck] = [tuple(x) if isinstance(x, list) else x for x in foc[ck]]
        ad = sc.get("arch_data")
        if isinstance(ad, dict):
            for side in ("left", "right"):
                if isinstance(ad.get(side), dict) and "accent" in ad[side]:
                    ad[side]["accent"] = _hydrate_color(ad[side]["accent"])
            for tk in ("top_left", "top_right"):
                if isinstance(ad.get(tk), list) and len(ad[tk]) == 3:
                    lbl, amt, col = ad[tk]
                    ad[tk] = (lbl, amt, _hydrate_color(col))
            for ck in ("card_left", "card_right"):
                if isinstance(ad.get(ck), list) and len(ad[ck]) == 4:
                    kicker, big, desc, col = ad[ck]
                    ad[ck] = (kicker, big, desc, _hydrate_color(col))
            for rk in ("debit_rows", "credit_rows"):
                if isinstance(ad.get(rk), list):
                    ad[rk] = [(code, amt, note, _hydrate_color(col)) for code, amt, note, col in ad[rk]]
            if isinstance(ad.get("net_cols"), list):
                ad["net_cols"] = [(nt, na, ns, _hydrate_color(col)) for nt, na, ns, col in ad["net_cols"]]
            if isinstance(ad.get("buckets"), list):
                for bk in ad["buckets"]:
                    if isinstance(bk, dict) and "color" in bk:
                        bk["color"] = _hydrate_color(bk["color"])
            if isinstance(ad.get("cards"), list):
                for card in ad["cards"]:
                    if isinstance(card, dict) and "color" in card:
                        card["color"] = _hydrate_color(card["color"])
        out.append(sc)
    return out


def render_format(
    wmp,
    story_key: str,
    story: dict,
    sfx_map: dict[str, bytes],
    fmt_name: str,
    scenes_cfg: list[dict[str, Any]],
    preview_dir: pathlib.Path | None = None,
    validate_only: bool = False,
) -> pathlib.Path | None:
    is_short = fmt_name == "short"
    layout = LAYOUT_SHORT if is_short else LAYOUT_LONG
    W, H = layout["W"], layout["H"]
    FPS = 30

    vblock = (story.get("videoScript") or {}).get("short" if is_short else "long") or {}
    cache_file = _resolve_audio_cache(story_key, "short" if is_short else "long", str(vblock.get("elevenlabsVoiceId") or ""))
    if cache_file is None and not validate_only:
        raise RuntimeError(
            f"Missing audio cache for '{story_key}' ({fmt_name}) in {CACHE_DIR} or {TTS_CACHE_DIR}"
        )

    scenes_vo = story["videoScript"]["short" if is_short else "long"]["scenes"]
    if len(scenes_vo) != len(scenes_cfg):
        raise RuntimeError(f"Scene count mismatch {story_key}.{fmt_name}: vo={len(scenes_vo)} != cfg={len(scenes_cfg)}")
    fonts = load_fonts(is_short)

    sprite_sz = 166 if is_short else 156
    sprites = SpriteBank(sprite_sz)
    parchment_bg = make_parchment_canvas(W, H)

    slug_fmt = "short-9x16" if is_short else "long-16x9"
    out_mp4 = DIST_DIR / f"{story_key}-{slug_fmt}.mp4"
    out_srt = DIST_DIR / f"{story_key}-{slug_fmt}.srt"
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"wms_v72_{story_key}_{fmt_name}_") as tmp:
        tmp_dir = pathlib.Path(tmp)
        if cache_file is not None:
            cont_data = json.loads(cache_file.read_text(encoding="utf-8"))
            master_wav, scene_meta, total_dur = build_master_audio(scenes_vo, cont_data, sfx_map, tmp_dir)
            build_srt_chunks(scene_meta, max_words=8)
            assert_v51_containment(layout, scenes_cfg, scene_meta, fonts, sprite_sz, is_short, wmp_mod=wmp)
        else:
            synth_meta = [
                {"index": i, "win_t0": i * 10.0, "win_t1": (i + 1) * 10.0, "phrases": [{"t0": i * 10.0 + p * 2.5} for p in range(4)], "srt_chunks": []}
                for i in range(len(scenes_cfg))
            ]
            assert_v51_containment(layout, scenes_cfg, synth_meta, fonts, sprite_sz, is_short, wmp_mod=wmp)
            print(f"[VALIDATE ONLY PASS] {story_key}.{fmt_name} ({len(scenes_cfg)} scenes, LUẬT 6b/8/10 + B1–B4 clean)")
            return None
        if validate_only:
            print(f"[VALIDATE ONLY PASS] {story_key}.{fmt_name} ({len(scenes_cfg)} scenes, {total_dur:.2f}s, LUẬT 6b/8/10 + B1–B4 clean)")
            return None
        export_srt_subtitles(scene_meta, out_srt)

        if preview_dir is not None:
            preview_dir.mkdir(parents=True, exist_ok=True)
            saved_paths: list[str] = []
            for p_idx, p_tag in ((0, "hook"), (2, "step2")):
                if p_idx < len(scene_meta):
                    sm_p = scene_meta[p_idx]
                    p_dur = max(0.5, sm_p["win_t1"] - sm_p["win_t0"])
                    t_snap = sm_p["win_t0"] + min(2.4 if p_idx == 0 else 3.0, p_dur * 0.62)
                    p_img = render_v51_frame(layout, parchment_bg, sprites, scenes_cfg, scene_meta, p_idx, t_snap, fonts, is_short)
                    p_out = preview_dir / f"v72_{story_key}_{fmt_name}_s{p_idx}_{p_tag}.jpg"
                    p_img.save(str(p_out), format="JPEG", quality=90)
                    saved_paths.append(p_out.name)
            print(f"[PREVIEW PASS] {story_key}.{fmt_name} ({len(scenes_cfg)} scenes, {total_dur:.2f}s) -> {', '.join(saved_paths)}")
            return None

        ver_tag = "v7.2 Craft"
        total_frames = int(round(total_dur * FPS))
        print(f"=== [{story_key.upper()}.{fmt_name.upper()} {ver_tag} Zero-Zone3] Audio={total_dur:.2f}s | Frames={total_frames} | {W}x{H} ===")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
            "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
            "-i", str(master_wav),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4),
        ]
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.stdin is not None

        TRANS_HALF = 0.28
        t0_wall = time.time()
        paper_rgb = Image.new("RGB", (W, H), PAPER_BG)

        for f_idx in range(total_frames):
            t = f_idx / FPS
            frame_img: Image.Image | None = None

            for b_idx in range(len(scene_meta) - 1):
                b_t = scene_meta[b_idx]["win_t1"]
                if (b_t - TRANS_HALF) <= t <= (b_t + TRANS_HALF):
                    alpha = smoothstep(b_t - TRANS_HALF, b_t + TRANS_HALF, t)
                    img_a = render_v51_frame(layout, parchment_bg, sprites, scenes_cfg, scene_meta, b_idx, t, fonts, is_short)
                    img_b = render_v51_frame(layout, parchment_bg, sprites, scenes_cfg, scene_meta, b_idx + 1, t, fonts, is_short)
                    frame_img = Image.blend(img_a, img_b, alpha)
                    break

            if frame_img is None:
                cur_idx = len(scene_meta) - 1
                for idx, sm in enumerate(scene_meta):
                    if sm["win_t0"] <= t <= sm["win_t1"]:
                        cur_idx = idx
                        break
                frame_img = render_v51_frame(layout, parchment_bg, sprites, scenes_cfg, scene_meta, cur_idx, t, fonts, is_short)

            if t < 0.25:
                frame_img = Image.blend(paper_rgb, frame_img, smoothstep(0.0, 0.25, t))
            elif t > total_dur - 0.50:
                frame_img = Image.blend(frame_img, paper_rgb, smoothstep(total_dur - 0.50, total_dur, t))

            proc.stdin.write(frame_img.tobytes())
            if (f_idx + 1) % 600 == 0 or f_idx == total_frames - 1:
                elapsed = time.time() - t0_wall
                print(f"  -> [{story_key}.{fmt_name}] Frame {f_idx + 1}/{total_frames} ({(f_idx + 1)/max(0.01, elapsed):.1f} fps)")

        proc.stdin.close()
        stderr_out = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
        ret = proc.wait()
        if ret != 0:
            raise RuntimeError(f"FFmpeg error {ret}:\n{stderr_out[-1200:]}")

    print(f"[PASS] Saved {out_mp4} ({out_mp4.stat().st_size:,} bytes) + {out_srt.name}")
    return out_mp4


ALL_LEGACY_STORIES = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")


def _resolve_scenes(story_key: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if story_key == "card":
        return SHORT_SCENES, LONG_SCENES
    if story_key in ALL_LEGACY_STORIES:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        from wms_v72_topics import get_topic_scenes

        return get_topic_scenes(story_key)
    scene_json = ROOT / "data" / "video-scenes" / f"{story_key}.json"
    if not scene_json.is_file():
        raise FileNotFoundError(f"Thiếu cấu hình cảnh video cho bài '{story_key}': {scene_json}")
    cfg = json.loads(scene_json.read_text(encoding="utf-8"))
    return _hydrate_scenes_list(cfg["short"]), _hydrate_scenes_list(cfg["long"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", default="card")
    parser.add_argument("--format", default="both", choices=["short", "long", "both"])
    parser.add_argument("--preview-dir", type=pathlib.Path, default=None)
    parser.add_argument("--validate-only", action="store_true", help="Chỉ chạy kiểm định hình học LUẬT 6b/8/10 & B1–B4, không mã hoá MP4")
    args = parser.parse_args()

    wmp = load_pipeline_module()
    stories = wmp.extract_stories((ROOT / "docs/prototype.html").read_text(encoding="utf-8"))
    sfx_map = load_cached_sfx()
    if args.story == "all":
        target_stories = tuple(
            sk
            for sk in stories
            if sk in ALL_LEGACY_STORIES or (ROOT / "data" / "video-scenes" / f"{sk}.json").is_file()
        )
    else:
        if args.story not in stories:
            raise SystemExit(f"LỖI: Không tìm thấy bài '{args.story}' trong STORIES")
        target_stories = (args.story,)

    for sk in target_stories:
        story = stories[sk]
        audit = wmp.step_5_0_brand_safety_audit(sk, story)
        print(f"[Brand Safety B1-B4 PASS] {sk}: {audit['scenesAudited']} scenes clean")
        short_cfg, long_cfg = _resolve_scenes(sk)
        if args.format in ("short", "both"):
            render_format(wmp, sk, story, sfx_map, "short", short_cfg, preview_dir=args.preview_dir, validate_only=args.validate_only)
        if args.format in ("long", "both"):
            render_format(wmp, sk, story, sfx_map, "long", long_cfg, preview_dir=args.preview_dir, validate_only=args.validate_only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
