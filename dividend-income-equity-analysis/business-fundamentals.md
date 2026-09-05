# Business Fundamentals and Dividend Forecast Rules

This file defines how to connect long-term business fundamentals to future dividend capacity.

The purpose is to derive sustainable owner cash, future DPS, normalized DPS, and valuation inputs from operating drivers rather than extrapolating historical dividends. Read `business-outlook.md` for the three-to-five-year development thesis and `sector-fcf-proxies.md` before selecting a cash-generation measure. These modules share one forecast; do not build a separate, inconsistent growth-valuation forecast.

## 1. Required Causal Chain

Every full analysis must follow this chain:

```text
Business volume / customer / asset / commodity / rate drivers
-> Revenue or sector-equivalent income
-> Operating margin or sector-equivalent profitability
-> Attributable earnings and normalized operating cash / sector capital generation
-> Recurring Owner FCF / evidenced sector proxy
-> Committed growth reinvestment and mandatory capital uses, deducted once
-> Recurring Funds Available for Distribution (Recurring FAD)
-> Actual-period exceptional uses and explicitly available excess cash
-> Total distribution capacity
-> Dividend policy applied to its stated calculation base, subject to funding constraints
-> Modeled gross dividend entitlement
-> Dividend-entitled shares for each installment
-> Cash-election DPS, with issuer cash settlement and subsequent scrip dilution tracked separately
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

Use the most economically meaningful sector measure. Do not force revenue, EBITDA, or industrial OCF-minus-capex onto banks, insurers, or REITs. Preserve reported amounts and a reconciliation to the chosen measure; estimates do not become reported facts through normalization.

### Cash-Flow Definitions and Deduction Ledger

Use amounts attributable to ordinary owners, a consistent consolidation perimeter, currency, fiscal period, and units. State whether cash interest, tax, leases, non-controlling interests, preferred claims, and capitalized development costs are already included.

| Measure | Definition | Use |
|---|---|---|
| Reported FCF | Issuer-defined FCF with its exact reconciliation and source | Starting evidence, not automatically comparable across issuers |
| Actual all-in FCF | Cash generated after actual operating uses and all capital investment, before ordinary shareholder distributions; exclude financing proceeds and disposal proceeds | Actual-period cash affordability |
| Recurring Owner FCF | Normalized operating cash after cash interest/tax, maintenance investment and other owner claims, but before separately identified growth investment | Sustainable owner cash before growth allocation; not FCFF or cash already free to distribute |
| Recurring FAD | Recurring Owner FCF or eligible sector proxy less remaining committed growth investment and mandatory debt/regulatory uses | Recurring dividend coverage and sustainable dividend capacity |
| Total distribution capacity | Recurring FAD less exceptional cash uses not already included, plus explicitly available excess cash | Period-specific affordability, not a recurring payout base by default |

For operating companies:

```text
Recurring Owner FCF
= Normalized OCF
- Maintenance Capex
- Cash Lease Principal Not Already Included
- Minority / Senior Cash Claims Not Already Included

Recurring FAD
= Recurring Owner FCF or Sector Capital Proxy
- Committed Growth Reinvestment Not Already Included
- Mandatory Debt / Regulatory Uses Not Already Included

Total Distribution Capacity
= Recurring FAD
- Exceptional Cash Uses Not Already Included
+ Explicitly Available Excess Cash

Actual All-In FCF (operating-company forecast)
= Recurring Owner FCF
- Remaining Growth Investment
- Exceptional Cash Uses Not Already Included
+ Nonrecurring Operating Cash Inflow
```

Normalized OCF must be after cash interest and tax even if the issuer classifies them as financing or investing. Start from reported OCF and show each signed adjustment, its source, recurrence, cash timing, and whether it is already included. Distinguish a normalization adjustment from a cash obligation that still has to be paid.

Maintain a deduction ledger with `item`, `category`, `amount`, `already_in_starting_metric`, `incremental_deduction`, and `evidence`. Categories are maintenance, owner_claims, growth, mandatory and exceptional. Deduct an item exactly once. The growth, mandatory and exceptional incremental totals must reconcile to the distribution bridge; an internally consistent ledger alone is insufficient. If reported FCF already deducts all capex, either reconcile back to pre-growth Recurring Owner FCF or start with that after-investment figure and deduct no capex again. Do not add back total capex and pretend all of it is optional growth.

- Maintenance includes replacement, safety, environmental obligations, sustaining software and capitalized development needed to preserve the business. If maintenance/growth cannot be separated responsibly, use all capex as a conservative deduction and disclose the limitation.
- Expensed R&D is already an operating use. Do not add it back to cash available for dividends while also crediting the resulting growth. Recurring licensing, milestone, contingent-consideration, restructuring and litigation payments require an economic recurrence assessment, not an automatic "adjusted" add-back.
- Stock compensation is not free: include the resulting share dilution or the cash cost of offsetting issuance, without charging both for the same shares.
- Available excess cash excludes restricted cash, operating liquidity, regulatory buffers, subsidiary cash that cannot be remitted, and proceeds needed for committed uses. Asset sales, new debt and equity proceeds are separate funding sources, not recurring FAD.
- Reconcile `actual_all_in_fcf` to the forecast bridge rather than leaving it as an independent estimate. `nonrecurring_operating_cash_inflow` identifies a sourced temporary operating inflow excluded from normalized owner cash; it is not financing or asset-sale proceeds and never increases recurring FAD. Any portion used for distributions must also be identified within explicitly available excess cash, counted once. Financial-sector capital proxies do not use this industrial FCF identity.
- Do not silently floor negative FCF or FAD at zero. Report the deficit, financing need, and implications for payout and forecast confidence.

### Historical Coverage Contract

Keep both actual-period cash coverage and recurring FAD coverage. Use the relevant **cash paid** dividend denominator for the same fiscal periods and owner perimeter. Reconcile declared DPS, record-date shares, cash payments, and scrip elections; never divide paid cash by declared dividends without explaining timing.

```text
Three-Year Recurring Coverage = sum(Recurring FAD for 3 years) / sum(Relevant Cash Dividends for 3 years)
Annual Recurring Coverage = Recurring FAD / Relevant Cash Dividends
Five-Year Worst Recurring Coverage = minimum(valid Annual Recurring Coverage over the last 5 years)
```

Also show the worst **actual** cash-coverage year and the funding of any shortfall. Do not average annual coverage ratios. A zero dividend denominator is `Not Available`, not infinite coverage or a safety pass. Use three-to-five comparable years when available, disclose the years present, and use a full cycle for cyclical issuers. Demergers and accounting changes may prevent a comparable five-year series.

Record each historical `fiscal_year_end` in ISO date format. Select the latest three/five fiscal periods by date, never by arbitrary JSON array order. The summary lists those periods oldest first. A complete five-year worst-coverage figure requires five comparable valid annual ratios; otherwise show the worst available ratio and the limitation separately.

For fixed/progressive policies use ordinary cash dividends as the primary denominator; show total cash payouts as a secondary stress check. For variable/cycle-linked policies use total recurring/variable cash dividends. Separately identify one-off capital distributions. A historical exceptional cash shortfall calls for a liquidity review, not an automatic structural veto or an automatic normalization-based dismissal.

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

`sector-fcf-proxies.md` is the single source for the sector bridge, required disclosures, capital constraints, prohibited shortcuts, and missing-data treatment. Identify one primary model and any holding-company overlay before calculating coverage. Never turn OPAT, embedded value, NAV, EBITDA, or AFFO into distributable cash by renaming it.

## 6. Three-to-Five-Year Fundamental and FCF Forecast

Build a five-year development outlook using `business-outlook.md`. Provide detailed annual Bear, Base, and Bull forecasts for FY+1 through FY+3, then FY+4 and FY+5 extension scenarios when supported. If later years cannot be estimated, retain the year/scenario rows with unavailable values, lower confidence and specific missing inputs; do not extrapolate a convenient CAGR. If even the first three years are unsupported, mark them similarly and use Not Forecastable.

### Operating Driver Forecast

| Fiscal Year | Scenario | Primary Driver | Price / Mix Driver | Margin / Credit / Cost Driver | Capital-Intensity Driver | Key Assumptions |
|---|---|---|---|---|---|---|

### Financial Forecast

| Fiscal Year | Scenario | Revenue / Sector Income | Net Income / AFFO | Operating Cash Flow | Total Capex / Capital Need | Recurring Owner FCF / Proxy |
|---|---|---:|---:|---:|---:|---:|

Show a separate FCF build so the terminal number is reproducible:

| Year / Scenario | Normalized OCF | Maintenance Capex | Other Owner Cash Claims | Recurring Owner FCF / Proxy | Remaining Growth Investment | Recurring FAD |
|---|---:|---:|---:|---:|---:|---:|

Regulatory/debt deductions and exceptional cash obligations belong in the distribution bridge below; identify them explicitly rather than hiding the difference between columns. The sector proxy replaces industrial OCF arithmetic for financial firms.

Rules:

- Bear, Base, and Bull assumptions must differ through explicit operating drivers, not arbitrary percentage haircuts to DPS.
- Use company guidance, historical sensitivity, sector data, capacity, contracts, and policy where available.
- Do not use false precision. Use ranges when the driver is inherently uncertain.
- Label whether each value is reported, consensus cross-check, company guidance, historically observed, or analyst estimate.
- State fiscal period, currency, cash units, share units and forecast data cutoff. Distinguish a full fiscal-year forecast from the remaining-year cash flows used in valuation.
- Forecast working capital from receivable/inventory/payable days or a justified sector driver, not permanently favorable cash conversion. Separate normal working-capital needs from a temporary release.
- Tie growth investment to project capacity, commissioning dates, returns and funding. Revenue cannot arrive before the assets or approvals needed to produce it; include startup losses and investment-to-cash lags.
- Model debt maturities, interest/refinancing costs, minimum liquidity and regulatory capital under each scenario. Do not assume unlimited refinancing to preserve DPS.
- Split FCF change into operating growth/mix, margin, working capital, maintenance, growth investment, financing/tax and owner-claim effects. Distinguish temporary cash release from a durable run-rate improvement.
- Report FCF/FAD per diluted share as well as totals, a range of cumulative five-year FAD when estimable, and the estimated year any investment-led cash deficit becomes self-funding. Use `Not estimable` rather than invented break-even dates.
- No arbitrary probabilities: scenarios are not a probability-weighted expected value unless probabilities and evidence are explicitly supplied.

## 7. Dividend Forecast Bridge

Future DPS must be derived from forecast distributable capacity.

### Distributable-Cash Bridge

| Year / Scenario | Owner FCF / Sector Proxy | Remaining Growth Uses | Remaining Mandatory Uses | Recurring FAD | Exceptional Uses / Excess Cash | Total Distribution Capacity |
|---|---:|---:|---:|---:|---|---:|

Use this relationship:

```text
Cash Available for Distribution = Total Distribution Capacity
```

Use the definition and deduction ledger in Section 2. Exceptional uses and excess cash must be shown separately in the underlying records even when combined in a display cell. Recurring FAD, not a temporary cash-balance release, supports N and terminal dividends.

Track opening accessible excess cash, source-specific additions, uses and closing balance through the five years. The same surplus cannot fund repeated annual payouts. Reconcile ordinary shareholder prior claims, minority interests, trapped cash and subsidiary remittances once, using the parent overlay in `sector-fcf-proxies.md`. Verify parent distributable reserves, covenants and legal/regulatory headroom; a consolidated cash balance is not permission to distribute it.

### Payout-Policy Classification and Calculation Base

| Policy type | Policy-implied cash-equivalent dividend entitlement | Required constraint |
|---|---|---|
| `fixed_progressive` | Stated/derived DPS x dividend-entitled shares | Compare the commitment with recurring FAD and actual capacity; model a justified freeze/cut when needed |
| `earnings_linked` | Stated attributable earnings base x policy payout ratio | Earnings are not cash; independently test FAD, capital and remittances |
| `cash_flow_linked` | Issuer-specified FCF/FAD base x policy payout ratio | Reconcile the issuer definition; do not apply its ratio to a different base |
| `base_variable` | Supported base dividend plus policy-linked variable component | Keep base, variable and one-off sources separate; normalize through a cycle |
| `discretionary` | Evidence-backed board policy/scenario | Lower confidence if no repeatable allocation rule exists |

Always state `payout_calculation_basis`, `policy_implied_dividend`, the **forecast** dividend cash cost, any policy adjustment, and its funding rationale. A 40% earnings payout is not 40% of FAD. Do not silently cap the policy-implied amount to make coverage look safe, or assume a payout target overrides capital constraints.

For JSON, `payout_base_reference` identifies the corresponding forecast earnings/cash metric and signed `payout_base_adjustments` reconcile it to the issuer's exact definition. The runway's basis must match the documented policy. Base/variable policies include two separately calculated `policy_components`. For a ratio policy, negative eligible earnings imply zero policy dividends rather than negative payments; this does not floor negative FAD or erase a funding deficit. Fixed DPS uses the entitled share count; discretionary plans state the evidenced cash amount.

```text
Funding Gap = max(0, Forecast Dividend Cash Cost - Total Distribution Capacity)
Derived DPS per installment = Modeled Dividend Entitlement / Dividend-Entitled Share Count
Actual Dividend Cash Cost = Modeled Dividend Entitlement x cash-settled fraction + settlement_cash_adjustment
```

`policy_implied_dividend` is the gross all-shareholder entitlement before elections; `dividend_entitlement` is the modeled gross cash-equivalent amount after an explicitly explained policy/funding adjustment. Investor cash-election DPS uses this entitlement, never the issuer's reduced cash settlement after scrip. Report actual `funding_gap = max(0, dividend_cash_cost - capacity)` and `all_cash_funding_gap = max(0, dividend_entitlement - capacity)` separately. A scrip-funded reduction in actual cash cost cannot establish economic coverage of the ordinary dividend.

Use consistent cash/share units. A single installment may use the reported `dividend_entitled_shares`; EPS weighted-average diluted shares are a separate dilution check, not a default denominator. Where record-date share counts or elections differ, populate `dividend_installments` and sum their DPS and cash costs separately. The annual `dividend_entitled_shares` is then only the explicitly labelled dividend-weighted reconciliation count (`annual entitlement / annual DPS`, adjusted for unit scales), not an invented record-date quantity. Reconcile fixed-DPS policy installments against their actual entitled shares.

Each installment records its entitlement, entitled shares/record date, derived DPS, cash-settled fraction, actual cash cost and settlement cash adjustment. With no scrip cash retention, the fraction is 1 even if the broker reinvests the cash in market shares. Mandatory stock-only distributions have no cash-election DPS and must not populate this cash-income runway as an ordinary cash dividend. A cash adjustment represents only additional issuer settlement cash under the scheme, not withholding already included in the gross cash entitlement.

New issuer scrip shares affect subsequent entitlements when their terms allow; do not dilute the payment that created them in advance. Use issue price, participation and dates to roll shares forward. Keep all-cash-equivalent coverage alongside the retained legacy cash-paid coverage so high scrip participation cannot manufacture safety. [IFRS Foundation: IAS 33](https://www.ifrs.org/issued-standards/list-of-standards/ias-33-earnings-per-share.html/) explains the distinct EPS share denominator.

Machine-readable Derived DPS uses the financial currency's whole currency unit, with `cash_unit_scale / share_unit_scale` applied. Valuation cash and prices use the return record's `valuation_unit_scale` (for example 0.01 GBP per quoted penny); disclose FX separately from unit conversion.

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
- For variable or formula-based policies, apply the stated policy to its documented normalized calculation base, then test recurring FAD and actual capacity separately.
- DRIP purchased in the secondary market creates no issuer shares; only issuer-sponsored new shares create dilution. Do not assume every reinvestment plan is scrip.

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
- For `structural` changes, set Accumulation Upper-Bound Change to `Rebuild required`; rerun Fundamental Trend, the five-year outlook/forecast, scoring, value-trap checks, and valuation framework.
- When a growth DDM is used, a transient **cash** change affects only its dated cash-flow present value, not terminal growth or normalized N. Report `growth_value_change` separately; the ordinary accumulation-boundary change remains `N/A`. See `buy-zone.md`.

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

- `B` should come from Bear-case distributable cash, payout policy, entitled shares and investor cash-election treatment. State the selected year(s) and why they represent the adverse state; do not silently use the mildest Bear year.
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

## 11. Relationship to Valuation and Holding Review

This module forecasts operating cash and dividend capacity, not an unconstrained corporate DCF.

- Reuse the same operating assumptions and funded dividend path in `buy-zone.md`; conditional growth valuation does not create distributable cash.
- Link the five-year outlook's milestone and invalidation signals to `holding-review.md`.
- Use a dedicated enterprise DCF or detailed project valuation when the question extends beyond the supported dividend model.
- If the fundamental forecast conflicts with historical dividend patterns or management targets, explain the conflict explicitly.
