# RFX1427 Finance

### AI Financial News Scanner and Analysis Framework

[![Version](https://img.shields.io/badge/version-4.7-blue.svg)](https://github.com/Relf0910/rfx1427-finance)
[![Status](https://img.shields.io/badge/status-active-green.svg)](https://github.com/Relf0910/rfx1427-finance)
[![Phases](https://img.shields.io/badge/phases-4-orange.svg)](https://github.com/Relf0910/rfx1427-finance)
[![Language](https://img.shields.io/badge/language-English-yellow.svg)](https://github.com/Relf0910/rfx1427-finance)

RFX1427 Finance is a read-only AI financial news scanner and analysis framework. It combines deterministic Python data access with AI judgment across Phase 1, Phase 2, and Phase 3. Python fetches and prepares source data; the AI reads, interprets, filters, verifies, and produces the locked report formats.

The framework is designed for **Scalper, Intraday, Swing, and Investor** profiles. The selected profile changes the AI's reading lens, timing assessment, and relevant market levels, while the report structure remains unchanged.

> **Important:** This project is an analysis framework, not a trading advisor. It does not execute trades, provide buy/sell instructions, operate watchlists, send price alerts, or guarantee outcomes.

## Table of Contents

- [Overview](#overview)
- [What It Does](#what-it-does)
- [What It Does Not Do](#what-it-does-not-do)
- [Core Principles](#core-principles)
- [Trader Profile Adaptation](#trader-profile-adaptation)
- [End-to-End Workflow](#end-to-end-workflow)
- [Python and AI Responsibility Boundary](#python-and-ai-responsibility-boundary)
- [Phase 1 Scanner](#phase-1-scanner)
- [Phase 2 Deep Analysis](#phase-2-deep-analysis)
- [Phase 3 SEC EDGAR Verification](#phase-3-sec-edgar-verification)
- [Phase 4 Weekly Bias Summary](#phase-4-weekly-bias-summary)
- [Source Library Map](#source-library-map)
- [Data Contracts and Status States](#data-contracts-and-status-states)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Data Integrity and Safety](#data-integrity-and-safety)
- [Folder Structure](#folder-structure)
- [Hard Rules](#hard-rules)
- [Implementation Status](#implementation-status)
- [Change Log](#change-log)
- [References](#references)

## Overview

RFX1427 Finance uses a gated four-phase workflow. Each phase is opt-in where specified, and the system stops after each report instead of advancing automatically. Current data must be fetched before analysis. Missing or inaccessible data is labelled explicitly rather than estimated or fabricated.

The current implementation branch is `mistral-fix5th`. Python fetch layers are implemented for Phase 1 source news (WAJIB 7 target 10, staged 50→70→100 early-stop, profile-adaptive), Phase 2 market data, and Phase 3 SEC EDGAR data. Phase 4 remains AI-only and does not require Python.

## What It Does

| Capability | Status |
|---|---|
| Gate 0 intake with one question at a time | Supported |
| News scanning from a user-selected source | Supported |
| Python-assisted Phase 1 source fetch | Supported |
| Source registry for ten listed sources and custom URLs | Supported |
| Positive-only Phase 1 scan | Supported |
| WAJIB 7 target 10 (output 7–10), staged 50→70→100 early-stop, profile-adaptive | Supported |
| Trader profile adaptation | Supported |
| Python-assisted Phase 2 market-data fetch | Supported |
| Google Finance/Yahoo through `yfinance` | Supported |
| Finviz through `finvizfinance` | Supported |
| MarketBeat through HTTP and HTML parsing | Supported |
| Profile-specific Phase 2 market levels | Supported |
| Python-assisted SEC EDGAR fetch and parsing | Supported |
| Ticker-to-CIK resolution | Supported |
| SEC submissions and company facts access | Supported |
| 10-K, 10-Q, 8-K, 6-K, and Form 4 discovery | Supported |
| Phase 4 weekly bias summary | AI-only framework output |
| Trade execution, monitoring, watchlists, and alerts | Not supported |

## What It Does Not Do

RFX1427 Finance does not execute trades or provide buy/sell instructions, entry prices, stop-loss levels, position sizing, guaranteed targets, or guaranteed predictions. It does not continuously monitor markets, maintain watchlists, or automatically advance from one phase to the next. It does not replace unavailable source data with model training knowledge.

## Core Principles

The framework separates **Source Fact**, **Verification**, **AI Analysis**, and **Estimate**. Python is responsible for deterministic retrieval and preparation. The AI is responsible for interpretation and judgment. This boundary prevents a parser from silently becoming a trading decision engine.

The framework follows a strict no-fabrication policy. When a value cannot be retrieved, the output uses `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` as appropriate. When a source is inaccessible, the fetch status is recorded and the relevant fallback is attempted according to the phase rules.

Phase transitions are explicit. Phase 2 requires user opt-in after Phase 1. Phase 3 requires explicit SEC verification opt-in after Phase 2. Phase 4 runs only when requested. Every report ends with the required stop phrase for that phase.

## Trader Profile Adaptation

The profile changes the AI's reading style and opportunity-recognition lens. It does not change the locked report columns or permit Python to make judgments.

| Profile | Time Horizon | Phase 1 Focus | Phase 2 Relevant Levels | Phase 3 Emphasis |
|---|---|---|---|---|
| **Scalper** | 5–15 minutes | Pre-market gaps, breaking news, immediate earnings reactions | Pre-market high/low, R1, R2 | Official filings relevant to an immediate catalyst |
| **Intraday** | Current session | Analyst actions, earnings, economic data, sector-moving news | VWAP, Opening Range High/Low | Filings that may confirm the current-session catalyst |
| **Swing** | Days to weeks | Guidance, sector rotation, product launches, short interest | 20-day SMA, 50-day SMA, recent swing high/low | Filings supporting a multi-day thesis |
| **Investor** | Long term | M&A, regulation, capital allocation, competitive moat | 52-week range, current P/E, historical valuation | 10-K, 10-Q, debt, cash flow, shares, and material events |

## End-to-End Workflow

```text
GATE 0 — INTAKE
  Output language → Trader profile → Market focus → News source
       │
       ▼
PHASE 1 — MARKET SCANNER
  Python source fetch → AI reads and filters → Best 7 positive opportunities
       │
       ▼
STOP — WAIT FOR USER
       │
       ▼
PHASE 2 — DEEP ANALYSIS
  User selects Primary Tool → Python market-data fetch → AI analysis
       │
       ▼
STOP — WAIT FOR USER
       │
       ▼
PHASE 3 — SEC EDGAR VERIFICATION
  User opts in → Python SEC fetch/parse → AI verification judgment
       │
       ▼
STOP — WAIT FOR USER
       │
       ▼
PHASE 4 — WEEKLY BIAS SUMMARY
  AI-only locked summary → END OF SESSION
```

## Python and AI Responsibility Boundary

| Layer | Responsibilities | Prohibited Responsibilities |
|---|---|---|
| **Python** | Fetch, parse, normalize, deduplicate, sort, calculate deterministic technical fields, attach URLs and timestamps, emit status | Filtering opportunities, judging direction, scoring materiality, assigning confidence, ranking, or verification labels |
| **AI** | Read each item, identify tickers, classify facts, interpret catalysts, judge direction, assess timing, assign confidence, verify SEC claims, produce locked reports | Claiming a source was fetched when it was not, inventing unavailable values, or bypassing phase gates |

## Phase 1 Scanner

Phase 1 accepts a selected source, market, and trader profile. The Python executor selects the matching adapter, fetches up to 100 items staged 50→70→100 with early-stop (target pool 10, output 7–10; at 70 if pool 7–10 STOP, at 100 if 8/9 STOP; auto-refill pagination/alternate source + Layer 2 web_search only if pool <7), normalizes, deduplicates, and emits JSON Lines. Scan counts are never disclosed. AI reads staged pool with profile-adaptive ranking.

The Phase 1 Noise Gate keeps only items that have an identifiable ticker, match the selected market, have positive direction, have materiality ≥3, have Medium/High confidence, and have Strong/Partial horizon fit. Profile-adaptive ranking (Materiality > Confidence > Horizon Fit > Catalyst clarity > Freshness, plus profile weighting) selects 7–10 best positives — WAJIB 7 target 10, staged 50→70→100 with early-stop (at 70 if pool 7–10 STOP; at 100 if 8/9 STOP). Rare fail-safe with disclaimer is the only exception.

The locked report begins with `# MARKET SCANNER` (no `Items scanned` line), contains 7–10 opportunity cards (#1→#7, up to #10 if pool qualifies), and ends with exactly:

```text
STOP
WAIT FOR USER
```

Run the Python fetch layer with:

```bash
PYTHONPATH=src python3 -m rfx1427.phase1 \
  --source Investing.com \
  --market US \
  --profile INTRADAY \
  --limit 50
```

If Python receives an HTTP 403, timeout, empty response, parser error, or other fetch failure, it emits `FALLBACK_NEEDED`. The AI may then use the approved web-search fallback. If both layers fail, the final state is `BLOCKED — SOURCE COULD NOT BE ACCESSED`.

## Phase 2 Deep Analysis

Phase 2 is opt-in and uses one user-selected Primary Tool: Google Finance/Yahoo, Finviz, or MarketBeat. Python fetches data for every Phase 1 ticker and emits a common `MarketData` contract. The AI verifies the Phase 1 catalyst, assesses timing fit, interprets price levels, applies the confidence gate, and produces the locked report.

Python provides current price, percentage change, volume, technical fields, analyst data, earnings metadata, and source status when available. Missing fields are represented as `NOT AVAILABLE`. If both the primary and alternate Python methods fail, the result is marked `BLOCKED`; no market data is fabricated.

The locked Phase 2 report contains these blocks in this order:

1. `Primary Data Summary`
2. `Catalyst Verification`
3. `Deep Analysis Reports`
4. `Ranking Summary`

It ends with exactly:

```text
STOP
WAIT FOR USER
```

Run the fetch layer with:

```bash
PYTHONPATH=src python3 -m rfx1427.phase2 \
  --primary-tool 'Google Finance' \
  --profile INTRADAY \
  --opportunities tests/fixtures/opportunities.json
```

## Phase 3 SEC EDGAR Verification

Phase 3 is separate from Phase 2 and runs only after explicit user opt-in. Python uses official SEC EDGAR endpoints to resolve tickers to CIKs, read company submissions, read company facts/XBRL data, identify recent filings, and prepare the data for AI verification.

The implementation covers the following filing types and data categories:

| Filing or data | Purpose |
|---|---|
| 10-K | Annual revenue, earnings, debt, cash flow, and shares |
| 10-Q | Quarterly revenue, earnings, debt, cash flow, and shares |
| 8-K | Recent material corporate events |
| 6-K | Relevant foreign private issuer reports |
| Form 4 | Recent insider transactions |
| Company submissions | Filing history, company metadata, and filing URLs |
| Company facts/XBRL | Structured standardized financial facts |

Python only fetches and parses. The AI compares the SEC data with Phase 2 claims and assigns `VERIFIED` or `UNVERIFIED`. Python never assigns the verification label.

Run the SEC fetch layer with:

```bash
PYTHONPATH=src python3 -m rfx1427.phase3 \
  --tickers AAPL NVDA \
  --user-agent 'RFX1427 Finance contact@example.com'
```

The client requires an identified User-Agent containing a contact email, throttles requests, and uses official SEC sources only. If a primary SEC request fails, the alternate method remains within official SEC endpoints. If both fail, the data remains `UNVERIFIED — SEC DATA NOT AVAILABLE`.

The locked Phase 3 report begins with:

```markdown
**PHASE 3 — SEC EDGAR VERIFICATION**
(Opt-in only | Access: [DATE TIME])
```

It contains the Fetch Attempt table, per-ticker Verification Results, a verified/unverified summary, and ends with:

```text
STOP
WAIT FOR USER
```

## Phase 4 Weekly Bias Summary

Phase 4 does not require Python. It is an AI-only summary available after the relevant preceding phases and explicit user request. It uses the existing locked format, mandatory direction tags, the End of Session table, and the no-monitoring disclaimer. No Phase 4 implementation was changed by the Python work in this branch.

## Source Library Map

| Source | Python method | Notes |
|---|---|---|
| Finviz | `finvizfinance` or HTML fallback | Default Phase 1 source |
| Yahoo Finance | `yfinance` | Phase 1 alternative and Phase 2 market data |
| Investing.com | RSS or HTML parser | May return 403; fallback status is explicit |
| TradingView | Public feed/page parser | Access depends on public page availability |
| StockTitan | HTTP and HTML parser | Public page access only |
| PR Newswire | RSS via `feedparser` | Preferred structured source |
| GlobeNewswire | RSS via `feedparser` | Preferred structured source |
| Motley Fool | RSS or HTML parser | Public access only |
| Barchart | HTTP and HTML parser | Headers and parser are source-specific |
| StockAnalysis.com | HTTP and HTML parser | Public access only |
| Custom source | RSS, JSON, or HTML detection | Requires a valid URL |

The system does not bypass CAPTCHAs, login walls, or anti-bot protections. A blocked source is reported honestly and routed through the phase-approved fallback.

## Data Contracts and Status States

Phase 1 emits `NewsItem` objects containing `id`, `title`, `summary`, `url`, `source`, `timestamp`, `raw_text`, `collection_method`, and `status`. Phase 2 emits `MarketData` objects containing ticker, company, primary tool, fetch status, price fields, technical levels, analyst data, earnings metadata, and error metadata. Phase 3 emits SEC data containing ticker, CIK, company, filings, facts, material events, insider transactions, source URLs, accession numbers, and error metadata.

| Status | Meaning |
|---|---|
| `SUCCESS` | The selected Python method returned usable data |
| `FALLBACK_NEEDED` | The primary fetch failed and the approved fallback may be attempted |
| `BLOCKED` | The primary and approved alternate methods failed |
| `NOT AVAILABLE` | A specific field was not present in otherwise usable data |
| `UNVERIFIED` | AI cannot confirm a claim from available official data |
| `VERIFIED` | AI determines that official SEC data confirms the claim |

## Installation

The project requires Python 3.10 or later. Install the package and runtime dependencies in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
```

The dependency manifest is in [`pyproject.toml`](pyproject.toml). It includes `requests`, `beautifulsoup4`, `feedparser`, `yfinance`, and `finvizfinance`.

## Usage

The Python layers are data preparation executors. They do not replace the AI layer that reads the JSONL handoff and renders the locked Markdown reports. A host integration should invoke the relevant executor only after the phase gate has been satisfied.

All commands accept live source or market inputs, and all output should be treated as current-data results with the recorded access timestamp. A non-success status must be surfaced to the AI and the user rather than hidden.

## Testing

Run all tests with:

```bash
python3 -m pytest -q
```

The test suite covers source registry behavior, normalization, deduplication, Phase 1 fallback, Phase 2 profile levels, market-data contracts, CIK resolution, XBRL concept parsing, SEC fallback behavior, and JSONL handoff contracts.

## Data Integrity and Safety

The framework uses official SEC endpoints for Phase 3 and requires a descriptive contact User-Agent. The SEC documentation recommends efficient access, downloading only required data, and moderating request volume [1] [2]. The implementation therefore applies request throttling and does not use web search as a Phase 3 fallback.

The framework is read-only. It intentionally does not connect to brokerage accounts, order systems, portfolio management, automated monitoring, or alerting services.

## Folder Structure

```text
rfx1427-finance/
├── README.md
├── SKILL.md
├── pyproject.toml
├── .gitignore
├── agents/
│   └── openai.yaml
├── references/
│   ├── acceptance-tests.md
│   ├── change-log-v2.md
│   ├── data-integrity-hierarchy.md
│   ├── decision-tree.md
│   ├── error-states.md
│   ├── hard-rules-master.md
│   ├── intake-form.md
│   ├── phase1-scanner.md
│   ├── phase2-deep-analysis.md
│   ├── phase3-sec-edgar.md
│   └── phase4-weekly-bias.md
├── src/rfx1427/
│   ├── models.py
│   ├── phase1.py
│   ├── phase2.py
│   ├── phase3.py
│   └── sources/
│       ├── base.py
│       └── registry.py
└── tests/
    ├── fixtures/
    ├── test_phase1.py
    ├── test_phase2.py
    └── test_phase3.py
```

## Hard Rules

The following rules remain authoritative:

1. Ask one intake question at a time.
2. Complete intake before Phase 1.
3. Fetch current data before analysis.
4. Never fabricate a ticker, price, filing, financial figure, level, rating, or source result.
5. No ticker means noise.
6. Phase 1 reports positive opportunities only, with materiality at least 3, Medium or High confidence, and no Poor horizon fit.
7. Phase 1 reports 7–10 positive opportunities — WAJIB 7 target 10, profile-adaptive, staged 50→70→100 with early-stop (at 70 if 7–10 STOP; at 100 if 8/9 STOP). Python expands window (pagination/alternate source + Layer 2 web_search) only if pool <7; hard gates never lowered; fail-safe with disclaimer is the only exception.
8. Phase 2 is opt-in and uses the user-selected Primary Tool only.
9. Phase 2 does not use SEC EDGAR.
10. Phase 3 is a separate opt-in SEC verification phase.
11. Python fetches and prepares; AI judges and labels.
12. Low-confidence Phase 2 opportunities are skipped.
13. No automatic phase transition, loop, watchlist, monitoring, alert, trade execution, or buy/sell instruction.
14. Locked Phase 1–4 output structures and stop phrases must not be modified.
15. Phase 4 does not require Python.

## Implementation Status

| Area | Branch status |
|---|---|
| Phase 1 Python source layer | Implemented |
| Phase 2 Python market-data layer | Implemented |
| Phase 3 Python SEC EDGAR layer | Implemented |
| AI judgment and locked report rendering | Defined by skill/host integration |
| Phase 4 Python layer | Not applicable |
| Automated trading or monitoring | Intentionally excluded |

## Change Log

| Commit | Change |
|---|---|
| `64dde77` | Implemented Phase 1 Python source fetch layer |
| `cfbc77a` | Implemented Phase 2 Python market-data fetch layer |
| `e9a4069` | Implemented Phase 3 SEC EDGAR fetch and parsing layer |
| `4114b60` | Fix data-correctness Phases 1-3: accession matching, Finviz fields, HTML/RSS filtering |
| `a46fa36` | Fix Finviz Phase 1 parser: handle table layout (tr.news_table-row) |
| v4.6 | Phase 1 Exactly 7 mandatory (WAJIB 7, profile-adaptive: Scalper/Intraday/Swing/Investor), limit 50→100 + auto-refill, no scan-count disclosure, fail-safe with disclaimer |
| v4.7 | Phase 1 WAJIB 7 target 10 (output 7–10), staged 50→70→100 with early-stop, profile-adaptive ranking |

## References

[1]: https://www.sec.gov/search-filings/edgar-application-programming-interfaces "SEC EDGAR Application Programming Interfaces"
[2]: https://www.sec.gov/about/developer-resources "SEC Developer Resources"
[3]: https://github.com/Relf0910/rfx1427-finance/blob/mistral-fix5th/SKILL.md "RFX1427 Finance Master Skill"
[4]: https://github.com/Relf0910/rfx1427-finance/blob/mistral-fix5th/references/phase1-scanner.md "Phase 1 Scanner Specification"
[5]: https://github.com/Relf0910/rfx1427-finance/blob/mistral-fix5th/references/phase2-deep-analysis.md "Phase 2 Deep Analysis Specification"
[6]: https://github.com/Relf0910/rfx1427-finance/blob/mistral-fix5th/references/phase3-sec-edgar.md "Phase 3 SEC EDGAR Specification"
