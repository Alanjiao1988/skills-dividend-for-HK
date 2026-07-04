# Workflow

Use this workflow when reviewing a dividend-paying listed company.

## Data Rules

Always record the data date.

- Price must include as-of date and exchange.
- Dividend history should come from official announcements or annual reports when available.
- Latest dividend announcement must be checked for currency, record date, ex-date, payment date, and special dividend treatment.
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
- share buyback announcement
- historical dividend announcements
- historical share price or exchange price data when available

For US-listed stocks, search SEC EDGAR and company investor relations for 10-K, 10-Q, 8-K, proxy, dividend declaration, buyback authorization, latest 10-Q cover page share count, cash-flow statement, capex, share issuance, and ATM or shelf-registration filings.

For UK-listed stocks, search LSE RNS and company investor relations for annual report, dividend declaration, and buyback programme.

## Source Order

1. Official exchange announcement and company filings.
2. Annual report, interim report, results announcement, dividend announcement, and buyback announcement.
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

## Step 3: Dividend Record

For full analysis, follow `visual-output-rules.md` and `output-template.md`. Build the Dividend Snapshot and the DPS structure part of the Dividend Trajectory before long-form discussion.

Separate ordinary dividends from special or variable dividends. Do not annualize one-off special dividends.

The Yield and Coverage part of the Dividend Trajectory may be completed or backfilled after Step 4, because FCF / Dividend and Coverage Label depend on the cash-flow bridge.

## Step 4: Cash-Flow Coverage

For full analysis, build the Cash-Flow Coverage Bridge using the structures in `visual-output-rules.md`.

Use company-reported free cash flow if available. If not available, estimate free cash flow as operating cash flow minus capex and label it as estimated. EBITDA coverage can be mentioned only as a secondary cross-check.

After this step, return to Step 3 and fill any missing FCF / Dividend and Coverage Label fields in the Dividend Trajectory.

## Step 5: Capital Allocation

Review comments on dividends, buybacks, leverage, reinvestment, acquisitions, share issuance, ATM programs, and shareholder returns.

Identify whether the company has a fixed dividend, progressive dividend, payout-ratio policy, variable policy, or discretionary policy.

## Step 6: Three-Year Outlook

Build bear, base, and bull cases for the next three fiscal years. Follow the Three-Year Dividend Runway table in `visual-output-rules.md`, including DPS, net yield at current price, estimated FCF, dividend cash cost, FCF / Dividend, balance-sheet impact, and assumptions.

## Step 7: Dividend Trap Checklist

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

Flag whether a value-trap veto is Not triggered, Triggered, or Unclear. The veto result is a precondition for Step 8.

## Step 8: Expected Buy Zone

Read `buy-zone.md` and build an expected buy-zone analysis.

Use:

- Current price and as-of date.
- Historical price range, year-end price, average price, or high-low range.
- Historical gross and net dividend yield range.
- Normalized net DPS.
- Bear, base, and bull forecast net DPS.
- Required net yield based on dividend profile and risk.
- FCF coverage, balance-sheet safety, dividend visibility, and Step 7 value-trap veto status.

Core formula:

```text
Buy Price = Net DPS / Required Net Yield
```

Use the deterministic boundaries in `buy-zone.md` based on N, B, r_low, and r_high. State whether the buy-zone uses TTM DPS, normalized DPS, bear DPS, base DPS, or bull DPS. Do not use peak-cycle DPS as the base-case buy-zone anchor unless it is demonstrably sustainable.

If the value-trap veto is triggered, suspend ordinary buy-zone output or label it as special-situation only.
