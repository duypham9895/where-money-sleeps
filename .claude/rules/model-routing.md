# Quy tắc 16 — Định tuyến & Xoay vòng Model theo Độ phức tạp (Model Rotation Rule)

File này nằm trong `.claude/rules/` để mọi phiên Claude Code chạy trong `Vibe/` tự nạp.
Hợp đồng gốc: `docs/model-routing.md`. Script chấm điểm tất định: `python3 -I scripts/vibe-model-route.py`.

## 1. Bảng phân lớp Đầu Task (`T0 → T4`) theo tổng điểm `S = Ambiguity + Risk + Taste + Scope` (`0..8`)

| Bậc | Điểm `S` | Loại việc | Model Chính (`Primary`) | Kiểm chéo (`Cross-Check`) | Cờ CLI (`claude` / `agy`) |
|---|---|---|---|---|---|
| **`T0`** | `0` | Việc tất định (`DEDUPE`, đếm từ, cân `Σ Nợ = Σ Có`, kiểm đường dẫn) | **Python / Bash Script** | — | Chạy thẳng script (`0 token`) |
| **`T1`** | `1–2` | Quét `SWEEP` đa mũi, đọc DOM/log trình duyệt, sửa cơ học/lint/đồng bộ file | **Gemini 3.8 Flash** · **Claude Haiku 4.5** | Script `T0` | `--model haiku --effort low` / `Model: "flash"` |
| **`T2`** | `3–4` | **Ngựa thồ chủ lực (~70% việc):** Code S3 theo spec, viết test, lên bài mới theo khuôn `C9` đã khoá, tóm tắt HTML ≤520 từ | **Claude Sonnet 5.5** · **Gemini 4 Argon Medium** | Họ model ngược lại (`Argon` ↔ `Sonnet`) | `--model sonnet --effort high --fallback-model opus` |
| **`T3`** | `5–6` | Viết `PRD.md` S1, phản biện `REFUTE`, `ke-toan-reviewer` TT 99/2025, Pháp lý, đúc bài sâu mẫu đầu, T3 Tái lập S1/S2 | **Claude Opus 5.5** **↔ Gemini 4 Argon High** | Bắt buộc **khác họ model** (`Opus` ↔ `Argon High`) | `--model opus --effort high --fallback-model sonnet` |
| **`T4`** | `7–8` | **Đỉnh cao `0→1` Taste & Gỡ bế tắc:** Sáng tạo ngôn ngữ thiết kế `0→1` chống mùi AI (S2 Core UI / Diorama), hoặc khi `T3` fail 2 lần | **Claude Fable 5** | **Gemini 4 Argon High** + `chrome-devtools-mcp` | `--model fable --effort high --fallback-model opus,sonnet` |

## 2. Ba kỷ luật bắt buộc

1. **In nhãn `[Route: T0..T4 · S=../8 · Primary=.. · CrossCheck=..]`** ở đầu mỗi stage hoặc trước khi gọi subagent / `claude -p`.
2. **CẤM dùng `Fable` mặc định:** `Fable` tốn **10x** và dễ over-engineer việc đã có khuôn. Chỉ bật ở `T4` (`S ≥ 7`).
3. **Khoá-rồi-Hạ (`Lock-then-Downgrade`):** Một khi `Fable` (`T4`) hoặc `Opus` (`T3`) đã đúc xong khuôn mẫu + script kiểm, mọi tác vụ lặp lại tiếp theo **bắt buộc hạ về `T2 (Sonnet)` + `T0 (Script)`**.
