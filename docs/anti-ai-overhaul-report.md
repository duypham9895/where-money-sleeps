# Báo cáo Đại tu Giọng văn Anti-AI & Đóng gói Skill `anti-ai-writing` (`A1–A5`)

**Ngày:** 2026-11-15  
**Nhánh làm việc:** `Vibe` (`feat/anti-ai-writing-skill`) · `where-money-sleeps` (`content/anti-ai-voice-overhaul`)  
**Phạm vi:** Nghiên cứu & đóng gói skill `anti-ai-writing` (`A1–A5`), hồ sơ giọng điệu `VOICE-PROFILE.md`, cổng kiểm tự động `C8`/`C10` trong `scripts/check-story.py`, toàn bộ 7 bài học song ngữ `VI ⇄ EN` (website, `52` thuật ngữ `GLOSS`/`GLOSS_EN`, `7` nhóm `CATEGORIES`/`CATEGORIES_EN`, `36` mục `CHAP_FIGS`/`CHAP_FIGS_EN`, `14` thẻ trắc nghiệm `WMS_QUIZ_BANK`/`WMS_QUIZ_BANK_EN`, `14` kịch bản video `long`/`short`, `28` phụ đề `.srt`/`.en.srt`, bio kênh YouTube `@WhereMoneySleeps` & landing chrome).  
**Ghi chú kiểm chứng:** Đánh giá mù 2 vòng (\`blind REFUTE critic\`: \`e7c8e2bf\` cho EN/cấu trúc và \`abfab109\` cho toàn bộ VI) cùng họ model — **same vendor, same priors — no external verifier ran**. Phương án A giữ nguyên toàn bộ 14 file audio ElevenLabs cũ (\`\$0\` credit, giữ nguyên 14 \`youtubeId\`), tái đồng bộ 28 phụ đề \`.srt\`/\`.en.srt\`, mô tả/kênh YouTube và giao diện web song ngữ \`VI ⇄ EN\`.

---

## 1. Đóng gói Research thành Skill & Cổng Tự động (`A1–A5` + `C8`/`C10`)

1. **Báo cáo nghiên cứu gốc (Final):** [anti-ai-writing-research.md](file:///Users/edwardpham/Documents/Programming/Vibe/docs/anti-ai-writing-research.md) (38.588 bytes).
2. **Skill bản địa `anti-ai-writing` (`A1–A5`):** [SKILL.md](file:///Users/edwardpham/Documents/Programming/Vibe/.agents/skills/anti-ai-writing/SKILL.md) — đồng bộ 6 bản giống hệt nhau trên toàn xưởng (kiểm chứng qua `C8 governance`: `anti-ai-writing khớp giữa 5 bản`), kích hoạt bắt buộc khi tạo/sửa bất kỳ nội dung nào hướng người đọc hoặc người nghe (`LUẬT 14` trong `pm-core.md`, `Vibe/GEMINI.md`, `Vibe/CLAUDE.md`, `where-money-sleeps/GEMINI.md`, `where-money-sleeps/CLAUDE.md`, `docs/departments.md`, `WRITER.md`, `AGENT-CMS-PIPELINE.md`, `vibe-post/SKILL.md`).
3. **Hồ sơ giọng điệu dự án:** [VOICE-PROFILE.md](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/gates/01-spec/VOICE-PROFILE.md) — chốt nhịp câu Đề–Thuyết / SVO, nén chi tiết thừa, "show, don't notify", tách nhịp đọc mắt và nhịp nói `eleven_v3`.
4. **Cổng chặn tất định `C10` & mở rộng `C4`/`C8`:** [check-story.py](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/scripts/check-story.py) kiểm tra độ biến thiên độ dài câu (`Burstiness CV >= 0.40`), trần độ dài câu (`<= 44` từ VI / `<= 42` từ EN), trần dấu gạch ngang `—` (`<= 1` mỗi đoạn), sáo ngữ AI song ngữ, và bổ sung `"Face ID"`, `"Touch ID"` vào `BRANDS` ở `C4`.

---

## 2. Kết quả Đo lường Before vs. After (7 Bài × 2 Ngôn ngữ)

So sánh trực tiếp bản gốc trước đại tu (`origin/main:docs/prototype.html`) với bản hoàn chỉnh trong [docs/prototype.html](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/docs/prototype.html): **tổng lỗi `C10 FAIL` giảm từ `93` xuống `0`** (`0 WARN`).

| Bài | Ngôn ngữ | C10 FAIL (Trước → Sau) | Burstiness CV (Trước → Sau) | Số `—` trong bài (Trước → Sau) | Câu văn dài nhất (Trước → Sau) | Câu VO dài nhất (Trước → Sau) |
|---|---|---:|---:|---:|---:|---:|
| `card` | VI | 5 → **0** | 0.511 → **0.449** | 15 → **0** | 47 → **35w** | 42 → **38w** |
| `pay` | VI | 5 → **0** | 0.545 → **0.484** | 14 → **0** | 50 → **38w** | 44 → **41w** |
| `install` | VI | 6 → **0** | 0.505 → **0.479** | 17 → **2** | 48 → **40w** | 49 → **40w** |
| `minpay` | VI | 8 → **0** | 0.431 → **0.453** | 4 → **1** | 71 → **35w** | 53 → **47w** |
| `qr` | VI | 8 → **0** | 0.560 → **0.474** | 6 → **3** | 92 → **41w** | 58 → **43w** |
| `profitcash` | VI | 8 → **0** | 0.491 → **0.458** | 7 → **1** | 97 → **35w** | 67 → **41w** |
| `offus` | VI | 9 → **0** | 0.393 → **0.454** | 2 → **2** | 77 → **36w** | 58 → **39w** |
| `card` | EN | 6 → **0** | 0.439 → **0.473** | 14 → **0** | 52 → **39w** | 40 → **32w** |
| `pay` | EN | 6 → **0** | 0.392 → **0.456** | 8 → **0** | 48 → **38w** | 48 → **37w** |
| `install` | EN | 7 → **0** | 0.418 → **0.460** | 7 → **3** | 60 → **33w** | 48 → **42w** |
| `minpay` | EN | 5 → **0** | 0.415 → **0.501** | 4 → **3** | 42 → **34w** | 42 → **45w** |
| `qr` | EN | 6 → **0** | 0.441 → **0.494** | 6 → **6** | 49 → **35w** | 45 → **35w** |
| `profitcash` | EN | 8 → **0** | 0.374 → **0.446** | 7 → **0** | 56 → **31w** | 65 → **43w** |
| `offus` | EN | 6 → **0** | 0.406 → **0.432** | 3 → **2** | 41 → **29w** | 51 → **35w** |

*Ghi chú phạm vi:* Toàn bộ số liệu bảng giữ nguyên tuyệt đối cân đối `Σ Debit = Σ Credit`, mã tài khoản `TT 99/2025/TT-BTC`, `youtubeId` cũ, và nhãn `"unofficial summary"` trong văn bản đọc mắt/sổ sách (`AC-52`).

---

## 3. Ví dụ Trước / Sau Cụ thể (`VI` & `EN`)

### Tiếng Việt — Bài viết phổ thông (`qr`, đoạn mở)
- **Trước:** *"Sáng thứ Hai, bạn ghé quán quen mua một ly cà phê giá 50.000 đồng — số ví dụ của bài. Trên mặt quầy gỗ, cạnh chiếc máy quẹt thẻ nằm im lìm là một tấm bảng nhựa in hình vuông đen trắng. Thu ngân mỉm cười chỉ vào tấm bảng..."*
- **Sau:** *"Sáng thứ Hai, bạn ghé quán quen gọi một ly cà phê 50.000 đồng (ví dụ). Trên mặt quầy gỗ, ngay cạnh chiếc máy quẹt thẻ im lìm là tấm bảng nhựa mica in ô vuông đen trắng. Thu ngân chỉ vào tấm bảng: “Anh chị quét mã giúp quán nhé”. Bạn mở ứng dụng ngân hàng, rà ống kính rồi chạm xác nhận."*

### Tiếng Anh — Bài viết phổ thông (`profitcash`, đoạn mở)
- **Before:** *"At two o'clock in the afternoon on the thirty-first of December, an uncomfortable silence settles over the executive boardroom. On the mahogany desk rests an immaculate, audited financial performance report... The board of directors has prepared champagne, and the marketing department has drafted press releases..."* (tiểu thuyết hoá + kịch tính AI).
- **After:** *"Four o'clock on the afternoon of December 31. Two sheets of paper sit side by side on the director's desk at an equipment distributor. On the left lies the closed income statement: 10,000,000,000 VND in Q4 sales (10 billion VND, example). Subtract 6.5 billion in cost of goods sold and 1.5 billion in overhead, and net profit prints 2,000,000,000 VND. On the right glows Account 112 online banking: available checking cash reads 50,000,000 VND."*

### Kịch bản Video / Shorts (`VO`) & Phụ đề `.srt`
- **`profitcash` Shorts VI (cue 0):** *"Chiều ba mươi mốt tháng mười hai, báo cáo công ty ghi lãi ròng hai tỷ đồng, nhưng két ngân hàng chỉ còn năm mươi triệu..."* → *"Chiều ba mươi mốt tháng mười hai: sổ báo lãi hai tỷ, nhưng tài khoản ngân hàng chỉ còn năm mươi triệu. Trong khi đó, bảng lương năm trăm triệu đang chờ chuyển. Tiền đi đâu hết?"*
- **`qr` Shorts EN (cue 0):** *"Why does a coffee shop lose 2.2% in fees and wait two days when you swipe a card, but receives 100%..."* → *"Same 50,000 VND morning coffee sitting on the counter. Why does tapping a credit card cost the shop 2.2%, while scanning a plastic QR stand pays 100% in three seconds flat?"*
- **YouTube & Phụ đề:** Cập nhật bio song ngữ kênh `@WhereMoneySleeps` trong [wms-media-pipeline.py](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/scripts/wms-media-pipeline.py) (`desc_vi` 761 ký tự, `desc_en` 687 ký tự `<= 1000`), `14` mô tả/tiêu đề video và tái xuất đủ `28` file `.srt`/`.en.srt` dưới `dist/youtube/` (ví dụ [qr-long-16x9.srt](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/dist/youtube/qr-long-16x9.srt) và [qr-long-16x9.en.srt](file:///Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps/dist/youtube/qr-long-16x9.en.srt)), áp dụng nội suy khung thời gian thật của audio MP4 hiện hữu để giữ nguyên 100% âm thanh `eleven_v3` đã render.
- **Dữ liệu dùng chung & Landing UI:** Đồng bộ lại toàn bộ `52` mục `GLOSS`/`GLOSS_EN`, `7` nhóm `CATEGORIES`/`CATEGORIES_EN`, `28` hình `CHAP_FIGS`/`CHAP_FIGS_EN`, `14` câu `WMS_QUIZ_BANK`/`WMS_QUIZ_BANK_EN`, cùng tiêu đề/mô tả Landing (`#landingTagline`, `#heroKicker`, `#heroAha`, `#before-h`, `#beforeThree`, `#ftBio`, `renderStories`, `applyStaticChrome`).

---

## 4. Phản biện Mù (`REFUTE Critic` 2 Vòng) & Các Điểm Đã Vá

1. **Vòng 1 (`e7c8e2bf` — EN & cấu trúc, *same vendor, same priors — no external verifier ran*):**
   - **Rò thương hiệu / ngữ cảnh sai:** Gỡ `Face ID` khỏi `qr` EN (`biometrics`) và đưa `"Face ID"`, `"Touch ID"` vào `BRANDS` trong `check-story.py`; đổi `"dân sự"`/`"civil transfer"` ở `qr` sang `"cá nhân"`/`"standard transfer"`; đổi `"pull request"` sang `"pull instruction"`; bỏ `"giao thừa"`/`"New Year's Eve"` ở bối cảnh khoá sổ năm 31/12 sang `"giờ chốt năm"`/`"December 31"`.
   - **Mùi ẩn dụ & khung giảng bài AI:** Bỏ `"miếng bọt biển"`/`"porous sponges"`, `"pipes"` trong lời thoại (`rails`), `"phí chuyển giao"` (`Interchange`), `"câu hỏi bật ra ngay"`, `"Nhờ vậy mà"`, `"Thứ nhất là"`, `"Better yet"`, `"ta đặt"`/`"Ta cộng trừ"`, `"Stepping back"`, `"our working example for today"`; chuẩn hoá câu hỏi tiêu đề EN thiếu `do`/`does`; bớt lặp `"In second one... In second two..."` trong `vo`.
   - **Ngắt nhịp thở VO (`eleven_v3`) & bỏ vướng nói miệng:** Rút dấu ngoặc `(unofficial summary)` khỏi 7 câu `vo:` (giữ nguyên ở chữ đọc mắt/sổ kế toán cho `AC-52`), đồng thời tách các câu VO `>= 49` từ về cặp câu ngắn dễ thở.
2. **Vòng 2 (`abfab109` — Phản biện mù toàn bộ bản Tiếng Việt, *same vendor, same priors — no external verifier ran*):**
   - **52 phát hiện & quét regex toàn kho VI:** Bỏ hoàn toàn cách gọi `"két"`/`"két ngân hàng"` khi nói tới TK 112 (tiền gửi không kỳ hạn) trong `profitcash`, `GLOSS.{workingcapital,ccc}`, `CHAP_FIGS.profitcash`, `WMS_QUIZ_BANK.profitcash` (giữ đúng `"két thu ngân"` vật lý tại quán trong `card`); bỏ dấu lửng `"..."`/`"…"` tách giữa mệnh đề trong mọi `videoScript.{long,short}.scenes[].vo` để tránh phụ đề `.srt` mở cue bằng chữ thường; xoá tham chiếu nội bộ `"Bài 1"` trong `qr`; bỏ mở câu bằng `"Nó "` và câu rào đón phim tài liệu trong `install`, `minpay`, `card`, `pay`, `offus`.

---

## 5. Xác minh Sau Chỉnh sửa Cuối

- `python3 -I scripts/wms-media-pipeline.py --all-stories --mode dry-run`: `B1–B4 PASS` và `F1–F4 PASS` trên cả 7/7 bài (không gọi ElevenLabs live API).
- `python3 -I scripts/wms-studio-sync.py && python3 -I scripts/wms-studio-sync.py --verify`: đồng bộ `docs/wms-studio-data.js` (`1510 KB · hash=785205182ed6de84 · 7 bài · 14 sóng âm MP4 thật`) và `28` file `.srt`/`.en.srt`.
- `python3 -I scripts/wms-build-deploy.py`: đóng gói local `dist/site/` (`37.48 MB`).
- `bash scripts/wms-check.sh`: **`PASS`** — `C8 governance` (`FAIL 0 · WARN 1 · PASS 11 · SKIP 1`), `check-story.py` (`FAIL 0 · WARN 0 · SECONDARY 238 · PASS 138 · SKIP 0`), Tài chính (`FAIL 0 · PASS 51`), Bang-Motion (`FAIL 0 · PASS 22`), Vibe-Check (`PASS — 0 lỗi chặn, 1 cảnh báo` ngân sách >800 dòng trên file JS/render có sẵn).
- `python3 -I scripts/wms-qa-verify.py`: **`PASS`** — `5/5` cụm E2E đạt `100%` (`QA-1..QA-5`, gồm `4/4` viewport Playwright `320·390·768·1440px`).
