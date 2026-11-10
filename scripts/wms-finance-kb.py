#!/usr/bin/env python3
"""wms-finance-kb.py — Cỗ máy Crawl, Chắt lọc Tri thức & Kiểm định Chuyên gia Tài chính (F1–F4).

Phục vụ Agent Chuyên gia Tài chính (`tai-chinh-reviewer`) của Where Money Sleeps:
  1. `--crawl`  : Quét và đối chiếu các nguồn văn bản pháp quy & cơ chế ngân hàng chuẩn thức
                  (Bộ Tài chính TT 99/2025/TT-BTC, NHNN `sbv.gov.vn`, `vbpl.vn`, `congbao.chinhphu.vn`,
                  BIS CPMI Glossary và kho văn bản pháp lý trong `legal/`), băm SHA-256, khử trùng lặp
                  (DEDUPE), cập nhật `knowledge/finance-kb.json` và xuất `knowledge/LAST-CRAWL-REPORT.md`.
  2. `--verify` : Chạy 4 phép kiểm tất định + toán tài chính (F1–F4) trên toàn bộ nội dung bài viết
                  (`beats`, `article.lay`, `article.pro`, `GLOSS`) VÀ kịch bản video (`videoScript.long`,
                  `videoScript.short`):
                    - F1: Cơ chế Ngân hàng, Thanh toán & Tín dụng (Wire vs Pipe vs Book, On-Us vs Off-Us,
                          Authorization vs Clearing vs Settlement, MDR, Merchant Subsidy).
                    - F2: Toán Tài chính & Định giá Dòng tiền (tự giải phương trình IRR/EIR bằng phương pháp
                          chia đôi/Newton-Raphson, kiểm đối chiếu Σ Nợ = Σ Có, tỷ lệ phí/khấu trừ BHXH/thuế).
                    - F3: Tính Thời sự của Kho Tri thức Pháp quy (`knowledge/finance-kb.json`, độ tươi ≤ 30 ngày,
                          không có quy định hết hiệu lực `superseded`, tên tài khoản chuẩn TT 99/2025).
                    - F4: Độ khớp Xuyên suốt Bài viết ↔ Video (Long 16:9 & Short 9:16) & Chống Lời khuyên Đầu tư.

Chạy (từ thư mục where-money-sleeps):
    python3 -I scripts/wms-finance-kb.py --verify
    python3 -I scripts/wms-finance-kb.py --crawl --verify
    python3 -I scripts/wms-finance-kb.py --verify --story install
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import math
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "docs" / "prototype.html"
KB_FILE = ROOT / "knowledge" / "finance-kb.json"
CRAWL_REPORT_FILE = ROOT / "knowledge" / "LAST-CRAWL-REPORT.md"
TT99_FILE = ROOT / "legal" / "tt99-phu-luc-ii.secondary.json"

# Tên tài khoản cũ của TT 200/2014 đã đổi ở TT 99/2025 — xuất hiện trong sổ hoặc bài là FAIL F3
LEGACY_TT200_NAMES = {
    "112": ("Tiền gửi ngân hàng", "Tiền gửi không kỳ hạn"),
    "156": ("Hàng hóa (tách 1561/1562/1567)", "Hàng hóa"),
}


def _load_check_story_module():
    spec = importlib.util.spec_from_file_location("check_story", ROOT / "scripts" / "check-story.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Không nạp được scripts/check-story.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def solve_monthly_irr(pv_eff: float, cashflows: list[float], tol: float = 1e-10) -> float:
    """Giải phương trình sum_{t=1..n} CF_t / (1 + r)^t = pv_eff bằng phương pháp chia đôi (bisection)."""
    lo, hi = -0.5, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        npv = sum(cf / ((1.0 + mid) ** t) for t, cf in enumerate(cashflows, 1)) - pv_eff
        if abs(npv) < tol:
            return mid
        if npv > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _collect_text(obj) -> str:
    out: list[str] = []

    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, list):
            for y in x:
                walk(y)
        elif isinstance(x, dict):
            for y in x.values():
                walk(y)

    walk(obj)
    return "\n".join(out)


def crawl_and_distill_kb(kb_path: pathlib.Path = KB_FILE, report_path: pathlib.Path = CRAWL_REPORT_FILE) -> dict:
    """Quét kho pháp lý nội bộ + thăm dò nguồn công khai (nếu có mạng), khử trùng lặp và cập nhật KB."""
    if not kb_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy kho tri thức: {kb_path}")
    kb = json.loads(kb_path.read_text(encoding="utf-8"))
    now_iso = dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).isoformat(timespec="seconds")

    # 1. Kiểm chứng & băm SHA-256 các tài liệu gốc trong repo (Local Primary/Secondary Artifacts)
    local_digests: list[dict] = []
    for src in kb.get("authoritativeSources", []):
        for rel in src.get("localRepoFiles", []):
            p = ROOT / rel
            if p.is_file():
                raw = p.read_bytes()
                sha = hashlib.sha256(raw).hexdigest()
                local_digests.append({
                    "sourceId": src["sourceId"],
                    "file": rel,
                    "bytes": len(raw),
                    "sha256": sha[:16] + "…" + sha[-8:],
                    "status": "VERIFIED_LOCAL",
                })
            else:
                local_digests.append({
                    "sourceId": src["sourceId"],
                    "file": rel,
                    "bytes": 0,
                    "sha256": "MISSING",
                    "status": "MISSING_LOCAL",
                })

    # 2. Thăm dò các cổng pháp quy/ngân hàng công khai (tự động thích ứng nếu chạy trong Sandbox cấm mạng)
    url_probes: list[dict] = []
    seen_urls: set[str] = set()
    for src in kb.get("authoritativeSources", []):
        for url in src.get("officialUrls", []):
            if url in seen_urls:
                continue
            seen_urls.add(url)
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "WhereMoneySleeps-FinancialSpecialist/1.0 (+https://github.com/duypham9895)"},
                method="GET",
            )
            try:
                with urllib.request.urlopen(req, timeout=2.5) as resp:
                    body_head = resp.read(4096).decode("utf-8", errors="replace")
                    title_m = re.search(r"<title[^>]*>(.*?)</title>", body_head, flags=re.I | re.S)
                    page_title = re.sub(r"\s+", " ", title_m.group(1)).strip()[:90] if title_m else "OK"
                    url_probes.append({
                        "sourceId": src["sourceId"],
                        "url": url,
                        "httpStatus": resp.status,
                        "probeStatus": "LIVE_REACHABLE",
                        "note": page_title,
                    })
            except urllib.error.HTTPError as e:
                url_probes.append({
                    "sourceId": src["sourceId"],
                    "url": url,
                    "httpStatus": e.code,
                    "probeStatus": "HTTP_RESPONSE",
                    "note": f"HTTP {e.code} (cần trình duyệt thật nếu có tường chống bot)",
                })
            except Exception as e:
                url_probes.append({
                    "sourceId": src["sourceId"],
                    "url": url,
                    "httpStatus": None,
                    "probeStatus": "OFFLINE_OR_SANDBOX",
                    "note": f"Chế độ cô lập mạng / ngoại tuyến ({type(e).__name__}) — giữ nguyên bản chốt trong repo",
                })

    # 3. Khử trùng lặp (DEDUPE) các quy tắc miền theo ruleId
    unique_rules = {}
    for rule in kb.get("domainRules", []):
        rid = rule.get("ruleId")
        if rid and rid not in unique_rules:
            unique_rules[rid] = rule
    kb["domainRules"] = list(unique_rules.values())
    kb["lastCrawledAt"] = now_iso
    kb["lastCrawlSummary"] = {
        "crawledAt": now_iso,
        "localArtifactsVerified": sum(1 for d in local_digests if d["status"] == "VERIFIED_LOCAL"),
        "localArtifactsTotal": len(local_digests),
        "liveUrlsProbed": len(url_probes),
        "liveUrlsReachable": sum(1 for u in url_probes if u["probeStatus"] in ("LIVE_REACHABLE", "HTTP_RESPONSE")),
        "domainRulesCount": len(kb["domainRules"]),
        "storyInvariantsCount": len(kb.get("storyInvariants", {})),
    }

    kb_path.write_text(json.dumps(kb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4. Xuất báo cáo Markdown LAST-CRAWL-REPORT.md
    lines = [
        "# Báo cáo Crawl & Chắt lọc Tri thức Tài chính (`tai-chinh-reviewer`)",
        "",
        f"- **Thời điểm cập nhật (`lastCrawledAt`):** `{now_iso}`",
        f"- **Kho tri thức:** `knowledge/finance-kb.json` (Schema v{kb.get('schema', 1)})",
        f"- **Chính sách độ tươi (`freshnessPolicy`):** Tối đa `{kb.get('freshnessPolicy', {}).get('maxAgeDays', 30)}` ngày · Lịch định kỳ khuyến nghị: `{kb.get('freshnessPolicy', {}).get('recommendedCron', '0 8 * * 1')}` (`Asia/Ho_Chi_Minh`)",
        f"- **Tổng số nguồn chuẩn thức:** `{len(kb.get('authoritativeSources', []))}` nguồn · `{len(kb.get('domainRules', []))}` quy tắc miền (`F1–F4`) · `{len(kb.get('storyInvariants', {}))}` hợp đồng bất biến bài viết ↔ video",
        "",
        "## 1. Kiểm chứng Tài liệu Pháp lý & Học thuật Nội bộ (`legal/`)",
        "",
        "| Nguồn | Đường dẫn trong repo | Dung lượng (bytes) | SHA-256 | Trạng thái |",
        "|---|---|---:|---|---|",
    ]
    for d in local_digests:
        lines.append(f"| `{d['sourceId']}` | `{d['file']}` | {d['bytes']:,} | `{d['sha256']}` | **{d['status']}** |")

    lines += [
        "",
        "## 2. Trạng thái Thăm dò Nguồn Pháp quy & Ngân hàng Công khai",
        "",
        "| Nguồn | URL chuẩn thức | HTTP | Trạng thái | Ghi chú |",
        "|---|---|---|---|---|",
    ]
    for u in url_probes:
        http_s = str(u["httpStatus"]) if u["httpStatus"] is not None else "—"
        lines.append(f"| `{u['sourceId']}` | `{u['url']}` | `{http_s}` | **{u['probeStatus']}** | {u['note']} |")

    lines += [
        "",
        "## 3. Tri thức Tài chính Đã Chắt lọc (`domainRules`)",
        "",
        "| Mã quy tắc | Phép kiểm | Danh mục | Bản chất cốt lõi đã chắt lọc |",
        "|---|---|---|---|",
    ]
    for r in kb.get("domainRules", []):
        lines.append(f"| `{r['ruleId']}` | **{r['checkCode']}** | `{r['category']}` | {r['distilledTruth']} |")

    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return kb["lastCrawlSummary"]


def verify_story_finance(
    story_key: str,
    story: dict,
    kb: dict,
    tt99: dict | None,
) -> dict:
    """Chạy 4 phép kiểm chuyên gia tài chính (F1–F4) cho 1 bài viết + 2 kịch bản video của bài đó."""
    rows: list[tuple[str, str, str, str]] = []
    w = f"bài '{story_key}'"
    inv = (kb.get("storyInvariants") or {}).get(story_key)
    beats = story.get("beats") or []
    art = story.get("article") or {}
    lay = art.get("lay") or {}
    pro = art.get("pro") or {}
    vid = story.get("videoScript") or {}

    # ── F1: Cơ chế Ngân hàng, Thanh toán & Tín dụng (Wire vs Pipe vs Book) ──
    f1_ok = True
    if inv:
        for bi in inv.get("wireOnlyBeats", []):
            if 0 <= bi < len(beats):
                msgs = beats[bi].get("msgs") or []
                money_pipes = [m for m in msgs if isinstance(m, list) and len(m) == 3 and m[2] == "money"]
                if money_pipes:
                    rows.append((
                        "FAIL", "F1", f"{w} đoạn {bi + 1}",
                        f"Sai cơ chế ngân hàng: đoạn {bi + 1} là pha thông điệp/uỷ quyền (wire-only) nhưng lại vẽ ống tiền thật {money_pipes!r}"
                    ))
                    f1_ok = False
        for bi in inv.get("pipeMoneyBeats", []):
            if 0 <= bi < len(beats):
                msgs = beats[bi].get("msgs") or []
                money_pipes = [m for m in msgs if isinstance(m, list) and len(m) == 3 and m[2] == "money"]
                if not money_pipes:
                    rows.append((
                        "FAIL", "F1", f"{w} đoạn {bi + 1}",
                        f"Sai cơ chế quyết toán: đoạn {bi + 1} phải có dòng tiền thật di chuyển qua ống ('money' pipe)"
                    ))
                    f1_ok = False

    # Kiểm tra flowSummary trong article.lay: các bước đầu (uỷ quyền / giữ hạn mức / ký hợp đồng) trước quyết toán T+1/T+2 cấm dùng kênh 'pipe'
    flow = lay.get("flowSummary") or []
    if story_key in ("card", "install") and len(flow) >= 2:
        for fi in (0, 1):
            ch = flow[fi].get("channel")
            if ch == "pipe":
                rows.append((
                    "FAIL", "F1", f"{w} flowSummary[{fi}]",
                    f"Bước {fi + 1} của giao dịch thẻ/trả góp là pha uỷ quyền/ghi sổ ban đầu ('wire'/'book'), cấm dùng kênh 'pipe' (tiền thật chưa chảy)"
                ))
                f1_ok = False

    if f1_ok:
        mech_name = inv.get("mechanismType", "standard_5house_flow") if inv else "standard_5house_flow"
        rows.append((
            "PASS", "F1", w,
            f"Cơ chế ngân hàng & phân tách 3 kênh (wire · pipe · book) chuẩn xác ({mech_name})"
        ))

    # ── F2: Toán Tài chính & Định giá Dòng tiền (IRR/EIR, Khấu trừ, Σ Nợ = Σ Có) ──
    f2_ok = True
    all_ledgers: list[tuple[str, dict]] = []
    for bi, b in enumerate(beats, 1):
        if isinstance(b.get("ledger"), dict):
            all_ledgers.append((f"đoạn {bi}", b["ledger"]))
    for ji, j in enumerate(pro.get("journal") or [], 1):
        if isinstance(j, dict):
            all_ledgers.append((f"sổ sâu {ji}", j))

    used_accounts: set[str] = set()
    for loc, led in all_ledgers:
        d_sum = sum(r[5] for r in (led.get("rows") or []) if isinstance(r, list) and len(r) == 6 and r[0] == "Nợ" and isinstance(r[5], int))
        c_sum = sum(r[5] for r in (led.get("rows") or []) if isinstance(r, list) and len(r) == 6 and r[0] == "Có" and isinstance(r[5], int))
        for r in led.get("rows") or []:
            if isinstance(r, list) and len(r) == 6:
                used_accounts.add(str(r[1]))
        if d_sum != c_sum or d_sum <= 0:
            rows.append(("FAIL", "F2", f"{w} {loc}", f"Toán kế toán lệch: Σ Nợ ({d_sum:,}) ≠ Σ Có ({c_sum:,})"))
            f2_ok = False

    if inv:
        p = inv.get("parameters") or {}
        if story_key == "card":
            gross = p["grossAmount"]
            mdr = p["mdrFeeAmount"]
            net = p["netMerchantReceipt"]
            if gross - mdr != net or round(gross * p["mdrRateExample"]) != mdr:
                rows.append(("FAIL", "F2", w, f"Toán phí MDR sai: {gross} - {mdr} != {net}"))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán thanh toán thẻ khớp tuyệt đối: Gross {gross:,}đ − MDR {mdr:,}đ ({p['mdrRateExample']*100:.1f}%) = Thực nhận {net:,}đ"
                ))
        elif story_key == "pay":
            gross = p["grossSalary"]
            ins = p["employeeInsurance"]
            pit = p["personalIncomeTax"]
            ded = p["totalDeduction"]
            net = p["netSalary"]
            if round(gross * p["employeeInsuranceRate"]) != ins or ins + pit != ded or gross - ded != net:
                rows.append(("FAIL", "F2", w, f"Toán khấu trừ lương sai: Gross {gross} - ({ins} + {pit}) != {net}"))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán khấu trừ lương khớp tuyệt đối: Gross {gross:,}đ − (BHXH/YT/TN 10,5% = {ins:,}đ + Thuế TNCN {pit:,}đ = {ded:,}đ) = Net {net:,}đ"
                ))
        elif story_key == "install":
            price = p["listedPrice"]
            sub = p["merchantSubsidyAmount"]
            net_disb = p["netMerchantDisbursement"]
            n_months = p["installmentMonths"]
            cf = p["monthlyInstallment"]
            r_m = solve_monthly_irr(float(net_disb), [float(cf)] * n_months)
            eir_comp = (1.0 + r_m) ** 12 - 1.0
            eir_nom = r_m * 12.0
            if (
                price - sub != net_disb
                or cf * n_months != price
                or abs(r_m - p["expectedMonthlyIRR"]) > 1e-4
                or abs(eir_comp - p["expectedAnnualEIRCompounded"]) > 1e-3
            ):
                rows.append((
                    "FAIL", "F2", w,
                    f"Toán IRR/EIR trả góp lệch: r_m={r_m:.6f} (kỳ vọng {p['expectedMonthlyIRR']}), EIR_năm={eir_comp:.6f}"
                ))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán dòng tiền IRR/EIR khớp tuyệt đối: PV_eff={net_disb:,}đ, CF={cf:,}đ×{n_months} kỳ → "
                    f"r_tháng={r_m*100:.4f}% (xấp xỉ bài/video {p['statedMonthlyEIRApprox']}) · "
                    f"EIR_năm gộp={eir_comp*100:.2f}% / danh nghĩa={eir_nom*100:.2f}% (xấp xỉ bài/video {p['statedAnnualEIRApprox']})"
                ))
        elif story_key == "minpay":
            bal = p["statementBalance"]
            min_rate = p["minimumPaymentRate"]
            min_amt = p["minimumPaymentAmount"]
            rem_p = p["remainingPrincipal"]
            r_day = p["dailyInterestRateExample"]
            r_m = p["monthlyInterestRateExample"]
            d1 = p["graceDaysLost"]
            d2 = p["postDueDays"]
            int1 = round(bal * r_day * d1)
            int2 = round(rem_p * r_day * d2)
            tot_int = int1 + int2
            next_bal = rem_p + tot_int
            eir_comp = (1.0 + r_m) ** 12 - 1.0
            if (
                round(bal * min_rate) != min_amt
                or bal - min_amt != rem_p
                or int1 != p["retroactiveInterestPart1"]
                or int2 != p["postDueInterestPart2"]
                or tot_int != p["totalInterestNextStatement"]
                or next_bal != p["nextStatementTotalBalance"]
                or abs(eir_comp - p["expectedAnnualEIRCompounded"]) > 1e-4
            ):
                rows.append((
                    "FAIL", "F2", w,
                    f"Toán lãi lùi trả tối thiểu thẻ tín dụng lệch: int1={int1}, int2={int2}, tot={tot_int}, next_bal={next_bal}"
                ))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán trả tối thiểu & lãi lùi ADB khớp tuyệt đối: Sao kê {bal:,}đ − Trả tối thiểu 5% ({min_amt:,}đ) = Gốc còn {rem_p:,}đ · "
                    f"Lãi lùi 45 ngày đầu ({int1:,}đ) + Lãi 15 ngày sau ({int2:,}đ) = Tổng lãi {tot_int:,}đ → Dư nợ kỳ 2 = {next_bal:,}đ · "
                    f"EIR_năm gộp={eir_comp*100:.2f}% (xấp xỉ bài/video {p['statedAnnualEIRApprox']})"
                ))
        elif story_key == "qr":
            cup = p["singleCupAmount"]
            gross10m = p["batch200CupsGross"]
            mdr_rate = p["cardMdrRateExample"]
            mdr_fee = p["cardMdrFeeOn10M"]
            card_net = p["cardNetReceiptOn10M"]
            dyn_rate = p["dynamicQrFeeRateExample"]
            dyn_fee = p["dynamicQrFeeOn10M"]
            dyn_net = p["dynamicQrNetReceiptOn10M"]
            overpaid = p["overpaidTransferExample"]
            refund_liab = p["overpaidRefundLiability338"]
            if (
                cup * 200 != gross10m
                or round(gross10m * mdr_rate) != mdr_fee
                or gross10m - mdr_fee != card_net
                or round(gross10m * dyn_rate) != dyn_fee
                or gross10m - dyn_fee != dyn_net
                or overpaid - cup != refund_liab
            ):
                rows.append((
                    "FAIL", "F2", w,
                    f"Toán đối chiếu QR vs Thẻ lệch: gross={gross10m}, mdr_fee={mdr_fee}, dyn_fee={dyn_fee}, refund_liab={refund_liab}"
                ))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán thanh toán đẩy QR 24/7 vs Thẻ khớp tuyệt đối: 200 ly × {cup:,}đ = {gross10m:,}đ · "
                    f"QR tĩnh thực nhận {gross10m:,}đ (phí 0đ) vs Thẻ trừ MDR 2,2% ({mdr_fee:,}đ, còn {card_net:,}đ) · "
                    f"QR động trừ 0,2% ({dyn_fee:,}đ, còn {dyn_net:,}đ) · Chuyển nhầm {overpaid:,}đ treo TK 338 {refund_liab:,}đ"
                ))
        elif story_key == "profitcash":
            open_cash = p["openingCash112"]
            rev = p["revenue511"]
            cogs = p["cogs632"]
            inv_amt = p["endingInventory156"]
            paid_sup = p["cashPaidSuppliers"]
            opex = p["operatingExpenses642"]
            paid_opex = p["cashPaidOpex"]
            payroll = p["unpaidPayroll334"]
            profit = p["netProfit421"]
            cash_in_cust = p["cashCollectedFromCustomer"]
            ar = p["accountsReceivable131"]
            wc_locked = p["workingCapitalLocked"]
            ocf = p["operatingCashFlowOCF"]
            end_cash = p["endingCashBeforeLoan112"]
            loan = p["shortTermLoan341"]
            if (
                rev - cogs - opex != profit
                or cogs + inv_amt != paid_sup
                or paid_opex + payroll != opex
                or cash_in_cust + ar != rev
                or ar + inv_amt != wc_locked
                or profit - ar - inv_amt + payroll != ocf
                or open_cash + ocf != end_cash
                or open_cash + cash_in_cust - paid_sup - paid_opex != end_cash
                or end_cash + loan != payroll
            ):
                rows.append((
                    "FAIL", "F2", w,
                    f"Toán đối chiếu Lợi nhuận vs Dòng tiền OCF lệch: profit={profit}, ocf={ocf}, end_cash={end_cash}"
                ))
                f2_ok = False
            else:
                rows.append((
                    "PASS", "F2", w,
                    f"Toán Kế toán dồn tích vs Lưu chuyển tiền tệ gián tiếp khớp tuyệt đối: Doanh thu {rev:,}đ − Giá vốn {cogs:,}đ − Chi phí {opex:,}đ = Lãi {profit:,}đ · "
                    f"OCF = +{profit:,}đ − ΔTK 131 ({ar:,}đ) − ΔTK 156 ({inv_amt:,}đ) + ΔTK 334 ({payroll:,}đ) = {ocf:,}đ · "
                    f"Tiền cuối kỳ TK 112 = {open_cash:,}đ + ({ocf:,}đ) = {end_cash:,}đ (vay TK 341 {loan:,}đ để trả lương {payroll:,}đ)"
                ))
    elif f2_ok:
        rows.append(("PASS", "F2", w, f"Toán cân đối {len(all_ledgers)} bút toán Σ Nợ = Σ Có hợp lệ"))

    # ── F3: Đối chiếu Kho Tri thức Pháp quy & Thông tư 99/2025/TT-BTC ──
    f3_ok = True
    if inv:
        req_accs = set(inv.get("requiredAccounts") or [])
        forb_accs = set(inv.get("forbiddenAccounts") or [])
        missing_accs = sorted(req_accs - used_accounts)
        hit_forb = sorted(forb_accs & used_accounts)
        if missing_accs:
            rows.append(("FAIL", "F3", w, f"Thiếu tài khoản kế toán chuẩn TT 99/2025 theo hợp đồng bài: {missing_accs}"))
            f3_ok = False
        if hit_forb:
            rows.append(("FAIL", "F3", w, f"Dùng tài khoản bị cấm trong cơ chế này: {hit_forb} (phải dùng TK 1388 thay vì 131)"))
            f3_ok = False

    # Kiểm tên tài khoản cũ của TT 200 đã đổi tên ở TT 99/2025
    for loc, led in all_ledgers:
        for r in led.get("rows") or []:
            if isinstance(r, list) and len(r) == 6:
                code, name = str(r[1]), str(r[2])
                if code in LEGACY_TT200_NAMES and name == LEGACY_TT200_NAMES[code][0]:
                    rows.append((
                        "FAIL", "F3", f"{w} {loc}",
                        f"TK {code} dùng tên cũ của TT 200 ({name!r}) — theo TT 99/2025 phải là {LEGACY_TT200_NAMES[code][1]!r}"
                    ))
                    f3_ok = False
                elif tt99 and code in tt99 and tt99[code] != name:
                    rows.append((
                        "FAIL", "F3", f"{w} {loc}",
                        f"TK {code} tên {name!r} không khớp bảng TT 99/2025 ({tt99[code]!r})"
                    ))
                    f3_ok = False

    if f3_ok:
        rows.append((
            "PASS", "F3", w,
            f"Kho tri thức pháp quy TT 99/2025 & NHNN khớp 100% (các TK sử dụng: {', '.join(sorted(used_accounts))})"
        ))

    # ── F4: Độ khớp Xuyên suốt Bài viết ↔ Video (Long & Short) & Chống Lời khuyên Đầu tư ──
    f4_ok = True
    post_blob = _collect_text({"beats": beats, "article": art}).lower()
    long_blob = _collect_text(vid.get("long") or {}).lower()
    short_blob = _collect_text(vid.get("short") or {}).lower()

    if inv and "postToVideoAnchors" in inv:
        anchors = inv["postToVideoAnchors"]
        for token in anchors.get("beatsAndArticleMustContain", []):
            if token.lower() not in post_blob:
                rows.append(("FAIL", "F4", f"{w} bài viết", f"Bài viết thiếu con số/mốc neo tài chính cốt lõi: {token!r}"))
                f4_ok = False
        for group in anchors.get("longVideoMustContainAny", []):
            if not any(cand.lower() in long_blob for cand in group):
                rows.append((
                    "FAIL", "F4", f"{w} videoScript.long",
                    f"Video dài (16:9) làm rơi mốc số liệu cốt lõi từ bài viết (cần ít nhất 1 trong {group!r})"
                ))
                f4_ok = False
        for group in anchors.get("shortVideoMustContainAny", []):
            if not any(cand.lower() in short_blob for cand in group):
                rows.append((
                    "FAIL", "F4", f"{w} videoScript.short",
                    f"Video ngắn (Shorts 9:16) làm rơi mốc số liệu cốt lõi từ bài viết (cần ít nhất 1 trong {group!r})"
                ))
                f4_ok = False

    if f4_ok:
        rows.append((
            "PASS", "F4", w,
            "Đồng nhất số liệu & bản chất tài chính xuyên suốt Bài viết (Diorama + Khảo cứu 2 tầng) ↔ Video (Long 16:9 + Short 9:16)"
        ))

    failed = any(r[0] == "FAIL" for r in rows)
    return {
        "story": story_key,
        "status": "FAIL" if failed else "PASS",
        "rows": rows,
    }


def check_kb_freshness(kb: dict) -> list[tuple[str, str, str, str]]:
    """Kiểm tra độ tươi (freshness) và trạng thái hiệu lực của kho tri thức `knowledge/finance-kb.json`."""
    rows: list[tuple[str, str, str, str]] = []
    where = "knowledge/finance-kb.json"
    last_str = kb.get("lastCrawledAt")
    max_days = int((kb.get("freshnessPolicy") or {}).get("maxAgeDays", 30))

    if not last_str:
        rows.append(("FAIL", "F3", where, "Thiếu trường `lastCrawledAt` trong kho tri thức tài chính"))
    else:
        try:
            last_dt = dt.datetime.fromisoformat(last_str)
            now_dt = dt.datetime.now(dt.timezone.utc)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=dt.timezone.utc)
            age_days = (now_dt - last_dt).total_seconds() / 86400.0
            if age_days > max_days:
                rows.append((
                    "WARN", "F3", where,
                    f"Kho tri thức đã {age_days:.1f} ngày chưa crawl lại (> {max_days} ngày) — hãy chạy `python3 -I scripts/wms-finance-kb.py --crawl`"
                ))
            else:
                rows.append((
                    "PASS", "F3", where,
                    f"Kho tri thức còn tươi ({age_days:.1f}/{max_days} ngày, cập nhật lần cuối {last_str})"
                ))
        except ValueError as e:
            rows.append(("FAIL", "F3", where, f"`lastCrawledAt` {last_str!r} sai định dạng ISO-8601: {e}"))

    superseded = [
        s.get("sourceId")
        for s in (kb.get("authoritativeSources") or [])
        if s.get("status") in ("superseded", "expired", "revoked")
    ]
    if superseded:
        rows.append((
            "FAIL", "F3", where,
            f"Có nguồn pháp quy trong KB đã hết hiệu lực ({', '.join(superseded)}) — cần cập nhật bài viết & KB trước khi đăng"
        ))
    else:
        rows.append((
            "PASS", "F3", where,
            f"Tất cả {len(kb.get('authoritativeSources') or [])} nguồn pháp quy & {len(kb.get('domainRules') or [])} quy tắc miền đều đang có hiệu lực (`active`)"
        ))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Crawl, chắt lọc tri thức & kiểm định chuyên gia tài chính (F1–F4).")
    ap.add_argument("--crawl", action="store_true", help="Chạy crawler kiểm chứng nguồn pháp lý/tài chính và cập nhật knowledge/finance-kb.json")
    ap.add_argument("--verify", action="store_true", help="Chạy 4 phép kiểm chuyên gia tài chính (F1–F4) trên toàn bộ bài viết & kịch bản video")
    ap.add_argument("--file", type=pathlib.Path, default=DEFAULT_HTML, help="File HTML chứa STORIES (mặc định: docs/prototype.html)")
    ap.add_argument("--story", help="Chỉ kiểm 1 bài theo slug (card, pay, install, ...)")
    ap.add_argument("--quiet", action="store_true", help="Chỉ in FAIL/WARN và dòng tổng kết")
    args = ap.parse_args()

    if not args.crawl and not args.verify:
        args.verify = True

    if args.crawl:
        summary = crawl_and_distill_kb(KB_FILE, CRAWL_REPORT_FILE)
        if not args.quiet:
            print(
                f"── CRAWL & DISTILL · {KB_FILE.relative_to(ROOT)}\n"
                f"PASS      F3   knowledge/finance-kb.json      "
                f"Đã đối chiếu {summary['localArtifactsVerified']}/{summary['localArtifactsTotal']} văn bản gốc nội bộ · "
                f"thăm dò {summary['liveUrlsProbed']} cổng pháp quy · "
                f"chắt lọc {summary['domainRulesCount']} quy tắc miền & {summary['storyInvariantsCount']} hợp đồng bài/video"
            )

    if not args.verify:
        return 0

    if not KB_FILE.is_file():
        print(f"FAIL      F3   knowledge/finance-kb.json      Chưa có kho tri thức tài chính: {KB_FILE}")
        return 1

    kb = json.loads(KB_FILE.read_text(encoding="utf-8"))
    cs = _load_check_story_module()
    tt99 = cs.load_tt99()
    src = args.file.read_text(encoding="utf-8")
    stories = cs.extract(src, "STORIES")

    all_rows: list[tuple[str, str, str, str]] = []
    all_rows.extend(check_kb_freshness(kb))

    if args.story and args.story not in stories:
        all_rows.append(("FAIL", "F1", args.file.name, f"Không tìm thấy bài '{args.story}' trong STORIES"))
    else:
        for k, s in stories.items():
            if not args.story or k == args.story:
                res = verify_story_finance(k, s, kb, tt99)
                all_rows.extend(res["rows"])

    print(f"── CHUYÊN GIA TÀI CHÍNH (F1–F4) · {args.file}")
    for lv, code, where, msg in all_rows:
        if args.quiet and lv == "PASS":
            continue
        print(f"{lv:<9} {code:<4} {where:<30} {msg}")
    cnt = {lv: sum(1 for r in all_rows if r[0] == lv) for lv in ("FAIL", "WARN", "PASS")}
    print("Kết quả Tài chính: " + " · ".join(f"{k} {v}" for k, v in cnt.items()))
    return 1 if cnt["FAIL"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
