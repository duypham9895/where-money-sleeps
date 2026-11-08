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
