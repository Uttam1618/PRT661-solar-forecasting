# Planning Record — 1 August 2026

**Type:** Project setup
**Present:** *TBC*
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

## Open questions for the lecturer

1. Week 2 slide 12 states the group project must use open-source tools only, while slide 42
   refers to reflecting the existing AWS architecture. Which applies to A1?
2. Formatting requires a minimum 11-point font but also states all font sizes ≥ 10. Is 10 pt
   acceptable for figure and table captions?
3. Is workflow automation required for A1? It appears in the Week 1 slides but not in the A1
   instructions.

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Confirm the five roles and collect GitHub usernames | *TBC* | 3 Aug |
| 2 | Add all members to the repository and the Jira board | *TBC* | 3 Aug |
| 3 | Assign every Jira task to a named member | *TBC* | 3 Aug |
| 4 | Confirm AWS Academy access for all five members | *TBC* | 4 Aug |
| 5 | Email the lecturer the three open questions | *TBC* | 3 Aug |
| 6 | Export diagrams to PNG and commit alongside the sources | *TBC* | 4 Aug |
| 7 | Draft assigned report sections | All | 6 Aug |
| 8 | Assemble, format and submit the report | *TBC* | 8 Aug |

## Next meeting

*TBC — weekly cadence to be confirmed with the group.*
