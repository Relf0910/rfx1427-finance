---
name: rfx1427-finance
description: AI financial news scanner dan analysis framework versi 3.0 yang membaca SATU news source pilihan user, menapis public companies mengikut trader profile, market focus, time horizon, materiality dan confidence, dan menjalankan Deep Analysis dengan verification SEC EDGAR hanya selepas opt-in eksplisit. Gunakan hanya apabila user meminta imbasan berita kewangan, penapisan opportunities, rujukan eksplisit kepada nama skill ini, atau aliran Intake / Fasa 1 / Fasa 2 / Fasa 3 / Fasa 4 framework ini. Jangan gunakan untuk nasihat beli atau jual, pelaksanaan dagangan, monitoring berterusan, watchlist, price alert, portfolio management, soalan finance umum tanpa ticker dan skop news scanning, atau analisis saham individu di luar konteks sumber berita. Output adalah read-only analysis, bukan trading advisor.
---

# RFX1427 Finance

Financial News Scanner + Deep Analysis + SEC Verification + Plain Summary framework with strict gate controls, fact-based approach, and official SEC EDGAR verification.

## Version 3.0 — Master Framework (4 Fasa)

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate news, ticker, price, volume, financial figures, filing, rating, level, or source access. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when needed
- **OPT-IN ONLY** — Fasa 2 and Fasa 3 only after explicit user selection. Fasa 4 only on user request
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
FASA 2 — DEEP ANALYSIS (Google Finance Default + SEC EDGAR)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
FASA 3 — SEC EDGAR VERIFICATION (Jika Fasa 2 Gagal)
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

## Global Gate Rules (Wajib)

1. One question at a time
2. Complete Intake before Fasa 1
3. NO TICKER = NOISE
4. Materiality >= 3
5. Confidence >= Medium
6. Horizon Fit != Poor
7. Max 7 opportunities
8. Fasa 2 and Fasa 3 opt-in only
9. Fasa 4 only if user requests
10. NO LOOP, NO MONITOR, NO AUTO-PROCEED
11. Never invent data. Never use training data to replace fetch

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

## Fasa 2 — Deep Analysis (Google Finance Default + SEC EDGAR)

### Step 2A — Primary Tool Selection

Ask: "Apa primary tool untuk deep analysis?"
- [Google Finance (Default)] [MarketBeat] [Skip]

### Step 2B — 3-Stage Verification

1. Fetch Primary Data
2. Fetch SEC EDGAR Data
3. Comparison Matrix

### Comparison Matrix (Stage 3)

| Situation | Status | Action |
|---|---|---|
| Primary = SEC | MATCH — CONFIRMED | Use data |
| Primary ≠ SEC, SEC authoritative | DATA MISMATCH — SEC OVERRIDE | Use SEC |
| SEC unavailable | UNVERIFIED | Use Primary + label |
| Primary unavailable, SEC available | SEC ONLY | Use SEC |
| Both unavailable | DATA NOT AVAILABLE | Do not use |

---

## Fasa 3 — SEC EDGAR Verification (Jika Fasa 2 Gagal)

Triggered ONLY if Fasa 2 fails or user requests explicit SEC verification.

---

## Fasa 4 — Ringkesan Bias (LOCKED — Agora Style)

Output format LOCKED to Agora Dashboard Style (Tables + Cards).

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
| SEC data missing | `UNVERIFIED — SEC DATA NOT AVAILABLE` |
| Data conflict (SEC authoritative) | `DATA MISMATCH — SEC OVERRIDE` |
| Mechanism fails | `REJECTED` |
| Confidence Low | `LOW CONFIDENCE — SKIP` |
| No opportunity | `No qualifying opportunities found for this trader profile and market focus.` |

## Opportunity Lifecycle

`NEWS → TICKER FILTER → PROFILE FILTER → FACT EXTRACTION → MATERIALITY → CONFIDENCE → HORIZON FIT → NOISE GATE → FASA 1 REPORT → USER OPT-IN → PRIMARY DATA → SEC DATA → COMPARISON → MECHANISM → TIMING → PRICE LEVELS → FINAL CONFIDENCE → FASA 2 REPORT`

Any hard gate fails → `STOP / SKIP`

## References

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Fasa 1 Scanner | `references/phase1-scanner.md` |
| Fasa 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Fasa 3 SEC EDGAR Verification | `references/phase3-sec-edgar.md` |
| Fasa 4 Ringkesan Bias | `references/phase4-ringkesan-bias.md` |
| Error States | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master (37) | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Status & Controls

- **VERSION 3.0** — Master Framework with 4 Fasa
- **Authority Gate** — SEC EDGAR is mandatory verification partner; Primary Tool selected by user (Google Finance / MarketBeat / Skip). Primary Tool not selected by AI for user
- **Evidence Integrity Gate** — every important claim must be supported by real data (source URL, filing reference, or label `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`). No fabrication allowed
- **Completion Gate** — phase only complete after every step in reference is done and status recorded (PRIMARY DATA FETCHED, SEC DATA FETCHED, MATCH / MISMATCH, etc)

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
- VALIDATE — check hard gate (Materiality, Confidence, Horizon Fit, Noise Gate, Comparison Matrix)
- DIAGNOSE — identify cause if gate fails
- REPAIR — select corrective action (label NOT AVAILABLE, SKIP, etc)
- REVALIDATE — repeat validation after repair

Loop continues until Definition of Ready passes or blockers are documented.
