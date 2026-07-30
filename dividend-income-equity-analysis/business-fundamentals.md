# Business Fundamentals and Dividend Forecast Rules

This file defines how to connect long-term business fundamentals to future dividend capacity.

The purpose is not to build a full investment-bank financial model or DCF. The purpose is to ensure that future DPS, normalized DPS, and buy-zone inputs are derived from operating drivers, earnings, cash flow, balance-sheet constraints, and payout policy rather than guessed directly from historical dividends.

## 1. Required Causal Chain

Every full analysis must follow this chain:

```text
Business volume / customer / asset / commodity / rate drivers
-> Revenue or sector-equivalent income
-> Operating margin or sector-equivalent profitability
-> Net income / AFFO / capital generation
-> Operating cash flow
-> Maintenance and growth capex
-> Free cash flow or distributable cash
-> Mandatory debt, regulatory, and reinvestment uses
-> Cash available for shareholder distribution
-> Dividend policy and payout ratio
-> Dividend cash cost
-> Diluted share count
-> DPS
-> Net DPS and expected buy zone
```

Do not forecast future DPS as an independent input when the operating and cash-flow bridge can be built.

## 2. Historical Business Baseline

Use at least five fiscal years when available. For cyclical sectors, use a full business cycle where possible.

Identify:

- Main business segments and their contribution to revenue, profit, cash flow, or capital generation.
- The economic engine that actually funds dividends.
- Structural growth, cyclical growth, one-off growth, and accounting growth without cash-flow growth.
- Market share, customer or asset growth, pricing power, unit economics, margins, maintenance capex, and working-capital behavior.
- Dilution, acquisitions, disposals, and changes in segment mix.
- Whether per-share economics improved after accounting for issuance and buybacks.

### Historical Operating Trend Table

| Fiscal Year | Primary Business Driver | Revenue / Sector Income | Operating Margin / Equivalent | Net Income / AFFO | FCF / Distributable Cash | Comment |
|---|---|---:|---:|---:|---:|---|

Use the most economically meaningful sector measure. Do not force revenue or EBITDA onto banks, insurers, or REITs when a better measure exists.

## 3. Long-Term Fundamental Trend

Classify the next three-to-five-year business trend as:

- Structural Growth.
- Stable / Mature.
- Cyclical Recovery.
- Cyclical Peak / Normalization Risk.
- Structural Decline.
- Transformation / High Uncertainty.

Support the classification with evidence for:

- Industry demand and supply.
- Competitive position and market share.
- Pricing power and cost structure.
- Capital intensity and maintenance requirements.
- Regulation, technology, substitution, and geopolitical exposure.
- Balance-sheet and refinancing constraints.
- Management execution and capital-allocation record.

Distinguish clearly between facts, assumptions, and analyst judgment.

## 4. Core Forecast Drivers

Select three to five drivers that explain most of the future earnings and cash-flow outcome.

Examples:

- Volume, users, customers, occupancy, assets, fleet days, production, or loan growth.
- Price, ARPU, tariffs, spreads, commodity prices, day rates, rent reversion, or product mix.
- Operating margin, credit cost, loss ratio, unit cost, utilization, or interest expense.
- Maintenance capex, growth capex, working capital, regulatory capital, or debt repayment.
- Diluted share count and expected issuance or buybacks.

Do not use a long list of immaterial variables. Prefer a small number of auditable drivers.

## 5. Sector-Specific Forecast Bridges

### Banks

```text
Loan / asset growth
+ net interest margin
+ fee and trading income
- operating cost
- credit cost
-> net profit
-> CET1 and regulatory capital generation
- required RWA growth and buffers
-> distributable capital
-> dividends and buybacks
```

Check CET1, RWA growth, asset quality, credit cost, NPLs, provision coverage, regulatory payout constraints, and stress-test sensitivity.

### Insurers

```text
Premium / new business growth
+ underwriting or insurance margin
+ investment income
- claims and catastrophe losses
-> earnings and capital generation
- solvency and regulatory capital needs
-> distributable capital
-> dividends and buybacks
```

### Telecoms

```text
Subscribers / connections
x ARPU and service mix
+ cloud / enterprise / digital growth
- network operating cost
-> operating cash flow
- spectrum and network capex
-> free cash flow
-> payout policy
-> DPS
```

### Utilities and Infrastructure

```text
Regulated asset base / contracted volume
x allowed return / tariff
+ inflation linkage
- operating cost
- maintenance and growth capex
- financing cost
-> distributable cash
-> dividend capacity
```

### Energy and Mining

```text
Commodity price
x production volume
- unit operating cost
- sustaining capex
- taxes / royalties / windfall levies
-> free cash flow
- debt and project commitments
-> base plus variable dividend capacity
```

Use normalized commodity prices rather than spot peak prices for base-case dividends.

### Shipping

```text
Available vessel days
x spot / charter day rate
- vessel operating cost
- drydock and maintenance capex
- interest and debt repayment
- fleet renewal commitments
-> distributable cash
-> base plus variable dividend capacity
```

Check spot versus charter exposure, fleet age, orderbook, utilization, drydock schedule, asset sales, and vessel acquisitions.

### REITs and Property Trusts

```text
Occupancy and rent growth
+ rent reversion and acquisitions
- property operating cost
- cash interest
- maintenance capex
-> AFFO / distributable income
-> payout ratio
-> DPU
```

Check LTV, refinancing cost, WALE, tenant concentration, valuation losses, and equity issuance.

### Consumer, Industrial, Technology, and Other Operating Companies

```text
Volume / users / units
x price and mix
-> revenue
x operating margin
-> operating profit
- tax and interest
-> net income
+ non-cash charges
- working capital
- maintenance and growth capex
-> free cash flow
-> dividend capacity
```

## 6. Three-Year Fundamental Forecast

Build Bear, Base, and Bull cases for each of the next three fiscal years.

### Operating Driver Forecast

| Fiscal Year | Scenario | Primary Driver | Price / Mix Driver | Margin / Credit / Cost Driver | Capital-Intensity Driver | Key Assumptions |
|---|---|---|---|---|---|---|

### Financial Forecast

| Fiscal Year | Scenario | Revenue / Sector Income | Net Income / AFFO | Operating Cash Flow | Capex / Capital Need | FCF / Distributable Cash |
|---|---|---:|---:|---:|---:|---:|

Rules:

- Bear, Base, and Bull assumptions must differ through explicit operating drivers, not arbitrary percentage haircuts to DPS.
- Use company guidance, historical sensitivity, sector data, capacity, contracts, and policy where available.
- Do not use false precision. Use ranges when the driver is inherently uncertain.
- Label whether each value is reported, consensus cross-check, company guidance, or analyst estimate.

## 7. Dividend Forecast Bridge

Future DPS must be derived from forecast distributable capacity.

### Distributable-Cash Bridge

| Fiscal Year | Scenario | Net Income / AFFO | FCF / Capital Generation | Mandatory Debt / Regulatory Uses | Required Reinvestment | Cash Available for Distribution |
|---|---|---:|---:|---:|---:|---:|

### DPS Derivation

| Fiscal Year | Scenario | Cash Available for Distribution | Payout Policy / Ratio | Dividend Cash Cost | Diluted Share Count | Derived DPS |
|---|---|---:|---|---:|---:|---:|

Use this relationship:

```text
Cash Available for Distribution
= FCF or sector-equivalent capital generation
- mandatory debt repayment
- regulatory capital requirements
- required maintenance and committed reinvestment
+ explicitly available excess cash, if justified

Dividend Cash Cost
= Cash Available for Distribution x expected payout ratio

Derived DPS
= Dividend Cash Cost / diluted share count
```

For fixed or progressive policies, compare the derived capacity with the promised or expected DPS. For variable or formula-based policies, apply the stated policy to normalized distributable cash.

## 8. Normalized and Bear DPS Rules

The buy-zone inputs must be traceable to the fundamental forecast:

- `N`, normalized net DPS, should normally come from the base-case normalized distributable cash and payout policy.
- `B`, bear-case net DPS, should come from the bear-case distributable cash and payout policy.
- Historical DPS averages may be used only as a cross-check or fallback when the operating forecast cannot be built.
- If historical averages are used as a fallback, label the buy zone as lower-confidence and state why an operating forecast was unavailable.
- Do not set N or B solely by choosing a convenient yield or price target.

## 9. Forecast Confidence

Rate forecast confidence as High, Medium, Low, or Not Forecastable.

### High

- Contracted, regulated, or recurring revenue.
- Clear cost and capex structure.
- Credible payout policy.
- Limited balance-sheet uncertainty.

### Medium

- Several forecastable drivers but meaningful macro, pricing, or execution risk.
- Dividend capacity is estimable within a range.

### Low

- High commodity, rate, credit, or volume sensitivity.
- Uncertain capex, refinancing, or policy.
- Scenario ranges are wide.

### Not Forecastable

- Critical operating or cash-flow data is missing.
- Business model is undergoing a major transformation.
- Dividend depends on asset sales, litigation, rescue financing, or other non-repeatable events.

Required wording when a responsible forecast cannot be built:

```text
Future dividend cannot be forecast responsibly from operating fundamentals. The DPS scenarios below are illustrative rather than evidence-backed because the following inputs are missing or unreliable: ...
```

## 10. Relationship to Other Valuation Skills

This module forecasts dividend capacity. It is not a full intrinsic-value model.

- Use the dividend forecast to support normalized yield, dividend runway, and expected buy zone.
- Use a dedicated DDM, DCF, moat, or reinvestment skill when the user asks for full intrinsic value or competitive-advantage analysis.
- If the fundamental forecast conflicts with historical dividend patterns or management targets, explain the conflict explicitly.
