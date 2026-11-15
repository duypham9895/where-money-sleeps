#!/usr/bin/env python3
"""
wms-render-editorial-figs.py — Bộ dựng 28 Hình Minh Hoạ Biên Tập v7.2 (16:9 · 1200×675)
theo ngôn ngữ Paper-Warm Minimalist Craft thống nhất 100% với bộ Video v7.2.

Mỗi bài khảo cứu (7 bài × 4 Chương 02–05 = 28 hình) kết xuất trực tiếp từ
cảnh Long 16:9 tương ứng trong `wms-render-v50-focus.py` (`1920×1080`) rồi
thu mẫu chuẩn LANCZOS về `1200×675` vào `public/brand/{sid}-fig-{1..4}.jpg`.
"""

from __future__ import annotations

import importlib.util
import pathlib
import shutil
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
V50_PATH = ROOT / "scripts" / "wms-render-v50-focus.py"
BRAND_DIR = ROOT / "public" / "brand"
BRAIN_DIR = ROOT / ".cache" / "brain"

TARGET_SIZE = (1200, 675)

# Mapping chính xác giữa 4 hình mặt cắt mỗi bài (Chương 02..05 trong docs/prototype.html CHAP_FIGS)
# và chỉ số cảnh (s_idx) trong video Long 16:9 v7.2 của từng chủ đề.
FIG_SCENE_MAP: dict[str, list[int]] = {
    "card": [1, 5, 6, 9],
    "pay": [2, 5, 7, 8],
    "install": [2, 4, 6, 9],
    "minpay": [2, 5, 6, 8],
    "qr": [1, 3, 6, 7],
    "profitcash": [2, 5, 7, 6],
    "offus": [1, 4, 6, 8],
}


def load_v50_module():
    spec = importlib.util.spec_from_file_location("wms_v50_focus", V50_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Không nạp được {V50_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_synthetic_scene_meta(n_scenes: int) -> list[dict]:
    return [
        {
            "index": i,
            "win_t0": 0.0,
            "win_t1": 10.0,
            "phrases": [{"t0": 0.0}, {"t0": 2.5}, {"t0": 5.0}, {"t0": 7.5}],
        }
        for i in range(n_scenes)
    ]


def main() -> int:
    v50 = load_v50_module()
    layout = v50.LAYOUT_LONG
    W, H = layout["W"], layout["H"]
    fonts = v50.load_fonts(is_short=False)
    sprites = v50.SpriteBank(156)
    parchment_bg = v50.make_parchment_canvas(W, H)

    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    brain_brand = BRAIN_DIR / "public" / "brand"
    brain_brand.mkdir(parents=True, exist_ok=True)

    count = 0
    for story_key, scene_indices in FIG_SCENE_MAP.items():
        _, long_cfg = v50._resolve_scenes(story_key)
        synth_meta = build_synthetic_scene_meta(len(long_cfg))

        for fig_num, s_idx in enumerate(scene_indices, start=1):
            sc = long_cfg[s_idx]
            arch = sc.get("archetype")
            # WATERFALL_SPLIT & FULL_TRIPTYCH_3 hiển thị cả 3 cột/bể sáng rõ đồng đều tại beat4_idx=0 (t=1.5s >= anim_u=1.0).
            # Các archetype còn lại chốt đầy đủ 2 vế + huy hiệu đối xứng tại beat4_idx=3 (t=8.6s).
            t_snap = 1.5 if arch in ("WATERFALL_SPLIT", "FULL_TRIPTYCH_3") else 8.6

            frame_1080p = v50.render_v51_frame(
                layout,
                parchment_bg,
                sprites,
                long_cfg,
                synth_meta,
                s_idx,
                t_snap,
                fonts,
                is_short=False,
            )
            fig_img = frame_1080p.convert("RGB").resize(TARGET_SIZE, Image.Resampling.LANCZOS)

            out_name = f"{story_key}-fig-{fig_num}.jpg"
            out_path = BRAND_DIR / out_name
            fig_img.save(str(out_path), format="JPEG", quality=92, optimize=True)
            shutil.copy2(out_path, brain_brand / out_name)
            shutil.copy2(out_path, BRAIN_DIR / out_name)

            size_b = out_path.stat().st_size
            if size_b < 10_000:
                raise RuntimeError(f"Ảnh xuất ra quá nhỏ (<10KB): {out_path} ({size_b} bytes)")
            count += 1
            print(f"[OK] {out_name} <- {story_key}.long.s{s_idx} [{arch}] (t={t_snap:.1f}s, {size_b:,} bytes)")

    print(f"Done! Rendered {count} 16:9 (1200x675) v7.2 Paper-Warm Editorial Figures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
