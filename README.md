# PPNR CCAR Stress Testing

## Overview

This repository contains a Python-based implementation of a PPNR forecasting and CCAR scenario analysis framework built around a standard satellite-model architecture for earnings projection under stress. 

The analysis estimates the primary pre-provision revenue components: Net Interest Income (NII), Non-Interest Income (NIINC), and Non-Interest Expense (NIE) ; using macro-linked regression models calibrated on quarterly historical data, and projects earnings across a nine-quarter supervisory stress horizon under Baseline, Adverse, and Severely Adverse scenarios.

The framework focuses on the relationship between macroeconomic conditions and earnings performance, with application across PPNR forecasting, enterprise stress testing, capital planning, and balance sheet analytics. Outputs include model diagnostics, out-of-sample validation, scenario forecast paths, and single-factor macro sensitivity analysis.

## Scope

The framework projects quarterly PPNR through separate earnings component models and aggregates projected revenue and expense streams across the scenario horizon.

Components modelled:

- Net Interest Income (NII)
- Non-Interest Income (NIINC)
- Non-Interest Expense (NIE)

with:

PPNR = NII + NIINC − NIE

Forecasts are produced over a 9-quarter CCAR horizon under supervisory macroeconomic scenarios.

## Data & Calibration

Historical calibration period:

**2008 Q1 – 2021 Q4**

### Macroeconomic Drivers

| Variable | Description |
| --- | --- |
| Fed Funds Rate | Policy rate environment |
| Term Spread | 10Y–2Y Treasury slope |
| GDP Growth | Real economic activity |
| Unemployment Rate | Labor market stress |
| VIX | Market volatility proxy |
| HPI Growth | Housing cycle indicator |
| Loan Growth | Portfolio growth / balance sheet expansion |

A stylised large-bank quarterly financial history is generated against this macro backdrop to model earnings behaviour through the cycle.

---

## Model Architecture

PPNR is estimated through separate satellite models for each earnings component.

### Net Interest Income (NII)

Model drivers:

- Fed Funds Rate  
- Term Spread  
- Loan Growth  
- Lagged NII  

### Non-Interest Income (NIINC)

Model drivers:

- GDP Growth  
- VIX  
- Fed Funds Rate  
- House Price Growth  

### Non-Interest Expense (NIE)

Model drivers:

- Total Revenue  
- Unemployment Rate  
- GDP Growth  

Each component is forecast independently before aggregation into total projected PPNR.

---

## Scenario Framework

The model evaluates earnings performance across three macroeconomic paths.

| Scenario | Description |
| --- | --- |
| Baseline | Moderate growth and policy normalization |
| Adverse | Recessionary slowdown with rising unemployment |
| Severely Adverse | Deep recession scenario with significant macro deterioration |

Each scenario includes projected paths for:

- interest rates
- yield curve slope
- GDP growth
- unemployment
- market volatility
- house price growth
- loan growth

---

## Validation

Model performance is assessed through out-of-sample backtesting.

### Train / Test Split

| Dataset | Period |
| --- | --- |
| Training | 2008–2017 |
| Testing | 2018–2021 |

### Validation Metrics

- RMSE
- MAE
- MAPE
- Theil’s U
- Correlation between actual and predicted values

Diagnostics are produced independently for each satellite model prior to scenario forecasting.

---

## Sensitivity Analysis

A single-factor sensitivity framework is applied across key macroeconomic variables using **±1 standard deviation shocks** relative to the baseline path.

Sensitivity testing evaluates cumulative PPNR impact from movements in:

- Fed Funds Rate
- Term Spread
- GDP Growth
- Unemployment Rate
- VIX
- House Price Growth
- Loan Growth

Results are measured as **9-quarter cumulative PPNR variance versus baseline**.

---

## Outputs

The framework generates:

- Historical macroeconomic dataset
- Historical financial series
- Satellite model diagnostics
- Out-of-sample validation metrics
- 9-quarter scenario forecast outputs
- Macro sensitivity analysis
- Consolidated scenario visualizations

Generated files are available under:

`ppnr_outputs/`

---

## Technical Stack

- Python
- NumPy
- Pandas
- Statsmodels
- SciPy
- Matplotlib

## Repository Structure

```bash
ppnr-ccar-stress-testing/
│
├── README.md
│
├── src/
│   ├── main.py
│   │
│   ├── data/
│   │   ├── macro_history.py
│   │   └── financials.py
│   │
│   ├── models/
│   │   ├── satellite_models.py
│   │   └── validation.py
│   │
│   ├── scenarios/
│   │   ├── ccar_scenarios.py
│   │   └── forecasting.py
│   │
│   ├── analytics/
│   │   └── sensitivity.py
│   │
│   └── reporting/
│       └── charts.py
│
└── ppnr_outputs/
