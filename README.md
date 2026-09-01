<div align="center">

# 🏦 RFX1427 Finance

### AI Financial News Scanner & Analysis Framework

[![Version](https://img.shields.io/badge/version-4.4-blue.svg)](https://github.com/Relf0910/rfx1427-finance)
[![Status](https://img.shields.io/badge/status-active-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![Phase](https://img.shields.io/badge/phases-4-orange.svg)]()
[![Language](https://img.shields.io/badge/language-English-yellow.svg)]()

</div>

---

> **RFX1427 Finance** is an AI financial news scanner and analysis framework with strict gate controls, a fact-based approach, and official SEC EDGAR verification. Python works directly with the AI across Phase 1, 2 and 3 — Python brings the AI to the news source, the market-data tool, and the SEC EDGAR filings, while the AI judges. Phase 1 reads ONE user-selected source and reports the best positive opportunities per trader profile; Phase 2 performs deep analysis with a user-selected Primary Tool (NO SEC); Phase 3 verifies via SEC EDGAR only on explicit user opt-in.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Python + AI Model](#python--ai-model)
- [Workflow Architecture](#workflow-architecture)
- [Phase Summaries](#phase-summaries)
- [Source Library Map](#source-library-map)
- [Data Integrity Hierarchy](#data-integrity-hierarchy)
- [Error States](#error-states)
- [References](#references)
- [Folder Structure](#folder-structure)
- [Hard Rules](#hard-rules-38)
- [Status & Controls](#status--controls)
- [Change Log](#change-log)

---

## Overview

RFX1427 Finance is a **read-only analysis framework** — not a trading advisor. It scans financial news, filters opportunities through strict criteria, and produces structured reports across four phases. Every claim must be backed by fetched data. If data is missing, the framework uses explicit labels (`NOT AVAILABLE`, `UNVERIFIED`, `BLOCKED`) rather than fabricating values.

### What It Does

| Capability | Supported |
|---|---|
| News scanning from user-selected source | ✅ |
| **Python + AI unified flow across Phase 1, 2, 3** | ✅ |
| Trader profile filtering (Scalper / Intraday / Swing / Investor) | ✅ |
| Market focus filtering (US / Singapore / Malaysia / Other) | ✅ |
| Positive-only selection, max 7 opportunities | ✅ |
| Materiality & confidence scoring | ✅ |
| 3-layer hybrid fallback (Python fetch → web_search → BLOCKED) | ✅ |
| Deep Analysis with user-selected Primary Tool | ✅ |
| SEC EDGAR verification (opt-in only) | ✅ |
| Weekly bias summary with locked format | ✅ |

### What It Does NOT Do

| Prohibited | Reason |
|---|---|
| Buy/sell recommendations | Read-only analysis only |
| Trade execution | No execution capability |
| Continuous monitoring / watchlists | No loop, no monitoring |
| Price alerts | Session-based, fresh start each time |
| Guaranteed predictions | Estimates labelled, not guaranteed |
| Fabricated data | `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED` used instead |
| Python judging | Python only fetches & prepares; the AI judges |

---

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate data. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED`
- **PYTHON AS AI'S ARM** — Python fetches & prepares; AI interprets & judges. No separate collect-then-read pass
- **POSITIVE-ONLY** — Phase 1 keeps only positive opportunities (max 7, never force-filled)
- **OPT-IN ONLY** — Phase 2 on user selection. Phase 3 SEC Verification only on explicit user opt-in. Phase 4 only on user request
- **NO AUTOMATIC PHASE TRANSITION** — phase cannot jump without permission
- **NO LOOP, NO MONITOR, NO AUTO-PROCEED** — each session is fresh
- **ONE QUESTION AT A TIME** for Intake
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss, position sizing, or guaranteed target

---

## Python + AI Model

Python works **directly with** the AI inside each phase as its assisting arm. Python brings the AI to the data; the AI judges. This eliminates the collect-then-read two-pass.

| Phase | Python does (arm) | AI does (judge) |
|---|---|---|
| **Phase 1** | Fetch + stream news from the selected source; cascade to web_search if needed | Read items live with trader lens; filter, score, recognize opportunities; choose best positive (max 7) |
| **Phase 2** | Fetch market data from the selected Primary Tool; format for the AI | Verify catalyst, assess timing fit, identify price levels, apply confidence gate |
| **Phase 3** | Access SEC EDGAR, fetch + parse official filings | Verify against Phase 2 claims, assign VERIFIED / UNVERIFIED |
| **Phase 4** | — (no Python) | Weekly bias summary, locked format |

> **Python never filters, scores, extracts tickers, removes noise, or judges.** All judgement is the AI's.

---

## Workflow Architecture

```text
INTAKE (Gate 0 — 3 questions)
    │
    ▼
PHASE 1 — SCANNER (Python + AI Unified, Positive-Only)
    │  Live read → Trader Filter → Materiality → Confidence → Noise Gate → Best 7 Positive Report
    │
    ▼
STOP 1 — WAIT FOR USER (opt-in required)
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Python + AI Unified, Primary Tool Only, NO SEC)
    │  Python fetch market data → AI Catalyst Verify → Timing Fit → Confidence Gate → Phase 2 Report
    │
    ▼
STOP 2 — WAIT FOR USER (opt-in required)
    │
    ▼
PHASE 3 — SEC EDGAR VERIFICATION (Python + AI Unified, Opt-in Only)
    │  Python fetch + parse filings → AI Verification Labels → Phase 3 Report
    │
    ▼
STOP 3 — WAIT FOR USER (request required)
    │
    ▼
PHASE 4 — WEEKLY BIAS SUMMARY (Locked Format)
    │  Summary Table → Tags → END OF SESSION → NO MONITORING
    │
    ▼
END
```

---

## Phase Summaries

### 🚪 Gate 0 — Intake

Three questions, asked one at a time:

| Question | Options | Recorded As |
|---|---|---|
| Output language? | English / Bahasa Melayu / Other | `output_language` |
| Trader profile? | Scalper / Intraday / Swing / Investor | `trader_profile` |
| Market focus? | US / Singapore / Malaysia / Other | `market` |

### 📡 Phase 1 — Scanner (Python + AI Unified)

| Step | Action |
|---|---|
| 1A | Ask user for news source (default: Finviz) |
| 1B | **Python fetches** source live and streams items to the AI; AI reads each item live with the trader lens (ONE PASS). 3-layer fallback: Python → web_search → BLOCKED |
| 1C | Filter by trader profile. Hard rule: NO TICKER = NOISE |
| 1D | Extract facts. Distinguish FACT vs AI INFERENCE vs ESTIMATE |
| 1E | Map opportunity: Direction, Materiality (1-5), Confidence, Horizon Fit, Transmission Channel |
| 1F | Noise Gate: **Positive-only**, Materiality ≥ 3, Confidence ≥ Medium, Horizon Fit ≠ Poor. **Max 7 positive opportunities** |

**Output:** Market Scanner report with opportunity cards → `STOP / WAIT FOR USER`

### 🔍 Phase 2 — Deep Analysis (Python + AI Unified)

| Step | Action |
|---|---|
| 2A | Ask user for Primary Tool (default: Google Finance) |
| 2B | **Python fetches** market data for EVERY Phase 1 opportunity |
| 2C | **AI analyzes & synthesizes**: verify catalyst, timing fit, price levels, confidence gate |

**Primary Tool Options:**

| Tool | Python Library | Data Fetched |
|---|---|---|
| Google Finance / Yahoo | `yfinance` | Price, change %, news, analyst targets, analyst ratings, earnings |
| Finviz | `finvizfinance` | Price, change %, volume, RSI, SMA 20/50, P/E, EPS, revenue, headlines |
| MarketBeat | `requests` + `BeautifulSoup4` | Price, change %, short interest, analyst consensus, financial ratios |

**Output:** Deep Analysis report (4 blocks) → `STOP / WAIT FOR USER`

### ✅ Phase 3 — SEC EDGAR Verification (Python + AI Unified)

| Step | Action |
|---|---|
| 3A | **Python accesses SEC EDGAR**, fetches + parses official filings (10-K, 10-Q, 8-K, 6-K, Form 4) |
| 3B | **AI verifies** against Phase 2 claims and assigns VERIFIED / UNVERIFIED |

**Labels:** `VERIFIED` if SEC filing confirms data · `UNVERIFIED — SEC DATA NOT AVAILABLE` if data cannot be retrieved

**Output:** SEC EDGAR Verification report → `STOP / WAIT FOR USER`

### 📊 Phase 4 — Weekly Bias Summary

| Rule | Detail |
|---|---|
| Directions | Positive / Negative / Neutral only (NO MIXED) |
| Estimate format | Range (e.g., +3% to +8%) |
| Reason | Maximum 10 words |
| Tags | `PREPARE FOR VOLUME BUY` (Positive) · `BE CAREFUL — MARKET CRASH RISK` (Negative) · `WAIT FOR CONFIRMATION` (Neutral) |
| Mandatory sections | Summary Table + Penjelasan Ringkas + END OF SESSION table + NO MONITORING disclaimer |

**Output:** Weekly Bias Summary → `END OF SESSION`

---

## Source Library Map

All sources below are **FREE and accessible** (verified by testing). The user selects one at Step 1A. Python uses the matching library.

### Tier 1 — Primary (Default)

| Source | Python Library | Access Method | Notes |
|---|---|---|---|
| **Finviz** | `finvizfinance` | Scrape (HTML) | **DEFAULT SOURCE.** Most complete: news, screener, quotes. No API key needed. |

### Tier 2 — Optional Alternatives (Free)

| Source | Python Library | Access Method |
|---|---|---|
| Yahoo Finance | `yfinance` | API (free) |
| Investing.com | `investpy` | Scrape |
| TradingView | `tradingview-scraper` | Scrape |
| StockTitan | `requests` + `BeautifulSoup4` | Scrape (HTML) |
| PR Newswire | `feedparser` | RSS feed (free) |
| GlobeNewswire | `feedparser` | RSS feed (free) |
| Motley Fool | `feedparser` or `BeautifulSoup4` | RSS / Scrape |
| Barchart | `requests` + `BeautifulSoup4` | Scrape (with headers) |
| StockAnalysis.com | `requests` + `BeautifulSoup4` | Scrape |

### Tier 3 — Custom Sources

| Source | Method |
|---|---|
| Custom URL (user-provided) | `requests` + `BeautifulSoup4` |
| RSS feed URL | `feedparser` |
| Other platform name | `requests` + `BeautifulSoup4` |

### Blocked Sources (skip directly to web_search)

CNBC · Reuters · Bloomberg · Seeking Alpha · TheStreet · Investopedia · WSJ · MarketWatch

### 3-Layer Hybrid Fallback

```text
LAYER 1 — PYTHON FETCH (Primary)      → reads items live
LAYER 2 — AI WEB_SEARCH (Fallback)    → only if Python fails
LAYER 3 — BLOCKED (Final)             → only if both fail
```

> Python ALWAYS tries first. web_search is ONLY used when Python fails (or for a known blocked source). BLOCKED is ONLY declared when both layers fail.

---

## Data Integrity Hierarchy

```text
OFFICIAL SEC FILING
       ↓
PRIMARY FINANCIAL TOOL
       ↓
NEWS SOURCE
       ↓
AI INFERENCE
       ↓
ESTIMATE
```

> This hierarchy means: for items verifiable through SEC filings, SEC is the authority. For market data that SEC does not provide (price, volume, technical indicators), the Primary Tool is the authority.

---

## Error States

| Condition | Output Label |
|---|---|
| Source fails to access | `BLOCKED — SOURCE COULD NOT BE ACCESSED` |
| Primary tool fails | `PRIMARY TOOL — BLOCKED` |
| Data missing | `NOT AVAILABLE` |
| SEC data verified | `VERIFIED` |
| SEC data missing | `UNVERIFIED — SEC DATA NOT AVAILABLE` |
| Mechanism fails | `REJECTED` |
| Confidence Low | `LOW CONFIDENCE — SKIP` |
| Python fetch fails (needs fallback) | `FALLBACK_NEEDED` |
| No opportunity passes gate | `No qualifying opportunities found for this trader profile and market focus.` |
| Primary Tool fails (all) | `FETCH FAILED — ANALYSIS SKIPPED` |
| No ticker / company | `NO TICKER = NOISE` |

---

## References

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 SEC EDGAR Verification | `references/phase3-sec-edgar.md` |
| Phase 4 Weekly Bias Summary | `references/phase4-weekly-bias.md` |
| Error States | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |
| Change Log | `references/change-log-v2.md` |

---

## Folder Structure

```
rfx1427-finance/
├── SKILL.md                        # Main skill definition (v4.4)
├── README.md                       # This file
├── agents/
│   └── openai.yaml                  # Agent configuration
└── references/
    ├── intake-form.md              # Gate 0: Intake form
    ├── phase1-scanner.md            # Phase 1: Scanner
    ├── phase2-deep-analysis.md      # Phase 2: Deep Analysis
    ├── phase3-sec-edgar.md          # Phase 3: SEC EDGAR Verification
    ├── phase4-weekly-bias.md        # Phase 4: Weekly Bias Summary
    ├── error-states.md              # Error state definitions
    ├── hard-rules-master.md         # Hard rules master list
    ├── data-integrity-hierarchy.md  # Data integrity hierarchy
    ├── decision-tree.md             # Decision tree
    ├── acceptance-tests.md          # Acceptance tests
    └── change-log-v2.md            # Version change log
```

---

## Hard Rules (38)

Original ordering from SKILL.md § MASTER HARD RULES. Categories in brackets are indicative only.

| # | Category | Rule |
|---|---|---|
| 1 | Intake | One question at a time |
| 2 | Intake | Complete Intake before Phase 1 |
| 3 | Phase 1 | No ticker = noise |
| 4 | Phase 1 | Materiality < 3 = reject |
| 5 | Phase 1 | Confidence < Medium in Phase 1 = reject |
| 6 | Phase 1 | Poor Horizon Fit = reject |
| 7 | Phase 1 | **Maximum 7 positive Phase 1 opportunities** |
| 8 | Phase 2 | Phase 2 requires explicit opt-in |
| 9 | Phase 2 | User chooses Primary Tool (Google Finance default) |
| 10 | Phase 2 | Phase 2 uses Primary Tool ONLY. No SEC in Phase 2 |
| 11 | Phase 2/3 | Phase 3 is SEPARATE phase for SEC EDGAR (opt-in only) |
| 12 | Phase 2 | SEC EDGAR is NOT mandatory in Phase 2 |
| 13 | Phase 2 | Fetch before analysis |
| 14 | Global | No fabricated data |
| 15 | Global | No training data replacing required current fetch |
| 16 | Global | Missing data = Not Available |
| 17 | Global | Rejected mechanism = Skip |
| 18 | Global | Low final confidence = Skip |
| 19 | Phase 3 | Phase 3 only if user explicitly opt-in for SEC verification |
| 20 | Phase 4 | Phase 4 only when user asks |
| 21 | Global | No automatic phase transition |
| 22 | Global | No loop |
| 23 | Global | No watchlist |
| 24 | Global | No monitoring |
| 25 | Global | No buy/sell instruction |
| 26 | Global | No guaranteed prediction |
| 27 | Global | Every session starts fresh |
| 28 | Global | Format Phase 1, 2, 3, 4 are LOCKED. Do not modify |
| 29 | Phase 3 | SEC Verification labels: VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE |
| 30 | Phase 1 | **Python works directly with the AI inside Phase 1 (unified flow)**. Python brings the AI to the source and assists reading in real time — no separate collection step. Python does NOT filter, score, or judge; the AI judges |
| 31 | Phase 1 | All leftover news items after Phase 1 are discarded. No second pass. No re-reading. First-pass result is final |
| 32 | Phase 1 | AI adapts reading style and opportunity recognition to the selected trader profile. The AI becomes the trader type the user chose |
| 33 | Global | Source access uses the 3-layer fallback: Python fetch → AI web_search → BLOCKED. Python always tries first; web_search only when Python fails; blocked sources skip to Layer 2 |
| 34 | Global | Finviz is default/primary. All Source Library Map sources are free & verified. AI accepts any user source without rejection |
| 35 | Phase 1 | Phase 1 is POSITIVE-ONLY. Negative, mixed, neutral items are discarded |
| 36 | Phase 1 | Phase 1 outputs the best 7 positive opportunities (0-7). Does NOT force-fill |
| 37 | Phase 2 | **Python works directly with the AI inside Phase 2 (unified flow)**. Python fetches market data; AI analyzes, verifies catalyst, assesses timing fit, identifies price levels, applies confidence gate. Python does NOT analyze or judge. Primary Tool remains benchmark (NO SEC in Phase 2) |
| 38 | Phase 3 | **Python works directly with the AI inside Phase 3 (unified flow, opt-in only)**. Python fetches + parses SEC EDGAR filings; AI verifies against Phase 2 claims and assigns VERIFIED / UNVERIFIED. Python does NOT verify or label |

---

## Status & Controls

| Control | Description |
|---|---|
| **Version** | 4.4 — Python + AI Unified across Phase 1, 2 & 3, positive-only scan, locked templates |
| **Authority Gate** | Primary Tool selected by user. SEC EDGAR is separate opt-in phase |
| **Python/AI Boundary** | Python fetches + prepares; AI judges. No overlap |
| **Evidence Integrity Gate** | Every important claim must be supported by real data (source URL, filing reference, or label) |
| **Completion Gate** | Phase only complete after every step in reference is done |
| **Stagnation Breaker** | If Phase 1 produces 0 opportunities after two attempts with two different sources, stop. Do not loop |
| **Autonomous Loop** | INSPECT → PLAN → BUILD → VALIDATE → DIAGNOSE → REPAIR → REVALIDATE |

---

## Change Log

| Version | Change |
|---|---|
| **v4.0** | Locked output templates for all 4 phases; explicit OUTPUT FORMAT INSTRUCTIONS; README rewritten |
| **v4.1** | Pre-Phase 1 Python news collection (fetch → dedup → sort → cap 50); max opportunities 10; trader-adaptive reading; hard rules 30–32 |
| **v4.2** | Source Library Map (Finviz default + 9 free alternatives + blocked list); 3-layer hybrid fallback; `FALLBACK_NEEDED` status; hard rules 33–34 |
| **v4.3** | Pre-Phase 1 merged INTO Phase 1 as Python + AI Unified (one pass, positive-only); max opportunities reduced to 7; hard rules 35–36 |
| **v4.4** | **Python + AI Unified extended to Phase 2 & Phase 3** (one pass): Python fetches market data + parses SEC EDGAR while AI judges; hard rules 37–38 |

---

<div align="center">

**⚠️ NO MONITORING — This is read-only analysis. Not investment advice. No continuous monitoring.**

---

[View on GitHub](https://github.com/Relf0910/rfx1427-finance) · [Report Issue](https://github.com/Relf0910/rfx1427-finance/issues)

</div>
