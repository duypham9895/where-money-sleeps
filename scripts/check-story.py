#!/usr/bin/env python3
"""check-story.py — phép kiểm TẤT ĐỊNH cho dữ liệu bài của Where Money Sleeps.

Chạy (từ thư mục app):
    python3 -I scripts/check-story.py                     # kiểm docs/prototype.html
    python3 -I scripts/check-story.py --file <html> ...   # kiểm file khác
    python3 -I scripts/check-story.py --story install     # chỉ kiểm một bài
    python3 -I scripts/check-story.py --sync-with <html>  # C8: so khối Scene với một bản xem nhanh ngoài docs/

C8 (từ 2026-11-08) kiểm bộ luật nằm TRONG repo: file luật/skill/agent/hook có mặt, bản chép không lệch,
khối SCENECSS/SCENEJS nguyên vẹn. Chạy một lần mỗi lệnh, kể cả khi dữ liệu bài không parse được.

C9 v2 (từ 2026-11-08, Hướng 3A) kiểm mỗi bài có đủ 3 trụ: `article.lay` (≥ 3 lầm tưởng/sự thật · ≥ 4 chương
`sections` ≥ 850 từ · `flowSummary` ≥ 4 bước kênh wire/pipe/book · 5 vai · `whenHelps`/`whenTraps` ≥ 3 · ≥ 4 câu hỏi)
· `article.pro` (≥ 4 cơ chế ≥ 450 từ · ≥ 4 ghi chú kế toán ≥ 180 từ · ≥ 3 bút toán TT 99 — cùng luật C6 — · ≥ 3
ngoại lệ × 50 từ) · `videoScript.long` (≥ 10 cảnh, lời bình ≥ 1.350 từ, kết 7:30–11:00) + `videoScript.short`
(≥ 5 cảnh, lời bình 150–260 từ, kết 0:55–1:35). Cộng grep tất định: điều luật/URL, tên ngân hàng thương mại,
câu khuyên. Ngưỡng là ĐỘ DÀI và HÌNH DẠNG, không phải chất lượng.

Đọc ba khối dữ liệu `const GLOSS`, `const STORIES`, `const CATEGORIES` ngay trong file HTML
bằng một parser literal JS đệ quy (KHÔNG dùng regex→JSON), rồi kiểm các luật trong
gates/01-spec/AGENT-CMS-PIPELINE.md. Thoát mã 1 nếu có FAIL.

Script này KHÔNG kiểm được: câu chữ đúng nghĩa, con số kinh tế (EIR, % phí) có hợp lý không,
tên tài khoản có khớp văn bản GỐC TT 99/2025 không, và ai đã bấm "Duyệt & Đăng".
Những việc đó thuộc ke-toan-reviewer và Duy.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "docs" / "prototype.html"
TT99_FILE = ROOT / "legal" / "tt99-phu-luc-ii.secondary.json"

N_HOUSES = 5
N_BEATS = 5
# Đạo cụ (fx) mà mỗi archetype nhà có sẵn trong Scene. Phải khớp code vẽ; C2b tự kiểm từng tên có trong HTML.
FX_BY_TYPE = {
    "home": {"phone"},
    "shop": {"pos", "empty", "recv", "paid"},
    "acq": {"board", "split"},
    "scheme": {"wire"},
    "crowd": {"idle"},
    "iss": {"iledger", "hold", "release"},
    "pbank": {"two", "pool"},
    "co": {"hr", "deal"},
    "lend": {"loan"},
}
TERM = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


# ───────────────────────── parser literal JS ─────────────────────────
class JSLiteral:
    """Đọc một literal JS (object/array/string/number/true/false/null), có comment và dấu phẩy thừa."""

    NUM = re.compile(r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
    KEY = re.compile(r"[A-Za-z_$][\w$]*|\d+")

    def __init__(self, src: str, i: int):
        self.s, self.i = src, i

    def err(self, msg: str) -> ValueError:
        return ValueError(f"dòng {self.s.count(chr(10), 0, self.i) + 1}: {msg}")

    def ws(self) -> None:
        s = self.s
        while self.i < len(s):
            if s[self.i] in " \t\r\n":
                self.i += 1
            elif s.startswith("//", self.i):
                j = s.find("\n", self.i)
                self.i = len(s) if j < 0 else j + 1
            elif s.startswith("/*", self.i):
                j = s.find("*/", self.i + 2)
                if j < 0:
                    raise self.err("comment /* chưa đóng")
                self.i = j + 2
            else:
                return

    def peek(self) -> str:
        self.ws()
        return self.s[self.i:self.i + 1]

    def expect(self, ch: str) -> None:
        if self.peek() != ch:
            raise self.err(f"cần '{ch}', gặp {self.s[self.i:self.i + 20]!r}")
        self.i += 1

    def value(self):
        c = self.peek()
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'":
            return self.string()
        for lit, val in (("true", True), ("false", False), ("null", None)):
            end = self.i + len(lit)
            nxt = self.s[end:end + 1]
            if self.s.startswith(lit, self.i) and not (nxt.isalnum() or nxt == "_"):
                self.i = end
                return val
        m = self.NUM.match(self.s, self.i)
        if m and m.group():
            self.i = m.end()
            t = m.group()
            return float(t) if any(ch in t for ch in ".eE") else int(t)
        raise self.err(f"không đọc được giá trị: {self.s[self.i:self.i + 30]!r}")

    def string(self) -> str:
        q = self.s[self.i]
        self.i += 1
        out = []
        esc = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}
        while self.i < len(self.s):
            c = self.s[self.i]
            if c == q:
                self.i += 1
                return "".join(out)
            if c == "\n":
                raise self.err("chuỗi xuống dòng mà chưa đóng")
            if c == "\\":
                n = self.s[self.i + 1]
                if n == "u":
                    out.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                    continue
                out.append(esc.get(n, n))
                self.i += 2
                continue
            out.append(c)
            self.i += 1
        raise self.err("chuỗi chưa đóng")

    def key(self) -> str:
        c = self.peek()
        if c in "\"'":
            return self.string()
        m = self.KEY.match(self.s, self.i)
        if not m:
            raise self.err(f"không đọc được khoá: {self.s[self.i:self.i + 20]!r}")
        self.i = m.end()
        return m.group()

    def obj(self) -> dict:
        self.expect("{")
        out = {}
        while self.peek() != "}":
            k = self.key()
            self.expect(":")
            out[k] = self.value()
            if self.peek() == ",":
                self.i += 1
            elif self.peek() != "}":
                raise self.err(f"cần ',' hoặc '}}' sau khoá {k!r}")
        self.i += 1
        return out

    def arr(self) -> list:
        self.expect("[")
        out = []
        while self.peek() != "]":
            out.append(self.value())
            if self.peek() == ",":
                self.i += 1
            elif self.peek() != "]":
                raise self.err("cần ',' hoặc ']' trong mảng")
        self.i += 1
        return out


def extract(src: str, name: str):
    m = re.search(rf"\bconst\s+{name}\s*=\s*", src)
    if not m:
        raise ValueError(f"không thấy khối `const {name} =`")
    return JSLiteral(src, m.end()).value()


def scene_types(src: str) -> set[str]:
    """Lấy tên archetype từ `const TYPES = {...}`: tách theo dấu phẩy ở độ sâu 0, bỏ qua () {} [] và chuỗi."""
    m = re.search(r"\bconst\s+TYPES\s*=\s*\{", src)
    if not m:
        raise ValueError("không thấy `const TYPES = {` trong Scene")
    i, depth, part, parts, quote = m.end(), 0, [], [], None
    while i < len(src):
        c = src[i]
        if quote:
            part.append(c)
            if c == "\\":
                part.append(src[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
            part.append(c)
        elif c in "([{":
            depth += 1
            part.append(c)
        elif c in ")]}":
            if depth == 0:
                parts.append("".join(part))
                break
            depth -= 1
            part.append(c)
        elif c == "," and depth == 0:
            parts.append("".join(part))
            part = []
        else:
            part.append(c)
        i += 1
    keys = set()
    for p in parts:
        km = re.match(r"\s*([A-Za-z_$][\w$]*)", p)
        if km:
            keys.add(km.group(1))
    return keys


def load_tt99() -> dict[str, str] | None:
    try:
        data = json.loads(TT99_FILE.read_text(encoding="utf-8"))
        return {a["code"]: a["name"] for a in data.get("accounts", [])}
    except (OSError, ValueError, KeyError):
        return None


def all_text(story: dict) -> list[str]:
    out = [story.get("title", ""), story.get("teaser", "")]
    for b in story.get("beats", []):
        out += list(b.get("say", [])) + [b.get("life", ""), b.get("sys", ""), b.get("title", "")]
        led = b.get("ledger")
        led = led if isinstance(led, dict) else {}            # kiểu sai đã có C6 báo FAIL — ở đây chỉ không được chết
        out += [led.get("assume", ""), led.get("note", ""), led.get("lifeNote", "")]
    return [t for t in out if isinstance(t, str)]


# ───────────────────────── các phép kiểm ─────────────────────────
class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, str, str]] = []

    def add(self, level: str, code: str, where: str, msg: str) -> None:
        self.rows.append((level, code, where, msg))

    def has_fail(self) -> bool:
        return any(r[0] == "FAIL" for r in self.rows)


def check_js_syntax(src: str, rep: Report, label: str) -> None:
    """C0 — khối <script> cuối parse được bằng `node --check` (SKIP nếu máy không có node)."""
    node = shutil.which("node")
    if not node:
        rep.add("SKIP", "C0", label, "không có node trên PATH — chưa kiểm cú pháp JS")
        return
    scripts = re.findall(r"<script>(.*?)</script>", src, flags=re.S)
    if not scripts:
        rep.add("WARN", "C0", label, "không có <script> nội tuyến")
        return
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "page.js"
        p.write_text(scripts[-1], encoding="utf-8")
        r = subprocess.run([node, "--check", str(p)], capture_output=True, text=True)
    if r.returncode:
        lines = [ln.strip() for ln in r.stderr.splitlines() if ln.strip()]
        where = next((ln.rsplit(":", 1)[-1] for ln in lines if ln.endswith(tuple("0123456789")) and "page.js:" in ln), "?")
        msg = next((ln for ln in lines if "Error" in ln), lines[-1] if lines else "?")
        rep.add("FAIL", "C0", label, f"JS không parse được (dòng {where} của <script>): {msg}")
    else:
        rep.add("PASS", "C0", label, "cú pháp JS hợp lệ (node --check)")


def check_story(k: str, s: dict, ctx: dict, rep: Report) -> None:
    w = f"bài '{k}'"
    types, gloss, cat_ids, tt99 = ctx["types"], ctx["gloss"], ctx["cat_ids"], ctx["tt99"]
    if s.get("category") not in cat_ids:
        rep.add("FAIL", "C1", w, f"category '{s.get('category')}' không có trong CATEGORIES")
    if ctx["topic_refs"].get(k, 0) != 1:
        rep.add("FAIL", "C1", w, f"phải nằm ở đúng 1 chủ đề, đang ở {ctx['topic_refs'].get(k, 0)}")
    for f in ("name", "title", "teaser"):
        if not isinstance(s.get(f), str) or not s.get(f):
            rep.add("FAIL", "C1", w, f"thiếu `{f}` (trang sẽ in chữ 'undefined')")

    # C2 — 5 nhà archetype + 5 đoạn
    houses, beats = s.get("houses", []), s.get("beats", [])
    if len(houses) != N_HOUSES:
        rep.add("FAIL", "C2", w, f"cần đúng {N_HOUSES} nhà, có {len(houses)}")
    for hi, h in enumerate(houses):
        if h.get("type") not in types:
            rep.add("FAIL", "C2", f"{w} nhà {hi}", f"type '{h.get('type')}' không phải archetype của Scene ({', '.join(sorted(types))})")
        if not h.get("label"):
            rep.add("FAIL", "C2", f"{w} nhà {hi}", "thiếu nhãn `label`")
        for fx in (h.get("fxText") or {}):
            if fx not in FX_BY_TYPE.get(h.get("type"), set()):
                rep.add("WARN", "C2", f"{w} nhà {hi}", f"fxText '{fx}' không thuộc archetype '{h.get('type')}' — sẽ không hiện")
    if len(beats) != N_BEATS:
        rep.add("FAIL", "C2", w, f"cần đúng {N_BEATS} đoạn, có {len(beats)}")
    supported = set()
    for h in houses:
        supported |= FX_BY_TYPE.get(h.get("type"), set())
    rng = range(len(houses))
    is_idx = lambda x: isinstance(x, int) and not isinstance(x, bool) and x in rng   # bool là int trong Python — loại ra

    for bi, b in enumerate(beats, 1):
        bw = f"{w} đoạn {bi}"
        say = b.get("say")
        if not isinstance(say, list) or not say or not all(isinstance(x, str) and x for x in say):
            rep.add("FAIL", "C2", bw, "`say` phải là mảng câu không rỗng")
        for f in ("when", "sub", "title", "life", "sys"):
            if not isinstance(b.get(f), str) or not b.get(f):
                rep.add("FAIL", "C2", bw, f"thiếu `{f}` (trang sẽ in 'undefined')")
        # thiếu các trường này thì trang ném TypeError, không chỉ hiện sai
        for f, kind in (("lit", list), ("msgs", list), ("fx", list), ("tags", dict)):
            if not isinstance(b.get(f), kind):
                rep.add("FAIL", "C2", bw, f"`{f}` phải có và là {'mảng' if kind is list else 'object'} (thiếu ⇒ trang sập)")
        if "ledger" not in b:
            rep.add("FAIL", "C2", bw, "thiếu `ledger` — đoạn không có bút toán thì ghi `ledger:null`")
        # C3 — chỉ số nhà, luật dây (lời nhắn) / ống (tiền thật)
        for i in b.get("lit") or []:
            if not is_idx(i):
                rep.add("FAIL", "C3", bw, f"lit chứa {i!r}, ngoài 0..{len(houses) - 1}")
        tags = b.get("tags") if isinstance(b.get("tags"), dict) else {}
        for key, val in tags.items():
            if not str(key).isdigit() or int(key) not in rng:
                rep.add("FAIL", "C3", bw, f"tags có khoá {key!r}, ngoài 0..{len(houses) - 1}")
            if not (isinstance(val, list) and len(val) == 2 and val[1] in ("plus", "minus", "plain")):
                rep.add("FAIL", "C3", bw, f"tags[{key}] phải là [chữ, \"plus\"|\"minus\"|\"plain\"]: {val!r}")
        for m in b.get("msgs") or []:
            if not isinstance(m, list) or len(m) not in (2, 3) or any(not is_idx(x) for x in m[:2]):
                rep.add("FAIL", "C3", bw, f"msgs {m!r}: phải là [từ, tới] hoặc [từ, tới, \"money\"], chỉ số 0..{len(houses) - 1}")
            elif len(m) == 3 and m[2] != "money":
                rep.add("FAIL", "C3", bw, f"msgs {m!r}: phần tử thứ 3 chỉ được là \"money\" (tiền thật đi ống ngầm)")
            elif m[0] == m[1]:
                rep.add("FAIL", "C3", bw, f"msgs {m!r}: từ và tới trùng nhau")
        # C4 — đạo cụ phải có nhà hỗ trợ
        for fx in b.get("fx") or []:
            if fx not in supported:
                rep.add("FAIL", "C4", bw, f"fx '{fx}' không thuộc nhà nào trong bài — sẽ không hiện")
        # C6 — sổ cái kép
        led = b.get("ledger")
        # `{}` và `[]` là falsy trong Python nhưng TRUTHY trong JS ⇒ trang sẽ đọc .rows và sập. Chỉ `null` mới là "không có sổ".
        if led is not None:
            if not isinstance(led, dict):
                rep.add("FAIL", "C6", bw, f"`ledger` phải là object hoặc null, gặp {type(led).__name__}")
            else:
                check_ledger(led, bw, tt99, rep)

    # C5 — thuật ngữ chạm-để-hiểu (cả 5 đoạn lẫn bài sâu C9)
    for t in all_text(s) + article_text(s):
        for mt in TERM.finditer(t):
            key = (mt.group(2) or mt.group(1)).lower()
            if key not in gloss:
                rep.add("FAIL", "C5", w, f"{mt.group(0)} trỏ tới khoá '{key}' không có trong GLOSS")

    # C7 — trạng thái và duyệt (kiểm HÌNH THỨC: không chứng minh được ai bấm)
    st, by = s.get("status"), s.get("approvedBy") or ""
    if st not in ("review", "published"):
        rep.add("FAIL", "C7", w, f"status bài phải là 'review' hoặc 'published', gặp {st!r}")
    elif st == "published":
        if not by:
            rep.add("FAIL", "C7", w, "published nhưng thiếu `approvedBy`")
        elif "demo" in by.lower():
            rep.add("WARN", "C7", w, f"published ở chế độ demo ('{by}') — chưa phải Duy duyệt thật")
        elif not s.get("approvedAt"):
            rep.add("FAIL", "C7", w, "published nhưng thiếu `approvedAt`")
        else:
            rep.add("PASS", "C7", w, f"approvedBy '{by}' · {s.get('approvedAt')} (kiểm hình thức)")
    elif by:
        rep.add("FAIL", "C7", w, "bài đang 'review' mà đã có `approvedBy`")
    else:
        rep.add("PASS", "C7", w, "status 'review', chưa ai duyệt — đúng")

    # C6v — proxy yếu: số giả định có nhãn "ví dụ".
    # Mã cũ là C8 tới 2026-11-07; từ 2026-11-08 C8 dành cho Governance (AGENT-CMS-PIPELINE §6).
    if not any("ví dụ" in t for t in all_text(s)):
        rep.add("FAIL", "C6v", w, "không có chữ 'ví dụ' nào — số giả định phải gắn nhãn (proxy yếu)")

    # C9 — bài sâu 2 tầng + kịch bản video (từ 2026-11-08)
    check_article(k, s, tt99, rep)


def check_ledger(led: dict, bw: str, tt99: dict | None, rep: Report) -> None:
    debit = credit = 0
    for f in ("book", "assume", "note", "lifeNote"):
        if not isinstance(led.get(f), str) or not led.get(f):
            rep.add("FAIL", "C6", bw, f"bút toán thiếu `{f}` (trang sẽ in 'undefined')")
    if not isinstance(led.get("rows"), list) or not led.get("rows"):
        rep.add("FAIL", "C6", bw, "bút toán không có dòng nào — Σ 0 = 0 không phải là cân")
        return
    for r in led.get("rows", []):
        if not isinstance(r, list) or len(r) != 6:
            rep.add("FAIL", "C6", bw, f"dòng sổ phải có 6 cột [Nợ|Có, số TK, tên TK, chi tiết, lời thường, số tiền]: {r!r}")
            continue
        dc, code, name, detail, simple, amt = r
        if dc not in ("Nợ", "Có"):
            rep.add("FAIL", "C6", bw, f"cột 1 phải là 'Nợ' hoặc 'Có', gặp {dc!r}")
            continue
        if not isinstance(amt, int) or isinstance(amt, bool) or amt <= 0:
            rep.add("FAIL", "C6", bw, f"số tiền phải là số nguyên dương: {amt!r}")
            continue
        if dc == "Nợ":
            debit += amt
        else:
            credit += amt
        # luật 131: chỉ áp cho DÒNG SỔ, không quét ghi chú
        if str(code) == "131" and "ngân hàng" in f"{name} {detail} {simple}".lower():
            rep.add("FAIL", "C6", bw, "TK 131 dùng cho phải thu từ ngân hàng — dùng 1388 (Phải thu khác)")
        if tt99 is not None:
            ref = tt99.get(str(code))
            if ref is None:
                rep.add("WARN", "C6", bw, f"TK {code} không có trong bảng thứ cấp TT 99 — chờ ke-toan-reviewer")
            elif ref != name:
                rep.add("WARN", "C6", bw, f"TK {code}: tên '{name}' ≠ bảng thứ cấp '{ref}'")
            else:
                rep.add("SECONDARY", "C6", bw, f"TK {code} {name} — khớp nguồn thứ cấp (không bao giờ là PASS)")
    if debit != credit:
        rep.add("FAIL", "C6", bw, f"Σ Nợ {debit:,} ≠ Σ Có {credit:,}".replace(",", "."))
    else:
        rep.add("PASS", "C6", bw, f"Σ Nợ = Σ Có = {debit:,}".replace(",", "."))


# ───────────────────── C9 v2 — Bài khảo cứu 2 tầng + Studio Kịch bản Video 2 định dạng ─────────────────────
# Vì sao có (Duy, 2026-11-08): "mỗi bài viết phải đầy đủ thông tin cho users (là người có chuyên và kh có
# chuyên môn) để sau này tôi có để dùng content của bài post để tạo video". v2 (cùng ngày, Hướng 3A): bài khảo
# cứu ≥ 850 từ chia chương, sơ đồ dòng chảy 3 kênh, khi có lợi / khi thành bẫy, và kịch bản 2 định dạng —
# YouTube dài 8–10 phút + Shorts/Reels/TikTok 60–90 giây. C9 chặn bằng NGƯỠNG ĐỘ DÀI và HÌNH DẠNG, cộng vài
# phép grep tất định (trích điều luật, URL, tên ngân hàng thương mại, câu khuyên) — không chứng minh câu chữ
# đúng hay hay. "Từ" = token tách theo khoảng trắng; với tiếng Việt đó là ÂM TIẾT.
WPM = 190                      # âm tiết lời bình / phút — ước lượng cho giọng đọc tiếng Việt, chưa đo trên ElevenLabs
TIME = re.compile(r"^\s*(\d+):([0-5]\d)\s*[–-]\s*(\d+):([0-5]\d)\s*$")
C9_MIN = {"myths": 3, "myth": 10, "truth": 10, "sections": 4, "sections_words": 850, "flow": 4,
          "helps": 3, "traps": 3, "when_words": 10, "takeaways": 4, "takeaway_words": 6,
          "mechanics": 4, "mechanics_words": 450, "acc_notes": 4, "acc_words": 180, "journal": 3,
          "edge": 3, "edge_words": 50}
# Khung thời lượng. Duy viết hai khung trong cùng yêu cầu 2026-11-08 (§1 nội dung · §3 script):
# FAIL ngoài khung lỏng (§3), WARN trong khe giữa hai khung. Trình duyệt chỉ soi mức FAIL.
VIDEO = {
    "long":  {"scenes": 10, "vo_lo": 1350, "vo_hi": None, "end_fail": (450, 660), "end_warn": (450, 630),
              "need": ("time", "chapter", "visual", "vo", "onScreen"), "head": ("title", "hookNote"), "cover": True},
    "short": {"scenes": 5, "vo_lo": 150, "vo_hi": 260, "end_fail": (55, 95), "end_warn": (55, 90),
              "need": ("time", "visual", "vo", "onScreen"), "head": ("title", "angle"), "cover": False},
}
CHANNELS = ("wire", "pipe", "book")
# Grep tất định trên MỌI chuỗi của article + videoScript. Chỉ Thông tư 99/2025/TT-BTC được trích — trích
# "Thông tư 200/2014" để so sánh cũng FAIL, CÓ CHỦ Ý (không có bản gốc trong repo để đối chiếu).
REG_RE = re.compile(r"Điều\s+\d+|Nghị định|Thông tư(?!\s*(?:số\s*)?99\b)|https?://", re.I)
# LUẬT 4 (VOICE-AND-PROSODY-SPEC.md §5) — Cấm tuyệt đối nhắc tên riêng / thương hiệu có thật / công cụ hậu trường
# trong bài viết, kịch bản video, giọng đọc (vo), chữ trên màn hình (onScreen), nhãn nhà (houses), GLOSS và CATEGORIES.
BRANDS = (
    # 1. Công cụ AI, Voice, Video hậu trường & Mạng xã hội
    "ElevenLabs", "Google", "Veo", "Gemini", "Claude", "Anthropic", "OpenAI", "ChatGPT", "Sora", "Runway", "Midjourney",
    "TikTok", "Reels", "Facebook", "Instagram", "Zalo", "Threads",
    # 2. Tổ chức thẻ & mạng chuyển mạch / trung gian thanh toán
    "Visa", "Mastercard", "JCB", "Amex", "American Express", "UnionPay", "NAPAS", "VietQR", "SmartPay", "Payoo", "VNPay",
    # 3. Ngân hàng thương mại & ngân hàng số
    "Vietcombank", "VietinBank", "BIDV", "Agribank", "Techcombank", "VPBank", "MB Bank", "MBBank", "ACB",
    "Sacombank", "TPBank", "HDBank", "SHB", "VIB", "OCB", "MSB", "SeABank", "Eximbank", "LPBank", "Shinhan",
    "HSBC", "Standard Chartered", "Timo", "Cake",
    # 4. Công ty tài chính tiêu dùng & BNPL
    "FE Credit", "Home Credit", "HD Saison", "Mcredit", "Mirae Asset", "Lotte Finance", "SHB Finance", "VietCredit",
    "Kredivo", "Fundiin", "Atome", "Reepay", "Muadee",
    # 5. Ví điện tử & cổng thanh toán
    "MoMo", "ZaloPay", "Viettel Money", "ShopeePay", "VTC Pay", "Moca", "GrabPay", "Apple Pay", "Google Pay", "Samsung Pay",
    # 6. Chuỗi bán lẻ, sàn TMĐT, hãng thiết bị, F&B & tên quán riêng
    "Thế Giới Di Động", "Điện Máy Xanh", "FPT Shop", "CellphoneS", "Di Động Việt", "Hoàng Hà Mobile",
    "Shopee", "Lazada", "Tiki", "Sendo", "Grab", "Xanh SM", "Gojek",
    "Apple", "iPhone", "iPad", "MacBook", "Samsung", "Galaxy", "Sony", "Xiaomi", "Oppo",
    "Highlands", "Phúc Long", "Starbucks", "Katinat", "The Coffee House", "Bách Hoá Xanh", "WinMart", "Circle K",
    "Nhà Liên", "Quán Nhà Liên",
    # 7. Tên riêng tác giả sách giáo khoa trong lời bài / khung hình
    "Hermanson", "Maher",
)
BRAND_RE = re.compile(r"(?<![\w])(" + "|".join(re.escape(b) for b in BRANDS) + r")(?![\w])", re.I)
ADVICE_RE = re.compile(r"\b(bạn|anh|chị|mình)\s+(nên|hãy|đừng)\s+(mua|vay|chọn|mở|gửi|trả góp|quẹt|dùng)\b"
                       r"|\bhãy\s+(mua|vay|chọn|mở thẻ|gửi tiền)\b", re.I)


def nwords(*texts) -> int:
    return sum(len(str(t).split()) for t in texts if isinstance(t, str))


def _walk(x, out: list[str]) -> list[str]:
    if isinstance(x, str):
        out.append(x)
    elif isinstance(x, list):
        for y in x:
            _walk(y, out)
    elif isinstance(x, dict):
        for y in x.values():
            _walk(y, out)
    return out


def article_text(story: dict) -> list[str]:
    """Mọi chuỗi trong article + videoScript — cho C5 (thuật ngữ) và grep C9. C6v vẫn chỉ đọc 5 đoạn."""
    return _walk(story.get("videoScript"), _walk(story.get("article"), []))


def secs(m: re.Match) -> tuple[int, int]:
    return int(m[1]) * 60 + int(m[2]), int(m[3]) * 60 + int(m[4])


def mmss(t: int) -> str:
    return f"{t // 60}:{t % 60:02d}"


YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
EMBED_STATES = {"pending_upload", "uploaded_unlisted", "uploaded_private", "uploaded_public"}
STACCATO_VIDU_RE = re.compile(
    r"(?:,\s*(?:vẫn\s+là\s+(?:số\s+)?|cũng\s+là\s+|chỉ\s+là\s+)?ví\s+dụ(?:\s+thôi)?\s*[.?!]"
    r"|(?:^|[.?!]\s+)(?:Vẫn|Tất\s+cả)\s+là\s+số\s+ví\s+dụ\s*[.?!])"
)
BARE_PCT_START_RE = re.compile(r"^\s*\d+(?:[.,]\d+)?\s*%")
RESIDUAL_CLAUSE_RE = re.compile(
    r"\b(?:nhưng|vì sao|mà)\b.*?\b(?:chỉ\s+(?:thực\s+)?nhận|nhận\s+về|còn\s+lại)\b",
    flags=re.I,
)


def check_video(fmt: str, v, s: dict, w: str, rep: Report) -> tuple[int, int, int]:
    """Một định dạng video. Trả (số cảnh, tổng từ lời bình, mốc cuối giây)."""
    cfg, tag = VIDEO[fmt], f"C·{fmt}"
    if not isinstance(v, dict):
        rep.add("FAIL", "C9", w, f"{tag}: thiếu `videoScript.{fmt}`")
        return 0, 0, 0
    for f in cfg["head"]:
        if not isinstance(v.get(f), str) or not v.get(f).strip():
            rep.add("FAIL", "C9", w, f"{tag} thiếu `{f}`")
    # VOICE-AND-PROSODY-SPEC.md §1 — Kiểm Luật Đủ 3 Điểm Neo Ngữ cảnh ở tiêu đề video
    v_title = str(v.get("title", "")).strip()
    if v_title:
        if nwords(v_title) < 8:
            rep.add("FAIL", "C9", w, f"{tag}.title {v_title!r} quá ngắn ({nwords(v_title)} từ < 8 từ) — thiếu ngữ cảnh tự thân (cần đủ 3 điểm neo: Hành động + Giá gốc → Cơ chế → Sự thật hệ thống)")
        if not re.search(r"\d+", v_title):
            rep.add("FAIL", "C9", w, f"{tag}.title {v_title!r} thiếu con số quy mô gốc ban đầu (VD: '10 triệu', '12 triệu', '15 triệu') — phải đủ 3 điểm neo ngữ cảnh tự thân (VOICE-AND-PROSODY-SPEC.md)")
        if BARE_PCT_START_RE.match(v_title):
            rep.add("FAIL", "C9", w, f"{tag}.title {v_title!r} mở đầu bằng số % trơ trọi — phải nêu hành động & giá trị gốc trước (VD: 'Mua hàng 12 triệu trả góp lãi suất 0%...')")
        m_res = RESIDUAL_CLAUSE_RE.search(v_title)
        if m_res and not re.search(r"\d+", v_title[:m_res.start()]):
            rep.add("FAIL", "C9", w, f"{tag}.title {v_title!r} nêu số nhận về ở vế sau nhưng thiếu con số giá trị ban đầu ở vế trước (VOICE-AND-PROSODY-SPEC.md)")
    # QĐ 56 & VOICE-AND-PROSODY-SPEC.md §2 — kiểm khoá nhúng YouTube & ElevenLabs voice ID (eleven_v3)
    yt_id = v.get("youtubeId")
    em_st = v.get("embedStatus")
    el_voice = v.get("elevenlabsVoiceId")
    if not isinstance(el_voice, str) or not el_voice.strip():
        rep.add("FAIL", "C9", w, f"{tag} thiếu `elevenlabsVoiceId` (QĐ 56)")
    elif el_voice.startswith("eleven_flash"):
        rep.add("FAIL", "C9", w, f"{tag}.elevenlabsVoiceId {el_voice!r} dùng model flash (nhịp phẳng, đọc từng chữ) — bắt buộc dùng 'eleven_v3:<voice_id>' (VOICE-AND-PROSODY-SPEC.md)")
    if em_st not in EMBED_STATES:
        rep.add("FAIL", "C9", w, f"{tag}.embedStatus {em_st!r} không hợp lệ — cần 1 trong {sorted(EMBED_STATES)} (QĐ 56)")
    if not isinstance(yt_id, str):
        rep.add("FAIL", "C9", w, f"{tag} thiếu `youtubeId` (chuỗi rỗng khi chờ upload hoặc mã 11 ký tự YouTube, QĐ 56)")
    elif em_st == "pending_upload" and yt_id != "":
        rep.add("FAIL", "C9", w, f"{tag}: embedStatus='pending_upload' nhưng youtubeId={yt_id!r} không rỗng")
    elif em_st in ("uploaded_unlisted", "uploaded_private", "uploaded_public") and not YT_ID_RE.match(yt_id):
        rep.add("FAIL", "C9", w, f"{tag}: embedStatus={em_st!r} cần youtubeId 11 ký tự chuẩn YouTube, gặp {yt_id!r}")
    if s.get("status") != "published" and em_st == "uploaded_public":
        rep.add("FAIL", "C9", w, f"{tag}: bài chưa đăng (status={s.get('status')!r}) không được để embedStatus='uploaded_public' (WMS-R4 / QĐ 56)")
    sc = v.get("scenes") if isinstance(v.get("scenes"), list) else []
    if len(sc) < cfg["scenes"]:
        rep.add("FAIL", "C9", w, f"{tag}.scenes: cần ≥ {cfg['scenes']} cảnh, có {len(sc)}")
    nb = len(s.get("beats", []))
    prev_end, covered, vo = 0, set(), 0
    for i, x in enumerate(sc):
        x = x if isinstance(x, dict) else {}
        for f in cfg["need"]:
            if not isinstance(x.get(f), str) or not x.get(f).strip():
                rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}] thiếu `{f}`")
        tm = TIME.match(str(x.get("time", "")))
        if not tm:
            rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}].time {x.get('time')!r}: phải dạng 'm:ss – m:ss'")
        else:
            a, b = secs(tm)
            if b <= a or a < prev_end:
                rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}].time {x.get('time')!r}: phải tăng dần, không chồng cảnh trước")
            prev_end = max(prev_end, b)
        bt = x.get("beat")
        if bt is not None and not (isinstance(bt, int) and not isinstance(bt, bool) and 0 <= bt < nb):
            rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}].beat {bt!r}: phải là null hoặc chỉ số đoạn 0..{nb - 1}")
        elif bt is not None:
            covered.add(bt)
        if "[[" in str(x.get("vo", "")) or "<" in str(x.get("vo", "")):
            rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}].vo còn markup [[…]] hoặc thẻ HTML — ElevenLabs sẽ đọc to")
        if STACCATO_VIDU_RE.search(str(x.get("vo", ""))):
            rep.add("FAIL", "C9", w, f"{tag}.scenes[{i}].vo đặt đuôi ', ví dụ.' cụt hứng ở cuối câu (End-Focus Sabotage) — phải đưa 'Trong ví dụ này,...' / 'Giả sử...' lên đầu mệnh đề (VOICE-AND-PROSODY-SPEC.md)")
        vo += nwords(x.get("vo"))
    if cfg["cover"]:
        first = sc[0] if sc and isinstance(sc[0], dict) else {}
        last = sc[-1] if sc and isinstance(sc[-1], dict) else {}
        if sc and (first.get("beat") is not None or last.get("beat") is not None):
            rep.add("FAIL", "C9", w, f"{tag}: cảnh đầu (Hook) và cảnh cuối (Kết) phải có beat: null")
        miss = sorted(set(range(nb)) - covered)
        if miss:
            rep.add("FAIL", "C9", w, f"{tag}: đoạn Diorama {', '.join(str(i + 1) for i in miss)} chưa có cảnh nào (beat)")
    if vo < cfg["vo_lo"] or (cfg["vo_hi"] and vo > cfg["vo_hi"]):
        band = f"{cfg['vo_lo']}–{cfg['vo_hi']}" if cfg["vo_hi"] else f"≥ {cfg['vo_lo']}"
        rep.add("FAIL", "C9", w, f"{tag}: tổng lời bình {vo} từ, cần {band}")
    lo, hi = cfg["end_fail"]
    wlo, whi = cfg["end_warn"]
    if prev_end and not lo <= prev_end <= hi:
        rep.add("FAIL", "C9", w, f"{tag}: mốc cuối {mmss(prev_end)} ngoài khung {mmss(lo)}–{mmss(hi)}")
    elif prev_end and not wlo <= prev_end <= whi:
        rep.add("WARN", "C9", w, f"{tag}: mốc cuối {mmss(prev_end)} trong khe {mmss(whi)}–{mmss(hi)} (Duy §1 ghi {mmss(wlo)}–{mmss(whi)})")
    if vo and prev_end and abs(vo / WPM * 60 - prev_end) > 0.25 * prev_end:
        rep.add("WARN", "C9", w, f"{tag}: {vo} từ lời bình ≈ {vo / WPM * 60:.0f}s ở {WPM} từ/phút, lệch > 25% so với mốc {prev_end}s (ước lượng)")
    return len(sc), vo, prev_end


def check_article(k: str, s: dict, tt99: dict | None, rep: Report) -> None:
    w = f"bài '{k}' C9"
    n0 = sum(1 for r in rep.rows if r[0] == "FAIL")
    art, vid = s.get("article"), s.get("videoScript")
    if not isinstance(art, dict) or not isinstance(vid, dict):
        rep.add("FAIL", "C9", w, "thiếu `article` (bài sâu 2 tầng) hoặc `videoScript` (kịch bản video) — bài sơ sài")
        return
    lay = art.get("lay") if isinstance(art.get("lay"), dict) else {}
    pro = art.get("pro") if isinstance(art.get("pro"), dict) else {}
    lst = lambda d, f: d.get(f) if isinstance(d.get(f), list) else []
    m = C9_MIN

    # PHẦN A — bài khảo cứu toàn cảnh cho người không chuyên
    myths = lst(lay, "myths")
    if len(myths) < m["myths"]:
        rep.add("FAIL", "C9", w, f"A·myths: cần ≥ {m['myths']} cặp Lầm tưởng/Sự thật, có {len(myths)}")
    for i, x in enumerate(myths):
        x = x if isinstance(x, dict) else {}
        for f in ("myth", "truth"):
            if nwords(x.get(f)) < m[f]:
                rep.add("FAIL", "C9", w, f"A·myths[{i}].{f}: cần ≥ {m[f]} từ, có {nwords(x.get(f))}")
    secs_ = lst(lay, "sections")
    paras = []
    for i, x in enumerate(secs_):
        x = x if isinstance(x, dict) else {}
        pp = x.get("paras") if isinstance(x.get("paras"), list) else []
        if not isinstance(x.get("h"), str) or not x.get("h").strip() or not pp or not all(isinstance(p, str) and p.strip() for p in pp):
            rep.add("FAIL", "C9", w, f"A·sections[{i}]: cần tiêu đề `h` và mảng `paras` không rỗng")
        paras += [p for p in pp if isinstance(p, str)]
    sw = nwords(*paras)
    if len(secs_) < m["sections"] or sw < m["sections_words"]:
        rep.add("FAIL", "C9", w, f"A·sections: cần ≥ {m['sections']} chương và ≥ {m['sections_words']} từ, có {len(secs_)} chương · {sw} từ")
    if "body" in lay:
        rep.add("FAIL", "C9", w, "A·body đã bỏ ở C9 v2 — nội dung nằm trong `sections` (tránh hai bản lệch nhau)")
    flow = lst(lay, "flowSummary")
    if len(flow) < m["flow"]:
        rep.add("FAIL", "C9", w, f"A·flowSummary: cần ≥ {m['flow']} bước dòng chảy, có {len(flow)}")
    for i, x in enumerate(flow):
        x = x if isinstance(x, dict) else {}
        for f in ("step", "fromTo", "amount", "essence"):
            if not isinstance(x.get(f), str) or not x.get(f).strip():
                rep.add("FAIL", "C9", w, f"A·flowSummary[{i}] thiếu `{f}`")
        if x.get("channel") not in CHANNELS:
            rep.add("FAIL", "C9", w, f"A·flowSummary[{i}].channel {x.get('channel')!r}: phải là wire (lời nhắn) · pipe (tiền thật) · book (ghi sổ)")
    roles, houses = lst(lay, "roles"), s.get("houses", [])
    if len(roles) != len(houses):
        rep.add("FAIL", "C9", w, f"A·roles: cần đúng {len(houses)} vai (một cho mỗi nhà), có {len(roles)}")
    for i, r in enumerate(roles):
        r = r if isinstance(r, dict) else {}
        if i < len(houses) and r.get("who") != houses[i].get("label"):
            rep.add("FAIL", "C9", w, f"A·roles[{i}].who '{r.get('who')}' ≠ nhãn nhà {i} '{houses[i].get('label')}'")
        for f in ("pays", "gains", "risk"):
            if not nwords(r.get(f)):
                rep.add("FAIL", "C9", w, f"A·roles[{i}].{f} rỗng — ai trả · ai hưởng · ai chịu rủi ro phải có chữ")
    for f, need in (("whenHelps", m["helps"]), ("whenTraps", m["traps"])):
        xs = lst(lay, f)
        if len(xs) < need or any(nwords(t) < m["when_words"] for t in xs):
            rep.add("FAIL", "C9", w, f"A·{f}: cần ≥ {need} dòng, mỗi dòng ≥ {m['when_words']} từ, có {len(xs)} dòng")
    tk = lst(lay, "takeaways")
    if len(tk) < m["takeaways"] or any(nwords(t) < m["takeaway_words"] for t in tk):
        rep.add("FAIL", "C9", w, f"A·takeaways: cần ≥ {m['takeaways']} câu, mỗi câu ≥ {m['takeaway_words']} từ")

    # PHẦN B — phân tích chuyên sâu cho người có chuyên môn
    mech = lst(pro, "mechanics")
    mw = nwords(*[x.get(f) for x in mech if isinstance(x, dict) for f in ("h", "p")])
    if len(mech) < m["mechanics"] or mw < m["mechanics_words"]:
        rep.add("FAIL", "C9", w, f"B·mechanics: cần ≥ {m['mechanics']} mục và ≥ {m['mechanics_words']} từ, có {len(mech)} mục · {mw} từ")
    notes = lst(pro, "accountingNotes")
    if len(notes) < m["acc_notes"] or nwords(*notes) < m["acc_words"]:
        rep.add("FAIL", "C9", w, f"B·accountingNotes: cần ≥ {m['acc_notes']} ghi chú và ≥ {m['acc_words']} từ, có {len(notes)} · {nwords(*notes)} từ")
    jr = lst(pro, "journal")
    if len(jr) < m["journal"]:
        rep.add("FAIL", "C9", w, f"B·journal: cần ≥ {m['journal']} bút toán từ phát sinh tới tất toán, có {len(jr)}")
    for i, e in enumerate(jr):
        if not isinstance(e, dict) or not e.get("step"):
            rep.add("FAIL", "C9", w, f"B·journal[{i}]: phải là object có `step`")
            continue
        check_ledger(e, f"bài '{k}' sổ sâu {i + 1}", tt99, rep)       # cùng luật C6: 6 cột, Σ Nợ = Σ Có, 1388≠131, TT 99 thứ cấp
    edges = lst(pro, "edgeCases")
    if len(edges) < m["edge"]:
        rep.add("FAIL", "C9", w, f"B·edgeCases: cần ≥ {m['edge']} tình huống ngoại lệ, có {len(edges)}")
    for i, x in enumerate(edges):
        x = x if isinstance(x, dict) else {}
        if not x.get("h") or nwords(x.get("p")) < m["edge_words"]:
            rep.add("FAIL", "C9", w, f"B·edgeCases[{i}]: cần tiêu đề `h` và ≥ {m['edge_words']} từ ở `p`, có {nwords(x.get('p'))}")
    texts = all_text(s) + article_text(s) + _walk(s.get("houses", []), [])
    if not any("ví dụ" in t for t in _walk(art, [])):
        rep.add("FAIL", "C9", w, "bài sâu không có chữ 'ví dụ' nào — số minh hoạ phải gắn nhãn (proxy yếu)")
    for rx, why in ((REG_RE, "trích điều luật / văn bản ngoài TT 99/2025 / URL — không có nguồn gốc trong repo"),
                    (BRAND_RE, "tên thương hiệu / nhãn hàng / công cụ / tên riêng có thật — LUẬT 4 & ONE-PAGER §3 cấm"),
                    (ADVICE_RE, "câu khuyên mua/vay/chọn — ONE-PAGER §3.2 cấm lời khuyên tài chính")):
        hits = sorted({mt.group(0) for t in texts for mt in rx.finditer(t)})
        if hits:
            rep.add("FAIL", "C9", w, f"grep: {why}: {', '.join(repr(h) for h in hits[:5])}")

    # PHẦN C — Studio Kịch bản Video 2 định dạng
    if "scenes" in vid:
        rep.add("FAIL", "C9", w, "C·videoScript.scenes là schema v1 — v2 dùng `long` + `short`")
    ln, lvo, lend = check_video("long", vid.get("long"), s, w, rep)
    sn, svo, send = check_video("short", vid.get("short"), s, w, rep)
    if sum(1 for r in rep.rows if r[0] == "FAIL") == n0:
        rep.add("PASS", "C9", w, f"C9 v2 đủ 3 trụ: A {len(myths)} lầm tưởng · {len(secs_)} chương {sw} từ · {len(flow)} bước dòng chảy · "
                f"{len(roles)} vai · {len(lst(lay, 'whenHelps'))}/{len(lst(lay, 'whenTraps'))} có lợi/thành bẫy · {len(tk)} câu hỏi"
                f" | B {len(mech)} cơ chế {mw} từ · {len(notes)} ghi chú {nwords(*notes)} từ · {len(jr)} bút toán · {len(edges)} ngoại lệ"
                f" | C dài {ln} cảnh · {lvo} từ · {mmss(lend)} — ngắn {sn} cảnh · {svo} từ · {mmss(send)}")


# ───────────────────── C8 — Scene Engine Sync & Governance Integrity ─────────────────────
# Vì sao có: repo này có .git riêng. Mở agent thẳng tại đây, hoặc clone riêng repo, thì luật/skill/hook
# của xưởng cha KHÔNG đi theo. C8 bảo đảm bộ luật nằm trong repo còn nguyên — nó kiểm SỰ CÓ MẶT và
# SỰ KHỚP NHAU, không chứng minh được agent nào đã đọc hay tuân theo chúng.
GOV_REQUIRED = [
    "CLAUDE.md", "GEMINI.md",
    "gates/01-spec/AGENT-CMS-PIPELINE.md",
    "gates/01-spec/VOICE-AND-PROSODY-SPEC.md",
    ".claude/rules/wms-pipeline-rules.md",
    ".claude/skills/vibe-post/SKILL.md",
    ".claude/commands/vibe/post.md",
    ".claude/agents/ke-toan-reviewer.md",
    ".claude/agents/tai-chinh-reviewer.md",
    ".claude/agents/brand-safety-reviewer.md",
    ".claude/settings.json",
    ".agents/skills/vibe-post/SKILL.md",
    ".agents/skills/ke-toan-reviewer/SKILL.md",
    ".agents/skills/tai-chinh-reviewer/SKILL.md",
    ".agents/skills/brand-safety-reviewer/SKILL.md",
    ".agents/hooks.json",
    "knowledge/finance-kb.json",
    "scripts/check-story.py", "scripts/wms-check.sh", "scripts/wms-hook-guard.sh",
    "scripts/wms-media-pipeline.py", "scripts/wms-finance-kb.py",
]
SHIP_ASK = ["Bash(git push:*)", "Bash(rtk git push:*)", "Bash(rtk proxy git push:*)",
            "Bash(gh pr merge:*)", "Bash(rtk gh pr merge:*)", "Bash(gh release:*)", "Bash(rtk gh release:*)",
            "Bash(vercel:*)", "Bash(npx vercel:*)", "Bash(netlify:*)", "Bash(npx netlify:*)",
            "Bash(wrangler:*)", "Bash(npx wrangler:*)",
            "Bash(youtube-upload:*)", "Bash(yt-upload:*)", "Bash(wms-youtube-upload:*)"]   # 16 mục (13 ship + 3 YouTube upload, QĐ 56)
HOOK_TOOLS = {"run_command", "edit_file", "write_file",
              "write_to_file", "replace_file_content", "multi_replace_file_content"}
SCENE_TAGS = ("SCENECSS", "SCENEJS")
KETOAN_COPIES = [
    ".claude/agents/ke-toan-reviewer.md",
    ".agents/skills/ke-toan-reviewer/SKILL.md",
    "../.claude/agents/ke-toan-reviewer.md",            # xưởng cha — chỉ có khi repo nằm trong Vibe/
    "../.agents/skills/ke-toan-reviewer/SKILL.md",
]
TAICHINH_COPIES = [
    ".claude/agents/tai-chinh-reviewer.md",
    ".agents/skills/tai-chinh-reviewer/SKILL.md",
    "../.claude/agents/tai-chinh-reviewer.md",          # xưởng cha — chỉ có khi repo nằm trong Vibe/
    "../.agents/skills/tai-chinh-reviewer/SKILL.md",
]
BRAND_SAFETY_COPIES = [
    ".claude/agents/brand-safety-reviewer.md",
    ".agents/skills/brand-safety-reviewer/SKILL.md",
    "../.claude/agents/brand-safety-reviewer.md",       # xưởng cha — chỉ có khi repo nằm trong Vibe/
    "../.agents/skills/brand-safety-reviewer/SKILL.md",
]


def scene_block(src: str, tag: str) -> str | None:
    m = re.search(rf"/\*{tag}:START.*?{tag}:END\*/", src, flags=re.S)
    return m.group() if m else None


def check_scene_blocks(src: str, label: str, rep: Report) -> None:
    """C8 — khối Scene dùng chung: đúng 1 START + 1 END, đúng thứ tự, không rỗng, nằm đúng chỗ."""
    ok = True
    for tag in SCENE_TAGS:
        starts = [m.start() for m in re.finditer(rf"/\*{tag}:START", src)]
        ends = [m.start() for m in re.finditer(rf"{tag}:END\*/", src)]
        if len(starts) != 1 or len(ends) != 1:
            rep.add("FAIL", "C8", label, f"{tag}: cần đúng 1 START và 1 END, gặp {len(starts)} START · {len(ends)} END")
            ok = False
            continue
        s, e = starts[0], ends[0]
        if s > e:
            rep.add("FAIL", "C8", label, f"{tag}: END đứng trước START")
            ok = False
            continue
        body = src[src.find("*/", s) + 2:e] if src.find("*/", s) < e else ""
        if not re.sub(r"/\*.*?\*/", "", body, flags=re.S).strip():
            rep.add("FAIL", "C8", label, f"{tag}: thân khối rỗng")
            ok = False
            continue
        if tag == "SCENECSS":
            inside = any(a.start() < s and e < a.end() for a in re.finditer(r"<style[^>]*>.*?</style>", src, flags=re.S))
            if not inside:
                rep.add("FAIL", "C8", label, "SCENECSS không nằm trọn trong một khối <style>")
                ok = False
        else:
            scripts = list(re.finditer(r"<script>(.*?)</script>", src, flags=re.S))
            if not scripts or not (scripts[-1].start() < s and e < scripts[-1].end()):
                rep.add("FAIL", "C8", label, "SCENEJS không nằm trọn trong khối <script> cuối (C0 sẽ không kiểm nó)")
                ok = False
            t = re.search(r"\bconst\s+TYPES\s*=", src)
            if not t or not (s < t.start() < e):
                rep.add("FAIL", "C8", label, "`const TYPES` (danh sách archetype hợp lệ) không nằm trong SCENEJS")
                ok = False
    if ok:
        rep.add("PASS", "C8", label, "SCENECSS + SCENEJS nguyên vẹn: 1 START · 1 END · đúng chỗ · TYPES trong SCENEJS")


def check_scene_sync(ref_src: str, ref_label: str, extra: list[pathlib.Path], rep: Report) -> None:
    """C8 — bản xem nhanh phải dùng đúng khối Scene của bản đầy đủ, từng byte."""
    def has_marker(p: pathlib.Path) -> bool:
        try:
            return "SCENECSS:START" in p.read_text(errors="replace")
        except OSError as e:                          # symlink hỏng, quyền đọc… ⇒ báo, không crash
            rep.add("FAIL", "C8", p.name, f"không đọc được để soát marker Scene: {e}")
            return False
    cands = [p for p in sorted((ROOT / "docs").glob("*.html"))
             if p.resolve() != DEFAULT_FILE.resolve() and has_marker(p)]
    cands += [p for p in extra if p not in cands]
    if not cands:
        rep.add("SKIP", "C8", "đồng bộ Scene",
                "không có bản xem nhanh nào TRONG repo (docs/*.html có marker) và không có --sync-with — chưa so được")
        return
    for p in cands:
        try:
            other = p.read_text(encoding="utf-8")
        except OSError as e:
            rep.add("FAIL", "C8", p.name, f"không đọc được bản xem nhanh: {e}")
            continue
        for tag in SCENE_TAGS:
            a, b = scene_block(ref_src, tag), scene_block(other, tag)
            if b is None:
                rep.add("FAIL", "C8", p.name, f"thiếu khối {tag}")
            elif a != b:
                rep.add("FAIL", "C8", p.name, f"{tag} lệch với {ref_label} — chép lại nguyên khối từ bản đầy đủ")
            else:
                rep.add("PASS", "C8", p.name, f"{tag} khớp từng byte với {ref_label}")


def _ketoan_core(text: str) -> str | None:
    m = re.search(r"^## Phạm vi", text, flags=re.M)     # heading ở ĐẦU DÒNG — comment giải thích cũng chứa chuỗi này
    if not m:
        return None
    i = m.start()
    # chuẩn hoá: tiền tố đường dẫn của xưởng cha và dấu backtick là định dạng, không phải nội dung
    return re.sub(r"\s+", " ", text[i:].replace("where-money-sleeps/", "").replace("`", "")).strip()


def check_governance(rep: Report) -> None:
    where = "repo"
    missing = [f for f in GOV_REQUIRED if not (ROOT / f).is_file() or (ROOT / f).stat().st_size == 0]
    for f in missing:
        rep.add("FAIL", "C8", where, f"thiếu hoặc rỗng: {f} — luật WMS không còn đi theo repo")
    if not missing:
        rep.add("PASS", "C8", where, f"{len(GOV_REQUIRED)}/{len(GOV_REQUIRED)} file luật & pipeline có mặt, không rỗng")

    # cổng ship của Claude Code
    try:
        ask = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))["permissions"]["ask"]
        lack = [x for x in SHIP_ASK if x not in ask]
        if lack:
            rep.add("FAIL", "C8", where, f".claude/settings.json thiếu permissions.ask: {', '.join(lack)}")
        else:
            rep.add("PASS", "C8", where, f"permissions.ask có đủ {len(SHIP_ASK)} mục lệnh ship (chỉ bắt tiền tố; không chạy ở bypass mode)")
    except (OSError, ValueError, KeyError, TypeError) as e:
        rep.add("FAIL", "C8", where, f".claude/settings.json không đọc được permissions.ask: {e!r}")

    # hook của Gemini / Antigravity
    try:
        hooks = json.loads((ROOT / ".agents/hooks.json").read_text(encoding="utf-8"))
        found = False
        for cfg in hooks.values():
            for ent in (cfg.get("PreToolUse") or []) if isinstance(cfg, dict) else []:
                tools = set(str(ent.get("matcher", "")).split("|"))
                for h in ent.get("hooks", []):
                    cmd = str(h.get("command", ""))
                    if not cmd.endswith("wms-hook-guard.sh"):
                        continue
                    found = True
                    target = (ROOT / ".agents" / cmd).resolve() if not cmd.startswith("/") else pathlib.Path(cmd)
                    if not target.is_file():
                        rep.add("FAIL", "C8", where, f"hooks.json trỏ '{cmd}' — giải từ .agents/ ra {target}, không tồn tại")
                    elif not os.access(target, os.X_OK):
                        rep.add("FAIL", "C8", where, f"{target.name} chưa có bit thực thi (chmod +x)")
                    else:
                        rep.add("PASS", "C8", where, f"hooks.json → {os.path.relpath(target, ROOT)} có và có bit thực thi (giải từ .agents/)")
                    if HOOK_TOOLS - tools:
                        rep.add("FAIL", "C8", where, f"matcher thiếu tool: {', '.join(sorted(HOOK_TOOLS - tools))}")
        if not found:
            rep.add("FAIL", "C8", where, ".agents/hooks.json không có PreToolUse nào gọi wms-hook-guard.sh")
    except (OSError, ValueError, AttributeError) as e:
        rep.add("FAIL", "C8", where, f".agents/hooks.json không đọc được: {e!r}")
    # Dòng này CỐ ĐỊNH, không bao giờ thành PASS: script không quan sát được Antigravity có chạy hook hay không.
    rep.add("WARN", "C8", where, "hook có thật sự chạy, gốc đường dẫn và tên tool của Antigravity: CHƯA XÁC MINH")

    # bản chép không được trôi
    a, b = ROOT / ".claude/skills/vibe-post/SKILL.md", ROOT / ".agents/skills/vibe-post/SKILL.md"
    if a.is_file() and b.is_file():
        if a.read_bytes() == b.read_bytes():
            rep.add("PASS", "C8", where, "vibe-post: bản .claude ≡ bản .agents (từng byte)")
        else:
            rep.add("FAIL", "C8", where, "vibe-post: bản .claude và .agents đã lệch — sửa một bản thì chép sang bản kia")
    cores, skipped = {}, []
    for rel in KETOAN_COPIES:
        p = ROOT / rel
        if not p.is_file():
            if rel.startswith(".."):
                skipped.append(rel)
            continue
        try:
            core = _ketoan_core(p.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            rep.add("FAIL", "C8", where, f"{rel}: không đọc được ({e})")
            continue
        if core is None:
            rep.add("FAIL", "C8", where, f"{rel}: thiếu mục '## Phạm vi' — không so được với các bản khác")
        else:
            cores[rel] = core
    if len(set(cores.values())) > 1:
        rep.add("FAIL", "C8", where, f"ke-toan-reviewer lệch giữa các bản (từ '## Phạm vi'): {', '.join(cores)}")
    elif cores:
        rep.add("PASS", "C8", where, f"ke-toan-reviewer khớp giữa {len(cores)} bản (bỏ qua tiền tố đường dẫn và backtick)")
    if skipped:
        rep.add("SKIP", "C8", where, "không thấy xưởng cha (repo đứng một mình) — chưa so ke-toan với bản của xưởng")

    tc_cores, tc_skipped = {}, []
    for rel in TAICHINH_COPIES:
        p = ROOT / rel
        if not p.is_file():
            if rel.startswith(".."):
                tc_skipped.append(rel)
            continue
        try:
            core = _ketoan_core(p.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            rep.add("FAIL", "C8", where, f"{rel}: không đọc được ({e})")
            continue
        if core is None:
            rep.add("FAIL", "C8", where, f"{rel}: thiếu mục '## Phạm vi' — không so được với các bản khác")
        else:
            tc_cores[rel] = core
    if len(set(tc_cores.values())) > 1:
        rep.add("FAIL", "C8", where, f"tai-chinh-reviewer lệch giữa các bản (từ '## Phạm vi'): {', '.join(tc_cores)}")
    elif tc_cores:
        rep.add("PASS", "C8", where, f"tai-chinh-reviewer khớp giữa {len(tc_cores)} bản (bỏ qua tiền tố đường dẫn và backtick)")
    if tc_skipped:
        rep.add("SKIP", "C8", where, "không thấy xưởng cha (repo đứng một mình) — chưa so tai-chinh với bản của xưởng")

    bs_cores, bs_skipped = {}, []
    for rel in BRAND_SAFETY_COPIES:
        p = ROOT / rel
        if not p.is_file():
            if rel.startswith(".."):
                bs_skipped.append(rel)
            continue
        try:
            core = _ketoan_core(p.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            rep.add("FAIL", "C8", where, f"{rel}: không đọc được ({e})")
            continue
        if core is None:
            rep.add("FAIL", "C8", where, f"{rel}: thiếu mục '## Phạm vi' — không so được với các bản khác")
        else:
            bs_cores[rel] = core
    if len(set(bs_cores.values())) > 1:
        rep.add("FAIL", "C8", where, f"brand-safety-reviewer lệch giữa các bản (từ '## Phạm vi'): {', '.join(bs_cores)}")
    elif bs_cores:
        rep.add("PASS", "C8", where, f"brand-safety-reviewer khớp giữa {len(bs_cores)} bản (bỏ qua tiền tố đường dẫn và backtick)")
    if bs_skipped:
        rep.add("SKIP", "C8", where, "không thấy xưởng cha (repo đứng một mình) — chưa so brand-safety với bản của xưởng")

    # đường dẫn chép từ xưởng mà quên đổi sang tương đối repo
    # settings.local.json do Claude Code tự sinh (đường dẫn tuyệt đối khi bấm "always allow") — không phải luật, bỏ qua
    def mentions_app_prefix(p: pathlib.Path) -> bool:
        try:
            return "where-money-sleeps/" in p.read_text(errors="replace")
        except OSError as e:
            rep.add("FAIL", "C8", where, f"không đọc được {p.relative_to(ROOT)}: {e}")
            return False
    stale = [str(p.relative_to(ROOT)) for d in (".claude", ".agents") for p in (ROOT / d).rglob("*")
             if p.is_file() and p.name != "settings.local.json" and mentions_app_prefix(p)]
    for f in stale:
        rep.add("FAIL", "C8", where, f"{f} còn đường dẫn 'where-money-sleeps/…' — trong repo phải là đường dẫn tương đối")


def check(src: str, label: str, rep: Report, only: str | None) -> dict:
    check_js_syntax(src, rep, label)
    check_scene_blocks(src, label, rep)          # chạy TRƯỚC extract: dữ liệu hỏng vẫn phải soát Scene
    try:
        gloss = extract(src, "GLOSS")
        stories = extract(src, "STORIES")
        cats = extract(src, "CATEGORIES")
        types = scene_types(src)
    except ValueError as e:
        rep.add("FAIL", "C-", label, f"không đọc được dữ liệu: {e}")
        return {}

    # C2b — bảng FX_BY_TYPE của script còn khớp code vẽ
    for t in sorted(types - FX_BY_TYPE.keys()):
        rep.add("WARN", "C2b", label, f"archetype '{t}' có trong Scene nhưng chưa có trong FX_BY_TYPE")
    for t, fxs in FX_BY_TYPE.items():
        for fx in sorted(fxs):
            if not re.search(rf'"data-fx":\s*"{fx}"|tagS\([^;\n]*?"{fx}"', src):
                rep.add("WARN", "C2b", label, f"fx '{fx}' ({t}) không thấy trong code vẽ — FX_BY_TYPE đã cũ?")

    # C1 — taxonomy 3 cấp
    cat_ids = [c.get("id") for c in cats]
    if len(set(cat_ids)) != len(cat_ids):
        rep.add("FAIL", "C1", label, "id danh mục bị trùng")
    topic_refs: dict[str, int] = {}
    for ci, c in enumerate(cats, 1):
        if not c.get("id") or not c.get("name") or not c.get("topics"):
            rep.add("FAIL", "C1", f"danh mục {ci}", "thiếu id/name/topics")
            continue
        # màu đi thẳng vào style="--c:…" — chỉ nhận mã hex, chặn chèn thuộc tính
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(c.get("c", ""))):
            rep.add("FAIL", "C1", f"danh mục {ci}", f"màu `c` phải là #rrggbb, gặp {c.get('c')!r}")
        if not re.fullmatch(r"[a-z0-9_-]+", str(c["id"])):
            rep.add("FAIL", "C1", f"danh mục {ci}", f"id chỉ dùng a-z 0-9 _ -, gặp {c['id']!r}")
        for ti, tp in enumerate(c["topics"], 1):
            w = f"{c['id']} chủ đề {ti}/{len(c['topics'])}"
            if "story" in tp:
                k = tp["story"]
                topic_refs[k] = topic_refs.get(k, 0) + 1
                if k not in stories:
                    rep.add("FAIL", "C1", w, f"trỏ tới bài '{k}' không có trong STORIES")
                elif stories[k].get("category") != c["id"]:
                    rep.add("FAIL", "C1", w, f"bài '{k}' khai category '{stories[k].get('category')}' nhưng nằm ở {c['id']}")
            else:
                if not tp.get("t"):
                    rep.add("FAIL", "C1", w, "chủ đề chưa có bài phải có tiêu đề `t`")
                if tp.get("status") != "upcoming":
                    rep.add("FAIL", "C1", w, "chủ đề chưa có bài phải mang status 'upcoming'")

    ctx = {"types": types, "gloss": gloss, "cat_ids": cat_ids, "tt99": load_tt99(), "topic_refs": topic_refs}
    if ctx["tt99"] is None:
        rep.add("WARN", "C6", label, "không đọc được legal/tt99-phu-luc-ii.secondary.json — chưa đối chiếu tên TK")
    if only and only not in stories:
        rep.add("FAIL", "C-", label, f"không có bài '{only}' trong STORIES")
    for k, s in stories.items():
        if not re.fullmatch(r"[a-z0-9_]+", k):
            rep.add("FAIL", "C1", f"bài '{k}'", "khoá bài chỉ dùng a-z 0-9 _ (đi thẳng vào data-story=\"…\")")
        if not only or k == only:
            check_story(k, s, ctx, rep)
    if not only:
        meta_hits = sorted({mt.group(0) for t in _walk(gloss, []) + _walk(cats, []) for mt in BRAND_RE.finditer(t)})
        if meta_hits:
            rep.add("FAIL", "C9", f"{label} GLOSS/CATEGORIES",
                    f"grep: tên thương hiệu / nhãn hàng / tên riêng có thật (LUẬT 4): {', '.join(repr(h) for h in meta_hits[:5])}")
    if not any(s.get("status") == "published" for s in stories.values()):
        rep.add("WARN", "C7", label, "không còn bài nào 'published' — người đọc thường sẽ thấy trang trống")

    n = {"published": 0, "review": 0, "upcoming": 0}
    for c in cats:
        for tp in c.get("topics", []):
            st = stories.get(tp["story"], {}).get("status") if "story" in tp else tp.get("status")
            n[st if st in n else "upcoming"] += 1
    return {"cats": len(cats), "topics": sum(len(c.get("topics", [])) for c in cats), **n}


def main() -> int:
    ap = argparse.ArgumentParser(description="Kiểm tất định dữ liệu bài (GLOSS/STORIES/CATEGORIES) trong file HTML.")
    ap.add_argument("--file", action="append", type=pathlib.Path, help="file HTML chứa GLOSS/STORIES/CATEGORIES (lặp được)")
    ap.add_argument("--story", help="chỉ kiểm một bài theo khoá trong STORIES")
    ap.add_argument("--quiet", action="store_true", help="chỉ in FAIL/WARN")
    ap.add_argument("--sync-with", action="append", type=pathlib.Path, default=[],
                    help="bản xem nhanh (ngoài docs/) phải có khối SCENECSS/SCENEJS giống bản đầy đủ (C8)")
    a = ap.parse_args()
    any_fail = False

    def show(rep: Report) -> None:
        for level, code, where, msg in rep.rows:
            if a.quiet and level in ("PASS", "SECONDARY", "SKIP"):
                continue
            print(f"{level:<9} {code:<4} {where:<30} {msg}")
        cnt = {lv: sum(1 for r in rep.rows if r[0] == lv) for lv in ("FAIL", "WARN", "SECONDARY", "PASS", "SKIP")}
        print("Kết quả: " + " · ".join(f"{k} {v}" for k, v in cnt.items()))

    # C8 — chạy một lần, KHÔNG phụ thuộc dữ liệu bài parse được hay không
    gov = Report()
    check_governance(gov)
    try:
        check_scene_sync(DEFAULT_FILE.read_text(encoding="utf-8"), DEFAULT_FILE.name, a.sync_with, gov)
    except OSError as e:
        gov.add("FAIL", "C8", "đồng bộ Scene", f"không đọc được bản đầy đủ {DEFAULT_FILE}: {e}")
    print(f"── C8 governance · {ROOT}")
    show(gov)
    any_fail |= gov.has_fail()

    for f in a.file or [DEFAULT_FILE]:
        rep = Report()
        try:
            src = f.read_text(encoding="utf-8")
        except OSError as e:
            print(f"FAIL      {f}: {e}")
            any_fail = True
            continue
        summary = check(src, f.name, rep, a.story)
        print(f"── {f}")
        for level, code, where, msg in rep.rows:
            if a.quiet and level in ("PASS", "SECONDARY", "SKIP"):
                continue
            print(f"{level:<9} {code:<4} {where:<30} {msg}")
        if summary:
            print(f"Tổng kho: {summary['cats']} danh mục · {summary['topics']} chủ đề — "
                  f"{summary['published']} đã đăng · {summary['review']} chờ duyệt · {summary['upcoming']} đang biên soạn")
        cnt = {lv: sum(1 for r in rep.rows if r[0] == lv) for lv in ("FAIL", "WARN", "SECONDARY", "PASS", "SKIP")}
        print("Kết quả: " + " · ".join(f"{k} {v}" for k, v in cnt.items()))
        any_fail |= rep.has_fail()
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
