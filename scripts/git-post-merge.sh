#!/usr/bin/env bash
# git-post-merge.sh — Hook tự động kiểm tra & deploy lên Cloudflare Workers + D1
# khi chạy `git merge` vào nhánh `main` ở máy local.
# Để cài đặt vào .git/hooks/post-merge:
#   ln -sf ../../scripts/git-post-merge.sh .git/hooks/post-merge && chmod +x scripts/git-post-merge.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$CURRENT_BRANCH" != "main" ]; then
  exit 0
fi

echo "[post-merge] Đã merge vào nhánh main — đang chạy cổng kiểm T1 + QA..."
bash scripts/wms-check.sh --quiet
python3 -I scripts/wms-qa-verify.py --ci

if [ "${WMS_SKIP_LOCAL_POST_MERGE_DEPLOY:-0}" = "1" ]; then
  echo "[post-merge] Bỏ qua local deploy (WMS_SKIP_LOCAL_POST_MERGE_DEPLOY=1). Tạo nhánh phụ & mở PR (gh pr create --base main) để GitHub Actions deploy khi PR merge."
  exit 0
fi

echo "[post-merge] Đang tự động deploy lên Cloudflare Workers + D1..."
python3 -I scripts/wms-deploy-cloudflare.py
echo "[post-merge] Hoàn tất! Theo LUẬT 12 (QĐ 64), mọi thay đổi mới phải đi qua nhánh phụ & Pull Request (gh pr create --base main) để GitHub Actions (.github/workflows/deploy.yml) verify & deploy."
