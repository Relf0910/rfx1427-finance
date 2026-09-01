---
name: rfx1427-finance
description: AI financial news scanner and analysis framework version 4.1 that reads any user-provided news source, filters public companies by trader profile, market focus, time horizon, materiality and confidence, and performs Deep Analysis with Primary Tool. SEC EDGAR Verification only on explicit user opt-in. Use only when user requests financial news scanning, opportunity filtering, explicit reference to this skill name, or the Intake / Phase 1 / Phase 2 / Phase 3 / Phase 4 workflow. Do not use for buy/sell advice, trade execution, continuous monitoring, watchlists, price alerts, portfolio management, or general finance questions without ticker and news scanning scope. Output is read-only analysis, not a trading advisor.
---

# RFX1427 Finance

Financial News Scanner + Deep Analysis + SEC Verification + Weekly Bias Summary framework with strict gate controls, fact-based approach, and official SEC EDGAR verification.

## Version 4.1 — Master Framework (4 Phase + Locked Output Templates + Improved Phase 1)

## Core Principle

```text
SCAN (Phase 1)
   ↓
ANALYZE (Phase 2) — Primary Tool Only, NO SEC
   ↓
SEC VERIFY (Phase 3) — Opt-in Only
   ↓
SUMMARISE (Phase 4)
   ↓
END
```

## Core Principles

- **Source Fact → Verification → AI Analysis → Estimate** — four layers always distinguished
- **NO FABRICATION** — never fabricate news, ticker, price, volume, financial figures, filing, rating, level, or source access. Use `NOT AVAILABLE`, `UNVERIFIED`, or `BLOCKED` when needed
- **OPT-IN ONLY** — Phase 2 on user selection. Phase 3 SEC Verification only on explicit user opt-in. Phase 4 only on user request
- **NO AUTOMATIC PHASE TRANSITION** — phase cannot jump without permission
- **NO LOOP, NO MONITOR, NO AUTO-PROCEED** — each session is fresh
- **ONE QUESTION AT A TIME** for Intake
- **READ-ONLY ANALYSIS** — not a trading advisor. No buy/sell, entry, stop-loss, position sizing, or guaranteed target

## Language

- User interaction: Bahasa Melayu
- Code, identifiers, error states, table headers, status enum: English (verbatim from framework)
- Report output (Phase 1/2/3/4): Language according to user `output_language` selection (English, Bahasa Melayu, Other)

## Global Flow (Session Architecture)

```text
INTAKE (Gate 0)
    │
    ▼
PHASE 1 — SCANNER (Finviz Default)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 2 — DEEP ANALYSIS (Primary Tool Only, NO SEC)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 3 — SEC EDGAR VERIFICATION (Opt-in Only)
    │
    ▼
STOP — WAIT FOR USER
    │
    ▼
PHASE 4 — WEEKLY BIAS SUMMARY (LOCKED FORMAT)
    │
    ▼
END
```

---

# ====================================================================
# WEBFETCH ENFORCEMENT — MANDATORY
# ====================================================================

1. AI **MUST fetch data BEFORE analysis**
2. AI **cannot skip fetch**
3. AI **cannot use training knowledge** to replace current tool data
4. Primary Tool blocked → label: `PRIMARY TOOL — BLOCKED`
5. SEC blocked/unavailable → label: `UNVERIFIED — SEC DATA NOT AVAILABLE`
6. **Do not claim verification without fetch**
7. **Do not invent missing data**
8. If Primary Tool fails → `FETCH FAILED — ANALYSIS SKIPPED`

---

# ====================================================================
# MASTER HARD RULES (29)
# ====================================================================

1. One question at a time.
2. Complete Intake before Phase 1.
3. No ticker = noise.
4. Materiality < 3 = reject.
5. Confidence < Medium in Phase 1 = reject.
6. Poor Horizon Fit = reject.
7. Maximum 7 Phase 1 opportunities.
8. Phase 2 requires explicit opt-in.
9. User chooses Primary Tool (Google Finance default).
10. Phase 2 uses Primary Tool ONLY. No SEC in Phase 2.
11. Phase 3 is SEPARATE phase for SEC EDGAR (opt-in only).
12. SEC EDGAR is NOT mandatory in Phase 2.
13. Fetch before analysis.
14. No fabricated data.
15. No training data replacing required current fetch.
16. Missing data = Not Available.
17. Rejected mechanism = Skip.
18. Low final confidence = Skip.
19. Phase 3 only if user explicitly opt-in for SEC verification.
20. Phase 4 only when user asks.
21. No automatic phase transition.
22. No loop.
23. No watchlist.
24. No monitoring.
25. No buy/sell instruction.
26. No guaranteed prediction.
27. Every session starts fresh.
28. Format Phase 1, 2, 3, 4 are LOCKED. Do not modify.
29. SEC Verification labels: VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE

---

# ====================================================================
# OUTPUT FORMAT INSTRUCTIONS — MANDATORY FOR AI
# ====================================================================

> **CRITICAL INSTRUCTION FOR THE AI:**
>
> Each phase below contains a **LOCKED OUTPUT TEMPLATE**.
> You MUST reproduce the exact structure shown — same headers, same table columns,
> same bold labels, same separator lines, same STOP phrases.
>
> Replace ALL placeholders (shown in `[BRACKETS]`) with real data fetched live.
>
> **NEVER use real ticker symbols in the template examples.**
> The templates below use `Stock X`, `Stock Y`, `[TICKER]`, `[COMPANY]` as placeholders.
> When producing real output, replace them with the actual fetched ticker and company name.
>
> **Do not add any section, paragraph, commentary, or formatting not shown in the template.**
> **Do not remove any section, table, or label shown in the template.**
>
> If you do not have data for a field, write `NOT AVAILABLE`.
> Do not leave any field blank. Do not invent data.
>
> These templates are the ONLY acceptable output structure for each phase.

---

## Gate 0 — Intake (3 Questions)

Ask ONE at a time.

**Q1:** "What language for output?"
- [English] [Bahasa Melayu] [Other]
- → record: `output_language`

**Q2:** "What trader profile?"
- [Scalper] [Intraday] [Swing] [Investor]
- → record: `trader_profile`

**Q3:** "What market focus?"
- [US] [Singapore] [Malaysia] [Other]
- → record: `market`

[INTAKE COMPLETE]
"Language: X | Profile: X | Market: X"
→ PROCEED TO PHASE 1

## Profile Definitions

| Profile | Time Horizon |
|---------|--------------|
| SCALPER | 5-15 minute catalyst |
| INTRADAY | Current trading session |
| SWING | Days to weeks |
| INVESTOR | Long-term business thesis |

---

## Phase 1 — Scanner (Finviz Default)

### Phase 1 Steps

**Step 1A — News Source Selection**

Ask the user:

"What news source for today?"
- [Finviz (Default)] [Reuters] [CNBC] [Bloomberg] [Other]

If the user selects a named source (Finviz, Reuters, CNBC, Bloomberg), proceed to Step 1B with that source.

If the user selects "Other" or provides a custom source:
- Ask: "What source? Please provide the name or URL."
- Accept ANY source the user gives: URL, platform name, website, local news site, or document.
- Do not reject any source. Do not judge the source quality at this stage.
- Record the source name and URL (if provided).
- Proceed to Step 1B with that source.

If the user does not choose any source, USE FINVIZ AS DEFAULT.

Record the selection as: `news_source`

**Step 1B — Fetch and Read Source (AI as Trader-Reader)**

Access the selected `news_source` live.

Required actions:
1. Access the source (fetch the page content)
2. Record: source name, URL (if available), access time
3. READ the content thoroughly — like an experienced trader reading a newspaper

How the AI MUST read:
- Read every headline and article summary carefully
- Understand the context of each news item — do NOT just scan for keywords
- Ask internally for each item: "What happened? Who is affected? How big is this?"
- Look for company names, ticker symbols, financial figures, dates, and events
- Identify which items could be trading opportunities for the user's trader profile
- Do NOT skip items just because they seem small — read first, filter later (Step 1C-1F)

Reading rules:
- The AI reads as a HUMAN READER, not as a keyword-matching script
- The AI understands business context: M&A, earnings, regulatory changes, geopolitical events, product launches, analyst ratings, sector shifts
- The AI distinguishes between: major market-moving news vs minor updates vs general commentary
- The AI pays attention to the user's `market` selection — if market is "US", prioritize US-listed companies and US market news

Source Access Rule:

If the source fails to access or returns no readable content:

`BLOCKED — SOURCE COULD NOT BE ACCESSED`

Do not claim the source was read. Do not generate a fabricated scanner report.
Do not use training knowledge as a substitute for reading the actual source.

**Step 1C — Profile Filter:** Apply trader profile. Hard rule: NO TICKER = NOISE.

**Step 1D — Extract Facts and Assess (Trader Judgment)**

For each news item that mentions a company or ticker, the AI extracts and assesses:

**Extract:**
- Company name
- Ticker symbol
- What happened (factual summary)
- Key numbers (revenue, EPS, price, percentage changes, deal values, etc.)
- Relevant dates
- Source

**Assess (AI applies trader judgment):**
- Is this a real, identifiable public company with a ticker? If NO → mark as NOISE and discard immediately
- How significant is this news for this specific company?
- Does this news create a trading opportunity for the user's trader profile?
- What is the transmission mechanism? (How does this news → business impact → financial expectation → potential price impact?)

**Fact Classification (MANDATORY):**

For every piece of information, label it as one of three categories:
- **FACT** — directly supported by the source content. The source states this clearly.
- **AI INFERENCE** — the AI's interpretation or conclusion based on the facts. The source does not state this directly, but the AI reasons it from context.
- **ESTIMATE** — an approximation based on available data. The exact figure is not available, but the AI estimates based on related information.

Do NOT mix these categories. Every claim must be labelled.
Do NOT present an inference as a fact. Do NOT present an estimate as a fact.

**Noise identification at this stage:**
- News items with no ticker or identifiable public company → NOISE (discard)
- News items about private companies with no public listing → NOISE (discard)
- General market commentary with no specific company → NOISE (discard)
- Opinion pieces or editorials with no actionable catalyst → NOISE (discard)
- Items unrelated to the user's `market` selection → NOISE (discard)

**Step 1E — Map Opportunity:** Direction, Materiality (1-5), Confidence (High/Medium/Low), Horizon Fit (Strong/Partial/Poor), Transmission Channel.

**Step 1F — Noise Gate (Final Filter — Noise Is Discarded)**

Every candidate must pass ALL of the following checks:

| Check | Rule | If Failed |
|-------|------|----------|
| Ticker / Company identifiable | Must have a real public company ticker | NOISE — discard |
| Market relevant | Must match the user's `market` selection | NOISE — discard |
| Materiality >= 3 | Score 1-5, minimum 3 to pass | NOISE — discard |
| Confidence >= Medium | Must be High or Medium (not Low) | NOISE — discard |
| Horizon Fit != Poor | Must be Strong or Partial (not Poor) | NOISE — discard |

**Noise handling rules:**
- Items that fail ANY check above are NOISE
- NOISE items are DISCARDED — do not include them in the report
- Do not list noise items in the output
- The report header shows "Filtered as noise: [K]" to acknowledge items were filtered
- Do not explain why individual items were filtered — just discard them

**Maximum opportunities:** 7

If more than 7 opportunities pass the Noise Gate, rank by:
1. Materiality (highest first)
2. Confidence (highest first)
3. Horizon Fit (Strong > Partial)
4. Catalyst clarity (most clear first)

Take the top 7. Discard the rest (they become noise).

### Phase 1 Output — LOCKED TEMPLATE

> **INSTRUCTION:** Reproduce EXACTLY this structure. Replace `[BRACKETS]` with live data. Use `Stock X`, `Stock Y` as the card numbering pattern. Do not add or remove anything.

```markdown
# MARKET SCANNER — [DATE] | Source: [SOURCE]

Akses: [DATE TIME (UTC+8)]
Items scanned: [N] | Material calls: [M] | Filtered as noise: [K]

---

## CARD [#1] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Direction | **Positive** / Negative / Mixed / Neutral |
| Materiality | ★★★☆☆ (X/5) |
| Confidence | HIGH / MEDIUM / LOW |
| Horizon Fit | Strong / Partial / Poor |

### What Happened
[Factual summary. Explicitly label FACT / INFERENCE / ESTIMATE where relevant]

### Why It Matters
[AI reasoning: 1–3 sentences explaining WHY this news matters for this specific trader profile. This is AI analysis, NOT fact restatement. Explain the transmission mechanism: how this news → business impact → financial/expectation change → potential price impact. Think like an experienced trader: "If I read this in the newspaper, why would I care about this stock today?"]

### Key Data
- [Key number or fact 1]
- [Key number or fact 2]
- Date: [Relevant date]

### Source
[Source name] | [URL if available]

---

## CARD [#2] — [TICKER]

| Field | Value |
|-------|-------|
| Company | [COMPANY NAME] |
| Direction | **Positive** / Negative / Mixed / Neutral |
| Materiality | ★★★☆☆ (X/5) |
| Confidence | HIGH / MEDIUM / LOW |
| Horizon Fit | Strong / Partial / Poor |

### What Happened
[Factual summary. Explicitly label FACT / INFERENCE / ESTIMATE where relevant]

### Why It Matters
[AI reasoning: 1–3 sentences explaining WHY this news matters for this specific trader profile. This is AI analysis, NOT fact restatement. Explain the transmission mechanism: how this news → business impact → financial/expectation change → potential price impact. Think like an experienced trader: "If I read this in the newspaper, why would I care about this stock today?"]

### Key Data
- [Key number or fact 1]
- [Key number or fact 2]
- Date: [Relevant date]

### Source
[Source name] | [URL if available]

---

[... repeat for each qualifying opportunity, maximum 7 cards ...]

---

STOP
WAIT FOR USER
```

> After the last card, output exactly `STOP` then `WAIT FOR USER` on separate lines.
> Do not proceed to Phase 2 unless the user explicitly opts in.

---

## Phase 2 — Deep Analysis (Primary Tool Only, NO SEC)

### Phase 2 Steps

**Step 2A — Primary Tool Selection:** Ask user. Default = Google Finance. If Skip → END SESSION.
**Step 2B — Fetch Primary Data:** Fetch from selected tool for EVERY Phase 1 opportunity. If blocked → `PRIMARY TOOL — BLOCKED`. If field missing → `NOT AVAILABLE`.
**Step 2C — Analyze & Synthesize:** Verify catalyst, assess timing fit, identify price levels, apply confidence gate. If Low confidence → `LOW CONFIDENCE — SKIP`.

### Phase 2 Output — LOCKED TEMPLATE

> **INSTRUCTION:** Reproduce EXACTLY this structure. Four mandatory blocks in this order: (1) Primary Data Summary, (2) Catalyst Verification, (3) Deep Analysis Reports, (4) Ranking Summary. Replace `[BRACKETS]` with live data. Do not add or remove anything.

```markdown
**PHASE 2 — DEEP ANALYSIS**
Primary Tool: **[Google Finance / Finviz / MarketBeat]**
Akses: [DATE TIME (UTC+8)]

---

### 1. Primary Data Summary

| Ticker | Company | Primary Tool | Fetch Status |
|--------|---------|--------------|--------------|
| Stock X | [COMPANY NAME] | [TOOL] | SUCCESS / BLOCKED / UNVERIFIED |
| Stock Y | [COMPANY NAME] | [TOOL] | SUCCESS / BLOCKED / UNVERIFIED |

---

### 2. Catalyst Verification

| Ticker | Phase 1 Catalyst | Verified | Notes |
|--------|------------------|----------|-------|
| Stock X | [Short description] | YES / PARTIAL / NO | [Notes] |
| Stock Y | [Short description] | YES / PARTIAL / NO | [Notes] |

---

### 3. Deep Analysis Reports

## [TICKER] — [COMPANY]

| Field | Value |
|-------|-------|
| **FETCH STATUS** | **SUCCESS** / BLOCKED / UNVERIFIED |
| Primary Tool | [Tool] |
| Direction | **POSITIVE** / NEUTRAL / NEGATIVE |

### Catalyst
[Factual summary with FACT / INFERENCE / ESTIMATE labels]

### Timing Fit
**Strong** / Partial / Poor (matched to [Profile])

### Relevant Levels
- [Level description]: [Value or NOT AVAILABLE]
- [Level description]: [Value or NOT AVAILABLE]

### Confidence
**HIGH** / MEDIUM

### Risk / Uncertainty
[Short risk note]

---

[... repeat for each ticker that passed the confidence gate ...]

---

### 4. Ranking Summary

| Rank | Ticker | Direction | Confidence | Timing Fit |
|------|--------|-----------|------------|------------|
| 1 | Stock X | POSITIVE | HIGH | Strong |
| 2 | Stock Y | NEUTRAL | MEDIUM | Partial |

---

STOP
WAIT FOR USER
```

> After the Ranking Summary, output exactly `STOP` then `WAIT FOR USER` on separate lines.
> Do not proceed to Phase 3 unless the user explicitly opts in.

---

## Phase 3 — SEC EDGAR Verification (Opt-in Only)

### Phase 3 Steps

**Trigger:** User explicitly asks for SEC EDGAR verification.
**Step 3A — Fetch SEC EDGAR Data:** For each ticker, access SEC EDGAR. Check: Revenue, Net Income/EPS, Total Debt, Cash Flow, Insider Transactions (Form 4), Outstanding Shares, Material Events (8-K).
**Step 3B — Label Results:** VERIFIED if SEC filing confirms data. UNVERIFIED — SEC DATA NOT AVAILABLE if data cannot be retrieved.

### Phase 3 Output — LOCKED TEMPLATE

> **INSTRUCTION:** Reproduce EXACTLY this structure. Two mandatory blocks: (1) Fetch Attempt, (2) Verification Results per ticker. Replace `[BRACKETS]` with live data. Do not add or remove anything.

```markdown
**PHASE 3 — SEC EDGAR VERIFICATION**
(Opt-in sahaja | Akses: [DATE TIME (UTC+8)])

---

### 1. Fetch Attempt

| Ticker | Filing Diakses | Status |
|--------|----------------|--------|
| Stock X | 10-Q / 10-K / 8-K / 6-K | SUCCESS / UNVERIFIED |
| Stock Y | 10-Q / 10-K / 8-K / 6-K | SUCCESS / UNVERIFIED |

---

### 2. Verification Results

## [TICKER] — [COMPANY]
**Label: VERIFIED**   or   **UNVERIFIED — SEC DATA NOT AVAILABLE**

- [Key financial item — e.g., Revenue]
- [Key financial item — e.g., Net Income / EPS]
- [Key financial item — e.g., Total Debt]
- [Key financial item — e.g., Cash Flow]
- [Key financial item — e.g., Insider Transactions]
- [Key financial item — e.g., Outstanding Shares]
- [Key financial item — e.g., Material Events]
- **Catatan:** [One-line link back to the Phase 1 catalyst]

---

[... repeat for each ticker ...]

---

### Ringkasan Verifikasi

| Ticker | Label |
|--------|-------|
| Stock X | VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE |
| Stock Y | VERIFIED / UNVERIFIED — SEC DATA NOT AVAILABLE |

**[N] VERIFIED | [M] UNVERIFIED**

---

STOP
WAIT FOR USER
```

> After the Ringkasan Verifikasi table, output exactly `STOP` then `WAIT FOR USER`.
> Do not proceed to Phase 4 unless the user explicitly asks.

---

## Phase 4 — Weekly Bias Summary (LOCKED FORMAT)

### Phase 4 Rules (MANDATORY)

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

### Phase 4 Output — LOCKED TEMPLATE

> **INSTRUCTION:** Reproduce EXACTLY this structure. Four mandatory components in order: (1) Summary Table, (2) Penjelasan Ringkas + Tag, (3) END OF SESSION table, (4) NO MONITORING disclaimer. Replace `[BRACKETS]` with live data. Do not add or remove anything.

```markdown
**PHASE 4 — WEEKLY BIAS SUMMARY**

| Saham | Arah | Anggaran % | Reason (max 10 words) |
|-------|------|------------|-----------------------|
| Stock X | Positive | +3% to +8% | [max 10 words] |
| Stock Y | Negative | -5% to -12% | [max 10 words] |

---

### Penjelasan Ringkas + Tag

**Stock X**
Arah Positive. [One short sentence].
`PREPARE FOR VOLUME BUY`

**Stock Y**
Arah Negative. [One short sentence].
`BE CAREFUL — MARKET CRASH RISK`

[... repeat for each stock. Use `WAIT FOR CONFIRMATION` for Neutral ...]

---

### END OF SESSION

| Ticker | Final Bias | Tag |
|--------|------------|-----|
| Stock X | Positive | PREPARE FOR VOLUME BUY |
| Stock Y | Negative | BE CAREFUL — MARKET CRASH RISK |

---

**NO MONITORING**
Ini adalah ringkasan bias berdasarkan analisis Fasa 1–3 sahaja.
Bukan nasihat pelaburan.
Tiada pemantauan berterusan.
Sesi tamat.
```

> This is the FINAL output of the session. Do not add anything after the NO MONITORING block.

---

# ====================================================================
# ERROR STATES SUMMARY (STANDARD)
# ====================================================================

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

---

# ====================================================================
# DATA INTEGRITY HIERARCHY
# ====================================================================

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

---

# ====================================================================
# OPPORTUNITY LIFECYCLE
# ====================================================================

`NEWS → TICKER FILTER → PROFILE FILTER → FACT EXTRACTION → MATERIALITY → CONFIDENCE → HORIZON FIT → NOISE GATE → PHASE 1 REPORT → USER OPT-IN → PRIMARY DATA FETCH → PHASE 2 REPORT → USER OPT-IN → SEC EDGAR FETCH → PHASE 3 REPORT → USER REQUEST → PHASE 4 REPORT → END`

Any hard gate fails → `STOP / SKIP`

---

# ====================================================================
# REFERENCES
# ====================================================================

| Phase | File |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 SEC EDGAR Verification | `references/phase3-sec-edgar.md` |
| Phase 4 Weekly Bias Summary | `references/phase4-weekly-bias.md` |
| Error States | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

---

# ====================================================================
# STATUS & CONTROLS
# ====================================================================

- **VERSION 4.0** — Locked Output Templates added for all 4 phases
- **Authority Gate** — Primary Tool selected by user (Google Finance / Finviz / MarketBeat / Skip). SEC EDGAR is separate opt-in phase
- **Evidence Integrity Gate** — every important claim must be supported by real data (source URL, filing reference, or label `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`)
- **Completion Gate** — phase only complete after every step in reference is done

---

# ====================================================================
# STAGNATION BREAKER
# ====================================================================

If Phase 1 produces 0 opportunities after two attempts with two different news sources (or one source + Other), stop with `No qualifying opportunities found for this trader profile and market focus.` Do not loop on the same source. Do not offer Phase 2 after Skip.

---

# ====================================================================
# AUTONOMOUS LOOP (7-STAGE)
# ====================================================================

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
