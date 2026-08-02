# Task Allocation and Team Structure

**Group 4 — four members.** The assessment brief specifies groups of five; confirmation has been
sought from the unit lecturer that a group of four is approved.

> **Status:** roles proposed, awaiting group confirmation. GitHub usernames still to be collected.

---

## Roles

| Role | Member | GitHub | Owns |
|---|---|---|---|
| Project Lead / PM | **Uttam Shrestha** | `Uttam1618` | Jira board, sprint plan, governance, timeline, report assembly |
| Data Engineer | **Abhishek Tamang** | *TBC* | Acquisition, storage design, ingestion pipeline |
| Data and Feature Engineer | **Sarin Uprety** | *TBC* | Cleaning, schema reconciliation, feature engineering |
| Modelling and Visualisation Lead | **Yogesh Basnet** | *TBC* | Models, evaluation protocol, dashboard, diagrams |

With four members rather than five, the Architecture and Design and Documentation and Governance
roles from the original five-person plan are distributed: diagram maintenance sits with the
Modelling and Visualisation Lead, and documentation and governance sits with the Project Lead.

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
`diagrams/02-workflow-plan.drawio`.

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

Drafts due **6 August**. Assembly, formatting and submission by the Project Lead on **8 August**.

Word totals per member: Uttam 280 plus assembly, Abhishek 240, Sarin 250, Yogesh 230.

## Contribution expectations

Recorded in full in [`../CONTRIBUTING.md`](../CONTRIBUTING.md). In summary, every member:

- makes regular visible commits to this repository
- owns named tasks in Jira with an owner, due date and status
- attends the weekly stand-up or posts an async update
- reviews at least one pull request per sprint

## Workload balance

Each member owns two epics, one to two report sections, and an independent evidence trail in both
GitHub and Jira. Where an epic spans multiple sprints the owner remains accountable but may
delegate individual tasks — recorded in Jira, not agreed verbally.

## Change history

Changes to roles or allocation are logged in [`../CHANGELOG.md`](../CHANGELOG.md) with a date and
a reason.
