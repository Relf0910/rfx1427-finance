# Fasa 2 — Deep Analysis

Source: Framework v3.0

## Overview

Fasa 2 performs detailed analysis on Phase 1 opportunities using user-selected primary tool and SEC EDGAR verification.

**Fasa 2 is: OPT-IN ONLY**

**Default Primary Tool: Google Finance** — If user does not choose, use Google Finance.

## STEP 2A — Primary Tool Selection

Ask:

> "Apa primary tool untuk deep analysis?"

Options:
- [Google Finance (Default)] [MarketBeat] [Skip]

→ If user does not choose, USE GOOGLE FINANCE AS DEFAULT.

### Action

If selects tool:
```text
primary_tool = selected tool
```
Proceed to Step 2B.

If selects Skip:
```text
END SESSION
```

### Hard Rules

- Do NOT select tool for user
- Do NOT run Fasa 2 without opt-in
- Do NOT offer Fasa 2 again after Skip
- SEC EDGAR is mandatory verification partner (not separately selected)

## STEP 2B — 3-Stage Verification

```text
STAGE 1 (Primary Data)
    ↓
STAGE 2 (SEC EDGAR Data)
    ↓
STAGE 3 (Compare, Analyze, Synthesize)
```

Next stage only starts after previous stage completes.

---

### STAGE 1 — Fetch Primary Tool Data

Fetch data for: EVERY PHASE 1 OPPORTUNITY

#### GOOGLE FINANCE

Fetch if available:
- Current price
- Price change %
- Recent news
- Analyst targets
- Analyst ratings
- Earnings data

#### MARKETBEAT

Fetch if available:
- Current price
- Price change %
- Short interest
- Analyst consensus
- Financial ratios

#### FINVIZ

Fetch if available:
- Current price
- Price change %
- Volume
- RSI
- SMA 20, SMA 50
- P/E, EPS
- Revenue
- Relevant news headlines

#### Primary Data Rule

If field not available:
```text
PRIMARY DATA — NOT AVAILABLE
```

Do NOT invent.

If primary tool fails:
```text
PRIMARY TOOL — BLOCKED
```

Do NOT claim data was fetched.

Internal state: `PRIMARY DATA FETCHED — [TOOL]`

---

### STAGE 2 — Fetch SEC EDGAR Data

Only after Stage 1 completes. Use ticker from Phase 1.

#### SEC Verification Matrix

| Item | Filing |
| --- | --- |
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

#### SEC Data States

**VERIFIED** — if SEC filing provides data:
```text
SEC_DATA
```
Record: filing type, filing date, relevant period, value, filing reference.

**UNVERIFIED** — if SEC data not available:
```text
UNVERIFIED — SEC DATA NOT AVAILABLE
```

#### Hard Rule

```text
NO SEC DATA ≠ FALSE
```

It means `UNVERIFIED`. Do not force verification.

Internal state: `SEC DATA FETCHED — [VERIFIED / UNVERIFIED]`

---

### STAGE 3 — Compare, Analyze & Synthesize

Only after Stage 1 and Stage 2 complete.

AI analysis tasks:
1. Compare Primary vs SEC data
2. Verify consistency
3. Confirm mechanism
4. Assess timing
5. Identify levels
6. Apply confidence gate

#### Data Authority Rule

SEC EDGAR is authority for financial filing data. Primary tool for market/technical/analyst data that SEC is not designed to provide.

Examples of Primary Tool data: Current price, intraday change, volume, RSI, VWAP, technical indicators, analyst targets, analyst consensus.

#### Comparison Matrix

| Situation | Status | Action |
| --- | --- | --- |
| Primary = SEC | MATCH — CONFIRMED | Use data |
| Primary ≠ SEC, SEC authoritative | DATA MISMATCH — SEC OVERRIDE | Use SEC |
| SEC unavailable | UNVERIFIED | Use Primary + label |
| Primary unavailable, SEC available | SEC ONLY | Use SEC |
| Both unavailable | DATA NOT AVAILABLE | Do not use |

---

### STEP 3.1 — Confirm Mechanism

Check transmission channel from Phase 1.

Output:
- Confirmed
- Partially Confirmed
- Rejected

If `Rejected`, opportunity cannot be presented as valid.

### STEP 3.2 — Assess Timing

Match with trader profile:

| Profile | Timing |
| --- | --- |
| SCALPER | 5–15 minutes |
| INTRADAY | Current session |
| SWING | Days → weeks |
| INVESTOR | Long-term |

Output: Strong / Partial / Poor

### STEP 3.3 — Identify Price Levels

| Profile | Levels |
| --- | --- |
| SCALPER | Pre-market high, Pre-market low, R1, R2 |
| INTRADAY | VWAP, Opening Range High, Opening Range Low |
| SWING | 20-day SMA, 50-day SMA, Recent swing high/low |
| INVESTOR | 52-week range, Current P/E, Historical valuation |

#### Price Level Integrity Rule

If data not available:
```text
NOT AVAILABLE
```

Do NOT invent numbers. Do NOT claim exact level if source does not support it.

### STEP 3.4 — Confidence Gate

After all verification:
- High
- Medium
- Low

#### Low Confidence

If `Confidence = Low`:
```text
LOW CONFIDENCE — SKIP
```

Do NOT include in final Deep Analysis report.

#### If All Opportunities Are Low

Output:
> No opportunities passed the final confidence gate.

Do NOT force-fill report.

---

## FASA 2 — OUTPUT FORMAT (LOCKED — AGORA STYLE)

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

### Agora Dashboard — Deep Analysis Report

```markdown
# DEEP ANALYSIS — [DATE]

---

## CARD [#1] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Primary Tool | [Google Finance / MarketBeat / Finviz] |
| SEC Status | Verified / Unverified / Mismatch / SEC Only |

### Data Comparison

| Item | Primary | SEC | Status |
|------|---------|-----|--------|
| [Item 1] | [X] | [Y] | Match / Mismatch / Unverified |
| [Item 2] | [X] | [Y] | Match / Mismatch / Unverified |

### Catalyst
[Factual summary with labels: FACT / INFERENCE / ESTIMATE]

### Mechanism
**Confirmed** / Partially Confirmed / Rejected

### Timing Fit
**Strong** / Partial / Poor (matched to [Profile])

### Relevant Levels
- [Level 1]: [Value]
- [Level 2]: [Value]

### Confidence
**HIGH** / MEDIUM

### Risk / Uncertainty
[Any identified risks or uncertainties]

---
```

## STOP 2

After Fasa 2 report:

```text
STOP
WAIT FOR USER
```

Do NOT proceed to Fasa 3 automatically.

User options at STOP 2:
- Proceed to Fasa 3 (SEC EDGAR Verification)
- Proceed to Fasa 4 (Ringkesan Bias) — only if requested
- Skip → END
