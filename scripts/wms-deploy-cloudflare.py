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

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRANGLER_JSONC = ROOT / "wrangler.jsonc"
ENV_FILE = ROOT / ".env"
DB_NAME = "where-money-sleeps-db"
DEFAULT_ACCOUNT_ID = "76cf12a5975b729026f1b1dd89005e53"
ANALYTICS_READ_TOKEN_ID = "81ce5a97dba02acd40d4e69071bad396"
DEFAULT_CUSTOM_DOMAIN = "https://wheremoneysleeps.duyslab.icu"
GITHUB_REPO = "duypham9895/where-money-sleeps"


def load_dotenv_token() -> tuple[str, str]:
    """Đọc `WMS_CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_API_TOKEN` và `CLOUDFLARE_ACCOUNT_ID` từ `.env` (nếu có)."""
    vals: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            vals[k.strip()] = v.strip().strip('"').strip("'")
    tok = vals.get("WMS_CLOUDFLARE_API_TOKEN") or vals.get("CLOUDFLARE_API_TOKEN") or ""
    acct = vals.get("CLOUDFLARE_ACCOUNT_ID") or os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip() or DEFAULT_ACCOUNT_ID
    return tok.strip(), acct.strip()


def is_analytics_read_only_token(tok: str, account_id: str) -> bool:
    """Kiểm tra xem token hiện tại có phải token chỉ-đọc `analytics-read` (`81ce5a97dba02acd40d4e69071bad396`) hay không."""
    if not tok:
        return False
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/tokens/verify",
        headers={"Authorization": f"Bearer {tok}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        tok_id = str((data.get("result") or {}).get("id") or "").strip()
        return tok_id == ANALYTICS_READ_TOKEN_ID
    except Exception:
        return False


def sync_github_secret(token: str, account_id: str) -> None:
    """Đồng bộ `CLOUDFLARE_API_TOKEN` và `CLOUDFLARE_ACCOUNT_ID` lên GitHub Actions Secrets qua stdin (không in secret)."""
    if not token:
        raise RuntimeError("Thiếu token Cloudflare để đồng bộ lên GitHub Actions Secrets")
    subprocess.run(
        ["gh", "secret", "set", "CLOUDFLARE_API_TOKEN", "--repo", GITHUB_REPO],
        input=token,
        text=True,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["gh", "secret", "set", "CLOUDFLARE_ACCOUNT_ID", "--repo", GITHUB_REPO],
        input=account_id,
        text=True,
        check=True,
        capture_output=True,
    )
    print(f"  ✓ Đã đồng bộ GitHub Secrets (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`) cho {GITHUB_REPO}", flush=True)


def clean_env() -> tuple[dict[str, str], bool]:
    """Chuẩn hoá môi trường deploy: ưu tiên `.env` -> shell write token -> OAuth Wrangler."""
    env = dict(os.environ)
    dotenv_token, account_id = load_dotenv_token()
    env["CLOUDFLARE_ACCOUNT_ID"] = account_id
    if dotenv_token:
        env["CLOUDFLARE_API_TOKEN"] = dotenv_token
        env.pop("CF_API_TOKEN", None)
        print("  ✓ Đang dùng CLOUDFLARE_API_TOKEN từ .env", flush=True)
        return env, True

    shell_tok = env.get("CLOUDFLARE_API_TOKEN", "").strip()
    if shell_tok and is_analytics_read_only_token(shell_tok, account_id):
        env.pop("CLOUDFLARE_API_TOKEN", None)
        env.pop("CF_API_TOKEN", None)
        print("  ℹ Gỡ CLOUDFLARE_API_TOKEN chỉ-đọc (analytics-read) khỏi shell để dùng token deploy hoặc OAuth", flush=True)
        return env, False

    if shell_tok:
        print("  ✓ Đang dùng CLOUDFLARE_API_TOKEN từ shell env", flush=True)
        return env, False

    return env, False


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
    custom_host = DEFAULT_CUSTOM_DOMAIN.replace("https://", "").replace("http://", "").rstrip("/")
    cfg = {
        "$schema": "node_modules/wrangler/config-schema.json",
        "name": "where-money-sleeps",
        "main": "cloudflare/worker.js",
        "compatibility_date": "2025-04-01",
        "workers_dev": True,
        "routes": [
            {
                "pattern": custom_host,
                "custom_domain": True
            }
        ],
        "observability": {
            "enabled": False,
            "logs": {
                "enabled": False
            }
        },
        "assets": {
            "directory": "./dist/site",
            "binding": "ASSETS",
            "run_worker_first": ["/", "/index.html", "/prototype.html", "/api/*"],
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
    print(
        f"  ✓ Đã cập nhật wrangler.jsonc: workers_dev=true, route={custom_host}, D1 binding DB -> {db_id}",
        flush=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Deploy Where Money Sleeps lên Cloudflare Workers + D1")
    ap.add_argument(
        "--sync-github-secret",
        action="store_true",
        help="Đồng bộ CLOUDFLARE_API_TOKEN và CLOUDFLARE_ACCOUNT_ID lên GitHub Actions Secrets",
    )
    args = ap.parse_args()

    env, from_dotenv = clean_env()
    tok = env.get("CLOUDFLARE_API_TOKEN", "").strip()
    acct = env.get("CLOUDFLARE_ACCOUNT_ID", DEFAULT_ACCOUNT_ID).strip()

    if args.sync_github_secret:
        if not tok or is_analytics_read_only_token(tok, acct):
            raise RuntimeError(
                "Chưa có CLOUDFLARE_API_TOKEN có quyền ghi (Edit Cloudflare Workers + Account D1 Edit) "
                "trong .env hoặc shell để đồng bộ lên GitHub Actions Secrets."
            )
        sync_github_secret(tok, acct)
    elif from_dotenv and tok and not is_analytics_read_only_token(tok, acct):
        try:
            sync_github_secret(tok, acct)
        except Exception as exc:
            print(f"  [WARN] Không đồng bộ được GitHub Secret tự động ({exc}); vẫn tiếp tục deploy.", flush=True)

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
    verify_targets = [
        ("/", "const STORIES"),
        ("/prototype.html", "const STORIES"),
        ("/workflows.html", None),
        ("/studio.html", "WMS Review Studio"),
        ("/wms-studio-data.js", None),
        ("/duyslab-overview.html", None),
        ("/llm-quiz.html", None),
        ("/studio-mockups.html", None),
        ("/landing-detail-mockups.html", None),
        ("/mockup-option-a.html", None),
        ("/mockup-option-b.html", None),
        ("/s0.html", None),
        ("/s1.html", None),
        ("/s2.html", None),
        ("/s3.html", None),
        ("/s4.html", None),
        ("/s5.html", None),
        ("/s6.html", None),
        ("/gates/06-iterate/TRIAGE.md", None),
        ("/gates/06-iterate/READOUT.md", None),
        ("/public/audio/beats-manifest.json", None),
        ("/public/brand/card-fig-1.jpg", None),
        ("/legal/licences.json", None),
        ("/legal/tt99-phu-luc-ii.secondary.json", None),
        ("/dist/youtube/card-long-16x9.srt", None),
        ("/favicon.svg", None),
        ("/robots.txt", "Sitemap:"),
        ("/sitemap.xml", "wheremoneysleeps.duyslab.icu/?story=profitcash"),
    ]

    def _verify_origin(base_url: str) -> None:
        base = base_url.rstrip("/")
        print(f"\n[4/4] Kiểm chứng trực tiếp trên URL sống: {base} ...", flush=True)
        for path, marker in verify_targets:
            req = urllib.request.Request(base + path, headers={"User-Agent": "WMS-Deploy-Verify/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read()
                if resp.status != 200 or not raw:
                    raise RuntimeError(f"GET {base}{path} trả HTTP {resp.status} ({len(raw)} bytes)")
                if marker is not None:
                    text = raw.decode("utf-8", errors="replace")
                    if marker not in text:
                        raise RuntimeError(f"GET {base}{path} thiếu nội dung kỳ vọng: {marker!r}")
                print(f"  ✓ GET {base}{path} -> HTTP {resp.status} ({len(raw)} bytes)", flush=True)

        req_beacon = urllib.request.Request(
            base + "/api/p",
            data=b'{"event":"invalid_test_probe"}',
            headers={"Content-Type": "application/json", "User-Agent": "WMS-Deploy-Verify/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req_beacon, timeout=20) as resp:
            print(f"  ✓ POST {base}/api/p (invalid probe) -> HTTP {resp.status} (expected 204)", flush=True)
            if resp.status != 204:
                raise RuntimeError(f"Endpoint {base}/api/p trả HTTP {resp.status} thay vì 204")

    _verify_origin(live_url)
    if DEFAULT_CUSTOM_DOMAIN.rstrip("/") != live_url.rstrip("/"):
        _verify_origin(DEFAULT_CUSTOM_DOMAIN)

    print(f"\n[DEPLOY SUCCESS] Where Money Sleeps đã live tại: {DEFAULT_CUSTOM_DOMAIN} ({live_url})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
