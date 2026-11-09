---
description: Biến một câu ý tưởng thành một bài mới cho Where Money Sleeps theo pipeline 6 bước của QĐ 53 + QĐ 56 (viết bài -> ke-toan-reviewer K1-K4 + tai-chinh-reviewer F1-F4 + brand-safety-reviewer B1-B4 -> build Audio/Video từ ElevenLabs + Locked-Stage v4.0 -> upload YouTube unlisted -> nhúng youtubeId vào bài viết -> status "review", không tự đăng).
argument-hint: <ý tưởng bài viết>
---

Đọc và thi hành đúng theo `.claude/skills/vibe-post/SKILL.md` và hợp đồng gốc `gates/01-spec/AGENT-CMS-PIPELINE.md` cho ý tưởng: `$ARGUMENTS`.

Kết thúc bắt buộc chạy bộ 3 specialist (`ke-toan-reviewer` `K1–K4`, `tai-chinh-reviewer` `F1–F4`, `brand-safety-reviewer` `B1–B4`), `python3 -I scripts/wms-finance-kb.py --crawl --verify`, `python3 -I scripts/wms-media-pipeline.py --story <khoá> --mode dry-run`, `python3 -I scripts/check-story.py` và `scripts/wms-check.sh`, giữ bài ở `status: "review"`, `approvedBy: ""`, `embedStatus` không phải `"uploaded_public"`, và nói rõ: *"Tôi không tự đăng được — chỉ Duy chuyển sang `published` / `uploaded_public`."*
