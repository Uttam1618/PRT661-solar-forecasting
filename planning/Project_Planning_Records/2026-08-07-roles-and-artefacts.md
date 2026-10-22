# Planning Record — 7 August 2026

**Type:** Role confirmation and artefact review
**Group:** Group 4 — Uttam Shrestha, Abhishek Tamang, Sarin Uprety, Yogesh Basnet
**Sprint:** Sprint 1 (A1 — Proposal and Design)

---

## Decisions made

1. **Group membership confirmed at four** — Uttam Shrestha, Abhishek Tamang, Sarin Uprety and
   Yogesh Basnet. The A1 brief specifies "3–5 students per group", so a group of four is compliant
   and no approval is required. The question raised on 1 August is closed.

2. **Roles agreed** — each member owns two epics and one to two report sections, giving every
   member an independent evidence trail in both GitHub and Jira.

   | Member | Role | Epics owned |
   |---|---|---|
   | Uttam Shrestha | Project Lead / PM | Workflow Automation, Governance and Monitoring |
   | Abhishek Tamang | Data Engineer | Data Acquisition, Data Storage |
   | Sarin Uprety | Data and Feature Engineer | Data Processing, Feature Engineering |
   | Yogesh Basnet | Modelling and Visualisation Lead | Analytics and Machine Learning, Visualisation |

3. **Data pipeline architecture separated from system architecture** — the assessment lists these
   as distinct artefacts. Diagram 01 shows the whole system including governance and the decision
   it serves; diagram 05 shows the data layers with formats, volumes and cadence.

4. **Submission deadline extended** — A1 moved from 9 August to 12 August. The internal schedule
   was rebaselined: section drafts 10 August, assembly 11 August, submission 12 August. Sprint 1
   extended to 12 August and Sprint 2 moved to begin 13 August.

5. **Raw data reorganised** — the 19 yearly extracts moved to `raw/` and the MasterMeter1
   cross-check file to `reference/`, so that the directory layout matches the documented storage
   design and the reference file cannot be mistaken for a modelling source.

## Work completed

| Area | Detail |
|---|---|
| Architecture diagrams | System architecture, data storage design, component interaction, data pipeline architecture — Draw.io sources committed |
| Workflow diagram | Workflow plan — Draw.io source committed |
| Diagram exports | All five diagrams exported to PNG at 200% zoom and committed alongside their sources |
| Documentation | Risk register (18 risks), ethics/privacy/security, data quality summary, planning, task allocation |
| Repository | Structure, README and `.gitignore` in place; teammates added as collaborators |

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Populate Jira epic dates, sprints and assignees | Uttam | 12 Aug |
| 2 | Collect GitHub usernames and replace placeholders | Sarin | 12 Aug |
| 3 | Confirm AWS Academy access for all four members | Abhishek | 12 Aug |
| 4 | Email the lecturer the outstanding formatting and scope questions | Yogesh | 12 Aug |
| 5 | Draft assigned report sections | All | 10 Aug |
| 6 | Assemble, format and submit the report | Uttam | 12 Aug |

## Next meeting

12 August 2026 — Sprint 1 review and A1 readiness check.
