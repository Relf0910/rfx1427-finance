# Intake Form (Gate 0)

Source: Framework v3.1

## Overview

Intake has **3 questions only**. Ask **one at a time** — do not ask all at once (Rule 1). If any field is incomplete, **WAIT** (Rule 2).

## Q1 — Output Language

Ask:

> "What language for output?"

Options:

- English
- Bahasa Melayu
- Other

Record as: `output_language`

## Q2 — Trader Profile

Ask:

> "What trader profile?"

Options:

- Scalper
- Intraday
- Swing
- Investor

Record as: `trader_profile`

## Q3 — Market Focus

Ask:

> "What market focus?"

Options:

- US
- Singapore
- Malaysia
- Other

Record as: `market`

## Intake Complete

After all three fields are complete:

```text
Language: X | Profile: X | Market: X
```

Then:

```text
PROCEED → PHASE 1
```

If any field is incomplete:

```text
WAIT
```

## Hard Gate

Do not proceed to Phase 1 if any question is unanswered. Repeat the unanswered question, one at a time.
