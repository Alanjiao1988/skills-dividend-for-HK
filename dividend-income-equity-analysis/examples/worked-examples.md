# Complete Fictional Analysis Examples

`ordinary.analysis.json` and `growth.analysis.json` are complete schema-2.2 records for Fictional Harbor Services, using the assumptions below as of 2026-01-01. All company data, taxes, rates and prices are teaching inputs, not fetched market facts. Validate both structure and arithmetic with `scripts/validate_analysis.py`. Display labels follow `buy-zone.md`; legacy JSON field names are compatibility keys.

## Assumptions A1-A8

| Reference | Fictional assumption |
|---|---|
| A1 | USD reporting and valuation; money in millions and shares in millions; 10 million dividend-entitled shares, one share per quoted security, no scrip. |
| A2 | Base year-1 revenue 500, profit 100, OCF after interest/tax 130, maintenance 20, other owner claims 10, remaining growth uses 20, mandatory uses 5, exceptional uses 5. No excess-cash release. Bear/Base/Bull operating levels are 80%/100%/120%; these are constructed cases, not empirical probabilities. |
| A3 | Dividend entitlement is 40% of attributable profit; all is paid in cash. Company cash, payout and entitled shares reconcile separately. |
| A4 | This hypothetical investor receives cash with zero tax, fees and FX deductions by explicit assumption. Real research must establish those inputs; USD does not imply tax-free dividends. |
| A5 | Required returns: assumed risk-free 4% plus independently stipulated premium 4%-6%, giving 8%-10%; no growth credit in the income comparison. These rates are not sector defaults. |
| A6 | Quote 40; no investor income target. Medium confidence and Acceptable safety limit actions; no Strong Buy or invented trade size. |
| A7 | Ordinary capacity is flat. Growth case assumes funded operating cash and dividends grow 2% yearly, with unchanged payout/shares and a funded steady state. Valuation uses the same R=9% in every operating scenario and year-end full cash entitlements. |
| A8 | Historical recurring FAD is 50/60/70/80/90; dividends are 40 each year. Actual cash capacity is 45/55/65/75/35. The final year's exceptional shortfall is disclosed, not hidden in recurring coverage. A 15% growth entry discount is a stated teaching convention, not a calibrated safeguard. |

## Cash and Ordinary Income Answers

Base Owner FCF = 130 - 20 - 10 = **100**. Recurring FAD = 100 - 20 - 5 = **75**. Actual capacity = 75 - 5 = **70**. Dividend entitlement and cash cost = 100 profit × 40% = **40**, not 75 FAD × 40%. DPS = 40 / 10 = **4**. Bear DPS is **3.2**.

The latest three-year recurring coverage is (70 + 80 + 90) / (40 + 40 + 40) = **2.0x**. Five-year worst recurring coverage is **1.25x**; worst actual capacity coverage is **0.875x**. These measures answer different questions.

With N=4, B=3.2 and required cash yields 8%-10%, boundaries are **50**, **40** and **32**. The assumed price 40 sits exactly at the normalized high-end requirement. Neither that position nor the legacy `strong_buy_zone` key creates an action; `action_assessment.strong_buy_eligible` is false. These are no-growth-credit income comparisons, not full intrinsic-value judgments.

## Growth Answers and Terminal Dependence

The growth examples have a full funded cash/share ledger, five explicit year-end cash payments, and the first terminal dividend in year 6. At R=9%, g=2%, their cash paths are internally constructed steady-growth cases, so the explicit forecast plus terminal value can independently be cross-checked against D1 / (R-g):

| Scenario | Year-1 net DPS | Total value |
|---|---:|---:|
| Bear | 3.2 | 45.7142857143 |
| Base | 4.0 | 57.1428571429 |
| Bull | 4.8 | 68.5714285714 |

Base explicit five-year cash PV is **16.1384704566** and terminal PV is **41.0043866862**. Terminal value contributes about **71.76%** in each scenario. This dependence remains material despite being below the 75% warning threshold. The safety-discounted entry ceiling is 45.7142857143 × 85% = **38.8571428571**, below the assumed price 40. R/g sensitivities keep the Base operating path fixed and do not replace operating scenarios.

Scenario percentages and the 2% steady-growth assumption are fictional. Real growth needs operating/funding/terminal evidence; it cannot be inferred simply because these fixtures pass. The examples do not assert that any named issuer qualifies or that the framework is calibrated to investment outcomes.
