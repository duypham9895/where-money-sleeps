---
status: pass
stage: 06-iterate
date: 2026-11-09
owner: pm
blocked_on: []
---

# TRIAGE — Sổ Phân Loại Phản Hồi & Hàng Đợi Sản Xuất Nội Dung (`S6 Iterate` — `where-money-sleeps`)

> **Quy tắc vận hành (`../docs/stages.md` & Quy tắc 14):** File này chỉ ghi thêm (`append-only`), mọi mục đều gắn ngày (`YYYY-MM-DD`). Mọi bài mới trong hàng đợi đều đi qua đúng 6 bước `/vibe-post` (`gates/01-spec/AGENT-CMS-PIPELINE.md`) ở bậc định tuyến `T2` (`Khoá-rồi-Hạ`: `Claude Sonnet 5.5` / `Gemini 4 Argon Medium` + `T0` `scripts/wms-check.sh`), giữ ở trạng thái chờ Duy duyệt trên `docs/studio.html` và `unlisted` trên `@WhereMoneySleeps`.

## 1. Nhật Ký Phân Loại Kỹ Thuật & Trải Nghiệm (`2026-11-09`)

| Ngày | Mã mục | Nguồn phát hiện | Phân loại & Xử lý | Trạng thái |
|---|---|---|---|---|
| 2026-11-09 | `TR-01` | Phản hồi trực tiếp của Duy ở cuối `S3` (*"tại sao trong video bây h kh còn bất kì animations nào hết vậy?"*) | **Đã xử lý triệt để (`commit db3767e`):** Nâng cấp `scripts/wms-render-short-v43.py` và `scripts/wms-render-long-v43.py` từ `v6.0` (`0,45s` bị nuốt trong cross-dissolve) lên **Calm Editorial Motion `v6.5`** (dời điểm bắt đầu nhịp 1 sang `win_t0 + 0,40s`, kéo dài hoạt cảnh lên `2,2s–4,4s` `ease_out_cubic`, thêm hạt sáng dẫn lưu `3,6s` + số nhảy `tabular-nums`), kết xuất lại và tải đủ 6 video `v6.5` (`unlisted`) lên `@WhereMoneySleeps`. | **`CLOSED`** |
| 2026-11-09 | `TR-02` | Kiểm toán viên độc lập cổng `S4 QA` (`subagent c5f36e90-35d7-4ae5-b886-c52133e8e483`) | **Đã xử lý triệt để (`commit 774f2d2`):** Đổi đường dẫn `sendBeacon` từ `/api/event` sang `/api/p` tránh danh sách cấm EasyPrivacy (`AC-68`), tính `from_start` từ `tel.lesson_completed["card"]` (`AC-62`), bổ sung nút & hàm tự khai giai đoạn Mở đầu `selfDeclareEntryStage()` (`AC-30`, `R3`) và thêm `reviewed_by="Duy"` + `source_quote` cho 6 thẻ `WMS_QUIZ_BANK`. | **`CLOSED`** |
| 2026-11-09 | `TR-03` | Hạng mục chờ trước khi mở `public` (`LAUNCH-READINESS.md` `H1–H4`) | **Đang theo dõi:** (H1) Duy đọc hợp đồng Ringkas (`R34`); (H2) chạm thử `#sync` trong WebView Zalo trên iPhone/Android thật (`AC-31`); (H3) nối Cloudflare Worker `/api/p` + D1 (`AC-35, 55`); (H4) Duy ký chuyển 3 bài mẫu & 6 video từ `unlisted` sang `public`. | **`OPEN (Human Gate)`** |

## 2. Hàng Đợi Sản Xuất 16 Bài Tiếp Theo Theo Khuôn `/vibe-post` Đã Khoá (`7 Danh Mục · 19 Chủ Đề`)

Ba bài trụ cột đầu tiên (`card`, `pay`, `install` — tương ứng 3 danh mục `c2`, `c1`, `c3`) đã hoàn tất 100% cả bài viết `C9 v2`, 12 hình mặt cắt `LUẬT 9`, 6 thẻ trắc nghiệm và 6 video Calm Editorial Motion `v6.5`. Dưới đây là thứ tự ưu tiên đề xuất cho **16 bài `upcoming`** còn lại trong `CATEGORIES` (`docs/prototype.html`):

| Đợt (`Wave`) | Danh mục (`catId`) | Tiêu đề 3 điểm neo dự kiến (`storyId` đề xuất) | Cơ chế cốt lõi & Tài khoản TT 99/2025 | Độ ưu tiên |
|---|---|---|---|---|
| **Đợt 1 (Ưu tiên số 1 — Gợi ý chạy `/vibe-post` tiếp theo)** | `c3` · Vay nợ & Lãi suất thực | **`minpay`** — *Trả tối thiểu 5% (500 nghìn) trên sao kê thẻ tín dụng 10 triệu: Vì sao bạn mất trắng 45 ngày miễn lãi và chịu lãi ~28–36%/năm tính lùi từ ngày quẹt?* | Cơ chế mất ân hạn toàn phần (`Grace Period Forfeiture`), tính lãi theo số dư bình quân ngày (`Average Daily Balance`), bút toán thu lãi & dự thu của ngân hàng phát hành | **P1 (Sẵn sàng chạy ngay)** |
| **Đợt 1** | `c2` · Thẻ, QR & Thanh toán | **`qr`** — *Quét mã QR chuyển khoản 50 nghìn ở quán cà phê: Vì sao quán nhận đủ 50 nghìn ngay lập tức mà không mất 2,2% phí như quẹt thẻ?* | Phân biệt `Push Payment` (chuyển khoản liên ngân hàng `24/7` qua tổ chức chuyển mạch, trừ thẳng `CASA`) vs `Pull Payment` (thẻ tín dụng 4 bên có `MDR` & `T+2`); `TK 112` vs `TK 1388` | **P1** |
| **Đợt 1** | `c4` · Doanh nghiệp, Hoá đơn & Thuế | **`profitcash`** — *Báo cáo lãi ròng 2 tỷ đồng cuối năm nhưng két tiền công ty chỉ còn 50 triệu: Vì sao doanh nghiệp có lãi trên sổ vẫn hết tiền trả lương?* | Kế toán dồn tích (`Accrual` — ghi nhận doanh thu `Có TK 511 / Nợ TK 131` ngay khi giao hàng) vs Dòng tiền thực (`Cash Flow` — tiền nằm ở phải thu `TK 131` và hàng tồn kho `TK 156`) | **P1** |
| **Đợt 2** | `c1` · Lương & Ngân hàng | **`offus`** — *Chuyển khoản 20 triệu cùng ngân hàng (`On-Us`) và khác ngân hàng (`Off-Us`): Tiền thật đi qua những sổ nào dưới lòng đất?* | Bù trừ ròng liên ngân hàng (`Net Settlement`) và tài khoản tiền gửi thanh toán tại Ngân hàng Trung ương | **P2** |
| **Đợt 2** | `c1` · Lương & Ngân hàng | **`termdep`** — *Gửi tiết kiệm kỳ hạn 100 triệu lãi 5,5%/năm: Ngân hàng lấy tiền của ai trả lãi cho bạn và vì sao rút trước hạn chỉ còn 0,1%/năm?* | Biến đổi kỳ hạn (`Maturity Transformation`), chênh lệch lãi suất ròng (`NIM`), dự phòng thanh khoản và chi phí trả lãi dự trả (`TK 335`) | **P2** |
| **Đợt 2** | `c2` · Thẻ, QR & Thanh toán | **`debitcredit`** — *Quẹt thẻ ghi nợ (`Debit`) và thẻ tín dụng (`Credit`) cùng một hoá đơn 2 triệu: Ai đang tiêu tiền của mình và ai đang vay ngân hàng?* | Nguồn tiền `CASA` của chính bạn vs hạn mức tín dụng ứng trước của ngân hàng phát hành (`Open-to-buy`) | **P2** |
| **Đợt 2** | `c2` · Thẻ, QR & Thanh toán | **`refund`** — *Huỷ giao dịch thẻ vừa quẹt tại quầy nhưng 5 ngày sau tiền mới về: Tiền của bạn nằm chờ ở đâu suốt 5 ngày đó?* | Ba đường đi ngược (`Reversal` trước `Clearing` vs `Refund` sau `Settlement` vs `Chargeback`), `Nợ TK 521 / Có TK 1388` | **P2** |
| **Đợt 2** | `c3` · Vay nợ & Lãi suất thực | **`mortgage`** — *Vay mua nhà 2 tỷ lãi ưu đãi 6,5%/năm năm đầu: Vì sao khi hết ưu đãi lãi thả nổi vọt lên 10,5%/năm và tiền trả hàng tháng tăng thêm 5 triệu?* | Lãi suất cơ sở + biên độ (`Reference Rate + Margin`), bảng phân bổ gốc/lãi (`Amortization`) và phí trả nợ trước hạn (`Prepayment Fee`) | **P2** |
| **Đợt 3** | `c4` · Doanh nghiệp, Hoá đơn & Thuế | **`vat`** — *Hoá đơn 1,1 triệu gồm 100 nghìn thuế GTGT (10%): Khoản 100 nghìn đó ngủ trong tài khoản cửa hàng bao lâu trước khi về Kho bạc?* | Thuế GTGT đầu ra (`Có TK 33311`) khấu trừ thuế GTGT đầu vào (`Nợ TK 1331`) và kỳ kê khai nộp thuế | **P3** |
| **Đợt 3** | `c4` · Doanh nghiệp, Hoá đơn & Thuế | **`voucher`** — *Mua phiếu quà tặng 1 triệu chưa dùng: Trên sổ kế toán của cửa hàng, 1 triệu đó là doanh thu hay một khoản nợ phải trả?* | Doanh thu chưa thực hiện (`Có TK 3387`) chỉ chuyển thành doanh thu bán hàng (`Có TK 511`) khi khách mang phiếu tới đổi hàng hoặc hết hạn | **P3** |
| **Đợt 3** | `c5..c7` · Bảo hiểm, Ngoại tệ & Sàn TMĐT | **6 chủ đề còn lại** (`insure`, `escrow_house`, `dcc_fx`, `remit_swift`, `ecom_escrow`, `ewallet_float`) | Sẵn sàng mở rộng theo đúng kiến trúc `Content-as-Data` mà không cần sửa giao diện hay bộ dựng video | **P3** |

## 3. Kiểm Chéo `T2` (Phòng Data hỏi — Phòng PM trả lời)

1. **Câu hỏi 1 (Phòng Data):** *"Khi sản xuất thêm bài mới trong Đợt 1 (ví dụ bài `minpay`), việc thêm phần tử vào `STORIES` và `WMS_QUIZ_BANK` có làm đổi vị trí hay ý nghĩa của bài số 1 (`card`) trong công thức tính `from_start` (`QĐ 39`) không?"*
   - **Trả lời (Phòng PM):** Hoàn toàn không. Bài số 1 của lối vào đã được khoá cứng vào khoá ổn định `lessonId = "card"` (`TRACKING-PLAN.md` §1 & §2.5); việc thêm bài `minpay` vào danh mục `c3` chỉ mở rộng danh sách bài mà không chạm vào khoá `"card"` hay lịch sử sự kiện cũ.
2. **Câu hỏi 2 (Phòng Legal):** *"Khi chạy `/vibe-post` cho bài mới ở `S6 Iterate`, cổng nào đảm bảo bài mới không vô tình lọt tên ngân hàng thật hay sai tên tài khoản TT 99/2025?"*
   - **Trả lời (Phòng PM):** Mọi bài mới đều bắt buộc chạy qua bộ 5 cổng `scripts/wms-check.sh` (`check-story.py` `C0–C9`, `wms-finance-kb.py` `F1–F4`, `wms-motion-snap.py` `M0–M4`, `wms-studio-sync.py`, `vibe-check.sh`) và `scripts/wms-qa-verify.py` trước khi trình lên `docs/studio.html` cho Duy duyệt.

## 4. Chưa xác minh được

- Phản hồi thực tế của độc giả đầu tiên sau khi mở `public` để điều chỉnh thứ tự ưu tiên giữa Đợt 1 và Đợt 2.
- Same vendor, same priors — no external verifier ran.
