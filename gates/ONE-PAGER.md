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
