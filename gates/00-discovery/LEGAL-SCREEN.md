---
status: pass
stage: 00-discovery
date: 2026-10-24
---
# LEGAL-SCREEN — Where Money Sleeps

> **2026-10-24:** thân bài viết trước 14 quyết định; **§Kết luận sau 14 quyết định (cuối file) thắng**. Đã thay: BIS không còn "host có điều kiện" mà chỉ link (câu 10); Hermanson theo catalog là CC BY **4.0** (trang bản quyền PDF gốc + hình "otherwise noted" vẫn chưa kiểm).

**TL;DR** · đọc khoảng 6 phút · *tôi không phải luật sư*
- **Không host PDF, bản scan hay đoạn trích dài của bất kỳ sách trả phí nào.** Đây là lỗi giết sản phẩm, không chỉ là cảnh báo.
- OpenStax bản hiện hành là CC BY-NC-SA và có điều khoản chống LLM, nên **chỉ deep-link**. Không dùng Claude để dịch hay tóm tắt sách OpenStax.
- Nguồn host được thật sự rất mỏng: **nội dung Duy tự viết** là chính. Ngoài ra có tối đa 1 sách CC BY (Hermanson, phải kiểm tại PDF gốc) và một số tài liệu BIS/World Bank có điều kiện.
- Pháp lý VN: đứng tên cá nhân thì được, nhưng **không được thành "trang tổng hợp"**, không khuyến nghị chứng khoán, có một dòng minh bạch về việc AI hỗ trợ.

## Bảng tài liệu

| Nhóm | Tài liệu | Giấy phép | Nguồn | Điều kiện |
|---|---|---|---|---|
| **Host được** | Bài học Duy tự viết (VN/EN) | Của Duy | n/a | Dạy lại khái niệm bằng lời mình (Đ.15 Luật SHTT không bảo hộ khái niệm, nguyên lý). Không chép nguyên văn sách. |
| **Host được** | Font IBM Plex, Be Vietnam Pro, Newsreader | OFL | github.com/google/fonts/…/METADATA.pb | Tự host, kèm OFL.txt, ghi vào `licences.json` |
| **Host được** | PDF.js · foliate-js (thư viện) | Apache-2.0 · MIT | github.com/mozilla/pdf.js/blob/master/LICENSE · github.com/johnfactotum/foliate-js | Pin phiên bản/commit |
| **Host có điều kiện** | *Accounting Principles: A Business Perspective* (Hermanson/Edwards/Maher, Global Text) | CC BY (bản 3.0 hay 4.0 chưa rõ) | openlibrary-repo.ecampusontario.ca/jspui/handle/123456789/425?mode=full · open.umn.edu/opentextbooks/textbooks/accounting-principles-a-business-perspective | **Chỉ sau khi đọc trang bản quyền trong PDF gốc.** Không dùng bản Textbook Equity (NC-SA). Ghi tác giả, "bản dịch, đã sửa đổi", không ngụ ý tác giả bảo trợ. Sách cũ, theo US GAAP. |
| **Host có điều kiện** | Tài liệu BIS | Phi thương mại | bis.org/terms_conditions.htm | Bản dịch phải ghi "not an official BIS translation" và link bản gốc. Trích ≤400 từ. Chỉ dùng khi site phi thương mại. |
| **Host có điều kiện** | Ấn phẩm World Bank ghi CC BY 3.0 IGO | CC BY 3.0 IGO | openknowledge.worldbank.org | Kiểm **từng** ấn phẩm, có câu miễn trừ cho bản dịch |
| **Host có điều kiện** | Luật TCTD 2024, NĐ 52/2024, TT 64/2024 | Loại trừ theo Đ.15 Luật SHTT (đọc qua nguồn thứ cấp) | hethongphapluat.com/luat-so-huu-tri-tue-2005/dieu-15 | **Ưu tiên link** vbpl.vn/sbv.gov.vn. Chỉ trích có chọn lọc. Đăng lại hàng loạt có rủi ro thành "tổng hợp" theo NĐ 147. |
| **Vùng xám, chưa xếp** | OpenStax *Principles of Finance*, snapshot CC BY 4.0 trên GitHub (commit 3b7fc65, trước khi đổi giấy phép ngày 2026-04-08) | CC BY 4.0 ("Our licenses are irrevocable") | github.com/openstax/osbooks-principles-finance/commit/c802474325f10146c2ba1ca9af727b7940c19772 | Điều khoản chống LLM có trên trang CC BY khác của OpenStax. Terms of Use của site chưa đọc. Trademark. **Câu hỏi cho luật sư.** |
| **Vùng xám → coi là NC** | Bigel, *Introduction to Financial Analysis* | NXB ghi CC BY-NC 4.0; Pressbooks và LibreTexts ghi CC BY 4.0 | touroscholar.touro.edu/opentextbooks/2 | Coi như NC cho đến khi đọc được PDF gốc |
| **Vùng xám** | Saylor (Money and Banking…), Lyryx | Chỉ có metadata của OTL | open.umn.edu/opentextbooks/textbooks/money-and-banking | Metadata OTL đã sai ít nhất một lần |
| **Chỉ link** | OpenStax hiện hành: Accounting V1/V2, Finance 2e, Economics/Micro/Macro 3e, Business Statistics 2e, Introduction to Business 2e | CC BY-NC-SA + chống LLM | openstax.org/books/principles-finance-2e/pages/preface | Deep-link tới đúng chương. Không dùng bìa, logo, tên làm UI. |
| **Chỉ link** | Modern Treasury, Stripe Guides/Docs, CFI, Swift ISO 20022, NAPAS VietQR, các blog engineering, Net Interest, Fintech Brainfood, Fintech Business Weekly | Mặc định all-rights-reserved. Stripe SSA cấm chép. | stripe.com/legal/ssa · moderntreasury.com/ebooks/accounting-for-developers | Gắn nhãn "Đọc thêm · EN · không bắt buộc", không tính vào tiến độ |
| **Chỉ link** | IMF | Chỉ cho dùng cá nhân, phi thương mại | imf.org/en/about/copyright-and-terms | n/a |
| **Chỉ link** | FATF · World Bank bản CC BY-NC-ND | Chưa đọc được điều khoản (403) · ND | n/a | n/a |
| **Chỉ link** | *Trí Tuệ Tài Chính* (Alpha Books 2014), 5 sách trả phí, khoá Maven | Còn bản quyền | goodreads.com/work/editions/28156-financial-intelligence | Thẻ sách do Duy tự viết + link mua |
| **Không đụng** | PDF, bản scan, mục lục kèm trích dài, ảnh bìa của 5 sách trả phí + Maven | Còn bản quyền | n/a | n/a |
| **Không đụng** | Tên, logo, bìa OpenStax/Rice | Không thuộc CC | openstax.org/books/principles-finance/pages/preface | n/a |
| **Không đụng** | Dùng Claude dịch/tóm tắt OpenStax hiện hành | Điều khoản chống LLM | openstax.org/books/principles-financial-accounting/pages/1-why-it-matters | Cần OpenStax cho phép bằng văn bản |
| **Không đụng** | Bản dịch EN luật VN của LuatVietnam/TVPL, bản dịch hệ thống tài khoản của KPMG/PwC | Tác phẩm phái sinh (suy luận) | n/a | Bản EN tự viết "unofficial summary" + link bản VN |
| **Không đụng** | Bảng lãi vay có tên ngân hàng chép từ báo | Rủi ro "tổng hợp", số liệu cũ | n/a | Thay bằng máy tính người học tự nhập |

## Pháp lý VN

| Văn bản | Áp vào Where Money Sleeps thế nào | Mức |
|---|---|---|
| NĐ 147/2024 Đ.24 k2–k3 | Website cá nhân hoặc dịch vụ chuyên ngành (có nêu giáo dục) được miễn giấy phép, **trừ khi** cung cấp "thông tin tổng hợp". Giấy phép tổng hợp chỉ cấp cho tổ chức, nên cá nhân không xin được. | Vùng xám (nguồn thứ cấp) |
| Luật CK 2019 Đ.4 k32, Đ.12 k4 | Không nêu mã chứng khoán, không khuyến nghị mua/bán/nắm giữ. Tiền lệ: ITP bị phạt 225 triệu năm 2026. Khoản vay không phải chứng khoán. | Đã verify |
| Luật AI 134/2025 (hiệu lực 01/3/2026) | Một dòng: "soạn với hỗ trợ AI, duyệt bởi <ai>, ngày" | Vùng xám (chưa rõ có áp cho văn bản không) |
| TT 99/2025/TT-BTC | Thay TT 200 từ 01/01/2026. Glossary phải theo TT 99. | Đã verify (KPMG) |
| NĐ 17/2023 Đ.114 | Kênh gỡ nội dung thứ hai ở VN, cộng thêm DMCA tới host ở Mỹ | Vùng xám |
| NĐ 174/2026 | Nghị định xử phạt website mới, hiệu lực 01/7/2026. Mức phạt cụ thể: phương pháp này không tìm thấy. | Vùng xám |
| Hợp đồng lao động với Ringkas | Lộ trình có phần vay mua nhà, đúng mảng của Ringkas | **Duy tự đọc** |

**Quy tắc vận hành:** không tài khoản, không bình luận hay diễn đàn. Chỉ đăng nội dung gốc, mọi nguồn khác là link. Disclaimer một lần ở footer và một lần ở các bài về pháp lý/lãi suất, có ngày "căn cứ văn bản hiệu lực đến". Có một boolean `published` để **gỡ trước, tranh luận sau**.

## Đã verify / Vùng xám / Câu hỏi luật sư

| Đã verify (fetch lại nguồn gốc) | Vùng xám | Câu hỏi cho luật sư |
|---|---|---|
| OpenStax đang live là NC-SA, có câu chống LLM, bìa/logo không thuộc CC | Phạm vi của "thông tin tổng hợp" (chưa đọc được nguyên văn NĐ 147 Đ.3) | Một site giáo dục do một người viết, có trích văn bản QPPL, có bị coi là "tổng hợp" không? |
| Commit OpenStax đổi CC BY sang NC-SA ngày 2026-04-08 | Hermanson CC BY (catalog nói vậy, chưa đọc PDF) | Điều khoản chống LLM của OpenStax có ràng buộc người dùng snapshot CC BY lấy từ GitHub không? |
| IMF, BIS, Stripe SSA, Modern Treasury (© không giấy phép mở) | Bigel: các nguồn ghi giấy phép mâu thuẫn | Quảng cáo, affiliate, donate có làm việc dùng nội dung thành "commercial" theo NC không? |
| Án ITP 225 triệu, Luật CK Đ.4 k32 | Luật AI 134 có áp cho văn bản không, cá nhân có là "bên triển khai" không | Việc từ bỏ quyền nhân thân theo CC BY 4.0 §2(b)(1) có hiệu lực với bản dịch phát hành ở VN không? |
| TT 99 thay TT 200 | Đ.15 Luật SHTT sau các lần sửa 2022/2025 | So sánh sản phẩm tín dụng có tên ngân hàng có cần phép hay chịu Luật Quảng cáo không? |
| Font OFL có subset vietnamese | Tài liệu giáo dục của NHNN có tính là "văn bản hành chính" không | "Văn bản hành chính" có gồm tài liệu giáo dục tài chính của NHNN không? |

## Chưa xác minh được

- Trang bản quyền trong PDF gốc của Hermanson và Bigel (pressbooks.pub, BCcampus trả 403).
- Terms of Use của openstax.org, của sbv.gov.vn, của website Modern Treasury, và điều khoản FATF (403).
- Lịch sử LICENSE năm 2021 của repo OpenStax Accounting: output bị cắt nên đọc không trọn.
- Giấy phép riêng của từng hình "otherwise noted" trong các sách mở.
- Nguyên văn NĐ 147 Đ.3 và Đ.24: chỉ đọc qua Vision & Associates, LuatVietnam, lsvn. thuvienphapluat bị chặn.
- Mức phạt cụ thể theo NĐ 174/2026 Đ.93.
- Thời hạn gỡ theo NĐ 17/2023 Đ.114.
- VOER (voer.edu.vn) bị timeout. Phương pháp này không tìm thấy giáo trình kế toán tiếng Việt nào có giấy phép mở; các thư viện số HPU, TNUT, VKU đều hạn chế truy cập.
- Tên cơ quan quản lý: Bộ TTTT có thể đã sáp nhập. Lượt này chưa kiểm, nên ghi "cơ quan quản lý".
- Mọi số điều luật phải đối chiếu với văn bản gốc trước khi hành động.
- Same vendor, same priors — no external verifier ran.

## Kết luận sau 14 quyết định — 2026-10-24

| Mục | Trạng thái |
|---|---|
| Nguồn nội dung mùa 1 | Bài Duy tự viết + Hermanson *Accounting Principles* (catalog eCampusOntario `dc.rights` = **CC BY 4.0**, Claude tự đọc 2026-10-24). Lõi **không** có nguồn NC. |
| Card sinh lúc build | Chỉ từ hai nguồn trên. Sách trả phí ⇒ chờ luật sư câu (b). OpenStax hiện hành ⇒ không. |
| Trình đọc PDF | PDF.js Apache-2.0; file của người học xử lý thuần cục bộ, không gửi đi, LLM không chạm. |
| Đo | Bộ đếm gộp tự host, không ID/cookie/IP lưu lại. Luật 91/2025: vùng xám nhẹ (Cloudflare xử lý IP khi truyền). |
| Rủi ro còn lại | **Duy chấp nhận (câu 11, phương án A).** Không thuê luật sư ở mùa 1. |
| **Điều kiện trước S5** | (1) Duy đọc hợp đồng lao động Ringkas · (2) Claude đọc trang bản quyền trong PDF gốc Hermanson |
| Sau release | Workflow chuẩn bị hồ sơ (a)–(f) cho luật sư. **Workflow không phải ý kiến pháp lý**; thuê luật sư trước mọi tính năng mùa 2 đụng sách người khác. |
| **Đính chính 2026-10-24 (review S0)** | Dòng "Sau release" ở trên ghi "thuê luật sư trước mọi tính năng mùa 2" như đã chốt — **sai**: phần Duy thật sự quyết là câu 3 (sách trả phí chờ luật sư trả lời câu (b)) và câu 11 (không luật sư mùa 1; sau release chạy workflow). "Workflow không thay luật sư" là **cách hiểu của Claude, chờ Duy xác nhận**. Hồ sơ luật sư phải gồm **cả** (a)–(f) của ADDENDUM **và** 6 câu trong bảng "Câu hỏi cho luật sư" ở trên (NĐ 147 "tổng hợp" là câu đụng thẳng mùa 1). |
| **Quyết định 12/14 — 2026-10-24** | Duy: **workflow thay luật sư, không thuê luật sư.** Cổng trước mọi tính năng mùa 2 đụng sách người khác (card sách trả phí, "Ôn với AI của bạn", affiliate) = workflow pháp lý chuyên sâu trên toàn bộ (a)–(f) + 6 câu ở trên → **Duy ký chấp nhận rủi ro** cho từng tính năng. Kết luận của workflow luôn ghi "không phải ý kiến pháp lý · same vendor, same priors — no external verifier ran". |
| **Kiểm Hermanson tại PDF gốc — 2026-10-24** (điều kiện 2 của câu 13: XONG phần chữ) | PDF gốc ghi **CC BY 3.0** (không phải 4.0 như catalog) — vẫn cho phép phái sinh, dịch, thương mại, chỉ cần ghi công. **Phát hiện:** sách nhúng **đoạn trích bên thứ ba có © riêng** (10 trích FASB, New Accountant 1990, báo cáo thường niên GE/Gillette/Coca-Cola, WSJ) — CC BY **không** phủ các đoạn này ⇒ máy sinh card phải loại chúng; host nguyên PDF chính thức là phân phối lại đúng file của bên cấp phép, rủi ro thấp. **Còn mở:** 64 hình trên 59 trang chưa soát nguồn từng hình. Sổ: `legal/licences.json`. |
| **Đính chính sau câu 12–14 — 2026-10-24** | (1) Hermanson: **CC BY 3.0** thắng mọi chỗ ghi 4.0 ở trên; câu hỏi quyền nhân thân dẫn CC BY 4.0 §2(b)(1) phải đối chiếu lại điều khoản tương ứng của **3.0**. (2) Điều kiện pháp lý là **trước khi S1 chốt** (câu 13), không phải "trước S5". (3) Mọi chỗ "chờ luật sư" ⇒ **chờ workflow pháp lý + Duy ký** (câu 12). (4) 64 hình Hermanson: **đã soát** — đều là hình của tác giả. (5) Host nguyên PDF = phân phối lại cả các đoạn trích © bên thứ ba có trong sách; "rủi ro thấp" là **phán đoán của Claude**, không phải kết luận pháp lý — rủi ro này xuất hiện sau câu 11 nên được nêu riêng trên trang review. |
| **Đính chính (review vòng 3) — 2026-10-24** | Mục (4) dòng trên ("64 hình: đã soát — đều là hình của tác giả") **SAI**. Ít nhất 2 hình có nguồn bên thứ ba: tr.803 Exhibit 160 (Kaplan & Norton, HBR 1996 — nguồn nằm trong ảnh) và tr.501 (bảng giá Kellogg/WSJ). Hai hình này thêm vào danh sách loại khỏi máy sinh card. Soát hình **chưa xong** — chưa OCR, chưa xem đủ 63 hình ở độ phân giải gốc. |
| **Quyết định 15 + soát phạm vi host — 2026-10-24** | Chỉ host **tr.1–197** (front matter + chương 1–4). 8/8 ảnh sạch (xem tận mắt). Redact 2 đoạn trích bên thứ ba ở tr.113 (Home Depot) và tr.166 (New Accountant, © New DuBois). Hai hình bên thứ ba tìm thấy ở vòng 3 (tr.501, tr.803) **nằm ngoài** phạm vi host. File host ghi: "Trích chương 1–4 và sửa đổi (che 2 đoạn trích bên thứ ba) từ Hermanson, Edwards & Maher, *Accounting Principles: A Business Perspective*, CC BY 3.0". |
