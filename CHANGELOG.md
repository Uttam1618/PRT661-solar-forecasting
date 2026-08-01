# Changelog

Scope changes, key decisions and their justification. Changes are permitted when justified and
documented.

Format: `YYYY-MM-DD — decision — reason — approved by`

---

## 2026-08

- **2026-08-01** — Repository initialised with project structure, team charter and data-quality
  summary. — Establishes collaboration and documentation evidence from the start of A1. — *TBC*

- **2026-08-01** — Primary modelling dataset set to the 17-column MasterMeter1 + weather extract;
  per-inverter channels declared out of scope. — Per-array analysis is anomaly detection
  (Theme 3), not forecasting (Theme 2). Keeps scope aligned to the selected theme. — *TBC*

- **2026-08-01** — `Wind_Speed` excluded from the candidate feature set. — 52.4% missing in the
  source data; also excluded by Thuseethan et al. (2025) on this site. — *TBC*
