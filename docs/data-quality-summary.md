# Data Quality Summary — DKASC Alice Springs

**Source:** [Desert Knowledge Australia Solar Centre](https://dkasolarcentre.com.au/download?location=alice-springs)
**Downloaded:** 29 July 2026
**Assessed:** 1 August 2026

All figures below are measured from the downloaded files, not estimated.

---

## 1. What we have

| File group | Files | Rows | Columns | Size |
|---|---|---|---|---|
| Yearly extracts | `Alice_Springs_2008.csv` … `_2026.csv` (19) | ~1.9M | 197 → 210 | ~3.0 GB |
| Master meter extract | `96-Site_DKA-MasterMeter1.csv` | 1,767,903 | 17 | 390 MB |

**Resolution:** 5-minute intervals throughout.

## 2. The 17-column file is a column slice, not an aggregate

`96-Site_DKA-MasterMeter1.csv` is often mistaken for a combined dataset. It is not. It contains:

- 1 × `timestamp`
- 7 × site **96 — DKA MasterMeter1** (active energy, current phase average, active power,
  power factor, average voltage, frequency, THD voltage)
- 9 × site **101 — Weather Station** (wind speed, temperature, relative humidity, global
  horizontal radiation, diffuse horizontal radiation, wind direction, daily rainfall,
  global tilted radiation, diffuse tilted radiation)

Every one of these appears in the yearly files, prefixed `96_DKA_MasterMeter1_*` and
`101_DKA_WeatherStation_*`. The ~200 columns in the yearly files are the **per-array
breakdown** — roughly 50 inverter/array channels (M1–M20, split by electrical phase), plus both
master meters and the weather station.

**Decision:** the 17-column file is our primary modelling dataset. Per-inverter channels are out
of scope — that is anomaly detection (Theme 3), not forecasting.

## 3. Coverage

| File | Rows | Columns | Range |
|---|---|---|---|
| 2008 | 32,047 | 197 | 2008-09-12 → 2009-01-01 |
| 2009–2023 | ~105,000/yr | 197 | full years |
| 2024 | 105,387 | **210** | full year |
| 2025 | 105,394 | 210 | full year |
| 2026 | 12,091 | 210 | 2026-01-01 → **2026-02-11** |
| Master meter | 1,767,903 | 17 | 2008-09-12 → **2025-08-23** |

## 4. Known issues

| # | Issue | Detail | Action |
|---|---|---|---|
| 1 | **Schema drift** | 197 columns 2008–2023, 210 from 2024. Thirteen added: BESS active/reactive/apparent power and state of charge, site demand totals, PV totals, grid totals. No columns removed. | Explicit reconciliation step; treat BESS columns as available from 2024 only |
| 2 | **Year-boundary overlap** | Each yearly file runs one day into the next (2008 file ends `2009-01-01 23:55`, 2009 file starts `2009-01-01 00:00`) | Deduplicate on `timestamp`; assert uniqueness |
| 3 | **Stale download** | 2026 file ends 11 Feb 2026; master meter ends 23 Aug 2025 | Re-download before A2; record download date |
| 4 | **Cumulative counter** | `Active_Energy_Delivered_Received` runs −2.6 → 623,572 — a meter odometer, not interval energy | Difference it; unit-test the result |
| 5 | **Sign convention** | `Active_Power` is negative when exporting | Decide and document one convention |

## 5. Missingness (master meter file, 1,767,903 rows)

| Column | Missing |
|---|---|
| `timestamp` | 0.0% |
| `Active_Power` | 1.5% |
| `Active_Energy_Delivered_Received` | 1.5% |
| `Average_Voltage_Line_to_Neutral` | 1.5% |
| `Frequency` | 1.5% |
| `Weather_Temperature_Celsius` | 2.2% |
| `Weather_Relative_Humidity` | 2.2% |
| `Global_Horizontal_Radiation` | 2.2% |
| `Diffuse_Horizontal_Radiation` | 2.2% |
| `Weather_Daily_Rainfall` | 2.2% |
| `Wind_Direction` | 2.3% |
| `Radiation_Diffuse_Tilted` | 33.7% |
| `Radiation_Global_Tilted` | 36.1% |
| `Current_Phase_Average` | 41.2% |
| `Power_Factor_Signed` | 41.2% |
| `THD_Voltage_Average` | 41.2% |
| **`Wind_Speed`** | **52.4%** |

**Note:** Thuseethan et al. (2025) use eight traditional features on this site and **exclude wind
speed**, which independently corroborates the 52% missingness measured here.

## 6. Rows per year (master meter)

| Year | Rows | | Year | Rows |
|---|---|---|---|---|
| 2008 | 31,758 | | 2017 | 104,614 |
| 2009 | 105,116 | | 2018 | 105,120 |
| 2010 | 105,120 | | 2019 | 102,905 |
| 2011 | 104,901 | | 2020 | 105,382 |
| 2012 | 105,394 | | 2021 | 100,538 |
| 2013 | 105,076 | | 2022 | 102,901 |
| 2014 | 105,111 | | 2023 | 101,797 |
| 2015 | 105,120 | | 2024 | 104,246 |
| 2016 | 105,408 | | 2025 | 67,396 |

A full year at 5-minute resolution is 105,120 rows. Shortfalls indicate sensor outages.

## 7. Gap in our extract

The master meter file covers **MasterMeter1 only**. The prior work benchmarks both meters, and
its best result (R² 0.8641) is on **Meter 2**. To compare like for like we need
`62_DKA_MasterMeter2_*` extracted from the yearly files.

## 8. The 5 Vs

| V | Assessment |
|---|---|
| **Volume** | ~3.4 GB, 1.8M rows on the master meter, 17 years |
| **Velocity** | 5-minute batch. The dispatch decision can wait → **batch**, not streaming |
| **Variety** | Structured time-series CSV; single schema after reconciliation |
| **Veracity** | Documented missingness, schema drift, sensor outages, cumulative counter |
| **Value** | Generation forecast driving battery dispatch and grid-import decisions |
