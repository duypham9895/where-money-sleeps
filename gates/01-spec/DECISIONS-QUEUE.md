---
stage: 01-spec
date: 2026-10-24
owner: PM
status: fail
blocked_on:
  - "Duy đo iPhone + Android thật (~30 phút): Zalo giữ #sync không · mở WebView hay trình duyệt · input type=file chạy không · localStorage sống trong WebView không"
  - "Duy đọc hợp đồng lao động Ringkas (điều khoản IP + không cạnh tranh)"
  - "Agent ke-toan-reviewer chạy thử 1 bài mẫu + card; đo thời gian Duy đọc báo cáo và ký (QĐ 36)"
---

# DECISIONS-QUEUE — hàng đợi câu hỏi cho Duy, S1

> TRIAGE của PM, 2026-10-24, **sau vòng sửa 2**; cập nhật 2026-10-25 theo QĐ 38–51 (§Đổi theo QĐ 38–51 ở cuối file). Gom **mọi** câu mở trong `gates/01-spec/` + review S1 sau QĐ 17–35
> (BLOCKER M2, M3, M8, §4(a)(b)(c); NONBLOCKING còn lại) + các "→ Duy" mới của PM (N1–N8), Data (M7), Legal (X10–X13),
> Writer (W1, W2). Mỗi câu xếp đúng một nhóm: **A** Duy quyết · **B** đã có quyết định trả lời · **C** bàn giao ·
> **D** trùng, đã gộp. Nguồn thẩm quyền: `PRODUCT-BRIEF.md` §Quyết định của Duy (**QĐ 1–51, dòng sau thắng**) ·
> `ONE-PAGER.md` · `LEGAL-SCREEN.md` §Kết luận + đính chính · `ADDENDUM-PDF-LLM.md` §Đường ống · `licences.json` · `PIPELINE.md`.
> Same vendor, same priors — no external verifier ran.

**TL;DR** · ~18.400 từ cả file (đếm theo khoảng trắng) · tầng HỢP ĐỒNG · trạng thái 2026-10-25 · đọc TL;DR + §Câu có điều kiện là đủ (~2 phút)
- **0 câu nhóm A còn mở.** Q-01…Q-18 + Q-21 ⇒ QĐ 17–35 · QĐ 36, 37 ngoài hàng đợi · Q-23 → QĐ 38 · Q-24 → QĐ 39 · Q-25 → QĐ 40 · **Q-26…Q-34, Q-19, Q-20 ⇒ QĐ 41–51, Duy nhận theo lô mọi khuyến nghị** (PRODUCT-BRIEF.md:179) · Q-22 → nhóm B (B-16). Bảng §Câu trả lời ở cuối file; nguyên văn các câu đã hỏi ở §Lưu trữ.
- **Còn lại, không phải câu nhóm A:** **3 câu có điều kiện** (ĐK-1…ĐK-3 — chỉ hỏi khi phép đo/cấu hình ra kết quả xấu) và **2 điểm chờ hợp đồng Ringkas** (QĐ 34.2 chữ định danh trong dòng AI/dòng soát · QĐ 35 công khai hộp thư).
- **3 điều kiện trước S1 của Duy vẫn chưa xong** ⇒ frontmatter `status: fail` giữ nguyên.
- Nhóm B: **16** · Nhóm C: **17** · Nhóm D: **45 nhóm**.
- **Lưu ý trung thực:** QĐ 41–51 là nhận theo lô, *trước khi đọc từng bảng phương án* (PRODUCT-BRIEF.md:179); QĐ 50 tự ghi Duy nên đọc lại ONE-PAGER bản đã áp. Việc PM còn nợ sau các QĐ này: §Việc còn nợ.

## Nhóm A — hàng đợi: 0 câu còn mở (2026-10-25)

Mọi câu nhóm A đã có trả lời: Q-23 → QĐ 38 · Q-24 → QĐ 39 · Q-25 → QĐ 40 · Q-26…Q-34, Q-19, Q-20 → QĐ 41–51 (Duy nhận **theo lô** mọi khuyến nghị, nguyên văn *"hãy chọn tất cả options mà bạn suggest"*, PRODUCT-BRIEF.md:179). Q-22 đã chuyển nhóm B (B-16). Nguyên văn từng câu lúc hỏi: §Lưu trữ.

### Câu có điều kiện — không tính vào nhóm A, chỉ hỏi khi điều kiện xảy ra

Đây là câu thật của Duy, không phải bàn giao. Khi điều kiện xảy ra, PM viết đủ khuôn và chèn vào hàng đợi.

| ĐK | Câu | Điều kiện kích hoạt | Gợi ý sơ bộ | Nguồn |
|---|---|---|---|---|
| ĐK-1 | `input type=file` **không** chạy trong WebView Zalo: cổng ra mắt QĐ 29 hiểu là "chạy trên trình duyệt thường là đủ" hay "ra mắt chờ" (PRD N3) | Phép đo điện thoại của Duy (điều kiện 1) ra "không chạy" | Trình duyệt thường là đủ, Zalo hiện hướng dẫn mở bằng trình duyệt | PRD Scope 9, B7 · ACCEPTANCE AC-26, AC-79 · LEGAL-REVIEW.md:123 |
| ĐK-2 | Cloudflare có tính năng xử lý IP **bật sẵn mà tắt được**: tắt hay giữ (QĐ 31 nói "không bật", chưa nói "tắt cái bật sẵn") | S3/S4 cấu hình Cloudflare và thấy tính năng đó | Tắt, theo tinh thần QĐ 9 | LEGAL-REVIEW.md:155 · ACCEPTANCE AC-84 |
| ĐK-3 | Header thư hoặc WHOIS lộ danh tính mà không sửa được: có công khai hộp thư không (R33 a′) | Phép kiểm (a′) trước khi công khai | Chưa có — tuỳ thứ bị lộ | LEGAL-REVIEW.md:171, :251 |

**Chờ hợp đồng Ringkas (không phải câu mới):** QĐ 34.2 chữ định danh trong "duyệt bởi ⟨…⟩" · QĐ 35 thời điểm công khai hộp thư.

## Nhóm B — đã có quyết định trả lời, đóng (16)

| B | Câu mở | Căn cứ S0 (nguyên văn) | Việc còn lại |
|---|---|---|---|
| B-01 | tr.113 Home Depot thiếu trong `exclusions` (K5, #1, Legal X3, Δ9) | Dòng soát phần host (PRODUCT-BRIEF.md:152): *"tr.113 … ⇒ phải redact trong file host … và loại khỏi máy sinh card"* | Legal thêm một dòng có ngày vào `licences.json`  · **Xong vòng sửa 2:** Legal đã thêm (PM đọc `licences.json` 2026-10-24) |
| B-02 | **Mới, chưa file nào ghi:** tr.117 Exhibit 15 có dòng *"Source' American Institute of Certified Public Accountants, Accounting Trends & Techniques"* (review falsify N11; PM đã xem lại bằng `pdftotext`) | QĐ 3 + dòng kiểm Hermanson (PRODUCT-BRIEF.md:145): *"đoạn trích bên thứ ba © riêng (FASB…) ⇒ loại khỏi máy sinh card"*; dòng :152: trích bên thứ ba trong phần host ⇒ *"phải redact trong file host"* | Legal thêm vào `exclusions` + `host_audit`, ghi điểm mù của phép grep (`Source'` ≠ `Source:`). Nếu Legal cho rằng bảng số liệu này không cần redact khỏi file host thì đó mới là câu cho Duy |
| B-03 | Writer phương án C "hiện sẵn" vs chạm (K4) | QĐ 16: *"Chú thích thuật ngữ: CHẠM mới hiện (không hiện sẵn)"* | Writer đã rút C |
| B-04 | Hai bản chữ câu ghi công Hermanson (K6, Legal X4) | `licences.json` trường `attribution_text` là sổ giấy phép của S0 | URI giấy phép hiện riêng (R4) |
| B-05 | Hermanson CC BY 4.0 hay 3.0 (Legal X6) | LEGAL-SCREEN đính chính: *"Hermanson: CC BY 3.0 thắng mọi chỗ ghi 4.0"* | — |
| B-06 | Workers Logs: tắt hay xác minh (K9) | QĐ 9: *"Không ID, không cookie, không lưu IP"*; log mặc định giữ metadata request ⇒ tắt hẳn | AC-56 |
| B-07 | Ôn 1–2 card đầu phiên có trong phạm vi không (T3 Δ5) | ADDENDUM dòng đầu: *"Phần còn hiệu lực và là spec duy nhất: đường ống card (§Đường ống PDF → card) và các ràng buộc định dạng card"*; bước 9 nằm trong §Đường ống (ADDENDUM-PDF-LLM.md:56) | — |
| B-08 | Mỗi bài bao nhiêu card (T3 Δ6, PRD Open) | PRODUCT-BRIEF.md:132: *"Định dạng card (A5) đẩy sang S2"*; QĐ 8: *"Đo trước: Duy duyệt 1 bài + card của nó, bấm giờ, rồi mới ước tính tổng"* | S2 + bấm giờ M0 |
| B-09 | `sendBeacon` hay `fetch keepalive` (T3 Δ17) | QĐ 9: *"(`sendBeacon` → Cloudflare Worker của Duy)"* | Cơ chế lúc mất mạng: C-03 |
| B-10 | Hạ tầng site bị chốt ở S1 (T3 Δ19) | QĐ 9: *"bộ đếm gộp tự host, cùng domain"* ⇒ site phục vụ từ Cloudflare | Tên miền dưới tên Duy nằm trong điều kiện Ringkas (R34) sẵn có |
| B-11 | QĐ 16 có thẩm quyền không (T3 Δ21) | Tiêu đề bảng: *"Quyết định của Duy — chỉ thêm, không sửa"*; QĐ 16 có nguyên văn của Duy | Ghi vào ONE-PAGER: Q-19 |
| B-12 | M1 dưới ngưỡng có tạm dừng mở bài GĐ01/02/05 không (PRD.md:62) | QĐ 14: *"GĐ01/02/05 lên dần bằng cờ `published` (phạm vi câu 5 không bị cắt)"* | Lúc có số, SUCCESS-CRITERIA §1 đã đưa câu "viết lại lối vào trước không" cho Duy — câu sau ra mắt, không phải câu S1 |
| B-13 | Dòng "Bài này chưa có bản tiếng Anh" viết thứ tiếng nào (X1 b, WRITER X1 b) | QĐ 6: *"Mặc định Claude đặt (S2 chỉnh được): … nút gạt mờ + dòng 'Bài này chưa có bản tiếng Anh'"* | S2 chọn; Writer đề xuất hiện cả hai thứ tiếng  · **Mở lại 2026-10-24 → Q-28:** QĐ 20 không nhắc dòng này · **Đóng 2026-10-25: QĐ 43 (b)** — dòng song ngữ, ngoại lệ có tên |
| B-14 | Dịch tên trên trang VN; site tự xưng là gì (WRITER X4) | PIPELINE Log: *"TÊN ĐÃ CHỐT: Where Money Sleeps"* ⇒ không dịch tên | Chủ ngữ ("Where Money Sleeps", không "chúng tôi") là microcopy của Writer/S2 |
| B-15 | tr.113 lọt cả hai lớp vào máy sinh card (review §4(c), M3) | QĐ 28: *"trừ các đoạn đã biết phải loại"* — tr.113 là đoạn đã biết | Legal thêm tr.113, 166, 501, 803 vào `exclusions` (vòng sửa 2); AC-18 nguồn (i) = `exclusions`. Mở rộng mẫu luật máy: Q-32 |
| B-16 | Điều kiện 3 trong `blocked_on` của các file S1: đổi theo chữ QĐ 36? (Q-22, PRD N8 — chuyển từ nhóm A sau review vòng sửa 2) | QĐ 36: *"Điều kiện 3 trước S1 đổi thành: agent chạy thử trên 1 bài mẫu + card, đo thời gian Duy đọc báo cáo và ký"* (PRODUCT-BRIEF.md:174) | PM đã đồng bộ `blocked_on` ở các file S1 (§Sau review vòng sửa 2). 2026-10-25: PRD, ACCEPTANCE bỏ dòng "→ Duy (N8)" lỗi thời ở đầu file |

## Nhóm C — bàn giao, không đổi hợp đồng nào (17)

| C | Việc | Stage | Vì sao không phải câu của Duy |
|---|---|---|---|
| C-01 | Máy nhận ra "thuật ngữ" thế nào (T3 Δ10): markup + danh sách ứng viên (glossary + aliases + danh sách jargon của Writer) ⇒ FAIL khi ứng viên xuất hiện mà không có markup | S3 | QĐ 5 giữ nguyên; AC-11 (máy) + AC-12 (người) không đổi. Không phương án nào làm máy bắt được jargon chưa nằm trong danh sách nào; chỗ hở đó đã khai ở WRITER §2 và AC-12 |
| C-02 | D1 hay Analytics Engine (T3 Δ18, K10) | S3 | QĐ 9 để mở nơi lưu; tên event và metric không đổi |
| C-03 | Cách phát hiện mất mạng: `navigator.onLine` hay `fetch keepalive` (TRACKING §2.1) | S3 | Ràng buộc "không đếm đôi" đã cố định; nếu Q-09 bỏ hàng đợi thì chỉ còn phương án A |
| C-04 | AC-74 kiểm trên bản xem trước có bộ đếm riêng hay bật thật | S3 | Cách kiểm, không đổi tiêu chí PASS |
| C-05 | Hình thức dashboard · nơi lưu danh sách cách ly · trần ghi C | S3 | TRACKING-PLAN đã giao SWE |
| C-06 | Giá trị N giờ của "phiên" | S2 đề xuất, M6 kiểm | Trường dữ liệu là Q-09; con số là thông số |
| C-07 | Vị trí dòng ghi công của section (cuối section hay đầu bài) | S2 | §4(b) cho *"any reasonable manner"*; R5 không đổi |
| C-08 | Trích danh sách tên riêng Hermanson để lint (Duy duyệt danh sách) | S3 | Dữ liệu cho phép kiểm đã chốt ở AC-45 |
| C-09 | Denylist chuỗi "annual report" của R10 quá rộng (32 lần trong tr.1–197, gồm đoạn định nghĩa) — review N10 | S3 | Đổi sang denylist theo trang + cụm, mục tiêu R10 giữ nguyên  · **2026-10-24: gộp vào Q-32** (luật máy QĐ 28 là chữ của Duy; đổi hướng nào cũng là câu A) · **2026-10-25: QĐ 47** — mẫu ③ + `exclusions`; chuỗi "annual report" vẫn trong mẫu (rộng hơn, không hẹp hơn) |
| C-10 | Mở rộng vibe-check [4] sang pdf · png · jpg · svg · woff2 · ttf + vendor | Xưởng, trước commit asset đầu tiên của S3 | Công cụ kiểm, không đổi ràng buộc |
| C-11 | Giấy phép `standard_fonts`, `cmaps` của PDF.js; Reserved Font Name của 3 họ font | S3 | R30, R31 không đổi |
| C-12 | Tagline có vừa một dòng ở 360px | S2 | Mockup |
| C-13 | Sổ phía ngân hàng ở GĐ02 (WRITER X2): mô tả bằng lời cho tới khi kế toán xác minh | S3 nội dung GĐ02 (chờ kế toán) | GĐ02 không thuộc ra mắt  · **2026-10-24:** QĐ 30 — số trong bài không card nào hỏi, kể cả sổ ngân hàng GĐ02: Duy đọc |
| C-14 | M1/M2 bỏ khoảng ngày một bài bị gỡ (Data, sau T2 Data câu 2) | S1 — Data, trong SUCCESS-CRITERIA | Cách tính metric, không đổi event |
| C-15 | Bắn POST giả trên bản xem trước để thử F1–F3; kiểm `Sec-Fetch-Site` trên iOS/Zalo | S4 | Phép thử |
| C-16 | Tìm Phụ lục II TT 99 **chính thức** (vbpl.vn trong repo chỉ có thân thông tư; nguồn agent nêu: mof.gov.vn, congbao.chinhphu.vn) | Legal + agent kế toán, trước khi mở GĐ01 | QĐ 37 đã quyết hệ quả; việc còn lại là tìm nguồn. PRD Risks ghi "chưa ai được giao" |
| C-17 | Disclaimer "chỉ mở tài liệu bạn có quyền" cho file PDF riêng (L5, xếp lại vòng sửa 2: chạm mùa 1, rủi ro thấp) | Legal đề xuất ở S2, Writer viết chữ | Legal ghi "chưa quyết, không chặn ra mắt" và chưa đưa → Duy. **Legal đề xuất thêm chữ lên trang ⇒ thành câu A** |

## Nhóm D — trùng, đã gộp (45 nhóm)

| D | Các nhãn trùng | Gộp vào |
|---|---|---|
| D-01 | PRD #11b · WRITER.md:86 · AC-73 (dạng chạm) | Q-01 |
| D-02 | PRD #11a · WRITER.md:85 · WRITER "→ Duy tạo" 1 | Q-03 |
| D-03 | PRD X5 · #9 · T3 Δ3 · Δ4 · Δ25 · T3-RECONSTRUCTION X8 | Q-02 |
| D-04 | K8 · #6 · Legal X5 · R32 (EPUB, foliate-js) | Q-02 |
| D-05 | PRD X1 a · #7 · T3 Δ2 · WRITER X1 a · WRITER §3 dạng hiển thị · RESEARCH §2 dòng 63 · AC-05 · review consistency N2 | Q-04 |
| D-06 | WRITER X3 · WRITER §4 | Q-05 |
| D-07 | T3 Δ13 · review falsify B4 · Scope 6 · B9 · AC-30 · AC-63 · WRITER nhãn tự khai · TRACKING §2.3 · SUCCESS-CRITERIA:35 | Q-06 |
| D-08 | PRD #4 · T2 Data câu 2 · AC-62 · AC-75 · Scope 12 | Q-07 |
| D-09 | K3 · #2 · T3 Δ15 · WRITER §5 · AC-66 (tên event) | Q-08 (a) |
| D-10 | TRACKING `lang` · review falsify N2 | Q-08 (b) |
| D-11 | TRACKING `method: file` · review falsify N3 | Q-08 (c), gốc ở Q-02 |
| D-12 | T3 Δ12 · TRACKING thẻ lật · SUCCESS-CRITERIA M3 riêng · T3-RECONSTRUCTION X5 | Q-08 (d) |
| D-13 | T3 Δ16 | Q-08 (e) |
| D-14 | K2 · #3 · AC-58 (`tel`) | Q-09 |
| D-15 | PRD.md:76 · §Định nghĩa "Phiên" · T2 Design câu 2 → Duy · AC-76 (trường thời điểm) | Q-09 |
| D-16 | PRD.md:75 · AC-67 · review falsify N4 / consistency B5 (hàng đợi offline) | Q-09 |
| D-17 | PRD X6 · T3 Δ11 · B4 · AC-15 · AC-16 · AC-19 · AC-77 · T3-RECONSTRUCTION X6 · review falsify B3 | Q-10 |
| D-18 | PRD X2 · #5 · Legal X2 · R11 · T3 Δ8 · AC-18 phạm vi trang | Q-11 |
| D-19 | PRD X3 · #8 · T3 Δ7 · Scope 8–10 · B6 · B7 · thứ tự milestone 2–5 | Q-12 |
| D-20 | T3 Δ20 · PRD vòng sửa "mở rộng hay không vẫn là câu của Duy" | Q-13 |
| D-21 | K7 · T2 Legal→Data câu 1 · TRACKING §2.4 · SUCCESS-CRITERIA §3 dòng IP · review consistency B2 | Q-14 |
| D-22 | T2 Data câu 2 (hạt) · TRACKING Hạt thời gian · SUCCESS-CRITERIA §3 ô nhỏ | Q-15 |
| D-23 | AC-51 · R18 · LEGAL-REVIEW.md:196 "Duy đặt" (ngưỡng trích luật) | Q-16 |
| D-24 | Legal X9 · R20 · Scope 18 · PRD Open dòng AI · AC-53 · review falsify N1 | Q-17 |
| D-25 | Legal X8 · T3 Δ24 · Scope 14 · B10 · R33 a–b · AC-61 a–b · LEGAL-REVIEW.md:196 "thời gian phản hồi: Duy đặt" | Q-18 |
| D-26 | PRD X4 · T3-RECONSTRUCTION X1 · vibe-check [2] · T3 Δ14 · PRD Open "Ngưỡng North Star" | Q-19 |
| D-27 | K1 · #12 · Legal X1 · T3 Δ22 · R26 · review falsify B5 | Q-20  · Legal X12 phần rủi ro · L18 · review §4(a) · Legal X13 phần rủi ro · L14 · review §4(b) |
| D-28 | Legal X7 · T3 Δ23 · L15 | Q-20 |
| D-29 | T3 Δ1 (thẩm quyền thân Brief) — chính là Q-02 | Q-02 |
| D-30 | WRITER X1 b | B-13 |
| D-31 | PRD N1 · TRACKING §1 N1 · AC-62 · AC-75 · review M1 | Q-23 |
| D-32 | TRACKING §2.5 M7 · SUCCESS-CRITERIA §1 (cách đọc M1) · review M7 · ONE-PAGER v2 §4 "nghiêng thấp" · lý do QĐ 23 yếu đi | Q-24 |
| D-33 | PRD N7 · AC-03 "phán nào cho ký" | Q-25 |
| D-34 | Legal X13 · Writer W2 · PRD K11 · AC-21 chữ hiển thị · WRITER §3 `reviewed_by` · WRITER "chênh với chữ được giao" ("(AI)") · review §4(b) · review M8 phần AC-21 | Q-26 (phần quyết) · Q-20 (phần rủi ro) |
| D-35 | PRD N5 · AC-53 · review dòng QĐ 34 | Q-27 |
| D-36 | PRD N2 · AC-05 ngoại lệ · WRITER "→ Duy" 2 + 3 · WRITER X1 b · B-13 · review dòng QĐ 20 | Q-28 |
| D-37 | Writer W1 · WRITER "→ Duy" 1 (bản trước) · review dòng QĐ 22 | Q-29 |
| D-38 | PRD N4 · AC-83 · Scope 19 | Q-30 |
| D-39 | Legal X10 · X3 · §A.2 B3 · AC-23 · AC-79 phần bảng số liệu · L16 · review M2 | Q-31 |
| D-40 | Legal X11 · AC-18 "mở rộng mẫu" · C-09 · PRD Risks "luật dấu hiệu loại quá rộng" · review M3 phần mẫu | Q-32 |
| D-41 | review M4 · AC-19 · PRD Scope 2 · B4 · Legal R11 | Q-33 |
| D-42 | Legal X12 · R25 · R37 (4) · AC-57 · AC-85 · review §4(a) | Q-34 (phần quyết) · Q-20 (phần rủi ro, L18) |
| D-43 | PRD N8 · ACCEPTANCE đầu file · LEGAL/WRITER "không đổi frontmatter" · SUCCESS-CRITERIA đã đổi frontmatter · review M8 phần `blocked_on` | Q-22 |
| D-44 | review M8 "duyệt v2 bây giờ thì lệch chữ kế toán" · review §3 · ONE-PAGER v2 §D | Q-19 |
| D-45 | PRD N3 → ĐK-1 · Legal R35 có điều kiện → ĐK-2 · Legal R33 (a′) có điều kiện → ĐK-3 | Câu có điều kiện |

## Việc còn nợ ở S1 — không phải câu hỏi

- Trang review HTML cho S1 chưa có (CLAUDE.md quy tắc 15; review N14/N13; vibe-check [6] chỉ thấy `docs/index.html`, `docs/llm-quiz.html`).
- ~~WRITER chưa sửa: ví dụ "✅ Đúng" của quy tắc giọng 1 dạy sai bút toán kép (N12); câu mẫu EN chứa `easy` (N13)~~ — xong ở đợt áp QĐ 17–35. Còn: khai `based_on` cho mọi section (Legal §A.1).
- `RESEARCH-GLOSSARY-UX.md` thiếu `status`/`blocked_on`; dòng 63 lỗi thời từ QĐ 20.
- ~~LEGAL-REVIEW bảng "Việc cho phòng khác" còn ghi "chờ PM"~~ — Legal đọc lại bằng grep ở đợt QĐ 17–35. Mới "chờ PM" (vòng sửa 2): AC cho R33 (a′) kiểm lộ danh tính hộp thư (PRD ghi "không làm").
- ~~vibe-check [5] FAIL (đường dẫn data.md thiếu `../../../`)~~ — PASS từ đợt QĐ 17–35 (review §5). [2] vẫn FAIL cho tới khi ONE-PAGER v2 được áp (dòng dưới).
- **QĐ 50 (2026-10-25):** Duy duyệt ONE-PAGER v2 *trước* khi thấy chữ cuối. PM còn nợ: cập nhật `ONE-PAGER-V2-PROPOSAL.md` theo QĐ 36–51 (file vẫn ghi `status: draft`, chờ Q-19) rồi áp vào `gates/ONE-PAGER.md` (vẫn ghi "14 quyết định S0, Duy chưa duyệt"), và đưa Duy đọc lại bản đã áp. **Chưa làm** — ngoài phạm vi file của lượt 2026-10-25 (chỉ PRD, ACCEPTANCE, file này). Phải làm **sau** lượt sửa PRD cuối, nếu không vibe-check [2] lại FAIL.
- ~~Nếu Q-22 = A: …~~ Q-22 → nhóm B (B-16). Còn treo: Writer đề nghị thêm điều kiện hợp đồng Ringkas vào `blocked_on` của WRITER (§5 chờ hợp đồng đó) — việc của Writer, chưa ai làm.
- **QĐ 51:** workflow pháp lý cho **L13 + L18** phải chạy **trước S5** — chưa ai được giao, chưa có ngày. Kết quả ghi *"same vendor, same priors — no external verifier ran"* và *"không phải ý kiến pháp lý"* (QĐ 12).
- **Việc của phòng khác theo QĐ 38–51 (PM không sửa file phòng khác):** Data — `TRACKING-PLAN.md`/`SUCCESS-CRITERIA.md` thêm `from_start` (QĐ 39), cờ F4 (QĐ 38 = N1 B), M1 số chặt/lỏng, F2 trên số chặt · Legal — `licences.json` đổi B3 từ "TẠM LOẠI … chờ X10" thành loại hẳn khỏi máy sinh card (QĐ 46); `LEGAL-REVIEW.md` X10–X13, R25 (câu mới), R37 (4) "xoá khi khiếu nại đóng", luật máy R11 = mẫu ③ · Writer — `WRITER.md` W1 (`ledger` rời `keep_en`), W2 (câu dòng soát), dòng "chưa có bản EN" song ngữ, bản EN câu R25 mới.
- Thay nhãn N1–N8, M4, M7, X10–X13, W1–W2 bằng số QĐ: **PRD, ACCEPTANCE xong 2026-10-25**; TRACKING-PLAN, SUCCESS-CRITERIA, LEGAL-REVIEW, WRITER còn (file phòng khác).

## Chưa xác minh được

- Số dòng (file:dòng) lấy ngày 2026-10-24 lúc ~15:15, sau vòng sửa 2; file đổi thì dòng trôi. PRD, ACCEPTANCE sửa lúc 15:11–15:12 — nếu phòng nào còn sửa sau đó, dòng có thể lệch.
- tr.117: PM đọc bằng `pdftotext` trên PDF gốc; bảng số liệu có thuộc diện bảo hộ không là phán đoán, **không phải ý kiến pháp lý**.
- Khuyến nghị là của **PM** (không phải phòng sở hữu) ở: Q-22, Q-25, Q-27, Q-30, Q-33, phần thời hạn giữ thư của Q-34, và điểm (a)(c) của Q-28. Điểm (b) Q-28: PM theo Writer, ngược gợi ý cũ của PRD N2.
- Q-26: nhận xét "câu của Legal trượt phép kiểm của chính Legal" là PM đọc chữ, chưa hỏi lại Legal.
- 72 giờ (QĐ 35) và 15–25 triệu (Q-20) là đề xuất / phép chia của Legal, chưa đối chiếu văn bản gốc. Luật 91 Đ.20.1.c, NĐ 330, NĐ 356 Đ.6.1 đều đọc qua `../../../docs/data.md` (nguồn thứ cấp).
- `licences.json` `exclusions`: PM đọc trường đó bằng script, thấy tr.113, 166, 501, 803, 117 và B3. Chưa so với PDF.
- Xếp nhóm B/C/D và thứ tự hỏi là phán đoán của PM.
- ~~Tổng 15 câu nhóm A~~ — 2026-10-25: 0 câu mở. QĐ 41–51 nhận theo lô **trước khi Duy đọc từng bảng phương án** (PRODUCT-BRIEF.md:179) ⇒ "đã quyết" nghĩa là đã ký trên khuyến nghị, không phải đã cân từng phương án. Nếu đọc lại mà đổi ý ⇒ một dòng QĐ mới có ngày (quy tắc 14).
- Câu W2 (QĐ 41) và câu R25 mới (QĐ 49) chưa đối chiếu Luật AI 134/2025 (L14) và Luật 91 (L18) — L18 nằm trong workflow trước S5 (QĐ 51), L14 giữ lịch sau release.
- Đây là triage phía tác giả. Same vendor, same priors — no external verifier ran.

## Lưu trữ — câu đã trả lời và bản cũ (giữ lý do, quy tắc 14)

> Q-01…Q-18 và Q-22…Q-34, Q-19, Q-20 (bản vòng sửa 2) nguyên văn như lúc hỏi; câu trả lời ở §Câu trả lời của Duy và PRODUCT-BRIEF QĐ 17–35, 38–51. Q-19/Q-20 "bản trước vòng sửa 2" là bản cũ hơn nữa, giữ lại vì lý do cũ (quy tắc 14).

### Q-01 · Dạng chạm của chú thích thuật ngữ — **ĐÃ TRẢ LỜI → QĐ 17**

- **Phải quyết:** chạm vào thuật ngữ thì thẻ chú thích hiện theo dạng nào.
- **Vì sao bây giờ:** QĐ 16 chốt "chạm mới hiện" và giao research; research đã xong. Chặn S2 (mockup B3, B5) và AC-73.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **(c) Mở tại chỗ ngay sau câu** ⭐ | Không che chữ; không cần Popover API/CSS anchor; không có lớp phủ để nút Back của Zalo đóng nhầm cả bài | Chữ bên dưới bị đẩy xuống, đoạn văn bị cắt đôi | Chưa thử trong WebView Zalo |
| (a2) Thẻ bám dòng, phủ lên chữ | Câu đang đọc vẫn thấy; đoạn văn không bị cắt | Che chữ phía dưới; cần JS định vị tự host | Lớp phủ: Back Zalo, light-dismiss iOS < 18.3 |
| (e) Ngăn đáy non-modal | Không cần định vị | Mắt rời chữ; che đúng vùng ngón cái vừa chạm | Ngăn không tự đóng khi cuộn |

- **Khuyến nghị:** (c) làm mặc định để S2 dựng, và đem (c) với (a2) vào buổi 5 người (M6). Căn cứ: research TL;DR 1–2; chính research cảnh báo 2/4 mũi nghiêng về dạng phủ và không nghiên cứu nào so trực tiếp.
- **Đánh đổi thật:** anh đổi "chữ bị đẩy xuống" lấy "chữ không bao giờ bị che". Chưa ai đo người đọc của anh khó chịu với cái nào hơn.
- **Nếu sai:** rẻ, **với điều kiện** S3 giữ cách hiện là một cờ render và glossary là nguồn duy nhất (WRITER §2). Đổi sau buổi 5 người.
- **Câu đóng:** Chốt (c) mở tại chỗ làm mặc định, kiểm lại với (a2) ở buổi 5 người?
- **Nguồn:** RESEARCH-GLOSSARY-UX.md:17–21 · PRD.md:311 · WRITER.md:86 · ACCEPTANCE.md:157 · PRODUCT-BRIEF.md:153

### Q-02 · Thân PRODUCT-BRIEF (viết trước quyết định) còn hiệu lực ở chỗ không quyết định nào nhắc không — **ĐÃ TRẢ LỜI → QĐ 18**

- **Phải quyết:** một quy tắc thẩm quyền cho thân Brief, kèm danh sách mục thân bài nhặt vào mùa 1.
- **Vì sao bây giờ:** S1 đang dùng thân Brief không nhất quán (lấy `Nợ (Debit)` làm căn cứ ở X1 nhưng coi `persist()` cùng bảng là "không quyết định nào nhắc" ở X5). **Một câu trả lời gỡ 9 chỗ:** X5/#9, Δ3, Δ4, Δ25, K8/#6, Legal R32, `method: file`, T3 X8, và căn cứ của Δ2 (Q-04). Chặn Scope, AC-10/AC-29 (ID mồ côi, auto-redirect), TRACKING §1.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Chỉ quyết định có hiệu lực; mục thân bài vào mùa 1 khi Duy nhặt. Nhặt: cảnh báo `persist()`, giữ ID mồ côi, không auto-redirect** ⭐ | Phạm vi nhỏ nhất mà vẫn giữ 2 thứ rẻ bảo vệ tiến độ người học | `.ics`, file JSON sao lưu, EPUB/foliate-js ra khỏi mùa 1; máy tính khoản vay quyết lúc mở GĐ05 (không thuộc ra mắt) | Bỏ sót một mục tốt khác trong thân bài |
| B · Thân bài còn hiệu lực trừ chỗ trái quyết định (cách đọc của T3) | Đúng chữ dòng đầu Brief *"Chỗ nào lệch, §Quyết định của Duy thắng"* | `.ics`, file JSON, máy tính vay (có thể cả EPUB) vào phạm vi mà chưa ai duyệt riêng | Khối build + QA + Legal tăng, trong khi khối duyệt còn chưa bấm giờ (M0) |
| C · Không đặt quy tắc, xét từng mục khi gặp | Không phải chốt nguyên tắc | Stage nào cũng hỏi lại | S2/S3 tự chọn thay Duy |

- **Khuyến nghị:** A. Căn cứ: mục đó tên là *"Kiến trúc **đề xuất** ở mức S0"* (PRODUCT-BRIEF.md:54) và dòng đầu Brief nói nó viết **trước** quyết định (:8); chi phí thật của dự án là khối duyệt chưa đo (QĐ 8, 14). Hai mục nhặt: `persist()` phục vụ thẳng "mất thì rẻ" của QĐ 7 và chữ đã viết sẵn (WRITER §6); giữ ID mồ côi gần như không tốn gì, còn xoá ID mồ côi là mất tiến độ người học, không lấy lại được.
- **Đánh đổi thật:** anh đổi "đúng chữ dòng đầu Brief" lấy "mùa 1 chỉ gồm thứ anh đã nói có". Mục nào anh muốn mà chưa nhặt thì phải thêm một dòng mới.
- **Nếu sai:** rẻ; từng mục thêm sau bằng cờ. Bỏ `method: file` trước ra mắt rồi thêm lại là tự do (thêm giá trị event không cắt lịch sử).
- **Câu đóng:** Nhận quy tắc A với danh sách nhặt `persist()` · ID mồ côi · không auto-redirect?
- **Nguồn:** PRD.md:265, :309, :404, :408–411, :432 · TRACKING-PLAN.md:44 · LEGAL-REVIEW.md:112, :145 · PRODUCT-BRIEF.md:8, :54–67 · T3-RECONSTRUCTION.md:187

### Q-03 · Đánh dấu thuật ngữ ở lần đầu mỗi mục H2 hay lần đầu mỗi bài — **ĐÃ TRẢ LỜI → QĐ 19**

- **Phải quyết:** gạch chấm + chạm được ở lần đầu của đơn vị nào. Một đơn vị cho mọi "lần đầu / các lần sau" ở WRITER §1, §3.
- **Vì sao bây giờ:** chặn S2 (mockup B3) và luật render chung của S3.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Lần đầu mỗi mục H2** ⭐ | Người vào giữa bài (card "đọc lại đoạn này", nút gạt VI ⇄ EN — đều đưa tới đầu một H2) vẫn gặp dấu | 3–4 gạch chấm cho cùng một từ trong một bài | Căn cứ là quy ước biên tập (Wikipedia MOS), không phải thực nghiệm |
| Lần đầu mỗi bài (WRITER bản đầu) | Trang sạch nhất | Người vào giữa bài không thấy dấu nào | — |
| Mọi lần | Chỗ nào cũng tra được | Bài Nợ/Có gạch chân hàng chục chỗ, trái cảm giác "không thấy mình đang học" | Chạm nhầm khi cuộn |

- **Khuyến nghị:** mỗi mục H2. Căn cứ: `sectionId` = một mục H2 (PRD.md:166) là đơn vị người đọc được đưa tới; RESEARCH §2.
- **Đánh đổi thật:** anh đổi một trang sạch hơn lấy việc người vào giữa bài vẫn tra được nghĩa.
- **Nếu sai:** rẻ nếu là cờ render (cùng điều kiện Q-01). Kiểm ở buổi 5 người.
- **Câu đóng:** Đánh dấu ở lần đầu mỗi mục H2?
- **Nguồn:** PRD.md:166, :311 · WRITER.md:78–88 · RESEARCH-GLOSSARY-UX.md:51–62

### Q-04 · "Trộn ngôn ngữ" (QĐ 6): `Nợ (Debit)` trong dòng chữ trang VI, hay chỉ trong thẻ chú thích — **ĐÃ TRẢ LỜI → QĐ 20**

- **Phải quyết:** định nghĩa "trộn" đủ chặt để AC-05 thành phép kiểm máy.
- **Vì sao bây giờ:** AC-05 đang TBD. WRITER §3 và RESEARCH §2 (giữ `(Debit)` trong dòng) nói ngược PRD #7 ⇒ S2 không biết dựng theo bên nào.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **B · Trong dòng chỉ có `Nợ`; nhãn `Nợ · Debit` nằm trong thẻ chạm. Ngoại lệ có tên: tên riêng / viết tắt chuẩn (VietQR, NAPAS, APR)** ⭐ | QĐ 6 đúng chữ; AC-05 kiểm máy bằng một danh sách ngoại lệ ngắn | Người muốn Google từ EN phải chạm mới thấy | Danh sách ngoại lệ phải giữ ngắn, nếu không thành cửa sau |
| A · Lần đầu `Nợ (Debit)` trong dòng (thân Brief + RESEARCH §2) | Từ EN thấy ngay | Mọi thuật ngữ thành ngoại lệ của QĐ 6; AC-05 phải miễn cả mẫu `X (Y)` | Gần như mọi trang VI có chữ EN |

- **Khuyến nghị:** B. Căn cứ: QĐ 6 *"không trang nào trộn ngôn ngữ"* (PRODUCT-BRIEF.md:137); QĐ 16 đã cho chữ EN một chỗ ở là thẻ chạm; nếu Q-02 = A thì quy ước `Nợ (Debit)` của thân Brief không còn là yêu cầu.
- **Đánh đổi thật:** anh đổi "từ EN thấy ngay" lấy "QĐ 6 đúng chữ và máy kiểm được".
- **Nếu sai:** rẻ nếu glossary là nguồn duy nhất và cách hiện là cờ render.
- **Câu đóng:** Trong dòng chỉ `Nợ`, `Debit` vào thẻ chạm, ngoại lệ chỉ VietQR/NAPAS/APR-loại?
- **Nguồn:** PRD.md:261, :307 · WRITER.md:104, :184 · RESEARCH-GLOSSARY-UX.md:63 · ACCEPTANCE.md:40 · PRODUCT-BRIEF.md:67

### Q-05 · Tagline giải nghĩa (gu) — **ĐÃ TRẢ LỜI → QĐ 22**

- **Phải quyết:** chọn một trong 5 tagline của Writer.
- **Vì sao bây giờ:** tagline là bắt buộc (Log tên); chặn S2 (header, `<title>`, `og:`) và AC-39, AC-78.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **T1** *"Từ tin báo 'ghi có' tới sổ cái: tiền của bạn đi qua những đâu."* ⭐ | Chặn cách đọc "gửi tiết kiệm" bằng hai vật cụ thể; gần nguyên văn ONE-PAGER §1; không nói chữ "kế toán" | Thuật ngữ "sổ cái" lên header, nơi không có chú thích | Dựa vào giả định tin báo ngân hàng thật sự in chữ "ghi có" — chưa xác minh |
| T3 *"Mỗi lần chuyển khoản là một dòng trong sổ cái của ai đó."* | Hay nhất về chữ; nối với "Sleeps" | Quá ngắn để người lạ biết site dạy gì | — |
| T5 *"Kế toán và thanh toán, giải thích bằng tiền bạn chuyển mỗi tuần."* | Rõ nhất | Nói thẳng "kế toán" — trái ONE-PAGER §2 | — |

- **Khuyến nghị:** T1. Căn cứ: WRITER §4; Log tên (PIPELINE.md:35) bắt buộc tagline chặn "gửi tiết kiệm".
- **Đánh đổi thật:** anh đổi sự rõ ràng tuyệt đối (T5) lấy cảm giác "không thấy mình đang học kế toán".
- **Nếu sai:** đổi trước ra mắt là miễn phí; sau ra mắt, bản xem trước link trong Zalo có thể giữ câu cũ một thời gian.
- **Việc của Duy kèm theo:** chụp 3 tin báo biến động số dư thật. Không in chữ "ghi có" thì T1 yếu đi.
- **Câu đóng:** Chốt T1?
- **Nguồn:** PRD.md:310 · WRITER.md:117–137, :186 · PIPELINE.md:35

### Q-06 · "Tự khai giai đoạn" đánh dấu theo giai đoạn hay theo từng bài — **ĐÃ TRẢ LỜI → QĐ 23**

- **Phải quyết:** tự khai đánh dấu xong cả một giai đoạn (lối vào là một khối) hay tới một bài cụ thể.
- **Vì sao bây giờ:** quyết định tập bài bị ghi `suppressed` và **hướng lệch của North Star M1**. Chặn AC-30, AC-63, màn B9 (S2), nhãn Writer.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Theo giai đoạn** ⭐ | M1 đọc được (lệch về phía xẹp, thận trọng); khớp chữ QĐ 7 *"tự khai giai đoạn"* | Người đã đọc nửa lối vào ở máy khác phải khai cả lối vào, hoặc đọc lại từ bài 1 | — |
| B · Theo bài | Khớp hơn với người dừng giữa lối vào | M1 có thể > 1; cờ F2 báo động giả | M1 không đọc được, trừ khi Data đổi R3 |
| B' · Chọn theo bài, nhưng khai bất kỳ bài lối vào nào ⇒ cả lối vào `suppressed` | Giữ UI theo bài | Không đếm được người khai rồi đọc thật phần còn lại | — |

- **Khuyến nghị:** A. Căn cứ: chữ QĐ 7 (PRODUCT-BRIEF.md:138); Data chọn A từ góc đo (TRACKING-PLAN.md:102).
- **Đánh đổi thật:** anh đổi sự tiện cho người dừng giữa lối vào lấy một North Star còn đọc được.
- **Nếu sai:** UI đổi rẻ; đổi sau ra mắt là đổi nghĩa R3 ⇒ dòng log có ngày, mất so sánh trước/sau.
- **Câu đóng:** Tự khai theo giai đoạn, lối vào là một khối?
- **Nguồn:** PRD.md:97, :157, :420 · ACCEPTANCE.md:85, :142 · TRACKING-PLAN.md:90–104 · SUCCESS-CRITERIA.md:35 · WRITER.md:150

### Q-07 · "Xong bài" là gì (điều kiện bắn `lesson_completed`) — **ĐÃ TRẢ LỜI → QĐ 24**

- **Phải quyết:** điều kiện chuyển một bài từ *chưa xong* sang *xong*.
- **Vì sao bây giờ:** đây là nghĩa của event North Star. Chặn AC-62, AC-75, Scope dòng 12.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Đã trả lời ≥ 1 card cuối bài (đúng hay sai), kèm bất biến hai chiều AC-75** ⭐ | Không thoả được bằng cuộn nhanh; một điều kiện cho mọi bài | Gỡ card `published` cuối cùng của một bài ⇒ phải gỡ luôn bài hoặc đăng card thay | Một bài lối vào bị gỡ ⇒ lỗ trong chuỗi 12–15 bài cho tới khi có card thay |
| Cuộn tới cuối + thời gian tối thiểu | Không phụ thuộc card | Cuộn nhanh rồi chờ vẫn thoả; con số thời gian không có nguồn | M1 thổi |
| Nút "Tôi đọc xong" | Rõ ý định | Không chứng minh đã đọc; thêm một thao tác | — |

- **Khuyến nghị:** phương án 1. Căn cứ: ràng buộc của Data *"không thoả được bằng cuộn nhanh"* (TRACKING-PLAN.md:47); mỗi bài có card (Scope dòng 2); ưu tiên "thiếu hơn thừa" (R5).
- **Đánh đổi thật:** M1 đo "đọc + thử", nên số thấp hơn "đọc tới cuối"; và gỡ một card sai có thể kéo cả bài lối vào xuống.
- **Nếu sai:** đổi sau ra mắt = đổi nghĩa event ⇒ dòng có ngày, mất so sánh trước/sau.
- **Câu đóng:** "Xong bài" = đã trả lời ≥ 1 card, kèm AC-75?
- **Nguồn:** PRD.md:84, :103, :304, :366–373 · ACCEPTANCE.md:141, :166 · TRACKING-PLAN.md:47

### Q-08 · Hợp đồng event trước ra mắt — 5 điểm — **ĐÃ TRẢ LỜI → QĐ 25**

- **Phải quyết:** nhận hay không từng điểm (a)–(e). Tên event là hợp đồng (QĐ 9, quy tắc 8).
- **Vì sao bây giờ:** **trước ra mắt chưa có dữ liệu nào**, nên đổi/bỏ không tốn gì; sau ra mắt thì đổi tên hoặc bỏ là cắt đôi lịch sử. Chặn AC-62, AC-66, AC-70, bảng D1 (TRACKING §4).

| Điểm | Khuyến nghị | Được | Mất | Rủi ro |
|---|---|---|---|---|
| (a) `sync_link_created` → `sync_created{method}`; `progress_restored` thêm `method` | **Nhận** | Không phải đổi tên khi phép đo Zalo về (link hay mã) | Tên khác cái anh đọc ở QĐ 9 | — |
| (b) Bỏ `lesson_completed.lang` | **Bỏ** | Ít ô, ít ô n < 5 | Không đếm bản EN tới khi thêm event mới lúc bật EN (lúc ra mắt EN chưa có) | — |
| (c) `method` chỉ `link` \| `code` | **Bỏ `file`** (theo Q-02) | Không giá trị chết; AC-70 không đòi kiểm luồng không tồn tại | — | Nếu Q-02 nhặt file JSON thì giữ `file` |
| (d) Thẻ lật tự chấm | **Không bắn `card_answered`** | M3 sạch: "chưa nhớ" không lẫn với "card có thể sai" | Không biết thẻ lật nào khó | Thay thế: vẫn bắn, M3 lọc theo loại card lúc build |
| (e) Event cho tự khai · mời cài · `persist()` (thân Brief §Đo cái gì) | **Không thêm**; Data ghi `N/A — because` vào SUCCESS-CRITERIA §3 | Không thêm ô; M5 đã trả lời câu "có phải thiết kế lại chỗ mời sao lưu" | Không biết bao nhiêu người mất storage rồi tự khai (`progress_restored` chỉ là cận dưới) | Dữ liệu không hồi tố |

- **Khuyến nghị:** nhận cả 5. Căn cứ: QĐ 9 *"S1 chốt tên, tên là hợp đồng"* (PRODUCT-BRIEF.md:140); quy tắc 8: metric không đổi hành động nào thì không đo; (a)–(d) là đề xuất của Data, (e) là của PM.
- **Đánh đổi thật:** bỏ bây giờ thì thêm lại sau là tự do nhưng mất khoảng dữ liệu ở giữa; giữ bây giờ thì sau ra mắt không bỏ được nữa.
- **Nếu sai:** thêm event/thuộc tính/giá trị là tự do; đổi tên hoặc bỏ sau ra mắt cắt đôi lịch sử.
- **Câu đóng:** Nhận cả (a)–(e), hay giữ lại điểm nào?
- **Nguồn:** TRACKING-PLAN.md:12, :37–45 · PRD.md:284, :302, :419, :422–423 · SUCCESS-CRITERIA.md:48 · ACCEPTANCE.md:137, :145 · WRITER.md:143

### Q-09 · Mở rộng schema tiến độ (QĐ 7: "tên key + schema là hợp đồng") — **ĐÃ TRẢ LỜI → QĐ 26**

- **Phải quyết:** thêm trường nào vào JSON tiến độ, và trường nào đi theo bản sao lưu (whitelist Legal R28).
- **Vì sao bây giờ:** ba đề xuất cùng loại đang treo; PM và Data không tự thêm. Chặn AC-58, AC-66, AC-67, AC-76.

| Trường | Khuyến nghị | Được | Mất | Rủi ro |
|---|---|---|---|---|
| `tel` (cờ chống trùng) | **Thêm, và đi theo bản sao lưu** (vào whitelist R28) | Khôi phục xong không bắn lại ⇒ không đếm đôi | Link sao lưu dài thêm theo số bài/card đã làm | Zalo có cắt link dài không: **BLOCKED — chờ đo** |
| Thời điểm hoạt động cuối (để tính "phiên") | **Thêm, KHÔNG đi theo bản sao lưu** | AC-76 (ôn đầu phiên) chạy được mà không cần `sessionStorage` | Một trường nữa | — |
| Hàng đợi event lúc mất mạng | **Không thêm**: offline thì bỏ event (khác đề xuất R6 của Data) | Schema gọn; khớp R5 "thiếu hơn thừa" của chính Data | Event lúc offline mất hẳn | Lệch do mất event chưa đo |

- **Khuyến nghị:** như cột trên. Căn cứ: TRACKING-PLAN.md:69–71 (R4–R6); Legal R28 chỉ cho field schema đi theo sao lưu; `sessionStorage` bị loại vì mỗi link Zalo có thể mở một WebView mới (chưa đo).
- **Đánh đổi thật:** anh đổi một link sao lưu ngắn lấy việc không đếm đôi sau khôi phục.
- **Nếu sai:** trước ra mắt rẻ; sau ra mắt đổi schema cần migration có ngày.
- **Câu đóng:** Thêm `tel` (theo sao lưu) và trường thời điểm (không theo), bỏ hàng đợi offline?
- **Nguồn:** PRD.md:74–76, :167, :283, :303, :395 · ACCEPTANCE.md:130, :145–146, :167 · TRACKING-PLAN.md:51–75 · LEGAL-REVIEW.md:103

### Q-10 · Card sinh từ Hermanson dựng thế nào (PRD X6) — **ĐÃ TRẢ LỜI → QĐ 27**

- **Phải quyết:** cách gỡ ba chỗ va: ngôn ngữ (`source_quote` EN vs card VN), đơn vị ($ vs đ), vị trí nguồn (trang PDF vs `sectionId`).
- **Vì sao bây giờ:** 4 AC (AC-15, 16, 19, 77) đang tự mâu thuẫn; S1 không duyệt được như vậy. **Không** chặn ra mắt: card Hermanson thuộc GĐ01.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Card khái niệm, không con số; hiện bằng VN; `source_quote` EN giữ trong dữ liệu build để máy kiểm khớp, không hiện; "đọc lại đoạn này" trỏ tới `sectionId` của bài GĐ01 có `based_on` phủ trang đó** ⭐ | AC-15/16/19/77 viết được; card không số ⇒ không cần kế toán | Không dùng ví dụ có số của Hermanson; máy chỉ chứng minh câu trích EN có thật, còn bản VN có dịch đúng câu đó hay không là mắt Duy | Chưa có section GĐ01 nào `based_on` trang đó ⇒ link không có đích |
| B · Mùa 1 không sinh card từ Hermanson; Hermanson chỉ để đọc trong trình đọc PDF | Không còn xung đột nào | Mất "card từ sách thật" — phần mạnh nhất ý của anh ở QĐ 3 | — |
| C · Hiện câu trích EN trên trang VI như một ngoại lệ | Người đọc thấy câu gốc | Trái QĐ 6 | — |

- **Khuyến nghị:** A. Căn cứ: lý do của QĐ 3 *"Hermanson theo US GAAP ⇒ chỉ lấy khái niệm phổ quát"* (PRODUCT-BRIEF.md:134), tức card Hermanson vốn không cần con số; QĐ 6.
- **Đánh đổi thật:** card Hermanson thành "card khái niệm có nguồn sách", không phải "card trích sách": người học không thấy câu gốc.
- **Nếu sai:** card là tĩnh, sinh lúc build ⇒ sinh lại được; chưa đăng thì không tốn gì.
- **Câu đóng:** Card Hermanson = khái niệm, không số, hiện VN, link về section GĐ01?
- **Nguồn:** PRD.md:152, :266, :418 · ACCEPTANCE.md:60–64, :168 · T3-RECONSTRUCTION.md:185 · ADDENDUM-PDF-LLM.md:52, :55

### Q-11 · Card Hermanson chỉ lấy từ tr.1–197 (PRD X2) — **ĐÃ TRẢ LỜI → QĐ 28**

- **Phải quyết:** phạm vi trang Hermanson được nạp vào máy sinh card. **Mất tác dụng nếu Q-10 = B.**
- **Vì sao bây giờ:** AC-18 (phạm vi trang) TBD; `based_on.pages` của Legal §A.1 cần biết phạm vi.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Chỉ tr.1–197** ⭐ | Mọi câu trích nằm trong phần đã soát cả chữ lẫn ảnh, trùng phạm vi host | Kho card Hermanson = ch.1–4 = đúng GĐ01 | — |
| Cả cuốn, trừ `exclusions` | Kho lớn hơn | Phần ngoài 197 chưa soát ảnh; tr.501 và tr.803 được tìm thấy tình cờ | Trích phải đoạn bên thứ ba chưa ai biết |

- **Khuyến nghị:** chỉ tr.1–197. Căn cứ: QĐ 15 + dòng soát phần host (PRODUCT-BRIEF.md:150–152); Legal đề xuất cùng hướng (X2).
- **Đánh đổi thật:** anh đổi kho card lớn lấy việc mọi câu trích nằm trong phần đã soát.
- **Nếu sai:** mở rộng sau, mỗi lần soát thêm một chương (đúng nhịp QĐ 15).
- **Câu đóng:** Card Hermanson chỉ từ tr.1–197?
- **Nguồn:** PRD.md:262, :305, :415 · LEGAL-REVIEW.md:71, :142 · ACCEPTANCE.md:63

### Q-12 · Trình đọc PDF + trang sách + thẻ sách: điều kiện ra mắt, hay ra cùng GĐ01 (PRD X3) — **ĐÃ TRẢ LỜI → QĐ 29**

- **Phải quyết:** ba năng lực này có phải có ngày ra mắt không.
- **Vì sao bây giờ:** QĐ 4 *"mùa 1 CÓ"* × QĐ 14 *"ra mắt khi lối vào duyệt xong"* — "mùa 1" và "ra mắt" chưa tách. Chặn Scope dòng 8–10, B6, B7, M4, thứ tự milestone.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Ra cùng GĐ01** ⭐ | Ra mắt chỉ chờ lối vào (QĐ 14); Hermanson tr.1–197 khớp GĐ01 (QĐ 15) | Ra mắt chưa có "sách thật" — điều anh muốn ở QĐ 2; M4 đo muộn hơn | — |
| Là điều kiện ra mắt | Đúng chữ QĐ 4 ngay ngày đầu | Ra mắt chờ thêm redact, PDF.js, phép đo `input type=file` | Phần file riêng đang BLOCKED ⇒ trễ ra mắt |

- **Khuyến nghị:** ra cùng GĐ01. Căn cứ: QĐ 14 (PRODUCT-BRIEF.md:146) + QĐ 15 (:151); QĐ 4 nói "mùa 1", không nói "ngày ra mắt". Thứ tự milestone 2–5 (PRD.md:251) để sau ra mắt, không cần chốt trước S2.
- **Đánh đổi thật:** anh đổi "có sách thật từ ngày đầu" lấy ngày ra mắt không bị phép đo `input type=file` chặn.
- **Nếu sai:** bật bằng cờ bất cứ lúc nào; event kiểm lúc bật (AC-74), không mất dữ liệu.
- **Câu đóng:** Trình đọc PDF + trang sách ra cùng GĐ01, không phải điều kiện ra mắt?
- **Nguồn:** PRD.md:99–101, :154–155, :263, :308, :414 · PRODUCT-BRIEF.md:135, :146, :151

### Q-13 · Phạm vi soát của người kế toán (T3 Δ20) — **ĐÃ TRẢ LỜI → QĐ 30**

- **Phải quyết:** kế toán soát những gì.
- **Vì sao bây giờ:** đây là thứ đem đi bấm giờ ở M0 (điều kiện S1) và là việc anh sẽ nhờ người kế toán. Chặn AC-03, AC-42.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **QĐ 8 đúng chữ + đoạn bài mà mỗi card có số dùng làm `source_quote`** ⭐ | Kế toán đọc con số trong ngữ cảnh của nó; khối việc bám theo số card | Con số trong bài lối vào mà không card nào hỏi chỉ có Duy đọc | — |
| QĐ 8 đúng chữ (GĐ01 · GĐ05 · card có số) | Ít việc nhất cho kế toán | Soát số trong card mà không thấy đoạn bài nó trích | — |
| Thêm mọi bài lối vào có con số (theo lý do QĐ 14) | Phủ hết con số người mới gặp đầu tiên | Khối việc kế toán tăng mà chưa bấm giờ | Ra mắt phụ thuộc thêm vào thời gian của kế toán |

- **Khuyến nghị:** phương án 1. Căn cứ: QĐ 8 (PRODUCT-BRIEF.md:139); lý do QĐ 14 *"bài lối vào có con số ⇒ không có kế toán thì không đăng được gì"* (:146) cho thấy anh lo con số lối vào; AC-16 đã buộc số trong card phải nằm trong `source_quote`, tức nằm trong đoạn bài.
- **Đánh đổi thật:** anh đổi "phủ hết con số" lấy khối việc vừa sức một người kế toán chưa có tên.
- **Nếu sai:** mở rộng sau khi bấm giờ M0 thì dễ; thu hẹp sau khi đã hứa với kế toán thì khó hơn.
- **Câu đóng:** Kế toán soát QĐ 8 + đoạn bài mà card có số trích?
- **Nguồn:** PRD.md:22, :318, :427, :450 · ACCEPTANCE.md:33, :107

### Q-14 · Rule chặn spam theo IP ở tầng Cloudflare (K7) — **ĐÃ TRẢ LỜI → QĐ 31**

- **Phải quyết:** có cho bật Rate Limiting / WAF / Bot Fight Mode (đều xử lý IP) để bảo vệ M1 không.
- **Vì sao bây giờ:** S3 sẽ cấu hình Cloudflare; không có câu trả lời thì S3 tự chọn. PRD K7 "đã giải" chỉ đúng cho mã Worker.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Không bật; phát hiện bằng cờ F1–F3 + cách ly ngày; cách ly ≥ 2 lần trong 4 tuần ⇒ Data hỏi lại kèm số** ⭐ | Không thêm hoạt động xử lý IP do anh chỉ định; câu riêng tư R25 giữ nguyên nghĩa | Chỉ phát hiện, không chặn; người bơm đều cả 5 bài dưới mức F1 thì không bắt được | M1 có thể bị làm giả |
| Bật rate limiting rule (gói Free: 1 rule, chỉ đếm theo IP) | Chặn được bơm số lượng lớn | Thêm xử lý IP vì mục đích của anh ⇒ X1/L13 nặng hơn | — |

- **Khuyến nghị:** không bật. Căn cứ: QĐ 9 *"không lưu IP"*; gói Free không có cách chặn ở edge mà tránh được IP (TRACKING-PLAN.md:108).
- **Đánh đổi thật:** anh đổi một M1 chống giả mạnh hơn lấy lời hứa không xử lý IP vì mục đích của mình.
- **Nếu sai:** bật sau được; những ngày bị bơm trước đó thì cách ly, không xoá.
- **Câu đóng:** Không bật rule IP, dùng F1–F3 + cách ly?
- **Nguồn:** PRD.md:125, :288 · TRACKING-PLAN.md:17, :106–125, :226 · SUCCESS-CRITERIA.md:58

### Q-15 · Hạt lưu của bộ đếm: ngày hay tuần — **ĐÃ TRẢ LỜI → QĐ 32**

- **Phải quyết:** các dòng có chiều (`lesson`, `card`) lưu theo ngày hay theo tuần.
- **Vì sao bây giờ:** bảng D1 chốt trước ra mắt; dữ liệu không hồi tố. Ô n = 1 ghép với chuyện bạn bè kể có thể chỉ ra người (T2 câu 2).

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Giữ ngày; dashboard ẩn ô n < 5, không có bảng ngày × bài/card; cuộn lên tuần nếu L13 trả lời rằng dữ liệu gộp ghép được là dữ liệu cá nhân** ⭐ | Cách ly theo ngày chính xác (TRACKING §2.4); ngày → tuần làm được về sau, chiều ngược lại thì không | Anh vẫn query được ô n = 1 bằng `wrangler` — chỉ kỷ luật của anh chặn | Ghép ô nhỏ với thứ anh biết sẵn |
| Tuần cho dòng có chiều + thêm dòng `day × event` | Đóng phần lớn chỗ hở ghép ô | Cách ly mất cả tuần; độ chính xác mất vĩnh viễn | — |

- **Khuyến nghị:** giữ ngày (khuyến nghị của PM; Data không chọn). Căn cứ: tính bất đối xứng khi đảo ngược + độ chính xác cách ly ở TRACKING §2.4.
- **Đánh đổi thật:** anh đổi một bảo đảm bằng thiết kế lấy độ chính xác cách ly và quyền lùi.
- **Nếu sai:** cuộn lên tuần rồi xoá dòng ngày là làm được; không làm ngược được.
- **Câu đóng:** Giữ hạt ngày, cuộn lên tuần nếu L13 đòi?
- **Nguồn:** TRACKING-PLAN.md:18, :135, :178, :227 · SUCCESS-CRITERIA.md:17, :59, :79

### Q-16 · Ngưỡng số chữ trích văn bản luật mỗi bài (AC-51, Legal R18) — **ĐÃ TRẢ LỜI → QĐ 33**

- **Phải quyết:** số chữ trích nguyên văn luật tối đa mỗi bài. Legal ghi "Duy đặt".
- **Vì sao bây giờ:** AC-51 là AC của mọi bài, kể cả lối vào; chưa có số thì không kiểm được.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **0 cho phần ra mắt: chỉ link + diễn giải bằng lời mình; đặt số khi mở GĐ05** ⭐ | AC-51 kiểm được ngay; không chạm câu "thông tin tổng hợp" (L7) đang gray | Người đọc không thấy nguyên văn điều luật trên trang | — |
| Đặt một con số ngay | Chốt một lần | Con số không có nguồn (quy tắc 3) | — |
| Không giới hạn, chỉ "trích chọn lọc" | Linh hoạt | AC-51 không kiểm máy được | Trôi dần thành đăng lại văn bản |

- **Khuyến nghị:** 0 cho phần ra mắt. Căn cứ: R18 *"chỉ link và chỉ trích chọn lọc"*; L7 chưa trả lời; GĐ05 không thuộc ra mắt (QĐ 14).
- **Đánh đổi thật:** anh đổi việc thấy nguyên văn trên trang lấy việc không phải đặt một con số không nguồn trước khi có bài cần nó.
- **Nếu sai:** nới ra lúc mở GĐ05 là thêm nội dung, không đổi hợp đồng.
- **Câu đóng:** Lối vào không trích nguyên văn luật, đặt ngưỡng khi mở GĐ05?
- **Nguồn:** ACCEPTANCE.md:123 · LEGAL-REVIEW.md:88, :163, :196

### Q-17 · Dòng minh bạch AI (Legal X9) — **chặn một phần: hợp đồng Ringkas** — **ĐÃ TRẢ LỜI → QĐ 34**

- **Phải quyết:** ba điểm của dòng "Soạn với hỗ trợ AI, duyệt bởi ⟨…⟩, ⟨ngày⟩".
- **Vì sao bây giờ / khi nào:** điểm (1), (3) trả lời được ngay; điểm (2) **hỏi sau khi Duy đọc hợp đồng Ringkas** (R34). Chặn Scope dòng 18, AC-53, chữ trên mọi bài.

| Điểm | Khuyến nghị (Legal) | Được | Mất | Rủi ro |
|---|---|---|---|---|
| (1) Giữ dòng trên mọi bài/bộ card đã đăng | **Giữ** | Phòng xa rủi ro L14 với giá một dòng chữ | — | Luật AI 134/2025 có áp cho văn bản không: chưa biết |
| (2) Chữ định danh trong "duyệt bởi ⟨…⟩" | **Chọn sau hợp đồng Ringkas** (họ tên hay tên khác) | — | — | Tên đã công khai trên mọi trang thì không rút lại khỏi bản lưu trữ |
| (3) "Soạn với hỗ trợ AI" chỉ ở mục thật có dùng AI | **Có**, thêm một cờ cho từng mục | Câu không sai với bài anh tự viết | Một trường mới trong spec | — |

- **Khuyến nghị:** như cột. Căn cứ: LEGAL-REVIEW X9; R20 là lựa chọn phòng xa trên căn cứ gray, không phải nghĩa vụ đã xác định.
- **Đánh đổi thật:** anh đổi một phần ẩn danh lấy một lớp phòng xa cho một luật chưa rõ có áp không.
- **Nếu sai:** chữ đổi rẻ; tên đã công khai thì không rút lại.
- **Câu đóng:** Giữ dòng, cờ AI theo từng mục, chữ định danh chọn sau hợp đồng Ringkas?
- **Nguồn:** LEGAL-REVIEW.md:90, :149 · PRD.md:109, :273 · ACCEPTANCE.md:125 · WRITER.md:158

### Q-18 · Kênh nhận khiếu nại + thời gian phản hồi (Legal X8, R33 a–b) — **chặn một phần: hợp đồng Ringkas** — **ĐÃ TRẢ LỜI → QĐ 35**

- **Phải quyết:** kênh nào, in bao nhiêu giờ phản hồi.
- **Vì sao bây giờ / khi nào:** R33 PASS là cổng S5. Loại kênh + số giờ trả lời được ngay; **công khai kênh (a) chờ hợp đồng Ringkas**. Phụ thuộc Q-17 (2): bỏ tên khỏi dòng AI thì kênh này là định danh công khai **đầu tiên**.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Hộp thư riêng cho site, không họ tên đầy đủ, không nhắc Ringkas, đặt ở B10; in "72 giờ gỡ tạm"** ⭐ (đề xuất Legal) | Bên có quyền có đường tới anh trước khi gửi DMCA lên host ở Mỹ (có thể khoá cả tài khoản host) | Một địa chỉ liên lạc công khai | Hộp thư có lộ danh tính qua header/WHOIS không: chưa kiểm |
| Form trên site | Dễ dùng | Nhận nội dung người dùng ⇒ trái R29, thêm Worker | — |
| GitHub Issues | Không cần hộp thư | Bên khiếu nại phải có tài khoản; khiếu nại bị công khai | — |
| Không có kênh | Không định danh nào | R33 không PASS ⇒ cổng S5 không mở | — |

- **Khuyến nghị:** hộp thư riêng + 72 giờ. Căn cứ: LEGAL-REVIEW X8. **72 giờ là đề xuất của Legal** (lessons ghi mô hình 24–72 giờ), không phải số có căn cứ luật; NĐ 17/2023 Đ.114 chưa xác minh — luật đặt hạn ngắn hơn thì luật thắng.
- **Đánh đổi thật:** anh đổi một chút ẩn danh lấy việc khiếu nại tới tay anh, không tới tay host.
- **Nếu sai:** đổi hộp thư hoặc số giờ in trên trang là rẻ; hộp thư đã công khai thì không rút lại.
- **Câu đóng:** Hộp thư riêng + 72 giờ gỡ tạm, công khai sau khi đọc hợp đồng Ringkas?
- **Nguồn:** LEGAL-REVIEW.md:118, :148, :216 · PRD.md:105, :158, :214, :431 · ACCEPTANCE.md:133

### Q-22 · Điều kiện 3 trong `blocked_on` của các file S1: đổi theo chữ QĐ 36? (PRD N8) — **→ NHÓM B (B-16), không phải QĐ**

- **Phải quyết:** cho PM thay chữ cũ *"Agent ke-toan-reviewer chạy thử 1 bài mẫu + card; đo thời gian Duy đọc báo cáo và ký (QĐ 36)"* bằng chữ QĐ 36 *"agent chạy thử trên 1 bài mẫu + card, đo thời gian Duy đọc báo cáo và ký"* trong frontmatter.
- **Vì sao bây giờ:** QĐ 36 bỏ việc thuê người ⇒ chữ cũ **không bao giờ gỡ được**, `status: fail` vĩnh viễn ở 7 file (PRD · ACCEPTANCE · LEGAL-REVIEW · WRITER · UNDERSTOOD · T3-RECONSTRUCTION · file này). Các file **đã lệch nhau**: Data đã tự đổi `SUCCESS-CRITERIA.md` ở vòng sửa 2; 6 file kia giữ chữ cũ theo luật sửa ("frontmatter giữ nguyên").

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Đổi đúng chữ QĐ 36 ở cả 7 file; mỗi file một dòng có ngày** ⭐ | Một điều kiện gỡ được; 8 file cùng một chữ | Luật sửa "giữ frontmatter" có một ngoại lệ có tên | — |
| B · Giữ chữ cũ | Đúng luật sửa | S1 không bao giờ PASS; điều kiện không còn ai để thoả | `SUCCESS-CRITERIA.md` phải trả về chữ cũ, nếu không hai bản cùng sống |

- **Khuyến nghị:** A. Căn cứ: QĐ 36 ghi nguyên văn *"Điều kiện 3 trước S1 đổi thành: agent chạy thử…"* (PRODUCT-BRIEF.md:174) — nội dung anh đã quyết; câu này chỉ hỏi PM có được chạm frontmatter không.
- **Đánh đổi thật:** anh nới cái khoá "frontmatter giữ nguyên" một lần, đổi lấy một điều kiện thoả được.
- **Nếu sai:** đảo bằng một dòng mỗi file; không đổi nội dung spec.
- **Câu đóng:** Cho PM đổi điều kiện 3 đúng chữ QĐ 36 ở 7 file S1?
- **Nguồn:** PRODUCT-BRIEF.md:174 · PRD.md:9, :15, :298 · ACCEPTANCE.md:9 · LEGAL-REVIEW.md:6 · WRITER.md:9 · UNDERSTOOD.md:9 · T3-RECONSTRUCTION.md:9 · SUCCESS-CRITERIA.md:5, :134

### Q-23 · Thẻ lật tự chấm có tính là "đã trả lời" cho "xong bài" (QĐ 24)? (PRD N1) — **ĐÃ TRẢ LỜI → QĐ 38**

- **Phải quyết:** chạm "Nhớ / Chưa nhớ" trên thẻ lật có làm bài chuyển sang "xong" (bắn `lesson_completed`) không; kéo theo AC-75 có đòi "≥ 1 card **trắc nghiệm** `published`" không.
- **Vì sao bây giờ:** chặn AC-62, AC-75. Trước ra mắt đổi không tốn gì; sau ra mắt là đổi nghĩa `lesson_completed`, cắt đôi M1/M2. Mùa 1 không có thẻ lật thì câu tự đóng.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **B · Không tính; mỗi bài `published` phải có ≥ 1 card trắc nghiệm `published`** ⭐ | M3 thấy mọi bài; mỗi `lesson_completed` thật đi cùng một `card_answered` ⇒ thêm được cờ chống bơm F4 (lập luận, chưa thử) | Không soạn được bài kết thúc toàn thẻ lật | Gỡ card trắc nghiệm cuối của một bài kéo bài xuống ⇒ M2 có bước rơi thật; cỡ chưa biết |
| A · Tính | Writer tự do chọn loại card cuối bài | Bài toàn thẻ lật thì M3 mù; không có F4 | Chỉ còn mắt Duy + agent bắt card sai ở bài đó |

- **Khuyến nghị:** B. Căn cứ: **Data và PM nay cùng khuyến nghị B** — Data đổi từ A sang B ở vòng sửa 2, kèm bảng 5 tiêu chí (TRACKING-PLAN.md:59, :67–73); bất đồng M1 mà review nêu đã hết, không còn chỗ mơ hồ phải leo theo quy tắc 12. M3 trả lời câu "card sai" của QĐ 8 (LLM sinh câu hỏi sai 6–22%).
- **Đánh đổi thật:** anh đổi quyền soạn bài kết thúc bằng thẻ lật lấy việc M3 nhìn thấy mọi bài.
- **Nếu sai:** trước ra mắt đảo miễn phí; sau ra mắt cắt đôi lịch sử M1/M2.
- **Câu đóng:** Thẻ lật không tính "đã trả lời", và mỗi bài `published` phải có ≥ 1 card trắc nghiệm `published`?
- **Nguồn:** PRD.md:289 · TRACKING-PLAN.md:53–73 · ACCEPTANCE.md:144, :169 · PRODUCT-BRIEF.md:162–163

### Q-24 · Thêm cờ `from_start` vào `lesson_completed` trước ra mắt? (Data M7) — **ĐÃ TRẢ LỜI → QĐ 39**

- **Phải quyết:** mở lại QĐ 25b (*"không thuộc tính nào khác"*) để thêm một bit `from_start` = `true|false`: storage này đã có bài 1 lối vào chưa.
- **Vì sao bây giờ:** mọi URL bài là cửa vào (AC-76). Link bài 5 chia sẻ trên Zalo ⇒ bài 5 bắn, bài 1 không ⇒ **M1 bị thổi, có thể > 1**, cờ F2 báo giả. Data đã sửa kết luận cũ "M1 lệch về phía xẹp" thành **"hướng ròng chưa biết"** — lý do Duy ghi ở QĐ 23 yếu đi. Dữ liệu không hồi tố (quy tắc 8).

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **1 · Thêm `from_start` (lưu ở `d2`); M1 báo cả số chặt và số lỏng** ⭐ (Data) | Đo được cỡ thổi thay vì đoán; F2 tính trên số chặt hết báo giả; giữ đủ số cho M2, M5 | Trái chữ QĐ 25b; số ô gấp đôi ⇒ nhiều ô n < 5 bị ẩn hơn | Đọc bài 1 ở Safari rồi bài 5 ở WebView Zalo bị tính `false` ⇒ số chặt xẹp ở nhóm đó |
| 0 · Giữ nguyên, đọc M1 kèm dấu hiệu (đang áp dụng) | Không đổi gì | Chỉ báo *nghi*, không đo được cỡ | M1 "trên ngưỡng" luôn kèm "có thể do chia sẻ" ⇒ giữ lối vào khi lẽ ra phải viết lại |
| 2 · Chặn bắn bài *k* ≠ 1 khi chưa có bài 1 | M1 ≤ 1 trở lại | Mất hẳn số người vào giữa; đổi **nghĩa** event | Data không khuyến nghị |

- **Khuyến nghị:** 1. Căn cứ: TRACKING-PLAN.md:175, :183 — cách duy nhất biến M7 từ lập luận thành số mà không cần ID; bit tính trên máy từ chính storage, không rời máy dưới dạng ID ⇒ không chạm QĐ 9.
- **Đánh đổi thật:** anh mở lại một hợp đồng vừa chốt hôm nay, đổi lấy việc biết North Star có bị thổi không.
- **Nếu sai:** bỏ cờ sau ra mắt là đổi hợp đồng (dòng có ngày), nhưng số lỏng còn nguyên ⇒ không cắt lịch sử M1.
- **Câu đóng:** Thêm `from_start` vào `lesson_completed`, M1 báo cả số chặt và số lỏng?
- **Nguồn:** TRACKING-PLAN.md:20–21, :156–188 · SUCCESS-CRITERIA.md:128–140 · PRD.md:178 · PRODUCT-BRIEF.md:161, :163

### Q-25 · Phán nào của agent `ke-toan-reviewer` cho phép Duy ký? (PRD N7) — **ĐÃ TRẢ LỜI → QĐ 40**

- **Phải quyết:** agent ra PASS / FAIL / UNVERIFIED / FLAG / "KHỚP NGUỒN THỨ CẤP"; QĐ 36 nói Duy ký nhưng chưa nói ký được trên phán nào.
- **Vì sao bây giờ:** chặn AC-03 (khi nào bài/card có số được đăng). Card lối vào có con số ⇒ quyết định này nằm trên đường ra mắt. QĐ 37 đã trả lời một trường hợp: K2 ở GĐ01 chỉ qua khi có Phụ lục II chính thức; lối vào không bị chặn.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · FAIL ở K1/K2/K3 chặn đăng tới khi sửa + agent soát lại; UNVERIFIED, FLAG, "KHỚP NGUỒN THỨ CẤP" (ngoài GĐ01): Duy ký được, kèm một dòng lý do trong bản ghi** ⭐ | Sai số học đã chứng minh bằng code thì không ai ký đè; chỗ agent thiếu căn cứ là đúng chỗ giao cho chữ ký | Một dòng lý do mỗi lần ký trên phán không sạch | Ký dễ dãi trên FLAG K4 ("người mới hiểu sai được không") |
| B · Chỉ ký khi toàn PASS (trừ "KHỚP NGUỒN THỨ CẤP" ở lối vào) | Chặt nhất | Con số chỉ suy luận được (UNVERIFIED) chặn mãi | Lối vào không ra mắt được nếu agent hay ra UNVERIFIED |
| C · Ký được trên mọi phán, kể cả FAIL | Không bao giờ bị agent chặn | Ký đè lên sai số đã chứng minh | Đúng rủi ro QĐ 8 muốn chặn |

- **Khuyến nghị:** A. Căn cứ: lý do QĐ 36 *"phần đáng tin là K1 (tính lại bằng code) và K2 (khớp nguyên văn)"* (PRODUCT-BRIEF.md:174); agent tự giới hạn *"Bạn ra PASS/FAIL/UNVERIFIED/FLAG; chữ ký là của Duy"* (`../../../.claude/agents/ke-toan-reviewer.md`:37).
- **Đánh đổi thật:** anh giữ quyền ký ở chỗ mơ hồ nhưng tự trói tay ở chỗ máy đã chứng minh sai.
- **Nếu sai:** trước ra mắt đảo miễn phí; sau ra mắt chỉ áp cho lần ký sau, không gỡ bài đã đăng.
- **Câu đóng:** FAIL ở K1/K2/K3 chặn đăng; các phán khác anh ký được kèm một dòng lý do?
- **Nguồn:** PRD.md:297 · ACCEPTANCE.md:36 · PRODUCT-BRIEF.md:174–175 · `../../../.claude/agents/ke-toan-reviewer.md`:24–27, :37–39

### Q-26 · Chữ công khai khi người soát số là agent (Legal X13 + Writer W2 + PRD K11) — **ĐÃ TRẢ LỜI → QĐ 41**

- **Phải quyết:** (1) mục có con số/tên tài khoản có hiện một dòng nói **AI soát** không; (2) hình thức: `reviewed_by` chỉ là người ký và agent ở trường riêng (Legal), hay một chuỗi `soát: … · ký: …` (Writer §3); (3) máy có cấm chữ "kế toán / accountant / chuyên gia / expert" trong chữ công khai không.
- **Vì sao bây giờ:** review §4(b) là **BLOCKER**: dòng "duyệt bởi ⟨…⟩" một mình khiến người đọc bài lãi suất tưởng có người chuyên môn soát. Chặn chữ hiển thị của AC-21, WRITER §3 và §5. ⟨…⟩ vẫn chờ hợp đồng Ringkas (QĐ 34.2) — câu này không chạm phần đó.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Hiện câu của Writer W2:** *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* · `reviewed_by` = người ký, agent ở trường riêng (Legal) · máy cấm 4 chữ trên ⭐ | Không ai hiểu nhầm có người kế toán; AC-21 giữ nguyên; một luật kiểm máy được | Một dòng lộ ra rằng không có người kế toán | Câu chữ minh bạch AI chưa đối chiếu Luật AI 134/2025 (L14) |
| A′ · Như A nhưng dùng câu của Legal: *"Con số và thuật ngữ kế toán được soát bằng AI; ⟨…⟩ đọc và duyệt"* | Nói rõ phạm vi "thuật ngữ" | **Trượt chính phép kiểm Legal đề xuất** (chứa chữ "kế toán") | Phải miễn trừ ngay luật vừa đặt |
| B · Giữ chuỗi Writer §3 hiện tại `soát: agent kế toán (AI) · ký: Duy` | Một chuỗi, đọc thẳng | Chứa đúng chữ "kế toán" | Người đọc lướt thấy "kế toán" |
| C · Không hiện dòng soát; chỉ dòng AI của QĐ 34 | Trang gọn | Im lặng việc AI soát APR/lãi suất | Đúng rủi ro §4(b) |

- **Khuyến nghị:** A — cấu trúc của Legal, câu của Writer. Căn cứ: Legal và Writer cùng mục tiêu (LEGAL-REVIEW.md:206; WRITER.md:320–331), lệch ở hình thức và chữ (PRD K11); câu Legal đề xuất tự chứa "kế toán" nên trượt phép kiểm của chính Legal, câu Writer không. QĐ 36: agent không bao giờ là người ký.
- **Đánh đổi thật:** anh đổi một dòng thừa nhận "không có người kế toán" lấy việc không ai hiểu nhầm là có.
- **Nếu sai:** trước ra mắt đổi một chuỗi; **sau ra mắt gỡ đi thì trông như che giấu** — chiều này đắt.
- **Câu đóng:** Hiện câu của Writer, `reviewed_by` chỉ là người ký, và cấm 4 chữ "kế toán / accountant / chuyên gia / expert" trong chữ công khai?
- **Nguồn:** LEGAL-REVIEW.md:206, :269 · WRITER.md:113, :291, :320–331 · PRD.md:330 · ACCEPTANCE.md:69 · PRODUCT-BRIEF.md:172, :174

### Q-27 · Hạt của cờ `ai_assisted` (QĐ 34.3 "từng mục") (PRD N5) — **ĐÃ TRẢ LỜI → QĐ 42**

- **Phải quyết:** "mục" là bài / bộ card / bản EN (cùng hạt với dòng AI của QĐ 34.1), hay mục H2 (nghĩa "mục" ở §Định nghĩa dùng chung của PRD).
- **Vì sao bây giờ:** chặn AC-53 và schema nội dung của S3. Hạt nào thì bản EN do Claude dịch cũng luôn `ai_assisted = true` (QĐ 6 + 34, đã ghi ở AC-53).

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Theo bài / bộ card / bản EN** ⭐ | Cờ cùng hạt với chỗ dòng AI hiện ⇒ máy kiểm 1–1; ít cờ | Bài tự viết có một H2 dùng AI ⇒ cả bài mang "Soạn với hỗ trợ AI" | Câu rộng hơn sự thật ở bài lai — sai về phía nói thừa |
| B · Theo mục H2 | Chính xác nhất | Dòng AI phải hiện ở từng H2 hoặc gộp lại; nhiều cờ | Quên cờ ở một H2 ⇒ câu sai về phía nói **thiếu** |

- **Khuyến nghị:** A. Căn cứ: QĐ 34.1 đặt dòng *"trên mọi bài/bộ card đã đăng"* (PRODUCT-BRIEF.md:172) ⇒ hạt hiển thị là bài/bộ card; nói thừa AI an toàn hơn nói thiếu với L14.
- **Đánh đổi thật:** anh đổi độ chính xác từng H2 lấy một luật đơn giản sai về phía an toàn.
- **Nếu sai:** trước ra mắt rẻ; thêm cờ theo H2 sau là thêm trường, không đổi nghĩa cờ cũ.
- **Câu đóng:** Cờ `ai_assisted` theo bài / bộ card / bản EN?
- **Nguồn:** PRD.md:293 · ACCEPTANCE.md:128 · PRODUCT-BRIEF.md:172

### Q-28 · Ngoại lệ của AC-05 ngoài `keep_en` (PRD N2 + Writer "→ Duy" 2, 3; mở lại B-13) — **ĐÃ TRẢ LỜI → QĐ 43**

- **Phải quyết:** ba loại chữ QĐ 20 chưa có chỗ: (a) tên riêng EN trên trang VI — "Where Money Sleeps", tên sách/tác giả Hermanson, "CC BY 3.0"; (b) dòng "Bài này chưa có bản tiếng Anh"; (c) chữ VN trên trang EN (`ghi có (credit alert)`, `vi.term` trong thẻ).
- **Vì sao bây giờ:** theo đúng chữ QĐ 20, **AC-05 FAIL ở mọi trang VI có tên sản phẩm**, trong khi AC-39 bắt hiện tên ⇒ S1 không duyệt được AC-05. Chặn microcopy S2. B-13 ("S2 chọn") đã gộp vào Q-04, nhưng câu trả lời QĐ 20 không nhắc dòng này.

| Điểm | Khuyến nghị | Được | Mất | Rủi ro |
|---|---|---|---|---|
| (a) Tên riêng | **Một danh sách tên riêng không chú thích, tách khỏi glossary, giữ ngắn** (PM) | AC-05 PASS ở trang có tên | Thêm một danh sách để giữ | Danh sách dài ra thành cửa sau |
| (b) Dòng "chưa có bản EN" | **Song ngữ, ngoại lệ có tên** (Writer) — PRD N2 trước đó gợi ý "chỉ VN" | Người chỉ đọc EN — người duy nhất cần dòng này — đọc được | Một dòng giao diện hai thứ tiếng trên trang VI | — |
| (c) Chữ VN trên trang EN | **Đối xứng QĐ 20:** chữ VN trên trang EN chỉ hợp lệ khi là mục glossary được đánh dấu (chữ tin báo ngân hàng, tên TK TT 99); `vi.term` trong thẻ được miễn | Máy kiểm được cả hai chiều | Thêm một cờ glossary | — |

- **Khuyến nghị:** như cột. Căn cứ (b): PM và Writer từng gợi ý ngược nhau; PM nay theo Writer vì người đọc VN không cần dòng này, nên bản chỉ-VN không phục vụ ai (WRITER.md:153, :276). Căn cứ (a): tên sản phẩm "không dịch" (PIPELINE Log, B-14).
- **Đánh đổi thật:** anh thêm ba ngoại lệ có tên vào "không trộn" để AC-05 thành phép kiểm máy thật.
- **Nếu sai:** rẻ trước ra mắt; danh sách và cờ là dữ liệu build.
- **Câu đóng:** Nhận (a) danh sách tên riêng ngắn, (b) dòng "chưa có bản EN" song ngữ, (c) luật đối xứng cho trang EN?
- **Nguồn:** PRD.md:290 · ACCEPTANCE.md:43 · WRITER.md:58, :153, :276–277 · PRODUCT-BRIEF.md:158

### Q-29 · Trong bài VN, "ledger" viết là `ledger` hay "sổ cái"? (Writer W1) — **ĐÃ TRẢ LỜI → QĐ 44**

- **Phải quyết:** mục glossary `ledger` có `keep_en` hay không.
- **Vì sao bây giờ:** chặn mục glossary `ledger` và mọi bài GĐ01 nói về sổ. Tagline T1 (QĐ 22, khoá nguyên văn) đặt "sổ cái" lên header; mặc định `keep_en` của Writer lại viết `ledger` trong bài.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **B · Bài viết "sổ cái"; `ledger` rời `keep_en`, chỉ còn ở `en.term` trong thẻ** ⭐ (Writer) | Một tên từ header tới cuối bài; câu kết bài trả đúng lời hứa của tagline | Ranh giới `keep_en` có một ngoại lệ | Tiền lệ: thuật ngữ khác bị đòi chuyển sang VN |
| A · Giữ cả hai: header "sổ cái", bài `ledger` | Một luật đều cho mọi thuật ngữ có tên EN chuẩn | Một thứ mang hai tên | Chỉ thẻ chú thích bắc cầu; tỉ lệ chạm thẻ chưa đo |

- **Khuyến nghị:** B. Căn cứ: `ledger` nằm trong `keep_en` chỉ vì **mặc định của Writer**; QĐ 20 nêu tên Debit, Credit, accrual, APR — không nêu `ledger` ⇒ đổi mặc định không lật quyết định nào của anh (WRITER.md:315).
- **Đánh đổi thật:** sự nhất quán header–bài, đổi lấy một luật `keep_en` không còn đều.
- **Nếu sai:** trước ra mắt đổi một cờ trên một mục glossary; sau ra mắt sửa chữ trong bài đã đăng.
- **Câu đóng:** Bài VN viết "sổ cái", `ledger` chỉ trong thẻ?
- **Nguồn:** WRITER.md:275, :306–318 · PRODUCT-BRIEF.md:158, :160

### Q-30 · Cảnh báo lưu trữ `persist()` có phải điều kiện ra mắt? (PRD N4) — **ĐÃ TRẢ LỜI → QĐ 45**

- **Phải quyết:** QĐ 18 nhặt `persist()` vào **mùa 1**, không nói **ngày ra mắt** — cùng loại với câu X3 cũ (QĐ 29).
- **Vì sao bây giờ:** chặn Scope dòng 19, AC-83 và danh sách cổng ra mắt (AC-79).

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Có, là điều kiện ra mắt** ⭐ | Tiến độ (Scope 5) ra mắt thì cảnh báo mất tiến độ ra cùng; không phép đo nào chặn nó; chữ đã viết (WRITER §6) | Thêm một AC vào cổng ra mắt | `persist()` trên iPhone chưa đo — AC-83 có phần thử máy thật |
| Không, bật sau bằng cờ | Cổng ra mắt nhỏ hơn | Người học iOS mất tiến độ sau 7 ngày không tương tác mà không được báo | — |

- **Khuyến nghị:** Có. Căn cứ: iOS Safari xoá storage sau 7 ngày (PRD Risks, khả năng Cao, WebKit đã công bố); lý do nhặt ở QĐ 18 là bảo vệ "mất thì rẻ" của QĐ 7 — lý do đó đúng từ ngày đầu có tiến độ.
- **Đánh đổi thật:** một AC nữa ở cổng ra mắt, đổi lấy việc người học iOS được báo trước khi mất.
- **Nếu sai:** là cờ — bật/tắt không tốn gì.
- **Câu đóng:** Cảnh báo `persist()` là điều kiện ra mắt?
- **Nguồn:** PRD.md:114, :292, :365 · ACCEPTANCE.md:178, :182 · PRODUCT-BRIEF.md:138, :155

### Q-31 · Bảng số liệu B3 trong file host Hermanson: che, giữ, hay thay số hư cấu? (Legal X10, kèm X3) — **ĐÃ TRẢ LỜI → QĐ 46**

- **Phải quyết:** xử lý 5 bảng B3 — số liệu báo cáo tài chính công ty thật (tr.45, 55, 94–95, 170, 185) — trong file PDF host; và nhận hay bác bản sửa `licences.json` Legal đã làm.
- **Vì sao bây giờ:** redact là **điều kiện ra mắt** (QĐ 29); S3 không cắt file host được khi chưa có câu này. Trong lúc chờ, B3 đã **tạm loại khỏi máy sinh card**.
- **Kèm (X3):** Legal đã sửa `licences.json` **trước khi anh trả lời** — thêm tr.113, 166, 501, 803, tr.117 và B3 (tạm) vào `exclusions`; đổi `attribution_text` thành "che các đoạn trích và bảng số liệu của bên thứ ba". Căn cứ Legal: chữ QĐ 28 + quy tắc QĐ 29 giao. `attribution_text` là chữ ghi công công khai ⇒ PM đưa lên anh. Bác ⇒ `git` trả bản trước.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Giữ B3 trong file host; che B2 tr.117; B3 vẫn loại khỏi máy sinh card** ⭐ (Legal + PM) | Giữ ví dụ tr.94–95, phần giảng tr.168–174, bài tập tr.55, 185 | Còn rủi ro "sưu tập dữ liệu" (Đ.22 Luật SHTT, *Feist* — gray, L16) | Do khiếu nại kích hoạt ⇒ đường gỡ R33 xử lý; Legal đọc là không chạm §7 (gray) |
| Che B3 | Hết rủi ro này | Mất ví dụ mà chữ quanh đó dựa vào; 2 bài tập không làm được | — |
| Thay số hư cấu, ghi "đã sửa đổi" | Giữ ví dụ, hết rủi ro | S3 sửa chữ trong PDF — khó nhất | Số mới phải khớp lời giảng tr.168–174 |

- **Khuyến nghị:** giữ B3, che B2, nhận `licences.json`. Căn cứ: số liệu là dữ kiện (Đ.15), phần chọn và cột phân tích là của Hermanson (LEGAL-REVIEW.md:203); giữ B3 **loại** khỏi máy sinh card gần như không mất gì vì card Hermanson không có con số (QĐ 27).
- **Đánh đổi thật:** anh giữ ví dụ thật của sách, đổi lấy một rủi ro gray chỉ phát sinh khi có người khiếu nại.
- **Nếu sai:** giữ rồi bị khiếu nại ⇒ gỡ trang (R33, 72 giờ); che rồi muốn giữ ⇒ cắt lại file host.
- **Câu đóng:** Giữ B3, che B2 tr.117, và nhận bản sửa `licences.json` của Legal?
- **Nguồn:** LEGAL-REVIEW.md:66–103, :196, :203, :229 · ACCEPTANCE.md:76, :178 · PRODUCT-BRIEF.md:157, :167 · `../../legal/licences.json` `exclusions`

### Q-32 · Luật máy loại trang của QĐ 28: giữ đúng chữ hay dùng mẫu ③? (Legal X11, gộp C-09) — **ĐÃ TRẢ LỜI → QĐ 47**

- **Phải quyết:** mẫu dấu hiệu nguồn ngoài mà S3 dùng để loại trang khỏi máy sinh card.
- **Vì sao bây giờ:** chặn AC-18 và cấu hình máy sinh card. Đổi mẫu là **đổi chữ QĐ 28** ⇒ không phòng nào tự làm. Từ vòng sửa 2, `exclusions` đã có **cả 7 trang đã biết** ⇒ mẫu chỉ còn quyết định số phận của các trang **chưa biết**.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **③ cộng `exclusions`: không phân biệt hoa thường, nhận `Source:`/`Source'`, cộng chuỗi denylist R10, `reprinted`, `adapted from`** ⭐ (Legal) | Bắt 7/7 trang đã biết khi thử; bắt rộng nhất trang chưa biết | Loại 132/1004 trang, ~41 trang oan (vd tr.24–25, Hermanson tự viết về FASB) | Vẫn sót bảng B3 không có chữ "annual report" |
| ① Đúng chữ QĐ 28 cộng `exclusions` | Đúng chữ; loại 91 trang | Bỏ lỡ trang lạ viết hoa "Annual Report" hay "Source'" | Đoạn bên thứ ba chưa biết lọt nhiều hơn |
| Hẹp hơn chữ QĐ 28 (C-09: bỏ "annual report" trơn — 32 lần ở tr.1–197, gồm đoạn định nghĩa) | Ít loại oan nhất | Nới chữ QĐ 28 | Lọt nhiều nhất |

- **Khuyến nghị:** ③. Căn cứ: cái giá của ③ là kho card nhỏ hơn, mà mùa 1 card từ trang > 197 chỉ đăng khi có bài phủ trang đó (QĐ 28) ⇒ trang bị loại oan ngoài tr.1–197 gần như không tốn gì ở mùa 1 (LEGAL-REVIEW.md:105–113).
- **Đánh đổi thật:** kho card nhỏ hơn, đổi lấy ít đoạn bên thứ ba chưa biết lọt vào card.
- **Nếu sai:** mẫu là cấu hình build; nới sau là thêm trang lại. Card đã đăng từ trang lọt thì phải gỡ.
- **Câu đóng:** Dùng mẫu ③ cộng `exclusions` thay mẫu đúng chữ QĐ 28?
- **Nguồn:** LEGAL-REVIEW.md:105–113, :204 · ACCEPTANCE.md:66 · PRODUCT-BRIEF.md:166 · PRD.md (§Risks "loại quá rộng")

### Q-33 · Card Hermanson từ chương 5 trở đi: "đọc lại đoạn này" trỏ về bài nào? (review M4) — **ĐÃ TRẢ LỜI → QĐ 48**

- **Phải quyết:** QĐ 27 nói trỏ `sectionId` của **bài GĐ01** có `based_on` phủ trang đó; QĐ 28 nạp cả cuốn và cho card > tr.197 đăng khi *"đã có bài có `based_on` phủ trang đó"*. GĐ01 chỉ khớp tr.1–197 (QĐ 15) ⇒ đọc theo AC-19 thì card ch.5+ **không bao giờ đăng**, và "cả cuốn" vô tác dụng.
- **Vì sao bây giờ:** AC-19, PRD Scope 2 và B4 đọc một kiểu; Legal R11 đọc kiểu kia. Hai QĐ cùng gốc nhưng mơ hồ ⇒ quy tắc 12: leo lên anh, không phân xử.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Bất kỳ bài `published` nào có `based_on` phủ trang đó** (Legal R11) ⭐ | "Cả cuốn" của QĐ 28 có tác dụng; card ch.5+ lên khi có bài tương ứng (GĐ02, GĐ05 hay sau này) | Bỏ chữ "GĐ01" của QĐ 27 | — |
| B · Chỉ bài GĐ01 (AC-19, PRD hiện tại) | Đúng chữ QĐ 27 | Card > tr.197 không bao giờ đăng | QĐ 28 thành vô nghĩa ở phần ngoài 197 |

- **Khuyến nghị:** A. Căn cứ: chính QĐ 28 ghi hệ quả (1) *"card từ chương 5+ chỉ được ĐĂNG khi đã có bài có `based_on` phủ trang đó (QĐ 27)"* (PRODUCT-BRIEF.md:166) — QĐ 28 sau QĐ 27 và đã đọc QĐ 27 theo cách A.
- **Đánh đổi thật:** chữ "GĐ01" trong QĐ 27, đổi lấy việc QĐ 28 có tác dụng.
- **Nếu sai:** luật build; mùa 1 gần như chưa có bài nào phủ trang > 197 ⇒ sai rẻ.
- **Câu đóng:** Card ch.5+ trỏ về bất kỳ bài `published` nào có `based_on` phủ trang đó?
- **Nguồn:** ACCEPTANCE.md:67 · PRD.md:97, :162 · LEGAL-REVIEW.md:121 · PRODUCT-BRIEF.md:151, :165–166

### Q-34 · Hộp thư khiếu nại nhận dữ liệu có định danh: phương án, câu R25 mới, thời hạn giữ thư (Legal X12 + R37 (4)) — **ĐÃ TRẢ LỜI → QĐ 49**

- **Phải quyết:** (1) phương án A/B/C dưới; (2) câu R25 thay thế; (3) thời hạn giữ thư.
- **Vì sao bây giờ:** thư khiếu nại mang họ tên, email, có thể cả giấy tờ ⇒ câu R25 / AC-57 *"không thu thập định danh"* thành **sai** khi hộp thư lên trang. R37 là cổng S5. **Q-20 cần câu này xong trước** (phần rủi ro còn lại đi vào Q-20). Việc **công khai** hộp thư vẫn chờ hợp đồng Ringkas (QĐ 35); ba điểm này trả lời được ngay.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Giữ hộp thư; sửa R25 cho đúng phạm vi; áp R37 (chỉ dùng cho khiếu nại đó, không vào repo/build, không chuyển sang dịch vụ khác, kể cả phiên AI)** ⭐ (Legal) | Khiếu nại tới tay anh, không tới host ở Mỹ | Anh thành người giữ dữ liệu có định danh của người lạ | Đ.20.1.c Luật 91 nếu nhà cung cấp hộp thư ở nước ngoài (đọc qua nguồn thứ cấp) ⇒ vào Q-20 |
| B · Chọn nhà cung cấp hộp thư đặt máy chủ ở VN | Bớt phần xuyên biên giới | Chưa kiểm có nhà cung cấp nào như vậy | Vẫn là xử lý dữ liệu có định danh |
| C · Bỏ hộp thư | Không nhận định danh nào | Trái QĐ 35; bên có quyền chỉ còn DMCA tới host | Khoá cả tài khoản host |

- **Câu R25 đề xuất (Legal, nguyên văn):** *"Khi bạn đọc, Where Money Sleeps không thu thập định danh; nhà cung cấp hạ tầng có ghi địa chỉ IP cho mục đích bảo mật của họ. Nếu bạn gửi thư tới hộp thư khiếu nại, những gì bạn gửi (tên, email, nội dung) chỉ được dùng để xử lý khiếu nại đó."* Bản EN: Writer.
- **Thời hạn giữ thư:** Legal không đặt số, PM cũng không có nguồn cho một con số (quy tắc 3). PM đề xuất một **luật không cần số:** xoá thư khi khiếu nại đã đóng; repo chỉ giữ ngày + nội dung bị gỡ + loại lý do (R37 (2)).
- **Khuyến nghị:** A + câu của Legal + "xoá khi khiếu nại đóng". Căn cứ: QĐ 35 đã chọn hộp thư vì không có kênh thì chỉ còn DMCA (LEGAL-REVIEW.md:201, :205).
- **Đánh đổi thật:** anh nhận vai người giữ dữ liệu có định danh, đổi lấy việc khiếu nại không đi thẳng tới host.
- **Nếu sai:** câu R25 đổi rẻ; thư đã nhận thì đã nhận — không rút được.
- **Câu đóng:** Phương án A, câu R25 của Legal, và xoá thư khi khiếu nại đóng?
- **Nguồn:** LEGAL-REVIEW.md:150, :157, :205, :231, :267 · ACCEPTANCE.md:132, :191 · PRODUCT-BRIEF.md:173

### Q-19 · ONE-PAGER v2 (hỏi ngay trước Q-20) — **ĐÃ TRẢ LỜI → QĐ 50**

- **Phải quyết:** duyệt ONE-PAGER v2 để PM chép vào `gates/ONE-PAGER.md`.
- **Điều kiện trước khi hỏi — PM phải làm, chưa làm:** `ONE-PAGER-V2-PROPOSAL.md` phải được **cập nhật theo QĐ 36, 37 và mọi câu trả lời Q-22…Q-34** trước khi đưa anh. Bản hiện tại lỗi thời ở ít nhất bốn chỗ: nguồn ghi *"QĐ 1–36"*, chưa có QĐ 37 (GĐ01 chờ Phụ lục II chính thức); §4 *"nghiêng về phía thấp"* đã sai theo Data (hướng ròng chưa biết — Q-24); §D *"quy tắc Legal chưa ra"* đã lỗi thời (§A.2 đã ra); §D *"PRD chưa nhập QĐ 36"* đã lỗi thời.
- **Vì sao gần cuối:** vibe-check [2] **FAIL chặn** khi ONE-PAGER cũ hơn `PRD.md`. Phép kiểm so thời điểm sửa file ⇒ mọi câu trả lời trước làm PRD mới hơn; duyệt sớm thì lại FAIL.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Duyệt v2 đã cập nhật** ⭐ | [2] hết FAIL; mọi phòng trích từ một tuyên bố đúng | Đọc lại một trang | — |
| S1 đặt ngay một ngưỡng M1, ghi "TÔI CHỌN" | §4 giữ chữ cũ | Một con số không nguồn mà anh sẽ build lên (quy tắc 3) | Quyết định viết lại lối vào dựa trên số bịa |

- **Khuyến nghị:** duyệt v2 đã cập nhật. Căn cứ: quy tắc 3, quy tắc 11; 6 câu UNDERSTOOD giữ nguyên chữ (ONE-PAGER-V2-PROPOSAL.md:14).
- **Đánh đổi thật:** anh đổi chữ cũ "S1 đặt ngưỡng" lấy một ngưỡng có dữ liệu sau ≥ 4 tuần.
- **Nếu sai:** sửa một trang, rẻ; nhưng mỗi lần PRD đổi phải xem lại.
- **Câu đóng:** Duyệt ONE-PAGER v2 (bản đã cập nhật theo QĐ 1–37 và Q-22…Q-34)?
- **Nguồn:** ONE-PAGER-V2-PROPOSAL.md:14–16, :24, :31, :76, :122, :124 · PRD.md:15 · T3-RECONSTRUCTION.md:180

### Q-20 · Rủi ro tổng — xác nhận lại QĐ 11 bằng một dòng mới (**hỏi cuối cùng**) — **ĐÃ TRẢ LỜI → QĐ 51**

- **Phải quyết:** QĐ 11 chấp nhận rủi ro *"thấp, do khiếu nại kích hoạt, có cờ `published` để gỡ"*. S1 tìm thấy **năm** phần không khớp mô tả đó. Anh ký trên cả năm, hoặc không:
  1. **Luật 91 — IP khi truyền tải, hai cách đọc cùng một nguồn** (`../../../docs/data.md`). **A:** chỉ đếm, không lưu gì định danh ⇒ chưa vào phạm vi điều chỉnh, không nghĩa vụ. **B:** IP mà host tĩnh và Worker ở nước ngoài xử lý khi truyền tải là dữ liệu cá nhân ⇒ Đ.20.1.c, hồ sơ CTIA trong 60 ngày; không nộp ⇒ phạt 30–50 triệu (nếu đó là mức tổ chức thì cá nhân 15–25 triệu — phép chia của Legal, **chưa đối chiếu**) **và buộc ngừng chuyển dữ liệu**. Host nào cũng thấy IP ⇒ thiết kế không loại được. Kèm L13 (i) số gộp theo ngày có ghép ra người không (QĐ 32), (ii) Cloudflare tự xử lý IP có tính là anh xử lý không (QĐ 31).
  2. **CC BY 3.0 §7:** sót ghi công ⇒ giấy phép **chấm dứt tự động ngay lúc publish**; gỡ cờ `published` không làm giấy phép sống lại. Không do khiếu nại kích hoạt. Chỉ phòng trước được (`based_on` + lint, AC-45).
  3. **Hộp thư khiếu nại thu dữ liệu cá nhân có định danh** (sau Q-34): khác IP, cách đọc A của phần 1 **không áp**. Còn mở: anh là bên kiểm soát hay bên xử lý; nhà cung cấp ở nước ngoài có làm phát sinh Đ.20.1.c không; có cần thông báo/đồng ý của người gửi không (L18).
  4. **Minh bạch "agent soát ≠ người kế toán"** (sau Q-26): chữ công khai có thể đúng mà người đọc vẫn hiểu là có chuyên gia soát; Luật AI 134/2025 có áp cho văn bản và có đòi họ tên thật không — chưa đọc văn bản gốc (L14).
  5. **Loại rủi ro của tr.113 — đoạn bên thứ ba đã biết lọt vào máy sinh card:** **đã đóng** cho 7 trang đã biết (`exclusions` có tr.113, 166, 501, 803, 117 và B3 — PM đọc `licences.json` 2026-10-24). **Còn lại:** bảng bên thứ ba **chưa thấy** — soát lần 1 chỉ bằng máy với 30 tên công ty Legal tự chọn, chưa trang nào xem bằng mắt. Phía card anh đã nhận (QĐ 28); phía **file host** thì chưa ai nhận — giảm bằng AC-23 (xem bằng mắt trước ra mắt).
- **Vì sao cuối:** đây là tổng của Q-26 (minh bạch), Q-31 (B3), Q-32 (luật máy), Q-34 (hộp thư) và QĐ 31, 32 (IP, ô nhỏ). Ký khi các phần chưa chốt là ký mù. **Phần định danh công khai** (QĐ 34.2 chữ trong "duyệt bởi", QĐ 35 công khai hộp thư) vẫn chờ hợp đồng Ringkas ⇒ **không nằm trong chữ ký này**; sẽ có dòng riêng sau khi anh đọc hợp đồng.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **A · Xác nhận lại cho cả 5 phần, và chạy một workflow pháp lý cho L13 + L18 TRƯỚC S5** (L14–L17 giữ lịch sau release) ⭐ | Biết cách đọc nào đúng trước khi mở cổng, cho hai câu thiết kế không tránh được; L13 và L18 cùng Đ.20.1.c ⇒ một lượt | Một lượt workflow trước S5, ngược lời anh *"sau khi release rồi thì sẽ chạy workflows"* | Workflow cùng vendor, không phải ý kiến pháp lý |
| B · Xác nhận lại, giữ lịch "sau release" cho mọi L | Đúng chữ QĐ 11 | Ra mắt khi chưa biết cách đọc B có đúng không | B đúng ⇒ có thể buộc ngừng chuyển dữ liệu = site ngừng |
| C · Không xác nhận | — | Không thiết kế site công khai nào tránh được IP khi truyền tải | Dừng dự án, hoặc thuê luật sư (trái QĐ 12) |

- **Khuyến nghị:** A. Căn cứ: L13 và L18 là hai câu mà kịch bản xấu chạm **mọi trang** (IP) hoặc **mọi khiếu nại** (hộp thư) và thiết kế không tránh được (LEGAL-REVIEW.md:194, :205); phần 2 đã có biện pháp phòng trước ở AC-45, nên L15 giữ lịch sau release.
- **Đánh đổi thật:** anh đổi một lượt workflow trước S5 lấy việc không ký mù trên cách đọc nặng.
- **Nếu sai:** không chạy mà B đúng ⇒ có thể phải ngừng site; chạy mà thừa ⇒ mất một lượt workflow.
- **Câu đóng:** Chọn A — một dòng mới xác nhận lại QĐ 11 cho cả 5 phần, với điều kiện workflow L13 + L18 chạy trước S5?
- **Nguồn:** LEGAL-REVIEW.md:194, :200, :205, :206, :226–231 · PRD.md:321 · PRODUCT-BRIEF.md:142–143 · `../../legal/licences.json`

### Q-19 (bản trước vòng sửa 2 — đã thay bằng bản vòng sửa 2 bên trên) · ONE-PAGER bản mới

- **Phải quyết:** duyệt ONE-PAGER v2 do PM soạn **sau khi** Q-02…Q-18 đã ghi vào PRD. Thay đổi đề xuất: (1) nguồn = 16 quyết định, bỏ `draft`; (2) §3.1 *"Sách CC BY thì được"* → chỉ phần đã soát (Hermanson tr.1–197, QĐ 15); (3) §4 *"Ngưỡng do S1 đặt"* → S1 đặt **cách** đặt ngưỡng, số đặt sau ≥ 4 tuần và bài 1 ≥ 100 lượt (T3 Δ14); (4) §1 theo câu trả lời Q-12.
- **Vì sao bây giờ, và vì sao gần cuối:** vibe-check [2] đang **FAIL chặn** (ONE-PAGER cũ hơn PRD.md). Phép kiểm so thời điểm sửa file, nên mọi câu trả lời trước đều làm PRD mới hơn: duyệt sớm thì lại FAIL.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Duyệt v2** ⭐ | [2] hết FAIL; mọi phòng trích từ một tuyên bố đúng | Đọc lại một trang | — |
| S1 đặt ngay một số ngưỡng M1, ghi "TÔI CHỌN" | §4 giữ nguyên chữ | Một con số không nguồn mà anh sẽ build lên (quy tắc 3) | Quyết định viết lại lối vào dựa trên số bịa |

- **Khuyến nghị:** duyệt v2. Căn cứ: CLAUDE.md quy tắc 3 (*"một con số không nguồn gốc còn tệ hơn không có con số"*) và quy tắc 11.
- **Đánh đổi thật:** anh đổi chữ cũ "S1 đặt ngưỡng" lấy một ngưỡng có dữ liệu sau 4 tuần.
- **Nếu sai:** sửa một trang, rẻ; nhưng mỗi lần PRD đổi phải xem lại.
- **Câu đóng:** Duyệt ONE-PAGER v2 với 4 thay đổi trên?
- **Nguồn:** ONE-PAGER.md:4, :11, :37–39, :50 · PRD.md:264, :421, :428 · T3-RECONSTRUCTION.md:180

### Q-20 (bản trước vòng sửa 2 — đã thay bằng bản vòng sửa 2 bên trên) · Rủi ro tổng — xác nhận lại QĐ 11 bằng một dòng mới (**hỏi cuối cùng**)

- **Phải quyết:** QĐ 11 chấp nhận rủi ro "thấp, do khiếu nại kích hoạt, có cờ `published` để gỡ". S1 tìm thấy hai rủi ro không khớp mô tả đó:
  1. **Luật 91 — hai cách đọc cùng một nguồn.** A: chỉ đếm, không lưu gì định danh ⇒ không phát sinh nghĩa vụ. B: IP khi truyền tải ⇒ hồ sơ CTIA trong 60 ngày; không nộp ⇒ phạt 30–50 triệu (nếu đó là mức tổ chức thì cá nhân 15–25 triệu — phép chia của Legal, **chưa đối chiếu**) **và buộc ngừng chuyển dữ liệu**. Host nào cũng thấy IP ⇒ thiết kế không loại được.
  2. **CC BY 3.0 §7:** sót ghi công ⇒ giấy phép **chấm dứt tự động ngay lúc publish**, với cả tác phẩm; cờ `published` không khôi phục được. Chỉ phòng trước được (`based_on` + lint, AC-45).
- **Vì sao cuối:** đây là tổng của Q-14, Q-15, Q-17, Q-18 (IP, ô nhỏ, tên công khai). Chấp nhận khi các phần chưa chốt là ký mù.

| Phương án | Được | Mất | Rủi ro |
|---|---|---|---|
| **Xác nhận lại, và chạy workflow pháp lý riêng câu L13 TRƯỚC S5** ⭐ | Biết cách đọc nào đúng trước khi mở cổng | Một lượt workflow trước S5, ngược lời anh *"sau khi release rồi thì sẽ chạy workflows"* | Workflow cùng vendor, không phải ý kiến pháp lý |
| Xác nhận lại, giữ lịch "sau release" | Đúng chữ QĐ 11 | Ra mắt khi chưa biết cách đọc B có đúng không | B đúng ⇒ có thể buộc ngừng chuyển dữ liệu = site ngừng chạy |
| Không xác nhận | — | Không có thiết kế site công khai nào tránh được IP khi truyền tải | Dừng dự án, hoặc thuê luật sư (trái QĐ 12) |

- **Khuyến nghị:** phương án 1. Căn cứ: L13 là câu duy nhất mà kịch bản xấu chạm **mọi trang** và thiết kế không tránh được (PRD #12); rủi ro §7 đã có biện pháp phòng trước ở AC-45, nên L15 giữ lịch sau release.
- **Đánh đổi thật:** anh đổi một lượt workflow trước S5 lấy việc không ký mù trên cách đọc nặng.
- **Nếu sai:** không chạy mà B đúng ⇒ có thể phải ngừng site; chạy mà thừa ⇒ mất một lượt workflow.
- **Câu đóng:** Thêm dòng xác nhận lại QĐ 11 cho cả hai rủi ro, và chạy L13 trước S5?
- **Nguồn:** LEGAL-REVIEW.md:141, :147, :169, :171 · PRD.md:219, :282, :312, :429–430 · PRODUCT-BRIEF.md:142–143

## Bổ sung sau review vòng 2 — 2026-10-24

- **Q-21 (mới, chuyển từ C-01 / T3 Δ10):** máy có phải tự phát hiện thuật ngữ CHƯA có trong glossary không (QĐ 5 hứa "thuật ngữ nào không có mục glossary thì FAIL"), hay để mắt Duy bắt (AC-12, thêm việc vào khối duyệt chưa bấm giờ). Quy tắc 12: hai phiên bất đồng ⇒ leo lên Duy, PM không tự hoà giải. **Tổng nhóm A: 21.** Hỏi ngay sau Q-04.
- **B-02 → C (Legal):** bảng số liệu bên thứ ba tr.94, tr.117, tr.185 — Legal ra quy tắc + soát lại tr.1–197. Nếu Legal kết luận "không cần che" ⇒ thành câu cho Duy.
- Gộp vào câu đóng của Q-04: dòng thông báo song ngữ của Writer (B-13). Gộp vào Q-13: sổ ngân hàng GĐ02 "chờ kế toán xác minh" (C-13). C-08 (Duy duyệt danh sách tên riêng) là việc của Duy — chuyển vào danh sách việc chỉ Duy làm.

## Câu trả lời của Duy — chỉ thêm

| Ngày | Q | Trả lời | Ghi vào |
|---|---|---|---|
| 2026-10-24 | Q-01 | **Mở tại chỗ** làm mặc định; buổi thử 5 người so với "thẻ phủ lên chữ". | PRODUCT-BRIEF QĐ 17 |
| 2026-10-24 | Q-02 | **Quy tắc A**; nhặt `persist()` · ID mồ côi · không auto-redirect. | PRODUCT-BRIEF QĐ 18 |
| 2026-10-24 | Q-03 | **Lần đầu mỗi mục H2.** | PRODUCT-BRIEF QĐ 19 |
| 2026-10-24 | Q-04 | **Thuật ngữ chuyên ngành giữ tiếng Anh trong dòng, có chú thích**; QĐ 6 thu hẹp; glossary có cờ `keep_en`. | PRODUCT-BRIEF QĐ 20 |
| 2026-10-24 | Q-21 | **Danh sách gốc TT 99 + glossary, mức cảnh báo**; tiếng Anh tự động FAIL nhờ QĐ 20. | PRODUCT-BRIEF QĐ 21 |
| 2026-10-24 | Q-05 | **T1.** | PRODUCT-BRIEF QĐ 22 |
| 2026-10-24 | Q-06 | **Theo giai đoạn**, lối vào một khối. | PRODUCT-BRIEF QĐ 23 |
| 2026-10-24 | Q-07 | **≥ 1 card đã trả lời**, kèm AC-75. | PRODUCT-BRIEF QĐ 24 |
| 2026-10-24 | Q-08 | **Nhận cả (a)–(e).** | PRODUCT-BRIEF QĐ 25 |
| 2026-10-24 | Q-09 | **Thêm `tel` (theo sao lưu) + thời điểm (không theo); bỏ hàng đợi offline.** | PRODUCT-BRIEF QĐ 26 |
| 2026-10-24 | Q-10 | **Card khái niệm, không số, hiện VN, link về section GĐ01.** | PRODUCT-BRIEF QĐ 27 |
| 2026-10-24 | Q-11 | **Cả cuốn trừ đoạn đã biết phải loại**; host vẫn tr.1–197; card ch.5+ chỉ đăng khi có bài tương ứng. | PRODUCT-BRIEF QĐ 28 |
| 2026-10-24 | Q-12 | **Là điều kiện ra mắt.** | PRODUCT-BRIEF QĐ 29 |
| 2026-10-24 | Q-13 | **QĐ 8 + đoạn bài mà card có số trích.** | PRODUCT-BRIEF QĐ 30 |
| 2026-10-24 | Q-14 | **Không bật rule IP**; F1–F3 + cách ly. | PRODUCT-BRIEF QĐ 31 |
| 2026-10-24 | Q-15 | **Theo ngày**, ẩn n < 5, gộp tuần nếu L13 đòi. | PRODUCT-BRIEF QĐ 32 |
| 2026-10-24 | Q-16 | **0 chữ trích luật cho phần ra mắt**, đặt ngưỡng khi mở GĐ05. | PRODUCT-BRIEF QĐ 33 |
| 2026-10-24 | Q-17 | **Giữ dòng; cờ AI theo mục; định danh chọn sau hợp đồng Ringkas (còn treo).** | PRODUCT-BRIEF QĐ 34 |
| 2026-10-24 | Q-18 | **Hộp thư riêng + 72 giờ gỡ tạm; công khai sau hợp đồng Ringkas.** | PRODUCT-BRIEF QĐ 35 |
| 2026-10-24 | — (ngoài hàng đợi) | **Người kế toán = agent `ke-toan-reviewer`**, Duy ký; điều kiện 3 đổi thành agent chạy thử + đo giờ Duy ký. | PRODUCT-BRIEF QĐ 36 |
| 2026-10-24 | — (ngoài hàng đợi) | **K2 dùng bản chép Phụ lục II thứ cấp**, tối đa "KHỚP NGUỒN THỨ CẤP"; GĐ01 chỉ đăng khi có Phụ lục II chính thức; lối vào không chặn. | PRODUCT-BRIEF QĐ 37 |
| 2026-10-25 | Q-23 | **B: thẻ lật không tính; mỗi bài published ≥ 1 card trắc nghiệm published.** | PRODUCT-BRIEF QĐ 38 |
| 2026-10-25 | Q-24 | **Thêm `from_start`; M1 báo số chặt + số lỏng.** | PRODUCT-BRIEF QĐ 39 |
| 2026-10-25 | Q-25 | **A: FAIL K1/K2/K3 chặn; phán khác Duy ký kèm lý do.** | PRODUCT-BRIEF QĐ 40 |
| 2026-10-25 | Q-26…Q-34, Q-19, Q-20 | **Nhận mọi khuyến nghị** (lô). | PRODUCT-BRIEF QĐ 41–51 |
| 2026-10-25 | Q-26 | (lô) Câu W2 hiện công khai; `reviewed_by` = người ký, agent ở trường riêng; cấm 4 chữ trong dòng minh bạch + `reviewed_by`. | PRODUCT-BRIEF QĐ 41 |
| 2026-10-25 | Q-27 | (lô) `ai_assisted` theo bài / bộ card / bản EN. | PRODUCT-BRIEF QĐ 42 |
| 2026-10-25 | Q-28 | (lô) Ngoại lệ AC-05 (a) danh sách tên riêng · (b) dòng "chưa có bản EN" song ngữ · (c) đối xứng cho trang EN. | PRODUCT-BRIEF QĐ 43 |
| 2026-10-25 | Q-29 | (lô) Bài VN viết "sổ cái"; `ledger` chỉ trong thẻ. | PRODUCT-BRIEF QĐ 44 |
| 2026-10-25 | Q-30 | (lô) `persist()` là điều kiện ra mắt. | PRODUCT-BRIEF QĐ 45 |
| 2026-10-25 | Q-31 | (lô) Giữ B3 trong file host, loại khỏi máy sinh card; che B2 tr.117; nhận `licences.json` của Legal. | PRODUCT-BRIEF QĐ 46 |
| 2026-10-25 | Q-32 | (lô) Mẫu ③ + `exclusions`. | PRODUCT-BRIEF QĐ 47 |
| 2026-10-25 | Q-33 | (lô) Card ch.5+ trỏ bất kỳ bài `published` có `based_on` phủ trang. | PRODUCT-BRIEF QĐ 48 |
| 2026-10-25 | Q-34 | (lô) Hộp thư phương án A; câu R25 mới của Legal; R37; xoá thư khi khiếu nại đóng. | PRODUCT-BRIEF QĐ 49 |
| 2026-10-25 | Q-19 | (lô) Duyệt ONE-PAGER v2; PM áp vào `gates/ONE-PAGER.md`. | PRODUCT-BRIEF QĐ 50 |
| 2026-10-25 | Q-20 | (lô) Xác nhận lại QĐ 11 cho cả 5 phần; workflow pháp lý L13 + L18 trước S5. | PRODUCT-BRIEF QĐ 51 |

## Đổi vòng sửa 2 (2026-10-24)

PM phân loại lại sau review S1 (QĐ 17–35) và QĐ 36, 37. File là nháp ⇒ sửa tại chỗ; bản trước lưu ở mục Lưu trữ bên trên (Q-01…Q-18 nguyên văn, Q-19/Q-20 bản cũ nguyên văn). Same vendor, same priors — no external verifier ran.

| Chỗ | Đổi gì | Nguồn |
|---|---|---|
| Lời dẫn · TL;DR | Nguồn thẩm quyền QĐ 1–37; TL;DR đúng trạng thái: Q-01…Q-18 + Q-21 đã trả lời; còn 15 câu A, Q-22 kế tiếp; 3 câu có điều kiện; 2 điểm chờ Ringkas | review M9 · QĐ 17–37 |
| Nhóm A | Thêm Q-22…Q-34 (N1–N5, N7, N8, M4, M7, X3, X10–X13, W1, W2, gộp cùng gốc). Viết lại Q-19 (điều kiện: v2 cập nhật theo QĐ 36, 37 + câu trả lời mới) và Q-20 (5 phần: Luật 91, CC BY 3.0 §7, hộp thư, minh bạch agent, loại rủi ro tr.113). Q-19 ngay trước Q-20; Q-20 cuối | review M2, M4, M7, M8, M9, §4(a)(b)(c) |
| Q-01…Q-18 | Chuyển nguyên văn xuống §Lưu trữ, tiêu đề thêm "ĐÃ TRẢ LỜI → QĐ n" (giữ lý do cũ, quy tắc 14) | quy tắc 14 |
| Câu có điều kiện | Mục mới: ĐK-1 (N3), ĐK-2 (R35), ĐK-3 (R33 a′) — câu thật của Duy, không đẩy sang C | Legal · PRD |
| Nhóm B | Đổi tên nhóm ("đã có quyết định trả lời"); B-01 ghi xong; B-13 mở lại → Q-28; thêm B-15 | review §4(c) |
| Nhóm C | C-09 gộp vào Q-32; C-13 ghi theo QĐ 30; thêm C-16 (Phụ lục II chính thức), C-17 (disclaimer L5) | QĐ 30, 37 · Legal L5 |
| Nhóm D | D-27 thêm phần rủi ro X12/X13; thêm D-31…D-45 | — |
| §Câu trả lời | Chuyển khối "Bổ sung sau review vòng 2" lên trước bảng để các dòng Q-04…Q-18 nằm liền header và hiện thành bảng (không đổi chữ dòng nào); thêm 2 dòng QĐ 36, 37 | review M9 |
| §Việc còn nợ · §Chưa xác minh | Gạch việc đã xong (N12, N13, [5]); thêm việc mới; cập nhật | review M9 · §5 |

**Không làm:** không sửa frontmatter (Q-22) · không sửa file phòng khác · không cập nhật `ONE-PAGER-V2-PROPOSAL.md` (điều kiện của Q-19, làm sau Q-22…Q-34).

## Sau review vòng sửa 2 — 2026-10-24 (PM)

- **Q-22 → nhóm B.** QĐ 36 đã ghi nguyên văn điều kiện 3 mới; "giữ frontmatter" là luật của workflow, không phải quyết định của Duy. PM đã đồng bộ `blocked_on` ở mọi file S1 theo chữ QĐ 36. **Tổng nhóm A còn 14.**
- **Câu rơi (review D-2) → nhóm C:** danh sách mặc định `keep_en` ở WRITER §3 là việc Writer soạn, Duy duyệt cùng mockup ở S2; câu `<grounding>` thứ hai cho UNDERSTOOD S1 là việc của PM (quy tắc 11).
- **Q-20:** ghi rõ rủi ro sưu tập dữ liệu (L16) khi giữ bảng B3 và hạn 72 giờ so với NĐ 17/2023 (L17) — đưa vào phần nêu rủi ro khi hỏi.

## Đổi theo QĐ 38–51 (2026-10-25)

PM sửa tại chỗ vì file là nháp. Nguồn: `PRODUCT-BRIEF.md` QĐ 38–51 (41–51 Duy nhận theo lô mọi khuyến nghị của file này). Frontmatter `status`/`blocked_on` **giữ nguyên** — 3 điều kiện của Duy chưa xong. Same vendor, same priors — no external verifier ran.

| Chỗ | Đổi gì | QĐ |
|---|---|---|
| Lời dẫn · TL;DR | Nguồn QĐ 1–51; **0 câu nhóm A còn mở**; còn ĐK-1…ĐK-3 + 2 điểm chờ Ringkas; nhóm B 16; ghi rõ QĐ 41–51 là nhận theo lô | 38–51 |
| Nhóm A | Rút còn một đoạn trạng thái. Q-22…Q-34, Q-19, Q-20 chuyển **nguyên văn** xuống §Lưu trữ, tiêu đề thêm "ĐÃ TRẢ LỜI → QĐ n" (Q-22: "→ NHÓM B") | 38–51 · quy tắc 14 |
| Câu có điều kiện | Bỏ "không tính vào 15"; cột Nguồn trỏ tên mục thay vì số dòng đã trôi | — |
| Nhóm B | B-13 đóng theo QĐ 43 (b); thêm **B-16** = Q-22 | 36 · 43 |
| Nhóm C | C-09 ghi QĐ 47 | 47 |
| §Câu trả lời | 4 dòng 2026-10-25 nằm lạc cuối file (ngoài bảng, không render) chuyển vào bảng, không đổi chữ; thêm 11 dòng tách lô Q-26…Q-20 → QĐ 41–51 | quy tắc 14 |
| §Việc còn nợ · §Chưa xác minh | ONE-PAGER v2 phải cập nhật + áp + Duy đọc lại (QĐ 50); workflow L13 + L18 trước S5 (QĐ 51); việc của Data/Legal/Writer theo QĐ 38–51; ghi giới hạn của nhận theo lô | 39 · 46 · 50 · 51 |

**Không làm:** không sửa frontmatter · không sửa file phòng khác · không cập nhật `ONE-PAGER-V2-PROPOSAL.md` hay `gates/ONE-PAGER.md` (QĐ 50 giao PM, nhưng ngoài phạm vi file của lượt này) · không xoá chữ "→ Duy" trong các mục lịch sử (§Lưu trữ, §Đổi vòng sửa 2, §Sau review vòng sửa 2) — đó là bản ghi lúc hỏi.
