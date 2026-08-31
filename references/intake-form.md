# Intake Form (Gate 0)

Sumber: framework v2.2, Seksyen 5 & 6.

Intake mempunyai **3 soalan** sahaja. Tanya **satu per satu** — jangan tanya semua serentak (Rule 1). Jika mana-mana field belum lengkap, **WAIT** (Rule 2).

## Q1 — Output Language

Tanya:

> Apa bahasa untuk output?

Pilihan:

- English
- Bahasa Melayu
- Other

Rekod sebagai: `output_language`

## Q2 — Trader Profile

Tanya:

> Apa trader profile?

Pilihan:

- Scalper
- Intraday
- Swing
- Investor

Rekod sebagai: `trader_profile`

## Q3 — Market Focus

Tanya:

> Apa market focus?

Pilihan:

- US
- Singapore
- Malaysia
- Other

Rekod sebagai: `market`

## Intake Complete

Selepas ketiga-tiga field lengkap:

```text
Language: X | Profile: X | Market: X
```

Kemudian:

```text
PROCEED → PHASE 1
```

Jika salah satu field belum lengkap:

```text
WAIT
```

## Hard Gate

Jangan terus ke Phase 1 jika mana-mana soalan belum dijawab. Ulang soalan yang tertinggal, satu per satu.