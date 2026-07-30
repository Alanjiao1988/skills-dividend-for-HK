# Output Template

This file is the output section order. Detailed table structures live in `visual-output-rules.md`, `business-fundamentals.md`, and `buy-zone.md`; do not duplicate or redefine them here.

## 1. Executive Summary

### 1A. Key Metrics at a Glance

If rich visualization or card-style layout is available, render these as four metric cards. If not, use this one-row table.

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| | | | |

If normalized yield is a range, display it directly as `x-y%`.

### 1B. Secondary Summary

- Company:
- Ticker:
- Exchange:
- As-of date:
- Price used:
- TTM gross yield:
- TTM net yield:
- Normalized net yield:
- Expected buy zone:
- Fundamental trend:
- Forecast confidence: High / Medium / Low / Not Forecastable
- Value-trap veto: Not triggered / Triggered / Unclear
- Withholding rate:
- Withholding basis:
- Broker-observed withholding: Yes / No / Unknown
- Broker cash-line type if broker statement is used: dividend / PIL / mixed / unknown
- Initial view:

## 2. Dividend Snapshot

One-sentence takeaway before the table. Use the Dividend Snapshot table defined in `visual-output-rules.md`.

## 3. Standard Charts or Text Fallback

Follow `visual-output-rules.md`.

If rich visualization is available, render the standard charts:

1. DPS Structure Chart.
2. Yield Ladder.
3. Coverage Chart.
4. Fundamental Forecast Chart.
5. Buy-Zone Ladder.

If rich visualization is unavailable, provide the plain-text fallback:

- Business and FCF trend:
- DPS path:
- Yield stack:
- Buy-zone ladder:
- Coverage labels:

Charts are the communication layer. Tables below are the data record.

## 4. Company and Listing Structure

One-sentence takeaway before details.

Describe domicile, issuer type, listing venue, dividend currency, reporting currency, official share count from filings, and whether the security is an H-share, red-chip, ADR, REIT, fund, trust, or ordinary share.

## 5. Dividend Treatment

One-sentence takeaway before details.

Read `withholding-notes.md` and apply the priority rule. Explain the basis for the withholding assumption and any uncertainty.

If withholding is 0%, state once: "Withholding 0% — gross equals net." Do not repeat Withholding / Net DPS / Net Yield columns in every historical row.

If broker records are used, identify whether the cash line is a normal dividend, payment in lieu, mixed, or unknown. PIL-only records must not be used as withholding-rate evidence.

## 6. Business Fundamentals and Long-Term Trend

One-sentence takeaway before the tables.

Read `business-fundamentals.md` and include:

- Main business segments and the economic engine that funds dividends.
- Historical operating trend using sector-appropriate KPIs.
- Three-to-five-year trend classification: Structural Growth / Stable / Mature / Cyclical Recovery / Cyclical Peak / Structural Decline / Transformation / High Uncertainty.
- Three to five core operating drivers.
- Key structural, cyclical, competitive, regulatory, capital-intensity, and balance-sheet factors.

Use the Historical Operating Trend table from `business-fundamentals.md`.

## 7. Dividend Trajectory and Yearly Yield

One-sentence takeaway before the tables.

Use `visual-output-rules.md` Section 4 for the authoritative table structures. Apply table slimming rules before rendering.

Add a short Dividend Pattern paragraph after the tables.

## 8. Historical Cash-Flow Coverage Bridge

One-sentence takeaway before the tables.

Use `visual-output-rules.md` Section 5 for the authoritative bridge structures. If FCF is estimated as operating cash flow minus capex, label it as estimated.

Explain whether historical dividends were funded by operating free cash flow, cash balance, asset sales, debt, equity issuance, or mixed sources.

## 9. Management Capital Allocation

One-sentence takeaway before details.

Summarize dividend policy, buyback policy, leverage target, reinvestment priority, acquisition policy, share issuance, ATM programs, and whether equity issuance coincides with elevated payout.

## 10. Buyback Quality

One-sentence takeaway before details.

Assess share-count change, dilution, valuation discipline, whether buybacks are debt-funded, and whether buybacks are offset by share issuance.

## 11. Three-Year Fundamental Forecast

One-sentence takeaway before the tables.

Use `business-fundamentals.md` Section 6 for the authoritative operating-driver and financial-forecast structures.

For each of the next three fiscal years, show Bear, Base, and Bull scenarios for:

- Core operating drivers.
- Revenue or sector-equivalent income.
- Net income / AFFO / capital generation.
- Operating cash flow.
- Capex or required capital.
- FCF or distributable cash.

State which inputs are reported facts, company guidance, consensus cross-checks, or analyst estimates.

## 12. Dividend Forecast Bridge

One-sentence takeaway before the tables.

Use `business-fundamentals.md` Section 7 for the authoritative Distributable-Cash Bridge and DPS Derivation tables.

Show explicitly how operating performance becomes:

```text
Cash Available for Distribution
-> Dividend Cash Cost
-> Diluted Share Count
-> Derived DPS
```

State the payout policy or ratio, mandatory debt or regulatory uses, required reinvestment, and any justified use of excess cash.

Rate forecast confidence as High, Medium, Low, or Not Forecastable.

## 13. Three-Year Dividend Runway

One-sentence takeaway before the table.

Use `visual-output-rules.md` Section 10 for the authoritative runway table structure. If more detail is needed, add a separate assumptions table for Balance Sheet Impact and Key Assumptions.

The DPS in this section must be derived from Section 11 and Section 12. Separate TTM yield from normalized and scenario yield.

If the forecast is not evidence-backed, state this prominently and do not present the scenario DPS as a reliable estimate.

## 14. Dividend Trap Checklist

One-sentence takeaway before the table.

List each red flag and the evidence for or against it. Include equity issuance or ATM program concurrent with elevated payout when relevant.

Also test whether forecast DPS is inconsistent with the projected business, FCF, payout policy, or diluted share count.

The checklist is a precondition for Expected Buy Zone. If a major value-trap veto is triggered, buy-zone ranges must be suspended or explicitly labelled as special-situation only.

## 15. Expected Buy Zone

One-sentence takeaway before the tables.

Read `buy-zone.md` and estimate an expected buy zone using normalized net DPS, required net yield, historical yield bands, historical price context, and downside safety checks.

At minimum include:

- Source of N: Base fundamental forecast and Dividend Forecast Bridge.
- Source of B: Bear fundamental forecast and Dividend Forecast Bridge.
- Required net yield assumptions with `r_low` and `r_high`.
- Formula: Buy Price = Net DPS / Required Net Yield.
- Deterministic boundaries from `buy-zone.md`: too expensive, fair / hold, accumulation zone, strong buy zone.
- Value-trap veto status: Not triggered / Triggered / Unclear.
- Historical price and yield context.
- Whether the current price is above, inside, or below the income entry zone.

If N or B cannot be derived from operating fundamentals, label the buy zone lower-confidence or state: "Buy zone cannot be responsibly estimated."

## 16. Visual Summary

Add a compact visual summary:

- Business and FCF trend:
- DPS path:
- Yield normalization: TTM vs normalized vs bear/base/bull.
- Buy-zone ladder: current price vs fair / accumulation / strong-buy zones and veto status.
- Coverage labels by year: Strong / Adequate / Weak.

If charts were already rendered, keep this section brief and use it as a written recap.

## 17. Score, Required Ratings, and Portfolio Role

One-sentence takeaway before the score table.

Use `scoring.md` and show points by module.

Always output the six required ratings:

- Dividend Quality: High / Medium / Low
- Dividend Safety: Strong / Acceptable / Weak / Unclear
- Withholding Efficiency: High / Medium / Low
- Buyback Quality: Good / Neutral / Poor / Not Applicable
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid

Also output:

- Fundamental Trend: Structural Growth / Stable / Mature / Cyclical Recovery / Cyclical Peak / Structural Decline / Transformation / High Uncertainty
- Forecast Confidence: High / Medium / Low / Not Forecastable

## 18. Sources and Data Quality

List official filings, announcements, operating statistics, guidance, broker records, historical price sources, and third-party cross-checks used.

State missing data, stale data, fallback calculations, forecast assumptions, scenario sensitivities, and whether future DPS is evidence-backed or illustrative.
