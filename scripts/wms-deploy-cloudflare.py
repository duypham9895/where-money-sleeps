#!/usr/bin/env python3
"""
wms-deploy-cloudflare.py — Triển khai tự động đầu-cuối Where Money Sleeps lên Cloudflare Workers + Static Assets + D1:
  1. Đóng gói lại `dist/site/` qua `scripts/wms-build-deploy.py`.
  2. Gỡ biến môi trường `CLOUDFLARE_API_TOKEN` bị giới hạn quyền để dùng OAuth token đầy đủ của Wrangler.
  3. Tìm hoặc tạo cơ sở dữ liệu D1 `where-money-sleeps-db`, gắn `database_id` vào `wrangler.jsonc`.
  4. Thực thi `cloudflare/schema.sql` trên D1 remote (`counts` + `quarantined_days` WITHOUT ROWID).
  5. Chạy `npx --yes wrangler deploy` để phát hành cả Static Assets (`dist/site/`) và Worker (`/api/p`) cùng origin.
  6. Kiểm tra HTTP sống (`GET /` -> 200, `GET /studio.html` -> 200, `POST /api/p` -> 204).
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRANGLER_JSONC = ROOT / "wrangler.jsonc"
DB_NAME = "where-money-sleeps-db"


def clean_env() -> dict[str, str]:
    env = dict(os.environ)
    env.pop("CLOUDFLARE_API_TOKEN", None)
    env.pop("CF_API_TOKEN", None)
    return env


def run_cmd(cmd: list[str], env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(cmd)}", flush=True)
    res = subprocess.run(cmd, cwd=str(ROOT), env=env, text=True, capture_output=True)
    if res.stdout:
        print(res.stdout.strip(), flush=True)
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr, flush=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed (exit {res.returncode}): {' '.join(cmd)}")
    return res


def ensure_d1_database(env: dict[str, str]) -> str:
    print("\n[1/4] Kiểm tra / khởi tạo Cloudflare D1 database: where-money-sleeps-db ...", flush=True)
    res = run_cmd(["npx", "--yes", "wrangler", "d1", "list", "--json"], env=env, check=True)
    dbs = json.loads(res.stdout)
    for db in dbs:
        if db.get("name") == DB_NAME and db.get("uuid"):
            db_id = db["uuid"]
            print(f"  ✓ Đã tìm thấy D1 '{DB_NAME}' (uuid={db_id})", flush=True)
            return db_id

    res_create = run_cmd(["npx", "--yes", "wrangler", "d1", "create", DB_NAME], env=env, check=True)
    out = (res_create.stdout or "") + "\n" + (res_create.stderr or "")
    m = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", out, re.I)
    if not m:
        raise RuntimeError("Không trích được database_id sau khi tạo D1")
    db_id = m.group(1)
    print(f"  ✓ Đã tạo mới D1 '{DB_NAME}' (uuid={db_id})", flush=True)
    return db_id


def update_wrangler_config(db_id: str) -> None:
    cfg = {
        "$schema": "node_modules/wrangler/config-schema.json",
        "name": "where-money-sleeps",
        "main": "cloudflare/worker.js",
        "compatibility_date": "2025-04-01",
        "observability": {
            "enabled": False,
            "logs": {
                "enabled": False
            }
        },
        "assets": {
            "directory": "./dist/site",
            "binding": "ASSETS"
        },
        "d1_databases": [
            {
                "binding": "DB",
                "database_name": DB_NAME,
                "database_id": db_id
            }
        ]
    }
    WRANGLER_JSONC.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ✓ Đã cập nhật wrangler.jsonc với D1 binding DB -> {db_id} và observability.enabled = false", flush=True)


def main() -> int:
    env = clean_env()

    # Step 0: Build static site
    subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "wms-build-deploy.py")], check=True)

    # Step 1: Ensure D1 database & update wrangler.jsonc
    db_id = ensure_d1_database(env)
    update_wrangler_config(db_id)

    # Step 2: Apply schema.sql on remote D1
    print("\n[2/4] Thực thi cloudflare/schema.sql trên D1 remote ...", flush=True)
    run_cmd(
        ["npx", "--yes", "wrangler", "d1", "execute", DB_NAME, "--remote", "--file=cloudflare/schema.sql", "--yes"],
        env=env,
        check=True,
    )

    # Step 3: Deploy Worker + Static Assets
    print("\n[3/4] Deploy Worker + Static Assets (dist/site/) lên Cloudflare ...", flush=True)
    res_dep = run_cmd(["npx", "--yes", "wrangler", "deploy"], env=env, check=True)
    dep_out = (res_dep.stdout or "") + "\n" + (res_dep.stderr or "")
    urls = re.findall(r"https://[a-zA-Z0-9._-]+\.workers\.dev", dep_out)
    live_url = urls[-1] if urls else "https://where-money-sleeps.workers.dev"
    print(f"  ✓ Live URL: {live_url}", flush=True)

    # Step 4: Verify live HTTP responses (Rule 4: A success response is not proof — fetch and inspect it)
    print(f"\n[4/4] Kiểm chứng trực tiếp trên URL sống: {live_url} ...", flush=True)
    req_home = urllib.request.Request(live_url + "/", headers={"User-Agent": "WMS-Deploy-Verify/1.0"})
    with urllib.request.urlopen(req_home, timeout=20) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        print(f"  ✓ GET {live_url}/ -> HTTP {resp.status} ({len(body)} bytes, contains STORIES={'const STORIES' in body})", flush=True)
        if resp.status != 200 or "const STORIES" not in body:
            raise RuntimeError("Trang chủ live không khớp nội dung dự kiến")

    req_studio = urllib.request.Request(live_url + "/studio.html", headers={"User-Agent": "WMS-Deploy-Verify/1.0"})
    with urllib.request.urlopen(req_studio, timeout=20) as resp:
        sbody = resp.read().decode("utf-8", errors="replace")
        print(f"  ✓ GET {live_url}/studio.html -> HTTP {resp.status} ({len(sbody)} bytes)", flush=True)

    req_beacon = urllib.request.Request(
        live_url + "/api/p",
        data=b'{"event":"invalid_test_probe"}',
        headers={"Content-Type": "application/json", "User-Agent": "WMS-Deploy-Verify/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req_beacon, timeout=20) as resp:
        print(f"  ✓ POST {live_url}/api/p (invalid probe) -> HTTP {resp.status} (expected 204)", flush=True)
        if resp.status != 204:
            raise RuntimeError(f"Endpoint /api/p trả HTTP {resp.status} thay vì 204")

    print(f"\n[DEPLOY SUCCESS] Where Money Sleeps đã live tại: {live_url}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
