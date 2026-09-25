# Complete Fictional Analysis Examples

`ordinary.analysis.json` and `growth.analysis.json` are complete schema-3.0 records for Fictional Harbor Services, using the assumptions below as of 2026-01-01. Their normalization evidence/state construction, scorecard, rating and entry evidence reference these stipulated assumptions, not verified issuer disclosures. `safety-review.analysis.json` is a separate lightweight variant, not an update to either full forecast. All company data, taxes, rates and prices are teaching inputs, not fetched market facts. Validate both structure and arithmetic with `scripts/validate_analysis.py` from the installed skill root. Display labels follow `buy-zone.md`; legacy JSON boundary names remain compatibility keys.

This is an English maintenance/audit example, not a reader-facing report. Actual reports retain the local simplified-Chinese, single self-contained HTML contract in `output-template.md` and `report-language.md`. Repository-only GPT-bundle build instructions, if consulted, are source-development aids, not required tools for using or validating the installed skill.

## Assumptions A1-A8

| Reference | Fictional assumption |
|---|---|
| A1 | USD reporting and valuation; money in millions and shares in millions; 10 million dividend-entitled shares, one share per quoted security, no scrip. |
| A2 | Base year-1 revenue 500, profit 100, OCF after interest/tax 130, maintenance 20, other owner claims 10, remaining growth uses 20, mandatory uses 5, exceptional uses 5. No excess-cash release. Bear/Base/Bull operating levels are 80%/100%/120%; these are constructed cases, not empirical probabilities. |
| A3 | Dividend entitlement is 40% of attributable profit; all is paid in cash. Company cash, payout and entitled shares reconcile separately. |
| A4 | This hypothetical investor receives cash with zero tax, fees and FX deductions by explicit assumption. Real research must establish those inputs; USD does not imply tax-free dividends. |
| A5 | Required returns: assumed risk-free 4% plus independently stipulated premium 4%-6%, giving 8%-10%; no growth credit in the income comparison. These rates are not sector defaults. |
| A6 | Quote 40; no investor income target. Cash 25m, debt 50m, EBITDA 100m, unrestricted capital access and no refinancing need within five years are stipulated. Medium confidence and Acceptable safety permit conditional gradual accumulation, not Strong Buy. The local security-level role remains Watchlist under the documented Medium-visibility/Acceptable-safety rationale; this is separate from entry eligibility, not a mechanical score cutoff or a personal allocation. A cheaper quote alone changes neither quality nor role. |
| A7 | Ordinary capacity is flat. Growth case assumes funded operating cash and dividends grow 2% yearly, with unchanged payout/shares and a funded steady state. Valuation uses the same R=9% in every operating scenario and year-end full cash entitlements. |
| A8 | Historical recurring FAD is 50/60/70/80/90; ordinary dividends of 40 were paid on schedule each year, with ten million shares and no buyback/issuance program. Actual capacity is 45/55/65/75/35; the final 5m shortfall uses the stipulated cash buffer. A 15% growth safety discount is a teaching convention, not calibrated to price. Three-year return scenarios assume a 10% Bear exit yield and 8% Base/Bull exit yield, using year-3 funded DPS, zero costs and no reinvestment; these are assumptions, not guaranteed rerating. |

The JSON `withholding_basis: company_announcement` represents a fictional announcement scenario stipulated by A4, not a real issuer notice or broker-observed payment. Likewise the supported normalization links document internal consistency of A1-A8; they do not certify external facts.

## Analytical-Quality Assumptions Q1-Q4

| Reference | Fictional assumption and independent check |
|---|---|
| Q1 | The reference business is noncyclical: stipulated service-volume index 100 at each 2021-2025 annual observation, with the same reference asset/cost/share scope. The joint central state uses A2-A4: Owner FCF 100, growth 20, mandatory uses 5, FAD 75, earnings-based entitlement 40, 10 entitled shares, gross/net N=4. Low/high cycle states are not applicable, not made-up trough/peak dividends. N estimation bounds are unavailable, not borrowed from future Bear/Bull. A7's separate future growth does not add growth credit to this normalized income comparison. |
| Q2 | Stipulate a widely held company without a controlling parent's cash demand, and USD revenues/costs/debt, payout and investor reporting. These are scenario assumptions, not findings about an actual issuer. Under rubric 2, the six non-yield quality components are 13+18+10+10+5+6 = 62/85; the separate 14/15 income component gives 76/100. `quality_assessment` maps to the same scorecard quality result, not an independent discretionary score. Both summaries remain provisional because of estimated evidence. Price changes must not change 62/85 or mechanically improve Portfolio Role. |
| Q3 | Investor consumption basket/CPI data is not supplied, so Real Income Trend remains Not Assessed. A nominally stable dividend is not proof of preserved purchasing power. The primary tagged income driver is contracted service volume through revenue and fixed-cost cash conversion; no portfolio weights or correlations are invented. |
| Q4 | Independent safety-review variant: compare a sourced 2025-06-30 baseline to a 2025-12-31 disclosure as of 2026-01-01, on the same annual parent cash-capacity basis. FAD falls 75 to 60, cash dividends and full cash entitlement remain 40 (no scrip), actual capacity falls 70 to 55, liquidity 25 to 20, and signed capital surplus above the applicable minimum falls 1.5 to 1.2 headroom units. New recurring coverage is 60/40=1.5x on both dividend bases, actual coverage 55/40=1.375x, both gaps=0. Safety weakens but remains Acceptable under the stipulated nonstructural/no-veto evidence. No N/B, new entry price, score or position size is generated by this light task. |

## Cash and Ordinary Income Answers

Base Owner FCF = 130 - 20 - 10 = **100**. Recurring FAD = 100 - 20 - 5 = **75**. Actual capacity = 75 - 5 = **70**. Dividend entitlement and cash cost = 100 profit × 40% = **40**, not 75 FAD × 40%. DPS = 40 / 10 = **4**. Bear DPS is **3.2**.

The latest three-year recurring coverage is (70 + 80 + 90) / (40 + 40 + 40) = **2.0x**. Five-year worst recurring coverage is **1.25x**; worst actual capacity coverage is **0.875x**. These measures answer different questions.

With N=4, B=3.2 and required cash yields 8%-10%, boundaries are **50**, **40** and **32**. The assumed price 40 sits exactly at the normalized high-end requirement. Neither that position nor the legacy `strong_buy_zone` key creates an action; `action_assessment.strong_buy_eligible` is false. These are no-growth-credit income comparisons, not full intrinsic-value judgments.

The independent entry plan is **accumulate**: ordinary starter/add/strict reference prices are 50/40/32, with signed distances +25%/0%/-20% from price 40. Positive distance is headroom below a conditional ceiling, not forecast upside. The strict stage also lacks High confidence and Strong safety; Medium does not block the otherwise supported first stages.

## Growth Answers and Terminal Dependence

The growth examples have a full funded cash/share ledger, five explicit year-end cash payments, and the first terminal dividend in year 6. At R=9%, g=2%, their cash paths are internally constructed steady-growth cases, so the explicit forecast plus terminal value can independently be cross-checked against D1 / (R-g):

| Scenario | Year-1 net DPS | Total value |
|---|---:|---:|
| Bear | 3.2 | 45.7142857143 |
| Base | 4.0 | 57.1428571429 |
| Bull | 4.8 | 68.5714285714 |

Base explicit five-year cash PV is **16.1384704566** and terminal PV is **41.0043866862**. Terminal value contributes about **71.76%** in each scenario. This dependence remains material despite being below the 75% warning threshold. The safety-discounted entry ceiling is 45.7142857143 × 85% = **38.8571428571**, below the assumed price 40. R/g sensitivities keep the Base operating path fixed and do not replace operating scenarios.

That is the **strict** threshold. The Base-supported starter is 57.1428571429 × 85% = **48.5714285714**; add is min(starter, low scenario value) = **45.7142857143**. At 40, the supported Medium-confidence action is **accumulate**, not "wait until 38.8571 or do nothing". Strong Buy remains unavailable.

## Reproducible Score and Rating Answers

Both cases use the same seven band selections and refinement results; growth changes valuation, not automatically quality.

| Module | Band / Range | Met Checks | Raw / Final |
|---|---|---:|---:|
| Net yield | 1 / 13-15 | 2 | 14 |
| Dividend stability | 1 / 12-15 | 1 | 13 |
| Cash coverage | 1 / 17-20 | 1 | 18 |
| Balance sheet | 2 / 8-11 | 2 | 10 |
| Capital allocation | 2 / 8-11 | 2 | 10 |
| Buyback discipline | 2 / 5-7 | 1 | 5 |
| Visibility | 2 / 5-7 | 2 | 6 |

For example, buyback discipline is `5 + floor(2 x 1/3) = 5`; no program is labelled **Not Applicable**, not penalized by an invented fixed deduction. Stability has an established no-cut band, but no inflation or adverse-cycle corroboration for extra points. Cash availability and capital access are stipulated; separate covenant/stress-liquidity disclosure is not supplied for refinement. Acquisition/issuance decisions, valuation-based buyback abstention and past milestone delivery are also uncorroborated refinements, not new entry vetoes.

Quality = **62/85** and income = **14/15**; combined = **76/100**, unadjusted/final Grade **B**, no Grade cap. Dividend Quality is **Medium** because 62 is within 51-67. A lower share price alone cannot change 62. Each JSON rating supplies its rule, supporting evidence and observable upgrade/downgrade trigger.

Both records have `summary.status: provisional` because income, balance-sheet and visibility primary bands use teaching estimates, even though every band has a point result. The score interval collapses to **76-76**, so scalar 76 is retained, and evidence coverage is **100%** (100 exact assessed weight, zero bounded/missing weight). Coverage does not mean certainty or independently verified facts. `reported` refers only to a stipulated fictional disclosure in this packet.

## Partial-Evidence Score Controls

These are independent modifications of the teaching scorecard, not new issuer assessments. Recompute using `scripts/decision_rules.py`; corresponding full-contract regressions are in `tests/test_provisional_scoring.py`. Paths are relative to the installed skill root; for example, run `python -m unittest discover -s tests -p test_provisional_scoring.py`.

| Change to the supplied evidence | Quality /85 | Combined /100 | Covered weight /100 | Grade / Consequence |
|---|---:|---:|---:|---|
| Only the buyback primary band is unknown | 57-67 | 71-81 | 90 | B provisional; no extra entry veto |
| Only tax/income evidence is unknown | 62 | 62-77 | 85 | C-B; wait for tax evidence, do not lose quality |
| Buyback is bounded to bands 2-3, with one met and two unknown checks | 59-64 | 73-78 | 100, including 10 bounded | B provisional; no neutral midpoint |
| Reconciled FY2024-2025 cash proxy spans 2.0-2.3x; full forward evidence otherwise unchanged | 60 | 74 | 100, including 20 bounded | B provisional; proxy capped at 16/20, three-year ratio stays null |
| Every primary module is unknown | No company score | No company score | 0 | Insufficient; mathematical 0-100 is not 0 or 50 quality |

For the first row, five-point buyback discipline is removed from the original 76, leaving 71 across 90 weight; its remaining contribution is 0-10. That means 71-81, **not** `71/90 x 100`, not a 76 midpoint, and not an actual 71-point company score. The quality interval lies wholly in Medium, so a matching provisional label remains available.

For the bounded buyback row, the worst candidate yields `2 + floor(2 x 1/3)=2`, while resolving both unknown checks favorably in band 2 yields 7. Exact subtotal stays 71 across 90, bounded weight is 10, and aggregate range is 73-78. `Buyback Quality` itself is Unclear with Neutral/Poor alternatives when a program exists; a known no-program label remains Not Applicable.

If a cash/capital bridge is genuinely unreconciled, the coverage module remains unknown and action stays suspended, but the other modules and their aggregate interval survive. A current recurring-income proxy can be scored separately at a maximum 9/15 with supported tax/cash treatment, without establishing N or a buy price. The lowest visibility band requires actual adverse issuer evidence, not merely an unfinished forecast.

## Holding-Period Return and Downside Answers

Use the first three entitled cash payments from the same runway, with A8's stated exit-yield assumptions:

| Case / Scenario | Three-Year Net Cash | Exit Price | Cumulative Return at 40 |
|---|---:|---:|---:|
| Ordinary / Bear | 9.6 | 32 | 4% |
| Ordinary / Base | 12 | 50 | 55% |
| Ordinary / Bull | 14.4 | 60 | 86% |
| Growth / Bear | 9.79328 | 33.2928 | 7.7152% |
| Growth / Base | 12.2416 | 52.02 | 60.654% |
| Growth / Bull | 14.68992 | 62.424 | 92.7848% |

The ordinary Bear exit loses **20% of principal**, and growth Bear loses **16.768%**, despite positive modeled cumulative cash returns. Base/Bull outcomes partly depend on exit-yield assumptions; they are not an intrinsic-value guarantee or an annualized return. The passing risk review is a teaching research assumption, not a finding about a real investor's loss tolerance. Funding impairment, payout restrictions or persistent operating/dilution changes invalidate the entry thesis. No personal position size is inferred.

Scenario percentages and the 2% steady-growth assumption are fictional. Real growth needs operating/funding/terminal evidence; it cannot be inferred simply because these fixtures pass. The examples do not assert that any named issuer qualifies or that the framework is calibrated to investment outcomes.
