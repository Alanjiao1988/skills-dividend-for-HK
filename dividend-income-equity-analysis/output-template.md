# Output Template

This file is the output section order. Detailed table structures live in `visual-output-rules.md`; buy-zone structures live in `buy-zone.md`; do not duplicate or redefine them here.

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
4. Buy-Zone Ladder.

If rich visualization is unavailable, provide the plain-text fallback:

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

## 6. Dividend Trajectory and Yearly Yield

One-sentence takeaway before the tables.

Use `visual-output-rules.md` Section 4 for the authoritative table structures. Apply table slimming rules before rendering.

Add a short Dividend Pattern paragraph after the tables.

## 7. Cash-Flow Coverage Bridge

One-sentence takeaway before the tables.

Use `visual-output-rules.md` Section 5 for the authoritative bridge structures. If FCF is estimated as operating cash flow minus capex, label it as estimated.

Explain whether dividends were funded by operating free cash flow, cash balance, asset sales, debt, equity issuance, or mixed sources.

## 8. Management Capital Allocation

One-sentence takeaway before details.

Summarize dividend policy, buyback policy, leverage target, reinvestment priority, acquisition policy, share issuance, ATM programs, and whether equity issuance coincides with elevated payout.

## 9. Buyback Quality

One-sentence takeaway before details.

Assess share-count change, dilution, valuation discipline, whether buybacks are debt-funded, and whether buybacks are offset by share issuance.

## 10. Three-Year Dividend Runway

One-sentence takeaway before the table.

Use `visual-output-rules.md` Section 9 for the authoritative runway table structure. If more detail is needed, add a separate assumptions table for Balance Sheet Impact and Key Assumptions.

Separate TTM yield from normalized and scenario yield.

## 11. Dividend Trap Checklist

One-sentence takeaway before the table.

List each red flag and the evidence for or against it. Include equity issuance or ATM program concurrent with elevated payout when relevant.

The checklist is a precondition for Expected Buy Zone. If a major value-trap veto is triggered, buy-zone ranges must be suspended or explicitly labelled as special-situation only.

## 12. Expected Buy Zone

One-sentence takeaway before the tables.

Read `buy-zone.md` and estimate an expected buy zone using normalized net DPS, required net yield, historical yield bands, historical price context, and downside safety checks.

At minimum include:

- DPS basis used: TTM / normalized / bear / base / bull.
- Required net yield assumptions with `r_low` and `r_high`.
- Formula: Buy Price = Net DPS / Required Net Yield.
- Deterministic boundaries from `buy-zone.md`: too expensive, fair / hold, accumulation zone, strong buy zone.
- Value-trap veto status: Not triggered / Triggered / Unclear.
- Historical price and yield context.
- Whether the current price is above, inside, or below the income entry zone.

If data is insufficient, state: "Buy zone cannot be responsibly estimated" and list missing inputs.

## 13. Visual Summary

Add a compact visual summary:

- DPS path:
- Yield normalization: TTM vs normalized vs bear/base/bull.
- Buy-zone ladder: current price vs fair / accumulation / strong-buy zones and veto status.
- Coverage labels by year: Strong / Adequate / Weak.

If charts were already rendered, keep this section brief and use it as a written recap.

## 14. Score, Required Ratings, and Portfolio Role

One-sentence takeaway before the score table.

Use `scoring.md` and show points by module.

Always output the six required ratings:

- Dividend Quality: High / Medium / Low
- Dividend Safety: Strong / Acceptable / Weak / Unclear
- Withholding Efficiency: High / Medium / Low
- Buyback Quality: Good / Neutral / Poor / Not Applicable
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid

## 15. Sources and Data Quality

List official filings, announcements, broker records, and third-party cross-checks used. State any missing data or fallback calculations clearly.
