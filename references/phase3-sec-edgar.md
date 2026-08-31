# Phase 3 — SEC EDGAR Verification (Opt-in Only)

Source: Framework v3.1

## Overview

Phase 3 is **OPT-IN ONLY**. Only runs if user explicitly requests SEC EDGAR verification.

**IMPORTANT: Phase 3 is SEPARATE from Phase 2. Phase 2 does NOT include SEC.**

## PHASE 3 — RULES (MANDATORY)

1. **Only run if user opt-in**
2. **If still fails** → label `UNVERIFIED — SEC DATA NOT AVAILABLE`
3. Do NOT fabricate data
4. **No auto-proceed** — ask user at every step

## When Phase 3 is Triggered

User explicitly asks:
- "Run SEC EDGAR Verification?"
- "Verify with SEC"
- "SEC verification"
- "Phase 3"

At STOP 2, ask user:
> "Run SEC EDGAR Verification?"

Options:
- [Yes] → Proceed to Phase 3
- [Skip — Continue to Phase 4] → Proceed to Phase 4
- [Skip] → END

## STEP 3A — Fetch SEC EDGAR Data

For each ticker from Phase 1, access SEC EDGAR (sec.gov/edgar)

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

## STEP 3B — Label Verification Results

For each ticker:

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
(Opt-in sahaja | Akses: [DATE TIME])
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
3. Never auto-advance phases. Always stop and wait for explicit user opt-in
4. Keep the exact markdown structure, bold labels, and stop phrases shown above
5. Never include buy/sell recommendations, entry prices, stop-loss levels, position sizing, or guaranteed targets
