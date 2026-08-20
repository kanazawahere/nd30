<!-- nha-van:exempt — tài liệu tham chiếu kỹ thuật nội bộ, không phải văn bản gửi ra ngoài -->
# Thể thức VBQPPL — Nghị quyết HĐND cấp tỉnh (Mẫu số 17, NĐ 78/2025)

> **Nguồn duy nhất của thông số dưới đây: Nghị định 78/2025/NĐ-CP, Phụ lục I** (trích PDF chính
> thức, tải 2026-08-20 từ trang phổ biến pháp luật). **Phạm vi: CHỈ Mẫu số 17** — "Nghị quyết của
> Hội đồng nhân dân cấp tỉnh (quy định trực tiếp)". **CHƯA phủ**: Mẫu số 18 (NQ ban hành kèm
> Quy định/Quy chế), luật/pháp lệnh/nghị quyết Quốc hội, quyết định/chỉ thị QPPL của UBND tỉnh,
> thông tư. Đây là bước MỞ ĐẦU cho track VBQPPL, không phải phủ toàn bộ NĐ 78/2025 + NĐ 187/2025.

## Khác biệt với NĐ30 cần lưu ý

- **Lề trang**: trên/dưới/phải 15-20mm, trái 30-35mm (NĐ30: trên/dưới 20-25mm, phải 15-20mm,
  trái 30-35mm) — **trùng khoảng với NĐ30 ở giá trị 2cm/3cm đã dùng làm mặc định**, nên
  `setup_page()` hiện có (2cm/2cm/2cm/3cm) đã nằm gọn trong dải QPPL, KHÔNG cần hàm riêng.
- **Không có "V/v" trích yếu** — chỉ có "NGHỊ QUYẾT" (tên loại) + tên gọi bên dưới, không phải
  "Số: .../TTr-UBND — V/v ...".
- **Không có dòng "QUYẾT NGHỊ:"** cho Mẫu 17 HĐND (khác luật/NQ Quốc hội) — sau phần Căn cứ
  + "Xét Tờ trình...; Báo cáo thẩm tra...; ý kiến thảo luận..." là câu **"Hội đồng nhân dân ban
  hành Nghị quyết ...(tên gọi)..."** viết thường, không phải dòng riêng in hoa.
- **Dòng đóng riêng biệt**: *"Nghị quyết này đã được Hội đồng nhân dân ...Khóa...Kỳ họp thứ...
  thông qua ngày...tháng...năm..."* — chữ nghiêng, đặt ngay dưới Điều cuối cùng. NĐ30 không có
  dòng này.

## Thông số theo từng thành phần (trích Phụ lục I NĐ 78/2025)

| Thành phần | Font | Cỡ chữ | Kiểu | Ghi chú |
|---|---|---|---|---|
| Quốc hiệu | Times New Roman | 12-13pt | ĐẬM, IN HOA | Phía trên-phải trang 1 |
| Tiêu ngữ | Times New Roman | 13-14pt | ĐẬM | Dưới Quốc hiệu, gạch chân full-width |
| Tên cơ quan (HĐND tỉnh...) | Times New Roman | 12-13pt | ĐẬM, IN HOA | Trên-trái trang 1, gạch chân 1/3-1/2 width |
| Số, ký hiệu | Times New Roman | 13pt | thường | `Số: .../20../NQ-HĐND` |
| Địa danh, ngày tháng | Times New Roman | 13-14pt | NGHIÊNG | Cùng dòng/hàng với Số-ký hiệu (2 cột) |
| Tên loại VB "NGHỊ QUYẾT" | Times New Roman | 14pt | ĐẬM, IN HOA | Canh giữa |
| Tên gọi nghị quyết | Times New Roman | 13-14pt | ĐẬM | Dưới tên loại, canh giữa, gạch chân 1/3-1/2 |
| Căn cứ ban hành | Times New Roman | 14pt | NGHIÊNG | Mỗi căn cứ 1 dòng, `;` cuối dòng trên, `.` dòng cuối — GIỐNG NĐ30 |
| "Điều 1." + tên điều | Times New Roman | 13-14pt | ĐẬM, đứng | Cách lề trái 1-1,27cm — GIỐNG NĐ30 |
| Khoản (1., 2.) | Times New Roman | 13-14pt | đứng | Số Ả Rập + `.` |
| Điểm (a), b)) | Times New Roman | 13-14pt | đứng | Chữ cái + `)` |
| Nội dung thường | Times New Roman | 13-14pt | đứng | Justify, thụt đầu dòng 1-1,27cm — GIỐNG NĐ30 |
| Dòng "Nghị quyết này đã được..." | Times New Roman | 13-14pt | NGHIÊNG | Dưới Điều cuối cùng, KHÔNG có ở NĐ30 |
| Chức vụ ký (CHỦ TỊCH) | Times New Roman | 13pt | ĐẬM, IN HOA | Giống NĐ30 |
| Nơi nhận | Times New Roman | 11-12pt | đứng | Giống NĐ30 |

## Bố cục Mẫu số 17 (trích nguyên văn từ Phụ lục, đã bỏ chú thích ghi chú)

```
HỘI ĐỒNG NHÂN DÂN TỈNH ...          CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
        -------                            Độc lập - Tự do - Hạnh phúc
                                                   ---------------
   Số:.../20.../NQ-HĐND                    ..., ngày...tháng...năm 20...

                            NGHỊ QUYẾT
                          ...(tên gọi)...

Căn cứ Luật Tổ chức chính quyền địa phương ngày ... tháng ... năm ...;
Căn cứ ...;
Xét Tờ trình ...; Báo cáo thẩm tra của ...; ý kiến thảo luận của đại
biểu Hội đồng nhân dân tại kỳ họp;

Hội đồng nhân dân ban hành Nghị quyết ...(tên gọi)...

Điều 1. (Tên của điều)
1. ...
   a) ...
Điều ... (Tên của điều)
...

Nghị quyết này đã được Hội đồng nhân dân ...Khóa...Kỳ họp thứ... thông
qua ngày...tháng...năm...

                                                          CHỦ TỊCH
Nơi nhận:                                              (Chữ ký, dấu)
- ...;
- Lưu: VT, ...
                                                          Họ và tên
```

## Cách sinh bằng `generate_docx.py`

Dùng `"profile": "administrative"` như bình thường (margin trùng khoảng), thêm 2 điểm khác:
1. `header.co_quan_chu_quan` để trống (không có dòng "cơ quan chủ quản" cho HĐND).
2. Body item mới `{"type": "italic_paragraph", "text": "Nghị quyết này đã được..."}` cho dòng
   đóng — KHÁC NĐ30, chưa có trong schema `body` types trước bản này.

Ví dụ đầy đủ: [`examples/nghi_quyet_hdnd.json`](../examples/nghi_quyet_hdnd.json).

⚠️ **Validate:** `validate_docx.py` hiện tại kiểm theo mặc định NĐ30 (mong đợi "V/v" hoặc tên loại
chuẩn hành chính) — CHƯA có profile riêng cho VBQPPL. Dùng `--profile administrative` sẽ báo một
số cảnh báo không chính xác 100% cho VBQPPL (vd không nhận diện "NGHỊ QUYẾT" như tên loại chuẩn).
Đây là nợ kỹ thuật đã biết — coi kết quả validate là THAM KHẢO, vẫn phải soi mắt kỹ hơn cho VBQPPL
so với văn bản hành chính thường.
