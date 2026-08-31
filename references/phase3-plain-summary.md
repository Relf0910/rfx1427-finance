# Fasa 4 — Ringkesan Bias

Source: Framework v3.0

## Overview

Fasa 4 provides a plain, non-technical summary of opportunities with weekly bias direction. This is the final phase before END.

**Fasa 4 is: USER REQUEST ONLY**

**Output Style: LOCKED — Agora Dashboard (Tables + Cards)**

## FASA 4 — PERATURAN (WAJIB)

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

## When Fasa 4 is Triggered

Trigger keywords:
- "Buat ringkasan"
- "Summary"
- "Phase 4"
- "Ringkasan"
- "Weekly bias"
- "Fasa 4"

Fasa 4 available after:
- Fasa 2 completed (if user requests)
- Fasa 3 completed or bypassed (if SEC failed, auto-proceed)

## Bias Categories & Tags

| Bias | Tag | Meaning |
|------|-----|---------|
| **POSITIVE** | PREPARE FOR VOLUME BUY | Catalysts identified that may support upside |
| **NEGATIVE** | BE CAREFUL — MARKET CRASH RISK | Catalysts identified that may pressure downside |
| **NEUTRAL** | WAIT FOR CONFIRMATION | No clear directional catalyst |

---

## FASA 4 — OUTPUT FORMAT (LOCKED)

WAJIB ikut format ini TEPAT. Jangan tambah apa-apa di luar format.

```markdown
# WEEKLY BIAS SUMMARY — [DATE]
Language: [English / Bahasa Melayu]

---

## CARD [#1] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Direction | **POSITIVE** / NEGATIVE / NEUTRAL |
| Est. Range | [+X% to +Y%] / [-X% to -Y%] / N/A |
| Reason | [Max 10 words factual reason] |
| Tag | **PREPARE FOR VOLUME BUY** / BE CAREFUL — MARKET CRASH RISK / WAIT FOR CONFIRMATION |

### Key Points
- [Point 1 — FACT / INFERENCE]
- [Point 2 — FACT / INFERENCE]

### Source
[Source name] | SEC: [Verified / Unverified / N/A]

---
```

**Repeat for each opportunity**

---

## END OF SESSION TABLE

```markdown
## END OF SESSION

| Ticker | Direction | Est. Range | Tag |
|--------|-----------|------------|-----|
| XXX | **POSITIVE** | +X% to +Y% | PREPARE FOR VOLUME BUY |
| XXX | NEGATIVE | -X% to -Y% | BE CAREFUL — MARKET CRASH RISK |
| XXX | NEUTRAL | N/A | WAIT FOR CONFIRMATION |

---

**NO MONITORING**

This session has ended. No watchlist, no alerts, no continuous monitoring.
Each session starts fresh.

---
```

---

After Fasa 4 output:
```text
END
```

No loop. No monitoring. No additional phases.
