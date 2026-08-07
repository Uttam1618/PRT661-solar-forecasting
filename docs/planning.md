# Project Planning

PRT661 Solar Generation Forecasting · Semester 2, 2026
Jira board: *link to be added*

---

## Milestones

| Assessment | Focus | Weight | Week | Date |
|---|---|---|---|---|
| A1 | Project Proposal and Design | 10% | 3 | 12 Aug 2026, 23:29 (extended from 9 Aug) |
| A2 | Progress Report and Development | 20% | 6 | Week of 24 Aug |
| A3 | Group Technical Demonstration | 30% | 9 | Week of 14 Sep |
| A4 | Final Professional Report | 40% | 12 | TBC — confirm on Learnline |

Semester runs 20 July – 23 September 2026. Week 1 = 20–26 July.

## Sprints

| Sprint | Covers | Start | End |
|---|---|---|---|
| Sprint 1 | A1 — Proposal and Design | 20 Jul | 12 Aug |
| Sprint 2 | A2 — Progress and Development | 13 Aug | 30 Aug |
| Sprint 3 | A3 — Demonstration | 31 Aug | 20 Sep |
| Sprint 4 | A4 — Final Report | 21 Sep | TBC |

## Epic schedule

| Epic | Start | Due | Primary owner |
|---|---|---|---|
| Data Acquisition | 20 Jul | 12 Aug | Data Engineer |
| Data Storage | 3 Aug | 23 Aug | Data Engineer |
| Data Processing | 10 Aug | 30 Aug | Data Engineer |
| Feature Engineering | 17 Aug | 6 Sep | Modelling Lead |
| Analytics and Machine Learning | 24 Aug | 20 Sep | Modelling Lead |
| Visualisation | 7 Sep | 23 Sep | Architecture and Design |
| Workflow Automation | 7 Sep | 23 Sep | Project Lead |
| Governance and Monitoring | 20 Jul | 23 Sep | Documentation and Governance |

These eight names are used identically in the Jira board and in the Draw.io workflow diagram
(`diagrams/02-workflow-plan.drawio`).

## Sprint 1 plan — A1

| # | Task | Epic | Status |
|---|---|---|---|
| 1 | Download DKASC yearly extracts 2008-2026 | Data Acquisition | Done |
| 2 | Verify required column groups exist in yearly files | Data Acquisition | Done |
| 3 | Re-download current data before A2 | Data Acquisition | Sprint 2 |
| 4 | Design raw, cleaned and feature storage layout | Data Storage | Done |
| 5 | Create Draw.io storage design diagram | Data Storage | Done |
| 6 | Document schema drift 197 to 210 columns | Data Processing | Done |
| 7 | Handle year-boundary duplicate rows | Data Processing | To Do |
| 8 | Define candidate feature set excluding wind speed | Feature Engineering | In Progress |
| 9 | Define walk-forward evaluation protocol | Analytics and Machine Learning | In Progress |
| 10 | Document baseline results from prior work as performance targets | Analytics and Machine Learning | In Progress |
| 11 | Draft dashboard concept | Visualisation | To Do |
| 12 | Define pipeline orchestration approach | Workflow Automation | To Do |
| 13 | Draft risk register | Governance and Monitoring | Done |
| 14 | Draft ethics, privacy and security section | Governance and Monitoring | Done |
| 15 | Confirm AWS Academy access for all five members | Governance and Monitoring | To Do |
| 16 | Assemble and format A1 report | Governance and Monitoring | In Progress |

*Update statuses to match the Jira board before submission.*

## Dependencies

- Feature Engineering cannot start until Data Processing has produced a clean table
- Analytics and Machine Learning depends on the feature table and the evaluation protocol
- Visualisation depends on model outputs existing
- Governance and Monitoring runs across the whole project

## Approach

Design proceeds backwards from the decision, per the unit's design principle:

```
Decision → Required insight → Data needed → Pipeline design → Tool selection → Evidence
```

The decision is **when the battery should charge or discharge**. Everything upstream exists to
serve it.
