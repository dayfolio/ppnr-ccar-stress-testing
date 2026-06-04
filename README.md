# PPNR Forecasting & CCAR Scenario Analysis Framework

## Overview

Pre-Provision Net Revenue (PPNR) forecasting framework incorporating macroeconomic satellite models, out-of-sample validation, scenario forecasting, and sensitivity analysis for a stylised large U.S. commercial bank.

The framework decomposes earnings into Net Interest Income (NII), Non-Interest Income (NIINC), and Non-Interest Expense (NIE), estimates each component using macro-linked econometric models, and projects earnings performance over a nine-quarter forecast horizon under multiple macroeconomic scenarios.

Outputs include model diagnostics, validation statistics, scenario forecasts, earnings attribution, and sensitivity analysis.

---

## Analytical Framework

| Component            | Methodology                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| NII Forecasting      | OLS satellite model with rates, curve shape, loan growth, and lagged earnings       |
| NIINC Forecasting    | OLS satellite model with GDP growth, market volatility, rates, and housing activity |
| NIE Forecasting      | Revenue-linked expense model incorporating macroeconomic conditions                 |
| Scenario Forecasting | Recursive 9-quarter projection engine                                               |
| Validation           | Out-of-sample backtesting                                                           |
| Sensitivity Analysis | One-standard-deviation macro shocks                                                 |
| Diagnostics          | R², Adjusted R², RMSE, Durbin-Watson, t-statistics, p-values                        |

---

## Macroeconomic Drivers

The forecasting framework incorporates:

* Federal Funds Rate
* Treasury Term Spread
* Real GDP Growth
* Unemployment Rate
* VIX
* House Price Growth
* Loan Growth

Historical driver paths are calibrated across a 2008Q1–2021Q4 sample period, capturing the Global Financial Crisis, zero-rate environment, hiking cycle, and COVID shock.

---

## Satellite Model Architecture

PPNR is modelled through separate component-level forecasting models:

```text
PPNR = NII + NIINC – NIE
```

### Net Interest Income (NII)

Drivers:

* Federal Funds Rate
* Term Spread
* Loan Growth
* Lagged NII

### Non-Interest Income (NIINC)

Drivers:

* GDP Growth
* VIX
* Federal Funds Rate
* House Price Growth

### Non-Interest Expense (NIE)

Drivers:

* Total Revenue
* Unemployment Rate
* GDP Growth

Each component is estimated independently and aggregated within the forecasting engine.

---

## Forecasting Framework

The projection engine generates nine-quarter forward forecasts using recursive model estimation.

Forecasts are produced for:

* Net Interest Income
* Non-Interest Income
* Non-Interest Expense
* Aggregate PPNR

The framework supports dynamic propagation of forecasted values through lag-dependent model specifications.

---

## Scenario Analysis

Three macroeconomic scenarios are evaluated:

| Scenario         | Description                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| Baseline         | Moderate economic growth and rate normalisation                                                  |
| Adverse          | Recessionary environment with weakening earnings conditions                                      |
| Severely Adverse | Deep stress environment with elevated unemployment, market volatility, and housing deterioration |

Outputs include:

* Quarterly PPNR forecasts
* Component-level earnings forecasts
* Cumulative nine-quarter PPNR
* Trough earnings analysis

---

## Model Validation

Model performance is evaluated through an out-of-sample testing framework.

Training Period:

* 2008Q1 – 2017Q4

Testing Period:

* 2018Q1 – 2021Q4

Validation metrics include:

* RMSE
* MAE
* MAPE
* Theil's U
* Correlation Analysis

---

## Sensitivity Analysis

Scenario-independent sensitivity testing evaluates the impact of one-standard-deviation shocks across key macroeconomic drivers.

Drivers assessed:

* Federal Funds Rate
* Term Spread
* GDP Growth
* Unemployment Rate
* VIX
* House Price Growth
* Loan Growth

Results quantify incremental impacts on cumulative forecast PPNR.

---

## Outputs

The framework generates:

* Historical Macroeconomic Dataset
* Historical Financial Dataset
* Satellite Model Diagnostics
* Out-of-Sample Validation Results
* Scenario Forecasts
* Sensitivity Analysis
* Forecast Visualisations

Outputs are written to:

```text
ppnr_outputs/
```

---

## Repository Structure

```text
ppnr-forecasting-framework/
│
├── src/
│   ├── data/
│   ├── models/
│   ├── scenarios/
│   ├── analytics/
│   ├── reporting/
│   └── main.py
│
└── ppnr_outputs/
```

---

## Technology Stack

Python • Pandas • NumPy • Statsmodels • SciPy • Matplotlib

---

## Applications

* CCAR / DFAST Analytics
* PPNR Forecasting
* Earnings Stress Testing
* Balance Sheet Analytics
* Scenario Analysis
* Model Risk Management
* Forecasting & Quantitative Analytics
* Risk Model Validation







