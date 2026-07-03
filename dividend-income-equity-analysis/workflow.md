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

## Search Instructions

When web search is available, actively search official disclosure sources before relying on third-party data.

For HK-listed stocks, search HKEXnews / issuer announcements for:

- latest annual report
- latest interim report
- latest results announcement
- latest dividend announcement
- tax note in dividend announcement
- share buyback announcement

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

## Step 3: Dividend Record

For full analysis, follow `visual-output-rules.md` and `output-template.md`. Build the Dividend Snapshot and Dividend Trajectory tables before long-form discussion.

Separate ordinary dividends from special or variable dividends. Do not annualize one-off special dividends.

## Step 4: Cash-Flow Coverage

For full analysis, build the Cash-Flow Coverage Bridge from `output-template.md`.

Use company-reported free cash flow if available. If not available, estimate free cash flow as operating cash flow minus capex and label it as estimated. EBITDA coverage can be mentioned only as a secondary cross-check.

## Step 5: Capital Allocation

Review comments on dividends, buybacks, leverage, reinvestment, acquisitions, share issuance, ATM programs, and shareholder returns.

Identify whether the company has a fixed dividend, progressive dividend, payout-ratio policy, variable policy, or discretionary policy.

## Step 6: Three-Year Outlook

Build bear, base, and bull cases for the next three fiscal years. Follow the Three-Year Dividend Runway table in `output-template.md`, including DPS, net yield at current price, estimated FCF, dividend cash cost, FCF / Dividend, balance-sheet impact, and assumptions.

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
