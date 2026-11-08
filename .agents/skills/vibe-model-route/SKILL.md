---
name: vibe-model-route
description: >-
  Phân loại độ phức tạp của task (T0..T4) và chọn đúng model giữa Gemini (4 Argon, 3.8 Flash)
  và Claude (Fable 5, Opus 5.5, Sonnet 5.5, Haiku 4.5) để tối ưu chi phí và chất lượng theo Quy tắc 16.
  Kích hoạt ở đầu mỗi stage/task lớn hoặc khi Duy gõ /vibe-model-route.
---

# /vibe-model-route — Phân loại Task & Xoay vòng Model (Quy tắc 16)

**Hợp đồng gốc:** `docs/model-routing.md` (ở thư mục gốc `Vibe/docs/model-routing.md`).
**Công cụ tất định:** `python3 -I scripts/vibe-model-route.py` (hoặc `../scripts/vibe-model-route.py` khi đứng trong một repo app con).

## Các bước thực thi

1. **Chạy script phân loại tất định:**
   ```sh
   # Theo mẫu công việc (preset):
   python3 -I scripts/vibe-model-route.py --list-presets
   python3 -I scripts/vibe-model-route.py --preset <tên-preset>

   # Hoặc chấm điểm 4 trục (0..2 mỗi trục):
   python3 -I scripts/vibe-model-route.py --ambiguity <0..2> --risk <0..2> --taste <0..2> --scope <0..2> --stage <S0..S6>

   # Hoặc truyền mô tả công việc:
   python3 -I scripts/vibe-model-route.py --task "<mô tả công việc>" --stage <S0..S6>
   ```
2. **In nhãn `[Route: ...]` ra đầu phản hồi** trước khi chạy stage hoặc gọi subagent / `claude -p`.
3. **Thi hành đúng lệnh gọi model mà script trả ra:**
   - `T0 (S=0)`: Chạy thẳng script Python/Bash (`0 token`). CẤM gọi LLM.
   - `T1 (S=1..2)`: Dùng `Gemini 3.8 Flash` (`Model: "flash"`) hoặc `Claude Haiku 4.5` (`--model haiku --effort low`).
   - `T2 (S=3..4)`: Dùng `Claude Sonnet 5.5` (`--model sonnet --effort high`) hoặc `Gemini 4 Argon Medium`.
   - `T3 (S=5..6)`: Dùng `Claude Opus 5.5` (`--model opus --effort high`) ↔ `Gemini 4 Argon High` (`Model: "pro"`), kiểm chéo khác họ model.
   - `T4 (S=7..8)`: Dùng `Claude Fable 5` (`--model fable --effort high --fallback-model opus,sonnet`) **chỉ cho `0→1` Taste / Core UI Design hoặc sau khi `T3` fail 2 lần**, sau đó áp dụng **Khoá-rồi-Hạ (`Lock-then-Downgrade`)** về `T2 (Sonnet)`.
