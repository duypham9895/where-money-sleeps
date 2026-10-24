---
slug: where-money-sleeps
pointer: 01-spec
created: 2026-10-24
---

# PIPELINE — where-money-sleeps

**Đây là trạng thái DUY NHẤT của app này.** Không có con trỏ toàn cục ở đâu khác.

| # | Stage | Trạng thái | Artifact | Duyệt ngày |
|---|---|---|---|---|
| S0 | Discovery | `pass` | `gates/00-discovery/PRODUCT-BRIEF.md` · `LEGAL-SCREEN.md` · `ADDENDUM-PDF-LLM.md` (spec đường ống card) | 2026-10-24 |
| S1 | PRD | pending | `gates/01-spec/PRD.md` · `ACCEPTANCE.md` · `SUCCESS-CRITERIA.md` · `TRACKING-PLAN.md` · `LEGAL-REVIEW.md` | |
| S2 | Design | pending | `gates/02-design/` — direction · tokens · mockup · a11y · ui-states · microcopy | |
| S3 | Build | pending | `gates/03-build/SLICE-LOG.md` + commit `feat:` + `licences.json` | |
| S4 | QA | pending | `gates/04-qa/VERIFICATION.md` · `REVIEW.md` · `EVENT-VERIFICATION.md` | |
| S5 | Launch | pending | `gates/05-launch/LAUNCH-READINESS.md` · `POSITIONING.md` · đường gỡ | |
| S6 | Iterate | pending | `gates/06-iterate/TRIAGE.md` · `READOUT.md` | |

Trạng thái hợp lệ: `pending` · `in-progress` · `pass` · `fail` · `waived` · `N/A — because <lý do>`

**Ba cổng cứng ở S1, không cái nào waive được:** thiếu `SUCCESS-CRITERIA.md`,
`TRACKING-PLAN.md`, hoặc `LEGAL-REVIEW.md` ⇒ S1 không duyệt được.
**S5 `LAUNCH-READINESS` là cổng duy nhất không waive được ở bất kỳ hoàn cảnh nào.**

Bảng định tuyến đầy đủ — phòng ban nào vào, gọi lệnh gì: `../../docs/stages.md`.

## Log — chỉ thêm, không bao giờ sửa hay xoá

| Ngày | Sự kiện | Lý do |
|---|---|---|
| 2026-10-24 | MỞ PIPELINE, con trỏ ở `00-discovery`. Slug `dongtien` là **tên tạm**. | Duy muốn biến artifact *Lộ trình học Finance & Money Workflows* thành website song ngữ VN/EN, tiến độ lưu trên máy người học, kèm sách + trình đọc PDF, cho người không có nền tảng. Đầu vào tóm tắt ở `gates/00-discovery/SOURCE-ROADMAP.md`. |
| 2026-10-24 | S0 `in-progress` — Workflow 6 mũi + 3 lens phản bác đang chạy (`wf_06247c8a-dce`). | Quy tắc 2: research trước, build sau. Mũi giấy phép sách là mũi có khả năng **đổi hình dạng sản phẩm** nhất: các sách trả phí trong lộ trình gốc còn bản quyền. |
| 2026-10-24 | **TÊN ĐÃ CHỐT: Where Money Sleeps** · repo & slug `where-money-sleeps`. Thay tên tạm `dongtien`. | Duy chọn trong 3 phương án (Where Money Sleeps · Who Holds the Money · Money Trail). Lý do: gợi tò mò nhưng vẫn đoán ra chủ đề tiền, và trỏ thẳng vào câu hỏi mở đầu của lộ trình (*9.800.000đ trong đêm T+0 là tiền của ai?*). Đánh đổi đã nói ra: tên hơi thơ, có thể bị đọc thành "gửi tiết kiệm ở đâu" ⇒ **tagline giải nghĩa là BẮT BUỘC**, không tuỳ chọn. Loại *Follow the Money* vì trùng toà soạn điều tra Hà Lan. `wherethemoneysleeps.com` chưa đăng ký theo whois 2026-10-24 — **chưa mua**. Thư mục đổi tên **sau** khi workflow S0 xong, vì nó đang đọc file theo đường dẫn cũ. |
| 2026-10-24 | S0 có đủ artifact: `PRODUCT-BRIEF.md` · `LEGAL-SCREEN.md` · `UNDERSTOOD.md` · `gates/ONE-PAGER.md` (nháp, Duy chưa duyệt) · `docs/index.html` (447 từ). `vibe-check` PASS, 1 cảnh báo (chưa có `licences.json`). **Con trỏ KHÔNG được đẩy.** | Workflow `wf_06247c8a-dce`: 25 agent, 0 lỗi. Kết luận **Go có điều kiện**, ý gốc đổi 3 chỗ: không host sách, trình đọc HTML reflow, lối vào ngắn cho người mới. Tự fetch lại 2 kết luận then chốt: OpenStax là CC BY-NC-SA + cấm đưa vào LLM; TT 99/2025 thay TT 200 từ 01/01/2026. Còn **9 câu** cho Duy, hỏi từng câu. Same vendor, same priors — no external verifier ran. |
| 2026-10-24 | Câu 1/9 chốt: **hai tầng** — lối vào cho mọi người + lộ trình sâu tuỳ chọn. | Ghi ở `PRODUCT-BRIEF.md` §Quyết định của Duy. |
| 2026-10-24 | **Mở rộng phạm vi:** trình đọc PDF + LLM tóm tắt sách thành quiz card. Chạy S0 bổ sung. | Tính năng mới chạm cả ba thứ đã chốt ở S0: không backend/chi phí 0, không gửi dữ liệu ra ngoài, và giấy phép (OpenStax cấm đưa vào LLM). Quy tắc 2: research trước. |
| 2026-10-24 | S0 bổ sung có `ADDENDUM-PDF-LLM.md`. Câu hỏi hợp nhất thành **11** (xong 1). | Addendum khuyến nghị hoãn PDF reader — **ngược quyết định của Duy**, nên đưa thành câu hỏi, không tự áp. Same vendor, same priors — no external verifier ran. |
| 2026-10-24 | Câu 2/11 chốt: **không LLM runtime ở mùa 1**, chỉ card tĩnh sinh lúc build. | Ghi ở `PRODUCT-BRIEF.md` §Quyết định của Duy. |
| 2026-10-24 | Câu 3/11 chốt: nạp **bài tự viết + sách CC BY** (sau khi kiểm PDF gốc); sách trả phí chờ luật sư. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 4/11 chốt: **có trình đọc PDF ở mùa 1** (phương án A). | Ghi ở `PRODUCT-BRIEF.md`. Ngược khuyến nghị hoãn của addendum — Duy quyết, lý do hoãn đã bị câu 3 gỡ. |
| 2026-10-24 | Câu 5/11 chốt: **mùa 1 = B** (~28–30 bài) + chuẩn: mọi thuật ngữ có chú thích. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 6/11 chốt: **song ngữ C, nút gạt VI ⇄ EN tại chỗ.** | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 7/11 chốt: **lưu tiến độ A** + phép đo iPhone/Android của Duy là điều kiện chốt S1. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 8/11 chốt: **Duy duyệt hết + kế toán soát GĐ01/GĐ05/card có số**, chưa duyệt không đăng. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 9/11 chốt: **đo B**, bộ đếm gộp tự host, 5 event dự kiến. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 10/11 chốt: **không cam kết phi thương mại, lõi không có nguồn NC, mùa 1 không kiếm tiền.** | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Câu 11/11 chốt: **chấp nhận rủi ro còn lại (A)**, 2 điều kiện trước S5, workflow chuẩn bị hồ sơ luật sư sau release. **Đủ 11/11 quyết định S0.** | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | **Review gói S0** (`wf_5a7d7fe7-ad9`, 3 lens: consistency · falsify · design-asks). Đã sửa phần cơ học: ghi chú superseded có ngày ở đầu PRODUCT-BRIEF / ADDENDUM / LEGAL-SCREEN; ONE-PAGER sửa "không có giấy phép mở", phạm vi kế toán, thước đo thành **tỉ lệ gộp (proxy)**, tagline bắt buộc; trang review sửa nhãn câu 11 + câu VMLU nói quá; viết lại ONE-PAGER/index.html/kết luận LEGAL-SCREEN sau 11 quyết định (index.html giờ 338 từ). | Còn **3 câu cho Duy** từ review: (12) xác nhận cách hiểu "workflow cho luật sư"; (13) dời hai điều kiện pháp lý (Ringkas, Hermanson) từ trước S5 lên **trước S1**; (14) ngưỡng ra mắt + người kế toán làm điều kiện S1. Hai câu Design (bản đồ bề mặt, cách hiện chú thích) là câu S1/S2, không chặn S0. Same vendor, same priors — no external verifier ran. |
| 2026-10-24 | Câu 12/14 chốt: **workflow thay luật sư**, Duy ký chấp nhận rủi ro từng tính năng mùa 2. | Ngược khuyến nghị của Claude; ghi ở `PRODUCT-BRIEF.md` + `LEGAL-SCREEN.md`. |
| 2026-10-24 | Câu 13/14 chốt: **Ringkas + Hermanson phải xong trước S1**. | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | Hermanson kiểm tại PDF gốc: **CC BY 3.0**, đoạn trích bên thứ ba bị loại khỏi máy sinh card, 64 hình chưa soát. Tạo `legal/licences.json`. | Điều kiện 2/2 trước S1 xong phần chữ. Ringkas vẫn chờ Duy. |
| 2026-10-24 | Câu 14/14 chốt: **ra mắt khi lối vào duyệt xong, phần sau lên dần**; kế toán + bấm giờ là điều kiện S1. **S0 đủ 14/14.** | Ghi ở `PRODUCT-BRIEF.md`. |
| 2026-10-24 | **Review vòng 2** (`wf_b37d8b40-625`): 6/7 blocker vòng 1 đã gỡ. Hai blocker mới đã sửa: (1) soát 64 hình Hermanson bị Claude tự dời sang S3 — **đã làm luôn**, đều là hình của tác giả; (2) trang review nói quá "chưa ai dạy" — sửa thành "phương pháp không tìm thấy". Nonblocking đã sửa: số đếm 11→14, "chờ luật sư"→workflow + Duy ký, CC BY 3.0, rủi ro host PDF có trích bên thứ ba nêu trên trang review, luật loại trích dẫn vào ADDENDUM. | Same vendor, same priors — no external verifier ran. |
| 2026-10-24 | **Review vòng 3** (`wf_1673ba8d-757`, lượt cuối): blocker (b) gỡ; **blocker (a) CHƯA GỠ** — Claude ghi sai "64 hình đều của tác giả"; ít nhất 2 hình có nguồn bên thứ ba (tr.803 HBR, tr.501 WSJ). Đã đính chính có ngày ở PRODUCT-BRIEF, LEGAL-SCREEN, licences.json, index.html. **Hết 3/3 lượt review ⇒ leo thang lên Duy.** | `review-loop` bước 6: còn blocker sau lượt 3 thì dừng, không chạy vòng 4. Same vendor, same priors — no external verifier ran. |
| 2026-10-24 | Câu 15 chốt: **Hermanson chỉ host tr.1–197 (chương 1–4)**. Soát xong phạm vi đó: 8/8 ảnh sạch, 2 đoạn trích bên thứ ba phải redact ở S3. **Blocker vòng 3 gỡ bằng quyết định của Duy.** S0 đủ **15/15** quyết định. | Leo thang theo `review-loop` bước 6 đã được Duy giải. Kiểm sau cùng là của Claude (author-side), không phải lượt review thứ 4. |
| 2026-10-24 | **APPROVE S0** bởi Duy qua `/vibe:approve where-money-sleeps 00-discovery`. Con trỏ `00-discovery` → `01-spec`. | Artifact S0 đều `status: pass`; 15/15 quyết định; vibe-check PASS. **S1 chưa chốt được** cho tới khi xong 3 điều kiện của Duy: đo iPhone/Android · đọc hợp đồng Ringkas · có tên kế toán + bấm giờ 1 bài. |
