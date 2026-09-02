# Phase 1 — Scanner

Source: Framework v4.6

## Overview

Phase 1 is a **Python + AI unified flow**. Python brings the AI directly to the selected news source and assists reading in real time. The AI reads each item with a trader-profile lens, filters by trader profile and market focus, applies a **positive-only** scan, and outputs **exactly 7 positive opportunities — WAJIB 7, profile-adaptive** through the Noise Gate — in one single pass. Scan counts are internal and never disclosed. Python auto-expands the fetch window (up to 100 items + pagination + alternate source + Layer 2 web_search) until 7 are assembled.

**Default Source: Finviz** — If user does not choose, use Finviz.

## 6 Steps: `1A → 1B → 1C → 1D → 1E → 1F`

## Python + AI Division of Work

| Layer | What it does |
|-------|--------------|
| **Python** | Fetch/stream the source, format each item, assist search fallback. Python does NOT filter, score, or judge. |
| **AI** | Reads each item, applies trader profile, identifies tickers, judges direction (positive-only), filters noise, ranks, outputs the best 7 positive cards. |

## STEP 1A — News Source

Ask:

> "What news source for today?"

Options:
- [Finviz (Default)] [Yahoo Finance] [Investing.com] [TradingView]
- [StockTitan] [PR Newswire] [GlobeNewswire] [Motley Fool]
- [Barchart] [StockAnalysis.com] [Other]

SOURCE PRIORITY:
- Finviz is the DEFAULT and PRIMARY source.
- All other listed sources are FREE alternatives (see Source Library Map in SKILL.md).
- The user may pick any source.

→ If user does not choose, USE FINVIZ AS DEFAULT.

If user selects "Other" or a custom source:
- Accept ANY source (URL, platform name, website, RSS feed, document).
- Do not reject or judge the source.
- If the source is a known BLOCKED source (CNBC, Reuters, Bloomberg, etc.), inform the user that Python will try and fall back to web_search if it fails.

Record as: `news_source`

## STEP 1B — Python-Assisted Read (ONE PASS, 3-Layer Hybrid Fallback)

Python brings the AI directly to the selected source and streams each news item. The AI reads each item live with its trader lens — there is NO separate collect-then-read step.

Plain: LAYER 1 (Python fetch) → LAYER 2 (AI web_search) → LAYER 3 (BLOCKED).

Required:
1. Python accesses source using Source Library Map library (Layer 1)
2. If Python fails → AI uses web_search fallback (Layer 2)
3. If both fail → BLOCKED (Layer 3)
4. Record URL if available
5. Record access time
6. Read each item live, apply trader-profile + market focus
7. Discard negative/mixed/neutral + noise immediately
8. Continue to Step 1C

### Source Access Rule

If both Python fetch AND AI web_search fail:

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

Do not claim source was read. Do not generate fabricated scanner report. Do not use training knowledge as a substitute.

### Fallback Architecture (v4.6 — refill to Exactly 7)

```text
LAYER 1 — PYTHON FETCH (Primary): use Source Library Map library (up to 100 items).
  Success → stream items to AI → AI reads live → if <7 qualifying, Python auto-expands
  (next page / next source e.g. StockTitan) before invoking Layer 2.
LAYER 2 — AI WEB_SEARCH (Fallback + Refill): if Python fails (FALLBACK_NEEDED) OR if <7
  qualifying after Layer 1, AI uses web_search to collect up to 50 additional items to
  refill toward exactly 7. AI reads refilled items with trader lens, re-applies Noise Gate
  + profile-adaptive ranking until 7 are assembled. Scan counts are internal, never disclosed.
LAYER 3 — BLOCKED (Final): only when all layers exhausted.
  Fail-safe (<7 even after all layers): output what exists with disclaimer and documented
  blocker; do NOT fabricate, do NOT lower thresholds.
```

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

## STEP 1E — Map Opportunity (POSITIVE ONLY)

For each candidate:

### Direction
- **Positive** (only positive is reported)
- Negative / Mixed / Neutral → discarded (positive-only scan)

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
Direction Positive (not negative/mixed/neutral)
Materiality >= 3
Confidence >= Medium
Horizon Fit != Poor
Identifiable ticker/company
Market focus relevant
```

Exactly: **7 positive opportunities — WAJIB 7 (Profile-Adaptive)**

### Ranking (Profile-Adaptive)

Base order (all profiles):
1. Materiality (descending)
2. Confidence (HIGH > MEDIUM)
3. Horizon Fit (Strong > Partial)
4. Catalyst clarity
5. News strength (most recent/fresh first)

Profile weighting (applied on top of base order):
| Profile | Time Horizon | Weighting |
|---------|--------------|-----------|
| SCALPER | 5–15 minutes | Freshness <60m heaviest; pre-market gap / volume spike = bonus |
| INTRADAY | Current session | Intraday catalyst (earnings today, upgrade/downgrade session, CEO interview) = bonus |
| SWING | Days → Weeks | Guidance / sector rotation / short-interest / product catalyst = bonus; freshness moderate |
| INVESTOR | Long-term | Structural / M&A / 10-K / 10-Q / moat > freshness; structural catalyst = bonus even if older |

Procedure:
- If ≥7 qualifying after first fetch → rank profile-adaptively → take top 7 → output exactly 7.
- If <7 qualifying → Python auto-expands fetch window (next page / next source + Layer 2 web_search) without asking the user, re-applies hard gates + profile-adaptive ranking, until 7 are assembled. Thresholds are never lowered; fabrication is never allowed.

### Leftover / Fail-Safe

- If 7 qualifying assembled → output exactly 7 cards, discard ALL remaining.
- If after exhausting all layers (100 items + pagination + alternate source + Layer 2 web_search) still <7 qualifying → fail-safe: output what exists (X cards) with explicit disclaimer: "Hanya X peluang memenuhi gate daripada semua sumber — tidak dapat capai 7 tanpa melanggar hard gate." Document the blocker; do NOT fabricate, do NOT lower thresholds. This is the only exception to the 7-card rule.
- ALL leftover items beyond the 7 (or beyond X in fail-safe) are DISCARDED. No re-reading.

---

# PHASE 1 — MARKET SCANNER (LOCKED FORMAT)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

Output must begin with (v4.6 — no scan counts):

```markdown
# MARKET SCANNER — [DATE] | Source: [SOURCE]

Akses: [DATE TIME]
```

Then output exactly 7 positive cards (profile-adaptively ranked), each in this exact structure:

```markdown
## CARD [#N] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Direction | **Positive** |
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

[... repeat for CARD [#2] through CARD [#7] — exactly 7 positive cards, profile-adaptively ranked ...]

---
```

After the last card (CARD [#7]), output exactly:

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
