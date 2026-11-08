---
name: vibe-post
description: >-
  Biến một câu ý tưởng thành một bài mới cho Where Money Sleeps theo pipeline 6 bước của QĐ 53 + QĐ 56:
  phân loại danh mục → 5 đoạn kể hai góc nhìn → bài khảo cứu 2 tầng + kịch bản video 2 định dạng (C9 v2) → Mặt cắt Kiến trúc Diorama v3.0 → kiểm bằng
  check-story.py + ke-toan-reviewer → build Audio/Video từ ElevenLabs + upload YouTube (unlisted) + nhúng youtubeId vào bài viết (wms-media-pipeline.py) → hàng đợi Preview 1:1 (status "review") cho Duy duyệt.
  Dùng khi Duy gõ "/vibe-post <ý tưởng>", "/vibe:post <ý tưởng>", hoặc đưa ý tưởng một bài/chủ đề mới.
  KHÔNG BAO GIỜ tự đăng bài.
---

<!-- Bản gốc nằm trong repo where-money-sleeps (2026-11-08). Hai bản .claude/skills/vibe-post/SKILL.md và
     .agents/skills/vibe-post/SKILL.md phải giống nhau TỪNG BYTE — scripts/check-story.py C8 kiểm.
     Mọi đường dẫn dưới đây tương đối với gốc repo where-money-sleeps. -->

# /vibe-post — từ một câu ý tưởng tới một bài chờ Duy duyệt

**Hợp đồng gốc:** `gates/01-spec/AGENT-CMS-PIPELINE.md`. Đọc file đó trước khi bắt đầu; khi skill này
và hợp đồng lệch nhau, **hợp đồng thắng**. Luật WMS-R1..R5 tóm ở `CLAUDE.md` / `GEMINI.md` của repo.

## Khoá thật vs luật trong prompt — nói đúng phạm vi

```
   KHOÁ THẬT   scripts/check-story.py — script, thoát mã 1 khi FAIL (hình dạng dữ liệu bài + C8 bộ luật + C9 v2 bài sâu & video 2 định dạng).
               scripts/wms-check.sh   — check-story + vibe-check của xưởng (SKIP nếu repo đứng một mình).
   CÓ ĐIỀU KIỆN scripts/wms-hook-guard.sh qua .agents/hooks.json — bắt hộp hỏi khi ghi approvedBy /
               status "published" / đổi pointer / lệnh ship. Antigravity có chạy hook thật không:
               CHƯA XÁC MINH. Claude Code KHÔNG chạy hook này.
   ADVISORY    Mọi thứ còn lại trong file này, kể cả luật "agent không tự đăng".
               Nút "Duyệt & Đăng" trong prototype là JS ai bấm cũng được, không lưu.
```

## Đầu vào

Một câu ý tưởng của Duy. Thiếu gì thì **hỏi một câu một lần, kèm khuyến nghị** (quy tắc 9 của xưởng) —
không tự đoán danh mục mới, không tự đoán con số.

## Sáu bước — làm đúng thứ tự, mỗi bước có cổng ra

| Bước | Làm gì | Cổng ra |
|---|---|---|
| **1. Phân loại & "Cái À"** | Đọc `CATEGORIES` trong `docs/prototype.html`. Chọn danh mục có sẵn, hoặc **đề xuất** danh mục mới và hỏi Duy. Viết một câu hỏi mở màn mà câu trả lời làm người đọc *"à"*. | Trả lời được trong 5 đoạn; không phải lời khuyên đầu tư (không mã CK, không "nên mua") |
| **2. 5 đoạn + 2 góc nhìn** | `beats[0..4]`, mỗi đoạn đủ mọi trường ở hợp đồng §1 (`when`, `sub`, `title`, `say[]` ≤ 3 câu, `lit`, `tags`, `msgs`, `fx`, `life` = Đời thường, `sys` = Sổ kế toán, `ledger` hoặc `null`). Thuật ngữ chuyên ngành viết `[[nhãn\|khoá]]` và thêm vào `GLOSS` (giữ tiếng Anh, chú thích tiếng Việt). | Mọi con số giả định có `<span class="ex">ví dụ</span>`; giọng theo `gates/01-spec/WRITER.md` |
| **2b. Bài khảo cứu 2 tầng + Studio Kịch bản Video** *(luật C9 v2 + QĐ 56, 2026-11-08)* | Thêm `article` và `videoScript` vào bài (khuôn ở hợp đồng §1). **A · `article.lay`** cho người không chuyên: `myths[{myth,truth}]` ≥ 3 (không bịa thống kê kiểu "90%") · `sections[{h,paras[]}]` ≥ 4 chương, ≥ 850 từ: tình huống đời thực → giải phẫu đường đi của tiền & lời nhắn → động cơ kinh tế từng bên → bức tranh lớn (**không** có `body`) · `flowSummary[{step,channel,fromTo,amount,essence}]` ≥ 4, `channel` = `wire` (lời nhắn trên dây) · `pipe` (tiền thật trong ống ngầm, khớp `msgs` có `"money"`) · `book` (ghi sổ nội bộ) · `roles[]` đúng 1 vai cho mỗi nhà theo thứ tự, `who` = nhãn nhà · `whenHelps[]` / `whenTraps[]` ≥ 3 mỗi bên, viết ở ngôi thứ ba về **cơ chế**, không ra lệnh cho người đọc, không tên ngân hàng · `takeaways[]` ≥ 4 câu hỏi tự soi. **B · `article.pro`**: `mechanics[{h,p}]` ≥ 4, ≥ 450 từ (thanh toán bù trừ ròng, cấu trúc phí, FTP, dự trữ bắt buộc, DCF/IRR/EIR có ví dụ tính) · `accountingNotes[]` ≥ 4, ≥ 180 từ (sổ DN TT 99/2025 vs nguyên lý sổ ngân hàng — không số hiệu TK ngân hàng; nêu rõ điểm FLAG chờ người ký) · `journal[]` ≥ 3 bút toán từ phát sinh tới tất toán, y khuôn `ledger` + `step` · `edgeCases[{h,p}]` ≥ 3 × 50 từ. **C · `videoScript.long`** (YouTube 16:9, 8–10 phút): `title` · `hookNote` · `youtubeId` (`""` khi chờ upload hoặc 11 ký tự) · `embedStatus` (`"pending_upload"` \| `"uploaded_unlisted"` \| `"uploaded_private"` \| `"uploaded_public"`) · `elevenlabsVoiceId` (vd: `"eleven_flash_v2_5:vi_editorial"`) · `scenes[]` 10–12 cảnh (Hook `beat:null` → 5 cảnh `beat` 0..4 + cảnh đào sâu → Kết `beat:null`), mỗi cảnh `time` · `chapter` · `visual` · `vo` · `onScreen`. **`videoScript.short`** (YouTube Shorts 9:16): `title` · `angle` (cú twist đắt nhất) · `youtubeId` · `embedStatus` · `elevenlabsVoiceId` · `scenes[]` 5–6 cảnh. `vo` văn nói tự nhiên cho ElevenLabs, số đọc thành chữ, không markup; `onScreen` chữ/số + gợi ý SFX chung chung. | C9 v2 + QĐ 56: ngưỡng ở hợp đồng §1. Dài: lời bình ≥ 1.350 từ (nhắm 1.450–1.650 ≈ 8–9 phút), kết 7:30–10:30 (script FAIL ngoài 7:30–11:00). Ngắn: lời bình 150–260 từ (nhắm 170–240), kết 0:55–1:30 (FAIL ngoài 0:55–1:35). Có đủ `youtubeId`, `embedStatus`, `elevenlabsVoiceId` ở cả `long` và `short`; bài chưa `published` cấm đặt `embedStatus: "uploaded_public"`. Số khớp 5 đoạn; số mới gắn "ví dụ" và tính bằng code; không điều luật, URL, thống kê không nguồn, tên ngân hàng thương mại, câu khuyên (script grep) |
| **3. Mặt cắt Diorama v3.0** | `houses[5]` chỉ dùng archetype có sẵn — khoá của `const TYPES` trong khối SCENEJS (`home shop acq scheme crowd iss pbank co lend`); đổi chữ cứng bằng `sign` / `fxText`. Lời hứa, hợp đồng, hồ sơ, lệnh cấp phép ⇒ dây trên: `[từ, tới]`. Tiền thật (quyết toán, giải ngân, trả nợ, nộp thuế/phí) ⇒ ống ngầm: `[từ, tới, "money"]`. `ledger` theo TT 99/2025, có `assume`; tiền thẻ chờ quyết toán / phải thu từ ngân hàng thanh toán ghi TK 1388, không TK 131; lương qua TK 334. **Không sửa khối SCENECSS/SCENEJS** trừ khi thêm archetype — sửa thì chép nguyên khối sang mọi bản xem nhanh. | Luật D1–D7 của hợp đồng. Không archetype nào hợp ⇒ **dừng và đề xuất**, không vẽ hộp phẳng |
| **4. Kiểm** | Từ gốc repo: `python3 -I scripts/check-story.py --story <khoá>`, rồi `scripts/wms-check.sh`. Rồi gọi subagent **ke-toan-reviewer** cho mọi bài có con số hoặc bút toán. Chép **nguyên văn** dòng tổng của nó vào `review.ketoan` kèm ngày; sửa bài sau đó mà chưa chạy lại thì thêm `"(trước khi sửa; chưa soát lại)"` — không tự tóm thành số nhỏ hơn. | **FAIL 0** ở cả hai script. FAIL của ke-toan-reviewer ⇒ sửa, chạy lại cả hai. 3 vòng vẫn FAIL ⇒ leo thang lên Duy |
| **5. Build Audio & Video qua ElevenLabs → Upload YouTube → Nhúng vào bài viết** *(QĐ 52 · QĐ 56, 2026-11-08)* | Chạy `python3 -I scripts/wms-media-pipeline.py --story <khoá>` thực thi 4 bước khép kín: **(5A) Build Audio + Timestamps + SFX qua ElevenLabs API:** Gọi `POST /v1/text-to-speech/{voice_id}/with-timestamps` (`eleven_flash_v2_5` + `previous_text`/`next_text`) và `POST /v1/sound-generation` cho các gợi ý SFX trong `onScreen`, lưu qua SHA-256 content-hash cache (`.cache/elevenlabs/{sha256}.json`). **(5B) Render Video `.mp4`:** Đồng bộ Mặt cắt Diorama v3.0 với `alignment` timestamps của ElevenLabs (chuẩn âm lượng `-14 LUFS`), xuất `dist/youtube/<khoá>-long-16x9.mp4` (`1920×1080`) và `dist/youtube/<khoá>-short-9x16.mp4` (`1080×1920`). **(5C) Upload lên YouTube:** Đẩy lên qua `YouTube Data API v3` (`videos.insert`), bắt buộc đặt `privacyStatus: "unlisted"` (hoặc `"private"` — nhờ `"unlisted"`, video nhúng xem thử được trong `?preview=1` mà không lộ công khai trên kênh), nhận về mã `youtubeId` 11 ký tự cho bản Dài và Shorts. **(5D) Nhúng ngược Video YouTube vào bài viết:** Ghi ngược `youtubeId` 11 ký tự và `embedStatus: "uploaded_unlisted"` vào `STORIES[<khoá>].videoScript.long` và `STORIES[<khoá>].videoScript.short` trong `docs/prototype.html` (`--bind-long-id <id> --bind-short-id <id> --embed-status uploaded_unlisted`) để khung trình phát `youtube-nocookie.com/embed/<youtubeId>` hiển thị trực tiếp ở đầu bài viết (`#pnl-lay` và `#pnl-vid`). Chưa có API key ở môi trường local ⇒ chạy `--mode dry-run` để xuất `dist/youtube/<khoá>-elevenlabs-youtube-manifest.json`, giữ `youtubeId: ""`, `embedStatus: "pending_upload"`, và ghi rõ trong báo cáo. | Có mục `elevenlabs-commercial-tts-sfx` trong `legal/licences.json` (gói trả phí có Commercial License — quy tắc 4). Trình nhúng `.yt-embed` hiển thị trong bài viết (`#pnl-lay` & `#pnl-vid`). Mọi lệnh upload YouTube đều qua cổng hỏi Duy (`force_ask`); **CẤM** tự đặt `embedStatus: "uploaded_public"` khi bài chưa `published` |
| **6. Hàng đợi Preview 1:1** | Thêm bài vào `STORIES` với `status: "review"`, `approvedBy: ""`, `review.draftedBy: "agent"`; thêm `{story:"<khoá>"}` vào đúng danh mục trong `CATEGORIES`. Chạy lại `python3 -I scripts/check-story.py` và `scripts/wms-check.sh`. | Dừng. Nói đúng câu dưới đây |

## Kết thúc — luôn nói đúng câu này

> *"Bài `<khoá>` ở `status: review` (Video YouTube nhúng trong bài ở `embedStatus: uploaded_unlisted` / `pending_upload`). Mở `docs/prototype.html?preview=1` để xem cả bài viết lẫn trình phát YouTube nhúng đúng như người đọc.
> Tôi không tự đăng được — chỉ Duy chuyển sang `published` / `uploaded_public`."*

Kèm theo: kết quả `check-story.py` (dán nguyên văn dòng "Kết quả"), bảng của ke-toan-reviewer, và mục
**"chưa xác minh được"**. Báo cáo review ghi *"same vendor, same priors — no external verifier ran"*.

## Không bao giờ

- Đặt `status: "published"` hay điền `approvedBy` — kể cả khi Duy nói "ok" trong chat mà chưa có dòng quyết định có ngày.
- Viết "0 lỗi kế toán" khi ke-toan-reviewer chưa chạy, hoặc gọi agent là "kế toán".
- Đưa bài vào hàng chờ khi thiếu một trong 3 trụ C9 v2 (bài khảo cứu · phân tích chuyên sâu · kịch bản video dài + ngắn) — bài sơ sài không phải bài nháp, là bài chưa xong.
- Gõ số đếm cứng (số danh mục, số bài) vào giao diện — mọi số suy từ dữ liệu.
- Đổi tên khoá bài (`STORIES` key) đã đăng — đó là hợp đồng với tiến độ của người đọc (QĐ 52).
