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
| Repository access | Public repository containing no sensitive material. Write access limited to the five group members. `main` is protected; changes arrive by reviewed pull request. |
| Lab evidence | AWS Academy screenshots are checked for visible account identifiers or session tokens before being committed. |
| Data integrity | Raw data is immutable. All transformations are scripted, so any output can be regenerated and verified against source. |

## 6. Academic integrity

Prior work on this dataset — including our unit lecturer's published paper — is cited explicitly
rather than absorbed silently. Where generative AI tools assist with drafting or code, their use
is acknowledged in accordance with CDU policy, and all technical decisions recorded in this
repository are ones the group can explain and defend.

---

## References

Thuseethan, S., Gangajaliya, S., Hamlin, L., Shanmugam, B., & Thennadil, S. (2025).
Conv-Ensemble for solar power prediction with First Nations seasonal information.
*IEEE Open Journal of the Computer Society*, 6, 884–895.
https://doi.org/10.1109/OJCS.2025.3580339

Desert Knowledge Australia Solar Centre. (2026). *Alice Springs data download*.
https://dkasolarcentre.com.au/download?location=alice-springs
