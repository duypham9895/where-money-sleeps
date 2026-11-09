# Báo cáo Crawl & Chắt lọc Tri thức Tài chính (`tai-chinh-reviewer`)

- **Thời điểm cập nhật (`lastCrawledAt`):** `2026-11-09T23:23:09+07:00`
- **Kho tri thức:** `knowledge/finance-kb.json` (Schema v1)
- **Chính sách độ tươi (`freshnessPolicy`):** Tối đa `30` ngày · Lịch định kỳ khuyến nghị: `0 8 * * 1` (`Asia/Ho_Chi_Minh`)
- **Tổng số nguồn chuẩn thức:** `5` nguồn · `7` quy tắc miền (`F1–F4`) · `5` hợp đồng bất biến bài viết ↔ video

## 1. Kiểm chứng Tài liệu Pháp lý & Học thuật Nội bộ (`legal/`)

| Nguồn | Đường dẫn trong repo | Dung lượng (bytes) | SHA-256 | Trạng thái |
|---|---|---:|---|---|
| `SRC-MOF-TT99-2025` | `legal/VanBanGoc_TT 99.2025-btc.pdf` | 1,603,054 | `357add90184f37e6…97c76036` | **VERIFIED_LOCAL** |
| `SRC-MOF-TT99-2025` | `legal/tt99-phu-luc-ii.secondary.json` | 40,471 | `612a971a43479a3d…9844d918` | **VERIFIED_LOCAL** |
| `SRC-HERMANSON-ACCOUNTING` | `legal/licences.json` | 14,430 | `87c0c6aac7dbb633…88bff733` | **VERIFIED_LOCAL** |

## 2. Trạng thái Thăm dò Nguồn Pháp quy & Ngân hàng Công khai

| Nguồn | URL chuẩn thức | HTTP | Trạng thái | Ghi chú |
|---|---|---|---|---|
| `SRC-MOF-TT99-2025` | `https://vbpl.vn/botaichinh/Pages/vbpq-toanvan.aspx?ItemID=180615` | `308` | **HTTP_RESPONSE** | HTTP 308 (cần trình duyệt thật nếu có tường chống bot) |
| `SRC-MOF-TT99-2025` | `https://mof.gov.vn` | `200` | **LIVE_REACHABLE** | Cổng thông tin điện tử Bộ Tài Chính |
| `SRC-MOF-TT99-2025` | `https://congbao.chinhphu.vn` | `200` | **LIVE_REACHABLE** | Công báo điện tử Nước CHXHCN Việt Nam |
| `SRC-SBV-PAYMENT-CARD` | `https://www.sbv.gov.vn` | `—` | **OFFLINE_OR_SANDBOX** | Chế độ cô lập mạng / ngoại tuyến (TimeoutError) — giữ nguyên bản chốt trong repo |
| `SRC-SBV-PAYMENT-CARD` | `https://www.bis.org/cpmi/publ/d00b.htm` | `200` | **LIVE_REACHABLE** | OK |
| `SRC-SBV-CONSUMER-FINANCE` | `https://vbpl.vn/nganhangnhanuoc` | `404` | **HTTP_RESPONSE** | HTTP 404 (cần trình duyệt thật nếu có tường chống bot) |
| `SRC-HERMANSON-ACCOUNTING` | `https://openlibrary-repo.ecampusontario.ca/jspui/bitstream/123456789/425/1/Accounting%20Principles%20A%20Business%20Perspective.pdf` | `200` | **LIVE_REACHABLE** | OK |

## 3. Tri thức Tài chính Đã Chắt lọc (`domainRules`)

| Mã quy tắc | Phép kiểm | Danh mục | Bản chất cốt lõi đã chắt lọc |
|---|---|---|---|
| `FIN-MECH-01` | **F1** | `spending` | Quẹt thẻ thành công tại máy POS chỉ là thông điệp uỷ quyền (Authorization) và phong tỏa hạn mức (Hold) chạy trên dây tín hiệu trong 2 giây; tiền thật chỉ di chuyển qua ống ngầm liên ngân hàng ở kỳ bù trừ/quyết toán (T+1/T+2) sau khi đã trừ phí MDR. |
| `FIN-MECH-02` | **F1** | `borrowing` | Trả góp 0% không phải là khoản vay không có lãi trong hệ thống: cửa hàng chịu khấu trừ một phần giá bán (ví dụ 5% = 600.000đ trên món hàng 12.000.000đ, chỉ thực nhận 11.400.000đ) để bù lãi cho công ty tài chính. Nghĩa vụ trả nợ hàng tháng của người mua là với công ty tài chính, độc lập với cửa hàng. |
| `FIN-MECH-03` | **F1** | `income` | Chi lương cùng ngân hàng chỉ đổi tên chủ sở hữu trên sổ cái nội bộ của đúng ngân hàng đó (0 đồng tiền dự trữ rời kho, giữ trọn CASA). Về kế toán doanh nghiệp, chi phí lương ghi nhận theo lương gộp (Gross) vào TK 642/641/622 đối ứng TK 334; phần BHXH/BHYT/BHTN (10,5% lương đóng bảo hiểm) và thuế TNCN được khấu trừ từ TK 334 sang TK 338 và TK 3335 trước khi chi lương thực lĩnh (Net) qua TK 112. |
| `FIN-MATH-01` | **F2** | `accounting` | Mọi bút toán kế toán trong cả Diorama (beats.ledger) và Bài chuyên sâu (article.pro.journal) phải thoả mãn Σ Nợ = Σ Có tuyệt đối tới từng đồng. Mọi phép quy đổi lãi suất thực tế (EIR) từ dòng tiền trả góp đều phải giải phương trình giá trị hiện tại: sum_{t=1..n} CF_t / (1 + r_m)^t = PV_eff, với EIR_năm = (1 + r_m)^12 - 1 (hoặc lãi danh nghĩa năm = 12 * r_m nêu rõ cách tính). |
| `FIN-REG-01` | **F3** | `regulatory` | Từ 01/01/2026, tên và số hiệu tài khoản kế toán doanh nghiệp tuân theo Phụ lục II Thông tư 99/2025/TT-BTC (ví dụ TK 112 mang tên 'Tiền gửi không kỳ hạn', không còn gọi là 'Tiền gửi ngân hàng' như TT 200 cũ). Bài viết và video chỉ mô tả cơ chế vận hành ở ngôi thứ ba, tuyệt đối không đưa lời khuyên cá nhân ('bạn nên vay/mua/mở thẻ'). |
| `FIN-MECH-04` | **F1** | `borrowing` | Thời gian ân hạn miễn lãi (45–55 ngày) của thẻ tín dụng là ưu đãi có điều kiện: chỉ hiệu lực khi chủ thẻ thanh toán đủ 100% dư nợ sao kê đúng hạn. Khi chỉ trả mức tối thiểu (ví dụ 5% = 500.000đ trên sao kê 10.000.000đ ở Ngày 45), chủ thẻ thoát phí phạt trễ hạn và nợ quá hạn nhưng mất toàn bộ thời gian miễn lãi: ngân hàng tính lãi lùi từ ngày giao dịch phát sinh (Ngày 01) trên toàn bộ 10.000.000đ cho 45 ngày đầu (450.000đ ở mức ví dụ 0,1%/ngày hay 3%/tháng) cộng lãi trên 9.500.000đ dư nợ còn lại cho 15 ngày tiếp theo (142.500đ), tổng cộng 592.500đ tiền lãi ở sao kê Ngày 60 (lớn hơn cả khoản trả tối thiểu 500.000đ, nâng dư nợ mới lên 10.092.500đ). |
| `FIN-MECH-05` | **F1** | `spending` | Quét mã QR chuyển khoản liên ngân hàng 24/7 là giao dịch thanh toán đẩy (Push Payment) đi trực tiếp từ tài khoản tiền gửi thanh toán (CASA) của người mua sang tài khoản tiền gửi của cửa hàng qua hệ thống chuyển mạch liên ngân hàng 24/7: không qua mạng lưới tổ chức thẻ quốc tế, không cấp tín dụng/rủi ro hoàn trả (chargeback), nên cửa hàng nhận đủ 100% mệnh giá với mã QR tĩnh (ví dụ 50.000đ hoặc lô 200 ly = 10.000.000đ thu đủ 10.000.000đ vào TK 112 ngay lập tức, so với quẹt thẻ mất MDR 2,2% = 220.000đ chỉ còn 9.780.000đ treo trên TK 1388). Với mã QR động tích hợp phần mềm bán hàng/loa báo tiền tự động, phí dịch vụ thu hộ chỉ khoảng 0,1%–0,5% (ví dụ 0,2% = 20.000đ trên 10.000.000đ, thực nhận 9.980.000đ). Về cuối ngày, các ngân hàng thành viên quyết toán chênh lệch ròng (Deferred Net Settlement) trên tài khoản tiền gửi thanh toán tại Ngân hàng Nhà nước. |
