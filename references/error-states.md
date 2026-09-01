# Error States

Source: Framework v4.5

## SOURCE ERROR

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

Used when: News source fails to be accessed in Phase 1.

## PRIMARY TOOL ERROR

```text
PRIMARY TOOL — BLOCKED
```

Used when: Primary tool (Google Finance / MarketBeat / Finviz) fails in Phase 2.

## SEC EDGAR ERROR

```text
BLOCKED — SEC EDGAR COULD NOT BE ACCESSED
```

Used when: SEC EDGAR fails to be accessed in Phase 2 or Phase 3.

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

## SEC DATA VERIFIED

```text
VERIFIED
```

Used when: SEC filing confirms the data.

## PYTHON FETCH NEEDS FALLBACK

```text
FALLBACK_NEEDED
```

Used when: Python fetch fails (Layer 1) in Phase 2 or Phase 3. Python retries with an alternate method (Layer 2). Only if the alternate method also fails do we declare a Layer 3 label.

## FETCH FAILED (ALL PRIMARY TOOL FAILURES)

```text
FETCH FAILED — ANALYSIS SKIPPED
```

Used when: All primary-tool fetches fail in Phase 2 after fallback. Analysis is skipped for those tickers.

## MECHANISM FAILED

```text
REJECTED
```

Used when: Transmission mechanism is not confirmed in Phase 2 analysis.

## LOW CONFIDENCE

```text
LOW CONFIDENCE — SKIP
```

Used when: Final confidence gate evaluates to Low. Opportunity excluded from report.

## NO QUALIFYING OPPORTUNITIES

```text
No qualifying opportunities found for this trader profile and market focus.
```

Used when: No opportunity passes Noise Gate in Phase 1.

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
- `VERIFIED` → SEC filing confirms the data
- These labels are MANDATORY — do not replace with loose descriptions
