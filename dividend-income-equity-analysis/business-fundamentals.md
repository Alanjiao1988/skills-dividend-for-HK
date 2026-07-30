# Business Fundamentals and Dividend Forecast Rules

This file defines how to connect long-term business fundamentals to future dividend capacity.

The purpose is not to build a full investment-bank financial model or DCF. The purpose is to ensure that future DPS, normalized DPS, and buy-zone inputs are derived from operating drivers, earnings, cash flow, balance-sheet constraints, payout policy, and diluted share count rather than guessed directly from historical dividends.

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
-> Diluted share count, including scrip / DRIP dilution where relevant
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
- Whether per-share economics improved after accounting for issuance, buybacks, scrip dividends, and DRIP participation.

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
- Diluted share count, scrip participation, expected issuance, and buybacks.

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

Use normalized commodity prices rather than spot peak prices for normalized dividends.

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

Check LTV, refinancing cost, WALE, tenant concentration, valuation losses, equity issuance, and DRIP dilution.

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
- Label whether each value is reported, consensus cross-check, company guidance, historically observed, or analyst estimate.

## 7. Dividend Forecast Bridge

Future DPS must be derived from forecast distributable capacity.

### Distributable-Cash Bridge

| Fiscal Year | Scenario | FCF / Capital Generation | Mandatory Debt / Regulatory Uses | Required Reinvestment | Excess Cash Used | Cash Available for Distribution |
|---|---|---:|---:|---:|---:|---:|

Use this relationship:

```text
Cash Available for Distribution
= FCF or sector-equivalent capital generation
- mandatory debt repayment
- regulatory capital requirements
- required maintenance and committed reinvestment
+ explicitly available excess cash, if justified
```

The final dividend, DPS, and yield output belongs in the Dividend and Yield Runway table defined in `visual-output-rules.md`. Do not repeat Dividend Cash Cost and Derived DPS in a second table here.

### Share Count and Scrip / DRIP Assumptions

| Fiscal Year | Scenario | Diluted Share Count | Scrip / DRIP Available | Expected Participation / Dilution | Buyback Offset | Comment |
|---|---|---:|---|---|---|---|

Rules:

- Identify whether the issuer offers scrip dividend, stock dividend, elective share distribution, or DRIP.
- Record whether cash or shares is the default election where disclosed.
- Use historical participation rates when available; otherwise state the assumption.
- Include expected scrip / DRIP shares in diluted share count unless the company credibly offsets them through buybacks.
- Default investor cash-yield calculations to an all-cash election when that election is available, but disclose company-level dilution created by shareholders who elect shares.
- For fixed or progressive policies, compare derived capacity with the promised or expected DPS.
- For variable or formula-based policies, apply the stated policy to normalized distributable cash.

## 8. Single-Driver Sensitivity

Every full analysis should include a compact sensitivity table for the three to five most important operating drivers when the forecast model supports it.

Use one-driver-at-a-time sensitivity around the Base case while holding other assumptions constant.

| Driver Change | Sensitivity Type | Distributable Cash Change | Derived DPS Change | Net Yield Change at Current Price | Accumulation Upper-Bound Change | Interpretation |
|---|---|---:|---:|---:|---:|---|

Classify every sensitivity as:

- `transient`: a temporary or near-term change that does not alter normalized mid-cycle economics;
- `persistent`: a change expected to persist across the normalization horizon and alter sustainable distributable cash;
- `structural`: a change to the business model, competitive position, regulation, asset base, or long-run economics that requires the full model to be rebuilt.

Rules:

- State the Base-case driver level and the unit change.
- Show whether the relationship is calculated, historically observed, company-disclosed, or estimated.
- Treat the result as local sensitivity around the Base case. Do not assume linearity under extreme conditions.
- If the driver affects multiple variables simultaneously, explain the interaction rather than claiming false one-variable precision.
- For `transient` changes, set Accumulation Upper-Bound Change to `N/A`. The effect belongs only in the affected forecast-year cash flow, DPS, and net yield.
- For `persistent` changes, recalculate normalized distributable cash and N before updating the accumulation boundary.
- For `structural` changes, set Accumulation Upper-Bound Change to `Rebuild required`; rerun Fundamental Trend, the three-year forecast, scoring, value-trap checks, and valuation framework.

Examples:

- One-year VLCC day-rate spike: transient.
- Permanent tariff reset or durable NIM regime shift: persistent.
- Regulation that makes a business line uneconomic: structural.

## 9. Normalized and Bear DPS Rules

The buy-zone inputs must be traceable to the fundamental forecast.

### Normalized Net DPS, N

Use this source priority:

1. Explicit mid-cycle normalized distributable cash and payout-policy-derived net DPS.
2. Full-cycle median distributable cash and payout-policy-derived net DPS when a complete cycle is available.
3. Average of the three-year Base-case derived net DPS only when the forecast assumptions have returned to normal operating conditions and do not retain temporary cycle premiums or trough discounts.
4. Fundamentally adjusted historical normalized DPS as a lower-confidence fallback.

Always output the N basis as one of:

```text
mid_cycle
full_cycle_median
three_year_base_average
historical_fundamental_fallback
```

A near-term Base case is not automatically normalized. Do not use a Base year containing temporary commodity, freight-rate, geopolitical, credit, regulatory, interest-rate, or pricing windfalls as N without normalizing those drivers.

N may be re-estimated through sensitivity analysis only when a driver change is classified as `persistent`. A `transient` change must not move N or the long-term buy-zone boundaries. A `structural` change requires the full model to be rebuilt rather than mechanically updating N.

### Bear Net DPS, B

- `B` should come from the Bear-case distributable cash, payout policy, and diluted share count.
- Bear assumptions must represent a plausible adverse operating state, not an arbitrary DPS haircut.
- Historical DPS averages may be used only as a cross-check or fallback when the operating forecast cannot be built.
- If historical values are used as a fallback, label the buy zone Lower Confidence and explain why.
- Do not set N or B solely by choosing a convenient yield or price target.

## 10. Forecast Confidence

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
- Uncertain capex, refinancing, policy, scrip dilution, or share issuance.
- Scenario ranges are wide.

### Not Forecastable

- Critical operating or cash-flow data is missing.
- Business model is undergoing a major transformation.
- Dividend depends on asset sales, litigation, rescue financing, or other non-repeatable events.

Required wording when a responsible forecast cannot be built:

```text
Future dividend cannot be forecast responsibly from operating fundamentals. The DPS scenarios below are illustrative rather than evidence-backed because the following inputs are missing or unreliable: ...
```

## 11. Relationship to Other Valuation Skills

This module forecasts dividend capacity. It is not a full intrinsic-value model.

- Use the dividend forecast to support normalized yield, dividend runway, sensitivity, and expected buy zone.
- Use a dedicated DDM, DCF, moat, or reinvestment skill when the user asks for full intrinsic value or competitive-advantage analysis.
- If the fundamental forecast conflicts with historical dividend patterns or management targets, explain the conflict explicitly.
