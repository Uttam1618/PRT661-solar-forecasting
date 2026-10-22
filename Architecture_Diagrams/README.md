# Architecture and Design Diagrams

Every diagram is maintained as an editable `.drawio` source in [`drawio/`](drawio/) and an exported `.png` in [`png/`](png/).
Sources are edited at [app.diagrams.net](https://app.diagrams.net).

Diagrams are updated as the project evolves. Each change is recorded in the revision history below
and the updated version is included in both this repository and the relevant assessment report.

---

## Coverage against the assessment requirements

| Required artefact | File |
|---|---|
| High-level system architecture | `01-system-architecture` (A1 design), `07-system-architecture-a2`, `08-system-architecture-a3`, `09-system-architecture-a4` (as built) |
| Data pipeline architecture | `05-data-pipeline-architecture` |
| Database or data storage design | `03-data-storage-design` |
| Component interaction | `04-component-interaction` |
| Workflow diagram | [`../Workflow_Diagrams/02-workflow-plan`](../Workflow_Diagrams/) |
| Deployment architecture *(if applicable)* | `10-deployment-architecture` (A4), see below |

### Deployment architecture

Not produced for A1, A2 or A3, because nothing ran outside a laptop and the dashboard did not yet
exist, so a deployment diagram would have described an intention rather than a design.

Produced for **A4** as `10-deployment-architecture.png`. It shows how the notebook chain runs as a
nightly batch: ingest at 21:00, forecast at 21:15, health checks at 21:30, battery plan at 22:00 and
a demand model refit on the first of each month, with the data zones mapped onto S3, the Glue
catalog and Athena as practised in the AWS Data Engineering capstone. The operator approves the
plan; the Streamlit dashboard is read only.

## Which diagrams appear in which report

| Report | Figures included |
|---|---|
| A1 | System architecture, workflow plan |
| A2 | + data pipeline, data storage design |
| A3 | + component interaction, deployment |
| A4 | As built `09-system-architecture-a4` (Figure 1) and `10-deployment-architecture` (Figure 13) |

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
| 29 Sep 2026 | `08-system-architecture-a3` added: system as built at A3, with interval calibration, site and battery model, and dispatch simulation; built and planned parts marked | Abhisek Tamang |
| 18 Oct 2026 | `09-system-architecture-a4` added: system as built at A4 with demand forecasting, monitoring and retraining, and the decision support dashboard. `10-deployment-architecture` added: nightly batch schedule, data zones and operator approval. Both kept as editable `.drawio` sources with PNG exports at 200% zoom | Abhisek Tamang |
| 22 Oct 2026 | Sources moved into `drawio/` and PNG exports into `png/` | Uttam Shrestha |
