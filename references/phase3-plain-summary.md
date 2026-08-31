# Phase 4 — Weekly Bias Summary

Source: Framework v3.1

## Overview

Phase 4 provides a plain, non-technical summary of opportunities with weekly bias direction. This is the final phase before END.

**Phase 4 is: USER REQUEST ONLY**

**Output Style: LOCKED FORMAT**

## PHASE 4 — RULES (MANDATORY)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

1. **Only 3 directions:** Positive / Negative / Neutral (NO MIXED)
2. **Estimate in range** (example: +3% to +8%)
3. **Reason maximum 10 words**
4. **Every stock MUST have tag:**
   - `PREPARE FOR VOLUME BUY` (Positive)
   - `BE CAREFUL — MARKET CRASH RISK` (Negative)
   - `WAIT FOR CONFIRMATION` (Neutral)
5. **MUST have END OF SESSION table**
6. **MUST have NO MONITORING disclaimer**
7. **Do NOT add anything outside this format**

## When Phase 4 is Triggered

Trigger keywords:
- "Ringkasan"
- "Summary"
- "Phase 4"
- "Weekly bias"
- "Fasa 4"

Phase 4 available after:
- Phase 2 completed (if user requests)
- Phase 3 completed or bypassed

## Bias Categories & Tags

| Bias | Tag | Meaning |
|------|-----|---------|
| **POSITIVE** | PREPARE FOR VOLUME BUY | Catalysts identified that may support upside |
| **NEGATIVE** | BE CAREFUL — MARKET CRASH RISK | Catalysts identified that may pressure downside |
| **NEUTRAL** | WAIT FOR CONFIRMATION | No clear directional catalyst |

---

## PHASE 4 — OUTPUT FORMAT (LOCKED)

STRICTLY FOLLOW THIS FORMAT. Do not add anything outside this format.

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

After Phase 4 output:
```text
END
```

No loop. No monitoring. No additional phases.
