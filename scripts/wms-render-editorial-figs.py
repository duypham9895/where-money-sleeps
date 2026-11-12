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

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "public/brand"
BRAIN_DIR = ROOT / ".cache/brain"

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

MINPAY_HOUSES = [
    ("BẠN", "Chủ thẻ"),
    ("CỬA HÀNG", "Nơi mua máy"),
    ("NGÂN HÀNG", "Cửa hàng"),
    ("NGÂN HÀNG", "Phát hành"),
    ("NGÂN HÀNG", "Tài khoản"),
]

QR_HOUSES = [
    ("BẠN", "Người mua"),
    ("QUÁN QUEN", "Cà phê"),
    ("NGÂN HÀNG", "Của bạn"),
    ("TỔ CHỨC", "Chuyển mạch"),
    ("NGÂN HÀNG", "Của quán"),
]

PROFITCASH_HOUSES = [
    ("KHO HÀNG", "Đầu vào"),
    ("CÔNG TY", "Lãi 2 tỷ"),
    ("KHÁCH SỈ", "Đối tác B2B"),
    ("NGÂN HÀNG", "Công ty"),
    ("NHÂN SỰ", "Đội ngũ"),
]

OFFUS_HOUSES = [
    ("BẠN", "20 triệu"),
    ("NGÂN HÀNG", "Của bạn"),
    ("TỔ CHỨC", "Chuyển mạch"),
    ("NGÂN HÀNG", "Người nhận"),
    ("NH TRUNG", "Ương"),
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
    "minpay": [
        {
            "out": "minpay-fig-1.jpg",
            "plate": "public/brand/card-short-plate-1.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  ĐIỀU KIỆN CỦA 45 NGÀY MIỄN LÃI",
            "title": "Quẹt thẻ 10 triệu ở Ngày 01: Ngân hàng đã ứng tiền thật cho cửa hàng từ Ngày T+2",
            "houses": MINPAY_HOUSES,
            "active_houses": {0, 1, 2, 3},
            "left_pills": [
                (354, 72, "NGÀY T+2: NGÂN HÀNG PHÁT HÀNH ĐÃ ỨNG TIỀN THẬT CHO CỬA HÀNG", "amber"),
                (354, 598, "45 NGÀY MIỄN LÃI: CHỈ HIỆU LỰC KHI TRẢ ĐỦ 100% DƯ NỢ SAO KÊ", "teal"),
            ],
            "steps": [
                ("1. Ngày 01 · Quẹt thẻ 10.000.000 đ", "Bạn nhận thiết bị ngay; ngân hàng phát hành giữ hạn mức 10.000.000 đ và mở kỳ sao kê.", "amber"),
                ("2. Ngày T+2 · Ngân hàng ứng tiền", "Ngân hàng phát hành chuyển tiền thật qua ngân hàng cửa hàng (cửa hàng nhận 9.800.000 đ sau phí 2%).", "green"),
                ("3. Ngày 30 · Chốt sao kê kỳ 1", "Sao kê báo dư nợ 10.000.000 đ, hạn thanh toán Ngày 45: trả đủ 10 triệu (lãi 0 đ) hoặc tối thiểu 500.000 đ.", "clay"),
            ],
            "footer_eq": "Ngân hàng đã bỏ tiền túi ứng trước từ Ngày T+2 — miễn lãi 45 ngày là ưu đãi có điều kiện",
        },
        {
            "out": "minpay-fig-2.jpg",
            "plate": "public/brand/card-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  TÍNH LÃI LÙI VỀ NGÀY 01",
            "title": "Trả tối thiểu 500.000 đ ở Ngày 45: Vì sao kỳ sau bị cộng tới 592.500 đ tiền lãi?",
            "houses": MINPAY_HOUSES,
            "active_houses": {0, 3, 4},
            "left_pills": [
                (354, 72, "KHÚC 1 (NGÀY 01–45): LÃI LÙI TRÊN CẢ 10.000.000 Đ = 450.000 Đ", "amber"),
                (354, 598, "KHÚC 2 (NGÀY 46–60): LÃI TRÊN 9.500.000 Đ CÒN LẠI = 142.500 Đ", "clay"),
            ],
            "steps": [
                ("Khúc 1 · 45 ngày đầu (10.000.000 đ)", "Do không trả đủ 100% ở Ngày 45, miễn lãi bị huỷ: 10.000.000 đ × 0,1%/ngày × 45 ngày = 450.000 đ.", "amber"),
                ("Khúc 2 · 15 ngày sau (9.500.000 đ)", "Sau khi trừ 500.000 đ, gốc còn 9.500.000 đ chịu tiếp 15 ngày: 9.500.000 đ × 0,1%/ngày × 15 ngày = 142.500 đ.", "clay"),
                ("Sao kê Ngày 60 · Dư nợ vọt lên", "Tổng lãi kỳ 2 là 450.000 + 142.500 = 592.500 đ; cộng gốc 9.500.000 đ thành 10.092.500 đ.", "green"),
            ],
            "footer_eq": "Trả 500.000 đ ở Ngày 45 nhưng chịu 592.500 đ tiền lãi ở Ngày 60 — dư nợ mới: 10.092.500 đ",
        },
        {
            "out": "minpay-fig-3.jpg",
            "plate": "public/brand/card-short-plate-4.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  ĐỔI PHÍ PHẠT LẤY TIỀN LÃI",
            "title": "500.000 đ trả tối thiểu giúp bạn mua được thứ gì — và đánh mất thứ gì?",
            "houses": MINPAY_HOUSES,
            "active_houses": {0, 3, 4},
            "left_pills": [
                (354, 72, "THỨ MUA ĐƯỢC: THOÁT PHÍ PHẠT TRỄ HẠN & GIỮ NHÓM TÍN DỤNG", "green"),
                (354, 598, "THỨ ĐÁNH MẤT: 45 NGÀY MIỄN LÃI & MIỄN LÃI GIAO DỊCH MỚI", "amber"),
            ],
            "steps": [
                ("1. Bảo vệ lịch sử tín dụng", "Trả đủ 5% (500.000 đ) trước hạn giúp bạn không bị phạt trễ hạn và không bị ghi nhận nợ quá hạn.", "green"),
                ("2. Chi phí thực của 15 ngày trì hoãn", "Trả 592.500 đ lãi để giữ lại 9.500.000 đ thêm 15 ngày tương đương chi phí vốn ~6,24% chỉ trong nửa tháng.", "amber"),
                ("3. Lây nhiễm sang giao dịch mới", "Khi thẻ còn dư nợ chuyển kỳ, mọi giao dịch quẹt mới ở kỳ sau đều bị tính lãi ngay từ ngày quẹt.", "clay"),
            ],
            "footer_eq": "Lãi danh nghĩa 36%/năm (3%/tháng) khi nhập gốc hàng tháng tương đương EIR ~42,6%/năm",
        },
        {
            "out": "minpay-fig-4.jpg",
            "plate": "public/brand/card-short-plate-3.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  BẪY LÃI NGÀY & KHÔI PHỤC",
            "title": "Vì sao thiếu 10.000 đ vẫn mất miễn lãi — và làm sao khôi phục lại 45 ngày ân hạn?",
            "houses": MINPAY_HOUSES,
            "active_houses": {0, 1, 2, 3, 4},
            "left_pills": [
                (354, 72, "TRẢ 9.990.000 Đ (THIẾU 10.000 Đ): VẪN MẤT TRẮNG 45 NGÀY MIỄN LÃI", "amber"),
                (354, 598, "TẤT TOÁN 100% SAO KÊ KỲ SAU: KHÔI PHỤC LẠI ĐỒNG HỒ MIỄN LÃI", "teal"),
            ],
            "steps": [
                ("1. Thiếu 10.000 đ trên sao kê 10 triệu", "Hệ thống vẫn huỷ miễn lãi 45 ngày đầu trên toàn bộ 10.000.000 đ (~450.000 đ tiền lãi lùi).", "amber"),
                ("2. Rút tiền mặt tại cây ATM", "Không có ngày miễn lãi nào: thu phí rút ~4% ngay lập tức và tính lãi ngày từ giây tiền rời máy.", "clay"),
                ("3. Cách cắt đứt vòng xoáy lãi ngày", "Tạm ngưng quẹt mới trên thẻ đang nợ và thanh toán dứt điểm 100% dư nợ sao kê (10.092.500 đ).", "green"),
            ],
            "footer_eq": "Chỉ khi dư nợ sao kê được trả đủ 100%, chiếc thẻ mới trở lại là công cụ miễn lãi 45 ngày",
        },
    ],
    "qr": [
        {
            "out": "qr-fig-1.jpg",
            "plate": "public/brand/card-short-plate-1.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  THANH TOÁN ĐẨY VS KÉO",
            "title": "Quét mã QR 50.000 đ (Push) vs Quẹt thẻ (Pull): Tiêu tiền CASA có sẵn nên không mất 2,2% phí",
            "houses": QR_HOUSES,
            "active_houses": {0, 1, 2},
            "left_pills": [
                (354, 72, "QUÉT MÃ QR: BẠN CHỦ ĐỘNG ĐẨY LỆNH TỪ SỐ DƯ CASA (0% PHÍ)", "green"),
                (354, 598, "QUẸT THẺ: MÁY POS KÉO TIỀN QUA 4 BÊN (CHỊU MDR 2,2%)", "amber"),
            ],
            "steps": [
                ("1. Bảng mã QR đứng yên (Thụ động)", "Bảng nhựa trên quầy chỉ chứa số tài khoản của quán, không phát lệnh đi vòng qua 4 bên như máy POS.", "teal"),
                ("2. Bạn chủ động đẩy lệnh (Push)", "Bạn xác thực sinh trắc học trên ứng dụng ngân hàng để trích thẳng 50.000 đ từ số dư CASA đang có sẵn.", "green"),
                ("3. Không ai ứng vốn vay 45 ngày", "Vì không có ngân hàng nào phải ứng vốn hay chịu rủi ro bùng nợ, quán không bị thu 2,2% phí MDR.", "amber"),
            ],
            "footer_eq": "Thanh toán đẩy (Push) trừ thẳng tiền CASA có sẵn — 0 đồng ứng vốn nên 0% phí MDR",
        },
        {
            "out": "qr-fig-2.jpg",
            "plate": "public/brand/card-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  GHI CÓ 3 GIÂY & BÙ TRỪ RÒNG",
            "title": "Ba giây trên mặt quầy và phiên bù trừ ròng (Net Settlement) giữa hai ngân hàng",
            "houses": QR_HOUSES,
            "active_houses": {0, 1, 2, 3, 4},
            "left_pills": [
                (354, 72, "GIÂY 03: BẢN TIN 24/7 BẢO CHỨNG · GHI CÓ NGAY +50.000 Đ", "green"),
                (354, 598, "CUỐI PHIÊN: HAI NGÂN HÀNG BÙ TRỪ RÒNG TẠI NGÂN HÀNG TRUNG ƯƠNG", "teal"),
            ],
            "steps": [
                ("1. Bản tin 24/7 có bảo chứng (3 giây)", "Ngân hàng bạn trừ 50.000 đ và gửi bản tin qua tổ chức chuyển mạch; ngân hàng quán ghi Có ngay cho quán.", "green"),
                ("2. Sổ của quán (TT 99/2025)", "Ghi Nợ TK 112 (Tiền gửi không kỳ hạn: 50.000 đ) / Có TK 511 (Doanh thu: 50.000 đ) ngay tại T+0.", "amber"),
                ("3. Quyết toán ròng cuối phiên", "Hàng triệu lệnh hai chiều được cộng bù trừ (ví dụ 100 tỷ − 96 tỷ = chỉ chuyển 4 tỷ phần chênh).", "clay"),
            ],
            "footer_eq": "Tách bản tin ghi Có tức thời (T+0) khỏi phiên quyết toán ròng liên ngân hàng tại NHTW",
        },
        {
            "out": "qr-fig-3.jpg",
            "plate": "public/brand/pay-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  ĐỔI PHÍ 0 Đ LẤY VỐN CASA",
            "title": "Vì sao ngân hàng chịu miễn phí 0 đồng? Để giữ tiền mặt nằm lại trong bể vốn CASA ~0,1%/năm",
            "houses": QR_HOUSES,
            "active_houses": {1, 2, 4},
            "left_pills": [
                (354, 72, "MIỄN PHÍ CHUYỂN KHOẢN QR: TIỀN KHÔNG RỜI HỆ THỐNG NGÂN HÀNG", "amber"),
                (354, 598, "200 LY/NGÀY = 10 TRIỆU ĐỒNG NẰM TRONG BỂ VỐN CASA ~0,1%/NĂM", "green"),
            ],
            "steps": [
                ("1. Chặn rò rỉ tiền mặt tại cây ATM", "50.000 đ chỉ nhảy từ tài khoản CASA của bạn sang tài khoản CASA của quán, giảm chi phí kiểm đếm tiền giấy.", "teal"),
                ("2. Giữ trọn 220.000 đ/ngày cho quán", "Với 200 ly/ngày (10.000.000 đ), quét QR giúp quán giữ lại 220.000 đ/ngày (6,6 triệu/tháng) so với quẹt thẻ.", "green"),
                ("3. Ngân hàng thu lợi ở cửa sau", "Số dư doanh thu nằm lại trong TK 112 (lãi ~0,1%/năm) làm nguồn vốn rẻ để ngân hàng cho vay ~8,5%/năm.", "amber"),
            ],
            "footer_eq": "Ngân hàng miễn phí chuyển khoản lẻ ở cửa trước để giữ bể vốn CASA giá rẻ ở cửa sau",
        },
        {
            "out": "qr-fig-4.jpg",
            "plate": "public/brand/card-short-plate-3.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  MÃ QR ĐỘNG & CHARGEBACK",
            "title": "Mã QR tĩnh (0 đ) vs Mã QR động tự gạch nợ (~0,2%) — và lưu ý khi mua hàng từ xa",
            "houses": QR_HOUSES,
            "active_houses": {0, 1, 2, 4},
            "left_pills": [
                (354, 72, "MÃ QR ĐỘNG: KHOÁ SỐ TIỀN + TỰ GẠCH NỢ ĐƠN HÀNG (PHÍ ~0,2%)", "teal"),
                (354, 598, "LƯU Ý NGƯỜI MUA: CHUYỂN KHOẢN QR KHÔNG CÓ QUYỀN CHARGEBACK", "clay"),
            ],
            "steps": [
                ("1. Mã QR tĩnh cá nhân (Phí 0 đ)", "Rẻ nhưng thu ngân phải nhìn màn hình bằng mắt thường (dễ bị biên lai giả) và kế toán phải dò sao kê tay.", "amber"),
                ("2. Mã QR động thương mại (Phí ~0,2%)", "Trên 10.000.000 đ doanh thu chỉ tốn ~20.000 đ (Nợ TK 641), tự động khớp đơn và rẻ hơn 11 lần so với thẻ.", "green"),
                ("3. Không có lá chắn Chargeback", "Vì chính bạn đẩy tiền đi như trao tiền mặt, ngân hàng không thể tự động thu hồi nếu người bán từ xa gian lận.", "clay"),
            ],
            "footer_eq": "Tại quầy quen: Quét QR giữ 99,8%–100% cho quán  ·  Mua từ xa: Lưu ý QR không có Chargeback",
        },
    ],
    "profitcash": [
        {
            "out": "profitcash-fig-1.jpg",
            "plate": "public/brand/pay-short-plate-1.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  DỒN TÍCH VS DÒNG TIỀN",
            "title": "Hợp đồng 10 tỷ đồng qua hai lăng kính: Doanh thu ghi đủ 10 tỷ nhưng tiền về chỉ 7,5 tỷ",
            "houses": PROFITCASH_HOUSES,
            "active_houses": {0, 1, 2, 3},
            "left_pills": [
                (354, 72, "SỔ KẾT QUẢ KINH DOANH: GHI ĐỦ 10 TỶ DOANH THU · BÁO LÃI 2 TỶ", "green"),
                (354, 598, "SỔ TIỀN GỬI TK 112: XUẤT 7,45 TỶ MUA HÀNG · MỚI THU VỀ 7,5 TỶ", "amber"),
            ],
            "steps": [
                ("1. Kế toán dồn tích (Accrual)", "Ngay khi giao hàng và ký nghiệm thu, kế toán ghi Có TK 511 đủ 10.000.000.000 đ dù khách chưa trả hết.", "green"),
                ("2. Chi tiền tươi ở đầu vào (TK 156)", "Ngày 01/10 công ty đã xuất 7.450.000.000 đ từ TK 112 trả nhà cung cấp (6,5 tỷ giá vốn + 950 triệu tồn kho).", "amber"),
                ("3. Bán chịu trả chậm ở đầu ra (TK 131)", "Khách sỉ mới trả 7.500.000.000 đ đợt 1, còn giữ lại 2.500.000.000 đ hẹn 60–90 ngày sau mới thanh toán.", "clay"),
            ],
            "footer_eq": "Doanh thu ghi sổ 10 tỷ đồng (TK 511) nhưng tiền thực thu chỉ là 7,5 tỷ đồng (TK 112)",
        },
        {
            "out": "profitcash-fig-2.jpg",
            "plate": "public/brand/pay-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  HAI BỌT BIỂN HÚT TIỀN",
            "title": "Giải phẫu 3,5 tỷ Tổng tài sản chiều 31/12: 3,45 tỷ đang ngủ ở Phải thu và Tồn kho",
            "houses": PROFITCASH_HOUSES,
            "active_houses": {0, 1, 2, 3},
            "left_pills": [
                (354, 72, "PHẢI THU KHÁCH SỈ (TK 131): 2,50 TỶ ĐỒNG NẰM TRÊN GIẤY NỢ", "amber"),
                (354, 598, "HÀNG TỒN KHO (TK 156): 950 TRIỆU ĐỒNG NẰM TRÊN KỆ KHO", "teal"),
            ],
            "steps": [
                ("1. Phép cộng trừ tiền mặt (TK 112)", "Tiền vào 8,50 tỷ (1 tỷ đầu kỳ + 7,5 tỷ thu khách) trừ Tiền ra 8,45 tỷ (7,45 tỷ mua hàng + 1 tỷ vận hành) = 50 triệu.", "teal"),
                ("2. Bọt biển #1: Phải thu TK 131 (2,5 tỷ)", "Khách sỉ đang chiếm dụng hợp pháp 2.500.000.000 đ vốn lưu động không mất lãi của công ty bạn.", "amber"),
                ("3. Bọt biển #2: Tồn kho TK 156 (950 triệu)", "Lô hàng nhập thêm 950.000.000 đ chưa bán nên chưa vào chi phí, nhưng đã rút tiền thật khỏi TK 112.", "clay"),
            ],
            "footer_eq": "Tổng tài sản 3,50 tỷ = Phải thu 2,50 tỷ + Tồn kho 0,95 tỷ + Tiền mặt 0,05 tỷ (50 triệu)",
        },
        {
            "out": "profitcash-fig-3.jpg",
            "plate": "public/brand/install-short-plate-3.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  VÒNG QUAY TIỀN MẶT (CCC)",
            "title": "Khi Vòng quay tiền mặt kéo giãn: Cho khách nợ 2,5 tỷ nhưng phải vay 450 triệu trả lương",
            "houses": PROFITCASH_HOUSES,
            "active_houses": {1, 2, 3, 4},
            "left_pills": [
                (354, 72, "BẢNG LƯƠNG THÁNG 12 (TK 334): 500 TRIỆU ĐỒNG ĐẾN HẠN CHIỀU 31/12", "amber"),
                (354, 598, "GIẢI CỨU: VÉT 50 TRIỆU TK 112 + VAY NGẮN HẠN 450 TRIỆU (TK 341)", "green"),
            ],
            "steps": [
                ("1. Vòng quay tiền mặt CCC = DIO + DSO − DPO", "Trả tiền tươi cho nhà cung cấp (DPO = 0) nhưng chờ khách sỉ trả nợ 90 ngày làm két tiền bị rút rỗng.", "amber"),
                ("2. Bút toán vay cứu lương chiều 31/12", "Ghi Nợ TK 334 (500.000.000 đ) / Có TK 112 (50.000.000 đ) + Có TK 341 (Vay ngắn hạn: 450.000.000 đ).", "green"),
                ("3. Nghịch lý chi phí lãi vay (TK 635)", "Công ty báo lãi 2 tỷ đồng nhưng phải trả lãi vay ngân hàng vì đang cho khách sỉ mượn không lãi 2,5 tỷ.", "clay"),
            ],
            "footer_eq": "Tăng trưởng đơn hàng sỉ trên một vòng quay tiền mặt lệch pha sẽ hút cạn két tiền",
        },
        {
            "out": "profitcash-fig-4.jpg",
            "plate": "public/brand/install-short-plate-4.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  CẦU NỐI OCF & 3 VAN GIẢI PHÓNG",
            "title": "Cầu nối Lợi nhuận (+2 tỷ) sang Dòng tiền OCF (−950 triệu) và 3 van giải phóng tiền mặt",
            "houses": PROFITCASH_HOUSES,
            "active_houses": {0, 1, 2, 3, 4},
            "left_pills": [
                (354, 72, "LỢI NHUẬN RÒNG (+2 TỶ) ≠ DÒNG TIỀN KINH DOANH OCF (−950 TRIỆU)", "teal"),
                (354, 598, "3 VAN ĐIỀU TIẾT: THU THEO TIẾN ĐỘ · ĐỊNH MỨC KHO · GIÃN PHẢI TRẢ", "green"),
            ],
            "steps": [
                ("1. Phương trình Lưu chuyển tiền tệ gián tiếp", "OCF = Lãi (+2,00 tỷ) − ΔPhải thu (2,50 tỷ) − ΔTồn kho (0,95 tỷ) + ΔLương chưa chi (0,50 tỷ) = −950 triệu.", "teal"),
                ("2. Thu hồi công nợ TK 131 sớm", "Chia nhỏ đợt thanh toán theo tiến độ hoặc chiết khấu thanh toán sớm để kéo tiền tươi về TK 112.", "green"),
                ("3. Đồng bộ tồn kho TK 156 & phải trả TK 331", "Nhập kho sát tốc độ bán thật và thương lượng kỳ hạn trả nhà cung cấp khớp với kỳ hạn thu khách hàng.", "amber"),
            ],
            "footer_eq": "Lợi nhuận trên TK 421 là ý kiến kế toán — Tiền mặt trong TK 112 mới là oxy duy trì sự sống",
        },
    ],
    "offus": [
        {
            "out": "offus-fig-1.jpg",
            "plate": "public/brand/pay-short-plate-1.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 01  ·  CHƯƠNG 02  ·  CÙNG NGÂN HÀNG (ON-US)",
            "title": "Chuyển khoản 20 triệu cùng ngân hàng (On-Us): Sửa 2 dòng sổ, 0 đồng rời nhà",
            "houses": OFFUS_HOUSES,
            "active_houses": {0, 1},
            "left_pills": [
                (354, 72, "SỔ CÁI NỘI BỘ (ON-US): TRỪ BẠN 20 TRIỆU · CỘNG ĐỐI TÁC 20 TRIỆU", "green"),
                (354, 598, "BỂ VỐN CASA & DỰ TRỮ TẠI NH TRUNG ƯƠNG: BIẾN ĐỘNG 0 ĐỒNG", "teal"),
            ],
            "steps": [
                ("1. Bút toán nội mạng (Book Transfer)", "Ngân hàng chỉ sửa hai dòng nợ phải trả trong cùng một cuốn sổ cái: đổi chủ nợ từ bạn sang người nhận.", "green"),
                ("2. Bất biến bể vốn CASA (~0,1%/năm)", "Tổng tiền gửi không kỳ hạn của ngân hàng giữ nguyên 100%, không tốn một đồng dự trữ liên ngân hàng nào.", "teal"),
                ("3. Sổ doanh nghiệp (TT 99/2025)", "Bên chuyển ghi Nợ TK 331 (Phải trả người bán) / Có TK 112 (Tiền gửi không kỳ hạn): 20.000.000 đ.", "amber"),
            ],
            "footer_eq": "Giao dịch On-Us: Tiền chỉ đổi tên người sở hữu ngay trong cùng một toà nhà ngân hàng",
        },
        {
            "out": "offus-fig-2.jpg",
            "plate": "public/brand/pay-short-plate-2.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 02  ·  CHƯƠNG 03  ·  KÝ QUỸ BẢO CHỨNG 24/7",
            "title": "Khác ngân hàng (Off-Us): Bí mật Hạn mức ký quỹ giúp ghi Có ngay sau 3 giây",
            "houses": OFFUS_HOUSES,
            "active_houses": {0, 1, 2, 3},
            "left_pills": [
                (354, 72, "GIÂY 02: CHUYỂN MẠCH KIỂM HẠN MỨC KÝ QUỸ BẢO CHỨNG (PRE-FUND)", "amber"),
                (354, 598, "GIÂY 03: NGÂN HÀNG NHẬN GHI CÓ +20 TRIỆU TRƯỚC KHI DỰ TRỮ CHẠY", "green"),
            ],
            "steps": [
                ("1. Đặt cọc Hạn mức ký quỹ (Pre-funded Cap)", "Ngân hàng gửi đã ký quỹ sẵn tiền dự trữ hoặc trái phiếu tại hệ thống để bảo lãnh cho các lệnh trong phiên.", "amber"),
                ("2. Đóng dấu bảo chứng ở giây thứ 2", "Tổ chức chuyển mạch trừ lùi 20.000.000 đ hạn mức khả dụng của ngân hàng gửi rồi chuyển tiếp bản tin.", "teal"),
                ("3. Ghi Có tức thời ở giây thứ 3 (TK 112)", "Ngân hàng nhận cộng ngay +20.000.000 đ cho người nhận tiêu dùng (Nợ TK 112 / Có TK 131: 20.000.000 đ).", "green"),
            ],
            "footer_eq": "Nhờ hạn mức ký quỹ bảo chứng trước, bản tin 3 giây an toàn tương đương tiền mặt",
        },
        {
            "out": "offus-fig-3.jpg",
            "plate": "public/brand/pay-short-plate-3.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 03  ·  CHƯƠNG 04  ·  BÙ TRỪ RÒNG CUỐI PHIÊN",
            "title": "Gom 970 tỷ giao dịch hai chiều (500 tỷ − 470 tỷ) thành 1 lệnh quyết toán 30 tỷ",
            "houses": OFFUS_HOUSES,
            "active_houses": {1, 2, 3, 4},
            "left_pills": [
                (354, 72, "BÙ TRỪ ĐA PHƯƠNG: 500 TỶ CHIỀU ĐI − 470 TỶ CHIỀU VỀ = 30 TỶ RÒNG", "teal"),
                (354, 598, "NH TRUNG ƯƠNG: CẮT ĐÚNG 30 TỶ DỰ TRỮ · TIẾT KIỆM 940 TỶ (96,9%)", "green"),
            ],
            "steps": [
                ("1. Cộng gộp hai chiều suốt phiên (Clearing)", "Chiều Ngân hàng bạn → đối tác là 500 tỷ đồng; chiều ngược lại về Ngân hàng bạn là 470 tỷ đồng (gộp 970 tỷ).", "teal"),
                ("2. Tính vị thế ròng (Netting = 30 tỷ đồng)", "Đặt lên bàn cân bù trừ: 500 tỷ − 470 tỷ chỉ còn nghĩa vụ phải trả ròng đúng 30.000.000.000 đ.", "amber"),
                ("3. Quyết toán tại Ngân hàng Trung ương", "Cắt chuyển 1 lệnh 30 tỷ đồng dự trữ duy nhất — giải phóng 940 tỷ đồng thanh khoản (96,9% tổng gộp).", "green"),
            ],
            "footer_eq": "Bù trừ ròng giải phóng 96,9% thanh khoản dự trữ, mở dư địa miễn phí 0 đồng cho người dùng",
        },
        {
            "out": "offus-fig-4.jpg",
            "plate": "public/brand/pay-short-plate-4.jpg",
            "crop": (0, 290, 768, 1220),
            "badge": "HÌNH 04  ·  CHƯƠNG 05  ·  ĐẠI LỘ RTGS & TREO TK 113",
            "title": "Khi nào tiền đi thẳng từng lệnh qua RTGS (10 tỷ) và khi nào treo trên TK 113?",
            "houses": OFFUS_HOUSES,
            "active_houses": {0, 1, 2, 4},
            "left_pills": [
                (354, 72, "LỆNH LỚN 10 TỶ ĐỒNG: ĐI THẲNG ĐẠI LỘ RTGS TỪNG LỆNH TỨC THỜI", "amber"),
                (354, 598, "LỆNH NGHẼN CHIỀU 31/12: GHI NỢ TK 113 (TIỀN ĐANG CHUYỂN) / CÓ TK 112", "clay"),
            ],
            "steps": [
                ("1. Thanh toán tổng tức thời từng lệnh (RTGS)", "Các lô thanh toán lớn vượt trần 24/7 (ví dụ 10 tỷ đồng) cắt tiền dự trữ trực tiếp từng lệnh tại NH Trung ương.", "amber"),
                ("2. Lệnh nghẽn đối soát chiều 31/12 (TK 113)", "Đã trừ TK 112 nhưng đối tác chưa nhận được tiền: ghi Nợ TK 113 (Tiền đang chuyển) / Có TK 112: 20.000.000 đ.", "clay"),
                ("3. Tất toán công nợ đầu năm mới (TK 331)", "Khi ngân hàng đối tác báo Có hoàn tất, kế toán mới kết chuyển Nợ TK 331 / Có TK 113: 20.000.000 đ.", "green"),
            ],
            "footer_eq": "Treo TK 113 giúp khớp sao kê TK 112 ngày 31/12 mà không xoá khống công nợ phải trả TK 331",
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
