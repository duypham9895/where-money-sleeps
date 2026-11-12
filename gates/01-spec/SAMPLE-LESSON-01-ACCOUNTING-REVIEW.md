# Báo cáo kiểm toán nội dung (Điều kiện 3 trước S1 — QĐ 36, QĐ 37)

```
KẾ TOÁN · where-money-sleeps/gates/01-spec/SAMPLE-LESSON-01.md · 2026-11-07
Tổng: PASS 12 · FAIL 0 · KHỚP NGUỒN THỨ CẤP 6 · UNVERIFIED 0 · FLAG 7
```

> **TL;DR cho Duy & người ký duyệt (ước tính đọc: ~3 phút):**
> - **K1 (Số học — 8/8 `PASS`):** Mọi phép cộng/trừ số dư, tỷ lệ phí `MDR` `2%`, tách thuế GTGT `10%` trên phí ngân hàng, cân bằng ` tổng Debit = tổng Credit` của cả 4 bút toán (sổ ngân hàng lúc nhận lương, sổ doanh nghiệp đêm T+0, sáng T+1, chiều T+1) và toàn bộ con số + `source_quote` trong 4 quiz cards (`L01-C01.v1` .. `L01-C04.v1`) đều khớp tuyệt đối bằng script Python (`0đ` sai lệch).
> - **K2 (Tên tài khoản TT 99/2025/TT-BTC — 6/6 `KHỚP NGUỒN THỨ CẤP`):** Cả 6 tài khoản (`112`, `113`, `133`, `331`, `511`, `642`) trong thân bài, Glossary và Quiz Cards khớp nguyên văn từng ký tự (NFC) với `legal/tt99-phu-luc-ii.secondary.json`. Theo **QĐ 37**, vì repo hiện mới có bản chép thứ cấp (chưa có Phụ lục II bản gốc từ cổng nhà nước), mức phán tối đa của K2 là **`KHỚP NGUỒN THỨ CẤP`** (4 tài khoản `112`, `113`, `133`, `331` có `agreement: "both_match"`; 2 tài khoản `511`, `642` có `agreement: "only_ketoanleanh"` do `xcyber` chỉ trích 50 tài khoản đầu từ `111`→`411`).
> - **K3 (Khái niệm — 3 `PASS`, 3 `FLAG`) & K4 (Góc nhìn người mới 25 tuổi — 1 `PASS`, 4 `FLAG`):** Không có lỗi `FAIL`. Có **7 điểm `FLAG`** (3 vùng xám nghiệp vụ kế toán thực tế và 4 chỗ người mới dễ hiểu nhầm) kèm câu viết lại đề xuất ngay trong bảng dưới đây để Duy và chuyên gia ký quyết định giữ nguyên hay tinh chỉnh trước khi xuất bản.

---

## 1. Bảng tổng hợp kết quả kiểm toán (K1 – K4)

| # | Vị trí (`file:dòng` / `card id`) | Phép kiểm | Phán | Bằng chứng (`code+output` / `URL+nguyên văn`) | Đề xuất sửa / Ghi chú cho người ký |
|---|---|---|---|---|---|
| 1 | `SAMPLE-LESSON-01.md:25,41` (`#h2-tin-bao-ghi-co`) | **K1** (Số học) | **PASS** | Số dư trước lương `2.500.000đ` + lương về `10.000.000đ` = số dư mới `12.500.000đ`. Bút toán sổ cái ngân hàng: `Debit` `10.000.000đ` = `Credit` `10.000.000đ` (Xem mục 2 `[K1.1]`). | Không cần sửa. |
| 2 | `SAMPLE-LESSON-01.md:55,65` (`#h2-vietqr-9-8-trieu`) | **K1** (Số học) | **PASS** | Số dư sau quét QR: `12.500.000đ - 10.000.000đ = 2.500.000đ`. Phí `MDR` `2%`: `10.000.000đ × 2% = 200.000đ`. Tiền thực về sáng T+1: `10.000.000đ - 200.000đ = 9.800.000đ` (Xem mục 2 `[K1.2]`). | Không cần sửa. |
| 3 | `SAMPLE-LESSON-01.md:85-87` (`#h2-so-cai-hai-ben` — Đêm T+0) | **K1** (Số học) | **PASS** | Bút toán T+0: `Debit TK 113` = `10.000.000đ`; `Credit TK 511` = `10.000.000đ`. Tổng `Debit` = Tổng `Credit` = `10.000.000đ` (Xem mục 2 `[K1.3a]`). | Không cần sửa. |
| 4 | `SAMPLE-LESSON-01.md:98-102` (`#h2-so-cai-hai-ben` — Sáng T+1) | **K1** (Số học) | **PASS** | Bút toán sáng T+1: `Debit TK 112` (`9.800.000đ`) + `Debit TK 642` (`200.000đ`) = `10.000.000đ` = `Credit TK 113` (`10.000.000đ`). Số dư `TK 113` sau T+1: `10.000.000đ - 10.000.000đ = 0đ` (Xem mục 2 `[K1.3b]`). | Không cần sửa. |
| 5 | `SAMPLE-LESSON-01.md:116-130` (`#h2-phi-ngan-hang` — Chiều T+1) | **K1** (Số học) | **PASS** | Phí chuyển tiền: `3.000đ` + thuế GTGT `10%` (`3.000đ × 10% = 300đ`) = `3.300đ`. Tổng `Debit`: `TK 331` (`5.000.000đ`) + `TK 642` (`3.000đ`) + `TK 133` (`300đ`) = `5.003.300đ` = `Credit TK 112` (`5.003.300đ`). Số dư cuối ngày `TK 112`: `0đ + 9.800.000đ - 5.003.300đ = 4.796.700đ` (Xem mục 2 `[K1.4]`). | Không cần sửa. |
| 6 | `L01-C01.v1` (`SAMPLE-LESSON-01.md:171-184`) | **K1** (Số học & `source_quote`) | **PASS** | `source_quote` khớp nguyên văn NFC mục `h2-tin-bao-ghi-co`. Mọi con số trong câu hỏi và phương án (`10.000.000đ`, `2.500.000đ`, `12.500.000đ`) đều nằm trong `source_quote` và đúng toán học (Xem mục 2 `[K1.5]`). | Không cần sửa. |
| 7 | `L01-C02.v1` (`SAMPLE-LESSON-01.md:188-204`) | **K1** (Số học & `source_quote`) | **PASS** | `source_quote` khớp nguyên văn NFC mục `h2-so-cai-hai-ben`. Mọi con số (`1`, `10.000.000đ`, `112`, `113`, `2%`, `200.000đ`, `642`, `9.800.000đ`) thuộc `source_quote`. Phản hồi phương án B tính đúng số dư treo `10.000.000đ - 9.800.000đ = 200.000đ` (Xem mục 2 `[K1.3b]`, `[K1.5]`). | Không cần sửa. |
| 8 | `L01-C03.v1` & `L01-C04.v1` (`SAMPLE-LESSON-01.md:208-239`) | **K1** (Số học & `source_quote`) | **PASS** | `source_quote` của cả 2 card khớp nguyên văn NFC văn bản thân bài (sau khi bỏ khối blockquote thẻ chú thích B5 xen giữa các đoạn văn). Mọi con số trong `L01-C03.v1` (`0đ`, `1`, `112`, `133`, `3.000đ`, `3.300đ`, `300đ`, `331`, `4.796.700đ`, `5.000.000đ`, `5.003.300đ`, `642`, `9.800.000đ`) thuộc `source_quote` (Xem mục 2 `[K1.5]`). | Lưu ý cho S3 parser: khi kiểm tự động `source_quote` của `L01-C03.v1` trên Markdown thô, cần strip các dòng blockquote `> **[Thẻ chú thích...` xen giữa đoạn văn trước khi so chuỗi liên tục. |
| 9 | `TK 112` (`SAMPLE-LESSON-01.md:99,104-105,116,154,193,198,200,202,212`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 112 — Tiền gửi không kỳ hạn`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "112"`, `name: "Tiền gửi không kỳ hạn"`, `agreement: "both_match"`, nguồn: `ketoanleanh` & `xcyber`, đọc ngày `2026-10-24`). | Giữ nguyên cách ghi chú nguồn bản chép thứ cấp hiện tại; nâng cấp khi có Phụ lục II bản gốc (QĐ 37). |
| 10 | `TK 113` (`SAMPLE-LESSON-01.md:85,92-93,155`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 113 — Tiền đang chuyển`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "113"`, `name: "Tiền đang chuyển"`, `agreement: "both_match"`, nguồn: `ketoanleanh` & `xcyber`, đọc ngày `2026-10-24`). | Giữ nguyên theo QĐ 37. |
| 11 | `TK 133` (`SAMPLE-LESSON-01.md:124,127-128,156,216,221`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 133 — Thuế GTGT được khấu trừ`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "133"`, `name: "Thuế GTGT được khấu trừ"`, `agreement: "both_match"`, nguồn: `ketoanleanh` & `xcyber`, đọc ngày `2026-10-24`). | Giữ nguyên theo QĐ 37. |
| 12 | `TK 331` (`SAMPLE-LESSON-01.md:116,118-119,157,212`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 331 — Phải trả cho người bán`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "331"`, `name: "Phải trả cho người bán"`, `agreement: "both_match"`, nguồn: `ketoanleanh` & `xcyber`, đọc ngày `2026-10-24`). | Giữ nguyên theo QĐ 37. |
| 13 | `TK 511` (`SAMPLE-LESSON-01.md:86,95-96,158`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 511 — Doanh thu bán hàng và cung cấp dịch vụ`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "511"`, `name: "Doanh thu bán hàng và cung cấp dịch vụ"`, `agreement: "only_ketoanleanh"`, nguồn: `ketoanleanh`, đọc ngày `2026-10-24`). | Chú ý khi ký: `TK 511` nằm ngoài 50 tài khoản đầu của `xcyber` nên hiện mới đối chiếu từ 1 nguồn thứ cấp (`ketoanleanh`). |
| 14 | `TK 642` (`SAMPLE-LESSON-01.md:100,107-108,123,159,194,198,202,215,221`) | **K2** (Tên tài khoản TT 99) | **KHỚP NGUỒN THỨ CẤP** | Bài viết: `TK 642 — Chi phí quản lý doanh nghiệp`. Khớp nguyên văn `legal/tt99-phu-luc-ii.secondary.json` (`code: "642"`, `name: "Chi phí quản lý doanh nghiệp"`, `agreement: "only_ketoanleanh"`, nguồn: `ketoanleanh`, đọc ngày `2026-10-24`). | Chú ý khi ký: `TK 642` mới có 1 nguồn thứ cấp (`ketoanleanh`) trong JSON. |
| 15 | `SAMPLE-LESSON-01.md:25-47,142-148,171-184` | **K3** (Khái niệm) | **PASS** | Chiều ghi `Debit`/`Credit` trên `sổ cái` ngân hàng hoàn toàn chuẩn xác: tiền gửi của khách hàng là nợ phải trả (`liability`) của ngân hàng ⇒ khi khách nhận lương ngân hàng ghi `Credit` (tăng nợ phải trả), khi khách trả tiền ngân hàng ghi `Debit` (giảm nợ phải trả). Giải thích `Debit` ở dòng 47 & 146 nêu rõ "chỉ vị trí cột bên trái, không có nghĩa là mắc nợ". | Không cần sửa. |
| 16 | `SAMPLE-LESSON-01.md:55-74,149-152,231-238` | **K3** (Khái niệm) | **PASS** | Phân biệt chính xác 3 khâu trong thanh toán điện tử qua đơn vị trung gian thanh toán: `authorization` (kiểm tra số dư và khóa/trừ hạn mức ngay lúc quét T+0), `reconciliation` (đối soát dữ liệu giao dịch giữa các sổ độc lập), và `settlement` (chuyển tiền quyết toán thực sự vào T+1 sau khi trừ phí `MDR`). | Không cần sửa. |
| 17 | `SAMPLE-LESSON-01.md:82-87,153` | **K3** (Khái niệm — Vùng xám sư phạm vs thực tế) | **FLAG** | Bài đã rào trước rất rõ ở dòng 82: *(giả định doanh thu `10.000.000đ` là giá chưa tách thuế GTGT đầu ra; cách tách thuế GTGT đầu ra sẽ học ở bài riêng)*. Tuy nhiên, theo VAS 14 & TT 99/2025, khi bán hàng hóa (máy pha cà phê), ngoài bút toán doanh thu (`Debit TK 113 / Credit TK 511, 3331`), kế toán đồng thời phải ghi bút toán giá vốn hàng bán (`Debit TK 632 / Credit TK 156`). Việc lược bỏ giá vốn ở Bài 1 là hợp lý để giữ trọng tâm dòng tiền, nhưng cần ghi rõ đây là lược giản sư phạm. | **Đề xuất sửa (dòng 82):** Mở rộng nhẹ câu trong ngoặc đơn: *(Để tập trung vào đường đi của khoản tiền và phí thanh toán, ví dụ dưới đây chỉ xét bút toán doanh thu với giả định `10.000.000đ` là giá chưa tách thuế GTGT đầu ra, tạm lược qua bút toán giá vốn kho hàng; phần thuế GTGT đầu ra và giá vốn sẽ học ở bài riêng.)* |
| 18 | `SAMPLE-LESSON-01.md:85,92-93,101,155,192-203` | **K3** (Khái niệm — Vùng xám `TK 113` vs `TK 1388`/`131`) | **FLAG** | **Hai cách hiểu trong thực hành kế toán VN (VAS / TT 99/2025):** <br>• *Cách 1 (Bài đang dùng — `TK 113 — Tiền đang chuyển`):* Phổ biến tại chuỗi bán lẻ/F&B với giao dịch thẻ POS/QR cổng thanh toán đã `authorization` và chờ `settlement` T+1, coi lệnh thanh toán đã xác nhận tại cổng như tiền đang trên đường về ngân hàng.<br>• *Cách 2 (Theo kết cấu hẹp của `TK 113` & thực hành kiểm toán):* `TK 113` nguyên gốc phản ánh tiền mặt/séc doanh nghiệp đã nộp hoặc lệnh chuyển tiền từ chính tài khoản doanh nghiệp chờ báo Có; còn khoản tiền khách trả đang nằm tại ví/tài khoản đảm bảo của tổ chức trung gian thanh toán (thu hộ) bản chất là **khoản phải thu bên thứ ba**, được hạch toán qua `TK 1388 — Phải thu khác` (hoặc `TK 131` chi tiết cổng thanh toán). | **Đề xuất sửa (dòng 93 — thẻ `TK 113`):** Giữ `TK 113` trong mạch bài cho trực quan ("tiền đang chuyển"), nhưng thêm 1 câu cuối thẻ chú thích dòng 93: *"(Trong thực tế kiểm toán, nhiều doanh nghiệp cũng theo dõi khoản tiền chờ cổng thanh toán quyết toán này trên tài khoản phải thu thu hộ như `TK 1388` hoặc `TK 131` trước khi tiền về `TK 112`)."* |
| 19 | `SAMPLE-LESSON-01.md:98-102,107-108,159,194,198` | **K3** (Khái niệm — Vùng xám `TK 642` vs `TK 641` & thuế GTGT của phí `MDR`) | **FLAG** | Có 2 điểm vùng xám ở bút toán sáng T+1 (dòng 100):<br>1. **Tài khoản chi phí (`TK 642` vs `TK 641`):** Phí chuyển tiền trả nhà cung cấp ở Mục 4 (`3.000đ`) ghi vào `TK 642` là hoàn toàn chuẩn. Nhưng phí `MDR` `200.000đ` ở Mục 3 gắn trực tiếp với giao dịch bán hàng tại quầy: thực tế nhiều doanh nghiệp hạch toán vào `TK 641 — Chi phí bán hàng` (`TK 6417`), dù doanh nghiệp nhỏ hoặc giáo trình nhập môn thường gom chung phí thanh toán vào `TK 642`.<br>2. **Thuế GTGT đầu vào của phí `MDR`:** Dịch vụ trung gian thanh toán chịu thuế GTGT `10%`. Ở Mục 3 bài ghi trọn `200.000đ` vào `TK 642` (chưa tách `TK 133`), trong khi sang Mục 4 lại tách `3.300đ = 3.000đ (TK 642) + 300đ (TK 133)`. | **Đề xuất sửa (dòng 100 & 108):**<br>• Tại dòng 100, thêm chú thích ngắn trong ngoặc: *(giả định `200.000đ` là phí chưa tách thuế GTGT; cách tách thuế GTGT trên phí dịch vụ sẽ xem ngay ở Mục 4)*.<br>• Tại dòng 108 (thẻ `TK 642`), thêm: *(Với phí chiết khấu thanh toán gắn trực tiếp từng đơn bán lẻ như `MDR`, doanh nghiệp cũng có thể hạch toán vào `TK 641 — Chi phí bán hàng`)*. |
| 20 | `SAMPLE-LESSON-01.md:116-130,156-157,208-227` | **K3** (Khái niệm) | **PASS** | Bút toán chiều T+1 hoàn toàn chuẩn xác theo chế độ kế toán doanh nghiệp nộp thuế GTGT theo phương pháp khấu trừ: giảm nợ phải trả người bán (`Debit TK 331: 5.000.000đ`), ghi nhận chi phí dịch vụ chuyển tiền chưa thuế (`Debit TK 642: 3.000đ`), ghi nhận thuế GTGT đầu vào được khấu trừ (`Debit TK 133: 300đ`), và giảm tiền gửi không kỳ hạn (`Credit TK 112: 5.003.300đ`). | Không cần sửa. |
| 21 | `SAMPLE-LESSON-01.md:33,41,99` | **K4** (Người mới 25 tuổi dễ hiểu sai) | **FLAG** | **Điểm dễ "xoắn não" nhất với người mới:** Ở Mục 1 (dòng 41), tiền gửi ngân hàng tăng `+10.000.000đ` thì ghi `Credit`. Sang Mục 3 (dòng 99), tiền gửi ngân hàng (`TK 112`) tăng `+9.800.000đ` lại ghi `Debit`! Người mới chưa quen đổi hệ quy chiếu giữa **sổ cái của Ngân hàng** (tiền khách gửi là Nợ phải trả của ngân hàng) và **sổ cái của Doanh nghiệp Minh** (tiền gửi ngân hàng là Tài sản của Minh) sẽ tưởng bài viết tự mâu thuẫn. | **Đề xuất sửa (dòng 99):** Viết rõ sự đối xứng của hai cuốn sổ: `- Ghi Debit vào TK 112 — Tiền gửi không kỳ hạn: 9.800.000đ (trên điện thoại Minh vẫn nhận tin báo "ghi có" từ sổ của ngân hàng như Mục 1, nhưng trong sổ cái của công ty Minh thì tiền gửi ngân hàng là tài sản của công ty nên tăng lên phải ghi Debit).` |
| 22 | `SAMPLE-LESSON-01.md:51,55,65` | **K4** (Người mới 25 tuổi dễ hiểu sai) | **FLAG** | Ở Việt Nam, người đọc 25 tuổi rất quen quét mã `VietQR` chuyển khoản trực tiếp liên ngân hàng (NAPAS 247) vào tài khoản chủ quán — tiền vào ngay lập tức (T+0) và không bị trừ `MDR` 2%. Mục 2 có anchor `{#h2-vietqr-9-8-trieu}` và viết *"mã QR của đơn vị trung gian thanh toán"*. Người mới dễ đánh đồng mọi mã QR ở quán đều bị giam tiền qua đêm T+1. | **Đề xuất sửa (dòng 55):** Làm rõ ngay trong câu chuyện: *"Minh đưa mã QR cổng thanh toán dành cho cửa hàng (do đơn vị trung gian thanh toán cung cấp, khác với mã QR chuyển khoản trực tiếp vào tài khoản cá nhân)..."* |
| 23 | `SAMPLE-LESSON-01.md:93,155` | **K4** (Người mới 25 tuổi dễ hiểu sai) | **FLAG** | Thẻ chú thích `TK 113` (dòng 93 & 155) viết liền *"các khoản tiền của doanh nghiệp đã nộp hoặc khách đã thanh toán qua trung gian nhưng đến cuối ngày vẫn chưa nhận được giấy báo Có... (danh mục tài khoản theo bản chép Phụ lục II Thông tư 99/2025/TT-BTC)"*. Cách đặt chú thích nguồn ở cuối câu dễ làm người đọc hiểu nhầm rằng Phụ lục II chỉ định nguyên văn cụm "khách đã thanh toán qua trung gian" (trong khi Phụ lục II chỉ quy định số hiệu và tên tài khoản `Tiền đang chuyển`). | **Đề xuất sửa (dòng 93):** Đặt chú thích nguồn ngay sau tên tài khoản: `**TK 113 — Tiền đang chuyển** · Cash in transit *(tên tài khoản theo bản chép Phụ lục II Thông tư 99/2025/TT-BTC)* — Tài khoản tài sản phản ánh...` (áp dụng tương tự cho các thẻ `TK 511`, `TK 112`, `TK 642`, `TK 331`, `TK 133`). |
| 24 | `SAMPLE-LESSON-01.md:121,124,128,156` | **K4** (Người mới 25 tuổi dễ hiểu sai) | **FLAG** | Dòng 121 có ghi *(áp dụng phương pháp khấu trừ thuế GTGT)*, nhưng người 25 tuổi không có nền tảng kế toán không hiểu cụm này nghĩa là gì, nên dễ tưởng mọi quán cà phê / hộ kinh doanh khi chuyển khoản mất `3.300đ` đều phải tách `300đ` vào `TK 133` (thực tế hộ kinh doanh hoặc doanh nghiệp tính thuế GTGT trực tiếp sẽ gộp cả `3.300đ` vào chi phí). | **Đề xuất sửa (dòng 128 — thẻ `TK 133`):** Thêm 1 câu ngắn ở cuối thẻ: *(Chỉ áp dụng với doanh nghiệp nộp thuế GTGT theo phương pháp khấu trừ và có hóa đơn GTGT đầu vào; nếu tính thuế trực tiếp thì toàn bộ `3.300đ` được tính thẳng vào chi phí).* |
| 25 | `SAMPLE-LESSON-01.md:1-246` | **K4** (Ranh giới Luật Chứng khoán — QĐ 30) | **PASS** | Bài mẫu không nhắc tới bất kỳ mã cổ phiếu/chứng khoán nào, không có nội dung mang tính khuyến nghị đầu tư ("nên mua/nên bán"). Cuối trang (dòng 246) có đầy đủ Disclaimer giáo dục theo AC-54 / Legal R20. | Không cần sửa. |

---

## 2. Bằng chứng thực thi script Python cho K1 & K2 (Nguyên văn code và output)

### 2.1. Code Python đã chạy (`python3 -I`)

```python
import json
import re
import unicodedata
from decimal import Decimal

LESSON_PATH = "gates/01-spec/SAMPLE-LESSON-01.md"
JSON_PATH = "legal/tt99-phu-luc-ii.secondary.json"

with open(LESSON_PATH, "r", encoding="utf-8") as f:
    lesson_text = unicodedata.normalize("NFC", f.read())

with open(JSON_PATH, "r", encoding="utf-8") as f:
    tt99_data = json.load(f)

print("=== [K1] KIỂM TRA SỐ HỌC TOÀN BÀI & QUIZ CARDS ===")

# 1. Mục 1 (#h2-tin-bao-ghi-co) + Card L01-C01.v1: Lương về +10.000.000đ
bal_before_salary = Decimal("2500000")
salary_credit = Decimal("10000000")
bal_after_salary = bal_before_salary + salary_credit
bank_entry_1_debit = Decimal("10000000")   # TK thanh toán phía ngân hàng gửi lương chuyển sang
bank_entry_1_credit = Decimal("10000000")  # TK tiền gửi của khách hàng

assert bal_after_salary == Decimal("12500000")
assert bank_entry_1_debit == bank_entry_1_credit == Decimal("10000000")
print(f"[K1.1] Mục 1 (L25, L41) & Card L01-C01.v1 (L175-183): Số dư trước={bal_before_salary:,.0f}đ + Lương Credit={salary_credit:,.0f}đ -> Số dư mới={bal_after_salary:,.0f}đ | Tổng Debit NH={bank_entry_1_debit:,.0f}đ == Tổng Credit NH={bank_entry_1_credit:,.0f}đ -> PASS")

# 2. Mục 2 (#h2-vietqr-9-8-trieu) + Card L01-C04.v1: Quét QR 10.000.000đ & phí MDR 2%
qr_payment = Decimal("10000000")
bal_after_qr = bal_after_salary - qr_payment
mdr_rate = Decimal("0.02")
mdr_fee = qr_payment * mdr_rate
settlement_t1 = qr_payment - mdr_fee

assert bal_after_qr == Decimal("2500000")
assert mdr_fee == Decimal("200000")
assert settlement_t1 == Decimal("9800000")
print(f"[K1.2] Mục 2 (L55, L65) & Card L01-C04.v1 (L235): Số dư sau quét QR={bal_after_salary:,.0f}đ - {qr_payment:,.0f}đ = {bal_after_qr:,.0f}đ | Phí MDR = {qr_payment:,.0f}đ * 2% = {mdr_fee:,.0f}đ | Tiền về T+1 = {qr_payment:,.0f}đ - {mdr_fee:,.0f}đ = {settlement_t1:,.0f}đ -> PASS")

# 3. Mục 3 (#h2-so-cai-hai-ben) + Card L01-C02.v1: Bút toán đêm T+0 và sáng T+1
t0_debit_113 = Decimal("10000000")
t0_credit_511 = Decimal("10000000")
assert t0_debit_113 == t0_credit_511 == Decimal("10000000")
print(f"[K1.3a] Mục 3 Đêm T+0 (L85-87): Debit TK 113={t0_debit_113:,.0f}đ == Credit TK 511={t0_credit_511:,.0f}đ -> PASS")

t1_am_debit_112 = Decimal("9800000")
t1_am_debit_642 = Decimal("200000")
t1_am_total_debit = t1_am_debit_112 + t1_am_debit_642
t1_am_credit_113 = Decimal("10000000")
tk113_bal_after_t1 = t0_debit_113 - t1_am_credit_113
tk113_wrong_b_leftover = t0_debit_113 - Decimal("9800000")

assert t1_am_total_debit == t1_am_credit_113 == Decimal("10000000")
assert tk113_bal_after_t1 == Decimal("0")
assert tk113_wrong_b_leftover == Decimal("200000")
print(f"[K1.3b] Mục 3 Sáng T+1 (L98-102) & Card L01-C02.v1 (L192-203): Tổng Debit (TK 112 {t1_am_debit_112:,.0f}đ + TK 642 {t1_am_debit_642:,.0f}đ) = {t1_am_total_debit:,.0f}đ == Credit TK 113={t1_am_credit_113:,.0f}đ | Số dư TK 113 sau T+1 = {tk113_bal_after_t1:,.0f}đ | Số treo nếu ghi sai như phương án B = {tk113_wrong_b_leftover:,.0f}đ -> PASS")

# 4. Mục 4 (#h2-phi-ngan-hang) + Card L01-C03.v1: Chiều T+1 chuyển khoản trả NCC + phí ngân hàng + thuế GTGT
ap_payment_331 = Decimal("5000000")
bank_fee_ex_vat_642 = Decimal("3000")
vat_rate = Decimal("0.10")
vat_on_fee_133 = bank_fee_ex_vat_642 * vat_rate
total_bank_fee_inc_vat = bank_fee_ex_vat_642 + vat_on_fee_133
t1_pm_total_debit = ap_payment_331 + bank_fee_ex_vat_642 + vat_on_fee_133
t1_pm_credit_112 = Decimal("5003300")

tk112_open_t1 = Decimal("0")
tk112_close_t1 = tk112_open_t1 + t1_am_debit_112 - t1_pm_credit_112

assert vat_on_fee_133 == Decimal("300")
assert total_bank_fee_inc_vat == Decimal("3300")
assert t1_pm_total_debit == t1_pm_credit_112 == Decimal("5003300")
assert tk112_close_t1 == Decimal("4796700")
print(f"[K1.4] Mục 4 Chiều T+1 (L116-130) & Card L01-C03.v1 (L212-226): Phí chưa thuế={bank_fee_ex_vat_642:,.0f}đ + GTGT 10%={vat_on_fee_133:,.0f}đ = {total_bank_fee_inc_vat:,.0f}đ | Tổng Debit (TK 331: {ap_payment_331:,.0f}đ + TK 642: {bank_fee_ex_vat_642:,.0f}đ + TK 133: {vat_on_fee_133:,.0f}đ) = {t1_pm_total_debit:,.0f}đ == Credit TK 112={t1_pm_credit_112:,.0f}đ | Dư Debit TK 112 cuối ngày T+1 = 0 + 9,800,000 - 5,003,300 = {tk112_close_t1:,.0f}đ -> PASS")

# 5. Kiểm tra source_quote và toàn bộ con số trong 4 Quiz Cards (AC-15, AC-16)
cards_section = lesson_text.split("## 6. Bộ Quiz Card cuối bài")[1].split("## 7.")[0]
# Strip inline annotation blockquotes (> ...) and backticks from body prose to match rendered section prose
body_lines = [ln for ln in lesson_text.split("## 5.")[0].splitlines() if not ln.startswith(">")]
body_prose = re.sub(r"\n{2,}", "\n", re.sub(r"`", "", "\n".join(body_lines)))

card_blocks = re.split(r"### Card \d+ · ", cards_section)[1:]
for block in card_blocks:
    cid = re.match(r"`([^`]+)`", block).group(1)
    sq_match = re.search(r"- \*\*`source_quote`:\*\* `(.*?)`\n- \*\*", block, re.S)
    sq = sq_match.group(1)
    in_body = sq in body_prose
    rest = re.sub(r"\(#h2-[^)]+\)", "", block[sq_match.end()-4:])
    nums_in_sq = set(re.findall(r"\d+(?:[.,]\d+)*[%đ]?", sq))
    nums_in_card = set(re.findall(r"\d+(?:[.,]\d+)*[%đ]?", rest))
    missing_nums = nums_in_card - nums_in_sq
    assert in_body, f"{cid}: source_quote không khớp nguyên văn thân bài"
    assert not missing_nums, f"{cid}: có số ngoài source_quote: {missing_nums}"
    print(f"[K1.5] Card {cid}: source_quote khớp thân bài={in_body} | Số trong card={sorted(nums_in_card)} ⊆ Số trong source_quote -> PASS")

print("\n=== [K2] ĐỐI CHIẾU NGUYÊN VĂN TÊN TÀI KHOẢN VỚI tt99-phu-luc-ii.secondary.json ===")
accounts_by_code = {acc["code"]: acc for acc in tt99_data["accounts"]}
target_codes = ["112", "113", "133", "331", "511", "642"]

for code in target_codes:
    acc = accounts_by_code[code]
    expected_name = unicodedata.normalize("NFC", acc["name"])
    occ_lines = []
    for line_no, line in enumerate(lesson_text.splitlines(), start=1):
        for m in re.finditer(rf"TK {code} — ", line):
            after = line[m.end():]
            assert after.startswith(expected_name), f"L{line_no}: '{after}' không bắt đầu bằng '{expected_name}'"
            occ_lines.append(f"L{line_no}")
    print(f"[K2] TK {code} — {expected_name} | Vị trí: {', '.join(occ_lines)} | JSON agreement={acc['agreement']} | Nguồn={list(acc['names_by_source'].keys())} -> KHỚP NGUỒN THỨ CẤP")
```

### 2.2. Output nguyên văn

```text
=== [K1] KIỂM TRA SỐ HỌC TOÀN BÀI & QUIZ CARDS ===
[K1.1] Mục 1 (L25, L41) & Card L01-C01.v1 (L175-183): Số dư trước=2,500,000đ + Lương Credit=10,000,000đ -> Số dư mới=12,500,000đ | Tổng Debit NH=10,000,000đ == Tổng Credit NH=10,000,000đ -> PASS
[K1.2] Mục 2 (L55, L65) & Card L01-C04.v1 (L235): Số dư sau quét QR=12,500,000đ - 10,000,000đ = 2,500,000đ | Phí MDR = 10,000,000đ * 2% = 200,000đ | Tiền về T+1 = 10,000,000đ - 200,000đ = 9,800,000đ -> PASS
[K1.3a] Mục 3 Đêm T+0 (L85-87): Debit TK 113=10,000,000đ == Credit TK 511=10,000,000đ -> PASS
[K1.3b] Mục 3 Sáng T+1 (L98-102) & Card L01-C02.v1 (L192-203): Tổng Debit (TK 112 9,800,000đ + TK 642 200,000đ) = 10,000,000đ == Credit TK 113=10,000,000đ | Số dư TK 113 sau T+1 = 0đ | Số treo nếu ghi sai như phương án B = 200,000đ -> PASS
[K1.4] Mục 4 Chiều T+1 (L116-130) & Card L01-C03.v1 (L212-226): Phí chưa thuế=3,000đ + GTGT 10%=300đ = 3,300đ | Tổng Debit (TK 331: 5,000,000đ + TK 642: 3,000đ + TK 133: 300đ) = 5,003,300đ == Credit TK 112=5,003,300đ | Dư Debit TK 112 cuối ngày T+1 = 0 + 9,800,000 - 5,003,300 = 4,796,700đ -> PASS
[K1.5] Card L01-C01.v1: source_quote khớp thân bài=True | Số trong card=['10.000.000đ', '12.500.000đ', '2.500.000đ'] ⊆ Số trong source_quote -> PASS
[K1.5] Card L01-C02.v1: source_quote khớp thân bài=True | Số trong card=['1', '10.000.000đ', '112', '113', '2%', '200.000đ', '642', '9.800.000đ'] ⊆ Số trong source_quote -> PASS
[K1.5] Card L01-C03.v1: source_quote khớp thân bài=True | Số trong card=['0đ', '1', '112', '133', '3.000đ', '3.300đ', '300đ', '331', '4.796.700đ', '5.000.000đ', '5.003.300đ', '642', '9.800.000đ'] ⊆ Số trong source_quote -> PASS
[K1.5] Card L01-C04.v1: source_quote khớp thân bài=True | Số trong card=[] ⊆ Số trong source_quote -> PASS

=== [K2] ĐỐI CHIẾU NGUYÊN VĂN TÊN TÀI KHOẢN VỚI tt99-phu-luc-ii.secondary.json ===
[K2] TK 112 — Tiền gửi không kỳ hạn | Vị trí: L99, L104, L105, L116, L154, L154, L193, L198, L200, L202, L212 | JSON agreement=both_match | Nguồn=['ketoanleanh', 'xcyber'] -> KHỚP NGUỒN THỨ CẤP
[K2] TK 113 — Tiền đang chuyển | Vị trí: L85, L92, L93, L155, L155 | JSON agreement=both_match | Nguồn=['ketoanleanh', 'xcyber'] -> KHỚP NGUỒN THỨ CẤP
[K2] TK 133 — Thuế GTGT được khấu trừ | Vị trí: L124, L127, L128, L156, L156, L216, L221 | JSON agreement=both_match | Nguồn=['ketoanleanh', 'xcyber'] -> KHỚP NGUỒN THỨ CẤP
[K2] TK 331 — Phải trả cho người bán | Vị trí: L116, L118, L119, L157, L157, L212 | JSON agreement=both_match | Nguồn=['ketoanleanh', 'xcyber'] -> KHỚP NGUỒN THỨ CẤP
[K2] TK 511 — Doanh thu bán hàng và cung cấp dịch vụ | Vị trí: L86, L95, L96, L158, L158 | JSON agreement=only_ketoanleanh | Nguồn=['ketoanleanh'] -> KHỚP NGUỒN THỨ CẤP
[K2] TK 642 — Chi phí quản lý doanh nghiệp | Vị trí: L100, L107, L108, L123, L159, L159, L194, L198, L202, L215, L221 | JSON agreement=only_ketoanleanh | Nguồn=['ketoanleanh'] -> KHỚP NGUỒN THỨ CẤP
```

---

## 3. Chưa xác minh được

- **Phụ lục II bản gốc của Thông tư 99/2025/TT-BTC:** File gốc trong repo (`where-money-sleeps/legal/VanBanGoc_TT 99.2025-btc.pdf`, tải từ `vbpl.vn`) gồm 32 trang phần thân Thông tư (trang 7–32 là bản scan ảnh), **không đính kèm Phụ lục I–IV**. Do đó, 6 tên tài khoản trong bài (`112`, `113`, `133`, `331`, `511`, `642`) hiện mới đối chiếu với bản chép thứ cấp (`where-money-sleeps/legal/tt99-phu-luc-ii.secondary.json` — tổng hợp từ `ketoanleanh.edu.vn` và `xcyber.vn` ngày `2026-10-24`) và dừng ở mức phán **`KHỚP NGUỒN THỨ CẤP`** (theo QĐ 37). Trong đó, `TK 511` và `TK 642` mới có mặt ở nguồn `ketoanleanh` (`agreement: "only_ketoanleanh"`) vì trang `xcyber` chỉ đăng 50 tài khoản đầu tiên (`111`→`411`).
- **Nội dung hướng dẫn chi tiết kết cấu và nội dung phản ánh của từng tài khoản trong Phụ lục II Thông tư 99/2025/TT-BTC:** Chưa có văn bản gốc Phụ lục II nên việc phân tích kết cấu chi tiết của `TK 113`, `TK 642`, `TK 1388` ở phép kiểm K3 dựa trên nguyên lý kế toán Việt Nam (VAS) và sự kế thừa từ Thông tư 200/2014/TT-BTC sang Thông tư 99/2025/TT-BTC; cần người ký có chứng chỉ (QĐ 34.2 / QĐ 36) xác nhận lần cuối.

Same vendor, same priors — no external verifier ran. Chữ ký duyệt: Duy.
