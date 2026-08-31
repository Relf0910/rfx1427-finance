# Phase 2 — Deep Analysis

Sumber: framework v2.2, Seksyen 8.

Phase 2 ialah: `OPT-IN ONLY`.

## STEP 2A — Tool Selection

Tanya:

> Continue to Phase 2 — Deep Analysis?

Pilihan:

1. Finviz
2. Google Finance
3. MarketBeat
4. Skip Deep Analysis

### Action

Jika pilih 1–3:

```text
primary_tool = selected tool
```

Proceed ke Step 2B.

Jika pilih 4:

```text
END SESSION
```

### Hard Rule

- Jangan pilih tool bagi pihak user.
- Jangan jalankan Phase 2 tanpa opt-in.
- Jangan offer Phase 2 semula selepas Skip.
- SEC EDGAR tidak perlu dipilih secara berasingan — ia mandatory verification partner.

## STEP 2B — 3-Stage Verification

```text
STAGE 1
   ↓
STAGE 2
   ↓
STAGE 3
```

Stage seterusnya hanya bermula selepas stage sebelumnya selesai.

### STAGE 1 — Fetch Primary Tool Data

Fetch data untuk: `EVERY PHASE 1 OPPORTUNITY`.

#### FINVIZ

Fetch jika tersedia:

- Current price
- Price change %
- Volume
- RSI
- SMA 20
- SMA 50
- P/E
- EPS
- Revenue
- Relevant news headlines

#### GOOGLE FINANCE

Fetch jika tersedia:

- Current price
- Price change %
- Recent news
- Analyst targets
- Analyst ratings
- Earnings data

#### MARKETBEAT

Fetch jika tersedia:

- Current price
- Price change %
- Short interest
- Analyst consensus
- Financial ratios

#### Primary Data Rule

Jika field tidak tersedia:

```text
PRIMARY DATA — NOT AVAILABLE
```

Jangan invent.

Jika primary tool gagal:

```text
PRIMARY TOOL — BLOCKED
```

Jangan claim data telah fetched.

Internal state: `PRIMARY DATA FETCHED — [TOOL]` (tidak perlu output kepada user).

### STAGE 2 — Fetch SEC EDGAR Data

Hanya selepas Stage 1 selesai. Gunakan ticker daripada Phase 1 / Stage 1.

#### SEC Verification Matrix

| Item | Filing |
| --- | --- |
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

#### SEC Data States

**VERIFIED** — jika SEC filing menyediakan data:

```text
SEC_DATA
```

Rekod: filing type, filing date, relevant period, value, filing reference.

**UNVERIFIED** — jika SEC data tidak tersedia:

```text
UNVERIFIED — SEC DATA NOT AVAILABLE
```

#### Hard Rule

```text
NO SEC DATA ≠ FALSE
```

Ia bermaksud `UNVERIFIED`. Jangan paksa verification.

Internal state: `SEC DATA FETCHED — [VERIFIED / UNVERIFIED]` (tidak perlu output kepada user).

### STAGE 3 — Compare, Analyze & Synthesize

Hanya selepas Stage 1 dan Stage 2 selesai. AI kini boleh:

1. Compare
2. Verify
3. Confirm mechanism
4. Assess timing
5. Identify levels
6. Apply confidence gate

#### Data Authority Rule

SEC EDGAR ialah authority untuk financial filing data. Primary tool untuk market/technical/analyst data yang SEC tidak direka untuk menyediakan.

Contoh primary tool data: Current price, intraday change, volume, RSI, VWAP, technical indicators, analyst targets, analyst consensus.

#### Comparison Rules

| Situation | Status | Action |
| --- | --- | --- |
| Primary = SEC | MATCH — CONFIRMED | Use data |
| Primary ≠ SEC, SEC authoritative | DATA MISMATCH — SEC OVERRIDE | Use SEC |
| SEC unavailable | UNVERIFIED | Use Primary + label |
| Primary unavailable, SEC available | SEC ONLY | Use SEC |
| Both unavailable | DATA NOT AVAILABLE | Do not use |

### STEP 3.1 — Confirm Mechanism

Semak transmission channel daripada Phase 1.

Output:

- Confirmed
- Partially Confirmed
- Rejected

Jika `Rejected`, opportunity tidak boleh dipersembahkan sebagai valid opportunity.

### STEP 3.2 — Assess Timing

Match dengan trader profile:

- **SCALPER** → `5–15 minutes`
- **INTRADAY** → `Current session`
- **SWING** → `Days → weeks`
- **INVESTOR** → `Long-term`

Output: Strong / Partial / Poor.

### STEP 3.3 — Identify Price Levels

#### SCALPER

- Pre-market high
- Pre-market low
- R1
- R2

#### INTRADAY

- VWAP
- Opening Range High
- Opening Range Low

#### SWING

- 20-day SMA
- 50-day SMA
- Recent swing high
- Recent swing low

#### INVESTOR

- 52-week range
- Current P/E
- Historical valuation
- 5-year average P/E if available

#### Price Level Integrity Rule

Jika data tidak tersedia:

```text
NOT AVAILABLE
```

Jangan invent angka. Jangan claim exact level jika source tidak menyokongnya.

### STEP 3.4 — Confidence Gate

Selepas semua verification:

```text
High
Medium
Low
```

#### Low Confidence

Jika `Confidence = Low`:

```text
LOW CONFIDENCE — SKIP
```

Jangan masukkan ke final Deep Analysis report.

#### If All Opportunities Are Low

Output:

> No opportunities passed the final confidence gate.

Jangan force-fill report.

## Phase 2 Final Output

```markdown
# DEEP ANALYSIS — [DATE]

## [COMPANY] ([TICKER])

**Primary Tool:**
Finviz / Google Finance / MarketBeat

**SEC Verification:**
Verified / Unverified / Mismatch / SEC Only

**Data Comparison:**

* [Item 1]: Primary [X] | SEC [Y] → Match / Mismatch / Unverified
* [Item 2]: Primary [X] | SEC [Y] → Match / Mismatch / Unverified

**Catalyst:**
[...]

**Mechanism:**
Confirmed / Partially Confirmed / Rejected

**Timing Fit:**
Strong / Partial / Poor

**Relevant Levels:**
[...]

**Confidence:**
High / Medium

**Risk / Uncertainty:**
[...]

---
```

## STOP 2

Selepas Phase 2:

```text
STOP
WAIT FOR USER
```

Jangan jalankan Phase 3 secara automatik.