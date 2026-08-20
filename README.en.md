<!-- nha-van:exempt — technical README for AI agents/devs, examples are blank illustrative templates, not real outgoing documents -->
# nd30 — Vietnamese Administrative Document Formatting Engine

([Tiếng Việt](./README.md) | English | [中文](./README.zh.md) | [日本語](./README.ja.md))

[![release](https://img.shields.io/github/v/release/kanazawahere/nd30?label=release)](https://github.com/kanazawahere/nd30/releases)
[![license](https://img.shields.io/github/license/kanazawahere/nd30)](./LICENSE)
[![tests](https://img.shields.io/badge/tests-24%20passing-brightgreen)](./tests)
[![last commit](https://img.shields.io/github/last-commit/kanazawahere/nd30)](https://github.com/kanazawahere/nd30/commits/main)

An AI skill that produces **editable `.docx` files formatted per Vietnamese Decree 30/2020/NĐ-CP**
(font, size, margins in mm, exact position of every component) and **self-validates via script**
before handing off — not "text that merely looks like an administrative document."

Works with **Claude Code, Gemini (app/Spark), Gemini CLI**, or plain Python scripts. No MCP, no
server required.

## What it does

- **Classifies 27+ document types** (official letters, proposals, decisions, plans, reports,
  notices, minutes, invitations, voting ballots…) from how the user naturally phrases the request.
- **Interviews for data before drafting** — a dedicated question set per document type, instead of
  guessing and fabricating.
- **Generates `.docx`** to spec: A4, Times New Roman, left margin 30–35mm / right 15–20mm /
  top-bottom 20–25mm, borderless-2-column header (issuing body on the left, National
  Emblem/Motto on the right), Roman numeral → digit → letter → dash hierarchy, recipient grouping
  (`for reporting` / `for coordination` / `filed: VT`), signature block.
- **Auto-validates**: paper size, margins, font/color (including inside tables and
  headers/footers), required components per document type, auto-bullets (Decree 30 forbids
  them), tables overflowing the margin, and leftover placeholders.
- **Learns from an agency's own template**: if the agency already has its own `.docx` template,
  it wins over the skill's defaults.

## 3 hard rules

**1. Never fabricate.** Document number/code, legal basis, signer, amounts, issue date, voting
outcome, statistics → always left as `[NEEDS INPUT: ...]` for the user to fill in. The AI may only
decide administrative phrasing, structure, and layout.

**2. Match the law to the document type** — Decree 30 doesn't cover everything:

| Type | Formatted per |
|---|---|
| Administrative documents (official letters, proposals, individual decisions, plans, reports…) | **Decree 30/2020/NĐ-CP** ✅ this repo |
| Legal normative documents (provincial People's Council resolutions, provincial People's Committee normative decisions/directives, circulars…) | **Decree 78/2025 + Decree 187/2025** — separate format, don't reuse the Decree 30 template |
| Communist Party bodies (provincial/district Party committees, Party commissions) | **Guidance 36-HD/VPTW** — not yet covered by this repo, must ask first |

**3. Never claim "Decree-30-compliant" when only partially applied.** State clearly what was
applied and what's still a placeholder.

## How to use

### With Gemini (app or Spark) — nothing to install
Paste this into Gemini:

> Use the skill at https://github.com/kanazawahere/nd30 to draft me a [document type] about [the
> task], export a .docx file.

Gemini will read the repo itself, ask for any missing information, then create the `.docx` file
in its own sandbox.

### With Claude Code
Clone into the skills folder and invoke `/nd30`:
```bash
git clone https://github.com/kanazawahere/nd30.git ~/.claude/skills/nd30
```

### Using the scripts directly (no AI needed)
```bash
pip install python-docx
python3 scripts/validate_docx.py <file.docx> --profile administrative   # check an existing file's formatting
python3 scripts/inspect_docx.py  <file.docx>                            # inspect real measurements (margins, font, size)
python3 scripts/learn_template.py <agency-template.docx>                # extract formatting from an agency's own template
```

Blank templates are available in `templates/`: proposal, official letter, decision, plan, report.

Input for `generate_docx.py` follows the JSON schema at
[`schemas/nd30-input.schema.json`](./schemas/nd30-input.schema.json) — lets an AI agent generate
JSON without missing fields or wrong types; a complete example is at
[`examples/input-sample.json`](./examples/input-sample.json).

For chat-only environments that can't produce a file yet, see the 2-column Markdown preview
layout at [`references/hien-thi-markdown-fallback.md`](./references/hien-thi-markdown-fallback.md).

## Structure

```
SKILL.md            # entry point for AI agents — 5-phase workflow
llms.txt            # index file for AI agents (recommended reading order)
schemas/            # JSON Schema for generate_docx.py input
examples/           # complete sample input JSON
references/         # Decree 30 specs, 27+ document type catalog, interview questions, checklist
scripts/            # build / validate / inspect / learn-template / fill-template / generate (JSON-driven)
templates/          # 5 blank .docx templates, each passes validation on its own
assets/samples/     # teaching example script (build_to_trinh_thon_thong_minh.py)
tests/              # pytest
```

## Testing

```bash
pip install python-docx pytest pyyaml
python3 -m pytest tests/ -v
```

## Known limitations

- **Per-component font size** can't be reliably checked by script (python-docx reads style
  inheritance unreliably) → still needs a manual look, documented in
  `references/validation-checklist.md`.
- **Legal normative documents**: has an MVP for HĐND (People's Council) resolutions (Mẫu 17+18,
  see `references/the-thuc-qppl-nq-hdnd.md`) and provincial People's Committee decisions (Mẫu
  19+20, see `references/the-thuc-qppl-qd-ubnd.md`) — laws, ordinances, National Assembly
  resolutions, presidential orders/decisions, government decrees, and circulars are not yet
  covered.
- Does not yet cover **Party document formatting** (Guidance 36-HD/VPTW).
- No digital signature / seal support — that belongs to the agency's own records-management
  process.

## FAQ

**Is this repo complete, or do you still need more code/prompts/templates?**
It's complete. `SKILL.md` is already a full system prompt (3 hard rules + 5-phase workflow),
`scripts/build_docx.py` + `generate_docx.py` are already the `.docx` generation engine, and
`templates/*.docx` are real files (not Markdown skeletons). Before suggesting "add file X" —
**open the file in the repo and read it first**, and check the "already done — don't re-suggest"
table at the top of [`llms.txt`](./llms.txt).

**I'm an AI/agent that can only read the GitHub landing page (can't fetch the file tree) — how do I use this?**
This is a measured, real limitation (see the "2 CHẾ ĐỘ CHẠY" section in `SKILL.md`): the GitHub
landing page only shows this README, it doesn't automatically surface `SKILL.md`/`scripts/`. You
need to **actively fetch** each raw file
(`https://raw.githubusercontent.com/kanazawahere/nd30/main/<path>`), starting with
[`llms.txt`](./llms.txt) then `SKILL.md`. If your platform can't fetch links on its own, the user
should paste `SKILL.md`'s content directly into the chat.

**Why no MCP server?**
By design — this skill is plain Python scripts, runnable by pasting a link/content into any AI
chat with a code sandbox (Gemini, Claude, ChatGPT...), no extra infrastructure to install or host.

**How do I know I'm reading the latest version, not a cached one?**
Ask the AI "what's the nd30 SKILL_VERSION?" — the number returned must match the `SKILL_VERSION`
line in [`SKILL.md`](./SKILL.md). A mismatch means it's reading a cached copy (see the GitHub raw
CDN cache warning in `SKILL.md`).

**Why are margins/fonts given as "20-25mm" instead of one fixed number?**
Because Decree 30/2020/NĐ-CP's Phụ lục I specifies RANGES, not single fixed values — quoted
directly from the legal text, not an invented single number.

## Provenance

The business-logic portion (document type catalog, interview questions, builder/validator
foundation) is inherited from [biencuong/vbhc](https://github.com/biencuong/vbhc) — licensed
Unlicense (public domain), compatible with relicensing to MIT. Formatting specs are taken
directly from **Phụ lục I of Decree 30/2020/NĐ-CP** (a public legal document, not owned by any
individual or organization).

## License

MIT — see [LICENSE](./LICENSE).
