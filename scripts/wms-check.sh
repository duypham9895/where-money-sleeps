#!/usr/bin/env bash
# wms-check — MỘT lệnh kiểm toàn bộ repo where-money-sleeps.
#
#   1. scripts/check-story.py     dữ liệu bài (C0–C7, C6v, C9) + bộ luật trong repo (C8)
#   2. scripts/wms-finance-kb.py  chuyên gia tài chính (F1–F4: cơ chế ngân hàng, toán IRR/EIR, kho tri thức, bài↔video)
#   3. scripts/wms-motion-snap.py chuyên gia chuyển động bang-motion (M0–M4: Anti-PPT, Kinetic Counter, Split-Stage, Seek)
#   4. ../scripts/vibe-check.sh   pipeline · ONE-PAGER · kể-lại · giấy phép · đường dẫn chết · tầng HTML
#                                 — script của XƯỞNG CHA. Clone riêng repo thì không có ⇒ SKIP, nói rõ.
#
# Dùng:  scripts/wms-check.sh [tham số cho check-story.py, vd --story pay --quiet]
# Thoát: 0 = mọi bước chạy được đều sạch · 1 = có FAIL
# Chạy được từ bất kỳ thư mục nào: script tự cd về gốc repo.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 2
cd "$ROOT" || exit 2

# LUẬT 12 (QĐ 64): tự cài symlink .git/hooks/pre-push khi clone mới hoặc chạy CI
if [ -d .git/hooks ] && [ -f scripts/wms-pre-push.sh ] && [ ! -e .git/hooks/pre-push ]; then
  ln -sf ../../scripts/wms-pre-push.sh .git/hooks/pre-push 2>/dev/null || true
fi

rc=0
echo "════ [0/6] Entry parity (docs/prototype.html == index.html) ════"
if cmp -s docs/prototype.html index.html; then
  echo "PASS: docs/prototype.html ≡ index.html"
else
  echo "FAIL: docs/prototype.html lệch với index.html — chạy 'cp docs/prototype.html index.html'" >&2
  rc=1
fi

echo
echo "════ [1/6] check-story.py ════"
python3 -I scripts/check-story.py "$@" || rc=1

echo
echo "════ [2/6] wms-finance-kb.py (tai-chinh-reviewer F1–F4) ════"
python3 -I scripts/wms-finance-kb.py --verify || rc=1

echo
echo "════ [3/6] wms-motion-snap.py (bang-motion M1–M4) ════"
python3 -I scripts/wms-motion-snap.py || rc=1

echo
echo "════ [4/6] wms-studio-sync.py (Studio Data & Waveform Sync QĐ 59) ════"
python3 -I scripts/wms-studio-sync.py --verify || rc=1

echo
echo "════ [5/6] wms-feedback-test.py (Footer & Hộp thư E2E) ════"
python3 -I scripts/wms-feedback-test.py --ci || rc=1

echo
echo "════ [6/6] vibe-check.sh (xưởng cha) ════"
if [ -f ../scripts/vibe-check.sh ]; then
  bash ../scripts/vibe-check.sh . || rc=1
else
  echo "SKIP — không thấy ../scripts/vibe-check.sh: repo đang đứng một mình (không nằm trong xưởng Vibe)."
  echo "       Các phép [1]–[6] của xưởng (ONE-PAGER, kể-lại, giấy phép, đường dẫn chết, ngân sách HTML) CHƯA chạy."
fi

echo
if [ "$rc" -ne 0 ]; then echo "wms-check: FAIL"; else echo "wms-check: PASS (bước SKIP ở trên không tính là PASS)"; fi
exit "$rc"
