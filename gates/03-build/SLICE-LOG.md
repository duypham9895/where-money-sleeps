---
status: pass
stage: 03-build
date: 2026-11-09
owner: swe
blocked_on: []
---

# SLICE-LOG — Nhật Ký Lát Cắt Dọc (`S3 Build` — `where-money-sleeps`)

> **Hợp đồng `S3 Build` (`../docs/stages.md`):** Mỗi lát cắt dọc mang theo giao diện/logic, sự kiện đo lường (`gates/01-spec/TRACKING-PLAN.md`) và sổ giấy phép (`legal/licences.json`) tương ứng, kèm kiểm chéo T1 (`scripts/wms-check.sh`) và T2 (Phòng Data + Phòng Legal).

## 1. Bảng Lát Cắt Dọc Đã Thực Thi (`Vertical Slices`)

| Lát cắt | Hạng mục & File triển khai | Hợp đồng Event (`TRACKING-PLAN.md`) | Hợp đồng Giấy phép (`legal/licences.json`) | Trạng thái |
|---|---|---|---|---|
| **Slice 1 — Mặt cắt Diorama v3.0 · Điều hướng `1A` (`48px`) · Khảo cứu 2 tầng (`LUẬT 9`) · Bàn Duyệt `studio.html` (`QĐ 53–60`)** | `docs/prototype.html` · `docs/studio.html` · `docs/workflows.html` · `scripts/wms-studio-sync.py` · 12 hình mặt cắt `assets/figures/fig-{card,pay,install}-c{2..5}.jpg` (`1200×675`, `CLS = 0`) | Chuẩn bị khung bài viết `card`, `pay`, `install` cho sự kiện hoàn thành bài & trả lời thẻ | Đã ghi nhận 3 họ font OFL (`Fraunces`, `Be Vietnam Pro`, `JetBrains Mono`) và `bangtutorial/bang-motion` (`MIT License`) trong `legal/licences.json` | **`PASS`** |
| **Slice 2 — Thẻ Trắc nghiệm Cuối bài (`WMS_QUIZ_BANK`) · Tiến độ Cục bộ (`IndexedDB` + `localStorage`) · Giữ bộ nhớ `persist()` & Sao lưu `#sync` (`QĐ 24, 26, 38, 45`)** | `docs/prototype.html` (`#lessonQuizWrap`, `WMS_QUIZ_BANK` gồm 6 thẻ trắc nghiệm `card-q1.v1..install-q2.v1`, `loadWmsProgress()`, `saveWmsProgress()`, `encodeSyncToken()`, `restoreFromSyncToken()`) | `card_answered{card, correct}` · `lesson_completed{lesson, from_start}` · `sync_created{method}` · `progress_restored{method}` | `0` thư viện ngoài (`0 CDN runtime`, bảo toàn quyền riêng tư người đọc) | **`PASS`** |
| **Slice 3 — Máy Trạng Thái Đo lường Chống trùng Không Định danh `tel` (`R1–R6` · `QĐ 25, 38, 39`)** | `docs/prototype.html` (`emitWmsTelemetry()`, `window.__wmsTelemetryLog`, `navigator.sendBeacon("/api/event")`, khoá chống trùng `tel.{lesson_completed,card_answered,pdf_opened,sync_created}`, quy tắc `R3` `suppressed` khi tự khai và `R4` mang `tel` theo mã `#sync`) | Đủ 4 sự kiện cốt lõi + cờ `from_start` (`true`\|`false`) + bất biến `F4` (`lesson_completed` bắn cùng chạm với `card_answered` đầu tiên) | `0` cookie, `0` fingerprinter, `0` script theo dõi bên thứ ba | **`PASS`** |
| **Slice 4 — Bộ Dựng Video Calm Editorial Motion `v6.0` (`9:16` Shorts & `16:9` Longs) + Upload YouTube `@WhereMoneySleeps` (`unlisted`) + Nhúng `youtubeId` (`QĐ 56, 60, 61`)** | `scripts/wms-render-short-v43.py` · `scripts/wms-render-long-v43.py` · `dist/youtube/{card,pay,install}-{short-9x16,long-16x9}.{mp4,srt}` · `docs/prototype.html` · `docs/wms-studio-data.js` (`card`: `long=l6kS579ozbQ`, `short=NDJcFK1uVNU`; `pay`: `long=e0Socd4aJLc`, `short=3KNTKbwUpFQ`; `install`: `long=v7Fe0Rx1He4`, `short=DgO7F6D8jvs`) | Tích hợp trình phát `.yt-embed` + fallback MP4 cục bộ + phụ đề `.srt` | Giọng đọc `eleven_v3:JwqRvOqFdGeQNu7UjKjw` & SFX gói trả phí có Commercial License ghi trong `legal/licences.json` | **`PASS` (6/6 video Calm Editorial `v6.0` đã tải lên `@WhereMoneySleeps` `unlisted` và nhúng vào `docs/prototype.html`)** |

## 2. Kiểm Chéo T2 (Phòng Data & Phòng Legal hỏi — Phòng SWE trả lời)

1. **Câu hỏi 1 (Phòng Data):** *"Khi người học chạm chọn đáp án ở thẻ trắc nghiệm đầu tiên (`card-q1.v1`), hàm `emitWmsTelemetry` có ghi khoá `tel` vào `localStorage` TRƯỚC khi gọi `navigator.sendBeacon` theo quy tắc `R1` không, và nếu người học chạm lại vào chính thẻ đó hoặc tải lại trang từ mã `#sync` thì có bị bắn trùng không?"*
   - **Trả lời (Phòng SWE):** Trong `emitWmsTelemetry()` tại `docs/prototype.html`, mảng `WMS_PROG.tel[eventName][dedupeKey]` được kiểm tra đầu tiên; nếu chưa có thì gán `"sent"` và gọi `saveWmsProgress(WMS_PROG)` **trước** khi gọi `navigator.sendBeacon("/api/event", blob)`. Khi người học bấm lại cùng thẻ `card-q1.v1` hoặc khôi phục từ mã `#sync` (vốn đóng gói kèm đối tượng `tel` theo `R4`), khoá `"sent"` đã tồn tại nên hàm trả về `false` ngay lập tức, đảm bảo `0` đếm đôi.
2. **Câu hỏi 2 (Phòng Legal):** *"Trong toàn bộ các lát cắt `S3 Build` (kể cả 6 thẻ trắc nghiệm mới trong `WMS_QUIZ_BANK` và 6 video Calm Editorial `v6.0`), có xuất hiện bất kỳ tên thương hiệu/ngân hàng/mạng thẻ/công cụ hậu trường có thật nào vi phạm `LUẬT 4` hay script bên thứ ba nào vi phạm cam kết quyền riêng tư không?"*
   - **Trả lời (Phòng SWE):** Tuyệt đối không. Toàn bộ 6 thẻ trắc nghiệm mới dùng danh từ chung (`quán quen`, `ngân hàng của bạn`, `tổ chức chuyển mạch thẻ`, `doanh nghiệp`, `cửa hàng`, `công ty tài chính`), vượt qua bộ kiểm `scripts/check-story.py`, `scripts/wms-finance-kb.py` (`F1–F4`) và `scripts/wms-motion-snap.py` (`M1–M4`, `0` script CDN bên thứ ba).

## 3. Chưa xác minh được

- Tốc độ khôi phục `#sync` trên trình duyệt trong ứng dụng nhắn tin ở thiết bị iPhone/Android thật và số liệu giữ chân thực tế trên YouTube Analytics (sẽ kiểm ở cổng `S4 QA` / trước `S5 Launch`).
- Same vendor, same priors — no external verifier ran.
