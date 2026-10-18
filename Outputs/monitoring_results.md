# Monitoring, drift detection and retraining (notebook 08)

## 1. Forecast performance monitoring
Daily checks on the 24 h ahead daylight forecasts, 02 Jan 2019 to 22 Aug 2025.
Error alert: 30 day normalised MAE above 0.354 (99th percentile of 2019 to 2020).
Coverage alert: 30 day coverage of the calibrated 80% interval outside 0.70 to 0.90.

| year | days | nmae | coverage | error_alert_days | coverage_alert_days |
|---|---|---|---|---|---|
| 2019 | 345 | 0.087 | 0.801 | 0 | 3 |
| 2020 | 366 | 0.135 | 0.795 | 8 | 15 |
| 2021 | 342 | 0.157 | 0.803 | 3 | 18 |
| 2022 | 365 | 0.176 | 0.8 | 0 | 13 |
| 2023 | 365 | 0.174 | 0.808 | 24 | 7 |
| 2024 | 366 | 0.179 | 0.794 | 8 | 5 |
| 2025 | 234 | 0.138 | 0.797 | 0 | 18 |

Alert episodes: 28, the longest 17 days.

## 2. Data drift check
Reference: first 28 days of 2024, median site solar / Master Meter 1 = 2.24.
Rule: 7 day median more than 20% from the reference for 3 consecutive days.
Drift detected on 28 Feb 2024 (7 day median 1.13, -49%). Re-baselined ratio 1.14;
0 days flagged afterwards to August 2025.

## 3. Retraining strategy (gradient boosting demand model, 2024-07-01 to 22 Aug 2025)
| strategy | planning_MAE_kW | worst_month_MAE_kW | model_fits |
|---|---|---|---|
| static | 41.3 | 95.6 | 1 |
| scheduled monthly | 24.9 | 53.9 | 14 |
| triggered (error +15%) | 29.1 | 59.9 | 3 |

Triggered refits at the start of: 2024-11, 2025-01.

Figures: fig17_monitoring.png, fig18_drift_retraining.png
