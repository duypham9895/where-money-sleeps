---
status: pass
stage: 02-design
date: 2026-11-08
owner: design
blocked_on: []
---

# DESIGN-BRIEF — Bản Định Hướng Thiết Kế (`Where Money Sleeps`)

> **Quy tắc 13 (`S2 Design`):** `≤ 1 trang` cho phần quyết định gu thẩm mỹ (3 tính từ · 3 thứ KHÔNG giống · hướng thiết kế đã chọn & chạy sống trên `docs/prototype.html` và `docs/workflows.html`), theo sau là nhật ký diễn giải của PM và biên bản kiểm chéo T2 / T3.

## 1. Tuyên ngôn Gu Thẩm mỹ (3 Tính từ · 3 Thứ KHÔNG Giống)

| Ba tính từ dẫn đạo (`3 Adjectives`) | Ba thứ TUYỆT ĐỐI KHÔNG giống (`3 Anti-References`) |
|---|---|
| **1. Giải phẫu (`Architectural Cutaway`):** Mở mặt cắt ngang của 5 ngôi nhà tài chính với tường gạch chéo (`poché`), cửa cuốn mở theo nhịp, thấy rõ thông tin đi tầng trên và tiền thật chảy tầng ngầm. | **1. KHÔNG giống App Ngân hàng / Fintech xanh dương bóng bẩy:** Không dùng thẻ bo tròn kiểu ví điện tử, không dùng biểu đồ nến chứng khoán hay bảng lãi suất chào mời. |
| **2. Ấm màu giấy lưu trữ (`Warm Archival Risograph`):** Nền giấy kem ấm (`#f5efe3`), mực đen than (`#191714`), đỏ son biên tập (`#b83a22`) và xanh két ngân hàng (`#1c5d4b`) gợi cảm giác tạp chí điều tra kinh điển. | **2. KHÔNG giống Sách giáo khoa Kế toán khô khan:** Không mở đầu bằng định nghĩa Nợ/Có hay bảng hệ thống tài khoản; người đọc đi từ câu chuyện đời thường rồi mới lật sang `Sổ kế toán`. |
| **3. Chuyển động có quán tính vật lý (`Physical Kinetic Motion — M1–M4`):** Cửa cuốn, hạt xung ánh sáng và con số tiền tệ (`tabular-nums`) chuyển động trên một thế giới liền mạch (*Persistent World*) với đường cong `cubic-bezier(0.22, 1, 0.36, 1)`. | **3. KHÔNG giống Slide thuyết trình AI tím/xanh đại trà (`Anti-PPT / Anti-AI-Slop`):** Không cắt cảnh kiểu lật trang PowerPoint, không dùng ảnh stock trang trí vô nghĩa, không đè hộp chữ lên hoạt cảnh video (`LUẬT 8`). |

## 2. Hướng Thiết kế đã chọn & Kiểm chứng Thực tế

| Hạng mục | Quyết định Thiết kế đã khoá | File hợp đồng / Bản sống |
|---|---|---|
| **Hệ màu & Chữ** | Chế độ sáng *Archival Paper* (`#f5efe3`) cho tạp chí đọc sâu (`prototype.html`) + Chế độ tối *Night-Watch Ledger* (`#0e1015`) cho trung tâm điều phối (`workflows.html`); 3 họ font OFL (`Fraunces` · `Be Vietnam Pro` · `JetBrains Mono` `tabular-nums`) | `gates/02-design/TOKENS.md` |
| **Điều hướng `1A` (`48px`)** | Thanh 1 hàng `48px` (`Editorial Split-Pill`) + Overlay Mục lục 2 cột `Master–Detail` (`0px` đẩy sân khấu) + phím tắt `⌘K` + thẻ chuyển bài cuối bài (`QĐ 55`) | `gates/02-design/UI-STATES.md` |
| **Nhịp hình khảo cứu (`LUẬT 9`)** | Chương 01 thuần chữ có `drop-cap`; Chương 02–05 đan xen **4 hình mặt cắt `16:9` (`1200×675`)** ngay sau đoạn 1 kèm chú thích 3 tầng và nút nhảy lên nhịp Diorama (`CLS = 0`, `QĐ 57`) | `docs/prototype.html` (`CHAP_FIGS`) |
| **Video `Locked-Stage v4.0` (`LUẬT 8`)** | Nền mặt cắt khoá tĩnh `0px pan, 1.00x zoom`; tách 3 vùng không đè nhau (`Zone 1: 36..354`, `STAGE_BOX: 368..1280`, `CARD_BOX: 1294..1734`); khung `.yt-embed` hỗ trợ `16:9 ⇄ 9:16`, nhảy chương và fallback MP4 cục bộ (`QĐ 56`) | `scripts/wms-media-pipeline.py` |
| **Chuyển động `bang-motion` (`M1–M4`)** | Quán tính `cubic-bezier(0.22, 1, 0.36, 1)`, bộ đếm tiền `animateMoneyText()` / `animateCounter()`, hạt dẫn hướng SVG `<animateMotion>`, đồng hồ `window.__vibeSeek`, `prefers-reduced-motion`, 0 CDN ngoài (`QĐ 58`) | `scripts/wms-motion-snap.py` |

## 3. Nhật ký Diễn giải giữa S2 (PM + Design + Writer — Quy tắc 13)

- **`2026-11-08` (QĐ 55 — Điều hướng & Khử chữ `"sổ cái"`):** Duy chọn phương án `1A Editorial Split-Pill 48px` + Overlay Mục lục 2 cột và yêu cầu thay toàn bộ chữ `"sổ cái"` bằng `"Mục lục"` / `"Sổ kế toán"` / `"sổ sách ngân hàng"`. Đã áp dụng 100% trên `docs/prototype.html`.
- **`2026-11-08` (QĐ 57 — Nhịp hình minh hoạ khảo cứu `LUẬT 9`):** Duy yêu cầu nghiên cứu sâu hành vi đọc để đan xen hình minh hoạ chống ngán chữ. PM + Design chạy research 4 pha và chốt quy tắc 4 hình `16:9` (`1200×675`) ở Chương 02–05 ngay sau đoạn 1 kèm chú thích 3 tầng. Đã render đủ 12 hình `.jpg` và nhúng vào 3 bài mẫu.
- **`2026-11-08` (QĐ 58 — Trung tâm Điều phối Agent `docs/workflows.html` & `bang-motion` `M1–M4`):** Duy yêu cầu trực quan hoá realtime toàn bộ quy trình + minh bạch hoá nhà cung cấp/model và tích hợp tinh hoa `bangtutorial/bang-motion` (Phương án A). Đã hoàn tất và khoá bằng cổng kiểm `[3/4] scripts/wms-motion-snap.py`.
- **`2026-11-08` (Đồng bộ Diorama v4.0 trên `prototype.html` & Sân khấu Hoạt hoạ SVG trên `workflows.html`):** Duy chỉ ra `#stage` trên `prototype.html` còn vẽ cột điện, dây điện võng, đường nhựa và cửa cuốn sắt che phòng (lệch với Video & 12 hình `16:9`), đồng thời `workflows.html` quá nhiều chữ và thiếu hoạt hoạ trực quan. Đã nâng cấp `#stage` (`SCENECSS` + `SCENEJS`) lên **Diorama v4.0 (Mặt cắt Kiến trúc Xuyên thấu & 2 Ray Tài chính)** đồng bộ 100% với Video, và thiết kế lại `workflows.html` thành **Sân khấu Hoạt hoạ SVG Realtime (`1280×470`)** tự chạy từng bước từ lúc Duy giao 1 Topic qua 7 trạm phòng ban tới cổng khoá `force_ask` (giảm chữ tĩnh xuống 327 từ).
- **`2026-11-09` (QĐ 59 & `LUẬT 10` — Khử đè chữ SVG/Canvas, Tách Trang Đọc Sạch & Xây dựng Bàn Duyệt `docs/studio.html`):** (1) Duy chỉ ra lỗi đè chữ trên hộp trạm `workflows.html` — đã sửa triệt để và ban hành **`LUẬT 10` (`Zero Sibling Text Collision`)** kèm cổng kiểm tất định `M3b` trong `scripts/wms-motion-snap.py`; (2) Duy chốt **Phương án A (`QĐ 59`)**: tách biệt hoàn toàn giao diện người đọc trên `docs/prototype.html` (chỉ còn 2 tầng đọc sạch) khỏi kịch bản dựng video, đồng thời khảo sát 15 repo GitHub Studio + phân tích bảo mật ECC (`gates/02-design/STUDIO-RESEARCH-AND-SECURITY.md`) để dựng **`docs/studio.html`** (`0 dependency`, CSP `connect-src 'none'`, sóng âm thật trích từ MP4 qua `scripts/wms-studio-sync.py`).
- **`2026-11-09` (QĐ 60 — Tái thiết kế Video `Zone 2` mở rộng 80% + Phụ đề `.srt` & Bàn Duyệt `docs/studio.html` Phương án A `Calm Single-Focus`):** (1) Theo phản hồi của người xem và quyết định của Duy (**Phương án B cho Video**), gỡ bỏ đoạn văn kịch bản dài ở `Zone 3` (`CARD_BOX`), mở rộng `STAGE_BOX` (`Zone 2`) lên `(48, 368, 1032, 1548)` (`1180px`) chứa thêm **Bảng Sổ Kế Toán & Dòng Tiền Động (`y=1246..1524`)**, thu gọn `CARD_BOX` xuống `(48, 1564, 1032, 1734)` (`170px` — chỉ giữ 1 dòng công thức `≤ 8 từ` + chỉ dẫn bật CC), và tự động sinh 6 file `.srt` (`dist/youtube/*.srt`) cho YouTube Closed Captions; (2) Theo lựa chọn của Duy sau khi xem 3 bản mockup (`docs/studio-mockups.html`), nâng cấp **`docs/studio.html`** sang **Phương án A (`Calm Single-Focus`)** trên nền giấy ấm `#ede6d6` với 2 chế độ duyệt đơn tiêu điểm: **`📖 1. Duyệt Bài Viết (5 Chương & Sổ TT 99)`** (duyệt từng mục một trong 8 mục, kiểm tra 4 hình `16:9` `LUẬT 9` và các thuật ngữ `[[nhãn|khoá]]` của từng chương) và **`🎬 2. Duyệt Video & Phụ đề (.srt)`** (chỉ hiện 1 Thẻ Cảnh đang phát + lớp phủ phụ đề `.srt` trực tiếp trên video).

## 4. T2 — Câu hỏi Chéo-Phòng (Từ SWE & Data → Design)

> **Quy tắc 12 (T2):** Phòng không sở hữu stage (`SWE` và `Data`) đặt đúng HAI câu hỏi; `Design` trả lời trực tiếp trong artifact.

1. **Câu hỏi 1 (từ SWE):** *"Khi thêm danh mục thứ 8 hoặc bài viết thứ 20 bằng `/vibe-post`, giao diện `Layout 1A Split-Pill 48px`, `Overlay Mục lục 2 cột` và `Mặt cắt Diorama` có cần viết thêm CSS theo từng bài mới không?"*
   - **Trả lời của Design:** **Không cần sửa 1 dòng CSS nào.** Toàn bộ 5 ngôi nhà trong Mặt cắt Diorama được dựng từ tập 9 archetype cố định trong `const TYPES` (`home`, `shop`, `acq`, `scheme`, `crowd`, `iss`, `pbank`, `co`, `lend`), màu danh mục lấy động từ trường `CATEGORIES[i].c` qua biến CSS `--cat-color`, và `Overlay Mục lục 2 cột` cuộn độc lập hỗ trợ tới 50 danh mục mà không đổi chiều cao thanh `48px`.
2. **Câu hỏi 2 (từ Data):** *"Trên `docs/prototype.html`, việc chuyển bài qua `Split-Pill` hoặc `Overlay Mục lục` diễn ra tức thời không tải lại trang (SPA state). Vậy ở `S3 Build`, thời điểm tính một 'phiên' và sự kiện `lesson_completed` được kích hoạt ở mốc tương tác nào trên giao diện?"*
   - **Trả lời của Design:** Điểm neo kích hoạt sự kiện nằm ở khu vực cuối bài khảo cứu (`#baiday` / thẻ câu hỏi tự soi & quiz card cuối bài theo `QĐ 24` & `QĐ 38`), hoàn toàn độc lập với việc người đọc mở bài từ URL trực tiếp hay chuyển bài qua `Split-Pill`. Mỗi lần đổi bài qua `Split-Pill`, giao diện cập nhật hash/state `curStory` và cuộn về đầu bài để tách bạch từng lượt đọc bài.

## 5. T3 — Đối chiếu với Bản Tái Lập Độc Lập (`T3-RECONSTRUCTION.md`)

> Báo cáo chi tiết: [`gates/02-design/T3-RECONSTRUCTION.md`](T3-RECONSTRUCTION.md). Subagent `3d8bc758-9d1b-451a-a372-34cbb09b8f80` dựng lại từ `ONE-PAGER.md` + `PRD.md` + `AGENT-CMS-PIPELINE.md`.

- **1 Phát hiện chặn được sửa ngay nhờ T3:** Bản nháp đầu của `MICROCOPY.md` dùng cụm từ *"Đã qua 4 chuyên gia kiểm duyệt tự động"* trong dòng minh bạch AI. Phiên T3 chỉ ra `PRD.md` (QĐ 41, Legal R20, AC-21, AC-86) **cấm 4 chữ `"kế toán"`, `"accountant"`, `"chuyên gia"`, `"expert"`** trong dòng minh bạch công khai và `reviewed_by`. Đã sửa ngay trong `MICROCOPY.md` §2 theo đúng mẫu Writer W2.
- **0 điểm bất đồng chưa giải quyết** giữa bản S2 và bản T3 tái lập.
- **`2026-11-09` (QĐ 61 — Option A):** Khoá hợp đồng [`gates/02-design/VIDEO-INFORMATION-LAYOUT-AND-ANIMATION-RESEARCH.md`](VIDEO-INFORMATION-LAYOUT-AND-ANIMATION-RESEARCH.md) cho cả Video Ngắn (`9:16`, Safe Zone `x=48..868, y=268..1316`, 2 Beats/cảnh) và Video Dài (`16:9`, Safe Zone `x=64..1856, y=44..828`, 3 Dynamic Stage Modes `L-A/L-B/L-C`, 4 Progressive Beats/cảnh) với 9 Nguyên hàm Hoạt cảnh Thủ tục (`P1–P9`) và 6 khoá bảo vệ `F1–F6`.
- **`2026-11-15` (`LUẬT 13 · R1–R5` — Chuẩn Responsive Mobile + Touch Tablet + Desktop Parity):** Duy yêu cầu hệ thống hoá nguyên tắc thiết kế responsive chỉnh chu cho cả mobile, tablet và desktop và áp dụng lên toàn bộ `prototype.html`, `workflows.html`, `studio.html`, `doc.css`: kiểm đủ 6 khung nhìn (`320·390px` mobile touch, `768·820·1024px` tablet touch, `1440px` desktop), giữ thanh sticky `≤ 12% dvh` (1 hàng gọn trên mobile & tablet dọc `≤ 900px` không ép hẹp `.split-pill`), kẹp `#postPop`/`#atlas`/`#authorDock` trong viewport (`dvh` + `overscroll-behavior: contain`), `≥ 44×44px` hit box cho `pointer: coarse` (và `≥ 24×24px` fine pointer kể cả các nút phụ), `≥ 16px` input chống iOS zoom (gồm `#postNoteInput` ở `studio.html`), `.cat-pills` vuốt ngang 1 hàng tới `≤ 900px`, khung cuộn ngang cho `.hierarchy-stage`/`.oss-table` (`≥ 10px` SVG text), và sổ kế toán `.ledger` thoáng trên `320px`.

## 6. Chưa xác minh được

- Thử nghiệm thực địa 5 người đọc đầu tiên trên điện thoại thật trong WebView Zalo (sẽ thực hiện trước cổng `S5 Launch`).
- Cross-vendor model review (Claude ↔ Gemini) + T3 Independent Reconstruction — no human external verifier ran.
