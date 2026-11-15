---
status: fail
stage: 01-spec
date: 2026-10-24
owner: Writer
tier: THAM CHIẾU — PM gộp phần cần vào PRD.md; Duy không cần đọc hết file này
blocked_on:
  - "Duy đo iPhone + Android thật (~30 phút): Zalo giữ #sync không · mở WebView hay trình duyệt · input type=file chạy không · localStorage sống trong WebView không"
  - "Duy đọc hợp đồng lao động Ringkas (điều khoản IP + không cạnh tranh)"
  - "Agent ke-toan-reviewer chạy thử 1 bài mẫu + card; đo thời gian Duy đọc báo cáo và ký (QĐ 36)"
---

# WRITER — giọng văn, chú thích, glossary, tagline, chuỗi giao diện

**TL;DR** · đọc khoảng 8 phút · tham chiếu cho PRD
- **5 quy tắc giọng văn**, mỗi quy tắc có ví dụ đúng/sai bằng VN và EN. Cả năm quy tắc đều nhắm tới một câu trong ONE-PAGER §2: *"À, hoá ra tiền của mình đi như thế."*
- **Cách hiện chú thích thuật ngữ — ĐÃ CHỐT:** chạm mới hiện (QĐ 16) · **mở tại chỗ** ngay sau câu (QĐ 17) · gạch chấm ở lần đầu **mỗi mục H2** (QĐ 19). Xem §2.
- **Thuật ngữ chuyên ngành giữ tiếng Anh trong dòng chữ** (Debit, Credit, accrual, APR…), chạm mở thẻ có nhãn EN + giải thích VN (QĐ 20). **Ngoại lệ: bài VN viết "sổ cái"**, `ledger` chỉ trong thẻ (QĐ 44). Quy ước cũ "viết hoa Nợ/Có trong dòng" **bỏ**. Tên tài khoản lấy nguyên văn TT 99/2025: agent `ke-toan-reviewer` soát, Duy ký (QĐ 36). Hiện chỉ có bản chép thứ cấp ⇒ phán tối đa "KHỚP NGUỒN THỨ CẤP"; bài GĐ01 có tên tài khoản **BLOCKED** tới khi có Phụ lục II chính thức (QĐ 37).
- **Tagline = T1** (QĐ 22).
- **Chuỗi mới:** dòng minh bạch AI theo cờ `ai_assisted` **theo bài / bộ card / bản EN** (QĐ 34, 42; phần định danh **để trống chờ hợp đồng Ringkas**) · **dòng soát công khai = câu W2** (QĐ 41) · dòng "chưa có bản EN" **song ngữ** (QĐ 43b) · trang khiếu nại "gỡ tạm trong 72 giờ" (QĐ 35, hộp thư **để trống**). Xem §5. Ba chuỗi cảnh báo lưu trữ ở §6 là **chữ của cổng ra mắt** (QĐ 45).
- **W1, W2 và hai câu "→ Duy" cũ về ngôn ngữ đã đóng** (QĐ 41, 43, 44). Chỗ còn hở: cuối file, mục "Đổi theo QĐ 38–51".

> Mọi ví dụ trong file này chỉ để **minh hoạ giọng văn**, chưa phải nội dung đã duyệt.
> Các con số trong ví dụ (10.000.000đ, phí 2%) lấy từ ví dụ mở đầu của lộ trình gốc (`SOURCE-ROADMAP.md`). **Chưa qua agent kế toán (QĐ 36), chưa có chữ ký của Duy.**

---

## 0. Đã soát ECC trước khi viết (quy tắc 10)

| Thứ cần | Tìm thấy | Kết luận |
|---|---|---|
| `VOICE-PROFILE` của xưởng | `gates/01-spec/VOICE-PROFILE.md` + `anti-ai-writing` (`A1–A5`) | **Đã khởi tạo v1 (2026-11-15)** từ cặp giọng thật của `card` + `ONE-PAGER` + phản hồi đọc thật của Duy/người thân. Mọi lượt soạn & biên tập content (`article`, `beats`, `GLOSS`, `quiz`, `videoScript`, `.srt`, mô tả YouTube) bắt buộc chạy Pass 3b bằng `anti-ai-writing` và đạt cổng `C10`. Chờ vòng `Diff-Distillation` từ 5–8 đoạn Duy tự gạch sửa để khắc sâu thêm dấu ấn riêng. |
| Schema profile | `ecc:brand-voice/references/voice-profile-schema.md` | §1 dùng **các trục** của schema (nhịp câu, độ nén, cách nêu luận điểm, những gì bị cấm), nhưng là **giọng của sản phẩm**, rút từ ONE-PAGER, không phải giọng của Duy. |
| Danh sách cấm của brand-voice | `"not X, just Y"`, câu hỏi mồi, giọng thought-leader | Đã áp vào §1 và §4. |

---

## 1. Giọng văn bài học — 5 quy tắc

Người đọc ở tầng vào: khoảng 25 tuổi, không biết kế toán, đọc trên điện thoại lúc 10h tối (PRODUCT-BRIEF §Vấn đề & người dùng).

| # | Quy tắc | ❌ Sai | ✅ Đúng |
|---|---|---|---|
| 1 | **Đi từ chuyện đã xảy ra với người đọc, rồi mới gọi tên khái niệm.** Định nghĩa đứng sau ví dụ, không đứng trước. | VN: "Double-entry là nguyên tắc ghi mỗi nghiệp vụ vào ít nhất hai tài khoản."<br>EN: "Double-entry bookkeeping is the principle of recording each transaction in at least two accounts." | VN: "Lương về, điện thoại báo +10.000.000đ. Trong sổ cái của ngân hàng, cùng lúc có hai dòng: tài khoản của bạn được ghi Credit 10 triệu (khoản ngân hàng **nợ bạn** tăng lên), và một tài khoản khác bị ghi Debit đúng 10 triệu. Một sự kiện, hai dòng, hai bên bằng nhau. Người ta gọi đó là double-entry."<br>EN: "Payday. Your phone shows +10,000,000 VND. In the bank's books, two lines go in at once: your account gets a 10 million credit (what the bank **owes you** goes up), and another account gets a 10 million debit. One event, two lines, equal on both sides. That is double-entry." |
| 2 | **Một khái niệm mỗi đoạn. Dùng số cụ thể thay cho tính từ.** | VN: "Phí giao dịch có thể khá đáng kể đối với người bán."<br>EN: "Transaction fees can be quite significant for merchants." | VN: "Khách trả 10.000.000đ qua VietQR. Phí 2% là 200.000đ. Người bán nhận 9.800.000đ, và nhận vào ngày hôm sau."<br>EN: "A customer pays 10,000,000 VND by VietQR. A 2% fee is 200,000 VND. The merchant receives 9,800,000 VND, the next day." |
| 3 | **Nói rõ cái gì khác nhau và cái gì chưa chắc. Không khuyên, không hứa.** (ONE-PAGER §3.2: không tư vấn đầu tư) | VN: "Bạn nên chọn ngân hàng có phí thấp nhất."<br>EN: "You should pick the bank with the lowest fees." | VN: "Mỗi ngân hàng tính phí một kiểu. Bài này chỉ cho bạn tìm dòng phí trong biểu phí của chính ngân hàng bạn đang dùng."<br>EN: "Fees differ by bank. This lesson shows you where to find the fee line in your own bank's fee schedule." |
| 4 | **Nói chuyện ngang hàng. Không dùng giọng giáo trình, không dùng giọng bán khoá học.** Gọi người đọc là "bạn" (không "các bạn", không "quý vị"). Không cảm thán. Không viết "đơn giản thôi". | VN: "Thật đơn giản! Nắm vững 3 bước sau là bạn thành thạo kế toán!"<br>EN: "It's easy! Master these 3 steps and you'll be an accounting pro!" | VN: "Có ba bước. Bước hai dễ nhầm nhất, nên mình đi chậm ở đó."<br>EN: "Three steps. Step two is where most people slip, so we'll slow down there." |
| 5 | **Kết bài bằng đúng một câu nối lại chuyện ở đầu bài.** Đây là khoảnh khắc "À, hoá ra", và nó trùng với dòng tóm tắt trong khuôn bài của S0. | VN: "Tóm lại, bài học hôm nay đã giới thiệu các khái niệm quan trọng về kế toán."<br>EN: "In summary, today's lesson introduced key accounting concepts." | VN: "Vậy dòng +10.000.000đ tối qua là một dòng **Credit** trong sổ cái của ngân hàng, không phải trong sổ cái của bạn."<br>EN: "So last night's +10,000,000 VND was a **credit** in the bank's books, not in yours." |

**Trường bắt buộc khi soạn bài (Legal §A.1, QĐ 34, 42):** mọi mục H2 (`sectionId`, cả VI và EN) bắt buộc khai trường `based_on` (`[]` nếu tự viết không dựa trên nguồn CC BY nào; hoặc `{ asset, pages, mode }` theo `LEGAL-REVIEW.md` §A.1); mỗi bài, bộ card và bản EN bắt buộc khai cờ `ai_assisted` (`true`/`false`), `reviewed_by` và `reviewed_on`.

**Thuật ngữ trong bản VN (QĐ 20):** thuật ngữ chuyên ngành viết bằng tiếng Anh ngay trong dòng chữ, không dịch, không kèm ngoặc (`Debit`, không `Nợ (Debit)`); câu văn quanh nó vẫn là tiếng Việt. Từ đó phải là mục glossary có `keep_en` (AC-05). Ranh giới từ nào giữ EN: xem §3. **Ngoại lệ có tên của AC-05 (QĐ 43):** (a) **danh sách tên riêng** ngắn, không chú thích, tách khỏi glossary — ví dụ "Where Money Sleeps", tên sách/tác giả Hermanson, "CC BY 3.0"; (b) dòng "chưa có bản EN" song ngữ (§5).

**Quy ước riêng cho bản EN** (EN do Claude dịch lúc build, Duy duyệt; quyết định 6):

| Mục | Quy ước |
|---|---|
| Bối cảnh | **Giữ nguyên bối cảnh VN**: VND, VietQR, NAPAS 247. Không đổi sang ví dụ kiểu Mỹ. Bài dạy dòng tiền ở VN; nếu đổi ví dụ thì bản EN thành một bài khác, và phải duyệt lại từ đầu. |
| Tiền | VN: `10.000.000đ` · EN: `10,000,000 VND` |
| Số thập phân | VN: `2,5%` · EN: `2.5%`. Kiểm số trong card (ADDENDUM bước 5) phải hiểu **cả hai** định dạng. |
| Từ riêng của VN | Lần đầu mỗi mục H2 (QĐ 19): `ghi có (credit alert)`, sau đó chỉ dùng tên EN. **Chốt (QĐ 43c):** chữ VN trên trang EN chỉ hợp lệ khi là mục glossary **được đánh dấu** cho trang EN (chữ tin báo ngân hàng, tên TK TT 99); tên cờ do S3 đặt. `vi.term` trong thẻ chú thích được miễn. |

**Danh sách chữ cấm trong bài và giao diện** (máy grep được):
`lưu vĩnh viễn` · `không bao giờ mất` · `an toàn tuyệt đối` · `đơn giản thôi` · `dễ dàng` · `chắc chắn` · `nên mua` · `nên vay` · `bí quyết` · `làm giàu` · `thu nhập thụ động`
EN: `forever` · `never lose` · `easy` · `guaranteed` · `you should buy` · `get rich` · `passive income`

---

## 2. Chú thích thuật ngữ — **ĐÃ CHỐT** (QĐ 16, 17, 19)

Chuẩn của Duy (quyết định 5): *"nếu có các từ chuyên ngành thì phải có phần chú thích"*. Mọi chú thích lấy từ **một file glossary duy nhất**. Cách chú thích hiện ra đã chốt (QĐ 16, 17, 19).

> **2026-10-24 (vòng sửa):** QĐ 16 chốt *"chạm mới hiện"* (không hiện sẵn). Phương án C dưới đây **bị loại**, khuyến nghị C của Writer **rút lại**. Bảng giữ nguyên để giữ lý do cũ. Phần đã chốt ở cuối mục này.

| | A. Lần đầu mỗi bài · chạm | B. Mọi lần · chạm | ~~C. Lần đầu mỗi bài · hiện ngay; các lần sau · chạm~~ **LOẠI — QĐ 16** |
|---|---|---|---|
| Hiện thế nào | Lần đầu thuật ngữ có gạch chân chấm, chạm thì mở popover. Các lần sau là chữ thường. | Lần nào xuất hiện cũng có gạch chân, chạm được. | Lần đầu, một dòng định nghĩa ngắn (từ glossary) hiện ngay dưới đoạn văn. Các lần sau có gạch chân, chạm được. |
| Được gì | Trang sạch nhất. Bài giữ đúng độ dài. | Ở chỗ nào cũng tra lại được. | Người không biết cách chạm vẫn hiểu. Đúng với persona không có nền tảng. |
| Mất gì | Ai không chạm thì đọc tiếp mà không hiểu. Nếu quên nghĩa ở đoạn sau thì phải cuộn ngược lên tìm. | Bài về Nợ/Có có thể có Nợ hàng chục lần ⇒ cả trang toàn gạch chân. Dễ chạm nhầm khi cuộn trên điện thoại. | Bài dài thêm một chút, mỗi thuật ngữ mới thêm khoảng một dòng. Phải đo lại mức 5–8 phút mỗi bài. |
| Rủi ro | Tỉ lệ người chạm thật sự **chưa đo**. | Trang rối, mất cảm giác "sạch sẽ" mà quyết định 5 yêu cầu. | Dòng định nghĩa có thể lặp lại câu mà người viết vừa giải thích trong bài. |

~~**Khuyến nghị của Writer: C.**~~ **Rút lại 2026-10-24 — trái QĐ 16.** Lo ngại cũ (người tầng vào không biết thuật ngữ; điện thoại không có hover để gợi ý chữ chạm được) vẫn còn, nhưng giờ nó được **đo** ở buổi 5 người, không giải bằng cách hiện sẵn.

**Đã chốt sau QĐ 16** (bảng A/B ở trên chỉ còn để giữ lý do cũ; chữ "popover" ở cột A thay bằng mở tại chỗ):

| Câu | Chốt | Nguồn |
|---|---|---|
| (a) "Lần đầu" tính theo đơn vị nào | **Lần đầu mỗi mục H2** — gạch chấm + chạm được. Các lần sau trong cùng H2 là chữ thường | QĐ 19 |
| (b) Dạng chạm | **Mở tại chỗ**: thẻ chèn ngay sau câu, đẩy chữ xuống. Buổi 5 người so với "thẻ phủ lên chữ" | QĐ 17 |

**Một đơn vị cho cả file:** mọi chỗ "lần đầu / các lần sau" khác — §1 `ghi có (credit alert)`, §3 thuật ngữ, §3 `TK 112 — …` — đều tính theo **mục H2**, để S3 chỉ có một luật render.

**Thẻ chú thích trên trang VI (QĐ 20):** nhãn = `en.term` (đúng chữ trong dòng) · `vi.term` nếu có tên VN người học sẽ gặp ở sách/TT 99 · rồi `vi.short`. Ví dụ nhãn: **`Debit · bên Nợ`**, dòng dưới là `vi.short` (chữ định nghĩa do glossary cấp, chưa viết, kế toán duyệt). Mục `keep_en: false` (ví dụ `ledger`, QĐ 44): chữ trong dòng là `vi.term`, nên nhãn = `vi.term` · `en.term`, ví dụ **`sổ cái · ledger`**. Thứ tự và kiểu chữ trong thẻ: mặc định của Writer, S2 chỉnh được.

**Nếu chọn sai:** đảo ngược **rẻ**, *với điều kiện* glossary là nguồn duy nhất và cách hiện chú thích chỉ là một cờ render. S3 phải giữ được điều kiện này. Buổi quan sát 5 người đọc bài 1 (PRODUCT-BRIEF §Đo) là chỗ kiểm: ghi lại người đọc có chạm không.

**Quy tắc chung cho mọi dạng chạm:**
- Định nghĩa ngắn tối đa 25 từ VN / 20 từ EN. Không dùng thuật ngữ khác để giải thích một thuật ngữ, trừ khi thuật ngữ đó đã có chú thích trước đó trong **cùng mục H2** (QĐ 19: người đọc có thể vào thẳng đầu H2).
- Phép kiểm máy (QĐ 21): chữ EN trên trang VI không phải mục `keep_en` ⇒ **FAIL**; từ VN có trong danh sách gốc (TT 99 + glossary) mà bài chưa đánh dấu ⇒ **cảnh báo**. Jargon tiếng Việt ngoài danh sách thì máy không thấy, nên Duy vẫn phải bắt bằng mắt lúc duyệt.

---

## 3. Glossary song ngữ

| Quy ước | Chi tiết |
|---|---|
| **`Debit` / `Credit` và chữ "nợ"** (QĐ 20) | **Bên của bút toán** luôn viết bằng tiếng Anh trong dòng chữ: `Debit`, `Credit` (mục glossary `keep_en: true`). Không có dạng tiếng Việt nào của "bên" trong dòng chữ, viết hoa hay viết thường. **Chữ "nợ" tiếng Việt trong dòng chỉ có một nghĩa: khoản phải trả (debt)**, ví dụ "ngân hàng nợ bạn". Tên tiếng Việt của hai bên (`bên Nợ`, `bên Có`) chỉ nằm **trong thẻ chú thích**, ở trường `vi.term`, để người học nhận ra khi gặp ở sách hay TT 99. **Một bài đặt `Debit` cạnh "nợ" phải chỉ ra chỗ khác nhau**, vì đây là chỗ người mới hay vấp. *Quy ước cũ "viết hoa `Nợ/Có` trong dòng để phân biệt" không còn hiệu lực từ QĐ 20 (2026-10-24).* |
| **Ranh giới `keep_en`** (mặc định Writer) | **Giữ EN:** thuật ngữ kế toán / thanh toán có tên EN / tên chuẩn được dạy như khái niệm — `Debit`, `Credit`, `accrual`, `APR` (QĐ 20 nêu), và cùng loại: `double-entry`, `VietQR`, `NAPAS` (`VietQR` và `NAPAS` được dạy ở lối vào và GĐ02 nên nằm trong glossary với `keep_en: true` để có thẻ chú thích, không đưa vào danh sách tên riêng không-chú-thích). **Giữ VN:** **`sổ cái`** (QĐ 44: bài VN viết "sổ cái", khớp tagline T1; mục glossary `ledger` có `keep_en: false`, `en.term` = `ledger` chỉ hiện trong thẻ) · tên tài khoản TT 99 (văn bản VN, QĐ 21 coi là danh sách thuật ngữ VN) · chữ in nguyên văn trên tin báo/app ngân hàng VN (`ghi có`, `ghi nợ`, `số dư`). **Tên riêng không phải khái niệm học** ("Where Money Sleeps", tên tác giả/sách Hermanson, "CC BY 3.0"…): vào **danh sách tên riêng** của QĐ 43(a), tách khỏi glossary. QĐ 44 chỉ đổi `ledger`; `double-entry` và các mục khác giữ nguyên. |
| **Góc nhìn của tin nhắn ngân hàng** | Mục glossary "ghi có / ghi nợ" (trong tin báo biến động số dư) phải nói rõ: chữ đó tính **theo sổ của ngân hàng**, không theo sổ của bạn. |
| Dạng hiển thị trang VN | **Chốt (QĐ 20):** `Debit` trong dòng chữ, mọi lần, không ngoặc, không dịch. Lần đầu mỗi mục H2 có gạch chấm, chạm mở thẻ tại chỗ (QĐ 17, 19) với nhãn EN + giải thích VN (§2). Hai lập trường cũ (`Nợ (Debit)` trong dòng · chỉ `Nợ` trong dòng) đều **thôi**. |
| Dạng hiển thị trang EN | `debit`. Tên VN chỉ nằm **bên trong** thẻ chú thích chạm (trường `vi.term`, được miễn theo QĐ 43c). Chữ VN trong dòng chữ trang EN chỉ hợp lệ khi là mục glossary được đánh dấu cho trang EN (QĐ 43c). |
| **Tên tài khoản** | Lần đầu mỗi mục H2: `TK 112 — Tiền gửi không kỳ hạn`, với tên **nguyên văn** theo Phụ lục II TT 99/2025. Các lần sau: `TK 112`. Hiện chỉ đối chiếu được với bản chép thứ cấp `../../legal/tt99-phu-luc-ii.secondary.json` ⇒ phán tối đa **"KHỚP NGUỒN THỨ CẤP"**, không bao giờ PASS (QĐ 37). |
| Tên tài khoản bản EN | `Account 112 — Demand deposits`. Đây là **bản dịch tự làm, không chính thức**. Không chép bản dịch của KPMG/PwC/LuatVietnam (LEGAL-SCREEN xếp vào nhóm "Không đụng"). |
| Tên cũ theo TT 200 | Ghi vào `aliases` kèm chú thích "tên cũ, TT 200". Người học sẽ gặp tên cũ khi tự Google. |
| Trường tối thiểu mỗi mục | `id` (ASCII ổn định, dùng chung VN/EN) · `vi.term` · `en.term` · `vi.short` · `en.short` · `aliases` · `keep_en` (QĐ 20: `true` ⇒ trang VI hiện `en.term` trong dòng) · cờ "được hiện trên trang EN" cho mục VN (QĐ 43c; tên: S3) · `source` (`TT 99 PL II` \| `tự viết`) · `reviewed_by` · trường agent soát (QĐ 41; tên: S3, Legal X13) · `reviewed_at`. Cấu trúc file cụ thể do S3 quyết. |
| Duyệt (QĐ 36 thay "người kế toán" của QĐ 8; QĐ 41) | Mọi mục trong phạm vi QĐ 30 (tên tài khoản GĐ01, mục có con số): **`reviewed_by` = chỉ người ký (Duy)**; agent soát ghi ở **trường riêng** (QĐ 41). Chuỗi cũ `soát: agent kế toán (AI) · ký: Duy` **bỏ** vì chứa "kế toán". **Máy cấm** `kế toán` · `accountant` · `chuyên gia` · `expert` trong `reviewed_by` và trong dòng minh bạch (QĐ 41; không áp cho thân bài). Mặc định Writer, người bắt: không `CPA`, không chữ `duyệt`/`approved` gắn với agent — agent chỉ ra PASS/FAIL/UNVERIFIED/FLAG, chữ ký là của Duy. `reviewed_at` = ngày Duy ký, không phải ngày agent chạy. Tên tài khoản GĐ01: **BLOCKED — chờ Phụ lục II chính thức** (QĐ 37). Mục khác trong phạm vi QĐ 30: chờ agent soát + Duy ký. |

**Tên tài khoản đã đọc được** (qua nguồn thứ cấp LuatVietnam, đọc 2026-10-24). Writer so nhanh 12 tên dưới với `../../legal/tt99-phu-luc-ii.secondary.json` bằng script: **12/12 khớp chữ**, trong đó 111–411 (7 TK) khớp cả hai nguồn chép, 421–642 (5 TK) chỉ có một nguồn (`ketoanleanh`). Đây là kiểm phía tác giả, **không phải K2 của agent**, và mức cao nhất vẫn là "KHỚP NGUỒN THỨ CẤP" (QĐ 37). Đối chiếu với Phụ lục II chính thức: chưa làm được, vì bản gốc vbpl.vn trong repo không có Phụ lục.
111 Tiền mặt · 112 Tiền gửi không kỳ hạn *(TT 200 gọi là "Tiền gửi Ngân hàng")* · 113 Tiền đang chuyển · 131 Phải thu của khách hàng · 331 Phải trả cho người bán · 341 Vay và nợ thuê tài chính · 411 Vốn đầu tư của chủ sở hữu · 421 Lợi nhuận sau thuế chưa phân phối · 511 Doanh thu bán hàng và cung cấp dịch vụ · 515 Doanh thu hoạt động tài chính · 635 Chi phí tài chính · 642 Chi phí quản lý doanh nghiệp.

---

## 4. Tagline giải nghĩa — **bắt buộc** (Log 2026-10-24), **ĐÃ CHỐT T1** (QĐ 22)

> **Chốt 2026-10-24 (QĐ 22):** VN *"Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu."* · EN *"From the bank alert to the ledger: where your money actually goes."* Nguyên văn, không sửa chữ. Việc kèm của Duy: chụp 3 tin báo biến động số dư thật để xác nhận chữ "ghi có". Bảng dưới giữ lại để giữ lý do.

Tagline phải làm được ba việc: (1) chặn cách đọc *"gửi tiết kiệm ở đâu"*; (2) không biến thành lời khuyên tài chính; (3) không phá cảm giác của ONE-PAGER §2 (*"không thấy mình đang học kế toán"*).

**Phát hiện cần biết trước khi chọn:** trong tiếng Việt, chữ **"sổ"** đứng một mình gợi ngay **"sổ tiết kiệm"**. Vì vậy tagline nào có "sổ" phải viết đủ **"sổ cái"**, nếu không nó làm cách đọc sai **nặng thêm**.

| # | VN | EN | Ký tự VN/EN | Chặn "gửi tiết kiệm"? | Nối với chữ "Sleeps"? | Từ chuyên ngành |
|---|---|---|---|---|---|---|
| **T1** | Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu. | From the bank alert to the ledger: where your money actually goes. | 62 / 66 | **Mạnh**: hai vật cụ thể, không vật nào là tiết kiệm | Gián tiếp | "sổ cái" |
| T2 | Bài học ngắn về đường đi của đồng tiền, bắt đầu từ tiền của bạn. | Short lessons on how money moves, starting with yours. | 64 / 54 | Trung bình | Không | không |
| T3 | Mỗi lần chuyển khoản là một dòng trong sổ cái của ai đó. | Every transfer is a line in someone's ledger. | 56 / 45 | Mạnh | Có: tiền "nằm" trong sổ của người khác | "sổ cái" |
| T4 | Lương về, tiền nằm ở đâu, ai ghi sổ: kể từ giao dịch của chính bạn. | Payday, transfers, QR codes: who holds your money, and who writes it down. | 67 / 74 | Yếu: "ghi sổ" ≈ "sổ" | **Mạnh** | không |
| T5 | Kế toán và thanh toán, giải thích bằng tiền bạn chuyển mỗi tuần. | Accounting and payments, explained with the money you move every week. | 63 / 70 | **Mạnh nhất** | Không | "kế toán" — **trái ONE-PAGER §2** |

**Khuyến nghị (Duy đã nhận): T1.** Nó nói lại gần như nguyên văn câu mở đầu ONE-PAGER §1 (*"từ tin nhắn 'ghi có' khi lương về, tới bút toán Nợ/Có"*). Nó chặn cách đọc sai bằng hai vật cụ thể, mà không cần nói chữ "kế toán".

**Đánh đổi thật:** T1 gánh một thuật ngữ ("sổ cái") ngay trên header. T5 thì rõ nhất, nhưng nói thẳng ra điều ONE-PAGER muốn giấu. T3 hay nhất về chữ, nhưng ngắn tới mức người lạ có thể vẫn không biết site này dạy gì.

**Chỗ tagline xuất hiện** (đề xuất): dưới tên ở header · `<title>` · `og:description`, tức phần xem trước khi link được dán vào Zalo. Tên **"Where Money Sleeps" không dịch** trên trang VN. **⚠ X4.**

Độ dài vừa một dòng trên điện thoại: **TBD — cần xác minh** bằng mockup S2 ở bề ngang 360px với font đã chọn.

---

## 5. Chuỗi giao diện VN / EN

**Nguyên tắc đặt tên:** gọi đúng cái nó làm. Cơ chế "sync" của quyết định 7 là một **ảnh chụp tiến độ, gửi một lần**, không có máy chủ, không tự cập nhật. Chữ **"đồng bộ" / "sync"** hứa một thứ chạy liên tục ⇒ **không dùng trên giao diện**. Tên event là `sync_created{method}`, `method` ∈ {`link`, `code`} (QĐ 25 thay `sync_link_created` của QĐ 9). Nhãn giao diện không phụ thuộc câu trả lời: tên event là hợp đồng, nhãn giao diện thì không.

| Bề mặt | VN | EN | Trạng thái |
|---|---|---|---|
| Nút gạt ngôn ngữ | `VI · EN` (nhãn trợ năng: "Đổi ngôn ngữ") | `VI · EN` (aria: "Switch language") | Dùng `VI` (mã ngôn ngữ), không dùng `VN` (mã quốc gia) |
| Bài chưa có bản EN | Nút gạt mờ + **cả hai câu, trên trang VI:** `Bài này chưa có bản tiếng Anh.` · `This lesson isn't in English yet.` | (cùng dòng song ngữ; bài chưa có trang EN) | **Chốt — QĐ 43(b):** song ngữ là **ngoại lệ có tên** của AC-05, vì người chỉ đọc EN là người duy nhất cần dòng này. Một dòng hay hai dòng, thứ tự: S2 |
| Khôi phục tiến độ | `Khôi phục tiến độ` | `Restore progress` | |
| Tự khai giai đoạn (2 chạm) | `Chọn giai đoạn bạn đã học tới` | `Pick the stage you've reached` | **Chốt theo giai đoạn** (QĐ 23); lối vào là một khối trong danh sách chọn. Mọi bài của giai đoạn được khai ⇒ `suppressed`, không bắn `lesson_completed` |
| Mang tiến độ sang máy khác, **biến thể A: link** | `Gửi link tiến độ cho chính bạn` | `Send yourself a progress link` | **BLOCKED — chờ đo iPhone/Android** (Zalo có giữ `#` không) |
| … **biến thể B: mã** (nếu Zalo cắt `#`) | `Sao chép mã tiến độ` | `Copy progress code` | **BLOCKED — cùng phép đo** |
| Lời mời cài (sau khoảng 3 bài) | `Thêm vào màn hình chính để trình duyệt giữ tiến độ lâu hơn` | `Add to Home Screen so your browser keeps your progress longer` | **BLOCKED — đo iPhone/Android.** "Lâu hơn", không phải "luôn" (Dexie #739) |
| Mở file PDF của bạn | `Mở PDF của bạn — file không rời khỏi máy bạn` | `Open your own PDF — the file never leaves your device` | Câu này được phép tuyệt đối vì xử lý thuần cục bộ (quyết định 4). Tuyệt đối về **file**, không phải về tiến độ |
| Link đọc thêm | `Đọc thêm · EN · không bắt buộc` | `Further reading · optional` | Nguyên văn từ LEGAL-SCREEN |
| Giai đoạn chưa lên | `Sắp có` | `Coming later` | Không ghi ngày (quyết định 5) |
| Card lật | `Nhớ` · `Chưa nhớ` · `Đọc lại đoạn này` | `Got it` · `Not yet` · `Reread this part` | Theo ADDENDUM bước 8 |
| Dòng minh bạch AI — mục **có** `ai_assisted` | `Soạn với hỗ trợ AI, duyệt bởi ⟨…⟩, ngày <dd/mm/yyyy>.` | `Drafted with AI assistance, reviewed by ⟨…⟩, <yyyy-mm-dd>.` | QĐ 34: giữ trên mọi bài/bộ card đã đăng (1); vế "Soạn với hỗ trợ AI" chỉ ở mục có cờ `ai_assisted` (3). **Hạt của cờ = bài / bộ card / bản EN** (QĐ 42), cùng hạt với chỗ dòng hiện. Bài lai (một H2 dùng AI) ⇒ **cả bài** mang "Soạn với hỗ trợ AI" — sai về phía nói thừa. Bản EN do Claude dịch lúc build ⇒ luôn `true` (AC-53). Card sinh bằng máy (QĐ 2) ⇒ mặc định Writer: bộ card luôn mang cờ. **⟨…⟩ để trống — chọn sau khi Duy đọc hợp đồng Ringkas (QĐ 34.2).** Câu chữ cuối cùng thuộc Legal |
| Dòng minh bạch AI — mục **không** `ai_assisted` | `Duyệt bởi ⟨…⟩, ngày <dd/mm/yyyy>.` | `Reviewed by ⟨…⟩, <yyyy-mm-dd>.` | Hệ quả của QĐ 34 (1)+(3). **⟨…⟩ để trống — như trên.** Vị trí dòng (cuối mục hay cuối bài): S2. **Ràng buộc từ QĐ 36 cho cả hai dòng AI:** ⟨…⟩ chỉ là định danh của Duy; không được là, hay gợi tới, một người kế toán |
| Dòng soát công khai — mục có con số / tên tài khoản (phạm vi QĐ 30) | **Chốt:** `Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt.` | **Chốt:** `Figures and account names checked by an AI agent; signed off by ⟨…⟩.` | **QĐ 41 (câu W2): hiện.** Cả hai câu không chứa chữ máy cấm (`kế toán` · `accountant` · `chuyên gia` · `expert`). ⟨…⟩ để trống như dòng AI (QĐ 34.2). Rủi ro Luật AI 134/2025 (L14) nằm trong QĐ 51 |
| Trang khiếu nại (B10) | `Nếu bạn cho rằng một nội dung ở đây vi phạm quyền của bạn, hãy gửi thư tới ⟨…⟩. Nội dung bị khiếu nại sẽ được gỡ tạm trong 72 giờ sau khi nhận thư, trong lúc xem xét.` | `If you believe something here infringes your rights, email ⟨…⟩. The content will be taken down temporarily within 72 hours of receiving your email while it is reviewed.` | QĐ 35. **⟨…⟩ (hộp thư) để trống — công khai sau khi Duy đọc hợp đồng Ringkas.** Không họ tên, không nhắc Ringkas. "72 giờ" là đề xuất của Legal, **không có căn cứ luật** — NĐ 17/2023 đặt hạn ngắn hơn thì đổi chuỗi này. Câu chữ cuối thuộc Legal |
| Trang riêng tư — câu R25 mới (B10) | `Khi bạn đọc, Where Money Sleeps không thu thập định danh; nhà cung cấp hạ tầng có ghi địa chỉ IP cho mục đích bảo mật của họ. Nếu bạn gửi thư tới hộp thư khiếu nại, những gì bạn gửi (tên, email, nội dung) chỉ được dùng để xử lý khiếu nại đó.` | `When you read, Where Money Sleeps collects no identifiers; our infrastructure provider logs IP addresses for its own security purposes. If you email the complaints address, what you send (name, email, message) is used only to handle that complaint.` | **Chốt VN — QĐ 49** (`LEGAL-REVIEW.md` R25, `AC-57`). Bản EN do Writer soạn khớp từng vế, Duy duyệt theo AC-02. Cấm viết "không thu thập gì" / "collects nothing" |

---

## 6. Cảnh báo lưu trữ — trung thực, không dùng chữ "lưu vĩnh viễn"

Hiện **chỉ** cho tab iOS có `persist() = false` và đã có tiến độ. Khi `true` thì vẫn nhắc sao lưu (PRODUCT-BRIEF §Kiến trúc).

**Ba chuỗi dưới là chữ của cổng ra mắt (QĐ 45, AC-83):** không ra mắt khi thiếu chuỗi nào. Câu thứ ba của dòng `false` phụ thuộc biến thể link/mã ⇒ cổng ra mắt cũng chờ phép đo iPhone/Android.

| Khi nào | VN | EN |
|---|---|---|
| `persist() = false`, đã có tiến độ | **Tiến độ của bạn chỉ nằm trong trình duyệt này, trên máy này.** Safari có thể tự xoá nó nếu bạn dùng Safari 7 ngày mà không mở trang này. Gửi link tiến độ cho chính bạn để lấy lại khi cần. | **Your progress lives only in this browser, on this device.** Safari may erase it if you use Safari for 7 days without opening this site. Send yourself a progress link so you can get it back. |
| `persist() = true` | Trình duyệt đang giữ tiến độ của bạn, nhưng nó vẫn có thể mất khi máy đầy bộ nhớ hoặc khi bạn xoá dữ liệu trình duyệt. Thỉnh thoảng gửi link tiến độ cho chính bạn. | Your browser is keeping your progress, but it can still be lost if storage runs low or browsing data is cleared. Send yourself a progress link now and then. |
| Footer, luôn hiện | Không tài khoản. Tiến độ nằm trên máy bạn; Where Money Sleeps không giữ bản sao nào. | No account. Your progress stays on your device; Where Money Sleeps keeps no copy. |

**Kiểm từng câu với nguồn:**
- "7 ngày **dùng Safari**", không viết "7 ngày" trống trơn: nguồn là WebKit, Wilander 2020-03-24, trích trong `../../../docs/lessons.md` §Nền tảng.
- "Không giữ bản sao" đúng với quyết định 9: bộ đếm chỉ cộng số, không chứa tiến độ.
- Chủ ngữ là "Where Money Sleeps", không phải "chúng tôi", vì đây là site của một người. **⚠ X4.**
- Chữ "link" phụ thuộc biến thể A hay B. **BLOCKED — chờ đo iPhone/Android.**

---

## 7. Xung đột và chỗ cần Duy xử (Writer không tự quyết)

| # | Chỗ | Mâu thuẫn | Khuyến nghị của Writer |
|---|---|---|---|
| **X1** | Quyết định 6 *"không trang nào trộn ngôn ngữ"* đặt cạnh (a) quy ước S0 viết "Nợ (Debit)", và (b) dòng thông báo "Bài này chưa có bản tiếng Anh" | (a) đặt chữ EN vào giữa trang VN. (b) Nếu dòng thông báo viết bằng VN thì người chỉ đọc EN không đọc được. Nếu viết bằng EN thì trang VN có trộn ngôn ngữ. | (a) **Đóng — QĐ 20:** thuật ngữ chuyên ngành EN trong dòng không tính là trộn; viết `Debit`, không `Nợ (Debit)`. (b) **Đóng — QĐ 43(b):** dòng thông báo song ngữ, ngoại lệ có tên của AC-05. |
| X2 | Glossary "theo TT 99/2025" (quyết định 8) đặt cạnh các bài về **sổ của ngân hàng** (GĐ02, ví dụ tiền gửi là khoản ngân hàng nợ bạn) | TT 99 là chế độ kế toán cho **doanh nghiệp**. Tên tài khoản phía ngân hàng thuộc hệ thống tài khoản riêng của tổ chức tín dụng, và S0 không quyết nguồn nào cho phần này. | **TBD — cần xác minh bằng** agent kế toán (K3, QĐ 36), kèm văn bản NHNN hiện hành; Duy ký. Trong lúc chờ, bài chỉ mô tả bằng lời ("khoản ngân hàng nợ bạn"), không ghi số hiệu tài khoản ngân hàng. |
| X3 | ONE-PAGER §2 *"không thấy mình đang học kế toán"* đặt cạnh việc tagline phải giải nghĩa | Tagline rõ nhất (T5) là tagline nói chữ "kế toán". | **Đóng — QĐ 22: T1.** |
| X4 | Tên và chủ ngữ | S0 không quyết (a) trang VN có dịch tên không, và (b) site tự xưng là gì. | (a) **Không dịch tên.** (b) Dùng "Where Money Sleeps", không dùng "chúng tôi". Đây là mặc định của Writer; S2 chỉnh được. |

**Không thấy quyết định S0 nào không viết được thành spec.** X1 (a) đã có phạm vi chữ "trộn" (QĐ 20); X1 (b) đóng (QĐ 43b).

---

## Chưa xác minh được

| Điều | Cách xác minh |
|---|---|
| Tên tài khoản TT 99/2025 ở §3 | Mới khớp bản chép thứ cấp (12/12, kiểm phía tác giả). Agent K2 phán tối đa "KHỚP NGUỒN THỨ CẤP" (QĐ 37). **BLOCKED — chờ Phụ lục II chính thức** cho bài GĐ01; lối vào không bị chặn. |
| Bản dịch EN của tên tài khoản | Không có bản EN chính thức. Agent kế toán soát phần nghĩa (K3); Duy ký phần nghĩa và duyệt phần chữ (QĐ 36). |
| Người đọc có hiểu câu W2 ("một agent AI soát") là máy soát, không phải người có chuyên môn không | Chưa đo. Hỏi thêm ở buổi 5 người (W2 đã chốt hiện, QĐ 41) |
| Tin báo lương của ngân hàng VN có thật sự in chữ "ghi có" không (T1 và quy tắc 1 dựa vào chuyện này) | Duy chụp 3 tin báo biến động số dư thật, từ 3 ngân hàng khác nhau |
| Người đọc có chạm vào thuật ngữ không (§2) | Buổi quan sát 5 người đọc bài 1 |
| Tagline có vừa một dòng trên màn hình 360px không | Mockup ở S2 |
| ~~Đặt dòng định nghĩa (phương án C) vào thì bài còn trong mức 5–8 phút không~~ | N/A — because phương án C bị loại bởi QĐ 16 (2026-10-24) |
| Cách người đọc EN hiểu "ledger" và "credit alert" | Chưa có người đọc EN nào để thử. **Người đọc EN là ai, S0 chưa định nghĩa.** |
| Hiệu lực pháp lý của dòng minh bạch AI | Thuộc phòng Legal (LEGAL-REVIEW.md) |
| "72 giờ" trên trang khiếu nại có ngắn hơn hạn của NĐ 17/2023 không | NĐ 17/2023 Đ.114 chưa xác minh (DECISIONS-QUEUE Q-18). Luật đặt hạn ngắn hơn ⇒ đổi chuỗi §5 |
| Người đọc có hiểu thẻ `Debit · bên Nợ` mà không cần thấy `Nợ` trong dòng không (QĐ 20) | Buổi 5 người, cùng lúc với phép thử mở tại chỗ (QĐ 17) |
| Giọng văn của chính Duy (docs/VOICE-PROFILE.md) | Chưa có mẫu. Chạy `ecc:brand-voice` khi Duy đưa 5–20 bài viết thật |

Same vendor, same priors — no external verifier ran.

## Đổi ở vòng sửa 2026-10-24

Nguồn: review S1 vòng 1 (falsify B4, N12–N13; consistency N1, N2), T2 Design câu 1, PRD K3/K4 và câu #2, #7, #11, QĐ 16.

| # | Chỗ | Bản đầu | Bây giờ |
|---|---|---|---|
| 1 | TL;DR · §2 | Khuyến nghị C (lần đầu mỗi bài **hiện ngay**) | Rút lại vì trái QĐ 16 (chạm mới hiện). Cột C gạch, ghi LOẠI. Bỏ đoạn "Đánh đổi thật" của C. Thêm bảng câu (a) đơn vị "lần đầu", (b) dạng chạm, trỏ tới `RESEARCH-GLOSSARY-UX.md` |
| 2 | §5 nguyên tắc đặt tên | "`sync_link_created` vẫn giữ nguyên" | `sync_created{method}` theo TRACKING-PLAN, ghi đang chờ Duy |
| 3 | §3 dạng hiển thị VN · §7 X1 | Lần đầu `Nợ (Debit)` trong dòng; X1 khuyến nghị coi là ngoại lệ có tên | Nêu cả hai lập trường (WRITER/research giữ · PRD #7 bỏ khỏi dòng chữ vì QĐ 6). Writer không chọn |
| 4 | §2 · §3 | "Lần đầu" ngầm tính theo bài | Nêu đơn vị bài (WRITER) và mục H2 (research/PRD). Đánh dấu mọi "lần đầu" trong file phụ thuộc câu này |
| 5 | §5 nhãn tự khai | `Chọn chỗ bạn đã học tới` / `Pick up where you left off` (ngầm theo bài; EN đọc như "tiếp tục", dễ lẫn với Khôi phục) | Hai biến thể theo giai đoạn / theo bài, chọn theo định nghĩa "tự khai" chưa chốt |
| 6 | §3 dạng hiển thị EN · Chưa xác minh | "popover hoặc dòng định nghĩa"; hàng bấm giờ phương án C | "thẻ chú thích chạm"; hàng bấm giờ C ghi N/A |

**→ Duy tạo ở vòng này (để TRIAGE xếp số và gộp với PRD):**
1. Đánh dấu thuật ngữ ở lần đầu mỗi bài hay mỗi mục H2 (§2 a) — trùng PRD #11a.
2. Dạng chạm: mở tại chỗ hay dạng phủ (§2 b) — trùng PRD #11b.
3. `Nợ (Debit)` trong dòng chữ trang VI: giữ hay bỏ (§3, X1) — trùng PRD #7.
4. Tên event `sync_created{method}` thay `sync_link_created` (§5) — trùng PRD #2.
5. "Tự khai" đánh dấu theo giai đoạn hay theo bài (§5) — chưa có số trong PRD (review B4, T3 Δ13).

**Chưa sửa ở vòng này** (ngoài 5 việc được giao; Writer không tự sửa):
- Review N12: ví dụ "✅ Đúng" của quy tắc giọng 1 (§1) đặt "điện thoại báo +10tr" cạnh "ngân hàng nợ bạn" rồi gọi là hai dòng ghi — dạy sai bút toán kép.
- Review N13 / consistency N7: ví dụ EN đúng của quy tắc 4 chứa `easy`, từ nằm trong danh sách cấm; `chắc chắn` bắt nhầm "chưa chắc chắn".
- Legal T2: Writer phải khai `based_on` cho mọi section (LEGAL-REVIEW §A.1).

Same vendor, same priors — no external verifier ran.

## Đổi theo QĐ 17–35 (2026-10-24)

Nguồn: PRODUCT-BRIEF §Quyết định của Duy, QĐ 17, 19, 20, 21, 22, 23, 25, 34, 35 (Duy chốt qua DECISIONS-QUEUE §"Câu trả lời của Duy"). Năm dòng "→ Duy tạo ở vòng này" của mục trên đã đóng: 1 ⇒ QĐ 19 · 2 ⇒ QĐ 17 · 3 ⇒ QĐ 20 · 4 ⇒ QĐ 25 · 5 ⇒ QĐ 23.

| # | Chỗ | Trước | Bây giờ | QĐ |
|---|---|---|---|---|
| 1 | TL;DR | Hai câu chú thích còn mở; "viết hoa Nợ/Có"; tagline chờ chốt; 5 dòng → Duy | Ghi đã chốt; thêm dòng chuỗi mới; 3 dòng → Duy mới | 17, 19, 20, 22, 34, 35 |
| 2 | §2 | Bảng "còn mở" (a) đơn vị lần đầu, (b) dạng chạm + 2 dòng → Duy | Bảng "đã chốt": mỗi mục H2, mở tại chỗ. Mọi "lần đầu" trong file tính theo H2 | 17, 19 |
| 3 | §2 thẻ chú thích | Không có | Nhãn thẻ = `en.term` · `vi.term` · `vi.short` (ví dụ `Debit · bên Nợ`) | 20 |
| 4 | §2 quy tắc chung | "chú thích trước đó trong cùng bài"; máy chỉ bắt thuật ngữ đã có trong danh sách | "cùng mục H2"; mô tả phép kiểm FAIL (EN) / cảnh báo (VN) | 19, 21 |
| 5 | §1 ví dụ giọng văn | `Bút toán kép`, dòng **Có** | `Double-entry`, `Credit`/`Debit` trong dòng VN; thêm đoạn "Thuật ngữ trong bản VN" | 20 |
| 6 | §1 ví dụ quy tắc 1 | Gọi "+10tr trên điện thoại" và "ngân hàng nợ bạn" là hai dòng ghi (review N12: dạy sai double-entry) | Hai dòng đều nằm trong sổ ngân hàng: Credit tài khoản của bạn, Debit một tài khoản khác. **Sửa vì đang viết lại đúng câu này; kế toán vẫn phải soát** | 20 (+ N12) |
| 7 | §1 ví dụ quy tắc 4 EN | `the easy one to get wrong` (chứa chữ cấm `easy`, review N13) | `where most people slip`. **Sửa vì đang viết lại ví dụ** | 20 (+ N13) |
| 8 | §3 hai nghĩa "nợ" | `Nợ/Có` viết hoa trong dòng = bên bút toán | `Debit/Credit` trong dòng; `Nợ/Có` hoa chỉ trong thẻ; "nợ" thường = debt | 20 |
| 9 | §3 ranh giới `keep_en` | Không có | Mặc định Writer: thuật ngữ EN chuẩn giữ EN; tên tài khoản TT 99, chữ tin báo, tên riêng giữ VN | 20, 21 |
| 10 | §3 dạng hiển thị VN | Hai lập trường, → Duy | `Debit` trong dòng, mọi lần | 20 |
| 11 | §3 trường glossary | Không có `keep_en` | Thêm `keep_en` | 20 |
| 12 | §4 tagline | "Duy chốt" | Chốt T1, nguyên văn VN/EN | 22 |
| 13 | §5 tên event sync | "Đang chờ Duy", → Duy | `sync_created{method}`, `method` ∈ {`link`,`code`} | 25 |
| 14 | §5 nhãn tự khai | Hai biến thể + → Duy | Một nhãn theo giai đoạn | 23 |
| 15 | §5 dòng AI | Một chuỗi, `<tên>` | Hai chuỗi (có/không `ai_assisted`), định danh `⟨…⟩` **để trống** | 34 |
| 16 | §5 trang khiếu nại | Không có | Chuỗi VN/EN "gỡ tạm trong 72 giờ", hộp thư `⟨…⟩` **để trống** | 35 |
| 17 | §7 X1, X3 | X1 chờ Duy cả (a)(b); X3 chờ chốt | X1 (a) đóng, (b) → Duy; X3 đóng | 20, 22 |
| 18 | Chưa xác minh | — | Thêm: 72 giờ vs NĐ 17/2023; người đọc hiểu thẻ `Debit · bên Nợ` không | 20, 35 |

**Không đổi:** frontmatter (`status: fail`, `blocked_on`) · §6 cảnh báo lưu trữ (vẫn chờ đo iPhone/Android) · danh sách chữ cấm · Legal T2 `based_on` (vẫn chưa sửa, ngoài việc được giao).

**→ Duy mới ở vòng này:**
1. **Ranh giới `keep_en` vs tagline T1.** Mặc định Writer viết `ledger` / `double-entry` trong bài (QĐ 20), nhưng T1 đã chốt dùng "sổ cái" trên header (QĐ 22). Giữ cả hai (header VN, bài EN), hay bài cũng viết "sổ cái"? Kèm: Duy nhận danh sách mặc định ở §3 hay sửa.
2. **Dòng "Bài này chưa có bản tiếng Anh" (X1 b).** Writer khuyến nghị song ngữ, nhưng QĐ 20 nói chữ giao diện cùng một ngôn ngữ. Song ngữ là ngoại lệ có tên, hay chỉ VN?
3. **Chữ VN trên trang EN** (`ghi có (credit alert)`, `vi.term` trong thẻ). QĐ 20 chỉ định nghĩa "trộn" cho trang VI. Áp ngược cho trang EN không?

Định danh dòng AI (QĐ 34.2) và hộp thư (QĐ 35) **không phải câu mới**: đã treo, chờ hợp đồng Ringkas.

Same vendor, same priors — no external verifier ran.

## Đổi vòng sửa 2 (2026-10-24)

Nguồn: review S1 sau QĐ 17–35 (M8, §4(b), dòng QĐ 22, M9 "câu W1 chưa vào hàng đợi") · PRD "Giọng văn: WRITER §3 hết căn cứ" · PRODUCT-BRIEF QĐ 20, 36, 37.

| # | Chỗ | Trước | Bây giờ | QĐ |
|---|---|---|---|---|
| 1 | TL;DR · đầu file | "BLOCKED cho tới khi người kế toán ký" · "Chưa qua kế toán" | Agent `ke-toan-reviewer` soát, Duy ký; tên tài khoản tối đa "KHỚP NGUỒN THỨ CẤP"; GĐ01 chờ Phụ lục II chính thức | 36, 37 |
| 2 | §3 dòng "Hai nghĩa của nợ" | Viết như một quy ước viết hoa (`Nợ/Có` hoa chỉ còn trong thẻ) | Viết lại theo QĐ 20: bên bút toán = `Debit`/`Credit` trong dòng; không dạng VN nào của "bên" trong dòng; "nợ" = debt; `bên Nợ`/`bên Có` chỉ ở `vi.term` trong thẻ | 20 |
| 3 | §3 Duyệt | `reviewed_by` = người kế toán; BLOCKED chờ tên người | `reviewed_by` VN `soát: agent kế toán (AI) · ký: Duy` · EN `checked by: AI accounting agent · signed off by: Duy`; danh sách chữ cấm cho chuỗi soát; `reviewed_at` = ngày Duy ký | 36 |
| 4 | §3 Tên tài khoản · danh sách 12 TK | "kế toán phải đối chiếu văn bản gốc" | Đối chiếu với bản chép thứ cấp, phán tối đa "KHỚP NGUỒN THỨ CẤP"; kết quả so nhanh phía tác giả 12/12 khớp chữ (7 hai nguồn, 5 một nguồn) | 37 |
| 5 | §5 hai dòng AI | Không ràng buộc ⟨…⟩ | ⟨…⟩ chỉ là định danh Duy, không gợi tới người kế toán | 36 |
| 6 | §5 dòng mới | — | "Dòng soát kế toán" — đề xuất VN/EN, **chưa chốt**, → Duy W2 | 36 |
| 7 | §7 X2 · Chưa xác minh | "người kế toán" | Agent kế toán (K2/K3) + Duy ký; thêm dòng "người đọc có hiểu agent là máy không" | 36, 37 |
| 8 | §3 ranh giới `keep_en` | "→ Duy (dòng 1 cuối file)" | "→ Duy W1"; `ledger` giữ EN tới khi W1 có câu trả lời | 20, 22 |

**Chênh với chữ được giao:** chuỗi QĐ 36 được giao là `soát: agent kế toán · ký: Duy`. Writer thêm "(AI)" vì mục tiêu của cùng yêu cầu là "không gợi có người kế toán thật". PM/Duy bác thì bỏ "(AI)"; đổi một chuỗi, không đổi luật.

**Không đổi:** frontmatter (`status: fail`; `blocked_on` vẫn ghi `ke-toan-co-ten-bam-gio`, đã lỗi thời theo QĐ 36. Luật sửa giữ frontmatter, review M8 đã đưa lên Duy) · §6 · danh sách chữ cấm · Legal T2 `based_on` · cờ `ai_assisted` cho bản EN (review dòng QĐ 34, gắn N5, ngoài việc được giao).

**Cho PM, không phải câu mới:** chuỗi `reviewed_by` ở §3 va với AC-21 (cấm trường "duyệt bởi" là một model). Writer tách "soát" (agent) khỏi "ký" (Duy) để chuỗi không nói agent duyệt, nhưng AC-21 thuộc ACCEPTANCE, nằm trong M8.

**→ Duy mới ở vòng này:**

**W1 — Trong bài VN, "ledger" viết là `ledger` hay "sổ cái"?** (thay dòng 1 của "→ Duy mới" ở mục trên)
Vì sao bây giờ: chặn mục glossary `ledger` (`keep_en` true hay false) và mọi bài GĐ01 nói về sổ.

| Cách | Được gì | Mất gì | Rủi ro |
|---|---|---|---|
| A. Giữ cả hai: header "sổ cái" (T1), bài `ledger` (`keep_en`) | Đúng chữ cả QĐ 20 lẫn QĐ 22; một luật đều cho mọi thuật ngữ có tên EN chuẩn | Một thứ mang hai tên: header hứa "sổ cái", bài nói `ledger` | Người đọc không nối hai chữ; chỉ có thẻ chú thích (`ledger · sổ cái`) bắc cầu, và tỉ lệ chạm thẻ chưa đo |
| B. Bài cũng viết "sổ cái"; `ledger` rời `keep_en`, `en.term` vẫn là `ledger` trong thẻ | Một tên từ header tới cuối bài; câu kết "nối lại chuyện đầu bài" (quy tắc giọng 5) trả đúng lời hứa của tagline | Ranh giới `keep_en` có một ngoại lệ; phải viết nó ra | Tiền lệ: thuật ngữ khác (`double-entry`…) cũng bị đòi chuyển sang VN |
| ~~C. Sửa tagline thành `ledger`~~ | — | Trái QĐ 22 ("nguyên văn, không sửa chữ") | Loại |

**Khuyến nghị Writer: B.** Căn cứ: T1 là thứ người đọc thấy đầu tiên và đã khoá nguyên văn (QĐ 22), còn `ledger` nằm trong `keep_en` chỉ vì **mặc định của Writer**, không phải vì QĐ 20 nêu tên nó (QĐ 20 nêu Debit, Credit, accrual, APR). Đổi mặc định của Writer không lật quyết định nào của Duy.
**Đánh đổi thật:** sự nhất quán giữa header và bài, đổi lấy một luật `keep_en` không còn đều.
**Nếu sai:** đảo được trước ra mắt bằng một cờ trên một mục glossary; sau ra mắt chỉ tốn sửa chữ trong bài đã đăng.
**Câu hỏi đóng:** Anh chọn B (bài viết "sổ cái", `ledger` chỉ trong thẻ) hay A (giữ `ledger` trong bài)?

**W2 — Có hiện dòng "soát kế toán" trên trang của mục có con số / tên tài khoản không?**
Vì sao bây giờ: §4(b) của review S1 là BLOCKER — dòng "duyệt bởi ⟨…⟩" một mình có thể bị hiểu là có người kế toán soát số APR/lãi suất.

| Cách | Được gì | Mất gì | Rủi ro |
|---|---|---|---|
| A. Hiện: `Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt.` | Nói thẳng ai soát gì; gỡ cách hiểu "có người kế toán" | Thêm một dòng trên mỗi mục có số | Nói công khai việc soát bằng AI; câu chữ cần Legal (L14, Luật AI 134/2025 chưa đọc gốc) |
| B. Không hiện; chỉ dòng AI của QĐ 34 | Trang gọn | Người đọc không biết số do ai soát | Người đọc tự suy ra "duyệt" = người có chuyên môn — đúng rủi ro §4(b) |

**Khuyến nghị Writer: A.** Căn cứ: QĐ 36 ghi rõ phần đáng tin là K1/K2 và Duy vẫn ký; nói đúng điều đó là cách duy nhất không để người đọc tự điền "người kế toán". ⟨…⟩ vẫn để trống theo QĐ 34.2.
**Đánh đổi thật:** một dòng chữ lộ ra rằng không có người kế toán, đổi lấy việc không ai hiểu nhầm là có.
**Nếu sai:** gỡ một chuỗi trước ra mắt, không tốn gì; sau ra mắt, gỡ đi trông như che giấu.
**Câu hỏi đóng:** Anh có muốn hiện dòng soát kế toán (A) trên mục có con số không?

Same vendor, same priors — no external verifier ran.

## Đổi theo QĐ 38–51 (2026-10-25)

Nguồn: PRODUCT-BRIEF §Quyết định của Duy, QĐ 41–45 (Duy nhận theo lô mọi khuyến nghị của DECISIONS-QUEUE Q-26…Q-30). QĐ 38–40, 46–51 không chạm file này. **W1 ⇒ QĐ 44 · W2 ⇒ QĐ 41**; hai dòng "→ Duy mới" số 2, 3 của mục "Đổi theo QĐ 17–35" ⇒ QĐ 43(b), 43(c).

| # | Chỗ | Trước | Bây giờ | QĐ |
|---|---|---|---|---|
| 1 | TL;DR | 4 câu → Duy (W1, W2, dòng "chưa có EN", chữ VN trên trang EN) | Đã đóng; thêm ngoại lệ "sổ cái", W2, dòng song ngữ, cổng ra mắt §6 | 41–45 |
| 2 | §3 Duyệt · trường tối thiểu | `reviewed_by` = `soát: agent kế toán (AI) · ký: Duy`; cấm `kế toán viên`, `chuyên gia kế toán`, `accountant`, `CPA` | `reviewed_by` = chỉ người ký; agent ở trường riêng (tên: S3); máy cấm `kế toán` · `accountant` · `chuyên gia` · `expert` trong `reviewed_by` + dòng minh bạch, không áp thân bài. `CPA`, "duyệt" gắn agent: giữ làm mặc định Writer, người bắt | 41 |
| 3 | §5 dòng soát | "Đề xuất, chưa chốt", → Duy W2 | Câu W2 VN/EN **chốt**, nguyên văn; đổi nhãn nội bộ "Dòng soát kế toán" → "Dòng soát công khai" | 41 |
| 4 | §5 dòng AI | Cờ `ai_assisted` theo "mục" (hạt chưa rõ) | Theo bài / bộ card / bản EN; bài lai ⇒ cả bài mang cờ; bản EN luôn `true` | 42 |
| 5 | §1 thuật ngữ VN · §3 ranh giới | Chỉ `keep_en`; tên riêng xếp cột "Giữ VN" | Thêm ngoại lệ (a) danh sách tên riêng tách khỏi glossary, (b) dòng song ngữ; tên riêng ra khỏi ranh giới `keep_en` | 43a, 43b |
| 6 | §5 dòng "chưa có bản EN" · §7 X1(b) | ⚠ X1 → Duy | Song ngữ trên trang VI, ngoại lệ có tên; X1(b) đóng | 43b |
| 7 | §1 từ riêng VN · §3 dạng EN · trường tối thiểu | → Duy (dòng 3) | Chữ VN trên trang EN chỉ hợp lệ khi là mục glossary được đánh dấu (cờ mới, tên: S3); `vi.term` trong thẻ miễn | 43c |
| 8 | §3 ranh giới `keep_en` · §2 thẻ | `ledger` trong "Giữ EN" chờ W1 | `ledger` rời `keep_en`; bài VN viết "sổ cái"; nhãn thẻ mục `keep_en: false` = `vi.term · en.term` (`sổ cái · ledger`, mặc định Writer, S2 chỉnh được) | 44 |
| 9 | §6 | Không nói cổng ra mắt | Ba chuỗi là chữ của cổng ra mắt (AC-83) | 45 |
| 10 | Chưa xác minh | "nếu W2 chọn hiện" | W2 đã chốt; vẫn phải đo người đọc hiểu "agent AI" là máy | 41 |

**Hết hiệu lực:** đoạn "Chênh với chữ được giao" (thêm "(AI)") của vòng sửa 2 — chuỗi đó bị bỏ theo QĐ 41. Hai khối câu hỏi W1, W2 ở trên giữ lại để giữ lý do (quy tắc 14).

**Không đổi:** frontmatter (`status: fail`, `blocked_on` — 3 điều kiện của Duy chưa xong) · danh sách chữ cấm §1 · ví dụ giọng văn §1 · Legal T2 `based_on`.

**Đã đóng và bàn giao cho S2 / S3 (cập nhật 2026-11-07 sau review kiểm chéo S1):**
1. **Ghép dòng W2 với dòng AI của QĐ 34:** bố cục 1 dòng hay 2 dòng và vị trí đặt ngày trên trang bài/bộ card thuộc thiết kế bề mặt ở **S2** (`DESIGN-BRIEF` / mockup), giữ nguyên chữ đã chốt ở §5.
2. **Hạt của dòng W2:** đồng bộ theo `AC-86` và `LEGAL-REVIEW.md` R20 — câu W2 hiện trên mọi mục (section/bài/bộ card) thuộc phạm vi QĐ 30 (có trường báo cáo soát của agent khác rỗng theo `AC-03`/`AC-21`); mục có con số ngoài phạm vi QĐ 30 (không có báo cáo agent) không hiện câu W2.
3. **Giá trị trường agent (`ke-toan-reviewer`):** `AC-86` đã khoá trường nội bộ ghi tên agent khỏi HTML hiển thị để chuỗi không dấu `ke-toan` không lọt ra trang.
4. **Hai danh sách tên riêng:** S3 đặt tên trường tách biệt — `proper_nouns_allowlist` cho ngoại lệ QĐ 43(a) (`AC-05`) và `hermanson_entities_lint` cho lint nguồn CC BY của Legal §A.1 (`AC-45`).
5. **`VietQR`, `NAPAS`:** đã xếp vào glossary với `keep_en: true` ở §3 (có thẻ chú thích vì là khái niệm được dạy), không nằm trong `proper_nouns_allowlist`.
6. **Ví dụ giọng văn §1 (quy tắc 1, 5):** đã đổi `"sổ của ngân hàng"` → `"sổ cái của ngân hàng"` khớp QĐ 44; bài mẫu thật đã dựng tại `SAMPLE-LESSON-01.md` và qua `ke-toan-reviewer` (`SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`).
7. **Cổng ra mắt §6:** chờ kết quả đo iPhone/Android (điều kiện 1 của `blocked_on`) để chọn biến thể chữ "gửi link" hay "sao chép mã".

Same vendor, same priors — no external verifier ran.
