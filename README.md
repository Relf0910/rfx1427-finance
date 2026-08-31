# RFX1427 Finance

AI financial news scanner and analysis framework with strict gate controls, fact-based approach, and official SEC EDGAR verification.

## Overview

RFX1427 Finance reads ONE news source selected by the user, filters public companies by trader profile, market focus, time horizon, materiality, and confidence, and performs Deep Analysis with SEC EDGAR verification only after explicit user opt-in.

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate data. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED`
- **OPT-IN ONLY** — Phase 2 & 3 only after user explicitly selects
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss

## Workflow

```
GATE 0 — INTAKE (3 questions)
    │
    ▼
PHASE 1 — SCANNER (News → Ticker Filter → Profile Filter → Materiality → Confidence → Phase 1 Report)
    │
    ▼
STOP 1 — USER OPT-IN
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Primary Tool → SEC Verification → Comparison Matrix)
    │
    ▼
STOP 2 — USER REQUEST
    │
    ▼
PHASE 3 — PLAIN SUMMARY → END
```

## Data Integrity Hierarchy

```
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

## References

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 Plain Summary | `references/phase3-plain-summary.md` |
| Error States | `references/error-states.md` |
| Hard Rules Master (37) | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Folder Structure

```
rfx1427-finance/
├── SKILL.md                    # Main skill definition
├── agents/
│   └── openai.yaml             # Agent configuration
├── references/
│   ├── intake-form.md          # Phase 0: Intake form
│   ├── phase1-scanner.md       # Phase 1: Scanner
│   ├── phase2-deep-analysis.md # Phase 2: Deep Analysis
│   ├── phase3-plain-summary.md # Phase 3: Plain Summary
│   ├── error-states.md         # Error state definitions
│   ├── hard-rules-master.md    # 37 hard rules
│   ├── decision-tree.md        # Decision tree
│   ├── change-log-v2.md       # Version 2.2 changelog
│   ├── data-integrity-hierarchy.md
│   └── acceptance-tests.md
└── README.md
```

## Status

Version: **2.2** (DRAFT)

See `SKILL.md` for complete documentation.
