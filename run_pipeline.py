"""Run the PRT661 notebook chain in order and check that every expected output exists (SCRUM-51).

Usage, from the repository root:
    python run_pipeline.py --check            # only check outputs, run nothing (seconds)
    python run_pipeline.py                    # run notebooks 01 to 08, then check
    python run_pipeline.py --from 06          # run 06, 07 and 08 only, then check
    python run_pipeline.py --only 08          # run a single notebook, then check

Each notebook reads only the stores written by the notebooks before it, so running from any
stage forward reproduces everything after it. Notebooks are executed in place with
`jupyter nbconvert --execute`, so their saved outputs are refreshed too.

Before the first full run, place the raw DKASC files as described in Datasets/README.md and set
the REPO path in the first cell of each notebook to your own repository location.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
PROC, OUT, FIG = "Datasets/processed/", "Outputs/", "Outputs/figures/"

# notebook, expected outputs (relative to the repository root)
STAGES = [
    ("01_data_profiling", [OUT + "schema_matrix.csv"]),
    ("01b_schema_decisions", [OUT + "schema_drift_summary.md"]),
    ("02_ingest_mastermeter1", [PROC + "mastermeter1_5min.parquet", PROC + "mastermeter1_hourly.parquet",
                                OUT + "data_quality_mastermeter1.md"]),
    ("03_clean_mastermeter1", [PROC + "mastermeter1_5min_clean.parquet", PROC + "mastermeter1_hourly_clean.parquet",
                               OUT + "cleaning_report_mastermeter1.md"]),
    ("04_features_and_eda", [PROC + "features_hourly.parquet", FIG + "fig1_generation_history.png",
                             FIG + "fig2_diurnal_and_ramps.png", FIG + "fig3_correlations.png"]),
    ("04b_supporting_figures", [FIG + "fig4_data_availability.png", FIG + "fig5_autocorrelation.png",
                                FIG + "fig6_irradiance_power.png"]),
    ("05_modelling", [PROC + "forecasts_hourly.parquet", OUT + "model_results.md", FIG + "fig7_pred_vs_actual.png",
                      FIG + "fig8_forecast_week.png", FIG + "fig9_importance.png", FIG + "fig10_error_profile.png"]),
    ("06_bess_dispatch", [PROC + "forecasts_calibrated.parquet", PROC + "dispatch_hourly.parquet",
                          OUT + "dispatch_results.md", OUT + "dispatch_strategies.csv",
                          FIG + "fig11_interval_calibration.png", FIG + "fig12_site_average_day.png",
                          FIG + "fig13_dispatch_sensitivity.png", FIG + "fig14_example_week.png"]),
    ("07_demand_forecast", [PROC + "demand_forecasts.parquet", OUT + "demand_model_results.md",
                            OUT + "demand_model_comparison.csv", FIG + "fig15_demand_models.png",
                            FIG + "fig16_demand_dispatch.png"]),
    ("08_monitoring_retraining", [PROC + "monitoring_daily.parquet", OUT + "monitoring_results.md",
                                  OUT + "monitoring_alerts.csv", FIG + "fig17_monitoring.png",
                                  FIG + "fig18_drift_retraining.png"]),
]


def key(name):
    return name.split("_")[0]


def run(name, timeout):
    nb = REPO / "notebooks" / f"{name}.ipynb"
    if not nb.exists():
        print(f"  MISSING notebook {nb.relative_to(REPO)}")
        return False
    t0 = time.time()
    print(f"  running {nb.name} ...", flush=True)
    cmd = [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
           f"--ExecutePreprocessor.timeout={timeout}", str(nb)]
    res = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  FAILED after {time.time() - t0:.0f} s\n{res.stderr[-2000:]}")
        return False
    print(f"  done in {time.time() - t0:.0f} s")
    return True


def check(stages, since=None):
    """Every expected output must exist; after a run it must also be newer than the run start."""
    ok = True
    print(f"\n{'stage':<6} {'output':<52} {'size':>9}  status")
    for name, outputs in stages:
        for rel in outputs:
            p = REPO / rel
            if not p.exists():
                status, size = "MISSING", ""
                ok = False
            else:
                size = f"{p.stat().st_size / 1024:,.0f} kB"
                status = "ok"
                if since is not None and p.stat().st_mtime < since:
                    status, ok = "NOT UPDATED", False
            print(f"{key(name):<6} {rel:<52} {size:>9}  {status}")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Run and check the PRT661 notebook chain.")
    ap.add_argument("--check", action="store_true", help="only check that outputs exist")
    ap.add_argument("--from", dest="start", help="first notebook to run, for example 06")
    ap.add_argument("--only", help="run a single notebook, for example 08")
    ap.add_argument("--timeout", type=int, default=3600, help="seconds allowed per notebook")
    a = ap.parse_args()

    keys = [key(n) for n, _ in STAGES]
    if a.check:
        ok = check(STAGES)
    else:
        if a.only:
            todo = [s for s in STAGES if key(s[0]) == a.only]
        elif a.start:
            if a.start not in keys:
                sys.exit(f"unknown stage {a.start}; choose from {', '.join(keys)}")
            todo = STAGES[keys.index(a.start):]
        else:
            todo = STAGES
        if not todo:
            sys.exit(f"unknown stage; choose from {', '.join(keys)}")
        t0 = time.time()
        for name, _ in todo:
            if not run(name, a.timeout):
                sys.exit(1)
        ok = check(todo, since=t0) and check([s for s in STAGES if s not in todo])
    print("\nREPRODUCIBILITY CHECK PASSED" if ok else "\nREPRODUCIBILITY CHECK FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
