# Analytical Quality Records

This is the canonical source for the local analytical extensions originally added in schema **2.4** and retained in schema **2.5 / 3.0**. They explain provenance, sustainable cash economics and uncertainty; completing text boxes or passing arithmetic validation does not establish that the underlying evidence is true. Reuse the cash, sector, tax, settlement and valuation contracts rather than creating parallel models. For new scoring, `scoring.md` and rubric-2 `scorecard.summary` are authoritative; the legacy incomplete-total rule applies only when reading old records.

The machine modes are `screen`, `full_analysis` and `safety_review`. A focused normalization audit is a supporting task, not another mode. Full Analysis uses the **six-section main report** in `output-template.md`: every record below is still completed, its conclusion appears at the main-report location named here, and the full record goes to the named Audit Appendix part and JSON.

## 1. Minimum Work by Task

| Task | Mandatory minimum | Add only when relevant | Boundary |
|---|---|---|---|
| Screen | User target or Not Assessed, target basis/policy, current income and cash/capital evidence, triage | Evidence needed to resolve a specific screen flag | Follow `screen-mode.md`; no full-only records, N/B, forecasts, final score or action prices |
| Focused normalization audit | Arithmetic conclusion, evidence/action conclusion and the four operating-cash / funding / policy / entitled-share links | Driver/state provenance needed to test the proposed N | Follow `data-conventions.md`; do not fabricate a full report or create a fourth mode |
| Safety Review | Dated baseline/new disclosure, comparable cash/capital deltas, coverage, decision and escalation | Material controller, remittance or sector evidence | Follow `safety-review.md`; no new forecast, valuation, score or trade size |
| Full Analysis | Existing full contract plus the records below, each assessed or explicitly unavailable with reasons | Deeper source series, hedge detail or portfolio exposures when the conclusion depends on them | Keep the six-section main report, the on-request appendix and all existing action gates; missing data is not invented precision |

Required Full Analysis records are `controller_risk`, `quality_assessment`, `portfolio_role_assessment`, `real_income`, `fx_risk` and one or two `income_drivers`. Whenever `buy_zone` is present, `buy_zone.normalization_model` is also required, alongside the existing four-link `normalization_evidence`. A suspended report need not invent a buy zone to host the record.

| Record | Main-report conclusion | Audit Appendix part |
|---|---|---|
| Normalization model and evidence links | Section 3 names only missing or conflicting links | A10, referencing the operating/cash/policy/share bridges in A3/A8 |
| Controller risk | Section 2 one line only when material or unresolved-material; Section 5 when a trap item is flagged | A1 identity, A4 assessment; reused in A9 and A12 |
| Quality and role assessments | Section 1 status line (quality /85, combined point/range and coverage, role) | A11 |
| Real-income trend | Section 4 one clause, separate from nominal dividend stability | A2 |
| Economic FX and stress | Section 2 net-cash line when material; Section 5 when flagged | A5 map, A6 stress, conversion references in A10 |
| Income-driver tags | Section 4 business drivers | A5; used in A11 portfolio role only with actual portfolio exposure data |

Charts and extra presentation detail are optional. The analytical records, material limitations and source trail are not. Null means unavailable, not zero, immaterial exposure, a passed veto or a neutral score. State the missing disclosure, why it matters and what conclusion remains possible.

## 2. Normalization: Provenance and a Comparable State Ledger

The four evidence links are necessary but insufficient: they do not by themselves show how a sustainable operating state was selected. `buy_zone.normalization_model` records:

```text
status: assessed / not_assessed
method: cycle_distribution / supply_demand_balance / steady_state / not_assessed
cycle_applicability: cyclical / non_cyclical / unclear
cycle_length_years: supported estimate or null
cycle_basis:
period_start / period_end: ISO dates or null
frequency:
series_sources[]:
joint_assumption_rationale:
perimeter_adjustments:
drivers[]:
  name, unit, series_start, series_end, frequency, source
  selection: median / balance_point / steady_state
  selected_value, observations[]
cycle_states: low, mid, high
uncertainty_low / uncertainty_high: optional bounds on net N, otherwise null
uncertainty_basis:
```

### Select the Window and Joint Assumptions

- Justify the observation window from the industry's supply, contract, replacement or capital cycle. The five-year historical overview is **not** a default cycle length. State which regimes are covered, which are missing, and why the window is informative for today's business.
- Use `cycle_distribution` for an evidenced distribution across the relevant cycle, `supply_demand_balance` for a documented equilibrium/balance point, or `steady_state` for a supported noncyclical run rate. Method describes the model; it does not replace the existing `normalized_net_dps_basis` source hierarchy in `buy-zone.md`.
- Each driver identifies the full period, frequency, unit and source. A claimed median must be reproducible from the complete `observations` used, not a favorable subsample; preserve date ordering and the source's coverage/missing-observation explanation. A balance point or steady-state selection needs its economic rationale, even if no historical median is used.
- Construct a coherent **joint operating vector**. Independently taking marginal medians of prices, volumes, costs, utilization and spreads can produce a state that never coexists. Explain conditional relationships, lags, nonlinearities and any departures from individual medians. Do not stack unrelated marginal worst cases.
- Reconcile historical acquisitions/disposals, asset or product mix, current cost economics, maintenance requirements, payout policy and share structure to a comparable current perimeter. Keep reported history distinct from adjustments; do not erase a current obligation or treat a historical cash windfall as recurring.

`full_cycle_median` needs a coverage rationale for the actual cycle, not just a five-year label. Preserve the priority of explicit mid-cycle capacity, full-cycle median, a genuinely normalized three-year Base average, then a fundamentally adjusted historical fallback. Use `three_year_base_average` only under the existing normalization gates and reconcile it to the same Base runway; averaging three premium years does not normalize them. A fallback remains lower confidence.

### Recompute Each Applicable State

Every `cycle_states.low`, `.mid` and `.high` record contains:

```text
status: estimated / not_estimable / not_applicable
operating_assumptions:
owner_cash, growth_uses, mandatory_uses, recurring_fad, earnings
payout_basis: earnings / recurring_fad / stated_cash_flow / fixed_dps / discretionary
payout_base, payout_ratio, dividend_entitlement
shares, gross_dps, evidence
```

For an estimated state, use the financial model's owner perimeter, currency and cash/share scales:

```text
recurring_fad = owner_cash - growth_uses - mandatory_uses
gross_dps = dividend_entitlement * cash_unit_scale
            / (shares * share_unit_scale)
```

Deduct only remaining uses not already included in owner cash. Preserve negative FAD and actual funding obligations. For earnings-linked payouts, reconcile the documented earnings base and ratio; for FAD- or stated-cash-flow-linked payouts, identify the exact applicable cash base. Never blindly multiply a policy payout ratio by FAD. Fixed DPS uses the stated per-share amount and entitled shares; discretionary entitlement needs a sourced board/allocation basis, not an invented ratio. Explain any policy/funding adjustment and test recurring support and actual affordability independently.

`dividend_entitlement` is the full cash-equivalent entitlement before scrip elections, not the issuer's reduced cash payment. `shares` is the relevant entitled-share denominator, with an installment reconciliation when needed, not automatically EPS weighted-average shares. Apply `business-fundamentals.md` and `withholding-notes.md`: mandatory stock-only distributions do not create cash-election income.

The **mid** state represents the central sustainable gross DPS. When tax and the investor's cash treatment are known, reconcile it through the existing zone conversions:

```text
N = (cycle_states.mid.gross_dps * (1 - withholding_rate)
     * shares_per_quoted_security * normalization_fx_rate
     - normalization_cash_deductions) / valuation_unit_scale
```

State records store `gross_dps`; any net cycle-state DPS shown in the presentation is derived through these existing conversions, not an additional independent state input. Gross DPS is in whole source-currency units; fees are per quoted security in whole valuation-currency units. Apply share/ADR entitlement, FX, tax, fees and quote scaling once. A known gross state does not make unknown net tax treatment assessable. For `three_year_base_average`, the mid-state ledger must also reconcile to the permitted three-year Base average, not silently substitute a different N.

Low/high are **cycle-state DPS**, not three competing normalized Ns, not future Bear/Base/Bull years and not automatic sources for B. B retains its separately justified adverse forecast period and funding bridge. Optional `uncertainty_low`/`uncertainty_high` instead describe estimation bounds around the central **net N in quoted units**, with `uncertainty_basis` and `uncertainty_low <= N <= uncertainty_high`; do not relabel cycle extremes as those bounds. Supply the bounds as a pair; when unused, keep both nullable keys null as required by the machine contract.

A noncyclical steady-state case uses `cycle_length_years: null` and marks both low/high `not_applicable`, with the noncyclical rationale stated. A cyclical case with missing extremes uses `not_estimable` with the missing series/reason; never invent the extremes or call them inapplicable just to fill the ledger. Unsupported state amounts remain null. Missing extremes do not by themselves disprove a supported central estimate, but incomplete cycle coverage cannot support a claimed full-cycle median. If the mid-state evidence is insufficient, there is **no actionable N**: use `not_assessed`, explain the gap, and limit any supplied-number comparison to diagnosis or omit `buy_zone` when N/B cannot responsibly be populated.

## 3. Controller Cash Demand and Listed-Company Harm

Identify the **ultimate controller**, including an unlisted controlling parent. Trace the direction from the listed company paying or transferring resources to its controller; this is distinct from a listed holding company's ability to receive cash from its own subsidiaries. Assess both directions when relevant.

`controller_risk` contains `status` (`no_material_concern` / `watch` / `triggered` / `not_assessed`), `controller` (name or null), `materiality` (`material` / `not_material` / `unknown`), `material_harm_confirmed` (true / false / null), `cash_demand_evidence[]`, `listed_company_impact`, `channels[]`, `source_and_date` and `assessed_on`.

Review dated controller debt maturities/refinancing, share pledges, group investment or restructuring, related-party loans/guarantees/transactions, and documented payout-policy changes. Identify the mechanism, affected listed-company cash/capital, safeguards and counterevidence. Timing alone is association, **not causation**. Parent cash needs, group/state ownership or high payout alone never establish extraction or a veto.

| Assessment | Interpretation and consequence |
|---|---|
| `no_material_concern` | Sourced assessment finds no material harmful channel; it is not a guarantee of future conduct |
| `watch` | A documented demand/channel merits monitoring, but material harm is not confirmed; identify what would resolve or escalate it |
| `triggered` | Confirmed **material harm** to listed-company funding, necessary investment, liquidity or minority value; set value-trap veto `Triggered` and suspend actionable valuation |
| `not_assessed` | Evidence cannot establish the conclusion; explain the missing ownership/channel/cash information, not proven distress |

Materiality or a potentially material impact left unknown restricts conclusions to diagnosis and prevents Strong Buy/Core income until resolved; do not mark the veto passed. An identified controller need without material harm does not itself force a veto. A sourced finding of **no controlling shareholder** is valid: use `controller: null` with the ownership source and conclusion. Unknown ownership can also require null, but must be explicitly distinguished through status, evidence and limitations.

Use the same record in capital allocation, the trap checklist and holding review. Do not double-deduct the same cash transfer or apply a second risk premium for an effect already modeled.

## 4. Quality, Current-Price Income and Security Role

`quality_assessment` preserves the six existing non-current-price modules in `scoring.md`; it introduces no new weights or independent point choices. In schema 3.0 it is a projection of the same scorecard:

```text
status: assessed / provisional / not_assessed
components:
  dividend_stability: supported points / 15 or null
  cash_coverage: supported points / 20 or null
  balance_sheet: supported points / 15 or null
  capital_allocation: supported points / 15 or null
  buyback_quality: supported points / 10 or null
  visibility: supported points / 10 or null
score_85: scorecard.quality_score_85, including a collapsed provisional interval or null
component_ranges: the six quality entries from scorecard.summary.module_ranges
score_range: scorecard.summary.quality_range
coverage_pct: scorecard.summary.quality_coverage_pct
range_kind: rubric_bounds
price_independent: true
evidence_and_limitations:
```

For rubric 2, keep each component aligned with the corresponding scorecard module; do not invent a point for a non-collapsed module range. The four new range/coverage fields above are required mirrors, not independently estimated inputs. Display `scorecard.summary.quality_range`, `quality_rating_range` and `quality_coverage_pct` alongside the local record; `quality_rating_range` is not duplicated inside `quality_assessment`. Missing one component does not cancel the quality range, the combined score range or an otherwise stable provisional label. Status is `assessed` only when all six quality modules are exact `assessed` with `reported` or `reconstructed` primary evidence; it is `not_assessed` only when all six are `not_assessable`, and otherwise `provisional`. Income-only missing/estimated evidence does not change this quality-only status. A collapsed quality interval retains its scalar point without filling any unknown module with a midpoint.

The seven-module `score_100` and `grade` remain compatibility **mixed quality/income indicators**, not the primary quality measure. Their point/range/status follows the same rubric-2 summary. Never redistribute missing weights, scale partial points to 85/100, supply neutral points, or apply a second conservative deduction. Coverage is evidence coverage, not confidence or business quality. Real cash, tax, capital, normalization or controller gaps still restrict the conclusions that depend on them under their named gates; a missing noncritical scoring module alone is not a new buy veto.

Legacy local schema 2.4 records retain the original complete-component scalar semantics and their original scores/labels; legacy upstream rubric 1 similarly retains its null-total behavior. This compatibility path must not be applied to a new 3.0 report. Label historical comparisons by score type, framework version and as-of date; do not compare an 85-point quality total with a historical 100-point mixed total as if they were the same scale or silently re-rate old records.

Keep existing `income_assessment` for investor cash-income fit. When N, a positive current price and independent required cash yields are supported, its optional `required_yield_spread` is:

```text
normalized_net_yield = N / current_price
vs_low_pp = 100 * (normalized_net_yield - r_low)
vs_high_pp = 100 * (normalized_net_yield - r_high)
```

N and price must share currency, entitlement and quote units. These are percentage-point spreads; **they still depend on price** even though the required yields were independently assessed. They do not replace the user's target or override a hard income minimum.

Require `portfolio_role_assessment` with `basis: quality_safety_and_constraints`, an evidenced `rationale`, and `price_alone_changes_role: false`. Remove automatic Score-to-Role mapping. A lower quote with unchanged fundamentals, safety evidence and investor constraints leaves quality points and the assessed **security role unchanged**; it can improve income fit and entry attractiveness. A legacy grade, price band or yield spread cannot on its own award Core income. Core requires supported quality, safety, the applicable gates and investor mandate, not a magic score cutoff. Keep price-specific action eligibility explicit and separate; a newly attractive price cannot cure a material evidence gap.

Lead the main report's Section 1 status line with quality `/85`, the combined point/range with coverage, and role. The required scalar `key_metrics_at_a_glance.quality_score_85` must equal `quality_assessment.score_85` and `scorecard.quality_score_85`; null means the quality interval does not collapse, not that the range should disappear. Match the executive quality range and coverage to `scorecard.summary`. Show TTM yield and combined `/100` secondarily. Preserve all confidence, tax, cash-election, funding, growth, veto and Structural Decline overlays. Nominal dividend stability is the primary anchor; the rubric's explicit inflation refinement may use the same purchasing-power evidence once, without an extra ad hoc award or deduction for the separate real-income label.

## 5. Real After-Tax Income and Purchasing Power

`real_income` contains `status` (`assessed` / `not_assessed`), `currency`, `inflation_basket`, nullable `period_start`/`period_end`, `starting_net_cash`, `ending_net_cash`, `starting_price_index`, `ending_price_index`, `nominal_cagr`, `inflation_cagr`, `real_cagr`, nonnegative `flat_tolerance`, `trend` (`Growing` / `Flat` / `Eroding` / `Not Assessed`) and `source_and_method`.

Use historical after-tax cash, net of applicable fees and converted using actual-period FX, **per constant split-adjusted investor entitlement**. Separate distribution types and reconcile cash periods, corporate actions and tax/channel changes. New purchases or reinvested distributions do not create organic growth in per-entitlement income. A stock-only award is not received cash. State whether the comparable starting/ending observations are annual receipts or another matched period; do not compare a full year with a quarter.

Select a consumption basket that represents the investor's purchasing-power question, with its jurisdiction, index definition, source and observation periods. Do not choose CPI solely from the issuer's reporting currency, nor infer a personal spending basket from the listing venue. If the relevant basket is unknown, state the limitation.

With positive starting net cash, positive starting/ending price indices and a positive elapsed period:

```text
elapsed_years = (period_end - period_start).days / 365.25
nominal_cagr = (ending_net_cash / starting_net_cash) ** (1 / elapsed_years) - 1
inflation_cagr = (ending_price_index / starting_price_index) ** (1 / elapsed_years) - 1
real_cagr = (1 + nominal_cagr) / (1 + inflation_cagr) - 1
```

State this day-count convention. Five annual observations generally span **four intervals**, not five years of compounding. Subtracting inflation CAGR from nominal CAGR is only an approximation and is not the calculation contract. A zero ending cash amount can describe cessation; a zero/missing starting cash amount cannot produce an infinite growth rate. Missing inflation is not 0%. Unavailable inputs leave the affected rates null and the real trend `Not Assessed`, with the reason.

Justify `flat_tolerance` from data precision or a stated measurement convention; there is no hidden default. Classify Growing above the tolerance, Eroding below its negative, and Flat within the inclusive tolerance. Do not use an unsupported wide tolerance to conceal erosion.

Keep this purchasing-power diagnostic separate from nominal dividend stability and solvency. Real income erosion does not automatically mean dividend insolvency. Valuation cash flows and discount rates remain **nominal** under `buy-zone.md`; do not deflate only one side of the valuation.

## 6. Economic FX Exposure and Once-Only Stress

`fx_risk` contains `status` (`assessed` / `not_material` / `not_assessed`), `economic_exposure`, `operating_currencies[]`, `distribution_currency`, `investor_currency`, `material_exposure` (true / false / null), `hedge_and_natural_offsets`, `stress_rows[]` and `evidence_and_limitations`. Establish materiality from evidence; null is appropriate when it is unknown, never a fabricated false.

Map **revenue/cost/debt cash generation -> legally remittable cash -> payout currency -> investor currency**. The listing or accounting-reporting currency is not necessarily the economic exposure. Explain sensitivity direction, natural revenue/cost/debt offsets, hedge instruments, duration/coverage, costs and residual exposure. A peg or a same-currency dividend does not by itself establish immaterial economic FX risk.

Material assessed exposure needs at least an `fx_only` and a `combined_bear` row for the **same chosen forecast year**; any additional years also use matched pairs. Each row requires `kind`, `forecast_year`, `base_fx`, `stressed_fx`, `base_gross_dps`, `operating_gross_dps`, `hedge_cash_adjustment`, `investor_fees`, `base_net_cash`, `stressed_net_cash`, `delta_cash` and `evidence`. It also requires `economic_gross_dps_delta` (incremental revenue/cost/debt FX cash-and-payout impact in source-currency DPS), `economic_fx_in_runway` (boolean) and `economic_fx_bridge` (the supporting incremental reconciliation).

- Reference the same year's Base runway for `base_gross_dps` and its consistent baseline FX, tax, share entitlement and fees.
- `fx_only` holds the underlying **non-FX operating assumptions and starting Base runway gross DPS fixed**. Currency changes may still affect revenue, costs, debt service, margins, cash and payout through the explicit incremental `economic_fx_bridge`; they are not restricted to reporting or investor translation. Do not quietly add a non-FX operating Bear.
- `combined_bear` starts from that year's Bear runway operating DPS and a coherent stressed FX assumption. Identify which economic FX effects are already in that funded cash bridge and which are incremental. Any additional `economic_gross_dps_delta` must reconcile through cash, funding constraints and the documented payout base; it cannot be a free DPS haircut.
- If `economic_fx_in_runway: true`, `economic_gross_dps_delta` **must be zero**. Otherwise the bridge explains the incremental effect, or the evidenced absence of one. Reuse the existing operating/cash/payout records and a compact incremental calculation; no second full cash-flow forecast or table is required.
- An economic FX delta can be positive or negative. For example, an exporter may benefit from weakness in its cost currency, depending on revenue/debt currencies and hedges. Explain the direction and offsets rather than assuming every depreciation reduces income. Translation-only stress has zero economic delta; an unchanged payout-to-investor FX factor can still accompany a genuine operating cost-currency shock documented in the bridge. Do not combine unrelated most-adverse marginal assumptions as a purported coherent scenario.

Use FX as investor-currency units per source-currency unit, gross DPS per underlying entitled share, fees/hedge cash per quoted security in whole investor currency, and the same quote scale as valuation:

```text
base_net_cash = (base_gross_dps * (1 - withholding_rate)
                 * shares_per_quoted_security * base_fx
                 - investor_fees) / valuation_unit_scale
gross_after_fx = operating_gross_dps + economic_gross_dps_delta
stressed_net_cash = (gross_after_fx * (1 - withholding_rate)
                     * shares_per_quoted_security * stressed_fx
                     - investor_fees + hedge_cash_adjustment) / valuation_unit_scale
delta_cash = stressed_net_cash - base_net_cash
```

`gross_after_fx` cannot be negative; preserve any owner-cash deficit and its funding implications in the bridge rather than inventing a negative dividend. The hedge adjustment is incremental **net cash**, including its evidenced costs, not another multiplier. State the dated tax/fees/hedge basis and any baseline hedge cash already included; count each once. Do not invent a zero fee, hedge or FX shock to make an incomplete stress look assessed.

When growth valuation exists, retain the Base/combined-Bear reconciliation to the same year's `forecast_cash_flows[].fx_to_valuation_currency`. Trace the baseline and stressed receipts to the existing runway plus the incremental economic-FX bridge. If stressed cash is used in a valuation sensitivity, convert funded `gross_after_fx` once; discounted PV uses that already converted cash and its dated cash fraction, **not a second FX multiplier**. Do not count an economic FX effect both in the runway and as an incremental delta, or charge the same hedge cost or modeled FX downside again as an unexplained risk premium.

If material FX/tax/hedge support is unavailable, use `not_assessed`, no fabricated stress rows, diagnostic conclusions and no Strong Buy/Core income. `not_material` needs affirmative economic-exposure evidence and identified currencies, not merely missing observations.

## 7. Income-Driver Tags

Provide one or two dominant `income_drivers` with `driver`, `exposure_direction`, `horizon`, `transmission` and `evidence`. Allowed driver tags are:

```text
oil_gas_prices, freight_rates, credit_losses_and_spreads, long_term_rates,
regulated_tariffs, property_income, patent_product_cycle, consumer_demand,
contracted_volumes, other, not_assessed
```

`exposure_direction` is `higher_supports_income`, `higher_pressures_income`, `mixed` or `unknown`. Explain how the driver changes recurring owner cash, capital uses and payout over the stated horizon; a ticker's sector label alone is insufficient. Define an `other` driver in the transmission text. If unknown, use `not_assessed`/`unknown` with the missing evidence rather than selecting a convenient tag.

These tags are descriptive, not invented numerical weights or correlations. Security tagging and security-level cash safety do **not** require a personal holdings export. Quantifying portfolio concentration or shared-driver exposure does require actual holdings, exposure data and applicable constraints under `portfolio-context.md`; two different sector names do not prove diversification.
