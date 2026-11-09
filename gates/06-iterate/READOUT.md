---
status: pass
stage: 06-iterate
date: 2026-11-09
owner: Data
blocked_on: []
---

# READOUT — Sổ Đọc Số Liệu Thực Tế & Quyết Định Sản Phẩm (`S6 Iterate` — `where-money-sleeps`)

> **Quy tắc vận hành của Phòng Data (`../docs/departments.md` & `gates/01-spec/SUCCESS-CRITERIA.md`):** File này chỉ ghi thêm (`append-only`), mọi lần đọc số đều gắn ngày (`YYYY-MM-DD`). Dữ liệu bắn thử ở `S4 QA` trước ngày ra mắt công khai **không** được tính vào baseline (`TRACKING-PLAN.md` §3). Ngưỡng baseline `M1` chỉ được đặt sau **≥ 4 tuần** ra mắt công khai **và** bài 1 (`card`) đạt **≥ 100 lượt** `lesson_completed`.

## 1. Bảng Khung Đọc Số Liệu Hợp Đồng (`M1–M5` & YouTube `@WhereMoneySleeps`)

| Thước đo (`Metric`) | Công thức định nghĩa (`SUCCESS-CRITERIA.md`) | Câu hỏi quyết định (*Số là X thì làm gì, Y thì làm gì*) | Số đọc ngày `2026-11-09` (Trước khi mở `public`) |
|---|---|---|---|
| **`M1` · Tỉ lệ đi trọn lối vào (Chặt & Lỏng)** | **Chặt:** `lesson_completed(bài 5, from_start=true) / lesson_completed(bài 1 "card")` · **Lỏng:** `mọi bài 5 / bài 1` | Độc giả có đi từ bài đầu tới bài thứ 5 và chạm làm thử thẻ trắc nghiệm không? Nếu `M1` thấp ở một bài cụ thể ⇒ rút ngắn đoạn mở đầu hoặc tăng trực quan trên Mặt cắt Diorama của bài đó. | **`0 / 0` (Chưa mở `public`; chờ `≥ 4 tuần` & `bài 1 ≥ 100 lượt` để chốt baseline)** |
| **`M2` · Tỉ lệ hoàn thành từng bài (`card`, `pay`, `install`)** | Số lượt `lesson_completed{lesson}` theo ngày (ẩn ô `n < 5` theo `AC-69`) | Bài nào thu hút người đọc làm tới câu trắc nghiệm cuối bài nhiều nhất? Chủ đề nào cao ⇒ ưu tiên sản xuất tiếp các bài cùng danh mục ở `TRIAGE.md`. | **`0` lượt công khai** *(Cơ chế bắn `lesson_completed` qua `/api/p` đã PASS 100% ở `S4 QA`)* |
| **`M3` · Tỉ lệ trả lời đúng từng thẻ trắc nghiệm (`WMS_QUIZ_BANK`)** | `card_answered{card, correct=true} / Σ card_answered{card}` cho 6 thẻ `card-q1.v1..install-q2.v1` | Thẻ nào có tỉ lệ đúng `< 40%` (câu hỏi gây hiểu lầm hoặc đoạn bài giải thích chưa rõ)? Nếu `< 40%` sau `≥ 30` lượt ⇒ viết lại câu hỏi/đoạn giải thích và tăng phiên bản lên `.v2`. | **`0` lượt công khai** *(6 thẻ `.v1` đã gắn sẵn khoá phiên bản để tách lịch sử khi sửa)* |
| **`M5` · Tỉ lệ tạo & khôi phục sao lưu `#sync`** | `sync_created{method}` & `progress_restored{method}` (`link` vs `code`) | Người đọc dùng `link` hay `code` nhiều hơn? Nếu trên Zalo thực tế `progress_restored{method="link"} = 0` trong khi `sync_created{method="link"} > 0` ⇒ bằng chứng Zalo cắt `#fragment`, chuyển nút chính sang `method: "code"`. | **`0` lượt công khai** *(Cả 2 nút `link` và `code` đã hoạt động trên `docs/prototype.html`)* |
| **`YT-1` · Giữ chân khán giả trên `@WhereMoneySleeps` (`v6.5`)** | Thời lượng xem trung bình (`AVD`) & tỉ lệ xem hết (`APV`) của 3 video Dài `16:9` (`fxpFvVJcpRA`, `3NqEha4j53k`, `l_8aVo538jo`) và 3 Shorts `9:16` (`th6zR4gwV5c`, `XnMsbH0E_xo`, `J3DmDP4KKRI`) | Nhịp hoạt cảnh Calm Editorial Motion `v6.5` (`2,2s–4,4s`) giữ chân người xem ở cảnh nào tốt nhất và rơi ở giây nào? | **Đang ở chế độ `unlisted` (`6/6` video `v6.5` đã tải lên kênh `@WhereMoneySleeps`)** |

## 2. Nhật Ký Đọc Số (`Append-Only Readout Log`)

| Ngày | Kỳ đọc số | Tóm tắt số liệu & Cờ kiểm tra (`F1–F4`) | Quyết định hành động |
|---|---|---|---|
| 2026-11-09 | **Kỳ 0 (`Pre-Launch Baseline Setup`)** | Đã xác minh tất định `8/8` bất biến của máy trạng thái `tel` (`R1–R6`, `F4`, `from_start`, `/api/p`) qua `scripts/wms-qa-verify.py`; tách biệt hoàn toàn dữ liệu thử nghiệm `S4 QA` khỏi bảng đếm công khai; 6 video `v6.5` trên `@WhereMoneySleeps` đang ở trạng thái `unlisted`. | Giữ nguyên ngưỡng chưa đặt trước theo `ONE-PAGER.md` §4; chờ hoàn tất 4 cổng `H1–H4` (`LAUNCH-READINESS.md`) và đủ `≥ 4 tuần` + `≥ 100 lượt` bài 1 để ghi Kỳ 1. |

## 3. Chưa xác minh được

- Số liệu thực tế của `M1–M5` trên Cloudflare D1 và `YT-1` trên YouTube Analytics sau khi mở `public` (cần thời gian tích luỹ thực tế `≥ 4 tuần`).
- Same vendor, same priors — no external verifier ran.
