# Phase 1 — The Scanner

Sumber: framework v2.2, Seksyen 7.

7 steps: `1A → 1B → 1C → 1D → 1E → 1F → 1G`.

## STEP 1A — Ask News Source

Tanya:

> Apa news source untuk hari ini?

Pilihan:

- Reuters
- CNBC
- Bloomberg
- FT
- Other

Rekod sebagai: `news_source`

## STEP 1B — Read News Source

Gunakan `news_source` yang dipilih user.

Required:

1. Access source.
2. Record URL jika tersedia.
3. Record access time.
4. Read accessible relevant content.
5. Apply market focus.
6. Continue ke Step 1C.

### Source Access Rule

Jika source gagal diakses:

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

Jangan claim source telah dibaca. Jangan hasilkan fabricated scanner report.

## STEP 1C — Filter By Trader Profile

### SCALPER — horizon 5–15 minutes

Cari:

- Pre-market gap
- Earnings reaction
- Fed statement
- Major breaking news
- Immediate corporate catalyst

### INTRADAY — current trading session

Cari:

- Economic data
- CEO interview
- Analyst upgrade/downgrade
- Earnings
- Sector-moving news
- Regulatory announcement

### SWING — several days → weeks

Cari:

- Earnings preview
- Sector rotation
- Guidance change
- Short-interest changes
- Product catalyst
- Industry developments

### INVESTOR — long-term business thesis

Cari:

- 10-K
- 10-Q
- New CEO
- M&A
- Regulatory shift
- Capital allocation
- Competitive moat
- Structural industry change

### Hard Filter — NO TICKER

Jika tiada ticker atau identifiable public company:

```text
NO TICKER = NOISE
```

Discard.

## STEP 1D — Extract Facts

Untuk setiap candidate, rekod:

- Company
- Ticker
- What happened
- Key numbers
- Relevant dates
- Market context
- Source

### Fact Rule

Bezakan tiga kategori:

- **FACT** — disokong oleh source.
- **INFERENCE** — interpretasi AI berdasarkan facts.
- **ESTIMATE** — anggaran berdasarkan available data.

Jangan campur ketiga-tiga kategori.

## STEP 1E — Map Opportunity

Setiap candidate dinilai:

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
FINANCIAL IMPACT
 ↓
EXPECTATION / SENTIMENT
 ↓
POTENTIAL PRICE IMPACT
```

### Materiality

Skor 1–5:

| Score | Meaning |
| ----: | --- |
| 1 | Minimal |
| 2 | Low |
| 3 | Moderate |
| 4 | High |
| 5 | Very High |

### Confidence

- **HIGH** — Strong source support, catalyst jelas, mechanism jelas, low material uncertainty.
- **MEDIUM** — Core facts supported, mechanism reasonably supported, some uncertainty exists.
- **LOW** — Missing data, conflicting evidence, weak mechanism, high uncertainty.

### Horizon Fit

- Strong
- Partial
- Poor

## STEP 1F — Noise Gate

Candidate mesti memenuhi SEMUA:

```text
Materiality >= 3
Confidence >= Medium
Horizon Fit != Poor
Identifiable ticker/company
Market focus relevant
```

Maximum: **7 opportunities**.

### Ranking

Jika lebih daripada 7:

1. Materiality
2. Confidence
3. Horizon Fit
4. Catalyst clarity

Ambil maksimum 7.

## STEP 1G — Phase 1 Report

Format:

```markdown
# MARKET SCANNER — [DATE]

## 1. [COMPANY] ([TICKER])

**Direction:** Positive / Negative / Mixed / Neutral

**Materiality:** X/5

**Confidence:** High / Medium / Low

**Horizon Fit:** Strong / Partial / Poor

**What happened:**
[Factual summary]

**Why it matters:**
[Transmission mechanism]

**Key data:**
[Numbers / dates]

**Source:**
[Source]

---
```

Ulang sehingga maksimum 7 opportunities.

## Phase 1 Restrictions

Jangan beri:

- Buy command
- Sell command
- Entry instruction
- Stop-loss instruction
- Position sizing
- Guaranteed target
- Guaranteed return

Phase 1 ialah: `NEWS → FILTER → OPPORTUNITY`.

## STOP 1

Selepas Phase 1 report:

```text
STOP
WAIT FOR USER
```

Jangan jalankan Phase 2 secara automatik.