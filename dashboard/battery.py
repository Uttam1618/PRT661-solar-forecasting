"""Battery model and nightly planning rule, ported unchanged from notebook 06 (step 8).

The dashboard re-runs this rule so the operator can test other settings: how cautious the
solar forecast should be, which demand forecast to plan with, the battery size and the tariff.
"""
import numpy as np
import pandas as pd

# Battery fitted from site telemetry in notebook 06 (step 6)
BATT = {"capacity_kwh": 354.271, "soc_min": 0.022, "soc_max": 0.948,
        "p_charge_kw": 114.773, "p_discharge_kw": 114.773, "eta_oneway": 0.910, "standby_kw": 0.715}

TARIFF = {"offpeak": 0.15, "shoulder": 0.25, "peak": 0.40}   # $/kWh, illustrative
FEED_IN = 0.07                                               # $/kWh paid for exported solar
CAUTION = 0.5                                                # chosen on 2024 in notebook 06


def limits(scale=1.0, batt=BATT):
    cap = batt["capacity_kwh"] * scale
    return {"e_min": batt["soc_min"] * cap, "e_max": batt["soc_max"] * cap,
            "p_c": batt["p_charge_kw"] * scale, "p_d": batt["p_discharge_kw"] * scale,
            "eta": batt["eta_oneway"], "standby": batt["standby_kw"]}


def simulate(pv, dem, hours, mode, plan_pv=None, plan_dem=None, scale=1.0, batt=BATT):
    """Hour by hour simulation. mode: 'no battery', 'solar only', 'always fill' or 'planned'.

    Returns an array with columns imp, exp, chg, dis, stored (kWh) and, for every 22:00 hour,
    the decision taken: battery space, solar expected to fill it, and grid energy to buy.
    """
    L = limits(scale, batt)
    e_min, e_max, p_c, p_d, eta, standby = (L[k] for k in ("e_min", "e_max", "p_c", "p_d", "eta", "standby"))
    n = len(pv)
    res = np.zeros((n, 5))
    dec = np.full((n, 3), np.nan)
    e, target = (e_min + e_max) / 2, 0.0

    for t in range(n):
        h, net = hours[t], pv[t] - dem[t]
        if mode == "no battery":
            res[t] = (max(0.0, -net), max(0.0, net), 0.0, 0.0, 0.0)
            continue

        # 22:00, tonight's decision: how much cheap grid energy to store for tomorrow's peak
        if h == 22 and mode in ("always fill", "planned"):
            solar = 0.0
            if mode == "planned":
                tomorrow = slice(t + 9, t + 18)                       # 07:00 to 15:59
                solar = np.clip(plan_pv[tomorrow] - plan_dem[tomorrow], 0, p_c).sum() * eta
            target = max(0.0, (e_max - e) - solar) / eta
            dec[t] = (e_max - e, solar, target)
        if h == 7:
            target = 0.0

        imp, exp, chg, dis = standby, 0.0, 0.0, 0.0
        if net >= 0:
            chg = min(net, p_c, (e_max - e) / eta)
            e += chg * eta
            exp = net - chg
        else:
            deficit = -net
            if 16 <= h <= 21:
                dis = min(deficit, p_d, (e - e_min) * eta)
                e -= dis / eta
            imp += deficit - dis

        if target > 0 and (h >= 22 or h <= 6):
            g = min(target, p_c - chg, (e_max - e) / eta)
            if g > 0:
                e += g * eta; chg += g; imp += g; target -= g

        res[t] = (imp, exp, chg, dis, e)
    return res, dec


def run_scenario(sim, dem_plan, caution=CAUTION, scale=1.0):
    """All strategies on the full hourly table. Returns {name: DataFrame} with a decision table."""
    pv, dem, hrs = sim.pv.to_numpy(), sim.demand.to_numpy(), sim.index.hour.to_numpy()
    pv_plan = (sim.pv_fc50 - caution * (sim.pv_fc50 - sim.pv_fclo)).to_numpy()
    jobs = {"no battery": ("no battery", None, None),
            "solar only, no forecast": ("solar only", None, None),
            "always fill overnight": ("always fill", None, None),
            "forecast plan": ("planned", pv_plan, dem_plan),
            "perfect foresight": ("planned", pv, dem)}
    out = {}
    for name, (mode, ppv, pdem) in jobs.items():
        res, dec = simulate(pv, dem, hrs, mode, ppv, pdem, scale)
        df = pd.DataFrame(res, index=sim.index, columns=["imp", "exp", "chg", "dis", "stored"])
        df[["space", "solar_fill", "grid_buy"]] = dec
        out[name] = df
    return out


def hourly_cost(run, sim, tariff=TARIFF, feed_in=FEED_IN):
    price = sim.period.map(tariff)
    return run.imp * price - run.exp * feed_in


def score(runs, sim, mask, tariff=TARIFF, feed_in=FEED_IN):
    """Cost and headline indicators for each strategy on the hours in mask."""
    rows = {}
    for name, r in runs.items():
        c = hourly_cost(r, sim, tariff, feed_in)[mask]
        rows[name] = {"cost_$": c.sum(),
                      "import_MWh": r.imp[mask].sum() / 1e3,
                      "peak_import_MWh": r.imp[mask & (sim.period == "peak")].sum() / 1e3,
                      "export_MWh": r.exp[mask].sum() / 1e3,
                      "discharged_MWh": r.dis[mask].sum() / 1e3}
    t = pd.DataFrame(rows).T
    t["saving_vs_no_battery_%"] = 100 * (1 - t["cost_$"] / t.loc["no battery", "cost_$"])
    blind = t.loc[["solar only, no forecast", "always fill overnight"], "cost_$"].min()
    perfect = t.loc["perfect foresight", "cost_$"]
    kpi = {"saving_%": t.loc["forecast plan", "saving_vs_no_battery_%"],
           "value_$": blind - t.loc["forecast plan", "cost_$"],
           "share_%": 100 * (blind - t.loc["forecast plan", "cost_$"]) / (blind - perfect),
           "cost_$": t.loc["forecast plan", "cost_$"]}
    return t, kpi
