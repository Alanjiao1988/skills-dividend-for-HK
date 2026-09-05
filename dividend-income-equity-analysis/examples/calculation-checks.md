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

With N=1, B=0.50, r_low=5%, r_high=8%, the upper income boundary is 20, normalized accumulation boundary is 12.50 and Bear threshold is 6.25. A price of 5 satisfies the arithmetic Bear threshold.

- Strong Buy still requires all evidence and capital-risk gates, High confidence and Strong safety.
- Medium confidence permits at most gradual accumulation after the other gates pass.
- Low confidence is diagnostic only; Unclear veto suspends valuation output.
- B=0 gives no positive-price Strong Buy zone. B>N is an inconsistency to resolve, not a number to clamp. N<=0 or nonpositive required yield suspends ordinary valuation.

## Screening and Total Return

- At price 10, recurring gross cash DPS 0.40 plus a one-off special 0.50 can show 9% paid trailing gross yield but only 4% recurring gross income. Do not pass a 5% recurring-income hard minimum using the special. If the user explicitly selects total TTM cash as their criterion, use it and flag its composition.
- A 4.5%-5.5% net-yield range straddles a 5% hard minimum: Yield Fit is Unclear and the yield evidence alone supports Watch, not a false Pass or definitive No. With no target, use Not Assessed, not an invented minimum.
- Buy at 10, collect net cash dividends 0.60 for each of three years, sell at 7: no-reinvestment total return is -12%, despite 6% annual cash yield. Timing-aware annualized return requires an IRR calculation; do not label 6% the expected total return.
