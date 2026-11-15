---
status: pass
stage: 04-qa
date: 2026-11-14
owner: qa
blocked_on: []
---

# AUDIO-POV-AUDIT-REPORT — Kiểm Toán Lời Bình (`POV Người Mới`) & Đồng Bộ Audio Cache (`Where Money Sleeps`)

> **TL;DR (Tóm tắt quyết định):** Đã rà soát toàn bộ `14` kịch bản video (`7` bài × Short + Long) và `7` bộ thuyết minh web (`beats`) dưới góc nhìn người chưa biết tài chính. Xử lý tận gốc cụm gây rối `"Lùi lại giây"` / `"Quay lại đúng giây"` cùng `4` nhóm lỗi hệ thống trên `10/14` track video, đồng bộ `14/14` cache audio khớp `100%` ký tự với `docs/prototype.html`, và render kiểm mẫu cặp `card` (`Short` `70,39s` + `Long` `480,18s`, `0` phụ đề Zone 3).
> **Quan hệ kiểm duyệt (Quy tắc 7):** `same vendor, same priors — no external verifier ran`.

## 1. Nguyên Nhân Gốc Lỗi `"Lùi lại giây"` & Bản Vá Visual Hook (`v7.1`)

- **Nguyên nhân:** Ở cấu trúc cũ, cảnh `0` dùng chung bộ đếm bước hoặc kể lộn ngược dòng thời gian rồi kéo người nghe `"Lùi lại giây..."` (`card.short[1]`), `"Quay lại đúng giây chạm thẻ"` (`card.long[1]`), `"Lùi lại một bước"` (`pay.long[3]`). Khi nghe riêng audio mà không nhìn bảng timeline, người mới tưởng đoạn sau là flashback/sửa sai, không rõ mạch thời gian thực.
- **Khắc phục trong `scripts/wms-render-v50-focus.py`:** Đổi nhãn định hướng sang tiến thẳng từ mốc đầu tiên (`MỞ ĐẦU` → `BƯỚC 1`):
  - `SHORT_SCENES[0]["focal"]["pill"]`: đổi sang `"TIẾP THEO · BƯỚC 1: CHUYỆN GÌ XẢY RA LÚC CHẠM THẺ?"`
  - `LONG_SCENES[0]["hook_data"]["roadmap_title"]`: đổi sang `"LỘ TRÌNH 10 BƯỚC GIẢI MÃ NGAY SAU ĐÂY"`
  - `LONG_SCENES[0]["focal"]["pill"]`: đổi sang `"TIẾP THEO · BƯỚC 1/10: CHUYỆN GÌ XẢY RA LÚC CHẠM THẺ?"`

## 2. Bốn Nhóm Lỗi POV Người Mới & Bảng Sửa Chi Tiết (`10/14` Track Video)

| Nhóm lỗi POV người mới | Vì sao người chưa biết tài chính bị rối | Track bị ảnh hưởng |
|---|---|---|
| **1. Chuyển cảnh "lùi/quay lại" phi tuyến tính** | Gây cảm giác đang nói ngược thời gian sau hook mở đầu | `card.short[1]`, `card.long[1]`, `pay.long[3]` |
| **2. Rò rỉ ẩn dụ web ("con phố 5 nhà / tầng hầm")** | Video tối giản không có phố 5 ngôi nhà hay mặt cắt hầm; người xem nghe không thấy hình sẽ lạc nhịp | `card.long[0]`, `pay.long[0,6,9]`, `install.long[1,2]`, `qr.long[3]`, `offus.short[0]`, `offus.long[0,4,5,7,9]` |
| **3. Tham chiếu bài khác / ghi chú tác giả lộ ra lời thoại** | Người xem video độc lập không biết "bài số một" hay câu nháp `"câu chuyện không có con số này, mình giả sử"` | `card.long[6]`, `qr.long[0,5,6]` |
| **4. Thuật ngữ khô, mã hiệu T+2/số 01, hoặc đọc thô dãy số tài khoản (`511`, `632`, `1388`...)** | Dồn 3–4 số tài khoản liên tiếp làm người mới mất mạch câu chuyện chính về đường đi của tiền | `pay.long[7]`, `minpay.long[1,2,4,5,7]`, `qr.long[5]`, `profitcash.short[1,2,4]`, `profitcash.long[2,3,4,5,7,9]`, `offus.short[5]`, `offus.long[2,5,8]` |

### Bảng đối chiếu từng cảnh đã sửa trong `docs/prototype.html` & `index.html`

| Track · Cảnh | Trước khi sửa (tóm lược cụm lỗi) | Sau khi sửa (giữ nguyên toán & cơ chế) |
|---|---|---|
| `card.short[1]` | `Lùi lại giây bạn chạm thẻ trả hoá đơn mười triệu: lúc đó chưa có đồng nào chạy...` | `Ngay lúc bạn chạm thẻ trả hoá đơn mười triệu: chưa có đồng tiền nào chuyển đi cả, ngân hàng của bạn chỉ tạm giữ chỗ trên hạn mức.` |
| `card.short[2]` | `...quyết toán để tiền thật chảy về quán.` | `...hai ngày làm việc sau, ngân hàng mới chuyển tiền thật về quán.` |
| `card.long[0]` | `...đi dọc một con phố có năm ngôi nhà, và nhìn ba tầng vận hành nối chúng... trong mỗi nhà.` | `...đi qua ba tầng vận hành nối năm bên liên quan: luồng thông tin cấp phép, luồng chuyển tiền thật, và cuốn sổ kế toán ở từng nơi.` |
| `card.long[1]` | `Quay lại đúng giây chạm thẻ.` | `Bắt đầu từ đúng giây bạn vừa chạm thẻ.` |
| `card.long[6]` | `...câu chuyện không có con số này, mình giả sử ví dụ mười nghìn.` | `Một phần nhỏ trả phí cho tổ chức thẻ, ví dụ mười nghìn.` |
| `pay.long[0,3,6,7,9]` | `năm ngôi nhà trên một con phố` · `Lùi lại một bước` · `Ở tầng trên` · `giá nội bộ, gọi là FTP` · `cả con phố` | `năm bên tham gia` · `Giờ nhìn sang cuốn sổ của công ty.` · `Ở chiều ngược lại` · `mức giá vốn nội bộ giữa các bộ phận, gọi là FTP` · `toàn bộ vòng quay` |
| `install.long[1,2]` | `một ngôi nhà khác ở cuối phố` · `Ngôi nhà cuối phố` | `một bên thứ ba khác` · `Bên thứ ba đó` · `về phía công ty tài chính` |
| `minpay.long[1,2,4,5,7]` | `ngày số không một` · `ngày tê cộng hai` · `từ ngân hàng tài khoản thanh toán` · `huỷ hồi tố` · `tín dụng tuần hoàn đang có dư nợ` | `ngày đầu tiên` · `hai ngày làm việc sau đó` · `từ tài khoản thanh toán của mình` · `huỷ toàn bộ thời gian miễn lãi` · `trạng thái mang nợ quay vòng` |
| `qr.long[0,3,5,6]` | `Hãy nhớ lại bài số một` · `phòng giao dịch ngân hàng trung ương` · `Ở tầng trên mặt đất` · `bữa liên hoan ở bài một` · `một ba tám tám` / `một một hai` · `bài tiền lương` | `Thử so sánh` · `trung tâm quyết toán giữa các ngân hàng tại Ngân hàng Trung ương` · `Ngay giây thứ nhất` · diễn đạt lại bằng ngôn ngữ sổ sách/tài khoản thường (`phải thu trên sổ`, `tiền gửi không kỳ hạn`) · `bể vốn tiền gửi không kỳ hạn CASA của ngân hàng` |
| `profitcash.short[1,2,4]` | `Thủ phạm đầu tiên là kế toán dồn tích` · `Thủ phạm thứ hai` · `chi tươi` · `vốn lưu động phình to` | Giải thích thẳng lý do trên đơn hàng/két tiền (`vừa giao hàng xong... sổ sách đã ghi đủ doanh thu ngay`, `tiền hàng tồn kho`, `chi tiền mặt`, `tiền bị giam vào công nợ và hàng tồn kho`) |
| `profitcash.long[2,3,4,5,7,9]` | Đọc miệng mã tài khoản (`năm một một`, `sáu ba hai`, `một năm sáu`, `ba ba tư`, `một một hai`, `một ba một`, `ba bốn một`, `sáu ba lăm`) | Gỡ mã số thừa bằng cắt ghép PCM theo mốc ký tự (`tài khoản Doanh thu bán hàng`, `hàng tồn kho`, `phải trả người lao động`, `dòng tiền thật`, `Phải thu của khách hàng`, `chi phí lãi vay`) — giữ nguyên bản chất & con số TT 99/2025 trên bài viết/bảng |
| `offus.short[0,5]` | `dưới tầng hầm` · `ghi vào tài khoản 113` | `phía sau màn hình` · `tạm ghi vào tài khoản 113 Tiền đang chuyển` |
| `offus.long[0,2,4,5,7,8,9]` | `cắt dọc mặt đất... tầng hầm` · `ngôi nhà đứng giữa` · `ngôi nhà thứ năm trên mặt cắt` · đọc dãy mã `331`/`112`/`131` | `nhìn sâu vào cuốn sổ cái... trung tâm quyết toán` · `đơn vị trung gian đứng giữa` · diễn giải giảm nợ/tăng-giảm tiền trực diện (ElevenLabs `[0,2,4,8]` + cắt PCM `[5,7,9]`) |

## 3. Các Phần Đã Soát & Giữ Nguyên (`4` Track Short + `7` Bộ Web `beats`)

| Nhóm nội dung | Số từ / thời lượng cache | Kết luận audit |
|---|---|---|
| `pay.short` | `240` từ (`69,68s`) | Giải thích rõ Gross `17tr` → Net `15tr` qua khấu trừ, không jargon thừa — giữ nguyên |
| `install.short` | `258` từ (`76,00s`) | Rõ vai công ty tài chính trả `11,4tr` trước cho cửa hàng và người mua trả `12tr` — giữ nguyên |
| `minpay.short` | `245` từ (`67,68s`) | Dùng câu đời thường `"mất quyền miễn lãi từ ngày quẹt thẻ đầu tiên"` — giữ nguyên |
| `qr.short` | `257` từ (`74,08s`) | So sánh trực quan Thẻ trừ `220K` vs QR nhận đủ `10tr` — giữ nguyên |
| `beats` web (`7` bài × `5` beat) | `5` beat/bài | Gắn trực tiếp với giao diện 5 ngôi nhà & tầng hầm ngay trên màn hình web Diorama nên hình–lời đồng bộ, không cần sửa |

## 4. Biên Nhận Đồng Bộ Audio Cache, Video Mẫu `card` & Kiểm Toán Kỷ Thuật

1. **ElevenLabs `eleven_v3` (`JwqRvOqFdGeQNu7UjKjw`) & PCM Hybrid:**
   - Sinh mới hoàn toàn (`3` short): `card_short` (`1.097` ký tự), `profitcash_short` (`1.108` ký tự), `offus_short` (`1.082` ký tự).
   - Vá ghép theo cảnh kèm cân bằng âm lượng RMS (`base_rms` gốc, fading `12–15ms`): `card_long` (`[0,1,6]`), `pay_long` (`[0,3,6,7,9]`), `install_long` (`[1,2]`), `minpay_long` (`[1,2,4,5,7]`), `qr_long` (`[0,3,5,6]`), `offus_long` (`[0,2,4,8]`).
   - Do hết hạn mức ElevenLabs ngay sau batch `offus_long[0,2,4,8]`, thực hiện cắt ghép trực tiếp trên waveform PCM (dò điểm yên lặng ±`16ms`, cross-fade `12ms`, giữ khoảng nghỉ `35ms`) cho các cụm mã số thuần xoá ở `offus.long[5,7,9]` và `profitcash.long[2,3,4,5,7,9]`.
   - Kiểm tra đồng bộ `14/14` file `.cache/elevenlabs/*_continuous_v3.json`: `14/14` khớp `100%` chuỗi `"\n\n".join(vo)` trong `docs/prototype.html`.
2. **Kiểm toán Video mẫu `card` (`wms-render-v50-focus.py --story card --format both`):**
   - `Brand Safety B1–B4 PASS` (`card`: `17` scenes sạch).
   - `dist/youtube/card-short-9x16.mp4`: `6.283.150` bytes (`70,39s`, `2.112` khung, `1080×1920`), kiểm tra `3` khung (`4,5s`, `10,5s`, `23,0s`) đạt nhãn `MỞ ĐẦU` → `BƯỚC 1/5` → `BƯỚC 2/5`, cân xứng tâm, `0` sub Zone 3.
   - `dist/youtube/card-long-16x9.mp4`: `28.973.800` bytes (`480,18s`, `14.405` khung, `1920×1080`), kiểm tra `4` khung (`15,0s`, `32,0s`, `42,0s`, `280,0s`) đạt nhãn `MỞ ĐẦU` → `BƯỚC 1/10` → `BƯỚC 6/10`, lộ trình `10` bước rõ ràng, `0` chồng chữ.
   - Dọn file tạm trong `scratch/`: xoá `18/18` file nháp & khung hình kiểm tra (`28.216.484` bytes giải phóng, còn `0` file).
3. **Cập nhật hoàn tất toàn bộ `14/14` Video + `28/28` Hình Chương `v7.2` & Kiểm âm học `9` cảnh ghép PCM (`2026-11-15` · `commit 3eeaf0d`):**
   - Toàn bộ `14/14` video `.mp4` (`7 Short 9:16 + 7 Long 16:9`) và `28/28` hình minh hoạ chương (`1200×675`) đã kết xuất theo phong cách `v7.2` Paper-Warm Minimalist Craft và đẩy `public` lên `@WhereMoneySleeps` kèm `EXPECTED_YT_IDS` + `STORIES` đồng bộ (`14/14` video đạt chuẩn).
   - **Kiểm âm học tất định trên `9` cảnh cắt ghép PCM (`profitcash.long` & `offus.long`):**
     - `profitcash.long` (`431,72s` · `6.684` ký tự · `44.100 Hz` · `2ch`): `-14,2 LUFS` (`LRA = 2,8 LU`), `RMS = -17,00 dBFS`, `Peak = -1,15 dBFS`, `0` mẫu cắt ngọn (`clipped = 0`), `monotone_errors = 0`; độ lệch RMS giữa toàn bộ các cảnh chỉ `1,08 dB` (`-21,29..-20,21 dBFS`); `6/6` cảnh ghép PCM (`[2,3,4,5,7,9]`) ghi nhận `0` tiếng click (`step > 0,50 fs`), `max_sample_step = 0,1572..0,2310 fs`.
     - `offus.long` (`444,87s` · `6.939` ký tự · `44.100 Hz` · `2ch`): `-14,1 LUFS` (`LRA = 2,8 LU`), `RMS = -16,92 dBFS`, `Peak = -1,20 dBFS`, `0` mẫu cắt ngọn (`clipped = 0`), `monotone_errors = 0`; độ lệch RMS giữa các cảnh chỉ `0,91 dB` (`-21,49..-20,59 dBFS`); `3/3` cảnh ghép PCM (`[5,7,9]`) ghi nhận `0` tiếng click (`step > 0,50 fs`), `max_sample_step = 0,1915..0,2458 fs`.

## 5. Hành Động Tiếp Theo & Chưa Xác Minh Được

- **Phụ đề `.srt` trên YouTube:** Đã bổ sung `step_5c_upload_youtube_captions` và cờ `--upload-captions` + scope `youtube.force-ssl` trong `scripts/wms-media-pipeline.py`; cần Duy chạy `--auth-youtube` `1` lần khi muốn đẩy `14` file `.srt` sẵn có lên YouTube Captions API.
- **Triển khai bản build `v7.2` lên live `wheremoneysleeps.duyslab.icu`:** Đang chờ Duy cấp lại phiên Wrangler (`wrangler login` hoặc `CLOUDFLARE_API_TOKEN` đủ quyền Workers + D1).
- **Nghe kiểm định chủ quan bằng tai người trên `9` cảnh ghép PCM (`profitcash.long[2,3,4,5,7,9]` & `offus.long[5,7,9]`):** Đã đạt toàn bộ ngưỡng kỹ thuật tất định (`-14,2/-14,1 LUFS`, `LRA 2,8 LU`, `0` click, `0` clipping); giữ tuỳ chọn tổng hợp lại thuần một lượt (`eleven_v3`) nếu Duy muốn sau khi quota ElevenLabs gia hạn.
- **Trạng thái kiểm ngoài:** `same vendor, same priors — no external verifier ran`.
