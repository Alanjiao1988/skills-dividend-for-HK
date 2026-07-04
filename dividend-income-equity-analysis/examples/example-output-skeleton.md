# Example Output Skeleton

This is a structure example only. It is not a factual stock recommendation and must not be reused as market data.

Use current sources, current price, official filings, broker statements, and the skill rules before producing any real analysis.

## 1. Executive Summary

### 1A. Key Metrics at a Glance

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| 0.0% | 0.0%-0.0% | 00 / C | Watchlist |

### 1B. Secondary Summary

- Company: Example Company
- Ticker: 0000.HK
- Exchange: HKEX
- As-of date: YYYY-MM-DD
- Price used: HKD 0.00
- TTM gross yield: 0.0%
- TTM net yield: 0.0%
- Normalized net yield: 0.0%-0.0%
- Expected buy zone: HKD 0.00-0.00
- Value-trap veto: Not triggered / Triggered / Unclear
- Withholding rate: 0.0%
- Withholding basis: unknown
- Broker-observed withholding: Unknown
- Broker cash-line type if broker statement is used: unknown
- Initial view: Watchlist pending source verification.

## 2. Dividend Snapshot

Takeaway: The snapshot separates headline trailing yield from normalized yield before any long-form discussion.

| Metric | Value | Comment |
|---|---:|---|
| TTM DPS | 0.00 | Placeholder |
| TTM gross yield | 0.0% | Placeholder |
| TTM net yield | 0.0% | Placeholder |
| Normalized DPS | 0.00-0.00 | Placeholder |
| Normalized net yield | 0.0%-0.0% | Placeholder |
| Five-year DPS range | 0.00-0.00 | Placeholder |
| Latest DPS YoY | N/A | Placeholder |
| Dividend type | Unknown | Fixed / progressive / variable / cyclical / one-off |
| Coverage status | Not Available | Strong / Adequate / Weak / Not Available |

## 3. Standard Charts or Text Fallback

Takeaway: Use charts when available; otherwise use compact text visuals.

If rich visualization is available, render:

1. DPS Structure Chart.
2. Yield Ladder.
3. Coverage Chart.
4. Buy-Zone Ladder.

Plain-text fallback:

- DPS path: `FY-4 0.00 -> FY-3 0.00 -> FY-2 0.00 -> FY-1 0.00 -> FY0 0.00`
- Yield stack: `TTM 0.0% | normalized 0.0%-0.0% | bear 0.0% | base 0.0% | bull 0.0%`
- Buy-zone ladder: `Current 0.00 | Fair 0.00-0.00 | Accumulate 0.00-0.00 | Strong buy <0.00 | Veto: not triggered`
- Coverage labels: `FY-4 N/A | FY-3 N/A | FY-2 N/A | FY-1 N/A | FY0 N/A`

## 4. Company and Listing Structure

Takeaway: Identify the legal structure before estimating withholding or dividend quality.

Describe domicile, issuer type, listing venue, dividend currency, reporting currency, official share count from filings, and security type.

## 5. Dividend Treatment

Takeaway: Withholding treatment must follow `withholding-notes.md`, and broker PIL lines are not withholding evidence.

- Withholding rate: 0.0%
- Withholding basis: unknown
- Broker-observed withholding: Unknown
- Broker cash-line type: unknown
- Evidence: pending official announcement or broker statement.

If withholding is 0%, state once: "Withholding 0% — gross equals net."

## 6. Dividend Trajectory and Yearly Yield

Takeaway: The dividend path shows whether income is stable, growing, cyclical, or one-off.

Use `visual-output-rules.md` Section 4 for authoritative table structures.

### 6A. Per-share DPS Structure

| Fiscal Year | Total DPS | Base DPS | Special / Variable DPS | DPS YoY | Quality Tag | Notes |
|---|---:|---:|---:|---:|---|---|
| FY-4 | 0.00 | 0.00 | 0.00 | N/A | Not Available | Placeholder |
| FY-3 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY-2 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY-1 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY0 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |

### 6B. Yield and Coverage

| Fiscal Year | Yield at Current Price | Yield at Year Price | Payout Ratio | FCF / Dividend | Coverage Label | Comment |
|---|---:|---:|---:|---:|---|---|
| FY-4 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-3 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-2 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-1 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY0 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |

Dividend Pattern: State whether the stock is stable income, progressive income, formula-based variable income, cycle income, or one-off distribution.

## 7. Cash-Flow Coverage Bridge

Takeaway: The bridge shows whether dividends were funded by operating free cash flow, cash balance, asset sales, debt, or equity issuance.

Use `visual-output-rules.md` Section 5 for authoritative bridge structures.

### 7A. Cash Generation

| Fiscal Year | Net Income | Operating Cash Flow | Capex | Free Cash Flow | FCF Quality | Comment |
|---|---:|---:|---:|---:|---|---|
| FY-4 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-3 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-2 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-1 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY0 | N/A | N/A | N/A | N/A | Not Available | Placeholder |

### 7B. Cash Return and Funding

| Fiscal Year | Cash Dividends | Buybacks | Share Issuance | Net Debt Change | FCF / Dividend | Funding Source |
|---|---:|---:|---:|---:|---:|---|
| FY-4 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-3 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-2 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-1 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY0 | N/A | N/A | N/A | N/A | N/A | Not Available |

Explain whether FCF is company-reported or estimated as operating cash flow minus capex.

## 8. Management Capital Allocation

Takeaway: Management policy determines whether dividends are a commitment, formula, or residual payout.

Summarize dividend policy, buyback policy, leverage target, reinvestment priority, acquisition policy, share issuance, ATM programs, and whether equity issuance coincides with elevated payout.

## 9. Buyback Quality

Takeaway: Buybacks matter only if they reduce share count without weakening the balance sheet.

Assess share-count change, dilution, valuation discipline, whether buybacks are debt-funded, and whether buybacks are offset by share issuance.

## 10. Three-Year Dividend Runway

Takeaway: The runway converts dividend scenarios into net yield and cash-flow coverage.

Use `visual-output-rules.md` Section 9 for authoritative runway structure.

| Fiscal Year | Scenario | DPS | Net Yield at Current Price | Estimated FCF | Dividend Cash Cost | FCF / Dividend |
|---|---|---:|---:|---:|---:|---:|
| FY+1 | Bear | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Base | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Bull | N/A | N/A | N/A | N/A | N/A |
| FY+2 | Bear | N/A | N/A | N/A | N/A | N/A |
| FY+2 | Base | N/A | N/A | N/A | N/A | N/A |
| FY+2 | Bull | N/A | N/A | N/A | N/A | N/A |
| FY+3 | Bear | N/A | N/A | N/A | N/A | N/A |
| FY+3 | Base | N/A | N/A | N/A | N/A | N/A |
| FY+3 | Bull | N/A | N/A | N/A | N/A | N/A |

## 11. Dividend Trap Checklist

Takeaway: The checklist separates high yield from sustainable income and acts as the buy-zone veto gate.

| Red Flag | Status | Evidence |
|---|---|---|
| High yield from price fall | Unknown | Placeholder |
| Weak cash-flow coverage | Unknown | Placeholder |
| Payout above free cash flow | Unknown | Placeholder |
| Rising leverage | Unknown | Placeholder |
| Debt-funded payout | Unknown | Placeholder |
| Asset-sale-funded payout | Unknown | Placeholder |
| Equity issuance or ATM concurrent with elevated payout | Unknown | Placeholder |
| Special or variable dividends treated as recurring | Unknown | Placeholder |
| Weaker policy language | Unknown | Placeholder |
| Regulatory pressure | Unknown | Placeholder |
| Refinancing wall | Unknown | Placeholder |
| Cycle peak payout | Unknown | Placeholder |
| FX mismatch | Unknown | Placeholder |
| Ineffective buybacks or buybacks offset by issuance | Unknown | Placeholder |

Value-trap veto: Not triggered / Triggered / Unclear.

## 12. Expected Buy Zone

Takeaway: The buy zone translates normalized net DPS and required net yield into an income entry range, subject to the value-trap veto.

Use `buy-zone.md` for authoritative buy-zone logic.

Formula:

```text
Buy Price = Net DPS / Required Net Yield
```

Boundary inputs:

- N = normalized net DPS: 0.00
- B = bear-case net DPS: 0.00
- r_low = 0.0%
- r_high = 0.0%

### 12A. Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|
| Current price | 0.00 | N/A | Placeholder |
| 52-week high | N/A | N/A | Placeholder |
| 52-week low | N/A | N/A | Placeholder |
| 3-year median | N/A | N/A | Placeholder |
| 5-year median | N/A | N/A | Placeholder |
| Historical net-yield range | N/A | N/A | Placeholder |

### 12B. Buy-Zone Table

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Below required range | Normalized DPS | Yield below required return | Avoid adding |
| Fair value / hold | N / r_high < Price <= N / r_low | Required range | Normalized DPS | Fair yield, limited MOS | Hold |
| Accumulation zone | B / r_low < Price <= N / r_high | Attractive normalized yield | Normalized + bear DPS | Required yield met | Gradual buy |
| Strong buy zone | Price <= B / r_low | Bear-case yield meets minimum | Bear / conservative DPS | Strong coverage required | Higher conviction buy |

Value-trap veto: Not triggered / Triggered / Unclear.

## 13. Visual Summary

- DPS path: `FY-4 0.00 -> FY-3 0.00 -> FY-2 0.00 -> FY-1 0.00 -> FY0 0.00`
- Yield normalization: `TTM 0.0% vs normalized 0.0%-0.0% vs bear/base/bull N/A`
- Buy-zone ladder: `Current 0.00 | Fair N/A | Accumulate N/A | Strong buy N/A | Veto N/A`
- Coverage labels by year: `FY-4 N/A | FY-3 N/A | FY-2 N/A | FY-1 N/A | FY0 N/A`

## 14. Score, Required Ratings, and Portfolio Role

Takeaway: The final rating combines yield, stability, FCF coverage, balance sheet, management, buybacks, and visibility.

| Module | Weight | Score | Comment |
|---|---:|---:|---|
| Net dividend yield | 15 | 0 | Placeholder |
| Five-year dividend stability | 15 | 0 | Placeholder |
| Free cash-flow coverage | 20 | 0 | Placeholder |
| Balance-sheet safety | 15 | 0 | Placeholder |
| Management capital allocation | 15 | 0 | Placeholder |
| Buyback quality | 10 | 0 | Placeholder |
| Three-year visibility | 10 | 0 | Placeholder |
| Total | 100 | 0 | Placeholder |

Required ratings:

- Dividend Quality: Medium
- Dividend Safety: Unclear
- Withholding Efficiency: Medium
- Buyback Quality: Not Applicable
- Three-Year Dividend Outlook: High Uncertainty
- Portfolio Role: Watchlist

## 15. Sources and Data Quality

List official filings, announcements, broker records, and third-party cross-checks used.

Data quality notes:

- This skeleton contains placeholders only.
- Replace all placeholders with current, cited data before using for any real ticker.
- State missing data, fallback calculations, broker-statement uncertainty, historical price limitations, and buy-zone assumptions clearly.
