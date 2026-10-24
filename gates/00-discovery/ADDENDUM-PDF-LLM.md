---
status: pass
stage: 00-discovery
date: 2026-10-24
---
# ADDENDUM — Trình đọc PDF + LLM quiz card

> **2026-10-24 — SUPERSEDED MỘT PHẦN:** viết trước câu 3–11. Duy đã quyết **ngược** hai khuyến nghị của file này: câu 3 — máy sinh card nạp cả Hermanson CC BY (không chỉ bài tự viết); câu 4 — **CÓ** trình đọc PDF ở mùa 1 (không "hoãn", không "không build"). Bảng "8 câu hỏi" đã gộp vào 14 câu của `PRODUCT-BRIEF.md` §Quyết định của Duy. **Phần còn hiệu lực và là spec duy nhất:** đường ống card (§Đường ống PDF → card) và các ràng buộc định dạng card.

**TL;DR** · đọc khoảng 10 phút · *tôi không phải luật sư*
- Tính năng "người học tải PDF lên, LLM tóm tắt thành quiz" ở runtime **đã có sẵn và miễn phí** ở NotebookLM/Gemini Notebook. Tự dựng thì phải có proxy giữ key, chịu trách nhiệm bản quyền cho sách của người lạ và chuyển dữ liệu ra nước ngoài, mà doanh thu thì bằng 0.
- On-device không chạy được cho người học điển hình. Chrome built-in AI không có trên điện thoại và không có tiếng Việt. Apple không có JS API. WebLLM cần 1,6–2,5 GB VRAM.
- Thứ trả lời đúng nỗi lo *"không có tài liệu thì sao nắm kiến thức"* là **bài đọc HTML + 3–5 card cuối mỗi bài**. Card sinh nháp bằng LLM **lúc build**, chỉ từ bài Duy tự viết, và Duy duyệt từng thẻ.
- LLM sinh câu hỏi sai kiến thức 6–22% (đo ở y khoa/tiếng Anh). Không có người duyệt thì khoảng 1/5 card có thể dạy sai, mà người mới không tự phát hiện được.
- **Go-có-điều-kiện.** Go cho *card tĩnh sinh lúc build, Duy duyệt*. No-go cho *LLM chạy runtime trên PDF người dùng* ở mùa 1. Trình đọc PDF trong site: hoãn, chờ phép đo 5 người (Q3).

## Đối thủ đã làm việc này

| Tên | Miễn phí? | Tiếng Việt? | Ghi chú | URL |
|---|---|---|---|---|
| NotebookLM → đổi tên **Gemini Notebook** | Có. Gói rẻ nhất cho 100 notebook, 50 nguồn/notebook. Quota thẻ "reset after 24 hours", không nêu số | Vietnamese có trong danh sách output language. **Flashcard/quiz không có trong danh sách đó**, nên chưa xác minh | Chỉnh được độ khó và số thẻ. Bắt buộc tài khoản Google đã xác minh tuổi. Người xem notebook công khai **không tạo được thẻ** ("you need edit access"). Có app điện thoại, nhưng chưa xác minh flashcard có trên app không | blog.google/…/notebooklm-app-quizzes-flashcards · support.google.com/notebooklm/answer/16958963 · support.google.com/gemininotebook/answer/16261963 |
| Gemini app (bản free) | Có | Chưa kiểm | "document upload is now available to all Gemini users" (2/2025). Giới hạn khoảng 50 trang lấy từ nguồn thứ cấp, có thể đã đổi | 9to5google.com/2025/02/25/free-gemini-document-upload |
| ChatGPT app | Có gói free | Chưa kiểm | 81% người VN dùng AI chọn ChatGPT (Decision Lab, n=600, panel online). Giới hạn upload file của bản free chưa xác minh (help.openai.com trả 403) | decisionlab.co/blog/vietnam-consumer-ai-market-2025-… |
| flashcards.world | 3 lượt/ngày, phải đăng nhập | Chưa kiểm | Ghi rõ không đọc được PDF scan không có lớp text | flashcards.world/pdf-to-flashcards |
| Knowt | Free có quảng cáo, lượt AI giới hạn | Chưa kiểm | Giá gói trả phí mâu thuẫn giữa các review | itechguides.com/best/ai-study-tools/knowt |
| App VN làm PDF→flashcard tiếng Việt | n/a | n/a | **Phương pháp này không tìm thấy** (1 search tiếng Việt, chỉ ra app quốc tế) | n/a |

**Giá trị còn lại của Where Money Sleeps** không nằm ở "tóm tắt PDF bất kỳ" mà ở bốn điểm: (1) card **gắn vào đúng bài và đúng giai đoạn** của lộ trình dòng tiền fintech tiếng Việt; (2) card **đã được người duyệt**, quan trọng khi một con số sai về APR hay "ghi có" sẽ dạy sai; (3) không tài khoản; (4) chạy offline trên điện thoại yếu.

## Bốn cách chạy LLM trên PDF của người học (và phương án build-time)

Giá đọc từ trang pricing chính thức ngày **2026-10-24**. "1 cuốn" = 250 trang, **giả định** khoảng 150k token text và 30k token output. Hai con số giả định này chưa đo trên sách thật.

| Cách | Ai dùng được | Chi phí cho Duy / 1 cuốn | Dữ liệu đi đâu | Giữ lời hứa "không tài khoản, không định danh"? | Rủi ro chính |
|---|---|---|---|---|---|
| **On-device** (Chrome AI, WebLLM) | Chrome AI: 0% trên điện thoại, không có tiếng Việt. WebLLM: chỉ máy có WebGPU (iOS 26 Safari, Android 12+ GPU Qualcomm/ARM) và chịu tải model lớn | $0 | Ở lại máy | Có | Model 1,5B–3B cần 1,6–2,5 GB VRAM, context 4096 nên phải cắt hàng trăm khúc. Tiếng Việt yếu (VMLU 48,6–52,9, đây là thước đo kiến thức, không đo tóm tắt). iOS có thể kill tab mà không báo lỗi. Người học bỏ site >7 ngày trong tab Safari thì mất model cache (web app standalone có persist()=true thì được miễn) |
| **BYOK** (key của người học, trình duyệt gọi thẳng) | Gần như không ai trong persona: người học không có API key | $0 | Từ trình duyệt người học đi thẳng tới nhà cung cấp ở Mỹ | Phía site có giữ được | Key nằm trong localStorage nên extension/XSS đọc được. Google khuyên dùng backend proxy chứ không nhúng key vào web app |
| **Proxy của Duy** (Cloudflare Worker + key Duy) | Mọi người, kể cả trên điện thoại | Gemini 2.5 Flash-Lite paid ($0.10 in / $0.40 out mỗi 1M; PDF 258 token/trang): **khoảng $0,018**. Claude Haiku 5.5 ($0.10/$0.50 khi ≤100k): **khoảng $0,03**, Batch khoảng $0,015. gpt-5-nano ($0.05/$0.40): khoảng $0,02 (chưa kiểm chéo). Workers AI free: 10.000 neurons/ngày, tức **khoảng 4–6 cuốn/ngày cho cả site** | Đi qua Worker của Duy tới Google/Anthropic ở Mỹ. Gói paid của Gemini không dùng dữ liệu để train nhưng vẫn lưu log có hạn để chống lạm dụng. Gói free cho người duyệt đọc input | **Không.** Phá lời hứa "file không rời máy bạn" | Relay LLM miễn phí cho cả internet (Turnstile chặn bot, không chặn người). Duy **bảo đảm theo hợp đồng** là có quyền với mọi sách người dùng tải lên. Phải nộp hồ sơ chuyển dữ liệu xuyên biên giới (Luật 91/2025). Trần ngân sách cứng chỉ có ở Gemini prepaid (hết credit thì trả 402). gemini-2.5-flash-lite không còn được khuyên dùng cho dự án mới |
| **Trao tay công cụ ngoài** (NotebookLM, hoặc "Ôn với ChatGPT/Gemini của bạn") | Người có tài khoản Google/ChatGPT. Mở link trong WebView Zalo sẽ bị chặn đăng nhập Google (nguồn 2021, đọc qua bản tóm tắt), người học phải tự chuyển sang Chrome/Safari | $0 | Người học tự đưa file vào tài khoản của họ. Không qua hạ tầng của Duy | Phía site có. Người học phải có tài khoản ở bên kia | Card không ai duyệt nên phải gắn nhãn "do AI của bạn tạo, có thể sai". Card không đổ về tiến độ trong site. Site chính là bên gợi ý đường đi: đặt nút này cạnh link OpenStax là chạm điều khoản chống LLM |
| *Build-time (Duy chạy, card tĩnh)* | Mọi người, offline | Khoảng $0,02–0,03/cuốn, nhưng tập sách được phép nạp gần như rỗng. **Đơn vị chi phí thật là giờ duyệt của Duy** | Chỉ bài của Duy đi tới LLM, không có dữ liệu người học | Có | Card sai lọt ra nếu duyệt ẩu. Không đáp ứng ý "sách thật trong tay" |

## Đường ống PDF → card và cơ chế chống sai

Đường ống này chạy **ở phía tác giả, trên máy Duy**, không chạy trên điện thoại người học.

| Bước | Làm gì | Chống sai bằng gì |
|---|---|---|
| 1. Nguồn | Chỉ bài Duy tự viết. Hermanson chỉ sau khi kiểm trang bản quyền trong PDF gốc. **Không** OpenStax hiện hành, không sách trả phí | LEGAL-SCREEN |
| 2. Trích chữ | Bài HTML thì lấy thẳng. PDF thì dùng PDF.js `getTextContent`; trang nào ra rỗng thì đánh dấu là scan | Không đoán chữ từ trang rỗng |
| 3. Scan / tiếng Việt | Dùng tesseract `vie` trên máy Duy, sau đó Duy soát dấu (dễ nhầm "lãi" với "lại") | Con số ">97%" là tuyên bố cũ, chỉ cho 4 font và scan 200–400 DPI. Một worker tesseract.js tốn khoảng 164 MB (benchmark web của dự án). Vì vậy **không OCR trên điện thoại** |
| 4. Chia nhỏ | Mỗi lần gọi chỉ một mục hoặc một trang khái niệm, **tối đa khoảng 5 card**, prompt kèm mục tiêu học | Hallucination dồn về cuối các response dài. Câu hỏi không trúng trọng tâm thì mất hiệu ứng testing (Myers 2023) |
| 5. Kiểm tất định (script) | Mỗi card có `source_quote` và số trang. (a) `source_quote` phải khớp chuỗi trong nguồn. (b) Mọi con số và ký hiệu `%`, `đ`, `$` trong đáp án phải có trong `source_quote`. Trượt thì **loại, không sửa** | Bắt được trích dẫn bịa và con số không có nguồn. **Không** bắt được trường hợp hiểu sai một câu trích đúng |
| 6. Không dùng LLM chấm LLM | n/a | FABLES: các rater LLM về faithfulness không tương quan mạnh với người chấm (đo trên sách hư cấu, model 2024; áp sang sách tài chính là ngoại suy) |
| 7. Duy duyệt từng card | Việc không agent nào làm thay (quy tắc 6) | Drexel: 91% câu LLM là "điểm khởi đầu hợp lý để sửa", tức mô hình nháp-rồi-duyệt có cơ sở |
| 8. Định dạng | **Chạm, không gõ**: trắc nghiệm có phản hồi ngay, hoặc lật thẻ rồi tự chấm Nhớ/Chưa nhớ. Cấm dùng con số tài chính làm phương án nhiễu nếu không có phản hồi. Sau đáp án hiện một dòng giải thích và link "đọc lại đoạn này" tới `sectionId` | Phương án nhiễu có thể bị nhớ nhầm; phản hồi làm giảm điều đó (Butler & Roediger) |
| 9. Ôn | Theo phiên, đặt ngay cuối bài và 1–2 thẻ ở đầu phiên sau. Không có bộ ôn riêng, không lịch theo ngày | Safari xoá storage sau 7 ngày không tương tác. Mất thì chỉ mất trạng thái "đã thuộc", card vẫn còn |

## Pháp lý

**Người dùng tự tạo card từ sách của họ** và **Duy tạo sẵn card rồi publish** là hai chuyện pháp lý khác hẳn nhau.

| Tình huống | Đã verify (nguồn gốc) | Vùng xám | Câu hỏi luật sư |
|---|---|---|---|
| **Duy publish card làm sẵn từ sách còn bản quyền** | Castle Rock (2d Cir. 1998): sách 643 câu đố Seinfeld không phải fair use | Án đó về tác phẩm hư cấu, và toà coi trọng việc tác phẩm không phải "commentary or analysis". Quiz khái niệm từ sách phi hư cấu chưa có án lệ. **Lằn ranh "không publish" là lựa chọn thận trọng, không phải điều án lệ buộc** | (b) Tóm tắt hay bộ câu hỏi do LLM tạo có là "cải biên/biên soạn" theo Đ.4 k8 Luật SHTT không? |
| **Duy publish card từ bài tự viết** | Đ.15 Luật SHTT không bảo hộ khái niệm (LEGAL-SCREEN) | Luật AI 134/2025: một dòng "soạn với hỗ trợ AI, duyệt bởi Duy, ngày" | n/a |
| **Duy publish card từ OpenStax hiện hành** | Cấm "ingested into large language models or generative AI offerings" khi chưa có phép | n/a | **Không đụng** |
| **Người dùng tải PDF lên, proxy dùng key của Duy** | Anthropic Commercial Terms §L.1: Customer bảo đảm có quyền với mọi Input; §K.3 loại Input khỏi bồi hoàn. OpenAI Services Agreement (ONLINE v.010126) §4.3 + §13.2: Input gồm cả input của End User, Customer bồi hoàn cho OpenAI. Google API Terms: developer phải có quyền "from your end users". Luật 91/2025 (hiệu lực 01/01/2026): dùng nền tảng nước ngoài xử lý dữ liệu thu tại VN là chuyển xuyên biên giới, hồ sơ trong 60 ngày; miễn trừ SME không che phần này | Duy cá nhân có được hưởng miễn trừ SME không. Duy là "bên kiểm soát và xử lý" hay "bên xử lý". Sao kê ngân hàng có là dữ liệu nhạy cảm theo Luật 91 không | (a) Ngoại lệ Đ.25 có che cho dịch vụ bên thứ ba xử lý bản sao của người dùng không? (d) Vai trò của Duy theo Luật 91? (e) Disclaimer "chỉ tải tài liệu bạn có quyền" có chuyển được trách nhiệm không? |
| **Người dùng tải PDF lên, xử lý trên máy họ (on-device hoặc BYOK)** | Luật 91 có ngoại lệ "chủ thể tự chuyển dữ liệu của mình" | Đ.25 k1: hai nguồn thứ cấp ghi khác nhau ("học tập" hay "giảng dạy"), và có câu loại trừ "sao chép bằng thiết bị sao chép" | (c) Trình duyệt gọi thẳng nhà cung cấp có đúng là "chủ thể tự chuyển" không? |
| **Site chỉ phát prompt, người dùng tự đưa sách vào chatbot của họ** | n/a | Site là bên gợi ý đường đi. Đặt cạnh link OpenStax thì đúng là dẫn tới việc OpenStax cấm | (f) Duy có trách nhiệm gián tiếp không, nhất là với OpenStax? |
| **Trình đọc PDF thuần cục bộ (PDF.js, không gửi gì đi)** | PDF.js Apache-2.0 (LEGAL-SCREEN) | n/a | n/a |
| NĐ 147 | n/a | Tóm tắt riêng cho một người thì nhiều khả năng **không** thành "thông tin tổng hợp" (nguồn thứ cấp, công văn đính chính 2025 chưa đọc) | n/a |

## Đề xuất hình dạng tính năng

| | Mùa 1 | Mùa 2 (chỉ khi có điều kiện ở cột phải) |
|---|---|---|
| Tài liệu đọc | Bài HTML reflow (đã chốt ở S0), thẻ sách "đọc chương nào" kèm link mua, deep-link OpenStax | n/a |
| Quiz card | 3–5 card mỗi bài, LLM nháp lúc build, qua kiểm `source_quote` + kiểm con số, Duy duyệt từng thẻ, ship JSON tĩnh. Thay luôn "3–5 câu tự kiểm" của S0, không thêm khối mới | Card theo chương cho thẻ sách: Duy tự viết câu hỏi khái niệm bằng chữ của mình, người học tự mua sách. **Chờ luật sư trả lời câu (b)** |
| Trình đọc PDF | **Không build.** Thêm một câu vào buổi 5 người đọc bài 1: "bạn có PDF sách nào muốn đọc ở đây không?" | Nếu ≥2/5 người có: lát mỏng PDF.js lazy, thuần cục bộ, ghi "file không rời máy bạn", **LLM không chạm vào file** |
| "Ôn với AI của bạn" | Không | Prompt tĩnh có nút Copy, hướng dẫn 3 bước, gắn nhãn "có thể sai", không đặt cạnh OpenStax. Cần Duy tự thử prompt 30 phút trên Gemini/ChatGPT free, và luật sư trả lời câu (f) |
| LLM runtime trên PDF người dùng (on-device / BYOK / proxy) | **No-go** | Ghi `N/A — because` không đáp ứng persona và lời hứa riêng tư; xem lại khi Chrome AI có tiếng Việt trên điện thoại |

## Câu hỏi Duy phải quyết

**Tổng cộng 8 câu, hỏi từng câu một.** Thứ tự: câu rẻ nhất và gỡ được nhiều thứ nhất đi trước, câu tổng về rủi ro đi cuối. Q1 có trước thì mới biết có cần proxy hay không; nếu Q1 là "có" thì Q7 và Q8 gần như tự trả lời.

| # | Phải quyết | Quan hệ với PRODUCT-BRIEF | Khuyến nghị và lý do |
|---|---|---|---|
| 1 | **Loại LLM runtime trên PDF người dùng (on-device, BYOK, proxy) khỏi mùa 1?** | **Thay thế** phần "LLM chạy ở đâu, ai trả tiền" của 2/9 | **Có.** On-device dùng được 0% trên điện thoại. BYOK không ai trong persona có key. Proxy bắt Duy bảo đảm bản quyền cho sách của người lạ và nộp hồ sơ Luật 91. Đảo lại được ở mùa 2 mà không mất gì |
| 2 | **Máy sinh card chỉ được nạp bài Duy tự viết (Hermanson sau khi kiểm PDF gốc)?** | **Đóng** câu còn treo ở dòng log 2/9 thứ ba ("nạp sách NÀO") | **Có.** Đây là tập duy nhất không có rủi ro bản quyền và không đụng điều khoản chống LLM của OpenStax |
| 3 | **Trình đọc PDF trong site còn bắt buộc ở mùa 1 không?** | **Thay thế** câu 2/9 (dòng log đặt PDF thành bắt buộc) | **Hoãn**, gắn vào phép đo 5 người. Persona khó có PDF sách tài chính hợp pháp, iOS Files/Chrome đã mở được PDF, và PDF.js không reflow. Đảo lại rẻ: lát PDF.js lazy chỉ khoảng 577 KB và không đụng trang bài |
| 4 | **Duy có chấp nhận duyệt từng card không?** | Liên quan câu 7 (duyệt chuyên môn): card về APR/TT 99 đi chung luồng với người kế toán | **Có, nhưng đo trước trên 1 bài** để biết số phút mỗi bài. Không duyệt thì khoảng 1/5 card có thể sai (ngoại suy từ y khoa) |
| 5 | **Định dạng card: chạm, không gõ?** | Mới | **Có.** Trắc nghiệm có phản hồi ngay + lật thẻ tự chấm. Cấm con số làm phương án nhiễu nếu không có phản hồi. Có thể để S2 chốt chi tiết |
| 6 | **"Ôn với AI của bạn" (trao tay prompt) làm ở mùa nào?** | Mới | **Mùa 2.** Tốn $0 và không có proxy, nhưng card không ai duyệt và chưa có câu trả lời (f) từ luật sư. Duy cần thử prompt 30 phút trước |
| 7 | **Có bao giờ trả tiền LLM runtime (ví dụ nạp trước $10 Gemini) khi doanh thu bằng 0 không?** | **Gộp vào câu 6** (kiếm tiền) | **Không ở mùa 1.** Q1 = "có" thì câu này không phát sinh. Build-time tốn dưới $1 cho cả thư viện, đã nằm trong "chi phí gần 0" |
| 8 | **Chấp nhận rủi ro pháp lý còn lại? Thuê luật sư trả lời (a)–(f)?** | **Gộp vào câu 9** (rủi ro pháp lý tổng) | **Không thuê ở mùa 1** nếu Q1 và Q2 đều là "có", vì khi đó không còn phần B. Thuê trước khi làm bất kỳ thứ gì ở mùa 2 có dính sách của người khác (card theo chương, nút trao tay) |

## Chưa xác minh được

- **Tỉ lệ sai khi LLM sinh card từ văn bản tiếng Việt về tài chính/kế toán.** Con số 6–22% đo trên y khoa, tiếng Anh, ChatGPT-4/4o. Drexel n=65; PMC thiếu cỡ mẫu (24/34 người), mỗi bộ 100 câu.
- Token/trang của sách thật (giả định 600) và token output (giả định 30k). Tiếng Việt có tốn token hơn không. Mọi con số "chi phí 1 cuốn" đều đứng trên hai giả định này.
- Giá của Gemini 3.5 Flash-Lite / 3.8 Flash (model Google khuyên cho dự án mới) và cách tính token PDF của chúng. Hạn mức free tier Gemini (nguồn thứ ba mâu thuẫn).
- Lens evidence chỉ fetch lại 7/18 citation của mũi API. OpenAI pricing, Claude PDF-support, available-regions, rate-limits, api-key, hai README SDK, Workers limits, Turnstile **chưa được kiểm chéo**.
- Flashcard/quiz của Gemini Notebook có sinh bằng tiếng Việt không. Có trên app điện thoại không. Có miễn phí cho tài khoản cá nhân ở VN không. Giới hạn số thẻ/ngày.
- Giới hạn upload file của ChatGPT và Gemini bản free (help.openai.com trả 403).
- WebView Zalo: `input type=file` có chạy không, đăng nhập Google có bị chặn không (câu trích 2021 đọc qua bản tóm tắt).
- Cỡ file model WebLLM phải tải (chỉ có `vram_required_MB`). Tốc độ trên điện thoại tầm trung. WebGPU có bật mặc định ở Safari 26 bản cuối không. Cache API có bị xoá theo mốc 7 ngày không.
- Số liệu StatCounter VN (Apple 40,2%) và iOS 26 adoption 79%: đọc qua bản tóm tắt search.
- Decision Lab 78%/81% là panel online n=600; Microsoft 2026 đưa số thấp hơn nhiều (~27,9%). Persona "không biết LLM là gì" có thể sai.
- **Tỉ lệ người học có PDF hợp pháp muốn đọc**: không có số liệu nào. Đó là lý do Q3 gắn với phép đo 5 người.
- Độ chính xác tesseract `vie` trên sách VN thật. tesseract.js có kèm sẵn `vie` không.
- Luật VN: nguyên văn Đ.25 k1 và Đ.4 k8 sau sửa 2022; NĐ 13/2023 còn hiệu lực phần nào sau Luật 91; nội dung NĐ 330/2026; DPA của Anthropic; phần luật VN chưa được lens evidence fetch lại.
- Các lens phản bác đều là phiên Claude. **Same vendor, same priors — no external verifier ran.**

## Nguồn

Đọc ngày 2026-10-24 trừ khi ghi khác.

- On-device: https://developer.chrome.com/docs/ai/get-started · https://developer.chrome.com/docs/ai/built-in-apis · https://developer.chrome.com/docs/ai/summarizer-api · https://developer.apple.com/forums/thread/833716 · https://webkit.org/blog/16993/news-from-wwdc25-web-technology-coming-this-fall-in-safari-26-beta/ · https://developer.chrome.com/blog/new-in-webgpu-121 · https://github.com/mlc-ai/web-llm/blob/main/src/config.ts · https://kiki-ailab-readme.static.hf.space/ · https://bugs.webkit.org/show_bug.cgi?id=303203 · https://9to5mac.com/2026/06/10/ios-26-adoption-grows-but-still-lags-slightly-behind-ios-18/ · https://gs.statcounter.com/vendor-market-share/mobile/viet-nam · https://pinggy.io/blog/run_llm_in_browser_webgpu/
- Giá và API: https://ai.google.dev/gemini-api/docs/pricing · https://ai.google.dev/gemini-api/docs/document-processing · https://ai.google.dev/gemini-api/docs/billing · https://ai.google.dev/gemini-api/docs/deprecations · https://ai.google.dev/gemini-api/docs/available-regions · https://ai.google.dev/gemini-api/docs/rate-limits · https://ai.google.dev/gemini-api/docs/api-key · https://platform.claude.com/docs/en/about-claude/pricing · https://platform.claude.com/docs/en/build-with-claude/pdf-support · https://developers.openai.com/api/docs/pricing · https://github.com/anthropics/anthropic-sdk-typescript · https://github.com/openai/openai-node · https://developers.cloudflare.com/workers-ai/platform/pricing/ · https://developers.cloudflare.com/workers-ai/models/qwen3-30b-a3b-fp8/ · https://developers.cloudflare.com/workers/platform/limits/ · https://developers.cloudflare.com/turnstile/plans/
- Pháp lý: https://www.copyright.gov/fair-use/summaries/castlerock-carolpubl’g-2dcir1998.pdf · https://matthewsag.com/copyright-winter-is-coming-to-wikipedia/ · https://lsvn.vn/bo-sung-cac-truong-hop-ngoai-le-khong-xam-pham-quyen-tac-gia1657018953-a120831.html · https://hethongphapluat.com/luat-so-huu-tri-tue-2005/dieu-25 · https://hethongphapluat.com/luat-so-huu-tri-tue-2005/dieu-4 · https://www.anthropic.com/legal/commercial-terms · https://cdn.openai.com/osa/openai-services-agreement.pdf · https://developers.google.com/terms · https://ai.google.dev/gemini-api/terms · https://openstax.org/books/principles-finance-2e/pages/preface · https://openstax.org/tos · https://www.tgu.edu.vn/upload/files/Tailieu-gioithieu-LuatBaovedulieucanhan.pdf · https://hethongphapluat.com/nghi-dinh-147-2024-nd-cp-quan-ly-cung-cap-su-dung-dich-vu-internet-va-thong-tin-tren-mang/dieu-3
- Chất lượng: https://researchdiscovery.drexel.edu/esploro/outputs/journalArticle/LLM-Generated-Multiple-Choice-Practice-Quizzes-for/991022059818004721 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11806894/ · https://bjo.bmj.com/content/110/7/836 · https://mrbartonmaths.com/resourcesnew/8.%20Research/Formative%20Assessment/Feedback%20enhances%20the%20positive%20effects%20and%20reduces.pdf · https://escholarship.org/uc/item/4043m5w0 · https://arxiv.org/abs/2507.05629v2 · https://hausman.sites.ucsc.edu/files/2023/08/2023-99019-001.pdf · https://arxiv.org/abs/2404.01261 · https://arxiv.org/abs/2505.15291 · https://vietunicode.sourceforge.net/howto/tesseract-ocr.html · https://unpkg.com/tesseract.js@6.0.1/docs/performance.md · https://github.com/naptha/tesseract.js/releases/tag/v5.0.0 · https://andymatuschak.org/prompts/
- Đối thủ và người dùng: https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-app-quizzes-flashcards/ · https://support.google.com/gemininotebook/answer/16261963?hl=en&co=GENIE.Platform%3DDesktop · https://support.google.com/notebooklm/answer/16213268?hl=en · https://support.google.com/notebooklm/answer/16958963?hl=en · https://support.google.com/notebooklm/answer/16269187?hl=en · https://support.google.com/notebooklm/answer/16322204?hl=en · https://workspaceupdates.googleblog.com/2025/09/flashcards-quizzes-reports-notebook-lm-google-education.html · https://9to5google.com/2025/11/06/notebooklm-app-flashcards-quizzes/ · https://9to5google.com/2025/02/25/free-gemini-document-upload/ · https://www.itechguides.com/best/ai-study-tools/knowt/ · https://flashcards.world/pdf-to-flashcards/ · https://www.decisionlab.co/blog/vietnam-consumer-ai-market-2025-78-of-online-population-have-engaged-with-ai-one-third-turn-it-into-a-daily-habit · https://technode.global/2025/08/27/report-78-percent-of-online-population-in-vietnam-have-engaged-with-ai-one-third-turn-it-into-a-daily-habit/
- Nội bộ: `gates/00-discovery/PRODUCT-BRIEF.md` (dòng log 2/9) · `gates/00-discovery/LEGAL-SCREEN.md` · `../../../docs/lessons.md` (iOS 7 ngày, Stripe không hỗ trợ merchant VN)

> **2026-10-24 — bổ sung cho §Đường ống, bước 1 (Nguồn):** với Hermanson, **loại** mọi đoạn trích bên thứ ba có © riêng (10 trích FASB, New Accountant 1990, báo cáo thường niên GE/Gillette/Coca-Cola, WSJ — danh sách ở `legal/licences.json` trường `exclusions`). Mọi chỗ "chờ luật sư" trong file này ⇒ **chờ workflow pháp lý + Duy ký** (câu 12).
