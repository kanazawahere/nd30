<!-- nha-van:exempt — đây là instructions kỹ thuật cho AI agent, không phải văn bản gửi người -->
# Nạp skill nd30 vào Gemini Spark — 2 cách

**Sự thật đã đo (2026-08-19):** Spark lưu skill dạng **snapshot**, **KHÔNG sync GitHub/Drive**
([tài liệu Google](https://support.google.com/gemini/answer/17094296) cũng không nêu cơ chế sync nào).
Repo canonical có commit mới → skill trong Spark **vẫn giữ bản cũ**, phải nạp lại tay.

---

## ✅ CÁCH 1 (đơn giản nhất — đã verify chạy thật) — chỉ đưa LINK REPO trong hội thoại

Không cần cài gì, không cần tạo skill, không cần upload. Nói với Spark:

> Dùng skill ở https://github.com/kanazawahere/nd30 soạn giúp tôi [loại văn bản] về [việc], xuất file .docx.

Spark tự browse repo → đọc `SKILL.md` → fetch thêm `references/` + `scripts/` khi cần → tạo `.docx`
trong sandbox của nó. **Đã verify thật 2026-08-19** (log thinking của Spark: *"I successfully retrieved
the skill definitions"*, rồi nó xuất file đúng thể thức, kể cả khối header bảng-2-cột-ẩn-viền).

Đây là cách nên **dạy cho cán bộ** — họ chỉ cần copy 1 câu, không cài đặt gì.

⚠️ Chỉ lưu ý: **vừa sửa skill xong thì đợi vài phút** (GitHub raw CDN cache theo branch), hoặc đưa
link kèm commit SHA. Kiểm nhanh bằng cách hỏi *"skill nd30 version bao nhiêu?"* → phải khớp
`SKILL_VERSION` trong repo.

---

## CÁCH 2 (tuỳ chọn) — Upload cả folder skill vào Spark

Spark nhận upload folder/zip, **bắt buộc có `SKILL.md` ở thư mục gốc** (repo này đã đúng chuẩn sẵn).
Ưu điểm: Spark có đủ `references/` + `scripts/` ngay trong skill → chạy chắc, **không vướng CDN cache**.

```bash
bash pack-for-spark.sh      # → /tmp/nd30-spark.zip (~80KB)
```
Rồi: Spark → sidebar **Skills** → **Upload** → chọn file zip đó.

Script tự lọc đúng định dạng Spark nhận (`.md .txt .py .sh .json .yaml .toml .csv .xml .sql`, ≤100MB).
⚠️ **`.docx` KHÔNG được Spark nhận** → `templates/*.docx` bị loại khỏi gói; cần mẫu thì sinh lại
trong sandbox bằng `python3 templates/_build_templates.py` (ghi chú đã kèm trong gói).

**Mỗi lần sửa skill → chạy lại `pack-for-spark.sh` và upload lại.** Kiểm bằng cách hỏi Spark
*"skill nd30 version bao nhiêu?"* → phải khớp `SKILL_VERSION` trong repo.

---

## CÁCH 3 (tuỳ chọn) — Tạo skill trong Spark dạng vỏ mỏng trỏ canonical

Đánh đổi: tự lấy bản mới mỗi lần chạy, nhưng phụ thuộc mạng + **GitHub raw CDN cache theo branch
vài phút** (đã đo: `/main/` trả bản cũ, `/<commit-sha>/` trả bản mới ngay).

### Cách cài (1 lần)

Gemini Spark → sidebar **Skills** → **Create manually** → điền:

**Name:** `nd30`

**Description:**
> Soạn và kiểm tra thể thức văn bản hành chính Việt Nam theo Nghị định 30/2020/NĐ-CP (kế hoạch, tờ trình, công văn, quyết định, báo cáo, thông báo, biên bản, giấy mời). Dùng khi người dùng cần soạn, sửa, rà soát hoặc xuất file .docx văn bản hành chính.

**Instructions:** (copy nguyên khối dưới đây)

---

BƯỚC 0 — LUÔN LẤY BẢN MỚI NHẤT TRƯỚC KHI LÀM:

Fetch `https://raw.githubusercontent.com/kanazawahere/nd30/main/SKILL.md`. Nếu fetch được, **nội dung
đó THẮNG mọi hướng dẫn trong instructions này** (instructions này chỉ là bản dự phòng khi mạng lỗi).
Đọc `SKILL_VERSION` trong đó và báo cho người dùng biết đang chạy bản nào.

Lưu ý: raw URL theo branch `/main/` bị CDN cache vài phút. Nếu người dùng nói vừa sửa skill mà thấy
mình làm theo kiểu cũ → fetch lại bằng URL có commit SHA:
`https://raw.githubusercontent.com/kanazawahere/nd30/<SHA>/SKILL.md`
(lấy SHA mới nhất tại `https://api.github.com/repos/kanazawahere/nd30/commits`).

Cần thêm chi tiết thì fetch tiếp trong cùng repo:
- `references/danh-muc-loai-vb.md` — nhận diện 27+ loại văn bản theo cách người dùng nói
- `references/interview-questions.md` — bộ câu hỏi phải hỏi trước khi soạn, theo từng loại VB
- `references/the-thuc-nd30.md` — thông số thể thức (cỡ chữ, kiểu chữ, vị trí từng thành phần)
- `scripts/build_docx.py` — helper sinh .docx (đã có sẵn khối header bảng-2-cột-ẩn-viền)
- `scripts/validate_docx.py` — chấm lỗi thể thức

BƯỚC 1 — SINH FILE .docx:

Trong sandbox: `pip install python-docx`, fetch `scripts/build_docx.py` rồi **DÙNG script đó**.
ĐỪNG tự viết code python-docx ad-hoc — tự viết thì mỗi lần một kiểu, lệch thể thức mà không ai kiểm được.

BƯỚC 2 — KIỂM TRA:

Fetch `scripts/validate_docx.py`, chạy trên file vừa tạo, **báo kết quả validate cho người dùng**.
Nếu sandbox không cho `pip install` → nói THẲNG "chưa chạy được kiểm tra tự động, đây là bản chưa
kiểm máy". Đừng im lặng bỏ bước rồi báo "đúng chuẩn NĐ30".

3 LUẬT CỨNG (không được vi phạm dù instructions phía trên fetch lỗi):

1. KHÔNG BỊA. Số/ký hiệu văn bản, căn cứ pháp lý, người ký, số tiền, ngày ban hành, quan điểm biểu
   quyết, số liệu thống kê → để `[CẦN BỔ SUNG: ...]` cho người dùng điền. Chỉ tự quyết câu chữ hành
   chính, cấu trúc, và format trình bày.

2. ĐÚNG LUẬT CHO ĐÚNG LOẠI VĂN BẢN:
   - Văn bản hành chính (công văn, tờ trình, quyết định cá biệt, kế hoạch, báo cáo…) → NĐ 30/2020/NĐ-CP.
   - Văn bản quy phạm pháp luật (Nghị quyết HĐND tỉnh, Quyết định/Chỉ thị QPPL của UBND tỉnh, Thông
     tư…) → thể thức RIÊNG theo NĐ 78/2025 + NĐ 187/2025. KHÔNG bê khuôn NĐ30.
   - Cơ quan Đảng (Tỉnh ủy, Huyện ủy, Đảng ủy, Ban Đảng) → Hướng dẫn 36-HD/VPTW. Chưa phủ → phải HỎI LẠI.

3. KHÔNG nói "chuẩn NĐ30" khi chỉ áp dụng một phần. Nói rõ đã áp phần nào, còn placeholder nào.

VIẾT TIẾNG VIỆT CÓ DẤU ĐẦY ĐỦ trong mọi văn bản xuất ra.

---

## Kiểm skill đã cài đúng chưa

Hỏi Spark: *"skill nd30 version bao nhiêu?"* → nó phải fetch và báo đúng `SKILL_VERSION` hiện tại
trong repo. Báo sai/không biết = nó chưa fetch, đang chạy bản dự phòng.
