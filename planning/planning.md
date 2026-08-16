# Project Planning

PRT661 Solar Generation Forecasting

Jira board: https://uttamshrestha1618.atlassian.net/jira/software/projects/SCRUM/boards/1

---

## Milestones

| Assessment | Focus | Weight | Week | Date |
|---|---|---|---|---|
| A1 | Project Proposal and Design | 10% | 3 | 16 Aug 2026 (extended from 9 Aug) |
| A2 | Progress Report and Development | 20% | 6 | Week of 24 Aug |
| A3 | Group Technical Demonstration | 30% | 9 | Week of 14 Sep |
| A4 | Final Professional Report | 40% | 12 | Week 12, 5–11 Oct 2026 — confirm exact date on Learnline |


Semester runs 20 July – 11 October 2026.

Week 1 = 20–26 July, so Week 3 = 3–9 Aug,
Week 6 = 24–30 Aug, Week 9 = 14–20 Sep and Week 12 = 5–11 Oct.

## Sprints

| Sprint | Covers | Start | End | Goal |
|---|---|---|---|---|
| Sprint 1 | A1 — Proposal and Design | 20 Jul | 16 Aug | Deliver the A1 proposal and design: repository, diagrams, populated board, report |
| Sprint 2 | A2: Progress and Development | 17 Aug | 30 Aug | Build the data pipeline and deliver the A2 progress report |
| Sprint 3 | A3: Demonstration | 31 Aug | 20 Sep | Train and evaluate models, build the dashboard, deliver the demonstration |
| Sprint 4 | A4: Final Report | 21 Sep | 11 Oct | Finalise the system and submit the final professional report |

## Epic schedule

| Epic | Start | Due | Accountable owner | Second member |
|---|---|---|---|---|
| Data Acquisition | 20 Jul | 16 Aug | Abhishek Tamang | |
| Data Storage | 3 Aug | 23 Aug | Abhishek Tamang | |
| Data Processing | 10 Aug | 30 Aug | Sarin Uprety | |
| Feature Engineering | 17 Aug | 6 Sep | Sarin Uprety | Uttam Shrestha |
| Analytics and Machine Learning | 24 Aug | 20 Sep | Yogesh Basnet | Uttam Shrestha |
| Visualisation | 7 Sep | 23 Sep | Yogesh Basnet | |
| Workflow Automation | 7 Sep | 23 Sep | Uttam Shrestha | |
| Governance and Monitoring | 20 Jul | 23 Sep | Uttam Shrestha | |

Accountable owners are set as the Jira assignee on each of the eight epics. Second members hold
named tasks inside an epic without taking accountability for it.

These eight names are used identically in the Jira board and in the Draw.io workflow diagram
(`../Workflow_Diagrams/02-workflow-plan.drawio`).

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
| 15 | Confirm AWS Academy access for all four members | Governance and Monitoring | To Do |
| 16 | Assemble and format A1 report | Governance and Monitoring | In Progress |

*Statuses verified against the Jira board on 12 August 2026.*

## Carried into Sprint 2

Raised by the architecture diagram review of 16 August 2026 and allocated to Sprint 2.

| Key | Task | Epic | Owner | Status |
|---|---|---|---|---|
| SCRUM-29 | Specify `bess_available` flag and BESS null handling in the feature table | Feature Engineering | Uttam Shrestha | To Do |
| SCRUM-30 | Add persistence baseline and prediction interval reporting to the evaluation protocol | Analytics and Machine Learning | Uttam Shrestha | To Do |

The board now holds 18 tasks, every one allocated to a sprint and assigned to a named member.

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
