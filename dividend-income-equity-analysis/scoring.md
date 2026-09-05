# Scoring Model

Use a 100-point framework for Full Analysis. Do not invent new weights during execution. Screen Mode does not use this score.

## Weights

| Module | Weight |
|---|---:|
| Net dividend yield | 15 |
| Five-year dividend stability | 15 |
| Free cash-flow coverage | 20 |
| Balance-sheet safety | 15 |
| Management capital-allocation attitude | 15 |
| Buyback quality | 10 |
| Three-to-five-year fundamental and dividend visibility | 10 |

## Anchor Rules

### 1. Net Dividend Yield, 15 points

Use recurring or normalized net yield. Exclude one-off special dividends unless clearly recurring.

| Recurring or normalized net yield | Points |
|---|---:|
| >= 7% | 13-15 |
| 5% to 7% | 10-12 |
| 3.5% to 5% | 6-9 |
| 2% to 3.5% | 3-5 |
| < 2% | 0-2 |

### 2. Five-Year Dividend Stability, 15 points

| Pattern | Points |
|---|---:|
| Stable or growing ordinary DPS, no cut | 12-15 |
| Mostly stable with mild cyclicality | 8-11 |
| Volatile but still paid most years | 4-7 |
| Cut, suspended, or highly unstable | 0-3 |

### 3. Free Cash-Flow Coverage, 20 points

Use the recurring FAD coverage contract in `business-fundamentals.md`: three-year cumulative recurring FAD divided by matching cash dividends paid, accompanied by the five-year worst recurring and actual cash-coverage years. This is not an arithmetic mean of annual ratios. Apply the same owner perimeter and the sector proxy in `sector-fcf-proxies.md`.

For fixed/progressive policies use ordinary cash dividends; for variable/cycle-linked policies use total recurring/variable cash dividends. Keep exceptional capital returns separate. Do not score peak-cycle cash, asset sales, excess capital releases or unsupported OPAT proxies as recurring coverage.

| Recurring FAD / relevant cash dividend | Points |
|---|---:|
| >= 1.5x on normalized basis | 17-20 |
| 1.0x to 1.5x on normalized basis | 12-16 |
| 0.7x to 1.0x or peak-cycle-only coverage | 6-11 |
| < 0.7x, debt-funded, equity-funded, or asset-sale-funded payout | 0-5 |

Anchor points to the aggregate, then explain the worst-year and funding stress. Do not grant the top band when recurring shortfalls are unresolved, capital/remittance restrictions are unknown, or a material cash bridge is estimated without reconciliation. Missing coverage earns no unsupported safety points: report `score_100 = null`, `grade = null`, and an incomplete-score reason if this prevents a responsible module score; do not silently treat missing data as either zero risk or proven distress.

### 4. Balance-Sheet Safety, 15 points

| Condition | Points |
|---|---:|
| Low leverage, strong liquidity, no near-term maturity pressure | 12-15 |
| Manageable leverage and refinancing risk | 8-11 |
| Elevated leverage or weak interest cover | 4-7 |
| Distressed balance sheet or major refinancing wall | 0-3 |

### 5. Management Capital Allocation, 15 points

| Condition | Points |
|---|---:|
| Clear policy, disciplined payout, balanced reinvestment and returns | 12-15 |
| Reasonable but partly discretionary policy | 8-11 |
| Unclear policy or inconsistent communication | 4-7 |
| Value-destructive allocation, elevated payout with unexplained issuance, or dividend not prioritized | 0-3 |

Persistent unoffset scrip / DRIP dilution prevents the highest capital-allocation score.

### 6. Buyback Quality, 10 points

| Condition | Points |
|---|---:|
| Real share-count reduction at reasonable valuation | 8-10 |
| Neutral or small buyback, limited dilution | 5-7 |
| Cosmetic buyback offset by issuance or scrip / DRIP dilution | 2-4 |
| Debt-funded, equity-offset, or value-destructive buyback | 0-1 |
| Not applicable | Neutral 5 unless buybacks are central to the thesis |

### 7. Three-to-Five-Year Fundamental and Dividend Visibility, 10 points

| Condition | Points |
|---|---:|
| High visibility: operating drivers, three-year FCF/DPS and the year-four/five development path are evidenced, funded and reconcilable | 8-10 |
| Moderate visibility: capacity is estimable but macro, pricing, credit, execution, capex, or dilution risk remains | 5-7 |
| Low visibility: wide scenarios, high cyclicality, uncertain policy, or weak reconciliation | 2-4 |
| Not forecastable, unsupported DPS assumptions, or likely dividend cut | 0-1 |

Do not award more than 4 points when future DPS is illustrative rather than evidence-backed.

Do not upgrade visibility merely because the model contains five numerical years. Uncertain later years must carry explicit limitations and monitoring milestones. Retain the separate Three-Year Dividend Outlook rating; the five-year view is in `business_outlook`.

## Score and Valuation Separation

Weights remain 100 points. Do not map the overall score or Grade to risk-premium or discount-rate bands: net yield contains current price, which would make valuation circular. The price-independent risk assessment in `buy-zone.md` uses business, capital, policy and evidence quality directly. A lower income score can coexist with a credible growth value; it does not waive an explicit investor cash-income minimum.

## Structural Decline Overlay

If Fundamental Trend is `Structural Decline`, apply these limits after calculating the unadjusted numeric score:

- Final Grade cannot exceed C.
- Portfolio Role cannot be more favorable than Opportunistic.
- Three-to-Five-Year Fundamental and Dividend Visibility cannot exceed 4 / 10.
- The security cannot be classified as Core income.
- Ordinary and growth valuation are suspended; a satisfied Harvest / Managed Runoff Exception permits only the finite-life primary mode and its explicitly labelled ordinary cross-check.

### Harvest / Managed Runoff Exception

The exception is satisfied only when all are demonstrated:

- Management is explicitly shrinking, harvesting, or running off the business while returning capital.
- The balance sheet is net cash or conservatively financed.
- The decline in distributable cash is measurable and reasonably predictable.
- Distributions do not depend on refinancing, uncertain asset-sale timing, or new equity issuance.
- The entry price is assessed through finite-life cash recovery rather than a perpetual franchise assumption.

The exception permits the finite-life valuation mode in `buy-zone.md`; it does not convert the company into a Core income asset and does not remove the Grade C cap.

Required output:

- Unadjusted numeric score.
- Overlay-adjusted Grade.
- Final Portfolio Role.
- Structural Decline cap applied: Yes / No.
- Harvest / Managed Runoff Exception applied: Yes / No.
- Valuation mode: suspended / finite_life_harvest.
- Expected cash-harvest horizon when applicable.

## Score Bands

| Score | Grade | Default Portfolio Role |
|---:|---|---|
| 85-100 | A | Core income candidate |
| 70-84 | B | Income holding or buy on valuation weakness |
| 55-69 | C | Watchlist |
| 40-54 | D | High-risk income or special situation only |
| Below 40 | E | Avoid for dividend strategy |

Qualitative overlays may make the final Grade or Portfolio Role less favorable than the numeric band. Explain every override.

## Required Ratings

Always output:

- Dividend Quality: High / Medium / Low
- Dividend Safety: Strong / Acceptable / Weak / Unclear
- Withholding Efficiency: High / Medium / Low
- Buyback Quality: Good / Neutral / Poor / Not Applicable
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid
- Fundamental Trend: Structural Growth / Stable / Mature / Cyclical Recovery / Cyclical Peak / Structural Decline / Transformation / High Uncertainty
- Forecast Confidence: High / Medium / Low / Not Forecastable
- Structural Decline cap applied: Yes / No
- Harvest / Managed Runoff Exception applied: Yes / No
- Valuation mode: ordinary_yield_based / total_return_based / finite_life_harvest / suspended
- Holding review action and missing portfolio inputs, following `holding-review.md`
