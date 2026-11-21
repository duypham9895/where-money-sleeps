#!/usr/bin/env python3
# wms-hook-guard.sh — PreToolUse hook cho Gemini / Antigravity (& Claude Code), NẰM TRONG repo where-money-sleeps.
#
# Khoá LUẬT 12 (QĐ 64 — cấm push thẳng main / --no-verify / core.hooksPath), cổng duyệt bài WMS-R4 / QĐ 56,
# và cổng con trỏ PIPELINE.md — kèm ngoại lệ hẹp cho nhánh daily automation (`content/daily-YYYY-MM-DD`).

from __future__ import annotations

import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _clean_git_env() -> dict[str, str]:
    return {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GIT_") and k not in ("GH_REPO", "SSH_ASKPASS")
    }


def _resolve_common_git_dir() -> pathlib.Path:
    res = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=False,
        env=_clean_git_env(),
    )
    if res.returncode == 0 and res.stdout.strip():
        raw = pathlib.Path(res.stdout.strip())
        return raw.resolve() if raw.is_absolute() else (REPO_ROOT / raw).resolve()
    return (REPO_ROOT / ".git").resolve()


WMS_COMMON_GIT_DIR = _resolve_common_git_dir()
WMS_ORIGIN_RE = re.compile(
    r"^(?:git@github\.com:|https://github\.com/|ssh://git@github\.com/)duypham9895/where-money-sleeps(?:\.git)?$",
    re.IGNORECASE,
)
WMS_REPO_SLUG = "duypham9895/where-money-sleeps"
WMS_DAILY_BRANCH_RE = re.compile(r"^content/daily-\d{4}-\d{2}-\d{2}$")
CONFIG_BLOCK_RE = r"^(remote\.origin\.(push|pushurl)|push\.|url\.|core\.sshcommand)"

MAIN_BRANCHES = {"main", "master", "refs/heads/main", "refs/heads/master"}
MAIN_REFS = MAIN_BRANCHES | {"HEAD:main", "HEAD:master"}
GIT_OPTS_WITH_VAL = {"-C", "-c", "--config-env", "--exec-path", "--git-dir", "--work-tree", "--namespace", "--super-prefix"}
GIT_CONFIG_OVERRIDE_FLAGS = {"-c", "--config-env", "--exec-path", "--namespace", "--super-prefix"}
ENV_OPTS_WITH_VAL = {"-u", "--unset", "-C", "--chdir", "-P", "--argv0", "-S", "--split-string"}
NPX_NO_ARG_FLAGS = {"--yes", "-y", "--no", "--quiet", "-q", "--offline", "--prefer-offline", "--ignore-existing"}
PUSH_OPTS_WITH_VAL = {"--repo", "-o", "--push-option", "--receive-pack", "--exec", "--signed"}
ALLOWED_DAILY_PUSH_LONG = {"--set-upstream", "--quiet", "--verbose", "--progress", "--porcelain", "--dry-run"}
ALLOWED_DAILY_PUSH_SHORT = set("uqv")
UNSAFE_DAILY_ENV_RE = re.compile(r"^(?:GIT_|GH_|SSH)", re.IGNORECASE)
SAFE_DAILY_TOOLS = {
    "git", "gh", "cd", "sh", "bash", "zsh", "eval", "export", "declare", "typeset",
    "local", "readonly", "unset", "true", "false", "test", "[", "pwd", "ls", "which",
    "dirname", "basename", "grep", "rg", "egrep", "fgrep", "echo", "cat", "head", "tail",
}
SAFE_DAILY_GIT_SUBS = {"status", "rev-parse", "symbolic-ref", "show-ref", "diff", "log", "add", "commit", "checkout", "switch", "fetch", "push"}
SHELL_BINS = {"sh", "bash", "zsh", "dash", "ksh"}
READONLY_SEARCH_CMDS = {"grep", "rg", "egrep", "fgrep"}

GH_PR_CREATE_VAL_LONG = {
    "--assignee", "--base", "--body", "--body-file", "--head", "--label",
    "--milestone", "--project", "--recover", "--reviewer", "--template", "--title", "--repo",
}
GH_PR_CREATE_VAL_SHORT = {"a", "B", "b", "F", "H", "l", "m", "p", "r", "T", "t", "R"}
GH_PR_MERGE_VAL_LONG = {"--author-email", "--body", "--body-file", "--match-head-commit", "--subject", "--repo"}
GH_PR_MERGE_VAL_SHORT = {"A", "b", "F", "t", "R"}
GH_GLOBAL_VAL_FLAGS = {"-R", "--repo"}

SHIP_OTHER = {"vercel", "netlify", "wrangler", "youtube-upload", "yt-upload", "wms-youtube-upload"}
PIPELINE_UPLOAD_FLAGS = {"--upload-short", "--upload-long"}

APPROVED = re.compile(r"""["'`]?approvedBy["'`]?\s*[:=]\s*(["'`])(.*?)\1""")
PUBLISHED = re.compile(r"""["'`]?status["'`]?\s*[:=]\s*["'`]published["'`]""")
UPLOADED_PUBLIC = re.compile(r"""["'`]?embedStatus["'`]?\s*[:=]\s*["'`]uploaded_public["'`]""")
APPROVE_LINE = re.compile(r"\b(?:APPROVE|DUYỆT)\s+S[0-6]\b")
POINTER = re.compile(r"^pointer:\s*(\S+)", re.M)

PATH_KEYS = ("Path", "TargetFile", "AbsolutePath", "File", "path", "file_path")
NEW_KEYS = ("Replacement", "Content", "CodeContent", "ReplacementContent", "content", "new_string")
OLD_KEYS = ("Target", "TargetContent", "old_string")
CHUNK_KEYS = ("ReplacementChunks", "Chunks", "edits")
WRITE_TOOLS = {
    "edit_file", "write_file", "write_to_file", "replace_file_content",
    "multi_replace_file_content", "Edit", "Write", "MultiEdit",
}
IS_CLAUDE = False


def out(decision: str, reason: str = "") -> None:
    if IS_CLAUDE:
        if decision == "allow":
            sys.exit(0)
        mapped = "deny" if decision == "deny" else "ask"
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": mapped,
                        "permissionDecisionReason": reason,
                    }
                },
                ensure_ascii=False,
            )
        )
        sys.exit(0)
    d = {"decision": decision}
    if reason:
        d["reason"] = reason
    print(json.dumps(d, ensure_ascii=False))
    sys.exit(0)


def _strip_js_comments(text: str) -> str:
    """Loại // và /* ... */ ngoài chuỗi để tránh lách regex kiểu approvedBy: /*x*/ \"Duy\"."""
    out_chars: list[str] = []
    i = 0
    n = len(text)
    in_str: str | None = None
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_str is not None:
            out_chars.append(ch)
            if ch == "\\" and i + 1 < n:
                out_chars.append(nxt)
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ('"', "'", "`"):
            in_str = ch
            out_chars.append(ch)
            i += 1
            continue
        if ch == "/" and nxt == "*":
            end = text.find("*/", i + 2)
            out_chars.append(" ")
            i = n if end == -1 else end + 2
            continue
        if ch == "/" and nxt == "/":
            nl = text.find("\n", i + 2)
            i = n if nl == -1 else nl
            continue
        out_chars.append(ch)
        i += 1
    return "".join(out_chars)


def _norm_scan(text: str) -> str:
    return _strip_js_comments(text)


def approved_count(text: str) -> int:
    norm = _norm_scan(text)
    return sum(1 for m in APPROVED.finditer(norm) if m.group(2).strip() and "demo" not in m.group(2).lower())


def non_auto_approved_count(text: str) -> int:
    norm = _norm_scan(text)
    return sum(
        1
        for m in APPROVED.finditer(norm)
        if m.group(2).strip() and "demo" not in m.group(2).lower() and m.group(2).strip() != "auto-daily"
    )


def published_count(text: str) -> int:
    return len(PUBLISHED.findall(_norm_scan(text)))


def uploaded_public_count(text: str) -> int:
    return len(UPLOADED_PUBLIC.findall(_norm_scan(text)))


def extract_edit_pairs(args: dict) -> tuple[str, str, list[tuple[str, str]]]:
    pairs: list[tuple[str, str]] = []
    new_top = [args[k] for k in NEW_KEYS if isinstance(args.get(k), str)]
    old_top = [args[k] for k in OLD_KEYS if isinstance(args.get(k), str)]
    if new_top or old_top:
        pairs.append(("\n".join(new_top), "\n".join(old_top)))
    all_new = list(new_top)
    all_old = list(old_top)
    for ck in CHUNK_KEYS:
        for ch in args.get(ck) or []:
            if isinstance(ch, dict):
                cn = "\n".join(ch[k] for k in NEW_KEYS if isinstance(ch.get(k), str))
                co = "\n".join(ch[k] for k in OLD_KEYS if isinstance(ch.get(k), str))
                pairs.append((cn, co))
                if cn:
                    all_new.append(cn)
                if co:
                    all_old.append(co)
    return "\n".join(all_new), "\n".join(all_old), pairs


def _run_git(cwd: pathlib.Path, *args: str, git_dir: str | None = None, work_tree: str | None = None) -> subprocess.CompletedProcess:
    cmd = ["git", "-C", str(cwd)]
    if git_dir:
        cmd.extend(["--git-dir", git_dir])
    if work_tree:
        cmd.extend(["--work-tree", work_tree])
    cmd.extend(args)
    return subprocess.run(cmd, capture_output=True, text=True, check=False, env=_clean_git_env())


def _is_wms_repo(cwd: pathlib.Path, git_dir: str | None = None, work_tree: str | None = None) -> bool:
    if not cwd.exists():
        return False
    res_cd = _run_git(cwd, "rev-parse", "--git-common-dir", git_dir=git_dir, work_tree=work_tree)
    if res_cd.returncode != 0 or not res_cd.stdout.strip():
        return False
    cd_raw = pathlib.Path(res_cd.stdout.strip())
    cd_resolved = cd_raw.resolve() if cd_raw.is_absolute() else (cwd / cd_raw).resolve()
    if cd_resolved != WMS_COMMON_GIT_DIR:
        return False
    for uargs in (("remote", "get-url", "origin"), ("remote", "get-url", "--push", "origin")):
        res_u = _run_git(cwd, *uargs, git_dir=git_dir, work_tree=work_tree)
        if res_u.returncode != 0 or not WMS_ORIGIN_RE.match(res_u.stdout.strip()):
            return False
    res_cfg = _run_git(cwd, "config", "--get-regexp", CONFIG_BLOCK_RE, git_dir=git_dir, work_tree=work_tree)
    if res_cfg.returncode not in (0, 1) or (res_cfg.returncode == 0 and res_cfg.stdout.strip()):
        return False
    return True


def _repo_state(cwd: pathlib.Path, git_dir: str | None = None, work_tree: str | None = None) -> tuple[str, str]:
    if not cwd.exists():
        return str(cwd.resolve()), ""
    res_top = _run_git(cwd, "rev-parse", "--show-toplevel", git_dir=git_dir, work_tree=work_tree)
    repo_key = str(pathlib.Path(res_top.stdout.strip()).resolve()) if (res_top.returncode == 0 and res_top.stdout.strip()) else (git_dir or str(cwd.resolve()))
    res_br = _run_git(cwd, "symbolic-ref", "--quiet", "--short", "HEAD", git_dir=git_dir, work_tree=work_tree)
    return repo_key, (res_br.stdout.strip() if res_br.returncode == 0 else "")


def _is_verified_daily_dir(cwd: pathlib.Path, git_dir: str | None = None, work_tree: str | None = None) -> tuple[bool, str]:
    if not _is_wms_repo(cwd, git_dir, work_tree):
        return False, ""
    _, br = _repo_state(cwd, git_dir, work_tree)
    return bool(WMS_DAILY_BRANCH_RE.match(br)), br


def _tokenize(seg: str) -> list[str]:
    try:
        return shlex.split(seg, posix=True)
    except ValueError:
        return seg.split()


def _has_env_override(tokens: list[str]) -> bool:
    for t in tokens:
        if t in ("-S", "--split-string", "-i", "--ignore-environment", "-u", "--unset", "-C", "--chdir", "-P", "--argv0"):
            return True
        if t.startswith(("-S", "--split-string=", "-u", "--unset=", "-C", "--chdir=", "-P")):
            return True
        if t.startswith("-") and not t.startswith("--") and any(c in "SiCuP" for c in t[1:]):
            return True
        if "=" in t and UNSAFE_DAILY_ENV_RE.match(t.split("=", 1)[0]):
            return True
    return False


def _strip_wrappers_ext(tokens: list[str]) -> tuple[list[str], bool]:
    i = 0
    n = len(tokens)
    env_override = False
    while i < n:
        tok = tokens[i]
        if tok in ("(", ")", "{", "}", "!", "then", "do", "else"):
            i += 1
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tok):
            if UNSAFE_DAILY_ENV_RE.match(tok.split("=", 1)[0]):
                env_override = True
            i += 1
            continue
        base = pathlib.PurePosixPath(tok).name
        if base in ("rtk", "proxy", "nohup"):
            i += 1
            continue
        if base in ("command", "time"):
            i += 1
            while i < n and tokens[i].startswith("-") and tokens[i] != "--":
                i += 1
            if i < n and tokens[i] == "--":
                i += 1
            continue
        if base == "env":
            i += 1
            while i < n:
                t = tokens[i]
                if t == "--":
                    i += 1
                    break
                if "=" in t and not t.startswith("-"):
                    if UNSAFE_DAILY_ENV_RE.match(t.split("=", 1)[0]):
                        env_override = True
                    i += 1
                    continue
                if t in ("-i", "--ignore-environment") or (t.startswith("-") and not t.startswith("--") and any(c in "SiCuP" for c in t[1:])):
                    env_override = True
                if t in ENV_OPTS_WITH_VAL:
                    env_override = True
                    if t in ("-S", "--split-string") and i + 1 < n:
                        inner = _tokenize(tokens[i + 1])
                        sub_core, sub_ov = _strip_wrappers_ext(inner + tokens[i + 2 :])
                        return sub_core, env_override or sub_ov
                    i += 2
                    continue
                if t.startswith(("--split-string=", "-S")):
                    env_override = True
                    val = t.split("=", 1)[1] if "=" in t else t[2:]
                    sub_core, sub_ov = _strip_wrappers_ext(_tokenize(val) + tokens[i + 1 :])
                    return sub_core, env_override or sub_ov
                if t.startswith("-") and not t.startswith("--") and "S" in t[1:]:
                    env_override = True
                    idx_s = t.find("S", 1)
                    rem = t[idx_s + 1 :]
                    if rem:
                        sub_core, sub_ov = _strip_wrappers_ext(_tokenize(rem) + tokens[i + 1 :])
                        return sub_core, env_override or sub_ov
                    if i + 1 < n:
                        sub_core, sub_ov = _strip_wrappers_ext(_tokenize(tokens[i + 1]) + tokens[i + 2 :])
                        return sub_core, env_override or sub_ov
                    i += 1
                    continue
                if t.startswith(("--chdir=", "--unset=", "--argv0=")) or (
                    t.startswith("-") and not t.startswith("--") and any(t.startswith(f"-{f}") and len(t) > 2 for f in ("u", "C", "P"))
                ):
                    env_override = True
                    i += 1
                    continue
                if t.startswith("-"):
                    i += 1
                    continue
                break
            continue
        if base in ("npx", "bunx"):
            i += 1
            while i < n and tokens[i].startswith("-"):
                if tokens[i] == "--":
                    i += 1
                    break
                i += 1 if (tokens[i] in NPX_NO_ARG_FLAGS or "=" in tokens[i]) else 2
            continue
        if base in ("pnpm", "yarn"):
            j = i + 1
            while j < n and tokens[j].startswith("-"):
                j += 1
            if j < n and tokens[j] == "dlx":
                i = j + 1
                while i < n and tokens[i].startswith("-"):
                    if tokens[i] == "--":
                        i += 1
                        break
                    i += 1
                continue
        break
    return tokens[i:], env_override


def _strip_wrappers(tokens: list[str]) -> list[str]:
    return _strip_wrappers_ext(tokens)[0]


def _norm_cmd(tok: str) -> str:
    return re.sub(r"@[^@/\s]+$", "", pathlib.PurePosixPath(tok).name)


def _extract_shell_c_script(core: list[str]) -> str | None:
    if not core or _norm_cmd(core[0]) not in SHELL_BINS:
        return None
    i = 1
    found_c = False
    while i < len(core):
        t = core[i]
        if t == "--":
            i += 1
            return core[i] if (found_c and i < len(core)) else None
        if t in ("-o", "+o") or (t.startswith("-") and not t.startswith("--") and t.endswith("o")):
            if t.startswith("-") and "c" in t[1:]:
                found_c = True
            i += 2
            continue
        if t.startswith("--"):
            i += 1
            continue
        if t.startswith(("+", "-")):
            if t.startswith("-") and "c" in t[1:]:
                found_c = True
            i += 1
            continue
        return t if found_c else None
    return None


def _parse_git(core: list[str], cwd: pathlib.Path) -> dict:
    if not core or _norm_cmd(core[0]) != "git":
        return {"is_git": False}
    git_cwd = cwd
    git_dir_arg = None
    work_tree_arg = None
    c_configs: list[str] = []
    has_config_override = False
    i = 1
    while i < len(core):
        tok = core[i]
        if tok in GIT_OPTS_WITH_VAL:
            val = core[i + 1] if i + 1 < len(core) else ""
            if tok == "-C" and val:
                git_cwd = (git_cwd / val).resolve()
            elif tok in GIT_CONFIG_OVERRIDE_FLAGS:
                has_config_override = True
                if tok == "-c" and val:
                    c_configs.append(val)
                elif tok == "--config-env" and val:
                    c_configs.append(val)
            elif tok == "--git-dir" and val:
                git_dir_arg = str((git_cwd / val).resolve())
            elif tok == "--work-tree" and val:
                work_tree_arg = str((git_cwd / val).resolve())
            i += 2
            continue
        if tok.startswith("-C") and len(tok) > 2:
            git_cwd = (git_cwd / tok[2:]).resolve()
            i += 1
            continue
        if tok.startswith("-c") and len(tok) > 2:
            has_config_override = True
            c_configs.append(tok[2:])
            i += 1
            continue
        if "=" in tok and tok.split("=", 1)[0] in GIT_OPTS_WITH_VAL:
            flag, val = tok.split("=", 1)
            if flag in GIT_CONFIG_OVERRIDE_FLAGS:
                has_config_override = True
                if flag in ("-c", "--config-env"):
                    c_configs.append(val)
            elif flag == "--git-dir":
                git_dir_arg = str((git_cwd / val).resolve())
            elif flag == "--work-tree":
                work_tree_arg = str((git_cwd / val).resolve())
            i += 1
            continue
        if tok.startswith("-"):
            i += 1
            continue
        return {
            "is_git": True, "git_cwd": git_cwd, "git_dir_arg": git_dir_arg, "work_tree_arg": work_tree_arg,
            "c_configs": c_configs, "has_config_override": has_config_override, "sub": tok, "rest": core[i + 1 :],
        }
    return {
        "is_git": True, "git_cwd": git_cwd, "git_dir_arg": git_dir_arg, "work_tree_arg": work_tree_arg,
        "c_configs": c_configs, "has_config_override": has_config_override, "sub": "", "rest": [],
    }


def _split_shell_events(cmd: str) -> list[tuple[str, str, list[str], str]]:
    """Tách sự kiện đóng/mở ( ), { } và pipeline ngoài chuỗi/heredoc."""
    events: list[tuple[str, str, list[str], str]] = []
    buf: list[str] = []
    stages: list[str] = []
    group_stack: list[str] = []
    in_sq = in_dq = esc = False
    heredoc_delim: str | None = None
    pipe_start = 0
    i = 0
    n = len(cmd)

    def flush_stage() -> None:
        s = "".join(buf).strip()
        buf.clear()
        if s:
            stages.append(s)

    def flush_pipe(end_idx: int, sep: str) -> None:
        nonlocal pipe_start
        flush_stage()
        if stages or sep:
            events.append(("pipe", cmd[pipe_start:end_idx], list(stages), sep))
            stages.clear()
        pipe_start = end_idx

    while i < n:
        ch = cmd[i]
        if heredoc_delim is not None:
            nl = cmd.find("\n", i)
            line = cmd[i:] if nl == -1 else cmd[i:nl]
            buf.append(line + ("\n" if nl != -1 else ""))
            if line.strip() == heredoc_delim:
                heredoc_delim = None
                end_idx = n if nl == -1 else nl + 1
                flush_pipe(end_idx, "\n")
                i = end_idx
                continue
            if nl == -1:
                break
            i = nl + 1
            continue
        if esc:
            buf.append(ch)
            esc = False
            i += 1
            continue
        if ch == "\\" and not in_sq:
            buf.append(ch)
            esc = True
            i += 1
            continue
        if ch == "'" and not in_dq:
            in_sq = not in_sq
            buf.append(ch)
            i += 1
            continue
        if ch == '"' and not in_sq:
            in_dq = not in_dq
            buf.append(ch)
            i += 1
            continue
        if not in_sq and not in_dq:
            if not "".join(buf).strip() and ch in ("(", "{"):
                group_stack.append(ch)
                events.append(("open", ch, [], ""))
                i += 1
                pipe_start = i
                continue
            if group_stack and ch in (")", "}"):
                flush_pipe(i, "")
                group_stack.pop()
                events.append(("close", ch, [], ""))
                i += 1
                pipe_start = i
                continue
            if cmd[i : i + 2] in ("&&", "||"):
                sep = cmd[i : i + 2]
                flush_pipe(i, sep)
                i += 2
                pipe_start = i
                continue
            if ch in (";", "\n"):
                cur_line = cmd[pipe_start:i].rsplit("\n", 1)[-1]
                m_hd = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", cur_line)
                if ch == "\n" and m_hd:
                    heredoc_delim = m_hd.group(1)
                    buf.append(ch)
                    i += 1
                    continue
                flush_pipe(i, ch)
                i += 1
                pipe_start = i
                continue
            if ch == "|":
                flush_stage()
                i += 1
                continue
        buf.append(ch)
        i += 1
    flush_pipe(n, "")
    return events


def _extract_substitutions(cmd: str) -> list[str]:
    """Quét $(...) và backtick ngoài chuỗi nháy đơn và heredoc, tôn trọng dấu nháy bên trong."""
    subs: list[str] = []
    in_sq = in_dq = esc = False
    heredoc_delim: str | None = None
    i = 0
    line_start = 0
    n = len(cmd)
    while i < n:
        ch = cmd[i]
        if heredoc_delim is not None:
            nl = cmd.find("\n", i)
            line = cmd[i:] if nl == -1 else cmd[i:nl]
            if line.strip() == heredoc_delim:
                heredoc_delim = None
            if nl == -1:
                break
            i = nl + 1
            line_start = i
            continue
        if esc:
            esc = False
            i += 1
            continue
        if ch == "\\" and not in_sq:
            esc = True
            i += 1
            continue
        if ch == "'" and not in_dq:
            in_sq = not in_sq
            i += 1
            continue
        if ch == '"' and not in_sq:
            in_dq = not in_dq
            i += 1
            continue
        if ch == "\n" and not in_sq and not in_dq:
            m_hd = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", cmd[line_start:i])
            if m_hd:
                heredoc_delim = m_hd.group(1)
            line_start = i + 1
            i += 1
            continue
        if not in_sq and cmd[i : i + 2] == "$(":
            j = i + 2
            depth = 1
            sub_sq = sub_dq = sub_esc = False
            while j < n and depth > 0:
                c2 = cmd[j]
                if sub_esc:
                    sub_esc = False
                elif c2 == "\\" and not sub_sq:
                    sub_esc = True
                elif c2 == "'" and not sub_dq:
                    sub_sq = not sub_sq
                elif c2 == '"' and not sub_sq:
                    sub_dq = not sub_dq
                elif not sub_sq and not sub_dq:
                    if c2 == "(":
                        depth += 1
                    elif c2 == ")":
                        depth -= 1
                        if depth == 0:
                            break
                j += 1
            if depth == 0:
                inner = cmd[i + 2 : j].strip()
                if inner:
                    subs.append(inner)
                i = j + 1
                continue
        if not in_sq and ch == "`":
            j = i + 1
            sub_esc = False
            while j < n:
                c2 = cmd[j]
                if sub_esc:
                    sub_esc = False
                elif c2 == "\\":
                    sub_esc = True
                elif c2 == "`":
                    break
                j += 1
            if j < n:
                inner = cmd[i + 1 : j].strip()
                if inner:
                    subs.append(inner)
                i = j + 1
                continue
        i += 1
    return subs


def _pipe_has_unsafe_redir(pipe_text: str) -> bool:
    in_sq = in_dq = esc = False
    i = 0
    n = len(pipe_text)
    while i < n:
        ch = pipe_text[i]
        if esc:
            esc = False
            i += 1
            continue
        if ch == "\\" and not in_sq:
            esc = True
            i += 1
            continue
        if ch == "'" and not in_dq:
            in_sq = not in_sq
        elif ch == '"' and not in_sq:
            in_dq = not in_dq
        elif not in_sq and not in_dq:
            if pipe_text[i : i + 2] == "&&":
                i += 2
                continue
            if ch == "&" and pipe_text[i : i + 2] != "&>":
                return True
            if ch == ">":
                j = i + 1
                while j < n and pipe_text[j] in (">", "|", " "):
                    j += 1
                k = j
                while k < n and not pipe_text[k].isspace() and pipe_text[k] not in (";", "|", "&", ">"):
                    k += 1
                if pipe_text[j:k] not in ("&1", "&2", "/dev/null"):
                    return True
                i = k
                continue
        i += 1
    return False


def _pos_args(rest: list[str], opts_val: set[str]) -> list[str]:
    out_pos: list[str] = []
    after_dd = False
    i = 0
    while i < len(rest):
        t = rest[i]
        if t == "--" and not after_dd:
            after_dd = True
            i += 1
            continue
        if not after_dd and t.startswith("-"):
            if t in opts_val:
                i += 2
                continue
            i += 1
            continue
        out_pos.append(t)
        i += 1
    return out_pos


def _parse_pflag_args(rest: list[str], val_long: set[str], val_short: set[str]) -> tuple[dict[str, list[str]], set[str], set[str], list[str], bool]:
    opt_vals: dict[str, list[str]] = {}
    enabled: set[str] = set()
    seen_long: set[str] = set()
    pos: list[str] = []
    after_dd = False
    i = 0
    while i < len(rest):
        tok = rest[i]
        if tok == "--" and not after_dd:
            after_dd = True
            i += 1
            continue
        if not after_dd and tok.startswith("--"):
            if "=" in tok:
                flag, val = tok.split("=", 1)
                seen_long.add(flag)
                if flag in val_long:
                    opt_vals.setdefault(flag, []).append(val)
                elif val.lower() in ("1", "t", "true"):
                    enabled.add(flag)
                elif val.lower() in ("0", "f", "false"):
                    enabled.discard(flag)
                else:
                    return opt_vals, enabled, seen_long, pos, True
            else:
                seen_long.add(tok)
                if tok in val_long:
                    if i + 1 >= len(rest):
                        return opt_vals, enabled, seen_long, pos, True
                    opt_vals.setdefault(tok, []).append(rest[i + 1])
                    i += 2
                    continue
                enabled.add(tok)
            i += 1
            continue
        if not after_dd and tok.startswith("-") and tok != "-":
            consumed = False
            for idx, ch in enumerate(tok[1:]):
                if ch in val_short:
                    rem = tok[idx + 2 :]
                    if rem:
                        opt_vals.setdefault(f"-{ch}", []).append(rem)
                    else:
                        if i + 1 >= len(rest):
                            return opt_vals, enabled, seen_long, pos, True
                        opt_vals.setdefault(f"-{ch}", []).append(rest[i + 1])
                        consumed = True
                    break
                enabled.add(f"-{ch}")
            i += 2 if consumed else 1
            continue
        pos.append(tok)
        i += 1
    return opt_vals, enabled, seen_long, pos, False


def _extract_gh_pr_sub(core: list[str]) -> tuple[str, str, list[str], list[str]]:
    """Parse `gh [global flags] pr [group flags] <subcmd> <rest>`, returning (group, sub, pr_extra_flags, rest)."""
    tokens = core[1:]
    pre_flags: list[str] = []
    i = 0
    group = ""
    while i < len(tokens):
        t = tokens[i]
        if t in GH_GLOBAL_VAL_FLAGS:
            if i + 1 < len(tokens):
                pre_flags.extend([t, tokens[i + 1]])
                i += 2
            else:
                pre_flags.append(t)
                i += 1
            continue
        if t.startswith("--repo="):
            pre_flags.append(t)
            i += 1
            continue
        if t.startswith("-R") and len(t) > 2:
            pre_flags.extend(["-R", t[2:]])
            i += 1
            continue
        if t.startswith("-"):
            i += 1
            continue
        group = t
        i += 1
        break
    if group != "pr":
        return group, "", pre_flags, tokens[i:]
    sub = ""
    while i < len(tokens):
        t = tokens[i]
        if t in GH_GLOBAL_VAL_FLAGS:
            if i + 1 < len(tokens):
                pre_flags.extend([t, tokens[i + 1]])
                i += 2
            else:
                pre_flags.append(t)
                i += 1
            continue
        if t.startswith("--repo="):
            pre_flags.append(t)
            i += 1
            continue
        if t.startswith("-R") and len(t) > 2:
            pre_flags.extend(["-R", t[2:]])
            i += 1
            continue
        if t.startswith("-"):
            i += 1
            continue
        sub = t
        i += 1
        break
    return group, sub, pre_flags, tokens[i:]


def _normalize_gh_repo(raw: str) -> str:
    s = raw.strip().lower()
    for pfx in ("https://github.com/", "http://github.com/", "github.com/"):
        if s.startswith(pfx):
            s = s[len(pfx) :]
            break
    s = s.rstrip("/")
    return s[:-4] if s.endswith(".git") else s


def _is_daily_push(g: dict, active_branch: str) -> bool:
    rest = g["rest"]
    pre_dd = rest[: rest.index("--")] if "--" in rest else rest
    for tok in pre_dd:
        if tok.startswith("--"):
            if tok not in ALLOWED_DAILY_PUSH_LONG:
                return False
        elif tok.startswith("-") and tok != "-":
            if not all(ch in ALLOWED_DAILY_PUSH_SHORT for ch in tok[1:]):
                return False
    ppos = _pos_args(rest, PUSH_OPTS_WITH_VAL)
    if len(ppos) != 2 or ppos[0] != "origin":
        return False
    refspec = ppos[1]
    if refspec.startswith("+") or "*" in refspec:
        return False
    if not _is_wms_repo(g["git_cwd"], g["git_dir_arg"], g["work_tree_arg"]):
        return False
    if not WMS_DAILY_BRANCH_RE.match(active_branch):
        return False
    allowed_src = {"HEAD", "@", active_branch, f"refs/heads/{active_branch}"}
    allowed_dst = {active_branch, f"refs/heads/{active_branch}"}
    if ":" in refspec:
        src, dst = refspec.split(":", 1)
        return src in allowed_src and dst in allowed_dst
    return refspec in allowed_dst


def _is_daily_gh_pr(sub: str, rest: list[str], cwd: pathlib.Path, trusted_daily: dict[str, str]) -> bool:
    if sub not in ("create", "merge") or not _is_wms_repo(cwd):
        return False
    repo_key, disk_br = _repo_state(cwd)
    active_br = trusted_daily.get(repo_key, disk_br)
    if sub == "create":
        opt_vals, _, _, pos, bad = _parse_pflag_args(rest, GH_PR_CREATE_VAL_LONG, GH_PR_CREATE_VAL_SHORT)
        if bad or pos:
            return False
        if any(_normalize_gh_repo(r) != WMS_REPO_SLUG for r in opt_vals.get("-R", []) + opt_vals.get("--repo", [])):
            return False
        if any(b != "main" for b in opt_vals.get("-B", []) + opt_vals.get("--base", [])):
            return False
        heads = opt_vals.get("-H", []) + opt_vals.get("--head", [])
        if heads:
            for h in heads:
                hb = h.split(":", 1)[1] if ":" in h else h
                if ":" in h and h.split(":", 1)[0].lower() != "duypham9895":
                    return False
                if not WMS_DAILY_BRANCH_RE.match(hb):
                    return False
            return True
        return bool(WMS_DAILY_BRANCH_RE.match(active_br))
    opt_vals, enabled, seen_long, pos, bad = _parse_pflag_args(rest, GH_PR_MERGE_VAL_LONG, GH_PR_MERGE_VAL_SHORT)
    if bad:
        return False
    if any(_normalize_gh_repo(r) != WMS_REPO_SLUG for r in opt_vals.get("-R", []) + opt_vals.get("--repo", [])):
        return False
    if "--auto" not in enabled or "--admin" in seen_long or "--disable-auto" in seen_long:
        return False
    if len(pos) == 0:
        return bool(WMS_DAILY_BRANCH_RE.match(active_br))
    if len(pos) == 1:
        return bool(WMS_DAILY_BRANCH_RE.match(pos[0]))
    return False


def _is_pipeline_upload_cmd(core: list[str]) -> bool:
    if "wms-media-pipeline.py" not in " ".join(core):
        return False
    if any(t in PIPELINE_UPLOAD_FLAGS for t in core):
        return True
    for idx, t in enumerate(core):
        if t in ("--privacy=public", "--embed-status=uploaded_public"):
            return True
        if t == "--privacy" and idx + 1 < len(core) and core[idx + 1] == "public":
            return True
        if t == "--embed-status" and idx + 1 < len(core) and core[idx + 1] == "uploaded_public":
            return True
    return False


def _inspect_run_command(
    cmd: str,
    cwd: pathlib.Path,
    pending_asks: list[str],
    depth: int = 0,
    sticky_unsafe_env: bool = False,
    trusted_daily: dict[str, str] | None = None,
    daily_tainted: bool = False,
) -> None:
    if depth > 4:
        pending_asks.append("CỔNG WMS: lồng lệnh quá sâu — hỏi Duy.")
        return
    if not cmd:
        return
    if trusted_daily is None:
        trusted_daily = {}
    subshell_stack: list[pathlib.Path] = []
    prev_sep = ""
    checkout_poisoned = False

    for sub in _extract_substitutions(cmd):
        _inspect_run_command(sub, cwd, pending_asks, depth + 1, sticky_unsafe_env, {}, daily_tainted)

    for ev_kind, pipe_text, stages, sep_after in _split_shell_events(cmd):
        if ev_kind == "open":
            trusted_daily.clear()
            if pipe_text == "(":
                subshell_stack.append(cwd)
            continue
        if ev_kind == "close":
            trusted_daily.clear()
            if pipe_text == ")" and subshell_stack:
                cwd = subshell_stack.pop()
            continue

        has_redir = _pipe_has_unsafe_redir(pipe_text)
        if has_redir:
            daily_tainted = True

        # Bảo vệ Gate 5 PIPELINE.md ngay cả qua shell redirection / heredoc
        if "PIPELINE.md" in pipe_text and "templates/app/PIPELINE.md" not in pipe_text:
            first_core = _strip_wrappers(_tokenize(stages[0])) if stages else []
            first_cmd = _norm_cmd(first_core[0]) if first_core else ""
            if not (first_cmd in READONLY_SEARCH_CMDS and not has_redir):
                if POINTER.search(pipe_text) or APPROVE_LINE.search(pipe_text):
                    pending_asks.append("CỔNG DUYỆT (Quy tắc 1): lệnh shell sửa pointer / ghi APPROVE vào PIPELINE.md. Chỉ Duy.")

        for seg in stages:
            raw_toks = _tokenize(seg)
            core, env_ov = _strip_wrappers_ext(raw_toks)
            if env_ov:
                sticky_unsafe_env = True
                daily_tainted = True
            if not core:
                continue

            cmd_name = _norm_cmd(core[0])
            if cmd_name not in SAFE_DAILY_TOOLS:
                daily_tainted = True
            if cmd_name in ("source", "."):
                sticky_unsafe_env = True
                daily_tainted = True
            elif cmd_name in ("export", "declare", "typeset", "local", "readonly"):
                if any(UNSAFE_DAILY_ENV_RE.match(t.split("=", 1)[0]) for t in core[1:] if not t.startswith("-")):
                    sticky_unsafe_env = True
                    daily_tainted = True

            if cmd_name == "cd" and len(core) >= 2 and not core[1].startswith("-"):
                target = pathlib.Path(os.path.expanduser(core[1]))
                cwd = target.resolve() if target.is_absolute() else (cwd / target).resolve()
                continue

            c_script = _extract_shell_c_script(core)
            if c_script:
                _inspect_run_command(c_script, cwd, pending_asks, depth + 1, sticky_unsafe_env, dict(trusted_daily), daily_tainted)
                daily_tainted = True
                continue
            if cmd_name in SHELL_BINS:
                if "\n" in pipe_text and "<<" in pipe_text:
                    hd_nl = pipe_text.find("\n")
                    _inspect_run_command(pipe_text[hd_nl + 1 :], cwd, pending_asks, depth + 1, sticky_unsafe_env, dict(trusted_daily), daily_tainted)
                    daily_tainted = True
                    trusted_daily.clear()
                    continue
                if "<<<" in pipe_text:
                    rhs = pipe_text.split("<<<", 1)[1].strip()
                    for cand in (" ".join(_tokenize(rhs)), rhs):
                        if cand:
                            _inspect_run_command(cand, cwd, pending_asks, depth + 1, sticky_unsafe_env, dict(trusted_daily), daily_tainted)
                    daily_tainted = True
                    trusted_daily.clear()
                    pending_asks.append("CỔNG WMS: shell here-string (<<<) không nằm trong ngoại lệ daily — cần Duy xác nhận.")
                    continue
                if len(stages) > 1:
                    for prev_st in stages[:-1]:
                        ptoks = _tokenize(prev_st)
                        for cand in (" ".join(ptoks[1:]), prev_st):
                            if cand:
                                _inspect_run_command(cand, cwd, pending_asks, depth + 1, sticky_unsafe_env, dict(trusted_daily), daily_tainted)
                    daily_tainted = True
                    trusted_daily.clear()
                    pending_asks.append("CỔNG WMS: đẩy lệnh qua pipe vào shell (| bash/sh) cần Duy xác nhận.")
                    continue
            if cmd_name == "eval" and len(core) > 1:
                _inspect_run_command(" ".join(core[1:]), cwd, pending_asks, depth + 1, sticky_unsafe_env, dict(trusted_daily), daily_tainted)
                daily_tainted = True
                trusted_daily.clear()
                continue

            g = _parse_git(core, cwd)
            if g["is_git"]:
                sub, rest = g["sub"], g["rest"]
                if any(c.split("=", 1)[0].strip().lower() == "core.hookspath" for c in g["c_configs"]):
                    out("deny", "VI PHẠM LUẬT 12 (QĐ 64): CẤM ghi đè core.hooksPath!")
                if sub == "config" and any("core.hookspath" in t.lower() for t in rest):
                    out("deny", "VI PHẠM LUẬT 12 (QĐ 64): CẤM sửa core.hooksPath qua git config!")
                pre_dd = rest[: rest.index("--")] if "--" in rest else rest
                if sub in ("push", "merge", "cherry-pick", "rebase") and any(
                    t.startswith("--no-veri") and "--no-verify".startswith(t) for t in pre_dd
                ):
                    out("deny", f"VI PHẠM LUẬT 12 (QĐ 64): CẤM --no-verify trên git {sub}!")
                if sub == "commit" and any(
                    (t.startswith("--no-veri") and "--no-verify".startswith(t))
                    or (t.startswith("-") and not t.startswith("--") and "n" in t[1:])
                    for t in pre_dd
                ):
                    out("deny", "VI PHẠM LUẬT 12 (QĐ 64): CẤM git commit -n / --no-verify!")

                repo_key, disk_br = _repo_state(g["git_cwd"], g["git_dir_arg"], g["work_tree_arg"])
                if g["has_config_override"] or (sub and sub not in SAFE_DAILY_GIT_SUBS):
                    daily_tainted = True
                    trusted_daily.clear()

                if sub in ("checkout", "switch"):
                    new_br = None
                    pos: list[str] = []
                    saw_dd = False
                    j = 0
                    while j < len(rest):
                        t = rest[j]
                        if t == "--":
                            saw_dd = True
                            j += 1
                            continue
                        if not saw_dd and t in ("-b", "-B", "-c", "-C", "--create", "--force-create") and j + 1 < len(rest):
                            new_br = rest[j + 1]
                            j += 2
                            continue
                        if not saw_dd and t.startswith("-"):
                            j += 1
                            continue
                        if not saw_dd:
                            pos.append(t)
                        j += 1
                    tgt = new_br or (pos[0] if pos else "")
                    if tgt:
                        is_br = bool(new_br) or tgt in MAIN_BRANCHES or sub == "switch" or (
                            _run_git(g["git_cwd"], "show-ref", "--verify", "--quiet", f"refs/heads/{tgt}",
                                     git_dir=g["git_dir_arg"], work_tree=g["work_tree_arg"]).returncode == 0
                        )
                        if is_br:
                            if not daily_tainted and not checkout_poisoned and prev_sep in ("", "&&") and not sticky_unsafe_env and not g["has_config_override"]:
                                trusted_daily[repo_key] = tgt
                            else:
                                trusted_daily.pop(repo_key, None)
                    continue

                if sub == "push":
                    ppos = _pos_args(rest, PUSH_OPTS_WITH_VAL)
                    refspecs = ppos[1:]
                    targets_main = any("*" in s or s.lstrip("+") == ":" for s in refspecs) or any(
                        flag in pre_dd for flag in ("--all", "--mirror", "--branches")
                    )
                    if not targets_main:
                        if not refspecs:
                            targets_main = trusted_daily.get(repo_key, disk_br) in MAIN_BRANCHES
                        else:
                            for sp in refspecs:
                                clean = sp.lstrip("+")
                                src, dst = clean.split(":", 1) if ":" in clean else (clean, clean)
                                if dst.lstrip("+") in MAIN_REFS or (":" not in clean and src in ("HEAD", "@") and trusted_daily.get(repo_key, disk_br) in MAIN_BRANCHES):
                                    targets_main = True
                                    break
                    if targets_main:
                        out("deny", "VI PHẠM LUẬT 12 (QĐ 64): CẤM push thẳng vào nhánh main/master! Bắt buộc mở PR.")
                    active_br = trusted_daily.get(repo_key, disk_br)
                    if daily_tainted or sticky_unsafe_env or g["has_config_override"] or not _is_daily_push(g, active_br):
                        pending_asks.append("CỔNG SHIP WMS: git push ngoài ngoại lệ daily automation cần Duy xác nhận trực tiếp.")
                continue

            if cmd_name == "gh":
                grp, gsub, gpre, grest = _extract_gh_pr_sub(core)
                if grp == "pr" and gsub in ("create", "merge"):
                    if daily_tainted or sticky_unsafe_env or has_redir or not _is_daily_gh_pr(gsub, gpre + grest, cwd, trusted_daily):
                        pending_asks.append("CỔNG SHIP WMS: lệnh `gh pr` ngoài ngoại lệ daily automation cần Duy xác nhận.")
                elif grp in ("pr", "release") and gsub not in ("list", "view", "checks", "status", "diff", "comment", ""):
                    if grp == "release":
                        pending_asks.append("CỔNG SHIP WMS: gh release cần Duy xác nhận trực tiếp.")
                elif grp == "release":
                    pending_asks.append("CỔNG SHIP WMS: gh release cần Duy xác nhận trực tiếp.")
                continue

            if _is_pipeline_upload_cmd(core):
                daily_ok, _ = _is_verified_daily_dir(cwd)
                repo_key, _ = _repo_state(cwd)
                chain_daily = WMS_DAILY_BRANCH_RE.match(trusted_daily.get(repo_key, ""))
                if sticky_unsafe_env or has_redir or not (daily_ok or chain_daily):
                    pending_asks.append("CỔNG SHIP WMS: tải video YouTube / đặt public ngoài nhánh daily cần Duy xác nhận.")
                continue

            if cmd_name in SHIP_OTHER:
                pending_asks.append("CỔNG SHIP WMS: lệnh phát hành ra ngoài cần Duy xác nhận trực tiếp.")

            # Shell inline write check (bỏ qua lệnh tìm kiếm đọc thuần không chuyển hướng)
            if not (cmd_name in READONLY_SEARCH_CMDS and not has_redir):
                if non_auto_approved_count(seg):
                    pending_asks.append("CỔNG DUYỆT WMS-R4: lệnh shell ghi approvedBy không phải \"auto-daily\".")
                elif approved_count(seg) or published_count(seg) or uploaded_public_count(seg):
                    daily_ok, _ = _is_verified_daily_dir(cwd)
                    repo_key, _ = _repo_state(cwd)
                    if sticky_unsafe_env or has_redir or not (daily_ok or WMS_DAILY_BRANCH_RE.match(trusted_daily.get(repo_key, ""))):
                        pending_asks.append("CỔNG DUYỆT WMS-R4 / QĐ 56: lệnh shell ghi trạng thái xuất bản ngoài nhánh daily.")

        if sep_after in ("||", "|"):
            checkout_poisoned = True
            trusted_daily.clear()
        elif sep_after != "&&":
            checkout_poisoned = False
            trusted_daily.clear()
        else:
            checkout_poisoned = False
        prev_sep = sep_after


def _resolve_existing_dir(path_str: str, fallback_cwd: pathlib.Path) -> pathlib.Path:
    if not path_str:
        return fallback_cwd
    p = pathlib.Path(path_str)
    p = (fallback_cwd / p).resolve() if not p.is_absolute() else p.resolve()
    cur = p if p.is_dir() else p.parent
    while not cur.exists() and cur != cur.parent:
        cur = cur.parent
    return cur if cur.exists() else fallback_cwd


def main() -> None:
    global IS_CLAUDE
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if "tool_name" in payload:
            IS_CLAUDE = True
            name = str(payload.get("tool_name") or "")
            args = payload.get("tool_input") or {}
        else:
            tc = payload.get("toolCall") or {}
            name = str(tc.get("name") or "")
            args = tc.get("args") or {}
        if not isinstance(args, dict):
            raise TypeError("args không phải object")
        raw_cwd = payload.get("cwd")
        init_cwd = pathlib.Path(raw_cwd).resolve() if isinstance(raw_cwd, str) and raw_cwd else pathlib.Path.cwd().resolve()
    except Exception as e:  # noqa: BLE001 — fail-closed có chủ đích
        out("force_ask", f"CỔNG WMS: không đọc được payload hook ({e!r}) — hỏi Duy thay vì cho qua.")

    if name in ("run_command", "Bash"):
        cmd = str(args.get("CommandLine") or args.get("command") or "")
        pending_asks: list[str] = []
        _inspect_run_command(cmd, init_cwd, pending_asks)
        if pending_asks:
            out("force_ask", pending_asks[0])
        out("allow")

    path_str = next((str(args[k]) for k in PATH_KEYS if args.get(k)), "")
    new_text, old_text, pairs = extract_edit_pairs(args)
    if not path_str and not new_text:
        out("allow")

    is_pipeline = pathlib.PurePath(path_str).name == "PIPELINE.md"
    if name in WRITE_TOOLS and not new_text and (is_pipeline or not path_str.endswith(".md")):
        out("force_ask", f"CỔNG WMS: {name} không có khoá nội dung nào guard đọc được — hỏi Duy thay vì cho qua.")

    p = pathlib.Path(path_str) if path_str else None
    if p is not None and not p.is_absolute():
        p = (init_cwd / p).resolve()
    try:
        disk = p.read_text(errors="replace") if p is not None and p.is_file() else ""
    except OSError:
        disk = ""
    if not old_text and name in ("write_file", "write_to_file", "Write"):
        old_text = disk
        pairs = [(new_text, disk)]

    # 4 — cổng duyệt bài (WMS-R4), cho mọi file trừ .md
    if not path_str.endswith(".md"):
        check_pairs = pairs + [(new_text, old_text)]
        inc_non_auto = any(non_auto_approved_count(cn) > non_auto_approved_count(co) for cn, co in check_pairs)
        if inc_non_auto:
            out("force_ask", "CỔNG DUYỆT WMS-R4: không được ghi approvedBy cá nhân (như \"Duy\") — chỉ Duy hoặc \"auto-daily\" trên nhánh daily.")

        inc_appr = any(approved_count(cn) > approved_count(co) for cn, co in check_pairs)
        inc_pub = any(published_count(cn) > published_count(co) for cn, co in check_pairs)
        inc_up = any(uploaded_public_count(cn) > uploaded_public_count(co) for cn, co in check_pairs)
        if inc_appr or inc_pub or inc_up:
            target_dir = _resolve_existing_dir(path_str, init_cwd)
            daily_ok, _ = _is_verified_daily_dir(target_dir)
            if not daily_ok:
                if inc_appr:
                    out("force_ask", "CỔNG DUYỆT WMS-R4: ghi approvedBy (đã duyệt). Agent không được tự duyệt — chỉ Duy.")
                if inc_pub:
                    out("force_ask", "CỔNG DUYỆT WMS-R4: đặt status \"published\". Agent để \"review\"; chỉ Duy đăng.")
                out("force_ask", "CỔNG DUYỆT WMS-R4 / QĐ 56: đặt embedStatus \"uploaded_public\". Chỉ Duy mở công khai.")

    # 5 — cổng con trỏ PIPELINE.md
    if pathlib.PurePath(path_str).name == "PIPELINE.md" and "templates/app/PIPELINE.md" not in path_str:
        m_old = POINTER.search(old_text) or POINTER.search(disk)
        m_new = POINTER.search(new_text)
        if m_new and (not m_old or m_new.group(1) != m_old.group(1)):
            frm = m_old.group(1) if m_old else "?"
            out("force_ask", f"CỔNG DUYỆT (Quy tắc 1): đổi pointer PIPELINE.md {frm} → {m_new.group(1)}. Chỉ Duy.")
        if len(APPROVE_LINE.findall(new_text)) > len(APPROVE_LINE.findall(old_text or disk)):
            out("force_ask", "CỔNG DUYỆT (Quy tắc 1): ghi dòng APPROVE/DUYỆT vào PIPELINE.md. Chỉ Duy duyệt stage.")

    out("allow")


if __name__ == "__main__":
    main()
