import numpy as np
import pandas as pd
import statsmodels.api as sm
import os, json
OUTPUT_DIR = "./ppnr_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# ─────────────────────────────────────────────────────────────
#    MODEL VALIDATION
#    Out-of-sample backtest: train on 2008Q1–2017Q4 (40Q),
#    test on 2018Q1–2021Q4 (16Q)
#    Metrics: RMSE, MAE, MAPE, Theil's U
# ─────────────────────────────────────────────────────────────

def validate_oos(macro_hist, fin_hist):
    """Out-of-sample validation via rolling window backtest."""
    df = pd.concat([macro_hist, fin_hist], axis=1).dropna()
    df["lag_nii"]   = df["nii"].shift(1)
    df["lag_niinc"] = df["niinc"].shift(1)
    df["total_rev"] = df["nii"] + df["niinc"]
    df = df.dropna()

    train_end = 40   # 2008Q1–2017Q4
    train = df.iloc[:train_end]
    test  = df.iloc[train_end:]

    val_results = {}

    for component, features, target in [
        ("NII",   ["fed_funds","term_spread","loan_growth","lag_nii"],    "nii"),
        ("NIINC", ["gdp_growth","vix","fed_funds","hpi_growth"],          "niinc"),
        ("NIE",   ["total_rev","unemp_rate","gdp_growth"],                "nie"),
    ]:
        X_tr = sm.add_constant(train[features])
        X_te = sm.add_constant(test[features])
        mod  = sm.OLS(train[target], X_tr).fit()
        pred = mod.predict(X_te)
        actual = test[target].values
        pred   = pred.values

        rmse  = np.sqrt(np.mean((actual - pred)**2))
        mae   = np.mean(np.abs(actual - pred))
        mape  = np.mean(np.abs((actual - pred) / actual)) * 100
        # Theil's U: <1 = beats naive forecast
        naive = np.roll(actual, 1)[1:]
        theils_u = np.sqrt(np.mean((actual[1:] - pred[1:])**2)) / \
                   np.sqrt(np.mean((actual[1:] - naive)**2))
        corr = np.corrcoef(actual, pred)[0, 1]

        val_results[component] = {
            "rmse": rmse, "mae": mae, "mape": mape,
            "theils_u": theils_u, "corr": corr,
            "actual": actual, "predicted": pred,
            "test_index": test.index,
        }
        print(f"  {component:<6} OOS — RMSE: ${rmse:.3f}B  MAE: ${mae:.3f}B  "
              f"MAPE: {mape:.1f}%  Theil's U: {theils_u:.3f}  Corr: {corr:.3f}")

    return val_results
