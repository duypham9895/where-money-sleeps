---
status: pass
stage: 01-spec
date: 2026-11-15
owner: pm
blocked_on: []
---

# PRD — Where Money Sleeps

> **`status: fail` vì `blocked_on` chưa rỗng, KHÔNG phải vì nội dung sai.** Bản nháp viết được;
> chốt thì chưa (PIPELINE Log, APPROVE S0). Chỗ nào phụ thuộc điều kiện ghi `BLOCKED — chờ <điều kiện>`.
> Điều kiện 3 trong `blocked_on` đã theo chữ QĐ 36 (agent `ke-toan-reviewer` chạy thử + đo thời gian Duy ký) — PM đồng bộ sau review vòng sửa 2; N8 đóng (`DECISIONS-QUEUE.md` B-16).
> Khuôn: `/ecc:plan-prd` — nói **cái gì** và **vì sao**, dừng trước **làm thế nào**.
> Nguồn thẩm quyền: 51 quyết định ở `gates/00-discovery/PRODUCT-BRIEF.md` §Quyết định của Duy (dòng sau thắng dòng trước). **QĐ 16** (chú thích: chạm mới hiện) được thêm ngày 2026-10-24, **sau** APPROVE S0. **QĐ 17–35** Duy chốt cùng ngày qua `DECISIONS-QUEUE.md` §Câu trả lời của Duy. **QĐ 36** (người kế toán = agent `ke-toan-reviewer`, Duy ký) và **QĐ 37** (K2 dùng bản chép Phụ lục II, GĐ01 chờ bản chính thức) chốt cùng ngày, sau đợt sửa QĐ 17–35. **QĐ 38–51** chốt 2026-10-25 qua `DECISIONS-QUEUE.md` (38–40 từng câu; **41–51 Duy nhận theo lô mọi khuyến nghị**, trước khi đọc từng bảng phương án). **QĐ 18 — quy tắc thẩm quyền:** chỉ bảng quyết định có hiệu lực; mục thân Brief chỉ vào mùa 1 khi Duy nhặt.
> Bản gộp S1 (2026-10-24): PM gộp từ `SUCCESS-CRITERIA.md` · `TRACKING-PLAN.md` (Data) · `LEGAL-REVIEW.md` (Legal) · `WRITER.md` (Writer). PRD chỉ giữ thứ PRD cần; chi tiết ở file gốc.

**TL;DR** · ~19.500 từ (đếm theo khoảng trắng, sau QĐ 38–51, 2026-10-25) · đọc ~108 phút (tầng HỢP ĐỒNG — Duy đọc TL;DR + §Xung đột giữa các phòng + §Câu hỏi cho Duy là đủ để quyết)
- Website song ngữ dạy người **không có nền tài chính** đi theo đồng tiền: từ "ghi có" khi lương về tới bút toán Nợ/Có tới một khoản VietQR. Hai tầng: **lối vào 12–15 bài** + lộ trình sâu (GĐ01 · khái niệm GĐ02 · người vay GĐ05).
- **Cổng ra mắt (QĐ 14 + QĐ 29):** lối vào VN đã duyệt **+** trình đọc PDF chạy (Hermanson host + file riêng) **+** Hermanson đã redact (2 đoạn trích + bảng số liệu bên thứ ba theo quy tắc Legal) **+** trang sách + thẻ sách **+ cảnh báo lưu trữ `persist()`** (QĐ 45). Hermanson host: **giữ** bảng B3, **che** bảng B2 tr.117 (QĐ 46). Kế toán = **agent `ke-toan-reviewer` soát, Duy ký** (QĐ 36), phạm vi QĐ 30: **GĐ01 (TT 99) · GĐ05 (APR/lãi suất) · mọi card có con số + đoạn bài mà card đó trích**. Card lối vào có con số ⇒ **chưa có báo cáo soát của agent + chữ ký Duy thì không ra mắt được.** FAIL ở K1/K2/K3 chặn đăng; phán khác Duy ký kèm một dòng lý do (QĐ 40). Mục có số hiện câu công khai *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* (QĐ 41). Tên tài khoản: K2 chỉ có bản chép thứ cấp, phán tối đa "KHỚP NGUỒN THỨ CẤP" ⇒ **GĐ01 chỉ đăng khi có Phụ lục II chính thức**; lối vào không bị chặn (QĐ 37).
- 10 bề mặt, nối ở §Bản đồ bề mặt. 2 bề mặt bị chặn bởi phép đo điện thoại của Duy: khôi phục/sync, mở file riêng trong trình đọc PDF — **file riêng giờ chặn cả ra mắt** (QĐ 29). Lời mời cài màn hình chính cũng bị chặn, nhưng nó không phải bề mặt.
- **Legal có quyền CHẶN** qua 37 ràng buộc (R1–R37; R35, R36 thêm theo QĐ 31, 32; R37 dữ liệu người khiếu nại, Legal vòng sửa 2); cổng S5 cần **R29 + R33 + R37 PASS**, cổng ra mắt thêm **R1–R4, R6, R13, R31 + §A.2** theo QĐ 29 (§Ràng buộc có quyền CHẶN). **Trước S5: workflow pháp lý L13 + L18 phải chạy** (QĐ 51). Đo: **M1 = `lesson_completed` bài 5 ÷ bài 1**, báo **số chặt** (`from_start=true`) và **số lỏng** (tất cả) (QĐ 39); chưa có ngưỡng — đặt sau ≥ 4 tuần và ≥ 100 lượt bài 1 (§Success Metrics).
- **Câu hỏi cho Duy: `DECISIONS-QUEUE.md` — 0 câu nhóm A còn mở (2026-10-25).** N1–N5, N7, X4, Legal X10–X13, Writer W1–W2, K1, K11 đã quyết ở QĐ 38–51; N8 đóng (B-16). Còn: **ĐK-1** (= N3, chỉ hỏi nếu `input type=file` không chạy trong Zalo) · ĐK-2 · ĐK-3 · 2 điểm chờ hợp đồng Ringkas (QĐ 34.2 định danh trong dòng AI/dòng soát · QĐ 35 công khai hộp thư). ONE-PAGER v2 đã duyệt (QĐ 50) và **đã áp** vào `gates/ONE-PAGER.md` (`vibe-check [2]` PASS); Duy nên đọc lại bản đã áp. Bài mẫu M0 (`SAMPLE-LESSON-01.md`) và báo cáo `ke-toan-reviewer` (`SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`) đã dựng sẵn chờ Duy bấm giờ ký.
- T2 (2026-10-24): Data và Design hỏi 4 câu — trả lời ở §T2 cuối file.

## Problem

Người Việt đi làm gặp dòng tiền mỗi tuần — "ghi có", "đang xử lý 1–2 ngày", APR trả góp, quét VietQR — mà không có chỗ nào giải thích bằng tiếng Việt **tiền thật sự nằm ở đâu và đi qua ai**, cho người không học kế toán. Tài liệu tiếng Việt hiện có chia hai cực: học kế toán để đi làm kế toán (trả phí), hoặc bài cho kỹ sư backend. Bỏ ngỏ thì người học tiếp tục đọc FAQ từng ngân hàng và không bao giờ có mô hình chung để tự hiểu lần sau.

## Evidence

| Bằng chứng | Loại | Nguồn |
|---|---|---|
| Ít nhất 6 ngân hàng/báo có bài "chuyển khoản thành công nhưng chưa nhận được tiền" ⇒ người ta thật sự gõ câu hỏi này | Quan sát gián tiếp | PRODUCT-BRIEF §Vấn đề & người dùng |
| 24% người trưởng thành VN hiểu biết tài chính — **số cũ (2014), không đo kế toán** | Số liệu thứ cấp | PRODUCT-BRIEF |
| Phương pháp S0 (~8 search VN) **không tìm thấy** lộ trình VN dạy dòng tiền doanh nghiệp/fintech cho người không chuyên — không có nghĩa là không tồn tại | Khảo sát đối thủ | PRODUCT-BRIEF §Bản đồ đối thủ |
| Tỉ lệ học xong MOOC miễn phí 3,13% ⇒ không đặt mục tiêu "hoàn thành lộ trình" | Số liệu thứ cấp | PRODUCT-BRIEF |
| Nhu cầu tầng sâu: chỉ có artifact của chính Duy (n=1) | **Assumption — cần xác minh bằng buổi 5 người đọc bài 1** | PRODUCT-BRIEF §Chưa xác minh |
| Người học muốn đọc PDF trong site | **Assumption — cần xác minh bằng buổi 5 người + event `pdf_opened`** | Quyết định 4 |

## Users

| | Ai | Điều gì kích hoạt nhu cầu |
|---|---|---|
| **Primary — tầng vào** | Nhân viên văn phòng ~25 tuổi, không biết kế toán, đọc trên điện thoại lúc tối, thường mở link từ Zalo | Một giao dịch vừa xảy ra với chính họ: lương về, chuyển khoản treo, trả góp |
| **Secondary — tầng sâu** | Người làm fintech/ngân hàng/ops/PM tại VN không có nền kế toán | Phải hiểu đối soát, ledger, NAPAS/VietQR trong việc |
| **Not for** | Người cần tư vấn đầu tư · người học để thi/làm kế toán · kỹ sư cần code ledger (GĐ03 hoãn) · người cần so sánh lãi suất có tên ngân hàng | Quyết định 5; ONE-PAGER §3 |

## Hypothesis

We believe **một lối vào song ngữ đi theo dòng tiền của chính người học, mỗi bài kèm card đã duyệt và chú thích cho mọi thuật ngữ**, will **cho người không có nền tài chính một mô hình "tiền đi qua ai, nằm ở đâu" mà họ tự áp lại được** for **nhân viên văn phòng VN đọc trên điện thoại**.
We'll know we're right when **tỉ lệ gộp `lesson_completed` bài 5 / bài 1 của lối vào đạt ngưỡng** — ngưỡng và cách chống trùng: xem `SUCCESS-CRITERIA.md`.

## Success Metrics

Phòng Data sở hữu `SUCCESS-CRITERIA.md` và `TRACKING-PLAN.md`. PRD **không đặt số**. Bảng dưới chỉ giữ phần PRD cần để biết mỗi số dùng vào việc gì.

| Metric | Đổi hành động nào | Target | How measured |
|---|---|---|---|
| **M1 — North Star (proxy, gộp)** | Dưới ngưỡng ⇒ viết lại lối vào theo M2 trước; phạm vi GĐ01/02/05 **không cắt** (QĐ 14; `DECISIONS-QUEUE.md` B-12) · trên ⇒ dồn công vào GĐ01/02/05 | **TBD** — đặt sau **≥ 4 tuần** ra mắt **và** bài 1 ≥ 100 lượt (lựa chọn của Data, không phải chuẩn ngành) | `lesson_completed{lesson}` bài 5 ÷ bài 1, theo `lessonId` lúc ra mắt. Báo **hai số**: **chặt** = chỉ `from_start=true` · **lỏng** = tất cả (QĐ 39). "Xong" = đã trả lời ≥ 1 card **trắc nghiệm** cuối bài (QĐ 24, 38) ⇒ M1 đo "đọc + thử" |
| M2 — đường rơi | Viết lại bài nào trước | Xếp hạng, không ngưỡng | `lesson_completed` bài *k* ÷ bài 1 |
| M3 — card sai lần đầu | Card nào Duy đọc lại (card có số: agent `ke-toan-reviewer` soát lại, Duy ký — QĐ 36, 40) | Top 10% trong card ≥ 30 lượt (lựa chọn của Data) | `card_answered{correct}` — **chỉ card trắc nghiệm**; thẻ lật tự chấm không bắn (QĐ 25d). Mỗi bài `published` có ≥ 1 card trắc nghiệm `published` (QĐ 38) ⇒ M3 thấy mọi bài |
| M4 — PDF có ai mở | Có soát + host thêm chương Hermanson không (QĐ 15) | **TBD** — như M1. Đo **từ ngày ra mắt** (trình đọc PDF là điều kiện ra mắt, QĐ 29) | `pdf_opened{source}` ÷ bài 1 |
| M5 — sao lưu/khôi phục | Có phải thiết kế lại chỗ mời sao lưu không | **BLOCKED — chờ đo iPhone/Android** (link hay mã đổi nghĩa metric) | `sync_created{method}` · `progress_restored{method}`, `method` ∈ {`link`,`code`} (QĐ 25a, c) |
| M6 — 5 người đọc bài 1 | Sửa độ dài/giọng **trước** khi viết tiếp | — | Duy quan sát, không instrument |

**Ràng buộc từ Data mà PRD phải chở theo**

| Ràng buộc | Nguồn | AC |
|---|---|---|
| Chống trùng không ID: mỗi event bắn **tối đa một lần mỗi khoá** trên một bộ storage, khoá theo `lessonId`/`cardId`, không theo ngôn ngữ; bài "tự khai" **không bao giờ bắn**; khi nghi thì **thiếu hơn thừa** | TRACKING-PLAN §2 | AC-62 – AC-67 |
| Cờ chống trùng (`tel`) nằm **trong JSON tiến độ** và **đi theo bản sao lưu** (vào whitelist Legal R28) | QĐ 26 · TRACKING-PLAN §2 R4 | AC-58 · AC-66 |
| **Không hàng đợi event** lúc mất mạng: mất mạng ⇒ event mất. Khoá ghi `sent` **trước** khi gọi `sendBeacon` một lần ⇒ không đếm đôi | QĐ 26 · TRACKING-PLAN §2 R1, R6 | AC-67 |
| Trường thời điểm hoạt động cuối (để tính "phiên") trong JSON tiến độ, **không** đi theo bản sao lưu | QĐ 26 | AC-58 · AC-76 |
| Hợp đồng event: `lesson_completed{lesson, from_start}` (bỏ `lang`; `from_start` ∈ {`true`,`false`} = storage này đã có `lesson_completed` của bài 1 lối vào chưa, tính trên máy, không rời máy dưới dạng ID — QĐ 39 mở lại QĐ 25b có chủ đích) · `card_answered{card, correct}` chỉ card trắc nghiệm · `pdf_opened{source}` · `sync_created{method}` · `progress_restored{method}`, `method` ∈ {`link`,`code`}. **Không event** cho tự khai, mời cài, `persist()` — `N/A — because` ở SUCCESS-CRITERIA §3 | QĐ 25 · 39 · TRACKING-PLAN §1 | AC-62 – AC-66 |
| Bộ đếm lưu theo **ngày**; dashboard ẩn mọi ô n < 5, không có bảng ngày × bài/card; workflow pháp lý L13 kết luận số gộp ghép ra được người ⇒ gộp lên tuần, xoá dòng ngày | QĐ 32 | AC-80 |
| **Không** rule chặn theo IP ở Cloudflare (Rate Limiting / WAF / Bot Fight Mode). Bơm số ⇒ cờ F1–F4 + cách ly ngày, không xoá; cách ly ≥ 2 lần trong 4 tuần ⇒ Data đưa số lên Duy. **F2 tính trên số chặt** (QĐ 39). QĐ 38 thêm cờ F4 (TRACKING-PLAN §2.4 — lập luận, chưa thử; Data đã cập nhật) | QĐ 31 · 38 · 39 · TRACKING-PLAN §2.4 | AC-84 |
| `card` mang phiên bản `<cardId>.v<n>`; `cardId` gán lúc duyệt, không đổi khi máy sinh card chạy lại | TRACKING-PLAN §1 | AC-64 |
| Site và bộ đếm **cùng origin** ⇒ site không host trên GitHub Pages. Tên miền **chưa mua**; đăng ký dưới tên Duy là việc chạm Legal R34 | TRACKING-PLAN §3 · LEGAL-REVIEW R34 | AC-68 |
| **Workers Logs mặc định BẬT** cho Worker mới ⇒ phải tắt hẳn | TRACKING-PLAN §3 | AC-56 |
| **Dashboard đọc được M1–M5 bằng số thật phải sống trước S5**; S4 bắn tay đủ 5 event trên máy thật và **nhìn thấy số** | SUCCESS-CRITERIA TL;DR · CLAUDE.md quy tắc 8 | AC-69 · AC-70 |
| Event của tính năng **không ra mắt cùng M1** (sao lưu/khôi phục; PDF `hosted`/`own` giờ **ra mắt cùng M1** theo QĐ 29; bản EN không có event riêng sau QĐ 25b — thêm event lúc bật EN là quyết định khi đó) ⇒ ở cổng S5 ghi `N/A — because <tính năng chưa bật>, kiểm lúc bật <tên>`; phép "nhìn thấy số" gắn vào **lúc bật từng tính năng**, không chỉ S5 *(T2 Data, 2026-10-24)* | CLAUDE.md quy tắc 8 | AC-74 |
| Nơi lưu: khuyến nghị **D1** — **lệch có chủ ý** khỏi kiến trúc tham chiếu của xưởng (Analytics Engine chỉ giữ 3 tháng). SWE chốt ở S3 | TRACKING-PLAN §4 | — |

**Định nghĩa "xong bài"** (điều kiện chuyển trạng thái của `lesson_completed`): **đã trả lời ≥ 1 card trắc nghiệm cuối bài, đúng hay sai** (QĐ 24, 38). Chạm "Nhớ / Chưa nhớ" trên thẻ lật tự chấm **không** tính (QĐ 38). Kèm bất biến **hai chiều** AC-75: bài `published` phải còn ≥ 1 card **trắc nghiệm** `published` (đăng **và** gỡ). Không thoả được bằng cuộn nhanh. Cái giá đã nói ở Q-23: không soạn được bài kết thúc toàn thẻ lật; gỡ card trắc nghiệm cuối của một bài kéo bài xuống.

## Scope

**MVP (mùa 1)** — thứ tối thiểu để kiểm giả thuyết, theo quyết định 1–51. Cột "Ra mắt cần?" theo **QĐ 14 + QĐ 29 + QĐ 45** (cổng ra mắt).

| # | Năng lực | Ra mắt cần? | Quyết định |
|---|---|---|---|
| 1 | Lối vào 12–15 bài VN, đọc tốt trên điện thoại | **Có** | 1 · 5 · 14 |
| 2 | Card cuối mỗi bài (chạm, không gõ; có phản hồi + "đọc lại đoạn này") + 1–2 card ôn đầu phiên sau. "Xong bài" = đã trả lời ≥ 1 card trắc nghiệm (QĐ 24); thẻ lật **không** tính; mỗi bài `published` có ≥ 1 card trắc nghiệm `published` (QĐ 38). Card Hermanson = card **khái niệm, không con số, hiện VN**, link về `sectionId` của **bất kỳ bài `published` nào** có `based_on` phủ trang đó (QĐ 27, 48) | **Có** (card bài lối vào). Card Hermanson lên cùng bài có `based_on` tương ứng (QĐ 28, 48) | 2 · 3 · 8 · 24 · 27 · 28 · 38 · 48 · ADDENDUM §Đường ống bước 8–9 |
| 3 | Glossary một nguồn; mọi thuật ngữ có chú thích. **Chạm ⇒ thẻ mở tại chỗ ngay sau câu, đẩy chữ xuống** (QĐ 17); gạch chấm ở **lần đầu mỗi mục H2** (QĐ 19); thuật ngữ chuyên ngành **giữ tiếng Anh trong dòng** (Debit, Credit, accrual, APR…), mục glossary có cờ `keep_en` (QĐ 20); **ngoại lệ: bài VN viết "sổ cái", `ledger` chỉ trong thẻ chú thích** (QĐ 44); thuật ngữ VN so với **danh sách gốc** (tên TK TT 99 + glossary) ⇒ cảnh báo (QĐ 21) | **Có** | 5 · 16 · 17 · 19 · 20 · 21 · 44 |
| 4 | Nút gạt VI ⇄ EN tại chỗ; bài chưa có EN đã duyệt ⇒ nút mờ + một dòng báo. "Không trộn ngôn ngữ" = câu văn + chữ giao diện cùng một ngôn ngữ; thuật ngữ `keep_en` không tính là trộn (QĐ 20). Ngoại lệ có tên (QĐ 43): (a) danh sách tên riêng ngắn, không chú thích, tách khỏi glossary · (b) dòng "chưa có bản EN" **song ngữ** · (c) chữ VN trên trang EN chỉ hợp lệ khi là mục glossary được đánh dấu; `vi.term` trong thẻ được miễn | **Có** (nút); bản EN lên dần | 6 · 20 · 43 |
| 5 | Tiến độ trên máy người học (bài đã đọc · trạng thái card · trang PDF · ngôn ngữ) **+ `tel` + thời điểm hoạt động cuối** (QĐ 26); **giữ ID mồ côi** — không xoá tiến độ của bài/card đã gỡ (QĐ 18) | **Có** | 7 · 18 · 26 |
| 6 | Tự khai **theo giai đoạn** trong 2 chạm; lối vào là một khối; mọi bài của giai đoạn được khai ⇒ `suppressed` | **Có** | 7 · 23 |
| 7 | Link sync gửi cho chính mình qua Zalo; `method` ∈ {`link`,`code`} (không `file`) | BLOCKED — chờ đo iPhone/Android | 7 · 18 · 25 |
| 8 | Trình đọc PDF: Hermanson tr.1–197, **đã redact** tr.113 + tr.166 + **bảng B2 tr.117** (QĐ 46). Bảng B3 (tr.45, 55, 94–95, 170, 185 — dữ kiện) **giữ** trong file host, **loại hẳn** khỏi máy sinh card (QĐ 46). Bản sửa `licences.json` của Legal: nhận (QĐ 46) | **Có** | 4 · 15 · 29 · 46 |
| 9 | Trình đọc PDF: mở file riêng của người học, thuần cục bộ | **Có** — BLOCKED — chờ đo `input type=file` trong WebView Zalo ⇒ **chặn ra mắt**. Đo ra không chạy: **→ Duy (ĐK-1, `DECISIONS-QUEUE.md`)** | 4 · 29 |
| 10 | Trang sách (B6) + thẻ sách do Duy viết ("đọc chương nào") + link mua | **Có** — Duy viết thẻ sách | 29 · ONE-PAGER §3 |
| 11 | Bộ đếm gộp tự host, cùng domain, chỉ cộng số; lưu theo ngày (QĐ 32); không rule IP ở Cloudflare (QĐ 31) | **Có** (dữ liệu không hồi tố) | 9 · 31 · 32 |
| 12 | Cờ `published` cho từng bài/card/bản EN — gỡ trước, tranh luận sau. Bài `published` luôn có ≥ 1 card `published` (AC-75) | **Có** | 8 · 11 · 14 · 24 |
| 13 | GĐ01 → khái niệm GĐ02 → người vay GĐ05 lên dần sau ra mắt. **Bài GĐ01 có tên tài khoản chính thức chỉ đăng khi có Phụ lục II TT 99 chính thức** (QĐ 37) | Không | 5 · 14 · 37 |
| 14 | Trang nguồn & giấy phép (ghi công Hermanson CC BY 3.0), disclaimer, riêng tư · **kênh khiếu nại = hộp thư riêng cho site**, không họ tên đầy đủ, không nhắc Ringkas, trang in **"gỡ tạm trong 72 giờ"** (NĐ 17/2023 đặt hạn ngắn hơn thì luật thắng) · hộp thư theo **phương án A** (QĐ 49): trang riêng tư dùng **câu R25 mới** của Legal (nguyên văn ở AC-57); thư khiếu nại theo Legal R37, **xoá khi khiếu nại đóng** | **Có** — công khai hộp thư: **BLOCKED — chờ Duy đọc hợp đồng Ringkas** (QĐ 35) | LEGAL-SCREEN · `licences.json` · Legal R33 · R37 · 35 · 49 |
| 15 | Mời cài màn hình chính sau ~3 bài | BLOCKED — chờ đo iPhone (storage tab ↔ app tách?) | 7 |
| 16 | Dashboard đọc M1–M5 bằng số thật; ẩn mọi ô n < 5, không bảng ngày × bài/card (QĐ 32) | **Có** — trước S5. M4 có số thật từ ra mắt (QĐ 29); M5 ghi `N/A` tới lúc bật sao lưu (AC-74) | 9 · 32 · SUCCESS-CRITERIA |
| 17 | Diễn tập gỡ bằng cờ `published` (bài, card, file host Hermanson) **và** diễn tập đầu-cuối khiếu nại giả → Duy nhận → lật cờ → 404, trong 72 giờ (Legal R33 c, d) | **Có** — trước S5; (d) BLOCKED cùng công khai hộp thư | 14 · 35 · LEGAL-REVIEW R33 |
| 18 | Dòng minh bạch AI trên **mọi** bài/bộ card đã đăng (QĐ 34.1); "Soạn với hỗ trợ AI" **chỉ** ở mục có cờ `ai_assisted` (QĐ 34.3); **hạt của cờ = bài / bộ card / bản EN** — bài lai ⇒ cả bài mang cờ (QĐ 42). Mục có con số/tên tài khoản hiện **dòng soát công khai** *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."*; `reviewed_by` = chỉ người ký, agent ở trường riêng; dòng minh bạch và `reviewed_by` **không** chứa "kế toán / accountant / chuyên gia / expert" (QĐ 41); **mọi bản EN do Claude dịch lúc build ⇒ `ai_assisted = true`** — hệ quả trực tiếp của QĐ 6 + 34, không phải quyết định mới; chữ định danh trong "duyệt bởi ⟨…⟩": **BLOCKED — chờ hợp đồng Ringkas** (QĐ 34.2). Disclaimer footer; khối "căn cứ văn bản hiệu lực đến" cho bài lãi suất/pháp lý. **0 chữ trích nguyên văn luật** ở phần ra mắt (QĐ 33) | **Có** | 33 · 34 · 41 · 42 · LEGAL-REVIEW R18 · R20 · R21 |
| 19 | Cảnh báo lưu trữ theo `persist()` — 3 biến thể chữ WRITER §6; chỉ khi đã có tiến độ (QĐ 18 nhặt từ thân Brief) | **Có** — điều kiện ra mắt (QĐ 45) | 18 · 45 |
| 20 | Không auto-redirect theo ngôn ngữ trình duyệt (QĐ 18 nhặt) | **Có** (là thuộc tính, không phải tính năng) | 18 |
| 21 | **Soát kế toán = agent `ke-toan-reviewer`** (`../../../.claude/agents/ke-toan-reviewer.md`, K1 số học bằng code · K2 tên tài khoản · K3 khái niệm · K4 người mới hiểu sai), phạm vi QĐ 30; agent **soát**, **Duy ký**. K2 hiện chỉ có bản chép thứ cấp `legal/tt99-phu-luc-ii.secondary.json` ⇒ phán tối đa "KHỚP NGUỒN THỨ CẤP", không bao giờ PASS (QĐ 37). **Luật ký (QĐ 40):** FAIL ở K1/K2/K3 chặn đăng tới khi sửa + agent soát lại; UNVERIFIED · FLAG · "KHỚP NGUỒN THỨ CẤP" (ngoài GĐ01): Duy ký được, kèm một dòng lý do trong bản ghi | **Có** — card lối vào có con số cần nó. Chạy thử trên bài mẫu = điều kiện 3 trước S1 (QĐ 36) | 8 · 30 · 36 · 37 · 40 |

**Out of scope**

| Thứ không làm | Vì sao | Nguồn |
|---|---|---|
| LLM chạy runtime (proxy · BYOK · on-device) | Chi phí, key, riêng tư; Chrome AI không có VN trên điện thoại | Quyết định 2 |
| Card sinh từ sách trả phí, OpenStax hiện hành, mọi nguồn NC | Bản quyền; OpenStax cấm đưa vào LLM | Quyết định 3 · 10 |
| Host Hermanson ngoài tr.1–197 | Chưa soát ảnh phần còn lại; ≥2 hình có nguồn bên thứ ba. **Máy sinh card thì được nạp cả cuốn** trừ đoạn đã biết phải loại (QĐ 28) — phạm vi host không đổi | Quyết định 15 · 28 |
| Tài khoản, bình luận, diễn đàn | Lời hứa không định danh | ONE-PAGER §1 · LEGAL-SCREEN |
| Tư vấn đầu tư, mã chứng khoán, bảng lãi suất có tên ngân hàng | Luật CK; rủi ro "thông tin tổng hợp" | ONE-PAGER §3 |
| Trích nguyên văn văn bản luật ở phần ra mắt | Chỉ link văn bản gốc + diễn giải; ngưỡng trích đặt khi mở GĐ05 | QĐ 33 |
| Kiếm tiền mùa 1 (affiliate, donate) | Giữ lời hứa "dạy, không bán"; không khoá vĩnh viễn | Quyết định 10 |
| GĐ03 (code), GĐ04, GĐ06, GĐ07 | Hiện "sắp có", **không ghi ngày** | Quyết định 5 |
| "Ôn với AI của bạn" | Mùa 2 | Quyết định 2 (dòng 11 câu) |
| Nút "Thêm vào lịch" (`.ics`) · sao lưu bằng file JSON (`method: file`) · EPUB / foliate-js | Ra khỏi mùa 1 ⇒ LEGAL-REVIEW R32 thành N/A | QĐ 18 · 25c |
| Máy tính khoản vay tự nhập offer | Quyết lúc mở GĐ05 (không thuộc ra mắt) | QĐ 18 |
| Funnel theo từng người, % hoàn thành 26 tuần | Cần định danh; nền 3,13% tự kết án | PRODUCT-BRIEF §Đo cái gì |
| Thời gian đọc, cuộn, quốc gia, thiết bị, referrer | Không đổi hành động nào; muốn thêm ⇒ Duy quyết, dòng có ngày | SUCCESS-CRITERIA §3 |
| Event cho tự khai · mời cài · kết quả `persist()` · thẻ lật tự chấm | Không đổi hành động nào ở mùa 1 | QĐ 25d, e |
| Chặn spam theo IP — **cả trong mã Worker lẫn rule ở Cloudflare** | Đọc IP là xử lý dữ liệu; giữ QĐ 9. Phát hiện bằng F1–F4 + cách ly ngày | LEGAL-REVIEW R23 · QĐ 31 · 38 · TRACKING-PLAN §2.4 |

## Bản đồ bề mặt

Trả lời câu Design #1 của review S0. **Tên bề mặt là tên tạm** — Writer sở hữu cách gọi (stages.md).
PRD nói bề mặt nào tồn tại và nối nhau ra sao; bố cục, vị trí, cách hiện là việc S2.

```
   Link chia sẻ (Zalo) ──► Trang chủ   HOẶC   thẳng vào Trang bài   (hai cửa vào — §Định nghĩa dùng chung)

   Trang chủ ──┬──► Bản đồ lộ trình (2 tầng) ──► Trang bài ──► Card cuối bài
     │         │                                   │   ▲          │
     │         │                                   │   └──────────┘ "đọc lại đoạn này" (sectionId)
     │         │                                   └──► Glossary (từ mỗi thuật ngữ)
     │         ├──► Trang sách ──► Trình đọc PDF  [Hermanson tr.1–197 | file của bạn]
     │         ├──► Khôi phục / Sync  ◄── mở link #sync từ Zalo
     │         └──► Nguồn & giấy phép · Riêng tư · Disclaimer
     │
     └─ Nút gạt VI ⇄ EN: có trên MỌI bề mặt, giữ nguyên vị trí (sectionId)
```

| # | Bề mặt | Việc của nó | Vào từ | Đi tới | Trạng thái | Quyết định |
|---|---|---|---|---|---|---|
| B1 | Trang chủ | Tên **kèm tagline T1** (QĐ 22): VN *"Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu."* · EN *"From the bank alert to the ledger: where your money actually goes."*; người mới vào bài 1, người quay lại "đọc tiếp"; 1–2 card ôn **nếu B1 là bề mặt đầu phiên** | Link chia sẻ trang chủ, tìm kiếm | B2 · B3 · B6 · B7 · B9 | Sẵn | 1 · 14 · 22 · Log tên |
| B2 | Bản đồ lộ trình hai tầng | Lối vào ở trên; GĐ01/02/05 bên dưới; GĐ03/04/06/07 "sắp có" không ngày; đánh dấu bài đã đọc | B1 | B3 | Sẵn | 1 · 5 |
| B3 | Trang bài | Đọc reflow trên điện thoại; thuật ngữ chuyên ngành giữ tiếng Anh trong dòng nếu là mục `keep_en` (QĐ 20); gạch chấm ở lần đầu mỗi mục H2, chạm ⇒ thẻ chú thích **mở tại chỗ ngay sau câu** (QĐ 17, 19); card ở cuối. **Khi B3 là bề mặt đầu phiên** (vào thẳng từ link): 1–2 card ôn nếu có card đã trả lời ở phiên trước; lối vào B9 nếu chưa có tiến độ — cả hai **không chặn đọc**, bỏ qua bằng 1 chạm; vị trí và dạng do S2 | B1 · B2 · card · **link chia sẻ thẳng vào bài** | B4 · B5 · B9 · bài kế | Sẵn | 5 · 7 · 8 · 17 · 19 · 20 · ADDENDUM bước 9 |
| B4 | Card | Chạm-không-gõ; phản hồi ngay + 1 dòng giải thích + link về `sectionId` | Cuối B3; đầu phiên ở B1 **hoặc B3** | B3 | Card từ bài tự viết: Sẵn · card Hermanson: **khái niệm, không con số, hiện VN**; `source_quote` EN chỉ nằm trong dữ liệu build; "đọc lại đoạn này" trỏ `sectionId` của **bất kỳ bài `published` nào** có `based_on` phủ trang đó; chưa có bài đó ⇒ chưa đăng được (QĐ 27, 28, 48) | 2 · 24 · 27 · 28 · 48 · ADDENDUM |
| B5 | Glossary | Một nguồn cho mọi chú thích; xem riêng được; mỗi mục có cờ `keep_en` (QĐ 20) | Thuật ngữ trong B3 | B3 | Sẵn — **QĐ 16** chạm mới hiện · **QĐ 17** mở tại chỗ (thử 5 người với "thẻ phủ lên chữ") · **QĐ 19** lần đầu mỗi mục H2 | 5 · 16 · 17 · 19 · 20 |
| B6 | Trang sách | Hermanson (đọc trong site) + thẻ sách Duy viết + link mua + deep-link OpenStax | B1 | B7 · link ngoài | **Ra mắt** (QĐ 29) — thẻ sách: Duy viết | 3 · 4 · 29 · ONE-PAGER §3 |
| B7 | Trình đọc PDF | Mở Hermanson tr.1–197 (bản redact) hoặc file riêng thuần cục bộ; nhớ trang đang đọc | B6 | B6 | **Ra mắt** (QĐ 29). Hermanson: chờ redact (tr.113, tr.166, B2 tr.117; B3 giữ — QĐ 46) · File riêng: BLOCKED — chờ đo `input type=file` ⇒ chặn ra mắt; đo ra không chạy: **→ Duy (ĐK-1)** | 4 · 15 · 29 · 46 |
| B8 | Nút gạt VI ⇄ EN | Đổi ngôn ngữ tại chỗ, giữ `sectionId`; lựa chọn nhớ trên máy; **không** auto-redirect theo ngôn ngữ trình duyệt (QĐ 18) | Mọi bề mặt | Cùng bề mặt, ngôn ngữ kia | Sẵn — "trộn ngôn ngữ" theo QĐ 20; ngoại lệ ngoài `keep_en` theo QĐ 43 (tên riêng · dòng "chưa có bản EN" song ngữ · đối xứng cho trang EN) | 6 · 18 · 20 · 43 |
| B9 | Khôi phục / Sync | Tự khai **theo giai đoạn** (2 chạm, lối vào một khối — QĐ 23); tạo link/mã sao lưu gửi Zalo; nhận link sync | B1 **hoặc B3** (khi chưa có tiến độ) · link `#sync` | B1 · B2 · bài đang đọc (nếu vào từ B3) | Tự khai: Sẵn · Sync: BLOCKED — chờ đo Zalo `#fragment` | 7 · 23 · 25 |
| B10 | Nguồn & giấy phép · Riêng tư · Disclaimer · Khiếu nại | Ghi công CC BY; nói bộ đếm đếm gì, không đếm gì; disclaimer có ngày "căn cứ văn bản hiệu lực đến"; **hộp thư riêng cho site** (không họ tên đầy đủ, không nhắc Ringkas) + in **"gỡ tạm trong 72 giờ"** (QĐ 35; Legal R33 a, b); trang riêng tư dùng câu R25 mới (QĐ 49) | Footer mọi trang | — | Ghi công · riêng tư · disclaimer: Sẵn — nội dung do `LEGAL-REVIEW.md` · Công khai hộp thư: **BLOCKED — chờ hợp đồng Ringkas** (QĐ 35) | LEGAL-SCREEN · Legal R33 · R37 · 35 · 49 |

Lời mời cài màn hình chính **không phải bề mặt**: là một lời nhắc sau ~3 bài, kèm bước sync. BLOCKED — chờ đo iPhone.

**Định nghĩa dùng chung** — thêm 2026-10-24 (T2 Design). PM định nghĩa vì chưa file nào định nghĩa; đổi thì thêm dòng có ngày.

| Từ | Nghĩa | Vì sao, và cái giá | AC |
|---|---|---|---|
| `sectionId` | Một mục **H2** của bài. Mỗi H2 có đúng một `sectionId`; không có `sectionId` ở cấp đoạn văn. "Đọc lại đoạn này", nút gạt VI ⇄ EN và dấu chú thích lần đầu (QĐ 19) dùng **cùng** đơn vị này | AC-08 bắt tập `sectionId` VI = EN; ở cấp đoạn văn, bản dịch tách/gộp một đoạn là FAIL. Cái giá: card và nút gạt đưa người đọc tới **đầu mục**, không tới đúng đoạn | AC-77 |
| Phiên | Một lần mở site mà lần hoạt động cuối ghi trong JSON tiến độ đã cách ≥ **N giờ**. N: **TBD — S2 đề xuất, kiểm ở buổi 5 người (M6)**. Trường thời điểm hoạt động cuối nằm trong schema tiến độ, **không** đi theo bản sao lưu (QĐ 26) | Không dùng `sessionStorage`: nếu mỗi link Zalo mở một WebView mới thì mỗi lần bấm là một phiên — **chưa đo** (phép đo iPhone/Android) | AC-20 · AC-76 |
| Cửa vào | **Mọi URL trang bài** (`/vi/…`, `/en/…`) là cửa vào, không riêng B1. Bề mặt đầu tiên của phiên làm việc "đầu phiên" (ôn, mời khôi phục) | Site tĩnh có URL cho từng trang (AC-10) ⇒ vào thẳng B3 chắc chắn xảy ra. Không đo được cửa nào là chính (referrer ngoài phạm vi — SUCCESS-CRITERIA §3) ⇒ S2 thiết kế cho **cả hai** | AC-76 · AC-78 |
| Tagline trên trang bài | R16 áp cho **mọi** chỗ tên sản phẩm xuất hiện — kể cả header trang bài và thẻ chia sẻ `og:` của link bài, không riêng ba chỗ AC-39 nêu. Trang bài không bắt buộc hiện tên; hiện tên thì phải kèm tagline T1 (QĐ 22) | Link Zalo hay trỏ thẳng vào bài ⇒ thẻ xem trước của link bài là lần đầu người lạ thấy cái tên | AC-78 |
| Trộn ngôn ngữ | Câu văn + chữ giao diện của một trang cùng một ngôn ngữ. Thuật ngữ chuyên ngành tiếng Anh trong dòng chữ trang VI **không** tính là trộn khi là mục glossary `keep_en` (QĐ 20). Ngoại lệ có tên (QĐ 43): (a) tên riêng trong một danh sách ngắn, không chú thích, tách khỏi glossary (tên sản phẩm, tên sách/tác giả, tên giấy phép) · (b) dòng "chưa có bản EN" song ngữ · (c) chữ VN trên trang EN chỉ hợp lệ khi là mục glossary được đánh dấu; `vi.term` trong thẻ được miễn | QĐ 20 thu hẹp QĐ 6; QĐ 43 đặt ngoại lệ | AC-05 · AC-06 |

## Ràng buộc từ S0

R1–R20 từ quyết định S0 (1–16); **R21–R29 từ QĐ 17–35** (Duy chốt trong S1, 2026-10-24); QĐ 36–37 sửa R7, R10, R17 (không thêm dòng); **QĐ 38–51 (2026-10-25)** sửa R3, R5, R7, R17, R23–R25, R28, R29 và thêm **R30–R33**. Dòng R cũ đã sửa theo QĐ mới ghi số QĐ ở cột Quyết định.

| # | Ràng buộc | Quyết định | Nguồn |
|---|---|---|---|
| R1 | Hai tầng trên **một** bộ nội dung | 1 | PRODUCT-BRIEF §Quyết định |
| R2 | Không LLM runtime; card tĩnh sinh lúc build trên máy Duy, soát rồi mới ship | 2 | PRODUCT-BRIEF |
| R3 | Nguồn nạp máy sinh card: bài Duy tự viết + **cả cuốn** Hermanson, trừ đoạn đã biết phải loại (danh sách trang trong `licences.json` `exclusions`, Legal cập nhật vòng sửa 2) **và** mọi trang có dấu hiệu nguồn ngoài theo **mẫu ③ của Legal** (không phân biệt hoa thường; `annual report`, `Accounting Trends`, `Source:`/`Source'`, `©`, `copyright`, chuỗi denylist R10, `reprinted`, `adapted from` — LEGAL-REVIEW §A.2), thay mẫu đúng chữ QĐ 28 (QĐ 47). Bảng B3 loại hẳn khỏi máy sinh card (QĐ 46). Phần lọt qua luật là rủi ro Duy nhận | 3 · 28 · 46 · 47 · Log Hermanson | PRODUCT-BRIEF · `licences.json` `exclusions` |
| R4 | Có trình đọc PDF mùa 1; file riêng xử lý thuần cục bộ, LLM không chạm; nhớ trang đang đọc | 4 | PRODUCT-BRIEF |
| R5 | Hermanson: **chỉ host tr.1–197**, redact tr.113 + tr.166 + **che bảng B2 tr.117**; **giữ** bảng B3 tr.45, 55, 94–95, 170, 185 (QĐ 46); ghi "đã trích & sửa đổi", CC BY **3.0**. Redact xong là **điều kiện ra mắt** | 15 · 29 · 46 | PRODUCT-BRIEF · LEGAL-SCREEN §Kết luận · `licences.json` |
| R6 | Mùa 1 = lối vào 12–15 + GĐ01 + khái niệm GĐ02 + người vay GĐ05 (~28–30 bài, **chưa đo**) | 5 | PRODUCT-BRIEF |
| R7 | Mọi thuật ngữ chuyên ngành có chú thích, từ **một** glossary; tên tài khoản theo **TT 99/2025**. Thuật ngữ chuyên ngành giữ tiếng Anh trong dòng (`keep_en`), trừ `ledger` — bài VN viết "sổ cái" (QĐ 44); chữ EN không phải `keep_en` và không thuộc ngoại lệ QĐ 43 trên trang VI ⇒ FAIL; thuật ngữ VN so với danh sách gốc (TT 99 + glossary, dựng ở S3) ⇒ cảnh báo, không FAIL. Tên TK đối chiếu nguyên văn Phụ lục II (agent K2); repo hiện chỉ có bản chép thứ cấp ⇒ tối đa "KHỚP NGUỒN THỨ CẤP"; bài GĐ01 có tên TK chính thức chỉ đăng khi có Phụ lục II chính thức | 5 · 20 · 21 · 37 · 43 · 44 | PRODUCT-BRIEF · LEGAL-SCREEN §Pháp lý VN |
| R8 | VN là gốc; EN dịch lúc build, **Duy duyệt mới hiện**; không trang nào trộn ngôn ngữ — **"trộn" = câu văn + chữ giao diện khác ngôn ngữ; thuật ngữ `keep_en` không tính** (QĐ 20); nút gạt giữ `sectionId`; URL `/vi/` `/en/` + hreflang; không auto-redirect (QĐ 18) | 6 · 18 · 20 | PRODUCT-BRIEF |
| R9 | Tiến độ: một bản ghi có `schema` trên máy người học; tên key + schema là **hợp đồng**. Schema thêm `tel` (đi theo sao lưu) + thời điểm hoạt động cuối (không đi theo); không hàng đợi event; giữ ID mồ côi | 7 · 18 · 26 | PRODUCT-BRIEF |
| R10 | Duy duyệt mọi bài + card (cả EN); **agent `ke-toan-reviewer` soát** GĐ01 · GĐ05 · mọi card có con số **+ đoạn bài mà card đó dùng làm `source_quote`**, **Duy ký** (QĐ 36 thay "người kế toán" ở QĐ 8, 14, 30); con số trong bài không card nào hỏi (kể cả sổ ngân hàng GĐ02): Duy đọc; **chưa duyệt thì không đăng** | 8 · 30 · 36 | PRODUCT-BRIEF · ONE-PAGER §3 |
| R11 | Đo: bộ đếm gộp tự host cùng domain; không ID, không cookie, không lưu IP; **không script bên thứ ba** | 9 | PRODUCT-BRIEF · CLAUDE.md quy tắc 8 |
| R12 | Lõi chỉ bài tự viết + CC BY; nguồn NC (BIS, OpenStax) chỉ là link; mùa 1 không kiếm tiền | 10 | PRODUCT-BRIEF |
| R13 | Không luật sư; kết luận pháp lý từ workflow ghi "không phải ý kiến pháp lý"; Duy ký chấp nhận rủi ro | 11 · 12 | PRODUCT-BRIEF · LEGAL-SCREEN |
| R14 | Hợp đồng Ringkas đọc xong **trước khi S1 chốt** | 13 | PRODUCT-BRIEF |
| R15 | Ra mắt khi lối vào VN duyệt xong; phần sau lên bằng cờ `published` | 14 | PRODUCT-BRIEF |
| R16 | Tên luôn đi kèm tagline giải nghĩa — **T1** | Log 2026-10-24 · 22 | PIPELINE · ONE-PAGER §1 |
| R17 | Card: chạm không gõ; có `source_quote` + số trang; con số trong đáp án phải có trong `source_quote`; trượt thì **loại, không sửa**; không dùng LLM chấm LLM **thay người ký** — agent `ke-toan-reviewer` được soát (QĐ 36, dòng sau thắng ADDENDUM), phán của nó không bao giờ là chữ ký; người ký là Duy; không dùng con số tài chính làm phương án nhiễu nếu không có phản hồi. Card Hermanson: khái niệm, **không con số**, hiện VN; `source_quote` EN giữ trong dữ liệu build, không hiện; bản dịch VN đúng câu trích hay không: Duy kiểm; "đọc lại đoạn này" trỏ bất kỳ bài `published` có `based_on` phủ trang (QĐ 48) | 2 · 3 · 27 · 36 · 48 | ADDENDUM §Đường ống bước 5–8 |
| R18 | Ôn theo phiên, không theo lịch ngày | — | ADDENDUM §Đường ống bước 9 |
| R19 | Không tư vấn đầu tư, không mã chứng khoán, không bảng lãi có tên ngân hàng | — | ONE-PAGER §3 · LEGAL-SCREEN |
| R20 | Chú thích thuật ngữ **chạm mới hiện**, không hiện sẵn; **mở tại chỗ** ngay sau câu (đẩy chữ, không phủ); gạch chấm ở **lần đầu mỗi mục H2** | 16 · 17 · 19 | PRODUCT-BRIEF §Quyết định |
| R21 | Thẩm quyền: chỉ bảng quyết định có hiệu lực; mục thân Brief vào mùa 1 khi Duy nhặt. Đã nhặt: cảnh báo `persist()` · giữ ID mồ côi · không auto-redirect. Ra: `.ics`, sao lưu file JSON, EPUB/foliate-js | 18 | PRODUCT-BRIEF |
| R22 | Tự khai theo **giai đoạn**, lối vào một khối; bài của giai đoạn được khai ⇒ `suppressed` | 23 | PRODUCT-BRIEF |
| R23 | "Xong bài" = đã trả lời ≥ 1 card **trắc nghiệm** cuối bài; thẻ lật không tính; bài `published` phải còn ≥ 1 card **trắc nghiệm** `published` (AC-75) | 24 · 38 | PRODUCT-BRIEF |
| R24 | Hợp đồng event theo QĐ 25 (a)–(e), cộng `from_start` trên `lesson_completed` (QĐ 39 mở lại 25b) — §Success Metrics | 25 · 39 | PRODUCT-BRIEF · TRACKING-PLAN §1 |
| R25 | **Cổng ra mắt** = lối vào đã duyệt + trình đọc PDF chạy (sách host + file riêng) + Hermanson đã redact + trang sách + thẻ sách **+ cảnh báo lưu trữ `persist()`** (QĐ 45). Hệ quả Legal: R1–R4, R6, R13, R31 + §A.2 phải PASS (LEGAL-REVIEW §2) | 14 · 29 · 45 | PRODUCT-BRIEF · LEGAL-REVIEW §2 |
| R26 | Bộ đếm: lưu theo ngày, ẩn ô n < 5, không bảng ngày × bài/card; không rule IP ở Cloudflare | 31 · 32 | PRODUCT-BRIEF |
| R27 | Phần ra mắt: **0 chữ** trích nguyên văn văn bản luật — chỉ link + diễn giải; ngưỡng đặt khi mở GĐ05 | 33 | PRODUCT-BRIEF |
| R28 | Dòng minh bạch AI trên mọi bài/bộ card đã đăng; "Soạn với hỗ trợ AI" chỉ ở mục `ai_assisted`, cờ theo **bài / bộ card / bản EN** (QĐ 42); chữ định danh chọn sau hợp đồng Ringkas. Bản EN do Claude dịch lúc build ⇒ `ai_assisted = true` (hệ quả trực tiếp của QĐ 6 + 34, không phải quyết định mới) | 6 · 34 · 42 | PRODUCT-BRIEF |
| R29 | Kênh khiếu nại = hộp thư riêng cho site, không họ tên đầy đủ, không nhắc Ringkas, ở B10; in "gỡ tạm trong 72 giờ"; công khai sau hợp đồng Ringkas. Phương án A (QĐ 49): câu R25 mới của Legal; thư theo Legal R37; **xoá thư khi khiếu nại đóng** (repo chỉ giữ ngày + nội dung bị gỡ + loại lý do) | 35 · 49 | PRODUCT-BRIEF |
| R30 | **Luật ký trên phán agent kế toán:** FAIL ở K1/K2/K3 chặn đăng tới khi sửa + agent soát lại; UNVERIFIED · FLAG · "KHỚP NGUỒN THỨ CẤP" (ngoài GĐ01, theo QĐ 37) Duy ký được, kèm một dòng lý do trong bản ghi | 40 | PRODUCT-BRIEF |
| R31 | **Dòng soát công khai:** mục có con số/tên tài khoản hiện *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* (Writer W2); `reviewed_by` = chỉ người ký, agent ở trường riêng; máy cấm "kế toán / accountant / chuyên gia / expert" **trong dòng minh bạch và `reviewed_by`** (không áp cho thân bài) | 41 | PRODUCT-BRIEF |
| R32 | **Ngoại lệ "không trộn"** (AC-05): danh sách tên riêng ngắn, không chú thích, tách khỏi glossary · dòng "chưa có bản EN" song ngữ · chữ VN trên trang EN chỉ khi là mục glossary được đánh dấu, `vi.term` trong thẻ miễn | 43 | PRODUCT-BRIEF |
| R33 | **Rủi ro tổng xác nhận lại QĐ 11 "cho cả 5 phần"** (chữ QĐ 51; dòng QĐ liệt kê: Luật 91 IP khi truyền tải · CC BY 3.0 §7 · hộp thư thu dữ liệu định danh — L18 · minh bạch "agent ≠ người kế toán" · bảng bên thứ ba chưa thấy + sưu tập dữ liệu khi giữ B3 — L16 · hạn 72 giờ vs NĐ 17/2023 — L17). **Workflow pháp lý L13 + L18 chạy trước S5**; L14–L17 sau release. Workflow là research cùng vendor, không phải ý kiến pháp lý (QĐ 12) | 11 · 51 | PRODUCT-BRIEF |

## Ràng buộc có quyền CHẶN — từ Legal

> Không phải ý kiến pháp lý (QĐ 12). Chi tiết, căn cứ, trạng thái verified/gray: `LEGAL-REVIEW.md` §1.
> **CHẶN** nghĩa là: ràng buộc FAIL thì thứ ở cột "Chặn" **không đi tiếp**, không có ngoại lệ do lịch.
> Số hiệu dưới đây là **Legal R1–R37**, khác R1–R29 của PRD.

| Nhóm | Legal R | Chặn | AC |
|---|---|---|---|
| Hermanson: chỉ tr.1–197, redact tr.113 + tr.166 + bảng B2 tr.117 khỏi **lớp chữ**; bảng B3 giữ (QĐ 29, 46); ghi công đúng chữ `attribution_text` + URI CC BY 3.0, card/bài dịch là Adaptation ⇒ có dòng ghi công, file tải trực tiếp được, không làm méo ý. **Mọi section mang trường `based_on` bắt buộc** (thiếu ⇒ build FAIL) + lint tên riêng Hermanson — Legal §A.1, vì CC BY 3.0 §7 chấm dứt giấy phép tự động khi sót ghi công | R1–R8 | Đăng file host và mọi card/bài dựa trên Hermanson | AC-22 – AC-25 · AC-43 – AC-48 |
| Nguồn card: chỉ bài tự viết + Hermanson (cả cuốn, QĐ 28); loại mọi trang trong `licences.json` `exclusions` (gồm tr.113, Legal vòng sửa 2; B3 loại hẳn — QĐ 46) + mọi trang khớp **mẫu ③** (QĐ 47); máy sinh card ghi danh sách file input | R9 · R10 · R12 | Ship card | AC-14 – AC-18 · AC-49 |
| Phạm vi trang Hermanson cho card | R11 | Ship card | AC-18 · AC-19 — **đã quyết QĐ 28, 47, 48:** cả cuốn trừ `exclusions` + mẫu ③; card ch.5+ chỉ đăng khi có **bất kỳ bài `published`** có `based_on` phủ trang (khác đề xuất tr.1–197 của Legal) |
| Sách trả phí chỉ thẻ + link; nguồn NC/all-rights-reserved chỉ deep-link, không tính vào tiến độ | R14 · R15 | Commit asset, đăng trang sách | AC-38 · AC-50 · AC-60 |
| Không mã CK, không khuyến nghị; không bảng lãi có tên ngân hàng; link luật chỉ tới domain chính thức, **phần ra mắt 0 chữ trích nguyên văn** (QĐ 33); EN luật là "unofficial summary"; dòng minh bạch AI + cờ `ai_assisted` theo bài / bộ card / bản EN (QĐ 34, 42); dòng soát công khai + cấm 4 chữ (QĐ 41); disclaimer + ngày hiệu lực | R16–R21 | Đăng bài | AC-37 · AC-51 – AC-54 · AC-86 — định danh trong dòng AI: **BLOCKED — chờ hợp đồng Ringkas** (QĐ 34.2) |
| Tên tài khoản TT 99 + soát kế toán: **agent `ke-toan-reviewer` soát, Duy ký** (QĐ 36); K2 tối đa "KHỚP NGUỒN THỨ CẤP" (QĐ 37); FAIL K1/K2/K3 chặn, phán khác ký kèm lý do (QĐ 40) | R22 | Đăng GĐ01, GĐ05, mọi card có số **+ đoạn bài card đó trích** (QĐ 30) | AC-03 · AC-04 · AC-21 — **BLOCKED — chờ agent chạy thử trên 1 bài mẫu + card (điều kiện 3, QĐ 36)** · GĐ01: **BLOCKED — chờ Phụ lục II chính thức (QĐ 37)** |
| Worker không đọc/lưu IP, UA, cookie; tắt log; câu riêng tư viết đúng chữ; sao lưu chỉ mang field schema (gồm `tel`, không gồm thời điểm — QĐ 26), không tên file | R23–R25 · R28 | Deploy bộ đếm; bật sao lưu | AC-34 · AC-35 · AC-55 – AC-58 — R28: **BLOCKED — chờ đo Zalo** |
| Không rule chặn theo IP do Duy cấu hình ở Cloudflare (QĐ 31) · bộ đếm lưu theo ngày, ẩn ô n < 5 (QĐ 32) | R35 · R36 | Deploy bộ đếm | AC-84 · AC-80 |
| Không tài khoản, bình luận, upload | R29 | **Cổng S5** | AC-26 · AC-40 |
| Dữ liệu người khiếu nại (hộp thư QĐ 35): chỉ dùng cho khiếu nại đó, không chép vào repo/build, không chuyển tiếp; thời hạn giữ: xoá khi khiếu nại đóng (QĐ 49) | R37 | **Cổng S5** | AC-85 · AC-57 — **đã quyết QĐ 49:** phương án A, câu R25 mới, **xoá thư khi khiếu nại đóng**; rủi ro còn lại (L18) trong QĐ 51 — workflow trước S5 |
| Font OFL tự host + OFL.txt; PDF.js pin + LICENSE; mọi asset vào `licences.json` cùng commit | R30 · R31 | Commit asset đầu tiên của S3 | AC-59 · AC-60 |
| foliate-js chỉ khi giữ EPUB | R32 | — | **N/A** — EPUB ra khỏi mùa 1 (QĐ 18) |
| Đường gỡ = nhận khiếu nại + lật cờ. R33 PASS khi đủ (a) kênh khiếu nại công khai trên B10 — **hộp thư riêng cho site** · (b) thời gian in trên trang — **"gỡ tạm trong 72 giờ"** (QĐ 35) · (c) diễn tập cờ, đo bằng phút · (d) diễn tập đầu-cuối khiếu nại giả → 404 trong 72 giờ. Cờ `published` gỡ khỏi build output | R33 | **Cổng S5** | AC-01 · AC-61 — **(a) công khai hộp thư BLOCKED — chờ hợp đồng Ringkas** (QĐ 35); (d) BLOCKED cùng (a) |
| Hợp đồng Ringkas (GĐ05, IP, kế toán là đồng nghiệp — hết áp dụng nếu chỉ có agent soát (QĐ 36), tên miền) | R34 | **S1 chốt**; có thể cắt GĐ05 | điều kiện `blocked_on` — **BLOCKED** |

**Lỗ hổng máy kiểm Legal đã chỉ ra:** `vibe-check [4]` chiều "đĩa → sổ" hiện chỉ quét đuôi âm thanh ⇒ R14, R30, R31 **chưa có máy kiểm thật** cho PDF, ảnh, font, vendor. Phải sửa script **trước** commit asset đầu tiên của S3 (AC-60). Script ở cấp xưởng.

**Rủi ro đã chấp nhận, không có AC:** Legal R26 — host tĩnh và Worker ở nước ngoài đều thấy IP khi truyền tải; thiết kế không loại được. **Duy xác nhận lại QĐ 11 ở QĐ 51**, kèm điều kiện workflow pháp lý L13 + L18 chạy trước S5 (cổng S5, §Delivery Milestones).

## Giọng văn và chữ — tham chiếu `WRITER.md`

Writer sở hữu câu chữ (stages.md). PRD chỉ chở những gì thành **yêu cầu kiểm được**; phần còn lại đọc tại `WRITER.md`.

| Thứ | PRD yêu cầu | Chi tiết | AC |
|---|---|---|---|
| Giọng bài | 5 quy tắc: chuyện của người đọc trước, khái niệm sau · số thay tính từ · không khuyên, không hứa · ngang hàng, gọi "bạn" · kết bằng một câu nối lại đầu bài | WRITER §1 | NGƯỜI (Duy duyệt từng bài — AC-02) |
| Chữ cấm | Danh sách VN/EN máy grep được (có "lưu vĩnh viễn", "nên mua", "guaranteed"…) | WRITER §1 | AC-72 |
| Số VN ⇄ EN | `2,5%` ⇄ `2.5%` · `10.000.000đ` ⇄ `10,000,000 VND`; kiểm số trong card phải hiểu cả hai | WRITER §1 | AC-71 |
| Bối cảnh bản EN | Giữ VND, VietQR, NAPAS 247 — không đổi sang ví dụ Mỹ | WRITER §1 | NGƯỜI |
| Nhãn giao diện | Không dùng "đồng bộ"/"sync" trên giao diện (cơ chế là ảnh chụp gửi một lần). Tên event là chuyện khác (`sync_created`, QĐ 25a) | WRITER §5 | AC-72 |
| Glossary | Thuật ngữ chuyên ngành **giữ tiếng Anh trong dòng** (Debit, Credit, accrual, APR…), mục glossary có cờ `keep_en`, chạm mở chú thích tiếng Việt (QĐ 20); quy ước `Nợ`/`Có` viết hoa cho bên bút toán ở WRITER §3 đã bỏ (Writer đã cập nhật). **`ledger` không `keep_en`: bài VN viết "sổ cái", `ledger` chỉ ở `en.term` trong thẻ** (QĐ 44 — Writer đã cập nhật §3). Tên TK nguyên văn TT 99 PL II (tiếng Việt, vào danh sách gốc của QĐ 21); tên TT 200 vào `aliases`. Nguồn tên TK trong repo hiện chỉ là bản chép thứ cấp `legal/tt99-phu-luc-ii.secondary.json` (QĐ 37). **GĐ01: BLOCKED — chờ Phụ lục II chính thức** | WRITER §3 · QĐ 20 · 21 · 44 | AC-03 · AC-04 · AC-11 – AC-13 |
| Sổ phía ngân hàng (GĐ02) | TT 99 chỉ phủ doanh nghiệp ⇒ WRITER §7 X2 đề xuất **mô tả bằng lời**, không ghi số hiệu tài khoản của ngân hàng. Con số trong sổ ngân hàng GĐ02 không card nào hỏi: **Duy đọc**, không chờ agent kế toán (QĐ 30, 36) | WRITER §7 X2 · QĐ 30 | NGƯỜI |
| Cảnh báo lưu trữ | 3 biến thể theo `persist()`, nói "lâu hơn", không nói "luôn". **Điều kiện ra mắt** (QĐ 18, 45) | WRITER §6 · QĐ 18 · 45 | AC-72 · AC-83 |
| Dòng soát + minh bạch AI | Mục thuộc phạm vi QĐ 30 (có báo cáo agent): VN *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* · EN *"Figures and account names checked by an AI agent; signed off by ⟨…⟩."* (WRITER §5, Duy duyệt EN theo AC-02). Không chứa "kế toán / accountant / chuyên gia / expert" hoặc `ke-toan-reviewer` trong dòng minh bạch và `reviewed_by` (QĐ 41, AC-86). ⟨…⟩ chờ hợp đồng Ringkas (QĐ 34.2) | WRITER §5 · QĐ 41 | AC-21 · AC-86 |
| Dòng "chưa có bản EN" | **Song ngữ**, ngoại lệ có tên của "không trộn" (QĐ 43 b) | WRITER §5 · QĐ 43 | AC-05 · AC-06 |
| Tên và chủ ngữ | Không dịch "Where Money Sleeps"; site tự xưng bằng tên, không "chúng tôi" — **mặc định của Writer, S2 chỉnh được** | WRITER §7 X4 | — |
| Tagline | **T1** (QĐ 22). VN: *"Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu."* · EN: *"From the bank alert to the ledger: where your money actually goes."* Việc của Duy: chụp 3 tin báo biến động số dư thật để xác nhận chữ "ghi có" | WRITER §4 · QĐ 22 | AC-39 · AC-78 |

**Khoảng trống:** giọng của chính Duy (VOICE-PROFILE của xưởng) **chưa tồn tại**; giọng ở WRITER là giọng sản phẩm, rút từ ONE-PAGER.

## Delivery Milestones

| # | Milestone | Outcome người dùng thấy | Status | Plan |
|---|---|---|---|---|
| 0 | Gỡ ba điều kiện S1 | Không có — là cổng. Gồm **một bài mẫu + card nháp dựng tay** (`gates/01-spec/SAMPLE-LESSON-01.md`) và **báo cáo chạy thử của agent `ke-toan-reviewer`** (`gates/01-spec/SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`: `PASS 12 · FAIL 0 · KHỚP NGUỒN THỨ CẤP 6 · FLAG 7`) để **đo thời gian Duy đọc báo cáo + ký** — điều kiện 3 theo QĐ 36; `blocked_on` đã theo chữ QĐ 36 (B-16) | in-progress (bài mẫu + báo cáo agent đã xong 2026-11-07; chờ Duy bấm giờ ký + đo điện thoại + đọc hợp đồng Ringkas) | — |
| 1 | Ra mắt lối vào VN **+ sách** | Người lạ đọc được 12–15 bài, làm card, có glossary, tự khai, nút gạt (mờ khi chưa có EN); **mở Hermanson tr.1–197 đã redact và file PDF của chính mình trong trình đọc; đọc trang sách + thẻ sách** (QĐ 29); **được báo trước nguy cơ mất tiến độ** (`persist()`, QĐ 45) | pending — BLOCKED bởi M0 · phép đo `input type=file` · redact tr.113/166/117 (S3) · thẻ sách (Duy viết) | — |
| 2 | EN cho lối vào | Nút gạt sáng dần theo từng bài đã duyệt EN | pending | — |
| 3 | GĐ01 | Bút toán, T-account; **card Hermanson** bắt đầu đăng được (cần một bài `published` có `based_on` phủ trang — QĐ 27, 28, 48) | pending — **BLOCKED — chờ Phụ lục II TT 99 chính thức** (QĐ 37: bài có tên TK chính thức chỉ đăng khi có bản chính thức) | — |
| 4 | Khái niệm GĐ02 | NAPAS/VietQR sâu | pending | — |
| 5 | Người vay GĐ05 | APR, trả góp — agent kế toán đã soát, Duy đã ký (QĐ 36, 40) | pending | — |

Thứ tự 2–5 là **đề xuất của PM**, chưa có quyết định của Duy. Trình đọc PDF + trang sách + thẻ sách nằm trong M1 (QĐ 29). Sync/sao lưu: chưa có quyết định ra mắt — BLOCKED bởi phép đo Zalo, bật theo cờ khi đo xong.

**Cổng S5 của M1** (ngoài AC-42 + AC-79 + AC-83): **workflow pháp lý L13 + L18 đã chạy và Duy đã đọc kết quả** (QĐ 51; kết quả ghi "same vendor, same priors — no external verifier ran" và "không phải ý kiến pháp lý" — QĐ 12) · diễn tập gỡ AC-61 · dashboard sống AC-69 + ẩn ô n < 5 AC-80 · event về đích nhìn bằng mắt AC-70 — **chỉ event của tính năng ra mắt cùng M1**, nay gồm `pdf_opened{hosted}` và `pdf_opened{own}` (QĐ 29); event còn lại ghi `N/A — because …` · Legal R29 + R33 + R37 PASS (R33 PASS = đủ (a)–(d), không chỉ diễn tập cờ; (a) chờ hợp đồng Ringkas · R37 thêm ở Legal vòng sửa 2, AC-85; câu R25 mới + xoá thư khi đóng — QĐ 49) · Legal R1–R4, R6, R13, R31 + §A.2 PASS (cổng ra mắt QĐ 29, qua AC-79).

**Cổng bật tính năng** (sau S5, mỗi lần một tính năng mang event được bật — hiện chỉ còn sao lưu/khôi phục; bản EN không có event sau QĐ 25b): Duy làm phép kiểm AC-70 cho event của nó ngay ngày bật; FAIL hoặc chưa làm ⇒ tắt lại (AC-74).

## Open Questions

**X1, X2, X3, X5, X6 đã quyết (2026-10-24)** — X1 → QĐ 20 · X2 → QĐ 28 · X3 → QĐ 29 · X5 → QĐ 18 · X6 → QĐ 27. Nội dung cũ và khuyến nghị: `DECISIONS-QUEUE.md` Q-04, Q-11, Q-12, Q-02, Q-10.

**Đã quyết 2026-10-25 (QĐ 38–51).** Nhãn giữ lại vì file khác còn trỏ tới; lập luận lúc hỏi ở `DECISIONS-QUEUE.md` §Lưu trữ.

| Nhãn | Câu | Kết quả |
|---|---|---|
| X4 | ONE-PAGER cũ hơn PRD.md (vibe-check [2] FAIL) | **QĐ 50** — duyệt ONE-PAGER v2; PM **đã áp** vào `gates/ONE-PAGER.md` (`vibe-check [2]` PASS); Duy đọc lại bản đã áp |
| N1 | Thẻ lật tự chấm có tính "đã trả lời" | **QĐ 38** — không tính; mỗi bài `published` ≥ 1 card trắc nghiệm `published` |
| N2 | Ngoại lệ AC-05 ngoài `keep_en` | **QĐ 43** — (a) danh sách tên riêng · (b) dòng "chưa có bản EN" song ngữ · (c) đối xứng cho trang EN |
| N3 | `input type=file` không chạy trong Zalo | **Chưa quyết — câu có điều kiện ĐK-1**, chỉ hỏi nếu phép đo ra "không chạy" |
| N4 | `persist()` có phải điều kiện ra mắt | **QĐ 45** — có |
| N5 | Hạt của `ai_assisted` | **QĐ 42** — bài / bộ card / bản EN |
| N7 | Phán nào của agent cho Duy ký | **QĐ 40** — FAIL K1/K2/K3 chặn; phán khác ký kèm một dòng lý do |
| N8 | Điều kiện 3 của `blocked_on` | **Đóng** — `blocked_on` đã theo chữ QĐ 36 (`DECISIONS-QUEUE.md` B-16) |
| Legal X10 | Bảng B3 che hay giữ | **QĐ 46** — giữ trong file host, loại khỏi máy sinh card; che B2 tr.117; nhận `licences.json` của Legal |
| Legal X11 | Luật máy QĐ 28 | **QĐ 47** — mẫu ③ + `exclusions` |
| Legal X12 | Hộp thư nhận dữ liệu định danh | **QĐ 49** — phương án A, câu R25 mới, R37, xoá thư khi khiếu nại đóng; rủi ro L18 trong QĐ 51 |
| Legal X13 · Writer W2 | Chữ công khai khi người soát là agent | **QĐ 41** — câu W2; `reviewed_by` chỉ người ký; cấm 4 chữ |
| Writer W1 | "sổ cái" hay `ledger` | **QĐ 44** — "sổ cái"; `ledger` chỉ trong thẻ |
| review M4 | Card ch.5+ trỏ về bài nào | **QĐ 48** — bất kỳ bài `published` có `based_on` phủ trang |
| Data M7 | `from_start` | **QĐ 39** — thêm; M1 số chặt + số lỏng |
| K1 · Q-20 | Rủi ro tổng | **QĐ 51** — xác nhận lại QĐ 11; workflow L13 + L18 trước S5 |

**Còn treo**

- [ ] **QĐ 34.2** Chữ định danh trong "duyệt bởi ⟨…⟩" và dòng soát (QĐ 41) — **BLOCKED — chờ Duy đọc hợp đồng Ringkas.**
- [ ] **QĐ 35** Công khai hộp thư khiếu nại — **BLOCKED — chờ Duy đọc hợp đồng Ringkas.**
- [ ] **ĐK-1 · ĐK-2 · ĐK-3** — câu có điều kiện (`DECISIONS-QUEUE.md`), chỉ hỏi khi phép đo/cấu hình ra kết quả xấu.
- [x] **Áp ONE-PAGER v2** (QĐ 50) vào `gates/ONE-PAGER.md` (`vibe-check [2]` PASS); còn việc Duy đọc lại bản đã áp (QĐ 50 ghi "nên đọc lại").
- [ ] **Workflow pháp lý L13 + L18** trước S5 (QĐ 51) — chưa giao ai, chưa có ngày.

**Câu mở khác — không phải câu của Duy ở S1**

- [ ] Ngưỡng North Star — Data đã ghi **cách** đặt (sau ≥ 4 tuần và ≥ 100 lượt bài 1); số đặt sau ra mắt. Ngưỡng đặt trên số chặt hay số lỏng (QĐ 39): chưa quyết — là câu của lúc đặt ngưỡng, không phải câu S1.
- [ ] Mỗi bài bao nhiêu card — S2 + bấm giờ bài mẫu M0 (`DECISIONS-QUEUE.md` B-08). Ràng buộc mới: ≥ 1 card trắc nghiệm (QĐ 38).
- [x] Quy tắc Legal cho "bảng số liệu bên thứ ba" — **đã ra** (LEGAL-REVIEW §A.2, B1–B4); B2 che, B3 giữ (QĐ 46).

## Xung đột giữa các phòng — cho Duy

PM gộp bốn file và thấy các chỗ dưới. **PM không tự quyết.** Chỗ nào đã có quyết định S0 giải thì ghi "đã giải" và lý do. *2026-10-24:* cột "Duy cần" cập nhật theo QĐ 17–35; chỉ K1 còn treo (Q-20). *Vòng sửa 2:* thêm K11 (Legal X13 + Writer W2). *2026-10-25:* K1 → QĐ 51, K11 → QĐ 41 — không còn K nào treo.

| K | Chỗ vướng | Phòng A | Phòng B | Khuyến nghị PM | Duy cần |
|---|---|---|---|---|---|
| **K1** | **Mức rủi ro Luật 91 mà QĐ 11 đã chấp nhận** | LEGAL-SCREEN (S0): "vùng xám nhẹ" | Legal S1, theo `../../../docs/data.md` của xưởng: Đ.20.1.c phủ cả cá nhân, không miễn trừ; không nộp CTIA ⇒ phạt 30–50 triệu (mức tổ chức; cá nhân bằng một nửa, ~15–25 triệu, Điều 7 NĐ 330 theo `../../../docs/data.md` — chưa xác minh; và docs/data.md kết luận đếm lượt không lưu gì định danh thì không phát sinh nghĩa vụ — xem LEGAL-REVIEW X1, hai cách đọc) **và bị buộc ngừng chuyển dữ liệu**. Host nào cũng thấy IP ⇒ thiết kế không tránh được | Câu hỏi #12 | **Đã quyết — QĐ 51:** xác nhận lại QĐ 11; workflow L13 + L18 trước S5 |
| **K2** | Cờ chống trùng `tel` trong JSON tiến độ | Data: `tel` đi theo bản sao lưu, nếu không thì khôi phục xong bắn lại | Legal R28: sao lưu chỉ mang field schema (bài · card · trang PDF · ngôn ngữ). QĐ 7: schema là hợp đồng | Thêm `tel` vào schema **và** vào whitelist R28. `tel` chỉ chứa ID bài/card + `hosted`/`own` + `sent`/`suppressed`, không tên file | **Đã quyết — QĐ 26:** `tel` vào schema, đi theo sao lưu |
| **K3** | Tên event sao lưu | Data: `sync_link_created` → `sync_created{method}`, để Zalo cắt `#` không bắt đổi tên | Writer: "tên event `sync_link_created` vẫn giữ" — ý là nhãn giao diện khác tên event | Nhận tên của Data. Writer không phản đối đổi tên, chỉ nói nhãn ≠ event | **Đã quyết — QĐ 25a:** `sync_created{method}` |
| K4 | Cách hiện chú thích | Writer khuyến nghị C: lần đầu mỗi bài **hiện ngay** | **QĐ 16** (sau): chạm mới hiện, không hiện sẵn | **Đã giải bởi QĐ 16** (dòng sau thắng). Phương án C của Writer không áp. *2026-10-24 (T2 Design):* WRITER TL;DR, §2 và §3 (`Nợ (Debit)` trong dòng) đã được Writer cập nhật theo QĐ 16, 17, 19, 20, 44 | **Đã quyết — QĐ 17 · 19 · 20 · 44** (mở tại chỗ · lần đầu mỗi H2 · giữ EN trong dòng · ngoại lệ "sổ cái"). WRITER §2, §3 đã sửa khớp |
| K5 | `exclusions` trong `licences.json` thiếu tr.113 Home Depot | Legal: thêm dòng có ngày, sửa cơ học | PRODUCT-BRIEF: tr.113 phải loại khỏi máy sinh card | Cho Legal thêm dòng | **S0 đã trả lời** (`DECISIONS-QUEUE.md` B-01) — **Legal đã thêm ở vòng sửa 2** (2026-10-24): `exclusions` nay có tr.113, 166, 501, 803, tr.117 (B2) và B3 tạm loại |
| K6 | Hai bản chữ câu ghi công Hermanson | `licences.json` `attribution_text` | LEGAL-SCREEN dòng "Quyết định 15" (khác chữ, không có URI) | **Đã giải theo chỉ thị S1:** dùng `licences.json`; URI hiện riêng (Legal R4) | Không |
| K7 | Chặn spam ở bộ đếm | Data: chặn theo IP là xử lý IP ⇒ hỏi Legal | Legal R23: Worker không đọc IP | **Chỉ phần mã Worker đã giải** (R23 + QĐ 9): Worker không đọc IP; dùng whitelist + trần ghi. **Phần rule chặn theo IP ở tầng Cloudflare (Rate Limiting/WAF/Bot do Duy cấu hình) chưa giải:** Data khuyến nghị không bật, phát hiện bằng cờ F1–F3 + cách ly ngày (TRACKING-PLAN §2.4) | **Đã quyết — QĐ 31:** không bật rule IP ở Cloudflare |
| K8 | EPUB / foliate-js | Legal X5: PM phải ghi giữ hay bỏ | S0 không quyết; QĐ 4 chỉ nêu PDF | Bỏ khỏi mùa 1; R32 thành N/A | **Đã quyết — QĐ 18:** EPUB ra khỏi mùa 1; R32 N/A |
| K9 | Workers Logs | Legal R24: tắt **hoặc** xác minh không giữ IP | Data: tắt hẳn | **Đã giải:** lấy bản chặt hơn — tắt hẳn (AC-56) | Không |
| **K11** | **Chuỗi ghi duyệt khi người soát là agent (QĐ 36)** · thêm vòng sửa 2 | Writer §3: một chuỗi `reviewed_by` = `soát: agent kế toán (AI) · ký: Duy` (EN `checked by: AI accounting agent · signed off by: Duy`) | Legal X13 (A): `reviewed_by` **chỉ** là người ký; agent ghi ở **trường riêng**; dòng công khai và `reviewed_by` không chứa "kế toán", "accountant", "chuyên gia", "expert". PM (AC-21, theo giao việc): hai phần **soát** / **ký**, phần soát ghi đúng tên agent `ke-toan-reviewer` | Cả ba cùng mục tiêu (agent không bao giờ là người ký; không gợi có người kế toán thật). Lệch ở **hình thức** (một chuỗi hay hai trường) và ở **chữ** ("agent kế toán (AI)" chứa đúng chữ "kế toán" mà Legal đề xuất cấm). AC-21 viết ở mức chung cho cả hai hình thức. PM không chọn | **Đã quyết — QĐ 41:** cấu trúc của Legal (`reviewed_by` chỉ người ký, agent ở trường riêng), câu của Writer W2, cấm 4 chữ trong dòng minh bạch + `reviewed_by` |
| K10 | Nơi lưu bộ đếm | Data: D1 | `../../../docs/data.md` của xưởng: Analytics Engine + kho lạnh | Không chạm quyết định S0; lệch có lý do (giữ dữ liệu > 3 tháng). SWE chốt ở S3 | Chỉ cần biết |

## Câu hỏi cho Duy

**Danh sách câu hỏi, tổng số và thứ tự: [`DECISIONS-QUEUE.md`](DECISIONS-QUEUE.md)** (TRIAGE viết). PRD không đếm và không xếp thứ tự.

**Trạng thái 2026-10-25:** **0 câu nhóm A còn mở.** Q-01…Q-18, Q-21 → QĐ 17–35 · Q-23…Q-25 → QĐ 38–40 · Q-26…Q-34, Q-19, Q-20 → QĐ 41–51 (nhận theo lô) · Q-22 → nhóm B. **Còn:** ĐK-1…ĐK-3 (có điều kiện) · QĐ 34.2 và QĐ 35 (chờ hợp đồng Ringkas).

*Sổ ghi #1–#12 bên dưới là **nhãn tra cứu** — các file khác đang trỏ tới nó. Khuyến nghị và đánh đổi cũ của từng nhãn nằm trong `DECISIONS-QUEUE.md` ở câu Q tương ứng; ở đây chỉ còn kết quả.*

| # | Chủ đề | Kết quả |
|---|---|---|
| 1 | tr.113 vào `exclusions` (K5) | S0 đã trả lời — B-01; Legal đã thêm (vòng sửa 2) |
| 2 | Tên event sao lưu (K3) | **QĐ 25a** — `sync_created{method}`, `progress_restored{method}` |
| 3 | `tel` trong schema + whitelist sao lưu (K2) | **QĐ 26** — thêm, đi theo sao lưu |
| 4 | "Xong bài" | **QĐ 24** — ≥ 1 card đã trả lời + AC-75 · **QĐ 38** — thẻ lật không tính, ≥ 1 card trắc nghiệm |
| 5 | Phạm vi trang Hermanson cho card (X2) | **QĐ 28** — cả cuốn trừ đoạn loại (ngược khuyến nghị tr.1–197 của PM) |
| 6 | EPUB (K8) | **QĐ 18** — ra khỏi mùa 1 |
| 7 | "Trộn ngôn ngữ" (X1) | **QĐ 20** — thuật ngữ chuyên ngành giữ EN trong dòng, `keep_en` (khác khuyến nghị của PM) · **QĐ 43** ngoại lệ · **QĐ 44** "sổ cái" |
| 8 | Trình đọc PDF + trang sách: điều kiện ra mắt? (X3) | **QĐ 29** — là điều kiện ra mắt (ngược khuyến nghị của PM). N3 → ĐK-1 (có điều kiện) |
| 9 | `.ics` · máy tính vay · cảnh báo `persist()` (X5) | **QĐ 18** — `persist()` vào mùa 1; `.ics` ra; máy tính quyết lúc mở GĐ05 · **QĐ 45** — `persist()` là điều kiện ra mắt |
| 10 | Tagline | **QĐ 22** — T1 |
| 11 | Chú thích: đánh dấu + dạng chạm | **QĐ 19** lần đầu mỗi H2 · **QĐ 17** mở tại chỗ |
| 12 | Rủi ro tổng — Luật 91 (K1) | **QĐ 51** — xác nhận lại QĐ 11; workflow L13 + L18 trước S5 |

## Risks

| Rủi ro | Khả năng | Tác động | Giảm thiểu |
|---|---|---|---|
| Link bài giữa chừng chia sẻ qua Zalo thổi M1 lỏng (có thể > 1); người đọc bài 1 ở Safari rồi bài 5 ở WebView Zalo bị tính `from_start=false` ⇒ M1 chặt xẹp ở nhóm đó | TBD — chưa đo cả hai chiều | Đọc sai North Star | Báo cả số chặt lẫn số lỏng (QĐ 39); hướng lệch ròng chưa biết |
| Agent `ke-toan-reviewer` (QĐ 36) cùng vendor, cùng priors với máy sinh card ⇒ sai cùng kiểu và không bắt được nhau | TBD — agent chưa chạy lần nào trên nội dung app này | Card/bài có số sai lọt qua soát | Tin K1 (code chạy lại được) và K2 (so nguyên văn) hơn K3/K4 — FAIL ở K1/K2/K3 chặn đăng (QĐ 40); Duy ký từng mục, kèm lý do khi phán không sạch; chạy thử trên bài mẫu trước khi S1 chốt (điều kiện 3) |
| Thời gian Duy đọc báo cáo agent + ký vượt sức một người | TBD — **chưa đo** (điều kiện 3, QĐ 36) | Ra mắt trễ | Đo ở M0 trước khi hứa ngày |
| Không tìm được Phụ lục II TT 99 chính thức ⇒ K2 tối đa "KHỚP NGUỒN THỨ CẤP" ⇒ bài GĐ01 có tên TK chính thức không đăng được (QĐ 37) | TBD — văn bản gốc vbpl.vn trong repo (32 trang) không có Phụ lục I–IV | GĐ01 trễ; lối vào **không** bị chặn | Tìm trên nguồn chính thức khác (mof.gov.vn, congbao.chinhphu.vn — nguồn agent nêu); chưa ai được giao |
| Khối duyệt ~170–300 lượt (VN + EN) vượt sức một người | Cao (ước tính, **chưa đo** phút/lượt) | Ra mắt trễ | Bấm giờ bài mẫu (M0) trước khi hứa ngày |
| Zalo cắt `#fragment` hoặc WebView không giữ storage | TBD — cần xác minh bằng phép đo của Duy | Sync vô dụng; tiến độ mất | QĐ 7: Zalo cắt `#` ⇒ đổi sang copy mã |
| iOS Safari xoá storage sau 7 ngày không tương tác | Cao (WebKit đã công bố) | Người học tuần một lần mất tiến độ | Mất thì rẻ: tự khai 2 chạm; cảnh báo `persist()` có từ ngày ra mắt (QĐ 45) |
| Card dạy sai mà kiểm máy không bắt (hiểu sai câu trích đúng) | 6–22% ở y khoa/EN — **ngoại suy** sang tài chính VN | Người mới tin điều sai | Duy duyệt từng card; agent kế toán soát card có số, Duy ký (QĐ 36) |
| Hợp đồng Ringkas cấm (IP/không cạnh tranh, mảng vay mua nhà) | TBD — cần xác minh bằng việc Duy đọc hợp đồng | Phải cắt GĐ05 hoặc dừng | Điều kiện trước S1 chốt (QĐ 13) |
| Ước tính 28–30 bài sai | TBD — **chưa đo** | Mùa 1 kéo dài | Ra mắt cần lối vào + phần sách (QĐ 14, 29), không cần GĐ01/02/05 |
| `input type=file` không chạy trong WebView Zalo | TBD — cần xác minh bằng phép đo của Duy | **Chặn ra mắt** (QĐ 29) | ĐK-1 → Duy nếu đo ra không chạy |
| Bảng số liệu bên thứ ba: quy tắc Legal **đã ra** (§A.2), B3 giữ / B2 che (QĐ 46), nhưng soát lần 1 chỉ bằng máy (30 tên công ty Legal chọn, chưa xem bằng mắt) ⇒ có thể còn bảng phải xử lý; giữ B3 mang rủi ro "sưu tập dữ liệu" (L16, gray) | TBD | **Chặn ra mắt** (redact là điều kiện QĐ 29) | S3 liệt kê mọi trang tr.1–197 có bảng số tiền, người xem bằng mắt trang có tên thực thể thật (Legal §A.2, AC-23); B3 bị khiếu nại ⇒ gỡ trang (R33, 72 giờ). Rủi ro đã xác nhận ở QĐ 51 |
| Hộp thư khiếu nại nhận họ tên/email/giấy tờ của người khiếu nại ⇒ Duy xử lý dữ liệu cá nhân có định danh; câu R25 "không thu thập định danh" thành sai khi hộp thư lên trang | Chắc chắn khi có khiếu nại đầu tiên (Legal X12) | Luật 91 Đ.20.1.c nếu nhà cung cấp hộp thư ở nước ngoài (đọc qua nguồn thứ cấp) | Legal R37 (AC-85); câu R25 mới + xoá thư khi khiếu nại đóng (QĐ 49); rủi ro còn lại (L18) đã xác nhận ở QĐ 51, workflow L18 trước S5 |
| Luật máy loại trang (mẫu ③ + `exclusions`, QĐ 47) để lọt đoạn bên thứ ba không mang dấu hiệu | TBD — cả ba mẫu Legal thử đều sót bảng B3 không có chữ "annual report" (LEGAL-REVIEW §A.2); B3 đã biết thì nằm trong `exclusions` | Card trích nội dung bên thứ ba | Rủi ro Duy nhận (QĐ 28, 51); Duy duyệt từng card |
| Mẫu ③ (QĐ 47) loại **quá rộng**: 132/1004 trang, ~41 trang oan (vd tr.24–25, Hermanson tự viết về FASB); "annual report" xuất hiện 32 lần ở tr.1–197, gồm đoạn định nghĩa (số đo của Legal) | Cao | Kho card Hermanson nhỏ hơn dự tính | Duy nhận ở QĐ 47; card trang > 197 chỉ đăng khi có bài phủ trang (QĐ 28) ⇒ mùa 1 gần như không tốn. Muốn hẹp lại thì Duy thêm dòng |
| Luật 91: IP khi truyền tải bị coi là dữ liệu cá nhân ⇒ cần hồ sơ CTIA | TBD — cần xác minh bằng workflow câu L13 + đối chiếu văn bản gốc | Phạt + có thể bị buộc ngừng chuyển dữ liệu | QĐ 51: rủi ro xác nhận lại; **workflow L13 chạy trước S5** |
| Workers Logs mặc định bật ⇒ lưu metadata request mà không ai viết dòng code nào | Cao nếu không ai tắt (Cloudflare docs, TRACKING-PLAN §3) | Phá lời hứa không định danh | AC-56; S4 mở dashboard Cloudflare xác nhận không có log |
| Event bắn đúng ở code nhưng không về đích; dashboard trống | TBD | Mất dữ liệu không hồi tố được | AC-69 · AC-70 — nhìn số bằng mắt ở S4 |

## Chưa xác minh được

- Toàn bộ hành vi trên điện thoại thật: Zalo `#fragment`, WebView hay trình duyệt, `input type=file`, iOS 26 có tách storage tab ↔ app, `persist()` trên iPhone.
- Số bài thật của mùa 1 (~28–30 là ước tính) và số card (84–150 VN là ước tính).
- Thời gian duyệt một bài + card: Duy đọc bài, và Duy đọc báo cáo agent kế toán rồi ký (điều kiện 3, QĐ 36). Agent `ke-toan-reviewer` **đã chạy thử** trên bài mẫu `SAMPLE-LESSON-01.md` (báo cáo `SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`: `PASS 12 · FAIL 0 · KHỚP NGUỒN THỨ CẤP 6 · FLAG 7`), chờ Duy bấm giờ ký.
- Bản chép Phụ lục II (`legal/tt99-phu-luc-ii.secondary.json`): hai nguồn bên thứ ba; một nguồn chỉ trích đoạn (file tự ghi). Phụ lục II chính thức: chưa có trong repo, chưa biết lấy ở đâu (QĐ 37).
- Tỉ lệ người học có PDF muốn đọc trong site — không có số liệu.
- Tỉ lệ sai của card LLM trên văn bản tài chính tiếng Việt — mọi số đều ngoại suy.
- Nhu cầu tầng sâu ngoài Duy (n=1).
- Giá/hạn mức free của dịch vụ đếm (QĐ 9 ghi "chưa kiểm"). *2026-10-24:* Data đã đọc hạn mức D1/Analytics Engine; còn chưa rõ D1 tính `UPSERT` + `WITHOUT ROWID` là mấy dòng ghi, và lưu lượng thật không có ước tính (TRACKING-PLAN §7).
- Dạng chạm cho chú thích: QĐ 17 chốt **mở tại chỗ** làm mặc định, nhưng **chưa dạng nào được thử trong WebView Zalo** và chưa nghiên cứu nào so trực tiếp các dạng ⇒ buổi 5 người so với "thẻ phủ lên chữ".
- Máy nhận ra một từ trên trang VI là "chữ EN" thế nào (AC-05): từ VN không dấu trùng chữ EN ("do", "to", "an") — S3 chọn cách, không đổi tiêu chí.
- Hộp thư khiếu nại có lộ danh tính qua header/WHOIS không (QĐ 35 ghi chưa kiểm). 72 giờ là đề xuất của Legal, chưa đối chiếu NĐ 17/2023 Đ.114.
- Ngưỡng N giờ của "phiên"; Zalo có mở mỗi link trong một WebView mới không (quyết định có dùng được `sessionStorage` không).
- Tỉ lệ người vào thẳng trang bài so với vào trang chủ — không đo được (không đo referrer).
- URL gốc trên Công báo/vbpl.vn của các luật Legal dẫn (Luật CK 2019, NĐ 147, Luật AI 134, Luật 91, NĐ 356, NĐ 330): **chưa đối chiếu**. CC BY 3.0 §4(b)(iv) chưa đọc nguyên văn (LEGAL-REVIEW §Chưa xác minh).
- Tin báo biến động số dư của ngân hàng VN có thật sự in chữ "ghi có" không — tagline T1 và quy tắc giọng 1 dựa vào đó (WRITER §Chưa xác minh).
- Tagline có vừa một dòng ở bề ngang 360px không — chờ mockup S2.
- Link sao lưu có `tel` dài bao nhiêu và Zalo có giữ nguyên không — chờ phép đo của Duy.
- QĐ 41–51 nhận theo lô **trước khi Duy đọc từng bảng phương án** (PRODUCT-BRIEF.md:179). PRD áp đúng chữ khuyến nghị; Duy chưa thấy chữ PRD sau khi áp.
- Câu dòng soát W2 (QĐ 41) và câu R25 mới (QĐ 49) chưa đối chiếu Luật AI 134/2025 (L14) và Luật 91 (L18); bản EN của câu R25 mới đã có ở WRITER §5 (Duy duyệt theo AC-02).
- Số đo mẫu ③ (132/1004 trang, ~41 oan, 7/7 trang đã biết) là của Legal (LEGAL-REVIEW §A.2), PM chưa chạy lại.
- Bản gộp S1 đã qua review kiểm chéo sau QĐ 38–51 (2026-11-07). Same vendor, same priors — no external verifier ran.

---
*Status: DRAFT — requirements only. Implementation planning pending via /ecc:plan sau khi S1 được Duy duyệt.*

## T2 — câu hỏi chéo-phòng

> Quy tắc 12 T2. PM sở hữu PRD.md và ACCEPTANCE.md, **không** sở hữu WRITER.md. Trả lời ngày 2026-10-24.
> Same vendor, same priors — no external verifier ran.

### Từ Data → PRD + ACCEPTANCE

**Data câu 1** — nguyên văn: *"Event của một tính năng không ra mắt cùng M1 thì được kiểm "về đích" (AC-70) và lên dashboard (AC-69) vào lúc nào?"*

| | |
|---|---|
| Trả lời | **Lúc bật từng tính năng, không chỉ ở S5.** Data đúng: AC-69/AC-70 đặt một cổng duy nhất ở S5, nên tính năng bật sau S5 không còn ai bắt phải nhìn số. PM nhận đúng khuôn Data đề nghị: ở S5 ghi `N/A — because <tính năng chưa bật>, kiểm lúc bật <tên>`; lúc bật, Duy làm phép kiểm AC-70 cho event đó ngay trong ngày, FAIL hoặc chưa làm ⇒ tắt lại (gỡ trước, tranh luận sau). PM thêm một trường hợp cùng loại mà câu hỏi chưa nêu: **bản EN đầu tiên** — `lesson_completed{lang: en}` không thể có lúc ra mắt (nút gạt mờ) |
| Vì sao PM tự quyết, không → Duy | Không quyết định S0 nào nói gì về việc này; nó chỉ làm quy tắc 8 ("xong = đã nhìn thấy số") đúng với cách ra mắt theo cờ của QĐ 14. Đảo ngược rẻ. Duy thấy nó khi duyệt S1 |
| Đã sửa | PRD: §Success Metrics thêm một dòng ràng buộc · Scope dòng 16 · §Delivery Milestones (cổng S5 hẹp lại + "Cổng bật tính năng"). ACCEPTANCE: thêm **AC-74**; §Thay đổi ghi phạm vi mới của AC-69/AC-70 (không sửa tại chỗ) |
| Chưa giải | Phép kiểm trên máy thật cần tính năng chạy ở đâu đó mà event về **đúng** bộ đếm (AC-68: cùng origin). Bật thật rồi kiểm, hay có bản xem trước có bộ đếm riêng — **việc của SWE ở S3**, PRD không chọn "làm thế nào" |

**Data câu 2** — nguyên văn: *"PRD đề xuất "xong bài = đã trả lời ≥ 1 card cuối bài". Vậy khi card cuối cùng còn `published` của một bài bị gỡ, bài đó còn "xong" được không?"*

| | |
|---|---|
| Trả lời | **Không — và PRD không để chuyện đó xảy ra.** Khuyến nghị: phương án thứ nhất của Data — gỡ card `published` cuối cùng ⇒ build FAIL cho tới khi gỡ luôn bài **hoặc** đăng card thay đã duyệt. Phương án "điều kiện xong dự phòng" bị loại vì trái chính ràng buộc của Data: *một điều kiện, giống nhau ở mọi bài* |
| → Duy | **Gộp vào câu hỏi #4** (nhãn sổ ghi; số câu thật: `DECISIONS-QUEUE.md`). Bất biến này chỉ tồn tại nếu Duy nhận định nghĩa "xong" của #4; cột "Đánh đổi thật" của #4 giờ nói rõ cái giá: gỡ một card sai có thể kéo cả bài lối vào xuống |
| Đã sửa | PRD: câu hỏi #4 (hệ quả hai chiều + đánh đổi) · §Định nghĩa "xong bài" · Scope dòng 12. ACCEPTANCE: thêm **AC-75** (TBD hẳn, chờ #4) |
| Trả lại Data | Kể cả với AC-75, những ngày bài bị gỡ thì `lesson_completed` của bài đó vẫn bằng 0 ⇒ M2 vẫn có một bước rơi **thật nhưng không phải lỗi của bài**. Ngày gỡ/bật lấy được từ lịch sử commit của cờ `published`. M1/M2 bỏ khoảng đó ra thế nào là việc của Data trong `SUCCESS-CRITERIA.md` — PM không sửa file của Data |

### Từ Design → PRD + WRITER

**Design câu 1** — nguyên văn: *"Vậy S2 dựng theo bên nào? Và "lần đầu mỗi mục" tính theo `sectionId` (khuyến nghị của PRD) hay theo H2 (khuyến nghị của RESEARCH)? Hai cái này có phải là một không?"*

| | |
|---|---|
| Trả lời | **Dựng theo PRD, không theo WRITER.** QĐ 16 thắng phương án C của Writer (K4 đã giải); WRITER chưa cập nhật theo. **`sectionId` và H2 giờ là một:** PRD định nghĩa `sectionId` = một mục H2 (§Định nghĩa dùng chung), vì chưa file nào định nghĩa nó, và vì AC-08 ở cấp đoạn văn sẽ FAIL mỗi khi bản dịch tách/gộp đoạn. Hai khuyến nghị gộp làm một trong câu hỏi #11 |
| → Duy | Hai chỗ vẫn của Duy và đã có trong danh sách: **#7** (`Nợ (Debit)` trong dòng có tính là trộn ngôn ngữ không) và **#11** (đánh dấu theo mục H2 + dạng chạm). S1 chưa duyệt thì S2 chưa mở, nên hai câu này sẽ có trả lời **trước** khi S2 vẽ mockup |
| → Writer | Cập nhật WRITER TL;DR, §2 (khuyến nghị C) và §3 (dạng hiển thị `Nợ (Debit)`, "các lần sau" tính theo bài) theo QĐ 16 và theo câu trả lời #7, #11 của Duy. PM không sửa file của phòng khác |
| Đã sửa | PRD: B5 (bỏ "research chưa có") · bảng K4 · câu hỏi #11 (thêm khuyến nghị dạng chạm từ research, kèm cảnh báo 2/4 mũi) · §Định nghĩa dùng chung (`sectionId`) · §Open Questions · §Chưa xác minh. ACCEPTANCE: thêm **AC-77**; trạng thái AC-73 |

**Design câu 2** — nguyên văn: *"Vậy link chia sẻ trỏ thẳng vào một bài (B3) có phải là một cửa vào không? Nếu có, thì ba thứ sau xảy ra ở bề mặt nào khi người đọc vào thẳng B3 … Và "phiên" được định nghĩa thế nào?"*

| | |
|---|---|
| Trả lời — cửa vào | **Có.** Đây là sự thật của một site tĩnh có URL cho từng trang (AC-10), không phải một lựa chọn. Không đo được cửa nào là chính (không đo referrer) ⇒ S2 thiết kế cho **cả hai** |
| Trả lời — card ôn | Ở **bề mặt đầu tiên của phiên**, B1 hoặc B3. Nguồn ADDENDUM bước 9 nói "đầu phiên sau", không nói "ở trang chủ" — PRD cũ hẹp hơn nguồn, giờ sửa cho khớp. PM thêm: **không chặn đọc**, bỏ qua bằng 1 chạm, vì người vào thẳng B3 đến để đọc đúng bài đó |
| Trả lời — mời tự khai | Vào B3 khi chưa có tiến độ ⇒ có lối vào B9, **không chặn đọc**. Không phân biệt được người mới hẳn với người mất storage, nên không được bắt người mới đi qua màn tự khai |
| Trả lời — tagline | R16 áp cho mọi chỗ tên xuất hiện, kể cả header trang bài và thẻ chia sẻ `og:` của link bài. Trang bài không bắt buộc hiện tên |
| Trả lời — "phiên" | Lần mở site mà lần hoạt động cuối trong JSON tiến độ đã cách ≥ N giờ. **N: TBD — S2 đề xuất, kiểm ở buổi 5 người.** Không dùng `sessionStorage` vì có thể mỗi link Zalo là một WebView mới (chưa đo). Định nghĩa này cần một trường thời điểm trong schema tiến độ — đề xuất **không** đi theo bản sao lưu, nên không chạm Legal R28 |
| → Duy | Cửa vào, card ôn, mời tự khai, tagline: không — khớp nguồn đã duyệt hoặc là định nghĩa S1 phải tự có. **Trường thời điểm trong schema: → Duy (Q-xx)** — QĐ 7 coi schema là hợp đồng, cùng loại với `tel` (K2). *Sửa 2026-10-24 (vòng sửa):* bản trước ghi "→ Duy: Không" và tự thêm trường; đó là PM quyết thay Duy |
| Đã sửa | PRD: sơ đồ bề mặt (thêm hai cửa vào) · B1, B3, B4, B9 · §Định nghĩa dùng chung (phiên, cửa vào, tagline trên trang bài) · §Chưa xác minh. ACCEPTANCE: thêm **AC-76**, **AC-78** |

## T3 — chỗ lệch với bản tái lập

> Quy tắc 12 T3, 2026-10-24. So `T3-RECONSTRUCTION.md` (dựng lại từ S0, không đọc 01-spec) với `PRD.md` · `ACCEPTANCE.md` · `SUCCESS-CRITERIA.md` · `TRACKING-PLAN.md` · `LEGAL-REVIEW.md`.
> **Không phân xử.** Hai phiên cùng gốc bất đồng = câu S0 chưa rõ. Mỗi dòng ghi cả hai lập luận và câu S0 gây ra lệch; chỗ nào cần Duy thì leo lên Duy, không gọi phiên thứ ba bỏ phiếu.
> Same vendor, same priors — no external verifier ran.

**Gốc chung của Δ2–Δ5:** S0 không nói bảng `PRODUCT-BRIEF §Kiến trúc đề xuất ở mức S0` (thân bài, viết **trước** quyết định) còn hiệu lực ở chỗ không quyết định nào thay hay không. T3 coi là **còn hiệu lực**. S1 dùng không nhất quán: lấy `Nợ (Debit)` từ đó làm căn cứ xung đột (X1), nhưng coi cảnh báo `persist()` cùng bảng là "không quyết định nào nhắc" (X5), và bỏ sót hai dòng khác.

| Δ | Nội dung | Bản T3 nói | Bản S1 nói | Câu S0 mơ hồ gây lệch |
|---|---|---|---|---|
| Δ1 | Thẩm quyền của thân Brief | §Kiến trúc còn hiệu lực khi không bị quyết định nào thay | Thân Brief = đề xuất, chỉ vào nếu quyết định nhắc (X5) — nhưng vẫn dùng một phần (X1) | Chỉ thị S0: *"thân bài viết trước quyết định"* — không nói thân bài **mất** hiệu lực hay chỉ **thua** khi trái quyết định |
| Δ2 | `Nợ (Debit)` trong dòng chữ | Là yêu cầu (A5) | Xung đột với QĐ 6; khuyến nghị bỏ khỏi dòng chữ, đưa vào chú thích chạm (X1, #7) | Brief §Kiến trúc *"viết 'Nợ (Debit)'"* × QĐ 6 *"không trang nào trộn ngôn ngữ"* — "trộn" không định nghĩa |
| Δ3 | Cảnh báo lưu trữ theo `persist()` | Trong mùa 1 (A19, BLOCKED — chờ đo iPhone) | Ngoài phạm vi cho tới khi Duy nói; khuyến nghị đưa vào (X5, #9) | QĐ 7 liệt kê 4 thành phần, không có `persist()`; Brief §Kiến trúc dòng "Cảnh báo lưu trữ" có |
| Δ4 | "Giữ ID mồ côi" · "không auto-redirect" | Có trong A16, A15 | **Không nhắc** ở PRD lẫn ACCEPTANCE (AC-29, AC-10) — không loại có chủ ý, chỉ vắng | Chỉ ở Brief §Kiến trúc, không quyết định nào nhắc lại |
| Δ5 | Ôn 1–2 card đầu phiên | Chưa quyết — S1 phải hỏi, không tự thêm | Trong phạm vi: Scope #2, R18, AC-20, AC-76; S1 còn tự định nghĩa "phiên" (N giờ) | Chỉ thị: ADDENDUM *"chỉ §Đường ống card + ràng buộc định dạng card còn hiệu lực"* — bước 9 nằm trong §Đường ống nhưng là **hành vi**, không phải định dạng; "+" là hợp hay giao không rõ |
| Δ6 | Số card mỗi bài | 3–5 (theo ADDENDUM) | TBD — xác minh bằng bấm giờ bài mẫu | "3–5" nằm ở ADDENDUM §Đề xuất hình dạng tính năng và TL;DR, **ngoài** §Đường ống |
| Δ7 | Trình đọc PDF + trang sách + thẻ sách có là điều kiện ra mắt | Trong mùa 1, không thấy xung đột | TBD (X3); khuyến nghị ra cùng GĐ01 (#8) | QĐ 4 *"Mùa 1 CÓ trình đọc PDF"* (QĐ 2: "bắt buộc") × QĐ 14 *"ra mắt khi lối vào … đã duyệt xong"* — "mùa 1" và "ra mắt" chưa được phân biệt |
| Δ8 | Phạm vi trang Hermanson cho máy sinh card | Không giới hạn trang, chỉ trừ `exclusions` (A7); không nêu xung đột | Chưa quyết (X2, Legal R11); đề xuất chỉ tr.1–197 | QĐ 3 *"sách CC BY (Hermanson)"* không giới hạn trang × QĐ 15 chỉ host + soát ảnh tr.1–197 |
| Δ9 | tr.113 (Home Depot) trong `exclusions` | Liệt kê `exclusions` **không có** tr.113, đánh "sẵn sàng" (A7) | Thiếu tr.113, cần thêm dòng có ngày (K5, Legal X3, #1) | Dòng soát sau QĐ 15 *"loại khỏi máy sinh card"* × `licences.json` `exclusions` chưa cập nhật — hai nguồn S0 nói khác nhau |
| Δ10 | Thuật ngữ thiếu glossary ⇒ build FAIL | Làm được bằng máy nếu có markup (A3); cách đánh dấu chưa có (X7) | Máy chỉ kiểm thuật ngữ **đã** có trong glossary (AC-11); thiếu mục do người bắt (AC-12). **Không ghi là xung đột với QĐ 5** | QĐ 5 cột lý do: *"thêm được một phép kiểm máy: thuật ngữ nào xuất hiện mà không có mục glossary thì FAIL"* — không nói máy nhận ra "thuật ngữ" bằng cách nào |
| Δ11 | Ngôn ngữ card từ Hermanson (nguồn EN) | Nêu xung đột (X6): card VN mà `source_quote` phải khớp chuỗi EN? Người học đọc bản EN hay bản dịch? | **Không nêu.** AC-15 đòi khớp nguyên chuỗi; AC-71 chỉ xử lý định dạng số | QĐ 3 (nạp Hermanson) × ADDENDUM bước 5 (`source_quote` khớp nguồn) — không nói ngôn ngữ |
| Δ12 | `card_answered.correct` với thẻ lật tự chấm | Nêu xung đột (X5): "Nhớ/Chưa nhớ" là tự báo, trộn vào M3 làm hỏng câu hỏi card sai | `correct: true\|false` cho mọi card; M3 = "sai lần đầu"; **không** tách hai loại thẻ | ADDENDUM bước 8 *"trắc nghiệm … hoặc lật thẻ rồi tự chấm Nhớ/Chưa nhớ"* × QĐ 9 `card_answered {card, correct}` |
| Δ13 | Hướng lệch của M1 | Có thể **thổi**, thậm chí > 1: tự khai bỏ qua bài 1 rồi đọc bài 5 ⇒ tử tăng, mẫu không | **Xẹp** (TRACKING-PLAN §2.3): mất storage đọc lại từ bài 1 ⇒ mẫu thổi nhiều hơn tử; người tự khai không bắn. Cả hai **chưa đo** | ONE-PAGER §4 *"bị thổi lên bởi người tự khai giai đoạn…"* — không nói tự khai đánh dấu bài nào, bài **sau** mốc tự khai có bắn không |
| Δ14 | Ngưỡng M1 | ONE-PAGER giao S1 đặt; không nguồn ⇒ ghi "TÔI CHỌN" (data.md) | Không đặt số ở S1; Duy đặt sau ≥ 4 tuần và ≥ 100 lượt bài 1 | ONE-PAGER §4 *"Ngưỡng do S1 đặt"* — đặt **số** hay đặt **cách** |
| Δ15 | Tên event sao lưu | Giữ nguyên tên QĐ 9 ("T3 không đổi tên nào") | `sync_link_created` → `sync_created{method}`; `progress_restored` thêm `method` — chờ Duy (K3, #2) | QĐ 9 *"Event dự kiến (S1 chốt tên, tên là hợp đồng)"* × QĐ 7 *"Zalo cắt # ⇒ sync chuyển sang copy mã"* |
| Δ16 | Event cho tự khai · mời cài · kết quả `persist()` | Nêu: Brief từng muốn đo "lượt xem trang khôi phục / tự khai"; không quyết định nào giữ hay bỏ | Không có event; **cũng không** có trong "Không đo — cố ý" (SUCCESS-CRITERIA §3) | QĐ 9 chỉ là danh sách "dự kiến" × Brief §Đo cái gì dòng "Lượt xem trang khôi phục / tự khai" |
| Δ17 | Lúc bắn + cách gửi | Bắn ở `visibilitychange` (data.md); `sendBeacon` hay `fetch keepalive`: S1 phải chọn (X4) | `sendBeacon`; gửi **ngay** lúc sự kiện, mất mạng thì xếp hàng, xả ở `visibilitychange` (AC-67) | QĐ 9 ghi `sendBeacon` × `../../../docs/data.md` (xưởng, viết cho noelroom) ghi `fetch keepalive` ở `visibilitychange` |
| Δ18 | Nơi lưu bộ đếm | Áp quy tắc Analytics Engine: `sum(_sample_interval)`, giữ 3 tháng | Chọn D1, khai là lệch có chủ ý khỏi data.md (K10) | QĐ 9 *"Chưa kiểm: giá/hạn mức … Analytics Engine hay D1"* — không chọn nơi lưu |
| Δ19 | Hạ tầng site | Xung đột (X3): QĐ 9 "cùng domain" thực chất đã chốt Cloudflare ở S1, trái Brief "khung site chốt ở S3"; chưa có domain ⇒ subdomain `workers.dev` riêng | Nêu như hệ quả (Workers Static Assets), không nêu là xung đột với Brief; đăng ký domain chạm Legal R34 | QĐ 9 *"cùng domain"* × Brief thân bài để khung site cho S3 |
| Δ20 | Phạm vi soát của kế toán | Đúng chữ QĐ 8: bài GĐ01, GĐ05 + card có con số (A2) | PRD TL;DR: *"mọi bài/card có con số"*; Risks: bài lối vào **có** con số cần kế toán. AC-03 lại theo đúng QĐ 8 ⇒ S1 tự lệch trong nội bộ | QĐ 8 (GĐ01 · GĐ05 · card có số) × lý do QĐ 14 *"câu 8 × bài lối vào có con số ⇒ không có kế toán thì không đăng được gì"* |
| Δ21 | QĐ 16 có thuộc gói S0 đã duyệt | Không rõ (X2): PIPELINE APPROVE "15/15", Brief có dòng 16; ONE-PAGER chưa nhắc QĐ 15, 16 | Coi QĐ 16 có thẩm quyền ("16 quyết định", dòng sau thắng); X4 chỉ nêu status + "14" của ONE-PAGER, không nêu thiếu QĐ 15/16 | PIPELINE Log APPROVE S0 "15" × Brief dòng 16 cùng ngày, sau APPROVE |
| Δ22 | Mức rủi ro Luật 91 | "Vùng xám nhẹ" (L8, theo LEGAL-SCREEN) | Nặng hơn: Đ.20.1.c phủ cá nhân, buộc ngừng chuyển dữ liệu; Duy xác nhận lại QĐ 11 (Legal X1, K1, #12) | LEGAL-SCREEN §Kết luận "vùng xám nhẹ" × `../../../docs/data.md` §Pháp lý VN; QĐ 11 chấp nhận dựa trên nhãn LEGAL-SCREEN |
| Δ23 | Lỗi ghi công Hermanson có gỡ được bằng cờ không | L4, L10 "đã chốt": cờ `published` là đường gỡ | Không: CC BY 3.0 §7 chấm dứt tự động; cần `based_on` bắt buộc mọi section (Legal §A.1, X7, L15) | Lý do QĐ 11 *"rủi ro … do khiếu nại kích hoạt; có cờ `published` để gỡ"* |
| Δ24 | Kênh nhận khiếu nại | Không có; cờ `published` là đủ (L10) | R33 PASS cần kênh công khai trên B10 + thời gian phản hồi in ra (a–d); (a) BLOCKED — chờ hợp đồng Ringkas (Legal X8) | LEGAL-SCREEN *"gỡ trước, tranh luận sau"* không nói nhận khiếu nại ở đâu; Brief §Đề bài đã nắn lại có nhắc NĐ 17/2023 Đ.114 |
| Δ25 | Máy tính khoản vay (GĐ05) | Bỏ ra thì GĐ05 thiếu thứ thay bảng lãi (X8) | PRD: quyết lúc mở GĐ05 (#9), R17 chỉ ràng "không bảng lãi". LEGAL-REVIEW R17 lại ghi *"Thay bằng máy tính"* trong chính ràng buộc ⇒ S1 tự lệch | Brief + LEGAL-SCREEN đề xuất máy tính; QĐ 5 kéo GĐ05 vào mà không nhắc máy tính |

**S1 có, T3 không có — không truy được về một câu S0** (T3 im lặng, không phải bất đồng; vẫn là chỗ S1 tự định nghĩa thay S0): `sectionId` = mục H2 · "phiên" = ≥ N giờ · B3 là cửa vào · tagline ở mọi chỗ có tên (AC-78) · trường `tel` trong schema (K2) · bất biến bài ↔ card (AC-75) · cấm chặn spam theo IP kể cả ở edge · ẩn ô n < 5 · mẫu số M5 = bài 3.

**Khớp, không lệch:** CC BY 3.0 + tr.1–197 + redact tr.113/166 · không LLM runtime · cờ `published` mặc định false · EPUB và `.ics` chưa quyết (cả hai bản để Duy) · "xong bài" S0 không định nghĩa · ba mục BLOCKED theo đúng ba điều kiện của Duy · ONE-PAGER còn `draft` (X1 T3 = X4 PRD).

**Sau QĐ 17–35 (2026-10-24):** Δ1–Δ5 · Δ25 → QĐ 18 · Δ2 → QĐ 20 · Δ7 → QĐ 29 · Δ8 → QĐ 28 · Δ10 → QĐ 21 · Δ11 → QĐ 27 · Δ12 → QĐ 25d · Δ13 → QĐ 23 · Δ15, Δ16 → QĐ 25 · Δ20 → QĐ 30 · Δ24 → QĐ 35. Còn treo: Δ14, Δ21 (ONE-PAGER — Q-19) · Δ22, Δ23 (rủi ro tổng — Q-20). Bảng Δ ở trên giữ nguyên làm lịch sử lệch, cột "Bản S1 nói" là trạng thái **trước** các QĐ này. **Sau QĐ 38–51 (2026-10-25):** Δ14, Δ21 → QĐ 50 · Δ22, Δ23 → QĐ 51 · Δ12 thêm QĐ 38 · Δ13 thêm QĐ 39. Không còn Δ treo.

**Leo lên Duy — chưa có trong sổ ghi #1–#12 (TRIAGE gộp vào `DECISIONS-QUEUE.md`):** Δ1 (thẩm quyền thân Brief — gỡ luôn Δ2–Δ5), Δ10, Δ11, Δ12, Δ13, Δ14, Δ16, Δ20, Δ21, Δ23 (đã có ở Legal X7 nhưng chưa vào danh sách câu hỏi). PM **chưa** sửa số câu, thứ tự hay khuyến nghị — việc đó cần một lượt gộp riêng.

**Chưa xác minh được (mục này):** mọi hướng lệch ở Δ13 là lập luận, chưa có số · Δ4 có thể là bỏ sót của PM chứ không phải lựa chọn — chưa hỏi · bảng chỉ so năm file được giao, không so WRITER.md hay RESEARCH-GLOSSARY-UX.md.

## Đổi ở vòng sửa 2026-10-24

Theo review S1 vòng 1 (falsify + consistency + T3). PM sửa tại chỗ vì file là nháp chưa duyệt. Chỗ nào là quyết định của Duy ghi "→ Duy (Q-xx)"; TRIAGE xếp vào `DECISIONS-QUEUE.md`. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Vì sao |
|---|---|---|
| K1 · K10 · T3 Δ17 · Δ22 | Đường dẫn tương đối tới data.md của xưởng sửa thành `../../../docs/data.md` (bản cũ thiếu `../../../`) | Đường dẫn chết, vibe-check [5] |
| TL;DR · §Câu hỏi cho Duy · T2 Data câu 2 · T3 "Leo lên Duy" | Bỏ con số "12 câu"; §Câu hỏi giờ trỏ tới `DECISIONS-QUEUE.md`. Bảng #1–#12 giữ lại làm **sổ ghi khuyến nghị** (nhãn tra cứu, không phải số câu) | Tổng thật lớn hơn nhiều (10 Δ T3, Legal X7, X8, Data T2, ngưỡng AC-51, AC-61…). Giữ bảng vì các file khác trỏ tới nhãn #n và file chưa có trong git — xoá là mất nguồn của TRIAGE |
| TL;DR dòng 2 · Risks dòng 1 | Phạm vi kế toán theo đúng QĐ 8: GĐ01 · GĐ05 · card có con số | Bản cũ ghi "mọi bài/card có con số", rộng hơn QĐ 8 (T3 Δ20). Mở rộng hay không vẫn là câu của Duy (Δ20) |
| TL;DR dòng 3 | "3 bề mặt bị chặn" → 2 bề mặt + lời mời cài (không phải bề mặt) | Tự mâu thuẫn với §Bản đồ bề mặt |
| M1 (§Success Metrics) | Bỏ hành động "dừng mở thêm bài sâu"; → Duy (Q-xx) | Trái QĐ 14 *"phạm vi câu 5 không bị cắt"*. `SUCCESS-CRITERIA.md:23` còn ghi "dừng mở thêm bài GĐ01/02/05" — Data phải đổi cùng chữ; PM không sửa file Data |
| Ràng buộc từ Data | Thêm 2 dòng: hàng đợi offline và trường thời điểm "phiên" là mở rộng schema QĐ 7 → Duy (Q-xx) | Cùng loại `tel` (K2) nhưng bản cũ tự thêm |
| Scope 6 · B9 | Tự khai: bỏ "Sẵn"; → Duy (Q-xx) | Chưa định nghĩa theo giai đoạn hay từng bài |
| Scope 8 | "đã redact" → "sẽ redact ở S3" | Việc redact chưa làm |
| Scope 14 · B10 · Legal R33 · Cổng S5 | Thêm kênh khiếu nại + giờ phản hồi; R33 PASS = (a)–(d); (a) BLOCKED — chờ hợp đồng Ringkas; → Duy X8 (Q-xx) | Việc Legal giao (LEGAL-REVIEW §T2) |
| Scope 17 | Thêm diễn tập đầu-cuối khiếu nại → 404 | R33 (d) |
| Scope 18 · §Open Questions dòng AI | Bỏ `[x]`; → Duy (Q-xx) | R20 còn gray; tên Duy công khai khi R34 BLOCKED; câu "hỗ trợ AI" có thể sai với bài tự viết |
| Legal R1–R8 | Thêm `based_on` bắt buộc + lint tên riêng | Legal §A.1; CC BY 3.0 §7 |
| B4 · X6 mới | Card Hermanson: xung đột chưa giải (ngôn ngữ · đơn vị · trang PDF vs `sectionId`) → Duy (Q-xx) | Review S1 B3, T3 Δ11 |
| K7 · Out of scope | Chỉ phần mã Worker đã giải; rule IP tầng Cloudflare → Duy (Q-xx) | TRACKING-PLAN §2.4 nói ngược "đã giải" |
| §Định nghĩa dùng chung "Phiên" · T2 Design câu 2 | Trường thời điểm → Duy (Q-xx); sửa dòng "→ Duy: Không" | PM đã quyết thay Duy |

## Đổi theo QĐ 17–35 (2026-10-24)

PM sửa tại chỗ vì file là nháp chưa duyệt. Nguồn: `PRODUCT-BRIEF.md` §Quyết định của Duy QĐ 17–35, chốt qua `DECISIONS-QUEUE.md` §Câu trả lời của Duy. Frontmatter `status`/`blocked_on` giữ nguyên — ba điều kiện trước S1 của Duy chưa xong. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| Đầu file · TL;DR | Nguồn thẩm quyền = 35 QĐ + quy tắc thẩm quyền QĐ 18; cổng ra mắt QĐ 14 + 29; phạm vi kế toán QĐ 30; câu hỏi còn lại = Q-19, Q-20, 2 điểm chờ Ringkas + N1–N5 | 18 · 29 · 30 |
| §Success Metrics | M1 bỏ "→ Duy (Q-xx)" (B-12); "xong" theo QĐ 24; M3 chỉ card trắc nghiệm; M4 đo từ ra mắt; M5 `method` ∈ {`link`,`code`}. Ràng buộc từ Data: `tel`, thời điểm, không hàng đợi, hợp đồng event, lưu theo ngày + ẩn n < 5, không rule IP | 24 · 25 · 26 · 29 · 31 · 32 |
| §Định nghĩa "xong bài" | Từ TBD → QĐ 24 + AC-75; thẻ lật → Duy (N1) | 24 · 25d |
| §Scope | Dòng 2 (card Hermanson), 3 (chú thích), 4 (trộn ngôn ngữ), 5 (schema, ID mồ côi), 6 (tự khai), 7 (`method`), 8–10 (phần sách = **Có**, ra mắt), 11, 12, 14 (hộp thư + 72 giờ), 16, 17, 18 (dòng AI, 0 chữ trích luật); thêm 19 (`persist()`), 20 (không auto-redirect) | 17–35 |
| §Out of scope | Thêm: `.ics` · file JSON · EPUB (QĐ 18) · máy tính vay quyết lúc mở GĐ05 · trích nguyên văn luật ở phần ra mắt · event tự khai/mời cài/`persist()`/thẻ lật · rule IP ở Cloudflare. Bỏ dòng EPUB "chờ K8" | 18 · 25 · 31 · 33 |
| §Bản đồ bề mặt | B1 tagline T1 · B3, B5 chú thích · B4 card Hermanson · B6, B7 ra mắt · B8 trộn ngôn ngữ + không redirect · B9 tự khai · B10 hộp thư. §Định nghĩa: "Phiên" (trường thời điểm đã quyết), thêm "Trộn ngôn ngữ" | 17–35 |
| §Ràng buộc từ S0 | Sửa R3, R5, R7–R10, R16, R17, R20; thêm R21–R29 | 17–35 |
| §Ràng buộc có quyền CHẶN | Hermanson redact thêm bảng số liệu; nguồn card cả cuốn; R11 đã quyết; 0 chữ trích luật; R22 phạm vi kế toán; R28 whitelist; R32 N/A; R33 (a)(b) theo QĐ 35 | 18 · 26 · 28 · 29 · 30 · 33 · 34 · 35 |
| §Giọng văn | Glossary theo `keep_en` (WRITER §3 phải sửa — việc của Writer); sổ ngân hàng GĐ02 Duy đọc; cảnh báo lưu trữ vào mùa 1; tagline T1 | 18 · 20 · 22 · 30 |
| §Delivery Milestones | M1 gồm phần sách; M3 card Hermanson; cổng S5 gồm `pdf_opened` + AC-79, AC-80; cổng bật tính năng chỉ còn sao lưu | 25 · 27 · 29 |
| §Open Questions | Xoá X1, X2, X3, X5, X6 (đã quyết); giữ X4 → Q-19; thêm **N1–N5**; liệt kê Q-19, Q-20, QĐ 34.2, QĐ 35 | — |
| §Xung đột giữa các phòng | Cột "Duy cần" của K2–K5, K7, K8 → đã quyết; K1 → Q-20 | 17–31 |
| §Câu hỏi cho Duy | Trỏ `DECISIONS-QUEUE.md`; sổ #1–#12 rút còn bảng kết quả | — |
| §Risks · §Chưa xác minh | Thêm: file riêng chặn ra mắt · quy tắc Legal bảng số liệu · luật dấu hiệu lọt/loại quá rộng; nhận ra từ EN; hộp thư lộ danh tính | 28 · 29 · 35 |
| §T3 | Một đoạn ánh xạ Δ → QĐ; bảng Δ giữ làm lịch sử | — |

**→ Duy mới (N1–N5, §Open Questions):** N1 thẻ lật có tính "đã trả lời" (QĐ 24 × 25d) · N2 ngoại lệ AC-05 ngoài `keep_en` · N3 `input type=file` không chạy trong Zalo thì cổng ra mắt ra sao · N4 cảnh báo `persist()` có phải điều kiện ra mắt · N5 hạt của cờ `ai_assisted`.

## Đổi vòng sửa 2 (2026-10-24)

Theo review S1 sau QĐ 17–35 (BLOCKER M2, M3, M8, §4 (a)(b)(c); NONBLOCKING M1, M6, QĐ 29, 34) và PRODUCT-BRIEF **QĐ 36, 37**. PM sửa tại chỗ vì file là nháp chưa duyệt. Đọc kèm Legal vòng sửa 2 (R37, X12, X13; `licences.json` `exclusions` đã có tr.113) và Writer vòng sửa 2 (W1, W2) — hai phòng sửa **song song**, PM đọc bản lúc 15:02–15:04. Frontmatter `status`/`blocked_on` **giữ nguyên**: đổi hay không là **→ Duy (N8)**. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Nguồn |
|---|---|---|
| Đầu file · TL;DR | 37 QĐ; ghi điều kiện 3 lỗi thời (N8); kế toán = agent soát, Duy ký; GĐ01 chờ Phụ lục II chính thức; Legal 37 ràng buộc, cổng S5 thêm R37, cổng ra mắt R1–R4, R6, R13, R31 + §A.2; danh sách câu còn treo thêm N7–N8, Legal X10–X13, Writer W1–W2 | QĐ 36 · 37 · M2 · M6 · M8 |
| §Success Metrics · §Định nghĩa "xong bài" | M3: card có số do agent soát lại. N1: ghi rõ Data (A) và PM (B) khuyến nghị ngược nhau | QĐ 36 · M1 |
| §Scope | Dòng 8 (quy tắc Legal đã ra, B3 → X10) · 13 (GĐ01 chờ Phụ lục II) · 18 (bản EN ⇒ `ai_assisted = true`) · thêm dòng 21 (soát kế toán bằng agent) | QĐ 29 · 34 · 36 · 37 · M2 |
| §Bản đồ bề mặt | B7: quy tắc Legal đã ra, B3 → X10 | M2 |
| §Ràng buộc từ S0 | R3 (`exclusions` + X11) · R5 (§A.2) · R7 (K2, QĐ 37) · R10 (agent soát, Duy ký) · R17 (không LLM thay người ký) · R25 (Legal R của cổng ra mắt) · R28 (bản EN `ai_assisted`) | QĐ 6 · 28 · 29 · 34 · 36 · 37 |
| §Ràng buộc có quyền CHẶN | R1–R37; R22 theo QĐ 36–37; thêm dòng R35 + R36 (AC-84, AC-80) và R37 (AC-85); R11 mở rộng → X11; R34 ghi chú phần "kế toán đồng nghiệp" | QĐ 31 · 32 · 36 · 37 · M6 |
| §Giọng văn · §Delivery Milestones | Glossary: tên TK chỉ có bản chép thứ cấp; M0 = agent chạy thử + đo thời gian Duy ký; M1 chờ X10; M3 GĐ01 BLOCKED chờ Phụ lục II; M5 qua agent; cổng S5 thêm R37 + Legal R cổng ra mắt | QĐ 29 · 36 · 37 |
| §Open Questions · §Câu hỏi cho Duy | N1 hai khuyến nghị; thêm **N7, N8**; liệt kê X10–X13, W1–W2 chưa vào hàng đợi; Q-20 ghi thiếu (a) X12, (b) X13/W2, (c) đã đóng; quy tắc bảng số liệu → `[x]` đã ra | M1 · M2 · M9 · §4 |
| §Xung đột · sổ #1 | K5, #1: Legal đã thêm tr.113; thêm **K11** (chuỗi ghi duyệt: Writer vs Legal vs AC-21, không phân xử) | X3 · M8 · §4 (b) |
| §Risks · §Chưa xác minh | Thay rủi ro "không tìm được kế toán" bằng: agent cùng vendor · thời gian Duy ký · thiếu Phụ lục II; sửa rủi ro bảng số liệu; thêm hộp thư thu dữ liệu định danh (X12); thêm agent chưa chạy, nguồn Phụ lục II | QĐ 36 · 37 · §4 (a) |

**Không làm (ngoài phần được giao, ghi để khỏi tưởng đã làm):** AC cho R33 (a′) kiểm lộ danh tính hộp thư (Legal giao) · M7 cửa vào thổi M1 (→ Data) · LEGAL R17/R22/R28 (file Legal) · DECISIONS-QUEUE (TRIAGE).

**→ Duy mới (§Open Questions):** **N7** phán nào của agent `ke-toan-reviewer` cho phép Duy ký · **N8** đổi điều kiện 3 của `blocked_on` theo QĐ 36. Không có N6 (trùng nhãn ghi chú N6 của PRODUCT-BRIEF).

## Đổi theo QĐ 38–51 (2026-10-25)

PM sửa tại chỗ vì file là nháp chưa duyệt. Nguồn: `PRODUCT-BRIEF.md` QĐ 38–51 (41–51 Duy nhận theo lô mọi khuyến nghị của `DECISIONS-QUEUE.md`). Frontmatter `status`/`blocked_on` **giữ nguyên** — 3 điều kiện trước S1 của Duy chưa xong. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| Đầu file · TL;DR | 51 QĐ; bỏ ghi chú N8 lỗi thời (frontmatter đã theo QĐ 36 — B-16); cổng ra mắt + `persist()`, B3 giữ / B2 che; luật ký; dòng soát công khai; cổng S5 + workflow L13 + L18; M1 số chặt/lỏng; 0 câu nhóm A, còn ĐK-1…3 + 2 điểm Ringkas | 38–51 |
| §Success Metrics · Ràng buộc từ Data · §Định nghĩa "xong bài" | M1 số chặt/lỏng; `lesson_completed{lesson, from_start}`; F2 trên số chặt, F4 mở; M3 thấy mọi bài; "xong" = ≥ 1 card trắc nghiệm, thẻ lật không tính | 38 · 39 |
| §Scope | 2 (QĐ 38, 48) · 3 (`ledger`, QĐ 44) · 4 (ngoại lệ QĐ 43) · 8 (B3 giữ, B2 che) · 9 (N3 → ĐK-1) · 14 (hộp thư A, R25 mới, xoá thư) · 18 (hạt `ai_assisted`, dòng soát) · 19 (`persist()` ra mắt: Có) · 21 (luật ký) | 38 · 40–46 · 48 · 49 |
| §Bản đồ bề mặt · §Định nghĩa | B4 (QĐ 48) · B7 (QĐ 46, ĐK-1) · B8 + "Trộn ngôn ngữ" (QĐ 43) · B10 (R25 mới) | 43 · 46 · 48 · 49 |
| §Ràng buộc từ S0 | Sửa R3 (mẫu ③), R5, R7, R17, R23, R24, R25, R28, R29; thêm **R30** luật ký · **R31** dòng soát · **R32** ngoại lệ "không trộn" · **R33** rủi ro tổng + workflow trước S5 | 38–51 |
| §Ràng buộc có quyền CHẶN | Hermanson redact B2, giữ B3; nguồn card mẫu ③; R11 → AC-18/19; đăng bài + AC-86; R22 luật ký; R37 xoá thư; R26 → QĐ 51 | 40–42 · 46–49 · 51 |
| §Giọng văn | Cảnh báo lưu trữ = điều kiện ra mắt; `ledger`; thêm dòng "Dòng soát + minh bạch AI" và "Dòng chưa có bản EN" | 41 · 43 · 44 · 45 |
| §Delivery Milestones | M0 bỏ N8; M1 + `persist()`, bỏ chờ X10; M3 card Hermanson theo QĐ 48; cổng S5 + AC-83 + workflow L13 + L18 | 45 · 46 · 48 · 49 · 51 |
| §Open Questions | Viết lại: bảng nhãn đã quyết (X4, N1–N8, X10–X13, W1–W2, M4, M7, K1); còn treo = QĐ 34.2, QĐ 35, ĐK-1…3, áp ONE-PAGER v2, workflow L13 + L18 | 38–51 |
| §Xung đột · §Câu hỏi cho Duy · §Risks · §Chưa xác minh · §T3 | K1 → 51, K11 → 41; sổ #4, #7, #8, #9, #12; rủi ro `from_start`, mẫu ③, B3, hộp thư; giới hạn của nhận theo lô; Δ14, Δ21, Δ22, Δ23 đóng | 38–51 |

**Không làm ở lượt 2026-10-25 (đã hoàn tất ở đợt đồng bộ & review 2026-11-07):** frontmatter (`status: fail` giữ nguyên vì 3 điều kiện của Duy chưa xong) · `gates/ONE-PAGER.md` và `ONE-PAGER-V2-PROPOSAL.md` đã áp theo QĐ 50 · các file phòng khác (`TRACKING-PLAN.md`, `SUCCESS-CRITERIA.md`, `LEGAL-REVIEW.md`, `WRITER.md`, `licences.json`) đã đồng bộ hết theo QĐ 38–51 · chữ "→ Duy" trong các mục lịch sử (§T2, §T3 bảng Δ, §Đổi …) giữ nguyên làm bản ghi lúc đó, không phải câu đang mở.

## Đổi theo QĐ 52 (2026-11-07) — Định hướng Giá trị Kiến thức, Dual-Lens, ElevenLabs Video/Podcast & Kiến trúc Mở rộng (`Scalable Topic Engine`)

Theo Quy tắc 14 (thêm mục mới có ngày, giữ nguyên lịch sử bên trên; chỗ nào xung đột thì mục này thắng):

1. **Khung 6 Trụ cột Tài chính & Dòng tiền (`P01`–`P06`) mở rộng tự do (`Scalable Content-as-Data`):**
   - Mỗi bài học là một **Case Giải Phẫu Dòng Tiền Thực Tế** (*"Đằng sau quy định/hiện tượng đó, ai được lợi gì và dòng tiền di chuyển qua những sổ cái nào?"*).
   - **6 Trụ cột hiện tại:** `P01` Ngân hàng, Tiền gửi & Bảng lương (`CASA`, `On-Us` vs `Off-Us`) · `P02` Thẻ tín dụng, VISA/Mastercard, QR & Ví điện tử (`MDR`, `Interchange`, `Scheme Fee`, `Authorization` vs `Settlement`, `Escrow`) · `P03` Tín dụng, Trả góp, Vay mua nhà & Toán học Lãi suất (`EIR`, `Minimum Payment`, `FTP`) · `P04` Dòng tiền Doanh nghiệp, Thuế & Ảo ảnh Lợi nhuận (`Accrual` vs `Cash Flow`, VAT `TK 1331`, Voucher `TK 3387`) · `P05` Bảo hiểm, Bất động sản & Kênh giữ tài sản · `P06` Ngoại tệ, Tỷ giá & Tiền Xuyên biên giới (`DCC`, `SWIFT`, `Nostro/Vostro`).
   - **Phạm vi ra mắt Đợt 1:** Hiển thị đủ Bản đồ 6 Trụ cột trên trang chủ; mở trước các Case thuộc `P01`, `P02`, `P03`; các trụ cột `P04`–`P06` và các Topic mới trong tương lai (`P07`, `P08`...) bật dần qua cờ `published`.
   - **Gỡ bỏ trình đọc PDF sách *Hermanson (1998)*** khỏi cổng ra mắt M1 (ghi đè QĐ 4, 15, 27–29, 46–48 về việc bắt buộc host PDF *Hermanson* ở M1).
2. **Nút gạt 2 góc nhìn tự chọn (`Dual-Lens Switcher`):**
   - **`👤 Góc nhìn Cá nhân` (Mặc định):** Giải mã động cơ lợi ích, phí ẩn, lãi thực (`EIR`) và cách bảo vệ túi tiền; sổ cái chỉ hiện ở mức trực quan (*Ai giữ tiền thật* vs *Ai nợ ai*), không bắt người đọc phổ thông học số hiệu tài khoản kế toán thuế.
   - **`⚙️ Góc nhìn Hệ thống, PM & Kế toán`:** Bật lớp X-Ray kỹ thuật (luồng bản tin thanh toán, đối soát lô, xử lý lỗi/hoàn trả) và bút toán `Debit`/`Credit` chuẩn Thông tư 99/2025/TT-BTC (đã qua `ke-toan-reviewer`).
3. **Explainer Video tương tác & Podcast bằng ElevenLabs (Build-time):**
   - Mỗi Case sinh sẵn lúc build bằng ElevenLabs (`eleven_flash_v2_5` hỗ trợ tiếng Việt + từ điển phát âm PLS cho thuật ngữ chuyên ngành):
     - **🎬 Explainer Video tương tác:** Gọi API `POST /v1/text-to-speech/{voice_id}/with-timestamps` sinh file âm thanh + dữ liệu `timestamps` để sơ đồ dòng tiền (`flow` schema) tự động chạy hiệu ứng và nhảy số khớp từng câu thuyết minh.
     - **🎧 Podcast Mode:** Bản thu âm kể chuyện độc lập phát qua trình nghe Podcast cố định ở đáy trang để người học nghe khi di chuyển mà không cần nhìn màn hình.
   - **Pháp lý âm thanh (Quy tắc 4):** Sinh từ gói ElevenLabs trả phí có Commercial License (không dùng gói Free phi thương mại) và ghi đầy đủ vào `legal/licences.json` để khớp `vibe-check [4]`.
4. **Kiến trúc kỹ thuật mở rộng (`Zero-Code Topic & Case Plug-in` cho S2/S3):**
   - **Tách dữ liệu khỏi code giao diện:** Danh mục chủ đề nằm ở bảng khai báo `pillars` registry; mỗi bài học nằm trong một gói dữ liệu độc lập theo `caseSlug` (`case` data chứa nội dung 2 góc nhìn + quiz; `flow` data khai báo `actors[]` và `steps[]` cho bộ dựng Explainer Video; thư mục `audio` chứa file âm thanh + `timestamps`).
   - **Thêm Topic hoặc Case mới không sửa code:** Khi Duy yêu cầu thêm một Topic mới (`P07`...) hoặc Case mới, chỉ cần thêm mục vào danh mục `pillars` và tạo gói dữ liệu Case mới + chạy script build media ở S3; giao diện trang chủ, bộ lọc, trình phát Explainer Video, kênh Podcast và schema tiến độ (`progress.cases[caseId]`) tự động nhận diện mà không cần sửa code UI hay migrate dữ liệu cũ.

## Đổi theo QĐ 53 (2026-11-07) — Diorama v3.0 bắt buộc · Taxonomy đa danh mục · CMS Preview 1:1 · Pipeline agent `/vibe-post`

Theo Quy tắc 14 (mục mới có ngày, giữ nguyên lịch sử bên trên; chỗ nào xung đột thì mục này thắng). Hợp đồng chi tiết cho agent: `gates/01-spec/AGENT-CMS-PIPELINE.md`.

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | **Mọi bài dùng Mặt cắt Kiến trúc Diorama v3.0**: đúng 5 nhà là archetype có sẵn (cửa cuốn · poché · đạo cụ), lời hứa trên dây, tiền thật dưới ống ngầm, sổ cái kép TT 99/2025 | `scripts/check-story.py` C2–C6 |
| 2 | **Taxonomy 3 cấp** `Category → Topic/Story → Beats + Scene`; mở đầu 7 danh mục · 19 chủ đề; thêm danh mục/chủ đề = thêm dữ liệu, không sửa giao diện | C1 · đếm suy từ dữ liệu |
| 3 | **Định vị ngay dưới masthead**: tổng kho (danh mục · chủ đề · trạng thái), nhãn danh mục cuộn ngang không giới hạn có số bài, breadcrumb *"Đang ở danh mục X (k/N) → Bài k/N: tiêu đề"*, ngăn kéo *bản đồ toàn bộ* có tìm kiếm và lọc *Đang mở đọc / Bản nháp chờ Duy / Sắp lên* | Đã chạy thử headless trên `docs/prototype.html`, 2026-11-07 |
| 4 | **CMS Preview 1:1**: bài agent soạn vào `status: "review"`; Duy xem bằng `?preview=1` đúng như người đọc; thanh duyệt nổi: lọc Chờ duyệt/Đã đăng, cổng kiểm, *Sửa chữ trực tiếp* (không lưu), *Duyệt & Đăng* (không lưu) | Thanh duyệt trong prototype |
| 5 | **Pipeline 6 bước `/vibe-post`**: phân loại & "cái À" → 5 đoạn 2 góc nhìn → Diorama → kiểm (script + ke-toan-reviewer) → giọng đọc → hàng đợi `review`. Agent không bao giờ đặt `published` | Skill vibe-post (đã viết; chưa chạy thử lần nào, xem (d)) + hợp đồng |

**Khoá thật vs advisory:** chỉ `scripts/check-story.py` là khoá thật (thoát mã 1). "Chỉ Duy đăng" và "ẩn bản nháp" là luật trong prompt: nút *Duyệt & Đăng* là JS không lưu, bản nháp vẫn nằm trong mã nguồn trang.

**Chưa chốt — cần Duy:** (a) 7 danh mục của QĐ 53 chia khác 6 trụ cột P01–P06 của QĐ 52, quan hệ giữa hai cách chia chưa quyết. (b) Bài 3 "Trả góp 0%": ke-toan-reviewer trả **FAIL 0 · FLAG 6 · UNVERIFIED 3** (2026-11-07; agent không được chạy code). Sau đó tác giả sửa câu chữ theo 4 FLAG (#10–#13) và tự tính lại K1 bằng code (khớp: 0,80%/tháng, ~10%/năm) — **chưa chạy lại reviewer**. Hai FLAG còn lại là việc của người ký: ghi 1388 hay 131 cho phải thu từ công ty tài chính; ghi 641 hay giảm doanh thu cho hỗ trợ lãi suất. (c) Hai bài đang "đã đăng" trong prototype mang `approvedBy: "demo-prototype"` — chưa phải Duy duyệt thật, **và chưa chạy ke-toan-reviewer trên bản này** (trái ONE-PAGER §3.3 nếu coi là đã đăng thật). (d) Lệnh `/vibe-post` chưa dùng được trong Claude Code (skill nằm ở `.agents/skills`, Claude Code đọc `.claude/skills`).

## Đổi theo QĐ 54 (2026-11-08) — 7 danh mục khởi đầu · Luật C9: Bài sâu 2 tầng + Kịch bản Video

Theo Quy tắc 14 (mục mới có ngày, giữ nguyên lịch sử bên trên; chỗ nào xung đột thì mục này thắng). Nguồn: `gates/00-discovery/PRODUCT-BRIEF.md` QĐ 54.

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | **7 danh mục khởi đầu** (QĐ 52/53 mở rộng) là taxonomy hiển thị; 6 trụ cột P01–P06 không còn là cách chia trên giao diện. Mục (a) ở trên **đề xuất đóng — chờ Duy xác nhận chữ** (đề xuất gốc không nằm trong repo) | C1 · đếm suy từ dữ liệu |
| 2 | **Mỗi bài đủ 3 trụ (Luật C9):** A · bài giải thích cho người không chuyên (`article.lay`) · B · phân tích chuyên sâu hệ thống & kế toán TT 99/2025 (`article.pro`, chuỗi bút toán chỉ ghi sổ doanh nghiệp; phía ngân hàng viết bằng lời, không bịa số hiệu) · C · kịch bản ≥ 7 cảnh `time`/`visual`/`vo`/`onScreen`, lời bình ≥ 220 từ, dùng thẳng cho ElevenLabs | `scripts/check-story.py` C9 (hình dạng + độ dài — **không** đo chất lượng) |
| 3 | Trên `docs/prototype.html`: mục *"Bài viết đầy đủ & Kịch bản dựng Video"* với 3 tab A/B/C, nút *Sao chép toàn bộ kịch bản Video* và *Xuất JSON Voiceover*; thanh duyệt có cổng *C9 (Bài sâu 2 tầng + Kịch bản Video)*, là cổng nội dung thứ 5 | Chưa chạy thử trong trình duyệt ở phiên 2026-11-08 |
| 4 | `card`, `pay` về `status: "review"` (WMS-R4) — trước đó chỉ là demo. Người đọc thường không thấy bài nào cho tới khi Duy duyệt | C7 sẽ WARN "không còn bài nào published" — đúng sự thật |

**Chưa chốt — cần Duy:** (e) chữ chính xác của QĐ 54(1). (f) Phần B do agent soạn và agent cùng vendor soát; chưa người làm nghề nào đọc. (g) Giọng đọc ElevenLabs chưa sinh — chưa có giấy phép trong `legal/licences.json`.

## Đổi theo C9 v2 — Hướng 3A (2026-11-08)

Theo Quy tắc 14 (mục mới có ngày; chỗ nào xung đột với mục QĐ 54 bên trên thì mục này thắng). Duy, 2026-11-08, chọn *"Hướng 3A (Nâng cấp toàn diện chuẩn C9 — Bài khảo cứu sâu 2 tầng + Studio Kịch bản Video 2 định dạng: YouTube Dài 8–10 phút & Shorts/Reels/TikTok 60–90 giây)"*. Ngưỡng đầy đủ: `AGENT-CMS-PIPELINE.md` §1.

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | Thay dòng 2 của mục QĐ 54: **A** là bài khảo cứu ≥ 850 từ chia ≥ 4 chương, có sơ đồ dòng chảy 3 kênh (dây = lời nhắn · ống ngầm = tiền thật · sổ cái = ghi nội bộ), hộp *khi cơ chế có lợi / khi thành bẫy* (ngôi thứ ba, không khuyên), ≥ 4 câu hỏi tự soi. **B** ≥ 4 cơ chế ≥ 450 từ (bù trừ ròng, cấu trúc phí, FTP, dự trữ bắt buộc, DCF/IRR/EIR có ví dụ tính) · ≥ 4 ghi chú kế toán ≥ 180 từ · ≥ 3 bút toán · ≥ 3 ngoại lệ × 50 từ. **C** hai định dạng: YouTube dài ≥ 10 cảnh, lời bình ≥ 1.350 từ, kết 7:30–11:00; Shorts/Reels/TikTok ≥ 5 cảnh, lời bình 150–260 từ, kết 0:55–1:35 | `scripts/check-story.py` C9 v2 (hình dạng + độ dài + grep điều luật/URL/tên ngân hàng/câu khuyên — **không** đo chất lượng) |
| 2 | Thay dòng 3 của mục QĐ 54: tab A và B có mục lục nhanh; tab C có bộ chọn *YouTube Dài* / *Shorts · Reels · TikTok*, hiện số cảnh · số từ lời bình · thời lượng ước tính; nút *Sao chép kịch bản đang xem* và *Xuất JSON Voiceover* (gồm cả dài lẫn ngắn); cổng thanh duyệt *C9 v2* | Mở `docs/prototype.html?preview=1` |
| 3 | **Thay dòng 4 của mục QĐ 54:** `card`, `pay` **giữ** `published` / `approvedBy: "demo-prototype"` theo lời Duy (nguyên văn ở `AGENT-CMS-PIPELINE.md` §6, 2026-11-08) — ngoại lệ WMS-R4 cho hai bài mẫu, **không** phải Duy duyệt nội dung; `install` giữ `review` | C7 WARN demo · thanh duyệt ✗ *"chưa phải Duy duyệt thật"* |
| 4 | `review.ketoan` = dòng tổng **nguyên văn** của ke-toan-reviewer chạy trên nội dung đã tích hợp; ngày ở `review.ketoanAt` | Đọc dữ liệu bài |

**Chưa chốt — cần Duy:** (h) đọc và duyệt nội dung C9 v2 của cả 3 bài — hiện là chữ agent, đã hiện cho người đọc thường ở `card`/`pay`. (i) Nhịp 190 từ/phút chưa đo trên giọng ElevenLabs thật; video ngắn đọc nhanh có thể lệch ước lượng.

## Đổi theo QĐ 55 & QĐ 56 (2026-11-08) — Điều hướng Layout `1A` · Bỏ chữ `"sổ cái"` · Pipeline Build Audio/Video qua ElevenLabs & Upload YouTube

Theo Quy tắc 14 (mục mới có ngày; chỗ nào xung đột với các mục bên trên thì mục này thắng). Nguồn: `gates/00-discovery/PRODUCT-BRIEF.md` QĐ 55, QĐ 56 và `gates/01-spec/UX-CATEGORY-NAVIGATION-RESEARCH.md`.

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | **Layout `1A` (`Editorial Split-Pill` `48px` + Overlay Mục lục 2 cột `Master–Detail` + `⌘K` + Thẻ chuyển bài cuối bài):** Thay dải pill danh mục cuộn ngang 2–3 tầng (`162px`) bằng thanh điều hướng 1 hàng `48px` (Trái: tên thương hiệu `Where Money Sleeps`, không đặt icon hamburger cạnh logo; Giữa: `Split-Pill` `[Danh mục k/N ▾ │ Bài m/M: Tiêu đề ▾]` + nút `‹ ›` + Popover đổi nhanh bài cùng danh mục; Phải: `⌕ Mục lục & Tìm ⌘K` + `Chế độ duyệt bài`). Overlay Mục lục 2 cột nổi phủ không đẩy sân khấu Diorama xuống (**`0px` Layout Shift**) | Đã triển khai trong `docs/prototype.html` |
| 2 | **Thay toàn bộ wording `"sổ cái"` (QĐ 55):** Dùng **"Mục lục"** cho điều hướng, **"Sổ kế toán"** cho góc nhìn kế toán (`data-lens="ledger"`), và **"Từ tin báo “ghi có” tới sổ sách ngân hàng: tiền của bạn đi qua những đâu."** cho tagline tiếng Việt (sửa QĐ 22, QĐ 44, QĐ 53) | Quét Unicode NFC trên `docs/prototype.html` = `0` lần xuất hiện `"sổ cái"` |
| 3 | **Pipeline khép kín Build Audio + Video qua ElevenLabs → Upload YouTube (`unlisted`) → Nhúng Video YouTube vào bài viết (`QĐ 56` — Bước 5A–5D của `/vibe-post`, thực thi qua `scripts/wms-media-pipeline.py`):** (5A) **ElevenLabs API:** gọi `with-timestamps` (`eleven_v3:JwqRvOqFdGeQNu7UjKjw` Giọng Tâm + từ điển phát âm `.pls`) và `sound-generation` (cho SFX trong `onScreen`), lưu qua bộ nhớ đệm SHA-256 theo skill `content-hash-cache-pattern` của ECC; (5B) **Kết xuất Video `.mp4`:** đồng bộ Mặt cắt Diorama v3.0 với `alignment` timestamps của ElevenLabs (`30fps Locked-Stage v4.0` + `ffmpeg loudnorm=-14 LUFS`), xuất bản Dài `16:9` (`1920×1080`) và bản Shorts `9:16` (`1080×1920`); (5C) **Upload YouTube (`YouTube Data API v3` — `videos.insert`):** tự động sinh Chapters từ timestamps thật, đặt mặc định `privacyStatus: "unlisted"` (hoặc `"private"` — dùng `"unlisted"` để nhúng xem thử được trong `?preview=1` mà không lộ công khai trên kênh), `selfDeclaredMadeForKids: false`, `containsSyntheticMedia: true`; (5D) **Nhúng ngược vào bài viết:** tự động ghi `youtubeId` (11 ký tự) và `embedStatus: "uploaded_unlisted"` vào `STORIES[<khoá>].videoScript.{long,short}` trong `docs/prototype.html` để khung trình phát `.yt-embed` (`youtube-nocookie.com`, hỗ trợ chuyển đổi `16:9` ⇄ `9:16`, nhảy chương và fallback MP4 cục bộ khi chờ YouTube duyệt hạn mức API) hiển thị ngay đầu bài viết (`#pnl-lay` và `#pnl-vid`). Mọi lệnh upload YouTube và việc đặt `embedStatus: "uploaded_public"` đều qua cổng hỏi Duy (`force_ask` ở `scripts/wms-hook-guard.sh` + `SHIP_ASK` 16 mục của `scripts/check-story.py` C8 & C9) | `scripts/check-story.py` C8 + C9 · `scripts/wms-media-pipeline.py` · `legal/licences.json` (`elevenlabs-commercial-tts-sfx`) |

## Đổi theo QĐ 57 & QĐ 58 (2026-11-08) — Minh hoạ Mặt cắt Khảo cứu (`LUẬT 9`) · Trung tâm Điều phối Agent Realtime (`docs/workflows.html`) · Bộ 4 Chuyên gia (`K1–K4`, `F1–F4`, `B1–B4`, `M1–M4`)

Theo Quy tắc 14 (mục mới có ngày; chỗ nào xung đột với các mục bên trên thì mục này thắng).

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | **LUẬT 9 — Nhịp Minh hoạ Mặt cắt Giải thích Đan xen (`QĐ 57`):** Trong bài khảo cứu (`#pk-lay-essay`), giữ Chương 01 (mở bài có drop-cap) thuần chữ và đan xen đúng **4 hình mặt cắt giải thích `16:9` (`1200×675`, `CHAP_FIGS[<story>]`)** vào Chương 02–05 ngay sau đoạn 1 (*Mechanism Pivot / Advance Organizer*, ~1 hình mỗi 220–320 từ / `0.8–1.0 vh`), kèm `<figcaption>` 3 tầng (`kicker + nút nhảy lên nhịp Diorama`, `Action Thesis Title`, `2 câu giải thích cơ chế có [[glossary|term]]`), `width="1200" height="675"`, `loading="lazy"`, `decoding="async"`, `aspect-ratio: 16/9` (`CLS = 0`) | `scripts/wms-render-editorial-figs.py` · `scripts/check-story.py` (`C9 · CHAP_FIGS`) |
| 2 | **Bộ 4 Chuyên gia Kiểm duyệt & 4 Cổng `wms-check.sh` (`QĐ 58`):** Nâng cấp từ 3 lên **4 chuyên gia độc lập** chạy trên mọi bài, giao diện và video: (1) `ke-toan-reviewer` (`K1–K4` số học & TT 99/2025); (2) `tai-chinh-reviewer` (`F1–F4` cơ chế ngân hàng, toán `IRR/EIR`, độ tươi `knowledge/finance-kb.json` qua `scripts/wms-finance-kb.py`); (3) `brand-safety-reviewer` (`B1–B4` chặn 100% tên riêng thương mại/ngân hàng/công cụ AI hậu trường); (4) `bang-motion` (`M1–M4`, chắt lọc từ `bangtutorial/bang-motion` `MIT License` ghi trong `legal/licences.json`: `M1` Persistent World + `cubic-bezier(0.22, 1, 0.36, 1)` + hạt dẫn hướng SVG, `M2` Kinetic Financial Counter `tabular-nums`, `M3` Khoá khung nhìn `LUẬT 6b + LUẬT 8`, `M4` `window.__vibeSeek` + 0 CDN runtime ngoài + `prefers-reduced-motion`, kiểm qua `scripts/wms-motion-snap.py`) | `scripts/wms-check.sh` (`[1/4]` `check-story.py` 26/26 file · `[2/4]` `wms-finance-kb.py` · `[3/4]` `wms-motion-snap.py` · `[4/4]` `vibe-check.sh`) |
| 3 | **Trung tâm Điều phối Agent Realtime (`docs/workflows.html`):** Mô phỏng trực quan toàn bộ 5 quy trình trong repo (`/vibe-post` 6 bước, Xưởng 7 cổng `S0→S6`, Research 4 pha `SWEEP→DEDUPE→REFUTE→JUDGE`, Định tuyến Model `T0..T4` có thanh trượt 4 trục, và Kiểm toán Pháp quy), công khai minh bạch 100% nhà cung cấp/model (`Claude Fable 5 / Opus 5.5 / Sonnet 5.5 / Haiku 4.5`, `Gemini 4 Argon / 3.8 Flash`, `ElevenLabs eleven_v3 Giọng Tâm + SFX`, `Google Veo 3.1 / Imagen + Pillow/FFmpeg 30fps`, `YouTube Data API v3`, `Python T0 + Hook Guard`) trên từng nút | `docs/workflows.html` (`data-tier="reference"`) |

## Đổi theo QĐ 62 (2026-11-15) — Chuẩn Song Ngữ Toàn Diện Tiếng Việt ⇄ Tiếng Anh (`LUẬT 11`)

Theo Quy tắc 14 (mục mới có ngày; chỗ nào xung đột với mục cũ ưu tiên song ngữ từ đầu, mục này thắng). Mở rộng `QĐ 6`, `AC-05..10`, `AC-52`, `AC-62`, `AC-82` áp dụng cho **toàn bộ nội dung của `where-money-sleeps`**:

| # | Yêu cầu | Kiểm bằng |
|---|---|---|
| 1 | **100% nội dung độc giả & kiểm duyệt song ngữ `VI ⇄ EN`:** Toàn bộ `docs/prototype.html` (`7 STORIES` published, `52 GLOSS`, `7 CATEGORIES`, `28 CHAP_FIGS`, `14 WMS_QUIZ_BANK`, 7 máy tính, `Scene` SVG), `docs/studio.html`, `docs/workflows.html` và mọi trang review `docs/*.html` đều hỗ trợ công tắc `VI ⇄ EN` tại chỗ giữ nguyên bài/nhịp/tiến độ | `scripts/check-story.py` · `scripts/wms-qa-verify.py` · `scripts/wms-motion-snap.py` |
| 2 | **Chuẩn xác thuật ngữ TT 99/2025 ↔ IFRS/GAAP & BIS CPMI (`LUẬT 11`):** Giữ nguyên số hiệu TK Việt Nam (`112..642`), kèm tên tiếng Anh chuẩn và dòng `"unofficial summary of Circular 99/2025/TT-BTC"` (`AC-52`); giữ 0 tên riêng (`LUẬT 4`), 0 từ lóng đạo cụ tiếng Anh (`LUẬT 7`), 0 chữ `"accountant"/"expert"` (`QĐ 41`), chung khoá `WMS_PROGRESS_KEY` & `tel` (`AC-09`, `AC-62`) | `scripts/check-story.py` + `scripts/wms-qa-verify.py` |


