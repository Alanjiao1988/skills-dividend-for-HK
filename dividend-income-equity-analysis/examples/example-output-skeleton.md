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
- Fundamental trend: Stable / Mature
- Forecast confidence: Medium
- Value-trap veto: Not triggered / Triggered / Unclear
- Withholding rate: 0.0%
- Withholding basis: unknown
- Broker-observed withholding: Unknown
- Broker cash-line type if broker statement is used: unknown
- Initial view: Watchlist pending source verification.

## 2. Dividend Snapshot

Takeaway: The snapshot separates headline trailing yield from fundamentally normalized yield.

| Metric | Value | Comment |
|---|---:|---|
| TTM DPS | 0.00 | Placeholder |
| TTM gross yield | 0.0% | Placeholder |
| TTM net yield | 0.0% | Placeholder |
| Normalized DPS | 0.00-0.00 | Derived from Base forecast |
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
4. Fundamental Forecast Chart.
5. Buy-Zone Ladder.

Plain-text fallback:

- Business and FCF trend: `Historical stable -> Base modest growth -> Bear decline -> Bull upside`
- DPS path: `FY-4 0.00 -> FY-3 0.00 -> FY-2 0.00 -> FY-1 0.00 -> FY0 0.00`
- Yield stack: `TTM 0.0% | normalized 0.0%-0.0% | bear 0.0% | base 0.0% | bull 0.0%`
- Buy-zone ladder: `Current 0.00 | Fair 0.00-0.00 | Accumulate 0.00-0.00 | Strong buy <0.00 | Confidence: Medium | Veto: not triggered`
- Coverage labels: `FY-4 N/A | FY-3 N/A | FY-2 N/A | FY-1 N/A | FY0 N/A`

## 4. Company and Listing Structure

Takeaway: Identify legal and listing structure before estimating withholding, share count, and per-share economics.

Describe domicile, issuer type, listing venue, dividend currency, reporting currency, official diluted share count, and security type.

## 5. Dividend Treatment

Takeaway: Withholding treatment must follow `withholding-notes.md`, and PIL lines are not withholding evidence.

- Withholding rate: 0.0%
- Withholding basis: unknown
- Broker-observed withholding: Unknown
- Broker cash-line type: unknown
- Evidence: pending official announcement or broker statement.

If withholding is 0%, state once: "Withholding 0% — gross equals net."

## 6. Business Fundamentals and Long-Term Trend

Takeaway: The dividend is funded by the company's core operating engine, not by its historical DPS record alone.

- Dividend funding engine: Placeholder.
- Main segments: Placeholder.
- Fundamental trend: Stable / Mature.
- Core drivers: Driver 1; Driver 2; Driver 3.
- Main long-term risk: Placeholder.

### Historical Operating Trend

| Fiscal Year | Primary Business Driver | Revenue / Sector Income | Operating Margin / Equivalent | Net Income / AFFO | FCF / Distributable Cash | Comment |
|---|---|---:|---:|---:|---:|---|
| FY-4 | Placeholder | N/A | N/A | N/A | N/A | Placeholder |
| FY-3 | Placeholder | N/A | N/A | N/A | N/A | Placeholder |
| FY-2 | Placeholder | N/A | N/A | N/A | N/A | Placeholder |
| FY-1 | Placeholder | N/A | N/A | N/A | N/A | Placeholder |
| FY0 | Placeholder | N/A | N/A | N/A | N/A | Placeholder |

## 7. Dividend Trajectory and Yearly Yield

Takeaway: The historical dividend path shows whether income has been stable, progressive, cyclical, or one-off.

### 7A. Per-share DPS Structure

| Fiscal Year | Total DPS | Base DPS | Special / Variable DPS | DPS YoY | Quality Tag | Notes |
|---|---:|---:|---:|---:|---|---|
| FY-4 | 0.00 | 0.00 | 0.00 | N/A | Not Available | Placeholder |
| FY-3 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY-2 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY-1 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |
| FY0 | 0.00 | 0.00 | 0.00 | 0.0% | Not Available | Placeholder |

### 7B. Yield and Coverage

| Fiscal Year | Yield at Current Price | Yield at Year Price | Payout Ratio | FCF / Dividend | Coverage Label | Comment |
|---|---:|---:|---:|---:|---|---|
| FY-4 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-3 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-2 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY-1 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |
| FY0 | 0.0% | N/A | N/A | N/A | Not Available | Placeholder |

Dividend Pattern: Placeholder.

## 8. Historical Cash-Flow Coverage Bridge

Takeaway: Historical payout quality depends on whether dividends came from recurring cash generation.

### 8A. Cash Generation

| Fiscal Year | Net Income | Operating Cash Flow | Capex | Free Cash Flow | FCF Quality | Comment |
|---|---:|---:|---:|---:|---|---|
| FY-4 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-3 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-2 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY-1 | N/A | N/A | N/A | N/A | Not Available | Placeholder |
| FY0 | N/A | N/A | N/A | N/A | Not Available | Placeholder |

### 8B. Cash Return and Funding

| Fiscal Year | Cash Dividends | Buybacks | Share Issuance | Net Debt Change | FCF / Dividend | Funding Source |
|---|---:|---:|---:|---:|---:|---|
| FY-4 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-3 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-2 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY-1 | N/A | N/A | N/A | N/A | N/A | Not Available |
| FY0 | N/A | N/A | N/A | N/A | N/A | Not Available |

## 9. Management Capital Allocation

Takeaway: Management policy determines how much operating cash reaches shareholders.

Summarize payout policy, leverage target, reinvestment, acquisitions, issuance, and shareholder-return priorities.

## 10. Buyback Quality

Takeaway: Buybacks create value only when they reduce diluted share count at sensible prices without weakening the balance sheet.

Assess share-count change, dilution, valuation discipline, and funding source.

## 11. Three-Year Fundamental Forecast

Takeaway: Future DPS begins with explicit business and cash-flow assumptions.

### 11A. Operating Driver Forecast

| Fiscal Year | Scenario | Primary Driver | Price / Mix Driver | Margin / Credit / Cost Driver | Capital-Intensity Driver | Key Assumptions |
|---|---|---|---|---|---|---|
| FY+1 | Bear | Placeholder | Placeholder | Placeholder | Placeholder | Placeholder |
| FY+1 | Base | Placeholder | Placeholder | Placeholder | Placeholder | Placeholder |
| FY+1 | Bull | Placeholder | Placeholder | Placeholder | Placeholder | Placeholder |

Repeat Bear / Base / Bull for FY+2 and FY+3.

### 11B. Financial Forecast

| Fiscal Year | Scenario | Revenue / Sector Income | Net Income / AFFO | Operating Cash Flow | Capex / Capital Need | FCF / Distributable Cash |
|---|---|---:|---:|---:|---:|---:|
| FY+1 | Bear | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Base | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Bull | N/A | N/A | N/A | N/A | N/A |

Repeat Bear / Base / Bull for FY+2 and FY+3.

## 12. Dividend Forecast Bridge

Takeaway: Forecast DPS must reconcile to distributable cash, payout policy, and diluted share count.

### 12A. Distributable-Cash Bridge

| Fiscal Year | Scenario | Net Income / AFFO | FCF / Capital Generation | Mandatory Debt / Regulatory Uses | Required Reinvestment | Cash Available for Distribution |
|---|---|---:|---:|---:|---:|---:|
| FY+1 | Bear | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Base | N/A | N/A | N/A | N/A | N/A |
| FY+1 | Bull | N/A | N/A | N/A | N/A | N/A |

### 12B. DPS Derivation

| Fiscal Year | Scenario | Cash Available for Distribution | Payout Policy / Ratio | Dividend Cash Cost | Diluted Share Count | Derived DPS |
|---|---|---:|---|---:|---:|---:|
| FY+1 | Bear | N/A | Placeholder | N/A | N/A | N/A |
| FY+1 | Base | N/A | Placeholder | N/A | N/A | N/A |
| FY+1 | Bull | N/A | Placeholder | N/A | N/A | N/A |

Forecast Confidence: High / Medium / Low / Not Forecastable.

## 13. Three-Year Dividend Runway

Takeaway: The runway shows the yield and coverage produced by the derived DPS scenarios.

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

DPS source: Evidence-backed / Illustrative / Historical fallback / Unknown.

## 14. Dividend Trap Checklist

Takeaway: The checklist separates high yield from sustainable income and acts as the buy-zone veto gate.

Keep this checklist aligned with `workflow.md` Step 10; do not shorten it in real outputs.

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
| Fundamental forecast conflicts with assumed DPS | Unknown | Placeholder |
| DPS cannot reconcile to distributable cash and share count | Unknown | Placeholder |

Value-trap veto: Not triggered / Triggered / Unclear.

## 15. Expected Buy Zone

Takeaway: The buy zone uses fundamentally derived Base and Bear net DPS, not a convenient historical average.

Boundary inputs:

- N = Base-derived normalized net DPS: 0.00
- N source: Base fundamental forecast + Dividend Forecast Bridge
- B = Bear-derived net DPS: 0.00
- B source: Bear fundamental forecast + Dividend Forecast Bridge
- Forecast Confidence: Medium
- r_low = 0.0%
- r_high = 0.0%

### 15A. Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|
| Current price | 0.00 | N/A | Placeholder |
| 52-week high | N/A | N/A | Placeholder |
| 52-week low | N/A | N/A | Placeholder |
| 3-year median | N/A | N/A | Placeholder |
| 5-year median | N/A | N/A | Placeholder |
| Historical net-yield range | N/A | N/A | Placeholder |

### 15B. Buy-Zone Table

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Below required range | Base-derived N | Yield below required return | Avoid adding |
| Fair value / hold | N / r_high < Price <= N / r_low | Required range | Base-derived N | Fair yield, limited MOS | Hold |
| Accumulation zone | B / r_high < Price <= N / r_high | Attractive normalized yield | Base N + Bear B | Required yield met | Gradual buy |
| Strong buy zone | Price <= B / r_high | Bear yield meets high-end requirement | Bear-derived B | Strong coverage required | Higher conviction buy |

Value-trap veto: Not triggered / Triggered / Unclear.

## 16. Visual Summary

- Business and FCF trend: `Placeholder`
- DPS path: `FY-4 0.00 -> FY-3 0.00 -> FY-2 0.00 -> FY-1 0.00 -> FY0 0.00`
- Yield normalization: `TTM 0.0% vs normalized 0.0%-0.0% vs bear/base/bull N/A`
- Buy-zone ladder: `Current 0.00 | Fair N/A | Accumulate N/A | Strong buy N/A | Confidence N/A | Veto N/A`
- Coverage labels by year: `FY-4 N/A | FY-3 N/A | FY-2 N/A | FY-1 N/A | FY0 N/A`

## 17. Score, Required Ratings, and Portfolio Role

Takeaway: The final rating combines yield, stability, cash coverage, balance sheet, management, buybacks, and evidence-backed visibility.

| Module | Weight | Score | Comment |
|---|---:|---:|---|
| Net dividend yield | 15 | 0 | Placeholder |
| Five-year dividend stability | 15 | 0 | Placeholder |
| Free cash-flow coverage | 20 | 0 | Placeholder |
| Balance-sheet safety | 15 | 0 | Placeholder |
| Management capital allocation | 15 | 0 | Placeholder |
| Buyback quality | 10 | 0 | Placeholder |
| Three-year fundamental and dividend visibility | 10 | 0 | Placeholder |
| Total | 100 | 0 | Placeholder |

Required ratings:

- Dividend Quality: Medium
- Dividend Safety: Unclear
- Withholding Efficiency: Medium
- Buyback Quality: Not Applicable
- Three-Year Dividend Outlook: High Uncertainty
- Portfolio Role: Watchlist
- Fundamental Trend: Stable / Mature
- Forecast Confidence: Medium

## 18. Sources and Data Quality

List official filings, announcements, operating statistics, guidance, broker records, historical price sources, and third-party cross-checks used.

Data quality notes:

- This skeleton contains placeholders only.
- Replace all placeholders with current, cited data before using for any real ticker.
- State missing data, fallback calculations, broker-statement uncertainty, forecast assumptions, historical price limitations, and whether future DPS is evidence-backed or illustrative.
