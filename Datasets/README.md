# Data directory

**Contents of this folder are not committed to Git.** Individual source files range from
25 MB to 390 MB, exceeding GitHub's 100 MB per-file limit, and raw data does not belong in
version control.

## Layout

```
data/
├── raw/          Source of truth — 19 yearly extracts, 2008–2026 (~2.9 GB)
└── reference/    Cross-check only — 96-Site_DKA-MasterMeter1.csv (390 MB)
```

### `raw/` — the source of truth

The 19 yearly extracts. These are the only files containing **all** required column groups:

| Group | Prefix | Columns |
|---|---|---|
| Master meter 1 | `96_DKA_MasterMeter1_` | 7 |
| Master meter 2 | `62_DKA_MasterMeter2_` | 7 |
| Weather station | `101_DKA_WeatherStation_` | 9 |
| BESS and site totals *(2024 onward)* | `239_` `240_` `241_` `242_` | 13 |

Files here are **immutable**. Never edit them in place — all cleaning is scripted in `/src` so
every downstream output can be regenerated from these.

### `reference/` — validation only

`96-Site_DKA-MasterMeter1.csv` is a 17-column DKASC extract covering MasterMeter1 and the weather
station from 2008-09-12 to 2025-08-23.

It is **not** a source for modelling. Its only purpose is to validate our own processing: after
extracting MasterMeter1 from the yearly files and differencing the cumulative energy counter, the
result should match this file over the overlapping period. That check addresses risk T3 in
[`../docs/risk-register.md`](../docs/risk-register.md).

## How to obtain the data

1. Go to https://dkasolarcentre.com.au/download?location=alice-springs
2. Download the yearly Alice Springs extracts (2008–present) into `data/raw/`
3. Optionally download the `96-Site_DKA-MasterMeter1` extract into `data/reference/`
4. Record the download date in [`../docs/data-quality-summary.md`](../docs/data-quality-summary.md)

## What we know about it

See [`../docs/data-quality-summary.md`](../docs/data-quality-summary.md) for row counts, coverage,
schema drift and measured missingness.

## Attribution

Data © Desert Knowledge Australia Solar Centre. Used under their public data terms.
