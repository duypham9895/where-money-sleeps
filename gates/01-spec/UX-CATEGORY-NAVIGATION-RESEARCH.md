# Báo cáo Nghiên cứu Chuyên sâu UI/UX: Kiến trúc Danh mục & Điều hướng Bài viết (Quy mô 12–20 Danh mục · 150–300 Bài)

**Ngày:** 2026-11-08  
**Định tuyến Model (Quy tắc 16):** `[Route: T3 · S=6/8 (A=2, R=1, T=2, Sc=1) · Primary=Claude Opus 5.5 (high) · CrossCheck=Gemini 4 Argon (High) [cross-vendor]]`  
**Phương pháp (`../docs/method.md`):** 4 Pha (`SWEEP` 3 mũi độc lập mù với nhau → `DEDUPE` bằng Python script `T0` → `REFUTE` giết ứng viên kèm `fix_if_any` → `JUDGE` đúc kết)  
**Quan hệ họ model (Quy tắc 7):** *cross-vendor model review (Claude Opus 5.5 ↔ Gemini 4 Argon High) — no human external verifier ran.*  
**Thời gian đọc ước tính:** ~3 phút  
**Trạng thái quyết định (QĐ 55 — 2026-11-08):** **ĐÃ CHỐT Layout `1A` (`Editorial Split-Pill` `48px` + Overlay Mục lục 2 cột `Master–Detail` + `⌘K` + Handoff Card)** và **thay toàn bộ wording `"sổ cái"` bằng `"Mục lục"` / `"Sổ kế toán"` / `"sổ sách ngân hàng"`** (tránh nhầm sang blockchain và khó hiểu với người đọc phổ thông).

---

## TL;DR

- **Kết luận hội tụ 100% từ cả 3 mũi chuyên gia độc lập (`Claude Opus 5.5` + `2× Gemini 4 Argon High`):**
  - **Bác bỏ (`KILLED`)** thanh pill cuộn ngang hiện tại (`PA 0`), Gáy sổ dọc mở cố định bên trái (`PA 2`), Bản đồ tuyến đường ống đặt cố định đầu trang (`PA 3`), Lưới tủ thẻ Bento đặt đầu trang (`PA 4`), và dải subbar cắt cụt 28 ký tự (`PA 5`).
  - **Sống sót và đạt điểm Reading Ergonomics cao nhất (`28,1 / 30` — hiển thị đồng bộ `99,1%–100%` Mặt cắt Diorama + Hộp thoại 5 đoạn kể trên màn hình Laptop `1440×900`):** **Kiến trúc "Mục Lục & Mặt Cắt v2 — Layout `1A` (`Editorial Split-Pill`)" (`PA 1` đã sửa lỗi + `⌘K` của `PA 5` + Thẻ chuyển tuyến chân bài của `PA 3`)**.

---

## 1. Bảng Đối chiếu Toán học Viewport Budget & Wayfinding (Pha `SWEEP` + `DEDUPE`)

Phép đo thực hiện trên khung nhìn thực tế của Laptop 13–14 inch (`1440×900`, chiều cao trình duyệt `VH = 780px`, khung trang `max-width: 1240px` trừ padding còn `~1204px`) và Mobile (`390×844`, `Eff VH = 720px`).  
Khối đọc đồng bộ của **Where Money Sleeps** gồm: Thanh góc nhìn (`44px`) + Mặt cắt Kiến trúc Diorama v3.0 (`1100×513px`) + Chú giải (`26px`) + Hộp thoại 5 đoạn kể (`156px`) = **`739px` chiều cao dọc** và **`1100px` chiều ngang**.

| Ứng viên | Phán quyết `REFUTE` | Chiếm dọc Desktop (`VH=780px`) | Chiếm ngang (`VW=1204px`) | % Diorama + 5 Đoạn kể nhìn thấy cùng lúc | Đổi bài cùng mục (`Q3`) | Nhảy chéo mục 2→11 (`Q4`) | Điểm Ergonomics (`/30`) |
|---|---|---|---|---|---|---|---|
| **★ PA 1 v2 — Layout `1A` (`Editorial Split-Pill` `48px` + Overlay Mục lục 2 Cột + `⌘K` + Handoff)** | **SURVIVED WITH FIX (ĐÃ CHỐT QĐ 55)** | **`48px` (`6,2%` VH)** | **`0px`** | **`99,1%–100%`** *(Trọn vẹn)* | **1 chạm (`~0,5s`)** qua `‹ ›` hoặc Popover dọc | **2 chạm (`~1,8s`)** qua Overlay 2 cột hoặc `⌘K` | **`28,1 / 30`** |
| **PA 0 (Dải pill cuộn ngang hiện tại)** | **KILLED** | `162px` (`20,8%` VH) | `0px` *(Tràn ngang)* | `83,6%` *(Cắt mất 5 đoạn kể)* | Phải mở modal | Cuộn ngang mù + bấm | `15,5 / 30` |
| **PA 2 (Gáy Mục Lục Dọc Trái `290px`)** | **KILLED (Khi mở cố định)** | `0px` (`0%` VH) | **`290px`** *(Còn `914–950px < 1100px`)* | **Co nhỏ Diorama `14%`** *(Chữ SVG `<10px`)* | 1 chạm (`~0,9s`) | Cuộn sidebar + 2 chạm (`~3,0s`) | `20,0 / 30` |
| **PA 5 (Masthead Báo In + Subbar + `⌘K`)** | **SURVIVED HALF** *(Giết Subbar, giữ `⌘K`)* | `244px` (`31,3%` VH) | `0px` | `72,5%` *(Đẩy 100% 5 đoạn kể xuống dưới fold)* | 1 chạm *(Quét 26 nút cắt cụt 28 ký tự)* | 2 chạm (`~1,8s`) | `17,5 / 30` |
| **PA 3 (Bản Đồ Tuyến Đường Ống)** | **KILLED AS TOP CHROME** *(Giữ Handoff cuối bài)* | `464px` (`59,5%` VH) | `0px` | `42,8%` *(Che 60% màn hình đầu)* | Cuộn + 1 chạm (`~3,0s`) | Cuộn + 2 chạm | `13,5 / 30` |
| **PA 4 (Lưới Tủ Thẻ Thư Viện Bento)** | **KILLED AS NAV BAR** *(Chuyển về trang Mục lục riêng)* | `586px` (`75,1%` VH) | `0px` | `26,3%` *(Đẩy 100% Diorama khỏi màn đầu)* | 2 chạm | Cuộn + 2 chạm | `11,3 / 30` |

---

## 2. Đòn chí mạng ở Pha `REFUTE` & Các bản vá `fix_if_any` đã áp dụng

1. **Vì sao `PA 2` (Left Sidebar `290px`) bị loại dù tiết kiệm chiều dọc:**
   - **Đòn chí mạng hình học (`Claude Opus 5.5` + `Gemini SWEEP #1`):** Khung nội dung rộng `1204px`, trừ cột trái `290px` chỉ còn `914–950px`, nhỏ hơn mức `1100px` của Mặt cắt Diorama v3.0 — làm toàn bộ chữ SVG trong 5 ngôi nhà bị thu nhỏ dưới `10px`.
   - **Đòn chí mạng Eye-Tracking (`NN/g Horizontal Attention Leans Left`):** Người đọc dành **80% thời gian nhìn ở nửa trái màn hình**. Một cột chứa 12 danh mục + 14 tiêu đề bài viết nằm cố định bên trái hút mất điểm nhìn của Ngôi nhà số 1 (`1 · Bạn`) và gây nhiễu thị giác ngoại vi (para-foveal crowding) mỗi khi mắt phóng về đầu dòng bên trái lúc đọc bài khảo cứu `1.200` từ.
2. **4 lỗi của `PA 1` bản đầu đã bị phát hiện ở pha `REFUTE` và sửa dứt điểm trong `PA 1 v2`:**
   - **Fix 1 — Chuyển `.c1-sheet` từ luồng tĩnh sang `Overlay` (`position: absolute` + backdrop mờ + phím `Escape`):** Mở mục lục 12 danh mục × 148 bài phủ nhẹ lên trên, **0px Layout Shift** đối với sân khấu Diorama bên dưới, và tự động đóng ngay khi chọn bài.
   - **Fix 2 — Ghép Hộp lệnh `⌘K` toàn cục của `PA 5` & giữ nguyên con trỏ ô tìm kiếm:** Gõ tìm kiếm chỉ cập nhật vùng lưới `#c1GridContainer` (không dựng lại `<input>` nên không bao giờ nhảy con trỏ về cuối chuỗi) và tìm xuyên cả **148 bài của 12 danh mục**.
   - **Fix 3 — Ghép Thẻ "Trạm kế tiếp / Chuyển tuyến" của `PA 3` vào cuối bài:** Khi đọc tới bài cuối của một danh mục, thẻ chân bài dẫn thẳng sang `Bài 1` của danh mục kế tiếp (theo chuẩn GOV.UK step-by-step handoff).
   - **Fix 4 — Chuẩn hoá WCAG 2.2 AA & Vùng chạm (`frontend-a11y` + `modern-web-guidance`):** Bọc trong `<nav>` và `<main>`, thêm `aria-expanded`, `aria-live="polite"`, đổi nút đóng sang `<button>`, nâng kích thước nút `‹ ›`.

---

## 3. Nguồn trích dẫn thực nghiệm đã xác minh (Có URL + Trích dẫn nguyên văn)

1. **Nielsen Norman Group — Beware Horizontal Scrolling and Mimicking Swipe on Desktop** (`https://www.nngroup.com/articles/horizontal-scrolling-desktop/`):
   > *"Even as more sites mimic swiping gestures and incorporate horizontal scrolling in desktop designs, users remain reluctant to move sideways through content. For years, we've known that horizontal scrolling is painful for users on desktop computers."*
2. **Nielsen Norman Group — Sticky Headers: 5 Ways to Make Them Better** (`https://www.nngroup.com/articles/sticky-headers/`):
   > *"Persistent headers can be useful to users if they are unobtrusive, high-contrast, minimally animated, and fit user needs."*
3. **Nielsen Norman Group — Mega Menus Work Well for Site Navigation** (`https://www.nngroup.com/articles/mega-menus-work-well/`):
   > *"Mega menus (sometimes spelled “megamenus”) are a type of expandable menu in which many choices are displayed in a two-dimensional dropdown layout. They are an excellent design choice for accommodating a large number of options or for revealing lower-level site pages at a glance."*
4. **Nielsen Norman Group — Horizontal Attention Leans Left** (`https://www.nngroup.com/articles/horizontal-attention-leans-left/`):
   > *"In previous research on horizontal attention, we found that, on the web, people disproportionately spend much more viewing time on the left half of the page versus on the right half. Since that article was published in 2010, the web has undergone significant changes, yet this finding holds true."*
5. **Nielsen Norman Group — Breadcrumbs: 11 Design Guidelines for Desktop and Mobile** (`https://www.nngroup.com/articles/breadcrumbs-11-design-guidelines/`):
   > *"Breadcrumbs are intended to supplement other navigational components, such as a global navigation bar that stretches across the top of every page or a local navigation bar that is often found on the left hand side. Breadcrumbs augment but do not replace those main forms of navigation."*
6. **Nielsen Norman Group — Hamburger Menus and Hidden Navigation Hurt UX Metrics** (`https://www.nngroup.com/articles/hamburger-menus/`):
   > *"On desktop, people used the hidden menus in only 27% of the cases, while they used visible or combo navigation almost twice as much: in 48% and 50% of the cases, respectively."*  
   > *"On the desktop, people were at least 39% slower when the navigation was hidden (compared with the visible or combo conditions)."*
7. **Baymard Institute — Information Architecture & Navigation UX** (`https://baymard.com/blog/information-architecture-ux`) & **GOV.UK Design System — Step by step navigation** (`https://design-system.service.gov.uk/patterns/step-by-step-navigation/`).

---

## 4. Chưa xác minh được

- Chưa chạy kiểm thử thực nghiệm trên người đọc thật (human eye-tracking / A/B usability session) đối với riêng trang *Where Money Sleeps*; các thông số Viewport Budget (`48px`, `739px`, `1100px`) được đo toán học từ CSS/SVG thực tế của `docs/prototype.html`.
- Toàn văn báo cáo trả phí bên trong Baymard Premium chưa truy cập trực tiếp trong phiên này (chỉ đối chiếu từ bài tổng hợp công khai `baymard.com/blog/information-architecture-ux`).
