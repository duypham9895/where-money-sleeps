---
status: pass
stage: 02-design
date: 2026-11-08
owner: design
blocked_on: []
---

# TOKENS — Hệ thống Token Thiết kế (`Where Money Sleeps`)

> Hợp đồng token cho `S3 Build` và `S4 QA`, trích xuất trực tiếp từ hai bản mẫu tham chiếu đã chạy thật: `docs/prototype.html` (Tạp chí & Mặt cắt Diorama v3.0) và `docs/workflows.html` (Trung tâm Điều phối Agent Realtime).

## 1. Bảng màu hai chế độ (`Warm Archival Risograph` & `Night-Watch Ledger`)

Không dùng gradient tím/xanh kiểu AI đại trà (`ecc:design-system` Mode 3). Dùng bảng màu giấy lưu trữ ấm áp kết hợp mực in Risograph độ tương phản cao:

| Token CSS | Sáng (`Archival Paper` — `prototype.html`) | Tối (`Night-Watch Ledger` — `workflows.html` / `doc.css`) | Vai trò ngữ nghĩa | Độ tương phản với nền |
|---|---|---|---|---|
| `--paper` / `--bg` | `#f5efe3` | `#0e1015` | Nền trang chính (giấy kem ấm / đêm trực sổ) | — |
| `--paper2` / `--bg2` | `#ece3d2` | `#151922` | Nền thẻ phụ, ô tóm tắt, hộp công thức | — |
| `--paper3` / `--bg3` | `#e0d4be` | `#1c222e` | Viền phân cách đậm, nền pill đang chọn | — |
| `--ink` / `--fg` | `#191714` | `#f4efe6` | Chữ chính, nét vẽ kiến trúc mặt cắt | **14.8 : 1** (AAA) |
| `--ink2` | `#4a443b` | `#b8b0a2` | Chữ phụ, chú thích tầng 3, mô tả | **7.9 : 1** (AAA) |
| `--muted` | `#7a7164` | `#847d70` | Nhãn phụ, mốc thời gian, số thứ tự | **4.6 : 1** (AA) |
| `--red` (`--vermilion`) | `#b83a22` (`#f8e5df` tint) | `#e05a40` | Điểm nhấn biên tập, dòng phí bị khấu trừ (`MDR`/lãi ngầm), cổng chặn `FAIL` | **5.4 : 1** (AA) |
| `--green` (`--vault`) | `#1c5d4b` (`#dfeee8` tint) | `#3bba8c` | Dòng **tiền thật quyết toán** (`pipe`), số thực nhận, trạng thái `PASS` | **7.1 : 1** (AAA) |
| `--blue` (`--signal`) | `#1f4b7a` (`#dfe9f4` tint) | `#5b9bd5` | Luồng **thông tin & hợp đồng** (`wire`), liên kết thuật ngữ `[[...]]` | **7.8 : 1** (AAA) |
| `--amber` (`--gold`) | `#9a6512` (`#f7ecd6` tint) | `#e6a832` | Bút toán **ghi sổ kế toán** (`book`), cảnh báo `WARN`, hạt dẫn hướng | **4.7 : 1** (AA) |

## 2. Hệ thống Chữ (`Typography Scale & Numeric Discipline`)

| Token | Font stack | Dùng ở đâu | Quy tắc bắt buộc |
|---|---|---|---|
| `--serif` | `'Fraunces', Georgia, serif` | Tiêu đề bài (`h1`), tiêu đề chương (`h2`), chữ cái đầu chương (`drop-cap`), con số lớn ở ô tổng kết | `font-optical-sizing: auto`; tạo cảm giác tạp chí khảo cứu kinh điển |
| `--sans` | `'Be Vietnam Pro', system-ui, sans-serif` | Thân bài khảo cứu (`17px`, `line-height: 1.72`), thanh điều hướng `48px`, bảng dữ liệu, chú thích hình | Tối ưu dấu tiếng Việt, độ rộng dòng khảo cứu `62ch–68ch` |
| `--mono` | `'JetBrains Mono', ui-monospace, monospace` | Số tiền (`#sum-gross`, `#sum-fee`, `#sum-net`, `.h-bal`), số hiệu tài khoản TT 99/2025 (`TK 112`, `TK 1388`), mã kiểm `C0–C9` | **Bắt buộc `font-variant-numeric: tabular-nums`** (`M2` trong `scripts/wms-motion-snap.py`) để chữ số không giật ngang khi nội suy |

## 3. Lưới, Khoảng cách & Khung hình (`Layout & Aspect-Ratio Tokens`)

| Thành phần | Giá trị khoá cứng | Mục đích & Ràng buộc |
|---|---|---|
| Thanh điều hướng trên cùng (`.top-nav`) | `height: 48px` · `position: sticky; top: 0; z-index: 90` | **QĐ 55 (`Layout 1A`):** chỉ 1 hàng duy nhất, nhường tối đa chiều dọc màn hình đầu tiên cho Mặt cắt Diorama |
| Overlay Mục lục 2 cột (`.atlas-backdrop`) | `position: fixed; inset: 0; z-index: 200` · khung trong `max-width: 980px; max-height: 82vh` | Mở nổi phủ lên trên, **`0px` Layout Shift** đối với sân khấu bên dưới |
| Sân khấu Mặt cắt Diorama (`#stage`) | `min-height: 430px` · lưới 5 cột `repeat(5, minmax(0, 1fr))` | 5 ngôi nhà mặt cắt cố định vị trí xuyên suốt 5 đoạn (`M1` Persistent World) |
| Hình minh hoạ khảo cứu (`.chap-fig`) | `width="1200" height="675"` · `aspect-ratio: 16 / 9` | **LUẬT 9 (`QĐ 57`):** đặt sau đoạn 1 của Chương 02–05, `CLS = 0` |
| Khung Video phát sóng (`.yt-player-wrap`) | Chế độ Dài: `aspect-ratio: 16 / 9` (`1920×1080`) · Chế độ Ngắn: `aspect-ratio: 9 / 16` (`max-width: 360px`, `1080×1920`) | **LUẬT 8:** Video `9:16` chia 3 vùng không đè nhau (`Zone 1: 36..354`, `STAGE_BOX: 368..1280`, `CARD_BOX: 1294..1734`) |

## 4. Chuyển động & Quán tính Vật lý (`bang-motion M1–M4`)

| Token / Hàm | Giá trị chuẩn | Kiểm bằng |
|---|---|---|
| `--ease-out-expo` | `cubic-bezier(0.22, 1, 0.36, 1)` | `scripts/wms-motion-snap.py` (`M1`) — áp cho cửa cuốn `.shutter`, khay sổ kế toán, thẻ trạng thái |
| `--ease-in-out-quart` | `cubic-bezier(0.76, 0, 0.24, 1)` | Áp cho xung hạt tiền tệ và thanh tiêu điểm phụ đề |
| `animateMoneyText()` / `animateCounter()` | Nội suy `requestAnimationFrame` `420ms` theo hàm bậc ba `1 - Math.pow(1 - p, 3)` | `scripts/wms-motion-snap.py` (`M2`) |
| `<circle class="signal-orb">` | `<animateMotion dur="1.5s" repeatCount="indefinite" path="..." />` | `scripts/wms-motion-snap.py` (`M1`) — hạt ánh sáng trượt dọc đường cong Bézier đang hoạt động |
| `window.__vibeSeek(stepOrSec)` | Nhảy tất định tới nhịp `0..4` (Diorama) hoặc bước `0..N-1` (Workflows) | `scripts/wms-motion-snap.py` (`M4`) |
| `@media (prefers-reduced-motion: reduce)` | Tắt mọi `animation` và rút `transition-duration` về `0.01ms` | `scripts/wms-motion-snap.py` (`M4`) |

## 5. Chưa xác minh được

- Độ hiển thị sub-pixel của viền nét đứt Risograph (`1.5px dashed`) trên màn hình Android mật độ điểm ảnh thấp (`1.5x DPR`).
- Cross-vendor model review (Claude ↔ Gemini) — no human external verifier ran.
