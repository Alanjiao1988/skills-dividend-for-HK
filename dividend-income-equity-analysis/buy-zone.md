# Buy Zone Rules

This Full Analysis module translates sustainable after-tax dividend capacity and independently assessed risk into research entry and valuation-review ranges, not guaranteed target prices or trade instructions. Screen Mode must not use it to generate forecasts, N/B, buy zones, or a screening target.

Keep three questions separate:

- **Income fit:** does forward cash income meet the investor's explicitly stated objective?
- **Income entry comparison:** what price meets the required cash yield on sustainable ordinary DPS?
- **Growth value:** what are evidenced future shareholder dividends worth after funding the growth that produces them?

A low yield or a particular company name does not select a growth model. An income-yield shortfall alone does not establish intrinsic overvaluation.

## 1. Inputs and Valuation Routing

Read `business-fundamentals.md`, the applicable `sector-fcf-proxies.md` contract, and `business-outlook.md` before valuation. Required inputs include:

- Current price, quote currency/unit, share or ADR ratio, valuation date, and data cutoff.
- Trailing and recurring DPS separately; withholding, recurring ADR fees, cash election, FX and other material investor cash deductions.
- Historical operating and cash-generation evidence, recurring FAD coverage, payout policy, capital/remittance constraints, and diluted/dividend-entitled share counts.
- Bear / Base / Bull operating-to-dividend forecasts: detailed annual cash rows for years 1-3; an explicit development outlook for all years 1-5; supported year-4/5 numerical scenarios or unavailable values with reasons.
- Fundamental Trend, Forecast Confidence, Structural Decline overlay, and the completed Dividend Trap Checklist.
- The sourced return requirements in Section 4; an explicit investor income target or `Not Assessed`.
- N and B when an ordinary income comparison is credible. Record unavailable inputs rather than forcing normalization.

Apply this order before comparing any value with current price:

| Precondition | Primary mode | Permitted output |
|---|---|---|
| Veto `Triggered` or `Unclear`, material cash/capital evidence insufficient, or forecast Not Forecastable | `suspended` | Missing evidence, resolution conditions, and holding review; no actionable valuation range |
| Structural Decline without the satisfied exception in `scoring.md` | `suspended` | No ordinary or growth entry zones |
| Structural Decline with the satisfied exception and no unresolved veto | `finite_life_harvest` | Finite cash recovery; optional explicitly secondary income cross-check |
| Non-declining business with all growth gates satisfied and a material evidenced development/reinvestment case | `total_return_based` when justified | Growth range plus a separate ordinary income comparison where credible |
| Sustainable ordinary capacity and credible N/B, without a justified primary growth case | `ordinary_yield_based` | Deterministic ordinary income zones |

Print `valuation_mode` and `valuation_reason`. Failure of a growth-only gate does not prove that ordinary income capacity is unknowable: an ordinary model may still be used if its own inputs and the common preconditions are sound. Conversely, growth must never bypass a veto or insufficient material evidence. Later-year gaps cannot be hidden by choosing a shorter model horizon.

## 2. Value-Trap Precondition

Value trap is a veto condition, not a cheap-price band. Run the checklist before **all** valuation modes, including growth and harvest.

Major veto conditions include:

- An unsupported dividend likely to be cut or suspended.
- Recurring FAD / relevant cash dividends below 1.0x without a credible recovery path, using the coverage contract rather than a peak-year ratio.
- Ordinary distributions dependent on debt, equity issuance or asset sales rather than recurring owner cash.
- Balance-sheet stress, an unaddressed refinancing wall, or regulatory/remittance restrictions blocking payout.
- Peak-cycle DPS presented as recurring capacity.
- Elevated payout alongside unexplained equity issuance, ATM or persistent unoffset scrip dilution.
- Forecast DPS unreconciled to business drivers, FAD, payout policy and dividend-entitled shares.
- N retaining temporary cycle premiums; growth depending on unfunded investment or an unsupported terminal state.

Distinguish demonstrated failure (`value_trap_veto: Triggered`) from an unresolved material evidence gap (`Unclear`); neither is `Not triggered`. A planned, funded managed runoff must be assessed under its exception, not assumed exempt from the checklist.

Required wording when triggered:

```text
Value-trap veto triggered: buy-zone output is suspended. High implied yield should not be treated as an entry signal until the following conditions are resolved: ...
```

When evidence is insufficient, state `buy zone cannot be responsibly estimated`, identify the missing bridge/source, and suspend the affected valuation. Do not display speculative growth thresholds as an alternative entry signal. Continue the price-independent thesis/capital review in `holding-review.md`.

## 3. Fundamental N/B Sources and Net Cash

For a simple cash dividend without additional investor charges:

```text
Net DPS = Gross DPS x (1 - withholding rate)
Buy Price = Net DPS / Required Net Yield
Normalized Buy Price = Normalized Net DPS / Required Net Yield
```

When recurring ADR fees or other material cash deductions apply, reconcile them explicitly to investor net DPS. Convert dividend and valuation cash to the same currency, quoted unit and security entitlement as price; distinguish FX from unit conversion. Never mix whole pounds with a pence price, an underlying share with an ADR, or gross dividends with an after-tax required yield.

`return_requirements.valuation_unit_scale` is whole valuation-currency units per quoted unit: 1 for a whole currency unit, 0.01 for pence. Record `shares_per_quoted_security` (1 for an ordinary share), the source `buy_zone.dps_currency`, `normalization_fx_rate` (valuation currency per source currency) and `normalization_fx_basis`. After matching the share/ADR entitlement, convert whole-currency DPS by multiplying by FX and dividing by `valuation_unit_scale` **once**. N, B, prices and growth per-share cash/value outputs all use that same quoted unit.

### N Source Priority

`N`, normalized net DPS, must represent mid-cycle or otherwise sustainable net dividend capacity. Preserve this priority:

1. `mid_cycle`: explicit mid-cycle distributable cash, payout policy, diluted share count, and withholding-derived net DPS.
2. `full_cycle_median`: full-cycle median distributable cash and payout-policy-derived net DPS.
3. `three_year_base_average`: average of three-year Base-case derived net DPS only when assumptions have returned to normal operating conditions.
4. `historical_fundamental_fallback`: fundamentally adjusted historical normalized DPS; this is a Lower Confidence fallback.

Always output:

```text
N value:
N basis: mid_cycle / full_cycle_median / three_year_base_average / historical_fundamental_fallback
N source period:
N normalization adjustments:
```

A near-term Base case is not automatically normalized. Remove temporary commodity, freight-rate, geopolitical, credit, regulatory, interest-rate and pricing windfalls. Normalization changes operating capacity, cash uses, policy or shares first; it is not an arbitrary percentage haircut to historical DPS.

For `three_year_base_average`, reconcile directly to the same Base year-1/2/3 net DPS used in the Dividend and Yield Runway:

```text
Base Gross DPS Average = mean(Base runway derived_dps for years 1, 2, 3)
N = (Base Gross DPS Average x (1 - withholding_rate)
     x shares_per_quoted_security x normalization_fx_rate
     - normalization_cash_deductions) / valuation_unit_scale
```

Here source gross DPS is in whole units of the runway's financial currency, recorded as `dps_currency`. `normalization_cash_deductions` is the evidenced normalized annual investor fee per quoted security in whole valuation-currency units; use explicit zero only when justified. State the actual three fiscal periods and tax/FX basis; do not apply another unexplained adjustment after averaging. If those Base years are not normalized, use another eligible basis in the stated priority order or report N unavailable rather than forcing this basis to pass.

### B Source

- `B` normally comes from Bear-case distributable cash, payout policy, diluted/dividend-entitled share count and withholding treatment.
- Reconcile N and B to operating drivers, profitability, cash generation, required reinvestment, debt/regulatory uses and expected scrip / DRIP dilution.
- If a direct Bear forecast is unavailable, a documented conservative fundamental fallback is allowed with Lower Confidence. It must still derive cash capacity, policy and shares; an unexplained `B = N x haircut` is not a fallback.
- State B's scenario, source period, funding bridge, and any fallback reason. Do not choose N or B to justify a preferred price.
- If no responsible B can be derived, do not publish the complete ordinary ladder or a Strong Buy label. N alone may support a clearly limited income-yield comparison.
- Forecast Confidence `Not Forecastable` precludes an ordinary buy zone.

## 4. Price-Independent Required Returns

### 4.1 Risk-Free Anchor and Premium

Print the benchmark, source, observation date, currency, tenor, nominal/real convention and investor tax/FX treatment. Explain how tenor fits the cash-flow duration and investment horizon. The valuation here uses **nominal**, same-currency cash and nominal required returns.

`return_requirements` must identify `benchmark`, `benchmark_source`, `benchmark_date`, `benchmark_currency`, `benchmark_tenor`, `valuation_currency`, `valuation_unit_scale`, `tax_and_fx_basis`, `rate_basis`, and the anchor after the disclosed treatment as `risk_free_rate`.

A US 20-year Treasury may be used when the user chooses it or a USD valuation/duration makes it suitable. It is neither a universal benchmark nor a hardcoded current rate. A non-USD security requires a matching-currency benchmark or an explicit, consistent cash-conversion/hedging treatment; do not simply discount unchanged foreign-currency DPS at a USD rate. Explain any unavoidable tenor mismatch.

Derive the equity premium **before looking at the security's price or implied yield**:

| Independent factor | Evidence to assess | Overlap control |
|---|---|---|
| Business risk | Demand, competition, cyclicality, operating leverage, policy stability | Do not charge twice for the same operating downside already modelled |
| Forecast reliability | Disclosure quality, driver sensitivity, execution and terminal evidence | Unsupported evidence is a gate failure, not a risk that any large premium cures |
| Capital / refinancing | Leverage, maturities, liquidity, capital coverage and dilution | Separate financing cash costs from residual uncertainty |
| Country / FX / payout restrictions | Currency exposure, remittability, regulation and investor access | A priced hedge, tax deduction or blocked payout must not also receive an unexplained duplicate charge |

Show the price-independent premium range, its evidence/rationale, and how overlaps were removed. Components may be grouped rather than mechanically added; if added, show their reconciliation to the aggregate. Neither total score nor Grade may map to a premium/rate band: both incorporate price-sensitive yield. Do not raise or lower premiums to make current price fit a desired conclusion.

```text
Rf = risk_free_rate
RP_low = risk_premium_low
RP_high = risk_premium_high
R_low = required_total_return_low = Rf + RP_low
R_high = required_total_return_high = Rf + RP_high
R_base = (R_low + R_high) / 2
```

Use decimals, `0 <= RP_low < RP_high`, and `0 < R_low < R_high`. State sources versus analyst judgments. Freeze the derivation before price comparison; an unavailable credible anchor/premium means `status: not_assessed`, null rates and no numerical entry zone, not an invented sector rate. `price_independent` must be true.

### 4.2 Ordinary Cash-Yield Derivation and Investor Objective

The conservative ordinary anchor gives **no growth credit**:

```text
income_growth_credit = 0
r_low = R_low
r_high = R_high
```

Print this derivation. Do not silently subtract assumed growth from required total return to improve the yield-based price. The finite-harvest cross-check separately retains its 10% floor. With fixed N, B, r_low and r_high, the legacy ordinary formulas in Section 5 are unchanged.

Investor income requirements are separate from these asset-specific return requirements. Carry `income_assessment.target`, `forward_net_yield`, `yield_fit`, `income_eligible` and the reason. A target comes only from an explicit current request or an explicitly applicable portfolio objective; otherwise it is `Not Assessed`. Never substitute this module's rates or sector ranges for the Screen Mode target.

- A `preference` shortfall is an income-fit observation, not proof of intrinsic overvaluation or a stand-alone growth disqualifier.
- A `hard_minimum` cash-income shortfall cannot be offset by growth, capital gains or buybacks. Report `income_eligible: false` and no investor-eligible entry/add conclusion at that price, even if the unconstrained growth value is higher.
- Record `forward_net_dps` and `income_period` alongside the yield. For a positive hard yield floor on an evidenced full-year forward dividend, separately show `income_price_ceiling = forward_net_dps / target_net_yield`. A growth candidate must satisfy both this ceiling and `entry_upper`; do not change the underlying valuation formulas. The ceiling is null for a preference, no target, a zero target, or unavailable forward cash.
- A hard absolute-cash requirement needs holdings/capital and timing inputs. If these or forward cash are unknown, investor eligibility is unassessed, not assumed satisfied. A stub or normalized N must not silently replace the income period the user specified.

### 4.3 Legacy Income Cross-Checks

Retain these as **income-specific reasonableness checks**, not automatic rate selection, growth discount rates, current market facts or investor screening targets:

| Dividend Profile | Legacy Required Net Yield Cross-Check |
|---|---:|
| Stable, regulated, low-volatility income | 4%-6% |
| Strong bank / telecom / utility with moderate growth | 5%-7% |
| Cyclical but financially strong dividend payer | 7%-10% |
| Formula-based variable dividend or commodity / shipping exposure | 8%-12% |
| Weak visibility, likely cut, or high leverage | Reassess evidence and veto; suspend when the preconditions fail |

Explain differences between the independently derived range and historical/sector yields. Cycle, capital, policy and dilution risk belong in the documented risk assessment or cash scenarios, not price-fitting adjustments. Stable coverage and conservative capital can justify lower independent risk, but growth by itself is not a cash-yield discount.

## 5. Deterministic Ordinary Income Boundaries

Use as the primary ladder for `ordinary_yield_based`. In `total_return_based`, retain a separately labelled **ordinary income entry comparison** whenever its inputs are credible. A harvest case may use it only subject to Section 8. Never present a secondary income ladder as another perpetual intrinsic valuation.

Definitions and validity:

```text
N = normalized_net_dps
B = bear_net_dps
r_low = required_net_yield_low
r_high = required_net_yield_high
P_current = current share price
N > 0; 0 <= B <= N; 0 < r_low < r_high; P_current > 0
```

If B exceeds N, investigate period, normalization and scenario inconsistency; do not silently clip B to force valid ordering. Missing or non-credible N/B/rates or Dividend Forecast Bridge means `buy zone cannot be responsibly estimated`.

Boundary formulas:

```text
Too expensive boundary = N / r_low
Fair lower boundary = N / r_high
Fair upper boundary = N / r_low
Accumulation lower boundary = B / r_high
Accumulation upper boundary = N / r_high
Strong buy boundary = B / r_high
N / r_low >= N / r_high >= B / r_high
```

| Zone, in the income lens | Deterministic Boundary | Meaning, not a trading instruction |
|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Normalized income yield is below the required cash-yield range |
| Fair value / hold | N / r_high < Price <= N / r_low | Income yield is within the required range; limited income margin of safety |
| Accumulation zone | B / r_high < Price <= N / r_high | Normalized income is attractive; Bear yield approaches the high-end requirement |
| Strong buy zone | Price <= B / r_high | Credible Bear DPS still meets the high-end cash-yield requirement |

If B equals N, the accumulation zone is empty and Fair connects directly to Strong Buy. If B is zero, the Strong Buy boundary is zero: no positive share price qualifies. A missing Bear estimate is not assessed zero capacity.

Keep the legacy names only with their income-lens qualifier. A Strong Buy band is conditional on credible Bear funding, the veto being clear and investor hard constraints being met; it is not a command to buy or a position-size recommendation. `Price > N / r_low` means an **income valuation review**, not necessarily excessive growth value or an automatic sale.

## 6. Gated Dividend Growth Valuation

### 6.1 Eligibility and Forecast Horizon

Set `growth_assessment.status` to `eligible`, `ineligible` or `not_assessed`, with `evidence_and_reason`. Growth is eligible only when:

- `funded_dividend_path`: each annual dividend reconciles to payout policy and is covered by **both** recurring FAD and actual Total Distribution Capacity after exceptional uses.
- `reinvestment_to_dps_reconciled`: evidenced investment and incremental returns translate into earnings, owner cash and per-share dividends.
- `capital_remittance_verified`: debt/regulatory needs, remittability and dilution are covered, not assumed away.
- `credible_terminal_state`: a finite transition and sustainable reinvestment/payout regime are demonstrable.
- Common veto gates pass, Fundamental Trend is not Structural Decline, and the evidence supports at least Medium Forecast Confidence.

Eligibility does not force growth to be the primary method. Explain why the evidenced 3-5-year development path materially matters to value; neither a ticker, industry label nor low current yield supplies that reason.

For every scenario and modelled year, require:

```text
Forecast Dividend Cash Cost_t <= Recurring FAD_t
Forecast Dividend Cash Cost_t <= Total Distribution Capacity_t
Funding Gap_t = max(0, Forecast Dividend Cash Cost_t - Total Distribution Capacity_t) = 0
```

An unresolved `funding_gap` or recurring funding shortfall blocks eligible growth. Excess cash may help actual-period affordability but cannot replace recurring support; conversely, strong recurring coverage does not override cash consumed by exceptional obligations. Do not repair either failure by silently reducing the forecast payout or increasing R. Reassess the policy, funding path and veto with evidence.

Use `explicit_horizon_years = T`, an integer from 3 through 5, with explicit annual Bear / Base / Bull forecasts. Detailed cash rows for years 1-3 and the year-1-through-5 business outlook remain mandatory. For supported years 4/5, show explicit scenarios; otherwise mark numerical fields unavailable with reasons. A terminal dividend relying on those years requires evidence, not a shortcut around missing forecast rows.

Keep the common scenario identities: `three_year_fundamental_forecast` supplies the first nine rows, `forecast_extension` supplies six year-4/5 rows, and the bridge/runway retain all 15 year/scenario records. Unsupported later-year values remain null / `not_estimable` with reasons, not omitted rows. Valuation references those same periods and dividends rather than creating a different forecast.

An eligible growth value requires supported, funded cash throughout that five-year outlook, including years after a shorter explicit valuation horizon. When H is less than 5, the first terminal-year FAD, dividend and share count must reconcile to the next forecast year's records. Otherwise extend the transition or decline growth valuation; a terminal-value label cannot hide a known future funding gap.

If steady state is not reached by year T, add a finite `transition_years = L` and forecast every intervening year through `H = T + L`, even when H exceeds 5. Provide the cash/funding/share bridge and milestones for each extension year. A project cycle, expiring economic right, capital repair or growth fade cannot be skipped by attaching Gordon value to an unstable endpoint. If no credible finite transition is estimable, growth value is unavailable.

### 6.2 Earned Growth, Not a DPS Plug

Choose and document `growth_method`:

| Method | Simple relationship under stated assumptions | Required bridge |
|---|---|---|
| `equity_retention_roe` | `g_earnings ~= equity_retention_ratio x incremental_ROE` | Retained common earnings invested in equity -> common earnings -> cash/capital -> payout and shares -> DPS |
| `operating_reinvestment_roic` | `g_NOPAT ~= operating_reinvestment_rate x incremental_ROIC` | Operating investment -> NOPAT -> financing/tax/owner claims -> FAD -> payout and shares -> DPS |
| `direct_operating_to_dps` | Forecast operating quantities, economics and cash directly | Explicit investment, lag, cash conversion, capital, policy and dilution evidence |

Standalone derivations:

```text
equity_retention_ratio = earnings retained for incremental equity investment / common earnings
incremental_common_earnings_(t+1) ~= retained_equity_earnings_t x incremental_ROE
operating_reinvestment_rate = growth_operating_investment_t / NOPAT_t
incremental_NOPAT_(t+1) ~= growth_operating_investment_t x incremental_ROIC
```

These approximations require positive meaningful denominators, compatible return periods, sustainable marginal returns and a stated investment-to-profit lag. Stable leverage, payout and share count cannot be assumed when they are changing. Historical average ROE/ROIC is not automatically the return on new investment. Longer or uncertain investment lags require the direct bridge, not instant growth.

Do **not** multiply an equity earnings-retention ratio by ROIC. ROE belongs to equity earnings/equity investment; ROIC belongs to operating reinvestment/NOPAT. Earnings retained on paper are not necessarily deployable cash. Account for repurchases and other equity uses before claiming the same funds support investment.

Reuse the parent cash-flow contract:

```text
Owner Cash Base = Recurring Owner FCF (or the eligible sector proxy)
Recurring FAD = Owner Cash Base - Remaining Growth Uses - Remaining Mandatory Uses
Total Distribution Capacity = Recurring FAD - exceptional_cash_uses + excess_cash_used
Derived Gross DPS = Forecast Dividend Cash Cost / Dividend-Entitled Shares
D_net_t = investor net dividend after tax/fees and the disclosed currency/unit conversion
```

Recurring Owner FCF is after maintenance investment and owner cash claims, but before separately identified growth investment. Subtract only committed growth and mandatory debt/regulatory uses not already deducted upstream; exceptional cash uses and available excess cash affect actual capacity separately and once.

Every projected dividend, including the first terminal year's dividend, must reconcile to that bridge, the policy's actual calculation base, share issuance/buybacks/scrip and capital coverage. Apply both funding tests from Section 6.1; a nonzero unresolved funding gap prevents an eligible growth result. Do not silently cap policy cash cost to hide a funding gap. Reuse the Dividend and Yield Runway's values and references rather than duplicating its Dividend Cash Cost / Derived DPS table.

Each reinvestment cash use is funded once and deducted once. Growth capex, working capital and required capital cannot be both distributed today and credited with producing future growth. Expensed pharmaceutical R&D is already an operating cash use: adding it back to distributable cash while also claiming its future growth creates free-growth double counting. Buybacks consume cash and alter future share counts; do not then add a buyback yield to DPS growth or total return for the same continuing holder. Reconcile payout growth and net dilution before inferring `g_DPS`; earnings growth is not automatically DPS growth.

### 6.3 Cash Timing, Formula and Terminal State

For each scenario state the valuation date, actual fiscal/calendar periods, expected payment timing and whether the next forecast is a **full year or a remaining stub**. All net dividends and values must use the same nominal valuation currency, quoted unit and share/ADR entitlement as price.

For full annual periods paid at year ends and steady state reached at T:

```text
Value = sum(D_net_t / (1 + R)^t, t = 1..T)
      + D_net_(T+1) / ((R - g_terminal) x (1 + R)^T)
```

When a finite transition is needed, replace T by `H = T + L` in both terms and include all transition cash flows. `terminal_net_dps = D_net_(H+1)` is the **first full-year recurring net dividend after the transition**, not averaged N. If `D_net_(H+1) = D_net_H x (1 + g_terminal)` is used, demonstrate that year H is already a representative full-year steady state.

Each scenario must provide a **structured** `terminal_funding` ledger, not just narrative: `owner_cash_or_proxy`, `remaining_growth_uses`, `remaining_mandatory_uses`, `recurring_fad`, `dividend_cash_cost`, `dividend_entitled_shares`, `fx_to_valuation_currency` and `investor_cash_deductions`.

```text
terminal_funding.recurring_fad = terminal_funding.owner_cash_or_proxy
                              - terminal_funding.remaining_growth_uses
                              - terminal_funding.remaining_mandatory_uses
terminal_funding.dividend_cash_cost <= terminal_funding.recurring_fad
```

Reconcile terminal dividend cash cost and entitled shares using the declared cash/share scales, then tax/fees, entitlement conversion and FX/`valuation_unit_scale` to `terminal_net_dps`. The ledger and `terminal_funding_and_fade_evidence` are both required. Known material exceptional obligations must be resolved through the finite transition or reconciled to actual capacity; an excess-cash release cannot finance the perpetual dividend. A narrative assertion of terminal coverage does not replace the numerical funding checks.

Gordon is a permitted simplification only in a demonstrated steady state, cross-checked against the explicit forecast:

```text
Gordon Value = D1_net / (R - g_terminal)
```

`D1_net` is the next full-year steady-state net dividend, not an arbitrary historical or three-year average. A short forecast does not establish steady state.

For a stub or non-integer timing, use the dated version:

```text
net_cash_i = forecast_cash_flows[i].net_dps x cash_fraction_i
PV_dividends = sum(net_cash_i / (1 + R)^years_from_valuation_i)
PV_terminal = terminal_net_dps / (R - g_terminal)
              / (1 + R)^terminal_time_years
Value = PV_dividends + PV_terminal
```

`net_dps` is the full-period net dividend already converted into the valuation currency/unit; retain `fx_to_valuation_currency` as the conversion audit, not a second multiplier in PV. Convert gross underlying-share DPS after withholding using `shares_per_quoted_security` and FX, subtract `investor_cash_deductions` (full-period fees per quoted security in whole valuation currency), then divide by `valuation_unit_scale`. Explicitly record zero deductions when there are none; missing material fee evidence cannot be silently treated as zero.

`cash_fraction` is the evidenced remaining **net** cash entitlement, not automatically elapsed months divided by twelve. Exclude distributions already received or no longer attached to the purchased security. If several cash dates represent a fiscal year, reconcile their fractions: first-year fractions sum to at most one, and subsequent full-year fractions sum to one. Use the sum of the final full fiscal year's dated net cash, not an individual quarterly payment, as the steady-state terminal-year bridge.

Record fiscal period, expected cash date, day-count convention, tax/fee allocation and FX basis in `cash_timing_and_fx_evidence`. For the terminal formula, `terminal_time_years` is the boundary one year before the first full-year terminal cash receipt. Align the explicit schedule and terminal convention, disclose any annual-payment approximation, and avoid a gap or overlap at the stub/terminal boundary.

### 6.4 Terminal Growth and Spread Guardrails

Terminal growth must follow sustainable investment, returns, payout, dilution and currency assumptions after an evidenced fade:

```text
g_terminal <= min(g_sustainable, long_run_nominal_growth_bound, terminal_growth_cap)
-1 < g_terminal
minimum_return_growth_spread = 0.02
R > g_terminal
R - g_terminal >= minimum_return_growth_spread
```

Use a documented conservative `terminal_growth_cap` of **3% or lower** as a modeling guardrail, not a claim about market growth. Separately source the valuation currency's long-run nominal economic bound and sustainable company growth; explain their periods and applicability. The guardrail is not a default positive growth forecast.

Unknown sustainable growth or missing fade/capital evidence means growth value is **unavailable**, not an apparently assessed `g = 0`. Evidenced zero or negative sustainable dividend growth is allowed for a non-Structural-Decline business; Structural Decline remains confined to the separate finite-life route.

Refuse calculations when `R <= g_terminal`, or when `0 < R - g_terminal < 0.02`. Refuse growth above the evidenced caps. Do not lower g merely to pass a denominator test: if the operating dynamics do not support the required fade, rebuild the transition or decline to value.

### 6.5 Scenarios and Sensitivities

Use coherent operating Bear / Base / Bull cases, not three arbitrary DPS multipliers. Each supplies annual funded cash, terminal funding/fade evidence and a justified terminal growth rate.

The default scenario discount rate is the same predeclared `R_base` for all three cases; report the full R range separately. Each scenario records `required_return_basis`; a different scenario-specific `required_return` within that range needs an explicit price-independent reason and an overlap check against cash-flow downside. Record the separate `sustainable_terminal_growth_bound`; neither scenarios nor the Base-path sensitivity may exceed the applicable company bound or the common currency/policy cap. Do not mechanically count the same risk in cash, premium and safety discount.

For every scenario output:

```text
required_return; terminal_growth; terminal_net_dps; terminal_time_years
forecast_cash_flows; terminal_funding; terminal_funding_and_fade_evidence
present_value_of_dividends; present_value_of_terminal; total_value
terminal_value_share = present_value_of_terminal / total_value
```

Show an R/g sensitivity using R_low, R_base and R_high and evidenced alternative terminal growth assumptions around the Base cash path. Hold the explicit operating cash path fixed for this sensitivity. Invalid cap/spread cells have null value and `invalid_growth_cap` / `invalid_spread`, not an extreme target price. Sensitivities are **not** Bear / Base / Bull scenarios, probabilities or a replacement for their funding bridges.

If terminal value exceeds **75%** of total value in any scenario, print `terminal_dependence_warning`, identify the affected scenarios and reduce stated growth-valuation confidence to at most Medium. This is an uncertainty warning, not proof of value. If terminal evidence only supports Low confidence, do not publish an eligible growth entry range.

## 7. Deterministic Growth Range and Income Constraint

Compute the range only from eligible, coherent scenario present values:

```text
growth_value_low = min(PV_Bear, PV_Base, PV_Bull)
growth_value_high = max(PV_Bear, PV_Base, PV_Bull)
base_case_value = PV_Base
entry_upper = growth_value_low x (1 - margin_of_safety)
review_above = growth_value_high
0 <= margin_of_safety < 1
```

Declare `margin_of_safety` and `margin_of_safety_basis` before price comparison, including the uncertainty it addresses. There is no price-fitting discount or undisclosed default; even zero requires an explicit reason. The range is not a confidence interval or a probability-weighted expected value. Investigate unexpected scenario ordering rather than assuming Bear is automatically the minimum.

| Growth comparison | Price condition | Research interpretation |
|---|---|---|
| Safety-discounted entry candidate | Price <= entry_upper | At or below the weakest scenario value after the declared discount; all gates and income constraints still apply |
| Below scenario range, without full safety discount | entry_upper < Price < growth_value_low | Not yet within the declared entry discipline |
| Within scenario value range | growth_value_low <= Price <= growth_value_high | Assess prospective returns, cash income and uncertainty |
| Valuation-review band | Price > review_above | Reassess valuation and opportunity cost, not an automatic sell |

Where boundaries coincide, the entry row takes precedence at `entry_upper`. Do not turn a favourable Base/Bull value into Strong Buy when Bear does not support entry. R/g grid extrema do not replace `growth_value_low/high`.

Keep a credible ordinary income comparison alongside the growth primary view and say which question each answers. If N/B are unavailable, explain why; do not fabricate the ladder. Report hard-income eligibility separately: the effective eligible ceiling for a positive hard yield floor is `min(entry_upper, income_price_ceiling)`, while the unmodified economic `entry_upper` remains auditable. Missing hard-income inputs preclude claiming investor eligibility.

## 8. Structural Decline: Finite-Life Cash Recovery Only

A company classified as `Structural Decline` must not use an ordinary or growth perpetual franchise assumption.

Without the Harvest / Managed Runoff Exception in `scoring.md`:

```text
Valuation mode: suspended
Ordinary and growth buy zones: suspended
Reason: Structural Decline without a credible finite-life harvest case
```

No Fair, Accumulation or Strong Buy zones may be printed. A low price or high yield does not override the restriction.

With the exception satisfied **and the common veto clear**, use:

```text
Finite-Life Cash Recovery Value
= sum(Net DPS_t / (1 + k)^t, t = 1..T_harvest)
+ Residual Value_T / (1 + k)^T_harvest
k >= 0.10
```

Required evidence includes explicit management runoff/harvest intent, conservative financing, a measurable decline in distributable cash, and distributions independent of refinancing, uncertain asset-sale timing or new equity. State the dated annual after-tax cash path, harvest horizon, expected cash-decline rate and conservative residual/liquidation basis.

Rules:

- Retain the **10% discount-rate floor**. Derive cash-recovery risk independently of price using Section 4, then use `k = max(0.10, justified_cash_recovery_required_return)`.
- The legacy 10%-15% moderate-risk range is a disclosed conservative cross-check, not a substitute for derivation. Use higher rates when recovery, timing or residual risk warrants them; an unresolved veto cannot be cured with a higher k.
- Do not assume a perpetual terminal dividend, even with negative g. Residual value is a finite, evidenced net recovery after liabilities, costs and taxes, not a disguised Gordon value.
- An uncertain recovery may be assumed zero as an explicitly conservative scenario assumption. Do not describe unknown recovery as verified zero.
- Show the residual value's percentage of total PV and avoid counting an asset disposal both in distributions and residual recovery.
- Ordinary N / r comparisons are secondary only, with `r_low >= 10%` and credible N/B; they cannot replace the finite-life calculation or imply a permanent franchise.
- The Grade C cap remains and the security cannot be Core income.

Required output: `harvest_horizon_years`, the dated forecast net distributions, discount rate/rationale, PV of distributions, residual and its basis/PV share, finite-life value range, and any separately qualified ordinary cross-check.

## 9. Sensitivity and Revaluation

Use the one-driver-at-a-time classification from `business-fundamentals.md`:

| Type | Ordinary income boundaries | Dated dividend valuation | Required response |
|---|---|---|---|
| `transient` | N unchanged; Accumulation Upper-Bound Change = `N/A` | Change PV by actual affected-period net cash deltas | Keep terminal g and R unchanged unless there is a lasting effect |
| `persistent` | Recalculate normalized capacity and N before boundaries | Re-estimate annual cash, sustainable growth and funding | Revisit risk only for an evidenced independent lasting risk change |
| `structural` | No mechanical boundary update | No one-cell target-price adjustment | Rebuild trend, forecasts, scoring, veto, mode and valuation |

A temporary operating shock must not move the long-run ordinary income ladder. It **must** change DDM value when it changes cash actually received:

```text
delta_net_cash_i = revised_net_cash_i - baseline_net_cash_i
present_value_change_i = delta_net_cash_i / (1 + R)^years_from_valuation_i
growth_value_change = sum(present_value_change_i)
```

For full-year end payments this is simply `sum(delta_D_net_t / (1 + R)^t)`. Apply the same dated logic to finite-harvest distributions. A temporary FAD change with an unchanged, funded dividend can have zero immediate dividend PV impact, but explain the cash-buffer bridge; do not substitute FAD delta for shareholder cash delta. If the shock causes lasting leverage, funding, payout or reinvestment effects, reclassify it instead of pretending it is transient.

Make the transient calculation auditable. Alongside `driver_sensitivity[].growth_value_change`, record a `growth_cash_delta_audit` for each affected period: `forecast_year`, `cash_timing`, `years_from_valuation`, `baseline_net_cash`, `revised_net_cash`, `delta_net_cash`, `required_return`, `present_value_change`, and `evidence`. Use the same converted net cash units as valuation; cash fractions and FX must be traceable to the runway and timing record. Sum the audit to `growth_value_change`.

| Driver / Scenario | Fiscal Period / Cash Date | Baseline -> Revised Net Cash | Timing / R | PV Change | Evidence |
|---|---|---|---|---:|---|

When a DDM is not assessed, use a null `growth_value_change` with reason, not zero. For a structural rebuild, both mechanical boundary-change and growth-value-change fields are null / `Rebuild required`. A transient update does not itself alter terminal g, R or the safety-discount policy; recompute scenario values and the declared growth thresholds only to reflect the actual cash change.

## 10. Historical Cross-Checks

Historical yield and price are secondary context, not inputs for fitting premiums, terminal assumptions or safety discounts. They cannot override a deteriorating forecast or Structural Decline route.

| Period | DPS Used | Price Range | Gross Yield Range | Net Yield Range | Yield Percentile | Comment |
|---|---:|---:|---:|---:|---:|---|

Separate recurring from special/variable dividends and identify whether historical prices and cash use contemporaneous or a consistent normalized DPS basis.

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|
| Current price | | | |
| 52-week high / low | | | |
| 3-year / 5-year median | | | |
| Drawdown from recent high | | | |
| Relevant index / sector | | | |

## 11. Required Outputs and Presentation

All Full Analysis cases disclose mode/reason, veto status, Forecast Confidence, income target/eligibility, return requirements and material limitations. Unavailable values are null / `Not assessed` with reasons, not fabricated rates, zero growth or apparently precise entry prices.

- **Ordinary:** N value/basis/period/adjustments; B source/fallback; r_low/high derivation; deterministic boundaries; price's income band and the hard-income check.
- **Growth:** `growth_assessment`; annual cash references and timing; investment-to-DPS evidence; T/L and finite fade; terminal funding/growth caps/spread; scenario PVs and terminal shares; R/g sensitivities; `growth_value_low/high`, `base_case_value`, `margin_of_safety`/basis, `entry_upper`, `review_above`; ordinary income comparison where credible.
- **Harvest:** finite distributions/horizon, independent discount derivation with floor, residual evidence and dependence, finite-life range and exception/Grade limits.
- **Suspended:** the exact gate/evidence failure, which information could reopen valuation, and holding-review implications; no valuation ladder.
- **Sensitivity:** keep transient ordinary changes `N/A`, but show the dated cash PV change and its audit when a dividend model exists.

Visuals follow `visual-output-rules.md`: ordinary ladder, growth-value range with separate income-fit information, or finite-life cash-recovery summary as applicable. Never display a Strong Buy badge for an unsupported Bear case or while a hard income constraint fails. Keep every table to at most seven columns.

Use `expected buy zone`, `income entry comparison`, `growth value range` or `finite-life value range`, not guaranteed price. This module is a conditional dividend model, not a full corporate DCF. Broader enterprise valuation may be a separate cross-check, but conflicting methods must be explained rather than forced into one answer. Excess-valuation, thesis failure and portfolio decisions belong to `holding-review.md`, embedded in Full Analysis Section 17 rather than a new report section.
