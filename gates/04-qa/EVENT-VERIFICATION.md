---
status: pass
stage: 04-qa
date: 2026-11-09
owner: Data
blocked_on: []
---

# EVENT-VERIFICATION — Báo Cáo Xác Minh Hợp Đồng Đo Lường (`S4 QA` — `where-money-sleeps`)

> **Verdict của Phòng Data (Quy tắc 8):** **`PASS` — Toàn bộ 8 bất biến của máy trạng thái đo lường chống trùng `tel` (`R1–R6`, `F4`, `QĐ 39 from_start`, `AC-29 schema=1`, `AC-68 /api/p`) đã được kiểm chứng tự động bằng Node VM (`scripts/wms-qa-verify.py` mục `[QA-2]`) trên mã nguồn `docs/prototype.html`.**

## 1. Bảng Xác Minh Từng Sự Kiện Theo `gates/01-spec/TRACKING-PLAN.md`

| Tên Event | Payload hợp đồng (`TRACKING-PLAN.md` §1) | Quy tắc chống trùng (`tel`) | Kịch bản kiểm thử trong `scripts/wms-qa-verify.py` | Kết quả |
|---|---|---|---|---|
| `card_answered` | `{ event: "card_answered", card: "<cardId>.v<n>", correct: true\|false }` | `R1`: Khoá `tel.card_answered["<cardId>.v<n>"] = "sent"` ghi vào `localStorage` **trước** khi gọi `sendBeacon("/api/p")` | Gọi `answerQuizCard("card", "card-q1.v1", 0)` lần 1 ⇒ bắn `{ card: "card-q1.v1", correct: true }`; gọi lại lần 2 với đáp án khác ⇒ **không bắn lại** (`0` đếm đôi) | **`PASS`** |
| `lesson_completed` (Bài 1 / đi từ đầu) | `{ event: "lesson_completed", lesson: "<lessonId>", from_start: true }` (không có `lang` theo `QĐ 25b`) | `R1` + `F4` + `QĐ 39`: Bắn **cùng một chạm** với `card_answered` đầu tiên của bài; `from_start = true` khi bài là `"card"` hoặc `tel.lesson_completed["card"]` đã có mặt | Trả lời `card-q1.v1` trên bộ nhớ mới ⇒ bắn đồng thời `card_answered` + `lesson_completed{ lesson: "card", from_start: true }`; trả lời tiếp `card-q2.v1` ⇒ chỉ bắn `card_answered`, không bắn lại `lesson_completed` | **`PASS`** |
| `lesson_completed` (Nhảy thẳng vào bài giữa) | `{ event: "lesson_completed", lesson: "install", from_start: false }` | `QĐ 39` (`AC-62`): Bộ nhớ mới chưa có `tel.lesson_completed["card"]` mà hoàn thành `"install"` ⇒ `from_start = false` (đo lường độ lệch giữa số lỏng và số chặt) | Xoá bộ nhớ, gọi `answerQuizCard("install", "install-q1.v1", 0)` ⇒ bắn `lesson_completed{ lesson: "install", from_start: false }` | **`PASS`** |
| `lesson_completed` (Khi tự khai giai đoạn — `R3`) | **Không bắn** (`suppressed`) | `R3` (`AC-30`): Khi người học bấm tự khai giai đoạn (`selfDeclareEntryStage()`), mọi bài lối vào (`card`, `pay`, `install`) được gán `tel.lesson_completed[k] = "suppressed"` vĩnh viễn | Gọi `selfDeclareEntryStage()`, sau đó trả lời `pay-q1.v1` ⇒ `card_answered` vẫn bắn bình thường nhưng `lesson_completed` **bị chặn tuyệt đối** | **`PASS`** |
| `sync_created` | `{ event: "sync_created", method: "link"\|"code" }` | `R1`: Khoá `tel.sync_created[method] = "sent"` tối đa 1 lần mỗi phương thức trên một bộ nhớ | Gọi `createSyncBackup("code")` hai lần liên tiếp ⇒ chỉ bắn đúng **1** sự kiện `sync_created{ method: "code" }` | **`PASS`** |
| `progress_restored` | `{ event: "progress_restored", method: "link"\|"code" }` | `R4`: Không chống trùng cho chính sự kiện khôi phục, nhưng mang nguyên đối tượng `tel` sang máy mới để các bài/thẻ đã làm ở máy cũ **không bắn lại** | Khôi phục token trên bộ nhớ trắng (`restoreFromSyncToken(token, "code")`) ⇒ bắn `progress_restored{ method: "code" }`; sau đó chạm lại `card-q1.v1` ⇒ `0` sự kiện trùng | **`PASS`** |

## 2. Xác Minh Đường Truyền & Quyền Riêng Tư (`AC-33`, `AC-34`, `AC-68`)

- **Đường dẫn trung tính tránh bộ lọc EasyPrivacy (`AC-68`):** Mọi lời gọi `navigator.sendBeacon` trong `docs/prototype.html` gửi tới `/api/p`, hoàn toàn không chạm danh sách cấm (`/collect`, `/event`, `/track`, `/beacon`, `/metrics`, `/api/event`).
- **Không rò rỉ siêu dữ liệu cá nhân (`AC-29`, `AC-34`, `QĐ 26`):** Hàm `encodeSyncToken()` lọc bỏ trường `lastActive` trước khi mã hoá Base64; payload gửi qua `sendBeacon("/api/p")` chỉ chứa đúng tên `event` và các thuộc tính đã khai trong `TRACKING-PLAN.md` (`0` ID người dùng, `0` cookie, `0` địa chỉ IP phía client).

## 3. Chưa xác minh được

- Nhìn số tăng trực tiếp trên bảng Cloudflare D1 thật từ thao tác tay trên điện thoại iPhone/Android vật lý (`AC-36`, `AC-70`) và xác nhận tắt `Workers Logs` trên tài khoản Cloudflare của Duy (`AC-35`, `AC-55`) — sẽ thực hiện khi nối Worker trước cổng `S5 Launch`.
- Same vendor, same priors — no external verifier ran.
