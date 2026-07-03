# Scoring Model

Use a 100-point framework. Do not invent new weights during execution.

## Weights

| Module | Weight |
|---|---:|
| Net dividend yield | 15 |
| Five-year dividend stability | 15 |
| Free cash-flow coverage | 20 |
| Balance-sheet safety | 15 |
| Management capital-allocation attitude | 15 |
| Buyback quality | 10 |
| Three-year visibility | 10 |

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

For fixed or ordinary dividend policies, use recurring free cash flow divided by ordinary cash dividends.

For variable, supplemental, formula-based, shipping, commodity, or other cycle-linked dividend policies, use recurring or normalized free cash flow divided by total cash dividends, including base plus variable or supplemental dividends. Do not score peak-cycle FCF coverage as if it were normalized coverage.

If company-reported FCF is unavailable, estimate FCF as operating cash flow minus capex and label it as estimated. EBITDA coverage is only a fallback cross-check and should not replace FCF coverage for the score unless FCF data is genuinely unavailable.

| FCF / relevant cash dividend | Points |
|---|---:|
| >= 1.5x on normalized basis | 17-20 |
| 1.0x to 1.5x on normalized basis | 12-16 |
| 0.7x to 1.0x or peak-cycle-only coverage | 6-11 |
| < 0.7x, debt-funded, equity-funded, or asset-sale-funded payout | 0-5 |

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
| Value-destructive allocation, equity issuance during elevated payout without clear need, or dividend not prioritized | 0-3 |

### 6. Buyback Quality, 10 points

| Condition | Points |
|---|---:|
| Real share-count reduction at reasonable valuation | 8-10 |
| Neutral or small buyback, limited dilution | 5-7 |
| Cosmetic buyback offset by dilution | 2-4 |
| Debt-funded, equity-offset, or value-destructive buyback | 0-1 |
| Not applicable | Assign neutral 5 unless buybacks are central to the thesis |

### 7. Three-Year Visibility, 10 points

| Condition | Points |
|---|---:|
| High visibility of earnings and dividends | 8-10 |
| Moderate visibility | 5-7 |
| High cycle or policy uncertainty | 2-4 |
| Very low visibility or likely cut | 0-1 |

## Score Bands

| Score | Grade | Default Portfolio Role |
|---:|---|---|
| 85-100 | A | Core income candidate |
| 70-84 | B | Income holding or buy on valuation weakness |
| 55-69 | C | Watchlist |
| 40-54 | D | High-risk income or special situation only |
| Below 40 | E | Avoid for dividend strategy |

Portfolio role may be adjusted by qualitative risk, but explain any override clearly.

## Required Ratings

Always output these six ratings:

- Dividend Quality: High / Medium / Low
- Dividend Safety: Strong / Acceptable / Weak / Unclear
- Withholding Efficiency: High / Medium / Low
- Buyback Quality: Good / Neutral / Poor / Not Applicable
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid
