# Phase 2 — Deep Analysis (Primary Tool Only, NO SEC)

Source: Framework v3.1

## Overview

Phase 2 performs detailed analysis on Phase 1 opportunities using **Primary Tool ONLY**.

**IMPORTANT: No SEC EDGAR in Phase 2. SEC is handled in Phase 3 separately.**

**Phase 2 is: OPT-IN ONLY**

**Default Primary Tool: Google Finance** — If user does not choose, use Google Finance.

## PHASE 2 — RULES (MANDATORY)

1. **FETCH STATUS must be shown** — SUCCESS / BLOCKED / UNVERIFIED
2. **Do NOT invent data** — use NOT AVAILABLE, UNVERIFIED, BLOCKED
3. **Do NOT give buy/sell signals** — use labels: POSITIVE / NEUTRAL / NEGATIVE
4. **NO SEC in Phase 2** — SEC is handled in Phase 3 (separate opt-in phase)

## STEP 2A — Primary Tool Selection

Ask:

> "What primary tool for deep analysis?"

Options:
- [Google Finance (Default)] [Finviz] [MarketBeat] [Skip]

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
- Do NOT run Phase 2 without opt-in
- Do NOT offer Phase 2 again after Skip
- **No SEC EDGAR in Phase 2** — SEC verification is Phase 3 (separate opt-in)

## STEP 2B — Fetch Primary Data

Fetch data from selected Primary Tool for **EVERY PHASE 1 OPPORTUNITY**.

### GOOGLE FINANCE

Fetch if available:
- Current price
- Price change %
- Recent news
- Analyst targets
- Analyst ratings
- Earnings data

### FINVIZ

Fetch if available:
- Current price
- Price change %
- Volume
- RSI
- SMA 20, SMA 50
- P/E, EPS
- Revenue
- Relevant news headlines

### MARKETBEAT

Fetch if available:
- Current price
- Price change %
- Short interest
- Analyst consensus
- Financial ratios

### Primary Data Rules

If field not available:
```text
NOT AVAILABLE
```

Do NOT invent.

If primary tool fails:
```text
PRIMARY TOOL — BLOCKED
```

Do NOT claim data was fetched.

Internal state: `PRIMARY DATA FETCHED — [TOOL]`

---

## STEP 2C — Analyze & Synthesize

Only after all Primary Data is fetched.

AI analysis tasks:
1. Verify catalyst from Phase 1
2. Confirm transmission mechanism
3. Assess timing fit with trader profile
4. Identify relevant price levels
5. Apply confidence gate

### Timing Fit

Match with trader profile:

| Profile | Timing |
| --- | --- |
| SCALPER | 5–15 minutes |
| INTRADAY | Current session |
| SWING | Days → weeks |
| INVESTOR | Long-term |

Output: Strong / Partial / Poor

### Price Levels

| Profile | Levels |
| --- | --- |
| SCALPER | Pre-market high, Pre-market low, R1, R2 |
| INTRADAY | VWAP, Opening Range High, Opening Range Low |
| SWING | 20-day SMA, 50-day SMA, Recent swing high/low |
| INVESTOR | 52-week range, Current P/E, Historical valuation |

### Price Level Integrity Rule

If data not available:
```text
NOT AVAILABLE
```

Do NOT invent numbers. Do NOT claim exact level if source does not support it.

### Confidence Gate

After analysis:
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

## PHASE 2 — OUTPUT FORMAT (LOCKED)

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

### PHASE 2 — DEEP ANALYSIS

#### 1. Primary Data Summary

```markdown
| Ticker | Company | Primary Tool | Fetch Status |
|--------|---------|--------------|--------------|
| XXX | [Name] | [Tool] | SUCCESS / BLOCKED / UNVERIFIED |
```

#### 2. Catalyst Verification

```markdown
| Ticker | Phase 1 Catalyst | Verified | Notes |
|--------|------------------|----------|-------|
| XXX | [Description] | YES / PARTIAL / NO | [Notes] |
```

#### 3. Deep Analysis Reports

```markdown
## [TICKER] — [COMPANY]

| Field | Value |
|-------|-------|
| **FETCH STATUS** | **SUCCESS** / BLOCKED / UNVERIFIED |
| Primary Tool | [Google Finance / Finviz / MarketBeat] |
| Direction | **POSITIVE** / NEUTRAL / NEGATIVE |

### Catalyst
[Factual summary with labels: FACT / INFERENCE / ESTIMATE]

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

#### 4. Ranking Summary

```markdown
## RANKING SUMMARY

| Rank | Ticker | Direction | Confidence | Timing Fit |
|------|--------|-----------|------------|------------|
| 1 | XXX | POSITIVE | HIGH | Strong |
| 2 | XXX | NEUTRAL | MEDIUM | Partial |
```

---

## STOP 2

After Phase 2 report:

```text
STOP
WAIT FOR USER
```

Do NOT proceed to Phase 3 automatically.

User options at STOP 2:
- Opt-in to Phase 3 (SEC EDGAR Verification)
- Request Phase 4 (Weekly Bias Summary)
- Skip → END
