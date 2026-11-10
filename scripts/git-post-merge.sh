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
  echo "[post-merge] Bỏ qua local deploy (WMS_SKIP_LOCAL_POST_MERGE_DEPLOY=1). Hãy git push origin main để GitHub Actions deploy."
  exit 0
fi

echo "[post-merge] Đang tự động deploy lên Cloudflare Workers + D1..."
python3 -I scripts/wms-deploy-cloudflare.py
echo "[post-merge] Hoàn tất! Khi bạn chạy 'git push origin main', GitHub Actions (.github/workflows/deploy.yml) cũng sẽ tự động verify & deploy."
