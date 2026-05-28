def plot_all(macro_hist, fin_hist, forecasts, val_results, sens_df, satellite_models):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--",
    })
    NAVY="#1a3a5c"; BLUE="#1a5276"; RED="#c0392b"; GREEN="#1e8449"
    AMBER="#d4ac0d"; PURPLE="#6c3483"; GRAY="#7f8c8d"

    SC_COLORS = {"Baseline": GREEN, "Adverse": AMBER, "Severely Adverse": RED}

    fig = plt.figure(figsize=(18, 14))
    gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.42, wspace=0.35)
    fig.suptitle(
        "PPNR / CCAR Stress Testing Model — Stylised Large US Bank\n"
        "9-Quarter Forecast Horizon  |  Three CCAR Scenarios  |  Satellite Model Framework",
        fontsize=13, fontweight="bold")

    # 1. PPNR Forecast — all 3 scenarios
    ax = fig.add_subplot(gs[0, :2])
    hist_idx   = fin_hist.index[-12:]
    hist_ppnr  = fin_hist["ppnr"].iloc[-12:]
    ax.plot(hist_idx, hist_ppnr, color=NAVY, lw=2.5, label="Historical", zorder=5)
    ax.axvline(fin_hist.index[-1], color=GRAY, lw=1.2, linestyle="--", alpha=0.7)
    ax.text(fin_hist.index[-1], ax.get_ylim()[0] if ax.get_ylim()[0] > 0 else 0,
            " Forecast →", fontsize=8, color=GRAY)
    for sc_name, fc in forecasts.items():
        ax.plot(fc.index, fc["ppnr"], color=SC_COLORS[sc_name],
                lw=2, marker="o", markersize=4, label=sc_name)
    ax.set_title("PPNR Forecast — 9-Quarter Horizon under CCAR Scenarios (USD Bn)", fontweight="bold")
    ax.set_ylabel("PPNR (USD Billions)")
    ax.legend(fontsize=9)

    # 2. NII / NIINC / NIE breakdown — Severely Adverse
    ax = fig.add_subplot(gs[0, 2])
    sa = forecasts["Severely Adverse"]
    quarters_short = [f"Q{i+1}" for i in range(9)]
    x = np.arange(9)
    ax.bar(x, sa["nii"],  label="NII",   color=BLUE,  alpha=0.85, edgecolor="white")
    ax.bar(x, sa["niinc"],label="NIINC", color=GREEN, alpha=0.85, edgecolor="white",
           bottom=sa["nii"])
    ax.bar(x, -sa["nie"], label="NIE",   color=RED,   alpha=0.70, edgecolor="white")
    ax.plot(x, sa["ppnr"], "k--o", lw=1.5, markersize=4, label="PPNR", zorder=5)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(quarters_short, fontsize=8)
    ax.set_title("PPNR Components\nSeverely Adverse", fontweight="bold")
    ax.set_ylabel("USD Billions")
    ax.legend(fontsize=7.5)

    # 3. OOS Backtest — NII
    ax = fig.add_subplot(gs[1, 0])
    vr = val_results["NII"]
    ax.plot(vr["test_index"], vr["actual"],    color=NAVY, lw=2,   label="Actual")
    ax.plot(vr["test_index"], vr["predicted"], color=RED,  lw=1.8, linestyle="--", label="Predicted")
    ax.fill_between(vr["test_index"],
                    vr["predicted"] - vr["rmse"],
                    vr["predicted"] + vr["rmse"],
                    alpha=0.15, color=RED)
    ax.set_title(f"OOS Backtest — NII\nRMSE=${vr['rmse']:.2f}B  Corr={vr['corr']:.3f}", fontweight="bold")
    ax.set_ylabel("USD Billions")
    ax.legend(fontsize=8)

    # 4. OOS Backtest — PPNR (derived)
    ax = fig.add_subplot(gs[1, 1])
    vr_nii   = val_results["NII"]
    vr_niinc = val_results["NIINC"]
    vr_nie   = val_results["NIE"]
    ppnr_actual = vr_nii["actual"] + vr_niinc["actual"] - vr_nie["actual"]
    ppnr_pred   = vr_nii["predicted"] + vr_niinc["predicted"] - vr_nie["predicted"]
    ppnr_rmse   = np.sqrt(np.mean((ppnr_actual - ppnr_pred)**2))
    ppnr_corr   = np.corrcoef(ppnr_actual, ppnr_pred)[0,1]
    ax.plot(vr_nii["test_index"], ppnr_actual, color=NAVY, lw=2,   label="Actual PPNR")
    ax.plot(vr_nii["test_index"], ppnr_pred,   color=RED,  lw=1.8, linestyle="--", label="Predicted PPNR")
    ax.set_title(f"OOS Backtest — PPNR\nRMSE=${ppnr_rmse:.2f}B  Corr={ppnr_corr:.3f}", fontweight="bold")
    ax.set_ylabel("USD Billions")
    ax.legend(fontsize=8)

    # 5. Sensitivity tornado chart
    ax = fig.add_subplot(gs[1, 2])
    colors_sens = [RED if v < 0 else GREEN for v in sens_df.values]
    ax.barh(range(len(sens_df)), sens_df.values, color=colors_sens, edgecolor="white", alpha=0.85)
    ax.set_yticks(range(len(sens_df)))
    ax.set_yticklabels(sens_df.index, fontsize=8)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_title("PPNR Sensitivity\n±1SD Macro Shock (9Q Cumulative, USD Bn)", fontweight="bold")
    ax.set_xlabel("ΔPPNR (USD Billions)")

    # 6. Macro scenario paths — GDP & Unemployment
    ax = fig.add_subplot(gs[2, 0])
    for sc_name, sc_macro in CCAR_SCENARIOS.items():
        ax.plot(sc_macro.index, sc_macro["gdp_growth"],
                color=SC_COLORS[sc_name], lw=2, label=sc_name, marker="o", markersize=3)
    ax.axhline(0, color="black", lw=0.8, linestyle="--")
    ax.set_title("CCAR Scenario Paths — GDP Growth (%)", fontweight="bold")
    ax.set_ylabel("Real GDP Growth YoY (%)"); ax.legend(fontsize=8)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")

    ax = fig.add_subplot(gs[2, 1])
    for sc_name, sc_macro in CCAR_SCENARIOS.items():
        ax.plot(sc_macro.index, sc_macro["unemp_rate"],
                color=SC_COLORS[sc_name], lw=2, label=sc_name, marker="o", markersize=3)
    ax.set_title("CCAR Scenario Paths — Unemployment (%)", fontweight="bold")
    ax.set_ylabel("Unemployment Rate (%)"); ax.legend(fontsize=8)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")

    # 7. Cumulative 9Q PPNR comparison
    ax = fig.add_subplot(gs[2, 2])
    cum_ppnr = {sc: fc["ppnr"].sum() for sc, fc in forecasts.items()}
    bars = ax.bar(cum_ppnr.keys(), cum_ppnr.values(),
                  color=[SC_COLORS[s] for s in cum_ppnr.keys()],
                  edgecolor="white", width=0.5)
    ax.set_title("Cumulative 9Q PPNR by Scenario\n(USD Billions)", fontweight="bold")
    ax.set_ylabel("Cumulative PPNR (USD Billions)")
    for bar, val in zip(bars, cum_ppnr.values()):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                f"${val:.1f}B", ha="center", fontsize=9, fontweight="bold")

    plt.savefig(f"{OUTPUT_DIR}/ppnr_ccar_charts.png", dpi=160, bbox_inches="tight")
    plt.close()
    print("Charts saved.")
