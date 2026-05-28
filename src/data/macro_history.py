import numpy as np
import pandas as pd

# ─────────────────────────────────────────────────────────────
#    MACRO DRIVER HISTORY  (2008Q1 – 2021Q4, 56 quarters)
#
#    Drivers calibrated to US macro history:
#    fed_funds    : Federal Funds Rate (%)
#    term_spread  : 10Y–2Y Treasury spread (%) — yield curve slope
#    gdp_growth   : Real GDP growth YoY (%)
#    unemp_rate   : Unemployment rate (%)
#    vix          : Equity volatility index (proxy)
#    hpi_growth   : House Price Index growth YoY (%)
#    loan_growth  : Total loan portfolio growth YoY (%)
# ─────────────────────────────────────────────────────────────

def generate_macro_history(n_quarters=56, seed=42):
    np.random.seed(seed)
    quarters = pd.date_range("2008-01-01", periods=n_quarters, freq="QS")

    # Fed Funds: GFC cut → ZLB → hike cycle → COVID cut
    fed_funds = np.concatenate([
        np.linspace(4.5, 0.25, 7),       # GFC: Q1 2008 – Q3 2009 (7Q)
        np.ones(25) * 0.13,              # ZLB: Q4 2009 – Q4 2015 (25Q)
        np.linspace(0.25, 2.40, 13),     # Hike: Q1 2016 – Q1 2019 (13Q)
        np.linspace(2.40, 1.75, 4),      # Cut: Q2 2019 – Q1 2020 (4Q)
        np.ones(7)  * 0.09,              # COVID ZLB: Q2 2020-Q4 2021 (7Q)
    ])[:n_quarters]
    fed_funds += np.random.normal(0, 0.05, n_quarters)
    fed_funds  = np.clip(fed_funds, 0.05, 6.0)

    # Term spread: mean-reverting around 1.5%, flatter/inverted in hiking cycles
    term_spread = 1.5 - 0.3 * fed_funds + np.random.normal(0, 0.25, n_quarters)
    term_spread = np.clip(term_spread, -0.5, 3.5)

    # GDP growth: GFC recession, recovery, COVID shock
    gdp_base = np.concatenate([
        np.linspace(1.5, -4.0, 6),     # GFC contraction
        np.linspace(-4.0, 2.5, 8),     # Recovery
        np.ones(30) * 2.3,             # Expansion
        np.array([-2.5, -9.0, 4.0, 6.5, 5.5, 4.0, 3.5, 3.0, 2.5, 2.0, 2.0, 2.0]),  # COVID
    ])[:n_quarters]
    gdp_growth = gdp_base + np.random.normal(0, 0.4, n_quarters)

    # Unemployment: GFC spike → long recovery → COVID spike
    unemp_base = np.concatenate([
        np.linspace(5.0, 10.0, 6),
        np.linspace(10.0, 4.7, 38),
        np.array([3.5, 3.5, 14.7, 8.4, 6.7, 6.0, 5.8, 5.4, 4.6, 4.2, 4.0, 3.9]),
    ])[:n_quarters]
    unemp_rate = np.clip(unemp_base + np.random.normal(0, 0.15, n_quarters), 3.4, 15.0)

    # VIX: elevated in crises, low in calm markets
    vix_base = np.concatenate([
        np.array([24, 32, 45, 55, 40, 28, 25, 22, 20, 18, 17, 16]),
        np.ones(28) * 14,
        np.array([14, 16, 18, 15, 13, 12, 14, 16]),
        np.array([16, 18, 45, 26, 22, 20, 18, 17, 16, 15, 17, 18]),
    ])[:n_quarters]
    vix = np.clip(vix_base + np.random.normal(0, 1.5, n_quarters), 10, 60)

    # HPI growth: housing boom-bust-recovery
    hpi_base = np.concatenate([
        np.linspace(3.0, -12.0, 10),
        np.linspace(-12.0, 0.0, 6),
        np.linspace(0.0, 8.0, 24),
        np.array([6.0, 6.5, 5.5, 4.5, 5.0, 6.0, 7.0, 8.5, 9.0, 9.5, 10.5, 11.0, 12.0, 13.0, 14.0, 15.0]),
    ])[:n_quarters]
    hpi_growth = hpi_base + np.random.normal(0, 0.5, n_quarters)

    # Loan growth: pro-cyclical
    loan_growth = 0.4 * gdp_growth + 0.3 * hpi_growth - 0.5 * unemp_rate + \
                  3.0 + np.random.normal(0, 0.8, n_quarters)
    loan_growth = np.clip(loan_growth, -8, 15)

    return pd.DataFrame({
        "quarter":      quarters,
        "fed_funds":    fed_funds,
        "term_spread":  term_spread,
        "gdp_growth":   gdp_growth,
        "unemp_rate":   unemp_rate,
        "vix":          vix,
        "hpi_growth":   hpi_growth,
        "loan_growth":  loan_growth,
    }).set_index("quarter")

