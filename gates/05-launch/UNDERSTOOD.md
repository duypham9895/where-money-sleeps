---
status: pass
stage: 05-launch
date: 2026-11-09
owner: ops
blocked_on: []
---

# UNDERSTOOD — S5 Launch

**Phòng sở hữu stage: Ops + Marketing + Legal** (theo Quy tắc 11, Quy tắc 4 & `gates/01-spec/LEGAL-REVIEW.md`).

## Trích NGUYÊN VĂN từ ONE-PAGER

<grounding>
"Người học không thấy mình đang học kế toán."
"Mọi bài là một Mặt cắt Kiến trúc Diorama v3.0:"
"Tiến độ nằm trên máy của chính người học."
</grounding>

## Kể lại bằng chữ của tôi

`Where Money Sleeps` là tạp chí tương tác song ngữ giúp người đọc phổ thông nhìn thấu đường đi thật sự của dòng tiền qua các giao dịch hằng ngày (quẹt thẻ, nhận lương, mua trả góp 0%) bằng mặt cắt kiến trúc 5 ngôi nhà, bài khảo cứu hai góc nhìn (`Đời thường` ⇄ `Sổ kế toán TT 99/2025`), bàn duyệt `studio.html` và bộ 6 video Calm Editorial Motion `v6.5` trên kênh `@WhereMoneySleeps`. Toàn bộ tiến độ học tập được lưu cục bộ trên máy của người đọc, đo lường bằng bộ đếm gộp không định danh qua đường dẫn trung tính `/api/p`, và mọi nội dung/video đều đi kèm quy trình đường gỡ 72 giờ cũng như chỉ chuyển sang chế độ công khai khi có chữ ký duyệt trực tiếp của Duy.

## Stage của tôi phục vụ điều đó thế nào

1. **Hạng mục 1 — Hồ sơ Sẵn Sàng Ra Mắt & Đường Gỡ 72 Giờ (`gates/05-launch/LAUNCH-READINESS.md`):** Thiết lập cổng kiểm tra bất khả miễn trừ (`non-waivable`) trước khi mở công khai, bao gồm trạng thái 5/5 cổng `scripts/wms-check.sh`, 4/4 cụm E2E `scripts/wms-qa-verify.py`, sổ giấy phép `legal/licences.json`, quy trình vận hành đường gỡ 72 giờ (`AC-61`, `R33`, `R37` cho cả bài web lẫn video YouTube) và bảng các việc chỉ Duy làm được trước khi công khai (`Ringkas`, đo điện thoại thật, Cloudflare D1, ký chuyển `unlisted` → `public`).
2. **Hạng mục 2 — Định Vị, Tagline Bắt Buộc & Chuẩn Phát Hành Đa Kênh (`gates/05-launch/POSITIONING.md`):** Chốt thông điệp định vị, tagline bắt buộc (`AC-39`, `QĐ 22`, `QĐ 55`), công thức tiêu đề 3 điểm neo ngữ cảnh tự thân, chuẩn metadata kênh `@WhereMoneySleeps` (`B1–B4`, `containsSyntheticMedia: true`) và thẻ chia sẻ OpenGraph.
3. **Hạng mục 3 — Trang Tổng Kết Duyệt `S5 Launch` (`docs/s5.html`):** Trình bày ngắn gọn (`≤ 520 từ`) toàn bộ hồ sơ sẵn sàng ra mắt, đường gỡ 72 giờ và danh sách kiểm của Duy trước khi mở công khai.

## Chưa xác minh được

- Việc đọc hợp đồng lao động Ringkas của Duy (`R34`), phép đo `#sync` trong WebView Zalo trên điện thoại iPhone/Android thật (`AC-31, 32`), và đấu nối Cloudflare Worker `/api/p` + D1 thực tế (`AC-35, 55, 69`) thuộc quyền thực thi và ký xác nhận trực tiếp của Duy trước khi bấm công khai.
- Same vendor, same priors — no external verifier ran.
