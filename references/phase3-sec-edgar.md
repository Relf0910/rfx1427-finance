# Fasa 3 — SEC EDGAR Verification

Source: Framework v3.0

## Overview

Fasa 3 provides explicit SEC EDGAR verification for opportunities where Fasa 2 failed or where user explicitly requests SEC EDGAR verification.

**Fasa 3 is: OPT-IN ONLY**

**Trigger Condition:** Fasa 2 fails OR user explicitly requests SEC verification

## When Fasa 3 is Triggered

1. Fasa 2 Primary Tool is BLOCKED
2. Fasa 2 produced LOW CONFIDENCE for all opportunities
3. User explicitly requests: "Verify dengan SEC EDGAR"

## STEP 3A — Identify Opportunities for Verification

From Phase 1 opportunities, select those that:
- Have identifiable tickers
- Are relevant to market focus
- Could benefit from SEC verification

Maximum: **7 opportunities**

## STEP 3B — Fetch SEC EDGAR Data

For each selected opportunity, access SEC EDGAR (sec.gov/edgar)

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

### SEC Access Rule

If SEC EDGAR fails to access:
```text
BLOCKED — SEC EDGAR COULD NOT BE ACCESSED
```

If filing found but data not available:
```text
UNVERIFIED — SPECIFIC DATA NOT AVAILABLE
```

Do NOT fabricate. Do NOT claim filing was read if it was not.

## STEP 3C — Verify Facts Against SEC

For each opportunity, compare news facts against SEC filings:

### Verification Status

| Status | Meaning |
| --- | --- |
| VERIFIED | SEC filing confirms the fact |
| CONFLICT | SEC filing contradicts the fact |
| UNVERIFIED | SEC filing does not address this fact |
| NOT APPLICABLE | Fact cannot be verified by SEC |

### Conflict Resolution

```text
SEC IS AUTHORITATIVE
```

If conflict exists between news source and SEC:
- Use SEC data
- Label as: `DATA MISMATCH — SEC OVERRIDE`

## STEP 3D — Generate Verification Report

For each opportunity:

1. List verified facts
2. List unverified facts
3. List conflicts (if any)
4. Provide overall confidence based on verification

### Confidence Assessment

| Verification Rate | Confidence |
| --- | --- |
| >75% verified | HIGH |
| 50-75% verified | MEDIUM |
| <50% verified | LOW |

---

## FASA 3 — OUTPUT FORMAT (LOCKED — AGORA STYLE)

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

### Agora Dashboard — SEC Verification Report

```markdown
# SEC EDGAR VERIFICATION — [DATE]

---

## CARD [#1] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| SEC Access | SUCCESS / BLOCKED |
| Last Filing Checked | [Filing type] on [Date] |

### Fact Verification

| Fact | SEC Status |
|------|------------|
| [Fact from news] | Verified / Conflict / Unverified / N/A |
| [Fact from news] | Verified / Conflict / Unverified / N/A |

### Conflicts (if any)
[Detail any DATA MISMATCH — SEC OVERRIDE]

### Overall Confidence
**HIGH** / MEDIUM / LOW

### SEC Data Used
- [Item]: [Value] ([Filing type], [Date])

---
```

## STEP 3E — Trigger Fasa 4 or End

After Fasa 3 report:

If user requests Fasa 4:
```text
PROCEED TO FASA 4 — RINGKASAN BIAS
```

If user does not request:
```text
END SESSION
```

## STOP 3

```text
STOP
WAIT FOR USER
```

User options at STOP 3:
- Proceed to Fasa 4 (Ringkesan Bias)
- Skip → END
