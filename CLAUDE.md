# CLAUDE.md — Project context for Claude Code

This is the `rfx1427-finance` repo (v4.7.1). Claude Code reads this file automatically to
understand the project. For full framework rules, see `SKILL.md` and `references/`.

## Quick Start

```bash
pip install -e .                              # install Python fetch layer
python -m rfx1427.phase1 --list-sources       # show 10 supported news sources
python -m rfx1427.phase1 --source finviz --market US --limit 20
python -m rfx1427.phase2 --primary-tool Finviz --profile INTRADAY --opportunities <opps.json>
python -m rfx1427.phase3 --tickers MSFT --user-agent rfx1427-demo@example.com
```

Or via installed entry-points: `rfx1427-phase1`, `rfx1427-phase2`, `rfx1427-phase3`.

## 4-Phase Workflow

| Phase | What it does | Reference | Python entry |
|-------|--------------|-----------|--------------|
| 1. Scanner | Fetch news, 7-10 positive cards (WAJIB 7, target 10) | `references/phase1-scanner.md` | `phase1.py` |
| 2. Deep Analysis | Market data via Primary Tool (NO SEC) | `references/phase2-deep-analysis.md` | `phase2.py` |
| 3. SEC EDGAR | Verify via official SEC API (opt-in) | `references/phase3-sec-edgar.md` | `phase3.py` |
| 4. Weekly Bias | AI-only summary (locked format) | `references/phase4-weekly-bias.md` | — |

## Gate 0 — Intake (Locked)

Two questions only, asked one at a time:
1. **Language** → `English / Bahasa Melayu / Other`
2. **Trader Profile** → `Scalper / Intraday / Swing / Investor`

Market is **locked to US** — no question, no branching. Do not invent non-US paths.

## Critical Files

| Path | Role |
|------|------|
| `SKILL.md` | Master framework (Claude + OpenAI + others) |
| `references/phase*-*.md` | Locked output formats (CARD, hard rules) |
| `references/intake-form.md` | Gate 0 form |
| `references/hard-rules-master.md` | 39 hard rules |
| `agents/claude.yaml` | Claude Code interface |
| `agents/openai.yaml` | OpenAI interface |
| `src/rfx1427/phase{1,2,3}.py` | Python fetch layer |
| `src/rfx1427/sources/base.py` | Staged-fetch constants (50/70/100, POOL_MIN=7, POOL_TARGET=10) |

## Hard Rules (Top 5)

1. **No fabrication** — use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when data missing.
2. **Positive-only Phase 1** — discard negative / mixed / neutral.
3. **WAJIB 7, target 10** — staged 50→70→100 with early-stop; never lower thresholds.
4. **One question at a time** in Gate 0.
5. **No auto-advance** phases — wait for explicit user opt-in between phases.

## Common Tasks

- **Add a new source**: edit `src/rfx1427/sources/registry.py` `SOURCE_URLS` and `ALIASES`.
- **Tweak Phase 2 levels**: edit `src/rfx1427/phase2.py` `_levels()`.
- **Adjust SEC window**: edit `src/rfx1427/phase3.py` `SecClient.fetch()` ordering.
- **Change format**: edit `references/phase*-*.md` (the AI reads these, not the Python).

## Phase 1 Staged Fetch (Important)

`phase1.py` does three fetch waves against the source:
- **Stage 1 (50 items)**: if pool < 7, continue to Stage 2.
- **Stage 2 (70 items)**: if pool is 7–10, stop early. If still < 7, continue to Stage 3.
- **Stage 3 (100 items)**: hard cap.

`STAGE_1_LIMIT`, `STAGE_2_LIMIT`, `STAGE_3_LIMIT`, `POOL_MIN`, `POOL_TARGET` live in
`sources/base.py`. Adjusting these changes fetch behavior project-wide.

## Python Hygiene

- Verify with `pytest -q` after changes.
- Verify Phase 2 with real ticker: `MSFT` works (Finviz SUCCESS, price ~500).
- Verify Phase 3 with real ticker: `MSFT` returns 5× 10-Q in window.

## What this repo does NOT do

- No buy/sell, entry, stop-loss, position sizing, or guaranteed targets.
- No continuous monitoring, watchlists, price alerts, portfolio management.
- No non-US markets (Gate 0 locked to US).
- No web_search fallback (Python fetch only; AI may fall back per skill).
