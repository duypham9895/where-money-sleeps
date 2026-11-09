---
status: pass
stage: 04-qa
date: 2026-11-09
owner: qa
blocked_on: []
---

# UNDERSTOOD — S4 QA

**Phòng sở hữu stage: QA** (phối hợp cùng Phòng Data theo Quy tắc 11, Quy tắc 8 & `gates/01-spec/ACCEPTANCE.md`).

## Trích NGUYÊN VĂN từ ONE-PAGER

<grounding>
"Người học không thấy mình đang học kế toán."
"Mọi bài là một Mặt cắt Kiến trúc Diorama v3.0:"
"Tiến độ nằm trên máy của chính người học."
</grounding>

## Kể lại bằng chữ của tôi

`Where Money Sleeps` là tạp chí tương tác song ngữ giải thích đường đi ngầm của dòng tiền qua các giao dịch thường nhật (quẹt thẻ, nhận lương, trả góp 0%) bằng mặt cắt kiến trúc 5 ngôi nhà, bài khảo cứu hai góc nhìn (`Đời thường` ⇄ `Sổ kế toán TT 99/2025`), bàn dựng `studio.html` và bộ 6 video giải thích Calm Editorial Motion `v6.5` trên kênh `@WhereMoneySleeps`. Toàn bộ tiến độ và thẻ trắc nghiệm cuối bài đều nằm trong bộ nhớ cục bộ của thiết bị người học, đo lường bằng bộ đếm gộp không định danh có khoá chống trùng `tel`, và tuyệt đối không có nội dung hay video nào được chuyển sang chế độ công khai khi chưa có chữ ký duyệt của Duy.

## Stage của tôi phục vụ điều đó thế nào

1. **Hạng mục 1 — Xác minh Tất định & Chấp nhận (`gates/04-qa/VERIFICATION.md`):** Chạy bộ kiểm 5 cổng `scripts/wms-check.sh` (`C0–C9`, `F1–F4`, `M0–M4`, `wms-studio-sync.py --check`, `vibe-check.sh`) kết hợp kịch bản kiểm thử E2E đối chiếu toàn bộ tiêu chí `gates/01-spec/ACCEPTANCE.md` trên 3 bề mặt ứng dụng sống (`docs/prototype.html`, `docs/studio.html`, `docs/workflows.html`) và 6 video `v6.5`.
2. **Hạng mục 2 — Xác minh Sự kiện Đo lường & Chống trùng (`gates/04-qa/EVENT-VERIFICATION.md`):** Phòng Data thực thi kiểm thử máy trạng thái `tel` (`R1–R6`, bất biến `F4`, cờ `from_start`, sao lưu/khôi phục `#sync` mang theo `tel`, `window.__wmsTelemetryLog`) đảm bảo mọi event trong `gates/01-spec/TRACKING-PLAN.md` bắn đúng hợp đồng, không đếm đôi và `0` script theo dõi bên thứ ba.
3. **Hạng mục 3 — Kiểm duyệt Độc lập Đa chiều (`gates/04-qa/REVIEW.md`):** Triển khai phiên kiểm duyệt độc lập (`invoke_subagent`) rà soát an ninh CSP (`connect-src 'none'` trên `studio.html`), khả năng tiếp cận (`a11y`), bộ 4 chuyên gia `K1–K4` / `F1–F4` / `B1–B4` / `M1–M4`, và ghi trang tổng kết `docs/s4.html` (`≤ 520 từ`) để Duy duyệt.

## Chưa xác minh được

- Phép đo khôi phục `#sync` qua trình duyệt trong ứng dụng Zalo trên thiết bị iPhone/Android vật lý và điều khoản hợp đồng lao động Ringkas của Duy (thuộc cổng điều kiện trước `S5 Launch`).
- Same vendor, same priors — no external verifier ran.
