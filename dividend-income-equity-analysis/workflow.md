# Workflow

Use this workflow when reviewing dividend-paying listed companies.

## Mode Selection

Read `screen-mode.md` and `data-conventions.md` before research begins. Screen Mode reads only the supporting rules needed for the compact screen, not the Full Analysis forecast modules.

Use Screen Mode for screening, quick review, candidate-pool work, batch comparison, or multiple tickers where the user asks which names deserve deeper research.

Use Full Analysis for detailed single-stock research, three-to-five-year business/FCF outlooks, future dividend forecasts, expected buy zones, or holding and switching decisions.

Screen Mode ends after the compact screen output. It must not continue into the Full Analysis steps below.

## Screen Mode Workflow

1. Verify ticker, listing, current price, and as-of date.
2. Separate paid TTM yield from the selected recurring-income screening measure, with distribution, withholding, FX and fee basis.
3. Resolve the screening net-yield target using this priority:
   - user-explicit target for the current screen;
   - clearly applicable portfolio-level target;
   - `Not Assessed` when neither is available.
4. Classify target policy as `hard_minimum`, `preference`, or `not_assessed`.
5. Calculate Yield Fit and Yield Gap:
   - Follow `screen-mode.md`: compare the selected screening yield or supported range with the target.
   - Pass when its lower bound meets the target; Below target when its upper bound is below it.
   - Unclear when the range straddles the target or material inputs are unusable; normally Watch.
   - Not Assessed / N/A when no target is available.
6. Check whether a claimed dividend-growth path is documented by policy, earnings, cash flow, or an established record.
7. Classify the five-year DPS pattern.
8. Check latest FCF / Dividend or sector-equivalent coverage.
9. Check leverage, regulatory-capital, solvency, or refinancing alerts.
10. Make a preliminary Fundamental Trend classification.
11. Run the abbreviated dividend-trap screen.
12. Output `Full Analysis Recommended: Yes / Watch / No`.

Do not use `buy-zone.md` required-yield ranges as the investor's screening target.

If the screening target is Not Assessed, do not reject or downgrade a stock solely because its yield appears low.

If the target is a preference and Yield Fit is Below target, yield alone cannot produce `No`. Use `Watch` when a documented growth path or another unresolved question deserves Full Analysis.

If the target is an explicit hard minimum and Yield Fit is Below target, use `No` unless the user explicitly permits exceptions.

Required limitations:

```text
Mode: Screen
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
No three-to-five-year forecast, N, B, growth valuation, entry/trim price, Strong Buy label, or final score.
```

## Full Analysis Data Rules

Always record the data date.

- Price must include as-of date and exchange.
- Dividend history should come from official announcements or annual reports when available.
- Check dividend currency, record date, ex-date, payment date, special-dividend treatment, and scrip / DRIP terms.
- Distinguish reported facts, company guidance, consensus cross-checks, historical sensitivities, and analyst estimates.
- User broker statements are the priority source for actual cash received and actual withholding, subject to PIL classification.
- Use official share count from filings when available.
- Historical price inputs must identify period, frequency, source, and price type.

## Search Instructions

For HK-listed stocks, search HKEXnews and issuer materials for results, annual/interim reports, dividend and tax notes, scrip-election documents, operating statistics, guidance, cash flow, capex, share issuance, and buybacks.

For US-listed stocks, search SEC EDGAR and investor relations for 10-K, 10-Q, 8-K, proxy, operating KPIs, guidance, dividend declarations, DRIP terms, cash flow, share count, issuance, and buybacks.

For UK-listed stocks, search LSE RNS and investor relations for results, guidance, dividend and scrip terms, and buyback programmes.

Source order:

1. Official exchange announcements and filings.
2. Annual/interim reports, results, dividend documents, operating statistics, and guidance.
3. Company investor relations and management commentary.
4. User broker statement.
5. Third-party cross-checks.

## Step 1: Classification

Collect company, ticker, exchange, domicile, operating geography, listing structure, reporting currency, dividend currency, investor reporting currency, and security type.

Identify scrip dividend, stock dividend, elective share distribution, or DRIP.

## Step 2: Dividend Treatment

Read `withholding-notes.md`.

Show gross DPS, withholding rate and basis, net DPS, gross and net yield, broker-observed status, and broker cash-line type.

For scrip / DRIP, state the cash-election assumption and tax, broker, fractional-share, and dilution uncertainty.

## Step 3: Business Fundamentals and Long-Term Trend

Read `business-outlook.md`, `business-fundamentals.md`, and `sector-fcf-proxies.md`.

Identify the dividend funding engine and build the historical operating baseline. Classify Fundamental Trend and select three to five core operating drivers.

Track per-share effects from ordinary issuance, scrip / DRIP, and buyback offsets.

Select the sector model and any holding-company overlay. Build a five-year development thesis with segment/driver baselines, FY+3/FY+5 outcomes, competitive risks, investment/funding needs, and dated milestones that can invalidate the thesis. Separate disclosed facts, guidance and analyst assumptions.

## Step 4: Historical Dividend Record

Build the Dividend Snapshot and Dividend Trajectory. Separate recurring, special, variable, and one-off distributions.

The coverage fields may be backfilled after Step 5.

## Step 5: Historical Cash-Flow Coverage

Reconcile reported FCF/sector capital generation to Recurring Owner FCF and Recurring FAD using the once-only deduction ledger. Preserve actual all-in FCF, exceptional obligations and parent/remittance constraints separately.

Calculate three-year aggregate recurring FAD / relevant cash dividends paid, five-year worst recurring coverage, and worst actual coverage. Do not average ratios, mix declared and paid dividends, or call OPAT cash flow. Missing evidence remains unavailable.

Return to Step 4 and complete coverage fields.

## Step 6: Capital Allocation and Buybacks

Review payout policy, reinvestment, leverage, acquisitions, issuance, ATM, scrip / DRIP, and shareholder returns.

Classify fixed/progressive, earnings-linked, cash-flow-linked, base/variable or discretionary policy and identify its exact calculation base before applying a payout ratio.

Assess true diluted-share-count change and whether buybacks create value or merely offset dilution.

## Step 7: Three-to-Five-Year Fundamental and FCF Forecast

Build Bear, Base, and Bull cases from explicit operating drivers. Derive sector income, profitability, working capital, normalized OCF, maintenance investment, owner cash, remaining growth/capital uses and recurring FAD. Model funding, interest and dilution; growth does not arrive before investment.

Provide detailed FY+1 to FY+3 rows and supported FY+4/FY+5 extensions. Unsupported years retain null values, Not estimable, and a specific reason. Show total and per-share cash trends, the FCF change decomposition, cumulative cash generation and liquidity/self-funding implications. A five-year qualitative outlook is required even when later numerical estimates are unavailable.

Do not apply arbitrary percentage haircuts directly to DPS.

Build one-driver-at-a-time sensitivity for three to five important drivers and classify every row:

- `transient`: temporary; update affected-year cash flow, DPS, and yield only; Accumulation Upper-Bound Change = N/A;
- `persistent`: expected to alter normalized economics; recalculate N before updating boundaries;
- `structural`: rebuild Fundamental Trend, forecast, scoring, veto, and valuation mode.

For growth DDM, transient cash changes affect dated present value only, not terminal growth or ordinary boundaries.

State the evidence basis and nonlinear limitations.

## Step 8: Dividend Forecast Bridge

Use `business-fundamentals.md` Section 2 for the single cash definition: Recurring FAD equals owner cash/proxy less remaining growth and mandatory uses; total distribution capacity additionally deducts exceptional cash uses and includes only explicitly available excess cash. Never deduct capex or capital needs twice.

Build the Distributable-Cash Bridge and Share Count and Scrip / DRIP Assumptions table.

Forecast diluted share count using ordinary issuance, scrip / DRIP participation, and buyback offsets.

Rate Forecast Confidence by horizon. Reconcile the cash model, source units, share units and dividend-entitled versus diluted shares.

## Step 9: Dividend and Yield Runway

Build the single Dividend and Yield Runway:

```text
Policy-Implied Dividend
= stated policy applied to its stated earnings / cash / DPS base

Modeled Dividend Entitlement
= policy-implied amount after explicitly justified funding/policy adjustments

Derived DPS per installment
= Modeled Dividend Entitlement / dividend-entitled share count

Forecast Dividend Cash Cost
= Modeled Dividend Entitlement x cash-settled fraction + settlement cash adjustment

Funding Gap
= max(0, Forecast Dividend Cash Cost - Total Distribution Capacity)

Net Yield at Current Price
= Derived DPS x (1 - withholding rate) / current price
```

Aggregate installment cash cost and DPS separately; use the entitlement and settlement rules in `business-fundamentals.md`. Do not create another table that repeats Dividend Cash Cost and Derived DPS.

Reconcile forecasts across all five year/scenario pairs. Unsupported cash or share inputs must not yield precise DPS, coverage or terminal values.

## Step 10: Dividend Trap Checklist

Check at least:

- high yield caused by price collapse;
- weak normalized coverage;
- payout above FCF;
- rising leverage or refinancing wall;
- debt-, asset-sale-, or equity-funded payout;
- issuance, ATM, or persistent scrip dilution concurrent with elevated payout;
- one-off or peak-cycle distributions treated as recurring;
- weaker policy language or regulatory payout pressure;
- FX mismatch;
- ineffective buybacks;
- forecast DPS inconsistent with business drivers, cash generation, payout policy, or share count;
- N retaining temporary premiums;
- recurring FAD inflated by duplicated add-backs, omitted growth investment, or excess-cash releases;
- sector earnings proxies without capital/remittance evidence;
- growth dividends assuming unfunded reinvestment, unbounded terminal growth or nonexistent cash conversion;
- Structural Decline without a credible finite-life harvest case.

Set Value-Trap Veto to Not triggered / Triggered / Unclear.

## Step 11: Valuation Mode and Entry Framework

Read `buy-zone.md`.

First print a sourced, dated, currency/tax-consistent risk-free anchor, a price-independent risk-premium range and resulting required total return. Do not derive risk from the total score, which contains yield. Resolve any explicit cash-income target separately.

### Ordinary Dividend Asset

Use valuation mode `ordinary_yield_based` and deterministic N, B, r_low, and r_high boundaries.

Always state N value, N basis, source period, and normalization adjustments.

### Eligible Dividend-Growth Asset

Use `total_return_based` only after the evidence gates in `buy-zone.md` pass. Discount the same funded annual dividend path, with a justified transition and bounded terminal growth. Display scenario values, R/g sensitivity, terminal dependence, entry and valuation-review thresholds, plus the separate income entry comparison where credible. Do not force a stock into growth valuation to justify its current price.

### Structural Decline Without Exception

Use valuation mode `suspended`. Do not output Fair, Accumulation, or Strong Buy zones.

### Structural Decline With Harvest / Managed Runoff Exception

Use valuation mode `finite_life_harvest`.

Estimate the present value of finite annual after-tax distributions plus a conservative residual value. Use a discount-rate floor of 10%, state the harvest horizon, and do not assume a perpetual terminal dividend.

Ordinary yield-based zones may be shown only as a secondary cross-check with r_low at least 10%.

If the Value-Trap Veto is triggered, suspend ordinary and growth valuation output; growth cannot bypass the veto.

## Step 12: Holding and Switching Review

Read `holding-review.md`. Link business milestones, cash/solvency warnings, valuation-review levels and portfolio constraints to hold/review/trim/exit/switch or Not Assessed. A price threshold triggers review, not an order.

Compare alternatives only with evidenced prospective cash income and risk-adjusted returns on the same currency/horizon basis, net of taxes, fees and switching costs. Without position size, constraints or an identified alternative, state the missing inputs rather than inventing a trade.
