#!/usr/bin/env python3
"""
wms_tts_vieneu.py — Bộ tổng hợp giọng đọc tiếng Việt local (VieNeu-TTS v3 Turbo, Apache 2.0)
thay thế ElevenLabs cho Where Money Sleeps:
  - Chạy offline trên Apple Silicon (ONNX Runtime, torch-free) qua venv độc lập.
  - Đọc liền theo từng đoạn (block-level, temperature=0.60, top_k=20, crossfade_p=0.025)
    và xử lý mastering EQ podcast (atempo=0.96, highpass, warmth, de-harsh, compressor,
    loudnorm -14 LUFS) trước khi đo mốc thời gian để chống lệch nhịp.
  - Xuất đúng cấu trúc JSON (`audio_base64` + `alignment` từng ký tự) để
    `wms-build-beats-audio.py`, `wms-render-v50-focus.py`, `wms-studio-sync.py`
    tiêu thụ trực tiếp mà không phải đổi hợp đồng pipeline.
  - Mọi file `.wav`/`.mp3` tạm đều nằm trong `/tmp` (`TemporaryDirectory`), tuyệt đối không rơi vào repo.
"""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
VIENEU_PYTHON = pathlib.Path("/Users/edwardpham/.local/share/wms-vieneu-venv/bin/python")
DEFAULT_VIENEU_VOICE = "Hải Đăng"
AUDIO_PROFILE = "v2-block-tuned-eq"
BLOCK_GAP_SEC = 0.22
SAMPLE_RATE = 44_100


def resolve_main_root(repo_root: pathlib.Path = ROOT) -> pathlib.Path:
    """Resolve main git repository root even when invoked from a linked `/tmp` worktree."""
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


MAIN_ROOT = resolve_main_root(ROOT)
TTS_CACHE_DIR = MAIN_ROOT / ".cache" / "tts"


def plain_text(s: str) -> str:
    no_links = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", str(s or ""))
    return re.sub(r"\s+", " ", no_links).strip()


def split_sentences(block: str) -> list[str]:
    clean = block.strip()
    if not clean:
        return []
    raw_parts = [p.strip() for p in re.split(r"(?<=[.?!…])\s+", clean) if p.strip()]
    if len(raw_parts) <= 1:
        return raw_parts or [clean]
    merged: list[str] = []
    carry = ""
    for part in raw_parts:
        candidate = f"{carry} {part}".strip() if carry else part
        n_toks = len(candidate.split())
        if (n_toks <= 2 or re.match(r"^(?:\d+\.|VD\.|Ví\s+dụ\.)$", candidate, re.I)) and len(merged) == 0:
            carry = candidate
            continue
        if n_toks <= 2 or re.match(r"^(?:\d+\.|VD\.)$", candidate, re.I):
            merged[-1] = f"{merged[-1]} {candidate}"
        else:
            merged.append(candidate)
        carry = ""
    if carry:
        if merged:
            merged[-1] = f"{merged[-1]} {carry}"
        else:
            merged.append(carry)
    return merged or [clean]


def _char_weight(ch: str) -> float:
    if ch.isspace():
        return 0.05
    if ch in ",;:":
        return 0.45
    if ch in ".?!…":
        return 0.55
    if ch in "—–-\"'()[]":
        return 0.15
    return 1.0


def build_char_alignment(
    full_text: str,
    block_spans: list[tuple[int, int]],
    sent_entries: list[dict],
) -> dict:
    """Build character-level start/end timestamps matching `full_text` 1-to-1."""
    n = len(full_text)
    starts = [0.0] * n
    ends = [0.0] * n

    for ent in sent_entries:
        s_pos = ent["start_char"]
        s_end = ent["end_char"]
        t0 = float(ent["t0"])
        t1 = float(ent["t1"])
        span = full_text[s_pos : s_end + 1]
        weights = [_char_weight(ch) for ch in span]
        tot_w = max(1e-6, sum(weights))
        dur = max(0.05, t1 - t0)
        cur_t = t0
        for off, w in enumerate(weights):
            dt_ch = dur * (w / tot_w)
            idx = s_pos + off
            starts[idx] = round(cur_t, 4)
            ends[idx] = round(cur_t + dt_ch, 4)
            cur_t += dt_ch
        if s_end >= s_pos:
            ends[s_end] = round(t1, 4)

    if n > 0 and sent_entries:
        last_t = 0.0
        for i in range(n):
            if ends[i] > starts[i] or (starts[i] > 0.0):
                last_t = ends[i]
            else:
                nxt_t = last_t
                for j in range(i + 1, n):
                    if ends[j] > starts[j] or starts[j] > 0.0:
                        nxt_t = starts[j]
                        break
                starts[i] = round(last_t, 4)
                ends[i] = round(max(last_t, nxt_t), 4)

    for b0, b1 in block_spans:
        if 0 <= b0 <= b1 < n and ends[b1] < starts[b0]:
            ends[b1] = starts[b0]

    return {
        "characters": list(full_text),
        "character_start_times_seconds": starts,
        "character_end_times_seconds": ends,
    }


_WORKER_CODE = r'''
import json, pathlib, sys, wave
import numpy as np

job = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
out_dir = pathlib.Path(job["out_dir"])
voice_id = job["voice"]
blocks = job["blocks"]

from vieneu import Vieneu
tts = Vieneu(threads=6)
preset = tts.get_preset_voice(voice_id)
sr = int(getattr(tts, "sample_rate", 48_000))

def trim_and_fade(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr, dtype=np.float32).reshape(-1)
    if len(arr) == 0:
        return np.zeros(int(0.25 * sr), dtype=np.float32)
    nz = np.flatnonzero(np.abs(arr) > 0.004)
    if nz.size > 0:
        pad = int(0.030 * sr)
        i0 = max(0, int(nz[0]) - pad)
        i1 = min(len(arr), int(nz[-1]) + pad)
        arr = arr[i0:i1].copy()
    fade = min(int(0.015 * sr), len(arr) // 4)
    if fade > 1:
        ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        arr[:fade] *= ramp
        arr[-fade:] *= ramp[::-1]
    return np.clip(arr, -0.98, 0.98)

results = []
for idx, text in enumerate(blocks):
    wav = tts.infer(
        text=text,
        voice=preset,
        temperature=0.60,
        top_k=20,
        top_p=0.90,
        repetition_penalty=1.15,
        max_chars=256,
        silence_p=0.16,
        crossfade_p=0.025,
    )
    wav = trim_and_fade(wav)
    wav_path = out_dir / f"raw_{idx:04d}.wav"
    pcm16 = (wav * 32767.0).astype(np.int16)
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm16.tobytes())
    results.append({"index": idx, "wav": wav_path.name, "samples": int(len(wav)), "duration": len(wav) / sr})

pathlib.Path(sys.argv[2]).write_text(json.dumps({"sample_rate": sr, "results": results}), encoding="utf-8")
'''

_BLOCK_VOCAL_AF = (
    "atempo=0.96,"
    "highpass=f=75,"
    "lowshelf=f=175:g=2.4:w=0.8,"
    "equalizer=f=3400:t=q:w=1.8:g=-2.5,"
    "equalizer=f=6200:t=q:w=2.0:g=-1.5,"
    "highshelf=f=10500:g=1.2:w=0.9,"
    "acompressor=threshold=-20dB:ratio=2.2:attack=15:release=160:makeup=1.5"
)


def synthesize_continuous_json(
    blocks: list[str],
    out_json: pathlib.Path,
    voice_id: str = DEFAULT_VIENEU_VOICE,
    force: bool = False,
) -> dict:
    """Synthesize `blocks` joined by `\\n\\n` via block-level VieNeu-TTS + vocal mastering."""
    clean_blocks = [plain_text(b) for b in blocks if plain_text(b)]
    if not clean_blocks:
        raise ValueError("Danh sách đoạn văn đầu vào trống.")

    full_text = "\n\n".join(clean_blocks)
    voice_spec = f"vieneu:{voice_id}"

    if not force and out_json.is_file():
        try:
            existing = json.loads(out_json.read_text(encoding="utf-8"))
            cached_text = "".join((existing.get("alignment") or {}).get("characters") or [])
            if (
                existing.get("voice_spec") == voice_spec
                and existing.get("profile") == AUDIO_PROFILE
                and cached_text == full_text
                and existing.get("audio_base64")
            ):
                print(f"[VieNeu Cache Hit] {out_json.name} ({len(full_text)} chars · {voice_id})")
                return existing
        except Exception:
            pass

    if not VIENEU_PYTHON.is_file():
        raise RuntimeError(f"Thiếu môi trường VieNeu-TTS tại {VIENEU_PYTHON}")

    block_sentences: list[list[str]] = [split_sentences(b) for b in clean_blocks]
    sent_locs_by_block: list[list[tuple[int, int, str]]] = []
    block_spans: list[tuple[int, int]] = []
    cursor = 0
    total_sents = 0
    for b_idx, b_str in enumerate(clean_blocks):
        b_pos = full_text.find(b_str, cursor)
        if b_pos < 0:
            b_pos = cursor
        b_end = b_pos + len(b_str) - 1
        block_spans.append((b_pos, b_end))
        s_cur = b_pos
        b_list: list[tuple[int, int, str]] = []
        for s_str in block_sentences[b_idx]:
            s_pos = full_text.find(s_str, s_cur)
            if s_pos < 0:
                s_pos = s_cur
            s_end = s_pos + len(s_str) - 1
            b_list.append((s_pos, s_end, s_str))
            s_cur = s_end + 1
            total_sents += 1
        sent_locs_by_block.append(b_list)
        cursor = b_end + 1

    print(
        f"[VieNeu-TTS {voice_id} · {AUDIO_PROFILE}] Đang tổng hợp {len(clean_blocks)} đoạn liền khối "
        f"({total_sents} câu, {len(full_text)} ký tự)..."
    )

    with tempfile.TemporaryDirectory(prefix="wms_vieneu_") as td:
        tmp_dir = pathlib.Path(td)
        job_path = tmp_dir / "job.json"
        res_path = tmp_dir / "res.json"
        worker_path = tmp_dir / "worker.py"
        job_path.write_text(
            json.dumps({"voice": voice_id, "blocks": clean_blocks, "out_dir": str(tmp_dir)}, ensure_ascii=False),
            encoding="utf-8",
        )
        worker_path.write_text(_WORKER_CODE, encoding="utf-8")

        env = os.environ.copy()
        hf_hub = pathlib.Path.home() / ".cache" / "huggingface" / "hub"
        if (hf_hub / "models--pnnbao-ump--VieNeu-TTS-v3-Turbo").is_dir():
            env["HF_HUB_OFFLINE"] = "1"

        proc = subprocess.run(
            [str(VIENEU_PYTHON), str(worker_path), str(job_path), str(res_path)],
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,
            check=False,
        )
        if proc.returncode != 0 and env.get("HF_HUB_OFFLINE"):
            env.pop("HF_HUB_OFFLINE", None)
            proc = subprocess.run(
                [str(VIENEU_PYTHON), str(worker_path), str(job_path), str(res_path)],
                env=env,
                capture_output=True,
                text=True,
                timeout=1800,
                check=False,
            )
        if proc.returncode != 0:
            raise RuntimeError(
                f"VieNeu worker lỗi (exit {proc.returncode}): {(proc.stderr or proc.stdout)[-1000:]}"
            )

        res_data = json.loads(res_path.read_text(encoding="utf-8"))
        results = res_data["results"]

        sr = SAMPLE_RATE
        block_gap = np.zeros(int(BLOCK_GAP_SEC * sr), dtype=np.int16)
        pcm_parts: list[np.ndarray] = []
        sent_entries: list[dict] = []
        cur_samples = 0

        for b_idx, item in enumerate(results):
            if b_idx > 0:
                pcm_parts.append(block_gap)
                cur_samples += len(block_gap)

            raw_wav = tmp_dir / item["wav"]
            proc_wav = tmp_dir / f"proc_{b_idx:04d}.wav"
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(raw_wav),
                    "-af",
                    _BLOCK_VOCAL_AF,
                    "-ar",
                    str(sr),
                    "-ac",
                    "1",
                    "-sample_fmt",
                    "s16",
                    str(proc_wav),
                ],
                check=True,
                capture_output=True,
            )
            with wave.open(str(proc_wav), "rb") as wf:
                raw_pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)

            b_t0 = cur_samples / sr
            pcm_parts.append(raw_pcm)
            cur_samples += len(raw_pcm)
            b_t1 = cur_samples / sr
            b_dur = max(0.05, b_t1 - b_t0)

            s_items = sent_locs_by_block[b_idx]
            s_weights = [max(0.1, sum(_char_weight(ch) for ch in s_str)) for _, _, s_str in s_items]
            tot_w = max(1e-6, sum(s_weights))
            s_t = b_t0
            for s_i, (s_pos, s_end, _) in enumerate(s_items):
                dt_s = b_dur * (s_weights[s_i] / tot_w)
                st0 = s_t
                st1 = b_t1 if s_i == len(s_items) - 1 else (s_t + dt_s)
                sent_entries.append({"start_char": s_pos, "end_char": s_end, "t0": st0, "t1": st1})
                s_t = st1

        all_pcm = np.concatenate(pcm_parts) if pcm_parts else np.zeros(int(0.5 * sr), dtype=np.int16)
        stitched_wav = tmp_dir / "stitched.wav"
        stitched_mp3 = tmp_dir / "stitched.mp3"
        with wave.open(str(stitched_wav), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(all_pcm.tobytes())

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(stitched_wav),
                "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=9",
                "-ar",
                str(sr),
                "-ac",
                "2",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "128k",
                str(stitched_mp3),
            ],
            check=True,
            capture_output=True,
        )
        total_dur = round(cur_samples / sr, 3)
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(stitched_mp3),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        mp3_dur = float(probe.stdout.strip())
        if abs(mp3_dur - total_dur) >= 0.25:
            raise RuntimeError(
                f"Phát hiện lệch thời lượng MP3 sau mastering: mp3={mp3_dur:.3f}s vs alignment={total_dur:.3f}s"
            )
        audio_b64 = base64.b64encode(stitched_mp3.read_bytes()).decode("ascii")

    alignment = build_char_alignment(full_text, block_spans, sent_entries)
    payload = {
        "provider": "vieneu",
        "profile": AUDIO_PROFILE,
        "voice_spec": voice_spec,
        "sample_rate": sr,
        "duration_seconds": total_dur,
        "blocks_count": len(clean_blocks),
        "sentences_count": total_sents,
        "audio_base64": audio_b64,
        "alignment": alignment,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    tmp_json = out_json.with_suffix(".tmp")
    tmp_json.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp_json.replace(out_json)
    print(f"  -> Đã lưu cache TTS: {out_json} ({total_dur:.2f}s, mp3={mp3_dur:.2f}s · {out_json.stat().st_size // 1024} KB)")
    return payload


def _extract_blocks_for_story(story_key: str, fmt: str) -> tuple[list[str], str]:
    spec = importlib.util.spec_from_file_location("check_story", ROOT / "scripts/check-story.py")
    assert spec and spec.loader
    cs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cs)
    src = (ROOT / "docs/prototype.html").read_text(encoding="utf-8")
    stories = cs.extract(src, "STORIES")
    if story_key not in stories:
        raise KeyError(f"Không tìm thấy bài '{story_key}' trong STORIES")
    st = stories[story_key]
    if fmt == "beats":
        blocks = [" ".join(plain_text(s) for s in (b.get("say") or []) if plain_text(s)) for b in (st.get("beats") or [])]
        return blocks, DEFAULT_VIENEU_VOICE

    fobj = (st.get("videoScript") or {}).get(fmt) or {}
    blocks = [plain_text(sc.get("vo") or "") for sc in (fobj.get("scenes") or []) if plain_text(sc.get("vo") or "")]
    vspec = str(fobj.get("elevenlabsVoiceId") or "")
    parsed_voice = vspec.split(":", 1)[1].strip() if vspec.startswith("vieneu:") and ":" in vspec else ""
    voice = parsed_voice or DEFAULT_VIENEU_VOICE
    return blocks, voice


def main() -> int:
    ap = argparse.ArgumentParser(description="Tổng hợp giọng đọc VieNeu-TTS v3 Turbo local (Apache 2.0)")
    ap.add_argument("--story", default=None, help="Slug bài viết trong STORIES")
    ap.add_argument("--format", choices=("beats", "short", "long"), default="beats")
    ap.add_argument("--voice", default=None, help=f"Tên preset voice VieNeu (mặc định {DEFAULT_VIENEU_VOICE!r})")
    ap.add_argument("--force", action="store_true", help="Bỏ qua cache cũ và tổng hợp lại")
    ap.add_argument("--smoke", action="store_true", help="Chạy kiểm thử nhanh trên 2 đoạn ngắn trong /tmp")
    args = ap.parse_args()

    if args.smoke:
        with tempfile.TemporaryDirectory(prefix="wms_vieneu_smoke_") as td:
            out_p = pathlib.Path(td) / "smoke.json"
            blocks = [
                "Chín giờ mười lăm sáng thứ Ba. Bạn mở ứng dụng ngân hàng, bấm chuyển đúng mười hai triệu đồng đóng phí bảo hiểm cho một năm bảo vệ phía trước.",
                "Thực tế kế toán và dòng tiền vận hành khác hẳn cả hai suy nghĩ đó.",
            ]
            data = synthesize_continuous_json(blocks, out_p, voice_id=args.voice or DEFAULT_VIENEU_VOICE, force=True)
            full_text = "\n\n".join(blocks)
            al = data["alignment"]
            assert len(al["characters"]) == len(full_text)
            assert len(al["character_start_times_seconds"]) == len(full_text)
            assert len(al["character_end_times_seconds"]) == len(full_text)
            assert data.get("profile") == AUDIO_PROFILE
            assert data["duration_seconds"] > 2.0
            print(f"[SMOKE PASS] VieNeu-TTS ({data['voice_spec']} · {data['profile']}) alignment exact ({len(full_text)} chars, {data['duration_seconds']:.2f}s)")
        return 0

    if not args.story:
        ap.error("Cần truyền `--story <slug>` hoặc `--smoke`.")

    blocks, inferred_voice = _extract_blocks_for_story(args.story, args.format)
    voice_id = args.voice or inferred_voice
    out_json = TTS_CACHE_DIR / f"{args.story}_{args.format}_continuous.json"
    synthesize_continuous_json(blocks, out_json, voice_id=voice_id, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
