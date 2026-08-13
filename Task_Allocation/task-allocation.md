# Task Allocation and Team Structure

**Group 4 — four members.** The assessment brief specifies groups of 3–5 students, so a group of
four is compliant.

> **Status:** roles confirmed 7 August 2026. All four members have access to the GitHub repository
> and the Jira board, and every Jira task is assigned to a named member.

---

## Roles

| Role | Member | GitHub | Owns |
|---|---|---|---|
| Project Lead / PM | **Uttam Shrestha** | `Uttam1618` | Jira board, sprint plan, governance, timeline, report assembly |
| Data Engineer | **Abhishek Tamang** | `Abhisek000` | Acquisition, storage design, ingestion pipeline |
| Data and Feature Engineer | **Sarin Uprety** | `Sarin751` | Cleaning, schema reconciliation, feature engineering |
| Modelling and Visualisation Lead | **Yogesh Basnet** | `viperx-ux` | Models, evaluation protocol, dashboard, diagrams |

Each member owns two epics spanning the pipeline order, with diagram maintenance sitting with the
Modelling and Visualisation Lead and documentation and governance with the Project Lead.

## Epic ownership

Two epics each, following the pipeline order.

| Epic | Owner |
|---|---|
| Data Acquisition | Abhishek Tamang |
| Data Storage | Abhishek Tamang |
| Data Processing | Sarin Uprety |
| Feature Engineering | Sarin Uprety |
| Analytics and Machine Learning | Yogesh Basnet |
| Visualisation | Yogesh Basnet |
| Workflow Automation | Uttam Shrestha |
| Governance and Monitoring | Uttam Shrestha |

These eight names are used identically in the Jira board and in
[`../Workflow_Diagrams/02-workflow-plan.drawio`](../Workflow_Diagrams/02-workflow-plan.drawio).

## A1 report sections by owner

| Section | Words | Owner |
|---|---|---|
| 1. Project overview and objectives | 120 | Abhishek Tamang |
| 2. Theme justification | 80 | Yogesh Basnet |
| 3. Problem statement | 120 | Abhishek Tamang |
| 4. Initial architecture diagram + caption | 100 | Sarin Uprety |
| 5. Workflow plan | 100 | Uttam Shrestha |
| 6. Task allocation and team structure | 80 | Uttam Shrestha |
| 7. Initial risk analysis | 150 | Sarin Uprety |
| 8. Ethics, privacy and security | 150 | Yogesh Basnet |
| 9. References | 100 | Uttam Shrestha |
| **Total** | **1000** | |

Drafts due **14 August**. Assembly and formatting by the Project Lead on **15 August**, with a
compliance pass and submission ahead of the deadline of **16 August**.

Word totals per member: Uttam 280 plus assembly, Abhishek 240, Sarin 250, Yogesh 230.

## Contribution expectations

Every member:

- makes regular visible commits to this repository
- owns named tasks in Jira with an owner, due date and status
- attends the weekly stand-up or posts an asynchronous update
- reviews at least one pull request per sprint
- records decisions in [`../Project_Planning_Records/`](../Project_Planning_Records/) rather than
  agreeing them verbally

## Governance

- **Decision rights** — technical decisions sit with the epic owner; scope and schedule decisions
  sit with the Project Lead after group discussion.
- **Definition of done** — work is complete when it is committed, its Jira task is moved to Done,
  and any affected documentation is updated in the same commit.
- **Branching** — work on `main` for documentation; feature branches for code from A2 onward.
- **Data handling** — no raw data, credentials or `.env` files are ever committed.

## Workload balance

Each member owns two epics, one to two report sections, and an independent evidence trail in both
GitHub and Jira. Where an epic spans multiple sprints the owner remains accountable but may
delegate individual tasks — recorded in Jira, not agreed verbally.

## Change history

Changes to roles or allocation are recorded in
[`../Project_Planning_Records/`](../Project_Planning_Records/), dated and with a stated reason.
