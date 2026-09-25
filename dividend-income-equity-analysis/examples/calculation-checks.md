# Synthetic Calculation Checks

Use these cases after changing calculation or decision rules. They are fictional regression examples, not market forecasts. Recompute with a calculator or code and explain the accounting and decision basis.

## Cash Flow, Policy and Scrip

Given OCF 100 after interest and tax, total capex 30 (maintenance 20 included), no further claims, ordinary attributable profit 100, a 50%-of-profit payout policy, 100 dividend-entitled shares, and 120 weighted-average diluted EPS shares:

- Analytical FCF is 70; do not deduct maintenance 20 again.
- Policy dividend entitlement is 50; do not apply 50% to FCF 70 to produce 35.
- DPS is 0.50, using 100 entitled shares.
- If issuer scrip retains 40% of the dividend cash, actual issuer cash cost is 30. An investor choosing cash still receives gross DPS 0.50; at 10% withholding and price 10, net yield is 4.5% before fees.
- At scrip issue price 5, retained entitlement 20 issues 4 shares, affecting subsequent entitlements when eligible. A broker reinvesting an already paid cash dividend does not reduce issuer cash cost or itself issue shares: issuer cash cost remains 50.
- If available capacity falls to 20, the policy entitlement remains 50 until the policy or modeled payout changes. Show the 30 all-cash-equivalent shortfall, scrip settlement assumptions and any funding plan; the policy number is not evidence of a sustainable dividend.

## Price Threshold Versus Action

With N=1, B=0.50, r_low=5%, r_high=8%, the normalized low-end cash-yield boundary is 20, normalized high-end boundary is 12.50 and Bear high-end boundary is 6.25. The four income bands are: price above 20, below required cash yield; (12.50, 20], normalized income within required range; (6.25, 12.50], normalized income meets high-end requirement; and positive price at or below 6.25, Bear income meets high-end requirement. A price of 5 satisfies the arithmetic Bear threshold.

These are cash-income comparisons with no dividend growth credited, not a complete estimate of intrinsic value. Equality at 12.50 belongs to the normalized-high-end band and equality at 6.25 to the Bear-high-end band. No band assigns a trading action.

- Strong Buy still requires all evidence and capital-risk gates, High confidence and Strong safety.
- Medium confidence permits at most gradual accumulation after the other gates pass.
- Low confidence is diagnostic only; Unclear veto suspends valuation output.
- B=0 gives no positive-price Bear-high-end band and precludes a Strong Buy action for an ordinary-income strategy. B>N is an inconsistency to resolve, not a number to clamp. N<=0 or nonpositive required yield suspends ordinary valuation.

## Positive Entry and Transparent Scoring Controls

- With N=4, B=3.2, r_low=8%, r_high=10%, the ordinary starter/add/strict prices remain 50/40/32. At price 40, Medium confidence, Acceptable safety, verified cash/tax/capital and a passing return review produce **gradual accumulation**, not a blanket wait for High confidence. At 50, the starter boundary still qualifies; above 50, wait for price.
- With the same evidence at price 32, High confidence and Strong safety permit Strong Buy; Medium still permits only accumulation. No portfolio allocation percentage is inferred.
- For growth scenario values 45.7142857143 / 57.1428571429 / 68.5714285714 and a declared 15% safety discount, starter is 48.5714285714, add is 45.7142857143, strict is 38.8571428571. Price 40 can support Medium-confidence accumulation even though it has not reached the strict threshold.
- A hard 12% forward yield target with forward net cash 4 caps the starter price at 33.3333333333; from current 40 the gap is -16.6666667%. Wait for that price when other gates pass; do not describe a known price shortfall as missing company evidence. A 12% preference does not impose that cap.
- Coverage band 2, with floor 12 and ceiling 16, earns 12/13/14/16 points for 0/1/2/3 met checks. Unknown refinements do not become a middle-band guess or a new entry veto. Altering the total to 99 without matching module points is invalid even if the Grade is also changed to A.
- With only income unassessable and quality 62/85, retain quality and show combined **62-77/100, C-B**, assuming no lower income cap. The scalar total/Grade stay null, not the interval display. Missing tax still blocks entry.
- With only the ten-point buyback module unknown, the teaching scorecard retains **71 points across 90 weight**, yielding **71-81/100, B provisional** and quality **57-67/85, Medium**. Never rescale to 79, impute 5 or display the lower bound as an actual point score. This gap is not an independent entry veto.
- With buyback candidate bands 2-3, one met and two unknown checks, its supported score range is 2-7; exact subtotal 71 plus that range gives **73-78/100**, 90 exact weight plus 10 bounded weight. Coverage is 100%, not 100% confidence.
- With reconciled two-year FAD 80+90 and cash dividends 40+40, coverage is 2.125x, not a three-year measure. A supported proxy range 2.0-2.3x uses the explicit 16/20 cap; the teaching total becomes **74 provisional**, not an unavailable overall score.
- With every primary band unknown, status is insufficient and coverage 0%; the 0-100 rubric bound is not an assigned zero or neutral 50. Missing forecast work alone must not manufacture a one-point visibility score.

## Growth Evidence Without Project-Level ROIC

- A fictional regulated operator discloses installed capacity, commissioning dates, contracted tariffs and a funded capex plan. Bounded utilization and maintenance/working-capital estimates reconcile to owner cash, mandatory capital uses, payout policy and shares in every scenario and terminal year. This can support `direct_operating_to_dps` and Medium confidence even without management-published marginal ROIC for each project, provided the common tax, remittance, funding and terminal gates pass.
- If the same operator's material subsidiary remittances or required capital contribution cannot be bounded, the direct bridge is not sufficient for eligible growth. Leave the affected evidence gate unresolved; a larger margin of safety does not supply the missing fact. Use any independently credible ordinary income comparison only if its own common inputs remain sound.
- Do not apply a scenario cash haircut, a premium and a safety discount three times for the same commissioning risk. Explain which uncertainty each treatment covers.

## Screening and Total Return

- At price 10, recurring gross cash DPS 0.40 plus a one-off special 0.50 can show 9% paid trailing gross yield but only 4% recurring gross income. Do not pass a 5% recurring-income hard minimum using the special. If the user explicitly selects total TTM cash as their criterion, use it and flag its composition.
- A 4.5%-5.5% net-yield range straddles a 5% hard minimum: Yield Fit is Unclear and the yield evidence alone supports Watch, not a false Pass or definitive No. With no target, use Not Assessed, not an invented minimum.
- Buy at 10, collect net cash dividends 0.60 for each of three years, sell at 7: no-reinvestment total return is -12%, despite 6% annual cash yield. Timing-aware annualized return requires an IRR calculation; do not label 6% the expected total return.
