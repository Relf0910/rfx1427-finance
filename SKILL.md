---
name: rfx1427-finance
description: AI financial news scanner dan analysis framework versi 2.2 yang membaca SATU news source pilihan user, menapis public companies mengikut trader profile, market focus, time horizon, materiality dan confidence, dan menjalankan Deep Analysis dengan verification SEC EDGAR hanya selepas opt-in eksplisit. Gunakan hanya apabila user meminta imbasan berita kewangan, penapisan opportunities, rujukan eksplisit kepada nama skill ini, atau aliran Intake / Phase 1 / Phase 2 / Phase 3 framework ini. Jangan gunakan untuk nasihat beli atau jual, pelaksanaan dagangan, monitoring berterusan, watchlist, price alert, portfolio management, soalan finance umum tanpa ticker dan skop news scanning, atau analisis saham individu di luar konteks sumber berita. Output adalah read-only analysis, bukan trading advisor.
---

# RFX1427 Finance

Rangka kerja scanner berita kewangan dan analisis dengan kawalan gates yang ketat, berteraskan fakta, dan verification rasmi. Berasal dari `rfx1427-finance-framework-v2.2.txt` — setiap polisi di bawah adalah petikan atau restrukturisasi langsung dari framework asal.

## Prinsip teras

- **Source Fact → Verification → AI Analysis → Estimate** — empat lapisan ini mesti sentiasa dibezakan.
- **NO FABRICATION** — jangan reka berita, ticker, harga, volum, angka kewangan, filing, rating, aras atau akses sumber. Guna `NOT AVAILABLE`, `UNVERIFIED`, atau `BLOCKED` bila perlu.
- **OPT-IN ONLY** — Phase 2 hanya bermula selepas user memilih primary tool. Phase 3 hanya bermula selepas user meminta secara eksplisit.
- **NO AUTOMATIC PHASE TRANSITION** — lompat fasa tanpa keizinan dilarang.
- **NO LOOP** — jika user pilih `Skip Deep Analysis`, sesi berakhir.
- **NO MONITORING** — bukan watchlist manager, price alert, continuous monitor, atau portfolio manager.
- **ONE QUESTION AT A TIME** untuk Intake.
- **READ-ONLY ANALYSIS** — bukan trading advisor. Tiada buy/sell, entry, stop-loss, position sizing, atau guaranteed target.

## Bahasa

- Interaksi dengan user: Bahasa Melayu.
- Kod, identifier, error states, table headers, status enum: English (verbatim dari framework).
- Output laporan (Phase 1 / 2 / 3): Bahasa mengikut `output_language` pilihan user (English, Bahasa Melayu, Other).

## Aliran kerja (Session Architecture)

```text
USER
  │
  ▼
GATE 0 — INTAKE  (3 soalan, satu per satu, hard gate)
  │
  ├── incomplete → WAIT
  │
  ▼
PHASE 1 — SCANNER  (1A → 1B → 1C → 1D → 1E → 1F → 1G)
  │
  ├── source blocked → STOP
  ├── no qualifying opportunity → REPORT → STOP
  │
  ▼
PHASE 1 REPORT (max 7 opportunities)
  │
  ▼
STOP 1 — WAIT FOR USER
  │
  ├── Skip / no opt-in → END
  │
  └── Opt-in
        │
        ▼
PHASE 2 — DEEP ANALYSIS  (2A tool selection → 2B 3-stage verification)
        │
        ▼
PHASE 2 REPORT
        │
        ▼
STOP 2 — WAIT FOR USER
        │
        └── User asks
              │
              ▼
PHASE 3 — PLAIN SUMMARY
              │
              ▼
             END
```

## Pintu kawalan (Global Gate Rules)

1. **One question at a time** dalam Intake.
2. **Hard gate** — jangan terus jika maklumat wajib belum lengkap.
3. **No automatic phase transition** — fasa tidak melompat sendiri.
4. **No loop** — selepas Skip, sesi berakhir.
5. **No monitoring** — setiap sesi fresh.
6. **No fabrication** — guna `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`.

## Rujukan terperinci

Baca fail-fail ini mengikut fasa yang sedang berjalan:

| Fasa | Fail |
|---|---|
| Gate 0 Intake | `references/intake-form.md` |
| Phase 1 Scanner | `references/phase1-scanner.md` |
| Phase 2 Deep Analysis | `references/phase2-deep-analysis.md` |
| Phase 3 Plain Summary | `references/phase3-plain-summary.md` |
| Error states | `references/error-states.md` |
| Data Integrity Hierarchy | `references/data-integrity-hierarchy.md` |
| Hard Rules Master (37) | `references/hard-rules-master.md` |
| Decision Tree | `references/decision-tree.md` |
| Change Log v2.2 | `references/change-log-v2.md` |
| Acceptance Tests | `references/acceptance-tests.md` |

## Ringkasan error states (piawai)

| Keadaan | Output |
|---|---|
| Source gagal diakses | `BLOCKED — SOURCE COULD NOT BE ACCESSED` |
| Primary tool gagal | `PRIMARY TOOL — BLOCKED` |
| Data hilang | `NOT AVAILABLE` |
| SEC data hilang | `UNVERIFIED — SEC DATA NOT AVAILABLE` |
| Konflik data (SEC authoritative) | `DATA MISMATCH — SEC OVERRIDE` |
| Mechanism gagal | `REJECTED` |
| Confidence Low | `LOW CONFIDENCE — SKIP` |
| Tiada opportunity | `No qualifying opportunities found for this trader profile and market focus.` |

## Opportunity Lifecycle

`NEWS → TICKER FILTER → PROFILE FILTER → FACT EXTRACTION → MATERIALITY → CONFIDENCE → HORIZON FIT → NOISE GATE → PHASE 1 REPORT → USER OPT-IN → PRIMARY DATA → SEC DATA → COMPARISON → MECHANISM → TIMING → PRICE LEVELS → FINAL CONFIDENCE → PHASE 2 REPORT`

Mana-mana hard gate gagal → `STOP / SKIP`.

## Kriteria Noise Gate (Phase 1)

Semua mesti lulus:

- `Materiality >= 3` (skala 1–5)
- `Confidence >= Medium` (High / Medium / Low)
- `Horizon Fit != Poor` (Strong / Partial / Poor)
- Ticker atau public company boleh dikenal pasti
- Market focus relevan

Ranking jika > 7: Materiality → Confidence → Horizon Fit → Catalyst clarity. Maksimum **7 opportunities**.

## Comparison Matrix (Phase 2 Stage 3)

| Situation | Status | Action |
|---|---|---|
| Primary = SEC | MATCH — CONFIRMED | Use data |
| Primary ≠ SEC, SEC authoritative | DATA MISMATCH — SEC OVERRIDE | Use SEC |
| SEC unavailable | UNVERIFIED | Use Primary + label |
| Primary unavailable, SEC available | SEC ONLY | Use SEC |
| Both unavailable | DATA NOT AVAILABLE | Do not use |

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

Nota: Hierarchy bukan bermaksud SEC sentiasa lengkap. Untuk item yang memang boleh diverifikasi melalui SEC, SEC ialah authority. Untuk market data (price, volume, technicals), guna primary tool.

## Definisi siap (DoD) untuk setiap sesi

Sesi dianggap lengkap hanya selepas:

- Intake lengkap dengan ketiga-tiga field direkodkan.
- Phase 1 report dihantar dengan max 7 opportunities atau `No qualifying opportunities`.
- Phase 2 hanya jika user opt-in dan tool dipilih.
- Phase 3 hanya jika user meminta.
- Setiap dakwaan berlabel dengan betul (FACT / INFERENCE / ESTIMATE).
- Setiap error state menggunakan label piawai.
- Sesi berakhir dengan END (tiada loop, tiada monitoring).

## Status & Kawalan

- **DRAFT** — skill ini berada dalam status DRAFT sehingga user secara eksplisit memilih pilihan `Siap` (semua format + pasang, atau semua format tanpa pasang). Tiada auto-install, auto-publish, atau auto-replace tanpa arahan jelas.
- **Authority Gate** — SEC EDGAR ialah mandatory verification partner; Primary Tool dipilih oleh user (Finviz / Google Finance / MarketBeat / Skip). Primary Tool tidak dipilih oleh AI bagi pihak user.
- **Evidence Integrity Gate** — setiap dakwaan penting mesti disokong data sebenar (source URL, filing reference, atau label `NOT AVAILABLE` / `UNVERIFIED` / `BLOCKED`). Tiada fabrication dibenarkan.
- **Completion Gate** — fasa hanya selesai selepas setiap step dalam rujukan selesai dan status direkodkan (PRIMARY DATA FETCHED, SEC DATA FETCHED, MATCH / MISMATCH, dll).

## Intent-to-Command Engine

Setiap permintaan user (contoh: "scan berita untuk hari ini") dikompil kepada perintah operasi dengan elemen: tindakan + objek, skop/universe, input & kesegaran, urutan kerja, titik keputusan, kriteria/filter/ranking, format output, pengendalian kegagalan, had keselamatan, dan kriteria siap. Compiler merujuk kepada rujukan fasa yang berkaitan — `references/intake-form.md`, `references/phase1-scanner.md`, `references/phase2-deep-analysis.md`, `references/phase3-plain-summary.md`.

## Stagnation Breaker

Jika Phase 1 menghasilkan 0 opportunities selepas dua percubaan dengan dua news source berbeza (atau satu sumber + Other), hentikan dengan `No qualifying opportunities found for this trader profile and market focus.` Jangan loop pada sumber yang sama. Jangan tawar Phase 2 selepas Skip.

## Autonomous Loop (7-Stage)

Operasi setiap sesi melalui kitaran tertutup:

```text
INSPECT → PLAN → BUILD → VALIDATE → DIAGNOSE → REPAIR → REVALIDATE
```

- INSPECT — sahkan state semasa (Intake lengkap? Phase mana?).
- PLAN — pilih fasa & step seterusnya.
- BUILD — jalankan step (akses source, extract, verify).
- VALIDATE — semak hard gate (Materiality, Confidence, Horizon Fit, Noise Gate, Comparison Matrix).
- DIAGNOSE — kenal pasti punca jika gate gagal.
- REPAIR — pilih tindakan pembetulan (labelkan NOT AVAILABLE, SKIP, dsb).
- REVALIDATE — ulang validasi selepas repair.

Loop berterusan sehingga Definisi Siap lulus atau halangan didokumenkan.