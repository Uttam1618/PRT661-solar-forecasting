# Planning Record — 1 August 2026

**Type:** Project setup
**Group:** Group 4 — Uttam Shrestha, Abhishek Tamang, Sarin Uprety, Yogesh Basnet
**Sprint:** Sprint 1 (A1 — Proposal and Design)

---

## Decisions made

1. **Theme confirmed** — Theme 2, Predictive Analytics and Forecasting.

2. **Project framing agreed** — forecasting DKASC Alice Springs generation across 2008–2026 with
   degradation-aware features and ramp-event handling, to support battery dispatch scheduling.

3. **Prior work identified** — Thuseethan et al. (2025) uses the same site and task. It will be
   cited as prior work, not reproduced. We differ in three ways: a 17-year span versus their
   2019–2024, inclusion of post-2024 BESS data they did not have, and explicit treatment of
   ramp events, which their paper lists as an open problem.

4. **Primary data source changed** — from the 17-column MasterMeter1 extract to the yearly
   extracts. The slim file lacks BESS columns and ends 23 August 2025, so it cannot support the
   battery dispatch framing.

5. **Wind speed excluded** from the candidate feature set — 52.4% missing in source data, and
   also excluded by the prior work on this site.

6. **Per-inverter channels declared out of scope** — per-array analysis is anomaly detection
   (Theme 3), not forecasting.

## Infrastructure established

| Item | Status |
|---|---|
| GitHub repository | Created, public, structure and documentation committed |
| Jira board | Created, 8 epics matching the workflow diagram, 16 Sprint 1 tasks |
| Draw.io diagrams | System architecture, workflow plan, storage design, component interaction |
| Data quality assessment | Completed and committed to `docs/data-quality-summary.md` |


## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Confirm proposed roles and collect GitHub usernames | Uttam | 3 Aug |
| 2 | Add all members to the repository and the Jira board | Uttam | 3 Aug |
| 3 | Assign every Jira task to a named member | Abhishek| 3 Aug |
| 4 | Confirm AWS Academy access for all members | All | 4 Aug |
| 5 | Export diagrams to PNG and commit alongside the sources | Yogesh | 4 Aug |
| 7 | Draft assigned report sections | Sarin | 6 Aug |
| 8 | Assemble, format and submit the report | Uttam | 8 Aug |

## Next meeting

7 August 2026
