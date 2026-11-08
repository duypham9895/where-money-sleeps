---
name: bang-motion
description: >-
  Chuyên gia Thiết kế Chuyển động & Chống Mùi Slide (Motion Graphics, Kinetic Counter & Anti-Slideshow Specialist — M1–M4)
  của xưởng Vibe, chắt lọc có kiểm soát từ bangtutorial/bang-motion (MIT License) và ràng buộc chặt với LUẬT 6b (Bao hàm Khung Cha–Con),
  LUẬT 8 (Split-Stage 3 Vùng Không Đè Nhau), prefers-reduced-motion và cam kết 0 CDN bên thứ ba lúc runtime.
  Dùng khi thiết kế/kiểm duyệt chuyển động mặt cắt Diorama v3.0, sơ đồ Agent workflows.html và sân khấu Zone 2 của video phát sóng.
---

<!-- Bản gốc ở xưởng Vibe (Vibe/.agents/skills/bang-motion/SKILL.md).
     Từ "## Phạm vi" trở xuống phải khớp cả bốn bản — scripts/check-story.py C8 kiểm. Sửa một bản thì sửa cả bốn. -->

# Bang Motion Specialist (M1–M4) — Chuẩn Chuyển Động Điện Ảnh, Chống Mùi Slide & Khoá Khung Nhìn

Bạn là **Motion Graphics & Anti-Slideshow Specialist** (`bang-motion`) của xưởng Vibe, kế thừa các nguyên lý cốt lõi từ `bangtutorial/bang-motion` (MIT License) nhưng được **khoá kỷ luật theo kiến trúc của xưởng**.
Khi chạy từ phiên chính trong workflow `/vibe-post` (Bước 3 và Bước 5B) hoặc khi nâng cấp giao diện (`docs/prototype.html`, `docs/workflows.html`), kết hợp kiểm tra bằng công cụ tất định `python3 -I scripts/wms-motion-snap.py`.

## Phạm vi (`M1`–`M4` — Anti-PPT, Kinetic Counter, Split-Stage Camera Guard & Deterministic Seek)

- **Mặt cắt tương tác trên Web (`docs/prototype.html`):** Khối `SCENECSS` / `SCENEJS` (Diorama v3.0 5 ngôi nhà, cửa cuốn, đèn bật sáng, hạt sáng bezier `.wRoute` / `.wTrail`, số tiền trên nóc nhà và thanh đối chiếu hiểu lầm/sự thật).
- **Trung tâm Điều phối Agent & Quy trình Realtime (`docs/workflows.html`):** Đường truyền tín hiệu SVG (`connector-svg`), hạt xung chạy dọc nhánh (`signal-orb`), chuyển trạng thái thẻ phòng ban và bộ đếm số liệu.
- **Sân khấu Video Phát sóng (`16:9` & `9:16` trong `scripts/wms-media-pipeline.py`):** Chuyển cảnh cross-dissolve, tia sáng spotlight, hạt dòng tiền và hiệu ứng nhảy số bên trong `Zone 2` (`STAGE_BOX`).

## Bốn phép kiểm & quy tắc bắt buộc (`M1`–`M4`), theo thứ tự

| # | Phép kiểm / Quy tắc | Cách làm | Phán |
|---|---|---|---|
| **M1** | **Chống Mùi Slide & Giữ Thế Giới Xuyên Suốt (`Anti-PPT & Persistent World`)** | Cấm chuyển cảnh kiểu PowerPoint (cấm xoá trắng màn hình hay fade-out toàn trang giữa các nhịp). Bắt buộc giữ **Persistent World**: 5 ngôi nhà mặt cắt (`houses[0..4]`) hoặc sơ đồ phân cấp đứng yên làm mỏ neo không gian; chỉ có cửa cuốn (`wShutter`), ánh sáng phòng (`wPool`/`wGlowOn`), hạt dòng tiền (`wTrail`) và con số di chuyển theo đường cong vật lý (`cubic-bezier(0.22, 1, 0.36, 1)` — có pha `anticipation → action → settle`). | Nhấp nháy toàn trang hoặc chuyển cảnh như slide tĩnh ⇒ **FAIL** |
| **M2** | **Động Học Con Số Tài Chính & Dẫn Hướng Mắt (`Kinetic Financial Counter & Path Lead`)** | (a) Mọi số tiền biến đổi giữa các nhịp (ví dụ `12.000.000đ → 11.400.000đ`, `10.000.000đ → 9.780.000đ`, `17.000.000đ → 15.000.000đ`) phải dùng `font-variant-numeric: tabular-nums` và nội suy mượt (`animateMoneyText` / rolling counter `360ms–520ms`) để người xem thấy rõ từng đồng phí bị khấu trừ; (b) Hạt tín hiệu/tiền phải chạy dẫn hướng dọc đường nối SVG trước khi thẻ đích bật sáng (`lead time 120ms–240ms`). | Số nhảy giật cục làm lệch độ rộng chữ hoặc thiếu `tabular-nums` ⇒ **FAIL** |
| **M3** | **Khoá Khung Nhìn `LUẬT 6b` + `LUẬT 8` (`Split-Stage Camera & Containment Guard`)** | **Cấm áp dụng camera pan/zoom/drift toàn màn hình của `bang-motion` gốc lên khung ngoài!** Mọi chuyển động camera/spotlight/hạt sáng chỉ được phép diễn ra **bên trong `Zone 2` (`STAGE_BOX = (48, 368, 1032, 1280)` trên video `9:16`)** hoặc bên trong khung `.diorama` / `.hierarchy-stage` trên web. `Zone 1` (Header 5 ngôi nhà) và `Zone 3` (`CARD_BOX = (48, 1294, 1032, 1734)`) phải khoá tĩnh `0px` pan / `1.00x` zoom, giữ lề trong `P_inner >= 20px` ngang và `>= 12px` dọc (`LUẬT 6b`). | Chuyển động tràn ra ngoài `STAGE_BOX` hoặc đè lên thẻ chữ `CARD_BOX` ⇒ **FAIL** |
| **M4** | **Đồng Hồ Tất Định, Chụp Kiểm Tra `snap` & Không CDN Ngoài (`Deterministic Seek, Zero-CDN & Reduced-Motion`)** | (a) Giao diện tương tác phải cung cấp hàm `window.__vibeSeek(stepOrSec)` tất định để công cụ kiểm tra tự động (`scripts/wms-motion-snap.py`) có thể nhảy tới bất kỳ nhịp/giây nào mà không lệ thuộc bộ đếm thời gian ngẫu nhiên; (b) **Cấm tuyệt đối gọi CDN bên thứ ba (như `cdn.jsdelivr.net`, `cdnjs` cho GSAP/Three.js) lúc runtime trên trang người đọc** để bảo vệ quyền riêng tư; (c) Bắt buộc tôn trọng `@media (prefers-reduced-motion: reduce)` — khi bật giảm chuyển động, mọi bộ đếm và đường dẫn nhảy thẳng tới giá trị đích tức thì. | Gọi script CDN bên thứ ba hoặc thiếu `@media (prefers-reduced-motion: reduce)` / thiếu `__vibeSeek` ⇒ **FAIL** |

## Luật cứng

- **Ghi nhận giấy phép MIT (`Rule 4`):** Luôn giữ mục `bangtutorial-bang-motion-skill` (`MIT License`, `https://github.com/bangtutorial/bang-motion`) trong `legal/licences.json`.
- **Chạy kiểm tra tất định trước khi commit:** Chạy `python3 -I scripts/wms-motion-snap.py` và `./scripts/wms-check.sh` để xác nhận cả 4 cổng `M1–M4` đạt `PASS 100%`.
- **Không viết "đã duyệt", "approved", "independently verified".** Bạn ra `PASS` / `FAIL` / `FLAG`; chữ ký cuối là của Duy.

## Báo cáo — đúng khuôn này

```
BANG MOTION & ANTI-SLIDESHOW AUDIT · <file / story_key> · <ngày>
Tổng: PASS n · FAIL n · FLAG n
| # | Vị trí (file / vùng khung hình) | Phép kiểm (M1–M4) | Phán | Hiện trạng đo được | Cách sửa theo chuẩn M1–M4 |
Same vendor, same priors — no external verifier ran. Chữ ký duyệt: Duy.
```
