# Ethics, Privacy and Security Considerations

PRT661 Solar Generation Forecasting · Assessment 1

---

## 1. Privacy

The DKASC dataset contains **no personal information**. It consists of electrical measurements
from a demonstration solar facility and meteorological readings from a co-located weather station.
No individuals are identified or identifiable, and no consent or de-identification process is
required.

This is worth stating explicitly rather than omitting. The absence of personal data removes the
usual privacy obligations but does not remove the other duties set out below.

One indirect consideration: site-level generation and demand data can reveal operational patterns
of a facility. For a public demonstration site published under open terms this is not sensitive,
but the same pipeline applied to a private operator's data would require access controls. The
architecture separates raw, cleaned and feature zones partly so that such controls could be
applied per zone without redesign.

## 2. Data licensing and attribution

Data is sourced from the Desert Knowledge Australia Solar Centre and published for public use.
Our obligations:

- attribute DKASC as the source in the repository, in all reports, and in any dashboard
- record the source URL and download date so results are traceable to a specific extract
- not redistribute the raw data through this repository — it is excluded via `.gitignore`, both
  because of file size and because redistribution is not ours to authorise

CDU teaching materials carry an explicit copyright notice against further reproduction. Lecture
slides are therefore stored outside the repository and excluded in `.gitignore`.

## 3. Cultural considerations

Prior work on this site incorporated seasonal knowledge from the Tiwi, Gulumoerrgin, Kunwinjku
and Ngurrungurrudjba calendars. We have chosen **not** to build on that approach, for two reasons.

First, it is the substantive contribution of Thuseethan et al. (2025) and reproducing it would
add nothing. Second, Indigenous seasonal knowledge is cultural intellectual property held by
Traditional Owners. Using it appropriately requires engagement with the communities concerned,
which is outside the scope and timeframe of this unit. Applying such knowledge casually, without
consultation, risks appropriation even where the intent is respectful.

We note that the prior work itself acknowledges applying calendars from the Top End to a Central
Australian site, justified on grounds of geographical similarity. Its own ablation study found
the Ngurrungurrudjba calendar most predictive, which the authors attribute to it being the
closest region — a result that supports treating locality as material rather than incidental.

Where our work touches this ground at all, we cite the source and do not claim the knowledge as
our own.

## 4. Model risk and responsible use

The forecast is intended to inform battery charge and discharge scheduling. A poor forecast
therefore has an operational cost, not merely a statistical one.

Mitigations:

- report prediction intervals alongside point forecasts, so a user can see when the model is
  uncertain rather than acting on a single number
- document known weak periods openly — prior work on this site records elevated error at dawn,
  dusk and peak irradiance, and we expect the same
- present the system as decision **support**, never as automated control
- report results honestly, including where our approach fails to beat the published baseline

Forecasting solar generation carries no meaningful risk of discriminatory outcome, as the model
operates on physical measurements rather than data about people. The relevant responsible-AI
concern here is calibration and honest communication of uncertainty.

## 5. Security

| Area | Control |
|---|---|
| Credentials | Never committed. `.gitignore` excludes `.env`, `*.pem`, `*.key` and credential files. AWS credentials, API keys and tokens are never pasted into reports, the repository, or AI tools. |
| Exposure response | A committed credential is rotated immediately and reported to the team. Deleting the file in a later commit does not remove it from history. |
| Repository access | Public repository containing no sensitive material. Write access limited to the four group members. `main` is protected; changes arrive by reviewed pull request. |
| Lab evidence | AWS Academy screenshots are checked for visible account identifiers or session tokens before being committed. |
| Data integrity | Raw data is immutable. All transformations are scripted, so any output can be regenerated and verified against source. |

## 6. Academic integrity

Prior work on this dataset — including our unit lecturer's published paper — is cited explicitly
rather than absorbed silently. Where generative AI tools assist with drafting or code, their use
is acknowledged in accordance with CDU policy, and all technical decisions recorded in this
repository are ones the group can explain and defend.

---

## 7. Use of generative AI in Assessment 2

Section 6 commits this group to acknowledging generative AI use in accordance with CDU policy.
This section discharges that commitment for Assessment 2.

Generative AI (Claude, Anthropic) was used substantially during Assessment 2. Its use is set out
below in full rather than summarised, so that a reader can judge exactly where the boundary
between machine assistance and team work falls.

| Where used | Nature of the assistance | What the team did |
|---|---|---|
| Notebook code | Drafting the profiling, ingestion, cleaning, feature engineering, figure and modelling notebooks, including plotting code | Specified the requirements, executed every notebook, inspected all output, and identified and corrected errors in the generated code |
| Error identification | Reviewing printed output and flagging inconsistencies against expectations | Ran the checks and made the corrections. Four substantive errors were found this way and each is documented in the A2 report rather than removed from the record |
| Report drafting | Drafting and structuring the Assessment 2 technical section from the team's measured outputs | Verified every figure and number against the source artefact before inclusion |
| Project administration | Drafting Jira issue descriptions and the commit allocation document | Reviewed and applied by the Project Lead |
| Individual reflections | Not used, except for grammar and length corrections to text the member had already written | Each member wrote their own reflection in their own words |

### Errors in AI-generated code, found and corrected by the team

Recording these serves two purposes: it honours the disclosure commitment honestly, and it
demonstrates that the output was checked rather than accepted.

1. **A sentinel-removal rule destroyed the energy register.** A rule treating any value at or
   above 9,999 as an error code was applied to a cumulative counter that legitimately reaches the
   hundreds of thousands, taking the column from 2.34% to 98.59% missing. Caught by inspecting the
   before-and-after table.
2. **Cleaning was applied after aggregation**, letting sentinel values into hourly means. Caught
   because an air temperature of -39.988 C survived into the hourly store.
3. **An autocorrelation was computed on a filtered index.** Correlating by position within a
   daylight-only series meant the axis labelled hours was not hours. Caught because the periodicity
   appeared at roughly 12 rather than 24.
4. **A degradation trend was fitted across the site build-out period**, returning +0.748 kW per
   year and producing a chart labelled degradation that showed output rising. Caught by reading
   the annual means.

No result reported in Assessment 2 was generated by AI without being executed and inspected by the
team. Where AI-generated code proved wrong, the error and its correction appear in the body of the
report.

### Boundary the group applied

Generative AI was used as a drafting and review tool. It was not used to fabricate data, to
generate results that were not produced by running the committed notebooks, or to write the
individual reflections, which are assessed as each member's own words.

---

## References

Thuseethan, S., Gangajaliya, S., Hamlin, L., Shanmugam, B., & Thennadil, S. (2025).
Conv-Ensemble for solar power prediction with First Nations seasonal information.
*IEEE Open Journal of the Computer Society*, 6, 884–895.
https://doi.org/10.1109/OJCS.2025.3580339

Desert Knowledge Australia Solar Centre. (2026). *Alice Springs data download*.
https://dkasolarcentre.com.au/download?location=alice-springs
