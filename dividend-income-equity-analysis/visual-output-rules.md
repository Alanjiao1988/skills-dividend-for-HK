# Visual Output Rules

These rules apply to Full Analysis. Screen Mode uses the compact output in `screen-mode.md` and does not require these charts.

The Full Analysis should communicate in this order:

1. Four key numbers.
2. Business, cash-flow, dividend, and valuation visuals.
3. Slim tables as the audit trail.
4. Long-form explanation.

## 1. Output Capability Detection

- Use real charts when inline chart, artifact, HTML, or interactive rendering is available.
- Otherwise use compact text visuals plus markdown tables.
- Do not fail because chart rendering is unavailable.

## 2. Key Metrics at a Glance

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| | | | |

Normalized yield must be derived from normalized business and cash-flow capacity.

## 3. Standard Charts

### 3.1 DPS Structure Chart

Stack base / ordinary DPS separately from special, supplemental, or variable DPS by fiscal year.

### 3.2 Yield Ladder

Show TTM net yield, normalized net-yield band, and Bear / Base / Bull forecast yields.

### 3.3 Coverage Chart

Show recurring or normalized FCF / distributable cash against total cash dividends, with coverage multiples.

### 3.4 Fundamental Forecast Chart

Show historical actuals followed by Bear, Base, and Bull paths for one sector-appropriate operating measure and one cash-generation measure.

### 3.5 Valuation Visual

Use the visual that matches `valuation_mode`:

- `ordinary_yield_based`: Buy-Zone Ladder with Current, Fair, Accumulation, Strong Buy, N basis, confidence, and veto.
- `finite_life_harvest`: Finite-Life Cash-Recovery summary with annual net distributions, discount rate, residual value, and value range.
- `suspended`: prominent status stating why ordinary buy-zone output is suspended.

Do not display a Structural Decline company as an ordinary Fair / Accumulation / Strong Buy ladder unless the ordinary framework is explicitly shown only as a secondary cross-check permitted by `buy-zone.md`.

## 4. Dividend Trajectory Tables

### Per-Share DPS Structure

| Fiscal Year | Total DPS | Base DPS | Special / Variable DPS | DPS YoY | Quality Tag | Notes |
|---|---:|---:|---:|---:|---|---|

### Yield and Coverage

| Fiscal Year | Yield at Current Price | Yield at Year Price | Payout Ratio | FCF / Dividend | Coverage Label | Comment |
|---|---:|---:|---:|---:|---|---|

Quality Tag: Stable / Growing / Cyclical / One-off / Cut / Suspended / Event-driven / Peak-cycle.

Coverage Label: Strong / Adequate / Weak / Not Available.

## 5. Historical Cash-Flow Coverage Bridge

### Cash Generation

| Fiscal Year | Net Income | Operating Cash Flow | Capex | Free Cash Flow | FCF Quality | Comment |
|---|---:|---:|---:|---:|---|---|

### Cash Return and Funding

| Fiscal Year | Cash Dividends | Buybacks | Share Issuance | Net Debt Change | FCF / Dividend | Funding Source |
|---|---:|---:|---:|---:|---:|---|

Funding Source: Operating FCF / Cash Balance / Asset Sale / Debt / Equity Issuance / Mixed.

## 6. Fundamental Forecast and Dividend Tables

Use `business-fundamentals.md` as the calculation source. Required records:

- Historical Operating Trend.
- Operating Driver Forecast.
- Financial Forecast.
- Single-Driver Sensitivity.
- Distributable-Cash Bridge.
- Share Count and Scrip / DRIP Assumptions.
- Dividend and Yield Runway.

### Dividend and Yield Runway

| Fiscal Year | Scenario | Cash Available for Distribution | Payout Policy / Ratio | Dividend Cash Cost | Derived DPS | Net Yield at Current Price |
|---|---|---:|---|---:|---:|---:|

Do not duplicate Dividend Cash Cost or Derived DPS in another forecast table.

## 7. Sensitivity Display Rules

Every sensitivity row must show `transient`, `persistent`, or `structural`.

- Transient: show affected-year DPS and yield; buy-zone change is `N/A`.
- Persistent: show revised N basis or normalization adjustment before showing a boundary change.
- Structural: display `Rebuild required` instead of a numerical boundary change.

Text examples:

```text
Transient: VLCC day rate +5,000 for one year -> FY+1 DPS +0.40 -> buy-zone boundary N/A
Persistent: tariff reset +5% -> normalized N +0.20 -> Accumulation upper bound +3.30
Structural: regulation removes business line -> full model rebuild required
```

## 8. Table Slimming Rules

- Precede every chart or table with a one-sentence takeaway.
- Maximum 7 columns per table; split wider tables.
- When withholding is 0%, state once that gross equals net rather than repeating columns.
- Separate TTM and normalized yield for cyclical stocks.
- Distinguish facts, guidance, consensus cross-checks, historical sensitivity, and analyst estimates.
- Label partial-year data and avoid unstated annualization.

## 9. Ordinary Buy-Zone Tables

Use only when `valuation_mode = ordinary_yield_based`.

### Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|

### Buy-Zone Table

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|

Also show N basis, Forecast Confidence, and Value-Trap Veto.

## 10. Finite-Life Harvest Table

Use when `valuation_mode = finite_life_harvest`.

| Year | Forecast Net Distribution | Discount Factor | Present Value | Key Assumption |
|---|---:|---:|---:|---|

Then show:

- Harvest horizon.
- Discount rate.
- Present value of forecast distributions.
- Residual value and percentage of total value.
- Finite-life value range.

## 11. Plain-Text Fallback

- Business and FCF trend: `Historical -> Bear | Base | Bull`.
- DPS path: `FY-4 -> FY0 -> FY+1 scenarios`.
- Yield stack: `TTM | normalized | Bear/Base/Bull`.
- Sensitivity: include type and whether N changes.
- Coverage labels by year.
- Valuation:
  - ordinary: `Current | Fair | Accumulate | Strong Buy | Veto`;
  - finite-life: `Harvest horizon | PV distributions | residual | value range`;
  - suspended: `Buy zone suspended — reason`.
