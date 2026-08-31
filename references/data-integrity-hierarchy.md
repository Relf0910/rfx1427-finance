# Data Integrity Hierarchy & SEC Verification

Sumber: framework v2.2, Seksyen 11.

## Hierarchy

```text
OFFICIAL SEC FILING
       ↓
PRIMARY FINANCIAL TOOL
       ↓
NEWS SOURCE
       ↓
AI INFERENCE
       ↓
ESTIMATE
```

## Nota penting

Hierarchy ini bukan bermaksud SEC sentiasa mempunyai semua data. Ia bermaksud:

> Untuk sesuatu item yang memang boleh diverifikasi melalui SEC filing, SEC menjadi authority.

Untuk market data yang SEC tidak menyediakan, gunakan primary financial tool.

## Apa yang SEC Authority Untuk

- Financial filing data
- Revenue
- Net income
- EPS
- Debt
- Cash flow
- Shares
- Insider transactions
- Material events

## Apa Yang Primary Tool Untuk

- Current price
- Intraday change
- Volume
- RSI
- VWAP
- Technical indicators
- Analyst targets
- Analyst consensus

## SEC Verification Matrix

| Item | Filing |
| --- | --- |
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

## Comparison Rules

| Situation | Status | Action |
| --- | --- | --- |
| Primary = SEC | MATCH — CONFIRMED | Use data |
| Primary ≠ SEC, SEC authoritative | DATA MISMATCH — SEC OVERRIDE | Use SEC |
| SEC unavailable | UNVERIFIED | Use Primary + label |
| Primary unavailable, SEC available | SEC ONLY | Use SEC |
| Both unavailable | DATA NOT AVAILABLE | Do not use |