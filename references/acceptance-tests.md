# Acceptance Tests

Set ujian asas untuk `rfx1427-finance`. Setiap seksyen mengandungi jadual markdown untuk pengiraan automatik oleh validator.

## Pencetus positif

| ID | Input | Hasil jangkaan |
| --- | --- | --- |
| TC-P1 | "rfx1427 scan CNBC untuk swing trader di US market" | Mulakan Intake jika medan belum lengkap, kemudian tanya news source, lanjut ke Phase 1 |
| TC-P2 | Selepas Phase 1, user berkata "teruskan deep analysis" | Tanya tool selection (Finviz / Google Finance / MarketBeat / Skip); Skip → END SESSION |
| TC-P3 | Selepas Phase 2, user berkata "beri plain summary" | Output jadual Stock/Direction/Est. Change/Reason dengan direction language piawai |

## Bukan pencetus

| ID | Input | Hasil jangkaan |
| --- | --- | --- |
| TC-N1 | "monitor NVDA untuk alert harga sepanjang hari" | Tolak. Rujuk Rule 5 / Hard Rule 32 (NO MONITORING). |
| TC-N2 | "beli NVDA sekarang, apa target?" | Tolak. Read-only analysis, tiada buy/sell/entry/position sizing/guaranteed target. |

## Kes tepi

| ID | Input | Hasil jangkaan |
| --- | --- | --- |
| TC-E1 | Step 1B — webfetch CNBC mengembalikan ralat | Output `BLOCKED — SOURCE COULD NOT BE ACCESSED`. STOP. Jangan fabricate scanner report. |
| TC-E2 | Selepas Stage 3 Phase 2, semua opportunities dapat Confidence = Low | Output "No opportunities passed the final confidence gate." Jangan force-fill report. |

## Kes kegagalan

| ID | Input | Hasil jangkaan |
| --- | --- | --- |
| TC-F1 | Intake diberikan separa (contoh: trader profile sahaja) | Kekal di Intake. Tanya soalan tertinggal satu per satu. Hard gate aktif. |

## Konflik arahan

- **Konflik A — user minta skip DAN deep analysis serentak dalam satu mesej:** Patuhi Rule 3 (NO AUTOMATIC PHASE TRANSITION). Hentikan di STOP1, tanya "Skip atau opt-in?" dan tunggu jawapan tunggal.
- **Konflik B — user minta Phase 3 tanpa pernah melalui Phase 2:** Patuhi Rule 27 (User must explicitly ask) dan struktur fasa. Terangkan Phase 3 memerlukan Phase 2 selesai atau data Phase 1 yang relevan. Tawarkan lalai: jalankan Phase 3 berdasarkan Phase 1 sahaja dengan label "based on Phase 1 only".

## Kebergantungan hilang

- **Kebergantungan 1 — webfetch untuk news source tidak tersedia:** Source Access Rule terpakai → `BLOCKED — SOURCE COULD NOT BE ACCESSED`. Sesi STOP selepas Intake lengkap.
- **Kebergantungan 2 — SEC EDGAR tidak tersedia pada Phase 2 Stage 2:** UNVERIFIED state — Primary Tool digunakan dengan label, tiada fabrication.
- **Kebergantungan 3 — Primary tool (Finviz/Google Finance/MarketBeat) tidak tersedia:** PRIMARY TOOL — BLOCKED. Tahap penggunaan data jatuh ke SEC sahaja jika SEC available, atau DATA NOT AVAILABLE.