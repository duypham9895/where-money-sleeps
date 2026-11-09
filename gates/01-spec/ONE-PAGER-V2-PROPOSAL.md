---
status: "approved — QĐ 50 (2026-10-25), đã áp vào gates/ONE-PAGER.md"
stage: 01-spec
date: 2026-10-25
owner: pm
---

# ONE-PAGER v2 — đề xuất cho Q-19

**TL;DR** · đọc khoảng 4 phút
- **QĐ 50 (2026-10-25): Duy đã duyệt TRƯỚC** bản cập nhật theo QĐ 1–51, theo khuyến nghị, trước khi thấy chữ cuối. PM đã chép nguyên khối §A vào `gates/ONE-PAGER.md` ngày 2026-10-25. **Duy nên đọc lại §A** — đây là lần đầu chữ này tới tay anh.
- **Giữ nguyên chữ cả 6 câu UNDERSTOOD đang trích** ⇒ không UNDERSTOOD nào phải sửa (kiểm bằng `grep -F`, §C).
- 24 chỗ đổi so với ONE-PAGER cũ, mỗi chỗ có số quyết định (§B). QĐ 36 (agent kế toán) giờ nằm trong phạm vi được duyệt (QĐ 50 = "theo QĐ 1–51").
- Không số nào mới. §4 **không đặt ngưỡng** — chỉ ghi khi nào, ai đặt, và đặt trên số nào còn → Duy.

## A. Toàn văn ONE-PAGER v2

```markdown
---
owner: Duy
freshness: 2026-10-25
status: "approved — QĐ 50, 2026-10-25, duyệt trước theo khuyến nghị; Duy nên đọc lại bản này"
---

# Where Money Sleeps — MỘT trang

> Duy **DUYỆT và SỞ HỮU** trang này. Mọi stage phải trích nguyên văn được từ đây.
> Quy tắc 11: file này **cũ hơn `PRD.md` là lỗi CHẶN**, không phải cảnh báo.
> Nguồn của từng dòng: `gates/00-discovery/PRODUCT-BRIEF.md` §Quyết định của Duy (QĐ 1–51; dòng sau thắng dòng trước).

## 1. Sản phẩm này là gì, cho ai

Một website song ngữ VN/EN dạy người **không có nền tảng tài chính** đi theo đồng tiền:
từ tin nhắn "ghi có" khi lương về, tới bút toán Debit/Credit, tới cách một khoản VietQR thật sự chảy.

Hai tầng trên một bộ nội dung:
- **Lối vào** — khoảng 12–15 bài ngắn, bắt đầu từ dòng tiền của chính người học. Ai cũng đọc được.
- **Lộ trình sâu** — mùa 1 có GĐ01, phần khái niệm GĐ02 và phần người vay GĐ05.

Mỗi bài có quiz card đã được người duyệt, trong đó ít nhất một card trắc nghiệm. Thuật ngữ chuyên ngành giữ nguyên tiếng Anh (Debit, Credit, accrual, APR…);
chạm vào là thẻ chú thích tiếng Việt mở ngay tại chỗ. Đổi VI ⇄ EN bằng một nút gạt.
Có trình đọc PDF cho sách mở (chỉ phần đã soát, §3.1) và cho file của chính người học — file đó không rời máy. Không tài khoản.
Cái tên luôn đi kèm tagline, để không bị đọc thành "gửi tiết kiệm ở đâu":
*"Từ tin báo "ghi có" tới sổ cái: tiền của bạn đi qua những đâu."* · *"From the bank alert to the ledger: where your money actually goes."*
Tiến độ nằm trên máy của chính người học.
Ra mắt khi lối vào đã duyệt xong; GĐ01/02/05 lên dần.
Cổng ra mắt còn gồm: phần sách (trình đọc PDF chạy được với sách host + file riêng, Hermanson đã che theo §3.1, trang sách + thẻ sách);
cảnh báo lưu trữ `persist()` trước khi trình duyệt xoá tiến độ; và workflow pháp lý cho bộ đếm (L13) + hộp thư khiếu nại (L18) chạy xong, Duy ký kết luận, trước S5.

## 2. Cảm giác muốn tạo ra

**"À, hoá ra tiền của mình đi như thế."**

Người học không thấy mình đang học kế toán. Họ thấy mình đang hiểu ra chuyện vẫn xảy ra với
chính họ mỗi tuần — và cái tên trả lời câu hỏi đầu tiên: đêm nay, tiền của bạn đang ngủ ở đâu.

## 3. Ba thứ KHÔNG làm

1. **Không host sách không có giấy phép mở.** Không PDF, không bản scan, không ảnh bìa, không card sinh từ sách trả phí.
   Sách mở chỉ host phần đã soát: Hermanson *Accounting Principles* (CC BY 3.0) tr.1–197, che hai đoạn trích tr.113, tr.166
   và bảng B2 tr.117; bảng số liệu công ty thật (dữ kiện) được giữ trong file nhưng không sinh card.
   Card từ Hermanson là card khái niệm, không con số. Sách khuyến nghị còn lại là thẻ do Duy viết, kèm link mua.
2. **Không tư vấn đầu tư.** Không mã chứng khoán, không "nên mua", không bảng lãi suất có tên ngân hàng.
3. **Không đăng thứ chưa ai duyệt.** Không card, không bài, không bản EN nào lên site khi Duy chưa đọc;
   tên tài khoản GĐ01 (TT 99/2025), APR/lãi suất GĐ05, mọi card có con số và đoạn bài mà card đó trích
   còn phải qua agent kế toán `ke-toan-reviewer` trước khi Duy ký. Agent báo sai số học, tên tài khoản hay khái niệm
   thì chặn đăng tới khi sửa và soát lại; phán khác Duy ký được, kèm một dòng lý do.
   Bài GĐ01 có tên tài khoản chính thức chỉ đăng khi có Phụ lục II chính thức của TT 99/2025.
   Trên site, mục có con số hay tên tài khoản ghi rõ: một agent AI soát, một người ký — không gọi agent là kế toán hay chuyên gia.
   Bài, bộ card hay bản EN nào soạn với hỗ trợ AI thì ghi rõ "Soạn với hỗ trợ AI".

## 4. Thành công đo bằng gì

> Tỉ lệ **số lần `lesson_completed` của bài 5 trên bài 1** của lối vào — đếm gộp, không định danh.

"Xong bài" = đã trả lời ít nhất một card trắc nghiệm cuối bài (thẻ lật tự chấm không tính), nên số này đo "đọc + thử", không chỉ "đọc".
Đây là **proxy**, không phải funnel theo từng người: không có ID nên không theo được ai đi tới đâu.
Báo hai số: **chặt** — bài 5 trên bộ storage đã xong bài 1 (`from_start`, tính trên máy) — và **lỏng** — mọi bài 5.
Lỏng trừ chặt đo được phần thổi do người vào thẳng bài giữa từ link chia sẻ; số chặt còn lệch, chủ yếu về phía xẹp
(mất storage, đổi trình duyệt) — lập luận, chưa đo. Người tự khai giai đoạn không được đếm; nút gạt VI ⇄ EN không đếm đôi.
S1 phải định nghĩa cách chống trùng. Cách S1 đề xuất: mỗi bài đếm tối đa một lần trên một bộ storage (`01-spec/TRACKING-PLAN.md` §2).
Bộ đếm tự host, cùng domain, chỉ cộng số, lưu theo ngày; ô dưới 5 lượt không hiện.
Không đặt ngưỡng trước: Duy đặt sau **≥ 4 tuần** ra mắt **và** bài 1 **≥ 100** lượt, từ số thật. S1 chỉ đặt cách đặt.
Đặt ngưỡng trên số chặt hay số lỏng: Duy quyết lúc đặt baseline (Data khuyến nghị số chặt).
```

## B. Diff — ONE-PAGER cũ → v2 → quyết định

| # | Chỗ | Cũ | Mới | QĐ |
|---|---|---|---|---|
| 1 | frontmatter `status` | draft — 14 quyết định S0, Duy chưa duyệt | approved — QĐ 50, duyệt trước; Duy nên đọc lại | 50 |
| 2 | dòng nguồn | §Quyết định của Duy (14/14) | QĐ 1–51; dòng sau thắng dòng trước | 50 · 18 |
| 3 | §1 câu mở | bút toán Nợ/Có | bút toán Debit/Credit | 20 |
| 4 | §1 thuật ngữ | mọi thuật ngữ có chú thích | giữ tiếng Anh; chạm ⇒ chú thích VN mở tại chỗ | 17 · 20 |
| 5 | §1 card | quiz card đã được người duyệt | + ít nhất một card trắc nghiệm mỗi bài | 38 |
| 6 | §1 PDF | cho sách mở và cho file của người học | sách mở *chỉ phần đã soát*; file riêng không rời máy | 4 · 15 |
| 7 | §1 tagline | một tagline giải nghĩa (bắt buộc — Log) | nguyên văn T1, VN + EN | 22 |
| 8 | §1 cổng ra mắt | — | + phần sách: trình đọc PDF, che Hermanson, trang/thẻ sách | 29 |
| 9 | §1 cổng ra mắt | — | + cảnh báo lưu trữ `persist()` | 45 |
| 10 | §1 cổng ra mắt | — | + workflow pháp lý L13 + L18 xong, Duy ký, trước S5 | 51 |
| 11 | §3.1 phạm vi sách | Sách CC BY thì được — sau khi đọc trang bản quyền | chỉ Hermanson tr.1–197 (CC BY **3.0**) | 15 |
| 12 | §3.1 che | — | che tr.113, tr.166 (đoạn trích) + bảng B2 tr.117 | 29 · 46 |
| 13 | §3.1 bảng B3 | — | giữ trong file host, không sinh card | 46 |
| 14 | §3.1 card sách | — | card Hermanson = khái niệm, không con số | 27 |
| 15 | §3.3 người soát | một người kế toán | agent `ke-toan-reviewer`, Duy ký | 36 |
| 16 | §3.3 phạm vi soát | GĐ01 · GĐ05 · card có số | + đoạn bài mà card có số trích | 30 |
| 17 | §3.3 luật ký | — | FAIL số học / tên tài khoản / khái niệm chặn đăng; phán khác ký kèm lý do | 40 |
| 18 | §3.3 Phụ lục II | — | bài GĐ01 có tên tài khoản chính thức chờ Phụ lục II chính thức | 37 |
| 19 | §3.3 dòng soát công khai | — | agent AI soát, người ký; cấm gọi agent là kế toán/chuyên gia | 41 |
| 20 | §3.3 AI | — | "Soạn với hỗ trợ AI" theo bài / bộ card / bản EN | 34.1 · 42 |
| 21 | §4 "xong bài" | — | ≥ 1 card trắc nghiệm cuối bài; thẻ lật không tính | 24 · 38 |
| 22 | §4 hướng lệch | bị thổi lên bởi tự khai, mất storage, nút gạt | hai số chặt/lỏng; lỏng − chặt đo phần thổi; chặt lệch xẹp (lập luận) | 23 · 25b · 39 |
| 23 | §4 chống trùng · bộ đếm | (câu chống trùng giữ nguyên) · chỉ cộng số | + trỏ TRACKING-PLAN §2 · lưu theo ngày, ẩn ô < 5 | 32 |
| 24 | §4 ngưỡng | Ngưỡng do S1 đặt. | Duy đặt sau ≥ 4 tuần **và** bài 1 ≥ 100; đặt trên số nào → Duy | Q-19 (3) · SUCCESS-CRITERIA §2 · 39 |

**Cố ý không đưa vào** (thuộc PRD, không đổi tuyên bố sản phẩm): QĐ 16, 18 (danh sách nhặt/loại), 19, 21, 25, 26, 28, 31, 33, 35, 43, 44, 47, 48, 49.

## C. Sáu câu UNDERSTOOD — giữ nguyên chữ

| Câu | Ở v2 | UNDERSTOOD |
|---|---|---|
| "Không đăng thứ chưa ai duyệt." | §3.3, nguyên dòng | 01-spec · không đổi |
| "Ra mắt khi lối vào đã duyệt xong; GĐ01/02/05 lên dần." | §1, nguyên dòng | 01-spec · không đổi* |
| "S1 phải định nghĩa cách chống trùng." | §4, nguyên dòng | 01-spec · không đổi |
| "Không host sách không có giấy phép mở." | §3.1, nguyên dòng | 00-discovery · không đổi |
| "Tiến độ nằm trên máy của chính người học." | §1, nguyên dòng | 00-discovery · không đổi |
| "Không tư vấn đầu tư." | §3.2, nguyên dòng | 00-discovery · không đổi |

Đã kiểm 2026-10-25: chép khối §A ra file tạm, `grep -F` từng câu ⇒ 6/6 khớp; sau khi ghi `gates/ONE-PAGER.md`, vibe-check [3] chạy lại trên file thật.
\* Câu này vẫn khớp nhưng giờ chỉ là **một phần** cổng ra mắt (QĐ 29, 45, 51 nằm ở câu ngay sau). Thêm câu `<grounding>` thứ hai cho UNDERSTOOD S1 là việc của PM (DECISIONS-QUEUE nhóm C) — chưa làm ở lượt này.

## D. → Duy, và chưa xác minh được

- **Duy duyệt trước khi thấy chữ (QĐ 50).** §A là chữ PM soạn sau quyết định; chưa ai ngoài phiên Claude đọc nó. Chỗ nào Duy không nhận ⇒ thêm dòng QĐ mới, PM sửa lại `gates/ONE-PAGER.md`.
- **Ngưỡng M1 đặt trên số chặt hay lỏng → Duy**, không gấp (SUCCESS-CRITERIA §2 bước 2).
- **Chữ định danh "⟨…⟩ ký duyệt"** (QĐ 34.2, 41) và **công khai hộp thư** (QĐ 35, 49) chờ hợp đồng Ringkas — v2 cố ý không nêu tên người ký.
- **Danh sách bảng B3** (tr.45, 55, 94–95, 170, 185) chỉ từ soát bằng máy, chưa xem bằng mắt (LEGAL-REVIEW). Rủi ro sưu tập dữ liệu khi giữ B3 (L16) đã nhận ở QĐ 51.
- **Phụ lục II chính thức TT 99/2025** chưa có (QĐ 37) ⇒ phần tên tài khoản GĐ01 chưa đăng được; lối vào không bị chặn.
- **vibe-check [2] so thời điểm sửa file**, không so `freshness:` ⇒ mọi lần sửa `PRD.md` sau lần ghi `ONE-PAGER.md` này là FAIL lại.
- Frontmatter file này giữ nguyên theo luật sửa của workflow, nên `status`/`blocked_on` vẫn ghi "chờ Q-19" dù Q-19 đã trả lời (QĐ 50) — đổi hay không → Duy.
- Bản này là của một phiên Claude. Same vendor, same priors — no external verifier ran.

## Đổi theo QĐ 38–51 (2026-10-25)

PM sửa tại chỗ vì file là nháp. Nguồn: `PRODUCT-BRIEF.md` QĐ 37–51 (41–51 Duy nhận theo lô mọi khuyến nghị của `DECISIONS-QUEUE.md`). Frontmatter giữ nguyên. Bản trước (2026-10-24) không có trong git (file chưa track); các chỗ đổi liệt kê dưới đây.

| Chỗ | Bản 2026-10-24 | Bản này | QĐ |
|---|---|---|---|
| TL;DR | "Duy duyệt thì chép… (PM không sửa file đó)"; 17 chỗ đổi; QĐ 36 vượt phạm vi | Đã duyệt trước, PM đã áp, Duy nên đọc lại; 24 chỗ đổi; QĐ 36 trong phạm vi | 50 |
| §A frontmatter · dòng nguồn | `freshness: 2026-10-24` · "QĐ 1–36" · chờ Q-19 | `2026-10-25` · "QĐ 1–51" · approved — QĐ 50 | 50 |
| §A §1 card | — | ít nhất một card trắc nghiệm | 38 |
| §A §1 cổng ra mắt | phần sách | + `persist()` · + workflow L13 + L18 trước S5 | 45 · 51 |
| §A §3.1 | redact tr.113, tr.166 + bảng bên thứ ba "theo quy tắc Legal" (chưa ra) | che tr.113, tr.166, bảng B2 tr.117; giữ B3, không sinh card | 46 |
| §A §3.3 | agent soát, Duy ký; "mục nào" soạn với AI | + luật ký (FAIL chặn) · Phụ lục II chính thức · dòng soát công khai · AI theo bài/bộ card/bản EN | 37 · 40 · 41 · 42 |
| §A §4 | "xong bài" = card cuối bài; "nghiêng về phía thấp" | card trắc nghiệm, thẻ lật không tính; hai số chặt/lỏng, hướng lệch theo SUCCESS-CRITERIA; đặt trên số nào → Duy | 38 · 39 |
| §B | 17 dòng | 24 dòng; danh sách "cố ý không đưa vào" + 43, 44, 47, 48, 49 | 37–51 |
| §D | QĐ 36 vượt phạm vi · N1 treo · quy tắc Legal chưa ra · Q-20 treo | Bỏ bốn dòng đó (QĐ 50, 38, 46, 51 đã trả lời); thêm: duyệt trước, ngưỡng chặt/lỏng, B3 chưa xem bằng mắt, Phụ lục II, frontmatter cũ | 38 · 46 · 50 · 51 |

Same vendor, same priors — no external verifier ran.
