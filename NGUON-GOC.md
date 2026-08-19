<!-- nha-van:exempt — tài liệu ghi công/license nội bộ, không phải văn bản gửi ra ngoài -->
# Nguồn gốc skill `/nd30`

**Ngày bake: 2026-08-19.**

## 1. Thông số thể thức — trích thẳng văn bản pháp luật

Mọi con số (khổ giấy, lề mm, cỡ chữ pt, kiểu chữ, vị trí từng thành phần) trong
`references/the-thuc-nd30.md` lấy từ **Nghị định 30/2020/NĐ-CP, Phụ lục I** — văn bản pháp
luật công khai, không ai sở hữu bản quyền. Không con số nào do skill tự nghĩ ra.

## 2. `vbhc` — nguồn chính, copy trực tiếp

- Repo: `vbhc` (soạn thảo VBHC), tác giả **biencuong**
- License: **Unlicense (public domain)** → tự do copy, sửa, phân phối lại
- Phần đã lấy:
  - `references/danh-muc-loai-vb.md` ← `resources/danh-muc-loai-vb.md` (27+ loại VB, 3 nhóm,
    bảng nhận diện keyword, cảnh báo NĐ 78/2025 + NĐ 187/2025 cho VBQPPL) — giữ gần nguyên.
  - `references/interview-questions.md` ← `resources/interview-questions.md` — giữ gần nguyên.
  - `scripts/build_docx.py` ← `scripts/vbhc_doc_builder.py` (nền: helper XML, bảng 2 cột ẩn viền,
    gạch chân ngắn, khối Số/ngày, khối Nơi nhận + chữ ký, page numbering).
  - `scripts/validate_docx.py` — tầng B (9 thành phần thể thức) port từ `scripts/validate_thethuc.py`.
  - `scripts/inspect_docx.py`, `learn_template.py`, `fill_template.py`, `find_placeholders.py`,
    `normalize_template.py`, `_common.py`, `rules_loader.py`, `scripts/rules/*.yaml`.
- Phần skill này **viết thêm** vào các file trên:
  - `build_docx.py`: `setup_document()`, `add_two_col_block()` (helper bảng 2 cột ẩn viền tổng quát),
    `add_can_cu()` (tự đặt `;` / `.`), `add_bullet()`/`add_bullets()` (tiền tố tay),
    `add_centered()`, `add_table()` (có viền, không shading), `add_ket_thuc()`, `placeholder()`;
    sửa `add_signature_noi_nhan()` giữ dấu chấm cuối dòng `Lưu:` và thêm `w:cantSplit`
    (khối cuối từng bị chẻ ngang qua 2 trang khi render — đã bắt được bằng mắt).
  - `validate_docx.py`: toàn bộ tầng A (khổ giấy/lề/font/màu/bullet tự động/shading/bảng tràn lề/
    placeholder), cờ `--profile`, cờ `--allow-placeholder`, API `validate_doc()`.
  - `find_placeholders.py`: nhận thêm pattern `[CẦN BỔ SUNG: ...]`.
  - `rules_loader.py`: viết lại — bỏ tầng cache đồng bộ từ server, đọc `scripts/rules/`, PyYAML optional.

**Đã CỐ Ý bỏ khỏi vbhc:** toàn bộ `mcp/`, `cloud/`, `deploy/` (MCP server, KB Hub, systemd unit),
cùng các script vận hành riêng của repo đó (`manage_keys.py`, `aggregate_survey.py`,
`reorganize_folder.py`, `regenerate_check.py`, `build_*_template.py`).
**Lý do thiết kế:** skill phải chạy được bằng **script Python thuần**, không cần server nào —
để cán bộ tự dùng qua Gemini app / Claude, và để không nuôi thêm một hạ tầng phải trực.

## 3. `vietnamese-docs-style` — chỉ tham khảo Ý TƯỞNG, KHÔNG copy

- Repo: `vietnamese-docs-style`, tác giả **bGiaHuy**
- License: **KHÔNG RÕ** (không có file LICENSE)
- Vì repo `Central_Command` sẽ push lên GitHub của mình, **không đưa code/văn bản phái sinh
  từ nguồn không rõ license vào đây**. Đã đọc để hiểu cách tiếp cận (chia profile tài liệu,
  validate khổ giấy/lề/font/màu, checklist trước khi save) rồi **tự viết lại toàn bộ**:
  - `references/validation-checklist.md`, `references/editorial-quality-vi.md`,
    `references/document-profiles.md` — viết mới bằng lời của mình.
  - `scripts/validate_docx.py` tầng A, `scripts/render_docx.py`, `tests/test_validation.py`
    — code của skill này (nền tầng B là vbhc, public domain).
- Không lấy: script, reference, `assets/samples/`, `references/source-documents/` của repo đó.
- Ghi chú: một số file đã copy trong lần bake đầu (2026-08-19, sáng) **đã xoá và viết lại**
  sau khi chốt lại điều kiện license.

## 4. Tự kiểm
- `tests/test_validation.py` — 24 test, pass 100% (python-docx 1.2.0, pytest, PyYAML).
- Mẫu trong `templates/` sinh lại được bằng `templates/_build_templates.py --check`.
- Ví dụ dạy học: `assets/samples/build_to_trinh_thon_thong_minh.py`.
