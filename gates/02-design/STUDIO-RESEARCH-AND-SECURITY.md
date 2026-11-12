# Khảo Sát 15 Repo GitHub Studio & Phân Tích Bảo Mật — WMS Content & Video Review Studio (QĐ 59)

- **Owner:** Phòng PM + Design + SWE + Security (`security-review` + `opensource-sanitizer` + `modern-web-guidance`)
- **Ngày chốt:** 2026-11-09 (`QĐ 59`)
- **Stage:** `02-design` (`S2 Design`)
- **Reviewer:** `cross-vendor model review (Claude ↔ Gemini) — no human external verifier ran`
- **Sản phẩm bàn giao:**
  1. [`docs/studio.html`](../../docs/studio.html) — Bàn dựng & kiểm duyệt Nội dung, Kịch bản, Sóng âm & Video (`16:9` + `9:16` + `LUẬT 8` HUD + 4 Cổng Chuyên gia `K/F/B/M`)
  2. [`scripts/wms-studio-sync.py`](../../scripts/wms-studio-sync.py) + [`docs/wms-studio-data.js`](../../docs/wms-studio-data.js) — Bộ đồng bộ dữ liệu một nguồn chuẩn & trích xuất biên độ sóng âm thật (`RMS Peaks`) từ file MP4 qua `ffmpeg`
  3. [`docs/prototype.html`](../../docs/prototype.html) — Tách biệt 100% **Trang Người Đọc (`#baiday`: 2 tab Đời thường & Sổ kế toán TT 99/2025)** khỏi **Bàn Kiểm Duyệt Kịch Bản Video (`#studioScriptSec` / `docs/studio.html`)**

---

## 1. TL;DR Quyết Định Kiến Trúc (QĐ 59)

| Hạng mục | Quyết định đã chốt (`QĐ 59`) | Lý do kỹ thuật & bảo mật |
|---|---|---|
| **1. Tách giao diện Người đọc vs. Bàn dựng của Duy** | **Phương án A:** Trên `docs/prototype.html`, mục `#baiday` của độc giả **chỉ còn 2 tầng đọc sạch** (`A · Góc nhìn Đời thường` + `B · Sổ kế toán TT 99/2025`). Toàn bộ Kịch bản Video, Sóng âm, Thước đo `LUẬT 8` và Cổng kiểm 4 chuyên gia được đưa sang **[`docs/studio.html`](../../docs/studio.html)** (và ngăn kéo hậu trường `#studioScriptSec` ẩn mặc định). | Độc giả đọc bài khảo cứu không bị nhiễu bởi thông số kỹ thuật hậu trường (`timecode`, `onScreen`, `WPM`, `-14 LUFS`), trong khi Duy có một bàn dựng chuyên nghiệp kiểu NLE để duyệt trước khi lên bài. |
| **2. Có cài trực tiếp repo GitHub nào làm dependency (`npm` / Docker) không?** | **KHÔNG cài bất kỳ repo nào làm runtime/npm dependency (`0/15 repo`).** Chắt lọc **8 mẫu thiết kế UI/UX đắt giá nhất** từ các repo giấy phép sạch (`MIT` / `BSD-3-Clause` / `Apache-2.0`) vào **1 file tĩnh `docs/studio.html` (`0 node_modules`)**. | Giữ nguyên cam kết **Zero-Dependency Static Architecture**, bảo vệ tuyệt đối `.env` (`ELEVENLABS_API_KEY`, `GEMINI_API_KEY`) và `.secrets/youtube_token.json` khỏi tấn công chuỗi cung ứng `npm postinstall`, đồng thời tránh bẫy bản quyền `Remotion License` / `AGPL-3.0`. |
| **3. Cơ chế đồng bộ dữ liệu trên `file://` và `http://`** | `scripts/wms-studio-sync.py` trích xuất `STORIES`, `GLOSS`, `CATEGORIES`, `CHAP_FIGS`, manifest YouTube và **sóng âm thật (`RMS Peaks`)** từ 6 file MP4 sang `docs/wms-studio-data.js` (kèm mã băm `SHA-256` kiểm tra trong `wms-check.sh`). | Trình duyệt chặn `fetch()` đọc file nội bộ trên giao thức `file://` (CORS `origin: null`). Nạp qua `<script src="wms-studio-data.js">` giúp `studio.html` mở trực tiếp bằng cú đúp chuột (`file://`) lẫn localhost (`http://`). |

---

## 2. Báo Cáo Khảo Sát 15 Repo GitHub Studio (`SWEEP` → `DEDUPE` → `REFUTE` → `JUDGE`)

Ba mũi `SWEEP` độc lập đã quét 15 repo mã nguồn mở nổi bật nhất trên GitHub thuộc 3 nhóm, gộp trùng bằng Python (`DEDUPE`) và qua vòng phản biện bảo mật/pháp lý (`REFUTE`):

### Nhóm A — Programmatic Video & Motion Studios (6 Repo)

| # | Repo GitHub | Stars | Giấy phép | Điểm mạnh học hỏi vào `studio.html` | Lý do KHÔNG cài làm dependency (`REFUTE`) |
|---|---|---|---|---|---|
| 1 | [`remotion-dev/remotion`](https://github.com/remotion-dev/remotion) | ~42.6k | **Remotion License** (Source-available, thu phí >3 người) | Học **Social Media Safe-Zone Overlay** (`@remotion/elements`) và **Composition Switcher (`16:9` ⇄ `9:16`)**. | (1) Giấy phép thương mại độc quyền; (2) `@remotion/web-renderer` có gắn telemetry gửi về `remotion.run` (vi phạm Rule 8); (3) Kéo >500 gói npm vào cạnh `.env`. |
| 2 | [`motion-canvas/motion-canvas`](https://github.com/motion-canvas/motion-canvas) | ~18.6k | **MIT** | Học **Audio Waveform Scrubbing + Loop Range** và **Node Bounding-Box Inspector** (kiểm tra `LUẬT 6b` & `LUẬT 10`). | Đòi Vite Dev Server + Preact generator runtime, không mở trực tiếp bằng `file://` được. |
| 3 | [`midrender/revideo`](https://github.com/midrender/revideo) | ~3.9k | **MIT** | Học **Parameterized Variables Preview** & đồng bộ giữa bản xem trước và bản render FFmpeg. | Kéo Puppeteer + ~400 gói npm thừa vì ta đã có `scripts/wms-media-pipeline.py` (Pillow + FFmpeg 30fps). |
| 4 | [`theatre-js/theatre`](https://github.com/theatre-js/theatre) | ~11.9k | `Apache-2.0` (`@theatre/core`) / **AGPL-3.0 (`@theatre/studio`)** | Học kiến trúc **tách đôi Core Runtime (`prototype.html`) khỏi Studio (`studio.html`)** và xuất trạng thái ra JSON. | **Bẫy pháp lý nghiêm trọng:** Gói giao diện `@theatre/studio` mang giấy phép **AGPL-3.0** (copyleft lây nhiễm). |
| 5 | [`OpenCut-app/OpenCut`](https://github.com/OpenCut-app/OpenCut) | ~49.7k | **MIT** | Học bố cục **4-Pane NLE Workbench** (Left Queue · Center Player · Bottom Waveform · Right Gate Inspector). | App monorepo nặng (Next.js + Postgres + Upstash Redis + Rust/WASM). |
| 6 | [`diffusionstudio/core`](https://github.com/diffusionstudio/core) | ~2.3k | **MPL-2.0 + Watermark Clause** | Học mô hình tổ chức Track/Clip/Caption đa lớp. | **Vi phạm trực tiếp `LUẬT 4` (`brand-safety-reviewer`):** Giấy phép bắt buộc chèn watermark *"Made with Diffusion Studio"* nếu không trả phí. |

### Nhóm B — Frame-Accurate Video Review & Transcript Studios (5 Repo)

| # | Repo GitHub | Stars | Giấy phép | Điểm mạnh học hỏi vào `studio.html` | Lý do KHÔNG cài làm dependency (`REFUTE`) |
|---|---|---|---|---|---|
| 7 | [`cgwire/kitsu`](https://github.com/cgwire/kitsu) + `zou` | ~1.5k | **AGPL-3.0** | Học **Side-by-Side Split-Compare (`16:9` ⇄ `9:16`)** và **Bảng Ma trận Cổng Chuyên gia (`K/F/B/M`)**. | Giấy phép AGPL-3.0 + đòi backend Python Flask / PostgreSQL / Redis. |
| 8 | [`AcademySoftwareFoundation/OpenRV`](https://github.com/AcademySoftwareFoundation/OpenRV) | ~2.0k | **Apache-2.0** | Học **Broadcast Safe-Action / Title-Safe Matte Overlay (`LUẬT 8`)** và **Nhích từng Frame (`±33.3ms @ 30fps`)**. | Ứng dụng C++17 / Qt5 / OpenGL nặng cho Desktop; đã chuyển hoá thành lớp phủ `<svg id="safezoneSvg">` nhẹ 2KB. |
| 9 | [`ynput/ayon-frontend`](https://github.com/ynput/ayon-frontend) | ~55 | **FSL-1.1-ALv2** | Học **Publish Gate Inspector** (hiển thị trạng thái PASS/FAIL của từng cổng kiểm trước khi xuất bản). | Giấy phép Source-Available FSL-1.1 + đòi backend AYON server. |
| 10 | [bbc/react-transcript-editor](https://github.com/bbc/react-transcript-editor) + [bbc/peaks.js](https://github.com/bbc/peaks.js) | ~1.9k / ~2.5k | **Apache-2.0** / **LGPL-3.0** | Học **Click-Scene-to-Seek Bidirectional Sync**, **Bảng Kịch bản 3 Cột** (`Timecode` \| `VO + onScreen` \| `Visual` \| `Verdict`) và **cảnh báo tốc độ đọc WPM**. | Repo BBC đã ngừng bảo trì từ 2022, phụ thuộc vào `draft-js` (đã archive, tồn đọng nhiều lỗ hổng bảo mật npm). |
| 11 | [katspaugh/wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | ~9.9k | **BSD-3-Clause** | Học **Regions Banding** (tô màu từng phân đoạn cảnh + vạch cầu nối hơi thở `0.36s`) trên thanh sóng âm. | Thư viện `wavesurfer` dùng `fetch()` / `WebAudio` bị chặn bởi CORS khi mở qua `file://`. Thay bằng 50 dòng Canvas 2D vẽ trực tiếp mảng `RMS Peaks` trích sẵn từ MP4 qua `ffmpeg`. |

### Nhóm C — Git-Backed Local-First Editorial CMS Studios (4 Repo)

| # | Repo GitHub | Stars | Giấy phép | Điểm mạnh học hỏi vào `studio.html` | Lý do KHÔNG cài làm dependency (`REFUTE`) |
|---|---|---|---|---|---|
| 12 | [`sveltia/sveltia-cms`](https://github.com/sveltia/sveltia-cms) | ~1.9k | **MIT** | Học cơ chế **lưu biên bản review trực tiếp xuống đĩa bằng Browser `FileSystemAccess API` (`window.showSaveFilePicker`)** kèm fallback tải file JSON. | Dùng trực tiếp chuẩn Web API của trình duyệt, không cần nhúng cả bundle CMS 300KB. |
| 13 | [`Thinkmill/keystatic`](https://github.com/Thinkmill/keystatic) | ~3.6k | **MIT** | Học tư duy **Schema-as-Code** (mọi thay đổi phải khớp schema `C0–C9` của `check-story.py`). | Đòi Node server (Next.js/Astro) + >300 gói npm. |
| 14 | [`tinacms/tinacms`](https://github.com/tinacms/tinacms) | ~13.3k | **Apache-2.0** | Học chế độ **Bản Đọc Sạch (`Mode 3: Reader Preview`)** đặt ngay trong Studio để đối chiếu giao diện độc giả. | Đòi GraphQL daemon + TinaCloud proxy. |
| 15 | [`decaporg/decap-cms`](https://github.com/decaporg/decap-cms) & `pages-cms` | ~18.9k / ~2.6k | **MIT** | Học luồng trạng thái xuất bản `draft → review → published`. | **Rủi ro bảo mật CRITICAL:** Lưu GitHub Personal Access Token / OAuth token (`scope: repo`) trong `localStorage`. |

---

## 3. Phân Tích Bảo Mật Theo ECC `security-review` + `opensource-sanitizer` + `modern-web-guidance`

Đối chiếu 3 kiến trúc Studio trước các mối đe doạ thực tế của xưởng `Where Money Sleeps` (nơi lưu `.env` chứa `ELEVENLABS_API_KEY`, `GEMINI_API_KEY` và `.secrets/youtube_token.json` chứa OAuth Refresh Token kênh `@WhereMoneySleeps`):

| Mối đe doạ (Threat Vector) | Kiến trúc 1: Cloud / Server Git CMS (`Decap`, `Tina`, `Pages CMS`, `Kitsu`) | Kiến trúc 2: Heavy npm Framework (`Remotion Studio`, `OpenCut`, `Keystatic`) | Kiến trúc 3 (ĐÃ CHỌN): Zero-Dependency Local-First Studio (`docs/studio.html` + `wms-studio-sync.py`) |
|---|---|---|---|
| **T1. Lộ API Key & YouTube OAuth Token (`.env` / `.secrets/`)** | **CAO:** Server web có quyền đọc filesystem nếu dính lỗi Path Traversal / SSRF. | **NGHIÊM TRỌNG:** `npm install` thực thi script `postinstall` của hàng trăm gói phụ thuộc trong cùng thư mục chứa `.env` & `.secrets/`. | **0 RỦI RO (`PASS`):** `0 node_modules`, `0 server`. `wms-studio-sync.py` chỉ đọc `docs/prototype.html` và `dist/youtube/`, tuyệt đối không chạm `.env` hay `.secrets/`. |
| **T2. Rò rỉ dữ liệu qua mạng (Network Exfiltration / Telemetry)** | **CAO:** Gửi dữ liệu bài viết qua máy chủ trung gian bên thứ ba. | **TRUNG BÌNH:** `@remotion/web-renderer` gửi telemetry về máy chủ hãng. | **0 RỦI RO (`PASS`):** Khoá cứng header CSP `<meta http-equiv="Content-Security-Policy" content="... connect-src 'none'; form-action 'none';">`. Trình duyệt chặn 100% lệnh `fetch` / `XHR` / `WebSocket` / `sendBeacon`. |
| **T3. Tấn công DOM XSS khi render lời bình / ghi chú kịch bản** | Phụ thuộc vào bộ lọc của framework. | Phụ thuộc vào React/Preact. | **ĐÃ KHOÁ (`PASS`):** Áp dụng `Trusted Types` (`wms-studio-policy`) + hàm escape `esc()` trên mọi nội dung động (`modern-web-guidance` `trusted-types` & `sanitize-untrusted-html`). |
| **T4. Rò rỉ tên thương hiệu hoặc Secret Token lên bản xuất bản** | Không có cổng chặn chuyên biệt. | Không có cổng chặn chuyên biệt. | **ĐÃ KHOÁ (`PASS`):** Tích hợp bộ quét trực tiếp `BRAND_RE` (`brand-safety-reviewer`) + `SECRET_RE` (`sk-...`, `AIza...`, `GOCSPX-...`, `1//0...`) ngay trong cột Cổng kiểm `B1–B4` của `studio.html` và làm sạch hàm `exportVO()` trên `prototype.html`. |

---

## 4. Mục Chưa Xác Minh Được (Rule 3)

- **Chưa xác minh được trên môi trường Safari iOS thực tế:** API `window.showSaveFilePicker` (`FileSystemAccess API`) hiện được hỗ trợ đầy đủ trên Chromium (Chrome / Edge / Brave / Arc desktop), nhưng trên Safari/Firefox sẽ tự động chuyển về cơ chế tải file chuẩn `<a download="wms-review-<story>.json">` (đã cài sẵn fallback).
