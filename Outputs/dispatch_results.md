# Battery dispatch results (notebook 06)

Scored on 12,154 hours (506 days), 01 Apr 2024 to 22 Aug 2025.
Illustrative time of use tariff: off peak $0.15, shoulder $0.25, peak $0.4 per kWh, feed in $0.07.
Battery modelled from site telemetry: 354 kWh, 115 kW, one way efficiency 0.910.

## Key indicators
| KPI | value | meaning |
|---|---|---|
| coverage 1 h | 80.1% | share of daylight hours inside the 80% interval, 1 h ahead (target 80%) |
| coverage 24 h | 80.0% | same, 24 h ahead (target 80%) |
| cost, no battery | $128,709 | energy cost with no battery, illustrative tariff |
| cost, forecast plan | $99,999 | energy cost, battery planned with the forecast (caution 0.5) |
| saving | 22.3% | saving against no battery |
| value of the forecast | $3,419 | saving against the better rule without a forecast |
| benefit captured | 47% | share of the perfect foresight benefit captured |
| full cycles | 361 | equivalent full battery cycles over the period |
| export | 113.6 MWh | solar exported instead of stored or used |

## Strategies compared
| strategy | cost_$ | import_MWh | peak_import_MWh | export_MWh | discharged_MWh | saving_vs_no_battery_% |
|---|---|---|---|---|---|---|
| no battery | 128,709.2 | 571.1 | 146.2 | 176.1 | 0.0 | 0.0 |
| solar only, no forecast | 106,478.1 | 502.4 | 71.0 | 82.7 | 77.3 | 17.3 |
| always fill overnight | 103,418.0 | 605.9 | 22.8 | 175.9 | 125.6 | 19.6 |
| forecast, median | 100,463.7 | 527.7 | 36.8 | 100.6 | 111.5 | 21.9 |
| forecast, cautious (low edge) | 100,220.6 | 553.8 | 26.9 | 124.8 | 121.4 | 22.1 |
| perfect foresight | 96,136.1 | 515.1 | 22.8 | 85.2 | 125.6 | 25.3 |
| recorded battery, as operated | 116,067.0 | 518.0 | 106.0 | 101.5 | 66.5 | 9.8 |

## Which forecast limits the result
| setup | cost_$ | share_of_perfect_% |
|---|---|---|
| forecast solar, forecast demand | 100,464 | 41 |
| perfect solar,  forecast demand | 99,641 | 52 |
| forecast solar, perfect demand | 97,206 | 85 |
| perfect solar,  perfect demand | 96,136 | 100 |

## Caution level (chosen on 2024, judged on 2025)
| caution | cost_2024 | cost_2025 | captured_2025_% |
|---|---|---|---|
| 0 | 48,308 | 52,155 | 48 |
| 0 | 48,008 | 52,104 | 50 |
| 0 | 47,868 | 52,131 | 49 |
| 1 | 47,924 | 52,148 | 48 |
| 1 | 48,070 | 52,151 | 48 |
| 2 | 48,312 | 52,231 | 46 |
| 2 | 48,578 | 52,390 | 41 |

## Battery size (saving against no battery, %)
| battery size | solar only | always fill | forecast | perfect |
|---|---|---|---|---|
| 0.5x  (177 kWh) | 11.0 | 11.1 | 13.3 | 15.0 |
| 1x  (354 kWh) | 17.3 | 19.6 | 22.3 | 25.3 |
| 2x  (709 kWh) | 20.6 | 23.0 | 26.9 | 28.9 |

Figures: fig11_interval_calibration.png, fig12_site_average_day.png, fig13_dispatch_sensitivity.png, fig14_example_week.png
