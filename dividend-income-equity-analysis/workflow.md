# Workflow

Use this workflow when reviewing dividend-paying listed companies.

## Mode Selection

Read `screen-mode.md` before research begins.

Use Screen Mode for screening, quick review, candidate-pool work, batch comparison, or multiple tickers where the user asks which names deserve deeper research.

Use Full Analysis for detailed single-stock research, future dividend forecasts, expected buy zones, or explicit investment decisions.

Screen Mode ends after the compact screen output. It must not continue into the Full Analysis steps below.

## Screen Mode Workflow

1. Verify ticker, listing, current price, and as-of date.
2. Estimate TTM net yield with withholding basis.
3. Classify the five-year DPS pattern.
4. Check latest FCF / Dividend or sector-equivalent coverage.
5. Check leverage, regulatory-capital, solvency, or refinancing alerts.
6. Make a preliminary Fundamental Trend classification.
7. Run the abbreviated dividend-trap screen.
8. Output `Full Analysis Recommended: Yes / Watch / No`.

Required limitations:

```text
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
No three-year forecast, N, B, target price, Strong Buy label, or final score.
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

Read `business-fundamentals.md`.

Identify the dividend funding engine and build the historical operating baseline. Classify Fundamental Trend and select three to five core operating drivers.

Track per-share effects from ordinary issuance, scrip / DRIP, and buyback offsets.

## Step 4: Historical Dividend Record

Build the Dividend Snapshot and Dividend Trajectory. Separate recurring, special, variable, and one-off distributions.

The coverage fields may be backfilled after Step 5.

## Step 5: Historical Cash-Flow Coverage

Build the Historical Cash-Flow Coverage Bridge using company-reported FCF or a clearly labelled estimate.

Return to Step 4 and complete coverage fields.

## Step 6: Capital Allocation and Buybacks

Review payout policy, reinvestment, leverage, acquisitions, issuance, ATM, scrip / DRIP, and shareholder returns.

Assess true diluted-share-count change and whether buybacks create value or merely offset dilution.

## Step 7: Three-Year Fundamental Forecast and Sensitivity

Build Bear, Base, and Bull cases from explicit operating drivers. Derive sector-equivalent income, profitability, OCF, capex or capital needs, and FCF / distributable cash.

Do not apply arbitrary percentage haircuts directly to DPS.

Build one-driver-at-a-time sensitivity for three to five important drivers and classify every row:

- `transient`: temporary; update affected-year cash flow, DPS, and yield only; Accumulation Upper-Bound Change = N/A;
- `persistent`: expected to alter normalized economics; recalculate N before updating boundaries;
- `structural`: rebuild Fundamental Trend, forecast, scoring, veto, and valuation mode.

State the evidence basis and nonlinear limitations.

## Step 8: Dividend Forecast Bridge

Calculate:

```text
Cash Available for Distribution
= FCF or sector-equivalent capital generation
- mandatory debt repayment
- regulatory capital requirements
- required maintenance and committed reinvestment
+ justified excess cash
```

Build the Distributable-Cash Bridge and Share Count and Scrip / DRIP Assumptions table.

Forecast diluted share count using ordinary issuance, scrip / DRIP participation, and buyback offsets.

Rate Forecast Confidence.

## Step 9: Dividend and Yield Runway

Build the single Dividend and Yield Runway:

```text
Dividend Cash Cost
= Cash Available for Distribution x expected payout ratio

Derived DPS
= Dividend Cash Cost / diluted share count

Net Yield at Current Price
= Derived DPS x (1 - withholding rate) / current price
```

Do not create another table that repeats Dividend Cash Cost and Derived DPS.

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
- Structural Decline without a credible finite-life harvest case.

Set Value-Trap Veto to Not triggered / Triggered / Unclear.

## Step 11: Valuation Mode and Entry Framework

Read `buy-zone.md`.

### Ordinary Dividend Asset

Use valuation mode `ordinary_yield_based` and deterministic N, B, r_low, and r_high boundaries.

Always state N value, N basis, source period, and normalization adjustments.

### Structural Decline Without Exception

Use valuation mode `suspended`. Do not output Fair, Accumulation, or Strong Buy zones.

### Structural Decline With Harvest / Managed Runoff Exception

Use valuation mode `finite_life_harvest`.

Estimate the present value of finite annual after-tax distributions plus a conservative residual value. Use a discount-rate floor of 10%, state the harvest horizon, and do not assume a perpetual terminal dividend.

Ordinary yield-based zones may be shown only as a secondary cross-check with r_low at least 10%.

If the Value-Trap Veto is triggered, suspend ordinary valuation output.
