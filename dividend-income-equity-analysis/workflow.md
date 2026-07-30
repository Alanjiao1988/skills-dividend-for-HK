# Workflow

Use this workflow when reviewing a dividend-paying listed company.

## Data Rules

Always record the data date.

- Price must include as-of date and exchange.
- Dividend history should come from official announcements or annual reports when available.
- Latest dividend announcement must be checked for currency, record date, ex-date, payment date, and special dividend treatment.
- Historical and forecast business data must distinguish reported facts, company guidance, consensus cross-checks, and analyst estimates.
- Third-party data is for cross-checks only.
- User broker statement is the priority source for actual received dividend and actual withholding.
- Use official share count from filings when available. Do not infer market capitalization from net income divided by EPS unless no filing share-count data is available.
- Historical price data used for buy-zone analysis must state period, frequency, source, and whether the price is year-end, average, close, high-low range, or adjusted price.

## Search Instructions

When web search is available, actively search official disclosure sources before relying on third-party data.

For HK-listed stocks, search HKEXnews / issuer announcements for:

- latest annual report
- latest interim report
- latest results announcement
- latest dividend announcement
- tax note in dividend announcement
- segment revenue and profit disclosure
- business operating statistics and management guidance
- cash-flow statement and capex guidance
- share buyback announcement
- historical dividend announcements
- historical share price or exchange price data when available

For US-listed stocks, search SEC EDGAR and company investor relations for 10-K, 10-Q, 8-K, proxy, earnings presentation, segment disclosures, operating KPIs, management guidance, dividend declaration, buyback authorization, latest 10-Q cover page share count, cash-flow statement, capex, share issuance, and ATM or shelf-registration filings.

For UK-listed stocks, search LSE RNS and company investor relations for annual report, results announcement, operating KPIs, guidance, dividend declaration, and buyback programme.

## Source Order

1. Official exchange announcement and company filings.
2. Annual report, interim report, results announcement, dividend announcement, operating statistics, guidance, and buyback announcement.
3. Company investor relations page and management commentary.
4. User broker statement.
5. Third-party data for validation only.

## Step 1: Classification

Collect company name, ticker, exchange, legal domicile, operating geography, reporting currency, dividend currency, and listing structure.

Classify the security as local company, H-share, red-chip, P-chip, ADR, REIT, BDC, MLP, fund, trust, ETF, or ordinary company.

## Step 2: Dividend Treatment

Read `withholding-notes.md` before calculating net yield. Use broker-observed withholding first when available.

Show gross DPS, assumed withholding rate, withholding basis, net DPS, gross yield, and net yield.

If broker records are used, identify whether the cash line is a normal dividend, payment in lieu, mixed, or unknown.

## Step 3: Business Fundamentals and Long-Term Trend

Read `business-fundamentals.md`.

Identify the business segments and economic engine that actually fund dividends. Build the historical operating baseline and classify the three-to-five-year trend as Structural Growth, Stable / Mature, Cyclical Recovery, Cyclical Peak / Normalization Risk, Structural Decline, or Transformation / High Uncertainty.

Select three to five core operating drivers. Use sector-appropriate measures rather than forcing revenue or EBITDA onto every industry.

## Step 4: Historical Dividend Record

For full analysis, follow `visual-output-rules.md` and `output-template.md`. Build the Dividend Snapshot and the DPS structure part of the Dividend Trajectory before long-form discussion.

Separate ordinary dividends from special or variable dividends. Do not annualize one-off special dividends.

The Yield and Coverage part of the Dividend Trajectory may be completed or backfilled after Step 5, because FCF / Dividend and Coverage Label depend on the cash-flow bridge.

## Step 5: Historical Cash-Flow Coverage

For full analysis, build the Cash-Flow Coverage Bridge using the structures in `visual-output-rules.md`.

Use company-reported free cash flow if available. If not available, estimate free cash flow as operating cash flow minus capex and label it as estimated. EBITDA coverage can be mentioned only as a secondary cross-check.

After this step, return to Step 4 and fill any missing FCF / Dividend and Coverage Label fields in the Dividend Trajectory.

## Step 6: Capital Allocation and Buybacks

Review comments on dividends, buybacks, leverage, reinvestment, acquisitions, share issuance, ATM programs, and shareholder returns.

Identify whether the company has a fixed dividend, progressive dividend, payout-ratio policy, variable policy, or discretionary policy.

Assess whether buybacks create real per-share value or are offset by dilution.

## Step 7: Three-Year Fundamental Forecast

Use `business-fundamentals.md` to build Bear, Base, and Bull cases for each of the next three fiscal years.

Forecast explicit operating drivers first, then derive revenue or sector-equivalent income, net income / AFFO / capital generation, operating cash flow, capex or capital needs, and FCF / distributable cash.

Do not create the scenarios by applying arbitrary percentage haircuts directly to DPS.

## Step 8: Dividend Forecast Bridge

Translate the fundamental forecast into dividend capacity.

Calculate:

```text
Cash Available for Distribution
= FCF or sector-equivalent capital generation
- mandatory debt repayment
- regulatory capital requirements
- required maintenance and committed reinvestment
+ justified excess cash

Dividend Cash Cost
= Cash Available for Distribution x expected payout ratio

Derived DPS
= Dividend Cash Cost / diluted share count
```

For fixed or progressive policies, compare derived capacity with the expected or promised DPS. For variable or formula-based policies, apply the policy to normalized distributable cash.

Rate forecast confidence as High, Medium, Low, or Not Forecastable.

## Step 9: Three-Year Dividend Runway

Build the Three-Year Dividend Runway from the derived DPS in Step 8. Follow the table in `visual-output-rules.md`, including DPS, net yield at current price, estimated FCF, dividend cash cost, FCF / Dividend, balance-sheet impact, and assumptions.

The DPS values in the runway must trace back to Step 7 and Step 8. If they do not, label the scenarios illustrative rather than evidence-backed.

## Step 10: Dividend Trap Checklist

Check at least:

- High yield from price fall.
- Weak cash-flow coverage.
- Payout above free cash flow.
- Rising leverage.
- Debt-funded payout.
- Asset-sale-funded payout.
- Equity issuance or ATM program concurrent with elevated payout.
- Special or variable dividends treated as recurring income.
- Weaker policy language.
- Regulatory pressure.
- Refinancing wall.
- Cycle peak payout.
- FX mismatch.
- Ineffective buybacks or buybacks offset by issuance.
- Fundamental forecast implies declining distributable cash while DPS is assumed stable or growing.
- Forecast DPS cannot be reconciled to operating drivers, cash generation, payout policy, and share count.

Flag whether a value-trap veto is Not triggered, Triggered, or Unclear. The veto result is a precondition for Step 11.

## Step 11: Expected Buy Zone

Read `buy-zone.md` and build an expected buy-zone analysis.

Use:

- Current price and as-of date.
- Historical price range, year-end price, average price, or high-low range.
- Historical gross and net dividend yield range.
- Normalized net DPS derived from the Base fundamental forecast and Dividend Forecast Bridge.
- Bear net DPS derived from the Bear fundamental forecast and Dividend Forecast Bridge.
- Required net yield based on dividend profile and risk.
- FCF coverage, balance-sheet safety, forecast confidence, dividend visibility, and Step 10 value-trap veto status.

Core formula:

```text
Buy Price = Net DPS / Required Net Yield
```

Use the deterministic boundaries in `buy-zone.md` based on N, B, r_low, and r_high. Do not choose N or B merely to justify a preferred target price. Historical DPS averages are fallback cross-checks only.

If the value-trap veto is triggered, suspend ordinary buy-zone output or label it as special-situation only.
