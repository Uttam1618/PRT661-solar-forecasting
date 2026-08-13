# PRT661 — Solar Generation Forecasting (DKASC Alice Springs)

Semester 2, 2026 · Charles Darwin University · Data Science Practice (PRT661)
**Theme 2: Predictive Analytics and Forecasting**

---

## Project

Forecasting solar generation at the Desert Knowledge Australia Solar Centre (Alice Springs)
across 2008–2026, with degradation-aware features and explicit ramp-event handling, to support
**battery charge/discharge scheduling** using the 2024 BESS installation.

**The decision this supports:** when should the battery charge, and when should it discharge?

Everything upstream — acquisition, storage, processing, features, models, dashboard — exists to
serve that decision.

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
[`Task_Allocation/task-allocation.md`](Task_Allocation/task-allocation.md)

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
Assessment_Reports/         A1-A4 submissions as PDF
Architecture_Diagrams/      Four architecture diagrams, sources and PNG exports
Workflow_Diagrams/          Workflow plan, source and PNG export
Planning/                   Milestones, sprints, epic schedule, sprint plans
Task_Allocation/            Roles, epic ownership, report sections, governance
Project_Planning_Records/   Dated meeting and decision records
Supporting_Documents/       Risk register, ethics and privacy, data quality
Datasets/                   Local data directory, contents are NOT committed
```

## Data

Source: [Desert Knowledge Australia Solar Centre](https://dkasolarcentre.com.au/download?location=alice-springs) — Alice Springs.

Raw data is **not committed to this repository** (individual files are 25–390 MB, exceeding
GitHub limits). See [`Datasets/README.md`](Datasets/README.md) for the directory layout, and
[`Supporting_Documents/data-quality-summary.md`](Supporting_Documents/data-quality-summary.md)
for row counts, coverage, schema drift and measured missingness.

## Reproducing this work

*To be completed as the pipeline is built in A2.*

## Assessments

| | Focus | Weight | Due | Status |
|---|---|---|---|---|
| A1 | Project Proposal and Design | 10% | 16 Aug 2026 | In progress |
| A2 | Progress Report and Development | 20% | Week 6 | Not started |
| A3 | Group Technical Demonstration | 30% | Week 9 | Not started |
| A4 | Final Professional Report | 40% | Week 12 | Not started |

## Contribution expectations

Recorded in the governance section of
[`Task_Allocation/task-allocation.md`](Task_Allocation/task-allocation.md): decision rights,
definition of done, branching, and data handling.

## Licence and attribution

Data © Desert Knowledge Australia Solar Centre, used under their public data terms.
This repository is coursework submitted for assessment at Charles Darwin University.
CDU teaching materials are **not** redistributed here.
