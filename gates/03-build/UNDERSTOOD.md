---
status: pass
stage: 03-build
date: 2026-11-09
owner: swe
blocked_on: []
---

# UNDERSTOOD — S3 Build

**Phòng sở hữu stage: SWE** (phối hợp cùng Data + Legal theo Quy tắc 11 & `../docs/stages.md`).

## Trích NGUYÊN VĂN từ ONE-PAGER

<grounding>
"Người học không thấy mình đang học kế toán."
"Mọi bài là một Mặt cắt Kiến trúc Diorama v3.0:"
"Tiến độ nằm trên máy của chính người học."
</grounding>

## Kể lại bằng chữ của tôi

`Where Money Sleeps` là cuốn tạp chí tương tác giúp người đọc phổ thông lần theo đường đi thật sự của từng đồng tiền — từ khoảnh khắc quẹt thẻ, nhận lương hay ký trả góp 0% ngoài đời thực cho tới các bút toán ghi Nợ/Có và kỳ quyết toán ngầm giữa các định chế tài chính. Thay vì giảng lý thuyết kế toán khô khan, sản phẩm dùng mặt cắt kiến trúc 5 ngôi nhà, bài khảo cứu hai góc nhìn và video giải thích có giọng đọc tự nhiên để tạo khoảnh khắc vỡ lẽ tức thì. Mọi dữ liệu tiến độ đều lưu cục bộ trên thiết bị của người học, không thu thập định danh cá nhân, và tuyệt đối không có nội dung hay video nào được chuyển sang chế độ công khai khi chưa có chữ ký duyệt của Duy.

## Stage của tôi phục vụ điều đó thế nào

1. **Lát cắt 1 — Đồng bộ 6 Video Calm Editorial `v6.0` & Phụ đề `.srt` lên YouTube (`QĐ 56` & `QĐ 61`):** Tải toàn bộ 6 video vừa kết xuất chuẩn Calm Editorial `v6.0` (`card`, `pay`, `install` × `16:9` & `9:16`) kèm phụ đề `.srt` lên kênh `@WhereMoneySleeps` ở trạng thái `unlisted`, sau đó nhúng mã `youtubeId` 11 ký tự thật vào `docs/prototype.html` và `docs/wms-studio-data.js`.
2. **Lát cắt 2 — Thẻ Trắc nghiệm Cuối bài (`Quiz Cards`), Lưu Tiến độ Cục bộ & Sao lưu `#sync` + `persist()` (`gates/01-spec/PRD.md` & `gates/01-spec/ACCEPTANCE.md`):** Hoàn thiện bộ câu hỏi trắc nghiệm cuối mỗi bài (`≥ 2` card trắc nghiệm/bài đã qua `ke-toan-reviewer`), lưu tiến độ trên máy (`localStorage` + `IndexedDB` + cảnh báo `navigator.storage.persist()`) và tính năng tạo/khôi phục mã sao lưu `#sync`.
3. **Lát cắt 3 — Hợp đồng Đo lường Chống trùng Không Định danh (`gates/01-spec/TRACKING-PLAN.md`):** Lập trình máy trạng thái `tel` (`R1–R6`) bắn đúng 4 sự kiện (`lesson_completed{lesson, from_start}`, `card_answered{card, correct}`, `sync_created{method}`, `progress_restored{method}`) qua `navigator.sendBeacon` kèm bộ đệm kiểm thử `window.__wmsTelemetryLog` phục vụ `S4 QA`.
4. **Lát cắt 4 — Hồ sơ Bàn giao `S3 Build` (`legal/licences.json`):** Ghi nhật ký lát cắt dọc, cập nhật sổ giấy phép tài sản và chạy kiểm định `scripts/wms-check.sh` (`5/5 PASS`).

## Chưa xác minh được

- Tốc độ khôi phục `#sync` trên trình duyệt trong ứng dụng Zalo/Facebook ở thiết bị iPhone và Android thật (sẽ đo ở cổng `S4 QA` / trước `S5 Launch`).
- Same vendor, same priors — no external verifier ran.
