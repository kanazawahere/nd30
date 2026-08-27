<!-- nha-van:exempt — 面向 AI agent/开发者的技术说明文档，文中示例为空白模板，非真实发文 -->
# nd30 — 越南行政公文格式引擎

([Tiếng Việt](./README.md) | [English](./README.en.md) | 中文 | [日本語](./README.ja.md))

[![release](https://img.shields.io/github/v/release/kanazawahere/nd30?label=release)](https://github.com/kanazawahere/nd30/releases)
[![license](https://img.shields.io/github/license/kanazawahere/nd30)](./LICENSE)
[![tests](https://img.shields.io/badge/tests-24%20passing-brightgreen)](./tests)
[![last commit](https://img.shields.io/github/last-commit/kanazawahere/nd30)](https://github.com/kanazawahere/nd30/commits/main)

一个 AI 技能，用于生成**符合越南《30/2020/NĐ-CP 号政府议定》格式规范的可编辑 `.docx` 文件**——字体、
字号、页边距（毫米）、每个组成部分的精确位置——并在交付前**通过脚本自我校验**，而不是"看起来像"
行政公文的粗糙文本。

可在 **Claude Code、Gemini（网页版/Spark）、Gemini CLI** 中运行，也可直接用 Python 脚本，无需 MCP，
无需搭建服务器。

## 功能

- **识别 27 种以上公文类型**（公函、请示、决定、计划、报告、通知、会议纪要、邀请函、表决票……），
  根据用户日常表达方式自动判断。
- **先访谈收集数据再起草**——每种公文类型都有专属问题清单，而不是靠猜测编造。
- **生成符合规范的 `.docx`**：A4 纸张、Times New Roman 字体，左边距 30–35mm / 右边距 15–20mm /
  上下边距 20–25mm，隐藏边框的双栏页眉（左侧为发文机关，右侧为国号/格言），罗马数字→阿拉伯数字→
  字母→破折号的层级结构，收件方分组（"抄送"/"协办"/"存档：VT"），签署区块。
- **自动校验**：纸张尺寸、页边距、字体/颜色（包括表格与页眉页脚内）、各类型公文的必备要素、
  Word 自动项目符号（30 号议定禁止使用）、超出页边距的表格，以及遗留的占位符。
- **学习机关自有模板**：若机关已有自己的 `.docx` 模板，则以该模板为准，优先于本技能的默认设置。

## 3 条硬性规则

**1. 绝不编造。** 公文字号、法律依据、签署人、金额、发文日期、表决结果、统计数据等——一律留空
写作 `[需补充：...]`，由用户自行填写。AI 只能自行决定行政措辞、结构与排版格式。

**2. 不同类型公文对应不同法律依据**——30 号议定并未覆盖所有情形：

| 类型 | 依据规范 |
|---|---|
| 行政公文（公函、请示、个别决定、计划、报告……） | **30/2020/NĐ-CP 号议定** ✅ 本仓库 |
| 规范性法律文件（省人民议会决议、省人民委员会规范性决定/指示、通知……） | **78/2025 + 187/2025 号议定**——独立格式规范，不可套用 30 号议定模板 |
| 党组织公文（省委、县委、党委、党委各部门） | **36-HD/VPTW 号指导文件**——本仓库尚未覆盖，需先询问 |

**3. 仅部分符合规范时，不得声称"完全符合 30 号议定"。** 需明确说明已应用哪些部分、
还有哪些占位符待填写。

## 使用方法

### 通过 Gemini（网页版或 Spark）——无需安装
在 Gemini 中粘贴以下内容：

> 使用 https://github.com/kanazawahere/nd30 上的 skill，帮我起草一份关于 [具体事项] 的
> [公文类型]，导出 .docx 文件。

Gemini 会自行读取本仓库，询问缺失信息，然后在其沙盒环境中生成 `.docx` 文件。

### 通过 Claude Code
克隆到 skills 目录后调用 `/nd30`：
```bash
git clone https://github.com/kanazawahere/nd30.git ~/.claude/skills/nd30
```

### 直接使用脚本（无需 AI）
```bash
pip install python-docx
python3 scripts/validate_docx.py <file.docx> --profile administrative   # 校验现有文件格式
python3 scripts/inspect_docx.py  <file.docx>                            # 检查真实参数（页边距、字体、字号）
python3 scripts/learn_template.py <机关模板.docx>                        # 从机关模板中提取格式规则
```

`templates/` 目录中提供 5 种空白模板：请示、公函、决定、计划、报告。

`generate_docx.py` 的输入遵循 JSON Schema，见
[`schemas/nd30-input.schema.json`](./schemas/nd30-input.schema.json)——帮助 AI agent 生成不缺字段、
类型正确的 JSON，完整示例见 [`examples/input-sample.json`](./examples/input-sample.json)。

若所在环境暂不支持下载文件（仅聊天界面），可用 Markdown 双栏表格预览排版，详见
[`references/hien-thi-markdown-fallback.md`](./references/hien-thi-markdown-fallback.md)。

## 目录结构

```
SKILL.md            # AI agent 入口文件 — 5 阶段流程
llms.txt            # AI agent 索引文件（建议阅读顺序）
schemas/            # generate_docx.py 输入的 JSON Schema
examples/           # 完整的示例输入 JSON
references/         # 30 号议定参数、27+ 公文类型目录、访谈问题、检查清单
scripts/            # build / validate / inspect / learn-template / fill-template / generate（JSON 驱动）
templates/          # 5 个空白 .docx 模板，均可独立通过校验
assets/samples/     # 教学示例脚本（build_to_trinh_thon_thong_minh.py）
tests/              # pytest
```

## 测试

```bash
pip install python-docx pytest pyyaml
python3 -m pytest tests/ -v
```

## 已知局限

- **各组成部分的字号**尚无法通过脚本可靠校验（python-docx 读取样式继承关系不够稳定）→ 仍需人工
  核对，详见 `references/validation-checklist.md`。
- **规范性法律文件**：已有人民议会决议（Mẫu 17+18，见 `references/the-thuc-qppl-nq-hdnd.md`）和
  省人民委员会决定（Mẫu 19+20，见 `references/the-thuc-qppl-qd-ubnd.md`）的 MVP——法律、法令、
  国会决议、国家主席令/决定、政府议定、通知尚未覆盖。
- 尚未覆盖**党组织公文格式**（36-HD/VPTW 号指导文件）。
- 不支持数字签名/公章——这部分属于机关自身的公文管理流程。

## 常见问题

**本仓库是否已完整？还需要补充代码/提示词/模板吗？**
已经完整。`SKILL.md` 本身就是完整的系统提示词（3 条硬性规则 + 5 阶段流程），
`scripts/build_docx.py` + `generate_docx.py` 已是 `.docx` 生成引擎，`templates/*.docx` 是真实文件
（不是 Markdown 骨架）。在建议"再加个 X 文件"之前——**请先打开仓库中的文件阅读**，并对照
[`llms.txt`](./llms.txt) 开头的"已完成——勿重复建议"表格。

**我是只能读取 GitHub 首页（无法抓取文件树）的 AI/agent，该怎么用？**
这是已实测的真实限制（见 `SKILL.md` 的"2 CHẾ ĐỘ CHẠY"一节）：GitHub 首页只显示这份 README，
不会自动展示 `SKILL.md`/`scripts/` 的内容。你需要**主动抓取**每个 raw 文件
（`https://raw.githubusercontent.com/kanazawahere/nd30/main/<路径>`），从
[`llms.txt`](./llms.txt) 开始，再读 `SKILL.md`。若你的平台无法自动抓取链接，请让用户直接把
`SKILL.md` 内容粘贴到对话框中。

**为什么不用 MCP 服务器？**
这是有意为之——本技能就是纯 Python 脚本，只需把链接/内容粘贴到任何带代码沙盒的 AI 对话
（Gemini、Claude、ChatGPT……）即可运行，无需额外安装或搭建基础设施。

**如何确认自己读到的是最新版本，而不是缓存的旧版？**
问 AI"nd30 的 SKILL_VERSION 是多少？"——返回的编号必须与 [`SKILL.md`](./SKILL.md) 中的
`SKILL_VERSION` 一致。不一致说明读到了缓存版本（见 `SKILL.md` 中关于 GitHub raw CDN 缓存的提示）。

**为什么页边距/字号写的是"20-25mm"这种范围，而不是固定数值？**
因为《30/2020/NĐ-CP 号议定》附录一规定的就是一个范围，不是单一固定值——直接引自法律原文，
不是自行编造的单一数字。

## 来源说明

业务逻辑部分（公文类型目录、访谈问题、构建器/校验器基础）继承自
[biencuong/vbhc](https://github.com/biencuong/vbhc)——采用 Unlicense（公有领域）许可，可兼容
转授权为 MIT。格式规范直接摘自**30/2020/NĐ-CP 号议定附录一**（公开法律文件，不属于任何个人
或组织的版权）。

## 许可证

MIT — 见 [LICENSE](./LICENSE)。
