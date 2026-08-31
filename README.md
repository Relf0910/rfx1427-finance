# RFX1427 Finance

AI financial news scanner dan analysis framework dengan kawalan gate yang ketat, berteraskan fakta, dan verifikasi rasmi SEC EDGAR.

## Gambaran Keseluruhan

RFX1427 Finance membaca SATU news source pilihan user, menapis public companies mengikut trader profile, market focus, time horizon, materiality dan confidence, dan menjalankan Deep Analysis dengan verification SEC EDGAR hanya selepas opt-in eksplisit.

## Prinsip Teras

- **Source Fact → Verification → AI Analysis → Estimate** — empat lapisan sentiasa dibezakan
- **NO FABRICATION** — jangan reka data. Guna `NOT AVAILABLE`, `UNVERIFIED`, atau `BLOCKED`
- **OPT-IN ONLY** — Phase 2 & 3 hanya selepas user memilih secara eksplisit
- **READ-ONLY ANALYSIS** — bukan trading advisor. Tiada buy/sell, entry, stop-loss

## Aliran Kerja

```
GATE 0 — INTAKE (3 soalan)
    │
    ▼
PHASE 1 — SCANNER (News → Ticker Filter → Profile Filter → Materiality → Confidence → Phase 1 Report)
    │
    ▼
STOP 1 — USER OPT-IN
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Primary Tool → SEC Verification → Comparison Matrix)
    │
    ▼
STOP 2 — USER REQUEST
    │
    ▼
PHASE 3 — PLAIN SUMMARY → END
```

## Data Integrity Hierarchy

```
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

## Rujukan

| Fasa | Fail |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 Plain Summary | `references/phase3-plain-summary.md` |
| Error States | `references/error-states.md` |
| Hard Rules Master (37) | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Folder Structure

```
rfx1427-finance/
├── SKILL.md                    # Main skill definition
├── agents/
│   └── openai.yaml             # Agent configuration
├── references/
│   ├── intake-form.md          # Phase 0: Intake form
│   ├── phase1-scanner.md       # Phase 1: Scanner
│   ├── phase2-deep-analysis.md # Phase 2: Deep Analysis
│   ├── phase3-plain-summary.md # Phase 3: Plain Summary
│   ├── error-states.md         # Error state definitions
│   ├── hard-rules-master.md    # 37 hard rules
│   ├── decision-tree.md        # Decision tree
│   ├── change-log-v2.md       # Version 2.2 changelog
│   ├── data-integrity-hierarchy.md
│   └── acceptance-tests.md
└── README.md
```

## Status

Versi: **2.2** (DRAFT)

Baca `SKILL.md` untuk dokumentasi lengkap.
