---
status: fail
stage: 01-spec
date: 2026-10-24
owner: Data
blocked_on: [đo iPhone/Android (Zalo #sync, WebView, input file), agent ke-toan-reviewer chạy thử 1 bài mẫu + card và đo giờ Duy đọc báo cáo + ký (QĐ 36)]
---

# SUCCESS-CRITERIA — Where Money Sleeps, mùa 1

**TL;DR** · đọc khoảng 4 phút
- Thước đo chính (đã chốt ở ONE-PAGER §4): **M1 = số `lesson_completed` bài 5 ÷ bài 1 của lối vào**, đếm gộp, không định danh. Báo **hai số** (QĐ 39): **chặt** = bài 5 có `from_start = true` ÷ bài 1 · **lỏng** = mọi bài 5 ÷ bài 1. Là **proxy**, không phải funnel theo người. "Xong bài" = đã trả lời ≥ 1 card **trắc nghiệm** cuối bài; thẻ lật không tính (QĐ 24, 38) ⇒ M1 đo **"đọc + thử"**, thấp hơn "đọc tới cuối".
- **Không có ngưỡng nào ở file này là số có căn cứ.** Mỗi metric ghi **cách đặt ngưỡng** sau khi có dữ liệu, không bịa số.
- Chống trùng không cần ID: mỗi event bắn **tối đa một lần cho mỗi khoá trên mỗi bộ storage**. Chi tiết và phần **vẫn bị thổi** sau khi mất storage: `TRACKING-PLAN.md` §2.
- `status: fail` vì điều kiện trước S1 chưa xong. M5 có phần **BLOCKED** (chờ đo điện thoại). M3 **hết BLOCKED**: card có số được agent `ke-toan-reviewer` soát, Duy ký (QĐ 36).
- **Dashboard phải sống trước S5.** Không có dashboard đọc được M1–M5 bằng số thật thì S5 không duyệt (quy tắc 8: "xong" = đã nhìn thấy số).
- **"Không định danh" chỉ đúng khi không ai ghép được ô nhỏ với thứ mình biết sẵn.** Lưu lượng thấp thì ô n = 1 ghép được. Lưu theo ngày, ẩn ô n < 5, loại dữ liệu trước ra mắt; gộp tuần nếu L13 đòi (QĐ 32). Phần hở còn lại — Duy query được bảng thô — Duy đã nhận ở QĐ 32.
- **Lệch của M1 (sửa theo QĐ 39).** Số lỏng − số chặt = cỡ thổi do vào thẳng bài giữa lối vào từ link chia sẻ — giờ **đo được**, không còn chỉ là lập luận (`TRACKING-PLAN.md` §2.5). Số chặt còn lệch về phía **xẹp** (đọc lại từ bài 1 sau khi mất storage; bài 1 và bài 5 ở hai storage khác nhau), trừ hai trường hợp thổi ở §4 — **lập luận, chưa đo**.
- **M4 tính từ ngày ra mắt, mẫu số bài 1 lối vào** — trình đọc PDF là điều kiện ra mắt (QĐ 29).
- **Hai điểm → Duy của vòng trước đã chốt:** N1 = B, thẻ lật không tính (QĐ 38) ⇒ cờ chống bơm F4 chạy · `from_start` (QĐ 39). **Còn một điểm → Duy, không gấp:** ngưỡng M1 đặt trên số chặt hay số lỏng — quyết lúc đặt baseline (§2 bước 2). Data khuyến nghị số chặt.
- **Cảnh báo `persist()` là điều kiện ra mắt (QĐ 45)** nhưng **vẫn không có event**: `N/A — because` ở §3 giữ nguyên.

## 1. Metric — mỗi dòng phải đổi được một hành động

| # | Metric | Câu hỏi quyết định | Là X thì làm gì | Là Y thì làm gì | Ngưỡng |
|---|---|---|---|---|---|
| **M1** | `lesson_completed` bài 5 ÷ bài 1 (lối vào), báo hai số (QĐ 39): **chặt** = bài 5 `from_start=true` · **lỏng** = mọi bài 5 | Lối vào có đưa người tới bài 5 không ⇒ **đẩy tầng sâu lên** hay **viết lại lối vào**? | Dưới ngưỡng ⇒ **đưa Duy quyết** có viết lại lối vào theo M2 trước không. Data không tự dừng mở bài GĐ01/02/05: QĐ 14 ghi *"phạm vi câu 5 không bị cắt"* | Trên ngưỡng ⇒ giữ lối vào, dồn công vào bài GĐ01/02/05 kế tiếp | **TBD** — cách đặt ở §2; đặt trên số nào → Duy (§2 bước 2) |
| M2 | Đường rơi: `lesson_completed` bài *k* ÷ bài 1, với mọi *k* của lối vào | Nếu M1 thấp: **viết lại bài nào trước?** | Bước rơi lớn nhất giữa hai bài liền nhau ⇒ bài sau bước đó viết lại trước | Rơi đều, không có bước nổi bật ⇒ vấn đề là độ dài / giọng văn chung, không phải một bài | Không cần ngưỡng — xếp hạng tương đối |
| M3 | Tỉ lệ trả lời **sai lần đầu** theo từng card **trắc nghiệm** (`card_answered.correct = false` ÷ tổng, cùng `card`; thẻ lật không bắn, QĐ 25d). Mỗi bài `published` có ≥ 1 card trắc nghiệm ⇒ M3 thấy mọi bài (QĐ 38) | Card nào phải **quay lại duyệt** (có thể sai, mơ hồ — LLM sinh câu hỏi sai 6–22%, quyết định 8)? | Card lọt nhóm sai cao ⇒ Duy đọc lại; card có con số ⇒ chạy lại agent `ke-toan-reviewer` trên card đó (K1 tính lại bằng code; tên tài khoản ở K2 phán tối đa "KHỚP NGUỒN THỨ CẤP", QĐ 37), **Duy ký** (QĐ 36). Agent soát, không duyệt | Không card nào nổi bật ⇒ không làm gì | **TBD** — §2 |
| M4 | `pdf_opened{hosted}` ÷ bài 1 **lối vào** · `pdf_opened{own}` ÷ bài 1 lối vào | Trình đọc PDF (quyết định 4, ngược khuyến nghị hoãn) có được dùng không ⇒ có **soát + host thêm chương Hermanson** (quyết định 15) không? | ≈ 0 ⇒ không mở rộng phạm vi host, không đầu tư thêm cho trình đọc | Đáng kể ⇒ soát ảnh chương kế tiếp để host | **TBD** — §2 |
| M5 | `sync_created` ÷ bài 3 · `progress_restored` ÷ `sync_created` (`method` ∈ {`link`,`code`}, QĐ 25c) | Sao lưu có ai dùng không, và **khôi phục có chạy không** (quyết định 7)? | Tạo ≈ 0 ⇒ luồng sao lưu không ai thấy, S6 thiết kế lại chỗ mời | Tạo nhiều mà khôi phục ≈ 0 ⇒ nghi khôi phục hỏng ⇒ QA lại trên Zalo trước khi kết luận | **BLOCKED — chờ đo iPhone/Android** (link hay mã đổi nghĩa metric) |
| M6 | 5 người thật đọc bài 1 + mở PDF trên điện thoại, Duy quan sát | Bỏ giữa bài / không tìm ra PDF? | Bỏ giữa bài ⇒ sửa độ dài, giọng văn **trước** khi viết tiếp | Đọc hết ⇒ giữ khuôn bài | Không instrument — **việc của Duy** (quyết định 4) |

Bài 3 ở M5 vì quyết định 7 mời cài màn hình chính sau khoảng 3 bài — đó là lúc luồng sao lưu xuất hiện.

Mẫu số M4 là bài 1 **lối vào**, tính từ ngày ra mắt (sửa theo QĐ 29). Bản trước dùng bài 1 GĐ01 vì giả định PDF ra cùng GĐ01 (PRD #8) — giả định đó bị QĐ 29 bác: trình đọc PDF, trang sách và thẻ sách là **điều kiện ra mắt**, và trang sách (B6) đi được từ trang chủ (B1). Người có cơ hội mở PDF từ ngày đầu là người vào lối vào, nên mẫu số phải là họ. Giữ mẫu số GĐ01 thì ra mắt tới lúc GĐ01 bật sẽ có tử mà không có mẫu, và sau đó tử vẫn gồm người lối vào ⇒ M4 **thổi**, nghiêng sẵn về "mở rộng". Hệ quả nói thẳng: người mới ở lối vào có thể ít cần sách kế toán hơn người học GĐ01, nên M4 có thể thấp — đó là số thật của người được mời mở sách, không phải lệch đo.

**Đọc M1 thế nào** (sửa theo QĐ 39). Tự khai theo giai đoạn (QĐ 23) gỡ phần thổi **do tự khai**, nhưng không gỡ được phần thổi do người vào thẳng bài 5 từ link chia sẻ. `from_start` tách phần đó ra. Hai số dùng chung mẫu số bài 1:

| Số | Trả lời câu gì | Lệch đã biết (chưa đo cỡ) |
|---|---|---|
| **Chặt** — bài 5 `from_start=true` ÷ bài 1 | Lối vào có **đưa** người từ bài 1 tới bài 5 không. Data khuyến nghị đặt ngưỡng trên số này | **Xẹp:** đọc lại từ bài 1 sau khi mất storage; đọc bài 1 và bài 5 ở hai storage (Safari ⇄ app ⇄ WebView Zalo). **Thổi:** bị bơm; một bản sao lưu khôi phục sang máy thứ hai rồi cả hai máy cùng học tiếp (§4) |
| **Lỏng** — mọi bài 5 ÷ bài 1 | Như M1 trước QĐ 39. Có thể > 1 | Thêm phần thổi do vào thẳng bài giữa lối vào |
| **Lỏng − chặt** | Cỡ thổi do cửa vào giữa chừng (M7) — **đo được** | Gồm cả người đọc bài 1 ở storage khác, nên là **cận trên** của phần thổi do cửa vào |

Hai dấu hiệu vẫn dùng:

| Dấu hiệu | Nghĩa | Làm gì |
|---|---|---|
| Số **luỹ kế** có bước **ngược** (bài *k* > bài *k*−1) ở một bài không có cờ F | Có người vào thẳng bài *k*, hoặc bỏ qua bài *k*−1 | Xem số chặt cùng bài. Bước ngược chỉ có ở số lỏng ⇒ đó là cửa vào, đã nằm trong hiệu lỏng − chặt. Có cả ở số chặt ⇒ người đọc bỏ qua bài *k*−1. Ghi ngày + bài vào §2 |
| F2 bật mà F1 không bật | F2 tính trên **số chặt** (QĐ 39) ⇒ chia sẻ bài 5 cho người chưa đọc bài 1 **không còn** làm F2 bật. Còn lại: bơm nhắm số chặt, hoặc người đọc bỏ qua bài 4 | Duy xem F4 của bài 5 (`TRACKING-PLAN.md` §2.4) **trước khi** cách ly. Cách ly một ngày thật là mất số thật |

## 2. Cách đặt ngưỡng — không đặt trước

Không có benchmark công khai cho hạng sản phẩm này mà phương pháp đã tìm thấy (`../../../docs/data.md` §Chưa xác minh). Vì vậy:

| Bước | Quy tắc |
|---|---|
| 0. Dữ liệu nào được tính | Chỉ `day ≥ NGÀY_RA_MẮT`, trừ các ngày bị **cách ly** vì nghi bơm (QĐ 31, `TRACKING-PLAN.md` §2.4). S4 bắn tay và buổi M6 không vào metric (`TRACKING-PLAN.md` §5). Thêm 2026-10-24 (T2). |
| 1. Chưa đọc | Không kết luận gì từ M1, M2, M4, M5 khi mẫu số còn **dưới 100** (M1, M2, M4: bài 1 lối vào · M5: bài 3 hoặc `sync_created`). Dashboard không hiện tỉ lệ của các metric này khi mẫu số < 100. **M3 không theo bước này** mà theo dòng "M3 riêng" (≥ 30 lượt mỗi card). Lý do toán: tỉ lệ quanh 50% với n = 100 có khoảng tin cậy 95% xấp xỉ **±10 điểm** (1,96 × √(0,25/100)). Con số 100 là **lựa chọn của Data**, không phải chuẩn ngành; M1 cũng không phải tỉ lệ nhị thức thật (không theo người), nên khoảng này chỉ là ước lượng thô. |
| 2. Baseline | Khi đủ cả hai: **≥ 4 tuần sau ra mắt** và bài 1 ≥ 100 ⇒ giá trị đó là baseline. Duy đặt ngưỡng M1 và M4 dựa trên baseline + M6, ghi một dòng có ngày vào file này. **M1: Duy chọn đặt ngưỡng trên số chặt hay số lỏng — → Duy.** Data khuyến nghị số chặt, vì nó trả lời đúng câu "lối vào có đưa người tới bài 5 không"; số lỏng đọc kèm. Câu này không chặn S1: không có dữ liệu nào cần nó trước baseline (QĐ 39 chỉ chốt "báo cả hai số"). |
| 3. Đọc độ trễ | Bài 5 đến sau bài 1 vài ngày tới vài tuần ⇒ M1 tuần gần nhất luôn **thấp giả**. Dashboard hiện cả **luỹ kế** và **28 ngày trượt, bỏ 14 ngày cuối của mẫu số**. |
| 4. Sau mỗi lần sửa lối vào | So **trước/sau** trên cùng cách tính, không so với một con số tuyệt đối. |
| M3 riêng | Chỉ xét card có ≥ 30 lượt trả lời đầu; nhóm "sai cao" = 10% card có tỉ lệ sai cao nhất. Cả hai số là **lựa chọn của Data**, Duy sửa được. "Khó" không có nghĩa là "sai" — hành động là **đọc lại**, không phải xoá. Dashboard hiện tỉ lệ sai của một card khi card đó đủ 30 lượt; ngưỡng 100 ở bước 1 không áp dụng cho M3. M3 chỉ gồm card trắc nghiệm: thẻ lật tự chấm không bắn `card_answered` (QĐ 25d). |

## 3. Không đo — cố ý

| Không đo | Vì sao |
|---|---|
| Funnel theo từng người, retention, % hoàn thành cả lộ trình | Cần định danh — phá lời hứa của sản phẩm (quyết định 9) |
| Thời gian đọc, cuộn, heartbeat | Không đổi hành động nào ở trên; heartbeat báo thấp đúng lúc tab nền (`../../../docs/data.md`) |
| Tên/kích thước/số trang file PDF của người học | File của người học **thuần cục bộ** (quyết định 4) — không một byte nào về nó rời máy |
| Quốc gia, thiết bị, referrer | Không có trong quyết định 9. Muốn thêm ⇒ **Duy quyết**, thêm dòng có ngày |
| IP, kể cả để chặn spam ở edge Cloudflare | Rule do Duy bật là xử lý IP vì mục đích của Duy. **Không bật (QĐ 31).** Thay bằng cờ F1–F3 + cách ly ngày (`TRACKING-PLAN.md` §2.4). Cách ly ≥ 2 lần trong 4 tuần ⇒ Data đưa số lên Duy hỏi lại |
| Ô đếm n < 5 trên dashboard | Ghép với thứ Duy biết sẵn (bạn bè kể đã đọc) thì ô nhỏ chỉ ra được người. Ẩn thành `<5`, lưu theo ngày (QĐ 32). Bảng thô vẫn query được — Duy nhận. Gộp tuần + xoá dòng ngày khi L13 kết luận số gộp ghép ra được người. Thêm 2026-10-24 |
| Thẻ lật tự chấm | `N/A — because` "chưa nhớ" là tự báo, không phải tín hiệu card sai; trộn vào M3 thì Duy đọc lại nhầm card (QĐ 25d). Thẻ lật cũng không làm bài "xong" (QĐ 38). **Đo khi:** có câu hỏi quyết định về thẻ lật nào khó — thêm event mới, mất số giai đoạn trước |
| Tự khai giai đoạn · mời cài màn hình chính · `persist()` | `N/A — because` không metric nào ở §1 đổi hành động theo các số này; M5 đã trả lời câu "có phải thiết kế lại chỗ mời sao lưu" (QĐ 25e). Cái mất: không biết bao nhiêu người mất storage rồi tự khai — `progress_restored` chỉ là cận dưới. **QĐ 45 (2026-10-25)** đưa cảnh báo `persist()` vào cổng ra mắt; câu trả lời đo **không đổi**: cảnh báo là cờ bật/tắt, kiểm ở S4 bằng máy thật (AC-83), và không metric nào đổi hành động theo số người thấy cảnh báo hay số lần `persist()` được cấp. **Đo khi:** một câu hỏi quyết định cần nó; thêm event là tự do nhưng không hồi tố |
| Event lúc mất mạng | `N/A — because` không hàng đợi (QĐ 26); mất mạng ⇒ event mất, không bắn lại (`TRACKING-PLAN.md` §2.1 R1, R6) |

## 4. Chưa xác minh được

- M1: phần thổi do cửa vào giữa chừng **đo được** từ ngày ra mắt (lỏng − chặt, QĐ 39), nhưng **chưa có số**. Số chặt lệch bao nhiêu: **chưa đo**. Lực xẹp (mất storage rồi đọc lại từ bài 1; bài 1 và bài 5 ở hai storage) là lập luận. Hai lực thổi số chặt cũng là lập luận: (a) bơm POST mang `from_start=true`; (b) bản sao lưu khôi phục sang máy thứ hai khi đã qua bài 1, rồi cả hai máy học tiếp bài 5 ⇒ bài 5 đếm hai lần, bài 1 một lần.
- QĐ 38 (thẻ lật không tính) làm hành động của M3 có hệ quả lên M2: gỡ card trắc nghiệm **cuối cùng** của một bài ⇒ bài phải gỡ theo (AC-75) ⇒ M2 có bước rơi thật mà không phải lỗi của bài. Cỡ phụ thuộc mỗi bài có bao nhiêu card trắc nghiệm: **chưa biết**.
- "Không định danh" ở file này chỉ nói về **bộ đếm**. Hộp thư khiếu nại (QĐ 35) thu họ tên và email của người khiếu nại. Phần đó thuộc Legal §4(a) và Q-20, không thuộc metric nào ở đây.
- Agent `ke-toan-reviewer` có bắt được lỗi ở card mà M3 chỉ ra không: **chưa chạy thử**. Đó là điều kiện 3 của QĐ 36. Card GĐ01 có tên tài khoản chỉ đăng khi đã có Phụ lục II chính thức (QĐ 37), nên M3 của nhóm này bắt đầu muộn hơn ngày ra mắt.
- M3 hiện tỉ lệ cho card từ 30 lượt, nên tỉ lệ nhân số lượt sẽ ra được số lần sai, kể cả khi số đó < 5. Data chấp nhận vì dashboard không có bảng ngày × card. Đây vẫn là một phần của chỗ hở ở T2 câu 2, Duy đã nhận ở QĐ 32.
- M4: tử số gồm cả người mở PDF mà chưa xong bài 1 lối vào ⇒ tử và mẫu không cùng một nhóm người; M4 là proxy, có thể > 1 trên lý thuyết. **Chưa đo** lệch bao nhiêu.
- Event mất khi mất mạng (QĐ 26): tỉ lệ mất và có đều giữa bài 1 và bài 5 không — **chưa đo**.
- Tỉ lệ người dùng chặn beacon (adblock, Brave…) — thiếu đều cả tử và mẫu thì M1 không lệch, nhưng **chưa kiểm** nó có đều không.
- Ngưỡng 100 lượt, 4 tuần, 30 lượt/card, top 10%: lựa chọn của Data, không có nguồn.
- M5 phụ thuộc kết quả đo Zalo (`#fragment` sống hay chết) — **BLOCKED**.
- Cờ F1–F4 có bắt được một lần bơm thật không: **chưa thử**. S4 có thể bắn một loạt POST giả trên bản preview để xem cờ bật — **TBD, SWE/QA chốt**.
- Luật 91/2025 có coi dữ liệu gộp mà người vận hành ghép được với thông tin khác là dữ liệu cá nhân không: **chưa đối chiếu văn bản gốc** ⇒ Legal L13.
- Toàn bộ file là xác minh phía tác giả. **Same vendor, same priors — no external verifier ran.**

## T2 — câu hỏi chéo-phòng

Từ Legal, 2026-10-24. Phòng sở hữu: Data. Same vendor, same priors — no external verifier ran.

| # | Câu hỏi (nguyên văn) | Trả lời của Data | Đã sửa gì |
|---|---|---|---|
| 1 | "Cấm đọc IP có cấm luôn việc chặn spam theo IP ở tầng Cloudflare không?" | Data không bật, vì gói Free chỉ có 1 rule rate limiting và rule đó chỉ đếm theo IP. Khi M1 bị bơm: **phát hiện** bằng F1 (đột biến tổng), F2 (bài 5 > 1,2 × bài 4), F3 (gần trần). **Hành động:** Duy xác nhận ⇒ cách ly ngày ⇒ M1–M5 bỏ ngày đó. Bị cách ly ≥ 2 lần trong 4 tuần ⇒ đưa câu này lại cho Duy, kèm số. Cột "tổng ghi/ngày" giờ có ngưỡng và hành động. **Bật rule IP: → Duy.** **Đã chốt: không bật (QĐ 31).** | TL;DR · §2 bước 0 · §3 dòng IP · `TRACKING-PLAN.md` §2.4 |
| 2 | "Khi lưu lượng thấp, bảng đếm gộp có còn 'không định danh' không?" | Không hoàn toàn. Ba việc Data đã làm: chỉ tính dữ liệu từ ngày ra mắt; M6 sau ra mắt chạy trên D1 riêng; ẩn ô n < 5 và bỏ bảng ngày × bài/card. Bước 1 cũ chỉ cấm *kết luận* khi n < 100; giờ dashboard **không hiện** ô n < 5. Phần còn hở là Duy vẫn query được bảng thô. Đổi hạt lưu sang tuần: **→ Duy**. Câu luật: **→ Legal (L13)**. **Đã chốt: giữ ngày, gộp tuần nếu L13 đòi (QĐ 32).** | TL;DR · §2 bước 0 · §3 dòng ô nhỏ · `TRACKING-PLAN.md` §3, §5 |

## Đổi ở vòng sửa 2026-10-24

Data sửa theo review S1 vòng 1 (B4, N5, N6, N7, T3 Δ13). Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Vì sao |
|---|---|---|
| TL;DR | Thêm dòng: hướng lệch của M1 chưa biết → Duy (Q-xx) | B4 · Δ13 |
| §1 M1, cột "Là X" | Bỏ "dừng mở thêm bài GĐ01/02/05", thay bằng "đưa Duy quyết" | N6: QĐ 14 không cắt phạm vi |
| §1 M4 | Mẫu số đổi từ bài 1 lối vào sang bài 1 GĐ01, kèm đoạn giải thích dưới bảng | N5 |
| Dưới bảng §1 | Thêm điều kiện để M1 đọc được → Duy (Q-xx) | B4 |
| §2 bước 1 · M3 riêng | Ngưỡng 100 áp cho M1, M2, M4, M5. M3 dùng ngưỡng 30 lượt mỗi card. Thêm điểm treo về thẻ lật → Duy (Q-xx) | N7 · Δ12 |
| §4 | Câu "M1 xẹp" đổi thành hai kịch bản. Thêm dòng chỗ hở ô nhỏ của M3 | Δ13 · N7 |

## Đổi theo QĐ 17–35 (2026-10-24)

Data áp QĐ 23, 24, 25, 26, 29, 31, 32. Không tự quyết điều chưa có quyết định. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| TL;DR | M1 = "đọc + thử"; M1 lệch về phía xẹp; ô nhỏ đã chốt; M4 từ ngày ra mắt; thêm một điểm → Duy (thẻ lật × QĐ 24). Bỏ hai "→ Duy (Q-xx)" | 23 · 24 · 29 · 32 |
| §1 M3 | Chỉ card trắc nghiệm | 25d |
| §1 M4 | **Mẫu số đổi từ bài 1 GĐ01 sang bài 1 lối vào, tính từ ngày ra mắt**; đoạn giải thích viết lại | 29 |
| §1 M5 | `method` ∈ {`link`,`code`} | 25c |
| Dưới bảng §1 | Điều kiện M1 ≤ 1 đã thoả nhờ QĐ 23 | 23 |
| §2 bước 0, 1 · M3 riêng | Căn cứ cách ly = QĐ 31; mẫu số M4 trong bước 1; bỏ điểm treo thẻ lật | 25d · 29 · 31 |
| §3 | IP và ô nhỏ ghi đã chốt; thêm 3 dòng `N/A — because`: thẻ lật · tự khai/mời cài/`persist()` · event lúc mất mạng | 25d · 25e · 26 · 31 · 32 |
| §4 | M1 bỏ kịch bản B; thêm lệch tử/mẫu của M4 và mất event offline | 23 · 26 · 29 |
| T2 câu 1, 2 | Ghi đã chốt | 31 · 32 |

Frontmatter `status`/`blocked_on` giữ nguyên.

## Đổi vòng sửa 2 (2026-10-24)

Data sửa theo review sau QĐ 17–35: M7, M8, §4(b), và QĐ 36, 37. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Căn cứ |
|---|---|---|
| frontmatter `blocked_on` | Điều kiện 3 "có tên kế toán + bấm giờ 1 bài" đổi thành đúng chữ QĐ 36: agent chạy thử 1 bài mẫu + card, đo giờ Duy đọc báo cáo và ký. `status` vẫn là `fail` | QĐ 36 ("Điều kiện 3 trước S1 đổi thành…") · review M8 |
| TL;DR dòng `status` | M3 hết BLOCKED. Chỉ còn M5 BLOCKED | QĐ 36 |
| TL;DR dòng M1 | "Lệch về phía xẹp" đổi thành "hướng ròng **chưa biết**", vì có hai lực ngược nhau | review M7 |
| TL;DR dòng → Duy | Thêm M7 (`from_start`). N1: Data đổi khuyến nghị từ A sang B | review M1 · M7 |
| §1 M3, cột "Là X" | "Kèm người kế toán (BLOCKED)" đổi thành "agent `ke-toan-reviewer` soát, Duy ký". Ghi rõ trần phán của K2 | QĐ 36 · 37 · review §4(b) |
| Dưới bảng §1 | Câu "QĐ 23 giữ M1 ≤ 1 trừ khi bị bơm" bỏ, vì sai. Thay bằng cách đọc M1 khi chưa biết hướng lệch, kèm bảng hai dấu hiệu | review M7 |
| §4 | Viết lại dòng M1. Thêm hai dòng: phạm vi của "không định danh" (hộp thư khiếu nại), và agent kế toán chưa chạy thử | review M7 · §4(a) · QĐ 36 · 37 |

**Lý do cũ (giữ lại theo quy tắc 14):** bản trước kết luận "M1 lệch về phía xẹp, ≤ 1 trừ khi bị bơm". Kết luận đó chỉ xét tự khai và đọc lại sau khi mất storage, mà không xét cửa vào giữa chừng (PRD §Định nghĩa dùng chung "Cửa vào", AC-76). Lý do Duy ghi ở QĐ 23 ("Giữ M1 đọc được, lệch về phía xẹp") dựa trên kết luận đó, nên nay **yếu đi**. QĐ 23 vẫn làm đúng việc của nó: gỡ phần thổi do tự khai.

## Đổi theo QĐ 38–51 (2026-10-25)

Data áp QĐ 38, 39, 45. QĐ 40–44, 46–51 không chạm metric hay event. Không tự quyết điều chưa có quyết định. Frontmatter `status`/`blocked_on` giữ nguyên. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| TL;DR dòng M1 | M1 báo hai số chặt/lỏng; "xong bài" = card **trắc nghiệm** | 38 · 39 |
| TL;DR dòng lệch | "Hướng ròng chưa biết" đổi thành: phần thổi do cửa vào đo được (lỏng − chặt); số chặt lệch xẹp, trừ hai trường hợp thổi | 39 |
| TL;DR dòng → Duy | N1, M7 ghi đã chốt. Còn một điểm → Duy không gấp: ngưỡng M1 đặt trên số nào. Thêm dòng `persist()` | 38 · 39 · 45 |
| §1 M1 | Cột metric: hai số. Cột ngưỡng: đặt trên số nào → Duy | 39 |
| §1 M3 | M3 thấy mọi bài | 38 |
| Dưới bảng §1 | Viết lại "Đọc M1 thế nào": bảng ba số (chặt · lỏng · hiệu); hai dấu hiệu đọc theo số chặt, F2 trên số chặt, xem F4 trước khi cách ly | 38 · 39 |
| §2 bước 2 | Thêm: ngưỡng M1 trên số chặt hay lỏng → Duy, Data khuyến nghị chặt | 39 |
| §3 thẻ lật | Thẻ lật không làm bài xong | 38 |
| §3 `persist()` | Giữ `N/A — because`; ghi QĐ 45 không đổi câu trả lời đo | 45 |
| §4 | Viết lại dòng M1; thêm dòng hệ quả QĐ 38 lên M2 | 38 · 39 |

**Lý do cũ (giữ lại theo quy tắc 14):** trước QĐ 39, TL;DR ghi "hướng lệch ròng của M1: CHƯA BIẾT", và M1 được đọc kèm hai dấu hiệu chỉ báo **nghi**, không đo được cỡ, vì bảng đếm gộp không giữ liên kết giữa hai event của cùng một storage. Dấu hiệu "F2 bật một mình" khi đó có nghĩa "bơm **hoặc** bài 5 vừa được chia sẻ", và Duy phải tự kiểm việc chia sẻ trước khi cách ly.
