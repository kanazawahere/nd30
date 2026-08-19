"""Ví dụ THẬT dùng trong lớp tập huấn: Tờ trình xin chủ trương phê duyệt Kế hoạch
triển khai mô hình "Thôn thông minh" năm 2026.

nha-van:exempt — mã nguồn sinh file mẫu để DẠY, không phải văn bản gửi cơ quan.

Mọi dữ kiện chưa biết (số hiệu, tên xã/huyện, kinh phí, người ký, ngày ban hành) đều để
`[CẦN BỔ SUNG: ...]` theo Luật cứng #1 của skill — KHÔNG bịa số.

Chạy:
    python3 assets/samples/build_to_trinh_thon_thong_minh.py <đường-dẫn-file-ra.docx>
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_docx import (  # noqa: E402
    add_body_paragraph, add_bullet, add_header_section, add_ket_thuc, add_kinh_gui,
    add_section_heading, add_signature_noi_nhan, add_so_vb_and_date_section,
    add_title_block, placeholder, setup_document,
)

P = placeholder
XA = P("tên xã")
HUYEN = P("tên huyện/thành phố")


def build(out: Path):
    doc = setup_document(profile="administrative")

    add_header_section(doc,
                       co_quan_chu_quan="UBND " + HUYEN,
                       co_quan_ban_hanh="UBND XÃ " + P("TÊN XÃ IN HOA"))
    add_so_vb_and_date_section(doc, so_vb="", ky_hieu="TTr-UBND",
                               dia_danh=XA, ngay="", thang="", nam="2026",
                               trich_yeu="")
    add_title_block(doc, ten_loai="TỜ TRÌNH",
                    trich_yeu="Về việc xin chủ trương phê duyệt Kế hoạch triển khai "
                              "mô hình “Thôn thông minh” năm 2026")

    add_kinh_gui(doc, "Ủy ban nhân dân " + HUYEN)

    add_body_paragraph(doc,
        "Thực hiện " + P("văn bản chỉ đạo về chuyển đổi số: tên, số, ngày, cơ quan ban hành")
        + ", Ủy ban nhân dân xã " + XA + " kính trình Ủy ban nhân dân " + HUYEN
        + " xem xét, cho chủ trương phê duyệt Kế hoạch triển khai mô hình “Thôn thông minh” "
          "năm 2026 trên địa bàn xã, với các nội dung sau:")

    add_section_heading(doc, "1. Sự cần thiết")
    add_body_paragraph(doc,
        "Mô hình “Thôn thông minh” là một tiêu chí trong xây dựng nông thôn mới nâng cao. "
        "Trên địa bàn xã " + XA + ", việc tiếp nhận thông tin và giải quyết thủ tục hành chính "
        "của người dân còn phụ thuộc nhiều vào hình thức trực tiếp; hạ tầng thông tin ở thôn "
        "chưa đồng bộ. Triển khai mô hình sẽ giúp người dân tiếp cận thông tin và dịch vụ công "
        "trực tuyến thuận lợi hơn, đồng thời giảm thời gian đi lại.")

    add_section_heading(doc, "2. Nội dung xin chủ trương")
    add_bullet(doc, "Phạm vi triển khai: " + P("tên thôn được chọn làm điểm") + ".")
    add_bullet(doc, "Nội dung triển khai: lắp đặt hệ thống truyền thanh thông minh; "
                    "thiết lập nhóm thông tin điện tử của thôn; hướng dẫn người dân sử dụng "
                    "dịch vụ công trực tuyến và thanh toán không dùng tiền mặt.")
    add_bullet(doc, "Thời gian thực hiện: từ " + P("tháng bắt đầu")
                    + " đến " + P("tháng hoàn thành") + " năm 2026.")
    add_bullet(doc, "Tổng kinh phí dự kiến: " + P("số tiền")
                    + ", từ nguồn " + P("nguồn kinh phí") + ".")

    add_section_heading(doc, "3. Tổ chức thực hiện")
    add_bullet(doc, "Ủy ban nhân dân xã " + XA + " chủ trì xây dựng kế hoạch chi tiết, "
                    "phân công nhiệm vụ và bố trí kinh phí sau khi được phê duyệt.")
    add_bullet(doc, P("đơn vị/bộ phận được phân công") + " theo dõi, tổng hợp và báo cáo "
                    "tiến độ định kỳ.")

    add_body_paragraph(doc,
        "Ủy ban nhân dân xã " + XA + " kính trình Ủy ban nhân dân " + HUYEN
        + " xem xét, quyết định.")
    add_ket_thuc(doc)

    add_signature_noi_nhan(doc,
        noi_nhan_items=["- Như trên;", "- Lưu: VT, VP."],
        chuc_vu="CHỦ TỊCH",
        nguoi_ky=P("họ tên người ký"),
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print(f"đã sinh: {out}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("to-trinh-thon-thong-minh-mau.docx")
    build(target.resolve())
