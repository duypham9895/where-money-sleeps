# Where Money Sleeps (Đêm nay, tiền của bạn đang ngủ ở đâu?)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Edge-Cloudflare%20Workers%20%2B%20D1-orange)](https://wheremoneysleeps.duyslab.icu)
[![YouTube](https://img.shields.io/badge/YouTube-%40WhereMoneySleeps-red)](https://www.youtube.com/@WhereMoneySleeps)
[![Privacy](https://img.shields.io/badge/Privacy-Zero%203rd--party%20trackers-green)](https://wheremoneysleeps.duyslab.icu)

> **"Đêm nay, 10 triệu bạn vừa quẹt thẻ đang ngủ ở đâu?"**  
> An interactive investigative explainer decoding the hidden plumbing of banking, card networks, clearinghouses, and double-entry accounting in Vietnam.

🌐 **Live Website:** [wheremoneysleeps.duyslab.icu](https://wheremoneysleeps.duyslab.icu)  
📺 **YouTube Channel:** [@WhereMoneySleeps](https://www.youtube.com/@WhereMoneySleeps)  
💼 **Portfolio:** [duypham.me/labs](https://duypham.me/labs)

---

## What is Where Money Sleeps?

When you tap your credit card at a restaurant or scan a QR code at a café, the payment confirms in 2 seconds. But the actual cash doesn't move tonight. It sleeps in intermediate accounts across issuing banks, merchant acquirers, card schemes, and clearinghouses until settlement (T+1 / T+2).

**Where Money Sleeps** is a technical product and financial educational project that demystifies this journey across two parallel viewpoints:

1. **Everyday Mechanism View (Góc nhìn đời thường):** Follow the timeline of information authorizations vs. actual settlement conduits.
2. **Double-Entry Accounting Ledger (Sổ kế toán TT 99/2025/TT-BTC):** Inspect exact debit/credit journal entries (`TK 112`, `TK 1388`, `TK 511`, `TK 521`, `TK 641`) balancing Assets and Liabilities at each hop.

---

## Published Stories (7/19 Topics Live)

| Story | Title | Mechanism & Focus | YouTube (16:9 & Shorts) |
|---|---|---|---|
| `card` | 10 triệu quẹt thẻ ở quán ăn | 4-party card settlement, MDR 2.2%, Interchange fee, T+2 | `fxpFvVJcpRA` · `th6zR4gwV5c` |
| `pay` | Trả hết nợ thẻ trước hạn | Settlement of card balance, zero interest window | `3NqEha4j53k` · `XnMsbH0E_xo` |
| `install` | Mua 12 triệu trả góp lãi 0% | Merchant conversion fee vs bank loan disbursement | `l_8aVo538jo` · `J3DmDP4KKRI` |
| `minpay` | Trả tối thiểu 5% trên sao kê | Loss of 45-day grace period, compounding interest | `ubgdEOblCgo` · `-atHoEHCrSI` |
| `qr` | Quét mã QR 50 nghìn | Instant interbank credit transfer (NAPAS/VietQR) | `d_WpGSjBR-4` · `WpwLZw3ytwU` |
| `profitcash` | Lãi ròng 2 tỷ nhưng két còn 50 triệu | Net income on accrual basis vs operating cash flow | `WnlsZ9AtNdI` · `BpNggcnByQg` |
| `offus` | Chuyển khoản On-Us vs Off-Us | Internal ledger debit vs interbank clearing & RTGS | `Qn3SIzHi_Ik` · `9FdZabe_Q_4` |

---

## Architecture & Technical Highlights

```
┌────────────────────────────────────────────────────────┐
│ Cloudflare Edge (Workers + D1 Database)               │
│ · Custom Domain: wheremoneysleeps.duyslab.icu          │
│ · Static Assets: /dist/site (HTML/CSS/JS, zero npm)    │
│ · Privacy-First Telemetry: POST /api/p                 │
└────────────────────────────────────────────────────────┘
```

- **Zero-Dependency Static Delivery:** Native HTML5, modern CSS Grid/Flexbox with strict typographical hierarchy, and vanilla JavaScript (`0 runtime node_modules`).
- **Strict Privacy Architecture:**
  - Content Security Policy (CSP) blocking 100% third-party analytics/scripts.
  - Anonymized edge telemetry: `POST /api/p` collects **zero** PII, IP addresses, or user identifiers; aggregated daily counts stored in Cloudflare D1.
- **Calm Editorial Motion Graphics:** Programmatic 30fps compositing (`bang-motion` primitives) paired with synchronized audio timestamps and clean split-stage layouts.
- **Deterministic Quality Gates (`scripts/wms-check.sh`):**
  - K1–K4: Accounting equation balance ($\sum \text{Debit} = \sum \text{Credit}$).
  - F1–F4: Financial math, IRR/EIR verification, regulatory freshness with Circular 99/2025/TT-BTC.
  - M1–M4: Non-overlapping text collision audit across desktop (`1280px`), tablet (`768px`), and mobile (`390px`).

---

## Local Development & Testing

### 1. View Locally
You can run any local static file server from the repository root:

```bash
# Using Python
python3 -m http.server 8080 -d docs

# Or using npx serve
npx serve docs
```

Open `http://localhost:8080/prototype.html` in your browser.

### 2. Run Verification Gates
Run the full verification suite:

```bash
# Run all quality checks
bash scripts/wms-check.sh

# Run end-to-end QA tests
python3 -I scripts/wms-qa-verify.py --ci
```

### 3. Build & Deploy Bundle
Package static assets for deployment:

```bash
python3 -I scripts/wms-build-deploy.py
```

This compiles `dist/site/` with asset paths, security headers, and favicons.

---

## Author & License

Created by **Duy Pham** ([GitHub](https://github.com/duypham9895) · [Portfolio](https://duypham.me)).

- **Code & Scripts:** Licensed under the [MIT License](LICENSE).
- **Written Content & Media Assets:** Copyright &copy; 2026 Duy Pham. All rights reserved.
- **Third-Party Attributions:** See [LICENSE](LICENSE) and `legal/licences.json`.
