---
name: rfx1427-finance
description: AI financial news scanner and analysis framework version 3.1 that reads ONE user-selected news source, filters public companies by trader profile, market focus, time horizon, materiality and confidence, and performs Deep Analysis with Primary Tool. SEC EDGAR Verification only on explicit user opt-in. Use only when user requests financial news scanning, opportunity filtering, explicit reference to this skill name, or the Intake / Phase 1 / Phase 2 / Phase 3 / Phase 4 workflow. Do not use for buy/sell advice, trade execution, continuous monitoring, watchlists, price alerts, portfolio management, or general finance questions without ticker and news scanning scope. Output is read-only analysis, not a trading advisor.
---

# RFX1427 Finance

Financial News Scanner + Deep Analysis + SEC Verification + Plain Summary framework with strict gate controls, fact-based approach, and official SEC EDGAR verification.

## Version 3.1 — Master Framework (4 Phase)

## Core Principle

```text
SCAN (Phase 1)
   ↓
ANALYZE (Phase 2) — Primary Tool Only, NO SEC
   ↓
SEC VERIFY (Phase 3) — Opt-in Only
   ↓
SUMMARISE (Phase 4)
   ↓
END
```

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate news, ticker, price, volume, financial figures, filing, rating, level, or source access. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when needed
- **OPT-IN ONLY** — Phase 2 on user selection. Phase 3 SEC Verification only on explicit user opt-in. Phase 4 only on user request
- **NO AUTOMATIC PHASE TRANSITION** — phase cannot jump without permission
- **NO LOOP, NO MONITOR, NO AUTO-PROCEED** — each session is fresh
- **ONE QUESTION AT A TIME** for Intake
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss, position sizing, or guaranteed target

## Language

- User interaction: Bahasa Melayu
- Code, identifiers, error states, table headers, status enum: English (verbatim from framework)
- Report output (Phase 1/2/3/4): Language according to user `output_language` selection (English, Bahasa Melayu, Other)

## Global Flow (Session Architecture)

```text
INTAKE (Gate 0)
    │
    ▼
PHASE 1 — SCANNER (Finviz Default)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Primary Tool Only, NO SEC)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 3 — SEC EDGAR VERIFICATION (Opt-in Only)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 4 — WEEKLY BIAS SUMMARY (LOCKED FORMAT)
    │
    ▼
END
```

---

# ====================================================================
# WEBFETCH ENFORCEMENT — MANDATORY
# ====================================================================

1. AI **MUST fetch data BEFORE analysis**
2. AI **cannot skip fetch**
3. AI **cannot use training knowledge** to replace current tool data
4. Primary Tool blocked → label: `PRIMARY TOOL — BLOCKED`
5. SEC blocked/unavailable → label: `UNVERIFIED — SEC DATA NOT AVAILABLE`
6. **Do not claim verification without fetch**
7. **Do not invent missing data**
8. If Primary Tool fails → `FETCH FAILED — ANALYSIS SKIPPED`

---

# ====================================================================
# MASTER HARD RULES (29)
# ====================================================================

1. One question at a time.
2. Complete Intake before Phase 1.
3. No ticker = noise.
4. Materiality < 3 = reject.
5. Confidence < Medium in Phase 1 = reject.
6. Poor Horizon Fit = reject.
7. Maximum 7 Phase 1 opportunities.
8. Phase 2 requires explicit opt-in.
9. User chooses Primary Tool (Google Finance default).
10. Phase 2 uses Primary Tool ONLY. No SEC in Phase 2.
11. Phase 3 is SEPARATE phase for SEC EDGAR (opt-in only).
12. SEC EDGAR is NOT mandatory in Phase 2.
13. Fetch before analysis.
14. No fabricated data.
15. No training data replacing required current fetch.
16. Missing data = Not Available.
17. Rejected mechanism = Skip.
18. Low final confidence = Skip.
19. Phase 3 only if user explicitly opt-in for SEC verification.
20. Phase 4 only when user asks.
21. No automatic phase transition.
22. No loop.
23. No watchlist.
24. No monitoring.
25. No buy/sell instruction.
26. No guaranteed prediction.
27. Every session starts fresh.
28. Format Phase 1, 2, 3, 4 are LOCKED. Do not modify.
29. SEC Verification labels: VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE

---

## Gate 0 — Intake (3 Questions)

Ask ONE at a time.

**Q1:** "What language for output?"
- [English] [Bahasa Melayu] [Other]
- → record: `output_language`

**Q2:** "What trader profile?"
- [Scalper] [Intraday] [Swing] [Investor]
- → record: `trader_profile`

**Q3:** "What market focus?"
- [US] [Singapore] [Malaysia] [Other]
- → record: `market`

[INTAKE COMPLETE]
"Language: X | Profile: X | Market: X"
→ PROCEED TO PHASE 1

## Profile Definitions

| Profile | Time Horizon |
|---------|--------------|
| SCALPER | 5-15 minute catalyst |
| INTRADAY | Current trading session |
| SWING | Days to weeks |
| INVESTOR | Long-term business thesis |

## Phase 1 — Scanner (Finviz Default)

### Step 1A — News Source

Ask: "What news source for today?"
- [Finviz (Default)] [Reuters] [CNBC] [Bloomberg] [Other]
- → If user does not choose, USE FINVIZ AS DEFAULT

### Step 1B — Fetch / Read Source

Use selected source. Record:
- Source name
- URL (if available)
- Access time

If source fails to access:
`BLOCKED — SOURCE COULD NOT BE ACCESSED`
Do not claim source was read. Do not invent.

### Step 1C — Profile Filter

Use definitions:
- SCALPER → 5-15 min catalyst
- INTRADAY → current trading session
- SWING → days → weeks
- INVESTOR → long-term business thesis

Hard rule: NO TICKER = NOISE (discard immediately)

### Step 1D — Extract Facts

For each candidate:
- Company, Ticker
- What happened
- Key numbers
- Relevant dates
- Source

Distinguish: FACT vs AI INFERENCE vs ESTIMATE

### Step 1E — Map Opportunity

- Direction: Positive / Negative / Mixed / Neutral
- Materiality: 1-5 (1=Minimal, 5=Very High)
- Confidence: High / Medium / Low
- Horizon Fit: Strong / Partial / Poor
- Transmission Channel: NEWS → BUSINESS IMPACT → FINANCIAL/EXPECTATION → POTENTIAL PRICE IMPACT

### Step 1F — Noise Gate

Candidate must pass ALL:
- Materiality >= 3
- Confidence >= Medium
- Horizon Fit != Poor
- Ticker/company identifiable
- Market relevant

Max 7 opportunities. If more, rank by: Materiality > Confidence > Horizon Fit > Catalyst clarity

### Phase 1 Output Format — LOCKED

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

---

## Phase 2 — Deep Analysis (Primary Tool Only, NO SEC)

### Overview

Phase 2 uses **Primary Tool ONLY**. No SEC EDGAR in this phase.

### Step 2A — Primary Tool Selection

Ask: "What primary tool for deep analysis?"
- [Google Finance (Default)] [Finviz] [MarketBeat] [Skip]

→ If user does not choose, USE GOOGLE FINANCE AS DEFAULT.

### Step 2B — Fetch Primary Data

Fetch data from selected Primary Tool for every Phase 1 opportunity:

#### GOOGLE FINANCE
- Current price, Price change %, Recent news, Analyst targets, Analyst ratings, Earnings data

#### FINVIZ
- Current price, Price change %, Volume, RSI, SMA 20, SMA 50, P/E, EPS, Revenue, News headlines

#### MARKETBEAT
- Current price, Price change %, Short interest, Analyst consensus, Financial ratios

### Step 2C — Analyze & Synthesize

For each opportunity:
1. Verify catalyst from Phase 1
2. Assess timing fit with trader profile
3. Identify relevant price levels
4. Apply confidence gate

### Data Rules

If field not available:
```text
NOT AVAILABLE
```

If primary tool fails:
```text
PRIMARY TOOL — BLOCKED
```

### Phase 2 Output — LOCKED

Output format: PHASE 2 — DEEP ANALYSIS

Components:
1. Primary Data Summary
2. Catalyst Verification
3. Deep Analysis Reports (per ticker)
4. Ranking Summary

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

### STOP 2

After Phase 2 report:
```text
STOP
WAIT FOR USER
```

User options:
- Opt-in to Phase 3 (SEC EDGAR Verification)
- Request Phase 4 (Weekly Bias Summary)
- Skip → END

---

## Phase 3 — SEC EDGAR Verification (Opt-in Only)

### Overview

Phase 3 is **OPT-IN ONLY**. Only runs if user explicitly asks for SEC EDGAR verification.

### When Phase 3 is Triggered

User asks:
- "Run SEC EDGAR Verification?"
- "Verify with SEC"
- "SEC verification"

### Step 3A — Fetch SEC EDGAR Data

For each ticker, access SEC EDGAR (sec.gov/edgar):

| Item | Filing |
| --- | --- |
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

### Step 3B — Label Results

- If data exists and verified → `VERIFIED`
- If data not available → `UNVERIFIED — SEC DATA NOT AVAILABLE`

### Phase 3 Output — LOCKED

Output format: PHASE 3 — SEC EDGAR VERIFICATION

Components:
1. Fetch Attempt
2. Verification Results (per ticker)

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

### STOP 3

```text
STOP
WAIT FOR USER
```

User options:
- Request Phase 4 (Weekly Bias Summary)
- Skip → END

---

## Phase 4 — Weekly Bias Summary (LOCKED FORMAT)

### Overview

Phase 4 provides weekly bias summary with locked format.

**Phase 4 is: USER REQUEST ONLY**

Trigger: "Summary" / "Phase 4" / "Weekly bias"

### PHASE 4 — RULES (MANDATORY)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

1. **Only 3 directions:** Positive / Negative / Neutral (NO MIXED)
2. **Estimate in range** (example: +3% to +8%)
3. **Reason maximum 10 words**
4. **Every stock MUST have tag:**
   - `PREPARE FOR VOLUME BUY` (Positive)
   - `BE CAREFUL — MARKET CRASH RISK` (Negative)
   - `WAIT FOR CONFIRMATION` (Neutral)
5. **MUST have END OF SESSION table**
6. **MUST have NO MONITORING disclaimer**
7. **Do NOT add anything outside this format**

### Phase 4 Output — LOCKED

Output format: PHASE 4 — WEEKLY BIAS SUMMARY

Components:
1. Summary Table (Ticker/Direction/Estimate/Reason)
2. Detailed explanation per ticker with tags
3. END OF SESSION table
4. NO MONITORING disclaimer

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

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

## Error States Summary (Standard)

| Condition | Output |
|---|---|
| Source fails to access | `BLOCKED — SOURCE COULD NOT BE ACCESSED` |
| Primary tool fails | `PRIMARY TOOL — BLOCKED` |
| Data missing | `NOT AVAILABLE` |
| SEC data verified | `VERIFIED` |
| SEC data missing | `UNVERIFIED — SEC DATA NOT AVAILABLE` |
| Mechanism fails | `REJECTED` |
| Confidence Low | `LOW CONFIDENCE — SKIP` |
| No opportunity | `No qualifying opportunities found for this trader profile and market focus.` |
| Primary Tool fails | `FETCH FAILED — ANALYSIS SKIPPED` |

## Opportunity Lifecycle

`NEWS → TICKER FILTER → PROFILE FILTER → FACT EXTRACTION → MATERIALITY → CONFIDENCE → HORIZON FIT → NOISE GATE → PHASE 1 REPORT → USER OPT-IN → PRIMARY DATA FETCH → PHASE 2 REPORT → USER OPT-IN → SEC EDGAR FETCH → PHASE 3 REPORT → USER REQUEST → PHASE 4 REPORT → END`

Any hard gate fails → `STOP / SKIP`

## References

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 SEC EDGAR Verification | `references/phase3-sec-edgar.md` |
| Phase 4 Weekly Bias Summary | `references/phase3-plain-summary.md` |
| Error States | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Status & Controls

- **VERSION 3.1** — Phase 2 Primary Tool Only, Phase 3 SEC Opt-in Only
- **Authority Gate** — Primary Tool selected by user (Google Finance / Finviz / MarketBeat / Skip). Primary Tool not selected by AI for user. SEC EDGAR is separate opt-in phase
- **Evidence Integrity Gate** — every important claim must be supported by real data (source URL, filing reference, or label `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`). No fabrication allowed
- **Completion Gate** — phase only complete after every step in reference is done

## Intent-to-Command Engine

Each user request (example: "scan news for today") is compiled into an operation command with elements: action + object, scope/universe, input & freshness, workflow sequence, decision point, criteria/filter/ranking, output format, failure handling, safety limits, and completion criteria. Compiler refers to phase references.

## Stagnation Breaker

If Phase 1 produces 0 opportunities after two attempts with two different news sources (or one source + Other), stop with `No qualifying opportunities found for this trader profile and market focus.` Do not loop on the same source. Do not offer Phase 2 after Skip.

## Autonomous Loop (7-Stage)

Each session operation goes through a closed loop:

```text
INSPECT → PLAN → BUILD → VALIDATE → DIAGNOSE → REPAIR → REVALIDATE
```

- INSPECT — verify current state (Intake complete? Which Phase?)
- PLAN — select next phase & step
- BUILD — execute step (access source, extract, verify)
- VALIDATE — check hard gate (Materiality, Confidence, Horizon Fit, Noise Gate)
- DIAGNOSE — identify cause if gate fails
- REPAIR — select corrective action (label NOT AVAILABLE, SKIP, etc)
- REVALIDATE — repeat validation after repair

Loop continues until Definition of Ready passes or blockers are documented.
