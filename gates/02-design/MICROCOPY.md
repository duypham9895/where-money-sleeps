---
status: pass
stage: 02-design
date: 2026-11-15
owner: writer
blocked_on: []
---

# MICROCOPY — Hợp đồng Chữ trên Giao diện, Hình minh hoạ & Video (`Where Money Sleeps`)

> Phòng Writer + Design + PM đồng sở hữu. Toàn bộ chuỗi chữ trong `docs/prototype.html` và `docs/workflows.html` đều là **microcopy tiếng Việt thật**, không dùng *lorem ipsum* (QĐ 59 PIPELINE Log 2026-10-24).

## 1. Bốn luật chữ bất khả xâm phạm (`QĐ 55` · `LUẬT 4` · `LUẬT 7` · `VOICE-AND-PROSODY-SPEC`)

| Luật | Cấm tuyệt đối | Bắt buộc dùng thay thế | Kiểm bằng |
|---|---|---|---|
| **QĐ 55 — Khử chữ `"sổ cái"`** | Không xuất hiện cụm từ `"sổ cái"` ở bất kỳ nhãn UI, tagline hay bài viết nào (tránh gây nhầm sang tiền mã hoá / blockchain) | • Điều hướng kho bài: **`"Mục lục"`**<br>• Góc nhìn kế toán: **`"Sổ kế toán (TT 99/2025)"`**<br>• Bản chất ngân hàng: **`"sổ sách ngân hàng"`** | Quét Unicode NFC trong `scripts/check-story.py` |
| **LUẬT 4 — Không Tên Riêng (`B1–B4`)** | Cấm mọi tên ngân hàng, mạng thẻ, ví điện tử, cửa hàng, tác giả sách hoặc công cụ AI hậu trường (`Visa`, `Mastercard`, `NAPAS`, `VietQR`, `MoMo`, `ElevenLabs`, `Google`, `Veo`, `Hermanson`, `Quán Nhà Liên`...) trong bài học và khung hình video | Dùng 5 danh từ chung hệ thống:<br>• `Bạn / Người mua / Người lao động`<br>• `Cửa hàng / Quán quen / Doanh nghiệp`<br>• `Ngân hàng của quán / Ngân hàng công ty`<br>• `Tổ chức thẻ / Hệ thống chuyển mạch liên ngân hàng`<br>• `Ngân hàng của bạn / Công ty tài chính` | `scripts/check-story.py` (`C9 BRAND_RE`) + `brand-safety-reviewer` |
| **LUẬT 7 — Không Lộ Ẩn Dụ Đạo Cụ** | Cấm viết các câu chỉ đạo sân khấu như `"Nhìn lên dây điện trên cao"`, `"ống ngầm mới sáng đèn"`, `"dây tín hiệu"`, `"ống quyết toán"` trong lời bình, phụ đề và văn bản đọc | Dùng ngôn ngữ nghiệp vụ tài chính tự nhiên: **`"luồng hồ sơ & hợp đồng"`**, **`"luồng thông tin xét duyệt"`**, **`"giải ngân qua ngân hàng"`**, **`"luồng quyết toán liên ngân hàng"`** | `scripts/wms-media-pipeline.py` (`FORBIDDEN_STAGE_PROP_RE`) |
| **Tiêu đề 3 Điểm Neo & Giọng đọc Sóng** | Cấm tiêu đề cụt thiếu mốc tiền gốc (`"0% nhưng cửa hàng chỉ nhận 11,4 triệu"`) và cấm đuôi câu cụt `", ví dụ."` ở cuối câu lời bình | Tiêu đề đủ 3 vế: **`[1. Hành động + Giá gốc] → [2. Cơ chế bề mặt] → [3. Sự thật hệ thống / số thực nhận]`**; mở đầu giả định tự nhiên bằng `"Giả sử..."` / `"Trong ví dụ này..."` | `scripts/check-story.py` (`C9`) |

## 2. Từ điển Microcopy trên các bề mặt chính (`docs/prototype.html`)

| Vị trí giao diện | Chuỗi chữ chuẩn tiếng Việt | Chuỗi chữ chuẩn tiếng Anh (`EN`) | Ghi chú ngữ cảnh |
|---|---|---|---|
| **Tagline bắt buộc (QĐ 22 + QĐ 55)** | *"Từ tin báo “ghi có” tới sổ sách ngân hàng: tiền của bạn đi qua những đâu."* | *"From the bank alert to the bank's books: where your money actually goes."* | Luôn đi kèm tên `Where Money Sleeps` để không bị hiểu nhầm thành trang gửi tiết kiệm |
| **Thanh điều hướng `1A` (`48px`)** | • Giữa: `Danh mục {k}/{N}: {Tên} ▾` │ `Bài {m}/{M}: {Tiêu đề ngắn} ▾`<br>• Phải: `⌕ Mục lục & Tìm ⌘K` · `Chế độ duyệt bài` | • Center: `Category {k}/{N}: {Name} ▾` │ `Story {m}/{M}: {Short title} ▾`<br>• Right: `⌕ Index & Search ⌘K` · `VI ⇄ EN` | Gọn trong 1 hàng duy nhất, không dùng icon hamburger cạnh logo |
| **Nút gạt 2 góc nhìn (`Dual-Lens`)** | • `👤 Góc nhìn Cá nhân (Túi tiền & Phí ngầm)`<br>• `⚙️ Sổ kế toán (Bút toán TT 99/2025)` | • `👤 Personal Lens (Wallet & Hidden Fees)`<br>• `⚙️ Accounting Ledger (Circular 99/2025)` | Đặt ngay trên thanh điều khiển nhịp của Mặt cắt Diorama |
| **3 ô số tổng kết trên Diorama** | • Ô 1: `Số tiền giao dịch gốc`<br>• Ô 2: `Phí / Khấu trừ phát sinh`<br>• Ô 3: `Số tiền thực nhận cuối cùng` | • Box 1: `Original transaction amount`<br>• Box 2: `Fees / Deductions withheld`<br>• Box 3: `Final net amount settled` | Số nhảy bằng `animateMoneyText()` với `tabular-nums`; con số giả định gắn nhãn `<span class="ex">ví dụ / example</span>` |
| **Chú thích 3 tầng của Hình mặt cắt `16:9` (`LUẬT 9`)** | • Tầng 1 (`kicker` + nút nhảy): `HÌNH MẶT CẮT 0{i}/04 · CHƯƠNG 0{c}` + `↗ Xem trên Mặt cắt Diorama · Nhịp {b}/5`<br>• Tầng 2 (`title`): Câu kết luận hành động đầy đủ (Action Thesis Title)<br>• Tầng 3 (`desc`): 2 câu giải thích cơ chế có gắn thuật ngữ `[[nhãn\|khoá]]` | • Layer 1 (`kicker` + jump button): `CUTAWAY FIGURE 0{i}/04 · CHAPTER 0{c}` + `↗ Jump to Diorama · Beat {b}/5`<br>• Layer 2 (`title`): Complete Action Thesis Title<br>• Layer 3 (`desc`): 2-sentence mechanism takeaway with `[[label\|key]]` glossary links | Giúp người đọc quét lướt (*F-pattern*) chỉ đọc chú thích hình cũng nắm được 80% cốt lõi chương |
| **3 Tab nội dung sâu dưới sân khấu** | • Tab A: `A · Bài khảo cứu toàn cảnh (Dành cho mọi người)`<br>• Tab B: `B · Phân tích chuyên sâu & Sổ kế toán TT 99/2025`<br>• Tab C: `C · Studio Kịch bản & Video (YouTube 16:9 & Shorts 9:16)` | • Tab A: `A · Everyday Deep Dive (For everyone)`<br>• Tab B: `B · System Mechanics & Accounting Books (Circular 99/2025)`<br>• Tab C: `C · Video Script Studio (YouTube 16:9 & Shorts 9:16)` | Phân tầng rõ ràng để người mới không bị ngợp bởi bảng định khoản kế toán |
| **Dòng minh bạch AI & Kiểm duyệt (QĐ 41 · Legal R20 · AC-52)** | *"Soạn với hỗ trợ AI · Con số và tên tài khoản được một agent AI soát (`K1–K4 · F1–F4 · B1–B4 · M1–M4`); {approvedBy} ký duyệt."* | *"Drafted with AI assistance · Figures and account names checked by an AI agent (`K1–K4 · F1–F4 · B1–B4 · M1–M4`); signed off by {approvedBy}." + *"This is an unofficial summary of Circular 99/2025/TT-BTC."* | **Cấm tuyệt đối 4 từ** `"kế toán"`, `"accountant"`, `"chuyên gia"`, `"expert"` trong dòng minh bạch công khai và trường `reviewed_by` (QĐ 41 · Legal R20) |

## 3. Trạng thái Song ngữ (`QĐ 62` · `LUẬT 11`, 2026-11-15)

- Áp dụng song ngữ toàn diện `VI ⇄ EN` cho toàn bộ 7/7 bài `published` (`card`, `pay`, `install`, `minpay`, `qr`, `profitcash`, `offus`), 52 mục `GLOSS`, 7 danh mục / 19 chủ đề `CATEGORIES`, 28 hình `CHAP_FIGS`, 14 câu trắc nghiệm `WMS_QUIZ_BANK`, 7 máy tính tương tác, `Scene` SVG, `studio.html`, `workflows.html` và toàn bộ trang `docs/*.html`.
- Cross-vendor model review — no human external verifier ran.
