"""PRT661 Group 4 · Solar forecast and battery planning dashboard (SCRUM-64).

Run from the repository root after notebooks 05 to 08 have been run:
    streamlit run dashboard/app.py

Reads only the saved outputs in Datasets/processed and Outputs, never the raw data.
The battery rule from notebook 06 is re-run live (dashboard/battery.py), so every
setting in the sidebar changes the plan, the costs and the charts.
"""
from datetime import date
from pathlib import Path
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from battery import BATT, CAUTION, FEED_IN, TARIFF, hourly_cost, limits, run_scenario, score, simulate

REPO = Path(__file__).resolve().parents[1]
PROC, OUT = REPO / "Datasets" / "processed", REPO / "Outputs"
K = 1.135                        # Master Meter 1 to whole site solar, fitted on March 2024 (notebook 06)
A4_START = pd.Timestamp("2024-07-01")   # first month of out of sample demand forecasts (notebook 07)

# colours: one meaning each, used the same way on every page
INK, INK2, MUTED, GRID = "#1f1f1e", "#52514e", "#8f8e88", "#ecebe8"
BLUE, BLUE_L, ORANGE, AQUA, YELLOW = "#2a78d6", "#86b6ef", "#eb6834", "#1baf7a", "#eda100"
GREY, GREY_D, GOOD, CRITICAL = "#b9b8b1", "#6f6e69", "#0ca30c", "#d03b3b"
STRAT_COL = {"no battery": "#d9d8d2", "solar only, no forecast": GREY, "always fill overnight": GREY_D,
             "forecast plan": BLUE, "perfect foresight": AQUA}
MODEL_COL = {"gradient boosting": BLUE, "linear regression": ORANGE, "same hour last week": AQUA,
             "same hour yesterday": YELLOW, "A3: 7 day same hour mean": GREY_D}
DEM_LABEL = {"gradient boosting": "Gradient boosting (A4)", "linear regression": "Linear regression",
             "same hour last week": "Same hour last week", "same hour yesterday": "Same hour yesterday",
             "A3: 7 day same hour mean": "7 day mean (A3)", "perfect demand": "Perfect demand (hindsight)"}

st.set_page_config(page_title="Solar and battery planner", page_icon="☀️", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1320px;}
[data-testid="stMetricValue"] {font-size: 1.85rem; font-weight: 600; color: #1f1f1e;}
[data-testid="stMetricLabel"] p {font-size: .86rem; color: #52514e;}
.hero {padding: 20px 26px 18px; border-radius: 14px; margin-bottom: 1.1rem;
       background: linear-gradient(120deg, #0d366b 0%, #1c5cab 55%, #2a78d6 100%); color: #fff;}
.hero h1 {color: #fff; font-size: 1.75rem; line-height: 1.2; margin: 0; padding: 0; font-weight: 700;}
.hero p {color: #d7e6fa; margin: .35rem 0 0; font-size: .98rem;}
.chips {display: flex; gap: .45rem; flex-wrap: wrap; margin-top: .8rem;}
.chip {background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.28); color: #fff;
       padding: .14rem .7rem; border-radius: 999px; font-size: .8rem; white-space: nowrap;}
.chip.ok {background: rgba(12,163,12,.28);} .chip.bad {background: rgba(208,59,59,.45);}
.flow {display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; align-items: stretch; gap: .6rem;}
.flow .box {border: 1px solid #ecebe8; border-radius: 10px; padding: .7rem .9rem; background: #fff;}
.flow .box span {display: block; font-size: .8rem; color: #52514e;}
.flow .box b {display: block; font-size: 1.55rem; color: #1f1f1e; font-weight: 600; margin-top: .1rem;}
.flow .box small {color: #8f8e88; font-size: .76rem;}
.flow .box.key {border: 2px solid #2a78d6; background: #f3f8fe;}
.flow .op {align-self: center; font-size: 1.4rem; color: #8f8e88;}
.note {color: #52514e; font-size: .88rem;}
@media (max-width: 800px) {.flow {grid-template-columns: 1fr;} .flow .op {display: none;}}
</style>
""", unsafe_allow_html=True)


# ================================================================ data
def read_md_table(path, heading):
    """Read the markdown table under a heading of a results file written by a notebook."""
    if not path.exists():
        return None
    rows, on = [], False
    for ln in path.read_text().splitlines():
        if ln.startswith(heading):
            on = True
        elif on and ln.startswith("|"):
            rows.append([x.strip() for x in ln.strip("|").split("|")])
        elif on and rows:
            break
    if len(rows) < 3:
        return None
    df = pd.DataFrame(rows[2:], columns=rows[0]).set_index(rows[0][0])
    return df.apply(pd.to_numeric, errors="coerce")


@st.cache_data(show_spinner="Loading the saved outputs")
def load():
    sim = pd.read_parquet(PROC / "dispatch_hourly.parquet")
    fc = pd.read_parquet(PROC / "forecasts_calibrated.parquet")
    f24 = fc[fc.horizon == 24].drop_duplicates("target_time").set_index("target_time")
    for c in ["lo_c", "hi_c"]:
        sim[f"pv_{c}"] = (K * f24[c]).reindex(sim.index).clip(lower=0)
    sim["pv_hi_c"] = sim.pv_hi_c.fillna(sim.pv_fc50)
    opt = lambda p, f: f(p) if p.exists() else None
    d = {"sim": sim,
         "dem": opt(PROC / "demand_forecasts.parquet", pd.read_parquet),
         "mon": opt(PROC / "monitoring_daily.parquet", pd.read_parquet),
         "strat": opt(OUT / "Results/dispatch_strategies.csv", lambda p: pd.read_csv(p, index_col=0)),
         "models": opt(OUT / "Results/demand_model_comparison.csv", lambda p: pd.read_csv(p, header=[0, 1], index_col=0)),
         "alerts": opt(OUT / "Results/monitoring_alerts.csv", pd.read_csv),
         "retrain": read_md_table(OUT / "Results/monitoring_results.md", "## 3."),
         "mon_md": opt(OUT / "Results/monitoring_results.md", lambda p: p.read_text())}
    return d


try:
    D = load()
except FileNotFoundError as e:
    st.error(f"Missing output file: {e.filename}. Run notebooks 05 to 08 first (see README).")
    st.stop()

SIM, DEM, MON = D["sim"], D["dem"], D["mon"]
RECORDED = SIM.grid_recorded.notna()        # every strategy is scored on the same hours (notebook 06)

# demand forecasts the plan can use; the A4 models replace the A3 mean from July 2024 (as in notebook 07)
DEM_PLAN = {"A3: 7 day same hour mean": SIM.dem_fc.to_numpy()}
if DEM is not None:
    for m in DEM.columns.drop("actual"):
        s = SIM.dem_fc.copy()
        s.loc[DEM.index] = DEM[m]
        DEM_PLAN[m] = s.to_numpy()
DEM_PLAN["perfect demand"] = SIM.demand.to_numpy()
DEM_ORDER = [m for m in DEM_LABEL if m in DEM_PLAN]
DEFAULT_DEM = "gradient boosting" if "gradient boosting" in DEM_PLAN else "A3: 7 day same hour mean"
START = A4_START if DEM is not None else SIM.index.min()


@st.cache_data(max_entries=24, show_spinner="Running the battery simulation")
def scenario(dem_name, caution, scale):
    return run_scenario(SIM, DEM_PLAN[dem_name], caution, scale)


@st.cache_data(max_entries=12, show_spinner="Testing caution levels")
def caution_runs(dem_name, scale, levels):
    pv, dem, hrs = SIM.pv.to_numpy(), SIM.demand.to_numpy(), SIM.index.hour.to_numpy()
    out = {}
    for c in levels:
        plan = (SIM.pv_fc50 - c * (SIM.pv_fc50 - SIM.pv_fclo)).to_numpy()
        r, _ = simulate(pv, dem, hrs, "planned", plan, DEM_PLAN[dem_name], scale)
        out[c] = pd.DataFrame(r[:, :2], index=SIM.index, columns=["imp", "exp"])
    return out


@st.cache_data(max_entries=12, show_spinner="Testing each demand forecast")
def demand_runs(caution, scale):
    pv, dem, hrs = SIM.pv.to_numpy(), SIM.demand.to_numpy(), SIM.index.hour.to_numpy()
    plan = (SIM.pv_fc50 - caution * (SIM.pv_fc50 - SIM.pv_fclo)).to_numpy()
    out = {}
    for m in DEM_ORDER:
        r, _ = simulate(pv, dem, hrs, "planned", plan, DEM_PLAN[m], scale)
        out[m] = pd.DataFrame(r[:, :2], index=SIM.index, columns=["imp", "exp"])
    return out


def cost_of(run, mask, tariff=TARIFF, feed_in=FEED_IN):
    return hourly_cost(run, SIM, tariff, feed_in)[mask].sum()


# ================================================================ chart helpers
def style(fig, title=None, h=360, y=None, x=None, legend=True, hover="x unified", where="top"):
    """Shared look. Legend sits under the title (left), at the right, or below the plot."""
    leg = {"top": dict(yanchor="bottom", y=1.01, xanchor="left", x=0),
           "right": dict(yanchor="bottom", y=1.01, xanchor="right", x=1),
           "bottom": dict(yanchor="top", y=-0.16, xanchor="left", x=0)}[where]
    top = (34 if title else 10) + (30 if legend and where != "bottom" else 0) + 8
    fig.update_layout(
        height=h, template="plotly_white", hovermode=hover, showlegend=legend,
        title=dict(text=f"<b>{title}</b>" if title else None, x=0, xanchor="left", xref="container",
                   y=1, yref="container", yanchor="top", pad=dict(t=6, l=2), font=dict(size=15, color=INK)),
        margin=dict(l=8, r=8, t=top, b=8),
        font=dict(family="Helvetica, Arial, sans-serif", color=INK2, size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", bordercolor=GRID, font=dict(color=INK, size=12)),
        legend=dict(orientation="h", title=None, bgcolor="rgba(0,0,0,0)", font=dict(size=12, color=INK2), **leg),
        barcornerradius=4, bargap=.28, bargroupgap=.08)
    fig.update_xaxes(showgrid=False, linecolor=GRID, ticks="outside", tickcolor=GRID, title=x,
                     title_font=dict(size=12, color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID, title=y, title_font=dict(size=12, color=MUTED),
                     automargin=True)
    if any(getattr(t, "orientation", None) == "h" for t in fig.data):
        fig.update_layout(margin_l=170)
    return fig


def show(fig, key=None, **kw):
    return st.plotly_chart(fig, theme=None, key=key, config={"displaylogo": False, "modeBarButtonsToRemove":
                           ["select2d", "lasso2d", "autoScale2d"]}, **kw)


def hero(title, text, chips=()):
    c = "".join(f'<span class="chip {k}">{t}</span>' for t, k in chips)
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{text}</p>'
                f'{f"<div class=chips>{c}</div>" if c else ""}</div>', unsafe_allow_html=True)


def health():
    """Latest monitoring status: (ok, text)."""
    if MON is None:
        return None, "monitoring not run"
    last = MON.dropna(subset=["nmae"]).iloc[-1]
    bad = bool(last.alert_error or last.alert_coverage)
    return (not bad), ("forecast check: alert" if bad else "forecast check: within limits")


def sdollar(v):
    """Signed dollars with the sign first, so Streamlit colours the delta the right way."""
    return f"{'+' if v >= 0 else '-'}${abs(v):,.0f}"


# ================================================================ sidebar: plan settings
PLAN_HELP = ("These settings feed the nightly battery rule from notebook 06, re-run live. "
             "Defaults are the settings chosen in the notebooks.")


def plan_settings():
    with st.sidebar:
        st.markdown("**Plan settings**", help=PLAN_HELP)
        dem_name = st.selectbox("Demand forecast", DEM_ORDER, index=DEM_ORDER.index(DEFAULT_DEM),
                                format_func=DEM_LABEL.get, key="dem_name")
        caution = st.slider("Solar caution", 0.0, 2.0, CAUTION, 0.25, key="caution",
                            help="0 plans with the median solar forecast, 1 with the low edge of the "
                                 "calibrated 80% range. 0.5 was chosen on 2024 data in notebook 06.")
        scale = st.select_slider("Battery size", [0.5, 1.0, 1.5, 2.0], 1.0, key="scale",
                                 format_func=lambda s: f"{s:g}x ({s * BATT['capacity_kwh']:.0f} kWh)")
        changed = (dem_name, caution, scale) != (DEFAULT_DEM, CAUTION, 1.0)
        if changed:
            st.caption("Settings differ from the notebook defaults.")
            if st.button("Reset to defaults", width="stretch"):
                for k in ("dem_name", "caution", "scale"):
                    st.session_state.pop(k, None)
                st.rerun()
        st.divider()
        st.caption("Tariff (illustrative): \\$0.15 off peak, \\$0.25 shoulder, \\$0.40 peak 16:00 to 21:59, "
                   "\\$0.07 feed in. Forecasts are 24 h ahead, issued the evening before.")
        st.caption("DKASC Alice Springs · PRT661 Group 4")
    return dem_name, caution, scale


# ================================================================ page: overview
def page_overview():
    dem_name, caution, scale = SETTINGS
    runs = scenario(dem_name, caution, scale)
    mask = RECORDED & (SIM.index >= START)
    table, kpi = score(runs, SIM, mask)
    ref = None
    if dem_name != "A3: 7 day same hour mean":
        _, ref = score(scenario("A3: 7 day same hour mean", caution, scale), SIM, mask)

    ok, htxt = health()
    hero("Solar and battery planner",
         "Each evening at 22:00 the plan decides how much cheap grid energy to store for the next day's "
         "16:00 to 21:59 peak, using tomorrow's solar forecast and its uncertainty.",
         [(f"Data {SIM.index.min():%d %b %Y} to {SIM.index.max():%d %b %Y}", ""),
          (f"Scored {START:%d %b %Y} onward, out of sample", ""),
          (("✓ " if ok else "⚠ ") + htxt, "ok" if ok else "bad"),
          (f"Plan: {DEM_LABEL[dem_name]}, caution {caution:g}, {scale:g}x battery", "")])

    nob = hourly_cost(runs["no battery"], SIM)
    plan = hourly_cost(runs["forecast plan"], SIM)

    c = st.columns(4)
    d = (lambda k, f: f(kpi[k] - ref[k]) if ref else None)
    c[0].metric("Saving against no battery", f"{kpi['saving_%']:.1f}%", border=True,
                delta=d("saving_%", lambda v: f"{v:+.1f} points vs A3 demand"))
    c[1].metric("Value of the forecast", f"${kpi['value_$']:,.0f}", border=True,
                delta=d("value_$", lambda v: f"{sdollar(v)} vs A3 demand"),
                help="Saving beyond the better of the two rules that use no forecast")
    c[2].metric("Share of perfect foresight", f"{kpi['share_%']:.0f}%", border=True,
                delta=d("share_%", lambda v: f"{v:+.0f} points vs A3 demand"),
                help="How much of the benefit of knowing tomorrow exactly the plan captures")
    if D["models"] is not None:
        mae = D["models"][("planning hours 07 to 15", "MAE_kW")]
        m = dem_name if dem_name in mae.index else "gradient boosting"
        c[3].metric("Demand forecast error", f"{mae[m]:.1f} kW", border=True,
                    delta=f"{mae[m] - mae['A3: 7 day same hour mean']:.1f} kW vs A3", delta_color="inverse",
                    help=f"{DEM_LABEL.get(m, m)}: mean absolute error, planning hours 07:00 to 15:59, out of sample")

    left, right = st.columns([3, 2], gap="medium")
    with left:
        fig = go.Figure()
        for name in ["perfect foresight", "forecast plan", "always fill overnight", "solar only, no forecast"]:
            cum = (nob - hourly_cost(runs[name], SIM))[mask].resample("D").sum().cumsum()
            fig.add_trace(go.Scatter(x=cum.index, y=cum, name=name, line=dict(color=STRAT_COL[name],
                          width=3 if name == "forecast plan" else 2,
                          dash="dot" if name == "perfect foresight" else "solid"),
                          hovertemplate="$%{y:,.0f}"))
            fig.add_annotation(x=cum.index[-1], y=cum.iloc[-1], text=f"${cum.iloc[-1]:,.0f}", showarrow=False,
                               xanchor="left", xshift=6, font=dict(size=11, color=INK2))
        fig.update_xaxes(range=[cum.index[0], cum.index[-1] + pd.Timedelta("45D")])
        show(style(fig, "Cumulative saving against no battery", 380, "$"))
    with right:
        s = table["saving_vs_no_battery_%"].drop("no battery")
        if ref is not None:
            t3, _ = score(scenario("A3: 7 day same hour mean", caution, scale), SIM, mask)
            s["forecast plan, A3 demand"] = t3.loc["forecast plan", "saving_vs_no_battery_%"]
        s = s.sort_values()
        cols = [STRAT_COL.get(n, BLUE_L) for n in s.index]
        fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=cols,
                               text=[f"{v:.1f}%" for v in s.values], textposition="outside",
                               textfont=dict(color=INK2), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
        fig.update_xaxes(range=[0, s.max() * 1.3], showticklabels=False)
        show(style(fig, "Saving by strategy", 380, legend=False, hover="closest"))

    mon_tab = pd.DataFrame({n: (nob - hourly_cost(runs[n], SIM))[mask].resample("MS").sum()
                            for n in ["always fill overnight", "forecast plan", "perfect foresight"]})
    fig = go.Figure([go.Bar(x=mon_tab.index, y=mon_tab[n], name=n, marker_color=STRAT_COL[n],
                            hovertemplate="$%{y:,.0f}") for n in mon_tab])
    fig.update_xaxes(dtick="M1", tickformat="%b<br>%Y")
    show(style(fig, "Saving each month against no battery", 330, "$"))
    st.caption("Grey: rules that use no forecast. Blue: the forecast plan with the sidebar settings. "
               "Aqua: perfect foresight, the most any plan could save. August 2025 is a part month (to the 22nd).")

    if D["strat"] is not None:
        with st.expander("A3 result for comparison (notebook 06, 01 Apr 2024 to 22 Aug 2025)"):
            st.dataframe(D["strat"].round(1))


# ================================================================ page: battery plan by day
def page_day():
    dem_name, caution, scale = SETTINGS
    runs = scenario(dem_name, caution, scale)
    days = pd.Series(SIM.index.normalize().unique())
    days = days[(days >= START) & (days <= SIM.index.max().normalize())]
    if "day" not in st.session_state:
        st.session_state.day = date(2025, 5, 21)

    hero("Battery plan by day",
         "Pick a day on the calendar to see the decision taken the night before, the forecast it was based on, "
         "and what actually happened.",
         [(f"Plan: {DEM_LABEL[dem_name]}, caution {caution:g}, {scale:g}x battery", "")])

    # calendar of daily saving, clickable
    nob, plan = hourly_cost(runs["no battery"], SIM), hourly_cost(runs["forecast plan"], SIM)
    daily = (nob - plan)[RECORDED].resample("D").sum().reindex(days.values)
    cal = pd.DataFrame({"day": days.values, "saving": daily.values})
    cal["week"] = cal.day - pd.to_timedelta(cal.day.dt.dayofweek, unit="D")
    cal["dow"] = cal.day.dt.dayofweek
    st.session_state["cal_days"] = [d.date() for d in cal.day]
    lim = np.nanpercentile(np.abs(cal.saving), 98)

    fig = go.Figure(go.Scatter(
        x=cal.week, y=cal.dow, mode="markers",
        marker=dict(symbol="square", size=13, color=cal.saving, cmin=-lim, cmax=lim, cmid=0,
                    colorscale=[[0, "#e34948"], [.5, "#f0efec"], [1, BLUE]], line=dict(width=0),
                    colorbar=dict(title=dict(text="$ saved", side="right"), thickness=10, len=.9,
                                  outlinewidth=0, tickprefix="$")),
        customdata=np.stack([cal.day.dt.strftime("%a %d %b %Y"), cal.saving.round(0)], axis=1),
        hovertemplate="%{customdata[0]}<br>saved $%{customdata[1]}<extra></extra>"))
    sel = cal[cal.day.dt.date == st.session_state.day]
    fig.add_trace(go.Scatter(x=sel.week, y=sel.dow, mode="markers", hoverinfo="skip",
                             marker=dict(symbol="square-open", size=17, color=INK, line=dict(width=2))))
    fig.update_yaxes(tickvals=list(range(7)), ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                     autorange="reversed", showgrid=False)
    fig.update_xaxes(tickformat="%b %Y", dtick="M2", ticks="")
    fig.update_layout(dragmode=False, clickmode="event+select")
    show(style(fig, "Daily saving against no battery · click a day", 250, legend=False, hover="closest"),
         key="cal", on_select=_pick_day, selection_mode="points")

    day = st.date_input("Day", key="day", min_value=days.min().date(), max_value=days.max().date())
    t0 = pd.Timestamp(day)
    w = SIM.loc[t0: t0 + pd.Timedelta("23h")]
    dec_t = t0 - pd.Timedelta("2h")
    L = limits(scale)
    dplan = pd.Series(DEM_PLAN[dem_name], index=SIM.index).loc[w.index]

    # the decision taken at 22:00 the night before
    pr = runs["forecast plan"].loc[dec_t] if dec_t in SIM.index else None
    af = runs["always fill overnight"].loc[dec_t] if dec_t in SIM.index else None
    st.markdown(f"#### Decision at 22:00 on {dec_t:%A %d %B}")
    if pr is not None and not np.isnan(pr.space):
        st.markdown(f"""<div class="flow">
          <div class="box"><span>Empty space in the battery</span><b>{pr.space:,.0f} kWh</b>
               <small>between now and full ({L['e_max']:,.0f} kWh usable top)</small></div>
          <div class="op">→</div>
          <div class="box"><span>Solar expected to fill it tomorrow</span><b>{pr.solar_fill:,.0f} kWh</b>
               <small>surplus over forecast demand, 07:00 to 15:59</small></div>
          <div class="op">→</div>
          <div class="box key"><span>Buy from the grid tonight</span><b>{pr.grid_buy:,.0f} kWh</b>
               <small>at the off peak price; always fill would buy {af.grid_buy:,.0f} kWh</small></div>
        </div>""", unsafe_allow_html=True)

    # how sure was the solar forecast: fill under each edge of the 80% range against what happened
    win = (w.index.hour >= 7) & (w.index.hour <= 15)
    fill = lambda pv: float(np.clip(pv[win] - dplan[win], 0, L["p_c"]).sum() * L["eta"])
    pts = {"low edge": fill(w.pv_lo_c), "median": fill(w.pv_fc50), "high edge": fill(w.pv_hi_c),
           "plan (caution)": fill(w.pv_fc50 - caution * (w.pv_fc50 - w.pv_fclo)), "actual": fill(w.pv)}
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[pts["low edge"], pts["high edge"]], y=[0, 0], mode="lines", name="80% range",
                             line=dict(color=BLUE_L, width=10), hoverinfo="skip"))
    for k, sym, col, size in [("median", "line-ns-open", BLUE, 22), ("plan (caution)", "circle", BLUE, 13),
                              ("actual", "diamond", ORANGE, 15)]:
        fig.add_trace(go.Scatter(x=[pts[k]], y=[0], mode="markers", name=k,
                                 marker=dict(symbol=sym, size=size, color=col, line=dict(width=2, color=col)),
                                 hovertemplate=f"{k}: %{{x:,.0f}} kWh<extra></extra>"))
    fig.update_yaxes(visible=False, range=[-1, 1])
    fig.update_xaxes(title="solar energy into the battery tomorrow (kWh)", showgrid=True, gridcolor=GRID)
    show(style(fig, "How sure was tomorrow's solar?", 200, hover="closest"))

    cost = lambda n: hourly_cost(runs[n], SIM).loc[w.index].sum()
    c = st.columns(4)
    c[0].metric("Cost with no battery", f"${cost('no battery'):,.0f}", border=True)
    c[1].metric("Cost, always fill", f"${cost('always fill overnight'):,.0f}", border=True,
                delta=f"saves ${cost('no battery') - cost('always fill overnight'):,.0f}", delta_color="off", delta_arrow="off")
    c[2].metric("Cost with the plan", f"${cost('forecast plan'):,.0f}", border=True,
                delta=f"saves ${cost('no battery') - cost('forecast plan'):,.0f}", delta_color="off", delta_arrow="off")
    c[3].metric("Cost, perfect foresight", f"${cost('perfect foresight'):,.0f}", border=True,
                delta=f"saves ${cost('no battery') - cost('perfect foresight'):,.0f}", delta_color="off", delta_arrow="off")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w.index, y=w.pv_hi_c, line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=w.index, y=w.pv_lo_c, fill="tonexty", fillcolor="rgba(235,104,52,.15)",
                             line=dict(width=0), name="solar, 80% range", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=w.index, y=w.pv_fc50, name="solar forecast", line=dict(color=ORANGE, dash="dash")))
    fig.add_trace(go.Scatter(x=w.index, y=w.pv, name="solar actual", line=dict(color=ORANGE, width=3)))
    fig.add_trace(go.Scatter(x=w.index, y=dplan, name=f"demand forecast, {DEM_LABEL[dem_name]}",
                             line=dict(color=BLUE, dash="dot", width=2)))
    fig.add_trace(go.Scatter(x=w.index, y=w.demand, name="demand actual", line=dict(color=INK, width=3)))
    fig.add_vrect(x0=t0 + pd.Timedelta("16h"), x1=t0 + pd.Timedelta("22h"), fillcolor=CRITICAL, opacity=.06,
                  line_width=0, annotation_text="peak price", annotation_position="top left",
                  annotation_font=dict(size=11, color=MUTED))
    fig.update_traces(hovertemplate="%{y:.0f} kW")
    fig.update_xaxes(tickformat="%H:%M")
    show(style(fig, f"Forecast and actual, {t0:%A %d %B %Y}", 420, "kW"))

    fig = go.Figure()
    for n, width, dash, op in [("perfect foresight", 6, "solid", .45), ("always fill overnight", 2, "dash", 1),
                               ("forecast plan", 3, "solid", 1)]:
        r = runs[n].loc[w.index]
        fig.add_trace(go.Scatter(x=w.index, y=r.stored, name=n, opacity=op, hovertemplate="%{y:.0f} kWh",
                                 line=dict(color=STRAT_COL[n], width=width, dash=dash)))
    fig.add_hline(y=L["e_max"], line=dict(color=MUTED, width=1, dash="dot"),
                  annotation_text="full", annotation_font=dict(size=11, color=MUTED))
    fig.update_xaxes(tickformat="%H:%M")
    show(style(fig, "Energy stored in the battery", 300, "kWh"))
    st.caption("A good plan arrives at 16:00 with the battery full and empties it by 22:00. Buying too much "
               "overnight leaves no room for the midday solar, which is then exported for 7 cents. Each strategy starts "
               "the day with what it had left the night before, so on a single day a plan can beat perfect foresight; "
               "over the whole period it cannot.")

    out = pd.DataFrame({"solar_kW": w.pv, "solar_forecast_kW": w.pv_fc50, "demand_kW": w.demand,
                        "demand_forecast_kW": dplan, "price_$per_kWh": w.period.map(TARIFF),
                        "plan_import_kWh": runs["forecast plan"].imp.loc[w.index],
                        "plan_stored_kWh": runs["forecast plan"].stored.loc[w.index]}).round(2)
    st.download_button("Download this day as CSV", out.to_csv().encode(), f"battery_plan_{t0:%Y_%m_%d}.csv",
                       "text/csv", icon=":material/download:")


def _pick_day():
    sel = st.session_state.get("cal")
    pts = (sel or {}).get("selection", {}).get("points", [])
    if pts and pts[0].get("curve_number", 0) == 0:
        i = pts[0].get("point_index", pts[0].get("point_number"))
        st.session_state.day = st.session_state["cal_days"][i]


# ================================================================ page: scenario lab
def page_scenarios():
    dem_name, caution, scale = SETTINGS
    hero("Scenario lab",
         "Change the tariff, the period, and the plan settings in the sidebar. The battery rule is re-run on "
         "every hour of the period and compared with the rules that use no forecast.",
         [(f"Plan: {DEM_LABEL[dem_name]}, caution {caution:g}, {scale:g}x battery", "")])

    first, last = SIM.index.min().date(), SIM.index.max().date()
    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        period = st.slider("Period scored", first, last, (START.date(), last), format="DD MMM YYYY")
        if dem_name not in ("A3: 7 day same hour mean", "perfect demand") and pd.Timestamp(period[0]) < A4_START:
            st.caption("Before July 2024 the A4 demand models have no out of sample forecast, so the plan uses "
                       "the A3 mean there.")
    with c2:
        with st.popover("Tariff", icon=":material/payments:", width="stretch"):
            off = st.slider("Off peak, 22:00 to 06:59 ($/kWh)", 0.05, 0.40, TARIFF["offpeak"], 0.01)
            sh = st.slider("Shoulder, 07:00 to 15:59 ($/kWh)", 0.05, 0.60, TARIFF["shoulder"], 0.01)
            pk = st.slider("Peak, 16:00 to 21:59 ($/kWh)", 0.10, 0.90, TARIFF["peak"], 0.01)
            fi = st.slider("Feed in ($/kWh)", 0.0, 0.20, FEED_IN, 0.01)
        tariff = {"offpeak": off, "shoulder": sh, "peak": pk}
        st.caption(f"\\${off:.2f} off peak · \\${sh:.2f} shoulder · \\${pk:.2f} peak · \\${fi:.2f} feed in")

    mask = RECORDED & (SIM.index >= pd.Timestamp(period[0])) & (SIM.index < pd.Timestamp(period[1]) + pd.Timedelta("1D"))
    if mask.sum() < 24 * 7:
        st.warning("Choose a period of at least a week.")
        return
    runs = scenario(dem_name, caution, scale)
    table, kpi = score(runs, SIM, mask, tariff, fi)
    _, base = score(scenario(DEFAULT_DEM, CAUTION, 1.0), SIM, mask, tariff, fi)
    same = (dem_name, caution, scale) == (DEFAULT_DEM, CAUTION, 1.0)

    c = st.columns(4)
    dl = (lambda k, f: None if same else f(kpi[k] - base[k]))
    c[0].metric("Saving against no battery", f"{kpi['saving_%']:.1f}%", border=True,
                delta=dl("saving_%", lambda v: f"{v:+.1f} points vs defaults"))
    c[1].metric("Value of the forecast", f"${kpi['value_$']:,.0f}", border=True,
                delta=dl("value_$", lambda v: f"{sdollar(v)} vs defaults"))
    c[2].metric("Share of perfect foresight", f"{kpi['share_%']:.0f}%", border=True,
                delta=dl("share_%", lambda v: f"{v:+.0f} points vs defaults"))
    c[3].metric("Energy cost with the plan", f"${kpi['cost_$']:,.0f}", border=True,
                delta=dl("cost_$", lambda v: f"{sdollar(v)} vs defaults"), delta_color="inverse")

    blind = table.loc[["solar only, no forecast", "always fill overnight"], "cost_$"].min()
    perfect = table.loc["perfect foresight", "cost_$"]
    share = lambda cst: 100 * (blind - cst) / (blind - perfect)

    t1, t2, t3, t4 = st.tabs(["Solar caution", "Demand forecast", "Battery size", "All strategies"])
    with t1:
        levels = (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
        cr = caution_runs(dem_name, scale, levels)
        y = [share(cost_of(cr[l], mask, tariff, fi)) for l in levels]
        fig = go.Figure(go.Scatter(x=levels, y=y, mode="lines+markers", line=dict(color=BLUE, width=2.5),
                                   marker=dict(size=9, color=BLUE, line=dict(width=2, color="white")),
                                   hovertemplate="caution %{x}: %{y:.0f}%<extra></extra>", name="forecast plan"))
        fig.add_trace(go.Scatter(x=[caution], y=[share(kpi["cost_$"])], mode="markers", name="current setting",
                                 marker=dict(size=16, symbol="circle-open", color=INK, line=dict(width=2.5)),
                                 hoverinfo="skip"))
        fig.add_vline(x=CAUTION, line=dict(color=MUTED, dash="dot"), annotation_text="chosen on 2024 data",
                      annotation_position="bottom right", annotation_font=dict(size=11, color=MUTED))
        fig.update_xaxes(title="caution (0 = median forecast, 1 = low edge of the 80% range)", dtick=0.25)
        show(style(fig, "Share of the perfect foresight benefit by solar caution", 360, "% of perfect", hover="closest"))
        st.caption("Planning with the median trusts the forecast fully; a sunny forecast that turns cloudy then "
                   "leaves the battery short for the peak. Moving towards the low edge buys a little more overnight "
                   "as insurance. This is how the forecast uncertainty enters the decision.")
    with t2:
        dr = demand_runs(caution, scale)
        s = pd.Series({DEM_LABEL[m]: share(cost_of(dr[m], mask, tariff, fi)) for m in DEM_ORDER}).sort_values()
        cols = [BLUE if k == DEM_LABEL[dem_name] else (GREY if "hindsight" in k else BLUE_L) for k in s.index]
        fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=cols,
                               text=[f"{v:.0f}%" for v in s.values], textposition="outside",
                               hovertemplate="%{y}: %{x:.0f}%<extra></extra>"))
        fig.update_xaxes(range=[min(0, s.min() * 1.2), max(100, s.max()) * 1.12], title="% of perfect foresight benefit")
        show(style(fig, "Same solar forecast, different demand forecasts", 340, legend=False, hover="closest"))
        st.caption("Dark blue: the forecast selected in the sidebar. Grey: perfect demand, the ceiling for a "
                   "better demand model with this solar forecast.")
    with t3:
        sizes = [0.5, 1.0, 1.5, 2.0]
        res = {}
        for sz in sizes:
            tb, _ = score(scenario(dem_name, caution, sz), SIM, mask, tariff, fi)
            res[sz] = tb["saving_vs_no_battery_%"]
        res = pd.DataFrame(res).T
        fig = go.Figure([go.Bar(x=[f"{sz:g}x ({sz * BATT['capacity_kwh']:.0f} kWh)" for sz in sizes], y=res[n],
                                name=n, marker_color=STRAT_COL[n], hovertemplate="%{y:.1f}%")
                         for n in ["solar only, no forecast", "always fill overnight", "forecast plan", "perfect foresight"]])
        show(style(fig, "Saving against no battery by battery size", 360, "%"))
        st.caption("Power grows with size. A bigger battery saves more, and the gap between the forecast plan and "
                   "the simple rules shows what the forecast is worth at each size.")
    with t4:
        show_t = table.copy()
        show_t.insert(1, "share_of_perfect_%", [share(v) if k not in ("no battery",) else np.nan
                                                 for k, v in show_t["cost_$"].items()])
        st.dataframe(show_t.round(1), column_config={
            "cost_$": st.column_config.NumberColumn("Cost ($)", format="$%.0f"),
            "share_of_perfect_%": st.column_config.ProgressColumn("Share of perfect", format="%.0f%%",
                                                                  min_value=0, max_value=100),
            "saving_vs_no_battery_%": st.column_config.NumberColumn("Saving vs no battery", format="%.1f%%")})
        st.download_button("Download scenario as CSV", show_t.round(2).to_csv().encode(), "scenario_results.csv",
                           "text/csv", icon=":material/download:")


# ================================================================ page: forecast models
def page_models():
    hero("Demand forecast models",
         "Five ways to forecast tomorrow's demand, each refitted monthly and tested only on months it had not seen.",
         [("Walk forward, monthly refits", ""), (f"{A4_START:%d %b %Y} to {SIM.index.max():%d %b %Y}", "")])
    if D["models"] is None or DEM is None:
        st.info("Run notebook 07 to compare the demand models.")
        return

    tab = D["models"]["planning hours 07 to 15"].copy()
    best = tab["MAE_kW"].idxmin()
    c = st.columns(3)
    c[0].metric("Best model", DEM_LABEL.get(best, best).replace(" (A4)", ""), border=True)
    c[1].metric("Its error, planning hours", f"{tab.loc[best, 'MAE_kW']:.1f} kW", border=True,
                delta=f"{tab.loc[best, 'MAE_kW'] - tab.loc['A3: 7 day same hour mean', 'MAE_kW']:.1f} kW vs A3",
                delta_color="inverse")
    c[2].metric("Error reduction against A3", f"{tab.loc[best, 'MAE_vs_A3_%']:.0f}%", border=True)

    st.dataframe(tab.rename(index=DEM_LABEL), column_config={
        "MAE_kW": st.column_config.NumberColumn("MAE (kW)", format="%.1f"),
        "RMSE_kW": st.column_config.NumberColumn("RMSE (kW)", format="%.1f"),
        "bias_kW": st.column_config.NumberColumn("Bias (kW)", format="%.1f"),
        "MAE_vs_A3_%": st.column_config.ProgressColumn("Better than A3", format="%.0f%%", min_value=0, max_value=100)})

    kind = st.segmented_control("Days", ["All days", "Weekdays", "Weekends"], default="All days", key="kind") or "All days"
    d = DEM if kind == "All days" else DEM[(DEM.index.dayofweek >= 5) == (kind == "Weekends")]
    order = [m for m in MODEL_COL if m in d.columns]
    err = d[order].sub(d.actual, axis=0).abs()

    left, right = st.columns(2, gap="medium")
    with left:
        by_h = err.groupby(err.index.hour).mean()
        fig = go.Figure([go.Scatter(x=by_h.index, y=by_h[m], name=DEM_LABEL[m], hovertemplate="%{y:.1f} kW",
                                    line=dict(color=MODEL_COL[m], width=3 if m == "gradient boosting" else 2))
                         for m in order])
        fig.add_vrect(x0=6.5, x1=15.5, fillcolor=BLUE, opacity=.05, line_width=0, annotation_text="planning hours",
                      annotation_position="top left", annotation_font=dict(size=11, color=MUTED))
        fig.update_xaxes(dtick=3, title="hour of day")
        fig.update_layout(margin=dict(b=70))
        show(style(fig, f"Error by hour of day, {kind.lower()}", 420, "MAE (kW)", legend=False))
    with right:
        plan_h = (err.index.hour >= 7) & (err.index.hour <= 15)
        by_m = err[plan_h].resample("MS").mean()
        fig = go.Figure([go.Scatter(x=by_m.index, y=by_m[m], name=DEM_LABEL[m], mode="lines+markers",
                                    marker=dict(size=6), hovertemplate="%{y:.1f} kW",
                                    line=dict(color=MODEL_COL[m], width=3 if m == "gradient boosting" else 2))
                         for m in order])
        fig.update_xaxes(dtick="M2", tickformat="%b<br>%Y")
        show(style(fig, f"Error by month, planning hours, {kind.lower()}", 420, "MAE (kW)", where="bottom"))

    weeks = pd.Series(DEM.index.normalize().unique())
    mondays = list(weeks[weeks.dt.dayofweek == 0].dt.date)
    start = st.select_slider("Week starting", options=mondays, value=date(2025, 5, 19) if date(2025, 5, 19) in mondays
                             else mondays[-1], format_func=lambda x: f"{x:%d %b %Y}")
    pick = st.pills("Models to show", order, default=["A3: 7 day same hour mean", "gradient boosting"],
                    selection_mode="multi", format_func=DEM_LABEL.get)
    w = DEM.loc[pd.Timestamp(start): pd.Timestamp(start) + pd.Timedelta("167h")]
    fig = go.Figure(go.Scatter(x=w.index, y=w.actual, name="actual demand", line=dict(color=INK, width=3)))
    for m in order:
        if m in (pick or []):
            fig.add_trace(go.Scatter(x=w.index, y=w[m], name=DEM_LABEL[m], line=dict(color=MODEL_COL[m], width=2, dash="dot")))
    fig.update_traces(hovertemplate="%{y:.0f} kW")
    show(style(fig, f"Week of {pd.Timestamp(start):%d %b %Y}", 380, "kW"))
    st.caption("The A3 mean of the last 7 days expects weekday demand on Saturdays and Sundays, when the site is "
               "mostly closed. The A4 models know the day of the week, which is most of their gain.")


# ================================================================ page: system health
def page_health():
    ok, htxt = health()
    hero("System health",
         "Daily checks that the solar forecast is still accurate and its 80% range still holds 80% of outcomes, "
         "a drift check on the input data, and the retraining rule.",
         [(("✓ " if ok else "⚠ ") + htxt, "ok" if ok else "bad")] if ok is not None else [])
    if MON is None:
        st.info("Run notebook 08 to build the monitoring table.")
        return
    m = MON.dropna(subset=["nmae"])
    last = m.iloc[-1]
    md = D["mon_md"] or ""
    lim = float(re.search(r"above ([0-9.]+)", md).group(1)) if re.search(r"above ([0-9.]+)", md) else None
    alert_days = m.index[m.alert_error | m.alert_coverage]
    since = (m.index[-1] - alert_days[-1]).days if len(alert_days) else None

    if ok:
        st.success(f"**Within limits** on {m.index[-1]:%d %b %Y}. No action needed; the next scheduled demand "
                   "model refit is on the first of the month.", icon=":material/check_circle:")
    else:
        st.error("**Alert.** Review recent forecasts, check the data feed for drift, and retrain if the alert "
                 "persists.", icon=":material/error:")

    c = st.columns(4)
    c[0].metric("Latest check", f"{m.index[-1]:%d %b %Y}", border=True)
    c[1].metric("30 day interval coverage", f"{last.coverage:.0%}", border=True,
                help="Share of daylight hours inside the calibrated 80% range. Accepted 70% to 90%.",
                chart_data=list(m.coverage.iloc[-90:].round(3)))
    c[2].metric("30 day normalised error", f"{last.nmae:.3f}", border=True,
                help=f"Mean absolute error over mean output. Alert above {lim}." if lim else None,
                chart_data=list(m.nmae.iloc[-90:].round(3)))
    c[3].metric("Days since last alert", f"{since}" if since is not None else "none", border=True)

    rs = dict(buttons=[dict(count=3, label="3 m", step="month", stepmode="backward"),
                       dict(count=1, label="1 y", step="year", stepmode="backward"),
                       dict(count=2, label="2 y", step="year", stepmode="backward"),
                       dict(step="all", label="all")], bgcolor="#f3f2ef", activecolor=BLUE_L, x=0, y=1.02,
              font=dict(size=11))
    x0 = m.index[-1] - pd.DateOffset(years=2)

    fig = go.Figure()
    fig.add_hrect(y0=.70, y1=.90, fillcolor=GOOD, opacity=.06, line_width=0)
    fig.add_hline(y=.80, line=dict(color=MUTED, dash="dot", width=1), annotation_text="target 80%",
                  annotation_font=dict(size=11, color=MUTED))
    fig.add_trace(go.Scatter(x=m.index, y=m.coverage, name="30 day coverage", line=dict(color=BLUE, width=2),
                             hovertemplate="%{y:.1%}"))
    al = m[m.alert_coverage]
    fig.add_trace(go.Scatter(x=al.index, y=al.coverage, mode="markers", name="coverage alert",
                             marker=dict(color=CRITICAL, size=6, symbol="x"), hovertemplate="alert %{y:.1%}"))
    fig.update_xaxes(rangeselector=rs, range=[x0, m.index[-1]])
    fig.update_yaxes(tickformat=".0%")
    show(style(fig, "Coverage of the 80% forecast range", 340, where="right"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=m.index, y=m.nmae, name="30 day normalised error", line=dict(color=BLUE, width=2),
                             hovertemplate="%{y:.3f}"))
    if lim:
        fig.add_hline(y=lim, line=dict(color=CRITICAL, dash="dash", width=1),
                      annotation_text=f"alert limit {lim}", annotation_font=dict(size=11, color=CRITICAL))
    ae = m[m.alert_error]
    fig.add_trace(go.Scatter(x=ae.index, y=ae.nmae, mode="markers", name="error alert",
                             marker=dict(color=CRITICAL, size=6, symbol="x"), hovertemplate="alert %{y:.3f}"))
    fig.update_xaxes(rangeselector=rs, range=[x0, m.index[-1]])
    show(style(fig, "Forecast error, 24 h ahead, daylight hours", 340, where="right"))
    st.caption("Limits fixed on 2019 to 2020 and never refitted, so a slow decline in accuracy cannot hide inside "
               "a moving baseline.")

    left, right = st.columns([3, 2], gap="medium")
    with left:
        rt = D["retrain"]
        if rt is not None:
            rt = rt.sort_values("planning_MAE_kW", ascending=False)
            cols = {"static": GREY_D, "scheduled monthly": BLUE}
            fig = go.Figure(go.Bar(x=rt.planning_MAE_kW, y=rt.index, orientation="h",
                                   marker_color=[cols.get(i, ORANGE) for i in rt.index],
                                   text=[f"{v:.1f} kW · {int(f)} fits" for v, f in zip(rt.planning_MAE_kW, rt.model_fits)],
                                   textposition="outside", hovertemplate="%{y}: %{x:.1f} kW<extra></extra>"))
            fig.update_xaxes(range=[0, rt.planning_MAE_kW.max() * 1.45], title="planning hour MAE (kW)")
            show(style(fig, "Demand model retraining strategies", 280, legend=False, hover="closest"))
            st.markdown('<p class="note">Never retraining nearly doubles the error within a year. Monthly refits '
                        'give the lowest error; retraining only when the error rises 15% above its baseline needs '
                        'three fits instead of fourteen for a few kW more. Monthly is the operating choice.</p>',
                        unsafe_allow_html=True)
    with right:
        st.markdown("##### Data drift")
        drift = re.search(r"## 2\. Data drift check\n(.*?)\n\n", md, re.S)
        st.markdown(f'<p class="note">{drift.group(1).replace(chr(10), " ") if drift else "See notebook 08."}</p>',
                    unsafe_allow_html=True)
        if D["alerts"] is not None:
            a = D["alerts"].sort_values("start", ascending=False)
            kinds = st.pills("Alert type", sorted(a.type.unique()), selection_mode="multi", key="akind")
            a = a[a.type.isin(kinds)] if kinds else a
            st.dataframe(a, hide_index=True, height=230, column_config={
                "start": st.column_config.TextColumn("start", width="small"),
                "end": st.column_config.TextColumn("end", width="small"),
                "days": st.column_config.ProgressColumn("days", format="%d", min_value=0, max_value=int(a.days.max() or 1))})
    img = OUT / "Notebook_Figures" / "fig18_drift_retraining.png"
    if img.exists():
        with st.expander("Figure 18: drift check and retraining strategies"):
            st.image(str(img))


# ================================================================ page: data and pipeline
FILES = [("Datasets/processed/dispatch_hourly.parquet", "06", "Hourly solar, demand, forecasts, tariff, A3 plans"),
         ("Datasets/processed/forecasts_calibrated.parquet", "06", "Solar forecasts with calibrated 80% range"),
         ("Datasets/processed/demand_forecasts.parquet", "07", "Out of sample demand forecasts, five models"),
         ("Datasets/processed/monitoring_daily.parquet", "08", "Daily forecast error and coverage with alerts"),
         ("Outputs/Results/dispatch_strategies.csv", "06", "A3 strategy comparison"),
         ("Outputs/Results/demand_model_comparison.csv", "07", "Demand model accuracy"),
         ("Outputs/Results/demand_model_results.md", "07", "Demand model and battery plan summary"),
         ("Outputs/Results/monitoring_results.md", "08", "Monitoring, drift and retraining summary"),
         ("Outputs/Results/monitoring_alerts.csv", "08", "Alert episodes")]


@st.cache_data
def inventory():
    rows = []
    for rel, nb, what in FILES:
        p = REPO / rel
        n = None
        if p.exists() and p.suffix == ".parquet":
            n = len(pd.read_parquet(p, columns=[]))
        elif p.exists() and p.suffix == ".csv":
            n = len(pd.read_csv(p))
        rows.append({"file": rel, "notebook": nb, "contents": what, "found": p.exists(), "rows": f"{n:,}" if n is not None else "",
                     "size_kB": round(p.stat().st_size / 1024) if p.exists() else None,
                     "updated": pd.Timestamp(p.stat().st_mtime, unit="s").strftime("%d %b %Y %H:%M") if p.exists() else ""})
    return pd.DataFrame(rows)


def page_data():
    hero("Data and pipeline",
         "Where every number on this dashboard comes from, how fresh it is, and how it would run each night in "
         "operation.", [(f"Latest data {SIM.index.max():%d %b %Y %H:%M}", "")])
    st.graphviz_chart("""
    digraph {
      rankdir=LR; bgcolor="transparent"; nodesep=.25; ranksep=.35;
      node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=13 color="#d9d8d2" fillcolor="white" fontcolor="#1f1f1e" margin="0.14,0.07"];
      edge [color="#8f8e88" arrowsize=.6];
      raw [label="DKASC raw data\\n5 minute CSV, 2008 to 2025" fillcolor="#f3f2ef"];
      n13 [label="01 to 03\\nprofile, ingest, clean"]; n4 [label="04\\nfeatures"];
      n5 [label="05\\nsolar models"]; n6 [label="06\\ncalibration and\\nbattery plan"];
      n7 [label="07\\ndemand models"]; n8 [label="08\\nmonitoring and\\nretraining"];
      out [label="Datasets/processed\\nOutputs" fillcolor="#f3f2ef"];
      dash [label="Dashboard\\n(this app)" fillcolor="#2a78d6" fontcolor="white" color="#2a78d6"];
      raw -> n13 -> n4 -> n5 -> n6 -> n7 -> n8 -> out -> dash;
    }""", width="stretch")

    inv = inventory()
    st.dataframe(inv, hide_index=True, column_config={
        "found": st.column_config.CheckboxColumn("found"),
        "size_kB": st.column_config.NumberColumn("size (kB)", format="%d")})
    if not inv.found.all():
        st.warning("Some outputs are missing. Run the notebooks named in the table, in order.")

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("##### Nightly run in operation")
        st.dataframe(pd.DataFrame({
            "time": ["21:00", "21:15", "21:30", "22:00", "1st of month", "on alert"],
            "step": ["Load today's meter data and tomorrow's weather", "Solar forecast with calibrated 80% range",
                     "Demand forecast, monitoring checks, drift check", "Battery plan: grid energy to buy tonight",
                     "Refit the demand model on all history", "Review, and retrain early if the alert persists"]}),
            hide_index=True)
    with right:
        st.markdown("##### Reproduce these outputs")
        st.code("# from the repository root, raw CSVs in Datasets/raw\n"
                "jupyter nbconvert --to notebook --execute \\\n"
                "    --inplace notebooks/0*.ipynb\n"
                "streamlit run dashboard/app.py", language="bash")
        st.markdown('<p class="note">Raw data stays outside git (see .gitignore). The dashboard only reads the '
                    'processed files, so it holds no personal data and needs no credentials.</p>',
                    unsafe_allow_html=True)


# ================================================================ navigation
SETTINGS = plan_settings()
nav = st.navigation({
    "Decide": [st.Page(page_overview, title="Overview", icon=":material/dashboard:", default=True),
               st.Page(page_day, title="Battery plan by day", icon=":material/battery_charging_full:"),
               st.Page(page_scenarios, title="Scenario lab", icon=":material/tune:")],
    "Evidence": [st.Page(page_models, title="Forecast models", icon=":material/query_stats:"),
                 st.Page(page_health, title="System health", icon=":material/monitor_heart:"),
                 st.Page(page_data, title="Data and pipeline", icon=":material/account_tree:")]})
nav.run()
