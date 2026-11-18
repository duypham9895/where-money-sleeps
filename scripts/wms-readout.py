#!/usr/bin/env python3
"""
wms-readout.py — Công cụ CLI tổng hợp số liệu M1–M5 từ Cloudflare D1 (`counts` − `quarantined_days`).

Cách dùng:
  python3 -I scripts/wms-readout.py --selftest
  python3 -I scripts/wms-readout.py --remote
  python3 -I scripts/wms-readout.py --remote --append
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READOUT_MD = ROOT / "gates" / "06-iterate" / "READOUT.md"
DB_NAME = "where-money-sleeps-db"
LESSONS = ("card", "pay", "install", "minpay", "qr", "profitcash", "offus")
CARDS = tuple(f"{sid}-q{q}.v1" for sid in LESSONS for q in (1, 2))
D1_SQL = (
    "SELECT day, event, d1, d2, n FROM counts "
    "WHERE day NOT IN (SELECT day FROM quarantined_days) ORDER BY day ASC;"
)


def fmt_cell(n: int) -> str:
    if 0 < n < 5:
        return "<5 (ẩn theo AC-69)"
    return str(n)


def compute_metrics(rows: list[dict]) -> dict:
    days = sorted({str(r.get("day", "")) for r in rows if r.get("day")})
    lc_total: dict[str, int] = defaultdict(int)
    lc_from_start: dict[str, int] = defaultdict(int)
    card_ok: dict[str, int] = defaultdict(int)
    card_bad: dict[str, int] = defaultdict(int)
    sync_created: dict[str, int] = defaultdict(int)
    prog_restored: dict[str, int] = defaultdict(int)

    for r in rows:
        ev = str(r.get("event") or "")
        d1 = str(r.get("d1") or "")
        d2 = str(r.get("d2") or "")
        n = int(r.get("n") or 0)
        if n <= 0:
            continue
        if ev == "lesson_completed":
            lc_total[d1] += n
            if d2 == "true":
                lc_from_start[d1] += n
        elif ev == "card_answered":
            if d2 == "true":
                card_ok[d1] += n
            else:
                card_bad[d1] += n
        elif ev == "sync_created":
            sync_created[d1] += n
        elif ev == "progress_restored":
            prog_restored[d1] += n

    card1_total = lc_total["card"]
    qr5_total = lc_total["qr"]
    qr5_strict = lc_from_start["qr"]

    baseline_ready = len(days) >= 28 and card1_total >= 100
    m1_strict = (qr5_strict / card1_total) if card1_total >= 5 and qr5_strict >= 5 else None
    m1_loose = (qr5_total / card1_total) if card1_total >= 5 and qr5_total >= 5 else None

    m2 = {
        sid: {"total": lc_total[sid], "display": fmt_cell(lc_total[sid])}
        for sid in LESSONS
    }

    m3 = {}
    for cid in CARDS:
        ok_n = card_ok[cid]
        tot_n = ok_n + card_bad[cid]
        acc = (ok_n / tot_n) if tot_n >= 5 else None
        flag = bool(tot_n >= 30 and acc is not None and acc < 0.40)
        m3[cid] = {
            "correct": ok_n,
            "total": tot_n,
            "display_total": fmt_cell(tot_n),
            "display_correct": fmt_cell(ok_n),
            "accuracy": round(acc, 4) if acc is not None else None,
            "needs_revision_v2": flag,
        }

    m5 = {}
    for method in ("link", "code"):
        m5[method] = {
            "created": sync_created[method],
            "created_display": fmt_cell(sync_created[method]),
            "restored": prog_restored[method],
            "restored_display": fmt_cell(prog_restored[method]),
        }
    zalo_fragment_warning = sync_created["link"] >= 5 and prog_restored["link"] == 0

    return {
        "distinct_days": len(days),
        "first_day": days[0] if days else None,
        "last_day": days[-1] if days else None,
        "baseline_ready": baseline_ready,
        "m1": {
            "card_total": card1_total,
            "qr_total": qr5_total,
            "qr_from_start": qr5_strict,
            "strict_ratio": round(m1_strict, 4) if m1_strict is not None else None,
            "loose_ratio": round(m1_loose, 4) if m1_loose is not None else None,
        },
        "m2": m2,
        "m3": m3,
        "m5": m5,
        "zalo_fragment_warning": zalo_fragment_warning,
    }


def render_markdown(report: dict, today: str) -> str:
    m1 = report["m1"]
    strict_s = f"{m1['strict_ratio'] * 100:.1f}%" if m1["strict_ratio"] is not None else "ẩn/chưa đủ mẫu (AC-69)"
    loose_s = f"{m1['loose_ratio'] * 100:.1f}%" if m1["loose_ratio"] is not None else "ẩn/chưa đủ mẫu (AC-69)"
    lines = [
        f"### Đọc số tự động D1 ngày `{today}`",
        "",
        f"- Khoảng ngày có dữ liệu: `{report['first_day'] or '—'}` → `{report['last_day'] or '—'}` (`{report['distinct_days']}` ngày · điều kiện mở baseline `>= 28 ngày & bài 1 >= 100`: `{'ĐẠT' if report['baseline_ready'] else 'CHƯA ĐẠT'}`)",
        f"- **`M1` (Bài 5 `qr` / Bài 1 `card`):** Chặt = `{strict_s}` (`{fmt_cell(m1['qr_from_start'])} / {fmt_cell(m1['card_total'])}`) · Lỏng = `{loose_s}` (`{fmt_cell(m1['qr_total'])} / {fmt_cell(m1['card_total'])}`)",
        "- **`M2` (Hoàn thành theo bài):** " + " · ".join(f"`{s}`={report['m2'][s]['display']}" for s in LESSONS),
        f"- **`M5` (`#sync`):** `link` tạo `{report['m5']['link']['created_display']}` / khôi phục `{report['m5']['link']['restored_display']}` · `code` tạo `{report['m5']['code']['created_display']}` / khôi phục `{report['m5']['code']['restored_display']}`"
        + (" · **CẢNH BÁO:** Nghi ngờ WebView cắt `#fragment` (`link` khôi phục = 0)" if report["zalo_fragment_warning"] else ""),
    ]
    low_cards = [c for c, v in report["m3"].items() if v["needs_revision_v2"]]
    lines.append(
        "- **`M3` (`WMS_QUIZ_BANK`):** "
        + (", ".join(f"`{c}` cần soát `.v2` ({report['m3'][c]['accuracy']*100:.1f}%)" for c in low_cards) if low_cards else "Không có thẻ nào `< 40%` (với `n >= 30`)")
    )
    return "\n".join(lines) + "\n"


def fetch_remote_rows() -> list[dict]:
    cmd = ["npx", "--yes", "wrangler@4", "d1", "execute", DB_NAME, "--remote", "--json", f"--command={D1_SQL}"]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"wrangler d1 execute failed: {proc.stderr.strip() or proc.stdout.strip()}")
    payload = json.loads(proc.stdout)
    if isinstance(payload, list) and payload:
        return list(payload[0].get("results") or [])
    if isinstance(payload, dict):
        return list(payload.get("results") or [])
    return []


def run_selftest() -> int:
    sample_rows = [
        {"day": f"2026-11-{i:02d}", "event": "lesson_completed", "d1": "card", "d2": "true", "n": 4}
        for i in range(1, 29)
    ]
    sample_rows.extend([
        {"day": "2026-11-10", "event": "lesson_completed", "d1": "qr", "d2": "true", "n": 14},
        {"day": "2026-11-11", "event": "lesson_completed", "d1": "qr", "d2": "false", "n": 6},
        {"day": "2026-11-12", "event": "lesson_completed", "d1": "offus", "d2": "true", "n": 3},
        {"day": "2026-11-12", "event": "card_answered", "d1": "card-q1.v1", "d2": "true", "n": 10},
        {"day": "2026-11-12", "event": "card_answered", "d1": "card-q1.v1", "d2": "false", "n": 25},
        {"day": "2026-11-12", "event": "sync_created", "d1": "link", "d2": "", "n": 7},
        {"day": "2026-11-12", "event": "progress_restored", "d1": "code", "d2": "", "n": 2},
    ])
    rep = compute_metrics(sample_rows)
    assert rep["distinct_days"] == 28, rep
    assert rep["baseline_ready"] is True, rep
    assert rep["m1"]["card_total"] == 112, rep
    assert rep["m1"]["strict_ratio"] == round(14 / 112, 4), rep
    assert rep["m1"]["loose_ratio"] == round(20 / 112, 4), rep
    assert rep["m2"]["offus"]["display"] == "<5 (ẩn theo AC-69)", rep
    assert rep["m3"]["card-q1.v1"]["needs_revision_v2"] is True, rep
    assert rep["zalo_fragment_warning"] is True, rep
    assert rep["m5"]["code"]["restored_display"] == "<5 (ẩn theo AC-69)", rep
    md = render_markdown(rep, "2026-11-18")
    assert "<5 (ẩn theo AC-69)" in md and "card-q1.v1" in md
    print("PASS: wms-readout.py --selftest (AC-69, M1–M5, baseline >=28d & >=100, Zalo #fragment flag)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--remote", action="store_true")
    ap.add_argument("--append", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return run_selftest()
    if not args.remote:
        ap.print_help()
        return 1

    rows = fetch_remote_rows()
    rep = compute_metrics(rows)
    today = dt.date.today().isoformat()
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        md = render_markdown(rep, today)
        print(md)
        if args.append:
            with READOUT_MD.open("a", encoding="utf-8") as fh:
                fh.write("\n" + md)
            print(f"Appended readout to {READOUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
