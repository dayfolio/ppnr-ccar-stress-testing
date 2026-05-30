import numpy as np
import pandas as pd
# ─────────────────────────────────────────────────────────────
#  BANK FINANCIALS HISTORY
#
#  Stylised large US bank — balance sheet ~$2 trillion
#  All figures in USD billions, quarterly
#
#  NII    ~ driven by: fed_funds, term_spread, loan_growth, loan_balance
#  NIINC  ~ driven by: gdp_growth, vix, fed_funds (fee income vs trading)
#  NIE    ~ driven by: NII + NIINC (efficiency ratio), unemp_rate
#  PPNR   = NII + NIINC - NIE
# ─────────────────────────────────────────────────────────────

def generate_financials(macro, seed=42):
    np.random.seed(seed)
    n = len(macro)

    # Loan balance: starts $800B, grows with loan_growth
    loan_bal = np.zeros(n)
    loan_bal[0] = 800.0
    for i in range(1, n):
        loan_bal[i] = loan_bal[i-1] * (1 + macro["loan_growth"].iloc[i] / 400)  # quarterly

    # NIM: net interest margin — compresses at ZLB, expands with steeper curve
    nim = (2.50
           + 0.12 * macro["fed_funds"]
           + 0.35 * macro["term_spread"]
           - 0.05 * macro["unemp_rate"]
           + np.random.normal(0, 0.08, n))
    nim = np.clip(nim, 1.5, 4.5)

    # NII = loan_balance * NIM / 4 (quarterly)
    nii_true = loan_bal * nim / 400 + np.random.normal(0, 0.3, n)

    # Non-Interest Income: fee income (~GDP) + trading (~VIX) + service charges
    niinc_true = (4.5
                  + 0.18 * macro["gdp_growth"]
                  - 0.04 * macro["vix"]           # high VIX → lower fee income
                  + 0.02 * macro["fed_funds"]
                  + 0.08 * macro["hpi_growth"]     # mortgage banking fees
                  + np.random.normal(0, 0.25, n))
    niinc_true = np.clip(niinc_true, 1.5, 12.0)

    # NIE: efficiency ratio ~58% of revenues, plus macro drag
    rev = nii_true + niinc_true
    nie_true = (0.58 * rev
                + 0.12 * macro["unemp_rate"]       # labour costs correlated with unemployment
                - 0.05 * macro["gdp_growth"]
                + np.random.normal(0, 0.2, n))
    nie_true = np.clip(nie_true, 4.0, 25.0)

    ppnr_true = nii_true + niinc_true - nie_true

    return pd.DataFrame({
        "loan_bal":  loan_bal,
        "nii":       nii_true,
        "niinc":     niinc_true,
        "nie":       nie_true,
        "ppnr":      ppnr_true,
    }, index=macro.index)

