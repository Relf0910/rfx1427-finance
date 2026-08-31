# Error States

Source: Framework v3.0

## SOURCE ERROR

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

Used when: News source fails to be accessed in Fasa 1.

## PRIMARY TOOL ERROR

```text
PRIMARY TOOL — BLOCKED
```

Used when: Primary tool (Google Finance / MarketBeat / Finviz) fails in Fasa 2.

## SEC EDGAR ERROR

```text
BLOCKED — SEC EDGAR COULD NOT BE ACCESSED
```

Used when: SEC EDGAR fails to be accessed in Fasa 2 or Fasa 3.

## DATA MISSING

```text
NOT AVAILABLE
```

Used when: Specific data field is not available from source.

## SEC DATA MISSING

```text
UNVERIFIED — SEC DATA NOT AVAILABLE
```

Used when: SEC filing data cannot be retrieved or verified.

## SEC DATA CONFLICT

```text
DATA MISMATCH — SEC OVERRIDE
```

Used when: SEC is authoritative source and conflicts with primary tool or news source.

Rule: SEC IS AUTHORITATIVE for financial filing data.

## MECHANISM FAILED

```text
REJECTED
```

Used when: Transmission mechanism is not confirmed in Fasa 2 Stage 3.

## LOW CONFIDENCE

```text
LOW CONFIDENCE — SKIP
```

Used when: Final confidence gate evaluates to Low. Opportunity excluded from report.

## NO QUALIFYING OPPORTUNITIES

```text
No qualifying opportunities found for this trader profile and market focus.
```

Used when: No opportunity passes Noise Gate in Fasa 1.

Do NOT force-fill report.

## NO TICKER

```text
NO TICKER = NOISE
```

Used when: News item has no identifiable ticker or public company. Discard immediately.

## General Principles

- `NOT AVAILABLE` → data does not exist or cannot be reached
- `UNVERIFIED` → data may exist but cannot be confirmed through SEC
- `BLOCKED` → access to source or tool failed
- These labels are MANDATORY — do not replace with loose descriptions
