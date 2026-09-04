# Final Decision Tree

Sumber: framework v2.2, Seksyen 14.

```text
START
  │
  ▼
INTAKE
  │
  ├── incomplete ─────────→ WAIT
  │
  ▼
NEWS SOURCE
  │
  ├── blocked ────────────→ STOP
  │
  ▼
SCAN
  │
  ▼
FILTER
  │
  ├── no opportunities ──→ REPORT → STOP
  │
  ▼
MAX 7 OPPORTUNITIES
  │
  ▼
PHASE 1 REPORT
  │
  ▼
STOP
  │
  ├── SKIP ───────────────→ END
  │
  └── OPT-IN
          │
          ▼
    SELECT PRIMARY TOOL
          │
          ▼
      STAGE 1
    PRIMARY DATA
          │
          ▼
      STAGE 2
      SEC EDGAR
          │
          ▼
      STAGE 3
 COMPARE + ANALYZE
          │
          ├── rejected ───→ SKIP
          ├── low confidence → SKIP
          │
          ▼
    PHASE 2 REPORT
          │
          ▼
         STOP
          │
          ▼
    PHASE 3 (auto-proceeds, mandatory)
          │
          ▼
        END
```

## Ringkasan titik putus

- INTAKE incomplete → `WAIT`.
- Source blocked → `STOP`.
- Tiada opportunity → report → `STOP`.
- User pilih Skip → `END`.
- Mechanism rejected atau low confidence → `SKIP`.
- After Phase 2 → Phase 3 auto-proceeds → `END`.