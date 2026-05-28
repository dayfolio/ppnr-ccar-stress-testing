import pandas as pd

# ─────────────────────────────────────────────────────────────
#  9-QUARTER PPNR FORECAST
# ─────────────────────────────────────────────────────────────

def forecast_ppnr(scenarios, satellite_models, fin_hist):
    """
    Project NII, NIINC, NIE, and PPNR over 9 quarters under each scenario.
    Uses recursive forecasting for lag features.
    """
    forecasts = {}

    # Seed values: last observed quarter
    last_nii   = fin_hist["nii"].iloc[-1]
    last_niinc = fin_hist["niinc"].iloc[-1]
    last_loan  = fin_hist["loan_bal"].iloc[-1]

    for sc_name, sc_macro in scenarios.items():
        nii_f, niinc_f, nie_f, ppnr_f = [], [], [], []
        prev_nii   = last_nii
        prev_niinc = last_niinc
        loan_bal   = last_loan

        mod_nii   = satellite_models["nii"]["model"]
        mod_niinc = satellite_models["niinc"]["model"]
        mod_nie   = satellite_models["nie"]["model"]

        for q in range(9):
            row = sc_macro.iloc[q]

            # Update loan balance
            loan_bal = loan_bal * (1 + row["loan_growth"] / 400)

            # NII forecast
            x_nii = pd.DataFrame([[1.0, row["fed_funds"], row["term_spread"],
                                    row["loan_growth"], prev_nii]],
                                   columns=["const", "fed_funds", "term_spread",
                                            "loan_growth", "lag_nii"])
            nii_q = float(mod_nii.predict(x_nii)[0])
            nii_q = max(nii_q, 1.0)

            # NIINC forecast
            x_niinc = pd.DataFrame([[1.0, row["gdp_growth"], row["vix"],
                                      row["fed_funds"], row["hpi_growth"]]],
                                     columns=["const", "gdp_growth", "vix",
                                              "fed_funds", "hpi_growth"])
            niinc_q = float(mod_niinc.predict(x_niinc)[0])
            niinc_q = max(niinc_q, 0.5)

            # NIE forecast
            total_rev = nii_q + niinc_q
            x_nie = pd.DataFrame([[1.0, total_rev, row["unemp_rate"], row["gdp_growth"]]],
                                   columns=["const", "total_rev", "unemp_rate", "gdp_growth"])
            nie_q = float(mod_nie.predict(x_nie)[0])
            nie_q = max(nie_q, 1.0)

            ppnr_q = nii_q + niinc_q - nie_q

            nii_f.append(nii_q); niinc_f.append(niinc_q)
            nie_f.append(nie_q); ppnr_f.append(ppnr_q)

            prev_nii   = nii_q
            prev_niinc = niinc_q

        forecasts[sc_name] = pd.DataFrame({
            "nii":   nii_f, "niinc": niinc_f,
            "nie":   nie_f, "ppnr":  ppnr_f,
        }, index=sc_macro.index)

    return forecasts
