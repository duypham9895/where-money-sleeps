---
status: fail
stage: 01-spec
date: 2026-10-24
owner: T3 — phiên tái lập (đội vai PM + Data + Legal)
blocked_on:
  - đo iPhone/Android thật (Zalo giữ #fragment không, mở WebView hay Safari, input type=file, persist())
  - Duy đọc hợp đồng lao động Ringkas (IP, không cạnh tranh)
  - agent ke-toan-reviewer chạy thử 1 bài mẫu + card, đo giờ Duy đọc báo cáo và ký (QĐ 36)
---

# T3-RECONSTRUCTION — S1 dựng lại từ nguồn S0

> **Phạm vi phiên này (quy tắc 12 T3):** KHÔNG đọc file nào trong `gates/01-spec/`. Chỉ đọc
> `ONE-PAGER.md`, `PRODUCT-BRIEF.md`, `LEGAL-SCREEN.md`, `ADDENDUM-PDF-LLM.md`, `SOURCE-ROADMAP.md`,
> `legal/licences.json`, `PIPELINE.md` + `docs/` của xưởng. Mục đích: để S1 so lệch. **Chỗ nào lệch
> với S1 ⇒ là tín hiệu spec mơ hồ, leo lên Duy, không bỏ phiếu.**
> `status: fail` = S1 chưa chốt được vì `blocked_on`; phần tái lập thì đã xong.

**TL;DR** · đọc khoảng 8 phút
- MVP mùa 1 = ~28–30 bài VN (lối vào 12–15 + GĐ01 + khái niệm GĐ02 + phần người vay GĐ05), card tĩnh sinh lúc build, trình đọc PDF (Hermanson tr.1–197 + file riêng thuần cục bộ), nút gạt VI ⇄ EN, tiến độ localStorage, bộ đếm gộp cùng domain. **Ra mắt khi 12–15 bài lối vào VN đã duyệt.**
- 22 tiêu chí chấp nhận; **7 cái BLOCKED** bởi ba điều kiện của Duy.
- Thước đo chính: tỉ lệ `lesson_completed` bài 5 / bài 1. **S0 không nói cách chống trùng** — phần chống trùng ở §3 là suy luận T3, đánh dấu rõ.
- **9 xung đột / chỗ mơ hồ cần Duy** (§6). Quan trọng nhất: ONE-PAGER vẫn ghi `draft — Duy chưa duyệt` và "14 quyết định" trong khi S0 đã approve với 15 (+ dòng 16).

Quy ước nguồn: **D<n>** = dòng "Quyết định của Duy" số n trong `PRODUCT-BRIEF.md` · **OP** = ONE-PAGER · **LS** = LEGAL-SCREEN §Kết luận · **AD** = ADDENDUM §Đường ống · **LJ** = `licences.json` · **data.md / lessons.md** = tài liệu xưởng.

---

## 1. Phạm vi MVP (mùa 1)

| Thành phần | Trong mùa 1 | Nguồn |
|---|---|---|
| Người đọc | Hai tầng trên một bộ nội dung: lối vào cho mọi người + lộ trình sâu tuỳ chọn | D1 |
| Nội dung | Lối vào 12–15 bài + GĐ01 + phần khái niệm GĐ02 (NAPAS/VietQR) + phần người vay GĐ05; **ước ~28–30 bài, chưa đo** | D5 |
| Ngưỡng ra mắt | Khi **lối vào (12–15 bài VN) đã duyệt xong**; GĐ01/02/05 lên dần bằng cờ `published` | D14 |
| Khuôn bài | HTML reflow, mobile-first, 5–8 phút; giao dịch thật VN → 1 khái niệm → ví dụ giải sẵn → ví dụ giải dần → 1 dòng tóm tắt | Brief §Kiến trúc (không bị quyết định nào thay) |
| Chú thích thuật ngữ | Mọi thuật ngữ chuyên ngành có chú thích, từ **một file glossary duy nhất**; **chạm mới hiện** | D5, D16 |
| Quiz card | Card tĩnh sinh lúc build trên máy Duy (3–5/bài theo AD), soát rồi ship JSON. Nguồn nạp: bài Duy tự viết + Hermanson | D2, D3, AD |
| Trình đọc PDF | PDF.js lazy-load; Hermanson **tr.1–197** (đã redact tr.113, tr.166) + file riêng của người học **thuần cục bộ, LLM không chạm**; vị trí đọc lưu localStorage | D4, D15, LJ |
| Song ngữ | VN gốc; EN Claude dịch lúc build, Duy duyệt mới hiện; nút gạt tại chỗ giữ `sectionId`; URL `/vi/` `/en/` + hreflang | D6 |
| Lưu tiến độ | JSON có `schema` trong localStorage + tự khai giai đoạn 2 chạm + link `#sync` qua Zalo + mời cài màn hình chính sau ~3 bài | D7 |
| Duyệt | Duy duyệt mọi bài + mọi card (cả EN); kế toán soát GĐ01 (TT 99/2025) + GĐ05 (APR) + mọi card có con số | D8 |
| Đo | Bộ đếm gộp tự host, cùng domain, `sendBeacon` → Cloudflare Worker; không ID/cookie/IP lưu | D9 |
| Thẻ sách | Sách khuyến nghị còn bản quyền = thẻ Duy tự viết ("đọc chương nào") + link mua | OP §3.1 |
| Tên + tagline | "Where Money Sleeps" + **tagline giải nghĩa bắt buộc** | OP §1, PIPELINE Log |
| Không tài khoản | Không tài khoản, không bình luận/diễn đàn | OP §1, LEGAL-SCREEN §Quy tắc vận hành |

**Đề xuất ở thân bài S0 nhưng KHÔNG có quyết định nào chốt** (S1 phải hỏi, không tự thêm):

| Mục | Ghi chú |
|---|---|
| Nút "Thêm vào lịch" `.ics` | Thân bài đề xuất; hiệu quả chưa đo; không quyết định nào nhắc |
| Máy tính khoản vay (người học tự nhập offer) | Thân bài + LEGAL-SCREEN dùng nó **thay** bảng lãi có tên ngân hàng; D5 kéo GĐ05 vào nhưng không nói có máy tính |
| Ôn theo phiên (1–2 card đầu phiên sau) | AD bước 9 — AD còn hiệu lực phần đường ống, nhưng bước 9 là hành vi sản phẩm, không phải định dạng card. S0 không phân định |
| EPUB / foliate-js | Thân bài có; D4 chỉ nêu PDF.js. **S0 không nói** EPUB có trong mùa 1 |

### Ngoài phạm vi mùa 1

| Mục | Vì sao / nguồn |
|---|---|
| LLM runtime (on-device, BYOK, proxy) | D2 — `N/A — because` mùa 1; xem lại khi Chrome AI có tiếng Việt trên điện thoại |
| Card từ sách trả phí | D3 — chờ workflow pháp lý + Duy ký (D12) |
| OpenStax hiện hành vào máy sinh card hoặc host | D3, LS — chỉ deep-link |
| "Ôn với AI của bạn" | Brief dòng 11 câu — mùa 2 |
| GĐ03 (code) · GĐ04 · GĐ06 · GĐ07 | D5 — hiện "sắp có", **không ghi ngày** |
| Hermanson ngoài tr.1–197 | D15 — thêm sau, mỗi lần soát ảnh phần đó |
| Kiếm tiền (affiliate, donate) | D10 |
| Tư vấn đầu tư, mã chứng khoán, bảng lãi có tên ngân hàng | OP §3.2 |
| Định danh, cookie, funnel theo người, % hoàn thành 26 tuần | D9, Brief §Không đo |
| Script bên thứ ba (GA4, Plausible, Cloudflare Web Analytics…) | D9, data.md §Bảng loại trừ |

---

## 2. Tiêu chí chấp nhận — 22 cái quan trọng nhất

| # | Tiêu chí (kiểm được) | Nguồn | Kiểm bằng | Trạng thái |
|---|---|---|---|---|
| A1 | Không trang nào publish khi cờ `published` = false; mọi bài/card/bản EN mặc định `false` cho tới khi có dòng duyệt của Duy | D8, OP §3.3 | script: grep cờ + đối chiếu sổ duyệt | sẵn sàng |
| A2 | Bài GĐ01, GĐ05 và mọi card có con số có thêm chữ ký kế toán trước khi `published` = true | D8 | script: card chứa chữ số ⇒ bắt buộc trường duyệt kế toán | **BLOCKED — chờ tên kế toán** |
| A3 | Mỗi thuật ngữ chuyên ngành trong bài có mục trong **một** file glossary; thiếu mục ⇒ build FAIL | D5 | script (cách nhận diện "thuật ngữ" — S0 không nói, xem X7) | sẵn sàng (sau X7) |
| A4 | Chú thích thuật ngữ chỉ hiện khi chạm | D16 | QA bằng mắt | dạng chạm cụ thể chờ `RESEARCH-GLOSSARY-UX.md` |
| A5 | Tên tài khoản kế toán theo TT 99/2025, viết dạng "Nợ (Debit)" | Brief §Kiến trúc, LS | kế toán soát | **BLOCKED — chờ tên kế toán** |
| A6 | Mọi card có `source_quote` + số trang; `source_quote` khớp chuỗi trong nguồn; mọi con số/`%`/`đ`/`$` trong đáp án có trong `source_quote`. Trượt ⇒ **loại, không sửa** | AD bước 5 | script tất định | sẵn sàng |
| A7 | Máy sinh card chỉ nạp bài Duy viết + Hermanson; loại mọi đoạn trong `exclusions` của LJ (FASB, New Accountant, GE/Gillette/Coca-Cola, WSJ, tr.501, tr.803) | D3, LJ, AD bổ sung | script: danh sách nguồn + chặn trang/đoạn loại trừ | sẵn sàng |
| A8 | Không dùng LLM chấm LLM | AD bước 6 | review pipeline | sẵn sàng |
| A9 | Card: chạm, không gõ; trắc nghiệm có phản hồi ngay hoặc lật thẻ tự chấm; không dùng con số tài chính làm phương án nhiễu nếu không có phản hồi; sau đáp án có 1 dòng giải thích + link "đọc lại đoạn này" tới `sectionId` | AD bước 8 | QA + script (link `sectionId` tồn tại) | chi tiết hiển thị là của S2 |
| A10 | Trang bài tải **0 KB** của PDF.js; PDF.js chỉ tải khi mở file | Brief §Kiến trúc, D4 | đo network trên trang bài | sẵn sàng |
| A11 | File riêng của người học không rời máy: 0 request mạng mang nội dung/tên file | D4, LS | đo network khi mở file | sẵn sàng |
| A12 | Mở file riêng hoạt động trong WebView Zalo (iOS + Android) | D4, AD §Chưa xác minh | thiết bị thật | **BLOCKED — chờ đo iPhone/Android** |
| A13 | File Hermanson host = tr.1–197, đã redact tr.113 + tr.166, mang đúng `attribution_text` của LJ; `licences.json` có trường `file` khi file vào repo | D15, LJ | vibe-check [4] + mắt | sẵn sàng (việc S3) |
| A14 | Nút gạt VI ⇄ EN đổi tại chỗ, giữ `sectionId`; không trang nào trộn ngôn ngữ; bài chưa có EN đã duyệt ⇒ nút mờ + dòng "Bài này chưa có bản tiếng Anh" | D6 | QA | sẵn sàng |
| A15 | `/vi/` `/en/` có hreflang hai chiều, không auto-redirect | D6, Brief | script | sẵn sàng |
| A16 | Tiến độ = một JSON có `schema` trong localStorage (bài đã đọc · trạng thái card · trang PDF · ngôn ngữ); không cookie; ID chuỗi ổn định; giữ ID mồ côi. **Tên key + schema là hợp đồng** | D7, Brief | script + QA | tên key: **S0 không nói** |
| A17 | Tự khai giai đoạn trong ≤ 2 chạm | D7 | QA đếm chạm | sẵn sàng |
| A18 | Link `#sync` khôi phục đủ tiến độ khi gửi qua Zalo rồi mở lại; nếu Zalo cắt `#` ⇒ dùng copy mã | D7 | thiết bị thật | **BLOCKED — chờ đo iPhone/Android** |
| A19 | Mời cài màn hình chính sau ~3 bài, manifest `display: standalone`; `persist()` gọi ngầm làm cảm biến; cảnh báo chỉ cho tab iOS `false` đã có tiến độ; nhắc sao lưu cả khi `true`; **không bao giờ** dùng chữ "lưu vĩnh viễn" | D7, Brief, lessons.md | thiết bị thật + grep chuỗi | **BLOCKED — chờ đo iPhone/Android** (hành vi iOS 26) |
| A20 | Không request nào tới origin bên thứ ba (font tự host, không script đo bên ngoài) | D9, Brief §Font | đo network | sẵn sàng |
| A21 | Footer có disclaimer + dòng "soạn với hỗ trợ AI, duyệt bởi <ai>, ngày"; bài pháp lý/lãi suất có thêm disclaimer với ngày "căn cứ văn bản hiệu lực đến" | LEGAL-SCREEN §Pháp lý VN, §Quy tắc vận hành | grep + mắt | sẵn sàng |
| A22 | Nội dung GĐ05 (người vay, vay mua nhà) không vi phạm hợp đồng lao động Ringkas | D13 | Duy đọc hợp đồng | **BLOCKED — chờ hợp đồng Ringkas** |

Thêm một điều kiện **trước khi `ACCEPTANCE` chốt**, không phải tiêu chí sản phẩm: S1 dựng tay 1 bài mẫu + card nháp để Duy và kế toán bấm giờ (Brief ghi chú N6, D14). **BLOCKED — chờ tên kế toán.**

---

## 3. Thước đo chính + chống trùng

| Mục | Nội dung | Nguồn |
|---|---|---|
| Metric | Tỉ lệ **số lần `lesson_completed` của bài 5 / bài 1** của lối vào, đếm gộp, không định danh | OP §4 |
| Bản chất | **Proxy**, không phải funnel theo người | OP §4 |
| Quyết định | Thấp ⇒ viết lại lối vào. Cao ⇒ đầu tư tầng sâu | Brief §Đo cái gì |
| Ngưỡng | **S0 không nói** — "ngưỡng do S1 đặt". Theo data.md: ngưỡng không nguồn phải ghi **"TÔI CHỌN"** | OP §4, data.md |
| Ba nguồn thổi phồng | (1) người tự khai giai đoạn · (2) người mất storage làm lại bài · (3) nút gạt VI ⇄ EN | OP §4 |
| Cách chống trùng | **S0 không nói** — OP giao cho S1 | OP §4 |
| "Hoàn thành" bài là gì | **S0 không nói** (cuộn tới cuối? trả lời card?) | — |

**Suy luận T3 — KHÔNG phải nội dung S0**, đưa ra để S1 so lệch:

| Nguồn thổi phồng | Hướng chống trùng tương thích ràng buộc S0 | Còn hở |
|---|---|---|
| Nút gạt VI ⇄ EN | Cờ "đã bắn" theo **lessonId**, không theo (lessonId, lang), lưu trong JSON tiến độ ⇒ đổi ngôn ngữ không bắn lại | — |
| Tự khai giai đoạn | Bài được đánh dấu do tự khai **không** bắn `lesson_completed` | Người tự khai bỏ qua bài 1 rồi làm bài 5 vẫn làm tử số tăng mà mẫu số không ⇒ tỉ lệ có thể > 1 |
| Mất storage | Không chống được khi không có ID. Khôi phục qua `#sync` mang cờ về ⇒ không bắn lại | Mất mà không sync ⇒ đếm hai lần, ở **cả** tử và mẫu |

Quy tắc trình bày từ data.md áp vào: số đo được là **SÀN** (người chặn quảng cáo đóng góp 0); Analytics Engine **lấy mẫu** ⇒ dùng `sum(_sample_interval)`, không dùng `count()`; **chỉ giữ 3 tháng**.

---

## 4. Event

Tên dự kiến từ D9 — **"S1 chốt tên, tên là hợp đồng"**. T3 không đổi tên nào.

| Event | Thuộc tính (theo D9) | Phục vụ quyết định | Chỗ S0 không nói |
|---|---|---|---|
| `lesson_completed` | `lesson`, `lang` | Metric chính; câu 5/14 | Định nghĩa "hoàn thành"; tập giá trị `lang`; có bắn khi tự khai không |
| `card_answered` | `card`, `correct` | Câu 8 (card sai) | `correct` nghĩa là gì với thẻ lật tự chấm "Nhớ/Chưa nhớ" (X5) |
| `pdf_opened` | `source: hosted \| own` | Câu 4 (có dùng PDF không) | — |
| `sync_link_created` | (không thuộc tính) | Câu 7 (sync) | Có tính khi rơi về copy mã không |
| `progress_restored` | (không thuộc tính) | Câu 7 | Phân biệt khôi phục từ `#sync` hay từ mã copy |

**Event không có trong D9:** tự khai giai đoạn, mời cài màn hình chính, kết quả `persist()`. Thân bài Brief từng muốn đo "lượt xem trang khôi phục / tự khai" — **không quyết định nào giữ hay bỏ**.

Ràng buộc vận chuyển (data.md + lessons.md):

| Ràng buộc | Nguồn |
|---|---|
| Trang và endpoint **cùng origin**; mỗi sản phẩm một subdomain Cloudflare riêng | data.md §Ba điều kiện |
| Path trung tính — **cấm** `/collect` `/event` `/track` `/beacon` `/metrics` `/api/event` | data.md |
| Bắn ở `visibilitychange`, không heartbeat, không `unload`/`beforeunload` | data.md |
| Không dùng KV cho bộ đếm | D9, lessons.md |
| Giá / hạn mức Analytics Engine hay D1: **chưa kiểm** | D9 |

---

## 5. Ràng buộc pháp lý có quyền CHẶN

| # | Ràng buộc | Chặn cái gì | Nguồn | Trạng thái |
|---|---|---|---|---|
| L1 | Không host PDF/scan/ảnh bìa/trích dài/card từ sách trả phí | mọi asset sách | OP §3.1, LS | đã chốt |
| L2 | Lõi không có nguồn NC; BIS, OpenStax, IMF chỉ là link | host + máy sinh card | D10, LS | đã chốt |
| L3 | Không đưa OpenStax hiện hành vào LLM; không dùng tên/logo/bìa OpenStax làm UI | máy sinh card, UI | LS | đã chốt |
| L4 | Hermanson: CC BY **3.0**; host chỉ tr.1–197; redact tr.113 + tr.166; ghi công đúng `attribution_text`; loại `exclusions` khỏi máy sinh card | file host, card | D15, LJ | đã chốt; redact là việc S3 |
| L5 | Không mã chứng khoán, không khuyến nghị mua/bán/nắm giữ | mọi bài | OP §3.2, Luật CK 2019 | đã chốt |
| L6 | Không bảng lãi có tên ngân hàng chép từ báo | GĐ05 | LS, NĐ 147 | đã chốt |
| L7 | Văn bản QPPL: ưu tiên link vbpl.vn/sbv.gov.vn, chỉ trích chọn lọc — tránh thành "thông tin tổng hợp" | GĐ02/GĐ05 | LS, NĐ 147 Đ.24 | vùng xám, Duy đã chấp nhận (D11) |
| L8 | Không định danh, không cookie, không lưu IP; trang riêng tư phải nói nhà hạ tầng có ghi IP | bộ đếm, trang riêng tư | D9, data.md | vùng xám nhẹ (Luật 91/2025) |
| L9 | Dòng minh bạch AI + disclaimer có ngày | footer, bài pháp lý/lãi | LS | vùng xám (Luật AI 134) |
| L10 | Có cờ `published` để gỡ trước, tranh luận sau | ra mắt | LS | đã chốt |
| L11 | Hợp đồng lao động Ringkas (IP, không cạnh tranh) vs phần vay mua nhà | **toàn bộ S1** | D13 | **BLOCKED — chờ hợp đồng Ringkas** |
| L12 | Mọi kết luận pháp lý từ workflow ghi "không phải ý kiến pháp lý · same vendor, same priors — no external verifier ran"; Duy ký chấp nhận từng tính năng mùa 2 đụng sách người khác | mọi tính năng mùa 2 | D12 | đã chốt |
| L13 | Font/thư viện vào `licences.json` trước khi dùng (OFL, Apache-2.0) | S3 | CLAUDE.md quy tắc 4, Brief | font & PDF.js chưa có dòng trong LJ |

---

## 6. Xung đột và chỗ mơ hồ — cho Duy, T3 không tự quyết

| # | Chỗ | Vì sao là vấn đề |
|---|---|---|
| X1 | `ONE-PAGER.md` frontmatter còn `status: draft — Duy chưa duyệt` và dòng nguồn "14/14", trong khi PIPELINE ghi APPROVE S0 với 15/15 | Quy tắc 11: S1 phải trích nguyên văn từ một ONE-PAGER mà chính nó tự khai là chưa duyệt. ONE-PAGER cũng chưa nhắc D15 (chỉ host chương 1–4) và D16 |
| X2 | Brief có **dòng 16** (chú thích chạm mới hiện), task và PIPELINE nói "15 quyết định" | Không rõ D16 có thuộc gói S0 đã approve không. Nửa còn lại của D16 chờ `RESEARCH-GLOSSARY-UX.md` |
| X3 | D9 "cùng domain" ⇒ site **phải** được phục vụ từ Cloudflare (data.md: GitHub Pages không đếm được, tĩnh thuần không đếm được) | Thân bài Brief để khung site "chốt ở S3"; thực tế D9 đã chốt hạ tầng ở S1. Domain `wherethemoneysleeps.com` **chưa mua** ⇒ nếu dùng `*.workers.dev` phải là subdomain riêng |
| X4 | D9 ghi `sendBeacon`; data.md đề xuất `fetch(..., {keepalive:true})` ở `visibilitychange` | Không loại trừ nhau, nhưng S1 phải chọn một; data.md cấm path `/beacon` |
| X5 | `card_answered {correct}` vs thẻ lật tự chấm "Nhớ/Chưa nhớ" (AD bước 8) | "correct" của thẻ tự chấm là tự báo, không cùng nghĩa với trắc nghiệm ⇒ trộn hai loại làm hỏng câu hỏi 8 (card sai) |
| X6 | Card từ Hermanson (tiếng Anh, US GAAP) vs bài VN theo TT 99 | AD bước 5 đòi `source_quote` khớp chuỗi nguồn ⇒ card VN có trích EN? S0 không nói ngôn ngữ card Hermanson, cũng không nói người học đọc Hermanson bản EN hay có bản dịch |
| X7 | D5 "thuật ngữ xuất hiện mà không có glossary thì FAIL" | Máy không biết từ nào là thuật ngữ nếu không có markup. S0 không nói cách đánh dấu |
| X8 | `.ics`, máy tính khoản vay, EPUB, ôn đầu phiên: có ở thân bài, không ở quyết định | Đưa vào thì là thêm phạm vi không ai duyệt; bỏ ra thì GĐ05 thiếu thứ thay bảng lãi (L6) |
| X9 | D8 "Duy duyệt mọi card cả EN" × ~170–300 lượt duyệt **chưa đo phút** | Ngày ra mắt (D14) phụ thuộc con số này; đây chính là điều kiện bấm giờ đang BLOCKED |

---

## Chưa xác minh được

- Toàn bộ hành vi Zalo WebView (`#fragment`, `input type=file`, localStorage), iOS 26 tách storage, `persist()` trên iPhone — chỉ có bằng chứng macOS và 2018–2022.
- Số bài thật của mùa 1 (~28–30 là ước), số card (84–150 VN), phút duyệt mỗi bài.
- Tỉ lệ sai của card LLM trên văn bản tài chính tiếng Việt (6–22% là y khoa, tiếng Anh).
- Giá/hạn mức Workers Analytics Engine, D1; chính sách tính phí "in the coming months".
- EasyPrivacy có chặn `sendBeacon` tới path trung tính cùng origin không — T3 không kiểm.
- Giấy phép Astro (S0 ghi chưa kiểm).
- Các phần đánh dấu "Suy luận T3" ở §3 không có nguồn S0.
- Phiên này là Claude tái lập từ tài liệu do Claude viết. **Same vendor, same priors — no external verifier ran.**
