# Where Money Sleeps — luật của repo (Claude Code)

Repo này có `.git` riêng. **Khi nằm trong xưởng Vibe**, Claude Code tự nạp thêm CLAUDE.md của xưởng ở thư mục cha
(16 quy tắc cứng: không tự đẩy con trỏ, research có citation, nêu cái chưa xác minh, hỏi Duy một câu một lần, định tuyến model `scripts/vibe-model-route.py` / `../docs/model-routing.md`…).
**Khi repo được clone riêng**, file này cùng `.claude/` là toàn bộ luật — WMS-R1..R5 dưới đây + `.claude/rules/model-routing.md` đủ để làm việc đúng.
Lệch nhau: luật xưởng > hợp đồng AGENT-CMS-PIPELINE > file này > skill. Hợp đồng chi tiết: `gates/01-spec/AGENT-CMS-PIPELINE.md`.

Duy đọc tiếng Việt — **trả lời bằng tiếng Việt**; thuật ngữ (Debit, Credit, EIR, Settlement…) giữ tiếng Anh.

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
  trong repo (`docs/*.html`) hoặc truyền bằng `--sync-with`.

## WMS-R3 · Kế toán kép TT 99/2025 & nhãn `ví dụ`

- Mỗi `ledger`: **Σ Nợ (Debit) = Σ Có (Credit)**; dòng 6 cột; có `assume`.
- Tên tài khoản theo Thông tư 99/2025/TT-BTC: tiền thẻ chờ quyết toán / phải thu từ ngân hàng thanh toán ⇒ **TK 1388**,
  không TK 131; lương ⇒ **TK 334**. Script chỉ đối chiếu bảng thứ cấp ⇒ tối đa *"khớp nguồn thứ cấp"*; phán thật thuộc
  agent `ke-toan-reviewer` rồi Duy ký.
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
- **Chuyển Tiếp Âm Thanh & Hình Ảnh Mượt Mà + Sân Khấu Khoá Tĩnh (`VOICE-AND-PROSODY-SPEC.md §4 & §6` — `LUẬT 5`):** **CẤM** gọi TTS rời rạc từng cảnh rồi ghép bằng `ffmpeg -f concat` (gây đứt hơi và khoảng lặng chết `-inf dB`), **CẤM** cắt cứng 0-frame (`hard cut`) giữa các cảnh tĩnh, và **CẤM** dịch chuyển tấm nền kiến trúc (`pan != 0px` hoặc `zoom != 1.00x`). Bắt buộc: (1) thu **liền mạch 1 lần đọc** (`"\n\n".join(scene_texts)`) trên `eleven_v3` + cầu nối hơi thở mềm `0.36s` + nền Warm Night-Watch Room Tone (`-33 dBFS`) + hiệu ứng chuyển cảnh ElevenLabs `/v1/sound-generation` (`-22 dBFS`), chuẩn hoá `-14 LUFS`; (2) dựng **30fps liên tục trên Sân khấu Khoá Tĩnh (`0px` pan, `1.00x` zoom, LANCZOS pre-scaled)** với `0.96s in-place optical cross-dissolve (smoothstep)`, hạt dòng chảy trực tiếp trên thanh 5 ngôi nhà, và **phụ đề theo câu + tô sáng từng từ bằng viên thuốc ánh hổ phách không đổi độ đậm chữ** theo đúng `alignment.character_start_times_seconds`.
- **Chuyên gia Tài chính & Cơ chế Ngân hàng (`tai-chinh-reviewer` — `F1–F4`, `knowledge/finance-kb.json`, `scripts/wms-finance-kb.py`):** Mọi bài viết và kịch bản video bắt buộc đi qua `.claude/agents/tai-chinh-reviewer.md` ở **Bước 4** và tự động qua cổng `step_5_0b_financial_specialist_audit()` ở **Bước 5.0b** trong `scripts/wms-media-pipeline.py`. Định kỳ hàng tuần (hoặc trước khi tạo bài mới), chạy `python3 -I scripts/wms-finance-kb.py --crawl --verify` để quét văn bản pháp quy & cơ chế ngân hàng, chắt lọc vào `knowledge/finance-kb.json` và kiểm chứng toán tài chính (`IRR/EIR`, phí `MDR`, khấu trừ lương, độ khớp 100% giữa bài viết và 2 video).
- **Chuyên gia Kiểm duyệt An toàn Thương hiệu & Không Tên Riêng (`brand-safety-reviewer` — `B1–B4`, `LUẬT 4`–`LUẬT 6`):** Mọi bài và video bắt buộc đi qua `.claude/agents/brand-safety-reviewer.md` ở **Bước 4** (cùng lúc với `ke-toan-reviewer` và `tai-chinh-reviewer`) và tự động qua cổng `step_5_0_brand_safety_audit()` ở **Bước 5.0** trong `scripts/wms-media-pipeline.py` trước khi gọi TTS (`5A`), render video (`5B`) hoặc upload YouTube (`5C`). Tuyệt đối `0` tên riêng thương mại, ngân hàng, mạng thẻ (`Visa`, `Mastercard`, `NAPAS`, `VietQR`), quán xá (`Quán Nhà Liên`), tác giả sách (`Hermanson`) hay công cụ hậu trường (`ElevenLabs`, `Google`, `Veo`, `Gemini`, `Claude`).

## WMS-R4 · Cổng duyệt 1:1 (Web & YouTube) — agent KHÔNG BAO GIỜ tự đăng

- Bài agent tạo hoặc sửa ⇒ `status: "review"`, `approvedBy` rỗng (hợp đồng dùng `""`; `null` cũng qua C7).
- **CẤM** agent đặt `status: "published"` hoặc ghi `approvedBy: "Duy"` — kể cả khi Duy nói "ok" trong chat mà chưa có
  dòng quyết định có ngày. Duy xem bản **Preview 1:1** `docs/prototype.html?preview=1` — y hệt người đọc — rồi mới duyệt.
- **Đối với Video YouTube & Nhúng vào bài viết (QĐ 56):** Toàn bộ Audio (Voiceover + SFX) và Video (`16:9` YouTube Dài `1920×1080` + `9:16` YouTube Shorts `1080×1920`) được build qua **ElevenLabs API** (`POST /v1/text-to-speech/{voice_id}/with-timestamps` + `POST /v1/sound-generation`, có SHA-256 content-hash cache) kết hợp bộ dựng **Mặt cắt Diorama v3.0** (`scripts/wms-media-pipeline.py`, chuẩn `-14 LUFS`), đẩy lên YouTube (`YouTube Data API v3` — `videos.insert`) ở chế độ **`privacyStatus: "unlisted"`** (hoặc `"private"`), và **nhúng ngược mã `youtubeId` (11 ký tự) + `embedStatus: "uploaded_unlisted"` vào `STORIES[<khoá>].videoScript.{long,short}`** để trình phát `youtube-nocookie.com/embed/<youtubeId>` hiển thị trực tiếp ngay trong bài viết (`#pnl-lay` và `#pnl-vid`). Khi bài chưa `published`, **CẤM** đặt `embedStatus: "uploaded_public"`; **chỉ Duy duyệt và chuyển sang `"published"` / `"uploaded_public"`**.
- Câu kết bắt buộc: *"Bài `<khoá>` ở `status: review` (Video YouTube nhúng ở `embedStatus: uploaded_unlisted` / `pending_upload`). Tôi không tự đăng được — chỉ Duy chuyển sang `published` / `uploaded_public`."*

## WMS-R5 · Pipeline 6 bước `/vibe-post` & kiểm tất định

Thêm/sửa bài hoặc danh mục ⇒ chạy 6 bước của `gates/01-spec/AGENT-CMS-PIPELINE.md` (skill `vibe-post`, lệnh
`/vibe-post` hoặc `/vibe:post`): phân loại → 5 đoạn hai góc nhìn (+ bước 2b: bài khảo cứu 2 tầng + kịch bản video 2 định dạng, C9 v2) → Diorama → **kiểm** → **build Audio/Video qua ElevenLabs → Upload YouTube (`unlisted`) → Nhúng `youtubeId` vào bài viết (`scripts/wms-media-pipeline.py`)** → hàng chờ review.
Xong khi và chỉ khi:

```
   python3 -I scripts/wms-media-pipeline.py --story <khoá> --mode dry-run   (Bước 5A–5D)
   python3 -I scripts/check-story.py      ⇒ FAIL 0      (C0–C9, xem .claude/rules/wms-pipeline-rules.md)
   scripts/wms-check.sh                   ⇒ wms-check: PASS   (check-story + vibe-check của xưởng)
```

Dán nguyên văn dòng "Kết quả" vào báo cáo. Review do agent làm ghi *"same vendor, same priors — no external verifier ran"*.

## Khoá thật vs. advisory — nói đúng phạm vi

| Cơ chế | Giữ được gì | Loại |
|---|---|---|
| `scripts/check-story.py` + `scripts/wms-check.sh` | hình dạng dữ liệu bài, sổ cân; file luật trong repo có mặt, không rỗng, bản chép khớp nhau (C8 — không kiểm được nội dung luật có bị cắt xén) | **KHOÁ THẬT** — script, thoát mã 1. Chỉ khoá khi có người chạy nó |
| `.claude/settings.json` `permissions.ask` | hộp hỏi trước git push · gh pr merge · gh release · vercel · netlify · wrangler | Khoá của harness, **chỉ bắt tiền tố lệnh**; không chạy ở bypass mode; `git -C . push`, script gọi push đều lọt. Ở repo này: **chưa ai thấy hộp hỏi bật** |
| `scripts/wms-hook-guard.sh` qua `.agents/hooks.json` | hỏi Duy khi ghi approvedBy / `published` / đổi `pointer:` / lệnh ship | **Chỉ Gemini/Antigravity**, và hook có chạy thật: **CHƯA XÁC MINH**. Claude Code KHÔNG chạy hook này |
| Luật WMS-R4 "chỉ Duy đăng" trong Claude Code | — | **ADVISORY** — luật trong prompt. Nút *Duyệt & Đăng* là JS, ai bấm cũng được |
| Ẩn bản nháp | giao diện ẩn bài `review` | ADVISORY — nội dung vẫn nằm trong mã nguồn trang |

Nói *"repo này có khoá"* mà bỏ ba dòng cuối của bảng là làm Duy tin vào một bảo đảm không tồn tại.

## Git & Không bao giờ

- **Repo URL:** `https://github.com/duypham9895/where-money-sleeps` (`git@github.com:duypham9895/where-money-sleeps.git`, nhánh làm việc hiện tại: `spec/s1-draft`).
- **Giữ lịch sử từng bước (Duy, 2026-11-08):** Sau mỗi bước hoàn thành và vượt qua `scripts/wms-check.sh` (`FAIL 0`), thực hiện `git commit` (email `duypham9895@gmail.com`, commit message nói **vì sao**) và `git push` lên nhánh đang làm việc (qua cổng xác nhận `permissions.ask` / `force_ask` của Duy).
- **Không bao giờ:** tự ý commit thẳng lên `main` hoặc merge/release/deploy khi Duy chưa duyệt · đổi `pointer:` trong `PIPELINE.md` · sửa tại chỗ một quyết định đã ghi (thêm dòng mới có ngày bên dưới) · dùng âm thanh/ảnh/font chưa nêu được giấy phép trong `legal/licences.json` · nhắc bất kỳ tên riêng / thương hiệu / nhãn hàng / cửa hàng / mạng thanh toán / công cụ hậu trường có thật nào (`ElevenLabs`, `Google`, `Veo`, `Visa`, `Mastercard`, `NAPAS`, `VietQR`, `Hermanson`...) trong khung hình video, mô tả YouTube, lời bình `vo`, chữ trên màn hình `onScreen`, nhãn giao diện hay dữ liệu bài (`LUẬT 4` — `gates/01-spec/VOICE-AND-PROSODY-SPEC.md` §5) · **dừng thụ động chờ Duy hỏi *"tiếp theo là gì?"* hoặc bảo Duy tự gõ `/vibe-stage` sau khi xong việc/duyệt cổng (luôn chủ động khởi tạo bước tiếp theo + đề xuất rõ kế hoạch hành động kèm khuyến nghị).**
