# nd30 — Engine thể thức văn bản hành chính Việt Nam

AI skill giúp soạn **file .docx đúng thể thức Nghị định 30/2020/NĐ-CP** — font, cỡ chữ, lề theo mm,
vị trí từng thành phần — rồi **tự kiểm tra bằng script** trước khi giao. Không phải "chữ thô nhìn
giống văn bản hành chính".

Chạy được với **Claude Code, Gemini (app/Spark), Gemini CLI**, hoặc dùng script Python trực tiếp.
Không cần MCP, không cần dựng server.

## Nó làm được gì

- **Phân loại 27+ loại văn bản** (công văn, tờ trình, quyết định, kế hoạch, báo cáo, thông báo,
  biên bản, giấy mời, phiếu biểu quyết…) từ cách người dùng nói chuyện bình thường.
- **Hỏi lấy dữ liệu trước khi soạn** — bộ câu hỏi riêng theo từng loại VB, thay vì đoán rồi bịa.
- **Sinh .docx** đúng thể thức: A4, Times New Roman, lề trái 30–35mm / phải 15–20mm / trên-dưới
  20–25mm, header bảng-2-cột-ẩn-viền (tên cơ quan bên trái, Quốc hiệu–Tiêu ngữ bên phải), phân cấp
  La Mã → số → chữ cái → gạch đầu dòng, Nơi nhận nhóm `b/c`–`t/h`–`p/h`–`Lưu: VT`, khối chữ ký.
- **Validate tự động**: khổ giấy, lề, font/màu (cả trong bảng và header/footer), thành phần bắt buộc
  theo từng loại VB, bullet tự động của Word (NĐ30 không cho dùng), bảng tràn lề, và placeholder còn sót.
- **Học từ mẫu cơ quan**: cơ quan đã có khuôn .docx riêng thì khuôn của họ thắng mặc định của skill.

## 3 luật cứng

**1. Không bịa.** Số/ký hiệu văn bản, căn cứ pháp lý, người ký, số tiền, ngày ban hành, quan điểm
biểu quyết, số liệu thống kê → luôn để `[CẦN BỔ SUNG: ...]` cho người dùng điền. AI chỉ tự quyết
câu chữ hành chính, cấu trúc, và format trình bày.

**2. Đúng luật cho đúng loại văn bản** — NĐ30 không phủ hết:

| Loại | Thể thức theo |
|---|---|
| Văn bản hành chính (công văn, tờ trình, quyết định cá biệt, kế hoạch, báo cáo…) | **NĐ 30/2020/NĐ-CP** ✅ repo này |
| Văn bản quy phạm pháp luật (Nghị quyết HĐND tỉnh, Quyết định/Chỉ thị QPPL của UBND tỉnh, Thông tư…) | **NĐ 78/2025 + NĐ 187/2025** — thể thức riêng, đừng bê khuôn NĐ30 |
| Cơ quan Đảng (Tỉnh ủy, Huyện ủy, Đảng ủy, Ban Đảng) | **Hướng dẫn 36-HD/VPTW** — repo này chưa phủ, phải hỏi lại |

**3. Không nói "chuẩn NĐ30" khi chỉ áp dụng một phần.** Nói rõ đã áp phần nào, còn thiếu gì.

## Dùng thế nào

### Với Gemini (app hoặc Spark) — không cần cài gì
Dán câu này vào Gemini:

> Dùng skill ở https://github.com/kanazawahere/nd30 soạn giúp tôi [loại văn bản] về [việc cần làm], xuất file .docx.

Gemini sẽ tự đọc repo, hỏi lại thông tin còn thiếu, rồi tạo file .docx trong sandbox của nó.

### Với Claude Code
Clone vào thư mục skill rồi gọi `/nd30`:
```bash
git clone https://github.com/kanazawahere/nd30.git ~/.claude/skills/nd30
```

### Dùng script trực tiếp (không cần AI)
```bash
pip install python-docx
python3 scripts/validate_docx.py <file.docx> --profile administrative   # kiểm thể thức file có sẵn
python3 scripts/inspect_docx.py  <file.docx>                            # soi thông số thật (lề, font, cỡ)
python3 scripts/learn_template.py <mau-co-quan.docx>                    # bóc thể thức từ mẫu cơ quan
```

Mẫu rỗng có sẵn trong `templates/`: tờ trình, công văn, quyết định, kế hoạch, báo cáo.

## Cấu trúc

```
SKILL.md            # entry point cho AI agent — quy trình 5 pha
references/         # thông số NĐ30, danh mục 27+ loại VB, bộ câu hỏi phỏng vấn, checklist
scripts/            # build / validate / inspect / learn-template / fill-template
templates/          # 5 mẫu .docx rỗng, mỗi mẫu tự pass validate
tests/              # pytest
```

## Kiểm thử

```bash
pip install python-docx pytest pyyaml
python3 -m pytest tests/ -v
```

## Giới hạn đã biết

- **Cỡ chữ từng thành phần** chưa kiểm được đáng tin bằng script (python-docx đọc qua
  style-inheritance không chắc) → còn phải soi mắt, đã ghi trong `references/validation-checklist.md`.
- Chưa phủ thể thức **văn bản Đảng** (HD 36-HD/VPTW) và **văn bản QPPL** (NĐ 78/2025, NĐ 187/2025).
- Chưa có chữ ký số / con dấu — phần đó thuộc quy trình văn thư của cơ quan.

## Nguồn gốc

Xem [`NGUON-GOC.md`](./NGUON-GOC.md). Tóm gọn: phần nghiệp vụ (danh mục loại VB, bộ câu hỏi phỏng
vấn, nền builder/validator) kế thừa từ [biencuong/vbhc](https://github.com/biencuong/vbhc) — license
Unlicense (public domain); thông số thể thức trích thẳng **Phụ lục I Nghị định 30/2020/NĐ-CP**.

## License

MIT — xem [LICENSE](./LICENSE).
