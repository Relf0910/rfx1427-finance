---
name: rfx1427-finance
description: AI financial news scanner dan analysis framework versi 3.1 yang membaca SATU news source pilihan user, menapis public companies mengikut trader profile, market focus, time horizon, materiality dan confidence, dan menjalankan Deep Analysis dengan Primary Tool. SEC EDGAR Verification只有在用户明确要求时才进行。使用此框架仅当用户请求金融新闻扫描、机会筛选、明确引用此技能名称，或需要Intake / Fasa 1 / Fasa 2 / Fasa 3 / Fasa 4流程时。不要用于买卖建议、交易执行、持续监控、观察列表、价格警报、投资组合管理，或在没有 ticker 和新闻扫描范围的情况下进行的一般财务问题。输出是只读分析，不是交易顾问。
---

# RFX1427 Finance

Financial News Scanner + Deep Analysis + SEC Verification + Plain Summary framework with strict gate controls, fact-based approach, and official SEC EDGAR verification.

## Version 3.1 — Master Framework (4 Fasa)

## Core Principle

```text
SCAN (Fasa 1)
   ↓
ANALYZE (Fasa 2) — Primary Tool Only, NO SEC
   ↓
SEC VERIFY (Fasa 3) — Opt-in Only
   ↓
SUMMARISE (Fasa 4)
   ↓
END
```

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate news, ticker, price, volume, financial figures, filing, rating, level, or source access. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when needed
- **OPT-IN ONLY** — Fasa 2 on user selection. Fasa 3 SEC Verification only on explicit user opt-in. Fasa 4 only on user request
- **NO AUTOMATIC PHASE TRANSITION** — phase cannot jump without permission
- **NO LOOP, NO MONITOR, NO AUTO-PROCEED** — each session is fresh
- **ONE QUESTION AT A TIME** for Intake
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss, position sizing, or guaranteed target

## Language

- User interaction: Bahasa Melayu
- Code, identifiers, error states, table headers, status enum: English (verbatim from framework)
- Report output (Fasa 1/2/3/4): Language according to user `output_language` selection (English, Bahasa Melayu, Other)

## Global Flow (Session Architecture)

```text
INTAKE (Gate 0)
    │
    ▼
FASA 1 — SCANNER (Finviz Default)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
FASA 2 — DEEP ANALYSIS (Primary Tool Only, NO SEC)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
FASA 3 — SEC EDGAR VERIFICATION (Opt-in Only)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
FASA 4 — RINGKASAN BIAS (LOCKED — Agora Style)
    │
    ▼
END
```

---

# ====================================================================
# WEBFETCH ENFORCEMENT — WAJIB PATUH
# ====================================================================

1. AI **WAJIB fetch data SEBELUM analysis**
2. AI **tidak boleh skip fetch**
3. AI **tidak boleh gunakan training knowledge** untuk menggantikan current tool data
4. Primary Tool blocked → label: `PRIMARY TOOL — BLOCKED`
5. SEC blocked/unavailable → label: `UNVERIFIED — SEC DATA NOT AVAILABLE`
6. **Jangan claim verification tanpa fetch**
7. **Jangan invent missing data**
8. Jika Primary Tool gagal → `FETCH FAILED — ANALYSIS SKIPPED`

---

# ====================================================================
# MASTER HARD RULES (29)
# ====================================================================

1. One question at a time.
2. Complete Intake before Fasa 1.
3. No ticker = noise.
4. Materiality < 3 = reject.
5. Confidence < Medium in Fasa 1 = reject.
6. Poor Horizon Fit = reject.
7. Maximum 7 Fasa 1 opportunities.
8. Fasa 2 requires explicit opt-in.
9. User chooses Primary Tool (Google Finance default).
10. Fasa 2 uses Primary Tool ONLY. No SEC in Fasa 2.
11. Fasa 3 is SEPARATE phase for SEC EDGAR (opt-in only).
12. SEC EDGAR is NOT mandatory in Fasa 2.
13. Fetch before analysis.
14. No fabricated data.
15. No training data replacing required current fetch.
16. Missing data = Not Available.
17. Rejected mechanism = Skip.
18. Low final confidence = Skip.
19. Fasa 3 only if user explicitly opt-in for SEC verification.
20. Fasa 4 only when user asks.
21. No automatic phase transition.
22. No loop.
23. No watchlist.
24. No monitoring.
25. No buy/sell instruction.
26. No guaranteed prediction.
27. Every session starts fresh.
28. Format Fasa 1, 2, 3, 4 are LOCKED. Jangan ubah.
29. SEC Verification labels: VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE

---

## Gate 0 — Intake (3 Questions)

Ask ONE at a time.

**Q1:** "Apa bahasa untuk output?"
- [English] [Bahasa Melayu] [Other]
- → record: `output_language`

**Q2:** "Apa trader profile?"
- [Scalper] [Intraday] [Swing] [Investor]
- → record: `trader_profile`

**Q3:** "Apa market focus?"
- [US] [Singapore] [Malaysia] [Other]
- → record: `market`

[INTAKE COMPLETE]
"Language: X | Profile: X | Market: X"
→ PROCEED TO FASA 1

## Profile Definitions

| Profile | Time Horizon |
|---------|--------------|
| SCALPER | 5-15 minute catalyst |
| INTRADAY | Current trading session |
| SWING | Days to weeks |
| INVESTOR | Long-term business thesis |

## Fasa 1 — Scanner (Finviz Default)

### Step 1A — News Source

Ask: "Apa news source untuk hari ini?"
- [Finviz (Default)] [Reuters] [CNBC] [Bloomberg] [Other]
- → If user does not choose, USE FINVIZ AS DEFAULT

### Step 1B — Fetch / Read Source

Use selected source. Record:
- Source name
- URL (if available)
- Access time

If source fails to access:
`BLOCKED — SOURCE COULD NOT BE ACCESSED`
Do not claim source was read. Do not invent.

### Step 1C — Profile Filter

Use definitions:
- SCALPER → 5-15 min catalyst
- INTRADAY → current trading session
- SWING → days → weeks
- INVESTOR → long-term business thesis

Hard rule: NO TICKER = NOISE (discard immediately)

### Step 1D — Extract Facts

For each candidate:
- Company, Ticker
- What happened
- Key numbers
- Relevant dates
- Source

Distinguish: FACT vs AI INFERENCE vs ESTIMATE

### Step 1E — Map Opportunity

- Direction: Positive / Negative / Mixed / Neutral
- Materiality: 1-5 (1=Minimal, 5=Very High)
- Confidence: High / Medium / Low
- Horizon Fit: Strong / Partial / Poor
- Transmission Channel: NEWS → BUSINESS IMPACT → FINANCIAL/EXPECTATION → POTENTIAL PRICE IMPACT

### Step 1F — Noise Gate

Candidate must pass ALL:
- Materiality >= 3
- Confidence >= Medium
- Horizon Fit != Poor
- Ticker/company identifiable
- Market relevant

Max 7 opportunities. If more, rank by: Materiality > Confidence > Horizon Fit > Catalyst clarity

### Fasa 1 Output Format — LOCKED (Agora Style)

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

---

## Fasa 2 — Deep Analysis (Primary Tool Only, NO SEC)

### Overview

Fasa 2 uses **Primary Tool ONLY**. No SEC EDGAR in this phase.

### Step 2A — Primary Tool Selection

Ask: "Apa primary tool untuk deep analysis?"
- [Google Finance (Default)] [Finviz] [MarketBeat] [Skip]

→ If user does not choose, USE GOOGLE FINANCE AS DEFAULT.

### Step 2B — Fetch Primary Data

Fetch data from selected Primary Tool for every Fasa 1 opportunity:

#### GOOGLE FINANCE
- Current price, Price change %, Recent news, Analyst targets, Analyst ratings, Earnings data

#### FINVIZ
- Current price, Price change %, Volume, RSI, SMA 20, SMA 50, P/E, EPS, Revenue, News headlines

#### MARKETBEAT
- Current price, Price change %, Short interest, Analyst consensus, Financial ratios

### Step 2C — Analyze & Synthesize

For each opportunity:
1. Verify catalyst from Fasa 1
2. Assess timing fit with trader profile
3. Identify relevant price levels
4. Apply confidence gate

### Data Rules

If field not available:
```text
NOT AVAILABLE
```

If primary tool fails:
```text
PRIMARY TOOL — BLOCKED
```

### Fasa 2 Output — LOCKED

Output format: PHASE 2 — DEEP ANALYSIS

Components:
1. Primary Data Summary
2. Catalyst Verification
3. Deep Analysis Reports (per ticker)
4. Ranking Summary

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

### STOP 2

After Fasa 2 report:
```text
STOP
WAIT FOR USER
```

User options:
- Opt-in to Fasa 3 (SEC EDGAR Verification)
- Request Fasa 4 (Ringkesan Bias)
- Skip → END

---

## Fasa 3 — SEC EDGAR Verification (Opt-in Only)

### Overview

Fasa 3 is **OPT-IN ONLY**. Only runs if user explicitly asks for SEC EDGAR verification.

### When Fasa 3 is Triggered

User asks:
- "Jalankan SEC EDGAR Verification?"
- "Verify dengan SEC"
- "SEC verification"

### Step 3A — Fetch SEC EDGAR Data

For each ticker, access SEC EDGAR (sec.gov/edgar):

| Item | Filing |
| --- | --- |
| Revenue | 10-Q / 10-K |
| Net Income / EPS | 10-Q / 10-K |
| Total Debt | 10-Q / 10-K |
| Cash Flow | 10-Q / 10-K |
| Insider Transactions | Form 4 |
| Outstanding Shares | 10-Q / 10-K |
| Material Events | 8-K |

### Step 3B — Label Results

- If data exists and verified → `VERIFIED`
- If data not available → `UNVERIFIED — SEC DATA NOT AVAILABLE`

### Fasa 3 Output — LOCKED

Output format: PHASE 3 — SEC EDGAR VERIFICATION

Components:
1. Fetch Attempt
2. Verification Results (per ticker)

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

### STOP 3

```text
STOP
WAIT FOR USER
```

User options:
- Request Fasa 4 (Ringkesan Bias)
- Skip → END

---

## Fasa 4 — Ringkesan Bias (LOCKED — Agora Style)

### Overview

Fasa 4 provides weekly bias summary with locked format.

**Fasa 4 is: USER REQUEST ONLY**

Trigger: "Ringkasan" / "Summary" / "Phase 4" / "Fasa 4"

### FASA 4 — PERATURAN (WAJIB)

**FORMAT INI LOCKED. AI WAJIB IKUT TEPAT. JANGAN UBAH APA-APA.**

1. **Hanya 3 arah:** Positif / Negatif / Neutral (TIDAK ada MIXED)
2. **Anggaran dalam range** (contoh: +3% to +8%)
3. **Sebab ringkas maksimum 10 patah perkataan**
4. **Setiap saham WAJIB ada tag:**
   - `PREPARE FOR VOLUME BUY` (Positif)
   - `BE CAREFUL — MARKET CRASH RISK` (Negatif)
   - `WAIT FOR CONFIRMATION` (Neutral)
5. **WAJIB ada END OF SESSION table**
6. **WAJIB ada NO MONITORING disclaimer**
7. **JANGAN tambah apa-apa di luar format ini**

### Fasa 4 Output — LOCKED

Output format: PHASE 4 — RINGKASAN BIAS

Components:
1. Summary Table (Saham/Arah/Anggaran/Sebab)
2. Detailed explanation per ticker with tags
3. END OF SESSION table
4. NO MONITORING disclaimer

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

---

## Data Integrity Hierarchy

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

## Error States Summary (Standard)

| Condition | Output |
|---|---|
| Source fails to access | `BLOCKED — SOURCE COULD NOT BE ACCESSED` |
| Primary tool fails | `PRIMARY TOOL — BLOCKED` |
| Data missing | `NOT AVAILABLE` |
| SEC data verified | `VERIFIED` |
| SEC data missing | `UNVERIFIED — SEC DATA NOT AVAILABLE` |
| Mechanism fails | `REJECTED` |
| Confidence Low | `LOW CONFIDENCE — SKIP` |
| No opportunity | `No qualifying opportunities found for this trader profile and market focus.` |
| Primary Tool fails | `FETCH FAILED — ANALYSIS SKIPPED` |

## Opportunity Lifecycle

`NEWS → TICKER FILTER → PROFILE FILTER → FACT EXTRACTION → MATERIALITY → CONFIDENCE → HORIZON FIT → NOISE GATE → FASA 1 REPORT → USER OPT-IN → PRIMARY DATA FETCH → FASA 2 REPORT → USER OPT-IN → SEC EDGAR FETCH → FASA 3 REPORT → USER REQUEST → FASA 4 REPORT → END`

Any hard gate fails → `STOP / SKIP`

## References

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Fasa 1 Scanner | `references/phase1-scanner.md` |
| Fasa 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Fasa 3 SEC EDGAR Verification | `references/phase3-sec-edgar.md` |
| Fasa 4 Ringkesan Bias | `references/phase3-plain-summary.md` |
| Error States | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Status & Controls

- **VERSION 3.1** — Fasa 2 Primary Tool Only, Fasa 3 SEC Opt-in Only
- **Authority Gate** — Primary Tool selected by user (Google Finance / Finviz / MarketBeat / Skip). Primary Tool not selected by AI for user. SEC EDGAR is separate opt-in phase
- **Evidence Integrity Gate** — every important claim must be supported by real data (source URL, filing reference, or label `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`). No fabrication allowed
- **Completion Gate** — phase only complete after every step in reference is done

## Intent-to-Command Engine

Each user request (example: "scan news for today") is compiled into an operation command with elements: action + object, scope/universe, input & freshness, workflow sequence, decision point, criteria/filter/ranking, output format, failure handling, safety limits, and completion criteria. Compiler refers to phase references.

## Stagnation Breaker

If Fasa 1 produces 0 opportunities after two attempts with two different news sources (or one source + Other), stop with `No qualifying opportunities found for this trader profile and market focus.` Do not loop on the same source. Do not offer Fasa 2 after Skip.

## Autonomous Loop (7-Stage)

Each session operation goes through a closed loop:

```text
INSPECT → PLAN → BUILD → VALIDATE → DIAGNOSE → REPAIR → REVALIDATE
```

- INSPECT — verify current state (Intake complete? Which Phase?)
- PLAN — select next phase & step
- BUILD — execute step (access source, extract, verify)
- VALIDATE — check hard gate (Materiality, Confidence, Horizon Fit, Noise Gate)
- DIAGNOSE — identify cause if gate fails
- REPAIR — select corrective action (label NOT AVAILABLE, SKIP, etc)
- REVALIDATE — repeat validation after repair

Loop continues until Definition of Ready passes or blockers are documented.
