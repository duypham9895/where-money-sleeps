#!/usr/bin/env python3
"""
wms-build-beats-audio.py — Tổng hợp giọng đọc ElevenLabs eleven_v3 Signature Voice Giọng Tâm
(JwqRvOqFdGeQNu7UjKjw, stability=0.65, similarity_boost=0.80, style=0.20, use_speaker_boost=True)
cho 5 đoạn mặt cắt Diorama (STORIES[k].beats[0..4].say) của toàn bộ 7 bài học trên website.

Đầu ra:
  - .cache/elevenlabs/<story>_beats_continuous_v3.json (bộ nhớ đệm ElevenLabs with-timestamps)
  - public/audio/<story>-beats.mp3 (chuẩn âm lượng phát sóng -14 LUFS, Room Tone -33 dBFS, SFX -22 dBFS, cầu nối hơi thở 0.36s)
  - public/audio/beats-manifest.json (toạ độ thời gian [t0, t1] chính xác tới từng mili-giây cho từng đoạn beat và từng câu say[s])
"""

from __future__ import annotations

import base64
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache/elevenlabs"
AUDIO_OUT_DIR = ROOT / "public/audio"
VOICE_ID = "JwqRvOqFdGeQNu7UjKjw"
MODEL_ID = "eleven_v3"
VOICE_SETTINGS = {
    "stability": 0.65,
    "similarity_boost": 0.80,
    "style": 0.20,
    "use_speaker_boost": True,
}
STORIES_ORDER = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")


def load_pipeline():
    spec = importlib.util.spec_from_file_location("wmp", ROOT / "scripts/wms-media-pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def plain_text(s: str) -> str:
    return re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", str(s or "")).strip()


def load_sfx_pcm(sfx_name: str, sr: int, tmp_dir: pathlib.Path) -> np.ndarray | None:
    cfile = CACHE_DIR / f"{sfx_name}.json"
    if not cfile.is_file():
        return None
    try:
        data = json.loads(cfile.read_text(encoding="utf-8"))
        mp3_b = base64.b64decode(data["audio_base64"])
        mp3_p = tmp_dir / f"{sfx_name}.mp3"
        wav_p = tmp_dir / f"{sfx_name}.wav"
        mp3_p.write_bytes(mp3_b)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp3_p), "-ar", str(sr), "-ac", "2", str(wav_p)],
            check=True,
            capture_output=True,
        )
        with wave.open(str(wav_p), "rb") as wf:
            n = wf.getnframes()
            return np.frombuffer(wf.readframes(n), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0
    except Exception:
        return None


def synthesize_story_beats(story_key: str, story: dict, api_key: str) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_OUT_DIR.mkdir(parents=True, exist_ok=True)

    beats = story.get("beats") or []
    beat_sents: list[list[str]] = []
    beat_texts: list[str] = []
    for b in beats:
        sents = [plain_text(x) for x in (b.get("say") or []) if plain_text(x)]
        beat_sents.append(sents)
        beat_texts.append(" ".join(sents))

    full_text = "\n\n".join(beat_texts)
    cache_file = CACHE_DIR / f"{story_key}_beats_continuous_v3.json"

    if not cache_file.is_file():
        if not api_key:
            raise RuntimeError(f"Thiếu ELEVENLABS_API_KEY để tổng hợp {cache_file.name}")
        print(f"[ElevenLabs eleven_v3 Giọng Tâm] Đang thu âm 5 đoạn Diorama cho bài '{story_key}' ({len(full_text)} ký tự)...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
        payload = {
            "text": full_text,
            "model_id": MODEL_ID,
            "voice_settings": VOICE_SETTINGS,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw_bytes = resp.read()
        cache_file.write_bytes(raw_bytes)
        print(f"  -> Đã lưu bộ nhớ đệm: {cache_file.relative_to(ROOT)} ({len(raw_bytes):,} bytes)")
    else:
        print(f"[Cache Hit] Đã có sẵn {cache_file.relative_to(ROOT)}")

    cont_data = json.loads(cache_file.read_text(encoding="utf-8"))
    align = cont_data["alignment"]
    starts = [float(x) for x in align["character_start_times_seconds"]]
    ends = [float(x) for x in align["character_end_times_seconds"]]

    with tempfile.TemporaryDirectory(prefix=f"wms_beats_{story_key}_") as td:
        tmp_dir = pathlib.Path(td)
        raw_mp3 = tmp_dir / "raw.mp3"
        raw_wav = tmp_dir / "raw.wav"
        raw_mp3.write_bytes(base64.b64decode(cont_data["audio_base64"]))
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(raw_mp3), "-ar", "44100", "-ac", "2", str(raw_wav)],
            check=True,
            capture_output=True,
        )
        with wave.open(str(raw_wav), "rb") as wf:
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            pcm = np.frombuffer(wf.readframes(n_frames), dtype=np.int16).reshape(-1, 2).astype(np.float32) / 32768.0

        # Tìm vị trí ký tự [pos, end_pos] của từng beat và từng câu trong full_text
        raw_beat_bounds: list[tuple[int, int, float, float, list[tuple[int, int]]]] = []
        cursor = 0
        for b_idx, b_str in enumerate(beat_texts):
            pos = full_text.find(b_str, cursor)
            if pos < 0:
                pos = cursor
            end_pos = pos + len(b_str) - 1
            b_t0 = starts[min(pos, len(starts) - 1)]
            b_t1 = ends[min(end_pos, len(ends) - 1)]

            sent_spans: list[tuple[int, int]] = []
            s_cur = pos
            for s_str in beat_sents[b_idx]:
                s_pos = full_text.find(s_str, s_cur)
                if s_pos < 0:
                    s_pos = s_cur
                s_end = s_pos + len(s_str) - 1
                sent_spans.append((s_pos, s_end))
                s_cur = s_end + 1

            raw_beat_bounds.append((pos, end_pos, b_t0, b_t1, sent_spans))
            cursor = end_pos + 1

        LEAD_IN = 0.18
        BREATH_BRIDGE = 0.36
        TAIL_OUT = 0.45

        chunks: list[np.ndarray] = [np.zeros((int(LEAD_IN * sr), 2), dtype=np.float32)]
        cum_shift = LEAD_IN
        prev_sample_end = 0
        beats_meta: list[dict] = []

        for idx, (pos, end_pos, raw_t0, raw_t1, sent_spans) in enumerate(raw_beat_bounds):
            if idx < len(raw_beat_bounds) - 1:
                next_raw_t0 = raw_beat_bounds[idx + 1][2]
                mid_t = 0.5 * (raw_t1 + next_raw_t0)
                cut_sample = min(len(pcm), int(mid_t * sr))
            else:
                cut_sample = len(pcm)

            seg_pcm = pcm[prev_sample_end:cut_sample].copy()
            fade_len = min(int(0.025 * sr), len(seg_pcm) // 4)
            if fade_len > 1:
                ramp = np.linspace(0.0, 1.0, fade_len, dtype=np.float32)[:, None]
                seg_pcm[:fade_len] *= ramp
                seg_pcm[-fade_len:] *= ramp[::-1]

            chunk_start_sec = sum(len(c) for c in chunks) / sr
            raw_seg_start_sec = prev_sample_end / sr
            time_shift = chunk_start_sec - raw_seg_start_sec

            chunks.append(seg_pcm)
            if idx < len(raw_beat_bounds) - 1:
                chunks.append(np.zeros((int(BREATH_BRIDGE * sr), 2), dtype=np.float32))
            else:
                chunks.append(np.zeros((int(TAIL_OUT * sr), 2), dtype=np.float32))

            sents_out = []
            for s_pos, s_end in sent_spans:
                st0 = round(max(0.0, starts[min(s_pos, len(starts) - 1)] + time_shift), 3)
                st1 = round(max(st0 + 0.25, ends[min(s_end, len(ends) - 1)] + time_shift), 3)
                sents_out.append([st0, st1])

            bt0 = round(max(0.0, raw_t0 + time_shift), 3)
            bt1 = round(max(bt0 + 0.5, raw_t1 + time_shift), 3)
            beats_meta.append(
                {
                    "beat": idx,
                    "t0": bt0,
                    "t1": bt1,
                    "sents": sents_out,
                }
            )
            prev_sample_end = cut_sample

        master_pcm = np.concatenate(chunks, axis=0)
        total_samples = len(master_pcm)

        # Trộn Room Tone ấm -33 dBFS + SFX chuyển nhịp -22 dBFS
        rng = np.random.default_rng(19895 + sum(ord(c) for c in story_key))
        white = rng.standard_normal((total_samples, 2), dtype=np.float32)
        brown = np.cumsum(white * 0.02, axis=0)
        brown -= np.mean(brown, axis=0, keepdims=True)
        max_b = np.max(np.abs(brown)) or 1.0
        room_tone = (brown / max_b) * (10.0 ** (-33.0 / 20.0))
        master_pcm = master_pcm + room_tone

        sfx_wire = load_sfx_pcm("sfx_wire_pulse", sr, tmp_dir)
        sfx_pipe = load_sfx_pcm("sfx_pipe_flow", sr, tmp_dir)
        sfx_chime = load_sfx_pcm("sfx_scale_chime", sr, tmp_dir)
        sfx_gain = 10.0 ** (-22.0 / 20.0)

        for idx, b_obj in enumerate(beats):
            msgs = b_obj.get("msgs") or []
            has_money = any(len(m) >= 3 and m[2] == "money" for m in msgs)
            has_ledger = bool(b_obj.get("ledger"))
            chosen_sfx = sfx_pipe if has_money else (sfx_chime if has_ledger else sfx_wire)
            if chosen_sfx is not None:
                s0 = max(0, int(beats_meta[idx]["t0"] * sr) - int(0.08 * sr))
                s1 = min(total_samples, s0 + len(chosen_sfx))
                if s1 > s0:
                    master_pcm[s0:s1] += chosen_sfx[: s1 - s0] * sfx_gain

        master_pcm = np.clip(master_pcm, -0.98, 0.98)
        mixed_wav = tmp_dir / "mixed.wav"
        with wave.open(str(mixed_wav), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes((master_pcm * 32767.0).astype(np.int16).tobytes())

        out_mp3 = AUDIO_OUT_DIR / f"{story_key}-beats.mp3"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(mixed_wav),
                "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "128k",
                str(out_mp3),
            ],
            check=True,
            capture_output=True,
        )
        total_dur = round(total_samples / sr, 3)
        print(
            f"  [PASS] Đã xuất {out_mp3.relative_to(ROOT)} ({out_mp3.stat().st_size // 1024} KB · {total_dur}s · 5 đoạn Diorama)"
        )
        return {
            "story": story_key,
            "voice": f"{MODEL_ID}:{VOICE_ID}",
            "voiceName": "Giọng Tâm (ElevenLabs eleven_v3 Studio -14 LUFS)",
            "src": f"public/audio/{story_key}-beats.mp3",
            "duration": total_dur,
            "beats": beats_meta,
        }


def main() -> int:
    wmp = load_pipeline()
    wmp.load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    html_src = (ROOT / "docs/prototype.html").read_text(encoding="utf-8")
    stories = wmp.extract_stories(html_src)

    manifest = {}
    for sk in STORIES_ORDER:
        if sk not in stories:
            continue
        manifest[sk] = synthesize_story_beats(sk, stories[sk], api_key)

    manifest_path = AUDIO_OUT_DIR / "beats-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[HOÀN TẤT] Đã ghi {manifest_path.relative_to(ROOT)} cho {len(manifest)} bài học.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
