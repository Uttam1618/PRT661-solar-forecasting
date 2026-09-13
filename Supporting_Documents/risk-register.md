# Initial Risk Register

PRT661 Solar Generation Forecasting · Assessment 1

Likelihood and impact rated Low / Medium / High. Reviewed at each weekly stand-up and updated
before every assessment submission.

---

## Technical and data risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| T1 | Schema drift — files carry 197 columns to 2023 and 210 from 2024, so naive concatenation misaligns columns | High | Medium | Explicit reconciliation step; the 13 BESS/Totals columns treated as available from 2024 only and flagged as such in the feature table | Sarin Uprety |
| T2 | Duplicate rows at year-file boundaries — each yearly file overlaps the next by one day | High | Low | Deduplicate on timestamp during ingestion; assert uniqueness as a pipeline test | Abhishek Tamang |
| T3 | Cumulative counter misread as interval energy — `Active_Energy_Delivered_Received` is an odometer, not a per-interval value | Medium | High | Difference the series during processing; unit-test that differenced values are non-negative | Sarin Uprety |
| T4 | High missingness in several columns — wind speed 52%, tilted radiation ~35%, power factor and THD 41% | Certain | Medium | Wind speed excluded from the feature set; remaining gaps imputed or flagged, with the decision recorded in the planning records | Uttam Shrestha |
| T5 | Stale data — the 2026 extract ends 11 February 2026 | High | Medium | Re-download before A2 and record the download date; A1 states the coverage honestly | Abhishek Tamang |
| T6 | Limited BESS history — the battery was installed in 2024, so only ~2 years of dispatch-relevant data exists | High | Medium | Scope battery analysis to 2024 onward; use the full 2008–2026 span for generation forecasting | Uttam Shrestha |
| T7 | Model underperforms the published benchmark (R² 0.8641 on Meter 2) | Medium | Medium | Reproduce the baseline before extending; report results honestly either way, since a negative result with sound method still satisfies the learning outcomes | Yogesh Basnet |
| T8 | Overfitting through inappropriate validation — a random train/test split leaks future information in a time series | Medium | High | Walk-forward / rolling-origin validation only; no random shuffling at any point | Yogesh Basnet |

## Project and team risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| P1 | Uneven contribution across the group | Medium | High | Jira task ownership with named assignees; weekly stand-up; Project Lead escalates to the unit lecturer early rather than at submission | Uttam Shrestha |
| P2 | Scope creep into anomaly detection — per-inverter analysis belongs to Theme 3 | Medium | Medium | Scope locked to forecasting; per-array channels explicitly out of scope and recorded in the planning records | Uttam Shrestha |
| P3 | Evidence reconstructed at the end rather than accumulated | Medium | High | Commits and Jira updates made as work happens; weekly planning records committed to the repository | All members |
| P4 | Member unavailable through illness or competing deadlines | Medium | Medium | Every epic has a named owner and one other member familiar with it; work merged to `main` weekly so nothing sits only on one laptop | Uttam Shrestha |
| P5 | Deliverable fails formatting requirements — word count, searchable PDF, live links | Medium | High | Compliance pass scheduled two days before submission, not on the deadline | Uttam Shrestha |
| P6 | Schedule slippage — section drafts ran late against the internal 10 August deadline | High | Medium | Deadline extended to 16 August, restoring buffer; Project Lead assembles a complete first draft so remaining time is spent revising rather than writing | Uttam Shrestha |

## Governance and security risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| G1 | Credentials committed to a public repository | Low | High | `.gitignore` excludes `.env`, keys and credential files; the governance section of [`../Task_Allocation/task-allocation.md`](../Task_Allocation/task-allocation.md) forbids pasting AWS credentials into reports, repositories or AI tools; any exposed credential is rotated immediately | All members |
| G2 | Data licensing or attribution breach | Low | Medium | DKASC attribution recorded in the README and in `Datasets/README.md`; raw data excluded from version control | Uttam Shrestha |
| G3 | Course materials redistributed publicly | Low | Medium | CDU lecture slides excluded via `.gitignore` and stored outside the repository | Uttam Shrestha |
| G4 | Model risk — an inaccurate forecast drives a poor dispatch decision | Medium | Medium | Forecast intervals reported alongside point estimates; known weak periods (dawn, dusk, peak irradiance) documented as limitations rather than hidden | Yogesh Basnet |
| G5 | Irreproducible results | Medium | Medium | Raw data immutable; all transformations scripted and version-controlled; environment pinned in a requirements file | Abhishek Tamang |

## Review

| Date | Reviewed by | Changes |
|---|---|---|
| 1 Aug 2026 | Uttam Shrestha | Initial register created |
| 12 Aug 2026 | Uttam Shrestha | Reviewed before A1 submission. Owners changed from role titles to named members to match Jira assignees, with technical and data risks distributed two per member. References to the removed changelog and team charter redirected to the planning records and task allocation document. P6 added, schedule slippage against the internal draft deadline. |

---

# Assessment 2 review — 13 September 2026

Every risk below was reviewed against measured evidence from the A2 pipeline. Outcomes cite the
notebook or output file that substantiates them.

## Risks realised during Assessment 2

| # | Original assessment | What actually happened | Status |
|---|---|---|---|
| T1 | Schema drift, 197 columns to 2023 and 210 from 2024 | **Materially worse than assessed.** Profiling all 19 extracts found **406 distinct column names**, of which only 14 appear in every year and 3 of those are empty, leaving **11 populated columns** with unbroken coverage. The 392 drifting columns are inverters commissioned and decommissioned across seventeen years. Mitigated by selecting a single stable extract rather than reconciling nineteen schemas. Evidence: `Outputs/schema_drift_summary.md` | Realised, mitigated |
| T2 | Duplicate rows at year-file boundaries | **Confirmed.** Each yearly file overruns one day into the next; 2015 covers 1 Jan 2015 to 1 Jan 2016 23:55, exactly 366 days at 288 readings. Naive concatenation would duplicate ~288 rows at each of 18 boundaries. **Resolved by design change** rather than by deduplication: the single Master Meter 1 extract is used instead. Evidence: SCRUM-16 | Realised, closed by design change |
| T3 | Cumulative counter misread as interval energy; mitigation was "difference and unit-test that differenced values are non-negative" | **The mitigation as written would have failed.** The register is a **six digit counter that wraps at 1,000,000**, so differencing produces values near minus one million at each wrap, and a non-negativity test would have rejected valid data. Six wraps corrected by adding 1,000,000 back. Repair validated independently: 6,467,319 kWh from the register against 6,488,854 kWh integrated from Active Power, **agreement 99.7%**. Evidence: `notebooks/03_clean_mastermeter1.ipynb` | Realised, closed |
| T4 | High missingness: wind speed 52%, tilted radiation ~35% | **Realised exactly as forecast.** Measured at 52.77% and 34% to 37%. Wind speed excluded as planned; the remaining columns excluded on the same documented threshold of 30%. Evidence: `Outputs/data_quality_mastermeter1.md` | Realised, mitigated |
| T5 | Stale data, the 2026 extract ends 11 February 2026 | **Confirmed, and worse than assessed.** The primary dataset, Master Meter 1, ends **23 August 2025**, six months staler than the yearly extracts. Re-download carried into the current sprint. | Realised, **still open** |
| T6 | Limited BESS history | **Confirmed and reframed as an opportunity.** The 13 columns appearing at 2024 are the full site telemetry: BESS active, reactive and apparent power plus state of charge, and PV, grid and site demand totals. Surplus and battery headroom are therefore directly measurable from 2024, making the dispatch layer buildable in A3. | Realised, scoped to A3 |
| T7 | Model underperforms the published benchmark | **Not realised, but the comparison is not like for like.** Reported R2 exceeds the published figure at both horizons, however the published work solves a contemporaneous mapping in which irradiance at the predicted instant is an input, while this project forecasts ahead with no future weather. Parity conditions are stated explicitly in the report rather than the favourable number being claimed. | Not realised; caveated |
| T8 | Overfitting through inappropriate validation | **Mitigated as planned.** Four expanding-window walk forward folds, no shuffling at any point, every lag and rolling feature backward shifted. | Mitigated |
| P1 | Uneven contribution across the group | **Realised in Assessment 1.** An individual contribution deduction was applied to three members because no verifiable GitHub contribution could be identified. Mitigated for A2 by file-level ownership, per-member Jira assignment, and a documented commit allocation, so contribution is verifiable from `git log` rather than asserted in prose. Evidence: `Task_Allocation/a2-commit-allocation.md` | Realised, mitigation in place |
| P3 | Evidence reconstructed at the end rather than accumulated | **Realised.** Sprint 1 was left open for a month past its end date and Sprint 2, though planned in August with the correct goal, was not started until the delivery date. The work was compressed into a single intensive sprint. Recorded as a process failure rather than presented as paced delivery. | Realised, **open** |
| P6 | Schedule slippage | **Realised again**, more severely than in A1. See P3. | Realised, **open** |
| G4 | Inaccurate forecast drives a poor dispatch decision | **Partly mitigated.** Prediction intervals are reported alongside every point forecast and weak periods are documented. However the 24 hour interval is overconfident (see G6). | Partly mitigated |
| G5 | Irreproducible results | **Mitigated.** All ten figures and every reported number regenerate from committed notebooks 01 to 05 run in order. | Mitigated |

## New risks identified during Assessment 2

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| T9 | Cleaning applied after aggregation, allowing sentinel values into hourly means | Realised | High | Cleaning now runs at 5 minute resolution and the hourly store is rebuilt afterwards. Detected because an air temperature of -39.988 C survived into the hourly store. | Sarin Uprety |
| T10 | Training loss mismatched to the reported evaluation metric | Realised | High | The model must be trained with the loss it is judged on. Squared error training reported on MAE produced negative skill at 24 hours and an apparently unstable fold; absolute error loss reversed both. Closed. | Yogesh Basnet |
| T11 | An instrument-derived cleaning rule applied to a cumulative counter destroys the counter | Realised | High | Sentinel removal now exempts the register, which is diagnosed separately. Detected because the column went from 2.34% to 98.59% missing. Closed. | Sarin Uprety |
| G6 | Prediction intervals overconfident at the 24 hour horizon | Certain | Medium | Daylight coverage 0.706 against a nominal 0.80, failing the project's own quality gate. Published with an explicit warning rather than withdrawn, since the point forecast is unaffected. Recalibration scheduled for A3. | Yogesh Basnet |
| G7 | A statistic computed on a filtered index is silently mislabelled | Realised | Medium | An autocorrelation was computed by position within a daylight-only series, so the axis labelled hours was not hours. Any statistic over a filtered series must state what one unit of the index represents. Closed. | Yogesh Basnet |

## Review

| Date | Reviewed by | Changes |
|---|---|---|
| 13 Sep 2026 | Uttam Shrestha | Assessment 2 review. Thirteen A1 risks assessed against measured evidence: T3's stated mitigation would itself have failed and is documented; T1 and T5 were worse than assessed; T4 and T8 played out as planned; T2 closed by a design change. P1, P3 and P6 realised and remain open. Five new risks added: T9, T10, T11, G6 and G7, four of which were realised and closed during development. G6 remains open and fails a stated quality gate. |
