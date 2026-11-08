# Quy tắc Pipeline & Mặt cắt Diorama v3.0 — Where Money Sleeps

File này nằm trong `.claude/rules/` để Claude Code tự nạp khi làm việc trong repo. Hợp đồng gốc: `gates/01-spec/AGENT-CMS-PIPELINE.md`.

## 1. Bảng mã kiểm tất định (`scripts/check-story.py`)

| Mã | Kiểm gì | Lệch ⇒ |
|---|---|---|
| `C0` | Cú pháp JS của `<script>` cuối trong `docs/prototype.html` (`node --check`) | `FAIL` |
| `C1` | Taxonomy 3 cấp: `CATEGORIES` → `topics` → `STORIES`; khoá bài hợp lệ, nằm đúng 1 chủ đề | `FAIL` |
| `C2` | Đúng 5 nhà `houses[0..4]` thuộc `const TYPES` trong `SCENEJS`; đúng 5 đoạn `beats[0..4]` | `FAIL` |
| `C3` | Mọi chỉ số nhà trong `lit`, `tags`, `msgs` ∈ `0..4`; `from != to` | `FAIL` |
| `C4` | Tách 2 luồng vật lý: dây điện `[từ, tới]` (lời nhắn) vs ống ngầm `[từ, tới, "money"]` (tiền thật) | `FAIL` / `WARN` |
| `C5` | Mọi thuật ngữ `[[nhãn\|khoá]]` đều có trong `GLOSS` | `FAIL` |
| `C6` | Sổ kế toán kép TT 99/2025: `Σ Nợ == Σ Có`, không dùng TK 131 cho phải thu từ NH thanh toán (dùng TK 1388), đối chiếu `legal/tt99-phu-luc-ii.secondary.json` | `FAIL` / `SECONDARY` |
| `C6v` | Con số giả định có nhãn `<span class="ex">ví dụ</span>` | `WARN` |
| `C7` | Cổng duyệt: bài agent tạo phải ở `status: "review"`, `approvedBy: ""` | `FAIL` |
| `C8` | Đủ 15 file luật & pipeline trong repo (gồm cả `scripts/wms-media-pipeline.py`); khối `SCENECSS` & `SCENEJS` nguyên vẹn và đồng bộ | `FAIL` |
| `C9` | **v2 (2026-11-08, Hướng 3A + QĐ 56).** Bài khảo cứu 2 tầng (`article.lay`: ≥ 3 lầm tưởng · ≥ 4 chương `sections` ≥ 850 từ · `flowSummary` ≥ 4 bước kênh wire/pipe/book · 5 vai · `whenHelps`/`whenTraps` ≥ 3 · ≥ 4 câu hỏi — `article.pro`: ≥ 4 cơ chế ≥ 450 từ · ≥ 4 ghi chú ≥ 180 từ · ≥ 3 bút toán TT 99/2025 · ≥ 3 ngoại lệ × 50 từ) + Studio Video & Nhúng YouTube (`videoScript.long` ≥ 10 cảnh, lời bình ≥ 1.350 từ, kết 7:30–11:00 · `videoScript.short` ≥ 5 cảnh, lời bình 150–260 từ, kết 0:55–1:35; cả hai bắt buộc có `youtubeId`, `embedStatus`, `elevenlabsVoiceId`; bài chưa `published` cấm đặt `embedStatus: "uploaded_public"`) + grep điều luật / URL / tên ngân hàng / câu khuyên | `FAIL` / `WARN` |

## 2. Năm quy tắc cứng (WMS-R1..R5)

1. **WMS-R1 (Taxonomy):** Không gõ cứng số đếm danh mục/chủ đề lên UI; suy từ `CATEGORIES` và `STORIES`.
2. **WMS-R2 (Diorama v3.0):** Mọi bài có 5 nhà mặt cắt (`const TYPES`). Lời hứa/lệnh đi trên dây điện; tiền thật đi trong ống ngầm dưới đất.
3. **WMS-R3 (Kế toán TT 99/2025):** Mọi `ledger` cân bằng Nợ/Có và chạy qua `.claude/agents/ke-toan-reviewer.md`.
4. **WMS-R4 (Cấm tự đăng Web & YouTube + Nhúng Video YouTube vào bài viết — QĐ 56):** Agent chỉ ghi `status: "review"`, `approvedBy: ""`. Video build từ ElevenLabs + Diorama v3.0 qua `scripts/wms-media-pipeline.py` khi upload lên YouTube chỉ được đặt `privacyStatus: "unlisted"` (hoặc `"private"`), sau đó **nhúng ngược `youtubeId` 11 ký tự + `embedStatus: "uploaded_unlisted"` (hoặc `"pending_upload"`) vào `videoScript.long` và `videoScript.short`** để trình phát `youtube-nocookie.com/embed/` hiển thị ngay trong bài viết. Chỉ Duy chuyển sang `published` / `uploaded_public`.
5. **WMS-R5 (Kiểm cuối lượt):** Luôn chạy `python3 -I scripts/wms-media-pipeline.py --story <khoá> --mode dry-run`, `python3 -I scripts/check-story.py` và `scripts/wms-check.sh` trước khi báo cáo.
