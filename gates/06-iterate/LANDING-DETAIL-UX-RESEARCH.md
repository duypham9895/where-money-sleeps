---
status: proposal
stage: 06-iterate
date: 2026-11-14
owner: design+pm
---

# Báo cáo Nghiên cứu Sâu UI/UX, Typography, Màu sắc & Behavior (`v2`): `Landing Hub → Article Detail → 3 Bài Đọc Tiếp Nối Mạch → Từ Điển Thu Gọn` (`where-money-sleeps`)

**Định tuyến Model (Quy tắc 16):** `[Route: T3 · S=5/8 (A=1, R=1, T=2, Sc=1) · Primary=Gemini 4 Argon High · CrossCheck=Python T0 + wms-check.sh]`  
**Quan hệ họ model (Quy tắc 7):** *same vendor, same priors — no external verifier ran.*  
**Thời gian đọc ước tính:** ~5 phút  
**Mockup Prototype Độc lập cho Từng Phương án (`7 / 20 / 60` bài):** [`docs/mockup-option-a.html`](../../docs/mockup-option-a.html) (Phương án A) · [`docs/mockup-option-b.html`](../../docs/mockup-option-b.html) (Phương án B) · Bản tổng hợp gốc: [`docs/landing-detail-mockups.html`](../../docs/landing-detail-mockups.html)

---

## TL;DR

- **Chẩn đoán bản mẫu `v1` & Hiện trạng `docs/prototype.html`:** Bản gốc `docs/prototype.html` đang đổ toàn bộ ruột bài `card` và **52 thuật ngữ mở sẵn** ngay trên trang chủ `/` (`~11.800px`), trong khi bản mockup `v1` lại làm mất chất liệu *Warm Archival Risograph* (hạt giấy `feTurbulence`, sổ tay khâu gáy, hoá đơn răng cưa, sổ kế toán kẻ dòng, kệ gỗ 3D), lạm dụng sans-serif đậm và đóng khung viền đen dày quanh bài đọc.
- **Giải pháp Senior UI/UX `v2` (Kiến trúc + Craft + Behavior — Đã nạp 100% chi tiết bài gốc):**
  1. **Tách `Landing Hub` (`/`) khỏi `Article Detail` (`/?story=<slug>`):** Landing sạch 0% nội dung bài chi tiết (đo thật trên desktop `1440×900`: **`3.383px`**, giảm ~71% so với `~11.800px`), giữ trọn chất liệu biên tập (`Hero` điện thoại `22:47` & hoá đơn `.slip` + 3 câu hỏi serif + Lưới 7 cuốn sổ tay + Kệ gỗ `.shelf` + Ngăn kéo Từ điển đóng). Trang Detail đã nạp **100% chi tiết đầy đủ cho cả 7 bài** từ [`docs/prototype.html`](../../docs/prototype.html), với bài **`card`** làm mẫu duyệt bố cục hoàn chỉnh (`12.848px` desktop / `20.698px` mobile): 5 lát cắt sân khấu + Audio Giọng Tâm (`public/audio/<slug>-beats.mp3`) & transcript + Máy tính tách phí MDR/Interchange + Bài khảo cứu C9 Tab A (`1.197` từ, 5 chương, 4 tranh 16:9 `1200×675` tại `public/brand/` theo LUẬT 9, sơ đồ 7 mốc, bảng 5 vai) & Tab B (`1.450` từ TT 99/2025, 4 bút toán kép, 4 ngoại lệ, bỏ hoàn toàn `ol.asks` câu hỏi mở).
  2. **Khôi phục 3 tầng Typography & Màu sắc giấy Risograph:** Văn bản đọc dài đặt trực tiếp trên nền `--paper` (`#f3ebdd` ngày / `#15161f` đêm) phủ hạt giấy SVG, cỡ gốc `19px` `Newsreader` (`font-optical-sizing: auto`), bề rộng cột `--read: min(40rem, 92vw)` (`~62ch`, chuẩn 45–75 ký tự/dòng), số tiền `tabular-nums`, bỏ khung viền đen dư thừa quanh bài đọc.
  3. **Quiz Card kiểm chứng cuối bài + Bố cục bất đối xứng `1 + 2` (`Narrative Triad`) & 6 chuẩn Behavior (`B1–B6`):** Thay danh sách câu hỏi mở tĩnh cuối bài bằng **2 Thẻ Quiz (`WMS_QUIZ_BANK`)** có giải thích tại chỗ + trích dẫn bài viết, tự đánh dấu hoàn thành bài trước khi nối sang 3 bài gợi ý `1 + 2` (Thẻ #1 *Tiếp mạch* ngang + 2 thẻ đối xứng) và nối thông 2 chiều `.term` ↔ `#pop` ↔ `<details id="glDrawer">` (đóng mặc định `52px`, đủ **52 thuật ngữ**, lọc chính xác `20` từ xuất hiện trong toàn bài `card`).
  4. **Giả lập quy mô kho bài (`7 / 20 / 60` bài) & 3 chế độ hiển thị Landing:** Mặc định mở ở **`20` bài** (cho phép chuyển tức thì giữa **`7`**, **`20`** và **`60` bài** trên `.ux-lab-dock` hoặc `?scale=7|20|60`), kèm ô tìm nhanh `#landingSearch`, bộ chọn `#gridModeSeg` (`curated` phân trang chuẩn `6 bài/trang` / `flat` Đổ phẳng tất cả / `compact` Mục lục nén 7 nhánh), thanh `<nav id="catalogMoreBar" aria-label="Phân trang danh sách bài viết">` đánh số trang chuẩn (`‹ Trước 1 2 3 4 … Tiếp ›` với `aria-current="page"`), và chặn chiều cao `#postPop` (`max-height: min(52vh, 320px)`). Chế độ phân trang `curated` (`6 bài/trang`) giữ chiều cao Landing **cố định `~3.002px` desktop / `~7.070px` mobile** dù kho tăng lên `60` bài (thay vì phình tới `10.903px` / `33.672px` nếu đổ phẳng).

---

## 1. Đo đạc Viewport Budget & Đối chiếu Kiến trúc

| Chỉ số trải nghiệm | Hiện trạng (`docs/prototype.html`) | Thiết kế mới `v2` (`Landing` ⇄ `Detail` đủ 100%) | Tác động UX đo được |
|---|---|---|---|
| **Chiều dài trang Landing (`/`)** | `~11.800px` (dính toàn bộ ruột bài `card` + 52 thuật ngữ mở) | **`3.383px`** desktop (`1440×900`, Hero + 3 câu hỏi + 7 thẻ sổ tay + Kệ gỗ + Từ điển đóng) | Giảm **~71%** chiều cao cuộn trang chủ; 0% nội dung bài chi tiết lọt ra Landing |
| **Độ đầy đủ Page Detail (`?story=card`)** | Toàn bộ ruột bài trộn chung vào trang chủ | **`12.848px`** desktop / **`20.698px`** mobile (đủ 5 lát cắt, Audio, Máy tính MDR, Tab A 5 chương + 4 tranh `1200×675` + 7 mốc + 5 vai, Tab B 4 bút toán + 4 ngoại lệ, 2 Quiz + 3 gợi ý) | Duyệt trọn vẹn nhịp đọc thật của 1 bài hoàn chỉnh tách riêng khỏi Landing |
| **Chiều dài mục Giải nghĩa từ khi vào trang** | `~1.650px` (mở toang toàn bộ 52 thuật ngữ) | **`52px`** (1 bìa hồ sơ `<details>` đóng mặc định ở cả Landing & Detail) | Giảm **96%** chiều cao chân trang; không làm gãy nhịp chuyển sang 3 bài đọc tiếp |
| **Kiểm chứng kiến thức cuối bài** | Câu hỏi tự suy ngẫm mở (`ol.asks`) tách rời | **2 Thẻ Quiz tương tác (`WMS_QUIZ_BANK`)** đặt ngay giữa bài đọc và 3 bài gợi ý | Đo ngay độ hiểu cơ chế + trích nguyên văn đoạn bài liên quan, tự mở khoá trạng thái Đã đọc |
| **Cụm gợi ý cuối mỗi bài viết** | 1 hộp chuyển bài tuần tự (`nextKey`) | **3 bài nối mạch theo cấu trúc `1 Featured Lead + 2 Companion`** | Cho chiều ngang rộng rãi cho tiêu đề 3 mỏ neo + câu *Bridge Reason*, chống mỏi quyết định |
| **Thanh điều khiển & URL** | `history.replaceState` ngay khi tải trang | `history.pushState` chuyển `/` ⇄ `/?story=<slug>` + `popstate` + `startViewTransition` | Nút Back trình duyệt quay đúng về Landing; không có thanh debug đè lên `.atlasbar` |

---

## 2. Hệ thống Typography, Màu sắc & Chất liệu *Warm Archival Risograph*

| Tầng thiết kế | Quy chuẩn bắt buộc (khôi phục từ `docs/prototype.html`) | Lý do UI/UX & Thẩm mỹ |
|---|---|---|
| **Tầng 1 · Chữ đọc & Tiêu đề (`--serif`)** | `Newsreader` (`optical-sizing: auto`), gốc `19px / 1.6`, đoạn văn `.prose` `1.08rem / 1.7` với Drop-cap chương đầu `3.3em` màu `--clay`, `<dt>` từ điển dùng **serif nghiêng (`font-weight: 500`)** | Phản ánh đúng tinh thần báo in & sổ tay phân tích dài; `font-optical-sizing` giữ nét chữ mảnh mai ở `h1` (`clamp(2.3rem, 5.6vw, 4.1rem)`) và chắc khỏe ở `16–19px` |
| **Tầng 2 · Chữ điều hướng & Nhãn (`--sans`)** | `Be Vietnam Pro` (`400/500/600`), chỉ dùng cho `.atlasbar`, pill lọc danh mục, nút bấm, nhãn phụ và giải thích *Bridge Reason* (`12.5–14px`) | Tách bạch tức thì lớp "cơ chế điều khiển" (khả năng quét nhanh) khỏi lớp "nội dung câu chuyện" (khả năng đọc sâu không mỏi mắt) |
| **Tầng 3 · Con số & Bút toán (`--mono` + `.num`)** | `ui-monospace` kết hợp `font-variant-numeric: tabular-nums; font-feature-settings: "tnum" 1` cho đồng hồ `22:47`, hoá đơn `.slip` / `.receipt`, số hiệu tài khoản `TT 99/2025` | Các cột tiền `Debit` / `Credit` thẳng hàng tuyệt đối, vượt bài kiểm *I–L–1* khi đối chiếu số liệu tài chính |
| **Cấu trúc Vùng đọc & Vật liệu** | Bề rộng bài đọc tối đa `--read: min(40rem, 92vw)` (`~60–65ch`); đặt trực tiếp lên `--paper` (`#f3ebdd` / `#15161f` đêm) phủ hạt SVG `feTurbulence`; chỉ đóng khung **vật phẩm vật lý** (`.story` có đường chỉ khâu gáy, `.ledger` giấy kẻ dòng, `.receipt` răng cưa) | Tuân chuẩn *Practical Typography* (45–75 CPL); bỏ viền đen dày ở khối chữ dài giúp giảm nhiễu thị giác rõ rệt |

---

## 3. 6 Hành vi Tương tác Cốt lõi (`B1–B6` Behavioral UX Specifications)

| Mã | Hành vi (Behavior Spec) | Trạng thái & Chuyển đổi cụ thể |
|---|---|---|
| **`B1`** | **Thanh `.atlasbar` thích nghi theo ngữ cảnh (`Adaptive Masthead`)** | Trên Landing: chỉ giữ Logo + nút `⌕ Mục lục 7 danh mục (⌘K)` + nút Ngày/Đêm (trống thoáng). Trên Detail: tự bật nút `← Trang chủ`, cụm `Split-Pill` (`Danh mục › Bài đang đọc` + popover đổi bài), 4 mỏ neo nhảy phần trong bài, và **vạch tiến độ đọc `2px` (`#readingBar`)** chạy theo phần trăm cuộn của bài. |
| **`B2`** | **Thẻ sổ tay `.story` tối ưu *Information Scent*** | Trên Landing, mỗi bài là một cuốn sổ đóng gáy (`border-left: 1.5px dashed`) hiển thị theo đúng thứ tự quét mắt: (1) Danh mục màu riêng + Thời lượng đọc + Huy hiệu `✓ Đã đọc`; (2) Tiêu đề 3 mỏ neo `Newsreader`; (3) Teaser ngắn; (4) Dải tóm tắt **5 ngôi nhà** đi qua. Khi hoàn thành bài, thẻ gắn ruy-băng vàng đánh dấu ở góc trên phải. |
| **`B3`** | **Quiz Card kiểm chứng thay câu hỏi mở & Hành trình cuối bài `1 + 2`** | Cuối bài khảo cứu: thay `ol.asks` bằng **2 Thẻ Quiz (`WMS_QUIZ_BANK`)** — bấm chọn `A/B/C` hiện ngay kết quả (`--moss` đúng / `--clay` chưa khớp), giải thích cơ chế, trích dẫn `source_quote` + nút nhảy `Đọc lại đoạn này ↑`, và tự đánh dấu `✓ Đã đọc` (kèm ưu tiên bài chưa đọc trong cụm 3 bài `1 + 2` ngay bên dưới). |
| **`B4`** | **Liên kết hai chiều: Thuật ngữ `.term` ↔ `#pop` ↔ Sổ Từ điển** | Khi bấm bất kỳ chữ gạch chấm `.term` trong bài, `#pop` neo **ngay cạnh từ đang đọc** (tự lật lên/xuống tránh tràn màn hình bằng `getBoundingClientRect()`). Trong `#pop` có nút **`"Xem trong sổ Giải nghĩa từ ↓"`** — bấm vào tự mở `<details id="glDrawer">`, chuyển về đúng bộ lọc, cuộn mượt tới dòng `<dt>` đó và phát sáng 1,5 giây. |
| **`B5`** | **Ngăn kéo Giải nghĩa từ `<details id="glDrawer">` luôn đóng mặc định** | Luôn giữ `open = false` lúc tải trang và tự động khép lại mỗi khi chuyển bài hoặc quay về Landing. Khi ở trang Detail và bấm mở: tự chọn sẵn tab **`"Trong bài đang đọc (X từ)"`** để giảm nhiễu, kèm nút 1 chạm sang **`"Tất cả 52 thuật ngữ"`**, lọc nhanh theo chữ cái/từ khoá và chip nhảy ngược tới bài có dùng thuật ngữ đó. |
| **`B6`** | **Chuyển cảnh `View Transitions` & Focus bàn phím chuẩn Accessibility** | Mọi chuyển đổi Landing ⇄ Detail đi qua `runViewTransition()` kiểm tra `document.startViewTransition` + `prefers-reduced-motion`; `history.pushState` / `popstate` giữ nút Back hoạt động như web đa trang; sau khi chuyển sang Detail luôn đưa focus về `#detailTitle` (`tabindex="-1"`). |

---

## 4. Đối chiếu Phương án UI/UX (`PA A` vs `PA B` vs `PA C`)

| Tiêu chí | ★ Phương án A: [`docs/mockup-option-a.html`](../../docs/mockup-option-a.html) *(Khuyến nghị)* | Phương án B: [`docs/mockup-option-b.html`](../../docs/mockup-option-b.html) | Phương án C: `Split-Screen Sidebar` *(Loại)* |
|---|---|---|---|
| **Landing Hub (`/`)** | Đầy đủ Hero (`22:47` + hoá đơn `.slip`), 3 câu hỏi, Pill lọc 7 danh mục, Lưới sổ tay `.story` khâu gáy (mặc định `curated` phân trang chuẩn `6 bài/trang` qua `<nav aria-label="Phân trang danh sách bài viết">` với `aria-current="page"`) + dải 5 ngôi nhà, Kệ gỗ `.shelf` (`3.000–3.002px` desktop ở trang 1) | Compact Ledger Directory Hero (`~200px`), bỏ Hero 22:47, bỏ 3 câu hỏi & Kệ gỗ; mặc định Mục lục nén 7 nhánh (`2.014px` @7, `3.265px` @20, `6.173px` @60 desktop) + Hàng ngang tối giản | Sidebar cố định bên trái luôn mở |
| **Kiểm chứng & 3 Bài Gợi Ý** | **2 Thẻ Quiz kiểm chứng (`WMS_QUIZ_BANK`)** có trích dẫn `source_quote` + Cụm `1 + 2` (`1102px` / `541px`) có *Bridge Reason* và ưu tiên bài chưa đọc | Chỉ **1 Thẻ Quiz** rút gọn (ẩn trích dẫn `source_quote`) + **Lưới 3 cột đồng hạng (`354px × 3`)**, ẩn *Bridge Reason* | Đặt trong tab phụ |
| **Ngăn kéo Giải nghĩa từ** | Đóng mặc định (`52px`). Khi mở có 2 tab (`Trong bài: 20 từ` / `Tất cả 52 từ`), lọc nhanh + định vị từ từ `#pop` + chip bài viết | Đóng mặc định (`52px`). Khi mở đổ thẳng bảng tra cứu A–Z **52 từ phẳng** + ô tìm `#glSearch` (ẩn tab lọc & chip bài viết) | Đặt trong tab phụ |
| **Lý do chọn / loại** | Giữ trọn hồn *Warm Archival Risograph* của `docs/prototype.html`, Landing cố định `3.110px` dù lên `60` bài và tối đa **Information Scent** | Tối ưu tra cứu nhanh kiểu danh bạ (thấy ngay nhóm 01 ở màn hình đầu), nhưng giảm mạch kể chuyện và lên `16.155px` mobile ở `60` bài | **KILLED:** Phá tỷ lệ Mặt cắt Diorama và vi phạm QĐ 55 (`UX-CATEGORY-NAVIGATION-RESEARCH.md`) |

---

## 5. Ma trận Gợi ý 3 Bài Đọc Tiếp Nối Mạch (`NEXT_TRAIL_MAP` cho 7 bài hiện có)

| Bài đang đọc | ★ 1 · Tiếp mạch câu chuyện (`continue`) | 2 · Đối chiếu cùng cơ chế (`contrast`) | 3 · Mở rộng hệ thống (`expand`) |
|---|---|---|---|
| **`card`** *(Quẹt thẻ 10 triệu)* | **`minpay`** — *Bạn vừa thấy đêm T+0 và T+2 tiền về quán; tới Ngày 45 sao kê, chuyện gì xảy ra nếu chỉ trả tối thiểu 5%?* | **`qr`** — *Cũng tại quán quen, đổi từ quẹt thẻ (Pull) sang quét mã QR (Push): vì sao 220.000 đ phí biến mất?* | **`install`** — *Từ thẻ tín dụng sang mua trả góp 0%: ai đang trả thay phần lãi và lãi suất thực là bao nhiêu?* |
| **`pay`** *(Lương 15 triệu nằm yên)* | **`offus`** — *Vì sao công ty thích trả lương cùng ngân hàng (On-Us), và chuyện gì xảy ra khi bạn chuyển sang ngân hàng khác?* | **`profitcash`** — *Trên sổ công ty, 500 triệu bảng lương tháng 12 chưa chi đang nằm đâu trên bảng cân đối ngày 31/12?* | **`qr`** — *Ngân hàng miễn phí chuyển khoản QR cho cả bạn lẫn quán để giữ chính bể vốn CASA ~0,1%/năm này.* |
| **`install`** *(Trả góp 0% · 12 triệu)* | **`minpay`** — *So sánh trực diện: lãi ẩn ~10%/năm của trả góp 0% khác gì cái bẫy ~42,6%/năm khi trả tối thiểu thẻ?* | **`card`** — *Đặt cạnh đêm quẹt thẻ: công ty tài chính trừ 5% ngay T+1 còn thẻ trừ 2,2% MDR sau T+2 khác nhau thế nào?* | **`profitcash`** — *Vì sao cửa hàng chấp nhận mất 600.000 đ để thu tiền tươi về TK 112 ngay thay vì tự giữ công nợ TK 131?* |
| **`minpay`** *(Trả tối thiểu 5% thẻ)* | **`install`** — *Cũng chia nhỏ khoản mua thành nhiều tháng: chuyển sang trả góp 0% hay giữ dư nợ tuần hoàn, bên nào đắt hơn?* | **`card`** — *Quay lại gốc rễ đêm quẹt thẻ: ngân hàng đã ứng tiền thật cho quán từ T+2 trước khi đòi bạn ở Ngày 45.* | **`pay`** — *Soi hai đầu bảng cân đối ngân hàng: bạn gửi lương CASA nhận 0,1%/năm nhưng chậm trả thẻ chịu 36%/năm.* |
| **`qr`** *(Quét mã QR 50.000 đ)* | **`offus`** — *Mổ xẻ tầng hầm của 3 giây quét QR: hạn mức ký quỹ bảo chứng và phiên bù trừ ròng 30 tỷ cuối ngày.* | **`card`** — *Đặt cạnh quẹt thẻ tại cùng quán ăn: Thanh toán Đẩy qua số dư vs Thanh toán Kéo qua mạng lưới thẻ 4 bên.* | **`pay`** — *Nguồn tiền gốc chảy qua mã QR đến từ chính số dư CASA mà bài bảng lương đã giải phẫu.* |
| **`profitcash`** *(Lãi 2 tỷ · Két còn 50 triệu)* | **`offus`** — *Chiều 31/12 công ty chuyển khoản 20 triệu trả nhà cung cấp nhưng bị treo đối soát: hạch toán TK 113 ra sao?* | **`pay`** — *Nhìn lại khoản 500 triệu lương tháng 12 chưa chi (TK 334) từ phía người nhận lương và ngân hàng giữ vốn.* | **`install`** — *Nếu bán hàng trả chậm làm cạn tiền mặt, vì sao cửa hàng chọn bán trả góp qua công ty tài chính để thu tiền về ngay?* |
| **`offus`** *(Chuyển khoản 20 triệu On-Us vs Off-Us)* | **`qr`** — *Ứng dụng trực tiếp hạ tầng chuyển tiền nhanh 24/7 ra quầy thu ngân: vì sao loa báo tiền về sau 3 giây với 0 đồng phí?* | **`pay`** — *Giải thích trọn vẹn lý do ngày đầu đi làm, công ty yêu cầu bạn mở tài khoản nhận lương cùng ngân hàng (On-Us).* | **`profitcash`** — *Đặt lệnh chuyển khoản treo cuối năm (TK 113) vào bức tranh tổng thể Báo cáo lưu chuyển tiền tệ.* |

---

## 6. Kết quả Giả lập Quy mô Kho bài (`7` vs `20` vs `60` bài & 3 Chế độ Landing)

Đo trực tiếp trên Chromium headless (`1440×900` desktop & `390×844` mobile, 0 lỗi console, 0 lỗi trang, 0 tràn ngang `ox: false`) khi bật công tắc quy mô trên [`docs/landing-detail-mockups.html`](../../docs/landing-detail-mockups.html):

| Quy mô kho bài (`scale`) | Trạng thái danh mục | `curated` *(Mặc định: Phân trang `6 bài/trang`)* | `flat` *(Đổ phẳng toàn bộ thẻ `.story`)* | `compact` *(Mục lục nén 7 nhánh)* |
|---|---|---|---|---|
| **`7` bài** *(Kho thật)* | `7/19` (`4/7` danh mục mở) | **`~3.000px`** desktop · `~6.793px` mobile (`2` trang: `6 + 1`) | `3.523px` desktop · `7.391px` mobile (`7` thẻ, dư 1 thẻ lẻ) | `3.144px` desktop · `6.031px` mobile (`7` hàng) |
| **`20` bài** *(Mở đủ 7 nhánh)* | `20/20` (`7/7` danh mục mở) | **`~3.002px`** desktop · `~7.070px` mobile (`4` trang: `6+6+6+2`) | `5.245px` desktop · `13.751px` mobile (`20` thẻ) | `4.395px` desktop · `9.433px` mobile (`20` hàng) |
| **`60` bài** *(Kho dài hạn)* | `60/60` (`7/7` danh mục mở) | **`~3.002px`** desktop · `~7.070px` mobile (`10` trang `‹ 1..5 … 10 ›`) | `10.903px` desktop · `33.672px` mobile (`60` thẻ, gấp **`4,8×`**) | `7.303px` desktop · `18.584px` mobile (`60` hàng) |

- **Vấn đề khi chỉ "đổ phẳng" ở 20–60 bài:** Ở mobile `390×844`, chế độ `flat` phình từ `7.391px` (`7` bài) lên `13.751px` (`20` bài) và **`33.672px`** (`60` bài), biến Landing thành tường thẻ cuộn dài gấp `37×` chiều cao màn hình và đẩy `#glDrawer` xuống quá sâu. Ở `scale=7`, `flat` còn tạo hàng lẻ đơn độc ở thẻ thứ 7.
- **Lý do chọn `curated` (mặc định phân trang chuẩn `6 bài/trang` phủ đa danh mục ở trang 1) kết hợp `#landingSearch` + `<nav id="catalogMoreBar">` + `compact` + `#atlas ⌘K`:**
  1. **Giữ Landing bất biến theo quy mô:** Desktop đứng ở **`3.000–3.002px`**, mobile **`6.793–7.070px`** trên từng trang (`6 bài/trang`) dù kho có `7`, `20` hay `60` bài; giữ mặt bằng trang gọn ổn định.
  2. **Kiểm soát chiều cao popover điều hướng bài (`#postPop`) & từ điển (`#glDrawer`):** Khi mở bài giả lập tầng sâu (`?story=s45_vendorcredit&scale=60`), `#postPop` hiển thị đúng `Bài 7/8` (`8` mục) nhưng bị giữ trần `320px` (`max-height: min(52vh, 320px); overflow-y: auto`) không tràn màn hình; chip ngược trong từ điển gọn tối đa tag hiển thị kèm `+8 bài khác` (`glMoreTags: 8`).
  3. **Bảo toàn 100% đường tìm kiếm & duyệt toàn kho:** Bấm thanh phân trang chuẩn (`‹ Trước 1 2 3 4 … Tiếp ›` ở `#catalogMoreBar`), gõ `#landingSearch`, chuyển sang `compact`, hoặc bấm `⌘K` (`#atlas`: `Mục lục chủ đề: 7 danh mục · 60 bài`, đủ `60` mục, `ox: false`) đều truy cập tức thì tới từng bài.

---

## 7. Nguồn dẫn Chứng cứ UI/UX & Typography (Citations nguyên văn)

1. **Nielsen Norman Group — *How Users Read on the Web & Long-Form Scannability*** (`https://www.nngroup.com/articles/how-users-read-on-the-web/`): Người đọc quét trước khi đọc sâu; phân tầng H2/H3 rõ ràng và giảm khối bao thừa giúp tăng tốc độ định vị thông tin.
2. **Nielsen Norman Group — *Microinteractions in User Experience*** (`https://www.nngroup.com/articles/microinteractions/`): Cặp *trigger–feedback* tức thời tại chỗ (như `#pop` mở ngay cạnh `.term` + nối xuống bảng từ điển, hoặc badge tiến độ khi trả lời câu hỏi) giữ người đọc trong dòng chảy (*flow*).
3. **Nielsen Norman Group — *Information Scent*** (`https://www.nngroup.com/articles/information-scent/`):
   > *"The user's imperfect estimate of the value that a source of information (such as a webpage or link) will deliver relative to an information need, derived from a representation of the source (such as link labels, text snippets, headings, and context)."*
4. **Nielsen Norman Group — *Accordions on Desktop & Progressive Disclosure*** (`https://www.nngroup.com/articles/accordions-on-desktop/`, `https://www.nngroup.com/articles/progressive-disclosure/`):
   > *"Progressive disclosure defers advanced or rarely used features to a secondary screen, making applications easier to learn and less error-prone."*
   > *"Use accordions when the hidden content is strictly secondary or optional... Make the entire header clickable... caret icons (arrow/chevrons) work best to signal an expandable/collapsible section."*
5. **Practical Typography & Web.dev — *Line Length (Measure) & Font Optical Sizing***: Chuẩn bề rộng văn bản dài **45–75 ký tự/dòng** (`--read: min(40rem, 92vw)` ~62ch) kết hợp `font-optical-sizing: auto` và `line-height: 1.6–1.7` chống mỏi mắt khi đọc khảo cứu >1.200 từ.
6. **Modern Web Guidance** (`same-document-transitions`, `card`, `accordion`, `content-first-noise-reduction`): `<article>` + 1 `<button>` kéo vùng bằng `::after`; `startViewTransition()` kèm chuyển focus về `#detailTitle`; `<h2 id="gl-h">` nằm ngoài `<summary>` của `<details id="glDrawer">`.
7. **Modern Web Guidance — Forms & Validation** (`forms`, `accessibility`, `validate-input-after-interaction`): `<form>` bọc control gửi dữ liệu + `type="button"` cho nút phụ; `font-size: max(1rem, 1em)` chặn zoom iOS; `:user-invalid` + `WeakMap` dirty-field trì hoãn báo lỗi tới sau khi blur/submit kèm động bộ `aria-invalid` và `aria-describedby` chỉ trỏ sang thông báo lỗi khi không hợp lệ; thông báo kết quả bằng `role="status" aria-live="polite"`.

---

## 8. Phân tích Kệ sách (Con số 7) & Kiến trúc Footer Góp ý / Đề xuất Bài viết

### 8.1. Vì sao Kệ sách đang là `7` — và nên là bao nhiêu?

| Mốc nguồn | Nội dung thực tế trong repo | Hệ quả UX cho Kệ sách |
|---|---|---|
| **Nguồn gốc số `7`** | QĐ 52 (`2026-11-07`) khởi đầu với 6 Pillar (`P01–P06`). QĐ 53 & QĐ 54 (`2026-11-08`, `gates/ONE-PAGER.md` L64–66) tách Pillar 2 thành `c2` (*Thẻ, QR & Thanh toán*) và `c7` (*Sàn TMĐT, Ví & Trung gian*) -> tổng **7 danh mục (`c1..c7`)**. | Tiêu đề cũ viết cứng `"7 danh mục"` trong `prototype.html`; `AGENT-CMS-PIPELINE.md` L74 yêu cầu *"Không gõ số cứng (`CATEGORIES.length` suy từ dữ liệu)"*. |
| **Giới hạn nhận thức** | Định luật Miller / nhận thức phân loại đặt ngưỡng quét tức thì ở **5–7 danh mục** (tối đa 7±2 khối trên 1 hàng kệ). | Dưới 4 cột làm kệ thưa; quá 7 gáy trên 1 hàng ngang sẽ bóp hẹp chiều ngang gáy sách làm gãy chữ tiêu đề. |
| **Ngưỡng khi kho mở rộng (`20 → 60+` bài)** | **Luôn giữ `5–7` danh mục gốc trên kệ** (mở rộng bài mới vào trong 7 danh mục này qua bộ đếm bài trên gáy + thanh tiến độ đọc); **chỉ cho phép tối đa `8–9` danh mục** nếu thực sự phát sinh mảng độc lập mới (ví dụ *Thuế TNCN / Chứng khoán*) và chuyển `.shelf` sang CSS Grid đa hàng `.is-multi-row`. | Giữ được 1 hàng 7 cuốn cân đối ở viewport desktop `1440px` (`grid-template-columns: repeat(auto-fit, minmax(132px, 1fr))`), tự xuống hàng sạch trên tablet/mobile không vỡ gáy. |

### 8.2. So sánh giải pháp Ô Góp ý & Đề xuất Bài viết (về `hello@duypham.me`)

| Phương án | Cơ chế vận hành | Rào cản CSP / Bảo mật & Quyền riêng tư | Khuyến nghị & Đánh đổi |
|---|---|---|---|
| **A. Native `<form>` nhúng Footer + Endpoint nhẹ (Mockup A)** | Form 2 tab (`Đề xuất bài viết mới` / `Góp ý giao diện`), 3 chip gợi ý, tự đính kèm ngữ cảnh bài đang mở, validate `:user-invalid` + `WeakMap`; submit gửi `POST /api/feedback` (trên bản thật) kèm fallback `mailto:hello@duypham.me`. | **100% tương thích** `script-src 'self' 'unsafe-inline'; connect-src 'self'` (`scripts/wms-build-deploy.py` L152), 0 cookie/tracker (`L18` / NĐ 13/2023/NĐ-CP), 0 tên thương hiệu bên thứ ba. | **Khuyên dùng dài hạn:** Trải nghiệm liền mạch không nhảy trang; cần 1 handler nhỏ trong `cloudflare/worker.js` (kèm honeypot/Turnstile hoặc giới hạn tốc độ) để đẩy mail về `hello@duypham.me`. |
| **B. Quick-Draft `mailto:hello@duypham.me` + Copy 1 chạm (Mockup B)** | Giao diện chọn chủ đề & soạn nhanh ngay footer, tự build link `mailto:hello@duypham.me?subject=...&body=...` + nút sao chép clipboard 1 chạm. | **0 backend**, 0 rủi ro spam lên Worker, tuân thủ tuyệt đối CSP tĩnh. | **Tốt nhất nếu chưa muốn dựng `/api/feedback`:** Rủi ro UX là máy người dùng chưa cấu hình mail client mặc định (giảm nhẹ nhờ nút Copy kèm theo). |
| **Thư viện / SaaS ngoài (`Tally`, `Canny`, `Typeform`, `Userback`, `Disqus`)** | Nhúng iframe hoặc JS widget từ bên thứ ba. | **BỊ CHẶN** bởi chính sách `0 CDN / 0 script bên thứ ba` và ràng buộc không theo dõi độc giả; nặng JS và lạc tông Risograph. | **Loại bỏ.** |

---

## 9. Audit Khử "Mùi AI" (Anti-AI-Slop UI/UX Audit) & Thiết kế lại Toàn trang

Khảo sát thực tế ảnh chụp màn hình do Duy chỉ ra (`media_1794709635092_bfbc855d.png` — nút `⌕ Mục lục [60/60] [⌘K]`) và toàn bộ bề mặt UI của `mockup-option-a.html` / `mockup-option-b.html` (đối chiếu `gates/02-design/DESIGN-BRIEF.md`, ECC `frontend-design-direction`, và Modern Web Guidance):

### A. 10 điểm "Mùi AI" cần triệt tiêu tận gốc

1. **Nested-pill button (`⌕ Mục lục [60/60] [⌘K]`):** Bọc 3 lớp bo tròn lồng nhau (`border-radius: 999px` ngoài + badge `999px` tô nền vàng + `<kbd>` có khung riêng) cùng ký tự Unicode `⌕` lệch baseline. Khắc phục: bo biên tập phẳng (`3px` ở Phương án A / `0px` ô lưới ở Phương án B), biểu tượng kính lúp `<svg width="13" height="13" aria-hidden="true">` sắc nét, đếm số `tabular-nums` nền trong suốt phân tách bằng dấu `·` và nét mảnh `| ⌘K`.
2. **Dải `#optionBanner` khoe hàng trên đầu trang:** Chặn trên mắt ngay `y = 0` với nội dung tự mô tả ("Phương án A · Bản mẫu Prototype Độc lập") — vi phạm `content-first-noise-reduction`. Khắc phục: gắn `hidden` mặc định trên trang chính, dời hoàn toàn điều khiển so sánh vào thanh `.ux-lab-dock` nhỏ gọn ở chân trang.
3. **Copy tự thuật (Self-describing prompt copy):** Những cụm như `"Mô phỏng bố cục"`, `"Đoạn tóm lược cơ chế sau khi duyệt..."`, `"Mockup footer & kênh góp ý"` tự giải thích rằng trang đang là bản mẫu AI. Khắc phục: viết lại 100% thành ngữ điệu ấn phẩm tài chính tiếng Việt tự nhiên (`"Khảo cứu 5 chương"`, `"Tổng quan cơ chế"`, `"Bản in lưu trữ"`).
4. **Lạm dụng `border-radius: 999px` ("Pill-ception"):** Phát hiện ~29 quy tắc CSS bo tròn viên thuốc cho nút lọc, segmented control, tab, TOC, tag, quick chips và nút gửi footer (`Anti-Reference #1` của `DESIGN-BRIEF.md`). Khắc phục: thống nhất hệ hình học `0px–4px` theo thẩm mỹ sổ cái/báo in; dùng thanh gạch chân `2px` cho tab/filter đang chọn.
5. **Sân khấu `#secStage` mang dáng UI card SaaS:** `.house-node`, `.dio-flow-strip`, `.beat-btns` bo tròn mềm như widget dashboard. Khắc phục: nâng cấp thành **Mặt cắt Kiến trúc (Architectural Cutaway Blueprint)** với dải đầu `3px` trạng thái tĩnh/sáng đèn và **Thước thời gian 5 nhịp (5-Step Timeline Ruler)**.
6. **Hiệu ứng card "trình diễn" (`.story-card`):** Bóng đổ 3 lớp dày kèm `transform: rotate(-.35deg)` khi hover. Khắc phục: bỏ nghiêng góc và bóng dày, dùng viền mảnh (`hairline border`) + nhấn thanh biên rõ ràng.
7. **Nhãn chương & kết luận đóng hộp quá tay:** `.chap h4 span` đóng hộp nền đặc, `.verdict h4` xoay nghiêng `-1.2deg` / `1deg`, `.toc` bọc pill. Khắc phục: chỉ mục mono thuần chữ cho chương, thẳng hàng trang trọng cho `.verdict h4`, đường kẻ mảnh cho `.toc`.
8. **Chân trang `#siteFooter` mang emoji & nhiều nút viên thuốc:** Có emoji trang trí trong link footer và loạt nút pill. Khắc phục: loại bỏ 100% emoji, chuyển thành **Colophon & Phiếu Thư từ (`Archival Colophon + Correspondence Slip`)** nền mực giấy rõ rệt.
9. **Bỏ quên tối ưu typography & touch target hiện đại (`modern-web-guidance`):** Thiếu `text-wrap: balance` trên tiêu đề `h1–h4`, thiếu `text-wrap: pretty` trên đoạn văn `p, li, blockquote, dd`, dùng `height` cố định thay vì `min-block-size`, thiếu nâng vùng chạm `44px` trên `@media (pointer: coarse)`.
10. **Tắt animation thô bạo ở `@media (prefers-reduced-motion: reduce)`:** Đặt `animation-duration: .001ms !important` trên `*`. Khắc phục: giữ chuyển màu mượt, chỉ triệt tiêu chuyển động dịch chuyển/co giãn/xoay và animation lặp.

### B. Hai hướng đề xuất đối lập để Duy chốt trước khi áp vào `prototype.html`

- **Phương án A — *Archival Press Edition* (Ấn phẩm Lưu trữ · Đề xuất):** Giữ giấy ấm Risograph (`#f5efe4`), thanh điều hướng cao mảnh (`3px` radius, SVG kính lúp, badge trong suốt), bộ lọc `#catPills` dạng gạch chân biên tập, `#secStage` kiểu Mặt cắt Kiến trúc + Thước 5 nhịp, `<footer>` Colophon + Phiếu thư từ phẳng.
- **Phương án B — *Swiss Financial Ledger* (Sổ cái Thụy Sĩ):** Lưới viền mảnh `1px solid var(--rule)` sát cạnh (`border-radius: 0`), nút chỉ mục là ô lưới liền mạch (`Chỉ mục · 60 bài · ⌘K`), bảng/thẻ phân ô rõ ràng, `0px–2px` trên mọi control, chân trang Colophon tối giản chuẩn mực sổ kế toán.

### C. Audit & Tái cấu trúc Triệt tiêu "Nhiều Hộp Không Nhãn" (De-boxing & Semantic Information Architecture)

Đối chiếu ảnh thực tế do Duy chỉ ra (`media_1794716399478_bcc50bb7.jpg` — 6 hộp liên kết không nhãn ở chân trang) và ảnh chụp toàn trang (`final_step_10.png`), có 5 vùng bị lạm dụng khung viền hộp mà thiếu nhãn ngữ nghĩa:

1. **Cột trái chân trang (`.ft-info`):** 6 nút hộp `.ft-link`/`.ft-copy-btn` dàn hàng ngang không rõ vai trò từng liên kết. Khắc phục: thay hoàn toàn bằng **Danh bạ Ngữ nghĩa 4 hàng (`<dl class="ft-dir">`)** — `0` hộp viền, mỗi hàng có nhãn `<dt>` tường minh (`Liên hệ trực tiếp`, `Hồ sơ & Bài viết`, `Xưởng thử nghiệm`, `Mã nguồn & Kênh phát`) đi cùng liên kết chữ có gạch chân mảnh và mô tả ngắn.
2. **Hộp thư góp ý chân trang (`.ft-box` / `.fb-box`):** Chứa 9 hộp con bên trong (`2` nút tab mode, banner ngữ cảnh, `3` chip gợi ý đóng khung, `textarea`, `input`, nút gửi chính + nút `mailto` đóng hộp). Khắc phục: rút xuống đúng **3 khung nhập/hành động chính** (`textarea`, `input` email tuỳ chọn, nút gửi chính); chuyển `.fb-modes`/`.fb-tabs` thành tab gạch chân có nhãn `"Mục đích gửi:"`, chuyển `.fb-chips` thành liên kết gợi ý dạng chữ gạch chân chấm, và đưa `#fbMailtoLink`/`#fbMailtoLinkB` thành liên kết chữ thuần bên cạnh nút gửi chính.
3. **Thanh công cụ danh mục Landing (`.catalog-bar` + `#catPills`):** Các nhóm nút chế độ xem đứng rời rạc không có nhãn dẫn. Khắc phục: gắn nhãn tường minh (`Tìm bài:`, `Cách bày kệ:`) và làm phẳng nhóm nút chế độ hiển thị thành tab phân tách/gạch chân mảnh thay vì hộp lồng hộp.
4. **Thanh điều khiển thử nghiệm `.ux-lab-dock`:** Ở màn hình desktop (`final_step_10.png`), hộp tối nổi cố định góc dưới phải đè lên dải lọc `#catPills`. Khắc phục: chuyển `.ux-lab-dock` sang `position: static` trên **mọi độ rộng màn hình**, đặt gọn dưới `#siteFooter` kèm nhãn tường minh (`Quy mô kho:`, `Màn hình:`, `Phương án:`).
5. **Trang chi tiết `#secStage` & `#secTry`:** Khối sân khấu `.stage-card`, phần lời kể `.stage-caption` và thanh âm thanh `.audio-strip` tách thành 3 hộp rời; nút `.house-node` chỉ đánh số `01..05` và `.preset-btn` đứng thành hàng hộp không nhãn. Khắc phục: ghép liền mạch 3 tầng của `#secStage` thành một mô-đun bản vẽ thống nhất, thêm tiền tố `Vai trò 01..05` trên từng ngôi nhà, gắn nhãn `Lăng kính đọc:` trước `.seg`, gắn nhãn `Mức hoá đơn mẫu:` trước `.preset-row` và làm phẳng `.preset-btn` thành nút chữ gạch chân mảnh.

### D. Bộ 12 Test-Case Kiểm thử Chức năng "Hộp thư Góp ý & Đề xuất bài viết mới" + Nút Icon Sao chép Email (`scripts/wms-feedback-test.py`)

Nút chữ `"Sao chép email"` cạnh `hello@duypham.me` đã được thay bằng nút biểu tượng SVG hai tờ giấy lồng nhau (`svg.ico-copy`, đổi sang dấu tick `svg.ico-check` + nhãn `Đã chép` trong `2s`, giữ `aria-label` và `title` đầy đủ). Bộ kiểm thử Playwright headless `scripts/wms-feedback-test.py` xác minh 12 kịch bản (`TC-01`..`TC-12`) trên cả bản Phương án A, bản đồng bộ `landing-detail-mockups.html`, bản Phương án B và cặp HTML Artifact:

| Mã | Nhóm kiểm thử | Kịch bản & điều kiện đạt |
|---|---|---|
| `TC-01` | Nút icon Sao chép Email | Trạng thái nghỉ hiện `svg.ico-copy`, ẩn `svg.ico-check`/toast, `border-top: 0px`, không thừa chữ `"Sao chép email"`, đủ `aria-label` + `title` có `hello@duypham.me`. |
| `TC-02` | Ghi Clipboard & tự hoàn nguyên | Bấm nút icon gọi `navigator.clipboard.writeText("hello@duypham.me")`, bật `data-copied="true"` (`svg.ico-check` + `"Đã chép"`), và tự trả về `data-copied="false"` sau `2s`. |
| `TC-03` | Đổi mục đích gửi | Chuyển qua lại giữa `"Đề xuất bài viết mới"` và `"Góp ý"` cập nhật `aria-pressed` và tiền tố tiêu đề trong liên kết `mailto:`. |
| `TC-04` | Gợi ý nhanh 1 chạm | Bấm chip gợi ý điền mẫu câu vào textarea, gỡ trạng thái lỗi `aria-invalid`, đồng bộ nội dung vào `mailto:` và chống chèn lặp ở Phương án A. |
| `TC-05` | Chặn gửi khi bỏ trống | Bấm gửi khi ô nội dung rỗng bật `aria-invalid="true"`, hiện thông báo lỗi, đưa con trỏ về textarea và giữ vùng trạng thái gửi trống. |
| `TC-06` | Giới hạn tối thiểu 8 ký tự | Chặn cả chuỗi `"1234567"` lẫn chuỗi độn khoảng trắng `"  12345  "`, sau đó tự xoá lỗi ngay khi gõ đủ `>= 8` ký tự. |
| `TC-07` | Chặn chuỗi toàn khoảng trắng | Nhập 10 dấu cách vẫn bị từ chối khi bấm gửi (`aria-invalid="true"`). |
| `TC-08` | Email nhận phản hồi tuỳ chọn | Nhập email sai định dạng bị chặn (`aria-invalid="true"`); xoá trống ô email vẫn gửi ẩn danh thành công. |
| `TC-09` | An toàn XSS & gửi hợp lệ | Gửi payload chứa `<b>XSS</b>` và email hợp lệ không kích hoạt HTML/script (`#xssTag` count `0`), hiện thông báo xác nhận và `0` lỗi console. |
| `TC-10` | Đồng bộ liên kết `mailto:` | Thuộc tính `href` của nút mở trình mail luôn chứa `hello@duypham.me`, loại thư, nội dung và email phản hồi đã giải mã đúng. |
| `TC-11` | Bám ngữ cảnh bài đang đọc | Mở bài viết chi tiết khiến biểu ngữ ngữ cảnh và thân thư `mailto:` tự gắn tên bài đang xem thay vì trang chủ. |
| `TC-12` | Hình học & phản hồi 2 kích thước | Đạt `scrollWidth <= clientWidth` trên `1440×900` và `390×844`, đủ `5` hàng `<dl class="ft-dir">` ở bản đầy đủ (`docs/*.html`) / `4` hàng ở artifact so sánh, giữ `0` viền hộp thừa và `.ux-lab-dock` `position: static`. |

---

## 10. Chưa xác minh được

- Chưa đo thời gian đọc và tỉ lệ bấm chọn từng vị trí trong cụm 3 bài `1 + 2` trên người đọc thật, cũng như tỉ lệ dùng `#landingSearch` so với `#gridModeSeg` khi kho lên `20–60` bài.
- Chưa test thực địa với người dùng thật độ ưa thích giữa *Archival Press Edition* (Phương án A) và *Swiss Financial Ledger* (Phương án B) sau khi triệt tiêu các chi tiết pill-ception.
- **Phạm vi dữ liệu giả lập `8..60` (`SCALE_ITEMS_8_60` & `makeGeneratedDetailPack`):** Các bài `s08_termdep`..`s60_cashbackwallet` có tiêu đề 3 mỏ neo riêng (đã quét Brand Safety `B1–B4` `0` vi phạm), teaser riêng, 5 ngôi nhà riêng, 1 Quiz riêng + 1 Quiz kế thừa và cụm 3 bài đọc tiếp riêng, nhưng **tạm tái sử dụng phần ruột khảo cứu C9, audio MP3 và bộ 4 ảnh `1200×675` của bài gốc cùng loại (`calcKey`)** để đo hành vi giao diện và cuộn trang. Nội dung biên tập độc lập cho 53 bài này chưa viết.
- Do công cụ `chrome-devtools-mcp` bị khoá profile bởi một phiên Chrome chạy trước đó (`PID 27596`), việc kiểm thử DOM và bố cục đã được chạy trên Chromium headless (Playwright) ở hai kích thước `1440×900` và `390×844` (đã xác minh cả 4 ảnh `1200×675` bài `card`, kiểm tra `7 / 20 / 60` bài trên cả 3 chế độ và kiểm thử trực quan 5 ảnh chụp màn hình, `0` lỗi console, `0` tràn ngang); chưa test thực địa `<audio>` phát trực tiếp hay WebView ứng dụng nhắn tin trên điện thoại Android đời thấp với chuyển cảnh `startViewTransition` và hiệu ứng hạt giấy `feTurbulence`.
- Chưa mở kiểm tra trực quan từng pixel cho toàn bộ `53` bài giả lập còn lại và `6` bài thật (`pay`, `install`, `minpay`, `qr`, `profitcash`, `offus`) trên từng trình duyệt thực địa, dù đã xác minh DOM bài mẫu `s15_escrowhouse`, `s20_bnplfee` (`quiz: 2`, `triad: 3`, `houses: 5`) và `s45_vendorcredit` (`postPos: 'Bài 7/8'`, `ppItems: 8`, `ppHeight: 320px`).

---

## 11. Quyết định của Duy (2026-11-15)

- **Lựa chọn đã xác nhận:** Duy chọn **Phương án A — *Archival Press Edition*** cho bản triển khai thật tại [`docs/prototype.html`](../../docs/prototype.html) (`QĐ 63`).
- **Phạm vi tích hợp vào `docs/prototype.html`:** Chuyển toàn bộ trải nghiệm chính sang kiến trúc 2 khung tách biệt (`#landingView` với Hero `22:47`, thanh tìm kiếm `#landingSearch`, 3 chế độ `#gridModeSeg`, `#catPills` gạch chân, phân trang `#catalogMoreBar`, `#shelf` động; và `#detailView` với `.detail-head`, sân khấu Diorama `#stage`, 7 máy tính kèm nút ví dụ nhanh `.preset-btn`, bài khảo cứu C9 `#baiday`, `#lessonQuizWrap`, cụm 3 bài đọc tiếp `1+2` `.triad-grid`), ngăn kéo từ điển 2 phạm vi `#glDrawer` + `#popJumpBtn`, và chân trang 5 hàng `<dl class="ft-dir">` kèm `#ftCopyEmailBtn` + `#fbForm`. Giữ nguyên dữ liệu canonical 7 bài `published` / 19 chủ đề / 52 `GLOSS` (`wms-studio-sync.py --verify`) và tích hợp target `proto` vào `scripts/wms-feedback-test.py`.
