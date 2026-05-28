import pandas as pd

from scenarios.forecasting import forecast_ppnr

# ─────────────────────────────────────────────────────────────
#    SENSITIVITY ANALYSIS
#    Measure PPNR change from ±1 standard deviation shock
#    to each macro driver, holding others constant at Baseline
# ─────────────────────────────────────────────────────────────

def sensitivity_analysis(scenarios, satellite_models, fin_hist, macro_hist):
    """1-SD shock to each macro driver; measure 9Q cumulative PPNR impact."""
    base_forecasts = forecast_ppnr(
        {"Baseline": scenarios["Baseline"]}, satellite_models, fin_hist)
    base_ppnr_cum = base_forecasts["Baseline"]["ppnr"].sum()

    drivers     = ["fed_funds","term_spread","gdp_growth","unemp_rate","vix","hpi_growth","loan_growth"]
    sensitivities = {}

    for driver in drivers:
        sd = macro_hist[driver].std()
        for direction, sign in [("+1SD", 1), ("-1SD", -1)]:
            shocked_sc = scenarios["Baseline"].copy()
            shocked_sc[driver] = shocked_sc[driver] + sign * sd
            shocked_fc = forecast_ppnr(
                {direction: shocked_sc}, satellite_models, fin_hist)
            shocked_ppnr_cum = shocked_fc[direction]["ppnr"].sum()
            sensitivities[f"{driver} {direction}"] = shocked_ppnr_cum - base_ppnr_cum

    sens_df = pd.Series(sensitivities).sort_values()
    return sens_df
