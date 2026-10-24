---
source: https://claude.ai/artifact/5GLeW87JEhLxzFkpvYvFU9 (artifact của Duy, đọc 2026-10-24)
tier: THAM CHIẾU — tóm tắt nội dung đầu vào, không ai review
---

# Nội dung đầu vào: "Lộ trình học Finance & Money Workflows"

Gốc viết cho **PM fintech**, 26 tuần, 6–8 giờ/tuần, "không cần nền kế toán".
Đầu ra gốc: 1 mini-ledger (code Node/Postgres) + 1 money-flow spec. Chỉ tiếng Việt.
Tiến độ gốc: 21 checkbox, `localStorage` key `mw-roadmap-v1`.

Nguyên tắc dạy: Follow the money · Mọi sự kiện là một bút toán · Vẽ trước đọc sau · Gắn vào việc thật.
Ví dụ mở đầu: một khoản VietQR 10.000.000đ, phí 2%, T+1, phí NH 3.300đ — bảng Nợ/Có.

| # | Giai đoạn | Tuần | Cần học (rút gọn) |
|---|---|---|---|
| 01 | Nền tảng kế toán | 1–4 | A = L + E, bút toán kép, T-account, accrual vs cash, IFRS 15 khái niệm, 3 báo cáo, VAS vs IFRS |
| 02 | Money movement & payment rails | 5–9 | thẻ 4 bên, interchange/MDR, chargeback, RTGS/ACH/NAPAS 247/VietQR, ví, virtual account, SWIFT, nostro/vostro, ISO 20022 |
| 03 | Ledger, reconciliation & system design | 10–13 | ledger bất biến, pending/posted, idempotency, FBO/omnibus, reconcile 2–3 chiều — **có bài tập viết code** |
| 04 | Finance operations | 14–17 | O2C, P2P, 3-way match, month-end close, treasury, FP&A, unit economics, thuế VN |
| 05 | Lending & credit | 18–21 | vòng đời khoản vay, APR/EIR, amortization, DTI/LTV/DSCR, CIC, NIM, IFRS 9 ECL |
| 06 | Risk, compliance & regulation | 22–24 | KYC/AML, fraud, PCI DSS, Luật TCTD 2024, NĐ 52/2024, TT 64/2024, BaaS, ngoại hối |
| 07 | Capstone | 25–26 | Money-Flow Spec + mini-ledger 30 kịch bản + trình bày |

## Sách / tài liệu được khuyến nghị trong gốc

Trả phí (sách, **còn bản quyền**): Financial Intelligence (Berman & Knight) · Accounting Made Simple
(Mike Piper) · Payments Systems in the U.S. (Carol Coye Benson) · The Controller's Function (Bragg) ·
Bank Management & Financial Services (Rose & Hudgins) · Maven FinTech 101 (khoá học).

Miễn phí (web, **miễn phí đọc ≠ được phép chép lại**): Modern Treasury Accounting for Developers &
Journal · Stripe Guides · CFI Resources · Swift ISO 20022 · NAPAS VietQR · Stripe/Square/Airbnb
engineering blogs · IFRS 9 summary · FATF Recommendations · Net Interest · Fintech Business Weekly ·
Fintech Brainfood · văn bản NHNN.
