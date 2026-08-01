# Data directory

**Contents of this folder are not committed to Git.** Individual source files range from
25 MB to 390 MB, exceeding GitHub's 100 MB per-file limit, and raw data does not belong in
version control.

## How to obtain the data

1. Go to https://dkasolarcentre.com.au/download?location=alice-springs
2. Download the yearly Alice Springs extracts (2008–present) and the
   `96-Site_DKA-MasterMeter1` extract
3. Place the `.csv` files in this directory
4. Record the download date in `docs/data-quality-summary.md`

Expected layout:

```
data/
├── Alice_Springs_2008.csv
├── ...
├── Alice_Springs_2026.csv
└── 96-Site_DKA-MasterMeter1.csv
```

## What we know about it

See [`../docs/data-quality-summary.md`](../docs/data-quality-summary.md) for row counts,
coverage, schema drift, and measured missingness.

## Attribution

Data © Desert Knowledge Australia Solar Centre. Used under their public data terms.
