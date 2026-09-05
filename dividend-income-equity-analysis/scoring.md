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

Use credible normalized net yield in the investor's stated tax and currency context. Exclude one-off special dividends and economic capital recovery from recurring income. These bands measure income appeal within the 100-point framework, not business quality or expected total return; a falling share price must not mechanically improve the investment conclusion.

| Recurring or normalized net yield | Points |
|---|---:|
| >= 7% | 13-15 |
| >= 5% and < 7% | 10-12 |
| >= 3.5% and < 5% | 6-9 |
| >= 2% and < 3.5% | 3-5 |
| < 2% | 0-2 |

Apply these safeguards before summing the score:

- Award 13-15 only with evidence-backed normalization, at least Medium Forecast Confidence, at least Acceptable Dividend Safety, and value-trap veto Not triggered. Explain the yield spread versus the dated opportunity-cost comparison in `buy-zone.md`.
- Cap this module at 9 / 15 when Forecast Confidence is Low or normalization uses a historical fallback; cap it at 5 / 15 when Dividend Safety is Weak or the veto is Triggered. State the raw band and the applied cap.
- If normalized dividend capacity, tax / currency basis or essential safety evidence is unavailable, mark this module Not Assessable. Do not substitute a high TTM yield. Follow the incomplete-evidence rule below rather than assigning an invented neutral score.
- Fixed bands are a consistent scoring convention. Their interpretation must reflect current rates and company risk; do not change weights, silently alter thresholds or award additional points above 15 for an extreme yield.

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
| >= 1.0x and < 1.5x on normalized basis | 12-16 |
| >= 0.7x and < 1.0x or peak-cycle-only coverage | 6-11 |
| < 0.7x, debt-funded, equity-funded, or asset-sale-funded payout | 0-5 |

When scrip retains issuer cash, also show coverage of the full cash-equivalent entitlement; do not grant a better safety band solely from fewer holders electing cash. Anchor points to the aggregate, then explain the worst-year and funding stress. Do not grant the top band when recurring shortfalls are unresolved, capital/remittance restrictions are unknown, or a material cash bridge is estimated without reconciliation. Missing coverage earns no unsupported safety points: report `score_100 = null`, `grade = null`, and an incomplete-score reason if this prevents a responsible module score; do not silently treat missing data as either zero risk or proven distress.

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
| Value-destructive allocation, elevated payout with unexplained issuance, or payout policy persistently inconsistent with stated income commitments | 0-3 |

Do not penalize necessary reinvestment, prudent debt reduction or a justified dividend reset solely because management does not maximize today's dividend. Assess their effect on sustainable per-share value and future income; separately state whether the security fits the investor's current income mandate. Persistent scrip dilution that hides a cash shortfall or destroys per-share value prevents the highest score; quantify the economics rather than treating every reinvestment election as new issuance.

### 6. Buyback Quality, 10 points

| Condition | Points |
|---|---:|
| Real share-count reduction at reasonable valuation, or evidenced discipline in avoiding uneconomic buybacks with stable per-share ownership | 8-10 |
| Neutral or small buyback / no-buyback policy with limited dilution and no demonstrated value destruction | 5-7 |
| Cosmetic buyback offset by issuance or scrip / DRIP dilution | 2-4 |
| Buyback that creates financing stress or demonstrably destroys continuing shareholders' per-share value | 0-1 |
| No buyback program | Score the documented per-share outcome and rationale using the same bands; absence alone is not a fixed deduction |

Keep the module at 10 points and retain `Buyback Quality: Not Applicable` when no buyback program exists. The score in that case measures demonstrated per-share capital discipline: 8-10 requires evidence such as a stable share count, avoidance of repurchases above conservative value, and a credible funding / capital-allocation rationale; do not award a maximum merely because there is no program. If the relevant evidence is unavailable, mark Not Assessable. Do not redistribute the weight.

Reconcile repurchases with issuance, treasury-share reissuance, compensation and scrip over comparable periods. Distinguish issuer-created dilution from an investor's open-market DRIP. Consider debt financing together with leverage, liquidity and purchase valuation; debt financing alone does not establish value destruction. Avoid double counting: Module 5 assesses allocation and funding decisions, while this module assesses repurchase valuation and continuing owners' per-share outcome.

### 7. Three-to-Five-Year Fundamental and Dividend Visibility, 10 points

| Condition | Points |
|---|---:|
| High visibility: operating drivers, three-year FCF/DPS and the year-four/five development path are evidenced, funded and reconcilable | 8-10 |
| Moderate visibility: capacity is estimable but macro, pricing, credit, execution, capex, or dilution risk remains | 5-7 |
| Low visibility: wide scenarios, high cyclicality, uncertain policy, or weak reconciliation | 2-4 |
| Not forecastable, unsupported DPS assumptions, or likely dividend cut | 0-1 |

Do not award more than 4 points when future DPS is illustrative rather than evidence-backed.

Do not upgrade visibility merely because the model contains five numerical years. Uncertain later years must carry explicit limitations and monitoring milestones. Retain the separate Three-Year Dividend Outlook rating; the five-year view is in `business_outlook`.

## Evidence and Action Overlays

- If a required scoring module is Not Assessable, show the supported module scores and missing evidence, but set the total score and Grade to Not Assessable (`null` in JSON). Do not fill missing data with neutral points or scale a partial score to 100. Portfolio Role is at most Watchlist until the material gaps are resolved.
- A Triggered value-trap veto overrides any numeric score: actionable buy zones are suspended and the security cannot be Core income. An Unclear veto also suspends actionable buy zones and caps the Portfolio Role at Watchlist; missing evidence does not mean the veto passed.
- Low Forecast Confidence, a fallback N / B, provisional yield calibration or an unassessed capital-risk / total-return cross-check prevents an actionable Strong Buy and a Core income classification. Use diagnostic income sensitivities with Watchlist as the action. Not Forecastable suspends ordinary buy zones.
- A Strong Buy action requires High Forecast Confidence, Strong Dividend Safety, value-trap veto Not triggered and every action gate in `buy-zone.md`. Medium confidence permits at most gradual accumulation after the other gates pass. A price inside the arithmetic Strong Buy threshold is not sufficient.
- Dividend Safety Weak or Unclear prevents Core income. Income yield does not compensate for an unquantified risk of permanent loss of capital.

These overlays do not create new module weights. Report a computed score separately from confidence, safety, valuation eligibility and the final Portfolio Role; a high score cannot cancel a failed gate.

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
- Withholding Efficiency: High / Medium / Low / Unclear
- Buyback Quality: Good / Neutral / Poor / Not Applicable
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid
- Fundamental Trend: Structural Growth / Stable / Mature / Cyclical Recovery / Cyclical Peak / Structural Decline / Transformation / High Uncertainty
- Forecast Confidence: High / Medium / Low / Not Forecastable
- Structural Decline cap applied: Yes / No
- Harvest / Managed Runoff Exception applied: Yes / No
- Valuation mode: ordinary_yield_based / total_return_based / finite_life_harvest / suspended
- Holding review action and missing portfolio inputs, following `holding-review.md`
