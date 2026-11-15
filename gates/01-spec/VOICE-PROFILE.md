# Hồ sơ Giọng Văn Đặc Trưng — Where Money Sleeps (`VOICE-PROFILE.md`)

> **Stage:** `01-spec` (bổ sung cho `gates/01-spec/WRITER.md` §0 và `QĐ 53–65`, ngày `2026-11-15`)
> **Skill thi hành:** `anti-ai-writing` (`A1–A5`) · **Khoá máy:** `C10` trong `scripts/check-story.py`
> **Lưu ý (`Rule 6`):** Đây là **vân tay giọng văn biên tập v1** tổng hợp từ cặp giọng tự nhiên sẵn có của dự án (*bài `card` bản gốc* + `ONE-PAGER.md` + `WRITER.md`) và phản hồi đọc thật của Duy/người thân (2026-11-15). Khi Duy tự tay gạch sửa 5–8 đoạn, cập nhật bằng một dòng có ngày bên dưới để khoá dấu ấn cá nhân sâu hơn.

---

```text
VOICE PROFILE
=============
Persona: Người quen rành chuyện tiền nong ngồi kể rành mạch bên bàn cà phê tối
Reader: Người bình thường (như người yêu của Duy) lướt điện thoại lúc 10h tối — thông minh, không thích bị giảng bài, ghét chữ sách giáo khoa và văn dịch
Goal: Đọc ba câu thấy ngay cảnh thật trong đời, thấy con số đối xứng cạnh nhau rồi tự bật ra tiếng "À, hoá ra tiền đi kiểu vậy."

1. Rhythm (Nhịp điệu)
- Trung bình bài đọc (article.lay): 15–24 từ/câu (VI) · 14–21 từ/câu (EN).
- Tuyệt đối phải có câu ngắn đóng đinh 3–8 từ xen giữa câu giải thích 20–30 từ (Burstiness CV >= 0.42).
- Mục đích của câu ngắn: cắt ngay sau một phát hiện để ý kịp lắng ("Với bạn, chuyện đã xong." / "Quán giữ đủ 50 nghìn.").
- Kịch bản đọc (vo): giữ wave cadence mượt cho Giọng Tâm eleven_v3 — câu 14–22 âm tiết xen câu chốt 6–10 âm tiết.

2. Compression & Syntax (Độ nén & Cú pháp)
- Tiếng Việt đi thẳng Đề–Thuyết chủ động: "Quán trả 220 nghìn cho ngân hàng." Thay vì "Việc chi trả khoản phí này được thực hiện bởi đơn vị bán hàng."
- Tiếng Anh viết SVO sáng sủa như Planet Money / Bloomberg Opinion loại dễ đọc: 1 ý chính 1 câu, không nhồi 3 vế rồi treo thêm đuôi ", V-ing".
- Giới hạn tối đa 1 dấu gạch ngang (—) trong một đoạn văn. Quá 1 dấu là tách thành hai câu.
- Dữ liệu minh hoạ phải hoà tự nhiên vào cảnh: "Ly cà phê 50 nghìn (ví dụ)" — KHÔNG viết "(số ví dụ xuyên suốt bài này)" hay chú thích lộ đề.

3. Claim Style (Cách đưa phát hiện)
- Show, đừng Notify: đặt hai con số thật cạnh nhau (lãi sổ 2 tỷ vs két còn 50 triệu) rồi để khoảng cách đó tự nói.
- Cấm mọi câu đứng ra thuyết minh hộ người đọc: "Khoảng vênh khổng lồ đến từ một sự thật nền tảng...", "Điều kỳ diệu nằm ở...", "Crucially,", "Furthermore,".

4. Preferred Moves (Nước đi ưu tiên)
- Mở bằng giờ giấc + món đồ + tiếng máy/tin nhắn quen thuộc.
- Đổi ngôi tự nhiên "bạn" (người đọc) và đặt thẳng tên vai đời thường ("quán", "ngân hàng của bạn", "công ty tài chính").
- Sau một đoạn kỹ thuật/sổ sách (TK 131, TK 1388), kéo ngay một câu chạm về ví dụ đời thường ở đầu bài.
- Ví dụ chuẩn trong repo (giọng gốc đáng giữ của `card`):
  VI: "Bữa liên hoan cả nhóm ở quán quen hết 10 triệu (ví dụ). Bạn chạm thẻ tín dụng, máy kêu tít một tiếng. Với bạn, chuyện đã xong."
  EN: "Dinner with friends at your regular spot comes to 10,000,000 VND (example). You tap your credit card. The terminal beeps once. As far as you're concerned, you're done."

5. Banned Moves (Nước đi bị cấm vĩnh viễn)
- Giọng giảng bài / tự khen phát hiện ("hãy nhìn vào", "hãy nhớ", "sự thật nền tảng", "bài khảo cứu này mở").
- Ẩn dụ văn mẫu báo cáo ("tấm vé bảo hiểm", "chiếc cầu bảo hiểm", "con dấu bảo chứng", "đại lộ thanh toán", "miếng bọt biển").
- Từ vựng xác suất LLM tiếng Anh (ethereal, staggering, juxtapose, bifurcate, agonizing, effortless gesture, utterly frictionless, unsustainable liquidity).
- Văn dịch bị động/danh hoá tiếng Việt ("việc X giúp Y", "sự thật là", "được thực hiện bởi").
- Câu hỏi mồi sáo cuối đoạn kiểu clickbait.
```

---

## Nhật ký cập nhật

| Ngày | Người cập nhật | Thay đổi |
|---|---|---|
| 2026-11-15 | Lead (theo phản hồi đọc thật của Duy) | Khởi tạo `VOICE-PROFILE.md` v1 làm neo chuẩn cho `anti-ai-writing` (`A1–A5`) và cổng `C10`. Chờ vòng `Diff-Distillation` từ 5–8 đoạn Duy tự tay gạch sửa (nếu cần tinh chỉnh thêm gu riêng). |
