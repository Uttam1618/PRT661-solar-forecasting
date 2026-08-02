# PRT661 — Solar Generation Forecasting (DKASC Alice Springs)

Semester 2, 2026 · Charles Darwin University · Data Science Practice (PRT661)
**Theme 2 — Predictive Analytics and Forecasting**

---

## Project

Forecasting solar generation at the Desert Knowledge Australia Solar Centre (Alice Springs)
across 2008–2026, with degradation-aware features and explicit ramp-event handling, to support
**battery charge/discharge scheduling** using the 2024 BESS installation.

**The decision this supports:** when should the battery charge, and when should it discharge?

## Relationship to prior work

This project builds on and cites:

> Thuseethan, S., Gangajaliya, S., Hamlin, L., Shanmugam, B., & Thennadil, S. (2025).
> Conv-Ensemble for solar power prediction with First Nations seasonal information.
> *IEEE Open Journal of the Computer Society*, 6, 884–895.
> https://doi.org/10.1109/OJCS.2025.3580339

That paper uses the same site and task. We extend it in three ways:

| | Prior work | This project |
|---|---|---|
| Time span | 2019–2024 (465,078 rows) | 2008–2026 (~1.77M rows) |
| Battery | Not available (predates 2024 BESS install) | BESS state-of-charge and totals included |
| Open problem addressed | High error at peak irradiance and dawn/dusk; per-feature influence not analysed | Ramp-event handling and feature importance |

**Benchmark to beat** (their published results on this site):

| Meter | R² | MSE |
|---|---|---|
| Master Meter 1 | 0.8015 | 96.13 |
| Master Meter 2 | 0.8641 | 22.41 |

## Team — Group 4

| Role | Member | GitHub |
|---|---|---|
| Project Lead / PM | Uttam Shrestha | [@Uttam1618](https://github.com/Uttam1618) |
| Data Engineer | Abhishek Tamang | *TBC* |
| Data and Feature Engineer | Sarin Uprety | *TBC* |
| Modelling and Visualisation Lead | Yogesh Basnet | *TBC* |

Full allocation, epic ownership and report sections: [`docs/task-allocation.md`](docs/task-allocation.md)

## Project management

Jira board: *link to be added*

Workflow stages (these names are used identically in the Draw.io diagrams and as Jira epics):

1. Data Acquisition
2. Data Storage
3. Data Processing
4. Feature Engineering
5. Analytics and Machine Learning
6. Visualisation
7. Workflow Automation
8. Governance and Monitoring *(cross-cutting)*

## Repository structure

```
docs/        Assessment reports, data-quality summaries, planning records
data/        Local data directory — contents are NOT committed (see data/README.md)
diagrams/    Draw.io sources (.drawio) and exported PNGs
notebooks/   Exploratory analysis
src/         Reusable pipeline and modelling code
```

## Data

Source: [Desert Knowledge Australia Solar Centre](https://dkasolarcentre.com.au/download?location=alice-springs) — Alice Springs.

Raw data is **not committed to this repository** (individual files are 25–390 MB, exceeding
GitHub limits). See [`data/README.md`](data/README.md) for how to obtain it, and
[`docs/data-quality-summary.md`](docs/data-quality-summary.md) for what we know about it.

## Reproducing this work

*To be completed as the pipeline is built.*

```bash
# Planned
pip install -r requirements.txt
python src/build_dataset.py
```

## Assessments

| | Focus | Due | Status |
|---|---|---|---|
| A1 | Project Proposal and Design | Week 3 | In progress |
| A2 | Progress Report and Development | Week 6 | Not started |
| A3 | Group Technical Demonstration | Week 9 | Not started |
| A4 | Final Professional Report | Week 12 | Not started |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for branch strategy, review rules, and contribution
expectations.

## Licence and attribution

Data © Desert Knowledge Australia Solar Centre, used under their public data terms.
This repository is coursework submitted for assessment at Charles Darwin University.
CDU teaching materials are **not** redistributed here.
