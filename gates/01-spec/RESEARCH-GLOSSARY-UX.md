---
tier: reference
status: reference
date: 2026-10-24
stage: 01-spec
owner: PM (tổng hợp research)
answers: PRD.md §B5 "cách hiện chú thích là câu Design #2" — Duy đã chốt QĐ 16 (chạm mới hiện), QĐ 17 (mở tại chỗ), QĐ 19 (lần đầu mỗi mục H2), QĐ 20 + QĐ 44 (nhãn thẻ theo keep_en)
review: same vendor, same priors — no external verifier ran
---

# Chú thích thuật ngữ khi chạm: dạng nào tốt hơn cho người đọc

> Tham chiếu. Tổng hợp 4 mũi research (patterns · affordance · a11y-tech · learning), mỗi mũi có 2 lens
> phản bác (evidence · user). Không lens nào bác bỏ mũi nào (`refuted=false` cả 8). Các correction đã được áp vào file này.

## TL;DR

1. **Khuyến nghị: chạm vào thuật ngữ thì một thẻ chú thích MỞ RA TẠI CHỖ, ngay sau câu chứa thuật ngữ, đẩy phần chữ bên dưới xuống. Không dùng bong bóng phủ lên chữ, không dùng sheet ở đáy.**
2. Lý do: không che chữ. Câu đang đọc vẫn nằm trên thẻ. Không phụ thuộc Popover API hay CSS anchor (iOS < 18.3 và < 26 thiếu). Không có lớp phủ nào để nút Back của Zalo đóng nhầm cả bài. A11y dùng pattern disclosure, pattern này APG đã có đồng thuận.
3. Đánh dấu: gạch chân chấm, giữ màu chữ thân bài, chỉ ở **lần đầu mỗi mục (H2)**. Các lần sau là chữ thường.
4. Thẻ chứa nhãn song ngữ theo QĐ 20 & QĐ 44 (`Debit · bên Nợ` cho mục `keep_en: true`; `sổ cái · ledger` cho mục `keep_en: false`), một câu định nghĩa ≤ 25 từ (WRITER §2), và một câu ví dụ về tiền của chính người đọc. Không link rời trang.
5. **Cảnh báo:** 2 trên 4 mũi nghiêng về dạng phủ: thẻ bám dòng, hoặc ngăn đáy. Không có nghiên cứu nào so sánh trực tiếp các dạng này. Nên chọn bằng buổi thử 5 người, với 2 ứng viên, không chọn bằng lập luận.

---

## 1. So sánh các dạng chạm-mới-hiện

| Dạng | Che chữ? | Mất chỗ đọc? | A11y | iOS Safari · Android · Zalo WebView | Ví dụ thật | Nguồn |
|---|---|---|---|---|---|---|
| **(c) Mở tại chỗ sau câu** ⭐ | **Không** | **Thấp**: chữ phía dưới bị đẩy xuống, câu đang đọc giữ nguyên. Rủi ro: chữ nhảy khi đóng một thẻ nằm *phía trên* | APG disclosure: `<button aria-expanded>`. Không dùng `<details>` giữa câu vì không hợp lệ trong `<p>` | Chỉ cần HTML/CSS/JS cơ bản, không API mới. *Chưa đo trên Zalo* | Tufte CSS: trên màn hẹp, ghi chú lề ẩn cho tới khi người đọc bật lên | S6 · S11 · S20 · S26 |
| (a1) Bong bóng neo cạnh chữ | **Có**, che các dòng lân cận | Trung bình: phải đóng rồi tìm lại dòng | Popover API + `popovertarget` có sẵn `aria-expanded` ngầm | CSS anchor chỉ có từ Safari 26, và mới một phần. Chạm ra ngoài để đóng chỉ có từ iOS 18.3. Máy cũ cần JS định vị | Wikipedia Reference Previews, nhưng chỉ có trên desktop, mở bằng hover | S1 · S3 · S13 · S14 · S15 |
| (a2) Thẻ bám dòng: rộng hết màn, đặt ngay dưới dòng, phủ lên chữ | **Có**, che chữ phía dưới | Thấp: dòng chứa thuật ngữ vẫn thấy | Như (a1) | Định vị bằng JS tự host (không qua CDN, vì sản phẩm hứa không có script bên thứ ba) | *Chưa tìm thấy ví dụ đã kiểm* | lens user của mũi a11y |
| (b) Bottom sheet dạng modal | Che ⅓ đáy màn hình và **chặn cả trang** | Cao: mắt nhảy xuống đáy, vuốt đóng dễ lẫn với cuộn | Có scrim, cần quản lý focus | Rủi ro Back Android trong Zalo đóng cả bài (*chưa đo*) | HIG khuyên dùng sheet thay popover trên màn hẹp, nhưng đó là guideline cho app native | S2 · S4 · S5 |
| (e) Ngăn đáy non-modal | Che ⅓ đáy, đúng vùng ngón cái vừa chạm | Trung bình: mắt nhảy xuống, phải cuộn bù cho dòng nằm trên mép ngăn | Popover `auto` | Popover không tự đóng khi cuộn, nên ngăn nằm lì trên chữ | Wikipedia mobile: drawer cho chú thích nguồn. *Chưa kiểm trên trang live, không có số đo công bố* | S5 · S8 · S9 |
| (d) Footnote nhảy xuống cuối trang | Không | **Rất cao** | Link neo | Chạy được mọi nơi | WMDE ghi nhận người đọc không biết cách quay lại chỗ đang đọc | S7. **LOẠI** |

**Vì sao chọn (c) thay vì (a2) hay (e), dù hai dạng kia có người bênh:**

| Câu hỏi | (c) tại chỗ | (a2) thẻ bám dòng | (e) ngăn đáy |
|---|---|---|---|
| Câu đang đọc còn thấy khi thẻ mở (contiguity)? | Có | Có | Phải cuộn bù |
| Có lớp phủ cần đóng không (Back Zalo, light dismiss iOS < 18.3)? | **Không** | Có | Có |
| Cần định vị theo trình duyệt? | Không | JS tự host | Không |
| Nhược điểm thật | Chữ bên dưới bị đẩy, đoạn văn bị cắt | Che chữ bên dưới, thêm một dependency | Mắt rời chữ, che đúng vùng vừa chạm |

**Bất đồng còn treo (quy tắc 12): đây không phải tỉ số 2–2.** Câu spec chưa ai trả lời là:
*"Người đọc của mình khó chịu hơn khi chữ bị **đẩy xuống** hay khi chữ bị **che**?"*
Không nguồn nào đo câu này. Buổi thử 5 người ở §6 là chỗ trả lời.

---

## 2. Đánh dấu lần đầu hay mọi lần

**Khuyến nghị: gạch chấm và chạm được ở lần đầu trong MỖI MỤC (H2). Các lần sau trong cùng mục là chữ thường, không chạm được.**

| Phương án | Được | Mất | Bằng chứng |
|---|---|---|---|
| Lần đầu mỗi **bài** (WRITER §2 phương án A) | Trang sạch nhất | Ai quên nghĩa ở đoạn 12 thì không còn chỗ chạm | — |
| **Lần đầu mỗi mục H2** ⭐ | Mỗi mục có một chỗ tra lại. Không cần lưu trữ gì | Một bài có thể có 3–4 gạch chấm cho cùng một từ | Wikipedia MOS (S16), là quy ước biên tập, không phải thực nghiệm |
| Mọi lần | Chỗ nào cũng tra được | "Nợ" xuất hiện hàng chục lần ⇒ trang toàn gạch chân, đi ngược cảm giác "không thấy mình đang học" | Chữ được đánh dấu bị nhìn lâu hơn và bị coi là quan trọng (S17). Tác giả nói hiệu ứng này không hại mạnh tới việc đọc ⇒ mức tin **low** |
| Hai mức (gạch rõ ở lần đầu, gạch rất nhạt ở các lần sau) | Tra được mọi nơi | Lúc 10h tối, độ sáng thấp hoặc dark mode, gạch "rất nhạt" coi như không có | lens user của mũi affordance. **Bỏ** |

> **Cập nhật theo QĐ 19, 20, 44 (2026-10-25):** Xung đột cũ với `WRITER.md` §3 đã đóng — đơn vị đánh dấu lần đầu chốt theo **mỗi mục H2** (QĐ 19), thuật ngữ chuyên ngành viết tiếng Anh trong dòng (`Debit`, không viết `Nợ (Debit)`, QĐ 20), ngoại lệ `sổ cái` viết tiếng Việt trong dòng (QĐ 44).

**Tín hiệu:**
- Gạch chân **chấm**, cùng màu chữ, lệch xuống khoảng 3px.
- Không dùng xanh link, không dùng gạch liền. NN/g dành hai tín hiệu này cho link thật (S18).
- Không dùng icon ⓘ, không tô nền.
- Gạch chấm là quy ước quen thuộc cho "chữ này có định nghĩa" (S19). Nó cũng đáp ứng WCAG SC 1.4.1, không truyền thông tin chỉ bằng màu.

---

## 3. Chú thích chứa gì

```
┌──────────────────────────────────────────┐
│ Debit · bên Nợ (hoặc: sổ cái · ledger) ✕ │  nhãn song ngữ theo keep_en (QĐ 20, 44)
│ <một câu định nghĩa, ngôn ngữ đang đọc>  │  ≤ 25 từ VN / ≤ 20 từ EN — WRITER §2, đã có
│ Ví dụ: <một câu về tiền của chính bạn>   │  chưa có ngân sách — xem dưới
└──────────────────────────────────────────┘
```

| Quy tắc | Cơ sở |
|---|---|
| Định nghĩa viết bằng **ngôn ngữ đang đọc**. EN chỉ là nhãn đi kèm | Meta-analysis 42 nghiên cứu: chú thích L1 cho kết quả tốt hơn L2 (S21). Nghiên cứu đo người học ngoại ngữ |
| Thẻ **tự đủ nghĩa**. Glossary chỉ là nguồn dữ liệu, không phải nơi người đọc phải đến | Cùng meta-analysis: glossary tách rời là dạng kém nhất (S21) |
| **Không** có link "Xem thêm" rời trang ở mùa 1 | Trong WebView Zalo, quay lại có thể mất vị trí cuộn (*chưa đo*) |
| Đơn vị ngân sách: **token tách bằng dấu cách**, giống cách `vibe-check` đếm | Tiếng Việt: "tài khoản" = 2 token |
| Ví dụ ≤ 1 câu. **Con số chưa chốt**: viết thử 5 thuật ngữ thật rồi mới đặt | Không có nguồn cho con số. NN/g chỉ nói "giữ ngắn" (S1) |
| Cần hơn 2 câu ⇒ viết vào thân bài, đừng kéo dài thẻ | NN/g: nội dung dài thì không còn là "tip" (S1) |
| **Không** nút "đã hiểu", **không** trắc nghiệm trong thẻ | Người đã biết thì không chạm. Truy xuất thuộc về quiz card (S22, S23) |

---

## 4. Hành vi chi tiết của phương án khuyến nghị (c)

| Tình huống | Hành vi |
|---|---|
| **Markup** | Thuật ngữ là `<button type="button" aria-expanded="false" aria-controls="g-…">` nằm trong `<p>`. Thẻ là `<span id="g-…" hidden>` hiển thị dạng khối, chèn **sau dấu chấm của câu** (`<span>` hợp lệ trong `<p>`, `<details>` thì không, S20). Nếu không tách câu chắc chắn được thì chèn sau đoạn: kém hơn, nhưng là đường lui |
| **Chạm để mở** | Đổi trạng thái ngay khi chạm (`:active`). Thẻ mở ra bằng animation chiều cao ≤ 200ms; `prefers-reduced-motion` thì không animation. Thuật ngữ có nền nhạt khi thẻ đang mở. `aria-expanded="true"` |
| **Đóng** | Chạm lại vào thuật ngữ, hoặc nút ✕ trong thẻ (✕ không nằm trong câu ⇒ phải đạt ≥ 24×24px, S12) |
| **Chạm ra ngoài** | **Không đóng.** Thẻ tại chỗ không che gì. Đóng nhầm khi đang cuộn sẽ làm chữ nhảy |
| **Vuốt** | Không có cử chỉ vuốt-để-đóng, để tránh lẫn với cuộn (S4) |
| **Back Android / vuốt mép iOS** | Không thêm history entry. Back hoạt động như trên một trang thường |
| **Chạm thuật ngữ khác** | Mở thẻ đó. **Không tự đóng thẻ đang mở.** Đóng một thẻ nằm phía trên sẽ kéo cả trang lên, và iOS ≤ 26.6 không có `overflow-anchor` để bù (S25, *chưa kiểm lại*). Hai thuật ngữ cùng câu ⇒ hai thẻ xếp theo thứ tự xuất hiện |
| **Bàn phím** | Tab tới thuật ngữ, Enter/Space để mở hoặc đóng (APG disclosure, S11). Esc trên thuật ngữ hoặc trong thẻ ⇒ đóng, focus về thuật ngữ. Focus **không** tự nhảy vào thẻ |
| **VoiceOver** | Mong đợi: đọc tên thuật ngữ + "nút" + trạng thái thu gọn/mở rộng. Sau khi mở, vuốt phải đọc tiếp phần còn lại của câu rồi tới thẻ. *Câu chữ cụ thể bằng giọng VI, và việc nút giữa câu có làm ngắt nhịp đọc không: CHƯA KIỂM* |
| **Không có `role=tooltip`** | Pattern tooltip của APG chưa có đồng thuận, và tooltip không nhận focus (S10) |
| **Glossary chưa có mục** | Build **fail** (AC-11 · AC-13 trong `gates/01-spec/ACCEPTANCE.md`). Phòng thủ lúc runtime: render chữ thường, không gạch, không nút. **Không bao giờ có thẻ rỗng** |
| **JS lỗi** | Thuật ngữ thành chữ thường. Bài vẫn phải đọc hiểu được khi không mở thẻ nào (S1) |
| **Chế độ EN** | Cùng component. Nhãn theo bảng hiển thị trang EN của WRITER §3 (X1 đã đóng bởi QĐ 20, 43) |
| **Gõ chữ / biên tập** | `line-height` ≥ 1.6. **Không** dùng padding để nới vùng chạm, vì nó chồng lên dòng trên và dòng dưới. Quy tắc cho người viết: không để hai thuật ngữ chạm được đứng liền nhau (ca "Nợ/Có") |
| **Gợi ý khám phá** | Bài 1 của lối vào có một câu trong nội dung: *"Chữ có gạch chấm: chạm để xem nghĩa."* Không cần storage |

---

## 5. Rủi ro

| Rủi ro | Mức | Giảm thế nào |
|---|---|---|
| **Không ai chạm**, vì tooltip khó khám phá (S24) | Cao | Tín hiệu nhất quán + câu gợi ý trong bài 1 + đo ở buổi thử |
| Chạm trượt giữa hai thuật ngữ gần nhau | Trung bình | `line-height`, quy tắc biên tập ở trên |
| Chữ nhảy khi đóng thẻ phía trên trên iOS ≤ 26 | Trung bình | Không tự đóng. Thử trên iPhone iOS 26 trong Zalo |
| Đoạn văn bị cắt đôi, kém "sạch" | Trung bình | Duy duyệt bằng mắt. Nếu khó chịu thì chuyển sang (a2) |
| Gạch chấm hoặc `(Debit)` khó thấy lúc tối, dark mode | Trung bình | Kiểm tương phản ≥ 4.5:1 cho chữ phụ. Duy duyệt ở độ sáng thấp |

**Đổi ngược rẻ**, *với điều kiện* glossary là nguồn duy nhất và cách hiện chỉ là một cờ render (WRITER §2). Cả (c) lẫn (a2) đều dựng trên cùng `<button aria-expanded>` và cùng dữ liệu.

## 6. Cách thử với 5 người

Gộp vào buổi quan sát 5 người đọc bài 1 mà WRITER §2 đã hẹn.

| Mục | Cách làm |
|---|---|
| Người | 5 người đúng persona, dùng **máy của chính họ**. Cố có ≥ 1 iPhone iOS 18.x, ≥ 1 iOS 26, ≥ 1 Android tầm trung |
| Bối cảnh | Gửi link **qua Zalo**, mở trong WebView, buổi tối, không nhắc tới chú thích |
| So sánh | Hai bài: một bài dùng (c), một bài dùng (a2). Đổi thứ tự giữa các người |
| Ghi lại | Có tự chạm không · số lần chạm trượt · có đóng được không · có phải cuộn tìm lại chỗ đọc không · Back hoặc vuốt mép có làm văng khỏi bài không · sau bài hỏi "Nợ ở đoạn X nghĩa là gì" · thích dạng nào |
| Luật quyết (PM đề xuất, **không có nguồn**) | ≥ 2/5 người lạc chỗ đọc với (c) ⇒ chuyển sang (a2). ≤ 1/5 tự chạm ⇒ xem lại tín hiệu trước khi bàn tới dạng hiển thị. Back văng khỏi bài ở bất kỳ dạng nào ⇒ lỗi chặn |

---

## 7. Chưa xác minh được

- **Không tìm thấy nghiên cứu nào so sánh trực tiếp** inline, popover và bottom sheet cho chú thích thuật ngữ trên mobile, có đo mức hiểu bài. Đó là *phương pháp này không tìm thấy*, không có nghĩa là nghiên cứu đó không tồn tại.
- Toàn bộ bằng chứng về glossing là **người học ngoại ngữ**, phần lớn trên **giấy** hoặc máy tính. Người đọc WMS đọc tiếng mẹ đẻ, chỉ thuật ngữ là lạ. Chuyển kết quả sang là suy luận.
- **Zalo WebView chưa đo gì cả:** engine thực tế trên iOS (WKWebView hay SFSafariViewController), Back Android, vuốt mép iOS, giữ vị trí cuộn, thanh công cụ đáy, `text-decoration-style: dotted`.
- Tỉ lệ iPhone ở VN còn chạy iOS 18 hay đã lên 26/27: không có số liệu.
- `overflow-anchor` trên iOS (S25) và CSS anchor (S14) là ảnh chụp caniuse, chưa fetch lại, có thể đã đổi.
- Apple HIG là guideline cho app native. Nó khuyên **sheet modal** thay popover, tức **không** ủng hộ (c). Ở đây HIG chỉ được dùng làm lý lẽ chống popover.
- "Popup tip" của NN/g gắn với icon ?/i, bài viết tập trung vào desktop. Áp nó cho thuật ngữ nằm giữa câu là suy luận.
- Hành vi hiện tại của Wikipedia mobile drawer chỉ lấy từ ticket Phabricator. Wikimedia không công bố kết quả đo cho drawer.
- Kindle, Apple Books, Duolingo, Medium, Investopedia, app ngân hàng VN: **không kiểm được**, nên không có trong bảng so sánh.
- Nút giữa câu với VoiceOver và TalkBack giọng Việt; hỗ trợ `aria-details`: chưa thử tay.
- Ngân sách cho câu ví dụ, và lợi ích của ví dụ đời thường: không có nguồn.
- Bỏ khỏi bằng chứng vì chỉ đọc qua đoạn trích của kết quả tìm kiếm: DeStefano & LeFevre 2007, Mayer spatial contiguity, Floating UI docs, Abraham 2008 / Taylor 2006.
- Gui et al. 2025: vế "lặp lại giúp nhớ nghĩa" chưa có trong abstract đã đọc ⇒ không dùng.

---

## 8. Nguồn

Trích nguyên văn chỉ dùng cho nguồn có giấy phép mở (W3C, MDN, Wikipedia, caniuse, web.dev). Nguồn có bản quyền
(NN/g, Apple, bài báo) được **diễn đạt lại**. Nguyên văn của chúng đã được lens evidence đối chiếu ngày 2026-10-24.

| # | Nguồn | Nội dung |
|---|---|---|
| S1 | https://www.nngroup.com/articles/tooltip-guidelines/ | Tooltip thường không có trên màn cảm ứng. Che nội dung liên quan thì người dùng phải lặp lại thao tác. Thông tin quan trọng phải nằm trên trang. Nội dung dài thì không còn là tip |
| S2 | https://developer.apple.com/tutorials/data/design/human-interface-guidelines/popovers.json | Tránh popover ở màn hẹp, dùng sheet thay thế. Popover đóng khi chạm ra ngoài |
| S3 | https://developer.apple.com/design/human-interface-guidelines/popovers | Lý tưởng là popover không che phần tử đã gọi nó |
| S4 | https://www.nngroup.com/articles/bottom-sheet/ | Vuốt dọc dễ lẫn với cuộn. Đáy màn hình không phải lúc nào cũng dễ với tới. Nên có nút Close và cho Back đóng sheet |
| S5 | https://github.com/material-components/material-components-android/blob/master/docs/components/BottomSheet.md | Modal sheet chặn tương tác với phần còn lại; standard sheet thì không |
| S6 | https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php | Hoober: người dùng đọc tốt nhất ở giữa màn hình. Quan sát thực địa, không có đối chứng |
| S7 | https://meta.wikimedia.org/wiki/WMDE_Technical_Wishes/References/Reference_Previews | Người đọc nhảy xuống footnote rồi không biết quay lại đoạn đang đọc |
| S8 | https://phabricator.wikimedia.org/T216961 | Wikipedia mobile: footnote mở dạng drawer ở đáy |
| S9 | https://phabricator.wikimedia.org/T418812 | "a bottom sheet that appears when a reader taps a blue link" |
| S10 | https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/ | "Tooltip widgets do not receive focus." · "does not yet have task force consensus." |
| S11 | https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/ | "The element that shows and hides the content has role button." |
| S12 | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | Miễn trừ: "The target is in a sentence" |
| S13 | https://developer.mozilla.org/en-US/docs/Web/API/Popover_API/Using | "an implicit aria-details and aria-expanded relationship is set up between them" |
| S14 | https://caniuse.com/css-anchor-positioning | "Versions 26.0 to 26.6 have partial support." |
| S15 | https://web.dev/blog/popover-baseline | "needed to wait until the bug was fixed in Safari 18.3" |
| S16 | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Linking | "Link a term at most once per major section, at first occurrence." |
| S17 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7497986 | Fitzsimmons et al. 2020: người đọc dùng link làm dấu hiệu của thông tin quan trọng, và nhìn chữ có link lâu hơn. Link xanh, màn hình máy tính, người bản ngữ Anh |
| S18 | https://www.nngroup.com/articles/guidelines-for-visualizing-links | Chỉ dùng màu link cho link. Dành gạch chân cho link |
| S19 | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/abbr | "Some browsers add a dotted underline to the content of the element." |
| S20 | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details | "Permitted parents: Any element that accepts flow content." |
| S21 | Yanagisawa, Webb & Uchihara 2020, SSLA 42(2), DOI 10.1017/s0272263119000688 | Meta-analysis 42 nghiên cứu, N = 3802. Chú thích L1 tốt hơn L2. In-text gloss và glossary tách rời là hai dạng kém nhất. Gloss trắc nghiệm là dạng tốt nhất |
| S22 | https://psychology.ecu.edu/wp-content/pv-uploads/sites/216/2019/03/Roediger-Karpicke-2006.pdf | Tự kiểm tra cho khả năng nhớ sau 2 ngày và 1 tuần tốt hơn đọc lại. Ở mốc 5 phút thì đọc lại thắng |
| S23 | https://my.chartered.college/impact_article/expertise-reversal-effect-and-its-instructional-implications/ | Kalyuga: phần hỗ trợ giúp người mới có thể gây hại cho người đã biết |
| S24 | https://www.nngroup.com/articles/tooltip-guidelines/ | Tooltip khó khám phá vì thiếu tín hiệu thị giác |
| S25 | https://caniuse.com/css-overflow-anchor | iOS Safari "3.2 - 26.6: Not supported" |
| S26 | https://web.dev/articles/cls | "Layout shifts that occur within 500 milliseconds of user input". Dịch chuyển do người dùng gây ra không bị tính là bất ngờ. Đây là metric hiệu năng, không phải đo cảm nhận |
