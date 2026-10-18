# Demand forecast comparison (notebook 07)

Out of sample, walk forward with monthly refits on an expanding window, 2024-07-01 to 22 Aug 2025.
Inputs are known by 22:00 the evening before: demand at the same hour 1, 2 and 7 days earlier, the A3 7 day mean,
temperature at the same hour yesterday, hour, weekday, weekend and month.

## Accuracy
| model | planning hours 07 to 15 MAE_kW | planning hours 07 to 15 RMSE_kW | planning hours 07 to 15 bias_kW | all hours MAE_kW | all hours RMSE_kW | all hours bias_kW | planning hours 07 to 15 MAE_vs_A3_% |
|---|---|---|---|---|---|---|---|
| A3: 7 day same hour mean | 54.5 | 68.1 | -0.4 | 26.5 | 44.2 | -0.2 | 0.0 |
| same hour yesterday | 47.5 | 73.6 | -0.2 | 24.1 | 48.0 | -0.1 | 12.9 |
| same hour last week | 34.9 | 52.6 | -0.1 | 19.1 | 35.1 | -0.1 | 36.0 |
| linear regression | 30.3 | 43.2 | -2.8 | 18.3 | 29.5 | -1.4 | 44.5 |
| gradient boosting | 24.9 | 38.1 | -4.0 | 13.9 | 25.6 | -1.2 | 54.3 |

## Planning hour MAE by day type (kW)
| model | weekday | weekend |
|---|---|---|
| A3: 7 day same hour mean | 42.3 | 85.5 |
| same hour yesterday | 42.7 | 59.6 |
| same hour last week | 42.2 | 16.2 |
| linear regression | 33.4 | 22.3 |
| gradient boosting | 28.4 | 16.2 |

## Battery plan with each demand forecast (solar caution 0.5)
| strategy | cost_$ | saving_vs_no_battery_% | value_vs_best_rule_$ | share_of_perfect_% |
|---|---|---|---|---|
| no battery | 113071.7 | 0.0 |  |  |
| solar only, no forecast | 95869.3 | 15.2 |  |  |
| always fill overnight | 91716.3 | 18.9 |  |  |
| forecast plan, demand: A3: 7 day same hour mean | 89507.6 | 20.8 | 2208.7 | 38.9 |
| forecast plan, demand: same hour yesterday | 89592.0 | 20.8 | 2124.3 | 37.5 |
| forecast plan, demand: same hour last week | 88528.3 | 21.7 | 3188.1 | 56.2 |
| forecast plan, demand: linear regression | 88381.1 | 21.8 | 3335.2 | 58.8 |
| forecast plan, demand: gradient boosting | 87773.1 | 22.4 | 3943.2 | 69.5 |
| forecast plan, demand: perfect demand | 87150.7 | 22.9 | 4565.6 | 80.5 |
| perfect foresight | 86044.2 | 23.9 | 5672.2 | 100.0 |

Best model: gradient boosting. Saving 20.8% to 22.4%,
value of the forecast $2,209 to $3,943,
share of the perfect foresight benefit 39% to 70%.

Figures: fig15_demand_models.png, fig16_demand_dispatch.png
