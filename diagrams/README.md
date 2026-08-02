# Architecture and Design Artefacts

Every diagram is maintained as an editable `.drawio` source **and** an exported `.png`.
Sources are edited at [app.diagrams.net](https://app.diagrams.net).

Diagrams are updated as the project evolves. Each revision is recorded below and the updated
version is included in both this repository and the relevant assessment report.

---

## Coverage against the assessment requirements

| Required artefact | File | Status |
|---|---|---|
| High-level system architecture | `01-system-architecture.drawio` | v1.0 |
| Data pipeline architecture | `05-data-pipeline-architecture.drawio` | v1.0 |
| Workflow diagram | `02-workflow-plan.drawio` | v1.0 |
| Database or data storage design | `03-data-storage-design.drawio` | v1.0 |
| Component interaction diagram | `04-component-interaction.drawio` | v1.0 |
| Deployment architecture *(if applicable)* | — | Deferred, see below |

### Deployment architecture

Not produced for A1. At this stage nothing is deployed — the pipeline runs locally and the
dashboard does not yet exist, so a deployment diagram would describe an intention rather than a
design. The brief marks this artefact *"if applicable"*.

It will be produced for **A3**, once the Streamlit dashboard and scheduled pipeline exist and
there is a real execution environment to describe.

## Which diagrams appear in which report

| Report | Figures included | Rationale |
|---|---|---|
| A1 | Fig. 1 — system architecture · Fig. 2 — workflow plan | The 1000-word limit does not allow more; the remaining diagrams are referenced by repository link |
| A2 | + data pipeline, data storage design | Implementation begins, so pipeline detail becomes relevant |
| A3 | + component interaction, deployment | Demonstration requires the runtime view |
| A4 | All, updated to as-built | Final report documents the delivered system |

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

## Export procedure

1. Open the `.drawio` file at [app.diagrams.net](https://app.diagrams.net)
2. **File → Export as → PNG**
3. Zoom 200%, transparent background off, border width 10
4. Save into this folder using the same base name
5. Commit both the source and the PNG

## Revision history

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 1 Aug 2026 | Initial set created for A1 — system architecture, workflow plan, storage design, component interaction, data pipeline | *TBC* |
