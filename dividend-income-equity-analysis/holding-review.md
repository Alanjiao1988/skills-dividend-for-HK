# Holding Review

This Full Analysis module is embedded in **Section 17: Score, Portfolio Role, and Holding Review**. It does not add a nineteenth section or replace the scoring, cash-flow, business-outlook or valuation contracts.

The actions `hold`, `review`, `trim`, `exit`, `switch` and `not_assessed` are **research conclusions for human consideration**, never orders or automatic trading. Set `automatic_trade: false`. Do not execute trades, infer account permissions or invent position sizes.

## 1. Separate the Reasons for Review

Evaluate thesis/capital/payout failure first, independently of price. A cheap quote, high yield or favourable total score cannot cure a structural failure or a triggered veto. Distinguish this from valuation, a superior alternative and portfolio concentration:

| Category | Review trigger | Evidence required | Research response |
|---|---|---|---|
| `thesis` | A stated thesis invalidation signal; persistent or structural deterioration; failure of a development milestone | Original thesis, dated operating evidence, changed forecast and classification | Rebuild the thesis and evaluate holding/exit suitability without waiting for a price threshold |
| `cash_capital` — solvency | Liquidity, refinancing, remittance or regulatory capital support fails | Maturity/funding bridge, restrictions, available capital and credible remediation | Prioritize capital protection review; evaluate exit/trim when holder constraints are known |
| `cash_capital` — payout | Recurring FAD or actual post-exceptional-use distribution capacity no longer supports payout; material dilution | Both cash-coverage tests, policy calculation, share bridge and funding gap | Reassess sustainable forward income and the veto; distinguish planned change from unsupported payout |
| `valuation` | Price exceeds the applicable valuation-review boundary or forward return no longer compensates for evidenced risk | Updated independent return requirements, coherent forecasts and price/date | Review valuation and possible reduction; crossing a band is not an automatic sale |
| `opportunity_cost` | A named, researched alternative may provide a material same-basis net benefit | Comparable forward cash/returns, risks, costs and a documented switching hurdle | Complete Section 5 before concluding `switch` |
| `portfolio` | Concentration, liquidity, currency, sector or mandate constraints are breached | Actual holdings, portfolio exposures and explicitly applicable limits | Assess rebalance/trim independently of whether the business remains attractive |

Use company-specific, evidenced thresholds and investor-supplied constraints, not universal numeric stop-losses, target profits or concentration limits. Price appreciation, a percentage loss, a new high, or yield compression alone is not a mechanical sell signal.

A `Triggered` veto or Structural Decline must prompt action evaluation immediately, even below cost or with valuation suspended. An `Unclear` veto prompts evidence review, not a claim of proven failure or a reassuring hold. A managed-runoff exception requires checking whether the remaining finite cash-recovery case still holds; it is not permission to ignore new funding stress.

Check recurring support and actual affordability separately using `buy-zone.md`: exceptional cash uses can leave a funding gap despite apparently adequate recurring FAD, while excess cash can temporarily mask weak recurring support. An unresolved funding gap blocks an eligible growth valuation and prompts capital/payout review; it is not cured by a favourable terminal value.

## 2. Inputs and Unknowns

Use forward returns and cash income from **today**, not yield-on-cost:

```text
Forward Net Yield = evidenced next full-year recurring net DPS / current price
```

State whether the quoted cash is a full year, calendar-year forecast or remaining stub. Reuse the same year/scenario runway records for the 3-5-year dividend path; do not annualize a stub or use normalized N as near-term cash without explanation. Match price and DPS by currency, `valuation_unit_scale` and share/ADR entitlement before calculating yield. Cost basis is relevant to actual disposal taxes, not an economic reason to wait until a position breaks even.

Required position-specific inputs include:

- Security/ADR identity, quantity or capital at risk, current price/date and value.
- Total portfolio value, relevant weights and correlated sector/currency/issuer exposures.
- Investor currency, investment horizon, liquidity needs and risk/mandate restrictions.
- Explicit cash-income preference or hard minimum, including its measurement period and whether it is a yield or an absolute amount.
- Applicable tax/account treatment, FX method, recurring fees and execution costs. Cost basis is required when it materially affects disposal tax.
- The original thesis, current evidence, next decision-relevant milestone, and updated capital/payout/valuation analysis.

`portfolio_inputs_available` is true only when the material holdings and personal constraints needed for the conclusion are supplied. If false:

- Use `action: review` when there is an evidenced security-level concern; otherwise `not_assessed`.
- Set `position_change_fraction: null` and list the missing inputs.
- State the security-level concern without assuming a holding exists, choosing a lot size, or issuing a personalized hold/trim/exit/switch recommendation.

An unknown input is not zero, a waived restriction, a tax exemption or a satisfied hard-income floor. A missing price prevents a price-band comparison but does not prevent a thesis-failure review. Missing alternative research prevents a switch assessment, not every other form of review. If year-4/5 cash cannot be estimated, preserve the unavailable fields/reasons and explain the effect on prospective-return confidence.

## 3. Valuation Review Is Not an Exit Rule

Use the applicable primary model from `buy-zone.md`:

| Valuation basis | Review threshold | Meaning and limitation |
|---|---|---|
| Ordinary income primary | `P_current > N / r_low` | Current normalized cash yield is below the required income range; reassess prospective value/income, not automatic sale |
| Growth primary | `P_current > growth_value_high`, equivalently `P_current > review_above` | Price exceeds the highest coherent scenario PV; review returns and opportunity cost |
| Finite-life harvest | Price exceeds the documented finite-life recovery range, or expected remaining recovery/funding changes | Re-estimate the remaining dated cash and residual, retaining the discount floor and no perpetuity |
| Suspended / unavailable | No valid price threshold | Address the thesis/veto/evidence failure; do not invent a valuation-based exit price |

For a credible growth primary, an ordinary income comparison above `N / r_low` answers the cash-income question; it does not by itself mean intrinsic overvaluation. A preference shortfall may be compatible with holding for funded growth. A hard cash-income minimum still cannot be compensated by growth, capital gains or a buyback yield.

Review forward distributions, prospective total return, risk, taxes, costs and available alternatives before suggesting a valuation-driven trim or exit. Price appreciation or lower yield is only a prompt to update those inputs. Do not create a universal stop-loss, profit-taking percentage or yield-compression sell trigger.

## 4. Action Vocabulary and Decision Discipline

| Action | When supported | What must be explained |
|---|---|---|
| `hold` | Thesis, capital/payout and known portfolio constraints remain acceptable; prospective economics support retention | Forward cash/return rationale, remaining risks and next invalidation signal |
| `review` | A trigger, changed assumption, material uncertainty or incomplete holder context needs evaluation | Trigger, evidence, missing input and the decision it could change |
| `trim` | Evidence supports a partial reduction for concentration/mandate or prospective valuation/risk reasons | Why partial rather than full reduction; holder constraints and size basis if supplied |
| `exit` | Confirmed thesis/capital/payout failure or unacceptable mandate/prospective economics supports full withdrawal consideration | Failure evidence, alternatives to exit, costs and remaining uncertainty; not a reaction to cost basis |
| `switch` | A documented named alternative satisfies the net-benefit, risk and income conditions below | After-cost advantage, switching hurdle, robustness and comparable income |
| `not_assessed` | Material inputs do not support a responsible conclusion | Missing inputs and how to obtain them; do not disguise this as a neutral hold |

These labels do not execute anything. Even `exit` does not imply an available or suitable order type, date or tax strategy. `position_change_fraction` may be numeric only with a documented existing position, relevant constraints and a justified size calculation; otherwise it is null. There is no default trade fraction.

Keep every triggered category visible instead of blending them into a score. For example, a concentration-driven trim does not mean the thesis failed, and a thesis failure does not need an overpriced quote to warrant exit evaluation. State the primary rationale and any secondary rationale separately.

## 5. Opportunity-Cost and Switch Analysis

Never invent an alternative or infer that some unspecified “better stock” exists. Identify the candidate, sources/as-of dates, sustainable cash forecast and risks; apply the same fundamental and veto standards to it. If research is incomplete, `switch_analysis` is null with the missing work stated, not a fabricated numerical comparison.

Any eligible growth case used for either choice must pass both recurring-FAD and actual-capacity funding tests, including its structured terminal funding reconciliation. Do not compare a fully funded current holding with an alternative whose cash shortfall is hidden behind a narrative growth assumption.

Compare both choices on:

- The same decision-date starting wealth, nominal investor currency, horizon and treatment of cash held or reinvested.
- Forward after-tax recurring cash receipts, ADR charges, payout/remittance access and expected dilution.
- Currency conversions/hedges and FX costs; nominal returns and dividend timing must match.
- Capital, business, forecast and liquidity risks, including the risk of the prospective resale value.
- All incremental one-time switching costs: commissions, spreads/slippage, applicable sale taxes, FX conversion and ADR cancellation/transfer charges where relevant.
- Recurring taxes/fees and terminal sale costs for **both** choices. Do not count a recurring charge or one-time cost twice.

Historical purchase costs are sunk unless they affect a real future tax liability. For an absolute-income mandate, compare income on the capital actually deployable after switching, not the same assumed share count or a headline dividend yield.

An auditable cumulative-return comparison is:

```text
W0 = current holding's decision-date market value
C0 = incremental one-time taxes and costs of switching now
Alternative Deployable Capital = W0 - C0
W_hold_H = horizon net liquidation value of the retained holding
           + forward net cash receipts carried to the same horizon
W_switch_H = horizon net liquidation value bought with Alternative Deployable Capital
             + forward net cash receipts carried to the same horizon
Hold Net Return = W_hold_H / W0 - 1
Switch Net Return = W_switch_H / W0 - 1
after_cost_advantage = Switch Net Return - Hold Net Return
```

Use the same disclosed cash accumulation/reinvestment convention for both choices. Do not assume cash distributions are automatically reinvested in additional shares, and do not add buyback yield when its benefit is already in per-share cash/resale assumptions. C0 is already reflected in deployable capital and must not be subtracted again from `W_switch_H`.

`after_cost_advantage` and `switching_hurdle` are **cumulative decimal returns over the same horizon**, not a mixture of annual yield, annualized return and multi-year gain. Forecast terminal proceeds require evidence and scenario/sensitivity analysis; a quoted current multiple is not a guaranteed exit multiple. Without a responsible prospective-return comparison, do not conclude `switch`.

A switch is supported only when all conditions hold:

1. A named, researched alternative and sufficient holdings/personal inputs exist.
2. `after_cost_advantage > switching_hurdle` after all material costs and taxes. Equality is insufficient.
3. `switching_hurdle` and `hurdle_basis` explicitly describe the required improvement and allowance for forecast/implementation uncertainty. There is **no default numeric hurdle**; neither a guessed zero nor an invented universal percentage is acceptable.
4. `income_constraint_met` is true on the actual deployable capital and timing. Growth cannot repair a failed hard cash-income requirement.
5. `risk_comparison_supported` is true: remaining risk differences and any trade-off are evidenced and compatible with the stated constraints, not declared equivalent because the yields look similar.
6. The claimed benefit is not just an optimistic scenario. Explain its robustness to plausible cash, terminal-value, tax and FX uncertainty, or mark the case for further review.

If the hurdle, risk comparison, costs or material income inputs are unknown, leave the switch conclusion unassessed; a security-level review can still proceed. Do not create a numeric trigger to complete a table.

| Option | Deployable Capital | Forward Net Cash / Period | Same-Horizon Net Return | Taxes / Fees / FX / Costs | Risk and Evidence |
|---|---:|---|---|---|---|
| Retain current holding | | | | | |
| Named researched alternative | | | | | |

Report `switch_analysis.alternative`, `currency_and_horizon`, `current_forward_cash_income`, `alternative_forward_cash_income`, `cost_and_tax_assumptions`, `after_cost_advantage`, `switching_hurdle`, `hurdle_basis`, `income_constraint_met`, `risk_comparison_supported` and `evidence`. Identify the income period and currency in the accompanying text; preserve the broader annual income path by reference.

## 6. Monitoring, Re-Entry and Required Output

Every review must state:

- **Thesis invalidation signal:** the observable company-specific event or metric that would invalidate the thesis, its evidence and the associated research response. Record it as a `thesis` trigger, not a universal price loss.
- **Next recheck:** a stated date or concrete event, such as the next results release, debt maturity/refinancing decision, payout-policy announcement or development milestone. If the date is unknown, say so and specify the event/source to check; do not invent a reporting date.
- **Escalation:** material guidance, capital/remittance or payout changes, veto events and structural deterioration require earlier review regardless of price.
- **Re-entry conditions:** what must be repaired or evidenced, the applicable updated entry discipline, income constraints and required rerun of the veto/forecast. A thesis-driven exit cannot be reversed merely because price fell; a valuation-driven trim cannot be reversed merely because price returned to purchase cost.

Use `business-outlook.md` milestones for the full year-1-through-5 development path. Route misses as transient, persistent or structural and apply the appropriate revaluation rules. A future recheck is a documented research plan, not an automatically scheduled trade.

The `holding_review` output contains:

```text
action: hold / review / trim / exit / switch / not_assessed
rationale:
portfolio_inputs_available:
position_change_fraction: null unless supported by supplied holding/constraint inputs
missing_inputs:
automatic_trade: false
triggers[]: category, threshold, evidence, research_action
switch_analysis: supported comparison or null
next_review: date/event, earlier escalation signals, and re-entry/recheck conditions
```

Each trigger's evidence includes its source/date and relevant uncertainty. `threshold` must distinguish an observed breach from a condition being monitored; `research_action` states the proposed evaluation and reopening evidence. Include at least the thesis invalidation signal and all material active triggers. If no responsible signal or action can be assessed, explicitly record what is unknown and why.

Keep the rationale separate from the score and state facts, assumptions and judgments distinctly. Use null / `Not assessed` for missing numerical inputs and explain their effect. Tables must have at most seven columns. Conclusions are research, not individualized investment, tax or execution instructions.
