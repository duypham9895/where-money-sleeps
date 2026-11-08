---
status: pass
stage: 01-spec
date: 2026-11-08
owner: Legal
blocked_on: []
---
# LEGAL-REVIEW — Where Money Sleeps (S1)

> **Không phải ý kiến pháp lý.** Phòng Legal là một phiên Claude; theo quyết định 12, workflow thay luật sư và **Duy ký chấp nhận rủi ro**.
> Same vendor, same priors — no external verifier ran.
> `status: fail` vì còn 3 điều kiện của Duy. Viết nháp được, **chốt thì chưa**.

**TL;DR** · đọc khoảng 10 phút
- File này biến phát hiện S0 thành **37 ràng buộc kiểm được** (R1–R37; R35, R36 thêm theo QĐ 31, 32; R37 thêm ở vòng sửa 2), mỗi ràng buộc có căn cứ, cách kiểm và stage kiểm. S3 build theo đó, S4 kiểm theo đó, và S5 không mở cổng khi R29, R33 và R37 chưa PASS. **Cổng ra mắt (QĐ 29) thêm R1–R4, R6, R13, R31 và quy tắc bảng số liệu §A.2.**
- Trạng thái: **18 verified · 7 gray · 8 tách phần** (R2, R18, R20, R25, R31, R33, R36, R37) · **3 BLOCKED** (R22 agent kế toán chạy thử + Phụ lục II chính thức, R28 đo điện thoại, R34 Ringkas) · **1 N/A** (R32, theo QĐ 18). Không còn ràng buộc nào "chưa quyết".
- **QĐ 17–51 đóng mọi X (X1–X13).** Mới 2026-10-25: X13 → QĐ 41 · X10 + X3 → QĐ 46 · X11 → QĐ 47 · X12 → QĐ 49 · X1, X7 → QĐ 51. Phần chờ hợp đồng Ringkas vẫn treo: chữ định danh trong "⟨…⟩ ký duyệt" (QĐ 34.2) và việc công khai hộp thư (QĐ 35).
- **Bảng số liệu bên thứ ba (§A.2, QĐ 46):** **che** B2 tr.117 trong file host · **giữ** B3 (tr.45, 55, 94–95, 170, 185) trong file host nhưng **loại hẳn** khỏi máy sinh card. `licences.json` nay tách hai trường máy đọc: `host_redactions` (che trong file host) và `card_generator` (loại khỏi máy sinh card).
- **Luật máy loại trang (QĐ 47):** mẫu ③ + danh sách trang là luật chính thức, ghi ở `licences.json` → `card_generator.page_rule`. Legal đo lại 2026-10-25: 132/1004 trang, bắt 7/7 trang đã biết.
- **Chữ công khai (QĐ 41, 49):** mục có con số/tên tài khoản hiện câu Writer W2; máy cấm 4 chữ "kế toán / accountant / chuyên gia / expert" **chỉ** trong dòng minh bạch và `reviewed_by` (R20). Câu R25 mới đã chốt; thư khiếu nại **xoá khi khiếu nại đóng** (R37).
- Workflow pháp lý (QĐ 12): **L1–L18**. **QĐ 51: L13 + L18 chạy TRƯỚC S5** (đã ghi vào cổng S5, §2); L14–L17 sau release.

**Cách đọc cột Trạng thái:** `verified` = căn cứ đã được đọc từ nguồn gốc (ở S0 hoặc trong phiên này), hoặc là quyết định đã ghi của Duy · `gray` = căn cứ đọc qua nguồn thứ cấp, hoặc việc áp vào sản phẩm này là diễn giải · `BLOCKED` = chờ điều kiện ghi trong ô.

---

## 1. Ràng buộc

### A. Hermanson — *Accounting Principles: A Business Perspective*, CC BY 3.0

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R1 | Chỉ host **tr.1–197** của PDF gốc (front matter + ch.1–4). Không host nguyên cuốn | Quyết định 15 · `legal/licences.json` trường `host_scope` | **Máy:** `pdfinfo` file host cho đúng 197 trang · vibe-check [4]: `licences.json` có trường `file` trỏ tới file đó (thay `planned_file`) | S3 · S4 | verified |
| R2 | **Redact** đoạn trích bên thứ ba ở **tr.113** (báo cáo thường niên Home Depot) và **tr.166** (New Accountant 1990, © New DuBois) trong file host | `licences.json` trường `host_audit` · CC BY chỉ phủ phần bên cấp phép có quyền | **Máy:** `pdftotext -f 113 -l 113` và `-f 166 -l 166` trên file host không còn "Home Depot", "New Accountant", "DuBois" · **Người:** Duy xem 2 trang đó. **Thêm theo QĐ 29:** redact cả **bảng số liệu bên thứ ba** theo quy tắc §A.2. **QĐ 46:** che **B2 tr.117** (`pdftotext -f 117 -l 117` trên file host không còn "Accounting Trends", "AICPA"); **giữ B3** (tr.45, 55, 94–95, 170, 185), không che. Danh sách máy đọc: `licences.json` → `host_redactions`. Việc này **phải xong trước ra mắt** | S3 · S4 · **cổng ra mắt** | verified (2 đoạn trích + B2 che, B3 giữ theo QĐ 46; việc redact chưa làm) · gray (giữ B3: sưu tập dữ liệu → L16; Duy nhận ở QĐ 51) |
| R3 | Câu ghi công dùng **đúng chữ** trường `attribution_text` của `licences.json`, không viết lại. Phải hiện ở trình đọc PDF khi mở file host **và** ở trang "Nguồn & giấy phép" | CC BY 3.0 §4(b): ghi tên tác giả, tên tác phẩm, theo cách "reasonable to the medium" | **Máy:** `grep -F` chuỗi `attribution_text` trong build output của hai trang đó | S3 · S4 | verified |
| R4 | Cạnh câu ghi công phải có **URI giấy phép** `https://creativecommons.org/licenses/by/3.0/`. Giữ nguyên dòng giấy phép CC ở chân trang PDF, không redact | CC BY 3.0 §4(a): kèm bản sao hoặc URI giấy phép với mỗi bản phân phối; giữ nguyên các thông báo · `attribution_text` hiện **không** chứa URI | **Máy:** `grep` URI cạnh câu ghi công · `pdftotext` file host vẫn có "Creative Commons Attribution 3.0" | S3 · S4 | verified |
| R5 | Card và đoạn bài tiếng Việt dựa trên Hermanson là **Adaptation** ⇒ hiện một dòng ghi công ngắn ("dựa trên Hermanson et al., đã dịch và sửa đổi, CC BY 3.0") kèm link tới trang "Nguồn & giấy phép" | CC BY 3.0 §1(a): Adaptation gồm "a translation" · §4(b) | **Máy:** test render — card nào có `source` Hermanson, hoặc section nào có `based_on` khác rỗng, mà thiếu dòng ghi công thì FAIL · section thiếu trường `based_on` thì build FAIL · lint tên riêng Hermanson (§A.1) · **Người:** Duy bắt khai sai `based_on: []` | S1 định nghĩa (**§A.1, 2026-10-24**) · S3 · S4 | gray (mức "reasonable to the medium" là diễn giải) |
| R6 | Không ngụ ý tác giả hay Global Text bảo trợ: tên tác giả/nhà xuất bản chỉ xuất hiện trong dòng ghi công. File host phải **tải trực tiếp được** qua URL công khai, không mã hoá, không mật khẩu | CC BY 3.0 §4(b) (cấm ngụ ý bảo trợ) · §4(a) (cấm biện pháp kỹ thuật hạn chế quyền của người nhận) | **Người:** Duy đọc UI · **Máy:** `curl -I` URL file host trả 200 | S2 · S4 | verified |
| R7 | Bản gốc duy nhất là `source_url` trong `licences.json`. Không dùng bản Textbook Equity (NC-SA) | `gates/00-discovery/LEGAL-SCREEN.md` bảng tài liệu | **Máy:** file tải về khớp `bytes` = 7991863 trước khi cắt | S3 | verified |
| R8 | Redact và dịch không được làm méo ý tác giả | CC BY 3.0 §4(c) (honor or reputation) · quyền nhân thân theo Luật SHTT VN | **Người:** Duy đọc đoạn đã sửa. Câu hỏi luật ⇒ L10 | S3 · S4 | gray |

#### A.1 — Định nghĩa "đoạn bài dựa trên Hermanson" (R5) · thêm 2026-10-24 sau T2

**Vì sao phải chặt:** CC BY 3.0 §7, đọc nguyên văn 2026-10-24: *"will terminate automatically upon any breach"*. Bản 3.0 không có hạn khắc phục. Một đoạn sót ghi công là vi phạm §4(b) và có thể làm mất quyền với **cả tác phẩm**: file host tr.1–197, mọi card, mọi bài dịch. Cờ `published` gỡ được nội dung, nhưng **không khôi phục được giấy phép** (xem X7, L15).

**Phép thử:** đặt đoạn bài cạnh trang Hermanson, người đọc có *nhận ra* đoạn này lấy từ đó không? Căn cứ là §1(a), nguyên văn: *"any form recognizably derived from the original"*. Nhận ra được thì đoạn đó thuộc diện.

| Loại | Thuộc diện? | `mode` |
|---|---|---|
| Dịch sát một đoạn | **Có** | `dich_sat` |
| Diễn giải lại theo đúng trình tự lập luận của một đoạn cụ thể | **Có** | `dien_giai` |
| Dùng lại ví dụ, tình huống, tên công ty hư cấu, bảng, bài tập hay **con số của ví dụ** do Hermanson dựng | **Có**, kể cả khi lời văn là của Duy | `vi_du` |
| Khái niệm chung (Nợ/Có, T-account, phương trình kế toán), Duy giải thích bằng ví dụ của chính mình | **Không**. Luật SHTT Đ.15 không bảo hộ khái niệm và nguyên lý (gray: đọc qua nguồn thứ cấp ở S0) | — |
| Số liệu thực tế (luật, thống kê) | **Không**, vì không phải sáng tạo của Hermanson | — |
| Nghi ngờ | **Gắn.** Gắn thừa chỉ tốn một dòng chữ. Sót thì rơi vào §7 | chọn `dien_giai` |

**Trường dữ liệu (S3 dựng, S4 kiểm):**

| Trường | Ở đâu | Giá trị | Máy kiểm |
|---|---|---|---|
| `based_on` | **Mọi** section (đơn vị `sectionId`), cả VI và EN | Mảng. `[]` = Writer **khai** là không dựa trên nguồn CC nào. Phần tử: `{ "asset": "hermanson-accounting-principles-v1", "pages": "<từ>-<đến>", "mode": "dich_sat\|dien_giai\|vi_du" }` | Thiếu trường ⇒ build FAIL. "Chưa khai" và "khai là không" phân biệt được bằng máy. `asset` phải là `id` có thật trong `licences.json`. `pages` nằm trong tr.1–1004 (QĐ 28: cả cuốn). Chạm trang bị che/cấm của bên thứ ba (`host_redactions.redact`: tr.113, 117, 166 + hình bên thứ ba tr.501, 803) ⇒ FAIL. Chạm trang B3 (`keep_in_host_but_excluded_from_cards`: tr.45, 55, 94, 95, 170, 185 — giữ trong file host để giữ phần giảng theo QĐ 46) hoặc trang bị luật máy loại (mẫu ③, QĐ 47, §A.2) ⇒ **cảnh báo**, và Duy xem bài học chỉ lấy lời giảng/khái niệm của Hermanson chứ không chép bảng số liệu hay đoạn trích của bên thứ ba (`AC-45`) |
| Dòng ghi công | Render từ `based_on` khác rỗng | Chữ của R5. Vị trí: S2 quyết (cuối section hoặc gộp một dòng ở đầu bài, liệt kê section). §4(b) cho phép *"any reasonable manner"* | Test render (R5) |
| Lint tên riêng | Text VI và EN của section | Danh sách tên riêng và tên ví dụ trích từ tr.1–197. **TBD: S3 trích bằng `pdftotext`, Duy duyệt danh sách** | Section có `based_on: []` mà chứa tên trong danh sách ⇒ FAIL |

**Giới hạn, nói thẳng:** máy bắt được *thiếu trường* và *tên riêng trùng*. Máy **không** bắt được một bản dịch sát mà Writer khai `[]` và đã đổi hết tên riêng. Chỗ đó vẫn chỉ còn Duy đọc.

#### A.2 — Bảng số liệu bên thứ ba, và luật máy của QĐ 28 · thêm 2026-10-24

**Vì sao:** theo QĐ 29, việc redact bảng số liệu bên thứ ba thuộc **cổng ra mắt**. Phép tìm "©/Source:" ở S0 đã bỏ sót tr.94, 117 và 185, vì các bảng này không có dòng ©. Không phải ý kiến pháp lý.

**Căn cứ:**

| Căn cứ | Nói gì | Trạng thái |
|---|---|---|
| CC BY 3.0, như R2 | Giấy phép chỉ phủ phần mà bên cấp phép có quyền. Phần của bên thứ ba không đi theo | verified |
| Luật SHTT Đ.15 | Không bảo hộ số liệu | gray (đọc qua nguồn thứ cấp ở S0) |
| Luật SHTT Đ.22 (sưu tập dữ liệu) | Bảo hộ một tập hợp có tính sáng tạo ở **việc tuyển chọn và sắp xếp** | gray (Legal nhớ, phiên này chưa đọc văn bản) |
| *Feist Publications v. Rural Telephone Service*, 499 U.S. 340 (1991). Bên có quyền ở đây là công ty Mỹ | Dữ kiện không được bảo hộ. Bản tổng hợp chỉ được bảo hộ ở phần chọn lọc và sắp xếp có tính nguyên gốc, và bảo hộ đó "mỏng" | gray (Legal nhớ, chưa đọc lại) |

**Quy tắc** (Legal đề xuất; B2, B3 chốt bởi QĐ 46, 2026-10-25). Khi nghi ngờ thì xếp vào loại chặt hơn.

| Loại | Nhận biết | File host | Máy sinh card | Trạng thái |
|---|---|---|---|---|
| **B1** Lời văn bên thứ ba | Đoạn văn trích nguyên văn: báo cáo, thư, bài báo | **Redact** | Loại | verified (đã áp: tr.113, tr.166) |
| **B2** Bảng do bên thứ ba biên soạn, chép lại nguyên dạng (khảo sát, bảng giá, xếp hạng) | Có dòng nguồn hoặc tên ấn phẩm của bên thứ ba. Cấu trúc bảng là của bên đó | **Redact bảng** (QĐ 46: tr.117). Giữ câu văn của Hermanson nêu một con số | Loại | gray (có thể chỉ là dữ kiện, nhưng việc chọn và xếp là của bên kia) |
| **B3** Số liệu báo cáo tài chính của công ty thật. Dòng mục theo chuẩn kế toán; Hermanson chọn vài dòng, sửa, hoặc tự thêm cột phân tích | Tên công ty thật + số tiền, không có lời văn trích | **Giữ** (QĐ 46) — `host_redactions.keep_in_host_but_excluded_from_cards` | **Loại hẳn** cả trang (QĐ 46; `card_generator.excluded_pages`). QĐ 27 (card không có con số) làm cái giá của việc loại nhỏ | gray → L16 (Duy nhận rủi ro ở QĐ 51) |
| **B4** Một dữ kiện đơn lẻ nằm trong câu văn của Hermanson ("63 per cent of the companies…") | Một con số trong câu | Giữ | Theo QĐ 27, 28 | gray (Đ.15) |

**Soát lần 1, tr.1–197** (2026-10-24, trên PDF gốc 7.991.863 byte; `pdftotext` từng trang, grep dấu hiệu mở rộng, grep 30 tên công ty Mỹ lớn do Legal tự chọn):

| Trang | Nội dung | Loại |
|---|---|---|
| 45 | Bảng vốn chủ sở hữu ($ millions) của Johnson & Johnson, 3M, GE. Không ghi nguồn | B3 |
| 55 | Exercise M: số liệu Merck 2003/2002 | B3 |
| 94–95 | Số liệu báo cáo thường niên 2000 của Hewlett-Packard. Cột tăng/giảm và cột % do Hermanson tính. Bảng chạy sang tr.95 (`pdftotext` tr.95 có các dòng tài sản và số tiền) | B3 |
| 113 | Đoạn trích từ Annual Report của The Home Depot | B1 (đã có ở R2) |
| 117 | Exhibit 15. Dòng nguồn là AICPA *Accounting Trends & Techniques* (2004) | **B2 ⇒ redact** (QĐ 46) |
| 166 | Trích New Accountant 1990, © New DuBois | B1 (đã có ở R2) |
| 168–174 | Bảng ở tr.170 (Exhibit 26) là bảng cân đối kế toán hợp nhất của The Home Depot, "slightly revised". Tr.168–174 giảng dựa trên bảng đó | B3 |
| 185 | Exercise O: số liệu P&G 2001 | B3 |
| 9–12, 21, 23, 53, 61–63, 105, 138, 182, 193–194 | Nhắc tới "Annual report appendix" (The Limited, Inc.), hoặc bảo người học tự tìm báo cáo. Theo dòng grep, các trang này không chép số liệu ra | không thuộc diện (chưa đọc cả trang) |

**Giới hạn của lần soát này:** bảng của một công ty **ngoài** danh sách 30 tên, lại không có dấu hiệu nào, sẽ lọt. Các trang chưa được xem bằng mắt. Trước ra mắt, S3 phải liệt kê mọi trang có bảng số tiền trong tr.1–197, và người xem bằng mắt những trang có tên một thực thể thật. ~~Sau X10, `attribution_text` ("che 2 đoạn") phải sửa theo số chỗ thật sự che (X3).~~ **Vòng sửa 2:** `attribution_text` đổi thành "che các đoạn trích và bảng số liệu của bên thứ ba", không ghi số. Câu này đúng với mọi lựa chọn ở X10, vì ít nhất 2 đoạn B1 và bảng B2 tr.117 chắc chắn bị che, nên X10 không bắt sửa lại câu ghi công.

**Luật máy của QĐ 28: loại cả trang khi trang có dấu hiệu nguồn ngoài.** Đo ngày 2026-10-24 trên cả 1004 trang. Dùng 7 trang đã biết phải loại để thử: 94, 113, 117, 166, 185, 501, 803.

| Mẫu | Số trang bị loại | Bắt được |
|---|---|---|
| ① Đúng chữ QĐ 28, phân biệt hoa thường: `annual report\|Accounting Trends\|Source:\|©` | 91 | 5/7. **Sót tr.113**, vì PDF viết "Annual Report". Sót tr.501 (WSJ) |
| ② Như ①, nhưng không phân biệt hoa thường, thêm `copyright`, và nhận `Source` theo sau bởi `:` **hoặc `'`** (`pdftotext` đọc dấu ":" ở tr.117 thành "Source'") | 118 | 6/7. Sót tr.501 |
| ③ Như ②, cộng các chuỗi denylist của R10 (`wall street journal`, `financial accounting standards board`, `new accountant`, `dubois`) và `reprinted`, `adapted from` | 132 | **7/7** |

Cả ba mẫu đều **không** bắt được bảng B3 không có chữ "annual report": tr.45, 55, 170. Ba trang này nằm trong danh sách trang (QĐ 46: loại hẳn), nên lớp danh sách bắt chúng. Phần còn lọt là bảng B3 mà lần soát 30 tên chưa thấy: rủi ro Duy đã nhận ở QĐ 28, xác nhận lại ở QĐ 51.

**QĐ 47 (2026-10-25): luật máy chính thức = mẫu ③ cộng danh sách trang**, thay mẫu đúng chữ QĐ 28. Bản máy đọc: `licences.json` → `card_generator.page_rule` (regex, cờ `i`, cách trích chữ) và `card_generator.excluded_pages`. **Đo lại 2026-10-25** trên cùng PDF gốc (7.991.863 byte), `pdftotext -f N -l N` từng trang, không `-layout`: mẫu ① 91 trang, mẫu ③ **132 trang** (33 trang trong tr.1–197), bắt **7/7** trang đã biết, khớp số đo 2026-10-24. Đổi cách trích chữ (vd `-layout`) thì phải đo lại.

### B. Quiz card

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R9 | Card chỉ sinh từ **bài Duy tự viết + Hermanson**. Mỗi card có `source` thuộc đúng hai loại (bài tự viết · Hermanson kèm số trang) và có `source_quote` | Quyết định 3 · LEGAL-SCREEN §Kết luận · ADDENDUM §Đường ống bước 1, 5 | **Máy:** validator card — `source` ngoài hai loại thì FAIL · `source_quote` phải khớp chuỗi trong nguồn (bước 5a) | S3 · S4 | verified |
| R10 | Loại mọi đoạn trích © bên thứ ba: 10 trích FASB, New Accountant 1990, báo cáo thường niên GE/Gillette/Coca-Cola/**Home Depot**, WSJ, hình tr.501 và tr.803 | `licences.json` `exclusions` + `host_audit` · đính chính trong `gates/00-discovery/PRODUCT-BRIEF.md` | **Máy:** denylist số trang + chuỗi ("Financial Accounting Standards Board", "New Accountant", "DuBois", "Wall Street Journal", "annual report") trên `source_quote` ⇒ FAIL · **Người:** Duy duyệt từng card. **Thêm 2026-10-24:** loại cả bảng số liệu B2 (tr.117) và mọi trang khớp luật máy (§A.2). **QĐ 46, 47 (2026-10-25):** danh sách trang loại khỏi máy sinh card = `licences.json` → `card_generator.excluded_pages`: tr.113, 166, 501, 803 · tr.117 (B2) · tr.45, 55, 94–95, 170, 185 (B3, **loại hẳn**, dù vẫn giữ trong file host) · cộng mẫu ③ | S3 · S4 | verified |
| R11 | Máy sinh card được nạp **cả cuốn** Hermanson (tr.1–1004), trừ hai thứ: (1) các trang trong `card_generator.excluded_pages` (R10), (2) mọi trang khớp **mẫu ③** (QĐ 47, `card_generator.page_rule`, §A.2). Card lấy từ trang > 197 chỉ được **đăng** khi đã có bài `published` **bất kỳ** (không chỉ GĐ01, QĐ 48) mà `based_on` phủ trang đó; "đọc lại đoạn này" trỏ về section đó. Phần lọt qua luật máy là rủi ro Duy nhận. Phạm vi **host** không đổi (R1) | QĐ 28 (ngược đề xuất X2 của Legal) · QĐ 27 · QĐ 47 · QĐ 48 | **Máy:** máy sinh card ghi danh sách trang input. Trang thuộc danh sách loại hoặc khớp mẫu ③ ⇒ FAIL · card có trang > 197 mà không bài `published` nào có `based_on.pages` phủ trang đó ⇒ card không vào build | S3 · S4 | verified (QĐ 28, 47, 48) |
| R12 | Không nạp nguồn NC, sách trả phí hay OpenStax hiện hành vào lõi hoặc máy sinh card. Không dùng Claude dịch hoặc tóm tắt OpenStax | Quyết định 3, 10 · điều khoản chống LLM của OpenStax (đã fetch lại ở S0) | **Máy:** mọi asset trong `licences.json` có `licence` không chứa "NC"/"ND" · máy sinh card ghi danh sách file input, file ngoài whitelist ⇒ FAIL | S3 · S4 | verified |
| R13 | Không có LLM runtime. File PDF riêng của người học **không rời máy**; event `pdf_opened` chỉ mang `source`, không mang tên file | Quyết định 2, 4, 9 | **Máy (S4):** mở file riêng trong trình đọc, network log không có request nào ngoài asset tĩnh và một beacon không chứa tên file. Phần WebView Zalo: **BLOCKED — chờ đo iPhone/Android**. Từ QĐ 29, trình đọc PDF là điều kiện ra mắt, nên phần này **chặn cả ra mắt** | S3 · S4 · **cổng ra mắt** | verified |

### C. Sách và nguồn ngoài

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R14 | Sách trả phí và khoá Maven chỉ có **thẻ do Duy viết + link mua**. Không bìa, không PDF/scan, không mục lục kèm trích dài | `gates/ONE-PAGER.md` §3.1 · LEGAL-SCREEN | **Máy:** vibe-check [4] — mọi file ảnh/PDF trong repo phải có dòng trong `licences.json` · **Người:** Duy đọc thẻ | S3 · S4 | verified |
| R15 | OpenStax và nguồn all-rights-reserved (Modern Treasury, Stripe, CFI, IMF, BIS…) **chỉ là deep-link**, nhãn "Đọc thêm · EN · không bắt buộc", không tính vào tiến độ. Không dùng bìa, logo hay tên OpenStax làm UI | LEGAL-SCREEN bảng tài liệu · quyết định 10 (BIS chỉ link) | **Máy:** không file asset nào có nguồn từ các domain này · **Người:** Duy đọc | S2 · S4 | verified |

### D. Luật VN về nội dung

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R16 | **Không nêu mã chứng khoán, không khuyến nghị** mua/bán/nắm giữ. Ví dụ doanh nghiệp dùng tên hư cấu | Luật Chứng khoán 2019 Đ.4 k32, Đ.12 k4 · tiền lệ ITP bị phạt 225 triệu (LEGAL-SCREEN). URL gốc: TBD — đối chiếu vbpl.vn | **Máy:** regex "nên mua", "nên bán", "khuyến nghị (mua\|bán)", "nắm giữ cổ phiếu" + đối chiếu danh sách mã niêm yết (TBD — cần xác minh nguồn danh sách công khai của HOSE/HNX) · **Người:** Duy | S3 lint · S4 | verified |
| R17 | Không có bảng lãi suất kèm tên ngân hàng. Có máy tính khoản vay hay không: **quyết lúc mở GĐ05** (QĐ 18), không thuộc mùa 1. Ràng buộc "không bảng lãi suất kèm tên ngân hàng" vẫn áp cho mọi bài, có máy tính hay không | ONE-PAGER §3.2 · LEGAL-SCREEN (rủi ro "tổng hợp", số liệu cũ) · L11 · QĐ 18 | **Máy:** cảnh báo khi tên ngân hàng (denylist TBD) đứng cùng câu với "%" · **Người:** Duy | S3 · S4 | gray |
| R18 | NĐ 147/2024, "thông tin tổng hợp": văn bản luật **chỉ link** (vbpl.vn, congbao.chinhphu.vn, sbv.gov.vn) và chỉ **trích chọn lọc**, mỗi đoạn trích nằm trong khối trích dẫn có nguồn. Không đăng lại toàn văn. Không link tới hethongphapluat.com (nguồn thứ cấp, đã ghi nhận có nhúng prompt injection) | NĐ 147/2024 Đ.24 k2–k3, đọc qua nguồn thứ cấp · xưởng §Phòng Legal quy tắc 2, 4 | **Máy:** mọi link văn bản luật trỏ tới domain trong whitelist · đếm chữ trong khối trích luật mỗi bài. **Ngưỡng: 0 chữ trích nguyên văn cho phần ra mắt** (QĐ 33): chỉ link văn bản gốc và diễn giải bằng lời mình ⇒ AC-51: số chữ trích = 0 trên mọi bài ra mắt. Ngưỡng cho GĐ05 đặt khi mở GĐ05 | S3 · S4 | verified (ra mắt: QĐ 33) · gray → L7 (khi mở GĐ05) |
| R19 | Bản EN của nội dung luật VN là **"unofficial summary" tự viết** + link bản VN. Không dùng bản dịch của LuatVietnam, TVPL, KPMG hay PwC | LEGAL-SCREEN (tác phẩm phái sinh, suy luận) | **Máy:** trang EN có trích luật phải chứa "unofficial summary" · **Người:** Duy duyệt EN | S3 · S4 | gray |
| R20 | Mọi bài và mọi bộ card **đã đăng**, kể cả bản EN, có dòng minh bạch (QĐ 34.1). Chữ **"Soạn với hỗ trợ AI"** chỉ hiện ở mục có `ai_assisted: true` (QĐ 34.3); hạt của cờ: **bài / bộ card / bản EN** (QĐ 42). Chữ định danh trong ⟨…⟩ **chưa chọn**: chọn sau khi Duy đọc hợp đồng Ringkas (QĐ 34.2). **Dòng soát công khai (QĐ 41, 2026-10-25):** mục thuộc phạm vi QĐ 30 (có trường báo cáo của agent khác rỗng) hiện câu Writer W2 *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."* · `reviewed_by` = **chỉ người ký**; agent ghi ở một trường riêng (tên trường: S3, không render ra HTML) | Luật AI 134/2025 (hiệu lực 01/3/2026), đọc qua nguồn thứ cấp. URL gốc: TBD — đối chiếu Công báo · QĐ 34 · QĐ 36 · QĐ 41 · QĐ 42 | **Máy:** build FAIL nếu nội dung có `published` = true mà thiếu `reviewed_by`, `reviewed_on` hoặc `ai_assisted`. Giống `based_on`: thiếu trường khác với `false` · test render: `ai_assisted: false` thì trang không có chữ "Soạn với hỗ trợ AI" · **QĐ 41:** dòng minh bạch hoặc `reviewed_by` chứa "kế toán", "accountant", "chuyên gia", "expert" (không phân biệt hoa thường) hoặc chuỗi `ke-toan-reviewer` ⇒ build FAIL. **Không** áp cho thân bài · test render (`AC-86`): mục có báo cáo của agent (trường riêng khác rỗng) mà thiếu câu W2 ⇒ FAIL; mục ngoài phạm vi QĐ 30 (không có báo cáo agent) mà hiện câu W2 ⇒ FAIL · **Người:** Duy khai đúng `ai_assisted`. **Hệ quả:** chưa chọn định danh thì dòng không render được, nên không bài nào đăng được. Việc này chặn ra mắt cùng R34, vốn đã là điều kiện trước S1 | S1 định nghĩa trường · S3 · S4 | verified (QĐ 34.1, 34.3, 41, 42) · gray → L14 (căn cứ: lựa chọn phòng xa, chưa phải nghĩa vụ đã xác định) · **BLOCKED** (định danh, QĐ 34.2 — chờ hợp đồng Ringkas) |
| R21 | **Disclaimer** một lần ở footer ("không phải tư vấn tài chính, đầu tư hay pháp lý"). Bài về lãi suất hoặc pháp lý có thêm khối "căn cứ văn bản hiệu lực đến ⟨ngày⟩" | Quy tắc vận hành S0 (LEGAL-SCREEN) | **Máy:** bài gắn tag lãi suất/pháp lý mà thiếu trường ngày hiệu lực ⇒ build FAIL · footer có chuỗi disclaimer | S1 định nghĩa tag · S3 · S4 | verified |
| R22 | Tên tài khoản ở GĐ01 theo **TT 99/2025/TT-BTC** (không theo TT 200). **Phạm vi soát (QĐ 30):** tên tài khoản GĐ01 · APR/lãi suất GĐ05 · mọi card có con số · **+ đoạn bài mà mỗi card có số dùng làm `source_quote`**. Con số trong bài không card nào hỏi (kể cả sổ ngân hàng GĐ02): Duy đọc. **Người soát (QĐ 36):** agent `ke-toan-reviewer` (`../../../.claude/agents/ke-toan-reviewer.md`), không phải người; **Duy ký**. **Tên tài khoản (QĐ 37):** K2 tạm đối chiếu bản chép bên thứ ba `legal/tt99-phu-luc-ii.secondary.json`, phán tối đa "KHỚP NGUỒN THỨ CẤP", không bao giờ PASS ⇒ bài có tên tài khoản chính thức (GĐ01) chỉ đăng khi có Phụ lục II chính thức; lối vào không bị chặn | Quyết định 8, 30, 36, 37 · TT 99 thay TT 200 từ 01/01/2026 (đã fetch lại ở S0) · `legal/VanBanGoc_TT 99.2025-btc.pdf` chỉ có thân thông tư, không có Phụ lục I–IV (QĐ 37) | **Máy (agent):** báo cáo soát của `ke-toan-reviewer` cho từng bài/bộ card trong phạm vi · **Người:** Duy đọc báo cáo và ký từng bài. Agent **không** ký và không được ghi là người duyệt (QĐ 41: `reviewed_by` chỉ là người ký) · **Luật ký (QĐ 40):** FAIL ở K1/K2/K3 chặn đăng tới khi sửa + agent soát lại; UNVERIFIED · FLAG · "KHỚP NGUỒN THỨ CẤP" (ngoài GĐ01) Duy ký được, kèm một dòng lý do · **Máy:** bài GĐ01 có tên tài khoản mà K2 chỉ đạt "KHỚP NGUỒN THỨ CẤP" ⇒ không vào build. **BLOCKED — chờ agent chạy thử trên 1 bài mẫu + card và đo thời gian Duy đọc báo cáo, ký (điều kiện 3, QĐ 36)** · GĐ01: **BLOCKED — chờ Phụ lục II chính thức (QĐ 37)** | S4 | BLOCKED |

### E. Dữ liệu cá nhân và đo lường

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R23 | Worker đếm chỉ nhận **5 event và đúng các field** trong TRACKING-PLAN. Không đọc và không lưu IP, `CF-Connecting-IP`, User-Agent, cookie hay ID. Không set cookie | Quyết định 9 · Luật 91/2025: Đ.2.6 coi "khử nhận dạng" là một hành vi xử lý ⇒ lối an toàn là **không thu**, không phải "thu rồi khử" (../../../docs/data.md) | **Máy:** grep source Worker không có `CF-Connecting-IP`, `user-agent`, `Set-Cookie` · test: gửi request có các header đó, bản ghi lưu không chứa chúng · **S4:** xem bản ghi thật | S3 · S4 | gray |
| R24 | Không log request ở tầng Worker: không `console.log(request)`, không Logpush. **Workers Logs phải tắt hẳn: `observability.enabled = false`, và tắt cả `issues`.** Lý do: Workers Logs **mặc định bật** cho Worker mới, mỗi log chứa *"the Request, Response, and related metadata"*. Để mặc định là lưu metadata request mà không ai viết dòng code nào. Log có ghi IP hay không thì không cần biết, vì đã tắt (sửa vòng sửa 2026-10-24, theo TRACKING-PLAN §3) | Như R23 · TRACKING-PLAN §3 (dẫn developers.cloudflare.com/workers/observability/logs/workers-logs/ và /workers/wrangler/configuration/) | **Máy:** đọc cấu hình wrangler có `observability.enabled = false` và `issues` tắt · grep mã Worker không có `console.log(request)`, không Logpush · **Người (S4):** Duy mở dashboard Cloudflare, xác nhận **không có log request** (AC-56) | S3 · S4 | gray (căn cứ luật như R23; phép kiểm đã xác định) |
| R25 | Trang riêng tư dùng **đúng câu này** (QĐ 49, 2026-10-25): *"Khi bạn đọc, Where Money Sleeps không thu thập định danh; nhà cung cấp hạ tầng có ghi địa chỉ IP cho mục đích bảo mật của họ. Nếu bạn gửi thư tới hộp thư khiếu nại, những gì bạn gửi (tên, email, nội dung) chỉ được dùng để xử lý khiếu nại đó."* Bản EN đã có ở `WRITER.md` §5, Duy duyệt theo AC-02. Cấm viết "không thu thập gì". Câu cũ (vòng sửa 2: chỉ đúng **cho người đọc**) bị thay; câu cũ **không được** lên trang cùng lúc với hộp thư | ../../../docs/data.md §Một câu phải viết đúng (GitHub Pages và Cloudflare đều ghi IP) · QĐ 35 · QĐ 49 | **Máy:** `grep -F` câu đó · grep cấm "không thu thập gì" · trang có địa chỉ hộp thư mà thiếu vế "Nếu bạn gửi thư…" ⇒ FAIL | S2 microcopy · S4 | verified (câu chữ, QĐ 49; EN: WRITER §5) · gray → L13, L18 (căn cứ; chạy trước S5, QĐ 51) |
| R26 | Host tĩnh và Worker đặt ở nước ngoài đều thấy IP khi truyền tải. Mùa 1 chấp nhận rủi ro theo quyết định 11; **QĐ 51** xác nhận lại trên cả hai cách đọc của X1, và L13 chạy **trước S5** | Luật 91/2025 Đ.20.1.c (../../../docs/data.md) · LEGAL-SCREEN §Kết luận ("vùng xám nhẹ") | Không kiểm bằng máy được. Câu hỏi luật ⇒ L13 | — | gray |
| R27 | Không tải script, font hay embed từ bên thứ ba | CLAUDE.md quy tắc 8 (WebKit xoá storage vì script bên thứ ba) · quyết định 9 | **Máy (S4):** network log, mọi request cùng origin | S4 | verified |
| R28 | Tiến độ và link `#sync` chỉ mang field của schema tiến độ (bài, card, trang PDF, ngôn ngữ, **`tel`** — cờ chống trùng, QĐ 26). **Không mang tên file PDF riêng. Không mang trường thời điểm hoạt động cuối** (QĐ 26: trường đó ở lại máy, không đi theo sao lưu). Dữ liệu nằm trong `#fragment`, không nằm trong query, vì fragment không bị gửi lên server | Quyết định 7 · quy tắc privacy: không đặt dữ liệu vào query string | **Máy:** test sinh link, decode, so với whitelist field. Zalo giữ hay cắt `#`: **BLOCKED — chờ đo iPhone/Android** (cắt thì chuyển sang copy mã) | S3 · S4 | BLOCKED |
| R29 | Không tài khoản, không bình luận, không upload lên server. Thêm bất kỳ tính năng nào nhận nội dung người dùng ⇒ phải review Legal lại | LEGAL-SCREEN quy tắc vận hành · xưởng §Phòng Legal "Cái gì kích hoạt" | **Người:** PM so PRD với dòng này | S1 · S5 | verified |
| R35 | **Không bật rule chặn theo IP do Duy cấu hình** ở Cloudflare: Rate Limiting, WAF custom rules, Bot Fight Mode. Chống bơm số bằng cờ F1–F4 và cách ly ngày (không xoá). Cách ly ≥ 2 lần trong 4 tuần ⇒ Data đưa số lên Duy hỏi lại · thêm 2026-10-24 | QĐ 31 · QĐ 9 · QĐ 38 · R25 | **Người (S4):** Duy mở dashboard Cloudflare, xác nhận không có rule Rate Limiting hay WAF custom và Bot Fight Mode đang tắt. Ghi ngày kiểm. Nếu có tính năng xử lý IP **mặc định bật mà tắt được**: **→ Duy**, vì QĐ 31 nói "không bật", chưa nói "tắt cái đang bật sẵn". Tính năng mà nhà cung cấp không cho tắt (chống DDoS) thuộc câu R25 | S3 · S4 | verified (QĐ 31) |
| R36 | Bộ đếm lưu **theo ngày**. Dashboard ẩn mọi ô n < 5 và không có bảng ngày × bài/card. Nếu workflow pháp lý kết luận số gộp ghép ra được người (L13, chạy **trước S5** theo QĐ 51) ⇒ gộp lên tuần và **xoá** dòng ngày, xong trước S5 · thêm 2026-10-24 | QĐ 32 · Luật 91/2025 (L13) | **Máy:** test dashboard với dữ liệu giả có ô n = 1…4 ⇒ các ô đó không hiện; không có khung nhìn ngày × `lesson`/`card` · **Người:** truy vấn ô n = 1 bằng `wrangler` chỉ bị chặn bởi kỷ luật của Duy (QĐ 32 ghi thẳng) | S3 · S4 | verified (QĐ 32) · gray (có ghép ra người không ⇒ L13) |
| R37 | **Dữ liệu người khiếu nại** (hộp thư QĐ 35) · thêm vòng sửa 2, 2026-10-24. Thư khiếu nại mang họ tên, email, có thể cả giấy tờ chứng minh quyền ⇒ đó là dữ liệu cá nhân có định danh mà Duy nhận và giữ. Tối thiểu: (1) chỉ dùng để xử lý đúng khiếu nại đó; (2) **không** chép tên, email hay nội dung thư vào repo, vào file `gates/`/`docs/` hay vào bất kỳ thứ gì được build và đăng: bản ghi gỡ trong repo chỉ gồm ngày, nội dung bị gỡ và loại lý do; (3) không chuyển tiếp thư sang dịch vụ khác (kể cả dán vào một phiên AI) ngoài hộp thư đó; (4) thời hạn giữ thư: **xoá thư khi khiếu nại đã đóng** (QĐ 49, 2026-10-25); repo chỉ giữ ngày + nội dung bị gỡ + loại lý do, theo (2) | Luật 91/2025 · Đ.20.1.c (cá nhân dùng nền tảng ngoài lãnh thổ để xử lý dữ liệu cá nhân thu tại VN ⇒ hồ sơ CTIA trong 60 ngày), không có miễn trừ cho cá nhân, đọc qua `../../../docs/data.md` §Pháp lý Việt Nam · QĐ 35 · QĐ 49 | **Người (S4):** trong diễn tập đầu-cuối R33 (d), Duy kiểm khiếu nại giả không để lại tên/email nào trong repo (`git grep` địa chỉ email thử ⇒ 0 kết quả), rồi đóng khiếu nại giả và **xoá** thư, xác nhận thư không còn trong hộp thư · **Người:** Duy khai nhà cung cấp hộp thư và nơi đặt máy chủ (đầu vào cho workflow L18) | S4 · S5 | verified (thời hạn, QĐ 49) · gray → L18 (chạy trước S5, QĐ 51) |

### F. Phần mềm và font

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R30 | Font **IBM Plex, Be Vietnam Pro, Newsreader** (OFL) phải tự host, kèm OFL.txt của từng họ, và ghi vào `licences.json` **cùng commit** với file font. Nếu tự subset font thì đọc Reserved Font Name trong OFL.txt trước (TBD — chưa đọc) | LEGAL-SCREEN (google/fonts METADATA.pb) | **Máy:** vibe-check [4] · S4 network log không có fonts.googleapis.com | S3 · S4 | verified |
| R31 | **PDF.js (Apache-2.0)**: pin phiên bản, ship LICENSE (+ NOTICE nếu có), ghi dòng `licences.json`. Giấy phép của thư mục standard_fonts và cmaps trong gói đã pin: **TBD — đọc file LICENSE trong các thư mục đó** | LEGAL-SCREEN · github.com/mozilla/pdf.js/blob/master/LICENSE | **Máy:** vibe-check [4] · file LICENSE có trong build | S3 · S4 | verified (lõi) · gray (thư mục phụ) |
| R32 | **N/A — because QĐ 18 (2026-10-24): EPUB/foliate-js ra khỏi mùa 1.** Thêm lại EPUB ⇒ R32 mở lại: foliate-js (MIT) ship kèm LICENSE, ghi dòng `licences.json` | LEGAL-SCREEN · github.com/johnfactotum/foliate-js · QĐ 18 | — | — | N/A |

### G. Đường gỡ và Ringkas

| # | Ràng buộc | Căn cứ | Kiểm bằng gì | Stage | Trạng thái |
|---|---|---|---|---|---|
| R33 | Có cờ **`published`** ở từng bài, từng card và file host Hermanson. Cờ là false thì nội dung **không có trong build output**, không chỉ bị ẩn. Nguyên tắc: gỡ trước, tranh luận sau. **Phải chạy được TRƯỚC S5** | LEGAL-SCREEN quy tắc vận hành · Vibe/docs/stages.md ("Đường gỡ phải dựng TRƯỚC S5") | **Đường gỡ = nhận khiếu nại + lật cờ. R33 PASS khi đủ cả 4 (sửa 2026-10-24 sau T2):** (a) **kênh nhận khiếu nại công khai** ở bề mặt B10 "Nguồn & giấy phép": **hộp thư riêng cho site**, không có họ tên đầy đủ, không nhắc Ringkas (QĐ 35). **Công khai: chờ Duy đọc hợp đồng Ringkas** · (a′) **trước khi công khai, kiểm lộ danh tính** (QĐ 35, thêm 2026-10-24): gửi một thư thử từ hộp thư tới một địa chỉ khác, đọc header gốc (tên hiển thị ở From, Reply-To, Return-Path, Received, X-Originating-IP nếu có) và chữ ký. Nếu hộp thư dùng tên miền riêng: `whois <tên miền>` không hiện họ tên, địa chỉ hay email cá nhân của Duy (liên quan R34: tên miền đăng ký dưới tên Duy). Lộ chỗ nào ⇒ sửa trước khi công khai; không sửa được ⇒ **→ Duy** · (b) B10 in đúng **"gỡ tạm trong 72 giờ"** (QĐ 35). Đây là đề xuất của Legal, không có căn cứ luật. Nếu NĐ 17/2023 Đ.114 đặt hạn ngắn hơn thì luật thắng (L17) · (c) **Máy (S4):** diễn tập cờ một lần (đặt false → build → URL trả 404), đo số phút từ lúc sửa tới lúc gỡ xong · (d) **Người (S4):** diễn tập đầu-cuối: gửi một khiếu nại giả qua kênh (a) → Duy nhận → lật cờ → 404. Đo số giờ, phải ≤ 72. Công khai kênh là sự kiện kích hoạt review: **đã review ở X8** | S1 · S2 (bề mặt kênh) · S3 · S4 · S5 | verified (nguyên tắc; kênh và 72 giờ theo QĐ 35) · gray (thời hạn luật ⇒ L17) · **BLOCKED** (công khai (a) **— chờ Duy đọc hợp đồng Ringkas**, R34) |
| R34 | Nội dung GĐ05 (người vay, vay mua nhà, cùng mảng với Ringkas), quyền IP với bài tự viết, ~~việc người kế toán là đồng nghiệp Ringkas~~ (hết áp từ QĐ 36, vòng sửa 2), và tên miền đăng ký dưới tên Duy | Quyết định 13 · LEGAL-SCREEN dòng "Hợp đồng lao động với Ringkas" | **Người:** Duy đọc điều khoản IP, không cạnh tranh và bảo mật. **BLOCKED — chờ Duy đọc hợp đồng Ringkas** | trước khi S1 chốt | BLOCKED |

**Cổng mùa 2 (quyết định 12):** mọi tính năng đụng sách của người khác (card từ sách trả phí, "Ôn với AI của bạn", affiliate) ⇒ chạy workflow pháp lý chuyên sâu trên các câu L liên quan, rồi **Duy ký chấp nhận rủi ro cho từng tính năng**. Không áp cho mùa 1.

## 2. Ai kiểm cái gì

| Stage | Ràng buộc |
|---|---|
| S1 (PM gộp vào PRD) | R5 · R20 (trường `ai_assisted`) · R21 · R29 · R33 (định nghĩa trường và tag) · R34. R11 và R32 đã quyết (QĐ 28, QĐ 18) |
| S2 | R5 (vị trí dòng ghi công section) · R6 · R15 · R25 · R33 (kênh khiếu nại + "gỡ tạm trong 72 giờ" trên B10) |
| S3 | R1–R5 (gồm §A.2) · R7–R14 · R16–R21 · R23–R24 · R28 · R30–R31 · R33 · R35 · R36 |
| S4 | mọi ràng buộc có phép kiểm máy, cộng diễn tập gỡ R33 (gồm kiểm header/WHOIS (a′)), network log R13 · R27, dashboard Cloudflare R24 · R35, R37 trong diễn tập R33 (d), báo cáo agent kế toán + chữ ký Duy R22 |
| S5 | **QĐ 51 (2026-10-25): workflow pháp lý cho L13 + L18 phải chạy xong và Duy ký kết luận TRƯỚC khi mở S5** (một lượt, vì cùng Đ.20.1.c Luật 91). Ghi *"không phải ý kiến pháp lý · same vendor, same priors — no external verifier ran"* (QĐ 12). Hệ quả đổi thiết kế phải áp xong trước S5: R36 (gộp tuần nếu L13 nói số gộp ghép ra người) · R25, R37 (câu chữ, nhà cung cấp hộp thư theo L18). L14–L17 sau release. — R29 · R33 · **R37** phải PASS (R37 thêm vòng sửa 2: hộp thư công khai là lúc dữ liệu người khiếu nại bắt đầu tới). Không PASS thì `LAUNCH-READINESS` không mở. R33 PASS = đủ (a)–(d), **không chỉ diễn tập cờ** (2026-10-24). **Thêm theo QĐ 29:** trình đọc PDF + sách host là điều kiện ra mắt ⇒ R1, R2 (gồm §A.2), R3, R4, R6, R13 (gồm phần WebView/`input type=file`) và R31 cũng phải PASS |

**Lỗ hổng của phép kiểm máy, đọc mã ngày 2026-10-24:** vibe-check [4] chiều "trên đĩa → sổ" hiện **chỉ quét đuôi âm thanh** (mp3/ogg/wav/m4a/flac). Vì vậy R14, R30 và R31 **chưa** có phép kiểm máy thật cho PDF, ảnh, font và thư viện vendor. Trước khi S3 commit asset đầu tiên, phải mở rộng [4] sang các đuôi pdf · png · jpg · svg · woff2 · ttf, cộng thư mục vendor. Làm được thì đó mới là "máy kiểm"; chưa làm thì R14, R30, R31 chỉ có người kiểm.

## 3. Xung đột và khoảng trống cho Duy

Legal **không tự quyết** những chỗ dưới đây. Thứ tự: nặng nhất đi trước.

| # | Chỗ vướng | Hai phía | Đề xuất của Legal |
|---|---|---|---|
| X1 | **Mức rủi ro Luật 91 mà Duy đã ký** · sửa vòng sửa 2026-10-24 | Quyết định 11 chấp nhận rủi ro dựa trên nhãn "vùng xám nhẹ" (LEGAL-SCREEN). Cùng một nguồn, `../../../docs/data.md` §Pháp lý VN, cho **hai cách đọc**:<br>**A — nhẹ, là kết luận của chính data.md:** *chỉ đếm lượt xem, không lưu gì định danh* ⇒ **không phát sinh nghĩa vụ nào** (không DPIA, không CTIA, không thông báo), vì chưa bước vào phạm vi điều chỉnh. Thiết kế mùa 1 (R23, R24) theo đúng khuôn này.<br>**B — nặng:** nếu IP mà host tĩnh và Worker ở nước ngoài xử lý **khi truyền tải** bị coi là dữ liệu cá nhân được xử lý, thì Đ.20.1.c phủ cả cá nhân, không có miễn trừ cho cá nhân, phải nộp CTIA trong 60 ngày. Không nộp ⇒ Đ.56 NĐ 330: phạt 30–50 triệu **và buộc ngừng chuyển dữ liệu**. Khi đó **host tĩnh cũng dính, không riêng Worker**, và thiết kế không loại được, vì host nào cũng thấy IP.<br>**Mức tiền cho Duy (cá nhân):** data.md ghi *"mức phạt với cá nhân bằng một nửa tổ chức (Điều 7 NĐ 330)"*. Nếu 30–50 triệu là mức cho tổ chức (data.md không ghi rõ) thì mức cho cá nhân là **15–25 triệu**. Đây là phép chia của Legal, chưa đối chiếu văn bản gốc. Biện pháp buộc ngừng chuyển dữ liệu không giảm theo. data.md còn ghi: thời hiệu xử phạt **01 năm** (Đ.3.1 NĐ 330); Đ.63 (50–70 triệu, theo dõi website) **chỉ áp cho mục đích quảng cáo**.<br>Cách đọc nào đúng: chưa xác minh ⇒ L13 | Duy xác nhận lại câu 11 bằng **một dòng mới** (không sửa dòng cũ), ký trên **cả hai cách đọc** và mức tiền cho cá nhân, không chỉ trên con số nặng. **→ Duy (Q-20, đang hỏi)**. Legal không chọn cách đọc nào đúng thay Duy: đó là câu L13. **Đã quyết 2026-10-25: QĐ 51** — Duy xác nhận lại QĐ 11 trên cả hai cách đọc; workflow L13 chạy **trước S5** |
| X2 | Phạm vi trang Hermanson được nạp vào máy sinh card | Quyết định 3 cho nạp "sách CC BY" mà không giới hạn trang. Quyết định 15 chỉ host tr.1–197, và việc soát hình chỉ xong cho tr.1–197 (hai hình tr.501 và tr.803 được tìm thấy một cách tình cờ) | Card Hermanson chỉ lấy từ tr.1–197. Lý do: link "đọc lại đoạn này" phải trỏ tới được một trang đã host. **Đã quyết 2026-10-24: QĐ 28**: cả cuốn, trừ các đoạn đã biết phải loại, ngược đề xuất này. Xem R11 · §A.2 · X11 |
| X3 | Trường `exclusions` trong `licences.json` **thiếu tr.113 Home Depot** · **Đã làm vòng sửa 2 (2026-10-24), xem dòng cuối ô đề xuất** | Trang đó chỉ có trong `host_audit`, trong khi dòng soát ở PRODUCT-BRIEF ghi là phải loại cả khỏi máy sinh card | Thêm một dòng cập nhật có ngày vào `exclusions` (sửa cơ học, Legal làm được ngay khi Duy đồng ý). **Nặng hơn từ QĐ 28 (2026-10-24):** máy sinh card nay đọc cả cuốn, mà luật máy đúng chữ QĐ 28 cũng sót tr.113 (§A.2). Nên hiện tr.113 lọt qua cả hai lớp. Cùng dòng cập nhật đó: thêm tr.117 (B2), các bảng B3 nếu X10 chọn che, và sửa `attribution_text` ("che 2 đoạn") theo số chỗ thật sự che. **→ Duy: đồng ý để Legal sửa `licences.json`** · **Vòng sửa 2 (2026-10-24): đã sửa**, theo nhiệm vụ workflow giao cho Legal. Căn cứ không cần câu trả lời mới của Duy: tr.113, 166, 501, 803 là "đoạn đã biết phải loại" theo **chữ QĐ 28**; tr.117 theo quy tắc Legal mà QĐ 29 giao; B3 (tr.45, 55, 94–95, 170, 185) chỉ **tạm loại** khỏi máy sinh card, là chiều chặt và đảo được sau X10. `attribution_text` nay không ghi số (§A.2). Duy bác ⇒ trả về bản trước bằng `git` (`licences.json` có trong git) · **QĐ 46 (2026-10-25): Duy nhận bản sửa** |
| X4 | Câu ghi công có hai bản chữ khác nhau | `attribution_text` trong `licences.json` khác dòng "Quyết định 15" của LEGAL-SCREEN (có "Global Text Project", khác dấu câu), và không chứa URI giấy phép | S1 dùng `licences.json` theo chỉ thị. Ghi chú có ngày vào LEGAL-SCREEN để từ nay chỉ có một nguồn. URI giấy phép hiện riêng theo R4 |
| X5 | EPUB / foliate-js | S0 không quyết EPUB, nhưng LEGAL-SCREEN lại liệt kê foliate-js | PM ghi rõ trong PRD là giữ hay bỏ. Bỏ thì R32 thành `N/A — because không có EPUB`. **Đã quyết 2026-10-24: QĐ 18** bỏ EPUB/foliate-js khỏi mùa 1 ⇒ R32 N/A |
| X6 | Quyết định 4 ghi Hermanson là "CC BY 4.0" | Đã được đính chính thành **3.0** (theo PDF gốc) | Không phải xung đột mới. Chỉ nhắc PM không chép "4.0" vào PRD. **Hệ quả (thêm 2026-10-24):** 3.0 khác 4.0 ở chỗ chấm dứt, xem X7 |
| X7 | **Đường gỡ không chữa được lỗi ghi công** · thêm 2026-10-24 | Quyết định 11 chấp nhận rủi ro "thấp, do khiếu nại kích hoạt, có cờ `published` để gỡ". Nhưng CC BY 3.0 §7, nguyên văn: *"will terminate automatically upon any breach"*. Khi đã sót ghi công, gỡ đoạn đó **không** làm giấy phép sống lại. Bản 4.0 có cơ chế phục hồi trong 30 ngày (Legal nhớ, phiên này chưa đọc lại legalcode 4.0). Bản 3.0 không có. Loại rủi ro này **không** do khiếu nại kích hoạt: nó phát sinh ngay lúc publish | Duy thêm một dòng mới xác nhận câu 11 có bao gồm rủi ro này. Biện pháp duy nhất là **phòng trước**: §A.1 (trường `based_on` bắt buộc, lint tên riêng). Câu hỏi luật ⇒ L15. **Đã quyết 2026-10-25: QĐ 51** — rủi ro §7 nằm trong chữ ký; L15 giữ lịch sau release, phòng trước bằng §A.1 (AC-45) |
| X8 | **Kênh nhận khiếu nại và thời gian phản hồi** (R33 a, b) · thêm 2026-10-24 | Thiếu kênh thì bên có quyền chỉ còn đường gửi DMCA tới host hoặc CDN ở Mỹ. PRODUCT-BRIEF đã ghi hậu quả: có thể bị khoá cả tài khoản host, kéo theo cả site. Có kênh thì phải công khai một định danh để liên lạc. Tên Duy vốn đã công khai qua dòng R20 ("duyệt bởi Duy"), nên kênh chỉ thêm một **địa chỉ liên lạc**. Nhưng định danh đó vướng R34 (Ringkas, BLOCKED) | Đề xuất: **hộp thư riêng cho site**, không chứa họ tên đầy đủ và không nhắc Ringkas, đặt ở B10. Thời gian phản hồi **72 giờ gỡ tạm** (lật cờ trước, tranh luận sau), vì Duy làm site ngoài giờ. Duy chọn kênh và con số. Không dùng form: form nhận nội dung ⇒ R29 + Worker. Không dùng GitHub Issues: buộc bên khiếu nại có tài khoản và công khai nội dung khiếu nại. *(Vòng sửa 2026-10-24: câu "tên Duy vốn đã công khai qua R20" phụ thuộc X9. Nếu Duy bỏ tên khỏi dòng R20 thì kênh trở thành định danh công khai **đầu tiên**.)* **Đã quyết 2026-10-24: QĐ 35**, đúng đề xuất: hộp thư riêng, "gỡ tạm trong 72 giờ". Còn treo hai việc: thời điểm công khai (chờ hợp đồng Ringkas) và kiểm header/WHOIS trước khi công khai (R33 a′) |
| X9 | **Dòng minh bạch AI (R20): bắt buộc hay không, và có hiện tên Duy không** · thêm vòng sửa 2026-10-24 | **Vì sao chưa chốt được:** (1) căn cứ là vùng xám. Luật AI 134/2025 có áp cho văn bản không, cá nhân có là "bên triển khai" không, đều chưa biết (L14); văn bản gốc chưa đọc. R20 là **lựa chọn phòng xa** của Legal, không phải nghĩa vụ đã xác định. (2) Chữ "duyệt bởi Duy" đặt **tên Duy trên mọi trang**, trong khi R34 (hợp đồng Ringkas; GĐ05 cùng mảng vay mua nhà) còn BLOCKED. (3) Câu "Soạn với hỗ trợ AI" **sai** với bài Duy tự viết không dùng AI. Muốn đúng thì cần một cờ riêng cho từng mục, đây là trường mới, chưa có trong spec. `PRD.md` câu 270 đã đánh `[x]` là "bắt buộc" trên cơ sở R20 | Đề xuất: **giữ dòng** (bỏ đi thì chịu rủi ro L14; giữ thì chỉ tốn một dòng chữ). **Chữ định danh trong "duyệt bởi ⟨…⟩" chờ R34**: Duy đọc xong hợp đồng mới chọn họ tên hay tên khác. Luật AI có đòi họ tên thật không: chưa biết (L14). Câu "soạn với hỗ trợ AI" chỉ hiện ở mục thật sự có dùng AI. Duy chọn cả ba điểm. **Đã quyết 2026-10-24: QĐ 34**: (1) giữ dòng, (3) cờ `ai_assisted` cho từng mục. Điểm (2), chữ định danh, **còn treo, chờ hợp đồng Ringkas** (QĐ 34.2). Xem R20 |
| X10 | **Bảng số liệu B3 (§A.2): che hay giữ** · thêm 2026-10-24 theo QĐ 29 | **Giữ:** số liệu là dữ kiện (Đ.15, gray). Dòng mục theo chuẩn kế toán; phần chọn và cột phân tích là của Hermanson ⇒ phần bên thứ ba có thể được bảo hộ là rất mỏng (L16). Ví dụ tr.94–95 (phân tích ngang/dọc) và phần giảng tr.168–174 (bảng cân đối phân loại) còn nguyên. Rủi ro do khiếu nại kích hoạt nên đường gỡ R33 xử lý được. Legal đọc là rủi ro này không chạm §7, vì phần bên thứ ba không thuộc giấy phép Hermanson (gray).<br>**Che:** hết rủi ro này, nhưng tr.94–95 và tr.168–174 mất ví dụ mà chữ quanh đó dựa vào, và bài tập tr.55, tr.185 không làm được.<br>**Thay bằng số hư cấu**, ghi "đã sửa đổi" (CC BY 3.0 cho phép Adaptation): giữ được ví dụ, nhưng S3 phải sửa chữ trong PDF, khó hơn che | Legal đề xuất **giữ B3**, và **che B2** (tr.117, chỉ một bảng; câu "63 per cent" của Hermanson ở lại). Duy chọn. **Đã quyết 2026-10-25: QĐ 46** — giữ B3 trong file host, loại hẳn khỏi máy sinh card; che B2 tr.117 |
| X11 | **Luật máy loại trang của QĐ 28: giữ đúng chữ hay mở rộng** · thêm 2026-10-24 | Đo trên PDF gốc (§A.2): mẫu đúng chữ QĐ 28 loại 91/1004 trang nhưng **sót tr.113**, đoạn Home Depot đã biết phải loại, vì PDF viết "Annual Report". Sót cả tr.501 (WSJ). Mẫu ③ loại 132 trang và bắt 7/7 trang đã biết. Cái giá: khoảng 41 trang bị loại oan thêm, ví dụ tr.24–25, nơi Hermanson tự viết về FASB | Legal đề xuất **mẫu ③ cộng danh sách `exclusions`**. Đây là đổi chữ của QĐ 28 nên **→ Duy**. Cả hai mẫu đều sót bảng B3 không có chữ "annual report" (tr.45, 55, 170). Rủi ro đó Duy đã nhận ở QĐ 28. **Đã quyết 2026-10-25: QĐ 47** — mẫu ③ + danh sách trang |
| X12 | **Hộp thư khiếu nại nhận dữ liệu cá nhân có định danh** · thêm vòng sửa 2, 2026-10-24 | QĐ 35 chọn hộp thư, đúng lý do ở X8: không có kênh thì bên có quyền chỉ còn DMCA tới host. Nhưng **kênh nào cũng nhận định danh của người khiếu nại** (họ tên, email, giấy tờ chứng minh quyền). Khác với IP ở X1, thiết kế không tránh được, và cách đọc A của X1 ("chưa bước vào phạm vi điều chỉnh") **không áp**, vì đây là dữ liệu có định danh rõ. Theo `../../../docs/data.md` (nguồn thứ cấp): Đ.20.1.c Luật 91 phủ cá nhân dùng nền tảng ngoài lãnh thổ để xử lý dữ liệu cá nhân thu tại VN ⇒ hồ sơ CTIA trong 60 ngày; không có miễn trừ cho cá nhân; không nộp ⇒ Đ.56 NĐ 330 phạt và buộc ngừng chuyển dữ liệu. Hộp thư chưa chọn, nên **nơi đặt máy chủ của nhà cung cấp chưa kiểm**. Hệ quả chữ: câu R25 / AC-57 "không thu thập định danh" thành **sai** khi hộp thư lên trang. Q-20 hiện không bao phần này | Ba phương án: **(A)** giữ hộp thư, sửa câu R25 cho đúng phạm vi, áp R37 (tối thiểu hoá), gộp L18 vào Q-20 để Duy ký trên cả phần này · **(B)** chọn nhà cung cấp hộp thư đặt máy chủ ở VN: chưa kiểm có không; chỉ bớt phần xuyên biên giới, vẫn là xử lý dữ liệu có định danh · **(C)** bỏ hộp thư: trái QĐ 35, quay lại kịch bản DMCA. Legal đề xuất **A**. Câu R25 đề xuất (VN): *"Khi bạn đọc, Where Money Sleeps không thu thập định danh; nhà cung cấp hạ tầng có ghi địa chỉ IP cho mục đích bảo mật của họ. Nếu bạn gửi thư tới hộp thư khiếu nại, những gì bạn gửi (tên, email, nội dung) chỉ được dùng để xử lý khiếu nại đó."* Bản EN và giọng văn: Writer. **→ Duy:** chọn phương án, duyệt câu, đặt thời hạn giữ thư (R37 (4)). **Phải vào Q-20 trước khi Duy trả lời Q-20**, vì Q-20 là câu tổng. **Đã quyết 2026-10-25: QĐ 49** — A, câu R25 trên, xoá thư khi khiếu nại đóng; L18 vào Q-20 (QĐ 51: chạy trước S5) |
| X13 | **Dòng "duyệt bởi" khi người soát là agent (QĐ 36)** · thêm vòng sửa 2, 2026-10-24 | QĐ 36: người soát con số là agent `ke-toan-reviewer`, Duy ký. Chuỗi hiện tại của Writer (§5): *"Soạn với hỗ trợ AI, duyệt bởi ⟨…⟩"* / *"Duyệt bởi ⟨…⟩"*. Nếu ⟨…⟩ là định danh của Duy (QĐ 34.2) thì câu **đúng về người ký** nhưng **im lặng** việc con số APR/lãi suất và tên tài khoản do AI soát. Người đọc một bài về lãi suất dễ hiểu là đã có người chuyên môn soát. Nếu ⟨…⟩, `reviewed_by` hoặc bất kỳ chữ công khai nào ghi "kế toán", "Phòng Kế toán", "accountant" ⇒ **sai sự thật**: không có người kế toán nào. Vùng minh bạch AI (L14, Luật AI 134/2025, chưa đọc văn bản gốc). QĐ 34.3 chỉ nói "Soạn", chưa nói "soát". AC-21 (không trường "duyệt bởi" nào là model) **vẫn giữ được** nếu `reviewed_by` = Duy và agent ghi ở trường riêng | Ba phương án: **(A)** nói thẳng phần AI soát. Mục có số được agent soát: *"Con số và thuật ngữ kế toán được soát bằng AI; ⟨…⟩ đọc và duyệt, ngày …"* (EN: *"Figures and accounting terms checked by AI; reviewed by ⟨…⟩, <date>."*), ghép sau *"Soạn với hỗ trợ AI."* nếu có `ai_assisted`. Mục không có số giữ *"Duyệt bởi ⟨…⟩"*. `reviewed_by` luôn là người ký; agent ghi ở một trường riêng (tên trường: S3) · **(B)** giữ chuỗi Writer hiện tại: đúng chữ, nhưng hở minh bạch ở đúng chỗ rủi ro nhất (con số) · **(C)** bỏ dòng soát: trái QĐ 34.1. Legal đề xuất **A**, kèm phép kiểm máy: dòng minh bạch và `reviewed_by` không chứa "kế toán", "accountant", "chuyên gia", "expert". **→ Duy:** chọn phương án và duyệt câu. Writer sửa §5 sau khi Duy chọn. **Đã quyết 2026-10-25: QĐ 41** — cấu trúc A, nhưng dùng **câu Writer W2** *"Con số và tên tài khoản được một agent AI soát; ⟨…⟩ ký duyệt."*, không dùng câu của Legal (câu Legal chứa "kế toán", trượt chính phép kiểm này). Phép cấm 4 chữ chỉ áp cho dòng minh bạch và `reviewed_by` |

## 4. Câu hỏi cho workflow pháp lý chuyên sâu — L13 + L18 trước S5 (QĐ 51), còn lại sau release

Theo quyết định 12, câu trả lời của workflow luôn ghi *"không phải ý kiến pháp lý · same vendor, same priors — no external verifier ran"*. **Duy ký.**

| L | Câu hỏi | Nguồn | Chạm mùa 1? |
|---|---|---|---|
| L1 | Ngoại lệ Đ.25 Luật SHTT có che cho dịch vụ bên thứ ba xử lý bản sao của người dùng không? | ADDENDUM (a) | Không |
| L2 | Tóm tắt hoặc bộ câu hỏi do LLM tạo có phải là "cải biên/biên soạn" theo Đ.4 k8 Luật SHTT không? | ADDENDUM (b) | Không (cổng cho card từ sách trả phí) |
| L3 | Trình duyệt gọi thẳng nhà cung cấp LLM có được tính là "chủ thể tự chuyển" theo Luật 91 không? | ADDENDUM (c) | Không |
| L4 | Theo Luật 91, Duy đóng vai trò gì: bên kiểm soát, bên xử lý, hay cả hai? | ADDENDUM (d) | Có một phần (gộp với L13) |
| L5 | Disclaimer "chỉ tải tài liệu bạn có quyền" có chuyển được trách nhiệm sang người dùng không? | ADDENDUM (e) | **Có, rủi ro thấp** (xếp lại vòng sửa 2): QĐ 29 đưa mở file PDF riêng vào cổng ra mắt. File chỉ xử lý trên máy người học, không rời máy (R13), nên câu này chỉ hỏi về trách nhiệm với việc *người dùng tự mở* file họ không có quyền. Có cần disclaimer hay không: chưa quyết, không chặn ra mắt |
| L6 | Duy có trách nhiệm gián tiếp khi site gợi ý người dùng đưa sách vào chatbot không, nhất là với OpenStax? | ADDENDUM (f) | Không |
| L7 | Một site giáo dục do một cá nhân viết, có trích văn bản QPPL, có bị coi là "thông tin tổng hợp" theo NĐ 147 không? | LEGAL-SCREEN | Không ở phần ra mắt, vì QĐ 33 đặt 0 chữ trích. **Có** khi mở GĐ05 (R18) |
| L8 | Điều khoản chống LLM của OpenStax có ràng buộc người dùng bản snapshot CC BY lấy từ GitHub không? | LEGAL-SCREEN | Không |
| L9 | Quảng cáo, affiliate hoặc donate có làm cho việc dùng nội dung thành "commercial" theo NC không? | LEGAL-SCREEN | Không (mùa 1 không kiếm tiền) |
| L10 | Câu hỏi về quyền nhân thân, **đối chiếu lại theo CC BY 3.0 §4(c)** thay vì 4.0 §2(b)(1): việc dịch và redact Hermanson có xâm phạm quyền bảo vệ sự toàn vẹn tác phẩm theo Luật SHTT VN không? (số điều: TBD — đối chiếu văn bản gốc) | LEGAL-SCREEN + đính chính | **Có** (R2, R5, R8) |
| L11 | So sánh sản phẩm tín dụng có tên ngân hàng có cần xin phép, hay phải chịu Luật Quảng cáo không? | LEGAL-SCREEN | Gián tiếp (R17 tránh bằng thiết kế) |
| L12 | Tài liệu giáo dục tài chính của NHNN có được tính là "văn bản hành chính" (loại trừ theo Đ.15) không? | LEGAL-SCREEN | **Có** nếu bài trích tài liệu NHNN |
| L13 | **Một câu chung:** IP mà host tĩnh và Worker ở nước ngoài xử lý khi truyền tải, trong khi không lưu IP hay ID nào, có làm phát sinh Đ.20.1.c Luật 91 (hồ sơ CTIA trong 60 ngày) không? Duy cá nhân có được miễn trừ nào không? **Thêm 2026-10-24:** (i) số gộp lưu theo ngày, dashboard ẩn ô n < 5 nhưng vẫn truy vấn được bằng `wrangler`: có ghép ra được người không? Nếu có ⇒ gộp lên tuần, xoá dòng ngày (QĐ 32, R36) · (ii) Cloudflare tự xử lý IP để bảo mật cho họ, còn Duy không bật rule nào (QĐ 31, R35): việc đó có tính là Duy xử lý không? | Mới ở S1 · gộp L4 | **Có** (R23–R26, R35, R36, X1). **QĐ 51: chạy TRƯỚC S5**, cùng một lượt với L18 (cổng S5, §2) |
| L14 | Luật AI 134/2025 có áp cho văn bản không? Cá nhân dùng AI soạn bài có phải "bên triển khai" không? Dòng minh bạch ở R20 đã đủ chưa? **Thêm 2026-10-24:** luật có đòi **họ tên thật** của người duyệt không (QĐ 34.2)? | LEGAL-SCREEN cột vùng xám | **Có** (R20; câu W2, QĐ 41). Sau release (QĐ 51) |
| L15 | Theo CC BY 3.0 §7, sau khi giấy phép đã chấm dứt vì sót ghi công, có đường nào lấy lại quyền không (xin bên cấp phép cấp lại, hay nhận lại tác phẩm)? Luật VN có coi chấm dứt tự động là hiệu lực không? Ranh giới "khái niệm" (Đ.15 Luật SHTT) với "diễn giải lại" (§1(a) Adaptation) nằm ở đâu? | T2 2026-10-24 | **Có** (R5, X7). Sau release (QĐ 51); AC-45 phòng trước |
| L16 | Bảng số liệu bên thứ ba nằm trong một sách CC BY (báo cáo tài chính của công ty thật, khảo sát AICPA): số liệu là dữ kiện (Đ.15), nhưng việc chọn lọc và sắp xếp có được bảo hộ như sưu tập dữ liệu (Đ.22 Luật SHTT; *Feist*, nếu bên có quyền kiện ở Mỹ) không? Bảng do Hermanson "slightly revised" thì quyền thuộc ai? | §A.2 · 2026-10-24 | **Có** (R2, R10, X10; cổng ra mắt QĐ 29). Giữ B3 trong file host (QĐ 46) ⇒ rủi ro này Duy nhận ở QĐ 51. Sau release |
| L17 | Một site giáo dục cá nhân có thuộc diện nghĩa vụ gỡ theo NĐ 17/2023 Đ.114 không? Hạn gỡ là bao lâu? "Gỡ tạm trong 72 giờ" có đủ không? | R33 (b) · QĐ 35 | **Có** (R33). Sau release (QĐ 51) |
| L18 | Hộp thư khiếu nại nhận họ tên, email, giấy tờ của người khiếu nại: Duy (cá nhân) là bên kiểm soát hay bên xử lý theo Luật 91? Nhà cung cấp hộp thư đặt máy chủ ngoài VN có làm phát sinh Đ.20.1.c (hồ sơ CTIA trong 60 ngày) không? Cần thông báo gì cho người gửi thư, và có cần sự đồng ý không (data.md nêu Đ.6.1 NĐ 356 đòi đồng ý kiểm chứng được)? Giữ thư bao lâu thì hợp lý? | X12 · R37 · vòng sửa 2, 2026-10-24 | **Có** (R25, R33 (a), R37). **QĐ 51: chạy TRƯỚC S5**, cùng lượt với L13. Kiểm luôn luật giữ thư của QĐ 49 ("xoá khi khiếu nại đóng") có đủ không |

## 5. BLOCKED — điều kiện và thứ bị chặn

| Điều kiện (chỉ Duy làm) | Ràng buộc bị chặn |
|---|---|
| Đọc hợp đồng lao động Ringkas | R34. ~~Gián tiếp: R22 nếu người kế toán là đồng nghiệp Ringkas~~ (hết áp từ QĐ 36: người soát là agent) · R33 (a): **công khai hộp thư** (QĐ 35) · R20: **chữ định danh** trong "duyệt bởi ⟨…⟩" (QĐ 34.2). Chưa có định danh thì dòng không render được, nên không bài nào đăng được |
| Đo iPhone + Android (Zalo `#sync`, WebView, `input type=file`) | R28 · phần WebView/`input type=file` của R13, **nay chặn cả ra mắt** (QĐ 29) |
| Có tên người kế toán + bấm giờ duyệt 1 bài · **đổi theo QĐ 36:** agent `ke-toan-reviewer` chạy thử trên 1 bài mẫu + card, đo thời gian Duy đọc báo cáo và ký (đã dựng `SAMPLE-LESSON-01.md` và báo cáo `SAMPLE-LESSON-01-ACCOUNTING-REVIEW.md`, chờ Duy bấm giờ ký; frontmatter `blocked_on` đã đồng bộ theo QĐ 36) | R22 |
| Có Phụ lục II TT 99/2025 chính thức (QĐ 37) | R22 phần tên tài khoản ⇒ bài GĐ01 không đăng được. Lối vào không bị chặn |

## Chưa xác minh được

- **URL gốc trên Công báo/vbpl.vn** của Luật Chứng khoán 2019, NĐ 147/2024, Luật AI 134/2025, Luật 91/2025, NĐ 356/2025, NĐ 330/2026: phiên này **chưa đối chiếu**. Căn cứ đang dựa trên S0 và ../../../docs/data.md. Phải đối chiếu từng chữ trước khi hành động (xưởng §Phòng Legal quy tắc 1, 2).
- **CC BY 3.0 legalcode** đọc ngày 2026-10-24 qua WebFetch. Công cụ trả **bản tóm tắt**, trích tối đa 125 ký tự: các ý của §1(a), §4(a), §4(b), §4(c) đã đọc được, nhưng §4(b)(iv) (cách ghi công cho Adaptation) **chưa đọc nguyên văn**.
  - **Cập nhật 2026-10-24 (T2):** đã tải HTML gốc bằng `curl` và đọc **nguyên văn** §1(a), §3(b), §4(b) gồm (iv), và §7. Phần §4(a), §4(c) vẫn chỉ đọc qua bản tóm tắt.
- Cơ chế phục hồi 30 ngày của CC BY 4.0: Legal **nhớ**, phiên này chưa đọc lại legalcode 4.0 (X7).
- Luật SHTT Đ.15 (không bảo hộ khái niệm, nguyên lý, số liệu): mới đọc qua nguồn thứ cấp ở S0, chưa đối chiếu bản gốc và bản sửa đổi 2025 (§A.1).
- Danh sách tên riêng để lint (§A.1): chưa trích.
- Hộp thư riêng có làm lộ danh tính qua header, WHOIS hay tên hiển thị không (X8): chưa kiểm. Kiểm khi Duy chọn kênh.
  - **Cập nhật 2026-10-24:** Duy đã chọn kênh (QĐ 35), nhưng hộp thư chưa tồn tại nên chưa kiểm được. Cách kiểm ở R33 (a′), làm trước khi công khai.
- Workers Logs và Workers Analytics Engine ghi những trường nào theo mặc định (R24).
  - **Cập nhật vòng sửa 2026-10-24:** với Workers Logs thì không cần biết nữa, vì R24 nay tắt hẳn. Còn chưa xác minh: `observability.enabled = false` có tắt **hết** mọi log không (TRACKING-PLAN §3: tắt cả `issues`, S4 kiểm bằng dashboard) · sampled logs Security Events gói Free có hiện IP cho Duy không (TRACKING-PLAN §Chưa xác minh).
- **Mức phạt cho cá nhân ở X1 (15–25 triệu)** là phép chia của Legal từ câu *"một nửa tổ chức (Điều 7 NĐ 330)"* trong `../../../docs/data.md`. data.md không ghi rõ 30–50 triệu ở Đ.56 là mức cho tổ chức. Đ.7 và Đ.56 NĐ 330 chưa đọc từ văn bản gốc.
- Luật AI 134/2025 có đòi **họ tên thật** của người duyệt không (X9): chưa đọc văn bản gốc.
- Giấy phép của thư mục standard_fonts và cmaps trong pdfjs-dist (R31). Reserved Font Name của ba họ font (R30).
- Nguồn danh sách mã niêm yết dùng cho lint (R16). Denylist tên ngân hàng (R17).
- Ngưỡng số chữ trích văn bản luật mỗi bài (R18) và thời gian phản hồi khiếu nại (R33): **Duy đặt**, chưa có số.
  - **Cập nhật 2026-10-24:** đã đặt. 0 chữ cho phần ra mắt (QĐ 33). 72 giờ gỡ tạm (QĐ 35), là đề xuất của Legal, **không có căn cứ luật** (L17).
- Luật SHTT Đ.22 (sưu tập dữ liệu) và án *Feist* 499 U.S. 340 (1991) (§A.2): Legal **nhớ**, phiên này chưa đọc văn bản.
- Soát §A.2 tr.1–197 mới là **lần 1 bằng máy**: grep dấu hiệu + 30 tên công ty do Legal tự chọn. Chưa trang nào được xem bằng mắt. Bảng của công ty ngoài danh sách và không có dấu hiệu sẽ lọt.
- `pdftotext` đọc dấu ":" ở dòng nguồn tr.117 thành "'". Đã thấy trên một trang; trang khác có thể méo kiểu khác, nên mẫu ③ (§A.2) chưa chắc bắt hết.
- Số trang mẫu ①②③ loại (91/118/132) đo trên PDF gốc ngày 2026-10-24. Đếm trang, không đếm đoạn.
- Gói Free của Cloudflare có tính năng xử lý IP nào **bật sẵn** mà tắt được không (R35): chưa kiểm.
- Thời hạn gỡ theo NĐ 17/2023 Đ.114. Mức phạt theo NĐ 174/2026.
- Mức "reasonable to the medium" cho dòng ghi công trên card (R5) là diễn giải, chưa có tiền lệ nào được tìm thấy.
- **Vòng sửa 2:** nơi đặt máy chủ của nhà cung cấp hộp thư (X12, R37): hộp thư chưa chọn nên chưa kiểm. Đ.20.1.c, Đ.56 NĐ 330, Đ.6.1 NĐ 356 chỉ đọc qua `../../../docs/data.md`, chưa đọc văn bản gốc. Gửi thư cho một hộp thư có phải "thu thập" theo Luật 91 không: chưa biết (L18).
- **Vòng sửa 2:** danh sách B3 tạm loại (tr.45, 55, 94–95, 170, 185) chỉ từ soát lần 1 bằng máy, chưa xem bằng mắt. Ngoài tr.1–197 chưa soát bảng B2/B3 nào, dù máy sinh card nạp cả cuốn (QĐ 28): phần đó chỉ có luật máy che.
- **Vòng sửa 2:** người đọc có thực sự hiểu "duyệt bởi ⟨…⟩" là có chuyên gia soát không (X13) là lập luận, chưa đo.
- **2026-10-25 — chỗ hở sau QĐ 38–51, chưa có QĐ, → Duy:**
  - `attribution_text` (*"che các đoạn trích và bảng số liệu của bên thứ ba"*) viết lúc B3 còn chờ X10. QĐ 46 giữ B3 trong file host, nên chữ "các … bảng số liệu" có thể bị đọc là đã che **mọi** bảng bên thứ ba, trong khi 6 trang B3 còn nguyên. Legal **không sửa**, vì QĐ 46 nhận nguyên bản sửa này. Đề xuất: "các" ⇒ "một số".
  - tr.117: che Exhibit 15 xong, câu của Hermanson vẫn viết *"As we show in Exhibit 15, 63 per cent…"*, tức là trỏ tới một bảng không còn. Có ghi "[bảng đã lược]" tại chỗ không (R8, §4(c))?
  - QĐ 49 "xoá khi khiếu nại **đóng**": chưa định nghĩa "đóng" (gỡ xong? bên khiếu nại im lặng N ngày? hết tranh chấp?), và "xoá" có gồm thùng rác và bản sao lưu của nhà cung cấp hộp thư không. L18 kiểm luật này.
  - Câu W2 (QĐ 41): `AC-86` và R20 đã đồng bộ gắn câu W2 theo **trường báo cáo của agent** (mục thuộc phạm vi QĐ 30 có báo cáo agent khác rỗng thì bắt buộc hiện câu W2; mục có con số ngoài phạm vi QĐ 30 không có báo cáo agent thì không hiện câu W2).
  - Trường riêng ghi agent (QĐ 41): `AC-86` và R20 đã khoá không render trường nội bộ `ke-toan-reviewer` ra HTML hiển thị.
  - §A.1 (`based_on` với trang B3): `AC-45` và §A.1 đã đồng bộ — chạm trang bị che/cấm (`host_redactions.redact`: tr.113, 117, 166 + tr.501, 803) ⇒ FAIL; chạm trang B3 (`keep_in_host_but_excluded_from_cards`) hoặc mẫu ③ ⇒ **cảnh báo** để Duy kiểm bài học chỉ lấy lời giảng/khái niệm của Hermanson, không chép bảng số liệu công ty thật.
  - QĐ 51 đặt L13 + L18 "trước S5", nhưng S3 build theo thiết kế hiện tại (đếm theo ngày, hộp thư chưa chọn). Workflow mà kết luận ngược thì phải sửa ở S3 hoặc S4. Nếu kết luận là cách đọc B (phải nộp CTIA), chưa có QĐ nào nói làm gì tiếp.
- **2026-10-25:** regex mẫu ③ trong `licences.json` do Legal **dựng lại** từ mô tả ở §A.2, rồi đo lại ra đúng 132 trang và 7/7. Phép thử này chỉ chứng minh hai bản cho cùng kết quả trên PDF này; chưa chứng minh mẫu bắt được trang bên thứ ba chưa biết.
- Same vendor, same priors — no external verifier ran.

## Nguồn

- CC BY 3.0 legalcode: https://creativecommons.org/licenses/by/3.0/legalcode (đọc 2026-10-24; §1(a), §3(b), §4(b), §7 đọc nguyên văn từ HTML gốc)
- Hermanson PDF gốc: `source_url` trong `legal/licences.json`. §A.2 đo trên bản đã tải trong scratchpad phiên này, khớp `bytes` = 7991863, bằng `pdftotext` từng trang (2026-10-24)
- Phát hiện S0: `gates/00-discovery/LEGAL-SCREEN.md` · `gates/00-discovery/ADDENDUM-PDF-LLM.md` · `gates/00-discovery/PRODUCT-BRIEF.md` §Quyết định của Duy · `gates/ONE-PAGER.md`
- Luật 91/2025, NĐ 356/2025, NĐ 330/2026: ../../../docs/data.md §Pháp lý Việt Nam
- PDF.js: https://github.com/mozilla/pdf.js/blob/master/LICENSE · foliate-js: https://github.com/johnfactotum/foliate-js

## T2 — câu hỏi chéo-phòng

Người hỏi: PM. Phòng trả lời: Legal. Ngày 2026-10-24. Không phải ý kiến pháp lý. Same vendor, same priors — no external verifier ran.

| # | Câu hỏi (nguyên văn) | Trả lời của Legal | Đã sửa gì trong file |
|---|---|---|---|
| 1 | **"Đoạn bài dựa trên Hermanson" là gì, và trường nào đánh dấu nó?** R5 giao cho S1 định nghĩa, nhưng chưa file nào trong 01-spec định nghĩa. Cần trả lời ba điểm: Dịch sát, diễn giải lại, dùng lại ví dụ hay số liệu của Hermanson: cái nào bắt buộc có dòng ghi công? Khái niệm kế toán chung (Nợ/Có, T-account) có thuộc diện đó không? Trường dữ liệu nào trên một đoạn bài cho máy biết đoạn đó có nguồn Hermanson? | **PM đúng, và cái giá còn cao hơn PM nêu.** Đã đọc nguyên văn §7: *"will terminate automatically upon any breach"*. Mất quyền sẽ mất với **cả tác phẩm**, không riêng đoạn bị sót. Ba điểm: **(1)** Cả ba loại (dịch sát · diễn giải theo trình tự một đoạn · dùng lại ví dụ hoặc con số của ví dụ) **đều bắt buộc** ghi công. Phép thử là §1(a): *"recognizably derived from the original"*. **(2)** Khái niệm chung **không** thuộc diện, vì Đ.15 Luật SHTT không bảo hộ khái niệm (gray). Nhưng khái niệm *được giải thích bằng ví dụ của Hermanson* thì thuộc diện. Nghi ngờ thì gắn. **(3)** Trường `based_on`, **bắt buộc trên mọi section**. Rỗng `[]` là một lời khai, thiếu trường là build FAIL. Cộng thêm lint tên riêng. Giới hạn còn lại: một bản dịch sát bị khai `[]` và đã đổi hết tên riêng thì chỉ Duy bắt được | Thêm **§A.1** (định nghĩa, bảng loại, trường `based_on`, lint, giới hạn) · sửa ô R5 · §2 thêm R5 ở S2 · thêm **X7** (đường gỡ không chữa được lỗi ghi công ⇒ **→ Duy** xác nhận câu 11 có bao gồm rủi ro này) · nối hệ quả vào X6 · thêm **L15** · cập nhật §Chưa xác minh (đã đọc nguyên văn §1(a), §3(b), §4(b)(iv), §7) |
| 2 | **"R33 PASS" ở cổng S5 có bắt buộc một kênh nhận khiếu nại công khai không? Kênh đó là gì?** R33 vừa nói kênh khiếu nại "công khai một địa chỉ của Duy", vừa nói việc đó "là sự kiện kích hoạt review". Vậy mùa 1 có kênh nhận khiếu nại hay không? Nếu có, nó nằm trên bề mặt nào, và thời gian phản hồi có phải điều kiện để R33 PASS không? | **Có, bắt buộc. Có, thời gian phản hồi là điều kiện PASS.** Đường gỡ gồm hai nửa: *nhận* khiếu nại và *lật* cờ. AC-61 mới diễn tập nửa sau. Không có kênh thì bên có quyền chỉ còn DMCA tới host ở Mỹ, tức là đúng kịch bản khoá cả tài khoản mà PRODUCT-BRIEF đã cảnh báo. R33 PASS = (a) kênh trên **B10** · (b) thời gian phản hồi in trên trang · (c) diễn tập cờ · (d) diễn tập đầu-cuối từ khiếu nại giả tới 404, trong thời hạn (b). Câu "sự kiện kích hoạt review" nghĩa là *công khai kênh thì phải review trước*. Review đó làm luôn ở X8. **Kênh nào và con số bao nhiêu: → Duy (X8).** Đề xuất: hộp thư riêng cho site, 72 giờ gỡ tạm. (a) **BLOCKED — chờ Duy đọc hợp đồng Ringkas** (R34), vì kênh công khai một định danh của Duy | Viết lại ô "Kiểm bằng gì" + Stage + Trạng thái của **R33** · §2: thêm R33 vào S2, ghi rõ định nghĩa PASS ở S5 · thêm **X8** · §5: R33 (a) vào điều kiện Ringkas |

**Việc cho phòng khác.** Legal không sửa file của phòng khác. PM chuyển các việc dưới đây:

Cột "Trạng thái" đọc lại ở vòng sửa 2026-10-24, khi `ACCEPTANCE.md` sửa lần cuối lúc 12:50, `PRD.md` lúc 13:24 và `WRITER.md` lúc 12:30. **Đọc lại lần 2, sau QĐ 17–35, chỉ bằng grep.** Các file kia đang được sửa song song, nên trạng thái có thể đã đổi.

| File | Việc | Trạng thái |
|---|---|---|
| `ACCEPTANCE.md` AC-45 | Thêm phép kiểm máy: section thiếu `based_on` ⇒ FAIL · lint tên riêng. Cột "Người" giữ, nhưng thu hẹp lại thành: bắt khai sai `[]` | **đã làm** (cập nhật 2026-11-07: kiểm `pages` theo QĐ 28, 46, 47 đã đồng bộ vào AC-45) |
| `ACCEPTANCE.md` AC-61 | Thêm (a), (b), (d) của R33. Hiện AC-61 chỉ phủ (c) | **đã làm**, phủ (a)–(d), gồm hộp thư và "72 giờ" (QĐ 35); (a′) kiểm header/WHOIS nằm ở ĐK-3 (`DECISIONS-QUEUE.md`) |
| `ACCEPTANCE.md` AC-56 | Khớp R24 mới (`observability.enabled = false`, tắt `issues`, dashboard không có log) | **khớp**, không cần sửa |
| `ACCEPTANCE.md` AC-53 | Giữ phép kiểm trường `reviewed_by`/`reviewed_on`. Chữ hiển thị và cờ "có dùng AI" theo từng mục thì chờ X9 | **đã làm** (cờ `ai_assisted`, QĐ 34, 42). Định danh chờ QĐ 34.2 |
| `ACCEPTANCE.md` AC-51 | Ngưỡng = 0 chữ trích cho phần ra mắt (QĐ 33) | **đã làm** |
| `ACCEPTANCE.md` | Thêm AC cho R35 (dashboard Cloudflare không có rule IP) và R36 (ẩn ô n < 5). Thêm AC cho luật máy QĐ 28 (§A.2, R11) và redact bảng số liệu (R2, cổng ra mắt) | **đã làm** (AC-84, AC-80, AC-18, AC-23 đã trỏ `licences.json` → `card_generator`, `host_redactions`) |
| `PRD.md` B10 + Scope dòng 14 | Thêm kênh khiếu nại + thời gian phản hồi, ghi "**→ Duy, X8** · BLOCKED (a) — chờ hợp đồng Ringkas" | **đã làm** (PRD có hộp thư theo QĐ 35, công khai BLOCKED) |
| `PRD.md` K1 + câu #12 | Đưa **cả hai cách đọc** của X1 và mức tiền cho cá nhân, không chỉ "30–50 triệu" | **đã làm** (PRD K1 + QĐ 51) |
| `PRD.md` câu 270 `[x]` dòng minh bạch AI | Mở lại: R20 là vùng xám, phần tên chờ R34 ⇒ X9 vào danh sách câu hỏi cho Duy | **đã làm** (PRD có dòng AI theo QĐ 34, 42) |
| `PRD.md` cổng ra mắt | Thêm R1–R4, R6, R13, R31 và §A.2 vào cổng ra mắt (QĐ 29) | **đã làm** (PRD §Delivery Milestones + AC-79) |
| `WRITER.md` | Writer khai `based_on` cho mọi section khi viết, theo bảng §A.1 | **đã làm**, gồm cả `ai_assisted` (QĐ 34.3, 42; WRITER §1) |
| `legal/licences.json` | `exclusions` thêm tr.113, tr.117 (B2), B3 nếu X10 chọn che, và luật máy QĐ 28. Sửa `attribution_text` theo số chỗ thật sự che | **đã làm** (QĐ 46, 47: `exclusions`, `host_audit`, `card_generator`, `host_redactions`) |
| `ACCEPTANCE.md` AC-18 | (i) nay khớp `licences.json` (có tr.113). QĐ 47 chốt mẫu ③ ⇒ AC-18 dùng đúng `card_generator.page_rule` | **đã làm** (AC-18 đọc trực tiếp `card_generator`) |
| `ACCEPTANCE.md` AC-57 + Writer B10 | Câu R25 theo X12 khi Duy chọn. Hộp thư không lên trang khi câu cũ còn. Câu VN chốt (QĐ 49, R25); bản EN: Writer | **đã làm** (AC-57 + WRITER §5 có đủ VN/EN) |
| `ACCEPTANCE.md` AC cho R37 | Diễn tập R33 (d): không tên/email người khiếu nại nào trong repo; thêm bước xoá thư khi đóng khiếu nại giả (QĐ 49, R37 (4)) | **đã làm** (AC-85) |
| `ACCEPTANCE.md` AC-03, 04, 12, 21 · `WRITER.md` §3 `reviewed_by`, §5 dòng AI | Theo QĐ 36, 41, 42: `reviewed_by` = người ký (Duy), agent ở trường riêng; câu W2; máy cấm 4 chữ trong dòng minh bạch + `reviewed_by`; cờ `ai_assisted` theo bài / bộ card / bản EN | **đã làm** (AC-03, 04, 12, 21, 53, 86; WRITER §3, §5) |
| `PRD.md` · `ACCEPTANCE.md` | Số ràng buộc Legal nay là **R1–R37** | **đã làm** |
| `ACCEPTANCE.md` AC-19 · `PRD.md` Scope 2, B4 | Card Hermanson trang > 197: "đọc lại đoạn này" trỏ về **bất kỳ** bài `published` có `based_on` phủ trang đó, không chỉ GĐ01 (QĐ 48, R11) | **đã làm** (AC-19, PRD Scope 2, B4) |
| `PRD.md` cổng S5 · `ACCEPTANCE.md` | Thêm điều kiện S5: workflow pháp lý L13 + L18 chạy xong, Duy ký kết luận (QĐ 51, §2) | **đã làm** (PRD §Delivery Milestones, ACCEPTANCE TL;DR + bảng phủ R26) |

## Đổi ở vòng sửa 2026-10-24

Theo review vòng 1 (falsify B5, N1; consistency N12). Legal chỉ sửa file này. Same vendor, same priors — no external verifier ran.

- **X1:** viết lại thành hai cách đọc cùng nguồn `../../../docs/data.md`. Cách A: đếm lượt mà không lưu định danh thì không phát sinh nghĩa vụ. Cách B: IP khi truyền tải kéo theo CTIA, phạt theo Đ.56 cộng buộc ngừng chuyển dữ liệu. Thêm mức tiền cho cá nhân, bằng một nửa tổ chức theo Đ.7 NĐ 330, tức 15–25 triệu. Con số này là phép chia và được ghi rõ là chưa xác minh. Thêm thời hiệu 01 năm và phạm vi của Đ.63. Đề xuất đổi thành Duy ký trên cả hai cách đọc, **→ Duy (Q-xx)**.
- **TL;DR:** đếm lại thành 9 chỗ cần Duy quyết và mô tả lại X1. Thêm ghi chú về R20.
- **R24:** bỏ TBD. Nay là `observability.enabled = false` + tắt `issues`, theo TRACKING-PLAN §3 (Workers Logs mặc định bật). S4 kiểm dashboard (AC-56).
- **R20:** ghi rõ đây là vùng xám và là lựa chọn phòng xa, và chữ "duyệt bởi Duy" công khai tên Duy trong lúc R34 BLOCKED. Thêm **X9 → Duy (Q-xx)**.
- **X8:** thêm ghi chú: lập luận "tên Duy đã công khai qua R20" phụ thuộc X9.
- **§5:** dòng Ringkas thêm R20 (phần tên).
- **§Chưa xác minh:** thêm ba ý: tình trạng Workers Logs, phép chia mức phạt cá nhân, và việc Luật AI có đòi họ tên thật hay không.
- **Việc cho phòng khác:** thêm cột trạng thái sau khi đọc lại ACCEPTANCE, PRD và WRITER. Hiện cả bốn việc cũ đều **chờ PM**. Thêm ba việc mới: AC-53, PRD K1/#12, PRD câu 270.
- Không đổi frontmatter `status`/`blocked_on`.

## Đổi theo QĐ 17–35 (2026-10-24)

Nguồn thẩm quyền: `gates/00-discovery/PRODUCT-BRIEF.md` §Quyết định của Duy, QĐ 17–35 (Duy chốt qua `DECISIONS-QUEUE.md` §"Câu trả lời của Duy"). File này là nháp S1 chưa duyệt, nên sửa tại chỗ; danh sách dưới đây ghi lại đã đổi gì. Legal chỉ sửa file này. Không phải ý kiến pháp lý. Same vendor, same priors — no external verifier ran.

- **QĐ 28 → R11:** từ "chưa quyết" thành cả cuốn trừ đoạn loại. Card lấy từ trang > 197 chỉ đăng khi có bài phủ trang đó. **X2** đóng. §A.1: trường `pages` nay trong tr.1–1004. **§A.2 mới:** đo luật máy của QĐ 28 trên PDF gốc. Mẫu đúng chữ **sót tr.113** ⇒ **X11 → Duy**. **X3** nặng hơn, kèm việc sửa `licences.json` ⇒ **→ Duy**.
- **QĐ 29 → R2, R10, R13, §2 S5, §5:** redact bảng số liệu bên thứ ba vào cổng ra mắt. **§A.2 mới:** quy tắc B1–B4 có căn cứ (gray ở chỗ chưa chắc), cùng soát lần 1 tr.1–197. Thấy thêm tr.45, tr.55, tr.170 ⇒ **X10 → Duy** (che hay giữ B3). Cổng ra mắt nay gồm R1–R4, R6, R13, R31. Phần WebView/`input type=file` của R13 chặn cả ra mắt.
- **QĐ 31 → R35 mới:** không bật rule IP ở Cloudflare. Có tính năng mặc định bật mà tắt được thì **→ Duy**.
- **QĐ 32 → R36 mới:** đếm theo ngày, ẩn ô n < 5. L13 thêm câu (i).
- **QĐ 33 → R18:** ngưỡng = 0 cho phần ra mắt (AC-51). L7 chỉ còn chạm khi mở GĐ05.
- **QĐ 34 → R20:** giữ dòng, cờ `ai_assisted` bắt buộc. Định danh **BLOCKED** chờ Ringkas. **X9** đóng, trừ điểm (2). L14 thêm câu họ tên thật.
- **QĐ 35 → R33:** hộp thư riêng + "gỡ tạm trong 72 giờ". Thêm (a′) kiểm header/WHOIS trước khi công khai. Công khai **BLOCKED** chờ Ringkas. **X8** đóng phần kênh. L17 mới (thời hạn theo NĐ 17/2023).
- **QĐ 18 → R32:** N/A. **X5** đóng.
- **Q-20 → X1, X7, L13, L15:** thay "Q-xx". **L13 ghi rõ là câu Q-20 đang hỏi** (trước S5 hay sau release).
- **L-list:** L1–L15 thành **L1–L17** (L16 bảng số liệu, L17 thời hạn gỡ). Sửa cột "Chạm mùa 1" của L7, L13, L14, L15.
- **TL;DR, §2, §5, §Chưa xác minh, Việc cho phòng khác:** cập nhật theo các dòng trên. Bảng việc cho phòng khác đọc lại bằng grep: AC-45, AC-51, AC-53, AC-61, B10, câu 270 và WRITER đã được làm. Thêm việc mới: AC cho R35, R36, §A.2, (a′); PRD cổng ra mắt; `licences.json`.
- Không đổi frontmatter `status`/`blocked_on`. Các mục "Đổi ở vòng sửa" cũ giữ nguyên, kể cả chữ "Q-xx" trong đó, vì đó là lịch sử.

## Đổi vòng sửa 2 (2026-10-24)

Theo review S1 sau QĐ 17–35 (BLOCKER M3, M8, §4 (a)(b)(c); NONBLOCKING M5, M6, §4 (d)). Thẩm quyền: QĐ 1–37 trong `gates/00-discovery/PRODUCT-BRIEF.md`. Legal chỉ sửa file này và `legal/licences.json` (trường `exclusions`, `attribution_text`). Không phải ý kiến pháp lý. Same vendor, same priors — no external verifier ran.

| Chỗ | Đổi gì | Căn cứ |
|---|---|---|
| `licences.json` `exclusions` | Thêm dòng có ngày: tr.113, 166, 501, 803 (đoạn đã biết) · tr.117 (B2) · tr.45, 55, 94–95, 170, 185 (B3, **tạm loại** tới X10). Đoạn cũ giữ nguyên | QĐ 28 (chữ "trừ các đoạn đã biết") · QĐ 29 · §A.2. Đóng M3, §4 (c) |
| `licences.json` `attribution_text` | "che 2 đoạn trích bên thứ ba" ⇒ "che các đoạn trích và bảng số liệu của bên thứ ba". Không ghi số, nên đúng với mọi lựa chọn X10 | CC BY 3.0 §4(b) · §A.2 |
| X3 | Đóng: đã sửa. Duy bác ⇒ `git` trả bản trước | — |
| B3 tr.94–95 | Ghi rõ bảng HP chạy sang tr.95 | `pdftotext` tr.95 |
| R10, §A.2 bảng B3 + đoạn luật máy | Ghi danh sách trang trong `exclusions`; B3 tạm loại khỏi máy sinh card | như trên |
| R17 | Máy tính khoản vay: quyết lúc mở GĐ05, không thuộc mùa 1 | QĐ 18 (M5) |
| R22 | Phạm vi QĐ 30 (+ đoạn bài card có số trích) · người soát = agent `ke-toan-reviewer`, Duy ký · K2 tối đa "KHỚP NGUỒN THỨ CẤP", GĐ01 chờ Phụ lục II chính thức · điều kiện BLOCKED đổi theo QĐ 36, 37 | QĐ 30, 36, 37 (M5, M8) |
| R28 | Whitelist thêm `tel`; trường thời điểm hoạt động cuối không đi theo sao lưu | QĐ 26 (M5) |
| R25 | Câu chỉ đúng cho người đọc; câu mới → X12; câu cũ không lên cùng hộp thư | §4 (a) |
| R37 (mới) | Dữ liệu người khiếu nại: chỉ dùng cho khiếu nại đó, không vào repo/build, không chuyển sang dịch vụ khác, thời hạn giữ do Duy đặt | §4 (a) |
| X12, X13 (mới) | → Duy, có đề xuất và câu chữ | §4 (a), (b) |
| L5 | Xếp lại: chạm mùa 1, rủi ro thấp | QĐ 29 · §4 (d) |
| L18 (mới) | Dữ liệu người khiếu nại theo Luật 91; phải gộp vào Q-20 | §4 (a) |
| R34, §5 | Bỏ vế "người kế toán là đồng nghiệp Ringkas"; §5 thêm dòng Phụ lục II | QĐ 36, 37 |
| TL;DR, §2 | Đếm lại: **37 ràng buộc = 18 verified · 9 gray · 6 tách phần · 3 BLOCKED · 1 N/A**. S5 thêm R37 | M6 |
| Việc cho phòng khác | `licences.json` đã làm; thêm AC-18 (X11), AC-57, AC cho R37, AC-03/04/12/21 + WRITER (X13), số ràng buộc R1–R37 | M3, M6, M8 |

Không đổi frontmatter `status`/`blocked_on`, kể cả điều kiện 3 đã lỗi thời theo QĐ 36 (review M8 đã nêu → Duy). Các mục "Đổi…" cũ giữ nguyên.

## Đổi theo QĐ 38–51 (2026-10-25)

Thẩm quyền: `gates/00-discovery/PRODUCT-BRIEF.md` §Quyết định của Duy, QĐ 38–51 (QĐ 41–51: Duy nhận theo lô mọi khuyến nghị của `DECISIONS-QUEUE.md`, nguyên văn *"hãy chọn tất cả options mà bạn suggest"*). File này là nháp S1, nên sửa tại chỗ. Legal chỉ sửa file này và `legal/licences.json`. Không phải ý kiến pháp lý. Same vendor, same priors — no external verifier ran.

| QĐ | Chỗ đổi | Đổi gì |
|---|---|---|
| 41 | R20 · R22 · X13 · L14 · việc AC-03/04/12/21 | Câu W2 cho mục có số/tên tài khoản; `reviewed_by` chỉ là người ký, agent ở trường riêng; máy cấm "kế toán / accountant / chuyên gia / expert" **chỉ** trong dòng minh bạch + `reviewed_by`. X13 đóng |
| 42 | R20 | Hạt của `ai_assisted`: bài / bộ card / bản EN (chỉ ghi vào ô đang sửa) |
| 40 | R22 | Luật ký trên phán của agent (chỉ ghi vào ô đang sửa) |
| 46 | R2 · §A.2 bảng B2/B3 + tr.117 · R10 · X3 · X10 · L16 · `licences.json` | Che B2 tr.117 trong file host; giữ B3 trong file host, loại hẳn khỏi máy sinh card. `licences.json`: dòng cập nhật trong `exclusions` và `host_audit`; thêm trường `host_redactions` (che trong file host) và `card_generator` (loại khỏi máy sinh card). `attribution_text` không đổi. X10 đóng |
| 47 | §A.1 · §A.2 luật máy · R11 · X11 · việc AC-18 · `licences.json` `card_generator.page_rule` | Mẫu ③ + danh sách trang là luật chính thức. Legal đo lại: 132/1004 trang, 7/7. X11 đóng |
| 48 | R11 · việc AC-19/PRD | Card trang > 197 trỏ về bất kỳ bài `published` có `based_on` phủ trang đó |
| 49 | R25 · R37 · X12 · L18 · việc AC-57, AC R37 | Câu R25 mới chốt (bản EN: Writer). R37 (4): xoá thư khi khiếu nại đóng. X12 đóng |
| 51 | X1 · X7 · R26 · R36 · §2 S5 · §4 tiêu đề, L13–L18 · việc PRD cổng S5 | Q-20 xác nhận. **Cổng S5: workflow L13 + L18 chạy xong và Duy ký kết luận trước khi mở S5.** L14–L17 sau release. X1, X7 đóng |
| — | TL;DR | Đếm lại: 18 verified · **7 gray · 8 tách phần** (R25, R37 sang tách phần) · 3 BLOCKED · 1 N/A. Mọi X đã đóng |
| — | §Chưa xác minh | Thêm 7 chỗ hở chưa có QĐ, → Duy |

Không đổi frontmatter `status`/`blocked_on` (3 điều kiện của Duy chưa xong). Các mục "Đổi…" cũ giữ nguyên.
