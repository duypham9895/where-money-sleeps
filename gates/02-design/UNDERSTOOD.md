---
status: pass
stage: 02-design
date: 2026-11-08
owner: design
blocked_on: []
---

# UNDERSTOOD — S2 Design

**Phòng sở hữu stage: Design** (phối hợp cùng Writer + PM theo Quy tắc 11 & Quy tắc 13).

## Trích NGUYÊN VĂN từ ONE-PAGER

<grounding>
"Người học không thấy mình đang học kế toán."
"Mọi bài là một Mặt cắt Kiến trúc Diorama v3.0:"
"Mỗi bài khảo cứu đan xen 4 hình mặt cắt giải thích"
</grounding>

## Kể lại bằng chữ của tôi

Sản phẩm này không phải một giáo trình kế toán khô khan hay một ứng dụng ngân hàng giả lập, mà là một cuốn tạp chí giải phẫu kiến trúc dòng tiền dành cho người bình thường. Khi một người quẹt thẻ, nhận lương hay mua trả góp, họ chỉ nhìn thấy tin báo biến động số dư trên điện thoại, còn phần chìm của hệ thống — nơi lệnh uỷ quyền đi đường riêng, tiền thật đi đường quyết toán liên ngân hàng, và các khoản phí ngầm được ghi nhận trên sổ sách — lại bị che khuất.

Nhiệm vụ của thiết kế ở đây là mở tấm màn che đó ra bằng hai lớp trải nghiệm gắn kết chặt chẽ: trên đầu bài là sân khấu mặt cắt 5 ngôi nhà hoạt động theo từng nhịp câu chuyện kèm nút gạt đổi góc nhìn giữa túi tiền cá nhân và sổ kế toán; bên dưới là bài khảo cứu sâu có trình phát video phát sóng và các hình mặt cắt minh hoạ đan xen đúng điểm chuyển cơ chế để mắt người đọc luôn có điểm tựa thị giác.

## Stage của tôi phục vụ điều đó thế nào

1. **`DESIGN-BRIEF.md` (`≤ 1 trang`):** Khoá ngôn ngữ thẩm mỹ *Warm Archival Risograph & Night-Watch Ledger* (3 tính từ · 3 thứ KHÔNG giống · hướng thiết kế đã kiểm chứng trực tiếp trên `docs/prototype.html` và `docs/workflows.html`).
2. **`TOKENS.md`:** Định nghĩa bộ biến CSS chuẩn cho giấy kem ấm (`#f5efe3`), mực in Risograph (`#191714`), đỏ son biên tập (`#b83a22`), xanh két ngân hàng (`#1c5d4b`), bảng màu tối `#0e1015`, hệ chữ 3 họ (`Fraunces` · `Be Vietnam Pro` · `JetBrains Mono` với `tabular-nums`) và đường cong chuyển động vật lý `cubic-bezier(0.22, 1, 0.36, 1)` theo `bang-motion` `M1–M4`.
3. **`UI-STATES.md` & `MICROCOPY.md`:** Đặc tả toàn bộ trạng thái tương tác của 8 bề mặt (thanh điều hướng `1A Editorial Split-Pill 48px`, Overlay Mục lục 2 cột `Master–Detail` + `⌘K`, Mặt cắt Diorama 5 nhà, nút gạt 2 góc nhìn, bài khảo cứu 2 tầng kèm 4 hình `16:9` `LUẬT 9`, khung video `.yt-embed` `16:9 ⇄ 9:16` + fallback MP4 cục bộ, thanh duyệt CMS `?preview=1`, và sơ đồ `docs/workflows.html`) cùng bộ microcopy tiếng Việt thật (0 chữ `"sổ cái"`, 0 tên riêng `LUẬT 4`, 0 lộ ẩn dụ đạo cụ `LUẬT 7`).
4. **`A11Y.md`:** Đảm bảo độ tương phản WCAG 2.2 AA/AAA, vùng chạm `≥ 24×24px`, điều hướng bàn phím (`tabindex`, `aria-expanded`, `Escape`), `CLS = 0` trên mọi hình/video và tôn trọng `@media (prefers-reduced-motion: reduce)`.

## Chưa xác minh được

- Cảm nhận thực tế của 5 người đọc thử đầu tiên khi chạm mở thẻ chú thích `[[thuật ngữ|khoá]]` trên màn hình hẹp `360px` trong WebView Zalo iPhone/Android (sẽ đo trước cổng `S5 Launch`).
- Cross-vendor model review (Claude ↔ Gemini) — no human external verifier ran.
