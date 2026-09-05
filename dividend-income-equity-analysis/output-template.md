# Output Template

This file defines output modes and the 18-section Full Analysis order. Detailed rules live in the canonical screen, outlook, cash-flow, sector, valuation, visual and holding-review modules.

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
- Valuation mode: ordinary_yield_based / total_return_based / finite_life_harvest / suspended
- Expected buy zone or finite-life value range:
- Income fit versus growth-value conclusion:
- Three-to-five-year business / per-share FCF thesis:
- Three-year aggregate / five-year worst recurring coverage:
- Holding-review status:
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
5. Income ladder, conditional Growth-Value Range, or Finite-Life Cash-Recovery summary.

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

## 6. Business Fundamentals and Three-to-Five-Year Outlook

Use `business-fundamentals.md` to show:

- dividend funding engine;
- historical operating trend with sector-appropriate KPIs;
- Fundamental Trend classification;
- three to five core drivers;
- structural, cyclical, competitive, regulatory, and capital-intensity factors;
- per-share dilution from issuance, scrip / DRIP, and buyback offsets.

Use `business-outlook.md` for segment/driver baselines, FY+3/FY+5 outcomes, competitive position, management delivery, project timing, reinvestment/funding, scenario theses and dated invalidation milestones. State the sector proxy and any holding-company overlay from `sector-fcf-proxies.md`. Missing quantitative evidence does not remove the qualitative five-year outlook.

## 7. Dividend Trajectory and Yearly Yield

Use `visual-output-rules.md` Section 4 and add a Dividend Pattern paragraph.

## 8. Historical Cash-Flow Coverage Bridge

Use `visual-output-rules.md` Section 5. Explain whether historical distributions were funded by recurring cash flow, cash balance, asset sales, debt, equity issuance, or mixed sources.

Reconcile reported FCF/proxy to Recurring Owner FCF, recurring FAD and actual cash affordability. Show the once-only deduction ledger, three-year aggregate coverage, five-year worst recurring coverage and worst actual coverage with year and funding source. Identify insufficient/comparability-limited histories.

## 9. Management Capital Allocation

Summarize payout policy, reinvestment, leverage, acquisitions, ordinary issuance, ATM, scrip / DRIP, and shareholder returns.

State policy type, exact earnings/cash/DPS calculation base, source and capital/funding constraints.

## 10. Buyback Quality

Assess true diluted-share-count change and whether buybacks create value, offset ordinary issuance, merely neutralize scrip dilution, or are debt-funded.

## 11. Three-to-Five-Year Fundamental and FCF Forecast

Use `business-fundamentals.md` Sections 6 and 8.

Show detailed annual Bear/Base/Bull operating and FCF forecasts for FY+1 to FY+3 and supported FY+4/FY+5 extensions. Retain unsupported rows as Not estimable with null values and reasons. Include working capital, maintenance/growth investment, owner claims, financing/capital needs, total/per-share cash outlook, cumulative FAD, cash-conversion timing and liquidity trough. Explain changes in FCF by driver, not just the final CAGR.

Then show sensitivity for three to five material drivers.

Every sensitivity row must be classified:

- transient;
- persistent;
- structural.

Rules:

- Transient: Accumulation Upper-Bound Change = N/A.
- Transient in growth valuation: show the affected-year discounted cash impact separately; do not change terminal growth.
- Persistent: recalculate normalized distributable cash and N before updating the boundary.
- Structural: show `Rebuild required`; rerun the full model.

State the evidence basis and local/nonlinear limitations.

## 12. Dividend Forecast Bridge

Use `business-fundamentals.md` Section 7.

Show:

- Distributable-Cash Bridge.
- Recurring FAD versus total distribution capacity, with separate exceptional uses and excess cash.
- Deduction ledger and capital/remittance constraints.
- Share Count and Scrip / DRIP Assumptions.
- Forecast Confidence.

Do not repeat Dividend Cash Cost or Derived DPS here.

## 13. Dividend and Yield Runway

Use the single table in `visual-output-rules.md` Section 6:

- Cash Available for Distribution.
- Payout Policy / Ratio and correct calculation base.
- Policy-implied amount versus justified forecast payout.
- Dividend Cash Cost.
- Derived DPS.
- Net Yield at Current Price.
- Funding gap and dividend-entitled share-count reconciliation.

Cover the same five-year/scenario keys as Sections 11 and 12. Split audit detail from the main table to retain at most seven columns, without repeating Derived DPS or Dividend Cash Cost.

## 14. Dividend Trap Checklist

Test every required item in `workflow.md`, including:

- forecast DPS versus business and cash flow;
- normalized N basis;
- issuance and scrip dilution;
- Structural Decline without credible finite-life harvest logic.
- Unsupported sector cash proxies, omitted investment and double deductions/add-backs.
- Growth depending on unfunded reinvestment or an unsupported terminal dividend.

The checklist is a precondition for valuation.

## 15. Income Entry, Growth Value, or Finite-Life Value

Read `buy-zone.md` and first state the valuation mode.

Print the sourced risk-free anchor, currency/tenor/date/tax basis, price-independent premium range and required total return. Explain how ordinary required cash yields are derived. State the explicit income target or Not Assessed; growth cannot substitute for a hard income minimum.

### Ordinary Yield-Based Mode

Include:

- N value, basis, source period, and normalization adjustments;
- B value and source;
- DPS source currency, normalization FX/fees, share/ADR entitlement and quote-unit conversion;
- r_low and r_high;
- deterministic Fair, Accumulation, and Strong Buy boundaries;
- historical price and yield context;
- current price position;
- veto status.

### Conditional Total-Return-Based Mode

Require evidence-backed, funded annual dividends and the growth/transition gates in `buy-zone.md`. Show:

- annual dividend-path references to Section 13, with valuation cash-flow dates/stub treatment;
- reinvestment/ROIC or equity-retention/ROE evidence and its transmission to per-share DPS;
- explicit horizon, steady-state transition, terminal DPS, bounded terminal growth and R-g spread;
- scenario present values, terminal-value share and R/g sensitivity;
- growth-value range, declared safety discount, entry limit and valuation-review threshold;
- conditional hard-income price ceiling, using the evidenced forward cash period separately from growth value;
- a separately labelled ordinary income entry comparison when credible, not a forced single answer.

If growth is unassessable, state why and use only a credible ordinary/finite-life mode or suspend. Do not manufacture positive growth to justify a price.

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
- FY+3/FY+5 cash development and monitoring milestones.

## 17. Score, Portfolio Role, and Holding Review

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

Apply `holding-review.md` separately from the score: thesis/cash/solvency triggers, valuation-review band, concentration/mandate constraints, action and next evidence date. A valuation band is not an automatic sell order. For a proposed switch, show the named alternative, same-basis forward cash income/returns, taxes/fees/costs and documented improvement hurdle. Missing holdings/alternative information means no invented trade size or switch conclusion.

## 18. Sources and Data Quality

List official filings, announcements, operating statistics, guidance, broker records, historical price sources, and cross-checks.

State missing data, stale data, scope/restatement adjustments, every material forecast's source/date and confidence, unsupported later years, sector/cash reconciliation, payout basis, sensitivity type, scrip assumptions, N basis, rate/growth assumptions and whether future FCF/DPS is evidence-backed or illustrative. Separate observed facts from estimates and research judgments.
