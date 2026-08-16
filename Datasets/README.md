# Datasets

**Contents of this folder are not committed to Git.** Individual source files range from
25 MB to 390 MB, exceeding GitHub's 100 MB per file limit, and raw data does not belong in
version control.

## Layout

```
Datasets/
├── raw/          Source of truth — 19 yearly extracts, 2008–2026 (~3.1 GB)
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

Files here are **immutable**. Never edit them in place, all cleaning is performed by scripted
processing code so every downstream output can be regenerated from these.

### `reference/` — validation only

`96-Site_DKA-MasterMeter1.csv` is a 17-column DKASC extract covering MasterMeter1 and the weather
station from 2008-09-12 to 2025-08-23.

It is **not** a source for modelling. Its only purpose is to validate our own processing: after
extracting MasterMeter1 from the yearly files and differencing the cumulative energy counter, the
result should match this file over the overlapping period. That check addresses risk T3 in
[`../Supporting_Documents/risk-register.md`](../Supporting_Documents/risk-register.md).



## What we know about it

See [`../Supporting_Documents/data-quality-summary.md`](../Supporting_Documents/data-quality-summary.md) for row counts, coverage,
schema drift and measured missingness.

## Attribution

Data © [Desert Knowledge Australia Solar Centre](https://dkasolarcentre.com.au/download?location=alice-springs),
Alice Springs. Used under their public data terms. 
