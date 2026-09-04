# Phase 2 — Deep Analysis (Python + AI Unified, Primary Tool Only, NO SEC)

Source: Framework v4.5

## Overview

Phase 2 performs detailed analysis on Phase 1 opportunities using **Primary Tool ONLY**. Python works directly with the AI: Python fetches market data from the selected Primary Tool and prepares it; the AI analyzes and judges. No collect-then-read two-pass.

**IMPORTANT: No SEC EDGAR in Phase 2. SEC is handled in Phase 3 separately.**

**Phase 2 is: OPT-IN ONLY (user chooses to run it)**

**Default Primary Tool: Google Finance** — If user does not choose, use Google Finance.

## PHASE 2 — RULES (MANDATORY)

1. **FETCH STATUS must be shown** — SUCCESS / BLOCKED / UNVERIFIED
2. **Do NOT invent data** — use NOT AVAILABLE, UNVERIFIED, BLOCKED
3. **Do NOT give buy/sell signals** — use labels: POSITIVE / NEUTRAL / NEGATIVE
4. **NO SEC in Phase 2** — SEC is handled in Phase 3 (mandatory, auto-proceeds)
5. **Python fetches + prepares; AI judges** — Python does NOT analyze

## Python + AI Division of Work (Phase 2)

| Layer | What it does |
|-------|--------------|
| **Python** | Fetch market data from the selected Primary Tool, format it per ticker, assist fallback. Python does NOT analyze or judge. |
| **AI** | Reads the fetched data, verifies the catalyst, assesses timing fit vs trader profile, identifies price levels, applies the confidence gate, outputs the analysis. |

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

## STEP 2B — Python-Assisted Fetch (Primary Data)

Python fetches data from the selected Primary Tool for **EVERY PHASE 1 OPPORTUNITY** and streams it to the AI. Python prepares; AI judges.

### Python access method (by tool)

```text
Google Finance / Yahoo -> yfinance
Finviz                 -> finvizfinance
MarketBeat / other     -> requests + BeautifulSoup4
```

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

### Python Failure — Layered Fallback (Phase 2)

If Python fetch fails, use the layered fallback. Python ALWAYS tries the Primary Tool first; the label is ONLY declared when both methods fail.

```text
LAYER 1 — PYTHON FETCH (Primary)      -> if success, send to AI (Step 2C)
LAYER 2 — ALTERNATE METHOD (Fallback) -> if Python fails, try an alternate
                                         market-data method (Alpha Vantage /
                                         Finnhub / another free source, or
                                         retry once). If success, send to AI.
LAYER 3 — LABEL (Final)               -> if both fail, AI applies:
                                           per ticker   -> PRIMARY TOOL — BLOCKED
                                           all tickers  -> FETCH FAILED — ANALYSIS SKIPPED
```

Rules:
- Python ALWAYS tries the Primary Tool first (Layer 1).
- Layer 2 (alternate method) is ONLY used when Python fails.
- The label is ONLY declared when both layers fail (Layer 3).
- Python does NOT judge; the AI applies the label.

---

## STEP 2C — Analyze & Synthesize (AI judges, ONE PASS)

Python delivers the fetched data; the AI performs the analysis. AI does NOT depend on a separate collect-then-read step.

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

# PHASE 2 — DEEP ANALYSIS (LOCKED FORMAT)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

Output must begin with:

```markdown
**PHASE 2 — DEEP ANALYSIS**
Primary Tool: **[Google Finance / Finviz / MarketBeat]**
Akses: [DATE TIME]
```

Then the four mandatory blocks in this order:

### 1. Primary Data Summary

```markdown
| Ticker | Company | Primary Tool | Fetch Status |
|--------|---------|--------------|--------------|
| Stock X | [Name] | [Tool] | SUCCESS / BLOCKED / UNVERIFIED |
| Stock Y | [Name] | [Tool] | SUCCESS / BLOCKED / UNVERIFIED |
```

### 2. Catalyst Verification

```markdown
| Ticker | Phase 1 Catalyst | Verified | Notes |
|--------|------------------|----------|-------|
| Stock X | [Short description] | YES / PARTIAL / NO | [Notes] |
| Stock Y | [Short description] | YES / PARTIAL / NO | [Notes] |
```

### 3. Deep Analysis Reports

For each ticker that passed the confidence gate, output:

```markdown
## [TICKER] — [COMPANY]

| Field | Value |
|-------|-------|
| **FETCH STATUS** | **SUCCESS** / BLOCKED / UNVERIFIED |
| Primary Tool | [Tool] |
| Direction | **POSITIVE** / NEUTRAL / NEGATIVE |

### Catalyst
[Factual summary with FACT / INFERENCE / ESTIMATE labels]

### Timing Fit
**Strong** / Partial / Poor (matched to [Profile])

### Relevant Levels
- [Level description]: [Value or NOT AVAILABLE]
- [Level description]: [Value or NOT AVAILABLE]

### Confidence
**HIGH** / MEDIUM

### Risk / Uncertainty
[Short risk note]

---
```

### 4. Ranking Summary

```markdown
| Rank | Ticker | Direction | Confidence | Timing Fit |
|------|--------|-----------|------------|------------|
| 1 | Stock X | POSITIVE | HIGH | Strong |
| 2 | Stock Y | NEGATIVE | MEDIUM | Partial |
```

End Phase 2 with exactly:

```text
STOP
WAIT FOR USER
```

## Hard Rules for Phase 2

1. Never skip a required table or section
2. Never invent data. Use NOT AVAILABLE, BLOCKED, or UNVERIFIED when data is missing
3. Phase 2 waits for user opt-in; Phase 3 is mandatory and auto-proceeds
4. Keep the exact markdown structure, bold labels, and stop phrases shown above
5. Never include buy/sell recommendations, entry prices, stop-loss levels, position sizing, or guaranteed targets
