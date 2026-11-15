#!/usr/bin/env bash
# wms-pre-push.sh — Git pre-push hook cho repo where-money-sleeps (LUẬT 12 · QĐ 64).
# Cài đặt vào .git/hooks/pre-push:
#   ln -sf ../../scripts/wms-pre-push.sh .git/hooks/pre-push && chmod +x scripts/wms-pre-push.sh
#
# Khoá cứng quy trình PR-only: từ chối (exit 1) mọi thao tác `git push` nhắm thẳng vào
# `refs/heads/main` hoặc `refs/heads/master`. Mọi thay đổi phải đẩy lên nhánh phụ và merge qua PR.

set -euo pipefail

while IFS=' ' read -r local_ref local_sha remote_ref remote_sha; do
  [ -z "${remote_ref:-}" ] && continue
  case "$remote_ref" in
    refs/heads/main|refs/heads/master)
      cat >&2 <<'ERR'
[WMS HARD RULE — LUẬT 12 / QĐ 64] CẤM push thẳng vào nhánh 'main' (hoặc 'master')!
  Quy trình bắt buộc cho where-money-sleeps:
    1. Tạo/checkout nhánh phụ:  git checkout -b <feat|fix|content|docs|chore>/<mo-ta>
    2. Chạy cổng kiểm tra:     bash scripts/wms-check.sh && python3 -I scripts/wms-qa-verify.py --ci
    3. Đẩy nhánh phụ lên remote: git push -u origin <ten-nhanh>
    4. Mở Pull Request vào main: gh pr create --base main
ERR
      exit 1
      ;;
  esac
done

exit 0
