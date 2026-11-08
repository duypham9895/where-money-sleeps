---
status: pass
stage: 01-spec
date: 2026-11-08
owner: Data
blocked_on: []
---

# TRACKING-PLAN — Where Money Sleeps, mùa 1

**TL;DR** · đọc khoảng 6 phút
- **5 event, tên + thuộc tính đã chốt (QĐ 25, 39).** Ba tên giữ nguyên từ quyết định 9; `sync_link_created` → `sync_created{method}`; bỏ `lang`; `method` ∈ {`link`,`code`}; thẻ lật không bắn (§1). **`lesson_completed` thêm `from_start`** (QĐ 39, mở lại 25b có chủ đích; §2.5).
- **"Xong bài" = đã trả lời ≥ 1 card trắc nghiệm cuối bài** (QĐ 24, 38); thẻ lật không tính ⇒ M1 đo "đọc + thử", không phải "đọc tới cuối".
- **Chống trùng không cần ID:** cờ `tel` nằm **trong chính JSON tiến độ** và đi theo bản sao lưu (QĐ 26), khoá theo `lessonId` / `cardId` / nguồn — không theo ngôn ngữ. Mọi bài của giai đoạn được tự khai bị **chặn bắn vĩnh viễn** (QĐ 23, §2). Mất mạng ⇒ event mất, không hàng đợi (QĐ 26).
- **Nơi lưu khuyến nghị: Cloudflare D1** (bảng đếm gộp theo ngày), **không** Analytics Engine, **không** KV (§4).
- **Bắt buộc tắt Workers Logs** — mặc định BẬT cho Worker mới và ghi metadata request (§3).
- **Dashboard phải sống trước S5.**
- **Spam vào M1: không chặn theo IP** — kể cả rule ở Cloudflare (QĐ 31). Phát hiện bằng cờ F1–F4 + **cách ly ngày**, không xoá (§2.4).
- **Dữ liệu trước ngày ra mắt (S4 bắn tay, M6) không vào metric.** Lưu theo **ngày**, dashboard ẩn ô n < 5 (QĐ 32, §3, §5).
- **M1 báo hai số (QĐ 39):** chặt (bài 5 `from_start=true`) và lỏng (mọi bài 5). Lỏng − chặt = cỡ thổi do vào thẳng bài giữa lối vào (§2.5). **F2 tính trên số chặt.**
- **Cờ F4 chạy** (QĐ 38): mỗi `lesson_completed` thật bắn cùng một chạm với `card_answered` của một card trắc nghiệm ⇒ bài vượt tổng card của nó là nghi POST giả (§2.4).
- **Hai điểm → Duy của vòng trước đã chốt:** N1 = B (QĐ 38) · `from_start` (QĐ 39). **Cảnh báo `persist()` là điều kiện ra mắt (QĐ 45), vẫn không có event** (§1).

## 1. Event — hợp đồng

Quy ước: `snake_case`, danh từ + động từ quá khứ. Mọi giá trị là chuỗi ngắn từ **danh sách cho phép** sinh lúc build.

| Event | Thuộc tính | Bắn khi | Chống trùng (khoá) | Phục vụ |
|---|---|---|---|---|
| `lesson_completed` | `lesson`: lessonId ổn định (không phải số thứ tự) · `from_start`: `true`\|`false` (QĐ 39, định nghĩa §2.5). **Không thuộc tính nào khác** (bỏ `lang`, QĐ 25b) | Bài chuyển *chưa xong → xong* vì người học **trả lời card trắc nghiệm đầu tiên trong bộ card cuối bài** (đúng hay sai, QĐ 24). Chạm "Nhớ/Chưa nhớ" trên thẻ lật **không** làm bài xong (QĐ 38). Bắn **cùng một chạm** với `card_answered` của card đó. Không bắn khi trạng thái xong đến từ tự khai (R3) hay khôi phục (R4) | `lessonId` — **một lần, bất kể ngôn ngữ** | M1 (chặt + lỏng), M2, mẫu số M4/M5, F2, F4 |
| `card_answered` | `card`: `<cardId>.v<n>` · `correct`: `true`\|`false` | Lần trả lời **đầu tiên** của một card **trắc nghiệm**. Thẻ lật tự chấm **không bắn** (QĐ 25d) | `card` (kèm phiên bản) | M3, F4 |
| `pdf_opened` | `source`: `hosted`\|`own` | PDF render xong trang đầu | `source` — một lần mỗi nguồn | M4 |
| `sync_created` | `method`: `link`\|`code` | Người học tạo bản sao lưu (link `#sync` hoặc mã copy) | `method` — một lần mỗi cách | M5 |
| `progress_restored` | `method`: `link`\|`code` | Khôi phục tiến độ **thành công** từ bản sao lưu | **Không** chống trùng — mỗi lần khôi phục là một sự kiện thật | M5 |

Không có event cho tự khai, mời cài màn hình chính, `persist()` (QĐ 25e) — lý do và khi nào xét lại: `SUCCESS-CRITERIA.md` §3. QĐ 45 đưa cảnh báo `persist()` vào cổng ra mắt; điều đó **không** thêm event.

**Quy tắc phiên bản card:** `cardId` gán **lúc duyệt** và không đổi khi máy sinh card chạy lại. Sửa nội dung card sau khi đã đăng ⇒ tăng `v`. Nhờ vậy M3 tách được "trước sửa" và "sau sửa"; sinh lại card mà đổi `cardId` là **cắt đôi lịch sử**.

**Quy tắc bài số 1 và số 5:** M1 gắn với **lessonId** của vị trí 1 và 5 lúc ra mắt. Mẫu số M4 gắn với lessonId của **bài 1 lối vào** — trình đọc PDF có từ ngày ra mắt (QĐ 29, `SUCCESS-CRITERIA.md` §1). `from_start` cũng gắn với lessonId bài 1 lối vào lúc ra mắt (§2.5). PM đổi thứ tự lối vào ⇒ thêm một dòng có ngày ở §6, không sửa tại chỗ; đổi bài 1 là đổi **nghĩa** `from_start`.

**Đổi tên so với quyết định 9:** `sync_link_created` → `sync_created` + `method`. Lý do: quyết định 7 ghi *"Zalo cắt `#` ⇒ sync chuyển sang copy mã"* — nếu phép đo ra kết quả đó, tên cũ sai nghĩa và phải đổi, tức là cắt lịch sử. Duy nhận đổi tên này ở **QĐ 25(a)**. `progress_restored` thêm `method` cùng lý do.

**Ba điểm đã chốt ở QĐ 25** (trước ra mắt nên đổi không tốn gì; sau ra mắt thì thêm là tự do, bỏ hay đổi nghĩa là đổi hợp đồng):

| Điểm | Chốt | Hệ quả cho đo |
|---|---|---|
| `lesson_completed.lang` | **Bỏ** (25b) | `d2` của `lesson_completed` không mang `lang`; từ QĐ 39 nó mang `from_start` (§4). Bản EN bật mà có câu hỏi quyết định cho EN ⇒ thêm event/thuộc tính mới, ghi dòng có ngày ở §6 |
| `method: file` | **Bỏ** (25c, theo QĐ 18: sao lưu file JSON ra khỏi mùa 1) | `method` ∈ {`link`,`code`}. AC-70 không kiểm luồng file |
| Thẻ lật tự chấm | **Không bắn `card_answered`** (25d) · **không làm bài xong** (QĐ 38) | M3 chỉ gồm card trắc nghiệm. Ghi `N/A — because` ở `SUCCESS-CRITERIA.md` §3 |

**`definition` của "xong bài"** (QĐ 24, 38): bài chuyển *chưa xong → xong* khi người học **trả lời ≥ 1 card trắc nghiệm cuối bài, đúng hay sai**. Kèm bất biến AC-75, thắt lại ở QĐ 38: bài `published` phải còn ≥ 1 card **trắc nghiệm** `published`, nếu không bài không bao giờ xong được và M1/M2 có lỗ. Không thoả được bằng cuộn nhanh.

**N1 — đã chốt B (QĐ 38, 2026-10-25).**

| Mục | Nội dung |
|---|---|
| Chốt | Thẻ lật tự chấm **không** tính là "đã trả lời". Mỗi bài `published` phải có ≥ 1 card **trắc nghiệm** `published` (AC-75 thắt lại) |
| Hệ quả cho đo | M3 thấy mọi bài. Mỗi `lesson_completed` thật đi cùng một `card_answered` ⇒ **F4 chạy** (§2.4) |
| Đánh đổi Duy đã nhận | Quyền soạn bài kết thúc toàn thẻ lật, đổi lấy M3 thấy mọi bài và một phép kiểm chéo chống bơm |
| Nếu sai | Sau ra mắt, đổi lại là đổi nghĩa `lesson_completed` ⇒ dòng có ngày ở §6, cắt đôi lịch sử M1/M2 |

Lập luận của Data đã dẫn tới QĐ 38, giữ làm lý do. Đây là **lập luận đo lường**; chi phí nội dung là việc của PM và Writer.

| # | Tiêu chí | A · Tính thẻ lật | B · Không tính | Nghiêng về |
|---|---|---|---|---|
| 1 | QĐ 24 chặn được cuộn nhanh không | Được: lật rồi chạm, tức 2 chạm | Được: 1 chạm vào một đáp án | Hoà. **Sửa bản trước:** bản trước ghi cái mất của A là "chạm 'Nhớ' không cần nghĩ". Nhưng QĐ 24 tính cả "đúng hay sai", nên trắc nghiệm cũng thoả được bằng một chạm đoán bừa. Về công sức tối thiểu, hai loại ngang nhau |
| 2 | M3 nhìn thấy bài nào | Bài có bộ card cuối toàn thẻ lật thì **không có `card_answered` nào**: M3 mù với cả bài đó | Mọi bài `published` có ≥ 1 card M3 thấy được | **B.** M3 trả lời câu hỏi "card sai" (LLM sinh câu hỏi sai 6–22%, QĐ 8). Một bài mù M3 thì chỉ còn mắt Duy và agent kế toán |
| 3 | Kiểm chéo chống bơm | `lesson_completed` có thể đến từ thẻ lật, tức không có `card_answered` đi kèm | Mỗi `lesson_completed` thật bắn **cùng một chạm** với `card_answered` của một card trắc nghiệm trong bài đó. Vì vậy, theo ngày: `lesson_completed`(bài L) ≤ Σ `card_answered` của các card trắc nghiệm thuộc L, sai lệch chỉ do beacon mất | **B.** Thêm được cờ F4 rẻ: bài 5 vượt tổng `card_answered` của bài 5 ⇒ nghi POST giả chỉ nhắm `lesson_completed`. Kẻ bơm muốn lọt phải bơm cả hai, với `cardId` đúng. **Lập luận, chưa thử** |
| 4 | Lỗ ở M1/M2 khi gỡ card | Gỡ card cuối cùng (loại nào cũng được) ⇒ bài phải gỡ theo (AC-75) | Gỡ card **trắc nghiệm** cuối cùng ⇒ bài phải gỡ theo. Mà hành động của M3 chính là đọc lại, và có thể gỡ, card trắc nghiệm | **A.** B làm hành động của M3 dễ kéo theo ngày `lesson_completed` = 0, tức M2 có một bước rơi thật mà không phải lỗi của bài (PRD dòng 409). Cỡ lỗ phụ thuộc mỗi bài có bao nhiêu card trắc nghiệm: **chưa biết** |
| 5 | Ngưỡng "xong" có giống nhau giữa các bài không | Giống nhau: chạm 1 card bất kỳ | Giống nhau: chạm 1 card trắc nghiệm | Hoà |

**Vì sao Data đổi khuyến nghị.** Bản trước chọn A chủ yếu để AC-75 giữ nguyên, và nêu cái mất của A ở dòng 1. Viết đủ năm dòng thì dòng 1 thành hoà, còn B thắng ở 2 và 3, hai tiêu chí phục vụ trực tiếp M3 và §2.4. A chỉ thắng ở dòng 4.

**Điều kiện làm Data đưa câu này lại cho Duy:** bộ card cuối bài trong mùa 1 phần lớn chỉ có **một** card trắc nghiệm. Khi đó lỗ ở dòng 4 lớn.

**Không phải bằng chứng:** Data và PM giờ cùng chọn B, nhưng vì những lý do khác nhau. Hai phiên cùng vendor đồng ý với nhau không làm B đúng hơn. Nếu mùa 1 không có thẻ lật thì câu này tự đóng (ADDENDUM bước 8 cho phép thẻ lật).

## 2. Chống trùng không cần ID

### 2.1 Cơ chế

Trường `tel` trong JSON tiến độ — **đã vào schema theo QĐ 26**, đi theo bản sao lưu (whitelist R28). Trường thời điểm hoạt động cuối (cũng QĐ 26) **không** đi theo sao lưu và **không bao giờ** vào payload event:

```
"tel": {
  "lesson_completed": { "<lessonId>": "sent" | "suppressed" },
  "card_answered":    { "<cardId>.v<n>": "sent" },
  "pdf_opened":       { "hosted": "sent", "own": "sent" },
  "sync_created":     { "link": "sent", ... }
}
```

| Quy tắc | Nội dung |
|---|---|
| R1 · một khoá một lần | Trước khi bắn: khoá đã có trong `tel` ⇒ **không bắn**. Chưa có ⇒ ghi `"sent"` **trước**, rồi gọi `sendBeacon` **đúng một lần**, bất kể kết quả. `"sent"` nghĩa là "đã thử gửi", không phải "đã tới". |
| R2 · ngôn ngữ không nhân đôi | Khoá là `lessonId`, mà `sectionId`/`lessonId` **dùng chung VI/EN** (quyết định 6). Gạt VI ⇄ EN rồi đọc lại ⇒ không bắn. |
| R3 · tự khai giai đoạn | Tự khai **theo giai đoạn**, lối vào là một khối (QĐ 23). Mọi bài của giai đoạn được khai ⇒ ghi `"suppressed"`, **không bắn `lesson_completed`, kể cả nếu sau đó trả lời card thật**. Lý do: người tự khai phần lớn là người đã mất storage và đã được đếm. Đổi lại: thiếu đếm người tự khai để nhảy cóc rồi học thật. Đổi R3 sau ra mắt = đổi nghĩa ⇒ dòng có ngày ở §6. |
| R4 · khôi phục | `tel` **đi cùng** bản sao lưu (link/mã, QĐ 26). Khôi phục ⇒ cờ về theo, bài cũ không bắn lại. Bản sao lưu cũ không có `tel` ⇒ mọi bài đã xong trong đó ghi `"suppressed"`. |
| R5 · ưu tiên thiếu hơn thừa | `sendBeacon` trả `true` chỉ nghĩa là **đã xếp hàng**, không phải đã tới (MDN). Event mất ⇒ **không** bắn lại. Thiếu đếm được chấp nhận; đếm đôi thì không. |
| R6 · gửi khi nào | Gửi ngay lúc sự kiện xảy ra. **Không hàng đợi** (QĐ 26): mất mạng ⇒ event mất. Không dùng `unload`/`beforeunload`/`pagehide` (MDN: không bắn trên di động). |

**R5 × R6 khi mất mạng: đã gỡ bởi QĐ 26.** Không còn hàng đợi nên không còn hai nhánh phải đoán. R1 (ghi khoá trước, gửi một lần) bảo đảm không đếm đôi dù `sendBeacon` trả gì. Hệ quả: `fetch(…, {keepalive: true})` chờ phản hồi rồi mới ghi khoá **bị loại** — trang đóng trước phản hồi thì lần sau bắn lại, tức đếm đôi. Kiểm `navigator.onLine` trước khi gửi là tuỳ S3; kết quả đo như nhau.

### 2.2 Vẫn bị THỔI sau khi mất storage — không chống được

| Tình huống | Hệ quả |
|---|---|
| Storage bị xoá (ITP 7 ngày, xoá dữ liệu site, tab ẩn danh) và người học **đọc lại từ đầu** thay vì khôi phục/tự khai | Các bài đọc lại bắn lần hai |
| Cùng người dùng **tab Safari và app màn hình chính** (storage tách riêng — WebKit bug 181849, PRODUCT-BRIEF) | Một người = hai bộ storage = đếm hai lần. **BLOCKED — chờ đo iPhone/Android** (iOS 26 còn tách không) |
| Zalo/FB mở link trong WebView có storage riêng | Như trên. **BLOCKED — chờ đo iPhone/Android** |
| Nhiều thiết bị không đồng bộ | Mỗi thiết bị đếm riêng |
| Ai đó POST thẳng vào endpoint | Không có ID nên không chặn theo người được. Danh sách cho phép **không** chặn được POST giả mang tên + giá trị hợp lệ. Xử lý: **phát hiện và cách ly**, không chặn (§2.4) |

### 2.3 Hướng lệch của M1 — **đã chốt kịch bản A (QĐ 23)**, chưa đo

Bản đầu kết luận M1 **xẹp**. Kết luận đó chỉ đúng nếu tự khai đánh dấu **cả giai đoạn**. Duy chốt đúng như vậy ở QĐ 23 ⇒ cột A dưới đây là hiện hành; cột B giữ làm lý do vì sao không chọn.

| | A · Tự khai **theo giai đoạn** (lối vào là một khối) | B · Tự khai **theo bài** (chọn bài *k*) |
|---|---|---|
| R3 ghi `suppressed` | Mọi bài của các giai đoạn đã khai là xong, gồm cả bài 1 và bài 5 lối vào nếu khai đã qua lối vào | Bài 1 tới bài *k* − 1 |
| Đọc thật sau đó | Lối vào không bắn thêm gì | Bài *k* tới bài 5 bắn. Bài 5 được đếm ở tử số mà bài 1 không được đếm ở mẫu số |
| M1 | **Xẹp** (thận trọng), **nếu chỉ xét tự khai**. Lệch còn lại chủ yếu đến từ người mất storage rồi đọc lại từ bài 1: mẫu số bị thổi nhiều hơn tử số. Cửa vào giữa chừng kéo theo hướng ngược lại, xem §2.5 | **Thổi, có thể > 1.** Tử tăng mà mẫu không tăng. Người đã tới bài 5, mất storage, rồi khai lại ở bài 3 ⇒ bài 5 bị đếm hai lần |
| Cờ F2 (§2.4) | Không bị báo giả **do tự khai**. Từ QĐ 39, F2 tính trên số chặt nên cũng không bị báo giả do cửa vào giữa chừng (§2.5) | **Báo động giả.** Bài 5 > 1,2 × bài 4 có thể do tự khai thật, không phải do bơm |
| M1 đọc được không | Được, như `SUCCESS-CRITERIA.md` §1 | Không, trừ khi Data đổi R3: tự khai **bất kỳ bài nào trong lối vào** ⇒ cả lối vào ghi `suppressed`. Cách này kéo M1 về kịch bản A. Đổi lại: không đếm được người tự khai rồi đọc thật phần còn lại của lối vào |

**Đã chốt:** A (QĐ 23). F2 không bị báo động giả từ tự khai. Đổi sang B sau ra mắt = đổi nghĩa R3 ⇒ dòng có ngày ở §6.

**Giới hạn của bảng này (thêm vòng sửa 2):** bảng chỉ xét **một** lực là tự khai. Nó bỏ quên cửa vào giữa chừng, mà lực đó đi theo hướng ngược lại (§2.5). Câu "M1 xẹp" ở cột A vì vậy chỉ đúng **cho riêng lực tự khai**, không phải cho M1.

Cả hai kịch bản đều **chưa đo**. `progress_restored` chỉ cho cận dưới của số lần mất storage, vì người tự khai không để lại event nào (T3 Δ16).

### 2.4 Event giả — phát hiện và cách ly, không chặn theo IP (thêm 2026-10-24, T2 Legal)

**Không chặn theo IP ở bất kỳ tầng nào Duy cấu hình** — mã Worker (R23) **và** Rate Limiting Rules / WAF custom rules / Bot Fight Mode của Cloudflare (**QĐ 31**). Gói Free chỉ cho **1** rate limiting rule và **chỉ đếm theo IP**, nên ở gói này không có lối "chặn ở edge mà không xử lý IP".

| Cờ | Điều kiện (ngưỡng = **lựa chọn của Data**, Duy sửa được) | Bắt được gì |
|---|---|---|
| F1 · đột biến | Tổng ghi trong ngày > **5 ×** trung vị 7 ngày trước **và** > **300** | Bơm số lượng lớn |
| F2 · phễu ngược | Cửa sổ 7 ngày, **số chặt** (QĐ 39): `lesson_completed` bài 5{`from_start=true`} > **1,2 ×** bài 4{`from_start=true`}, với bài 5{`true`} ≥ **20** | Bơm nhắm thẳng M1 chặt. **Báo giả** khi người đọc bỏ qua bài 4 (§2.5). Chia sẻ bài 5 cho người chưa đọc bài 1 không còn làm F2 bật. **Không thấy** bơm chỉ nhắm số lỏng (`from_start=false`) — F1, F4 vẫn thấy |
| F4 · không card (QĐ 38) | Cửa sổ 7 ngày: `lesson_completed` bài L (gộp cả hai giá trị `from_start`) > Σ `card_answered` (gộp cả hai giá trị `correct`) của các card trắc nghiệm thuộc L, với L ∈ {bài 1, bài 5}. Ánh xạ card → bài lấy từ danh sách cho phép lúc build. Chỉ tính nội bộ, không hiện bảng card | POST giả chỉ nhắm `lesson_completed`. **Lập luận, chưa thử** (§1 N1) |
| F3 · gần trần | Tổng ghi trong ngày ≥ **80%** trần ghi (§3) | Sắp mất trọn ngày |

| Bước | Quy tắc |
|---|---|
| Cờ bật | Dashboard tô đỏ ngày đó. Không tự loại gì. |
| F2 bật một mình (F1 không bật) | Từ QĐ 39, chia sẻ bài 5 không còn làm F2 bật. Nguyên nhân thật còn lại: người đọc bỏ qua bài 4. **Trước khi** cách ly, Duy xem F4 của bài 5: F4 không bật nghĩa là bài 5 có `card_answered` đi kèm — hợp với người đọc thật, nhưng không loại được kẻ bơm cả card. Cách ly một ngày thật là mất số thật |
| Duy xác nhận nghi bơm | Thêm **một dòng có ngày** vào danh sách cách ly (`day`, lý do, ngày thêm). Chỉ thêm, không sửa. Nơi lưu: **TBD — SWE chốt ở S3** (file trong repo hoặc bảng D1) |
| Tính metric | M1–M5 **bỏ** ngày bị cách ly ở cả tử và mẫu. Số thô **không xoá** |
| Mở lại câu chặn IP | Cách ly ≥ **2 lần trong 4 tuần** ⇒ Data đưa số lên Duy hỏi lại QĐ 31 |

**Cái này KHÔNG bắt được:** người bơm đều cả 5 bài theo đúng tỉ lệ phễu, ở mức dưới F1. Chấp nhận ở mùa 1: site ngách, động cơ bơm thấp, và mọi kết luận M1 đã chờ n ≥ 100 + 4 tuần (`SUCCESS-CRITERIA.md` §2).

### 2.5 Cửa vào giữa chừng thổi M1 — hai lực ngược nhau (thêm vòng sửa 2, review M7)

**Sự thật thiết kế:** mọi URL trang bài đều là cửa vào (PRD §Định nghĩa dùng chung "Cửa vào", AC-76). Người mở link bài 5 trên Zalo với storage trống, đọc, rồi trả lời card thì **bài 5 bắn, bài 1 không**. Chống trùng vẫn đúng, vì mỗi khoá chỉ bắn một lần. Cái sai nằm ở chỗ **M1 giả định ai tới bài 5 cũng đã qua bài 1**.

| Lực | Cơ chế | Hướng của M1 | Cỡ |
|---|---|---|---|
| Mất storage rồi đọc lại từ bài 1 (§2.2) | Bài 1 bắn lại nhiều hơn bài 5 | **Xẹp** | Chưa đo. `progress_restored` chỉ là cận dưới |
| Tự khai theo giai đoạn (QĐ 23, §2.3) | Khai qua lối vào ⇒ cả lối vào `suppressed`, không vào tử lẫn mẫu | Gần trung tính. Xẹp nhẹ ở người khai rồi vẫn học thật | Chưa đo |
| **Vào thẳng bài *k* ∈ 2..5 từ link** | Bài *k* bắn, bài 1 không | **Thổi**, có thể > 1 khi *k* = 5. M2 có bước ngược ở bài được chia sẻ. F2 báo giả | Chưa đo. Phụ thuộc bài nào được chia sẻ |
| Bỏ qua một bài bằng điều hướng | Bài *k*−1 không bắn, bài *k* có | Không lệch M1 (vì bài 1 vẫn bắn). Có bước ngược ở M2 | — |
| Storage tách (Safari ⇄ app ⇄ WebView Zalo, §2.2) | Đọc bài 1–4 ở Safari, bài 5 ở WebView: mỗi bài vẫn chỉ đếm một lần | Không lệch số lỏng. Đọc lại ở storage thứ hai thì thổi bài đó. **Số chặt xẹp:** bài 5 ở WebView mang `from_start=false` | **BLOCKED — chờ đo iPhone/Android** |

**Kết luận: hướng lệch ròng của số lỏng chưa biết.** Bản trước kết luận "M1 xẹp, ≤ 1 trừ khi bị bơm" là sai, vì chỉ xét hai lực đầu. Thổi là hướng **đắt hơn**: M1 lên trên ngưỡng giả thì Duy giữ lối vào, trong khi lẽ ra phải viết lại. Từ QĐ 39, phần thổi do cửa vào **đo được** bằng lỏng − chặt; số chặt còn lệch về phía xẹp, trừ bơm và trường hợp khôi phục sang máy thứ hai (§7).

**Số gộp không tự tách được hai lực.** Bảng `counts` không giữ liên kết giữa hai event của cùng một storage. Muốn biết bài 5 nào "đã qua bài 1", client phải gửi thông tin đó, tức là phải đổi hợp đồng event. Có ba phương án, không phương án nào cần ID mới hay đổi tên event. **Duy chốt phương án 1 (QĐ 39).**

| Phương án | Cách làm | Được | Mất | Đổi hợp đồng? |
|---|---|---|---|---|
| 0 · Giữ, đọc kèm dấu hiệu | Không đổi gì. Đọc M1 kèm hai dấu hiệu ở `SUCCESS-CRITERIA.md` §1 (bước ngược, F2 bật một mình) | Không tốn gì | Chỉ báo **nghi**, không đo được cỡ. F2 vẫn báo giả | Không. Áp dụng ở vòng sửa 2; **thay bởi phương án 1** |
| **1 · Cờ `from_start`** — **ĐÃ CHỐT (QĐ 39)** | Lúc bắn `lesson_completed`, client xem `tel.lesson_completed[<lessonId bài 1 lối vào>]` đã có chưa (`sent` hoặc `suppressed`) ⇒ `from_start`: `true`\|`false`. Ghi vào `d2` (§4). **M1 chặt** = bài 5{`true`} ÷ bài 1. **M1 lỏng** = như hiện nay. Hiệu giữa hai số = cỡ thổi do cửa vào | Đo được M7 thay vì đoán. M1 chặt trả lời đúng câu "lối vào có **đưa** người tới bài 5 không". F2 tính trên số chặt thì hết báo giả do chia sẻ. Giữ đủ số cho M2 và mẫu số M5 | Trái chữ QĐ 25b ("không thuộc tính nào khác"). Số ô tăng gấp đôi nên nhiều ô `<5` hơn. Người đọc bài 1 ở Safari rồi bài 5 ở WebView bị tính `false`, tức M1 chặt **xẹp** ở nhóm này. Cờ được tính trên máy từ chính storage, không rời máy dưới dạng ID | **Có** ⇒ Duy chốt ở QĐ 39 |
| 2 · Chặn bắn | Chỉ bắn `lesson_completed` cho bài *k* ≠ 1 khi `tel` đã có bài 1 | M1 ≤ 1 trở lại, trừ khi bị bơm | **Mất hẳn** số của người vào giữa chừng: M2 mù với bài được chia sẻ, mẫu số M5 (bài 3) mất người. Đổi **nghĩa** `lesson_completed`. Không hồi tố được | **Có**, đổi nghĩa ⇒ **→ Duy**. Data **không** khuyến nghị |

**`from_start` — hợp đồng đã chốt (QĐ 39, 2026-10-25).**

| Mục | Quy định |
|---|---|
| Giá trị | `true`\|`false`, chuỗi trong danh sách cho phép (như `correct`). Worker bỏ event thiếu hoặc sai giá trị |
| `true` khi | `tel.lesson_completed[<lessonId bài 1 lối vào>]` đã có (`sent` **hoặc** `suppressed`) |
| Tính lúc nào | **Sau** bước ghi khoá của R1 ⇒ chính bài 1 lối vào luôn mang `true`. Không metric nào dùng giá trị của bài 1; quy ước này là lựa chọn của Data để một quy tắc phủ mọi bài |
| Tính ở đâu | Trên máy, từ chính `tel`. Không rời máy dưới dạng ID; payload chỉ có một bit |
| Bài nào mang | **Mọi** `lesson_completed`, kể cả bài ngoài lối vào — một hợp đồng cho một event. Bài ngoài lối vào: không metric nào dùng bit này (§7) |
| Lưu | `d2` của `counts` (§4) |
| Dùng cho | M1 chặt (bài 5{`true`} ÷ bài 1), F2 (§2.4). M1 lỏng, M2, mẫu số M4/M5, F4 gộp cả hai giá trị |
| Tự khai, khôi phục | Tự khai qua lối vào ⇒ cả lối vào `suppressed`, bài 5 không bắn (R3). Khôi phục ⇒ `tel` về theo, bit đúng như trên máy cũ (R4). Bản sao lưu cũ không có `tel` ⇒ bài 1 đã xong ghi `suppressed` ⇒ bài 5 học sau đó mang `true` |

**Lý do cũ (quy tắc 14):** trước QĐ 39, phương án 0 áp dụng và §4 giữ `d2 = ''` cho `lesson_completed`.

## 3. Bộ đếm

| Phần | Quy định | Nguồn |
|---|---|---|
| Gửi | `navigator.sendBeacon(path, JSON)` — POST, tối đa 64 KiB | MDN sendBeacon |
| Cùng domain | Site và Worker **cùng origin** ⇒ site phải phục vụ từ Cloudflare (Workers Static Assets), không phải GitHub Pages | quyết định 9 · `../../../docs/data.md` |
| Path | Trung tính. **Cấm** `/collect` `/event` `/track` `/beacon` `/metrics` `/api/event` (EasyPrivacy) | `../../../docs/data.md` |
| Worker nhận | Kiểm tên event + giá trị thuộc tính với danh sách cho phép (deploy cùng site). Sai ⇒ bỏ. **Luôn trả 204.** | — |
| Worker KHÔNG đọc/ghi | IP, `CF-Connecting-IP`, User-Agent, `request.cf` (geo), referrer, giờ trong ngày | quyết định 9 |
| **Workers Logs** | **`observability.enabled = false`** trong wrangler config. Cloudflare: *"All newly created Workers will come with the observability setting enabled by default"*, mỗi log chứa *"the Request, Response, and related metadata"* ⇒ để mặc định là **lưu metadata request 3 ngày** mà không ai viết dòng code nào | developers.cloudflare.com/workers/observability/logs/workers-logs/ · /workers/wrangler/configuration/ |
| Hạt thời gian | **Ngày** (QĐ 32), theo giờ Việt Nam (UTC+7). Không lưu giờ. Workflow pháp lý L13 kết luận số gộp ghép ra được người ⇒ gộp các dòng lên tuần và **xoá dòng ngày** (ngày → tuần làm được, ngược lại không) | QĐ 32 |
| Lọc origin | Header `Sec-Fetch-Site` có mặt mà khác `same-origin` ⇒ bỏ, vẫn trả 204. Không lưu header. Chặn được trình duyệt ở site khác; **không** chặn được `curl` | Thêm 2026-10-24 (T2) |
| Trần ghi | Worker ngừng ghi khi tổng ghi trong ngày chạm trần **C** < trần thực tế của D1 (§4), để vượt free không khoá luôn việc đọc dashboard. Phần còn lại của ngày **mất** và ngày đó bật F3. **Không phải hàng rào chống spam.** Giá trị C và cách đếm không làm tăng gấp đôi dòng ghi: **TBD — SWE chốt ở S3, kiểm bằng số dòng ghi D1 thật** | Thêm 2026-10-24 (T2) |

Cloudflare **vẫn thấy IP** ở edge khi truyền — trang riêng tư phải viết đúng câu ở `../../../docs/data.md` §"Một câu phải viết đúng".

## 4. Nơi lưu — khuyến nghị **D1**

Hạn mức đọc ngày 2026-10-24.

| | **D1 (CHỌN)** | Analytics Engine | KV |
|---|---|---|---|
| Free | *"100,000 / day"* rows written · *"5 million / day"* rows read · *"5 GB (total)"* | *"100,000 included per day"* điểm ghi · *"10,000 included per day"* query | **Loại** |
| Vượt free | *"you will not be able to run queries against D1"* — đếm ngày đó mất, **không ra hoá đơn**; reset *"00:00 UTC"* | *"Currently, you will not be billed"* — hành vi khi vượt free **chưa đọc được** | — |
| Giữ dữ liệu | Tới khi xoá | *"stored for three months"* ⇒ phải dựng kho lạnh (GitHub Actions; cron tự tắt sau 60 ngày im lặng) | — |
| Độ chính xác | Đếm đúng, `UPSERT n = n + 1` | Có lấy mẫu khi một index ghi nhiều; phải dùng `sum(_sample_interval)` | *"eventually-consistent"*, *"up to 60 seconds"* ⇒ cộng đồng thời **mất lượt** (`../../../docs/lessons.md`) |
| Tự lưu IP? | Không — chỉ lưu thứ code ghi | Docs chỉ nêu `timestamp` + `_sample_interval` tự thêm | — |

**Lý do chọn D1, một câu:** M1 đọc theo tháng và so trước/sau mỗi lần sửa lối vào, nên **dữ liệu sống quá 3 tháng mà không cần đường ống thứ hai** quan trọng hơn mọi ưu điểm khác của Analytics Engine.

**Đánh đổi nói thẳng:** đây là **lệch khỏi kiến trúc tham chiếu ở `../../../docs/data.md`** (Analytics Engine + kho lạnh, viết cho noelroom mùa 2). Lệch có lý do, không phải quên.

Bảng đề xuất (SWE chốt ở S3):

```
counts(day TEXT, event TEXT, d1 TEXT, d2 TEXT, n INTEGER,
       PRIMARY KEY (day, event, d1, d2)) WITHOUT ROWID
   lesson_completed  d1=lesson  d2=from_start ('true'|'false', QĐ 39)
   card_answered     d1=card    d2=correct
   pdf_opened        d1=source  d2=''
   sync_created      d1=method  d2=''
   progress_restored d1=method  d2=''
```

D1 tính thêm một dòng ghi cho mỗi index (*"Indexes will add an additional written row"*). `WITHOUT ROWID` để khoá chính **là** bảng — **chưa kiểm** D1 có tính nó là 1 hay 2 dòng. Trường hợp xấu: trần thực tế 50.000 event/ngày.

## 5. Dashboard — phải sống trước S5

| Yêu cầu | |
|---|---|
| Hiện được | M1 **chặt và lỏng** (QĐ 39), mỗi số luỹ kế + 28 ngày trượt, M2, M3 (card ≥ 30 lượt), M4, M5, và **tổng ghi/ngày** để thấy spam hoặc sắp chạm trần — kèm cờ F1–F4 và danh sách ngày cách ly (§2.4) |
| Ngày ra mắt | Mọi metric chỉ tính từ `day ≥ NGÀY_RA_MẮT` (một hằng số, ghi một dòng có ngày ở §6 lúc S5). Dòng trước đó — S4 bắn tay (AC-70), buổi M6 nếu làm trước ra mắt — giữ làm bằng chứng S4, **không vào metric** |
| M6 sau ra mắt | Nếu buổi 5 người diễn ra **sau** ngày ra mắt: chạy trên bản deploy preview có D1 **riêng**, không trên production |
| Ô nhỏ | (QĐ 32) Không hiện ô nào có n < **5** trong bảng tách theo `card`, `lesson` hay theo ngày — hiện `<5`. Tỉ lệ M1, M2, M4, M5 chỉ hiện khi mẫu số ≥ 100. Tỉ lệ sai M3 của một card hiện khi card đó đủ 30 lượt trả lời đầu (`SUCCESS-CRITERIA.md` §2, thống nhất ở vòng sửa 2026-10-24). k = 5 là **lựa chọn của Data**. Dashboard **không** có bảng ngày × bài hay ngày × card; chỉ có tổng theo cửa sổ |
| Hình thức | **TBD — SWE chốt ở S3.** Phương án rẻ nhất: script cục bộ `wrangler d1 execute --json` → trang tĩnh. Nếu là route trên Worker ⇒ phải có lớp chặn truy cập; **chưa kiểm** phương án nào free |
| S4 | `EVENT-VERIFICATION.md`: bắn tay đủ 5 event trên iPhone + Android thật, **nhìn thấy số** trên dashboard |

## 6. Log — chỉ thêm, không sửa

| Ngày | Thay đổi | Lý do |
|---|---|---|
| 2026-10-24 | Bản đầu. 5 event; `sync_link_created` → `sync_created{method}`; thêm `method` cho `progress_restored`; `card` mang phiên bản. **Chờ Duy xác nhận đổi tên.** | §1 |
| 2026-10-24 | T2 Legal: thêm §2.4 (cờ F1–F3, cách ly ngày), lọc `Sec-Fetch-Site`, trần ghi C, lọc ngày ra mắt, ẩn ô n < 5. Không đổi tên hay ý nghĩa event nào. | Cuối file |
| 2026-10-24 | Vòng sửa: **không đổi tên hay ý nghĩa event nào.** Có ba đề xuất chờ Duy: bỏ `lang`, bỏ `method: file`, và không bắn `card_answered` cho thẻ lật | §1 · cuối file |
| 2026-10-24 | **Hợp đồng event chốt trước ra mắt (QĐ 23–26):** `sync_created{method}` thay `sync_link_created`; bỏ `lesson_completed.lang`; `method` ∈ {`link`,`code`}; thẻ lật không bắn `card_answered`; `lesson_completed` = trả lời ≥ 1 card cuối bài; R3 theo giai đoạn; không hàng đợi offline. Chưa có dữ liệu nào ⇒ không cắt lịch sử | QĐ 23–26 |
| 2026-10-24 | Vòng sửa 2: **không đổi tên, thuộc tính hay ý nghĩa event nào.** Có hai đề xuất chờ Duy: (1) thêm `lesson_completed.from_start` (§2.5, M7); (2) N1 = B, thẻ lật không làm bài "xong" (§1). Thêm cờ F4, chỉ chạy khi N1 = B | §1 · §2.4 · §2.5 |
| 2026-10-25 | **Hợp đồng đổi trước ra mắt (QĐ 38, 39):** `lesson_completed` thêm `from_start` (`true`\|`false`, lưu ở `d2`); `lesson_completed` chỉ bắn khi trả lời card **trắc nghiệm** cuối bài — thẻ lật không làm bài xong; F4 chạy; F2 tính trên số chặt. QĐ 45 (`persist()`) không thêm event. Chưa có dữ liệu ⇒ không cắt lịch sử | QĐ 38 · 39 · 45 |

## 7. Chưa xác minh được

- Workers Logs có ghi **IP** không: docs chỉ nói "Request… metadata". Không cần biết — tắt hẳn. Nhưng S4 phải mở dashboard Cloudflare xác nhận **không có log**.
- `observability.enabled = false` có tắt hết mọi log không: wrangler docs nói `enabled` là *"Shorthand for logs.enabled"*; còn `issues.enabled` riêng — tắt cả hai, S4 kiểm.
- Analytics Engine khi vượt free trên gói Free: không tìm thấy câu trả lời.
- D1 tính `WITHOUT ROWID` + UPSERT là bao nhiêu dòng ghi: docs không nói về upsert.
- Lưu lượng thật: không có ước tính nào; mọi so sánh với trần 100k/ngày là **chưa có số**.
- Storage tab/app/WebView còn tách trên iOS 26, Zalo giữ `#` không: **BLOCKED — chờ đo iPhone/Android**.
- Sampled logs của Security Events trên gói Free có hiện IP cho Duy không: docs gợi ý cột "IP address" và ghi Free là *"Sampled logs only"*, không nói rõ. **TBD — cần xác minh bằng mở dashboard Cloudflare.**
- Bot Fight Mode có chèn JS vào trang không (chạm R27): **chưa kiểm**. Không bật, nên chưa cần.
- iOS Safari / WebView Zalo có gửi `Sec-Fetch-Site` với `sendBeacon` không: **chưa kiểm**. Thiếu header ⇒ quy tắc cho qua, nên không mất event thật. S4 kiểm.
- Ngưỡng F1–F3 (F4 không có ngưỡng số), k = 5: lựa chọn của Data, không có nguồn.
- Mất mạng ⇒ event mất (QĐ 26): **chưa đo** mất bao nhiêu, và mất có đều giữa bài 1 và bài 5 không (không đều thì M1 lệch). S4 kiểm bằng chế độ máy bay rằng bật mạng lại **không** bắn lại (R1).
- Độ dài link `#sync` khi mang `tel`: **BLOCKED — chờ đo Zalo** (QĐ 26).
- Hướng lệch của M1 ở kịch bản A (§2.3, QĐ 23): lập luận, **chưa đo**.
- Hướng lệch **ròng** của M1 lỏng (§2.5): phần thổi do cửa vào đo được bằng lỏng − chặt từ ngày ra mắt (QĐ 39), **chưa có số**. Số chặt lệch bao nhiêu: **chưa đo**.
- Hai lực thổi số chặt, lập luận chưa thử: (a) bơm POST mang `from_start=true`; (b) bản sao lưu khôi phục sang máy thứ hai sau bài 1, rồi cả hai máy học tiếp bài 5 ⇒ bài 5 đếm hai lần, bài 1 một lần.
- Bơm chỉ nhắm số lỏng (`from_start=false`) không làm F2 bật; F1 (nếu đủ lớn) và F4 vẫn thấy. **Chưa thử.**
- `from_start` trên bài ngoài lối vào: không metric nào dùng, nhưng làm số ô của các bài đó gấp đôi ⇒ nhiều ô `<5` hơn. Giới hạn bit vào bài lối vào là đổi hợp đồng: QĐ 39 không nói phạm vi bài, Data không tự thu hẹp.
- Cờ F4 có bắt được POST giả không, và beacon mất làm lệch bất đẳng thức của nó bao nhiêu: **chưa thử**. Lề an toàn của F4 là số card trắc nghiệm mỗi bài: bài có nhiều card thì Σ `card_answered` lớn hơn hẳn `lesson_completed`; bài chỉ một card thì một beacon `card_answered` mất cũng có thể làm F4 báo giả.
- Toàn bộ là xác minh phía tác giả. **Same vendor, same priors — no external verifier ran.**

## Nguồn (đọc 2026-10-24)

- https://developers.cloudflare.com/d1/platform/pricing/
- https://developers.cloudflare.com/analytics/analytics-engine/pricing/
- https://developers.cloudflare.com/analytics/analytics-engine/limits/
- https://developers.cloudflare.com/analytics/analytics-engine/sampling/
- https://developers.cloudflare.com/analytics/analytics-engine/get-started/
- https://developers.cloudflare.com/workers/observability/logs/workers-logs/
- https://developers.cloudflare.com/workers/wrangler/configuration/
- https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon
- `../../../docs/data.md` · `../../../docs/lessons.md` (KV) · `../00-discovery/PRODUCT-BRIEF.md` quyết định 4, 6, 7, 9, 15, 18, 23–26, 29, 31, 32, 38, 39, 45
- https://developers.cloudflare.com/waf/rate-limiting-rules/ — Free: *"Number of rules: 1"*, counting characteristics *"IP"*, chu kỳ 10 s
- https://developers.cloudflare.com/waf/analytics/security-events/

## T2 — câu hỏi chéo-phòng

Từ Legal, 2026-10-24. Phòng sở hữu: Data. Same vendor, same priors — no external verifier ran.

| # | Câu hỏi (nguyên văn) | Trả lời của Data | Đã sửa gì |
|---|---|---|---|
| 1 | "Cấm đọc IP có cấm luôn việc chặn spam theo IP ở tầng Cloudflare không?" | **Data không bật.** Rule rate limiting/WAF/Bot do Duy cấu hình là xử lý IP **vì mục đích của Duy** (giữ M1 sạch), khác IP mà Cloudflare tự xử lý cho bảo mật của họ — chính cái câu R25 đang mô tả. Gói Free chỉ đếm theo IP, nên không có phương án edge nào tránh được IP. Thay vào đó: phát hiện bằng số gộp (F1–F3) + cách ly ngày + trần ghi C. PRD K7 "đã giải" chỉ đúng cho mã Worker. **Có cho phép bật hay không: → Duy** (và → Legal: nối vào L13). **Đã chốt: không bật (QĐ 31).** | §2.2 dòng POST · §2.4 mới · §3 lọc origin, trần ghi · §5 cờ + cách ly · TL;DR |
| 2 | "Khi lưu lượng thấp, bảng đếm gộp có còn 'không định danh' không?" | **Không hoàn toàn.** Bảng không chứa ID, nhưng ô n = 1 ghép với thứ Duy biết sẵn thì chỉ ra được người. Data tự làm ba việc thuộc phạm vi của mình: (a) metric chỉ tính từ ngày ra mắt ⇒ S4 bắn tay và M6 trước ra mắt bị loại; (b) M6 sau ra mắt chạy trên D1 riêng; (c) dashboard ẩn ô n < 5 và không có bảng ngày × bài/card. **Còn hở:** Duy vẫn query được bảng thô bằng `wrangler`, nên (c) chỉ chặn việc *vô tình thấy*. Đóng hở đó cần đổi hạt lưu **ngày → tuần** cho dòng có chiều: **→ Duy** (đổi lại: cách ly mất cả tuần thay vì một ngày, và cần thêm một dòng ghi `day × event` để F1/F3 còn chạy). Dữ liệu ghép được có tính là "dữ liệu cá nhân" theo Luật 91 không: **→ Legal (L13)**. **Đã chốt: giữ ngày, ẩn n < 5, gộp tuần nếu L13 đòi (QĐ 32).** | §3 hạt thời gian · §5 ngày ra mắt, M6, ô nhỏ |

## Đổi ở vòng sửa 2026-10-24

Data sửa theo review S1 vòng 1 (B4, N2, N3, N9, N10, N11, T3 Δ12, Δ13). Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Vì sao |
|---|---|---|
| frontmatter `blocked_on` | Thêm điều kiện hợp đồng Ringkas, vì tên miền của bộ đếm vướng Legal R34 | N11 |
| TL;DR dòng 1 | "Duy xác nhận" đổi thành "**chờ** Duy xác nhận" | N10 |
| TL;DR | Thêm dòng liệt kê các điểm chờ Duy và việc S3 phải chọn | — |
| §1 đổi tên | "nhưng Duy xác nhận" đổi thành "chờ Duy xác nhận → Duy (Q-xx; PRD K3)" | N10 |
| §1 bài số 1/5 | Thêm lessonId bài 1 GĐ01 làm mẫu số M4 | N5 |
| §1 bảng mới | Ba điểm chờ Duy: `lang`, `method: file`, `correct` với thẻ lật, mỗi điểm có khuyến nghị | N2 · N3 · Δ12 |
| §2.1 | Thêm R5 × R6 khi mất mạng: S3 chọn giữa A (`onLine`) và B (`fetch keepalive`) | N9 |
| §2.3 | Viết lại thành hai kịch bản A/B, kèm phụ thuộc → Duy (Q-xx) | B4 · Δ13 |
| §5 Ô nhỏ | Ngưỡng 100 không áp cho M3; M3 dùng 30 lượt mỗi card | N7 |
| §6 Log · §7 | Thêm dòng log, thêm hai mục chưa xác minh | — |

Hợp đồng event (tên, thuộc tính, ý nghĩa) **chưa đổi**. Mọi đề xuất bỏ thuộc tính hay giá trị chờ Duy.

## Đổi theo QĐ 17–35 (2026-10-24)

Data áp QĐ 23, 24, 25, 26, 29, 31, 32. Không tự quyết điều chưa có quyết định. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| TL;DR | Viết lại: hợp đồng event đã chốt, định nghĩa "xong bài", `tel` theo sao lưu, không hàng đợi, không rule IP, hạt ngày; còn một điểm → Duy | 23–26 · 31 · 32 |
| §1 bảng event | Bỏ `lang`; `method` ∈ {`link`,`code`}; `card_answered` chỉ card trắc nghiệm; `lesson_completed` bắn khi trả lời card đầu tiên cuối bài, không bắn khi xong do tự khai/khôi phục; thêm dòng "không event cho tự khai / mời cài / `persist()`" | 24 · 25 |
| §1 bài số 1/5 | Mẫu số M4 đổi từ bài 1 GĐ01 sang bài 1 lối vào | 29 |
| §1 đổi tên · bảng ba điểm · `definition` | "Chờ Duy" ⇒ đã chốt; `definition` hết TBD | 24 · 25 |
| §1 mới | **→ Duy:** thẻ lật có tính là "đã trả lời" cho QĐ 24 không | 24 |
| §2.1 | `tel` đã vào schema, theo sao lưu; trường thời điểm không theo sao lưu, không vào event. R1: ghi khoá **trước**, gửi một lần. R3: theo giai đoạn. R6: không hàng đợi. Bảng A/B của S3 bỏ: hết xung đột, loại `fetch keepalive` chờ phản hồi | 23 · 26 |
| §2.3 | Đã chốt kịch bản A | 23 |
| §2.4 | Căn cứ đổi từ "T2 câu 1" sang QĐ 31 | 31 |
| §3 hạt thời gian | Ngày; gộp tuần + xoá dòng ngày nếu L13 đòi | 32 |
| §4 bảng D1 | `lesson_completed` `d2=''` | 25b |
| §5 ô nhỏ | Bỏ chiều `lang` | 25b · 32 |
| §6 Log | Thêm một dòng chốt hợp đồng | — |
| §7 | Thêm: mất event khi offline chưa đo; độ dài link `#sync` với `tel` BLOCKED | 26 |
| T2 câu 1, 2 | Ghi đã chốt | 31 · 32 |

Frontmatter `status`/`blocked_on` giữ nguyên.

## Đổi vòng sửa 2 (2026-10-24)

Data sửa theo review sau QĐ 17–35: M1 (hai khuyến nghị N1 ngược nhau) và M7 (cửa vào giữa chừng). Không đổi tên, thuộc tính hay ý nghĩa event nào. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | Căn cứ |
|---|---|---|
| TL;DR | "M1 lệch về phía xẹp" đổi thành "hướng ròng chưa biết". Hai điểm → Duy: N1, M7 | review M1 · M7 |
| §1 N1 | Viết lại theo khuôn quyết định. Thêm bảng 5 tiêu chí để đặt cạnh lập luận PM. **Data đổi khuyến nghị A → B.** Ghi điều kiện làm Data quay lại A | review M1 · quy tắc 12 |
| §2.3 | Ô M1 và F2 ghi "chỉ xét tự khai". Thêm đoạn giới hạn của bảng | review M7 |
| §2.4 | F2 ghi rõ khi nào báo giả. Thêm bước "F2 bật một mình ⇒ Duy kiểm việc chia sẻ trước khi cách ly". Thêm F4, chỉ chạy khi N1 = B | review M7 · N1 |
| §2.5 mới | Bảng năm lực, kết luận hướng ròng chưa biết, ba phương án, và → Duy (M7) | review M7 |
| §6 · §7 | Một dòng log; hai dòng chưa xác minh | — |

**Lý do cũ (giữ lại theo quy tắc 14):**
- N1: bản trước khuyến nghị A ("mọi loại card đều đưa bài tới xong; AC-75 giữ nguyên"), và nêu cái mất của A là "chạm 'Nhớ' không cần nghĩ".
- §2.3: bản trước viết "M1 xẹp", "F2 không bị ảnh hưởng" như kết luận cho cả M1.

## Đổi theo QĐ 38–51 (2026-10-25)

Data áp QĐ 38, 39, 45. QĐ 40–44, 46–51 không chạm event hay bộ đếm. Không tự quyết điều chưa có quyết định. Frontmatter `status`/`blocked_on` giữ nguyên. Same vendor, same priors — no external verifier ran.

| Chỗ | Đã đổi | QĐ |
|---|---|---|
| TL;DR | Hợp đồng thêm `from_start`; "xong bài" = card trắc nghiệm; M1 hai số, F2 trên số chặt; F4 chạy; N1, M7 đã chốt; `persist()` không có event | 38 · 39 · 45 |
| §1 bảng event | `lesson_completed`: thêm `from_start`; bắn khi trả lời card **trắc nghiệm** đầu tiên, cùng chạm với `card_answered`; thẻ lật không làm bài xong. Cột "Phục vụ" thêm F2, F4 | 38 · 39 |
| §1 dưới bảng | `persist()`: QĐ 45 không thêm event. Bài số 1: `from_start` gắn với lessonId bài 1 | 39 · 45 |
| §1 ba điểm QĐ 25 · `definition` | `d2` mang `from_start`; thẻ lật không làm bài xong; AC-75 đòi card **trắc nghiệm** | 38 · 39 |
| §1 N1 | Khuôn "→ Duy" thay bằng bảng "đã chốt B". Bảng 5 tiêu chí giữ làm lý do | 38 |
| §2.3 · §2.5 bảng lực | F2 hết báo giả do cửa vào; dòng storage tách: số chặt xẹp | 39 |
| §2.4 F2 · F4 · bước "F2 bật một mình" | F2 trên số chặt (bài 5 và bài 4 cùng `from_start=true`); F4 bỏ điều kiện "chỉ khi N1 = B"; trước khi cách ly xem F4 thay vì hỏi việc chia sẻ | 38 · 39 |
| §2.5 | Phương án 1 đã chốt; khuôn "→ Duy (M7)" thay bằng bảng hợp đồng `from_start` | 39 |
| §4 bảng D1 | `lesson_completed` `d2=from_start` | 39 |
| §5 | M1 chặt và lỏng; cờ F1–F4 | 38 · 39 |
| §6 · §7 · Nguồn | Một dòng log; viết lại hai dòng chưa xác minh, thêm ba dòng | — |

**Ba chi tiết hợp đồng là lựa chọn của Data, không có trong chữ QĐ 39** — Duy sửa được, trước ra mắt không tốn gì: (1) F2 so bài 5{`true`} với bài 4{`true`}, không với bài 4 gộp; (2) bit tính **sau** khi ghi khoá R1, nên bài 1 lối vào luôn `true`; (3) mọi `lesson_completed` mang bit, không chỉ bài lối vào.

**Lý do cũ (giữ lại theo quy tắc 14):** trước QĐ 38, F4 chỉ chạy "khi N1 = B", và `lesson_completed` bắn khi trả lời "card đầu tiên trong bộ card cuối bài" — chưa nói thẻ lật có tính không. Trước QĐ 39, `d2 = ''` cho `lesson_completed`; F2 tính trên số gộp và báo giả khi bài 5 vừa được chia sẻ, nên bước "F2 bật một mình" bắt Duy tự kiểm việc chia sẻ trước khi cách ly.
