---
status: pass
stage: 04-qa
date: 2026-11-09
owner: qa
blocked_on: []
---

# REVIEW — Báo Cáo Kiểm Toán Độc Lập Mã Nguồn, An Ninh & Trải Nghiệm (`S4 QA` — `where-money-sleeps`)

> **Verdict sau vòng sửa `S4 QA`:** **`PASS` — Đã phát hiện và xử lý triệt để 5 điểm vênh hợp đồng (`P1-A..P1-E`) do phiên kiểm toán độc lập (`subagent c5f36e90-35d7-4ae5-b886-c52133e8e483`) chỉ ra; toàn bộ 5/5 cổng `wms-check.sh` và 4/4 cụm E2E `wms-qa-verify.py` đạt `PASS` (`0` lỗi chặn).**
> *Nhãn quan hệ model (Quy tắc 7):* `same vendor, same priors — no external verifier ran`.

## 1. Nhật Ký 5 Phát Hiện Độc Lập (`c5f36e90-35d7-4ae5-b886-c52133e8e483`) & Biên Bản Khắc Phục Tại Chỗ

| Mã phát hiện | Nội dung phát hiện của Kiểm toán viên độc lập | Cách khắc phục đã áp dụng trên đĩa | Trạng thái sau sửa |
|---|---|---|---|
| **`[P1-A]`** | `scripts/wms-qa-verify.py` và `gates/03-build/SLICE-LOG.md` ghi đường dẫn cũ `docs/assets/figures/fig-...` thay vì đường dẫn thật `public/brand/{card,pay,install}-fig-{1..4}.jpg` | Đồng bộ đường dẫn `public/brand/{sid}-fig-{1..4}.jpg` trong cả `scripts/wms-qa-verify.py` và `gates/03-build/SLICE-LOG.md` | **`FIXED & VERIFIED`** |
| **`[P1-B]`** | 6 thẻ trắc nghiệm trong `WMS_QUIZ_BANK` thiếu `source_quote`, `sectionId`, `reviewed_by: "Duy"`, `accountant_agent: "ke-toan-reviewer"` (`AC-14, 19, 21`); schema tiến độ thiếu `schema: 1`, `lastActive` (`AC-29`); thiếu hàm & nút `selfDeclareEntryStage()` (`AC-30`) | Bổ sung trọn bộ trường hợp đồng vào 6 thẻ `WMS_QUIZ_BANK`, thêm liên kết `"Đọc lại đoạn này ↑"` nhảy tới `#sectionId`, nâng cấp `defaultWmsProgress()` có `schema: 1` + `lastActive`, và thêm nút/hàm `selfDeclareEntryStage()` trong `docs/prototype.html` | **`FIXED & VERIFIED`** |
| **`[P1-C]`** | `emitWmsTelemetry()` gọi `navigator.sendBeacon("/api/event")` vi phạm `AC-68` và `TRACKING-PLAN.md` §3 (danh sách cấm EasyPrivacy) | Đổi sang đường dẫn trung tính `navigator.sendBeacon("/api/p", blob)` trong `docs/prototype.html` + `SLICE-LOG.md`, và thêm assert tự động chặn mọi URL trong danh sách đen EasyPrivacy vào `scripts/wms-qa-verify.py` | **`FIXED & VERIFIED`** |
| **`[P1-D]`** | Cờ `from_start` trong `lesson_completed` đọc từ `WMS_PROG.completed["card"]` thay vì `WMS_PROG.tel.lesson_completed["card"]` theo `TRACKING-PLAN.md` §2.5 (`AC-62`) | Sửa `answerQuizCard()` trong `docs/prototype.html` tính `hadLesson1 = (storyKey === "card" || !!WMS_PROG.tel.lesson_completed["card"])` | **`FIXED & VERIFIED`** |
| **`[P1-E]`** | Đường dẫn tương đối tới bảng định tuyến trong `gates/04-qa/UNDERSTOOD.md` lệch 1 cấp thư mục; ghi nhận `<link>` font Google trên trang tĩnh chờ nội bộ hoá khi đóng gói sản phẩm chính thức | Sửa đường dẫn trong `gates/04-qa/UNDERSTOOD.md` (`vibe-check.sh [5]` đạt `0` đường dẫn chết); ghi nhận hạng mục self-host `.woff2` vào danh sách kiểm trước `S5 Launch` | **`FIXED & VERIFIED`** |

## 2. Đánh Giá Bảo Mật, Khả Năng Tiếp Cận (`a11y`) & Chất Lượng Video `v6.5`

- **An ninh bàn duyệt `docs/studio.html`:** Khung bảo mật `<meta http-equiv="Content-Security-Policy">` khoá cứng `connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'`; chính sách `trustedTypes.createPolicy("wms-studio-policy")` cùng hàm `esc()` và `textContent` bảo vệ chống XSS khi nạp phụ đề `.srt` và kịch bản.
- **Khả năng tiếp cận (`a11y`) & Chuyển động (`bang-motion` `M1–M4`):** Cả 3 bề mặt (`prototype.html`, `studio.html`, `workflows.html`) tôn trọng `@media (prefers-reduced-motion: reduce)`, có đầy đủ `aria-live="polite"`, điều hướng bàn phím `⌘K` / phím mũi tên, và đồng hồ tất định `window.__vibeSeek`.
- **Chất lượng 6 Video Calm Editorial Motion `v6.5`:** Cả 6 file MP4 (`30fps`, `-14 LUFS`) và 6 file `.srt` trên `@WhereMoneySleeps` (`unlisted`) giữ nguyên bố cục sạch của `v6.0` đồng thời hiển thị rõ hoạt cảnh 2,2s–4,4s (thanh tỷ lệ tách đôi, 12 cột kỳ hạn và 30 ô CASA sáng tuần tự, hạt sáng dẫn lưu `3,6s` và số nhảy `tabular-nums`).

## 3. Chưa xác minh được

- Kiểm thử mở link `#sync` trong WebView Zalo trên iPhone/Android vật lý (`AC-31`), kiểm tra hợp đồng lao động Ringkas của Duy (`R34`), và self-host file font `.woff2` + PDF Hermanson tr.1–197 trước khi mở cổng `S5 Launch`.
- Same vendor, same priors — no external verifier ran.
