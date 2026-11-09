---
status: pass
stage: 02-design
date: 2026-11-08
owner: research-t3
blocked_on: []
---

# T3-RECONSTRUCTION — Bản Tái Lập Độc Lập `S2 Design` (`where-money-sleeps`)

> **Quy tắc 7 & 12 (T3 TÁI LẬP):** Dựng lại độc lập từ `gates/ONE-PAGER.md`, `gates/01-spec/PRD.md`, và `gates/01-spec/AGENT-CMS-PIPELINE.md` bởi subagent `3d8bc758-9d1b-451a-a372-34cbb09b8f80` mà **không đọc bất kỳ file nào trong `gates/02-design/`**.
> *Same vendor, same priors — no external verifier ran.*

## 1. Ba phát hiện đối chiếu giữa S0/S1 và S2

1. **Phát hiện #1 (Chặn vi phạm QĐ 41 / Legal R20 trong dòng minh bạch AI — ĐÃ SỬA Ở `MICROCOPY.md`):**
   - Trong `PRD.md` (QĐ 41, Legal R20, AC-21, AC-86), dòng minh bạch công khai bắt buộc theo mẫu Writer W2 (*"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."*) và **cấm 4 từ `"kế toán"`, `"accountant"`, `"chuyên gia"`, `"expert"`** xuất hiện trong dòng minh bạch công khai hoặc trường `reviewed_by`.
   - Bản nháp đầu của `MICROCOPY.md` từng viết *"Đã qua 4 chuyên gia kiểm duyệt tự động"* (chứa từ `"chuyên gia"` bị cấm bởi R20). Nhờ đối chiếu T3, `MICROCOPY.md` đã được sửa ngay thành: *"Soạn với hỗ trợ AI · Con số và tên tài khoản được một agent AI soát (`K1–K4 · F1–F4 · B1–B4 · M1–M4`); {approvedBy} ký duyệt."*
2. **Phát hiện #2 (Định danh bảng màu & 3 họ font ở S2):**
   - S0/S1 khoá phong cách **Risograph**, mã màu `#rrggbb`, bộ số **`tabular-nums`** (`M2`), và **Font giấy phép mở OFL** (Legal R30). S2 (`DESIGN-BRIEF.md` & `TOKENS.md`) định danh cụ thể bảng màu *Warm Archival Risograph Paper (`#f5efe3`) & Night-Watch Ledger (`#0e1015`)* cùng 3 họ font OFL (`Fraunces`, `Be Vietnam Pro`, `JetBrains Mono`).
3. **Phát hiện #3 (Ánh xạ bề mặt S1 cũ sang kiến trúc QĐ 52–58):**
   - Các bề mặt trình đọc PDF *Hermanson* (B6/B7 cũ) đã được gỡ bỏ theo QĐ 52; bề mặt điều hướng chuyển thành `Layout 1A Editorial Split-Pill 48px` + `Overlay Mục lục 2 cột Master–Detail` (QĐ 55); bổ sung bề mặt `Khung Studio Video .yt-embed` (QĐ 56), `4 hình mặt cắt 16:9 LUẬT 9` (QĐ 57), và `Trung tâm Điều phối Agent Realtime docs/workflows.html` (QĐ 58).

## 2. Bảng tổng hợp 5 trụ yêu cầu tái lập từ S0/S1

| Trụ | Mã | Yêu cầu cốt lõi từ nguồn S0/S1 | Đối chiếu với `gates/02-design/` |
|---|---|---|---|
| **A · Thẩm mỹ & Typography** | `A1–A4` | Phong cách mặt cắt Risograph có tường gạch chéo `poché`, mã màu `#rrggbb`, số `tabular-nums` (`M2`), font OFL | Khớp 100% trong `DESIGN-BRIEF.md` & `TOKENS.md` |
| **B · Điều hướng & Bề mặt** | `B1–B6` | Thanh `1A Split-Pill 48px` (không hamburger cạnh logo), Overlay Mục lục 2 cột `0px` Layout Shift + `⌘K`, thẻ chuyển bài cuối bài, CMS Preview `?preview=1`, `docs/workflows.html` | Khớp 100% trong `UI-STATES.md` |
| **C · Mặt cắt Diorama & Motion** | `C1–C5` | 5 ngôi nhà archetype (`const TYPES`), tách 3 kênh `wire` / `pipe` / `book` (`TK 1388`), 2 góc nhìn `Cá nhân ⇄ Sổ kế toán`, chuyển động `bang-motion` `M1–M4` (`cubic-bezier(0.22,1,0.36,1)`, `window.__vibeSeek`, `prefers-reduced-motion`, 0 CDN ngoài) | Khớp 100% trong `TOKENS.md`, `UI-STATES.md`, `A11Y.md` |
| **D · Khảo cứu 2 tầng, Hình `LUẬT 9` & Video** | `D1–D3` | 3 tab `A/B/C` (`C9 v2`), Chương 01 thuần chữ + 4 hình `16:9` (`1200×675`, `CLS=0`) ở Chương 02–05 sau đoạn 1 kèm chú thích 3 tầng (`LUẬT 9`), khung `.yt-embed` (`16:9 ⇄ 9:16`, Split-Stage `LUẬT 8`, fallback MP4) | Khớp 100% trong `TOKENS.md` & `UI-STATES.md` |
| **E · Microcopy & Brand Safety** | `E1–E6` | Thay 100% chữ `"sổ cái"` bằng `"Mục lục"` / `"Sổ kế toán"` / `"sổ sách ngân hàng"` (QĐ 55), 0 tên riêng (`LUẬT 4`), 0 lộ đạo cụ (`LUẬT 7`), tiêu đề 3 điểm neo, dòng minh bạch AI tuân thủ R20 (QĐ 41) | Đã sửa `MICROCOPY.md` theo phát hiện #1 — khớp 100% |
