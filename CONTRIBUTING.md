# Contributing — Team Charter

This document records our **contribution expectations** and **project governance approach**.
It is referenced in Assessment 1 and updated as the project evolves.

---

## Contribution expectations

Every member is expected to:

- Make **regular, visible commits** to this repository — not one large commit at the end
- Own **named tasks in Jira** with an owner, due date and status
- Attend the weekly stand-up, or post an async update if unable to attend
- Review at least one other member's pull request per sprint
- Raise blockers early rather than at the deadline

Assessment 1 allocates 20% to collaboration evidence, assessed on what is **visible** in this
repository and the Jira board.

## Roles

| Role | Member | Owns |
|---|---|---|
| Project Lead / PM | *TBC* | Jira board, sprint plan, governance, timeline |
| Data Engineer | *TBC* | Acquisition, cleaning pipeline, storage design |
| Modelling Lead | *TBC* | Model plan, baselines, evaluation protocol |
| Architecture & Design | *TBC* | All Draw.io artefacts |
| Documentation & Governance | *TBC* | Report assembly, risk register, ethics, references |

## Governance

| Area | Approach |
|---|---|
| Meeting cadence | Weekly stand-up (fixed day/time) + async updates in group chat |
| Decision rights | Technical decisions by Modelling Lead; scope changes by group majority; PM breaks ties |
| Definition of done | Reviewed by one other member, merged to `main`, Jira task closed with an evidence link |
| Escalation | Blockers raised at stand-up; unresolved issues escalated to the unit lecturer |

## Branch strategy

- `main` is protected — **no direct pushes**
- Work on a feature branch named `<initials>/<short-description>`, e.g. `us/data-cleaning`
- Open a pull request; **one approval required** before merge
- Keep pull requests small enough to review in under 15 minutes

```bash
git checkout main
git pull
git checkout -b us/data-cleaning
# ... make changes ...
git add .
git commit -m "Add year-boundary deduplication to ingestion"
git push -u origin us/data-cleaning
# then open a pull request on GitHub
```

## Commit messages

Write in the imperative, describing what the commit does:

- Good — `Add schema reconciliation for 2024+ BESS columns`
- Poor — `updates`, `fix`, `asdf`

## Data handling rules

- **Raw data is immutable.** Never edit a downloaded file in place.
- All cleaning must be **scripted** in `src/` so outputs are regenerable.
- Do not commit data files — see `.gitignore`.

## Security rules

**Never commit** AWS credentials, API keys, access tokens, private keys, or screenshots
containing secrets — to this repository, to assessment reports, or into AI tools.

If a credential is committed by mistake: rotate it immediately, then tell the team. Removing
the file in a later commit does **not** remove it from history.

## Scope changes

Log every scope change in `CHANGELOG.md` with the date, the reason and who approved it.
Changes are permitted when justified and documented.
