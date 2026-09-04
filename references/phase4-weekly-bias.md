# Phase 4 — Weekly Bias Summary

Source: Framework v3.1

## Overview

Phase 4 provides weekly bias summary with locked format.

**Phase 4 is: USER REQUEST ONLY**

Trigger: "Summary" / "Phase 4" / "Weekly bias"

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

---

# PHASE 4 — WEEKLY BIAS SUMMARY (LOCKED FORMAT)

**THIS FORMAT IS LOCKED. STRICTLY FOLLOW. DO NOT MODIFY.**

This phase is user-request only. Output must follow this structure with zero additions:

```markdown
**PHASE 4 — WEEKLY BIAS SUMMARY**

| Saham | Arah | Anggaran % | Reason (max 10 words) |
|-------|------|------------|-----------------------|
| Stock X | Positive | +3% to +8% | [max 10 words] |
| Stock Y | Negative | -5% to -12% | [max 10 words] |
```

Allowed directions only: Positive / Negative / Neutral.
Anggaran % must be a range.
Reason must not exceed 10 words.

Then:

```markdown
### Penjelasan Ringkas + Tag

**Stock X**
Arah Positive. [One short sentence].
`PREPARE FOR VOLUME BUY`

**Stock Y**
Arah Negative. [One short sentence].
`BE CAREFUL — MARKET CRASH RISK`
```

(Use `WAIT FOR CONFIRMATION` for Neutral.)

Then the mandatory closing table:

```markdown
### END OF SESSION

| Ticker | Final Bias | Tag |
|--------|------------|-----|
| Stock X | Positive | PREPARE FOR VOLUME BUY |
| Stock Y | Negative | BE CAREFUL — MARKET CRASH RISK |
```

Finally, output exactly this disclaimer block and nothing after it:

```markdown
**NO MONITORING**
Ini adalah ringkasan bias berdasarkan analisis Fasa 1–3 sahaja.
Bukan nasihat pelaburan.
Tiada pemantauan berterusan.
Sesi tamat.
```

## Hard Rules for Phase 4

1. Never skip a required table or section
2. Never invent data. Use NOT AVAILABLE, BLOCKED, or UNVERIFIED when data is missing
3. Phase 3 is mandatory (auto-proceeds after Phase 2); Phase 4 only on user request
4. Keep the exact markdown structure, bold labels, and stop phrases shown above
5. Never include buy/sell recommendations, entry prices, stop-loss levels, position sizing, or guaranteed targets
