# Intake Form (Gate 0)

Source: Framework v4.7.1 — Gate 0 locked to 2 questions (Language + Trader Profile); Market fixed to US

## Overview

Intake has **2 questions only**. Ask **one at a time** — do not ask all at once (Rule 1). If any field is incomplete, **WAIT** (Rule 2). Market is locked to **US** — no market selection step.

## Presentation Mode (Adaptive)

Render each question using the platform's native choice UI when available (arrow keys +
Enter), else fall back to the manual text options. Question content, options, and recorded
field names are identical in both modes. Ask ONE question at a time (Rule 1) in both modes.

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

## Market — Locked

Market is fixed to `US` (stocks US only). No question is asked. Record as: `market = "US"`.

## Intake Complete

After both fields are complete:

```text
Language: X | Profile: X | Market: US (locked)
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

Do not proceed to Phase 1 if any question is unanswered or if market is not `US`. Repeat the unanswered question, one at a time.
