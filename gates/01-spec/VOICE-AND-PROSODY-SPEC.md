# Hợp đồng Giọng đọc Đặc trưng, Nhịp điệu Âm thanh & Logic Ngữ cảnh Tự thân (`VOICE-AND-PROSODY-SPEC.md`)

> **Dự án:** `where-money-sleeps` (*Đêm nay, tiền của bạn ngủ ở đâu?*)
> **Stage:** `01-spec` (bổ sung kỹ thuật cho `QĐ 53`, `C9 v2` và `QĐ 56`, ngày `2026-11-08`)
> **Phạm vi:** Áp dụng bắt buộc cho mọi tiêu đề (`title`), câu mở bài (`sub`, `hookNote`, `angle`) và kịch bản lời bình (`videoScript.long.scenes[].vo`, `videoScript.short.scenes[].vo`) trước khi gọi ElevenLabs API hoặc xuất bản.
> **Kiểm tất định:** Được khoá bằng code trong `scripts/check-story.py` (mục `C9`) và `scripts/wms-media-pipeline.py`.

---

## 1. Luật Logic Ngữ cảnh Tự thân — "Đủ 3 Điểm Neo" (3-Anchor Self-Contained Context Rule)

### 1.1. Căn bệnh cần diệt tận gốc
Một người đọc hoặc người xem lướt qua tiêu đề YouTube / Shorts **không hề biết trước kịch bản bên trong**. Viết tiêu đề kiểu ghi chú nội bộ như:
- ❌ *"0% nhưng cửa hàng chỉ nhận 11,4 triệu"* (Thiếu: `0%` là `0%` của cái gì? Giá gốc món hàng là bao nhiêu mà chỉ nhận `11,4 triệu`?)
- ❌ *"Lương về, 0 đồng di chuyển"* (Thiếu: Lương bao nhiêu? Trong điều kiện nào — cùng ngân hàng với công ty — mà `0 đồng` di chuyển?)
- ❌ *"Tiền hoàn của bạn có thể là tiền của chính bạn"* (Thiếu: Giao dịch gì, quy mô bao nhiêu?)

là **lỗi logic cơ bản**: ném ra phần kết quả (`11,4 triệu`) và một con số lơ lửng (`0%`) khi chưa thiết lập **mốc tham chiếu ban đầu (baseline)**.

### 1.2. Công thức bắt buộc: `[Điểm neo 1: Hành động + Quy mô gốc] → [Điểm neo 2: Cơ chế/Lời hứa bề mặt] → [Điểm neo 3: Sự thật hệ thống / Độ lệch]`

Mọi tiêu đề video (`videoScript.long.title`, `videoScript.short.title`) và câu mở màn (`scenes[0].vo`) bắt buộc phải tự chứa đủ **3 điểm neo logic** trong cùng một câu:

| Bài | ❌ Tiêu đề lỗi (Thiếu điểm neo) | ✅ Tiêu đề chuẩn 3 Điểm Neo (Đủ logic tự thân) | Giải phẫu 3 Điểm Neo |
|---|---|---|---|
| `install` (Shorts) | *0% nhưng cửa hàng chỉ nhận 11,4 triệu* | **Mua hàng 12 triệu trả góp lãi suất 0%, vì sao cửa hàng chỉ thực nhận 11,4 triệu?** | (1) Mua hàng `12 triệu` · (2) trả góp lãi suất `0%` · (3) cửa hàng chỉ thực nhận `11,4 triệu` |
| `install` (Long) | *Trả góp 0%: vậy ai đang trả tiền lãi?* | **Mua trả góp 12 triệu lãi suất 0%: ai đang trả 600 nghìn tiền lãi thay bạn?** | (1) Mua trả góp `12 triệu` · (2) lãi suất `0%` · (3) ai trả `600 nghìn` tiền lãi |
| `pay` (Shorts) | *Lương về, 0 đồng di chuyển* | **Nhận lương 15 triệu cùng ngân hàng với công ty: vì sao không đồng tiền nào thực sự di chuyển?** | (1) Nhận lương `15 triệu` · (2) cùng ngân hàng với công ty · (3) không đồng tiền nào di chuyển |
| `pay` (Long) | *Lương về mà không đồng nào di chuyển: tiền của bạn ngủ ở đâu?* | **Lương về 15 triệu mà không đồng nào di chuyển: đêm nay tiền của bạn ngủ ở đâu?** | (1) Lương về `15 triệu` · (2) không đồng nào di chuyển · (3) đêm nay ngủ ở đâu |
| `card` (Shorts) | *Tiền hoàn của bạn có thể là tiền của chính bạn* | **Quẹt thẻ 10 triệu được hoàn 100 nghìn: vì sao tiền hoàn ấy có thể lấy từ chính giá món hàng?** | (1) Quẹt thẻ `10 triệu` · (2) hoàn `100 nghìn` · (3) lấy từ chính giá món hàng (phí MDR 220 nghìn) |
| `card` (Long) | *Đêm nay, 10 triệu bạn vừa quẹt thẻ đang ngủ ở đâu?* | **Quẹt thẻ tín dụng 10 triệu ở nhà hàng: đêm nay tiền thật đang ngủ ở đâu?** | (1) Quẹt thẻ tín dụng `10 triệu` · (2) ở nhà hàng · (3) đêm nay tiền thật ngủ ở đâu |

### 1.3. Phép kiểm tất định trong `scripts/check-story.py` (`C9`)
Script tự động đánh **FAIL** nếu `videoScript.long.title` hoặc `videoScript.short.title`:
1. Ngắn hơn **8 từ** (`nwords(title) < 8`).
2. Mở đầu bằng số phần trăm trơ trọi (`^\s*\d+(?:[.,]\d+)?\s*%`) mà không có danh từ/động từ chỉ hành động đi trước.
3. Chứa cụm từ chỉ phần còn lại/bị trừ (`"chỉ nhận"`, `"chỉ thực nhận"`, `"nhận về"`, `"còn lại"`, `"bị trừ"`) sau liên từ đối lập (`"nhưng"`, `"vì sao"`, `"mà"`) nhưng ở vế trước **không có con số gốc (baseline)** để đối chiếu.

---

## 2. Hồ sơ Giọng đọc Đặc trưng (`Signature Audio Voice Profile` — Chuẩn ECC `brand-voice`)

```text
VOICE PROFILE
=============
Author: Where Money Sleeps — "Người gác đêm nhìn thấu đường ống ngầm" (The Night-Watch Architectural Storyteller)
Goal: Dẫn dắt người nghe đi theo đường đi thật của đồng tiền qua mặt cắt kiến trúc đêm (dây điện trên cao · cuốn sổ kế toán · ống ngầm dưới đất) bằng giọng kể điềm tĩnh, thân mật, sắc sảo, giúp người nghe tự bật ra tiếng "À, hoá ra tiền của mình đi như thế."
Confidence: High (đối chiếu từ ONE-PAGER.md §1–§6 và 3 bài gốc pay, card, install)

Archetype & Tinh thần tham chiếu
- Tinh thần NPR Planet Money / Vox Explainer / Phóng sự điều tra đêm muộn: bình tĩnh, thông tuệ, hơi hóm hỉnh ngầm (wry), nhìn thấu cơ chế mà không lên giọng dạy đời, không hô khẩu hiệu TikTok, không khô khan như đọc biên bản.

ElevenLabs Engine & Voice Configuration (Bắt buộc từ 2026-11-08)
- Model bắt buộc: `eleven_v3` (Flagship Expressive Model của ElevenLabs — tuyệt đối KHÔNG dùng `eleven_flash_v2_5` cho bản phát hành vì `flash` là model đàm thoại độ trễ thấp 75ms nên nhịp đọc bị phẳng).
- Voice Settings chuẩn cho tiếng Việt trên `eleven_v3`:
  + `stability`: 0.65 (đủ mở để `eleven_v3` luyến láy, nhấn trọng âm và hạ giọng ở dấu `...`, nhưng vẫn giữ chuẩn 6 thanh điệu tiếng Việt)
  + `similarity_boost`: 0.80 (giữ độ dày ấm nguyên bản của giọng thu)
  + `style`: 0.20 (kích hoạt sắc thái kể chuyện phóng sự đêm)
  + `use_speaker_boost`: true
- Danh sách Giọng đọc Đề cử (Signature Voice Candidates đã xác minh chạy trực tiếp trên `eleven_v3`):
  1. `JwqRvOqFdGeQNu7UjKjw` — **Tâm** (Nam miền Nam, trầm ấm, nhịp kể chuyện gần gũi, giàu chiều sâu — **Khuyến nghị mặc định**: `eleven_v3:JwqRvOqFdGeQNu7UjKjw`)
  2. `GaEEAHHYlbueVlFfyrPr` — **Tuấn Khang** (Nam miền Bắc, truyền cảm, nhấn nhá rõ, hợp giọng phóng sự điều tra đêm)
  3. `zvKj91MOobqOvPjHamvG` — **Văn Phong** (Nam miền Nam, điềm đạm, kiểu host podcast tài chính đêm muộn)
  4. `cKxI7IOUsPeiDfNgV1cE` — **Tùng Anh** (Nam miền Bắc, rõ chữ, mạch lạc, chuẩn mực)
  5. `rEvzjbRl5jRhZdVEX9vl` — **Nắng Xuân** (Nữ miền Bắc, trầm sâu, sắc sảo, giàu nội lực)
```

---

## 3. Năm Quy tắc Viết Kịch bản Cho Tai Nghe (`Prosody-Engineered Spoken Script`)

1. **CẤM đặt đuôi pháp lý `", ví dụ."` / `", vẫn là số ví dụ."` ở cuối câu (`End-Focus Sabotage`):**
   - Chữ cuối cùng của câu/cảnh là nơi TTS dồn trọng âm kết (Final Lengthening). Đặt `", ví dụ."` ở cuối câu làm giọng đọc rơi phịch xuống một từ hành chính cụt lủn.
   - **Cách viết đúng:** Đưa giả định lên **đầu câu hoặc đầu mệnh đề** như một lời mời bước vào tình huống: *"Giả sử bạn mua chiếc máy mười hai triệu..."*, *"Trong ví dụ mười hai triệu này,..."*, *"Ở ví dụ này,..."*.
   - **Khoá tất định (`check-story.py`):** Mọi mẫu `,\s*(?:vẫn là số\s+|cũng là\s+|chỉ là\s+)?ví dụ(?:\s+thôi)?\s*[.?!]` hoặc câu `"Vẫn là số ví dụ."` / `"Tất cả là số ví dụ."` trong `vo` đều bị đánh **FAIL**.
2. **CẤM băm câu kiểu điện tín (Staccato Telegraphic Periods):**
   - Không viết 3 câu ngắn dưới 6 chữ chấm câu liên tiếp (*"Trả góp không phần trăm. Mười hai triệu, mười hai kỳ, ví dụ."*). Mỗi dấu `.` buộc TTS hạ cao độ về đáy (Pitch Reset), tạo cảm giác đọc từng chữ rời rạc.
   - **Cách viết đúng:** Mở cảnh bằng một hành động đời thực gắn với con số gốc (*"Bạn cầm chiếc máy mười hai triệu bước ra khỏi cửa hàng mà chưa tốn một đồng lãi..."*).
3. **Điều khiển nhịp thở và trọng âm của `eleven_v3` bằng dấu `:` · `—` · `...`:**
   - Dùng dấu hai chấm `:` sau cụm dẫn thị giác (*"Nhìn lên dây điện trên cao:"*, *"nhưng nhìn kỹ con số mà xem:"*) để `eleven_v3` nâng nhẹ cao độ mở ra phát hiện mới.
   - Dùng dấu ba chấm `...` hoặc gạch ngang `—` ngay trước vế lật ngược vấn đề (The Reveal) để tạo **khoảng lặng lơ lửng (~250ms)** giữ cao độ trước khi nhả con số đắt giá (*"Sáu trăm nghìn bị giữ lại lúc giải ngân... chính là năm phần trăm hỗ trợ lãi suất cửa hàng trả thay bạn."*).
4. **Tương phản Nhịp sóng (Wave Cadence):**
   - Xen kẽ giữa câu dẫn có độ trôi (16–22 âm tiết, có nhịp nghỉ `,` hoặc `...` ở giữa) với câu chốt ngắn, sắc gọn (6–9 âm tiết: *"Từ giây đó, chủ nợ là họ."* / *"Khoảng chênh lộ ra... chính là tiền lãi."*).
5. **Mọi con số trong `vo` viết bằng chữ tiếng Việt kèm từ đệm dẫn nhịp:**
   - Không xả 5–6 con số liên tiếp không có từ chuyển ý. Luôn dùng từ đệm tạo nhịp tư duy (*"Đổi lại,"*, *"Tức là"*, *"Đặt hai con số cạnh nhau:"*).

---

## 4. Chuẩn Chuyển Tiếp Mượt Mà — Audio & Visual Continuity Standard (Cập nhật 2026-11-08)

### 4.1. Căn bệnh "Đứt gãy Chuyển cảnh" (Abrupt Scene Cuts) cần triệt tiêu
Khi dựng video từ nhiều cảnh (`scenes[0..5]`):
1. **Lỗi Audio:** Gọi TTS rời rạc từng cảnh rồi ghép bằng `ffmpeg -f concat` khiến mô hình thần kinh reset lại cao độ/âm sắc ở đầu mỗi cảnh, đồng thời khoảng nghỉ giữa hai cảnh rơi thẳng về mức "im lặng chết" (`-inf dB`).
2. **Lỗi Hình ảnh:** Cắt cứng (`0-frame hard cut`) giữa các tấm nền tĩnh, đập toàn bộ khối chữ 6–7 dòng lên màn hình cùng lúc, và nhảy cóc trạng thái 5 ngôi nhà trong `0.00s`.

### 4.2. Kiến trúc Chuyển Tiếp Âm Thanh Liền Mạch (`Continuous Audio Master`)
1. **Thu liền mạch 1 lần đọc (`Single-Take Continuous eleven_v3`):**
   - Nối toàn bộ lời bình các cảnh bằng `\n\n` (`"\n\n".join(scene_texts)`) và gửi trong **một request duy nhất** tới `/v1/text-to-speech/{voice_id}/with-timestamps` với `model_id: "eleven_v3"`.
   - Nhờ đọc liền mạch, giọng đọc giữ nguyên một hơi thở, một đường cong cảm xúc xuyên suốt từ giây đầu tới giây cuối, kèm khoảng lấy hơi tự nhiên `0.48s–0.66s` giữa các cảnh.
2. **Cầu nối Hơi thở Mềm (`0.36s Cosine-Crossfaded Breath Bridge`):**
   - Tại điểm giữa của khoảng lấy hơi tự nhiên giữa hai cảnh, mở rộng thêm `0.36s` với đường fade cosine `25ms` để tổng thời gian chuyển giao đạt `~0.85s–0.95s` — khớp hoàn hảo với thời gian chuyển cảnh thị giác.
3. **Lớp nền Không gian Đêm & Hiệu ứng Chuyển cảnh (`Warm Night-Watch Bed + ElevenLabs SFX`):**
   - Phủ xuyên suốt một lớp nền **Analog Night-Watch Room Tone** ấm áp ở mức `-33 dBFS` (tuyệt đối không có khoảng trống `-inf dB`).
   - Điểm xuyết **6 hiệu ứng âm thanh chuyển cảnh tinh tế** sinh từ ElevenLabs `/v1/sound-generation` ở mức `-22 dBFS` ngay tại ranh giới chuyển cảnh:
     + Mở bài: `sfx_lamp_switch` (tiếng bật đèn bàn dây tóc ấm)
     + Sang Cảnh 2 (Dây điện trên cao): `sfx_wire_pulse` (xung tín hiệu analog lướt qua dây)
     + Sang Cảnh 3 (Ống ngầm quyết toán): `sfx_pipe_flow` (dòng chảy trầm ấm trong đường ống ngầm)
     + Sang Cảnh 4 (12 kỳ trả góp): `sfx_clock_tick` (nhịp đồng hồ cơ đều đặn)
     + Sang Cảnh 5 (So sánh giá mặt): `sfx_scale_chime` (tiếng ngân nhẹ của chiếc cân đồng)
     + Sang Cảnh 6 (Kết bài): `sfx_shutter_close` (tiếng cửa cuốn phố đêm khép nhẹ)
   - Chuẩn hoá tổng thể về **`-14 LUFS`** (`TP <= -1.5 dBTP, LRA = 11`).

### 4.3. Kiến trúc Chuyển Tiếp Hình Ảnh 30fps (`Continuous 30fps Visual Compositor`)
1. **Chuyển cảnh `0.95s Smoothstep Cross-Dissolve` + `Camera Glide`:**
   - Sử dụng bộ **4 tấm tranh Mặt cắt Kiến trúc Đêm 9:16** (`install-short-plate-1..4.jpg`: Quầy cửa hàng · Ống ngầm quyết toán · Dây điện & Tháp tài chính · Toàn cảnh 5 ngôi nhà & Chiếc cân đồng).
   - Máy quay lướt liên tục (`pan + zoom` nội suy mượt bằng `smoothstep`) và hoà tan (`cross-dissolve 0.96s`) giữa hai cảnh, tuyệt đối không dùng `hard cut`.
2. **Thanh Đường Ống 5 Ngôi Nhà Chuyển Động Trực Tiếp (`30fps Live Animated Conduit Bar`):**
   - Độ sáng của 5 ngôi nhà (`1. Bạn · 2. Cửa hàng · 3. C.ty TC · 4. NH Bạn · 5. NH CH`) nội suy mượt (`lerp`) khi chuyển cảnh.
   - Hạt tín hiệu vàng chạy dọc dây điện trên cao ở Cảnh 2; giọt tiền thật xanh ngọc chảy dọc ống ngầm ở Cảnh 3 & Cảnh 4 (kèm bộ đếm trực tiếp `KỲ 1/12 .. KỲ 12/12`).
3. **Phụ đề Cuốn Chiếu Từng Cụm & Tô Sáng Từng Từ (`Phrase-by-Phrase Progressive Captions`):**
   - Mỗi cảnh được chia thành **3–5 cụm câu ngắn** (`12–20 chữ`, tối đa 2–3 dòng mỗi lần hiển thị), trượt nhẹ từ dưới lên (`ease-out 0.28s`) khi sang cụm câu mới.
   - Từng từ được đồng bộ tới `0.01s` theo `alignment.character_start_times_seconds` của ElevenLabs: từ đang đọc được bọc viên thuốc phát sáng vàng ấm (`#FFD166`), các con số neo tài chính giữ màu vàng kim sau khi đọc xong, giúp mắt người xem lướt theo giọng kể một cách tự nhiên.

---

## 5. Luật Cấm Nhắc Tên Riêng & Thương Hiệu Có Thật — Zero Real-Brand & Proper-Noun Policy (Khoá cứng 2026-11-08)

### 5.1. Năm Nguyên lý Gốc (First Principles) vì sao KHÔNG BAO GIỜ nhắc tên riêng có thật
1. **Bảo vệ Pháp lý & Chống Rủi ro Quy chụp Thương hiệu (Legal & Trade Libel Immunity):**
   - Khi bóc tách cơ chế *phí ẩn, chiết khấu thương nhân, hỗ trợ lãi suất 0%, giữ chỗ hạn mức, hay chênh lệch lãi suất*, nếu gắn bất kỳ tên ngân hàng, công ty tài chính, ví điện tử, mạng thẻ, hay chuỗi cửa hàng có thật nào vào ví dụ, người xem sẽ hiểu nhầm rằng sản phẩm đang tố cáo đích danh đơn vị đó thu phí cao hoặc gài bẫy. Dùng **nhân vật nguyên mẫu hệ thống (System Archetypes)** triệt tiêu 100% rủi ro khiếu nại thương hiệu (defamation / trade libel).
2. **Bảo toàn Bức Tường Thứ Tư & Thế giới Kể chuyện Đêm (Fourth Wall & Narrative Immersion):**
   - *Where Money Sleeps* là một không gian khảo cứu tĩnh lặng lúc nửa đêm. Việc để lọt tên công cụ hậu trường (*ElevenLabs, Google, Veo, Gemini, Claude, OpenAI*) hay tên tác giả sách giáo khoa (*Hermanson, Edwards & Maher*) vào khung hình video, dòng chữ dưới đáy video, mô tả YouTube, hoặc giao diện người đọc sẽ **đập vỡ ngay lập tức thế giới mặt cắt kiến trúc đêm** và biến tác phẩm thành một bản demo kỹ thuật.
3. **Tính Phổ quát & Vượt Thời gian của Nguyên mẫu (System Archetype Universality & Timelessness):**
   - Tên thương hiệu, ứng dụng hay cổng thanh toán có thể đổi tên, sáp nhập hoặc biến mất sau vài năm; nhưng **5 vai nguyên mẫu trong hệ thống tài chính** (*Người mua · Cửa hàng / Quán quen · Ngân hàng của quán · Tổ chức chuyển mạch thẻ / Chuyển mạch liên ngân hàng · Ngân hàng phát hành / Công ty tài chính*) là cấu trúc bất biến của kế toán kép và thanh toán hiện đại.
4. **Không Quảng cáo Không Công & Giữ Trọng tâm Nhận thức (Zero Unpaid Brand Plug & Cognitive Focus):**
   - Nhắc tên một nhãn hàng cụ thể kích hoạt định kiến sẵn có của người nghe về nhãn hàng đó (*"Hãng X tốt hay xấu"*), làm chệch hướng sự chú ý khỏi bản chất kế toán (`Σ Debit = Σ Credit`, dòng lời nhắn trên dây điện và dòng tiền thật dưới ống ngầm).
5. **An toàn Bản quyền Nhãn hiệu & Phân phối Đa nền tảng (Trademark & Platform Brand Safety):**
   - Video và bài viết hoàn toàn sạch bóng tên thương hiệu thứ ba giúp xuất bản tự nhiên trên mọi nền tảng mà không bao giờ vướng bộ lọc thương hiệu hay tranh chấp nhãn hiệu.

### 5.2. Từ điển Chuyển đổi Nguyên mẫu Chuẩn (Canonical Generic Archetype Dictionary)

| Nhóm bị cấm tuyệt đối (`BRAND_RE` FAIL) | CẤM viết (Thương hiệu / Tên riêng có thật) | BẮT BUỘC dùng (Nguyên mẫu Hệ thống — Generic Archetype) |
|---|---|---|
| **1. Công cụ AI, Voice, Video & Nền tảng** | `ElevenLabs`, `Google`, `Veo`, `Gemini`, `Claude`, `OpenAI`, `ChatGPT`, `TikTok`, `Reels`, `Facebook`, `Zalo` | Không nhắc trong nội dung/video/mô tả kênh; trên UI gọi là *"Giọng kể chuyên mục"*, *"Video Dọc 9:16"*, *"Video Dài 16:9"* |
| **2. Tổ chức thẻ & Mạng chuyển mạch** | `Visa`, `Mastercard`, `JCB`, `Amex`, `UnionPay`, `NAPAS`, `VietQR`, `VNPay`, `Payoo` | `Tổ chức thẻ`, `tổ chức chuyển mạch thẻ`, `hệ thống chuyển mạch liên ngân hàng`, `mã QR` |
| **3. Ngân hàng thương mại & Ngân hàng số** | `Vietcombank`, `Techcombank`, `VPBank`, `BIDV`, `ACB`, `MBBank`, `TPBank`, `HSBC`, `Timo`, `Cake`... | `Ngân hàng của bạn` (`Issuer`), `Ngân hàng của quán / cửa hàng` (`Acquirer`), `Ngân hàng trả lương` |
| **4. Công ty tài chính & Mua trước trả sau** | `FE Credit`, `Home Credit`, `HD Saison`, `Mcredit`, `Mirae Asset`, `Kredivo`, `Fundiin`, `Atome`... | `Công ty tài chính`, `bên cho vay trả góp`, `đơn vị cấp tín dụng tiêu dùng` |
| **5. Ví điện tử & Cổng thanh toán** | `MoMo`, `ZaloPay`, `Viettel Money`, `ShopeePay`, `Apple Pay`, `Google Pay`, `Samsung Pay`... | `Ví điện tử`, `ứng dụng thanh toán`, `tài khoản trung gian thanh toán` |
| **6. Chuỗi cửa hàng, Sàn TMĐT, Hãng & Quán** | `Thế Giới Di Động`, `Điện Máy Xanh`, `FPT Shop`, `Shopee`, `Lazada`, `Apple`, `iPhone`, `Samsung`, `Highlands`, `Starbucks`, `Quán Nhà Liên`... | `Cửa hàng`, `Quán quen` (`QUÁN ĂN QUEN`), `Sàn thương mại điện tử`, `chiếc điện thoại`, `món hàng` |
| **7. Tên riêng tác giả trong khung hình video** | `Hermanson, Edwards & Maher` in ở footer video | Chỉ lưu nguồn học thuật trong `legal/licences.json`; trên video dùng dòng chữ nguyên mẫu: `WHERE MONEY SLEEPS · ĐÊM NAY, TIỀN CỦA BẠN NGỦ Ở ĐÂU? · SỐ LIỆU VÍ DỤ MINH HOẠ CƠ CHẾ` |

### 5.3. Cổng kiểm Tất định (`scripts/check-story.py` — `BRAND_RE`)
- `scripts/check-story.py` quét `BRAND_RE` trên **toàn bộ** `all_text(s)` (5 đoạn Diorama), `article_text(s)` (bài sâu `lay` + `pro` + kịch bản video `long` + `short`), `houses` (`label`, `sign`, `fxText`), `GLOSS` và `CATEGORIES`. Bất kỳ tên riêng nào trong 7 nhóm trên xuất hiện sẽ lập tức trả về **`FAIL C9`**.


