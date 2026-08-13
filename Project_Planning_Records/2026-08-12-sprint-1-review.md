# Planning Record — 12 August 2026

**Type:** Sprint 1 review and A1 readiness check
**Group:** Group 4 — Uttam Shrestha, Abhishek Tamang, Sarin Uprety, Yogesh Basnet
**Sprint:** Sprint 1 (A1 — Proposal and Design)

---

## Decisions made

1. **Submission deadline extended to 16 August** — A1 moved again, from 12 August to 16 August.
   The internal schedule was rebaselined a second time: section drafts 14 August, assembly
   15 August, compliance pass and submission 16 August. Sprint 1 extends to 16 August and Sprint 2
   now begins 17 August.

2. **A4 window derived** — the unit outline places A4 in Week 12 without a calendar date. Counting
   from Week 1 (20–26 July), Week 12 is **5–11 October 2026**. This is consistent with A1 in
   Week 3, A2 in Week 6 and A3 in Week 9, all of which match their published dates. The exact
   date remains to be confirmed on Learnline.

3. **Repository restructured** — top-level folders now mirror the documentation artefacts named in
   the assessment instructions: `Assessment_Reports`, `Architecture_Diagrams`, `Workflow_Diagrams`,
   `Planning`, `Task_Allocation`, `Project_Planning_Records`. Supporting material that is not a
   named artefact was moved to `Supporting_Documents`. The rationale is that a marker should be
   able to locate each required artefact without searching.

4. **`CHANGELOG.md` and `CONTRIBUTING.md` removed** — neither is named in the assessment
   instructions. The scope-change history they recorded remains in the Git commit history and in
   these planning records.

5. **Data directory renamed** — `data/` became `Datasets/`, retaining the `raw/` and `reference/`
   split agreed on 7 August. `.gitignore` was updated so that no CSV is ever committed.

6. **Deployment architecture deferred to A3** — nothing is deployed at A1 and the brief marks this
   diagram "if applicable". A deployment diagram now would describe an intention rather than a
   design. Recorded as a deliberate deferral, not an omission.

7. **A2 scope reassessed** — A2 requires approximately 1,000 words per student (4,000–5,000 for
   the group) plus a one-page Individual Work and Contribution Summary each. This is materially
   larger than Sprint 2 currently assumes and will be re-planned at the Sprint 1 close.

## Work completed this sprint

| Area | Detail |
|---|---|
| Jira epics | 8 epics, each with start and due dates matching `Planning/planning.md` |
| Jira sprints | 4 sprints created with dates and sprint goals; Sprint 1 active |
| Jira tasks | 16 tasks, all allocated to a sprint, all assigned to a named member |
| Task status | 7 Done, 4 In Progress, 5 To Do — board and planning document reconciled |
| Team access | All four members on the GitHub repository and the Jira site |
| Repository | Restructured to match the required artefacts; documentation paths updated |

## Status of actions from 7 August

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Populate Jira epic dates, sprints and assignees | Uttam | Complete |
| 2 | Collect GitHub usernames and replace placeholders | Sarin | Outstanding |
| 3 | Confirm AWS Academy access for all four members | Abhishek | Outstanding |
| 4 | Email the lecturer the outstanding questions | Yogesh | Outstanding |
| 5 | Draft assigned report sections | All | In progress |
| 6 | Assemble, format and submit the report | Uttam | In progress — now due 16 Aug |

## Actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Draft assigned report sections | All | 14 Aug |
| 2 | Collect GitHub usernames and replace remaining placeholders | Sarin | 14 Aug |
| 3 | Verify every documentation link resolves after the restructure | Sarin | 14 Aug |
| 4 | Email the lecturer the outstanding formatting and scope questions | Yogesh | 14 Aug |
| 5 | Re-export any diagram revised during drafting | Yogesh | 15 Aug |
| 6 | Confirm AWS Academy access for all four members | Abhishek | 15 Aug |
| 7 | Assemble, format and submit A1 as searchable PDF | Uttam | 16 Aug |
| 8 | Commit the submitted PDF to `Assessment_Reports/` | Uttam | 16 Aug |
| 9 | Close Sprint 1, re-plan and start Sprint 2 | Uttam | 17 Aug |
| 10 | Re-download DKASC data and record the download date | Abhishek | Sprint 2 |

## Risks noted

- **Section drafts are behind schedule.** Mitigation: the extension to 16 August restores the
  buffer, and the Project Lead assembles from a complete first draft so remaining time is spent
  revising rather than writing.
- **A2 is substantially larger than Sprint 2 currently assumes.** Sprint 2 planning is to be
  revised at the Sprint 1 close rather than carried over unchanged.

## Next meeting

17 August 2026 — Sprint 1 close and Sprint 2 re-planning.
