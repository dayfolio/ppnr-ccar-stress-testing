import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

# ─────────────────────────────────────────────────────────────
#    SATELLITE MODELS - OLS REGRESSION
#    Each component modelled as a satellite (sub-model)
#    consistent with Fed SR 15-18 PPNR guidance.
#
#  NII model:   nii   ~ fed_funds + term_spread + loan_growth + lag_nii
#  NIINC model: niinc ~ gdp_growth + vix + fed_funds + hpi_growth
#  NIE model:   nie   ~ nii + niinc + unemp_rate + gdp_growth
# ─────────────────────────────────────────────────────────────

def fit_satellite_models(macro_hist, fin_hist):
    """Fit OLS satellite models. Returns fitted models and diagnostics."""
    df = pd.concat([macro_hist, fin_hist], axis=1).dropna()

    # Lag features
    df["lag_nii"]   = df["nii"].shift(1)
    df["lag_niinc"] = df["niinc"].shift(1)
    df = df.dropna()

    results = {}

    # ── NII model
    X_nii = sm.add_constant(df[["fed_funds", "term_spread", "loan_growth", "lag_nii"]])
    mod_nii = sm.OLS(df["nii"], X_nii).fit()
    results["nii"] = {
        "model": mod_nii,
        "features": ["fed_funds", "term_spread", "loan_growth", "lag_nii"],
        "r2": mod_nii.rsquared,
        "adj_r2": mod_nii.rsquared_adj,
        "dw": durbin_watson(mod_nii.resid),
        "rmse": np.sqrt(np.mean(mod_nii.resid**2)),
        "params": mod_nii.params,
        "pvalues": mod_nii.pvalues,
        "tvalues": mod_nii.tvalues,
    }

    # ── NIINC model
    X_niinc = sm.add_constant(df[["gdp_growth", "vix", "fed_funds", "hpi_growth"]])
    mod_niinc = sm.OLS(df["niinc"], X_niinc).fit()
    results["niinc"] = {
        "model": mod_niinc,
        "features": ["gdp_growth", "vix", "fed_funds", "hpi_growth"],
        "r2": mod_niinc.rsquared,
        "adj_r2": mod_niinc.rsquared_adj,
        "dw": durbin_watson(mod_niinc.resid),
        "rmse": np.sqrt(np.mean(mod_niinc.resid**2)),
        "params": mod_niinc.params,
        "pvalues": mod_niinc.pvalues,
        "tvalues": mod_niinc.tvalues,
    }

    # ── NIE model (revenue-driven + macro)
    df["total_rev"] = df["nii"] + df["niinc"]
    X_nie = sm.add_constant(df[["total_rev", "unemp_rate", "gdp_growth"]])
    mod_nie = sm.OLS(df["nie"], X_nie).fit()
    results["nie"] = {
        "model": mod_nie,
        "features": ["total_rev", "unemp_rate", "gdp_growth"],
        "r2": mod_nie.rsquared,
        "adj_r2": mod_nie.rsquared_adj,
        "dw": durbin_watson(mod_nie.resid),
        "rmse": np.sqrt(np.mean(mod_nie.resid**2)),
        "params": mod_nie.params,
        "pvalues": mod_nie.pvalues,
        "tvalues": mod_nie.tvalues,
    }

    print("\n" + "="*60)
    print("SATELLITE MODEL DIAGNOSTICS")
    print("="*60)
    for name, res in results.items():
        print(f"\n{name.upper()} Model:")
        print(f"  R²={res['r2']:.4f}  Adj-R²={res['adj_r2']:.4f}  "
              f"RMSE=${res['rmse']:.3f}B  DW={res['dw']:.3f}")
        print(f"  {'Feature':<18} {'Coef':>8} {'t-stat':>8} {'p-value':>8}")
        for feat in res["params"].index:
            sig = "***" if res["pvalues"][feat] < 0.01 else \
                  "**"  if res["pvalues"][feat] < 0.05 else \
                  "*"   if res["pvalues"][feat] < 0.10 else ""
            print(f"  {feat:<18} {res['params'][feat]:>8.4f} "
                  f"{res['tvalues'][feat]:>8.3f} {res['pvalues'][feat]:>8.4f} {sig}")

    return results, df

