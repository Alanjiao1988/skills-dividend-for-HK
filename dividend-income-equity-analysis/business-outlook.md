# Three-to-Five-Year Business Outlook

Full Analysis must explain how the business could develop, not just whether next year's dividend is covered. This module supplies the operating assumptions for `business-fundamentals.md`; it is not a second forecast or a reason to override a dividend-income requirement.

## 1. Required Questions

Answer these with dated evidence, a counterargument, and a cash-flow consequence:

1. Where will revenue, sector income and owner cash come from in three and five years? Distinguish existing assets/products, committed expansions and unproven options.
2. What can change demand, market share, pricing power, customer retention and margins? Quantify the exposed segment rather than relying on a generic market CAGR.
3. What could impair the franchise: substitution, regulation, patent or concession expiry, customer concentration, competition, credit or commodity normalization?
4. How much investment, working capital and regulatory capital is required before growth produces owner cash? Who funds it, at what cost and with what dilution?
5. Does growth improve **per-share** FCF/FAD and support dividends, or merely enlarge revenue/assets while consuming cash?
6. Which observable events would confirm or invalidate the thesis, and by when?

Assess management's delivery against earlier guidance, competitive advantages and their durability, capital-allocation incentives, industry supply additions, and the distinction between cyclical recovery and structural growth. Do not turn a market-size narrative into a company forecast without share, margin and investment assumptions.

## 2. Horizon and Evidence Ladder

| Horizon | Required Work | Evidence Standard |
|---|---|---|
| FY+1 | Guidance-to-model reconciliation, near-term orders/contracts, costs and funding | Latest filings, guidance and observable operations |
| FY+2 to FY+3 | Segment/project driver model, commissioning and cash-conversion path | Announced investment, capacity, contracts, regulation, historical unit economics |
| FY+4 to FY+5 | Durability, replacement/expiry, competitive response, growth fade and capital needs | Explain the extrapolation and provide ranges; lower confidence when appropriate |

Use annual Bear/Base/Bull rows across five years. First-three-year financial rows remain in `three_year_fundamental_forecast`; years four and five belong in `forecast_extension`, using the same row structure. This preserves the existing JSON field without mislabelling five years as three. Both feed the same five-year FCF, distribution and dividend runway records.

Record source, publication/data date, metric, unit, fiscal period, scenario value/range, evidence type, rationale and confidence for every material assumption. Distinguish `reported_fact`, `company_guidance`, `consensus_cross_check`, `historical_sensitivity` and `analyst_estimate`. A report's availability date must not postdate its analysis cutoff in a historical comparison.

Missing year-four/five inputs require null values plus `Not estimable` and a reason, not mechanical extension. A five-year qualitative outlook is still required. Extend the **valuation transition**, separately labelled, if a patent cliff or project cycle prevents a steady state by year five; do not invent a perpetual terminal value at an unstable endpoint.

## 3. Development Thesis and Milestones

Use three to five material drivers, each tied to a segment or cash engine:

| Driver / Segment | Current Baseline | FY+3 Outcome | FY+5 Outcome | Investment / Funding | Evidence / Confidence | Invalidation Signal |
|---|---|---|---|---|---|---|

Examples of measurable signals:

- A factory or regulated project: utilization, commissioning date, cost-to-complete, allowed return and first positive cash year.
- Pharmaceuticals: product exclusivity date, approved launch uptake, trial/regulatory milestones, erosion rates and royalties. A trial outcome is not guaranteed revenue.
- Banks/insurers: earning-asset or new-business quality, normalized losses, spread/reinvestment yields, required capital and remittance capacity.
- Mature consumer/telecom: price versus volume/churn, mix, competitive response, maintenance intensity and cash conversion.

Separate committed projects from optional projects. Base must not assume every option succeeds; Bear includes economically linked setbacks and the necessary spending response, not arbitrary percentage cuts to every line.

## 4. Forecast Free Cash Flow, Not Just Earnings

For each year and scenario, reconcile:

```text
Segment volumes x realized price / sector income drivers
-> margins and attributable earnings
-> operating cash, including working-capital timing
-> maintenance / sustaining investment and owner claims
-> Recurring Owner FCF or capital proxy
-> remaining growth investment and mandatory capital uses
-> recurring FAD
-> actual-period exceptional obligations and available excess cash
-> total distribution capacity
```

Show the following conclusions, with ranges where appropriate:

- Recurring Owner FCF and recurring FAD in FY+1, FY+3 and FY+5, both total and per diluted share.
- Actual all-in FCF versus normalized owner cash: which difference is economic investment, a temporary release or a genuine non-recurring item?
- FCF change decomposition: volumes/pricing/mix, margin, working capital, maintenance, growth, financing/tax and owner claims.
- Three-year and, when estimable, five-year cumulative recurring FAD; do not sum scenarios together.
- Cash needs before self-funding, liquidity trough, refinancing/capital requirements, and the assumed adjustment to buybacks/dividends.
- Dividend funding gap and coverage by scenario, using the policy's correct base and the same fiscal period.

Avoid one unsupported cash-conversion percentage applied indefinitely. Reconcile any ratio assumption to history, business changes and spending commitments. Do not count acquisition growth without its purchase price, funding cost, integration risk and share-count effects.

## 5. Growth Quality and Limits

Distinguish:

- Operating profit growth from reinvestment and incremental ROIC.
- Equity earnings growth from equity reinvestment/retention and incremental ROE under stated leverage assumptions.
- Per-share growth after issuance, buybacks and scrip.
- DPS growth after payout policy and capital constraints.

Use forward incremental returns where supportable; accounting return improvements on old assets do not prove that new investment can earn the same return. Do not multiply an equity retention rate by ROIC. A growing total profit pool can coexist with shrinking owner cash per share.

Show a bear outcome with slower cash conversion or less successful reinvestment. State how near-term growth converges to sustainable mature growth; do not assume a temporary margin rebound, payout-ratio expansion or buyback boost lasts forever.

## 6. Monitoring and Falsification

| Milestone | Due Period | Observable KPI / Threshold | Source to Revisit | FCF / FAD Implication | Action if Missed |
|---|---|---|---|---|---|

Set thresholds from the model or disclosed commitments, not invented universal cutoffs. At minimum revisit after results, material guidance/capital-policy changes, major project or regulatory events, and a thesis invalidation signal. Route a miss as `transient`, `persistent`, or `structural` and connect it to `holding-review.md`.

Output a concise bull thesis, base thesis and bear thesis, with the two or three facts most likely to change the conclusion. Do not assign personal holding sizes or imply a forecast is a promise.
