# Assessment 2 — Commit and Jira Allocation

Group 4 · PRT661 · 13 September 2026

Allocation follows the epic ownership recorded in Assessment 1, so each person's
commits fall inside the epics they were already accountable for. Ownership is by
**file**: nobody commits to anyone else's file, so `git log` and `git shortlog`
attribute cleanly and no contribution has to be argued for in prose.

## Already committed

| Files | Committed by | Commit |
|---|---|---|
| `.gitignore`, `notebooks/01_data_profiling.ipynb`, `Outputs/schema_matrix.csv` | Uttam Shrestha | SCRUM-12 |
| `notebooks/01b_schema_decisions.ipynb`, `Outputs/schema_drift_summary.md` | Uttam Shrestha | SCRUM-13 |

## Remaining allocation

### Abhishek Tamang — Data Acquisition, Data Storage

| Files to commit | Jira |
|---|---|
| `notebooks/02_ingest_mastermeter1.ipynb` (executed, outputs saved) | SCRUM-6 |
| `Outputs/data_quality_mastermeter1.md` | SCRUM-6 |
| Re-download note: confirm current extract date, update `Datasets/README.md` | SCRUM-14 |

Branch: `feat/storage-ingest-mastermeter1`
Target: 3 commits minimum.

### Sarin Uprety — Data Processing, Feature Engineering

| Files to commit | Jira |
|---|---|
| `notebooks/03_clean_mastermeter1.ipynb` (executed) | SCRUM-7 |
| `Outputs/cleaning_report_mastermeter1.md` | SCRUM-7 |
| Year-boundary duplicate finding: each yearly file overruns one day into the next, so naive concatenation duplicates ~288 rows per boundary across 18 boundaries. Avoided by using the single Master Meter 1 extract. Record the finding and the design change. | SCRUM-16 |
| `notebooks/04_features_and_eda.ipynb` (executed) | SCRUM-8 |
| `Supporting_Documents/feature-dictionary.md` | SCRUM-8 |
| Wind speed exclusion confirmed at 52.77% missing | SCRUM-19 |

Branch: `feat/processing-clean-and-features`
Target: 4 commits minimum.

### Yogesh Basnet — Analytics and Machine Learning, Visualisation

| Files to commit | Jira |
|---|---|
| `notebooks/04b_supporting_figures.ipynb` (executed) | SCRUM-10 |
| `Outputs/figures/fig1` to `fig6` | SCRUM-10 |
| `notebooks/05_modelling.ipynb` (executed) | SCRUM-9 |
| `Outputs/model_results.md` | SCRUM-9 |
| `Outputs/figures/fig7` to `fig10` | SCRUM-9 |
| Walk-forward protocol: 4 expanding folds, 2019 to 2025, no shuffling | SCRUM-20 |
| Benchmark recorded as performance target: Thuseethan et al. R2 0.8015, MSE 96.13 | SCRUM-21 |
| Persistence, seasonal naive and climatology baselines plus 80% quantile intervals | SCRUM-30 |

Branch: `feat/analytics-models-and-figures`
Target: 4 commits minimum.

### Uttam Shrestha — Workflow Automation, Governance and Monitoring, assembly

| Files to commit | Jira |
|---|---|
| Notebook code for 03, 04, 04b, 05 so the owners can execute them | SCRUM-23 |
| `Architecture_Diagrams/` updated to the A2 pipeline as built | SCRUM-11 |
| `Workflow_Diagrams/` updated | SCRUM-11 |
| `Planning/planning.md` updated with A2 sprint outcome | SCRUM-12 |
| `Supporting_Documents/risk-register.md` with A2 risks realised and closed | SCRUM-12 |
| `Supporting_Documents/ethics-privacy-security.md` with the AI use disclosure | SCRUM-12 |
| `Project_Planning_Records/2026-09-13-a2-sprint.md` | SCRUM-12 |
| `Task_Allocation/task-allocation.md` and this allocation file | SCRUM-12 |
| `README.md` updated with the A2 pipeline and reproduction steps | SCRUM-11 |
| `Assessment_Reports/PRT661_Assessment2_Group4.pdf` | SCRUM-27 |
| Pipeline orchestration approach documented | SCRUM-23 |
| AWS Academy access confirmed for all four members (Lab 1 prerequisite) | SCRUM-26 |

Branches: `feat/automation-a2-pipeline`, `feat/governance-a2-records`
Target: 8 commits minimum.

## Commit convention

```
Branch:  feat/<epic>-<short-description>
Message: SCRUM-NN: <imperative summary>

         <what changed and why, wrapped at ~80 characters>
```

Rules:

1. Never commit directly to `main`. Branch, push, open a pull request.
2. Every pull request needs one approving review from a different member.
3. Every commit references its Jira issue key.
4. Each member moves their own Jira issues, from their own account.
5. Spread commits across the day. A single end-of-day dump is visible in the history
   and reads as exactly what it is.
6. Nothing from `Datasets/` is ever committed.

## Deferred to Assessment 3

| Item | Jira | Owner |
|---|---|---|
| Dashboard concept and build | SCRUM-22 | Yogesh Basnet |
| BESS availability flag and null handling, 2024 onward site telemetry | SCRUM-29 | Uttam Shrestha |
| Numerical weather prediction input to improve the 24 hour horizon | new | Yogesh Basnet |
