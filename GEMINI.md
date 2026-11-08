@[Vibe Rules](../GEMINI.md)

# Where Money Sleeps — luật của repo (Gemini / Antigravity)

Dòng đầu nạp 16 quy tắc của xưởng Vibe (kể cả định tuyến model `scripts/vibe-model-route.py` / `../docs/model-routing.md`) khi repo nằm trong xưởng. **Clone riêng repo thì link đó không có đích** —
Antigravity xử lý link chết thế nào: CHƯA XÁC MINH. Vì vậy file này tự chứa đủ WMS-R1..R5 để làm việc đúng.
Lệch nhau: luật xưởng > hợp đồng AGENT-CMS-PIPELINE > file này > skill. Hợp đồng chi tiết: `gates/01-spec/AGENT-CMS-PIPELINE.md`.
Skill trong repo: `.agents/skills/vibe-post/SKILL.md` (gõ `/vibe-post` hoặc `/vibe:post`) · `.agents/skills/ke-toan-reviewer/SKILL.md` · `.agents/skills/vibe-model-route/SKILL.md`.

Duy đọc tiếng Việt — **trả lời bằng tiếng Việt**; thuật ngữ (Debit, Credit, EIR, Settlement…) giữ tiếng Anh.
Ghi file bằng `write_file` / `edit_file`, không bằng shell — với lệnh shell, hook guard chỉ thấy chuỗi lệnh (bắt lệnh ship và mẫu approvedBy/published nằm ngay trong lệnh), không thấy file bị ghi ra sao.

## WMS-R1 · Taxonomy 3 cấp & Điều hướng Layout 1A (QĐ 55)

`CATEGORIES` (danh mục, thêm không giới hạn) → `topics` / `STORIES` (bài) → `beats` (đúng 5 đoạn kể).
Giao diện **bắt buộc** hiện trên thanh điều hướng 1 hàng `48px` (**Layout `1A` — Editorial Split-Pill**):
- **Bên trái:** Tên thương hiệu `Where Money Sleeps` (không đặt hamburger icon sát logo).
- **Chính giữa:** Viên thuốc đôi `Split-Pill` (`[Danh mục k/N ▾ │ Bài m/M: Tiêu đề ▾]`) + nút chuyển nhanh `‹` `›` + Popover đổi nhanh bài cùng danh mục.
- **Bên phải:** Nút `⌕ Mục lục & Tìm (N mục · M bài) ⌘K` + `Chế độ duyệt bài`.
- **Overlay Mục lục 2 cột (`Master–Detail`, phím `⌘K` / `Escape`):** nổi phủ trên mặt cắt, **0px Layout Shift** (không đẩy Diorama xuống), cột trái là danh sách dọc danh mục, cột phải là lưới bài + ô tìm kiếm toàn cục.
- **Cuối bài (`#nextHandoff`):** Thẻ "Trạm đọc kế tiếp" dẫn sang bài kế tiếp hoặc mở Mục lục.
- **Từ vựng bắt buộc (QĐ 55):** Dùng **"Mục lục"** cho điều hướng và **"Sổ kế toán"** / **"sổ sách ngân hàng"** cho góc nhìn kế toán; **CẤM dùng chữ `"sổ cái"`** trên giao diện (tránh nhầm sang blockchain và khó hiểu với người đọc).
**Mọi con số suy từ dữ liệu, không gõ cứng.** Thứ tự trong mảng = số thứ tự hiển thị. Khoá bài đã đăng không bao giờ đổi tên (QĐ 52).

## WMS-R2 · Mặt cắt Kiến trúc Diorama v3.0 (D1–D7)

- Mỗi bài đúng 5 nhà `houses[0..4]`, `type` ∈ archetype hợp lệ = khoá của `const TYPES` trong khối SCENEJS
  (`home shop acq scheme crowd iss pbank co lend`). Mỗi archetype có cửa cuốn kéo lên (`wShutter`), tường cắt gạch chéo
  (poché), đạo cụ nội thất (`fx`). Không archetype nào hợp ⇒ **dừng, đề xuất archetype mới** — không vẽ hộp phẳng.
- **Hai luồng vật lý tách rời:**

  | Luồng | Cú pháp | Chỉ chở | CẤM |
  |---|---|---|---|
  | Dây điện trên cao | `msgs: [từ, tới]` | lời nhắn, lệnh cấp phép, hợp đồng, lời hứa | tiền thật |
  | Ống quyết toán ngầm | `msgs: [từ, tới, "money"]` | tiền thật: settlement, giải ngân, trả nợ, nộp thuế/phí | lời nhắn |

- Khối `/*SCENECSS:START … SCENECSS:END*/` và `/*SCENEJS:START … SCENEJS:END*/` trong `docs/prototype.html` dùng chung với
  bản xem nhanh 450px. Sửa một bên ⇒ chép **nguyên khối** sang bên kia. Script so từng byte với mọi bản xem nhanh nằm
  trong repo (`docs/*.html`) hoặc truyền bằng `--sync-with`. Bản trong thư mục brain của Antigravity **không phải nguồn**.

## WMS-R3 · Kế toán kép TT 99/2025 & nhãn `ví dụ`

- Mỗi `ledger`: **Σ Nợ (Debit) = Σ Có (Credit)**; dòng 6 cột; có `assume`.
- Tên tài khoản theo Thông tư 99/2025/TT-BTC: tiền thẻ chờ quyết toán / phải thu từ ngân hàng thanh toán ⇒ **TK 1388**,
  không TK 131; lương ⇒ **TK 334**. Script chỉ đối chiếu bảng thứ cấp ⇒ tối đa *"khớp nguồn thứ cấp"*; phán thật thuộc
  skill `ke-toan-reviewer` rồi Duy ký.
- Mọi tỉ lệ / con số minh hoạ gắn `<span class="ex">ví dụ</span>`. Mọi thuật ngữ `[[nhãn|khoá]]` có khoá trong `GLOSS`.

## WMS-R3b · Luật C9 v2 — mỗi bài đủ 3 trụ (từ 2026-11-08, Hướng 3A)

Duy, 2026-11-08: *"mỗi bài viết phải đầy đủ thông tin cho users (là người có chuyên và kh có chuyên môn) để sau này tôi có
để dùng content của bài post để tạo video"*. Năm đoạn kể chỉ là cửa vào. Mỗi bài trong `STORIES` phải có thêm:

| Trụ | Trường | Cho ai | Tối thiểu (C9) |
|---|---|---|---|
| A · Bài khảo cứu toàn cảnh | `article.lay` — `myths` · `sections[{h,paras}]` · `flowSummary` · `roles` · `whenHelps` · `whenTraps` · `takeaways` | người không chuyên | ≥ 3 lầm tưởng/sự thật (mỗi vế ≥ 10 từ) · ≥ 4 chương, ≥ 850 từ · ≥ 4 bước dòng chảy, kênh `wire`/`pipe`/`book` · 1 vai cho mỗi nhà · ≥ 3 khi có lợi + ≥ 3 khi thành bẫy (≥ 10 từ, ngôi thứ ba, không khuyên) · ≥ 4 câu hỏi tự soi |
| B · Phân tích chuyên sâu | `article.pro` — `mechanics` · `accountingNotes` · `journal` · `edgeCases` | người có chuyên môn | ≥ 4 cơ chế, ≥ 450 từ · ≥ 4 ghi chú kế toán TT 99/2025 vs sổ ngân hàng, ≥ 180 từ · ≥ 3 bút toán qua luật C6 · ≥ 3 ngoại lệ × ≥ 50 từ |
| C · Studio Kịch bản & Nhúng Video YouTube | `videoScript.long` (`title` · `hookNote` · `youtubeId` · `embedStatus` · `elevenlabsVoiceId` · `scenes[]` có `chapter`) + `videoScript.short` (`title` · `angle` · `youtubeId` · `embedStatus` · `elevenlabsVoiceId` · `scenes[]`) — cảnh: `time` · `beat` · `visual` · `vo` · `onScreen` | Duy dựng video / ElevenLabs / Nhúng YouTube | Dài (YouTube 16:9, 8–10 phút): ≥ 10 cảnh, Hook → 5 đoạn Diorama + cảnh đào sâu → Kết, lời bình ≥ 1.350 từ, kết 7:30–11:00 · Ngắn (YouTube Shorts 9:16): ≥ 5 cảnh, lời bình 150–260 từ, kết 0:55–1:35 · có đủ `youtubeId` (`""` hoặc 11 ký tự), `embedStatus`, `elevenlabsVoiceId` · không markup |

`journal` chỉ chứa sổ doanh nghiệp theo TT 99; phía ngân hàng viết bằng lời, **không bịa số hiệu tài khoản**. Số mới ⇒
gắn "ví dụ", tính bằng code. C9 đo **độ dài và hình dạng**, không đo chất lượng — câu chữ vẫn qua ke-toan-reviewer rồi Duy.
C9 v2 (2026-11-08, Hướng 3A) còn grep tất định: `Điều <số>` · `Nghị định` · Thông tư khác 99 · URL · tên ngân hàng thương mại · câu khuyên ⇒ FAIL.
Bản v1 (`lay.body`, `videoScript.scenes`) đã bỏ — còn sót là FAIL. Ngưỡng đầy đủ: `gates/01-spec/AGENT-CMS-PIPELINE.md` §1.

## WMS-R3c · QĐ 54 — 7 danh mục khởi đầu (2026-11-08)

Taxonomy hiển thị lúc khởi đầu là **7 danh mục** của QĐ 53 (mở rộng QĐ 52/53); thêm danh mục vẫn theo WMS-R1.
Chữ chính xác của đề xuất Duy đồng ý **chưa nằm trong repo** — xem `gates/00-discovery/PRODUCT-BRIEF.md` QĐ 54.

## WMS-R3d · Luật Đủ 3 Điểm Neo Ngữ cảnh (Tiêu đề/Hook) & Giọng Đọc `eleven_v3` (`VOICE-AND-PROSODY-SPEC.md`)

- **Đủ 3 Điểm Neo Ngữ cảnh Tự thân (Self-Contained Context Rule):** Mọi tiêu đề (`title`, `videoScript.{long,short}.title`) và câu mở đầu (`scenes[0].vo`) bắt buộc chứa đủ 3 điểm neo logic trong cùng một câu: **`[1. Hành động + Quy mô gốc ban đầu] → [2. Cơ chế / Lời hứa bề mặt] → [3. Sự thật hệ thống / Số thực nhận]`** (VD: *"Mua hàng 12 triệu trả góp lãi suất 0%, vì sao cửa hàng chỉ thực nhận 11,4 triệu?"*). **CẤM** viết tiêu đề cụt thiếu mốc giá trị ban đầu hoặc mở đầu bằng `%` trơ trọi kiểu *"0% nhưng cửa hàng chỉ nhận 11,4 triệu"* hay *"Lương về, 0 đồng di chuyển"*.
- **Giọng đọc Đặc trưng (`eleven_v3`) & Kịch bản Viết Cho Tai Nghe:** Bắt buộc dùng model **`eleven_v3`** (`elevenlabsVoiceId: "eleven_v3:<voice_id>"`, mặc định Signature Voice: `eleven_v3:JwqRvOqFdGeQNu7UjKjw` — giọng Tâm, `stability: 0.65, similarity_boost: 0.80, style: 0.20, use_speaker_boost: true`); **CẤM** dùng `eleven_flash_v2_5`. Trong `vo`: **CẤM** đặt đuôi rào đón pháp lý `", ví dụ."` / `", vẫn là số ví dụ."` ở cuối câu (làm tụt trọng âm kết câu — phải đưa `"Trong ví dụ này,..."` / `"Giả sử..."` lên đầu mệnh đề); dùng dấu `:` sau cụm dẫn thị giác và `...` / `—` trước vế lật ngược vấn đề để tạo nhịp nghỉ tự nhiên. Kiểm tất định tại `scripts/check-story.py` (`C9`). Hợp đồng đầy đủ: `gates/01-spec/VOICE-AND-PROSODY-SPEC.md`.
- **Chuyển Tiếp Âm Thanh & Hình Ảnh Mượt Mà (Smooth Continuity Standard — `VOICE-AND-PROSODY-SPEC.md §4`):** **CẤM** gọi TTS rời rạc từng cảnh rồi ghép bằng `ffmpeg -f concat` (gây đứt hơi và khoảng lặng chết `-inf dB`) và **CẤM** cắt cứng 0-frame (`hard cut`) giữa các cảnh tĩnh. Bắt buộc: (1) thu **liền mạch 1 lần đọc** (`"\n\n".join(scene_texts)`) trên `eleven_v3` + cầu nối hơi thở mềm `0.36s` + nền Warm Night-Watch Room Tone (`-33 dBFS`) + hiệu ứng chuyển cảnh ElevenLabs `/v1/sound-generation` (`-22 dBFS`), chuẩn hoá `-14 LUFS`; (2) dựng **30fps liên tục** với `0.95s smoothstep cross-dissolve` + `camera glide`, hạt dòng chảy trực tiếp trên thanh 5 ngôi nhà, và **phụ đề cuốn chiếu từng cụm** (`12–20 chữ`, trượt nhẹ `0.28s ease-out`) kèm **tô sáng từng từ** theo đúng `alignment.character_start_times_seconds`.

## WMS-R4 · Cổng duyệt 1:1 (Web & YouTube) — agent KHÔNG BAO GIỜ tự đăng

- Bài agent tạo hoặc sửa ⇒ `status: "review"`, `approvedBy` rỗng (hợp đồng dùng `""`; `null` cũng qua C7).
- **CẤM** agent đặt `status: "published"` hoặc ghi `approvedBy: "Duy"` — kể cả khi Duy nói "ok" trong chat mà chưa có
  dòng quyết định có ngày. Duy xem bản **Preview 1:1** `docs/prototype.html?preview=1` — y hệt người đọc — rồi mới duyệt.
- **Đối với Video YouTube & Nhúng vào bài viết (QĐ 56):** Toàn bộ Audio (Voiceover + SFX) và Video (`16:9` YouTube Dài `1920×1080` + `9:16` YouTube Shorts `1080×1920`) được build qua **ElevenLabs API** (`POST /v1/text-to-speech/{voice_id}/with-timestamps` + `POST /v1/sound-generation`, có SHA-256 content-hash cache) kết hợp bộ dựng **Mặt cắt Diorama v3.0** (`scripts/wms-media-pipeline.py`, chuẩn `-14 LUFS`), đẩy lên YouTube (`YouTube Data API v3` — `videos.insert`) ở chế độ **`privacyStatus: "unlisted"`** (hoặc `"private"`), và **nhúng ngược mã `youtubeId` (11 ký tự) + `embedStatus: "uploaded_unlisted"` vào `STORIES[<khoá>].videoScript.{long,short}`** để trình phát `youtube-nocookie.com/embed/<youtubeId>` hiển thị trực tiếp ngay trong bài viết (`#pnl-lay` và `#pnl-vid`). Khi bài chưa `published`, **CẤM** đặt `embedStatus: "uploaded_public"`; **chỉ Duy duyệt và chuyển sang `"published"` / `"uploaded_public"`**.
- Câu kết bắt buộc: *"Bài `<khoá>` ở `status: review` (Video YouTube nhúng ở `embedStatus: uploaded_unlisted` / `pending_upload`). Tôi không tự đăng được — chỉ Duy chuyển sang `published` / `uploaded_public`."*

## WMS-R5 · Pipeline 6 bước `/vibe-post` & kiểm tất định

Thêm/sửa bài hoặc danh mục ⇒ chạy 6 bước của `gates/01-spec/AGENT-CMS-PIPELINE.md`: phân loại → 5 đoạn hai góc nhìn
(+ bước 2b: bài khảo cứu 2 tầng + kịch bản video 2 định dạng, C9 v2) → Diorama → **kiểm** → **build Audio/Video qua ElevenLabs → Upload YouTube (`unlisted`) → Nhúng `youtubeId` vào bài viết (`scripts/wms-media-pipeline.py`)** → hàng chờ review. Xong khi và chỉ khi:

```
   python3 -I scripts/wms-media-pipeline.py --story <khoá> --mode dry-run   (Bước 5A–5D)
   python3 -I scripts/check-story.py      ⇒ FAIL 0      (C0–C9)
   scripts/wms-check.sh                   ⇒ wms-check: PASS   (check-story + vibe-check của xưởng)
```

Dán nguyên văn dòng "Kết quả" vào báo cáo. Review do subagent làm ghi *"same vendor, same priors — no external verifier ran"*.

## Khoá thật vs. advisory — nói đúng phạm vi

| Cơ chế | Giữ được gì | Loại |
|---|---|---|
| `scripts/check-story.py` + `scripts/wms-check.sh` | hình dạng dữ liệu bài, sổ cân; file luật trong repo có mặt, không rỗng, bản chép khớp nhau (C8 — không kiểm được nội dung luật có bị cắt xén) | **KHOÁ THẬT** — script, thoát mã 1. Chỉ khoá khi có người chạy nó |
| `.agents/hooks.json` → `scripts/wms-hook-guard.sh` | `force_ask` khi: lệnh ship · ghi approvedBy (giá trị không rỗng, không "demo") · đặt `published` · đổi `pointer:` / thêm APPROVE trong `PIPELINE.md` · payload không đọc được | **CÓ ĐIỀU KIỆN** — hook có chạy thật, gốc đường dẫn `../scripts/…`, tên tool ghi file: **CHƯA XÁC MINH**. Lọt: lệnh shell ghi file mà mẫu không nằm trong lệnh; hoán đổi approvedBy giữa hai bài |
| Terminal Sandbox | lệnh ship chạm mạng ⇒ phải xin BypassSandbox | theo luật xưởng; chưa thử ở repo này |
| Luật "chỉ Duy đăng" ngoài hook | — | **ADVISORY** — nút *Duyệt & Đăng* là JS, ai bấm cũng được |

Nói *"repo này có khoá"* mà bỏ hai dòng cuối của bảng là làm Duy tin vào một bảo đảm không tồn tại.

## Git & Không bao giờ

- **Repo URL:** `https://github.com/duypham9895/where-money-sleeps` (`git@github.com:duypham9895/where-money-sleeps.git`, nhánh làm việc hiện tại: `spec/s1-draft`).
- **Giữ lịch sử từng bước (Duy, 2026-11-08):** Sau mỗi bước hoàn thành và vượt qua `scripts/wms-check.sh` (`FAIL 0`), thực hiện `git commit` (email `duypham9895@gmail.com`, commit message nói **vì sao**) và `git push` lên nhánh đang làm việc (qua cổng xác nhận `force_ask` của Duy).
- **Không bao giờ:** tự ý commit thẳng lên `main` hoặc merge/release/deploy khi Duy chưa duyệt · đổi `pointer:` trong `PIPELINE.md` · sửa tại chỗ một quyết định đã ghi (thêm dòng mới có ngày bên dưới) · dùng âm thanh/ảnh/font chưa nêu được giấy phép trong `legal/licences.json` · nhắc bất kỳ tên riêng / thương hiệu / nhãn hàng / cửa hàng / mạng thanh toán / công cụ hậu trường có thật nào (`ElevenLabs`, `Google`, `Veo`, `Visa`, `Mastercard`, `NAPAS`, `VietQR`, `Hermanson`...) trong khung hình video, mô tả YouTube, lời bình `vo`, chữ trên màn hình `onScreen`, nhãn giao diện hay dữ liệu bài (`LUẬT 4` — `gates/01-spec/VOICE-AND-PROSODY-SPEC.md` §5).
