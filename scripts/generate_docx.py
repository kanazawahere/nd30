#!/usr/bin/env python3
"""generate_docx — sinh file .docx đúng thể thức NĐ30 từ 1 file JSON/YAML mô tả nội dung.

nha-van:exempt — đây là mã nguồn, không phải văn bản gửi ra ngoài.

Vì sao script này tồn tại: AI agent (đặc biệt Gemini Spark chạy trong sandbox không có
filesystem của mình) dễ SINH RA cấu trúc JSON đúng, nhưng dễ SAI khi tự viết code
python-docx ad-hoc gọi trực tiếp build_docx.py (phải đọc + transcribe ~1200 dòng code
qua giao diện web rất chậm và dễ lỗi). Đường đi đúng: agent chỉ cần sinh 1 file JSON nhỏ,
rồi gọi:

    python3 scripts/generate_docx.py input.json -o output.docx

Script tự import build_docx.py (cùng thư mục) và dựng file — KHÔNG cần agent đọc/hiểu
nội dung bên trong build_docx.py.

Schema JSON (mọi field đều optional trừ ghi chú *bắt buộc*):
{
  "profile": "administrative",
  "header": {
    "co_quan_chu_quan": "UBND HUYỆN ...",      // *bắt buộc*
    "co_quan_ban_hanh": "UBND XÃ ...",          // *bắt buộc*
    "so_vb": "",                                 // để trống nếu chưa có số
    "ky_hieu": "TTr-UBND",                       // *bắt buộc*
    "trich_yeu": "Về việc ...",                  // *bắt buộc*
    "dia_danh": "...",                           // *bắt buộc*
    "ngay": "", "thang": "", "nam": "",
    "is_cong_van": false,
    "ten_loai_in_hoa": "TỜ TRÌNH"                 // bỏ trống nếu is_cong_van=true
  },
  "kinh_gui": "UBND huyện ...",
  "body": [
    {"type": "heading", "text": "1. Sự cần thiết"},
    {"type": "paragraph", "text": "..."},
    {"type": "bullet", "text": "...", "level": 1},
    {"type": "table", "headers": ["A","B"], "rows": [["1","2"]]},
    {"type": "can_cu", "items": ["Căn cứ Luật ...", "Căn cứ Nghị định ..."]}
  ],
  "ket_thuc": "./.",
  "signature": {
    "noi_nhan_items": ["Như trên"],
    "phong_viet_tat": "VT",
    "chuc_vu": "CHỦ TỊCH",
    "nguoi_ky": "[CẦN BỔ SUNG: họ tên]",
    "quyen_han": "", "chuc_vu_thay": ""
  }
}

Dùng `placeholder("mô tả")` bằng cách gõ thẳng chuỗi "[CẦN BỔ SUNG: mô tả]" trong JSON —
validate_docx.py sẽ tự bắt được các placeholder này.

Ví dụ JSON đầy đủ có sẵn ở `examples/input-sample.json`.

Zero third-party dependency cho input .json: parser dùng module `json` chuẩn của Python, KHÔNG
cần cài `pyyaml`. `pyyaml` chỉ cần khi input là `.yaml`/`.yml` — sandbox không cài được pyyaml
vẫn dùng được script này miễn truyền input dạng `.json`.

Xuất file + validate luôn trong 1 lệnh (khỏi gọi validate_docx.py riêng):

    python3 scripts/generate_docx.py input.json -o output.docx --validate --profile administrative
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_docx as bd  # noqa: E402

try:
    import yaml  # optional; chỉ cần nếu input là .yaml/.yml
except ImportError:
    yaml = None


def load_spec(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        if yaml is None:
            raise SystemExit("Cần cài pyyaml để đọc file .yaml (pip install pyyaml), "
                              "hoặc chuyển input sang .json.")
        return yaml.safe_load(text)
    return json.loads(text)


def build_body_item(doc, item: dict, profile: str) -> None:
    kind = item.get("type", "paragraph")
    if kind == "heading":
        bd.add_section_heading(doc, item["text"], level=item.get("level", 1))
    elif kind == "paragraph":
        bd.add_body_paragraph(doc, item["text"])
    elif kind == "bullet":
        bd.add_bullet(doc, item["text"], level=item.get("level", 1), profile=profile)
    elif kind == "table":
        bd.add_table(doc, item["headers"], item["rows"])
    elif kind == "can_cu":
        bd.add_can_cu(doc, item["items"])
    elif kind == "centered":
        bd.add_centered(doc, item["text"], bold=item.get("bold", False))
    else:
        raise ValueError(f"body item không hỗ trợ type={kind!r}: {item}")


def generate(spec: dict) -> "bd.Document":
    profile = spec.get("profile", "administrative")
    header = spec["header"]

    doc = bd.Document()
    bd.setup_page(doc)
    bd.add_header_section(
        doc,
        co_quan_chu_quan=header["co_quan_chu_quan"],
        co_quan_ban_hanh=header["co_quan_ban_hanh"],
    )
    bd.add_so_vb_and_date_section(
        doc,
        so_vb=header.get("so_vb", ""),
        ky_hieu=header.get("ky_hieu", ""),
        trich_yeu=header.get("trich_yeu", ""),
        dia_danh=header.get("dia_danh", ""),
        ngay=header.get("ngay", ""),
        thang=header.get("thang", ""),
        nam=header.get("nam", ""),
        is_cong_van=header.get("is_cong_van", False),
    )
    if not header.get("is_cong_van") and header.get("ten_loai_in_hoa"):
        bd.add_title_block(doc, ten_loai=header["ten_loai_in_hoa"],
                            trich_yeu=header.get("trich_yeu", ""))

    if spec.get("kinh_gui"):
        bd.add_kinh_gui(doc, spec["kinh_gui"])

    for item in spec.get("body", []):
        build_body_item(doc, item, profile)

    if spec.get("ket_thuc"):
        bd.add_ket_thuc(doc, spec["ket_thuc"])

    sig = spec.get("signature")
    if sig:
        bd.add_signature_noi_nhan(
            doc,
            noi_nhan_items=sig.get("noi_nhan_items", ["Như trên"]),
            chuc_vu=sig.get("chuc_vu", bd.placeholder("chức vụ người ký")),
            nguoi_ky=sig.get("nguoi_ky", bd.placeholder("họ tên người ký")),
            quyen_han=sig.get("quyen_han", ""),
            chuc_vu_thay=sig.get("chuc_vu_thay", ""),
            phong_viet_tat=sig.get("phong_viet_tat", ""),
        )

    return doc


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="File .json hoặc .yaml mô tả nội dung văn bản")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Đường dẫn file .docx xuất ra")
    ap.add_argument("--validate", action="store_true",
                    help="Chạy luôn validate_docx.py trên file vừa tạo, in kết quả tóm tắt, "
                         "không cần gọi thêm lệnh riêng.")
    ap.add_argument("--profile", default="administrative",
                    help="Profile truyền cho validate_docx.py khi dùng --validate "
                         "(administrative | bieu-mau-noi-bo | minutes-administrative | academic | general)")
    ap.add_argument("--allow-placeholder", action="store_true",
                    help="Khi dùng --validate: coi placeholder [CẦN BỔ SUNG] là cảnh báo, không phải lỗi nặng "
                         "(dùng khi cố ý xuất bản nháp còn thiếu dữ liệu).")
    args = ap.parse_args()

    spec = load_spec(args.input)
    doc = generate(spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(args.output))
    print(f"✓ Đã xuất {args.output}")

    if not args.validate:
        print(f"  Chạy tiếp: python3 {Path(__file__).parent / 'validate_docx.py'} {args.output} --profile administrative")
        return

    import validate_docx as vd  # cùng thư mục, import trực tiếp — không cần subprocess
    results = vd.run_checks(args.output, args.profile, args.allow_placeholder)
    _, warn, fail = vd.report(args.output, args.profile, results)
    if fail:
        raise SystemExit(2)
    if warn:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
