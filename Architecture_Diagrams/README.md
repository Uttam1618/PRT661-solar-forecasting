# Architecture and Design Diagrams

Every diagram is maintained as an editable `.drawio` source and an exported `.png`.
Sources are edited at [app.diagrams.net](https://app.diagrams.net).

Diagrams are updated as the project evolves. Each change is recorded in the revision history below
and the updated version is included in both this repository and the relevant assessment report.

---

## Coverage against the assessment requirements

| Required artefact | File |
|---|---|
| High-level system architecture | `01-system-architecture` |
| Data pipeline architecture | `05-data-pipeline-architecture` |
| Database or data storage design | `03-data-storage-design` |
| Component interaction | `04-component-interaction` |
| Workflow diagram | [`../Workflow_Diagrams/02-workflow-plan`](../Workflow_Diagrams/) |
| Deployment architecture *(if applicable)* | Deferred to A3 — see below |

### Deployment architecture

Not produced for A1. At this stage nothing is deployed — the pipeline runs locally and the
dashboard does not yet exist — so a deployment diagram would describe an intention rather than a
design. The brief marks this artefact *"if applicable"*.

It will be produced for **A3**, once the dashboard and scheduled pipeline exist and there is a
real execution environment to describe.

## Which diagrams appear in which report

| Report | Figures included |
|---|---|
| A1 | System architecture, workflow plan |
| A2 | + data pipeline, data storage design |
| A3 | + component interaction, deployment |
| A4 | All, updated to as-built |

The 1000-word limit on A1 does not allow more than two figures; the remaining diagrams are
referenced by repository link.

## Naming contract

The eight stage names below appear **identically** as boxes in the workflow diagram and as epics
in the Jira board. Do not rename one without renaming the other.

```
Data Acquisition
Data Storage
Data Processing
Feature Engineering
Analytics and Machine Learning
Visualisation
Workflow Automation
Governance and Monitoring
```

## Revision history

| Date | Change | Author |
|---|---|---|
| 1 Aug 2026 | Initial set created for A1 — system architecture, workflow plan, storage design, component interaction | Uttam Shrestha |
| 7 Aug 2026 | Data pipeline architecture added as a separate diagram; all five exported to PNG at 200% zoom | Uttam Shrestha |
| 12 Aug 2026 | Diagrams reorganised into `Architecture_Diagrams/` and `Workflow_Diagrams/`; duplicated `.drawio.png` extensions corrected | Uttam Shrestha |
