---
status: pass
stage: 04-qa
date: 2026-11-09
owner: qa
blocked_on: []
---

# VERIFICATION — Báo Cáo Xác Minh Tất Định & Tiêu Chí Chấp Nhận (`S4 QA` — `where-money-sleeps`)

> **Verdict tổng thể:** **`PASS` (5/5 cổng `scripts/wms-check.sh` + 5/5 cụm kiểm thử E2E `scripts/wms-qa-verify.py` đạt 100%, `0` lỗi chặn).**
> *Nhãn định tuyến & kiểm duyệt (Quy tắc 7 & 16):* `[Route: T3 · S=5/8 · Primary=Claude Opus 5.5 · CrossCheck=Gemini 4 Argon High]` · `same vendor, same priors — no external verifier ran`.

## 1. Kết Quả 5 Cổng Kiểm Tất Định (`scripts/wms-check.sh`) & E2E (`scripts/wms-qa-verify.py`)

| # | Cổng kiểm / Công cụ | Phạm vi xác minh | Kết quả đo thật |
|---|---|---|---|
| **1** | `scripts/check-story.py` (`C0–C9`) | Schema 3 bài mẫu (`card`, `pay`, `install`), cân bằng bút toán kép `Σ Debit = Σ Credit`, đối chiếu TT 99/2025, 0 từ cấm `B1–B4`, đủ 3 trụ `C9 v2` (`article.lay`, `article.pro`, `videoScript.long/short`), 26/26 file quản trị đồng bộ `C8` | **`PASS` (`PASS 28 · FAIL 0`)** |
| **2** | `scripts/wms-finance-kb.py --verify` (`F1–F4`) | Cơ chế ngân hàng (`T+0 Auth` vs `T+2 Settlement`, `On-Us` vs `Off-Us`, `CASA`, `FTP`), toán tài chính `IRR/EIR` (`11,4 triệu` nhận trước vs `12 × 1 triệu` ⇒ `IRR tháng = 0,7981%`, `EIR năm = 10,01%`), kho tri thức `knowledge/finance-kb.json` | **`PASS` (`12/12 PASS · FAIL 0`)** |
| **3** | `scripts/wms-motion-snap.py` (`M0–M4` & `LUẬT 6b, 8, 9, 10`) | Bố cục mặt cắt Diorama v3.0, 12 hình khảo cứu `16:9` (`1200×675`, `CLS = 0`), đồng hồ tất định `window.__vibeSeek`, `0` cặp chữ đè nhau (`M3b`), `0` script CDN bên thứ ba lúc runtime | **`PASS` (`21/21 PASS · FAIL 0`)** |
| **4** | `scripts/wms-studio-sync.py --check` | Đồng bộ hàm băm SHA-256 giữa `docs/prototype.html`, 6 file MP4 `v6.5`, 6 file phụ đề `.srt` và `docs/wms-studio-data.js` (`hash=fe50a0cfdedbb726`) | **`PASS` (`hash=fe50a0cfdedbb726`)** |
| **5** | `scripts/wms-qa-verify.py` (`QA-1..QA-5`) | Kiểm thử E2E tất định trên `docs/prototype.html`, `docs/studio.html`, `docs/workflows.html`, `docs/s6.html`, `docs/assets/doc.css` (`WMS_QUIZ_BANK`, máy trạng thái `tel` `R1–R6` + `F4` + `AC-68`, CSP `connect-src 'none'`, `14` mã `youtubeId`, và `LUẬT 13 R1–R5` ở `320·390·768·1440px`) | **`PASS` (`5/5 cụm PASS · 4/4 Playwright viewports · 0 lỗi chặn`)** |

## 2. Bảng Đối Chiếu Hợp Đồng `gates/01-spec/ACCEPTANCE.md`

| Cụm AC (`ACCEPTANCE.md`) | Hạng mục kiểm chứng | Bằng chứng trên đĩa & Trạng thái S4 |
|---|---|---|
| **A. Duyệt & Đăng (`AC-01..AC-04`)** | Không bài/card/video nào ở trạng thái công khai khi chưa có chữ ký duyệt của Duy; 6 video trên `@WhereMoneySleeps` đều khoá ở `privacyStatus: "unlisted"` (`embedStatus: "uploaded_unlisted"`); 6 card trắc nghiệm có `reviewed_by: "Duy"` và `accountant_agent: "ke-toan-reviewer"` | **`PASS` phần cơ chế khoá nháp (`AC-01, AC-02, AC-21`)** · *Chờ Duy ký duyệt xuất bản công khai & Phụ lục II TT 99/2025 chính thức cho GĐ01 trước `S5 Launch` (`AC-03, AC-04`)* |
| **B–D. Ngôn ngữ, Glossary & Thẻ Trắc nghiệm (`AC-05..AC-21`)** | 100% thuật ngữ có thẻ chú thích tại chỗ (`GLOSS`), 6 thẻ trắc nghiệm (`card-q1.v1..install-q2.v1`) trong `WMS_QUIZ_BANK` có đủ `source_quote`, `sectionId`, phản hồi tức thì và liên kết `"Đọc lại đoạn này ↑"` | **`PASS` (`QA-1 PASS`)** |
| **F. Tiến độ cục bộ, Tự khai & Sao lưu `#sync` (`AC-29..AC-32`)** | Bản ghi `wms.progress.v1` có `schema: 1`, `completed`, `cards`, `pdfPage`, `lang`, `selfDeclared`, `persisted`, `lastActive`, `tel` (`AC-29`); nút tự khai giai đoạn Mở đầu trong `≤ 2` chạm (`selfDeclareEntryStage()`, `AC-30`); tạo/khôi phục `#sync` chỉ nằm sau dấu `#` và không gửi `lastActive` (`AC-31`, `QĐ 26`) | **`PASS` trên máy tính & Node VM (`QA-2 PASS`)** · *Chờ đo WebView Zalo trên iPhone/Android thật trước `S5 Launch` (`AC-31, AC-32`)* |
| **G. Đo lường & Quyền riêng tư (`AC-33..AC-36`, `AC-62`, `AC-68`)** | `0` `<script>` bên thứ ba trên cả 3 ứng dụng; `studio.html` khoá `connect-src 'none'`; `emitWmsTelemetry()` gửi qua đường dẫn trung tính `/api/p` (tránh danh sách cấm EasyPrivacy `/api/event` theo `AC-68`); tính `from_start` từ `tel.lesson_completed["card"]` (`AC-62`) | **`PASS` (`QA-2 & QA-3 PASS`)** |
| **H–I. Nội dung, Pháp lý & 6 Video `v6.5` (`AC-37..AC-48`, `QĐ 56–61`)** | `0` mã chứng khoán / khuyến nghị đầu tư / tên thương hiệu thật (`B1–B4`); tagline bắt buộc đi kèm tên trang (`AC-39`); đủ 6 video Calm Editorial Motion `v6.5` (`30fps`, `-14 LUFS`, animation 2,2s–4,4s) + 6 file `.srt` đã tải lên `@WhereMoneySleeps` (`unlisted`) | **`PASS` (`QA-4 PASS`)** |

## 3. Hai Câu Hỏi Kiểm Chéo `T2` (Phòng Data & Phòng Legal hỏi — Phòng QA trả lời)

1. **Câu hỏi 1 (Phòng Data):** *"Khi chạy kiểm thử độc lập cổng `S4 QA`, phát hiện nào về đường dẫn beacon (`AC-68`) và công thức `from_start` (`AC-62`) đã được tìm thấy và xử lý dứt điểm?"*
   - **Trả lời (Phòng QA):** Kiểm toán viên độc lập (`c5f36e90-35d7-4ae5-b886-c52133e8e483`) phát hiện `docs/prototype.html` gọi `navigator.sendBeacon("/api/event")` (nằm trong danh sách cấm EasyPrivacy của `AC-68`) và đọc `WMS_PROG.completed["card"]` thay vì `WMS_PROG.tel.lesson_completed["card"]` (`AC-62`). Chúng tôi đã sửa ngay sang đường dẫn trung tính `/api/p`, chuẩn hoá `hadLesson1 = (storyKey === "card" || !!WMS_PROG.tel.lesson_completed["card"])`, bổ sung kiểm tra tự động `AC-68` vào `scripts/wms-qa-verify.py` và chạy lại đạt `PASS 100%`.
2. **Câu hỏi 2 (Phòng Legal):** *"Trên bàn duyệt `docs/studio.html` và bộ 6 video Calm Editorial Motion `v6.5`, cơ chế nào bảo đảm không rò rỉ dữ liệu ra ngoài và không còn lỗi tĩnh hay rối mắt?"*
   - **Trả lời (Phòng QA):** `docs/studio.html` khoá cứng `<meta http-equiv="Content-Security-Policy" content="... connect-src 'none'; object-src 'none'; form-action 'none'">` và dùng `trustedTypes` + `textContent`. Cả 6 video `v6.5` giữ nguyên bố cục sạch `v6.0` (90% tranh Risograph thông thoáng, `0` hộp chữ bay đè hình) đồng thời khôi phục hoạt cảnh 2,2s–4,4s (`ease_out_cubic`), hạt sáng dẫn lưu `3,6s` và đếm số `tabular-nums`, được xác nhận qua dải ảnh time-lapse và `ffprobe`.

## 4. Chưa xác minh được

- Phép đo thực địa trên điện thoại iPhone/Android thật (mở link `#sync` trong WebView Zalo xem có bị cắt `#fragment` không, và kiểm tra tách bộ nhớ Safari/WebApp theo `AC-31`, `AC-32`).
- Kiểm tra cấu hình Cloudflare Worker/D1 thực tế khi triển khai (`observability.enabled = false`, không chặn IP theo `R35`, ẩn ô `n < 5` theo `AC-69`) và điều khoản hợp đồng lao động Ringkas của Duy (`R34`) trước cổng `S5 Launch`.
- Same vendor, same priors — no external verifier ran.

## 5. Bổ Sung `2026-11-15` — Kiểm Định Responsive Mobile + Desktop (`LUẬT 13 · R1–R5` · `[QA-5]`)

- **Phạm vi nâng cấp:** `docs/prototype.html` (`== index.html`), `docs/studio.html`, `docs/workflows.html`, `docs/assets/doc.css` (`320×568`, `390×844` touch, `768×1024`, `1440×900`): `0px` tràn ngang (`overflow-x:clip`), chạm `>=44×44px` (`@media (pointer:coarse)`), ô nhập `>=16px`, header 1 hàng `<=12% dvh` tự ẩn khi cuộn xuống (`scroll-hide`), overlay giữ `100dvh` (`overscroll-behavior:contain`), sơ đồ `#wfSvg` cuộn ngang tối thiểu `720px` (chữ `>=10px`) kèm nhãn `#svgSwipeHint` `VI⇄EN`.
- **Chưa xác minh được trên phần cứng thật:** Phép đo cảm ứng trên Safari iOS / Chrome Android vật lý (hiện kiểm thử trên Chromium headless Playwright + giả lập touch `is_mobile=True`).
