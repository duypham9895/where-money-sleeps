---
status: pass
stage: 01-spec
date: 2026-11-15
owner: pm
blocked_on: []
---

# ACCEPTANCE — Where Money Sleeps

> **`status: fail` vì `blocked_on` chưa rỗng**, không phải vì tiêu chí sai. QĐ 14: người kế toán có tên
> + bấm giờ 1 bài là điều kiện **trước khi S1 chốt file này**. **QĐ 36 thay điều kiện đó:** agent
> `ke-toan-reviewer` chạy thử trên 1 bài mẫu + card, đo thời gian Duy đọc báo cáo và ký. Dòng 3 của
> `blocked_on` đã theo chữ QĐ 36 (PM đồng bộ sau review vòng sửa 2; `DECISIONS-QUEUE.md` B-16).
> S4 (QA) đọc file này theo đường dẫn. **Số AC là hợp đồng**: thêm thì tự do; bỏ hoặc đổi nghĩa thì
> thêm một dòng có ngày ở §Thay đổi, không sửa tại chỗ.

**TL;DR** · ~13.800 từ (đếm theo khoảng trắng, sau QĐ 38–51, 2026-10-25) · đọc ~77 phút (tầng HỢP ĐỒNG, không phải trang review)
- **86 tiêu chí PASS/FAIL**: 56 chỉ MÁY · 19 MÁY+NGƯỜI · 11 chỉ NGƯỜI. AC-43…AC-73 thêm khi PM gộp S1; AC-74…AC-78 từ T2; AC-79…AC-83 từ QĐ 17–35 (§M); AC-84, AC-85 từ Legal R35, R37 (§N); **AC-86 từ QĐ 41** (§O, dòng soát công khai).
- **Phủ — có AC, chưa phải PASS được:** mọi ràng buộc `LEGAL-REVIEW.md` R1–R37 và mọi event `TRACKING-PLAN.md` có AC hoặc lý do ghi rõ. Còn hở: R5 danh sách lint tên riêng (S3) · **R33 (a) công khai hộp thư BLOCKED — chờ hợp đồng Ringkas** (QĐ 35) · R26 không có AC (rủi ro xác nhận lại ở QĐ 51; workflow L13 + L18 trước S5 là cổng ở PRD) · R32 N/A (QĐ 18) · R34 không phải AC sản phẩm. Event về đích phải được **nhìn bằng mắt ở S4** (AC-70).
- **5 BLOCKED hẳn** (AC-03, 04, 31, 32, 42) **+ 13 BLOCKED một phần** (AC-12, 26, 28, 53, 58, 61, 65, 66, 70, 74, 79, 85, 86) — chờ Duy đọc báo cáo agent kế toán bài mẫu và bấm giờ ký (QĐ 36), chờ Phụ lục II chính thức (QĐ 37), chờ đo điện thoại, chờ hợp đồng Ringkas. **0 TBD hẳn + 4 TBD một phần** (AC-45, 59, 72, 76 — phần của S2, S3). **0 xung đột.** **0 AC chờ quyết định mới của Duy**; còn 3 AC có nhánh **câu có điều kiện** (AC-26, AC-79 → ĐK-1; AC-84 → ĐK-2). Đếm bằng script trên cột Ai và Trạng thái, 2026-11-07.
- **Cổng ra mắt = AC-42 + AC-79 + AC-83** (lối vào + phần sách + cảnh báo `persist()`, QĐ 14 + 29 + 45). Máy kiểm **cái hỏng**, người kiểm **cái sai**: máy không bắt được thuật ngữ VN ngoài danh sách gốc, card hiểu sai một câu trích đúng, hay đoạn bên thứ ba không khớp mẫu ③. Agent kế toán (QĐ 36) soát nhưng **không ký**; FAIL K1/K2/K3 của nó chặn đăng (QĐ 40); người ký là Duy.

Cột **Ai**: `MÁY` = phép kiểm tất định, chạy lại được, không cần phán đoán · `NGƯỜI` = cần mắt/phán đoán, ghi tên người và ngày khi PASS · `MÁY+NGƯỜI` = máy kiểm phần hình thức, người kiểm phần nội dung.
**Agent `ke-toan-reviewer` (QĐ 36) không phải `MÁY`** (không tất định, trừ K1 chạy code) **và không phải `NGƯỜI`** (không ký). Chỗ có agent ghi *"soát: agent `ke-toan-reviewer` · ký: Duy"*; cột Ai tính theo người ký.

## A. Duyệt và đăng

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-01 | Không bài, card, bản EN nào truy cập được khi cờ `published` của nó khác `true` | Dựng site từ bộ nội dung có ≥1 bài, ≥1 card, ≥1 bản EN `published=false`; ba mục đó không có trong output, sitemap, liên kết nội bộ, và URL trực tiếp trả không tìm thấy | MÁY | QĐ 8 · 14 · ONE-PAGER §3 | Sẵn |
| AC-02 | Mọi mục `published=true` có ghi nhận duyệt của Duy (ngày), tách riêng VN và EN | Máy: trường duyệt tồn tại và có ngày. Người: Duy là người ký — máy **không** chứng minh được Duy đã đọc | MÁY+NGƯỜI | QĐ 8 | Sẵn |
| AC-03 | Mọi bài GĐ01, GĐ05, **mọi card có con số**, và **mục (`sectionId`) chứa `source_quote` của card có số đó**, chỉ `published=true` khi có **báo cáo soát của agent `ke-toan-reviewer`** cho đúng phiên bản nội dung đó **và chữ ký của Duy** (QĐ 36). Con số trong bài không card nào hỏi (kể cả sổ ngân hàng GĐ02): Duy đọc, không bắt buộc agent | Máy: card có chữ số ⇒ bắt buộc bản ghi soát (soát: agent · ký: Duy) trên card **và** trên `sectionId` nguồn của nó; bản ghi trỏ tới báo cáo agent theo khuôn của agent. Người: Duy đọc báo cáo và ký. **Luật ký (QĐ 40):** báo cáo có FAIL ở K1, K2 hoặc K3 ⇒ mục **không** được `published=true` dù có chữ ký, cho tới khi sửa + agent soát lại ra báo cáo mới; UNVERIFIED · FLAG · "KHỚP NGUỒN THỨ CẤP" (ngoài GĐ01) ⇒ ký được, bản ghi phải có **một dòng lý do** (máy: thiếu dòng lý do ⇒ FAIL) | MÁY+NGƯỜI | QĐ 8 · 30 · 36 · 40 | **BLOCKED — chờ agent chạy thử trên 1 bài mẫu + card (điều kiện 3, QĐ 36)** · GĐ01: thêm AC-04 · luật ký: Sẵn (QĐ 40) |
| AC-04 | Tên tài khoản kế toán trong GĐ01 theo TT 99/2025: agent chạy **K2** (đối chiếu nguyên văn) ra **PASS trên Phụ lục II chính thức**. "KHỚP NGUỒN THỨ CẤP" (bản chép `legal/tt99-phu-luc-ii.secondary.json`) **không bao giờ là PASS** ⇒ bài GĐ01 có tên TK chính thức không vào build (QĐ 37). Lối vào không bị chặn bởi AC này. Ngoài GĐ01: "KHỚP NGUỒN THỨ CẤP" ký được kèm lý do (QĐ 40, AC-03); FAIL K2 ở đâu cũng chặn | Agent K2 trên từng bài GĐ01 (số hiệu + tên + URL nguồn + ngày đọc); Duy đọc báo cáo và ký | NGƯỜI | QĐ 8 · 36 · 37 · 40 · LEGAL-SCREEN | **BLOCKED — chờ Phụ lục II TT 99 chính thức (QĐ 37)** |

## B. Ngôn ngữ và nút gạt

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-05 | Không trang nào trộn ngôn ngữ (QĐ 20): câu văn + chữ giao diện của trang VI bằng VI, trang EN bằng EN. Chữ EN trên trang VI **chỉ hợp lệ** khi là mục glossary có `keep_en = true`, **hoặc** thuộc một ngoại lệ có tên (QĐ 43): **(a)** khớp một mục trong **danh sách tên riêng** (ngắn, không chú thích, tách khỏi glossary — tên sản phẩm, tên sách/tác giả, tên giấy phép) · **(b)** nằm trong dòng "chưa có bản EN" (song ngữ, AC-06). **(c) Chiều ngược:** chữ VN trên trang EN chỉ hợp lệ khi là mục glossary được đánh dấu cho chiều này (vd chữ tin báo ngân hàng, tên TK TT 99); chữ VN trong `vi.term` của thẻ chú thích được miễn | Máy: trích chữ hiển thị (sau NFC) của trang VI và trang EN; trang VI: mỗi từ không phải VI phải khớp `keep_en` (kể cả `aliases`) hoặc danh sách tên riêng hoặc nằm trong dòng (b); trang EN: mỗi từ VN phải khớp mục glossary được đánh dấu hoặc nằm trong `vi.term`; không khớp ⇒ FAIL. Người: đọc mẫu; Duy duyệt danh sách tên riêng (giữ ngắn) | MÁY+NGƯỜI | QĐ 6 · 20 · 43 | Quy tắc + ngoại lệ: Sẵn (QĐ 43) · danh sách tên riêng + cờ đánh dấu chiều EN: **S3 dựng**, Duy duyệt · cách máy nhận ra từ EN/VN: S3 |
| AC-06 | Bài chưa có EN đã duyệt: nút gạt mờ + một dòng báo "chưa có bản tiếng Anh" **viết cả VI lẫn EN** (QĐ 43 b); **không bao giờ** hiện bản EN chưa duyệt hay ghép VN vào trang EN | Với một bài chỉ có VN: nút ở trạng thái mờ, có dòng báo chứa cả chuỗi VI và chuỗi EN, không URL `/en/` nào của bài trả nội dung | MÁY | QĐ 6 · 43 | Sẵn · dòng báo **song ngữ** (QĐ 43 b) — câu chữ: Writer, S2 chỉnh được |
| AC-07 | Nút gạt giữ `sectionId`: đứng ở section X bên VI, gạt sang EN ⇒ cùng bài, tới section X; chiều ngược lại cũng vậy | Chạy tự động trên **mọi** section của mọi bài có cả hai bản | MÁY | QĐ 6 | Sẵn |
| AC-08 | Bài có cả hai bản thì tập `sectionId` VI = tập `sectionId` EN | So hai tập | MÁY | QĐ 6 | Sẵn |
| AC-09 | Tiến độ và trạng thái card dùng chung hai ngôn ngữ: đọc xong ở VI ⇒ EN hiện đã đọc | Chạy tự động | MÁY | QĐ 6 · 7 | Sẵn |
| AC-10 | Mỗi trang có URL `/vi/` và `/en/` (khi có bản EN) với hreflang hai chiều; lựa chọn ngôn ngữ được nhớ trên máy; **không auto-redirect** theo ngôn ngữ trình duyệt (QĐ 18) — chi tiết AC-82 | Kiểm thẻ hreflang mọi trang; đổi ngôn ngữ, đóng mở lại ⇒ giữ lựa chọn | MÁY | QĐ 6 · 18 | Sẵn |

## C. Glossary

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-11 | Đánh dấu thuật ngữ (QĐ 19, 21): trong **mỗi mục H2**, lần đầu một thuật ngữ glossary xuất hiện thì có gạch chấm + chạm được, nối tới mục glossary; các lần sau trong cùng H2 không đánh dấu. **Thuật ngữ `keep_en`** thiếu dấu ở lần đầu mỗi H2 ⇒ **FAIL**. **Thuật ngữ VN** trong **danh sách gốc** (tên TK TT 99/2025 + mục glossary) mà chưa đánh dấu ⇒ **cảnh báo** trong báo cáo build, không FAIL | Quét bài theo glossary + danh sách gốc, so sau chuẩn hoá NFC (lessons §Tiếng Việt). Cảnh báo là đầu vào của AC-12. **Giới hạn: máy không phát hiện thuật ngữ VN ngoài danh sách gốc** | MÁY | QĐ 5 · 19 · 21 | Cơ chế: Sẵn · danh sách gốc: **S3 dựng** |
| AC-12 | Không bài nào có thuật ngữ chuyên ngành **chưa** có mục glossary; mọi cảnh báo của AC-11 đã được xử lý (đánh dấu, hoặc ghi "từ thường") | Duy đọc từng bài (GĐ01/GĐ05: agent `ke-toan-reviewer` soát thêm theo K3/K4, Duy ký — QĐ 36) cùng danh sách cảnh báo của AC-11, đánh dấu thuật ngữ thiếu; còn thiếu ⇒ bài chưa `published` | NGƯỜI | QĐ 5 · 21 · 36 | Sẵn (GĐ01/05: BLOCKED cùng AC-03 — chờ agent chạy thử) |
| AC-13 | Mỗi mục glossary có trường `keep_en` (true/false). Mục `ledger` có `keep_en = false` ⇒ bài VN viết "sổ cái", `ledger` chỉ ở `en.term` trong thẻ (QĐ 44). Mục glossary nào được trang EN dùng thì có đủ VI + EN; không có chú thích nào trỏ vào mục không tồn tại | Kiểm trường `keep_en` trên mọi mục, riêng mục `ledger` = false; đối chiếu liên kết chú thích ↔ mục glossary | MÁY | QĐ 5 · 6 · 20 · 44 | Sẵn |

## D. Card

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-14 | Mọi card có `source_quote` + vị trí nguồn (bài + `sectionId`, hoặc Hermanson + số trang). Card Hermanson: `source_quote` tiếng Anh nằm trong dữ liệu build, **không có trong HTML hiển thị** | Kiểm trường bắt buộc trên toàn bộ card; với card Hermanson, grep `source_quote` trong build output hiển thị ⇒ phải không thấy | MÁY | ADDENDUM §Đường ống bước 5 · QĐ 27 | Sẵn |
| AC-15 | `source_quote` khớp nguyên chuỗi trong nguồn (so sau chuẩn hoá NFC). Không khớp ⇒ **loại, không sửa**. Card Hermanson: `source_quote` EN khớp văn bản Hermanson; card hiện bằng VN và **nói đúng câu trích đó** | Máy: tìm chuỗi trong nguồn. Người: Duy đối chiếu bản VN của card Hermanson với câu trích EN | MÁY+NGƯỜI | ADDENDUM bước 5 · QĐ 27 | Sẵn |
| AC-16 | Mọi con số và ký hiệu `%`, `đ`, `$` trong đáp án có mặt trong `source_quote`. Trượt ⇒ loại. **Card Hermanson không có con số**: câu hỏi hoặc phương án chứa chữ số, `%`, `$`, `đ` ⇒ FAIL. **Giới hạn: không bắt được card hiểu sai một câu trích đúng** ⇒ AC-02, AC-03, AC-15 | Trích số/ký hiệu từ đáp án, tìm trong `source_quote`; quét card nguồn Hermanson tìm chữ số/ký hiệu | MÁY | ADDENDUM bước 5 · QĐ 27 | Sẵn |
| AC-17 | Card chỉ sinh từ bài Duy tự viết hoặc Hermanson | Trường nguồn ∈ danh sách cho phép | MÁY | QĐ 3 | Sẵn |
| AC-18 | Card từ Hermanson **được lấy từ cả cuốn** (QĐ 28), trừ: (i) **danh sách trang** trong `legal/licences.json` → `card_generator.excluded_pages` (gồm tr.113, 166, 501, 803 · bảng B2 tr.117 · bảng B3 tr.45, 55, 94–95, 170, 185 **loại hẳn** khỏi máy sinh card dù giữ trong file host — QĐ 46) — cùng đoạn khớp chuỗi denylist của Legal R10 (FASB, New Accountant, DuBois, Wall Street Journal, annual report); (ii) **mọi trang khớp mẫu ③** trong `legal/licences.json` → `card_generator.page_rule` (LEGAL-REVIEW §A.2, QĐ 47, thay mẫu đúng chữ QĐ 28): không phân biệt hoa thường — `annual report` · `Accounting Trends` · `Source` theo sau bởi `:` hoặc `'` · `©` · `copyright` · `wall street journal` · `financial accounting standards board` · `new accountant` · `dubois` · `reprinted` · `adapted from` | Máy: trang của `source_quote` không thuộc `card_generator.excluded_pages`, `source_quote` không khớp denylist R10, và trang không khớp `card_generator.page_rule` (`pdftotext` từng trang của PDF gốc). **Tự kiểm:** mẫu (ii) phải bắt đủ 7/7 trang đã biết (94, 113, 117, 166, 185, 501, 803) — thiếu ⇒ FAIL. Danh sách (i) và regex (ii) đọc trực tiếp từ `licences.json` lúc build, không chép vào code. Đoạn lọt qua cả hai lớp: **rủi ro Duy nhận** (QĐ 28), không có phép kiểm | MÁY | QĐ 3 · 28 · 46 · 47 · `licences.json` · Legal R10 · R11 · §A.2 | Sẵn (QĐ 46, 47 — đã có trong `licences.json` → `card_generator`) |
| AC-19 | Card là chạm, không gõ; sau khi trả lời có phản hồi ngay + một dòng giải thích + link "đọc lại đoạn này" tới `sectionId` **tồn tại**; không phương án nhiễu nào là con số tài chính nếu card không có phản hồi. **Card Hermanson:** link trỏ `sectionId` của **bất kỳ bài `published=true` nào** (không chỉ GĐ01) có `based_on` phủ trang của `source_quote`; không có `sectionId` nào như vậy ⇒ card đó `published=true` làm build FAIL (QĐ 27, 28, 48) | Máy: kiểu card, link sống, đối chiếu `based_on.pages` ↔ trang của card. Người: giải thích đúng | MÁY+NGƯỜI | ADDENDUM bước 8 · QĐ 27 · 28 · 48 | Sẵn |
| AC-20 | Ôn theo phiên: card ở cuối bài + tối đa 1–2 card ôn ở đầu phiên sau; không có lịch theo ngày. "Phiên" tính từ trường thời điểm hoạt động cuối trong JSON tiến độ (QĐ 26) | Chạy tự động hai phiên liên tiếp | MÁY | ADDENDUM bước 9 · QĐ 26 | Sẵn |
| AC-21 | Không dùng LLM chấm card của LLM **thay người ký**: mọi card `published` có người ký ghi tên (AC-02). Bản ghi duyệt có **hai trường** (QĐ 41): `reviewed_by` = **chỉ người ký** (Duy); agent soát ghi ở **trường riêng**, đúng tên `ke-toan-reviewer` (QĐ 36). Chữ công khai: AC-86 | Máy: `reviewed_by` không bao giờ là một model hay agent; mục có agent soát thì trường riêng ghi đúng `ke-toan-reviewer`; thiếu `reviewed_by` ⇒ FAIL | MÁY | ADDENDUM bước 6 · QĐ 36 · 41 | Sẵn · tên trường riêng: S3 |

## E. Trình đọc PDF

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-22 | PDF Hermanson được host chỉ gồm **tr.1–197** của PDF gốc | Đếm trang = 197; đối chiếu trang đầu/cuối với PDF gốc | MÁY | QĐ 15 | Sẵn |
| AC-23 | Tr.113, tr.166 (B1) **và bảng B2 tr.117** (quy tắc Legal §A.2; QĐ 46; đọc từ `legal/licences.json` → `host_redactions.redact`) đã redact: nội dung bị loại **bị xoá khỏi lớp chữ**, không chỉ bị che bằng hình. **Bảng B3** (tr.45, 55, 94–95, 170, 185 — `host_redactions.keep_in_host_but_excluded_from_cards`) **giữ nguyên** trong file host (QĐ 46). Là điều kiện ra mắt (QĐ 29, AC-79) | Máy: đọc `host_redactions` từ `licences.json`; trích chữ các trang trong `redact` (tr.113, 166, 117), không còn đoạn bị loại; các trang trong `keep_in_host_but_excluded_from_cards` (B3) còn bảng (không redact nhầm). Người: xem bằng mắt từng trang; **trước ra mắt**, S3 liệt kê mọi trang tr.1–197 có bảng số tiền và người xem bằng mắt các trang có tên một thực thể thật (giới hạn soát lần 1 của Legal §A.2) | MÁY+NGƯỜI | QĐ 15 · 29 · 46 · LEGAL-SCREEN §Kết luận · Legal §A.2 | Sẵn (B2 che, B3 giữ — QĐ 46; đã có trong `licences.json` → `host_redactions`) |
| AC-24 | File host và trang Nguồn mang nguyên văn `attribution_text` trong `licences.json`, ghi CC BY 3.0 | So chuỗi | MÁY | QĐ 15 · `licences.json` | Sẵn |
| AC-25 | `licences.json` có trường `file` trỏ đúng file host; `vibe-check [4]` PASS | Chạy vibe-check của xưởng trên app này | MÁY | CLAUDE.md quy tắc 4 | Sẵn |
| AC-26 | **File riêng của người học không rời máy**: từ lúc chọn file tới lúc đóng, không request mạng nào mang byte, tên hay nội dung của file; event đếm (nếu có) chỉ mang `source: own` | Máy: ghi toàn bộ network log khi mở/đọc/đóng file trên trình duyệt máy tính. Người: lặp lại trên điện thoại thật, trong WebView Zalo | MÁY+NGƯỜI | QĐ 4 · 9 · 29 | Máy: Sẵn · Điện thoại: **BLOCKED — chờ đo `input type=file`** — chặn ra mắt (AC-79); đo ra không chạy: **→ Duy (ĐK-1, `DECISIONS-QUEUE.md`)** |
| AC-27 | Trình đọc PDF chỉ tải khi người học mở PDF; trang bài không tải nó | Network log của một trang bài | MÁY | QĐ 4 | Sẵn |
| AC-28 | Vị trí đọc được nhớ: đóng rồi mở lại cùng tài liệu ⇒ mở đúng trang | Chạy tự động với Hermanson | MÁY | QĐ 4 · 7 | Sẵn (file riêng: BLOCKED cùng AC-26) |

## F. Tiến độ, khôi phục, sync

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-29 | Tiến độ là **một** bản ghi có trường `schema`; tên key + schema được ghi thành văn bản; đổi tên/nghĩa chỉ bằng dòng có ngày. Schema gồm: bài đã đọc · trạng thái card · trang PDF · ngôn ngữ · `tel` · thời điểm hoạt động cuối (QĐ 26); **không** có hàng đợi event | Đọc storage sau khi đọc 1 bài + làm 1 card | MÁY | QĐ 7 · 26 | Sẵn |
| AC-30 | Từ trạng thái chưa có tiến độ, tự khai **giai đoạn** trong **≤2 chạm**; lựa chọn là giai đoạn (lối vào là một khối), không phải từng bài (QĐ 23) | Máy: đếm thao tác; không có lựa chọn cấp bài. Người: thử trên điện thoại | MÁY+NGƯỜI | QĐ 7 · 23 | Sẵn |
| AC-31 | Link sync: tạo ở máy A, mở ở máy B qua Zalo ⇒ tiến độ B = A; dữ liệu sync chỉ nằm sau `#`, không bao giờ ở path/query; không request nào gửi dữ liệu sync lên server. Cách sao lưu chỉ `link` hoặc `code` — không file JSON (QĐ 18, 25c) | Máy: kiểm vị trí dữ liệu + network log. Người: thử qua Zalo thật | MÁY+NGƯỜI | QĐ 7 · 18 · 25 | **BLOCKED — chờ đo Zalo `#fragment`.** Zalo cắt `#` ⇒ AC này đổi sang "copy mã" (QĐ 7), thêm dòng ở §Thay đổi |
| AC-32 | Lời mời cài màn hình chính chỉ hiện sau ~3 bài và kèm bước sync | Chạy tự động | MÁY | QĐ 7 | **BLOCKED — chờ đo iPhone** (tab và app có tách storage không) |

## G. Đo và riêng tư

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-33 | Không script, font, ảnh hay request nào tới domain khác, trên mọi trang (trừ link người học tự bấm) | Network log toàn site | MÁY | QĐ 9 · CLAUDE.md quy tắc 8 | Sẵn |
| AC-34 | Payload bộ đếm chỉ gồm tên event + thuộc tính có trong `TRACKING-PLAN.md`; không ID; không cookie nào được đặt | Bắt payload; kiểm cookie jar | MÁY | QĐ 9 | Sẵn |
| AC-35 | Phía nhận không lưu IP | Duy đọc cấu hình phía nhận — **máy phía client không kiểm được điều này** | NGƯỜI | QĐ 9 | Sẵn |
| AC-36 | Mọi event trong `TRACKING-PLAN.md` bắn **và về đích**: nhìn thấy số ở phía nhận | Làm từng hành động, xem số tăng (S4) | NGƯỜI | CLAUDE.md quy tắc 8 | Sẵn · phạm vi ở S5: xem §Thay đổi 2026-10-24 vòng sửa (hẹp như AC-69/AC-70, AC-74) |

## H. Nội dung, pháp lý, ra mắt

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-37 | Không mã chứng khoán, không khuyến nghị mua/bán/nắm giữ, không bảng lãi suất có tên ngân hàng | Người: Duy đọc từng bài. Máy chỉ phụ trợ (quét cụm "nên mua/bán", tên ngân hàng cạnh `%`) — **không đủ để PASS một mình** | NGƯỜI | ONE-PAGER §3 · LEGAL-SCREEN | Sẵn |
| AC-38 | Nguồn NC (BIS, OpenStax…) và sách trả phí chỉ xuất hiện dưới dạng link; không file, ảnh bìa, logo của chúng trong site | Mọi asset có mục `licences.json` với giấy phép không NC; người soát trang sách | MÁY+NGƯỜI | QĐ 10 · ONE-PAGER §3 | Sẵn |
| AC-39 | Tên sản phẩm ở tiêu đề trang, trang chủ, thẻ chia sẻ luôn đi kèm tagline **T1** (QĐ 22): VN *"Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu."* · EN *"From the bank alert to the ledger: where your money actually goes."* | Kiểm title/meta + trang chủ, so nguyên chuỗi | MÁY | PIPELINE Log tên · ONE-PAGER §1 · QĐ 22 | Sẵn |
| AC-40 | Footer mọi trang có link Nguồn & giấy phép · Riêng tư · Disclaimer; không có đăng nhập, tài khoản, bình luận | Quét mọi trang | MÁY | LEGAL-SCREEN §Quy tắc vận hành | Sẵn (nội dung: `LEGAL-REVIEW.md`) |
| AC-41 | GĐ03/04/06/07 hiện "sắp có", **không ghi ngày** | Quét bản đồ lộ trình | MÁY | QĐ 5 | Sẵn |
| AC-42 | **Cổng ra mắt:** toàn bộ 12–15 bài lối vào VN `published=true` và mọi AC áp dụng cho chúng PASS, **AC-79 PASS** (phần sách, QĐ 29) **và AC-83 PASS** (cảnh báo `persist()`, QĐ 45) | Đếm + đọc bảng PASS của S4; Duy ký | MÁY+NGƯỜI | QĐ 14 · 29 · 45 | **BLOCKED — chờ agent `ke-toan-reviewer` chạy thử trên 1 bài mẫu + card** (điều kiện 3, QĐ 36; card lối vào có con số — phạm vi soát theo QĐ 8 + 30) · phần sách: BLOCKED cùng AC-79 · lối vào **không** chờ Phụ lục II (QĐ 37) |

## I. Ràng buộc Legal chưa có AC — thêm 2026-10-24

Số Legal R là của `LEGAL-REVIEW.md`. Không phải ý kiến pháp lý (QĐ 12).

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-43 | Khi trình đọc PDF mở file host Hermanson, và trên trang Nguồn & giấy phép: hiện nguyên văn `attribution_text` **và** URI `https://creativecommons.org/licenses/by/3.0/` cạnh nó | `grep -F` cả hai chuỗi trong build output của hai bề mặt | MÁY | Legal R3 · R4 | Sẵn |
| AC-44 | File host còn nguyên dòng giấy phép CC ở chân trang PDF, không bị redact | `pdftotext` file host có "Creative Commons Attribution 3.0" | MÁY | Legal R4 | Sẵn |
| AC-45 | Mọi card có nguồn Hermanson, và mọi section có `based_on` khác rỗng, hiện một dòng ghi công ngắn ("dựa trên Hermanson et al., đã dịch và sửa đổi, CC BY 3.0") kèm link tới trang Nguồn & giấy phép. **Mọi section (VI và EN) có trường `based_on`** theo Legal §A.1: `[]` = Writer khai không dựa trên nguồn CC nào; phần tử có `asset` là `id` có thật trong `licences.json`, `pages` là trang có thật của cuốn (QĐ 28: phạm vi nạp = cả cuốn), `mode` ∈ `dich_sat` · `dien_giai` · `vi_du`. Section `based_on: []` không chứa tên riêng nào trong danh sách lint Hermanson | Máy (build): (1) test render — card/section nguồn Hermanson thiếu dòng ghi công ⇒ FAIL · (2) section **thiếu trường** `based_on` ⇒ FAIL · (3) `asset` không có trong `licences.json`, `pages` ngoài tr.1–1004, hoặc `pages` chạm trang bị che/cấm của bên thứ ba (`host_redactions.redact`: tr.113, 117, 166 + hình bên thứ ba tr.501, 803) ⇒ FAIL; `pages` chạm trang B3 (`keep_in_host_but_excluded_from_cards`: tr.45, 55, 94, 95, 170, 185 — giữ trong file host để giữ phần giảng theo QĐ 46) hoặc trang khớp mẫu ③ ⇒ **cảnh báo** trong báo cáo build để Duy kiểm bài học chỉ lấy lời giảng/khái niệm của Hermanson, không chép bảng số liệu hay đoạn trích bên thứ ba · (4) **lint tên riêng** (`hermanson_entities_lint`): section `based_on: []` chứa tên trong danh sách ⇒ FAIL. Người: bắt **khai sai `[]`** và kiểm các mục có cảnh báo ở (3) | MÁY+NGƯỜI | Legal R5 · §A.1 · CC BY 3.0 §7 · QĐ 28 · 46 · 47 | (1)–(3): Sẵn (câu chữ: Legal; vị trí: S2; phân tách trang cấm/cảnh báo theo QĐ 46, 47) · (4) danh sách tên riêng: **TBD — S3 trích bằng `pdftotext` từ tr.1–197, Duy duyệt danh sách** |
| AC-46 | Tên tác giả/nhà xuất bản chỉ xuất hiện trong dòng ghi công (không ngụ ý bảo trợ); file host tải trực tiếp được qua URL công khai, không mật khẩu, không mã hoá | Máy: `curl -I` URL file host trả 200. Người: Duy đọc UI | MÁY+NGƯỜI | Legal R6 | Sẵn |
| AC-47 | File host được cắt từ đúng bản gốc ở `source_url` của `licences.json`, không từ bản Textbook Equity (NC-SA) | File tải về có `bytes` = 7991863 trước khi cắt | MÁY | Legal R7 | Sẵn |
| AC-48 | Đoạn đã redact và bản dịch không làm méo ý tác giả | Duy đọc các đoạn đã sửa, ghi tên + ngày | NGƯỜI | Legal R8 | Sẵn |
| AC-49 | Mỗi lần chạy máy sinh card ghi danh sách file input; có file ngoài whitelist (bài tự viết + Hermanson host) ⇒ lần chạy FAIL, không card nào của lần đó được ship. Không asset nào trong `licences.json` có giấy phép chứa "NC" hoặc "ND" | Đọc manifest input + quét `licences.json` | MÁY | Legal R12 · QĐ 3 · 10 | Sẵn |
| AC-50 | Link nguồn ngoài (OpenStax, Modern Treasury, Stripe, CFI, IMF, BIS…) mang nhãn "đọc thêm, không bắt buộc" (chữ: Writer) và **không tính vào tiến độ**: bấm vào không đổi JSON tiến độ, không bắn event | Chạy tự động: bấm link, so JSON trước/sau, xem payload | MÁY | Legal R15 | Sẵn |
| AC-51 | Mọi link tới văn bản luật trỏ tới domain trong whitelist (vbpl.vn, congbao.chinhphu.vn, sbv.gov.vn); không link nào tới hethongphapluat.com. **Phần ra mắt: 0 chữ trích nguyên văn văn bản luật** — chỉ link + diễn giải bằng lời mình (QĐ 33). Bài mở sau (từ GĐ05): mỗi đoạn trích nằm trong khối trích dẫn có nguồn, số chữ ≤ ngưỡng | Quét link + đếm chữ trong khối trích luật | MÁY | Legal R18 · QĐ 33 | Phần domain + 0 chữ ở phần ra mắt: Sẵn · ngưỡng cho GĐ05: đặt khi mở GĐ05 (QĐ 33) |
| AC-52 | Trang EN có trích luật VN chứa "unofficial summary" + link bản VN; không dùng bản dịch của LuatVietnam, TVPL, KPMG, PwC | Máy: grep chuỗi. Người: Duy duyệt EN | MÁY+NGƯỜI | Legal R19 | Sẵn · phần ra mắt không có trích luật (QĐ 33) ⇒ áp từ GĐ05 |
| AC-53 | Mọi bài và bộ card `published=true` (cả EN) hiện dòng minh bạch AI có người duyệt + ngày (QĐ 34.1); build FAIL nếu thiếu `reviewed_by` hoặc `reviewed_on`. Cờ `ai_assisted` (true/false) đặt **theo bài / bộ card / bản EN** — bài có bất kỳ phần nào dùng AI ⇒ cả bài `true` (QĐ 42); chữ "Soạn với hỗ trợ AI" hiện **khi và chỉ khi** `ai_assisted = true` (QĐ 34.3). **Mọi bản EN do Claude dịch lúc build có `ai_assisted = true`** — hệ quả trực tiếp của QĐ 6 + 34, không phải quyết định mới | Build trên bộ nội dung có một mục thiếu trường ⇒ phải FAIL; render một mục `ai_assisted=false` ⇒ không có chuỗi đó, `true` ⇒ có; bản EN dịch lúc build mà `ai_assisted ≠ true` ⇒ FAIL | MÁY | Legal R20 (gray → L14) · QĐ 34 · 42 | Trường + build FAIL + cờ: Sẵn · hạt: bài / bộ card / bản EN (QĐ 42) · chữ định danh trong "duyệt bởi ⟨…⟩": **BLOCKED — chờ hợp đồng Ringkas** (QĐ 34.2) |
| AC-54 | Footer mọi trang có chuỗi disclaimer; bài gắn tag lãi suất/pháp lý mà thiếu trường "căn cứ văn bản hiệu lực đến ⟨ngày⟩" ⇒ build FAIL | Quét footer; build với một bài gắn tag thiếu ngày | MÁY | Legal R21 | Sẵn |
| AC-55 | Mã Worker không đọc `CF-Connecting-IP`, User-Agent, `request.cf`, referrer, cookie; không `Set-Cookie`. Request mang các header đó ⇒ bản ghi lưu không chứa chúng. Event hoặc giá trị ngoài whitelist ⇒ bỏ, Worker vẫn trả 204 | grep mã Worker + test gửi request | MÁY | Legal R23 · TRACKING-PLAN §3 | Sẵn |
| AC-56 | Cấu hình wrangler có `observability.enabled = false` và tắt cả `issues`; mã Worker không `console.log(request)`, không Logpush. S4: dashboard Cloudflare **không có log request** | Máy: đọc config + grep. Người: Duy mở dashboard | MÁY+NGƯỜI | Legal R24 · TRACKING-PLAN §3 | Sẵn |
| AC-57 | Trang riêng tư chứa **đúng câu R25 mới** (QĐ 49, nguyên văn đề xuất của Legal X12): VN *"Khi bạn đọc, Where Money Sleeps không thu thập định danh; nhà cung cấp hạ tầng có ghi địa chỉ IP cho mục đích bảo mật của họ. Nếu bạn gửi thư tới hộp thư khiếu nại, những gì bạn gửi (tên, email, nội dung) chỉ được dùng để xử lý khiếu nại đó."* · EN *"When you read, Where Money Sleeps collects no identifiers; our infrastructure provider logs IP addresses for its own security purposes. If you email the complaints address, what you send (name, email, message) is used only to handle that complaint."* (WRITER §5); không trang nào chứa "không thu thập gì" / "collects nothing"; câu R25 cũ (thiếu vế hộp thư) không còn trên trang nào | `grep -F` câu mới (VN và EN); grep câu cũ đứng một mình ⇒ phải không thấy | MÁY | Legal R25 · QĐ 49 · WRITER §5 | Sẵn (VN: QĐ 49; EN: WRITER §5, Duy duyệt EN theo AC-02) |
| AC-58 | Bản sao lưu (link hoặc mã) decode ra chỉ gồm field trong whitelist schema tiến độ — **gồm `tel`, không gồm thời điểm hoạt động cuối** (QĐ 26); không chứa tên file PDF riêng; với link, dữ liệu chỉ nằm sau `#` | Test sinh bản sao lưu, decode, so whitelist | MÁY | Legal R28 · QĐ 7 · 26 | Máy: Sẵn · qua Zalo (độ dài link có `tel`): **BLOCKED — chờ đo** |
| AC-59 | Mỗi họ font tự host có OFL.txt đi kèm; PDF.js pin phiên bản, LICENSE (+ NOTICE nếu có) có trong build; font và PDF.js có dòng `licences.json` **cùng commit** với file | Quét build + lịch sử commit | MÁY | Legal R30 · R31 | Lõi: Sẵn · Giấy phép thư mục `standard_fonts`, `cmaps`: **TBD — đọc LICENSE trong thư mục đó** |
| AC-60 | `vibe-check [4]` chiều "đĩa → sổ" quét cả pdf, png, jpg, svg, woff2, ttf và thư mục vendor — **trước** commit asset đầu tiên của S3 | Đặt một file `.pdf` không có dòng sổ ⇒ [4] phải FAIL | MÁY | Legal §2 (lỗ hổng máy kiểm) | Sẵn — script ở cấp xưởng, chưa sửa |
| AC-61 | **Đường gỡ trước S5 = nhận khiếu nại + lật cờ.** PASS khi đủ cả bốn (Legal R33): **(a)** B10 có **hộp thư riêng cho site**, không họ tên đầy đủ, không nhắc Ringkas (QĐ 35) · **(b)** B10 in **"gỡ tạm trong 72 giờ"** (QĐ 35; NĐ 17/2023 đặt hạn ngắn hơn thì luật thắng) · **(c)** diễn tập cờ: đặt `published=false` cho 1 bài, 1 card và file host Hermanson ⇒ build ⇒ cả ba URL trả 404; ghi số phút từ lúc sửa tới lúc gỡ xong · **(d)** diễn tập đầu-cuối: gửi một khiếu nại giả tới hộp thư (a) ⇒ Duy nhận ⇒ lật cờ ⇒ 404; số giờ đo được ≤ 72 | (a), (b): quét build output trang B10 có địa chỉ hộp thư và chuỗi "72 giờ"; không có họ tên đầy đủ, không có "Ringkas" · (c): chạy một lần ở S4, ghi kết quả · (d): Duy làm tay một lần ở S4, ghi giờ gửi, giờ nhận, giờ 404 | MÁY+NGƯỜI | Legal R33 · QĐ 14 · 35 | (b), (c): Sẵn · **(a) công khai hộp thư: BLOCKED — chờ Duy đọc hợp đồng Ringkas** (QĐ 35) · (d): BLOCKED cùng (a) |

## J. Đo — từng event của TRACKING-PLAN — thêm 2026-10-24

Tên event theo `TRACKING-PLAN.md` §1 — hợp đồng đã chốt ở **QĐ 25**: `sync_created` thay `sync_link_created`; bỏ `lesson_completed.lang`; `method` ∈ {`link`,`code`}; thẻ lật không bắn `card_answered`.

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-62 | `lesson_completed{lesson, from_start}` (không thuộc tính nào khác — QĐ 25b, mở lại có chủ đích ở QĐ 39) bắn **đúng một lần** mỗi `lessonId` trên một bộ storage, bất kể ngôn ngữ, lúc người học **trả lời card trắc nghiệm đầu tiên của bộ card cuối bài, đúng hay sai** (QĐ 24, 38); chạm "Nhớ / Chưa nhớ" trên thẻ lật **không** bắn (QĐ 38); **không thoả được bằng cuộn nhanh tới cuối**. `from_start` = storage này đã có `lesson_completed` của bài 1 lối vào chưa (chữ QĐ 39; chính bài 1 lối vào luôn mang `from_start=true` vì tính sau bước ghi khoá R1 — TRACKING-PLAN §2.5); tính trên máy, không gửi ID nào | Trả lời 1 card trắc nghiệm ở VI, gạt EN, trả lời lại ⇒ đúng 1 beacon; chỉ chấm thẻ lật ⇒ 0 beacon; cuộn nhanh tới cuối không trả lời card ⇒ 0 beacon; storage trống vào thẳng bài 5 ⇒ `from_start=false`; xong bài 1 (`from_start=true`) rồi bài 5 ⇒ `from_start=true` | MÁY | TRACKING-PLAN §1 · §2 R1–R2 · §2.5 · QĐ 24 · 25 · 38 · 39 | Sẵn (TRACKING-PLAN §2.5) |
| AC-63 | Mọi bài của **giai đoạn** được tự khai (QĐ 23; lối vào là một khối) ghi `suppressed` và **không bao giờ** bắn `lesson_completed`, kể cả khi sau đó trả lời card thật | Tự khai lối vào ⇒ trả lời card ở một bài lối vào ⇒ 0 beacon | MÁY | TRACKING-PLAN §2 R3 · QĐ 23 | Sẵn |
| AC-64 | `card_answered{card, correct}` chỉ bắn ở lần trả lời **đầu tiên** của mỗi `<cardId>.v<n>`, **chỉ với card trắc nghiệm** — thẻ lật tự chấm không bắn (QĐ 25d); `cardId` không đổi khi máy sinh card chạy lại; sửa card đã đăng ⇒ tăng `v` | Trả lời 2 lần ⇒ 1 beacon; chấm một thẻ lật ⇒ 0 beacon; chạy lại máy sinh card ⇒ so tập `cardId` | MÁY | TRACKING-PLAN §1 · QĐ 25 | Sẵn |
| AC-65 | `pdf_opened{source}` bắn một lần mỗi `source` (`hosted`, `own`), lúc PDF render xong trang đầu; payload không có gì ngoài `source`. Ra mắt cùng M1 (QĐ 29) | Mở mỗi nguồn 2 lần ⇒ 2 beacon tổng | MÁY | TRACKING-PLAN §1 · QĐ 4 · 29 | Máy tính: Sẵn · `own` trên điện thoại: BLOCKED cùng AC-26 |
| AC-66 | `sync_created{method}` bắn một lần mỗi `method`, `method` ∈ {`link`,`code`} (QĐ 25a, c); `progress_restored{method}` bắn **mỗi lần** khôi phục thành công; sau khôi phục, các bài đã xong trong bản sao lưu **không** bắn lại vì `tel` đi theo bản sao lưu (QĐ 26); bản sao lưu không có `tel` ⇒ các bài đã xong ghi `suppressed` | Tạo sao lưu ⇒ khôi phục ở storage trống ⇒ đếm beacon | MÁY | TRACKING-PLAN §1 · §2 R4 · QĐ 25 · 26 | **BLOCKED một phần** — `method` nào thực sự có (link hay chỉ mã) chờ đo Zalo |
| AC-67 | Gửi bằng `navigator.sendBeacon`; khoá ghi `sent` **trước**, rồi gọi `sendBeacon` đúng một lần bất kể kết quả; **không hàng đợi**: mất mạng ⇒ event mất, không gửi lại (QĐ 26); không dùng `unload`/`beforeunload`/`pagehide` | Test offline: bắn khi offline, bật mạng, mở lại ⇒ 0 beacon cho khoá đó; JSON tiến độ không có trường hàng đợi | MÁY | TRACKING-PLAN §2 R1 · R5 · R6 · QĐ 26 | Sẵn |
| AC-68 | Site và bộ đếm **cùng origin**; path của bộ đếm không thuộc danh sách cấm (`/collect` `/event` `/track` `/beacon` `/metrics` `/api/event`) | Network log + so path | MÁY | TRACKING-PLAN §3 · QĐ 9 | Sẵn |
| AC-69 | **Dashboard sống trước S5**, đọc từ số thật: M1 (luỹ kế + 28 ngày trượt, bỏ 14 ngày cuối của mẫu số; **hai dòng: số chặt `from_start=true` và số lỏng** — QĐ 39), M2, M3 (card ≥ 30 lượt), M4, M5, và tổng ghi mỗi ngày. Ẩn ô n < 5: AC-80 | Duy mở dashboard, thấy đủ các dòng | NGƯỜI | SUCCESS-CRITERIA §1–2 · TRACKING-PLAN §5 | Sẵn (hình thức: SWE chốt ở S3) · phạm vi ở S5: xem §Thay đổi (AC-74; M4 nay có số từ ra mắt) |
| AC-70 | **Event về đích, nhìn bằng mắt ở S4:** trên **iPhone thật và Android thật**, làm tay hành động của đủ 5 event — `lesson_completed`, `card_answered`, `pdf_opened` (`hosted` và `own`), `sync_created`, `progress_restored` — và **thấy số tăng đúng** trên dashboard. Ghi kết quả vào file EVENT-VERIFICATION.md của S4. **Không PASS bằng đọc code.** Làm mịn AC-36, không thay nó | Duy làm tay, nhìn dashboard | NGƯỜI | CLAUDE.md quy tắc 8 · TRACKING-PLAN §5 | **BLOCKED một phần** — `pdf_opened{own}` (nay **ra mắt cùng M1**, QĐ 29) và hai event sao lưu chờ đo iPhone/Android · phạm vi ở S5: xem §Thay đổi (AC-74) |

## K. Chữ và chú thích — thêm 2026-10-24

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-71 | Kiểm số trong card (AC-16) hiểu cả hai định dạng: card EN có `2.5%` / `10,000,000 VND` khớp `source_quote` VN có `2,5%` / `10.000.000đ` sau chuẩn hoá | Bộ test số hai định dạng | MÁY | WRITER §1 · ADDENDUM bước 5 | Sẵn |
| AC-72 | Không bài, card hay chuỗi giao diện nào chứa **cụm** cấm của WRITER §1 (VN và EN); chữ hiển thị trên giao diện không dùng "đồng bộ"/"sync". Phép kiểm chỉ xét **chữ người đọc thấy**, không xét URL, `href`, fragment `#sync` (AC-31), thuộc tính, mã JS hay tên event (`sync_created`) | Máy: (1) trích text node hiển thị từ build output (sau chuẩn hoá NFC) · (2) so theo **cụm có ranh giới từ**, không theo chuỗi con · (3) mỗi mục cấm có danh sách ngoại lệ cụm (vd "chưa chắc chắn" không dính "chắc chắn") · (4) **tự kiểm:** mọi câu mẫu "✅ Đúng" của WRITER §1 phải PASS phép kiểm này — câu mẫu đúng mà FAIL ⇒ danh sách sai, không phải câu sai | MÁY | WRITER §1 · §5 | Cơ chế: Sẵn · danh sách cụm cấm + ngoại lệ: **TBD — Writer** chuyển WRITER §1 từ danh sách từ sang danh sách cụm (vd từ "easy" đang dính chính câu mẫu đúng ở WRITER §1 quy tắc 4) |
| AC-73 | Chú thích thuật ngữ **không hiện sẵn**; chỉ mở khi chạm vào thuật ngữ. Chạm ⇒ thẻ chú thích **chèn ngay sau câu chứa thuật ngữ, đẩy chữ phía dưới xuống** — không phải lớp phủ (QĐ 17). Dấu chạm được ở **lần đầu mỗi mục H2** (QĐ 19, AC-11) | Render bài: không định nghĩa nào hiện trước khi chạm; chạm ⇒ phần tử chú thích nằm **trong luồng tài liệu** ngay sau câu đó, không `position: fixed/absolute`, không popover | MÁY | QĐ 16 · 17 · 19 | Sẵn · so với "thẻ phủ lên chữ" ở buổi 5 người (QĐ 17) |

## L. Từ T2 chéo-phòng — thêm 2026-10-24

Câu hỏi và lý do: `PRD.md` §T2.

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-74 | **Cổng bật tính năng mang event.** Tính năng không ra mắt cùng M1 — hiện là sao lưu/khôi phục (`sync_created`, `progress_restored`) — khi bật cho người dùng thì **ngay trong ngày** Duy làm phép kiểm của AC-70 cho event đó và thấy dòng metric (M5) trên dashboard AC-69 có số thật; ghi vào EVENT-VERIFICATION.md kèm ngày bật. FAIL hoặc chưa làm ⇒ tắt lại tính năng. Ở cổng S5, event của tính năng chưa bật ghi `N/A — because <tính năng chưa bật>, kiểm lúc bật <tên>`. Trình đọc PDF **không** còn thuộc AC này (ra mắt cùng M1, QĐ 29); bản EN không có event (QĐ 25b) | Duy làm tay trên iPhone + Android thật, nhìn dashboard; đối chiếu ngày bật với dòng trong EVENT-VERIFICATION.md | NGƯỜI | CLAUDE.md quy tắc 8 · PRD §T2 Data câu 1 · QĐ 25 · 29 | Sẵn (hai event sao lưu: BLOCKED cùng AC-70) |
| AC-75 | Bài `published=true` mà không có **card trắc nghiệm** nào `published=true` ⇒ build FAIL; thẻ lật không tính (QĐ 38). Áp cả chiều đăng lẫn chiều gỡ: gỡ card trắc nghiệm `published` cuối cùng của một bài phải đi cùng gỡ bài, hoặc đăng card trắc nghiệm thay đã duyệt (AC-02, AC-03) | Build ba bộ nội dung: (a) bài `published` + 0 card `published`; (b) bài `published` có 1 card trắc nghiệm, đặt card đó `published=false`; (c) bài `published` chỉ có thẻ lật `published` ⇒ cả ba FAIL | MÁY | QĐ 24 · 38 · PRD §T2 Data câu 2 | Sẵn |
| AC-76 | Ôn đầu phiên ở **bề mặt đầu tiên của phiên**, B1 hoặc B3: có card đã trả lời ở phiên trước ⇒ hiện 1–2 card ôn, không chặn đọc (bỏ qua bằng 1 chạm), không hiện lại trong cùng phiên. Vào B3 khi chưa có tiến độ ⇒ có lối vào B9, không chặn đọc. "Phiên" theo PRD §Định nghĩa dùng chung, tính từ trường thời điểm hoạt động cuối (QĐ 26) | Chạy tự động: (a) phiên mới vào B1 · (b) phiên mới vào thẳng B3 · (c) mở lại trong cùng phiên ⇒ không ôn lại · (d) storage trống vào B3 ⇒ đọc được ngay, có lối vào B9 | MÁY | ADDENDUM bước 9 · QĐ 7 · 26 · PRD §T2 Design câu 2 | Sẵn · ngưỡng N giờ: **TBD — S2 đề xuất** |
| AC-77 | Mỗi H2 của bài mang đúng một `sectionId`; không phần tử nào dưới cấp H2 mang `sectionId`; link "đọc lại đoạn này" của **mọi** card (kể cả card Hermanson — AC-19) trỏ vào một `sectionId` trong tập đó | Quét build output của mọi bài | MÁY | QĐ 6 · 27 · PRD §Định nghĩa dùng chung · PRD §T2 Design câu 1 | Sẵn |
| AC-78 | Mọi trang có tên sản phẩm — kể cả header trang bài và thẻ chia sẻ `og:` của link bài — thì có tagline T1 đi kèm. Làm rộng AC-39, không thay nó | Quét build output mọi trang: có chuỗi tên ⇒ phải có chuỗi tagline | MÁY | PRD R16 · QĐ 22 · PRD §T2 Design câu 2 | Sẵn |

## M. Từ QĐ 17–35 — thêm 2026-10-24

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-79 | **Cổng ra mắt — phần sách** (QĐ 29), cùng AC-42: (1) trang sách B6 `published=true`, có thẻ sách Duy viết + link mua · (2) trình đọc PDF mở được file host Hermanson tr.1–197 **đã redact** tr.113, 166, B2 tr.117, **giữ** B3 (QĐ 46; AC-22, AC-23, AC-43, AC-44, AC-46 PASS; PDF.js + giấy phép AC-59 PASS — Legal R1–R4, R6, R31 + §A.2, LEGAL-REVIEW §2) · (3) trình đọc mở được file riêng thuần cục bộ (AC-26 PASS, cả phần điện thoại) · (4) `pdf_opened` `hosted` và `own` về đích (AC-70) | Máy: build có B6, B7, file host; chạy AC-22/23/26/43/44/46/59. Người: Duy duyệt thẻ sách (AC-02); làm AC-26, AC-70 trên máy thật | MÁY+NGƯỜI | QĐ 29 | (1) thẻ sách: **Duy viết** · (2) Sẵn — B2 che, B3 giữ (QĐ 46) · (3) **BLOCKED — chờ đo `input type=file`**; đo ra không chạy: **→ Duy (ĐK-1)** |
| AC-80 | Bộ đếm lưu theo **ngày**. Dashboard **không hiện ô nào có n < 5** và **không có bảng ngày × bài/card** (QĐ 32). Workflow pháp lý L13 kết luận số gộp ghép ra được người ⇒ gộp lên tuần và xoá dòng ngày, ghi dòng có ngày | Máy: render dashboard từ bộ số giả có ô n = 1…4 ⇒ không ô nào hiện số đó; quét định nghĩa dashboard không có bảng ngày × `lesson`/`card`. Người: truy vấn ô nhỏ bằng `wrangler` chỉ bị chặn bởi kỷ luật của Duy | MÁY+NGƯỜI | QĐ 32 · TRACKING-PLAN §3 · §5 | Sẵn |
| AC-81 | **Giữ ID mồ côi** (QĐ 18): bài hoặc card đã gỡ khỏi build mà còn trong JSON tiến độ ⇒ mục đó **không bị xoá** khi site tải lại; đăng lại bài ⇒ tiến độ cũ còn | Tạo tiến độ cho bài X ⇒ build không có X ⇒ mở site ⇒ JSON vẫn có X ⇒ build có lại X ⇒ X hiện đã đọc | MÁY | QĐ 18 · PRODUCT-BRIEF §Kiến trúc (dòng "Lưu tiến độ") | Sẵn |
| AC-82 | **Không auto-redirect theo ngôn ngữ** (QĐ 18): không trang nào chuyển hướng dựa trên `Accept-Language` hay `navigator.language`; ngôn ngữ chỉ đổi khi người học bấm nút gạt hoặc mở URL `/vi/`, `/en/` | Request mọi URL với `Accept-Language: en` và `vi` ⇒ cùng phản hồi, không 3xx theo ngôn ngữ; grep mã client không có điều hướng theo `navigator.language` | MÁY | QĐ 18 · PRODUCT-BRIEF §Kiến trúc (dòng "Song ngữ") | Sẵn |
| AC-83 | **Cảnh báo lưu trữ `persist()`** (QĐ 18) — **điều kiện ra mắt** (QĐ 45, qua AC-42): gọi `persist()` ngầm, không hiện hộp xin quyền do site tự vẽ; hiện đúng 3 biến thể của WRITER §6 — biến thể `false` **chỉ** cho tab iOS **đã có tiến độ**, biến thể `true` vẫn nhắc sao lưu, dòng footer luôn hiện; chữ PASS AC-72 (không "lưu vĩnh viễn") | Máy: chạy với `persist()` giả trả `true`/`false`, có/không tiến độ ⇒ đúng biến thể; `false` mà chưa có tiến độ ⇒ không hiện cảnh báo. Người: thử trên iPhone thật | MÁY+NGƯỜI | QĐ 18 · 45 · WRITER §6 | Cơ chế: Sẵn · `persist()` trên iPhone: chưa đo (phần NGƯỜI, S4) — chặn ra mắt qua AC-42 |

## N. Legal R35, R37 — thêm 2026-10-24 (vòng sửa 2)

R36 (QĐ 32) đã có AC-80. Không phải ý kiến pháp lý (QĐ 12).

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-84 | **Không rule chặn theo IP do Duy cấu hình** ở Cloudflare (QĐ 31): không rule Rate Limiting, không WAF custom rule, Bot Fight Mode tắt. Chống bơm số chỉ bằng cờ F1–F4 + cách ly ngày (TRACKING-PLAN §2.4) | Duy mở dashboard Cloudflare của zone/Worker (S4), xác nhận ba mục trên; ghi ngày kiểm | NGƯỜI | Legal R35 · QĐ 31 · QĐ 9 · QĐ 38 | Sẵn · gặp tính năng xử lý IP **mặc định bật mà tắt được**: **→ Duy (ĐK-2, `DECISIONS-QUEUE.md`)** (Legal R35 — QĐ 31 nói "không bật", chưa nói "tắt cái bật sẵn") |
| AC-85 | **Dữ liệu người khiếu nại** (Legal R37; hộp thư phương án A — QĐ 49): tên, email, nội dung thư khiếu nại **không** nằm trong repo, `gates/`, `docs/` hay build output; bản ghi gỡ trong repo chỉ gồm ngày, nội dung bị gỡ, loại lý do; thư không chuyển sang dịch vụ khác ngoài hộp thư (kể cả dán vào một phiên AI); **thư bị xoá khỏi hộp thư khi khiếu nại đóng** (QĐ 49) | Trong diễn tập đầu-cuối AC-61 (d): `git grep` địa chỉ email thử ⇒ 0 kết quả; Duy khai nhà cung cấp hộp thư và nơi đặt máy chủ; sau khi đóng khiếu nại giả, Duy xác nhận thư thử đã bị xoá khỏi hộp thư (ghi ngày) | NGƯỜI | Legal R37 · QĐ 35 · 49 | Sẵn (QĐ 49) · (d) BLOCKED cùng AC-61 (a) — chờ hợp đồng Ringkas |

## O. Từ QĐ 38–51 — thêm 2026-10-25

| AC | Tiêu chí PASS | Cách kiểm | Ai | Nguồn | Trạng thái |
|---|---|---|---|---|---|
| AC-86 | **Dòng soát công khai** (QĐ 41): mọi mục `published=true` thuộc phạm vi QĐ 30 (có trường báo cáo soát của agent khác rỗng theo AC-03/AC-21) hiện câu VN *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* · EN *"Figures and account names checked by an AI agent; signed off by ⟨…⟩."* (WRITER §5); mục ngoài phạm vi QĐ 30 (con số không card nào hỏi, do Duy đọc, không có báo cáo agent) **không** hiện câu W2. **Dòng minh bạch AI, dòng soát và trường `reviewed_by`** không chứa "kế toán", "accountant", "chuyên gia", "expert" (không phân biệt hoa thường); trường nội bộ ghi tên agent (`ke-toan-reviewer`) **không được render** ra HTML hiển thị. Luật cấm **không** áp cho thân bài | Máy: (1) mục có trường báo cáo soát của agent khác rỗng mà thiếu câu W2 ⇒ FAIL; mục không có báo cáo agent mà hiện câu W2 ⇒ FAIL (`LEGAL-REVIEW.md` R20) · (2) grep 4 chữ cấm và chuỗi `ke-toan-reviewer` trong chuỗi render của dòng minh bạch + dòng soát và trong giá trị `reviewed_by` ⇒ có là FAIL · (3) grep thân bài **không** chạy luật này | MÁY | QĐ 30 · 36 · 41 · Legal R20 · X13 · Writer W2 | Câu VN/EN + luật cấm: Sẵn (WRITER §5) · ⟨…⟩: **BLOCKED — chờ hợp đồng Ringkas** (QĐ 34.2) |

## Phủ LEGAL-REVIEW — mỗi ràng buộc trỏ tới AC

| Legal R | AC | | Legal R | AC |
|---|---|---|---|---|
| R1 | AC-22 · AC-25 | | R18 | AC-51 |
| R2 | AC-23 | | R19 | AC-52 |
| R3 | AC-24 · AC-43 | | R20 | AC-53 · AC-86 |
| R4 | AC-43 · AC-44 | | R21 | AC-40 · AC-54 |
| R5 | AC-45 (`based_on` + lint, §A.1) | | R22 | AC-03 · AC-04 · AC-21 · AC-86 (agent soát, Duy ký — QĐ 36; K2 tối đa "KHỚP NGUỒN THỨ CẤP" — QĐ 37; luật ký — QĐ 40; chữ công khai — QĐ 41) |
| R6 | AC-46 | | R23 | AC-34 · AC-35 · AC-55 |
| R7 | AC-47 | | R24 | AC-56 |
| R8 | AC-48 | | R25 | AC-57 (câu mới — QĐ 49) |
| R9 | AC-14 · AC-15 · AC-17 | | R26 | **Không có AC** — rủi ro đã chấp nhận (QĐ 11), xác nhận lại ở **QĐ 51**; workflow L13 + L18 trước S5 là cổng ở `PRD.md` §Delivery Milestones, không phải AC |
| R10 | AC-18 | | R27 | AC-33 |
| R11 | AC-18 · AC-19 (cả cuốn trừ trang trong `exclusions` + mẫu ③ — QĐ 47; card trỏ bất kỳ bài có `based_on` — QĐ 48) | | R28 | AC-31 · AC-58 |
| R12 | AC-38 · AC-49 | | R29 | AC-26 · AC-40 |
| R13 | AC-26 · AC-33 | | R30 | AC-33 · AC-59 · AC-60 |
| R14 | AC-38 · AC-60 | | R31 | AC-59 · AC-60 |
| R15 | AC-38 · AC-50 | | R32 | **N/A** — EPUB ra khỏi mùa 1 (QĐ 18) |
| R16 | AC-37 | | R33 | AC-01 · AC-61 (a)–(d); (a) hộp thư + (b) 72 giờ theo QĐ 35; công khai (a) BLOCKED — chờ hợp đồng Ringkas |
| R17 | AC-37 | | R34 | **Không phải AC sản phẩm** — điều kiện chốt S1 (`blocked_on`) |
| | | | R35 | AC-84 |
| | | | R36 | AC-80 |
| | | | R37 | AC-85 · AC-57 (câu R25 mới, xoá thư khi đóng — QĐ 49) |

## Phủ TRACKING-PLAN — mỗi event và quy tắc trỏ tới AC

| Event / quy tắc | AC |
|---|---|
| `lesson_completed` (`from_start` — QĐ 39) | AC-62 · AC-63 · AC-69 · AC-70 |
| `card_answered` | AC-64 · AC-70 · AC-75 (≥ 1 card trắc nghiệm mỗi bài — QĐ 38) |
| `pdf_opened` | AC-26 · AC-65 · AC-70 |
| `sync_created` · `progress_restored` | AC-66 · AC-70 |
| Chống trùng R1–R6 (không hàng đợi, QĐ 26) | AC-62 – AC-67 |
| Payload chỉ field cho phép, không ID, không cookie | AC-34 |
| Worker không đọc IP/UA; tắt Workers Logs | AC-55 · AC-56 |
| Cùng origin, path trung tính, không script bên thứ ba | AC-33 · AC-68 |
| Dashboard trước S5 | AC-69 · AC-74 (dòng của tính năng bật sau) · AC-80 (ẩn ô n < 5, lưu theo ngày) |
| Không rule chặn theo IP ở Cloudflare (§2.4, QĐ 31) | AC-84 |
| Event về đích, nhìn bằng mắt | AC-36 · AC-70 · AC-74 (lúc bật tính năng) |

## Giới hạn của phép kiểm máy — nói thẳng

| Máy KHÔNG bắt được | Ai bắt thay |
|---|---|
| Thuật ngữ chuyên ngành chưa có mục glossary (AC-11) | Duy; GĐ01/05: agent kế toán soát, Duy ký (AC-12) |
| Card trích đúng nhưng hiểu sai (AC-16) | Duy ký (AC-02); card có số: agent kế toán soát (AC-03) — **cùng vendor, cùng priors với máy sinh card** |
| Agent kế toán sai cùng kiểu với nội dung nó soát (QĐ 36) | Chỉ K1 (code chạy lại được) và K2 (so nguyên văn) không dựa vào ý kiến agent; K3/K4 chỉ còn Duy |
| Tên TK GĐ01 khớp văn bản chính thức (AC-04) | Chưa ai — bản chép thứ cấp tối đa "KHỚP NGUỒN THỨ CẤP"; chờ Phụ lục II chính thức (QĐ 37) |
| Duy có thật sự đọc trước khi bật `published` (AC-02) | Không ai — đây là lời hứa của Duy |
| Phía nhận có lưu IP (AC-35) | Duy đọc cấu hình |
| Hành vi trong WebView Zalo, iOS thật (AC-26, AC-31, AC-32) | Duy đo trên máy thật |
| Cloudflare có ghi log ngoài cấu hình wrangler không (AC-56) | Duy mở dashboard Cloudflare |
| Event bắn đúng ở code nhưng không về đích (AC-70) | Duy nhìn số trên dashboard |
| Đoạn bài dựa trên Hermanson mà chưa gắn nguồn (AC-45); bản dịch làm méo ý (AC-48); card Hermanson bản VN nói sai câu trích EN (AC-15) | Duy |
| Thuật ngữ VN ngoài danh sách gốc TT 99 + glossary (AC-11) | Duy; GĐ01/05: agent kế toán soát, Duy ký (AC-12) |
| Đoạn bên thứ ba trên trang không khớp mẫu ③ và không nằm trong `exclusions` (AC-18) | Không ai — rủi ro Duy nhận (QĐ 28, 47, 51); Duy duyệt từng card |
| Người đọc vẫn hiểu "agent soát" là có chuyên gia (AC-86) | Không ai — câu W2 đúng chữ nhưng cách đọc chưa đo; rủi ro xác nhận ở QĐ 51 |
| Duy truy vấn ô n < 5 bằng `wrangler` (AC-80) | Không ai — chỉ kỷ luật của Duy (QĐ 32) |

## Thay đổi — chỉ thêm, có ngày

| Ngày | AC | Thay đổi | Lý do |
|---|---|---|---|
| 2026-10-24 | AC-01…AC-42 | Bản nháp đầu | S1 mở |
| 2026-10-24 | AC-43…AC-61 | Thêm: ràng buộc Legal chưa có AC | PM gộp `LEGAL-REVIEW.md`; mọi ràng buộc chặn phải có AC |
| 2026-10-24 | AC-62…AC-70 | Thêm: từng event + chống trùng + dashboard + event về đích nhìn bằng mắt ở S4 | PM gộp `TRACKING-PLAN.md`, `SUCCESS-CRITERIA.md` |
| 2026-10-24 | AC-36 | **Không đổi nghĩa.** AC-70 làm mịn nó: nêu tên 5 event, đòi máy thật, đòi file ghi kết quả | Tránh sửa tại chỗ |
| 2026-10-24 | AC-71…AC-73 | Thêm: định dạng số VN/EN, chữ cấm, chú thích chạm mới hiện | `WRITER.md` · QĐ 16 |
| 2026-10-24 | AC-69 · AC-70 | **Phạm vi ở cổng S5 hẹp lại:** chỉ event của tính năng ra mắt cùng M1. Event của tính năng chưa bật ghi `N/A — because …` và được kiểm lúc bật, theo AC-74. Chữ của hai AC không đổi | T2 Data câu 1: cổng S5 một lần sẽ hoặc chặn ra mắt vì tính năng không ship, hoặc lặng lẽ bỏ qua event |
| 2026-10-24 | AC-74…AC-78 | Thêm: cổng bật tính năng · bất biến bài ↔ card · ôn đầu phiên ở B1 hoặc B3 · `sectionId` = H2 · tagline mọi chỗ có tên | `PRD.md` §T2 (Data + Design) |
| 2026-10-24 (vòng sửa) | AC-45 | **Rộng ra:** thêm trường `based_on` bắt buộc trên mọi section, kiểm `asset`/`pages`, lint tên riêng. Cột Người **hẹp lại** còn bắt khai sai `[]` | Legal §A.1 + mục giao việc: CC BY 3.0 §7 chấm dứt giấy phép tự động; cờ `published` không cứu được |
| 2026-10-24 (vòng sửa) | AC-61 | **Rộng ra:** từ một diễn tập cờ (R33 c) thành đủ (a) kênh khiếu nại · (b) giờ phản hồi in trên B10 · (c) · (d) diễn tập khiếu nại → 404 | Legal R33 sửa sau T2: R33 PASS = (a)–(d). Bản cũ làm định nghĩa PASS ở đây khác LEGAL-REVIEW |
| 2026-10-24 (vòng sửa) | AC-36 | **Phạm vi ở cổng S5 hẹp lại như AC-69/AC-70:** chỉ event của tính năng ra mắt cùng M1; event của tính năng chưa bật ghi `N/A — because …`, kiểm lúc bật theo AC-74. Chữ AC-36 không đổi. Dòng 2026-10-24 "AC-36 không đổi nghĩa" ở trên vẫn đúng cho phần chữ | Không thu hẹp thì ở S5 AC-36 FAIL vì event của tính năng chưa bật, va AC-74 |
| 2026-10-24 (vòng sửa) | AC-72 | **Đổi cách kiểm:** chỉ chữ hiển thị, so theo cụm có ranh giới từ, có ngoại lệ, tự kiểm bằng câu mẫu đúng của WRITER | Bản cũ grep chuỗi con trên cả build output ⇒ dính `#sync`, tên event, câu mẫu đúng "the easy one…", "chưa chắc chắn" |
| 2026-10-24 (QĐ 17–35) | AC-03 | **Rộng ra:** kế toán soát thêm `sectionId` chứa `source_quote` của card có số; số không card nào hỏi: Duy | QĐ 30 |
| 2026-10-24 (QĐ 17–35) | AC-05 · AC-13 | **Đổi nghĩa "trộn":** chữ EN trên trang VI hợp lệ khi là mục `keep_en`; glossary có trường `keep_en` | QĐ 20 |
| 2026-10-24 (QĐ 17–35) | AC-11 · AC-12 | **Đổi:** đánh dấu lần đầu mỗi mục H2; `keep_en` thiếu dấu ⇒ FAIL; VN trong danh sách gốc thiếu dấu ⇒ cảnh báo (trước: FAIL cho mọi thuật ngữ) | QĐ 19 · 21 |
| 2026-10-24 (QĐ 17–35) | AC-14 · AC-15 · AC-16 · AC-19 · AC-77 | **Gỡ xung đột card Hermanson:** khái niệm, không số, hiện VN, `source_quote` EN không hiển thị, link về `sectionId` bài GĐ01. AC-15 cột Ai: MÁY → MÁY+NGƯỜI (Duy kiểm bản VN) | QĐ 27 |
| 2026-10-24 (QĐ 17–35) | AC-18 · AC-45 | **Rộng ra:** phạm vi trang = cả cuốn, trừ `exclusions` + trang có dấu hiệu nguồn ngoài; card ch.5+ chỉ đăng khi có bài `based_on` phủ trang (AC-19) | QĐ 28 |
| 2026-10-24 (QĐ 17–35) | AC-23 · AC-42 · AC-65 · AC-70 · AC-74 | **Phần sách vào cổng ra mắt:** AC-23 thêm bảng số liệu bên thứ ba; AC-42 đòi thêm AC-79; `pdf_opened` kiểm ở S5, rời AC-74 | QĐ 29 |
| 2026-10-24 (QĐ 17–35) | AC-29 · AC-58 · AC-66 · AC-67 · AC-20 · AC-76 | **Schema:** thêm `tel` (theo sao lưu) + thời điểm hoạt động cuối (không theo); **bỏ hàng đợi offline** khỏi AC-67 | QĐ 26 |
| 2026-10-24 (QĐ 17–35) | AC-30 · AC-63 | **Định nghĩa:** tự khai theo giai đoạn, lối vào một khối | QĐ 23 |
| 2026-10-24 (QĐ 17–35) | AC-31 · AC-62 · AC-64 · AC-66 · AC-74 | **Hợp đồng event:** bỏ `lesson_completed.lang`; `method` ∈ {`link`,`code`}; thẻ lật không bắn `card_answered`; bản EN không có event | QĐ 25 |
| 2026-10-24 (QĐ 17–35) | AC-62 · AC-75 | **Định nghĩa "xong":** trả lời ≥ 1 card cuối bài; AC-75 từ TBD → Sẵn | QĐ 24 |
| 2026-10-24 (QĐ 17–35) | AC-39 · AC-78 | Tagline = T1, so nguyên chuỗi | QĐ 22 |
| 2026-10-24 (QĐ 17–35) | AC-51 · AC-52 | **Ngưỡng:** 0 chữ trích luật ở phần ra mắt; ngưỡng GĐ05 đặt khi mở GĐ05 | QĐ 33 |
| 2026-10-24 (QĐ 17–35) | AC-53 | **Rộng ra:** cờ `ai_assisted`, "Soạn với hỗ trợ AI" khi và chỉ khi `true` | QĐ 34 |
| 2026-10-24 (QĐ 17–35) | AC-61 | (a) = hộp thư riêng, (b) = "gỡ tạm trong 72 giờ"; (d) đo ≤ 72 giờ | QĐ 35 |
| 2026-10-24 (QĐ 17–35) | AC-73 | **Rộng ra:** thẻ chú thích chèn trong luồng ngay sau câu, không lớp phủ | QĐ 17 · 19 |
| 2026-10-24 (QĐ 17–35) | AC-79…AC-83 | Thêm: cổng ra mắt phần sách · dashboard ẩn ô n < 5 · giữ ID mồ côi · không auto-redirect · cảnh báo `persist()` | QĐ 29 · 32 · 18 |
| 2026-10-24 (vòng sửa 2) | AC-03 · AC-04 · AC-12 · AC-42 | **Đổi người soát:** "người kế toán" → agent `ke-toan-reviewer` soát, Duy ký. AC-04 PASS chỉ khi K2 PASS trên Phụ lục II chính thức; "KHỚP NGUỒN THỨ CẤP" không bao giờ PASS. Trạng thái: hết "chờ tên kế toán"; nay chờ agent chạy thử (điều kiện 3) và Phụ lục II chính thức (GĐ01) | QĐ 36 · 37 |
| 2026-10-24 (vòng sửa 2) | AC-21 | **Đổi nghĩa:** trước cấm mọi trường "duyệt bởi" là model; nay tách **soát** (được là agent, ghi đúng tên `ke-toan-reviewer`) và **ký** (chỉ người). Bản cũ va thẳng QĐ 36 | QĐ 36 (dòng sau thắng ADDENDUM bước 6) |
| 2026-10-24 (vòng sửa 2) | AC-18 | **Đổi nguồn (i):** từ danh sách đoạn chép tay (ghi sai là `exclusions` có tr.113) sang danh sách trang trong `licences.json` `exclusions` bản Legal vòng sửa 2. **Hẹp lại:** bỏ "thêm dấu hiệu là tự do" — mở rộng mẫu là đổi chữ QĐ 28, → Duy (Legal X11) | Review M3 · Legal X3, X11 |
| 2026-10-24 (vòng sửa 2) | AC-23 · AC-79 | Quy tắc Legal cho bảng số liệu đã ra (§A.2): B2 tr.117 redact; B3 → Duy (X10); thêm bước xem bằng mắt trang có bảng số tiền. AC-79 (2) thêm AC-46, AC-59 (Legal R6, R31 thuộc cổng ra mắt) | QĐ 29 · Legal §2 |
| 2026-10-24 (vòng sửa 2) | AC-53 | **Rộng ra:** bản EN do Claude dịch lúc build ⇒ `ai_assisted = true` (hệ quả QĐ 6 + 34) | QĐ 6 · 34 |
| 2026-10-24 (vòng sửa 2) | AC-84 · AC-85 | Thêm: không rule IP ở Cloudflare (Legal R35) · dữ liệu người khiếu nại (Legal R37) | QĐ 31 · 35 · Legal R35, R37 |
| 2026-10-25 (QĐ 38–51) | AC-62 · AC-75 | **Hẹp lại:** "xong" = trả lời ≥ 1 card **trắc nghiệm**; thẻ lật không tính; bài `published` phải có ≥ 1 card trắc nghiệm `published` (thêm bộ thử (c) chỉ-thẻ-lật) | QĐ 38 |
| 2026-10-25 (QĐ 38–51) | AC-62 · AC-69 | **Rộng ra:** `lesson_completed` thêm `from_start`; dashboard M1 hai dòng chặt/lỏng | QĐ 39 (mở lại QĐ 25b) |
| 2026-10-25 (QĐ 38–51) | AC-03 · AC-04 | **Rộng ra:** luật ký — FAIL K1/K2/K3 chặn `published`; phán khác ký kèm dòng lý do (máy kiểm có dòng lý do) | QĐ 40 |
| 2026-10-25 (QĐ 38–51) | AC-21 · AC-86 | **AC-21 đổi nghĩa:** từ "một chuỗi soát · ký" sang hai trường — `reviewed_by` chỉ người ký, agent ở trường riêng. **Thêm AC-86:** câu dòng soát công khai + cấm 4 chữ trong dòng minh bạch, dòng soát, `reviewed_by` | QĐ 41 |
| 2026-10-25 (QĐ 38–51) | AC-53 | Hạt `ai_assisted` = bài / bộ card / bản EN | QĐ 42 |
| 2026-10-25 (QĐ 38–51) | AC-05 · AC-06 | **Rộng ra:** ngoại lệ (a) danh sách tên riêng · (b) dòng "chưa có bản EN" song ngữ · (c) chiều VN trên trang EN | QĐ 43 |
| 2026-10-25 (QĐ 38–51) | AC-13 | Mục `ledger`: `keep_en = false` | QĐ 44 |
| 2026-10-25 (QĐ 38–51) | AC-42 · AC-83 | **Cổng ra mắt rộng ra:** thêm AC-83 (`persist()`) | QĐ 45 |
| 2026-10-25 (QĐ 38–51) | AC-18 · AC-23 · AC-79 | B3 giữ trong file host, loại hẳn khỏi máy sinh card; B2 che. AC-18 (ii) đổi từ mẫu đúng chữ QĐ 28 sang **mẫu ③**, thêm tự kiểm 7/7 | QĐ 46 · 47 |
| 2026-10-25 (QĐ 38–51) | AC-19 | **Rộng ra:** card Hermanson trỏ bất kỳ bài `published` có `based_on` phủ trang, không chỉ GĐ01 | QĐ 48 |
| 2026-10-25 (QĐ 38–51) | AC-57 · AC-85 | AC-57 đổi sang câu R25 mới (QĐ 49); AC-85 thêm xoá thư khi khiếu nại đóng | QĐ 49 |

## Chưa xác minh được

- Mọi AC có cột "Người" trên điện thoại: chưa ai thử, vì phép đo iPhone/Android chưa làm.
- Ngoại lệ AC-05: đã quyết (QĐ 43); danh sách tên riêng và cờ đánh dấu chiều EN chưa dựng (S3). Cách máy nhận ra từ EN trên trang VI (từ VN không dấu trùng chữ EN): S3.
- AC-18: "annual report" xuất hiện 32 lần trong tr.1–197, gồm đoạn định nghĩa (`DECISIONS-QUEUE.md` C-09) — mẫu ③ vẫn loại các trang đó (QĐ 47 nhận cái giá này).
- AC-23: quy tắc Legal cho bảng số liệu bên thứ ba **đã ra** (§A.2), nhưng soát lần 1 chỉ bằng máy (30 tên công ty do Legal chọn, chưa trang nào xem bằng mắt); B3 giữ (QĐ 46) mang rủi ro "sưu tập dữ liệu" (L16, gray) — đã xác nhận ở QĐ 51.
- AC-03, AC-04: agent `ke-toan-reviewer` đã chạy thử trên bài mẫu `SAMPLE-LESSON-01.md` (báo cáo `SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`: `PASS 12 · FAIL 0 · KHỚP NGUỒN THỨ CẤP 6 · FLAG 7`); thời gian Duy đọc báo cáo + ký chưa đo (điều kiện 3). Phụ lục II TT 99 chính thức: chưa có trong repo, chưa biết lấy ở đâu.
- AC-18: danh sách trang `card_generator.excluded_pages` và `card_generator.page_rule` đã có trong `licences.json` (QĐ 46, 47). Legal sửa tiếp thì AC-18 vẫn đúng vì đọc trường, không chép số trang vào code.
- Redact tr.113/tr.166 có làm được bằng cách xoá lớp chữ không — chưa thử, việc của S3.
- AC-37 không có phép kiểm máy đủ mạnh; phụ thuộc hoàn toàn vào người đọc.
- AC-56: `observability.enabled = false` có tắt hết mọi log không — Data mới đọc docs, chưa thử (TRACKING-PLAN §7).
- AC-59: giấy phép thư mục `standard_fonts`, `cmaps` của PDF.js chưa đọc; Reserved Font Name của ba họ font chưa đọc.
- AC-60: `vibe-check [4]` hiện chỉ quét âm thanh — cho tới khi sửa, AC-59 và AC-38 phần asset chỉ có người kiểm.
- AC-62: `from_start` đọc bài 1 ở Safari rồi bài 5 ở WebView Zalo ⇒ `false` (storage tách) ⇒ số chặt xẹp ở nhóm đó; cỡ chưa đo (Q-24). Chính lần bắn bài 1 luôn mang `from_start=true` (TRACKING-PLAN §2.5).
- AC-18: số đo mẫu ③ (132/1004 trang, 7/7 trang đã biết, ~41 trang oan) là của Legal (LEGAL-REVIEW §A.2), PM chưa chạy lại.
- AC-86: câu W2 đúng chữ nhưng người đọc có hiểu "agent AI soát" là không có người chuyên môn không — chưa đo; Luật AI 134/2025 (L14) chưa đọc văn bản gốc.
- AC-57: câu R25 mới chưa đối chiếu Luật 91 (L18) — workflow L18 chạy trước S5 (QĐ 51).
- QĐ 41–51 nhận theo lô trước khi Duy đọc từng bảng phương án (PRODUCT-BRIEF.md:179); AC áp đúng chữ khuyến nghị.
- AC-73: "mở tại chỗ" (QĐ 17) chưa thử trong WebView Zalo; buổi 5 người so với "thẻ phủ lên chữ".
- AC-74: bật thật rồi kiểm, hay kiểm trên bản xem trước có bộ đếm riêng (AC-68 bắt cùng origin) — SWE chọn ở S3.
- AC-76: ngưỡng N giờ của "phiên" chưa có; Zalo có mở mỗi link trong WebView mới không — chưa đo.
- AC-45: danh sách tên riêng để lint chưa trích; lint không bắt được bản dịch sát đã đổi hết tên riêng (Legal §A.1).
- AC-61: hộp thư riêng có làm lộ danh tính qua header, WHOIS, tên hiển thị không — chưa kiểm (Legal §Chưa xác minh). Thời hạn gỡ theo NĐ 17/2023 Đ.114 chưa xác minh; nếu luật đặt hạn ngắn hơn (b) thì luật thắng.
- AC-67: event mất lúc offline (QĐ 26, không hàng đợi) làm M1 lệch bao nhiêu — chưa đo.
- AC-72: danh sách cụm cấm + ngoại lệ chưa có; bản WRITER §1 hiện là danh sách từ.
- File này đã qua review kiểm chéo gói S1 sau QĐ 38–51 (2026-11-07). Same vendor, same priors — no external verifier ran.

## T2 — câu hỏi chéo-phòng

Data (2 câu) và Design (2 câu) hỏi PRD + ACCEPTANCE ngày 2026-10-24. Câu hỏi nguyên văn, trả lời và lý do: **`PRD.md` §T2** — một chỗ, không chép hai nơi.
File này đã sửa: thêm §L (AC-74…AC-78) · trạng thái AC-69, AC-70, AC-73 · §Phủ TRACKING-PLAN · §Thay đổi · §Chưa xác minh · TL;DR.
Same vendor, same priors — no external verifier ran.

## Đổi ở vòng sửa 2026-10-24

Theo review S1 vòng 1 (falsify + consistency). PM sửa tại chỗ vì file là nháp chưa duyệt; các thay đổi nghĩa AC cũng có dòng ở §Thay đổi. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Vì sao |
|---|---|---|
| TL;DR | Bỏ "phủ đủ R1–R34"; ghi rõ R5, R11, R33 (a)(b), R26, R32, R34 còn hở. Đếm lại BLOCKED/TBD bằng script: 5 + 9 BLOCKED, 3 + 8 TBD, 4 xung đột | Bản cũ ghi 6 BLOCKED một phần (thật là 8, nay 9 vì AC-61) và thiếu AC-61, AC-73 trong TBD; R5, R33 chưa phủ |
| AC-45 | Thêm `based_on` bắt buộc, kiểm `asset`/`pages`, lint tên riêng; cột Người hẹp lại | Việc Legal giao (LEGAL-REVIEW §T2 giao việc, §A.1) |
| AC-61 | Phủ đủ R33 (a)–(d); (a) BLOCKED — chờ hợp đồng Ringkas; (a), (b) → Duy (Q-xx) | Việc Legal giao; R33 PASS = (a)–(d) |
| AC-15 · AC-16 · AC-19 · AC-77 | Trạng thái phần card Hermanson: "Sẵn" → XUNG ĐỘT chưa giải, → Duy (Q-xx), PRD X6 | Nguồn EN vs card VN · USD vs đ · trang PDF vs `sectionId` |
| AC-30 | "Sẵn" → TBD, → Duy (Q-xx); AC-63 ghi tập bài bị đánh dấu chờ định nghĩa | "Tự khai giai đoạn" chưa định nghĩa |
| AC-36 | Phạm vi ở S5 hẹp như AC-69/AC-70 (dòng ở §Thay đổi) | Va AC-74 ở S5 |
| AC-42 | "bài lối vào có con số" → "card lối vào có con số", phạm vi kế toán đúng QĐ 8 | QĐ 8: GĐ01 · GĐ05 · card có con số |
| AC-53 | Dòng hiển thị AI → Duy (Q-xx) | R20 gray; tên Duy công khai khi R34 BLOCKED |
| AC-67 | Hàng đợi offline trong JSON tiến độ → Duy (Q-xx), không tự thêm vào schema | QĐ 7: schema là hợp đồng, cùng loại `tel` |
| AC-72 | Kiểm theo cụm trên chữ hiển thị, có ngoại lệ, tự kiểm bằng câu mẫu đúng | Bản cũ tự mâu thuẫn |
| AC-76 | Trường thời điểm "phiên" → Duy (Q-xx) | QĐ 7 |
| §Phủ LEGAL-REVIEW · §Chưa xác minh | Cập nhật R5, R33; thêm 4 dòng chưa xác minh | Khớp các sửa trên |

## Đổi theo QĐ 17–35 (2026-10-24)

PM sửa tại chỗ vì file là nháp chưa duyệt; mọi thay đổi nghĩa AC cũng có dòng ở §Thay đổi (nhãn "QĐ 17–35"). Frontmatter `status`/`blocked_on` giữ nguyên — ba điều kiện của Duy chưa xong. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| TL;DR | Đếm lại bằng script trên cột Ai và Trạng thái: 83 AC; 0 TBD hẳn; 0 xung đột; thêm danh sách → Duy | — |
| AC-03 | Kế toán soát thêm `sectionId` nguồn của card có số | 30 |
| AC-05 · AC-06 · AC-13 | "Trộn" = câu + chữ giao diện; EN trên trang VI hợp lệ khi `keep_en`; ngoại lệ khác → Duy (PRD N2) | 20 |
| AC-10 · AC-82 | Không auto-redirect theo ngôn ngữ | 18 |
| AC-11 · AC-12 | Lần đầu mỗi H2; `keep_en` FAIL, VN danh sách gốc cảnh báo | 19 · 21 |
| AC-14 · AC-15 · AC-16 · AC-19 · AC-77 | Card Hermanson khái niệm; hết "XUNG ĐỘT chưa giải" | 27 |
| AC-18 · AC-45 | Cả cuốn trừ đoạn loại + luật dấu hiệu trang; hết "TBD — chờ X2" | 28 |
| AC-23 · AC-26 · AC-42 · AC-65 · AC-70 · AC-74 · AC-79 | Phần sách vào cổng ra mắt; file riêng chặn ra mắt; đo ra không chạy → Duy (PRD N3) | 29 |
| AC-20 · AC-29 · AC-58 · AC-66 · AC-67 · AC-76 | `tel` theo sao lưu, thời điểm không theo; bỏ hàng đợi offline; hết "→ Duy (Q-xx)" | 26 |
| AC-30 · AC-63 | Tự khai theo giai đoạn; hết TBD | 23 |
| AC-31 · AC-62 · AC-64 · AC-66 | Bỏ `lang`; `method` ∈ {`link`,`code`}; thẻ lật không bắn | 25 |
| AC-62 · AC-75 | "Xong" = ≥ 1 card; AC-75 hết TBD; thẻ lật → Duy (PRD N1) | 24 |
| AC-39 · AC-78 | Tagline T1 nguyên chuỗi | 22 |
| AC-51 · AC-52 | 0 chữ trích luật ở phần ra mắt; hết "Ngưỡng TBD" | 33 |
| AC-53 | Cờ `ai_assisted`; hạt "mục" → Duy (PRD N5); định danh BLOCKED — chờ hợp đồng Ringkas | 34 |
| AC-61 | Hộp thư riêng + "gỡ tạm trong 72 giờ"; hết "→ Duy, X8"; công khai BLOCKED — chờ hợp đồng Ringkas | 35 |
| AC-73 | Mở tại chỗ trong luồng, không lớp phủ | 17 · 19 |
| AC-80 · AC-81 · AC-83 | Thêm: dashboard ẩn n < 5 · giữ ID mồ côi · cảnh báo `persist()` (ra mắt hay không → Duy, PRD N4) | 32 · 18 |
| §I · §J · §Phủ · §Giới hạn · §Chưa xác minh | Cập nhật theo các dòng trên (R11, R26 → Q-20, R32 N/A, R33) | — |

**→ Duy mới từ file này** (chi tiết ở `PRD.md` §Open Questions): N1 thẻ lật · N2 ngoại lệ AC-05 · N3 `input type=file` không chạy trong Zalo · N4 cảnh báo `persist()` có phải điều kiện ra mắt · N5 hạt của `ai_assisted`.

## Đổi vòng sửa 2 (2026-10-24)

Theo review S1 sau QĐ 17–35 (BLOCKER M2, M3, M8, §4 (a)(b)(c); NONBLOCKING QĐ 29, 31, 32, 34, M6) và PRODUCT-BRIEF **QĐ 36, 37**. PM sửa tại chỗ vì file là nháp chưa duyệt; mọi đổi nghĩa AC có dòng ở §Thay đổi (nhãn "vòng sửa 2"). Frontmatter `status`/`blocked_on` **giữ nguyên** — điều kiện 3 đã lỗi thời theo QĐ 36, đổi hay không: → Duy (PRD N8). Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Nguồn |
|---|---|---|
| Đầu file · cột Ai | Ghi QĐ 36 thay điều kiện 3; agent không phải MÁY, không phải NGƯỜI — cột Ai tính theo người ký | QĐ 36 · M8 |
| AC-03 · AC-04 · AC-12 · AC-42 | "Người kế toán" → agent `ke-toan-reviewer` soát, Duy ký; AC-04 PASS chỉ trên Phụ lục II chính thức; hết "chờ tên kế toán" | QĐ 36 · 37 · M8 |
| AC-21 | Viết lại: tách soát (agent, ghi đúng tên) / ký (chỉ người); dạng "soát: agent `ke-toan-reviewer` · ký: Duy". Chữ công khai → Duy (X13, W2) | QĐ 36 · M8 · §4 (b) |
| AC-18 | Nguồn (i) = danh sách trang `exclusions` của `licences.json` (Legal vòng sửa 2, có tr.113); bỏ "thêm dấu hiệu là tự do" ⇒ mở rộng mẫu → Duy (X11) | M3 · §4 (c) |
| AC-23 · AC-79 | Quy tắc Legal bảng số liệu đã ra; B3 → Duy (X10); thêm xem bằng mắt trang có bảng số tiền; AC-79 thêm AC-46, AC-59 | M2 · QĐ 29 |
| AC-53 | Bản EN do Claude dịch ⇒ `ai_assisted = true` (hệ quả QĐ 6 + 34) | QĐ 34 |
| AC-57 | Trạng thái: câu R25 sai khi hộp thư lên trang → Duy (X12, gộp Q-20) | §4 (a) |
| §N mới · AC-84 · AC-85 | Thêm AC cho Legal R35 (QĐ 31) và R37 (dữ liệu người khiếu nại); R36 trỏ AC-80 | QĐ 31 · 32 · Legal vòng sửa 2 |
| TL;DR · §Phủ (Legal + TRACKING) · §Giới hạn · §Chưa xác minh | R1–R34 → R1–R37; đếm lại bằng script: 85 AC (55 · 19 · 11), 5 + 12 BLOCKED, 0 + 4 TBD, 15 AC có phần → Duy; thêm giới hạn "agent cùng vendor" và "tên TK chưa có bản chính thức" | M6 · QĐ 36 · 37 |

**→ Duy mới từ file này** (chi tiết ở `PRD.md` §Open Questions): **N7** phán nào của agent cho Duy ký · **N8** đổi điều kiện 3 của `blocked_on` theo QĐ 36.

## Đổi theo QĐ 38–51 (2026-10-25)

PM sửa tại chỗ vì file là nháp chưa duyệt; mọi đổi nghĩa AC có dòng ở §Thay đổi (nhãn "QĐ 38–51"). Frontmatter `status`/`blocked_on` **giữ nguyên** — 3 điều kiện của Duy chưa xong. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| Đầu file · TL;DR | Bỏ ghi chú "→ Duy (PRD N8)" lỗi thời (frontmatter đã theo QĐ 36 — B-16); đếm lại bằng script; cổng ra mắt = AC-42 + AC-79 + AC-83 | 36 · 45 |
| AC-03 · AC-04 | Luật ký trên phán agent | 40 |
| AC-05 · AC-06 · AC-13 | Ngoại lệ "không trộn"; dòng "chưa có bản EN" song ngữ; `ledger` không `keep_en` | 43 · 44 |
| AC-18 · AC-19 · AC-23 · AC-79 | Mẫu ③ + tự kiểm 7/7; B3 loại hẳn khỏi máy sinh card nhưng giữ trong host; B2 che; card trỏ bất kỳ bài có `based_on` | 46 · 47 · 48 |
| AC-21 · AC-53 · **AC-86 (mới, §O)** | Hai trường soát/ký; hạt `ai_assisted`; dòng soát công khai + cấm 4 chữ | 41 · 42 |
| AC-26 · AC-79 · AC-84 | N3 → ĐK-1; "→ Duy" của R35 → ĐK-2 (câu có điều kiện, không phải QĐ mới) | — |
| AC-42 · AC-83 | `persist()` vào cổng ra mắt | 45 |
| AC-57 · AC-85 | Câu R25 mới nguyên văn; xoá thư khi khiếu nại đóng | 49 |
| AC-62 · AC-69 · AC-75 | `from_start`; M1 chặt/lỏng; ≥ 1 card trắc nghiệm, thẻ lật không tính | 38 · 39 |
| §Phủ · §Giới hạn · §Chưa xác minh | R11, R20, R22, R25, R26, R37; event `from_start`; giới hạn mẫu ③ và dòng soát; giới hạn nhận theo lô | 39 · 41 · 47 · 49 · 51 |

**Không làm:** frontmatter · AC riêng cho workflow pháp lý L13 + L18 trước S5 (QĐ 51) — đặt ở cổng S5 của `PRD.md` §Delivery Milestones, theo việc được giao · chữ "→ Duy" trong các mục lịch sử (§Thay đổi, §Đổi …).
