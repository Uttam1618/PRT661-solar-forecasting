# Changelog

Scope changes, key decisions and their justification. Changes are permitted when justified and
documented.

Format: `YYYY-MM-DD — decision — reason — approved by`

---

## 2026-08

- **2026-08-01** — Repository initialised with project structure, team charter and data-quality
  summary. — Establishes collaboration and documentation evidence from the start of A1. — *TBC*

- **2026-08-01** — Per-inverter channels declared out of scope. — Per-array analysis is anomaly
  detection (Theme 3), not forecasting (Theme 2). Keeps scope aligned to the selected theme. — *TBC*

- **2026-08-01** — Primary data source changed from the 17-column MasterMeter1 extract to the
  yearly extracts (2008–2026). — The slim extract contains no BESS columns and ends 23 Aug 2025,
  so it cannot support the battery dispatch framing. The yearly files contain both master meters,
  the weather station and the post-2024 BESS columns. The slim file is retained as a cross-check
  only. — *TBC*

- **2026-08-01** — `Wind_Speed` excluded from the candidate feature set. — 52.4% missing in the
  source data; also excluded by Thuseethan et al. (2025) on this site. — *TBC*
