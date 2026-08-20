<!-- nha-van:exempt — AI エージェント/開発者向けの技術ドキュメント。本文中の例は空白のテンプレートであり、実際に発行される文書ではない -->
# nd30 — ベトナム行政文書フォーマットエンジン

([Tiếng Việt](./README.md) | [English](./README.en.md) | [中文](./README.zh.md) | 日本語)

[![release](https://img.shields.io/github/v/release/kanazawahere/nd30?label=release)](https://github.com/kanazawahere/nd30/releases)
[![license](https://img.shields.io/github/license/kanazawahere/nd30)](./LICENSE)
[![tests](https://img.shields.io/badge/tests-24%20passing-brightgreen)](./tests)
[![last commit](https://img.shields.io/github/last-commit/kanazawahere/nd30)](https://github.com/kanazawahere/nd30/commits/main)

ベトナムの**政令 30/2020/NĐ-CP号**の書式（フォント、サイズ、mm単位の余白、各構成要素の正確な
位置）に準拠した編集可能な `.docx` ファイルを生成し、納品前に**スクリプトで自己検証**する
AIスキルです。「行政文書らしく見えるだけの生テキスト」ではありません。

**Claude Code、Gemini（アプリ/Spark）、Gemini CLI** で動作するほか、Pythonスクリプトを直接
使うこともできます。MCPもサーバー構築も不要です。

## できること

- **27種類以上の文書タイプを分類**（公文書、上申書、決定書、計画書、報告書、通知、議事録、
  招待状、投票用紙など）— ユーザーの自然な話し方から判断します。
- **作成前にデータをヒアリング** — 文書タイプごとに専用の質問セットを用意し、推測や捏造を
  避けます。
- **正しい書式で `.docx` を生成**：A4サイズ、Times New Roman、左余白30–35mm／右余白15–20mm／
  上下余白20–25mm、罫線非表示の2カラムヘッダー（左に発行機関名、右に国号・標語）、ローマ数字
  →算用数字→アルファベット→ハイフンの階層構造、宛先グループ（「報告用」／「協力用」／
  「保管：VT」）、署名ブロック。
- **自動検証**：用紙サイズ、余白、フォント・色（表やヘッダー・フッター内も含む）、文書タイプ
  ごとの必須要素、Wordの自動箇条書き（政令30号では禁止）、余白をはみ出した表、未入力の
  プレースホルダー。
- **機関独自テンプレートの学習**：機関が独自の `.docx` テンプレートを持っている場合、そちらが
  スキルのデフォルトより優先されます。

## 3つの絶対ルール

**1. 捏造しない。** 文書番号・記号、法的根拠、署名者、金額、発行日、議決結果、統計データなどは
すべて `[要補足：...]` というプレースホルダーのままにし、ユーザーに入力してもらいます。AI が
自ら決めてよいのは、行政的な言い回し・構成・レイアウトのみです。

**2. 文書タイプごとに正しい法令を適用する** — 政令30号がすべてをカバーしているわけではありません：

| タイプ | 準拠する規定 |
|---|---|
| 行政文書（公文書、上申書、個別決定、計画書、報告書など） | **政令 30/2020/NĐ-CP号** ✅ 本リポジトリ |
| 法規範文書（省人民評議会決議、省人民委員会の規範的決定・指示、通達など） | **政令 78/2025号 + 187/2025号** — 独自の書式であり、政令30号のテンプレートを流用しない |
| 党組織の文書（省委員会、県委員会、党委員会、党の各部門） | **指導文書 36-HD/VPTW号** — 本リポジトリは未対応、先に確認が必要 |

**3. 一部しか適用していない場合、「政令30号準拠」と言い切らない。** どの部分を適用し、
どこがまだプレースホルダーのままかを明確に伝えます。

## 使い方

### Gemini（アプリまたはSpark）を使う場合 — インストール不要
Geminiに以下を貼り付けてください：

> https://github.com/kanazawahere/nd30 のスキルを使って、[やりたいこと] についての
> [文書タイプ] を作成し、.docx ファイルとして出力してください。

Geminiがリポジトリを自ら読み込み、不足している情報を尋ねたうえで、サンドボックス内で
`.docx` ファイルを作成します。

### Claude Codeを使う場合
skillsフォルダにクローンして `/nd30` を呼び出します：
```bash
git clone https://github.com/kanazawahere/nd30.git ~/.claude/skills/nd30
```

### スクリプトを直接使う場合（AI不要）
```bash
pip install python-docx
python3 scripts/validate_docx.py <file.docx> --profile administrative   # 既存ファイルの書式を検証
python3 scripts/inspect_docx.py  <file.docx>                            # 実際の数値を確認（余白、フォント、サイズ）
python3 scripts/learn_template.py <機関テンプレート.docx>                # 機関のテンプレートから書式を抽出
```

`templates/` に5種類の空テンプレートがあります：上申書、公文書、決定書、計画書、報告書。

`generate_docx.py` への入力は
[`schemas/nd30-input.schema.json`](./schemas/nd30-input.schema.json) のJSON Schemaに従います —
AIエージェントがフィールド漏れや型違いのないJSONを生成できるようにするためのもので、完全な例は
[`examples/input-sample.json`](./examples/input-sample.json) にあります。

ファイル出力に対応していないチャットのみの環境向けには、
[`references/hien-thi-markdown-fallback.md`](./references/hien-thi-markdown-fallback.md) に
2カラムMarkdown表によるプレビュー方法を記載しています。

## 構成

```
SKILL.md            # AIエージェント向けエントリーポイント — 5フェーズのワークフロー
llms.txt            # AIエージェント向け索引ファイル（推奨読み順）
schemas/            # generate_docx.py の入力用JSON Schema
examples/           # 完全なサンプル入力JSON
references/         # 政令30号の仕様、27種類以上の文書タイプ一覧、ヒアリング項目、チェックリスト
scripts/            # build / validate / inspect / learn-template / fill-template / generate（JSON駆動）
templates/          # 5つの空.docxテンプレート、それぞれ単独で検証をパス
assets/samples/     # 教材用サンプルスクリプト（build_to_trinh_thon_thong_minh.py）
tests/              # pytest
```

## テスト

```bash
pip install python-docx pytest pyyaml
python3 -m pytest tests/ -v
```

## 既知の制限

- **各構成要素のフォントサイズ**はスクリプトで確実に検証できません（python-docxの
  スタイル継承の読み取りが不安定なため）→ 目視確認が必要、詳細は
  `references/validation-checklist.md` を参照。
- **党文書の書式**（指導文書 36-HD/VPTW号）および**法規範文書の書式**（政令78/2025号、
  187/2025号）は未対応。
- 電子署名・公印には非対応 — それぞれの機関の文書管理プロセスに委ねます。

## 出典

業務ロジック部分（文書タイプ一覧、ヒアリング項目、ビルダー/バリデーターの基盤）は
[biencuong/vbhc](https://github.com/biencuong/vbhc) から継承 — Unlicense（パブリックドメイン）
ライセンスで、MITへの再ライセンスと互換性があります。書式仕様は**政令30/2020/NĐ-CP号
付録I**から直接引用（公開の法令であり、個人・団体の著作物ではありません）。

## ライセンス

MIT — [LICENSE](./LICENSE) を参照。
