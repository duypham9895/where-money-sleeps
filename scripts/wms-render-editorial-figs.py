#!/usr/bin/env python3
"""
wms-render-editorial-figs.py — Bộ dựng 12 Hình Minh Hoạ Biên Tập (Inline Editorial Figures 16:9 · 1200×675)
cho 3 bài khảo cứu trong `where-money-sleeps/docs/prototype.html`.

Áp dụng kết quả nghiên cứu 4 pha (SWEEP → DEDUPE → REFUTE → JUDGE):
1. Mayer's Spatial Contiguity & Advance Organizer (1979, 2001):
   - Đặt ngay sau đoạn dẫn nhập (Paragraph 1) của các chương có Element Interactivity cao (Chương 02–05).
2. Chandler & Sweller (1991) & Florax & Ploetzner (2010) — Zero Split-Attention:
   - Khung 16:9 (1200×675) chia 2 vùng rõ ràng, không chồng lấn:
     * Vùng Trái (x=24..684, y=24..651): Mặt cắt kiến trúc Risograph Đêm (0 cột điện, 0 ống ngầm) + Nhãn dán trực tiếp (Direct Callout Pills).
     * Vùng Phải (x=704..1176, y=24..651): Bảng Giải Phẫu Cơ Chế (5 ngôi nhà 2 dòng + 3 tầng Dòng chảy / Bút toán / Tỷ lệ bảo toàn dòng tiền).
3. Brand Safety (B1–B4) & LUẬT 6b (Parent-Child Containment) & LUẬT 7 (Zero Pipe/Wire Jargon).
"""

from __future__ import annotations

import pathlib
import re
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path("/Users/edwardpham/Documents/Programming/Vibe/where-money-sleeps")
BRAND_DIR = ROOT / "public/brand"
BRAIN_DIR = pathlib.Path("/Users/edwardpham/.gemini/antigravity/brain/7f8bd653-2dd3-4155-8d12-ef6b38dd6a6e")

W, H = 1200, 675
LEFT_BOX = (24, 24, 684, 651)
RIGHT_BOX = (704, 24, 1176, 651)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
        ]
    )
    for c in candidates:
        p = pathlib.Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


CARD_HOUSES = [
    ("BẠN", "Người mua"),
    ("QUÁN QUEN", "Nơi ăn uống"),
    ("NGÂN HÀNG", "Của quán"),
    ("TỔ CHỨC", "Chuyển mạch"),
    ("NGÂN HÀNG", "Của bạn"),
]

PAY_HOUSES = [
    ("CÔNG TY", "Trả lương"),
    ("NGÂN HÀNG", "Trả lương"),
    ("BẠN", "Người nhận"),
    ("500 NGƯỜI", "Đồng nghiệp"),
    ("KHỐI VAY", "Ngân hàng"),
]

INSTALL_HOUSES = [
    ("BẠN", "Người mua"),
    ("CỬA HÀNG", "Nơi bán máy"),
    ("CÔNG TY", "Tài chính"),
    ("NGÂN HÀNG", "Của bạn"),
    ("NGÂN HÀNG", "Cửa hàng"),
]

FIGURES_SPEC: dict[str, list[dict]] = {
    "card": [
        {
            "out": "card-fig-1.jpg",
            "plate": "public/brand/card-short-plate-1.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  GIẢI PHẪU BA TẦNG XỬ LÝ",
            "title": "Quẹt thẻ 10 triệu lúc 22:47: Lời nhắn chạy ngay, tiền thật chờ T+2",
            "houses": CARD_HOUSES,
            "active_houses": {0, 1, 3, 4},
            "left_pills": [
                (354, 72, "NGÂN HÀNG CỦA BẠN: GIỮ CHỖ HẠN MỨC 10.000.000 Đ", "amber"),
                (354, 598, "QUẦY QUÁN QUEN: KÉT TIỀN VẪN TRỐNG · GHI PHẢI THU 1388", "teal"),
            ],
            "steps": [
                ("1. Luồng thông tin (Vài giây)", "Máy quẹt thẻ → Ngân hàng quán → Tổ chức thẻ → Ngân hàng bạn: xác nhận “đồng ý”, 0 đồng di chuyển.", "amber"),
                ("2. Sổ kế toán (Đêm đó)", "Quán ghi Nợ TK 1388 / Có TK 511: 10.000.000 đ (giữ lời hứa của ngân hàng quán, chưa có tiền).", "clay"),
                ("3. Quyết toán tiền thật (T+2)", "Ngân hàng bạn ứng 9.850.000 đ → Ngân hàng quán trả quán 9.780.000 đ sau hai ngày làm việc.", "green"),
            ],
            "footer_eq": "Đêm đầu tiên: 10.000.000 đ nằm trong dòng sổ phải thu, chưa vào tài khoản quán",
        },
        {
            "out": "card-fig-2.jpg",
            "plate": "public/brand/card-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  ĐỔI CHÁC GIỮA 5 NGÔI NHÀ",
            "title": "Vì sao quán chấp nhận mất 220.000 đ phí nhận thẻ trên hoá đơn 10 triệu?",
            "houses": CARD_HOUSES,
            "active_houses": {1, 2, 3, 4},
            "left_pills": [
                (354, 72, "NGÂN HÀNG PHÁT HÀNH: ỨNG TIỀN TRƯỚC & CHỊU RỦI RO TÍN DỤNG", "amber"),
                (354, 598, "QUÁN QUEN THỰC NHẬN: +9.780.000 Đ (ĐỔI LẤY KHÁCH QUẸT THẺ)", "green"),
            ],
            "steps": [
                ("Quán quen (Người bán)", "Chịu phí MDR 2,2% (220.000 đ) và chờ T+2 để không mất khách thanh toán không tiền mặt.", "amber"),
                ("Ngân hàng của bạn (Issuer)", "Ứng 9.850.000 đ trước cho quán và chịu rủi ro bạn trả chậm; nhận về 150.000 đ phí Interchange.", "green"),
                ("Tổ chức thẻ & NH của quán", "Giữ luật chơi đối chiếu liên ngân hàng và bảo lãnh thanh toán; nhận 10.000 đ + 60.000 đ.", "clay"),
            ],
            "footer_eq": "Hoá đơn 10.000.000 đ  =  9.780.000 đ (Quán)  +  220.000 đ (Phí dịch vụ 3 bên)",
        },
        {
            "out": "card-fig-3.jpg",
            "plate": "public/brand/card-short-plate-4.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  GIẢI PHẪU 220.000 Đ & TIỀN HOÀN",
            "title": "Chia 220.000 đ phí nhận thẻ: Nguồn tiền hoàn 100.000 đ đi từ đâu?",
            "houses": CARD_HOUSES,
            "active_houses": {0, 1, 4},
            "left_pills": [
                (354, 72, "PHÍ INTERCHANGE 150.000 Đ → TRÍCH TRẢ TIỀN HOÀN 100.000 Đ", "amber"),
                (354, 598, "GIÁ MÓN ĂN CHUNG: NGƯỜI TRẢ TIỀN MẶT CŨNG GÓP PHÍ QUẸT THẺ", "green"),
            ],
            "steps": [
                ("Khúc 1 · 150.000 đ (1,5%)", "Về Ngân hàng của bạn (Interchange) — nguồn chính để chi 100.000 đ tiền hoàn (Cashback 1%).", "amber"),
                ("Khúc 2 · 60.000 đ + 10.000 đ", "Ngân hàng của quán giữ 60.000 đ vận hành POS; Tổ chức thẻ thu 10.000 đ phí mạng lưới.", "clay"),
                ("Khúc 3 · Ẩn trong giá bán", "Quán đưa phí 2,2% vào giá thực đơn: tiền hoàn rất có thể là tiền của chính bạn đi một vòng.", "green"),
            ],
            "footer_eq": "220.000 đ MDR  =  150.000 đ (Interchange)  +  60.000 đ (Acquirer)  +  10.000 đ (Scheme)",
        },
        {
            "out": "card-fig-4.jpg",
            "plate": "public/brand/card-short-plate-3.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  HUỶ · HOÀN · KHIẾU NẠI",
            "title": "Huỷ trong ca (Reversal), Hoàn tiền (Refund) và Khiếu nại (Chargeback)",
            "houses": CARD_HOUSES,
            "active_houses": {0, 1, 2, 3, 4},
            "left_pills": [
                (354, 72, "TRƯỚC ĐỐI CHIẾU CUỐI NGÀY: HUỶ LỆNH GIỮ CHỖ · 0 ĐỒNG CHẠY", "amber"),
                (354, 598, "SAU QUYẾT TOÁN: TIỀN THẬT PHẢI CHẠY NGƯỢC QUA NGÂN HÀNG", "teal"),
            ],
            "steps": [
                ("1. Reversal (Huỷ ngay trong ca)", "Quán khởi xướng trước khi gửi danh sách Clearing: nhả lệnh giữ chỗ, không có tiền di chuyển.", "amber"),
                ("2. Refund (Quán hoàn tiền)", "Quán khởi xướng sau khi đã đối chiếu: tạo giao dịch ngược, tiền hoàn về ở kỳ quyết toán sau.", "green"),
                ("3. Chargeback (Chủ thẻ khiếu nại)", "Bạn khởi xướng qua Ngân hàng phát hành: Ngân hàng quán tạm trừ tiền quán chờ phân xử.", "clay"),
            ],
            "footer_eq": "Chỉ có Reversal (trước Clearing) là 0 đồng chạy; Refund & Chargeback đều đổi dòng tiền thật",
        },
    ],
    "pay": [
        {
            "out": "pay-fig-1.jpg",
            "plate": "public/brand/pay-short-plate-1.jpg",
            "crop": (0, 240, 768, 1180),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  LƯƠNG VỀ CÙNG NGÂN HÀNG",
            "title": "Lương thực lĩnh 15 triệu báo ghi có: Vì sao không đồng tiền nào rời toà nhà?",
            "houses": PAY_HOUSES,
            "active_houses": {0, 1, 2},
            "left_pills": [
                (354, 72, "SỔ CÁI NGÂN HÀNG: SỬA 2 DÒNG NỢ PHẢI TRẢ · TỔNG VỐN KHÔNG ĐỔI", "amber"),
                (354, 598, "KÉT TIỀN NGẦM: 0 ĐỒNG DI CHUYỂN TRONG GIAO DỊCH NỘI BỘ (ON-US)", "green"),
            ],
            "steps": [
                ("1. Sổ Công ty (Lương gộp 17tr)", "Giữ lại 2.000.000 đ (bảo hiểm + thuế ví dụ) nộp thay; gửi file lệnh chi 15.000.000 đ.", "clay"),
                ("2. Giao dịch On-Us (Cùng NH)", "Ngân hàng bớt khoản nợ Công ty (−15 triệu), tăng khoản nợ Bạn (+15 triệu) trên cùng cuốn sổ.", "amber"),
                ("3. Giao dịch Off-Us (Khác NH)", "Chỉ khi bạn dùng ngân hàng khác, tiền thật mới quyết toán qua kênh liên ngân hàng.", "green"),
            ],
            "footer_eq": "Tin nhắn “Ghi có +15.000.000 đ” = Ngân hàng ghi tăng khoản nợ phải trả cho chính bạn",
        },
        {
            "out": "pay-fig-2.jpg",
            "plate": "public/brand/pay-short-plate-2.jpg",
            "crop": (0, 220, 768, 1180),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  BỂ VỐN KHÔNG KỲ HẠN (CASA)",
            "title": "500 đồng nghiệp cùng để yên 5 triệu: Ngân hàng có ngay 2,5 tỷ đồng vốn rẻ",
            "houses": PAY_HOUSES,
            "active_houses": {1, 2, 3},
            "left_pills": [
                (354, 72, "500 TÀI KHOẢN NHẬN LƯƠNG: HIẾM KHI RÚT SẠCH CÙNG MỘT LÚC", "amber"),
                (354, 598, "BỂ VỐN GỘP 2,5 TỶ ĐỒNG: LÃI KHÔNG KỲ HẠN ~0,1%/NĂM (VÍ DỤ)", "green"),
            ],
            "steps": [
                ("Một cá nhân (10 triệu nằm yên)", "Ở lãi suất không kỳ hạn ví dụ 0,1%/năm, cả năm chỉ sinh ra khoảng 10.000 đ tiền lãi.", "amber"),
                ("Cả bảng lương (500 người × 5tr)", "Tạo thành mức nền ổn định 2,5 tỷ đồng; ngân hàng chỉ trả ~2,5 triệu đồng lãi mỗi năm.", "green"),
                ("So với huy động kỳ hạn 5%/năm", "Huy động 2,5 tỷ đồng có kỳ hạn tốn 125 triệu/năm — đắt gấp 50 lần nguồn CASA bảng lương.", "clay"),
            ],
            "footer_eq": "500 × 5.000.000 đ = 2,5 tỷ đ CASA (~2,5 triệu lãi/năm vs 125 triệu nếu huy động 5%/năm)",
        },
        {
            "out": "pay-fig-3.jpg",
            "plate": "public/brand/pay-short-plate-3.jpg",
            "crop": (0, 220, 768, 1180),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  GIÁ VỐN NỘI BỘ (FTP) & MẶC CẢ",
            "title": "Ba bên cùng hưởng lợi từ một bảng lương: Công ty, Huy động và Cho vay",
            "houses": PAY_HOUSES,
            "active_houses": {0, 1, 4},
            "left_pills": [
                (354, 72, "GIÁ MUA BÁN VỐN NỘI BỘ (FTP): GHI CÔNG CHO KHỐI HUY ĐỘNG", "amber"),
                (354, 598, "ĐỔI BẢNG LƯƠNG LẤY ƯU ĐÃI DOANH NGHIỆP (PHÍ & LÃI VAY)", "teal"),
            ],
            "steps": [
                ("Công ty trả lương", "Đối soát gọn trên một sao kê, giảm lỗi chuyển khoản và có vị thế đàm phán ưu đãi phí/lãi vay.", "amber"),
                ("Khối Huy động (Ngân hàng)", "Trả khách 0,1%/năm, bán vốn nội bộ qua FTP (ví dụ 4,5%/năm) → được ghi công 4,4 điểm %.", "green"),
                ("Khối Cho vay (Ngân hàng)", "Mua vốn nội bộ ở mức 6,0%/năm, cho vay mua nhà ~8,5%/năm → hưởng biên 2,5 điểm %.", "clay"),
            ],
            "footer_eq": "Biên lãi 8,4% (8,5% − 0,1%) = 4,4% (Huy động) + 1,5% (Quản lý vốn) + 2,5% (Cho vay)",
        },
        {
            "out": "pay-fig-4.jpg",
            "plate": "public/brand/pay-short-plate-4.jpg",
            "crop": (0, 220, 768, 1180),
            "badge": "HÌNH 04  ·  CHƯƠNG 05–06  ·  DỰ TRỮ & RỦI RO RÚT VỐN",
            "title": "Vì sao ngân hàng không thể đem 100% tiền lương nằm yên đi cho vay?",
            "houses": PAY_HOUSES,
            "active_houses": {0, 1, 2, 3, 4},
            "left_pills": [
                (354, 72, "SỔ KẾ TOÁN: SỐ DƯ CỦA BẠN LÀ KHOẢN NGÂN HÀNG ĐANG NỢ BẠN", "amber"),
                (354, 598, "DỰ TRỮ BẮT BUỘC & CHI PHÍ VẬN HÀNH GIỮ LẠI MỘT PHẦN VỐN", "green"),
            ],
            "steps": [
                ("Dự trữ bắt buộc (Ví dụ 3%)", "Trên 2,5 tỷ đồng CASA, 75 triệu phải nằm tại Ngân hàng Trung ương, chỉ 2,425 tỷ được cho vay.", "amber"),
                ("Chi phí ẩn của người nhận lương", "Không ai thu phí trực tiếp, nhưng phần lãi bạn bỏ lỡ trên số dư nằm yên chính là đóng góp của bạn.", "clay"),
                ("Rủi ro lớn nhất của ngân hàng", "Công ty chuyển bảng lương sang ngân hàng khác → cả bể CASA 2,5 tỷ đồng rút đi cùng lúc.", "green"),
            ],
            "footer_eq": "Gửi tiền không phải là cất hộ trong tủ khoá — bạn đang là chủ nợ không kỳ hạn của ngân hàng",
        },
    ],
    "install": [
        {
            "out": "install-fig-1.jpg",
            "plate": "public/brand/install-short-plate-2.jpg",
            "crop": (0, 360, 1080, 1460),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  CHUYỂN GIAO HỢP ĐỒNG VAY",
            "title": "Ký trả góp 0% cho máy 12 triệu: Chủ nợ của bạn là Công ty tài chính",
            "houses": INSTALL_HOUSES,
            "active_houses": {0, 1, 2},
            "left_pills": [
                (354, 72, "CÔNG TY TÀI CHÍNH: DUYỆT HỒ SƠ & NHẬN HỢP ĐỒNG VAY 12.000.000 Đ", "amber"),
                (354, 598, "QUẦY CỬA HÀNG: GIAO MÁY · GHI PHẢI THU TK 1388 (CHƯA CÓ TIỀN)", "teal"),
            ],
            "steps": [
                ("Bước 1–2 · Hồ sơ & Hợp đồng", "Hồ sơ gửi từ Cửa hàng về Công ty tài chính; hợp đồng vay 12 kỳ ký thẳng giữa bạn và họ.", "amber"),
                ("Bước 3 · Đêm đóng sổ (TK 1388)", "Cửa hàng ghi Nợ TK 1388 / Có TK 511 (12.000.000 đ) — phải thu từ Công ty tài chính.", "clay"),
                ("Bước 4–5 · Giải ngân & 12 kỳ trả", "Hôm sau (T+1) cửa hàng nhận 11.400.000 đ; 12 tháng tới bạn trả 1.000.000 đ/tháng.", "green"),
            ],
            "footer_eq": "Từ giây bấm duyệt: Bạn nợ Công ty tài chính 12.000.000 đ, không nợ Cửa hàng bán máy",
        },
        {
            "out": "install-fig-2.jpg",
            "plate": "public/brand/card-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  GIẢI NGÂN HỤT 600.000 Đ (5%)",
            "title": "Bán máy 12 triệu nhưng cửa hàng chỉ thực nhận 11,4 triệu: 600.000 đ đi đâu?",
            "houses": INSTALL_HOUSES,
            "active_houses": {1, 2, 4},
            "left_pills": [
                (354, 72, "CÔNG TY TÀI CHÍNH GIỮ LẠI 600.000 Đ (5% HỖ TRỢ LÃI SUẤT)", "amber"),
                (354, 598, "CỬA HÀNG THỰC NHẬN QUA NGÂN HÀNG: +11.400.000 Đ (Ở T+1)", "green"),
            ],
            "steps": [
                ("Cửa hàng (Người bán)", "Đổi 600.000 đ (5% giá bán) lấy việc chốt đơn ngay, tiền về sau 1 ngày và thoát rủi ro đòi nợ.", "green"),
                ("Công ty tài chính (Bên cho vay)", "Chi 11.400.000 đ hôm nay, thu về 12.000.000 đ trong 12 tháng → thu trước 600.000 đ tiền lãi.", "amber"),
                ("Hạch toán sổ Cửa hàng", "Nợ TK 112 (11.400.000 đ) + Nợ TK 641/521 (600.000 đ) / Có TK 1388 (12.000.000 đ).", "clay"),
            ],
            "footer_eq": "12.000.000 đ (Giá ghi bán)  −  600.000 đ (Hỗ trợ lãi suất)  =  11.400.000 đ (Thực nhận)",
        },
        {
            "out": "install-fig-3.jpg",
            "plate": "public/brand/install-short-plate-4.jpg",
            "crop": (0, 820, 768, 1376),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  KHI TIỀN LÃI ĐỔI CHỖ ĐỨNG",
            "title": "Trả góp 12 triệu so với trả thẳng 11,4 triệu: Lãi suất thực tế (EIR) ~10%/năm",
            "houses": INSTALL_HOUSES,
            "active_houses": {0, 1, 2, 3},
            "left_pills": [
                (354, 72, "TRẢ THẲNG ĐƯỢC GIẢM 600K? → BẠN ĐANG TRẢ LÃI ~0,8%/THÁNG", "amber"),
                (354, 598, "TRẢ THẲNG & TRẢ GÓP MỘT GIÁ? → CỬA HÀNG HOẶC GIÁ BÁN GÁNH 600K", "green"),
            ],
            "steps": [
                ("Kịch bản A · Trả thẳng giảm 600.000 đ", "Bạn nhận máy đáng 11,4 triệu, trả 12 kỳ × 1 triệu → EIR ≈ 0,80%/tháng (~10,0%/năm lãi kép).", "amber"),
                ("Kịch bản B · Một giá 12.000.000 đ", "Cửa hàng tự bớt lãi gộp 600.000 đ, hoặc đã cộng sẵn vào giá niêm yết của mọi người mua.", "green"),
                ("Biến thể · Trả góp qua thẻ tín dụng", "Nếu chủ thẻ chịu phí chuyển đổi 3% (360.000 đ), EIR riêng phần phí là ≈ 0,47%/tháng (~5,8%/năm).", "clay"),
            ],
            "footer_eq": "Công thức gốc: 11.400.000 = Tổng 12 kỳ [1.000.000 / (1 + r)^t] → r ≈ 0,80%/tháng",
        },
        {
            "out": "install-fig-4.jpg",
            "plate": "public/brand/install-short-plate-1.jpg",
            "crop": (0, 360, 768, 1260),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  TẤT TOÁN SỚM & TRẢ MÁY",
            "title": "Vì sao trả hết sớm ở tháng thứ 4 không được bớt đồng lãi nào?",
            "houses": INSTALL_HOUSES,
            "active_houses": {0, 1, 2},
            "left_pills": [
                (354, 72, "TẤT TOÁN SỚM THÁNG 4: DƯ NỢ CÒN NGUYÊN 8 KỲ = 8.000.000 Đ", "amber"),
                (354, 598, "TRẢ LẠI MÁY: PHẢI HUỶ HỢP ĐỒNG VAY VỚI CÔNG TY TÀI CHÍNH", "teal"),
            ],
            "steps": [
                ("1. Tất toán sớm (Cuối tháng 4)", "Hợp đồng ghi lãi 0% nên 8 kỳ còn lại vẫn là 8.000.000 đ; 600k dồn vào 4 tháng làm EIR vọt lên ~1,48%/tháng.", "amber"),
                ("2. Trễ hạn 1 kỳ (Phạt 150.000 đ)", "Công ty tài chính thu phí phạt và ghi lịch sử tín dụng; EIR tăng lên ~0,98%/tháng (~12,4%/năm).", "clay"),
                ("3. Khách trả lại chiếc điện thoại", "Cửa hàng nhận máy và hoàn 11,4 triệu; chỉ Công ty tài chính mới xoá được hợp đồng vay của bạn.", "green"),
            ],
            "footer_eq": "Câu hỏi duy nhất trước khi ký trả góp 0%: “Nếu trả thẳng một lần thì giá bao nhiêu?”",
        },
    ],
}

COLORS = {
    "amber": ((245, 166, 35, 240), (255, 214, 112, 255), (28, 22, 12, 255)),
    "green": ((72, 187, 120, 238), (154, 240, 180, 255), (12, 28, 18, 255)),
    "teal": ((64, 185, 175, 238), (168, 245, 238, 255), (12, 28, 28, 255)),
    "clay": ((214, 106, 76, 238), (250, 188, 168, 255), (28, 14, 12, 255)),
}

SLATE_LEAK_RE = re.compile(
    r"(\bCẢNH\s*\d|\bSCENE\s*\d|\bÝ\s*\d+\s*/\s*\d+|Chữ\s+to|SFX\s*gợi\s*ý|dây\s+điện|dây\s+tín\s+hiệu|ống\s+ngầm|ống\s+quyết\s+toán|[⇒Σ])",
    re.IGNORECASE,
)


def render_one_figure(spec: dict, fonts: dict[str, ImageFont.FreeTypeFont]) -> Image.Image:
    canvas = Image.new("RGBA", (W, H), (11, 15, 24, 255))
    draw = ImageDraw.Draw(canvas)

    # Outer frame border
    draw.rounded_rectangle((6, 6, W - 7, H - 7), radius=18, fill=(14, 19, 30, 255), outline=(245, 166, 35, 140), width=2)

    # 1. Left Pane: Architectural Cutaway Plate + Direct Callout Pills
    lx0, ly0, lx1, ly1 = LEFT_BOX
    lw, lh = lx1 - lx0, ly1 - ly0
    plate_img = Image.open(ROOT / spec["plate"]).convert("RGBA")
    cropped = plate_img.crop(spec["crop"]).resize((lw, lh), Image.Resampling.LANCZOS)

    # Subtle top/bottom vignette on left plate so direct callout pills have 100% contrast
    vig = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vig)
    for y in range(110):
        a = int(175 * (1.0 - y / 110.0) ** 1.5)
        vdraw.line([(0, y), (lw, y)], fill=(9, 13, 22, a))
    for y in range(lh - 110, lh):
        u = (y - (lh - 110)) / 110.0
        a = int(185 * (u ** 1.5))
        vdraw.line([(0, y), (lw, y)], fill=(9, 13, 22, a))
    cropped = Image.alpha_composite(cropped, vig)

    mask = Image.new("L", (lw, lh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, lw - 1, lh - 1), radius=14, fill=255)
    canvas.paste(cropped, (lx0, ly0), mask)
    draw.rounded_rectangle(LEFT_BOX, radius=14, fill=None, outline=(245, 166, 35, 165), width=2)

    # Draw left pills (LUẬT 6b checked against LEFT_BOX)
    for cx, cy, ptxt, pcol in spec["left_pills"]:
        if SLATE_LEAK_RE.search(ptxt):
            raise RuntimeError(f"Forbidden jargon/glyph in pill: {ptxt}")
        tw = draw.textlength(ptxt, font=fonts["pill"])
        pw = tw + 28
        ph = 34
        if pw > lw - 24:
            raise RuntimeError(f"Left pill overflow: {pw} > {lw - 24} ({ptxt})")
        px0 = max(lx0 + 12, min(lx1 - 12 - pw, cx - pw / 2))
        py0 = max(ly0 + 12, min(ly1 - 12 - ph, cy - ph / 2))
        outline_c, text_c, _ = COLORS[pcol]
        draw.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=9, fill=(13, 18, 29, 236), outline=outline_c, width=2)
        draw.text((px0 + 14, py0 + 8), ptxt, font=fonts["pill"], fill=text_c)

    # 2. Right Pane: Editorial Blueprint & Mechanism Breakdown
    rx0, ry0, rx1, ry1 = RIGHT_BOX
    rw = rx1 - rx0
    draw.rounded_rectangle(RIGHT_BOX, radius=14, fill=(17, 23, 36, 255), outline=(82, 102, 134, 150), width=2)

    pad_x = 22
    inner_w = rw - 2 * pad_x
    cur_y = ry0 + 20

    # Kicker badge
    btxt = spec["badge"]
    bw = draw.textlength(btxt, font=fonts["badge"]) + 22
    if bw > inner_w:
        raise RuntimeError(f"Badge overflow: {btxt}")
    draw.rounded_rectangle((rx0 + pad_x, cur_y, rx0 + pad_x + bw, cur_y + 28), radius=6, fill=(245, 166, 35, 245))
    draw.text((rx0 + pad_x + 11, cur_y + 6), btxt, font=fonts["badge"], fill=(14, 19, 30, 255))
    cur_y += 38

    # Title (wrapped cleanly within inner_w)
    t_lines = wrap_text(draw, spec["title"], fonts["title"], inner_w)
    for ln in t_lines:
        draw.text((rx0 + pad_x, cur_y), ln, font=fonts["title"], fill=(246, 241, 230, 255))
        cur_y += 28
    cur_y += 8

    # 5-House Mini Strip (2-line labels, computed deterministically from inner_w per LUẬT 6b)
    houses = spec["houses"]
    n_h = len(houses)
    gap_h = 6
    h_bw = (inner_w - gap_h * (n_h - 1)) / n_h
    h_bh = 44
    for i, (l1, l2) in enumerate(houses):
        hx0 = rx0 + pad_x + i * (h_bw + gap_h)
        hx1 = hx0 + h_bw
        if hx0 < rx0 + pad_x - 1 or hx1 > rx1 - pad_x + 1:
            raise RuntimeError("House box containment violation")
        tw1 = draw.textlength(l1, font=fonts["house_top"])
        tw2 = draw.textlength(l2, font=fonts["house_sub"])
        if tw1 > h_bw - 8 or tw2 > h_bw - 8:
            raise RuntimeError(f"House text overflow: '{l1}' / '{l2}' ({max(tw1, tw2):.1f} > {h_bw - 8:.1f})")
        is_act = i in spec["active_houses"]
        fill_c = (245, 166, 35, 245) if is_act else (25, 34, 52, 230)
        out_c = (255, 224, 138, 255) if is_act else (78, 96, 124, 190)
        top_c = (14, 19, 30, 255) if is_act else (228, 236, 246, 240)
        sub_c = (28, 36, 54, 240) if is_act else (162, 176, 198, 225)
        draw.rounded_rectangle((hx0, cur_y, hx1, cur_y + h_bh), radius=8, fill=fill_c, outline=out_c, width=2)
        draw.text(((hx0 + hx1 - tw1) / 2, cur_y + 7), l1, font=fonts["house_top"], fill=top_c)
        draw.text(((hx0 + hx1 - tw2) / 2, cur_y + 23), l2, font=fonts["house_sub"], fill=sub_c)
    cur_y += h_bh + 12

    draw.line([(rx0 + pad_x, cur_y), (rx1 - pad_x, cur_y)], fill=(78, 96, 124, 120), width=1)
    cur_y += 12

    # 3 Mechanism Cards
    for s_head, s_body, s_col in spec["steps"]:
        if SLATE_LEAK_RE.search(s_head) or SLATE_LEAK_RE.search(s_body):
            raise RuntimeError(f"Forbidden jargon/glyph in step: {s_head} / {s_body}")
        outline_c, text_c, _ = COLORS[s_col]
        b_lines = wrap_text(draw, s_body, fonts["body"], inner_w - 28)
        card_h = 34 + len(b_lines) * 21 + 10
        draw.rounded_rectangle(
            (rx0 + pad_x, cur_y, rx1 - pad_x, cur_y + card_h),
            radius=10,
            fill=(12, 17, 27, 235),
            outline=outline_c,
            width=2,
        )
        draw.text((rx0 + pad_x + 14, cur_y + 9), s_head, font=fonts["step_head"], fill=text_c)
        by = cur_y + 32
        for bln in b_lines:
            draw.text((rx0 + pad_x + 14, by), bln, font=fonts["body"], fill=(228, 234, 242, 255))
            by += 21
        cur_y += card_h + 10

    # Bottom Equation / Takeaway Bar anchored inside RIGHT_BOX
    if SLATE_LEAK_RE.search(spec["footer_eq"]):
        raise RuntimeError(f"Forbidden jargon/glyph in footer_eq: {spec['footer_eq']}")
    eq_lines = wrap_text(draw, spec["footer_eq"], fonts["eq"], inner_w - 24)
    eq_h = len(eq_lines) * 20 + 18
    eq_y0 = max(cur_y + 2, ry1 - 16 - eq_h)
    if eq_y0 + eq_h > ry1 - 10:
        raise RuntimeError(f"Vertical overflow in right box for {spec['out']}: {eq_y0 + eq_h} > {ry1 - 10}")
    draw.rounded_rectangle(
        (rx0 + pad_x, eq_y0, rx1 - pad_x, eq_y0 + eq_h),
        radius=9,
        fill=(28, 36, 54, 245),
        outline=(245, 166, 35, 195),
        width=1,
    )
    ey = eq_y0 + 9
    for eln in eq_lines:
        draw.text((rx0 + pad_x + 12, ey), eln, font=fonts["eq"], fill=(255, 214, 112, 255))
        ey += 20

    return canvas.convert("RGB")


def main() -> None:
    fonts = {
        "pill": get_font(15, bold=True),
        "badge": get_font(13, bold=True),
        "title": get_font(21, bold=True),
        "house_top": get_font(11, bold=True),
        "house_sub": get_font(10, bold=False),
        "step_head": get_font(15, bold=True),
        "body": get_font(14, bold=False),
        "eq": get_font(14, bold=True),
    }

    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    brain_brand = BRAIN_DIR / "public/brand"
    brain_brand.mkdir(parents=True, exist_ok=True)

    count = 0
    for story_slug, fig_list in FIGURES_SPEC.items():
        for spec in fig_list:
            img = render_one_figure(spec, fonts)
            out_path = BRAND_DIR / spec["out"]
            img.save(out_path, quality=92, optimize=True)
            shutil.copy2(out_path, brain_brand / spec["out"])
            shutil.copy2(out_path, BRAIN_DIR / spec["out"])
            count += 1
            print(f"[OK] Rendered {out_path.name} ({out_path.stat().st_size:,} bytes)")

    print(f"Done! Rendered {count} 16:9 Editorial Cutaway Figures.")


if __name__ == "__main__":
    main()
