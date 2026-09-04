# rfx1427-finance

> **⚠️ PERSONAL-USE TOOL**
> Built for my own personal use and for fun. Not a product. Not financial advice.
> Not production-ready. If you found this, you are welcome to read it, but I am
> not recommending anyone use it. Use at your own risk.

A read-only AI financial news scanner. Python fetches data; the AI judges and
renders the locked report. Four phases. No monitoring, no automation, no trading.

## What is in this repo

| Layer | What it is | Where |
|-------|------------|-------|
| Skill framework | Master rules, locked formats, 4-phase flow | `SKILL.md`, `references/*.md` |
| Python fetch layer | News, market data, SEC EDGAR → JSONL | `src/rfx1427/phase{1,2,3}.py` |
| Python package | Installable via `pip install -e .` | `pyproject.toml` |
| AI agent interface | Claude Code / OpenAI hooks | `agents/{claude,openai}.yaml` |

**Category:** Skill framework with a Python fetch engine packaged as a library.
The skill is the main thing. Python is the engine. The library is how the engine
is distributed.

## 4 phases

| Phase | What | Python | Reference |
|-------|------|--------|-----------|
| 1. Scanner | Fetch news, output 7–10 positive opportunities (WAJIB 7, target 10) | `phase1.py` | `references/phase1-scanner.md` |
| 2. Deep Analysis | Market data via user-selected Primary Tool | `phase2.py` | `references/phase2-deep-analysis.md` |
| 3. SEC EDGAR | Verify via official SEC API (mandatory) | `phase3.py` | `references/phase3-sec-edgar.md` |
| 4. Weekly Bias | AI-only summary (locked format) | — | `references/phase4-weekly-bias.md` |

## Quick start

```bash
pip install -e .
python -m rfx1427.phase1 --list-sources
python -m rfx1427.phase1 --source finviz --market US --limit 20
```

Or via installed entry-points: `rfx1427-phase1`, `rfx1427-phase2`, `rfx1427-phase3`.

> **Python:** requires ≥3.10 · tested on 3.12 · Python 3.14 missing wheels for `pandas`/`lxml` (use 3.12).

## Gate 0 (intake)

Two questions only, asked one at a time:

1. **Language** — `English` (default) / `Bahasa Melayu` / `Other`
2. **Trader profile** — `Scalper` / `Intraday` / `Swing` / `Investor`

**Market is locked to US.** No question is asked for it. Non-US markets return
`FALLBACK_NEEDED` with `error_code="MARKET_NOT_SUPPORTED"`.

## Hard rules (top 5)

1. **No fabrication.** Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when data is missing.
2. **Positive-only Phase 1.** Discard negative / mixed / neutral.
3. **WAJIB 7, target 10.** Staged 50→70→100 fetch with early-stop. Never lower thresholds.
4. **One question at a time** in Gate 0.
5. **Phase 3 auto-proceeds.** Phase 1 and Phase 2 wait for user opt-in; Phase 3 runs automatically after Phase 2.

Full rule list: `references/hard-rules-master.md` (39 rules) and `SKILL.md`.

## Output formats (locked)

| Phase | Format | File |
|-------|--------|------|
| 1 | `## CARD [N] — [TICKER]` table (7–10) | `references/phase1-scanner.md` |
| 2 | `## Primary Data Summary` blocks | `references/phase2-deep-analysis.md` |
| 3 | `**PHASE 3 — SEC EDGAR VERIFICATION**` + verification tables | `references/phase3-sec-edgar.md` |
| 4 | `**PHASE 4 — WEEKLY BIAS SUMMARY**` + end-of-session table | `references/phase4-weekly-bias.md` |

Python emits **JSONL**, not Markdown. The AI reads the JSONL and renders the
locked Markdown above.

## Status states

| Status | Meaning |
|--------|---------|
| `SUCCESS` | Python fetched usable data |
| `FALLBACK_NEEDED` | Primary fetch failed; approved fallback may be attempted |
| `BLOCKED` | Both primary and alternate methods failed |
| `NOT AVAILABLE` | Specific field missing from usable data |
| `UNVERIFIED` | AI cannot confirm claim from official data |
| `VERIFIED` | AI confirms claim from official data |

## Out of scope

No buy/sell advice. No entry / stop-loss / position sizing. No guaranteed
targets. No monitoring. No watchlists. No price alerts. No portfolio management.
No non-US markets. No web_search fallback inside the Python layer (AI may
fall back per the skill framework).

## Testing

```bash
python -m pytest -q
```

14 tests cover source registry, normalization, Phase 1/2/3 fallback, CIK
resolution, XBRL parsing, and JSONL contracts.

## Repo map

```
rfx1427-finance/
├── README.md           # this file
├── SKILL.md            # master framework
├── CLAUDE.md           # context for Claude Code
├── pyproject.toml      # Python package
├── agents/
│   ├── claude.yaml     # Claude Code / claude.ai
│   └── openai.yaml     # OpenAI
├── references/         # locked formats and rules
└── src/rfx1427/        # Python fetch layer
```

## Licence

Copyright (c) 2026 Relf0910. All Rights Reserved.

This is a personal-use project. You may view and read the code, but you may not
copy, redistribute, modify, or claim it as your own without written permission.
Not financial advice. See [`LICENSE`](LICENSE) for full terms.
