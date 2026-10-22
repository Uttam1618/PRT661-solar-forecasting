# PRT661 — Solar Generation Forecasting (DKASC Alice Springs)

Semester 2, 2026 · Charles Darwin University · Data Science Practice (PRT661)
**Theme 2: Predictive Analytics and Forecasting**

---

## Project

Forecasting solar generation at the Desert Knowledge Australia Solar Centre (Alice Springs)
across 2008–2026, with degradation-aware features and explicit ramp-event handling, to support
**battery charge/discharge scheduling** using the 2024 BESS installation.

**The decision this supports:** when should the battery charge, and when should it discharge?

Everything upstream (acquisition, storage, processing, features, models, and the battery
dispatch simulation added in Assessment 3) exists to serve that decision.

## Relationship to prior work

This project builds on and cites:

> Thuseethan, S., Gangajaliya, S., Hamlin, L., Shanmugam, B., & Thennadil, S. (2025).
> Conv-Ensemble for solar power prediction with First Nations seasonal information.
> *IEEE Open Journal of the Computer Society*, 6, 884–895.
> https://doi.org/10.1109/OJCS.2025.3580339

That paper forecasts generation at the same site, but for a different purpose: it evaluates
whether First Nations seasonal information improves predictive accuracy. This project forecasts in
order to support an operational decision — battery dispatch — and differs in four ways:

| | Prior work | This project |
|---|---|---|
| Purpose | Model accuracy for its own sake | Forecast drives battery charge/discharge decisions |
| Time span | 2019–2024 (465,078 rows) | 2008–2026 (~1.77M rows) |
| Battery | Not available (predates the 2024 BESS install) | BESS state-of-charge and totals included |
| Open problem addressed | High error at peak irradiance and dawn/dusk; per-feature influence not analysed | Ramp-event handling and feature importance |

The prior work's First Nations seasonal calendars are **not** reproduced here. The reasoning is
recorded in [`Supporting_Documents/ethics-privacy-security.md`](Supporting_Documents/ethics-privacy-security.md).

**Benchmark to beat** (their published results on this site):

| Meter | R² | MSE |
|---|---|---|
| Master Meter 1 | 0.8015 | 96.13 |
| Master Meter 2 | 0.8641 | 22.41 |

## Team — Group 4

| Role | Member | GitHub |
|---|---|---|
| Project Lead / PM | Uttam Shrestha | [@Uttam1618](https://github.com/Uttam1618) |
| Data Engineer | Abhishek Tamang | [@Abhisek000](https://github.com/Abhisek000) |
| Data and Feature Engineer | Sarin Uprety | [@Sarin751](https://github.com/Sarin751) |
| Modelling and Visualisation Lead | Yogesh Basnet | [@viperx-ux](https://github.com/viperx-ux) |

Full allocation, epic ownership and report sections:
[`Planning/Task_Allocation/task-allocation.md`](Planning/Task_Allocation/task-allocation.md)

## Project management

Jira board: https://uttamshrestha1618.atlassian.net/jira/software/projects/SCRUM/boards/1

Workflow stages (these names are used identically in the Draw.io diagrams and as Jira epics):

1. Data Acquisition
2. Data Storage
3. Data Processing
4. Feature Engineering
5. Analytics and Machine Learning
6. Visualisation
7. Workflow Automation
8. Governance and Monitoring *(cross-cutting)*

Schedule, sprints and epic dates: [`Planning/planning.md`](Planning/planning.md)

## Repository structure

Folders map directly to the documentation artefacts required by the assessment.

```
Assessment_Reports/         A1 to A4 submissions as PDF
Presentation/               A3 demonstration slides and individual summaries
Architecture_Diagrams/      Architecture diagrams 01 to 10: drawio/ (editable sources), png/ (exports)
Workflow_Diagrams/          Workflow plan and progress diagrams, draw.io sources and PNG exports
Planning/                   Milestones, sprints and epic schedule (planning.md)
  Project_Planning_Records/   dated meeting, sprint and decision records
  Task_Allocation/            roles, epic ownership, report sections, governance
Supporting_Documents/       Risk register, ethics and privacy, data quality, feature dictionary
Datasets/                   Local data directory, contents are NOT committed
notebooks/                  Analysis notebooks 01 to 08, run in order
dashboard/                  Streamlit decision support dashboard (A4)
Outputs/                    Evidence written by the notebooks, committed:
  Results/                    result tables (.csv) and markdown reports (.md)
  Notebook_Figures/           figures 1 to 18
  Dashboard_Figures/          dashboard screenshots
run_pipeline.py             Runs the notebooks in order and checks every expected output
.streamlit/                 Dashboard theme
```

## Data

Source: [Desert Knowledge Australia Solar Centre](https://dkasolarcentre.com.au/download?location=alice-springs) — Alice Springs.

Raw data is **not committed to this repository** (individual files are 25–390 MB, exceeding
GitHub limits). See [`Datasets/README.md`](Datasets/README.md) for the directory layout, and
[`Supporting_Documents/data-quality-summary.md`](Supporting_Documents/data-quality-summary.md)
for row counts, coverage, schema drift and measured missingness.

## Reproducing this work

Place the DKASC extracts under `Datasets/` as described in
[`Datasets/README.md`](Datasets/README.md), then run the notebooks in order. Each stage reads only
the store its predecessor wrote, and each emits a markdown artefact under `Outputs/` that the
reports cite.

| # | Notebook | Reads | Writes | Runtime |
|---|---|---|---|---|
| 01 | `01_data_profiling.ipynb` | 19 raw yearly CSVs | `Outputs/Results/schema_matrix.csv` | ~3 min |
| 01b | `01b_schema_decisions.ipynb` | schema matrix, raw CSVs | `Outputs/Results/schema_drift_summary.md` | ~2 min |
| 02 | `02_ingest_mastermeter1.ipynb` | `Datasets/reference/96-Site_DKA-MasterMeter1.csv` | 5 min and hourly Parquet, `Outputs/Results/data_quality_mastermeter1.md` | ~2 min |
| 03 | `03_clean_mastermeter1.ipynb` | 5 min Parquet | cleaned Parquet, `Outputs/Results/cleaning_report_mastermeter1.md` | ~3 min |
| 04 | `04_features_and_eda.ipynb` | cleaned hourly Parquet | `features_hourly.parquet`, figures 1 to 3, feature dictionary | ~1 min |
| 04b | `04b_supporting_figures.ipynb` | cleaned hourly, features | figures 4 to 6 | ~1 min |
| 05 | `05_modelling.ipynb` | `features_hourly.parquet` | `Outputs/Results/model_results.md`, figures 7 to 10, `forecasts_hourly.parquet` (all out of sample forecasts, added in A3) | ~6 min |
| 06 | `06_bess_dispatch.ipynb` | `forecasts_hourly.parquet`, `features_hourly.parquet`, `Datasets/raw/Alice_Springs_2024.csv` and `Alice_Springs_2025.csv` | `forecasts_calibrated.parquet`, `dispatch_hourly.parquet`, `Outputs/Results/dispatch_results.md`, `Outputs/Results/dispatch_strategies.csv`, figures 11 to 14 | a few min |
| 07 | `07_demand_forecast.ipynb` | `dispatch_hourly.parquet`, `mastermeter1_hourly_clean.parquet` (temperature) | `demand_forecasts.parquet`, `Outputs/Results/demand_model_results.md`, `Outputs/Results/demand_model_comparison.csv`, figures 15 and 16 | a few min |
| 08 | `08_monitoring_retraining.ipynb` | `forecasts_calibrated.parquet`, `demand_forecasts.parquet`, `Datasets/raw/Alice_Springs_2024.csv` and `Alice_Springs_2025.csv` | `monitoring_daily.parquet`, `Outputs/Results/monitoring_results.md`, `Outputs/Results/monitoring_alerts.csv`, figures 17 and 18 | a few min |

Requirements: Python 3.11 with pandas, numpy, matplotlib, scikit-learn, pyarrow and Pillow, plus
jupyter to run the chain from the command line. The dashboard adds streamlit and plotly
(`dashboard/requirements.txt`).
Parquet stores and raw data are excluded from version control; small artefacts under `Outputs/`
are committed as assessment evidence.

**Note on the notebook paths.** The notebooks currently hard-code the repository location. Change
the `REPO` variable in the first cell of each notebook to your own path.

### One command reproducibility check

`run_pipeline.py` runs the notebooks in order and checks that every expected output (stores,
result tables and all 18 figures) exists and, after a run, was rewritten by that run.

```
python run_pipeline.py --check     # check outputs only, runs nothing
python run_pipeline.py             # run notebooks 01 to 08, then check
python run_pipeline.py --from 06   # rerun 06, 07 and 08, then check
```

It ends with `REPRODUCIBILITY CHECK PASSED` or lists each missing or stale output.

## Decision support dashboard

An interactive Streamlit dashboard for the site operator (Assessment 4). It reads only the saved
outputs in `Datasets/processed` and `Outputs`, so run notebooks 05 to 08 first. The nightly battery
rule from notebook 06 is re-run live (`dashboard/battery.py`), so every setting changes the plan.

```
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

It opens at http://localhost:8501 with six pages:

| Page | What it shows |
|---|---|
| Overview | Saving, value of the forecast and share of perfect foresight, cumulative and monthly savings by strategy |
| Battery plan by day | Clickable calendar of daily savings, the 22:00 decision, solar forecast range against actual, battery charge |
| Scenario lab | Tariff, period, solar caution, demand forecast and battery size compared live |
| Forecast models | Demand model accuracy by hour, month and day type, week explorer |
| System health | Coverage and error monitoring with alerts, drift check, retraining strategies |
| Data and pipeline | Pipeline diagram, input file inventory, nightly run schedule |

Screenshots: [`Outputs/Dashboard_Figures/`](Outputs/Dashboard_Figures/)

## What changed in Assessment 2

The nineteen yearly extracts contain **no meteorological columns at all**. Master Meter 1 became
the primary dataset because it carries irradiance, temperature, humidity, wind and rainfall at the
same resolution and is the series the benchmark reports on. Full reasoning and a per-column
coverage table are in [`Outputs/Results/schema_drift_summary.md`](Outputs/Results/schema_drift_summary.md) and
[`Planning/Project_Planning_Records/2026-09-13-a2-sprint.md`](Planning/Project_Planning_Records/2026-09-13-a2-sprint.md).

## Assessment 2 headline results

Target: Master Meter 1 `Active_Power`, forecast 1 hour and 24 hours ahead. Features are taken at
time t and the label at t+h, so no weather forecast is assumed.

| Model | 1 h MAE | 1 h R2 | 24 h MAE | 24 h R2 |
|---|---|---|---|---|
| Gradient boosting | **3.61 kW** | **0.980** | **6.96 kW** | **0.913** |
| Seasonal naive | 7.74 kW | 0.887 | 7.74 kW | 0.887 |
| Persistence | 13.90 kW | 0.866 | 7.74 kW | 0.887 |
| Climatology | 11.07 kW | 0.889 | 11.07 kW | 0.889 |

Mean across four expanding-window walk forward folds, 2019 to 2025. At the 24 hour horizon
seasonal naive is identical to persistence by construction.

Measured panel degradation on the stable array, 2014 onward: **-0.454 kW per year, -0.94% of the
mean annually**.

**Known limitation.** The 80% prediction interval is overconfident at 24 hours: daylight coverage
is 0.706 against a nominal 0.80, which fails the project's own quality gate. It is published with
that warning rather than withdrawn. Recalibration is scheduled for Assessment 3.
This was done in Assessment 3; see the results below.

## Assessment 3 headline results

Notebook 06 turns the forecast into a battery decision and measures what it is worth. Full tables
are in [`Outputs/Results/dispatch_results.md`](Outputs/Results/dispatch_results.md); the as built architecture is
[`Architecture_Diagrams/png/08-system-architecture-a3.png`](Architecture_Diagrams/png/08-system-architecture-a3.png).

**1. Calibrated uncertainty.** Crossed quantiles were repaired and the 80% interval was
recalibrated with rolling conformal prediction (30 day window, using only data available at the
time). Daylight coverage across all folds is now **80.1% at 1 hour and 80.0% at 24 hours**, and lies
between 79.3% and 81.0% in every fold. In the latest fold, where A2 reported 0.772 and 0.706, the
24 hour coverage rose from 70.6% to 79.3%.

**2. The site and its battery.** Site telemetry from 2024 and 2025 balances as
demand = solar + grid + battery. A configuration change at the end of February 2024 halved the
ratio of site solar to Master Meter 1 (data drift), so the analysis starts on 1 March 2024. The
battery, modelled from its own telemetry, holds 354 kWh at up to 115 kW with an 82.8% round trip
efficiency.

**3. Forecast based dispatch.** Each night at 22:00 the plan decides how much off peak grid energy
to store, using the 24 hour forecast. Simulated from April 2024 to August 2025 under an
illustrative time of use tariff:

| Strategy | Saving against no battery |
|---|---|
| Store surplus solar only, no forecast | 17.3% |
| Always fill the battery overnight | 19.6% |
| **Forecast plan** (caution chosen on 2024, tested on 2025) | **22.3%** |
| Perfect foresight (upper bound) | 25.3% |

The forecast plan saves **$3,419** more than the best rule without a forecast and captures
**47%** of the benefit perfect foresight would give. The demand forecast is the main limit: with
perfect demand the same solar forecast would capture 85%.

**Planned for Assessment 4:** a better demand forecast (weekday and weekend patterns,
temperature), an optimiser in place of the rule, and drift monitoring with scheduled retraining.

**Assessment 3 demonstration video:** [Watch on Youtube](https://youtu.be/xvJuezoTlnU?si=Or8yRUyxQJGdn6X4)

## Assessment 4 headline results

Assessment 4 strengthened the decision, kept it healthy and put it in front of the operator.
Tables are in [`Outputs/Results/demand_model_results.md`](Outputs/Results/demand_model_results.md) and
[`Outputs/Results/monitoring_results.md`](Outputs/Results/monitoring_results.md); the as built and deployment
architecture are
[`Architecture_Diagrams/png/09-system-architecture-a4.png`](Architecture_Diagrams/png/09-system-architecture-a4.png)
and [`Architecture_Diagrams/png/10-deployment-architecture.png`](Architecture_Diagrams/png/10-deployment-architecture.png).

**1. Demand forecasting (notebook 07).** Five approaches were compared with monthly walk forward
refits, July 2024 to August 2025. Gradient boosting cut the planning hour error from 54.5 kW (the A3
seven day mean) to **24.9 kW**, mainly because it knows the weekday.

| Battery plan with demand from | Saving against no battery | Value of the forecast | Share of perfect foresight |
|---|---|---|---|
| A3: 7 day same hour mean | 20.8% | $2,209 | 39% |
| **Gradient boosting (A4)** | **22.4%** | **$3,943** | **70%** |
| Perfect demand (ceiling) | 22.9% | $4,566 | 80% |

**2. Monitoring, drift and retraining (notebook 08).** Daily checks of the 24 hour forecast error
and interval coverage against limits fixed on 2019 to 2020 raised 28 alert episodes over 2019 to
2025. A drift check on the site solar to Master Meter 1 ratio flags the February 2024 site change
automatically. Refitting the demand model monthly gives 24.9 kW against 41.3 kW for a model never
retrained, so monthly refits are the operating choice.

**3. Decision support dashboard.** Six pages, with the nightly battery rule rerun live for any
demand forecast, solar caution, battery size or tariff (see the dashboard section above).

## Assessments

| | Focus | Weight | Due | Status |
|---|---|---|---|---|
| A1 | Project Proposal and Design | 10% | 16 Aug 2026 | Submitted |
| A2 | Progress Report and Development | 20% | 13 Sep 2026 | Submitted |
| A3 | Group Technical Demonstration | 30% | 4 Oct 2026 | Submitted |
| A4 | Final Professional Report | 40% | 21 Oct 2026 (extended from 19 Oct) | Submitted |

## Contribution expectations

Recorded in the governance section of
[`Planning/Task_Allocation/task-allocation.md`](Planning/Task_Allocation/task-allocation.md): decision rights,
definition of done, branching, and data handling.

## Use of generative AI

Generative AI assisted with notebook code, report drafting and project administration during
Assessments 2, 3 and 4, and with the dashboard code in Assessment 4. Its use is disclosed in
full, including errors it introduced that the team found and corrected, in
[`Supporting_Documents/ethics-privacy-security.md`](Supporting_Documents/ethics-privacy-security.md).

## Licence and attribution

Data © Desert Knowledge Australia Solar Centre, used under their public data terms.
This repository is coursework submitted for assessment at Charles Darwin University.
CDU teaching materials are **not** redistributed here.
