# Phase 1 — Scanner

Source: Framework v3.1

## Overview

Phase 1 reads ONE news source selected by user, filters public companies by trader profile, and extracts qualifying opportunities through the Noise Gate.

**Default Source: Finviz** — If user does not choose, use Finviz.

## 6 Steps: `1A → 1B → 1C → 1D → 1E → 1F`

## STEP 1A — News Source

Ask:

> "What news source for today?"

Options:
- [Finviz (Default)] [Reuters] [CNBC] [Bloomberg] [Other]

→ If user does not choose, USE FINVIZ AS DEFAULT.

Record as: `news_source`

## STEP 1B — Fetch / Read Source

Use selected `news_source`.

Required:
1. Access source
2. Record URL if available
3. Record access time
4. Read accessible relevant content
5. Apply market focus filter
6. Continue to Step 1C

### Source Access Rule

If source fails to access:

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

Do not claim source was read. Do not generate fabricated scanner report.

## STEP 1C — Filter By Trader Profile

### Profile Definitions

| Profile | Time Horizon | Look For |
|---------|--------------|----------|
| SCALPER | 5-15 minutes | Pre-market gap, earnings reaction, Fed statement, major breaking news, immediate corporate catalyst |
| INTRADAY | Current session | Economic data, CEO interview, analyst upgrade/downgrade, earnings, sector-moving news, regulatory announcement |
| SWING | Days → Weeks | Earnings preview, sector rotation, guidance change, short-interest changes, product catalyst, industry developments |
| INVESTOR | Long-term | 10-K, 10-Q, new CEO, M&A, regulatory shift, capital allocation, competitive moat, structural industry change |

### Hard Filter — NO TICKER = NOISE

If no ticker or identifiable public company:

```text
NO TICKER = NOISE
```

Discard immediately.

## STEP 1D — Extract Facts

For each candidate, record:

- Company
- Ticker
- What happened
- Key numbers
- Relevant dates
- Market context
- Source

### Fact Classification Rule

Distinguish three categories:

- **FACT** — supported by source
- **AI INFERENCE** — AI interpretation based on facts
- **ESTIMATE** — approximation based on available data

Do not mix categories.

## STEP 1E — Map Opportunity

For each candidate:

### Direction
- Positive
- Negative
- Mixed
- Neutral

### Transmission Channel
```text
NEWS
  ↓
BUSINESS IMPACT
  ↓
FINANCIAL/EXPECTATION
  ↓
POTENTIAL PRICE IMPACT
```

### Materiality (1-5)

| Score | Meaning |
| ----: | --- |
| 1 | Minimal |
| 2 | Low |
| 3 | Moderate |
| 4 | High |
| 5 | Very High |

### Confidence

- **HIGH** — Strong source support, clear catalyst, clear mechanism, low material uncertainty
- **MEDIUM** — Core facts supported, mechanism reasonably supported, some uncertainty exists
- **LOW** — Missing data, conflicting evidence, weak mechanism, high uncertainty

### Horizon Fit
- Strong
- Partial
- Poor

## STEP 1F — Noise Gate

Candidate MUST pass ALL:

```text
Materiality >= 3
Confidence >= Medium
Horizon Fit != Poor
Identifiable ticker/company
Market focus relevant
```

Maximum: **10 opportunities**

### Ranking

If more than 10:

1. Materiality (descending)
2. Confidence (descending)
3. Horizon Fit (Strong > Partial)
4. Catalyst clarity

Take maximum 10.

---

# PHASE 1 — MARKET SCANNER (LOCKED FORMAT)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

Output must begin with:

```markdown
# MARKET SCANNER — [DATE] | Source: [SOURCE]

Akses: [DATE TIME]
Items scanned: N | Material calls: M | Filtered as noise: K
```

Then for every qualifying opportunity (maximum 10), output a card in this exact structure:

```markdown
## CARD [#N] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Direction | **Positive** / Negative / Mixed / Neutral |
| Materiality | ★★★☆☆ (X/5) |
| Confidence | HIGH / MEDIUM / LOW |
| Horizon Fit | Strong / Partial / Poor |

### What Happened
[Factual summary. Explicitly label FACT / INFERENCE / ESTIMATE where relevant]

### Why It Matters
[1–3 sentences explaining the transmission mechanism for the chosen trader profile]

### Key Data
- [Key number or fact 1]
- [Key number or fact 2]
- Date: [Relevant date]

### Source
[Source name] | [URL if available]

---
```

After the last card, output exactly:

```text
STOP
WAIT FOR USER
```

Do not proceed to Phase 2 unless the user explicitly opts in.

## Hard Rules for Phase 1

1. Never skip a required table or section
2. Never invent data. Use NOT AVAILABLE, BLOCKED, or UNVERIFIED when data is missing
3. Never auto-advance phases. Always stop and wait for explicit user opt-in
4. Keep the exact markdown structure, bold labels, and stop phrases shown above
5. Never include buy/sell recommendations, entry prices, stop-loss levels, position sizing, or guaranteed targets
