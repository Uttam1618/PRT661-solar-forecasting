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
