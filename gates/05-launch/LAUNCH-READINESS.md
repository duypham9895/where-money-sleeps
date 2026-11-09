---
status: pass
stage: 05-launch
date: 2026-11-09
owner: ops
blocked_on: []
---

# LAUNCH-READINESS — Hồ Sơ Sẵn Sàng Ra Mắt & Đường Gỡ 72 Giờ (`S5 Launch` — `where-money-sleeps`)

> **Quy tắc cứng (`PIPELINE.md` & `../docs/stages.md`):** `S5 LAUNCH-READINESS` là cổng duy nhất **không bao giờ waive được**. Chính sách quyền riêng tư, sổ giấy phép và đường gỡ 72 giờ phải hoàn tất trước khi người đọc đầu tiên truy cập bản công khai.
> *Nhãn định tuyến & kiểm duyệt (Quy tắc 7 & 16):* `[Route: T2 · S=4/8 · Primary=Claude Sonnet 5.5 · CrossCheck=Gemini 4 Argon Medium]` · `same vendor, same priors — no external verifier ran`.

## 1. Bảng Kiểm Chứng Kỹ Thuật, Pháp Lý & Quyền Riêng Tư Tự Động (Đã Đạt 100%)

| # | Hạng mục cổng `S5 Launch` | Bằng chứng xác minh trên đĩa | Trạng thái |
|---|---|---|---|
| **1** | **5 cổng tất định `scripts/wms-check.sh`** (`C0–C9`, `F1–F4`, `M0–M4`, `wms-studio-sync.py`, `vibe-check.sh`) | `PASS 28/28` (`C0–C9`) · `PASS 14/14` (`F1–F4`) · `PASS 21/21` (`M0–M4` & `LUẬT 10`) · `hash=fe50a0cfdedbb726` · `0` lỗi chặn | **`PASS`** |
| **2** | **4 cụm E2E `scripts/wms-qa-verify.py`** (`QA-1..QA-4`) | 12 hình `16:9` (`1200×675`, `CLS = 0`), 6 thẻ `WMS_QUIZ_BANK` có `reviewed_by: "Duy"` + `accountant_agent: "ke-toan-reviewer"` (`AC-21`), `8/8` bất biến máy đo lường `tel` (`R1–R6`, `F4`, `from_start`, `/api/p` `AC-68`), CSP `connect-src 'none'` trên `studio.html` | **`PASS`** |
| **3** | **Sổ giấy phép `legal/licences.json` & An toàn thương hiệu (`B1–B4`)** | Ghi nhận đầy đủ 3 họ font OFL (`Fraunces`, `Be Vietnam Pro`, `JetBrains Mono`), `bangtutorial/bang-motion` (`MIT`), giọng đọc `eleven_v3:JwqRvOqFdGeQNu7UjKjw` & SFX gói trả phí có Commercial License; `0` tên thương hiệu/ngân hàng/mạng thẻ/công cụ hậu trường có thật | **`PASS`** |
| **4** | **Khoá trạng thái nháp & Video `unlisted` (`AC-01`, `QĐ 56`)** | Cả 6 video Calm Editorial Motion `v6.5` trên kênh `@WhereMoneySleeps` (`fxpFvVJcpRA`, `th6zR4gwV5c`, `3NqEha4j53k`, `XnMsbH0E_xo`, `l_8aVo538jo`, `J3DmDP4KKRI`) đang khoá ở `privacyStatus: "unlisted"` chờ lệnh duyệt công khai của Duy | **`PASS`** |
| **5** | **Tuyên bố miễn trừ, Quyền riêng tư & Minh bạch AI (`AC-37`, `AC-40`, `AC-86`)** | Mỗi bài và chân trang đều hiển thị rõ: *"Đây không phải lời khuyên tài chính hay đầu tư"*, *"Tiến độ lưu 100% trên thiết bị của bạn"*, *"Soạn với hỗ trợ AI · Soát: agent ke-toan-reviewer · Ký: Duy"* | **`PASS`** |

## 2. Quy Trình Đường Gỡ Khẩn Cấp 72 Giờ (`Takedown & Redaction Runbook` — `AC-61`, `R33`, `R37`)

Khi nhận được bất kỳ khiếu nại nào về bản quyền, thuật ngữ kế toán/pháp quy, hoặc quyền riêng tư qua kênh liên hệ chính thức:

| Mốc thời gian | Bước xử lý bắt buộc | Lệnh / Thao tác kỹ thuật tất định |
|---|---|---|
| **Bước 1 (`≤ 24 giờ` từ khi nhận tin)** | **Tiếp nhận & Cô lập tạm thời (`Quarantine`):** Chuyển ngay bài viết hoặc thẻ trắc nghiệm bị khiếu nại về trạng thái ẩn (`status: "draft"`) và chuyển video YouTube tương ứng từ `public`/`unlisted` về `private`. | 1. Trong `docs/prototype.html`: đổi `status: "published"` của bài liên quan thành `status: "draft"`.<br>2. Chạy `python3 -I scripts/wms-studio-sync.py && ./scripts/wms-check.sh --quiet`.<br>3. Trên YouTube Studio (`@WhereMoneySleeps`): đổi `Visibility` của video ID tương ứng sang `Private`. |
| **Bước 2 (`24h – 48h`)** | **Kiểm tra độc lập 4 Chuyên gia (`K/F/B/M`):** Chạy lại `ke-toan-reviewer` (`K1–K4`), `tai-chinh-reviewer` (`F1–F4`) và `brand-safety-reviewer` (`B1–B4`) trên đoạn văn/hình ảnh/video bị phản ánh. | Chạy `python3 -I scripts/check-story.py` + `python3 -I scripts/wms-finance-kb.py --verify`. Nếu phát hiện lỗi thật: cắt bỏ/sửa đoạn vi phạm và render lại video qua `scripts/wms-render-{short,long}-v43.py`. |
| **Bước 3 (`≤ 72 giờ`)** | **Đóng hồ sơ & Ghi vết bất biến (`Audit Log`):** Cập nhật `legal/licences.json` và bảng Log của `PIPELINE.md` (ghi rõ ngày nhận, nội dung đã gỡ/sửa, commit SHA) và phản hồi người gửi. | Commit & push bản sửa lên nhánh chính; chỉ mở lại `status: "published"` sau khi Duy ký duyệt lại. |

## 3. Cổng Xác Nhận Của Duy Trước Khi Bấm Mở Công Khai (`Human & Live-Infra Gate Checklist`)

Theo Quy tắc 5 & Quy tắc 6 (*"Việc cần Duy thì nói thẳng là cần Duy"*), **4 hạng mục dưới đây không agent nào tự ký thay được** và được giữ làm danh sách kiểm cuối cùng trước khi Duy chuyển site/video từ `unlisted` sang `public`:

| # | Việc cần Duy trực tiếp kiểm / ký | Vì sao agent không làm thay được | Trạng thái hiện tại |
|---|---|---|---|
| **H1** | **Đọc hợp đồng lao động Ringkas (`R34`, `QĐ 13`)** trước khi công khai địa chỉ hộp thư khiếu nại hoặc tên cá nhân trên trang liên hệ (`AC-61a`, `AC-53`). | Tài liệu pháp lý cá nhân của Duy ngoài workspace; quyết định đứng tên hay dùng hộp thư ẩn danh thuộc quyền sở hữu rủi ro của Duy. | **Chờ Duy xác nhận trước khi mở `public`** |
| **H2** | **Chạm thử tạo & mở link `#sync` trong WebView Zalo trên iPhone & Android thật (`AC-31`, `AC-32`)**. | Cần thiết bị vật lý và ứng dụng Zalo thật để xác nhận Zalo không cắt `#fragment`; nếu Zalo cắt `#`, chỉ dùng nút *"Tạo mã sao lưu"* (`method: "code"` đã dựng sẵn trong `docs/prototype.html`). | **Đã sẵn sàng cả 2 chế độ (`link` + `code`) trên UI; chờ Duy chạm thử trên máy thật** |
| **H3** | **Đấu nối Cloudflare Worker `/api/p` + bảng D1 và tắt `Workers Logs` (`AC-35`, `AC-55`, `AC-69`)** khi trỏ tên miền thật. | Cần tài khoản Cloudflare của Duy để xác nhận `observability.enabled = false` và ẩn ô `n < 5`. | **Client đã gửi chuẩn `/api/p`; chờ nối Worker khi lên tên miền** |
| **H4** | **Duy ký chuyển 3 bài mẫu (`card`, `pay`, `install`) và 6 video `v6.5` trên `@WhereMoneySleeps` từ `unlisted` sang `public` (`AC-01`, `AC-02`, `QĐ 56`)**. | Quy tắc 5: chỉ Duy mới có quyền duyệt xuất bản công khai. | **Đang khoá an toàn ở `unlisted` / `demo-prototype`** |

## 4. Kiểm Chéo `T2` (Phòng PM & Phòng Data hỏi — Phòng Ops + Legal trả lời)

1. **Câu hỏi 1 (Phòng PM):** *"Nếu sau khi ra mắt, người đọc trên iPhone mở link chia sẻ từ Zalo mà WebView Zalo cắt mất phần `#sync=...` trên URL, sản phẩm có bị hỏng luồng sao lưu tiến độ không?"*
   - **Trả lời (Phòng Ops):** Không bị hỏng. Trong `docs/prototype.html` (`#lessonQuizWrap`), chúng tôi đã dựng song song cả 2 nút: **`Tạo mã sao lưu`** (`method: "code"` — chép chuỗi Base64 thuần không phụ thuộc URL) và **`Sao chép link #sync`** (`method: "link"`), cùng nút **`Khôi phục từ mã`** nhận cả chuỗi mã lẫn URL. Nếu phép đo thực địa `H2` cho thấy Zalo cắt `#`, người học vẫn khôi phục 100% tiến độ và khoá `tel` qua mã sao lưu.
2. **Câu hỏi 2 (Phòng Data):** *"Khi chuyển một bài hoặc video từ `published` về `draft`/`private` theo quy trình đường gỡ 72 giờ ở Mục 2, lịch sử sự kiện `lesson_completed` và `card_answered` của các bài khác có bị ảnh hưởng không?"*
   - **Trả lời (Phòng Ops & Legal):** Hoàn toàn không. Khoá chống trùng `tel` trong `wms.progress.v1` và bảng đếm gộp theo ngày gắn với `lessonId` và `cardId.v<n>` độc lập của từng bài (`TRACKING-PLAN.md` §1); việc tạm ẩn một bài chỉ ẩn giao diện của bài đó mà không xoá hay làm lệch dữ liệu của các bài còn lại.

## 5. Chưa xác minh được

- Kết quả 4 hạng mục `H1–H4` của Duy ở Mục 3 khi chuyển từ chế độ chạy thử nghiệm (`unlisted` / `demo-prototype`) sang tên miền công khai.
- Same vendor, same priors — no external verifier ran.
