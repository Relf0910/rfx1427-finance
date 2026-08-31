# Error States

Sumber: framework v2.2, Seksyen 10.

## SOURCE ERROR

```text
BLOCKED — SOURCE COULD NOT BE ACCESSED
```

## PRIMARY TOOL ERROR

```text
PRIMARY TOOL — BLOCKED
```

## DATA MISSING

```text
NOT AVAILABLE
```

## SEC DATA MISSING

```text
UNVERIFIED — SEC DATA NOT AVAILABLE
```

## DATA CONFLICT

Jika SEC ialah authoritative source untuk item tersebut:

```text
DATA MISMATCH — SEC OVERRIDE
```

## MECHANISM FAILED

```text
REJECTED
```

## LOW CONFIDENCE

```text
LOW CONFIDENCE — SKIP
```

## NO QUALIFYING OPPORTUNITIES

Jika tiada opportunity lulus Noise Gate:

> No qualifying opportunities found for this trader profile and market focus.

Jangan force-fill report.

## Prinsip Am

- `NOT AVAILABLE` → data tidak wujud atau tidak dapat dicapai.
- `UNVERIFIED` → data mungkin wujud tetapi tidak dapat disahkan melalui SEC.
- `BLOCKED` → akses kepada sumber atau tool gagal.
- Label ini wajib digunakan — jangan digantikan dengan deskripsi longgar.