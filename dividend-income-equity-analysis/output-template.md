# Output Template

This file defines output modes and the Full Analysis section order. Detailed structures live in `screen-mode.md`, `visual-output-rules.md`, `business-fundamentals.md`, and `buy-zone.md`.

## Mode Selection

### Screen Mode

When Screen Mode is triggered, follow `screen-mode.md` only. Do not produce the 18-section Full Analysis.

Required banner:

```text
Mode: Screen
Screening net-yield target: x.x% / Not Assessed
Target basis: user_explicit / portfolio_target / not_assessed
Target policy: hard_minimum / preference / not_assessed
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
This is a first-pass filter, not a full investment analysis.
```

For each ticker, output the compact screening fields, including:

- TTM net yield.
- Screening net-yield target.
- Yield Fit: Pass / Below target / Not Assessed.
- Yield Gap in percentage points or N/A.
- Documented dividend-growth path: Yes / No / Unclear.
- `Full Analysis Recommended: Yes / Watch / No`.

Do not infer a screening target from `buy-zone.md`. If no target is available, use `Not Assessed` and do not reject a stock solely because its yield appears low.

### Full Analysis Mode

Use the following 18 sections.

## 1. Executive Summary

### 1A. Key Metrics at a Glance

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| | | | |

If normalized yield is a range, display `x-y%`.

### 1B. Secondary Summary

- Company:
- Ticker / Exchange:
- As-of date / Price used:
- TTM gross yield:
- TTM net yield:
- Normalized net yield:
- Fundamental Trend:
- Forecast Confidence:
- Valuation mode: ordinary_yield_based / finite_life_harvest / suspended
- Expected buy zone or finite-life value range:
- Value-trap veto:
- Dividend currency / Investor reporting currency:
- Withholding rate / basis:
- Broker-observed withholding / cash-line type:
- Scrip / DRIP available:
- Initial view:

## 2. Dividend Snapshot

One-sentence takeaway, then the authoritative snapshot structure from `visual-output-rules.md`.

## 3. Standard Charts or Text Fallback

Follow `visual-output-rules.md`.

Rich output may include:

1. DPS Structure Chart.
2. Yield Ladder.
3. Coverage Chart.
4. Fundamental Forecast Chart.
5. Buy-Zone Ladder or Finite-Life Cash-Recovery summary.

Plain-text fallback:

- Business and FCF trend:
- DPS path:
- Yield stack:
- Driver sensitivity with type:
- Valuation summary:
- Coverage labels:

## 4. Company and Listing Structure

Describe domicile, listing venue, security type, dividend and reporting currencies, official share count, and scrip / DRIP availability and default election.

## 5. Dividend Treatment

Apply `withholding-notes.md`. State withholding rate, basis, broker-observed status, broker cash-line type, and evidence.

For scrip / DRIP, state whether cash yield assumes an all-cash election and disclose tax, broker, fractional-share, and dilution uncertainty.

## 6. Business Fundamentals and Long-Term Trend

Use `business-fundamentals.md` to show:

- dividend funding engine;
- historical operating trend with sector-appropriate KPIs;
- Fundamental Trend classification;
- three to five core drivers;
- structural, cyclical, competitive, regulatory, and capital-intensity factors;
- per-share dilution from issuance, scrip / DRIP, and buyback offsets.

## 7. Dividend Trajectory and Yearly Yield

Use `visual-output-rules.md` Section 4 and add a Dividend Pattern paragraph.

## 8. Historical Cash-Flow Coverage Bridge

Use `visual-output-rules.md` Section 5. Explain whether historical distributions were funded by recurring cash flow, cash balance, asset sales, debt, equity issuance, or mixed sources.

## 9. Management Capital Allocation

Summarize payout policy, reinvestment, leverage, acquisitions, ordinary issuance, ATM, scrip / DRIP, and shareholder returns.

## 10. Buyback Quality

Assess true diluted-share-count change and whether buybacks create value, offset ordinary issuance, merely neutralize scrip dilution, or are debt-funded.

## 11. Three-Year Fundamental Forecast and Sensitivity

Use `business-fundamentals.md` Sections 6 and 8.

Show Bear, Base, and Bull operating and financial forecasts, then a sensitivity table for three to five material drivers.

Every sensitivity row must be classified:

- transient;
- persistent;
- structural.

Rules:

- Transient: Accumulation Upper-Bound Change = N/A.
- Persistent: recalculate normalized distributable cash and N before updating the boundary.
- Structural: show `Rebuild required`; rerun the full model.

State the evidence basis and local/nonlinear limitations.

## 12. Dividend Forecast Bridge

Use `business-fundamentals.md` Section 7.

Show:

- Distributable-Cash Bridge.
- Share Count and Scrip / DRIP Assumptions.
- Forecast Confidence.

Do not repeat Dividend Cash Cost or Derived DPS here.

## 13. Dividend and Yield Runway

Use the single table in `visual-output-rules.md` Section 6:

- Cash Available for Distribution.
- Payout Policy / Ratio.
- Dividend Cash Cost.
- Derived DPS.
- Net Yield at Current Price.

Values must reconcile to Sections 11 and 12. Do not create a second table with the same DPS and Dividend Cash Cost.

## 14. Dividend Trap Checklist

Test every required item in `workflow.md`, including:

- forecast DPS versus business and cash flow;
- normalized N basis;
- issuance and scrip dilution;
- Structural Decline without credible finite-life harvest logic.

The checklist is a precondition for valuation.

## 15. Expected Buy Zone or Finite-Life Value

Read `buy-zone.md` and first state the valuation mode.

### Ordinary Yield-Based Mode

Include:

- N value, basis, source period, and normalization adjustments;
- B value and source;
- r_low and r_high;
- deterministic Fair, Accumulation, and Strong Buy boundaries;
- historical price and yield context;
- current price position;
- veto status.

### Structural Decline Without Exception

Output:

```text
Valuation mode: suspended
Ordinary buy zone: suspended
```

Do not output Fair, Accumulation, or Strong Buy zones.

### Harvest / Managed Runoff Exception

Use finite-life cash recovery and include:

- harvest horizon;
- annual forecast net distributions;
- discount rate, with a 10% floor;
- residual value and basis;
- present value of distributions;
- finite-life value range;
- optional ordinary yield cross-check with r_low at least 10%.

## 16. Visual Summary

Summarize:

- Business and FCF trend.
- DPS path.
- Yield normalization.
- Main driver sensitivity and type.
- Valuation mode and buy-zone or finite-life result.
- Coverage labels.

## 17. Score, Required Ratings, and Portfolio Role

Use `scoring.md` and show module points.

Output:

- Dividend Quality.
- Dividend Safety.
- Withholding Efficiency.
- Buyback Quality.
- Three-Year Dividend Outlook.
- Portfolio Role.
- Fundamental Trend.
- Forecast Confidence.
- Structural Decline cap applied.
- Harvest / Managed Runoff Exception applied.
- Valuation mode.
- Unadjusted score and overlay-adjusted Grade where applicable.

## 18. Sources and Data Quality

List official filings, announcements, operating statistics, guidance, broker records, historical price sources, and cross-checks.

State missing data, stale data, fallback calculations, forecast assumptions, sensitivity classification, scrip / DRIP assumptions, N basis, valuation mode, and whether future DPS is evidence-backed or illustrative.
