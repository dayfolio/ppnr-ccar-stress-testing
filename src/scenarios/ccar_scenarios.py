import pandas as pd

# ─────────────────────────────────────────────────────────────
#  CCAR MACRO SCENARIOS (9-quarter horizon: 2022Q1–2024Q1)
#
#  Baseline:         Moderate growth, gradual rate normalisation
#  Adverse:          Mild recession, rates cut, unemployment rises
#  Severely Adverse: Severe recession (GFC-scale), zero rates,
#                    high unemployment, market stress
#
#  Fed CCAR scenario structure — key variables:
#    fed_funds, term_spread, gdp_growth, unemp_rate, vix,
#    hpi_growth, loan_growth
# ─────────────────────────────────────────────────────────────

SCENARIO_QUARTERS = pd.date_range("2022-01-01", periods=9, freq="QS")

CCAR_SCENARIOS = {
    "Baseline": pd.DataFrame({
        "quarter":     SCENARIO_QUARTERS,
        "fed_funds":   [2.50, 3.00, 3.50, 3.75, 4.00, 3.75, 3.50, 3.25, 3.00],
        "term_spread": [0.80, 0.70, 0.60, 0.55, 0.50, 0.55, 0.60, 0.65, 0.70],
        "gdp_growth":  [2.20, 2.10, 2.00, 1.90, 1.80, 2.00, 2.10, 2.20, 2.30],
        "unemp_rate":  [3.90, 3.90, 4.00, 4.00, 4.10, 4.10, 4.00, 3.90, 3.80],
        "vix":         [18.0, 17.0, 17.0, 16.0, 16.0, 15.0, 15.0, 14.0, 14.0],
        "hpi_growth":  [8.00, 6.00, 4.50, 3.50, 3.00, 3.00, 3.50, 4.00, 4.50],
        "loan_growth": [7.00, 6.50, 6.00, 5.50, 5.00, 5.00, 5.50, 6.00, 6.50],
    }).set_index("quarter"),

    "Adverse": pd.DataFrame({
        "quarter":     SCENARIO_QUARTERS,
        "fed_funds":   [2.00, 1.50, 1.00, 0.50, 0.25, 0.25, 0.50, 0.75, 1.00],
        "term_spread": [0.50, 0.40, 0.30, 0.20, 0.15, 0.20, 0.25, 0.30, 0.40],
        "gdp_growth":  [1.00, -0.5, -1.5, -2.0, -1.5, -0.5,  0.5,  1.0,  1.5],
        "unemp_rate":  [4.50, 5.20, 6.00, 6.80, 7.20, 7.00, 6.50, 6.00, 5.50],
        "vix":         [24.0, 30.0, 34.0, 32.0, 28.0, 25.0, 22.0, 20.0, 18.0],
        "hpi_growth":  [4.00, 1.00, -2.0, -4.0, -4.5, -3.0, -1.0,  0.5,  2.0],
        "loan_growth": [4.00, 2.00, -1.0, -3.0, -4.0, -3.0, -1.0,  1.0,  3.0],
    }).set_index("quarter"),

    "Severely Adverse": pd.DataFrame({
        "quarter":     SCENARIO_QUARTERS,
        "fed_funds":   [1.00, 0.25, 0.10, 0.10, 0.10, 0.10, 0.10, 0.25, 0.50],
        "term_spread": [0.20, 0.10, 0.05, 0.05, 0.05, 0.10, 0.15, 0.20, 0.30],
        "gdp_growth":  [-0.5, -3.0, -5.0, -6.5, -5.0, -3.0, -1.0,  0.5,  1.5],
        "unemp_rate":  [5.50, 7.50, 9.50,11.00,12.00,11.50,10.50, 9.50, 8.50],
        "vix":         [35.0, 52.0, 58.0, 50.0, 42.0, 35.0, 28.0, 24.0, 20.0],
        "hpi_growth":  [2.00, -3.0, -8.0,-12.0,-14.0,-12.0, -8.0, -4.0, -1.0],
        "loan_growth": [2.00, -2.0, -6.0, -9.0,-10.0, -8.0, -5.0, -2.0,  0.5],
    }).set_index("quarter"),
}
