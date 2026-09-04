# Phase 3 — SEC EDGAR Verification (Python + AI Unified, Mandatory)

Source: Framework v4.5

## Overview

Phase 3 is **MANDATORY**. Auto-proceeds after Phase 2 completes. Python works directly with the AI: Python fetches and parses SEC EDGAR filings; the AI verifies against Phase 2 claims and labels VERIFIED / UNVERIFIED. No collect-then-read two-pass.

**IMPORTANT: Phase 3 is SEPARATE from Phase 2. Phase 2 does NOT include SEC.**

## PHASE 3 — RULES (MANDATORY)

1. **Mandatory after Phase 2** — auto-proceeds, no user prompt needed
2. **If still fails** → label `UNVERIFIED — SEC DATA NOT AVAILABLE`
3. Do NOT fabricate data
4. **No auto-proceed** — ask user at every step
5. **Python fetches + parses; AI verifies + labels** — Python does NOT judge

## Python + AI Division of Work (Phase 3)

| Layer | What it does |
|-------|--------------|
| **Python** | Access SEC EDGAR, fetch + parse official filings per ticker, prepare key items. Python does NOT verify or label. |
| **AI** | Reads each filing, compares against Phase 2 claims, assigns VERIFIED / UNVERIFIED label, links back to the catalyst. |

## When Phase 3 is Triggered

User explicitly asks:
- "Run SEC EDGAR Verification?"
- "Verify with SEC"
- "SEC verification"
- "Phase 3"

After Phase 2 report, Phase 3 auto-proceeds:
> "Running SEC EDGAR Verification..."

Python accesses SEC EDGAR for all Phase 1 tickers automatically.

## STEP 3A — Python-Assisted SEC Fetch

For each ticker from Phase 1, Python accesses SEC EDGAR (sec.gov/edgar), fetches and parses official filings. Python prepares; AI judges.

```text
STEP S1 — SEC ACCESS (Python fetches)
  - Access SEC EDGAR via its official API/library.
  - Fetch filings: 10-K, 10-Q, 8-K, 6-K, Form 4.
STEP S2 — PARSE KEY ITEMS (Python prepares)
  - Extract: Revenue, Net Income / EPS, Total Debt, Cash Flow,
    Insider Transactions (Form 4), Outstanding Shares, Material Events (8-K).
STEP S3 — VERIFY (AI judges)
  - AI compares the filing against Phase 2 claims.
  - AI assigns VERIFIED or UNVERIFIED.
```

### Filing Types to Check

| Item | Primary Filing | Notes |
| --- | --- | --- |
| Revenue | 10-K (annual), 10-Q (quarterly) | Most recent filing |
| Net Income / EPS | 10-K, 10-Q | Most recent filing |
| Total Debt | 10-K, 10-Q | Balance sheet |
| Cash Flow | 10-K, 10-Q | Cash flow statement |
| Insider Transactions | Form 4 | Recent transactions |
| Outstanding Shares | 10-K, 10-Q | Balance sheet |
| Material Events | 8-K | Recent events |

### SEC Access Rules

If SEC EDGAR fails to access:
```text
BLOCKED — SEC EDGAR COULD NOT BE ACCESSED
```

If filing found but data not available:
```text
UNVERIFIED — SPECIFIC DATA NOT AVAILABLE
```

Do NOT fabricate. Do NOT claim filing was read if it was not.

### Python Failure — Layered Fallback (Phase 3)

If Python SEC access fails, use the layered fallback. Python ALWAYS tries the primary SEC access first; the label is ONLY declared when both methods fail. Fallback is NOT web_search — SEC verification must come from official SEC sources.

```text
LAYER 1 — PYTHON SEC FETCH (Primary)   -> if success, parse (STEP S2)
LAYER 2 — ALTERNATE SEC METHOD (Fallback) -> if Python fails, try an alternate
                                             SEC access (sec-api / EDGAR full-text
                                             search API / another SEC library).
                                             If success, parse (STEP S2).
LAYER 3 — LABEL (Final)                -> if both fail, AI applies:
                                             BLOCKED — SEC EDGAR COULD NOT BE ACCESSED
                                             then -> UNVERIFIED — SEC DATA NOT AVAILABLE
```

Rules:
- Python ALWAYS tries the primary SEC access first (Layer 1).
- Layer 2 (alternate SEC method) is ONLY used when Python fails.
- The label is ONLY declared when both layers fail (Layer 3).
- Python does NOT verify or label; the AI applies the label.

## STEP 3B — Label Verification Results (AI judges)

Python delivers the parsed filings; the AI compares against Phase 2 and assigns the label. For each ticker:

| Status | Meaning |
| --- | --- |
| **VERIFIED** | SEC filing confirms the data |
| **UNVERIFIED — SEC DATA NOT AVAILABLE** | SEC data cannot be retrieved |

---

# PHASE 3 — SEC EDGAR VERIFICATION (LOCKED FORMAT)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

Output must begin with:

```markdown
**PHASE 3 — SEC EDGAR VERIFICATION**
(Mandatory | Akses: [DATE TIME])
```

### 1. Fetch Attempt

```markdown
| Ticker | Filing Diakses | Status |
|--------|----------------|--------|
| Stock X | 10-Q / 10-K / 8-K / 6-K | SUCCESS / UNVERIFIED |
| Stock Y | 10-Q / 10-K / 8-K / 6-K | SUCCESS / UNVERIFIED |
```

### 2. Verification Results (per ticker)

For each ticker:

```markdown
## [TICKER] — [COMPANY]
**Label: VERIFIED**   or   **UNVERIFIED — SEC DATA NOT AVAILABLE**

- [Key financial item]
- [Key financial item]
- [Shares / Cash / Debt / Material event if available]
- **Catatan:** [One-line link back to the Phase 1 catalyst]
```

After all tickers, add a one-line summary of how many were VERIFIED vs UNVERIFIED.

End Phase 3 with exactly:

```text
STOP
WAIT FOR USER
```

## Hard Rules for Phase 3

1. Never skip a required table or section
2. Never invent data. Use NOT AVAILABLE, BLOCKED, or UNVERIFIED when data is missing
3. Phase 3 auto-proceeds after Phase 2. Always stop and wait for explicit user opt-in for Phase 4
4. Keep the exact markdown structure, bold labels, and stop phrases shown above
5. Never include buy/sell recommendations, entry prices, stop-loss levels, position sizing, or guaranteed targets
