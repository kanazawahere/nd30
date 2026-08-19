#!/usr/bin/env bash
# Đóng gói skill /nd30 thành .zip đúng chuẩn upload Gemini Spark.
# Spark chỉ nhận: .txt .md .rst .rtf .tex .log .py .sh .json .yaml .csv .toml .xml .env .sql (<=100MB)
# → .docx trong templates/ BỊ LOẠI (Spark không nhận), thay bằng hướng dẫn tự sinh lại từ script.
# Chạy: bash .claude/skills/nd30/pack-for-spark.sh   → /tmp/nd30-spark.zip
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE="/tmp/nd30-spark"
OUT="/tmp/nd30-spark.zip"

rm -rf "$STAGE" "$OUT"
mkdir -p "$STAGE/nd30"

# Chỉ copy định dạng Spark nhận
cd "$SRC"
find . -type f \
  \( -name '*.md' -o -name '*.txt' -o -name '*.py' -o -name '*.sh' \
     -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.toml' \
     -o -name '*.csv' -o -name '*.xml' -o -name '*.sql' \) \
  ! -path './.pytest_cache/*' ! -path './__pycache__/*' ! -path '*/__pycache__/*' \
  ! -path './tests/fixtures/*' \
  -exec cp --parents {} "$STAGE/nd30/" \;

# Ghi chú thay cho templates/*.docx bị loại
cat > "$STAGE/nd30/templates/README-docx.md" <<'EOF'
# Vì sao không có file .docx ở đây

Gemini Spark không nhận upload `.docx`, nên bộ mẫu .docx đã bị loại khỏi gói này.

Cần mẫu rỗng thì tự sinh lại trong sandbox:

```bash
pip install python-docx
python3 templates/_build_templates.py      # sinh to-trinh / cong-van / quyet-dinh / ke-hoach / bao-cao
```

Hoặc tải bản .docx dựng sẵn từ repo canonical:
https://github.com/kanazawahere/nd30/tree/main/templates
EOF

# dùng python zipfile (máy fleet có thể không có `zip`)
cd "$STAGE" && python3 -m zipfile -c "$OUT" nd30
echo "✓ $OUT  ($(du -h "$OUT" | cut -f1))"
echo "  file: $(cd "$STAGE" && find nd30 -type f | wc -l)"
echo "  SKILL.md ở root gói: $([ -f "$STAGE/nd30/SKILL.md" ] && echo CÓ || echo 'THIẾU ← Spark sẽ từ chối')"
echo
echo "Nạp vào Spark: sidebar Skills → Create/Upload → chọn $OUT"
echo "Sau khi nạp, hỏi Spark 'skill nd30 version bao nhiêu?' → phải khớp:"
grep -o 'SKILL_VERSION: .*' "$SRC/SKILL.md" | head -1
