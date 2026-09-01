<div align="center">

# 🏦 RFX1427 Finance

### AI Financial News Scanner & Analysis Framework

[![Version](https://img.shields.io/badge/version-4.0-blue.svg)](https://github.com/Relf0910/rfx1427-finance)
[![Status](https://img.shields.io/badge/status-active-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![Phase](https://img.shields.io/badge/phases-4-orange.svg)]()
[![Language](https://img.shields.io/badge/language-English-yellow.svg)]()

</div>

---

> **RFX1427 Finance** is an AI financial news scanner and analysis framework with strict gate controls, a fact-based approach, and official SEC EDGAR verification. It reads ONE user-selected news source, filters public companies by trader profile, market focus, time horizon, materiality, and confidence, then performs Deep Analysis with a user-selected Primary Tool. SEC EDGAR verification runs only on explicit user opt-in.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Core Principles](#core-principles)
- [Workflow Architecture](#workflow-architecture)
- [Phase Summaries](#phase-summaries)
- [Data Integrity Hierarchy](#data-integrity-hierarchy)
- [Error States](#error-states)
- [References](#references)
- [Folder Structure](#folder-structure)
- [Hard Rules](#hard-rules-29)
- [Status & Controls](#status--controls)
- [Change Log](#change-log)

---

## Overview

RFX1427 Finance is a **read-only analysis framework** — not a trading advisor. It scans financial news, filters opportunities through strict criteria, and produces structured reports across four phases. Every claim must be backed by fetched data. If data is missing, the framework uses explicit labels (`NOT AVAILABLE`, `UNVERIFIED`, `BLOCKED`) rather than fabricating values.

### What It Does

| Capability | Supported |
|---|---|
| News scanning from user-selected source | ✅ |
| Trader profile filtering (Scalper / Intraday / Swing / Investor) | ✅ |
| Market focus filtering (US / Singapore / Malaysia / Other) | ✅ |
| Materiality & confidence scoring | ✅ |
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

---

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate data. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED`
- **OPT-IN ONLY** — Phase 2 on user selection. Phase 3 SEC Verification only on explicit user opt-in. Phase 4 only on user request
- **NO AUTOMATIC PHASE TRANSITION** — phase cannot jump without permission
- **NO LOOP, NO MONITOR, NO AUTO-PROCEED** — each session is fresh
- **ONE QUESTION AT A TIME** for Intake
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss, position sizing, or guaranteed target

---

## Workflow Architecture

```text
INTAKE (Gate 0 — 3 questions)
    │
    ▼
PHASE 1 — SCANNER (Finviz Default)
    │  News → Ticker Filter → Profile Filter → Materiality → Confidence → Noise Gate → Phase 1 Report
    │
    ▼
STOP 1 — WAIT FOR USER (opt-in required)
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Primary Tool Only, NO SEC)
    │  Primary Data Fetch → Catalyst Verification → Timing Fit → Confidence Gate → Phase 2 Report
    │
    ▼
STOP 2 — WAIT FOR USER (opt-in required)
    │
    ▼
PHASE 3 — SEC EDGAR VERIFICATION (Opt-in Only)
    │  SEC Filing Fetch → Verification Labels → Phase 3 Report
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

### 📡 Phase 1 — Scanner

| Step | Action |
|---|---|
| 1A | Ask user for news source (default: Finviz) |
| 1B | Fetch / read source live. Record source, URL, access time |
| 1C | Filter by trader profile. Hard rule: NO TICKER = NOISE |
| 1D | Extract facts. Distinguish FACT vs AI INFERENCE vs ESTIMATE |
| 1E | Map opportunity: Direction, Materiality (1-5), Confidence, Horizon Fit, Transmission Channel |
| 1F | Noise Gate: Materiality ≥ 3, Confidence ≥ Medium, Horizon Fit ≠ Poor. Max 10 opportunities |

**Output:** Market Scanner report with opportunity cards → `STOP / WAIT FOR USER`

### 🔍 Phase 2 — Deep Analysis

| Step | Action |
|---|---|
| 2A | Ask user for Primary Tool (default: Google Finance) |
| 2B | Fetch primary data for EVERY Phase 1 opportunity |
| 2C | Analyze & synthesize: verify catalyst, timing fit, price levels, confidence gate |

**Primary Tool Options:**

| Tool | Data Fetched |
|---|---|
| Google Finance | Price, change %, news, analyst targets, analyst ratings, earnings |
| Finviz | Price, change %, volume, RSI, SMA 20/50, P/E, EPS, revenue, headlines |
| MarketBeat | Price, change %, short interest, analyst consensus, financial ratios |

**Output:** Deep Analysis report (4 blocks) → `STOP / WAIT FOR USER`

### ✅ Phase 3 — SEC EDGAR Verification

| Item | Filing Type |
|---|---|
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

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
├── SKILL.md                        # Main skill definition (v4.2)
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

## Hard Rules (29)

### Intake

| # | Rule |
|---|---|
| 1 | One question at a time |
| 2 | Complete Intake before Phase 1 |

### Phase 1 — Scanner

| # | Rule |
|---|---|
| 3 | No ticker = noise |
| 4 | Materiality < 3 = reject |
| 5 | Confidence < Medium = reject |
| 6 | Poor Horizon Fit = reject |
| 7 | Maximum 10 opportunities |
| 8 | Stop after Phase 1 report |

### Phase 2 — Deep Analysis

| # | Rule |
|---|---|
| 9 | Opt-in only |
| 10 | User chooses Primary Tool |
| 11 | Primary Tool ONLY (no SEC in Phase 2) |
| 12 | Fetch before analysis |
| 13 | Missing data = NOT AVAILABLE |
| 14 | Low confidence = Skip |
| 15 | Stop after Phase 2 report |

### Phase 3 — SEC EDGAR

| # | Rule |
|---|---|
| 16 | Opt-in only |
| 17 | VERIFIED / UNVERIFIED labels mandatory |
| 18 | No fabrication of SEC data |
| 19 | Stop after Phase 3 report |

### Phase 4 — Weekly Bias

| # | Rule |
|---|---|
| 20 | User request only |
| 21 | Three directions only (Positive / Negative / Neutral) |
| 22 | Estimate in range |
| 23 | Reason max 10 words |
| 24 | Mandatory tags per stock |

### Global

| # | Rule |
|---|---|
| 25 | No loop |
| 26 | No monitoring |
| 27 | No fabricated data |
| 28 | Format Phase 1-4 are LOCKED |
| 29 | Every session starts fresh |

---

## Status & Controls

| Control | Description |
|---|---|
| **Version** | 4.0 — Locked Output Templates for all 4 phases |
| **Authority Gate** | Primary Tool selected by user. SEC EDGAR is separate opt-in phase |
| **Evidence Integrity Gate** | Every important claim must be supported by real data (source URL, filing reference, or label) |
| **Completion Gate** | Phase only complete after every step in reference is done |
| **Stagnation Breaker** | If Phase 1 produces 0 opportunities after two attempts with two different sources, stop. Do not loop |
| **Autonomous Loop** | INSPECT → PLAN → BUILD → VALIDATE → DIAGNOSE → REPAIR → REVALIDATE |

---

## Change Log

| Area | v3.1 | v4.0 |
|---|---|---|
| Phase structure | 4 phases | 4 phases (unchanged) |
| Output templates | Described, not shown | **Explicit LOCKED templates** with placeholders |
| Placeholder convention | None | `Stock X`, `Stock Y`, `[TICKER]`, `[COMPANY]` — no real tickers in templates |
| Phase 1 output | "Follow format" | Full card template with all fields |
| Phase 2 output | "Follow format" | 4-block template (Summary + Catalyst + Reports + Ranking) |
| Phase 3 output | "Follow format" | 2-block template (Fetch Attempt + Verification Results) |
| Phase 4 output | "Follow format" | 4-component template (Table + Penjelasan + End of Session + Disclaimer) |
| AI instructions | Implicit | **Explicit `OUTPUT FORMAT INSTRUCTIONS` block** directing AI to reproduce exact structure |
| README | 3-phase workflow, v2.2 | **4-phase workflow, v4.0, fully rewritten in English** |

---

<div align="center">

**⚠️ NO MONITORING — This is read-only analysis. Not investment advice. No continuous monitoring.**

---

[View on GitHub](https://github.com/Relf0910/rfx1427-finance) · [Report Issue](https://github.com/Relf0910/rfx1427-finance/issues)

</div>
