---
status: pass
stage: 05-launch
date: 2026-11-09
owner: marketing
blocked_on: []
---

# POSITIONING — Định Vị Sản Phẩm, Tagline Hợp Đồng & Chuẩn Phát Hành Đa Kênh (`S5 Launch` — `where-money-sleeps`)

> **Hợp đồng định vị (`gates/ONE-PAGER.md`, `QĐ 22`, `QĐ 55`, `QĐ 56`):** Mọi bề mặt xuất hiện tên `Where Money Sleeps` (tiêu đề trang, trang chủ, thẻ chia sẻ OpenGraph, mô tả kênh `@WhereMoneySleeps`) **bắt buộc** đi kèm tagline giải nghĩa để người đọc không nhầm với trang gửi tiết kiệm hay tiền mã hoá.

## 1. Tên Sản Phẩm & Tagline Bắt Buộc (`AC-39`, `QĐ 22`, `QĐ 55`)

| Thuộc tính | Bản Tiếng Việt (`vi`) | Bản Tiếng Anh (`en`) |
|---|---|---|
| **Tên sản phẩm** | **Where Money Sleeps** | **Where Money Sleeps** |
| **Tagline bắt buộc (`T1`)** | *"Từ tin báo “ghi có” tới sổ sách ngân hàng: tiền của bạn đi qua những đâu."* | *"From the bank alert to the ledger: where your money actually goes."* |
| **Cảm giác cốt lõi** | *"À, hoá ra tiền của mình đi như thế."* | *"Aha — so that is where my money actually goes."* |
| **Định danh thể loại** | Tạp chí tương tác & Mặt cắt kiến trúc dòng tiền (`Interactive Financial Cutaway Atlas`) | Interactive Financial Cutaway & Money-Flow Atlas |

## 2. Công Thức Tiêu Đề 3 Điểm Neo & Danh Sách 6 Video Khởi Đầu Trên `@WhereMoneySleeps`

Theo quy tắc học được (`VOICE-AND-PROSODY-SPEC.md` & `QĐ 56`), mọi tiêu đề bài viết và video phát hành trên kênh `@WhereMoneySleeps` tuân thủ nghiêm ngặt công thức **3 điểm neo ngữ cảnh tự thân**:
`[1. Hành động + Giá trị gốc] → [2. Cơ chế / Lãi suất bề mặt] → [3. Sự thật hệ thống / Số thực nhận]`

| Bài mẫu (`storyId`) | Tiêu đề chuẩn 3 điểm neo | Link YouTube Dài (`16:9` `v6.5`) | Link YouTube Shorts (`9:16` `v6.5`) |
|---|---|---|---|
| **`card`** (Danh mục 02 · Thẻ & QR) | **Quẹt thẻ 10 triệu lúc 22:47 báo thành công và hoàn tiền 100 nghìn: Vì sao hai ngày sau quán mới thực nhận 9,78 triệu?** | [`https://youtu.be/fxpFvVJcpRA`](https://youtu.be/fxpFvVJcpRA) (`unlisted`) | [`https://youtu.be/th6zR4gwV5c`](https://youtu.be/th6zR4gwV5c) (`unlisted`) |
| **`pay`** (Danh mục 01 · Ngân hàng & Bảng lương) | **Lương gộp 17 triệu thực nhận 15 triệu báo ghi có: Vì sao không một đồng tiền mặt nào rời toà nhà ngân hàng mà vẫn sinh lời qua đêm?** | [`https://youtu.be/3NqEha4j53k`](https://youtu.be/3NqEha4j53k) (`unlisted`) | [`https://youtu.be/XnMsbH0E_xo`](https://youtu.be/XnMsbH0E_xo) (`unlisted`) |
| **`install`** (Danh mục 03 · Tín dụng & Trả góp) | **Mua điện thoại 12 triệu trả góp lãi suất 0%: Vì sao cửa hàng chỉ thực nhận 11,4 triệu và lãi suất thực tế là 10%/năm?** | [`https://youtu.be/l_8aVo538jo`](https://youtu.be/l_8aVo538jo) (`unlisted`) | [`https://youtu.be/J3DmDP4KKRI`](https://youtu.be/J3DmDP4KKRI) (`unlisted`) |

## 3. Chuẩn Metadata Kênh YouTube `@WhereMoneySleeps` & Thẻ Chia Sẻ (`B1–B4`)

- **Không tên riêng thương mại (`Zero Proper Noun` — `B1–B4`):** Tuyệt đối không dùng tên ngân hàng thương mại, mạng thẻ, ví điện tử, chuỗi cửa hàng hay công cụ AI hậu trường trong tiêu đề, mô tả, thẻ tag hay khung hình thu nhỏ (`thumbnail`).
- **Nhãn minh bạch nội dung tổng hợp (`YouTube API`):** Mọi video tải lên qua `scripts/wms-media-pipeline.py` đặt `containsSyntheticMedia: true`, `selfDeclaredMadeForKids: false`, `categoryId: "27"` (`Education`), `defaultLanguage: "vi"`, kèm phụ đề `.srt` chuẩn và danh sách mốc chương (`chaptersText`) tự động.
- **Thẻ OpenGraph / Chia sẻ mạng xã hội (`<meta property="og:*">`):**
  - `og:title`: `Where Money Sleeps — Từ tin báo “ghi có” tới sổ sách ngân hàng: tiền của bạn đi qua những đâu.`
  - `og:description`: `Giải phẫu đường đi thật sự của đồng tiền qua mặt cắt kiến trúc 5 ngôi nhà, sổ kế toán Thông tư 99/2025 và video giải thích trực quan. Tiến độ lưu 100% trên máy của bạn.`

## 4. Chưa xác minh được

- Tỷ lệ nhấp (`CTR`) và thời lượng xem trung bình (`AVD`) thực tế trên YouTube Analytics sau khi Duy chuyển 6 video từ `unlisted` sang `public` (sẽ tổng hợp ở cổng `S6 Iterate`).
- Same vendor, same priors — no external verifier ran.
