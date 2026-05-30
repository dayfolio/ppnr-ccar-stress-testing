import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
import os, json 
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

OUTPUT_DIR = "./ppnr_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

from data.macro_history import generate_macro_history
from data.financials import generate_financials
from models.satellite_models import fit_satellite_models
from models.validation import validate_oos
from scenarios.ccar_scenarios import CCAR_SCENARIOS
from scenarios.forecasting import forecast_ppnr
from analytics.sensitivity import sensitivity_analysis
from reporting.charts import plot_all

def run():
    print("Generating macro history and bank financials...")
    macro_hist = generate_macro_history(n_quarters=56)
    fin_hist   = generate_financials(macro_hist)

    def fmt_q(ts):
        return f"{ts.year}Q{ts.quarter}"
    print(f"Historical sample: {fmt_q(macro_hist.index[0])} – {fmt_q(macro_hist.index[-1])}")
    print(f"Mean PPNR: ${fin_hist['ppnr'].mean():.2f}B/quarter | "
          f"Mean NIM proxy: {(fin_hist['nii'] / fin_hist['loan_bal'] * 400).mean():.2f}%")

    # Fit satellite models
    print("\nFitting satellite models...")
    satellite_models, model_df = fit_satellite_models(macro_hist, fin_hist)

    # OOS validation
    print("\n" + "="*60)
    print("OUT-OF-SAMPLE VALIDATION (Train: 2008–2017 | Test: 2018–2021)")
    print("="*60)
    val_results = validate_oos(macro_hist, fin_hist)

    # CCAR scenario forecasts
    print("\n" + "="*60)
    print("9-QUARTER CCAR SCENARIO FORECASTS")
    print("="*60)
    forecasts = forecast_ppnr(CCAR_SCENARIOS, satellite_models, fin_hist)

    for sc_name, fc in forecasts.items():
        cum = fc["ppnr"].sum()
        min_q = fc["ppnr"].min()
        print(f"\n  {sc_name}:")
        print(f"    Cumulative 9Q PPNR: ${cum:.2f}B")
        print(f"    Trough quarter PPNR: ${min_q:.2f}B")
        print(f"    {'Quarter':<12} {'NII':>8} {'NIINC':>8} {'NIE':>8} {'PPNR':>8}")
        for i, (idx, row) in enumerate(fc.iterrows()):
            print(f"    {str(idx.date()):<12} {row['nii']:>8.2f} {row['niinc']:>8.2f} "
                  f"{row['nie']:>8.2f} {row['ppnr']:>8.2f}")

    # Sensitivity analysis
    print("\n" + "="*60)
    print("SENSITIVITY ANALYSIS (±1SD, 9Q Cumulative PPNR Impact)")
    print("="*60)
    sens_df = sensitivity_analysis(CCAR_SCENARIOS, satellite_models, fin_hist, macro_hist)
    for driver, impact in sens_df.items():
        print(f"  {driver:<28} {impact:>+.3f}B")

    # Save outputs
    fin_hist.to_csv(f"{OUTPUT_DIR}/historical_financials.csv")
    macro_hist.to_csv(f"{OUTPUT_DIR}/macro_history.csv")
    for sc_name, fc in forecasts.items():
        fc.to_csv(f"{OUTPUT_DIR}/forecast_{sc_name.replace(' ','_').lower()}.csv")
    sens_df.to_csv(f"{OUTPUT_DIR}/sensitivity.csv", header=["PPNR_Impact_USD_Bn"])

    # Model diagnostics to JSON
    diagnostics = {}
    for name, res in satellite_models.items():
        diagnostics[name] = {
            "r2": res["r2"], "adj_r2": res["adj_r2"],
            "dw": res["dw"], "rmse": res["rmse"],
            "params": res["params"].to_dict(),
            "pvalues": res["pvalues"].to_dict(),
        }
    diagnostics["oos_validation"] = {
        k: {"rmse": v["rmse"], "mae": v["mae"],
            "mape": v["mape"], "theils_u": v["theils_u"], "corr": v["corr"]}
        for k, v in val_results.items()
    }
    diagnostics["cumulative_ppnr"] = {
        sc: float(fc["ppnr"].sum()) for sc, fc in forecasts.items()
    }
    json.dump(diagnostics, open(f"{OUTPUT_DIR}/model_diagnostics.json", "w"), indent=2)

    # Charts
    plot_all(macro_hist, fin_hist, forecasts, val_results, sens_df, satellite_models)
    print(f"\nAll outputs saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    run()