# Scoring Model

Use the fixed modules below for Full Analysis. Lead with **price-independent quality / 85**, then **income attractiveness / 15**, and show their **combined score / 100 and Grade** as a secondary compatibility measure. Partial evidence must produce a useful **provisional score or range with coverage**, not a whole-report "cannot score" headline. Screen Mode and Safety Review do not use these scores.

Quality is the sum of Modules 2-7; income attractiveness is Module 1. Changing only the share price can change income points, the combined Grade and entry readiness, but not quality points or the underlying business classification. Neither a Grade nor a low price is a buy recommendation.

`scoring.md` is the canonical scoring/range/rating contract. `analysis-quality.md` supplies the compatible local analytical records and material gates, including `quality_assessment`, `portfolio_role_assessment`, controller risk and income-yield spreads; it must not introduce a competing scoring rule.

The main report shows only quality /85, the combined score (a point, or the provisional range with Grade/Grade range and coverage) and Portfolio Role in the Bottom Line status line; module points, candidate bands, weights, overlays, `rating_audit` and override explanations belong to Audit Appendix part A11. All of them are still calculated for every Full Analysis.

## Weights

| Module | Machine ID | Weight |
|---|---|---:|
| Net dividend yield | net_yield | 15 |
| Five-year dividend stability | dividend_stability | 15 |
| Free cash-flow coverage | cash_coverage | 20 |
| Balance-sheet safety | balance_sheet | 15 |
| Management capital-allocation attitude | capital_allocation | 15 |
| Buyback quality | buyback_quality | 10 |
| Three-to-five-year fundamental and dividend visibility | visibility | 10 |

## Reproducible Point Selection

The anchor tables select a band, not an arbitrary score inside it. Number bands from best to worst, starting at 1; the yield module has five bands and the other modules have four. The no-buyback explanatory row is not an extra band.

For each module record the input and period, selected band and reason, and the three checks below in order. Each check is `met`, `not_met` or `unknown`, with specific evidence and exact references to the report's `sources`. Unknown is not evidence of business failure: it earns no refinement bonus, is disclosed, and is not separately deducted again.

```text
k = number of checks marked met, from 0 to 3
raw_score = band_floor + floor((band_ceiling - band_floor) x k / 3)
final_score = min(raw_score, applicable_module_cap)
```

These are integer points; do not round a midpoint, invent an extra adjustment, or choose a point to obtain a preferred Grade. The cap defaults to the module weight. Apply the smallest relevant explicit cap below once and identify its rule; do not subtract it as a second penalty.

| Module | Check 1 | Check 2 | Check 3 |
|---|---|---|---|
| net_yield | Evidenced full-year forward net cash is at least N | Credible B / current price meets r_high | N / current price meets the independently derived R_low |
| dividend_stability | Ordinary cash was paid on the disclosed schedule throughout the available five-year window | Real ordinary DPS did not decline over that window, using sourced inflation | Stability survived a documented adverse operating period without extraordinary funding |
| cash_coverage | All modeled years 1-3 cover the full cash-equivalent dividend from recurring FAD and actual capacity | The five-year worst actual cash coverage is at least 1.0x | A disclosed liquidity/capital buffer covers the modeled stress without new external funding |
| balance_sheet | Liquidity covers the next 24 months' maturities and committed cash uses | Bear cash/capital metrics remain within disclosed covenants or regulatory minima | The funded three-to-five-year plan does not require uncommitted refinancing or equity |
| capital_allocation | Payout decisions match the published policy or explain deviations | Reinvestment and debt reduction have an evidenced per-share rationale | Acquisition/issuance decisions have a documented record of protecting continuing owners |
| buyback_quality | Repurchases, issuance and scrip reconcile to continuing-owner share counts | Repurchase prices are below a contemporaneous conservative value, or abstention above value is documented | Capital returns preserve the funded investment plan and stress liquidity |
| visibility | Years 1-3 operating-to-cash-to-DPS bridges reconcile with dated sources | Years 4-5 are bounded, funded extensions, not mechanical CAGR plugs | Prior milestones or contracted outcomes corroborate management's delivery assumptions |

The band measures the primary condition; the checks refine durability, stress support or corroboration within that band. For example, coverage band 2 is 12-16: two met checks give `12 + floor(4 x 2 / 3) = 14`, not an unexplained 15. All three met checks give 16.

Missing refinement evidence alone does not make an otherwise supported band unassessable. Use the recovery order below before leaving a primary band unknown.

## Recovery-First Scoring, Rubric 2

Do the research rather than require the user to supply every model input. Unless the task is explicitly packet-only, retrieve the latest applicable filing and relevant notes, then attempt a reconciled derivation or bounded estimate. Follow `data-conventions.md` for cutoff, source access and materiality. An unfinished research model is not evidence of an unforecastable business.

| Evidence outcome | Module assessment | Output |
|---|---|---|
| Primary band can be supported by disclosed facts or a defensible derivation | `assessed` | Apply the existing point formula; identify `evidence_basis: reported / reconstructed / estimated` |
| Evidence limits the primary condition to one or more bands but does not support an ordinary exact assessment | `bounded` | Explain the metric interval or qualitative alternatives; calculate a provisional point range |
| Neither a band nor narrower evidence-backed bounds can be established after recovery | `not_assessable` | Keep that module's point null, record recovery and its remaining possible contribution; retain every other module |

For a bounded module, store `bounds.metric_basis`, `metric_low`, `metric_high`, ordered contiguous `bands`, `derivation`, `limitations` and declared `source_refs`. Qualitative bounds use null metric endpoints. Quantitative bands must cover the complete metric interval, including any threshold it crosses. Bounds are not freehand score ranges: the fixed bands, checks and caps determine them.

```text
k = met checks; u = unknown checks
module_low = min over candidate bands of min(score_points(band, k), cap)
module_high = max over candidate bands of min(score_points(band, k + u), cap)
```

The upper endpoint represents resolution of unknown refinements, not awarded points. A known `not_met` check never earns a bonus at either endpoint. An assessed module with unknown refinements keeps its existing conservative point result; only a genuinely bounded primary assessment uses the range rule.

For an entirely unassessable module, its mathematical contribution is `[0, current_module_cap]`. This **does not assign zero to the company**: the full missing weight remains disclosed. Named caps still apply and must be explained, including the Low/Not Forecastable income cap. No midpoint, arbitrary "industry average", removed weight, or partial-score rescaling is allowed.

An unassessable module requires `evidence_basis: unknown` and a compact `recovery` record: what was actually inspected/attempted, `outcome: not_found / not_in_packet / tool_unavailable / not_reconcilable`, and the next source needed. Do not claim a retrieval succeeded when it did not, or that the issuer does not disclose something merely absent from the packet.

### Aggregate and Headline Contract

Schema **3.0**, `rubric_version: "2"`, retains the seven modules and adds `scorecard.summary`:

- `module_ranges`, `quality_range`, `income_range` and `score_range`: sum lower and upper endpoints separately, with fixed denominators 85, 15 and 100.
- `assessed_points / assessed_weight`: the subtotal of exact assessed modules only, including any explicitly estimated point assessments. It is not a new /100 score.
- `bounded_weight`, `missing_weight` and `evidence_coverage_pct`: exact plus bounded weights count as covered; unknown modules do not. Also show `quality_coverage_pct` and `income_coverage_pct`. Coverage measures research coverage, **not confidence, business quality or probability of success**.
- `status: complete` for all exact modules without estimated primary evidence; `provisional` when any primary estimate, bounded module or missing module remains; `insufficient` only when no module is covered.
- `range_kind: rubric_bounds`: these are scoring-method bounds, not confidence intervals, return forecasts or probability distributions.
- `grade_range` and `quality_rating_range`: apply the fixed thresholds to both endpoints and the explicit Grade cap where applicable.

Overall covered weight is already an integer percentage of 100. Calculate `quality_coverage_pct = round(covered_quality_weight / 85 x 100, 2)`; income coverage is 0 or 100. These are the documented presentation-rounded coverage fields, not rounded financial-model inputs.

Keep a point in `quality_score_85`, `income_score_15` or `score_100` whenever its interval collapses to one value, including a uniquely capped provisional assessment. Otherwise leave the scalar null **and print the interval**, not "Not Assessed". A single Grade or Dividend Quality label is permitted when both endpoints give the same label, explicitly provisional where applicable. Across Grade bands use the Grade range and null scalar Grade; across quality bands use the quality-label range and scalar `Unclear`, not a pessimistic substitute.

The executive fields `score_status`, `score_range`, `quality_score_range`, `score_coverage_pct` and `grade_range` must match the scorecard. If all evidence is absent, say insufficient evidence with coverage 0%; `[0,100]` is an uninformative bound, not a company score or a reason to rank it last.

Example: known points **71 across 90 weight**, with only buyback quality missing, yield **71-81/100, Grade B (provisional), coverage 90%**. Quality remains **57-67/85, Medium**, not a blank or 71/90 scaled to 100. If only income is missing, **62/85 quality** survives and the combined interval is **62-77/100 (C-B)** under otherwise unchanged uncapped conditions.

Legacy schema 2.3/2.4 retains its original behavior; rubric 1 still nulls totals/Grade for missing modules. Schema 2.5 retains rubric 2 without retroactive recovery/output requirements. New schema 3.0 retains the same rubric-2 arithmetic and always prints numeric bounds, Grade bounds and coverage, even at zero coverage (uninformative method bounds, not a zero company score). Do not use the legacy null-total display rule in new reports or relabel old discretionary points as audited rubric-2 scores.

For cash coverage only, `peak_cycle_only` and `externally_funded` can override an apparently stronger numeric band. Record `band_override` with the rule, evidence and sources: each candidate band is no better than 3 or 4 respectively, never better than its metric band. Apply the override before points/caps and remove duplicate resulting candidates. An unresolved material cash/capital bridge remains unknown, not an invented adverse override.

The six modules other than Net dividend yield retain **85** total weight. The local `quality_assessment` is a projection of those same scorecard modules and summary, not a second scoring system. Its `score_85` equals `scorecard.quality_score_85`; a non-collapsed interval stays null in the scalar and is displayed with `scorecard.summary.quality_range` and quality coverage. Keep the 15-point income module separate and aggregate its bounds under the same rubric-2 rules. Never upscale a partial score to 85 or 100.

## Anchor Rules

### 1. Net Dividend Yield, 15 points

Use credible normalized net yield in the investor's stated tax and currency context. Exclude one-off special dividends and economic capital recovery from recurring income. These bands measure income appeal within the 100-point framework, not business quality or expected total return; a falling share price must not mechanically improve the investment conclusion.

This module is **not** part of `quality_assessment`. With fundamentals and constraints fixed, a lower price can improve its income points and entry appeal, but not quality points or the assessed security role.

| Recurring or normalized net yield | Points |
|---|---:|
| >= 7% | 13-15 |
| >= 5% and < 7% | 10-12 |
| >= 3.5% and < 5% | 6-9 |
| >= 2% and < 3.5% | 3-5 |
| < 2% | 0-2 |

Apply these safeguards before summing the score:

- Award 13-15 only with evidence-backed normalization, at least Medium Forecast Confidence, at least Acceptable Dividend Safety, and value-trap veto Not triggered. Explain the yield spread versus the dated opportunity-cost comparison in `buy-zone.md`.
- Cap this module at 9 / 15 when Forecast Confidence is Low or Not Forecastable, or N/B uses a historical/fundamental fallback; cap it at 5 / 15 when Dividend Safety is Weak or the veto is Triggered. State the raw band and the applied cap.
- If N is not yet established but ordinary recurring declarations, current price and applicable tax/FX/cash treatment are supported, use a **bounded `recurring_income_proxy`**, capped at 9/15 (or a lower applicable cap). Derive its range from documented ordinary payments or the current declared ordinary run rate, excluding specials and unnormalized cycle peaks. Label it current recurring income, not sustainable N, a forward promise or a buy price. It does not need a complete valuation ladder, B or the user's personal income target. Prefer supported normalization when already available; do not cherry-pick a different income basis.
- Unknown N/B refinements remain unknown. A proxy must not populate normalized-yield fields, establish N/B, upgrade safety or reopen a suspended entry. Material unresolved tax/currency/cash election still makes this module unassessable; a high TTM yield cannot solve those gaps.
- Fixed bands are a consistent scoring convention. Their interpretation must reflect current rates and company risk; do not change weights, silently alter thresholds or award additional points above 15 for an extreme yield.

### 2. Five-Year Dividend Stability, 15 points

| Pattern | Points |
|---|---:|
| Stable or growing ordinary DPS, no cut | 12-15 |
| Mostly stable with mild cyclicality | 8-11 |
| Volatile but still paid most years | 4-7 |
| Cut, suspended, or highly unstable | 0-3 |

Assess comparable **nominal** ordinary dividend stability, adjusting the entitlement basis for corporate actions. Keep `real_income` and its consumption-basket purchasing-power trend separate; do not double count the same nominal pattern or automatically penalize cash safety because inflation erodes real income.

### 3. Free Cash-Flow Coverage, 20 points

Use the recurring FAD coverage contract in `business-fundamentals.md`: three-year cumulative recurring FAD divided by matching cash dividends paid, accompanied by the five-year worst recurring and actual cash-coverage years. This is not an arithmetic mean of annual ratios. Apply the same owner perimeter and the sector proxy in `sector-fcf-proxies.md`.

For fixed/progressive policies use ordinary cash dividends; for variable/cycle-linked policies use total recurring/variable cash dividends. Keep exceptional capital returns separate. Do not score peak-cycle cash, asset sales, excess capital releases or unsupported OPAT proxies as recurring coverage.

| Recurring FAD / relevant cash dividend | Points |
|---|---:|
| >= 1.5x on normalized basis | 17-20 |
| >= 1.0x and < 1.5x on normalized basis | 12-16 |
| >= 0.7x and < 1.0x or peak-cycle-only coverage | 6-11 |
| < 0.7x, debt-funded, equity-funded, or asset-sale-funded payout | 0-5 |

If the standard three-year aggregate is unavailable but a shorter comparable history or conservative after-investment sector proxy can be reconciled, use bounded `reconciled_cash_proxy` scoring, capped at **16/20**, with the actual window, owner scope, adjustments and sensitivity. Do not fabricate a third year or fill `three_year_recurring_coverage` with a different measure. An evidenced interval around an available standard aggregate uses `three_year_recurring_coverage` instead; do not discard that aggregate to cherry-pick a favorable proxy. Missing future forecasts do not erase reconciled historical coverage; forecast funding checks simply remain unknown when unavailable.

When scrip retains issuer cash, also show coverage of the full cash-equivalent entitlement; do not grant a better safety band solely from fewer holders electing cash. Anchor points to the aggregate, then explain the worst-year and funding stress. Do not grant the top band when recurring shortfalls are unresolved, capital/remittance restrictions are unknown, or a material cash bridge is estimated without reconciliation. An unreconciled company FCF or OPAT number cannot become a "reconciled proxy" by changing its label. If the material bridge remains insufficient, preserve an unknown coverage contribution and a provisional aggregate score rather than deleting all scores.

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

Use `controller_risk` for transfers from the listed company to its ultimate controller, not just subsidiary remittances into a listed holding company. Parent cash demand alone is not adverse allocation evidence; confirmed material harm and unresolved potentially material exposure follow the canonical safety/veto gates.

### 6. Buyback Quality, 10 points

| Condition | Points |
|---|---:|
| Real share-count reduction at reasonable valuation, or evidenced discipline in avoiding uneconomic buybacks with stable per-share ownership | 8-10 |
| Neutral or small buyback / no-buyback policy with limited dilution and no demonstrated value destruction | 5-7 |
| Cosmetic buyback offset by issuance or scrip / DRIP dilution | 2-4 |
| Buyback that creates financing stress or demonstrably destroys continuing shareholders' per-share value | 0-1 |
| No buyback program | Score the documented per-share outcome and rationale using the same bands; absence alone is not a fixed deduction |

Keep the module at 10 points and retain `Buyback Quality: Not Applicable` when no buyback program exists. The score measures demonstrated per-share capital discipline: 8-10 requires evidence such as a stable share count, avoidance of repurchases above conservative value, and a credible funding / capital-allocation rationale; do not award a maximum merely because there is no program. Recover relevant evidence and use bounded alternatives where supportable before marking this module unassessable. Do not redistribute the weight.

Reconcile repurchases with issuance, treasury-share reissuance, compensation and scrip over comparable periods. Distinguish issuer-created dilution from an investor's open-market DRIP. Consider debt financing together with leverage, liquidity and purchase valuation; debt financing alone does not establish value destruction. Avoid double counting: Module 5 assesses allocation and funding decisions, while this module assesses repurchase valuation and continuing owners' per-share outcome.

Historical repurchase prices and documented execution discipline are evidence about allocation. Today's quote alone cannot retrospectively improve this quality module when the underlying evidence is unchanged.

### 7. Three-to-Five-Year Fundamental and Dividend Visibility, 10 points

| Condition | Points |
|---|---:|
| High visibility: operating drivers, three-year FCF/DPS and the year-four/five development path are evidenced, funded and reconcilable | 8-10 |
| Moderate visibility: capacity is estimable but macro, pricing, credit, execution, capex, or dilution risk remains | 5-7 |
| Low visibility: wide scenarios, high cyclicality, uncertain policy, or weak reconciliation | 2-4 |
| Demonstrated cash impairment, policy failure or structurally unpredictable cash defeats a responsible dividend outlook | 0-1 |

Do not award more than 4 points when future DPS is illustrative rather than evidence-backed.

Do not upgrade visibility merely because the model contains five numerical years. Conversely, **no completed five-year spreadsheet, no management DPS forecast, or no exact future record-date shares is not a 0-1 point business condition**. Use operating/contract/policy evidence for the primary band or bounded alternatives; missing model details affect refinements and coverage. If no band can be supported, leave this module unknown rather than assigning 1.

An assessed lowest-band visibility score in rubric 2 requires `adverse_evidence`: a sourced `demonstrated_cash_impairment`, `policy_failure` or `structurally_unpredictable_cash` condition and its specific consequence. The validator checks that record, not the source's truth. Uncertain later years carry limitations and milestones; retain the separate Three-Year Dividend Outlook and forecast-confidence labels.

## Evidence and Action Overlays

- Missing scoring inputs produce the provisional point/range and coverage contract above, not a report-wide scoring veto. Keep scalar fields null only when their range does not collapse; keep stable provisional labels where the entire interval supports them. Restrict entry or role only when the same gap independently fails a named material gate. Neither a score range nor a numerical proxy clears a cash/capital/tax gate.
- A Triggered value-trap veto overrides any numeric score: actionable buy zones are suspended and the security cannot be Core income. An Unclear veto also suspends actionable buy zones and caps the Portfolio Role at Watchlist; missing evidence does not mean the veto passed.
- Low Forecast Confidence, a fallback N / B, provisional yield calibration or an unassessed capital-risk / total-return cross-check prevents actionable entry and a Core income classification. Use diagnostic income sensitivities and identify the exact evidence needed. Not Forecastable suspends ordinary buy zones.
- A Strong Buy action requires High Forecast Confidence, Strong Dividend Safety, value-trap veto Not triggered and every action gate in `buy-zone.md`. Medium confidence permits at most gradual accumulation after the other gates pass. A price inside the Bear high-end cash-yield boundary is not sufficient; ordinary band names describe cash income and never assign actions.
- Dividend Safety Weak or Unclear prevents Core income. Income yield does not compensate for an unquantified risk of permanent loss of capital.
- Apply the shared entry gates in `buy-zone.md`: unverified withholding/cash election, non-evidence-backed ordinary DPS or failed/unassessed hard-income eligibility restrict entry to diagnostic use. Material safety or unresolved mandate evidence prevents supported Core suitability; report the limitation as Watchlist or Avoid where applicable. Keep the price-specific income result separate from security role, rather than mechanically upgrading the role when price falls. A High label cannot override contradictory source fields.
- Apply the controller and FX evidence gates in `analysis-quality.md`. Confirmed material controller harm triggers the veto; unknown potentially material harm or unsupported material FX limits conclusions to diagnosis and prevents Strong Buy/Core income, without declaring proven distress.

These overlays do not create new module weights. Report quality /85 and any legacy mixed /100 separately from confidence, safety, valuation eligibility and the final Portfolio Role; a high score cannot cancel a failed gate. `portfolio_role_assessment` records the quality/safety/constraints rationale and `price_alone_changes_role: false`.

Bounded analyst estimates can support Medium Forecast Confidence when their operating, investment, cash, tax, capital and payout bridges reconcile; exact project-by-project management ROIC disclosures are not mandatory for `direct_operating_to_dps`. Identify ranges and limitations. Unsupported material funding, remittance or terminal facts remain gate failures and cannot be cured with a higher risk premium, a lower entry price or a larger safety discount. Do not charge the same residual uncertainty again in multiple overlays.

## Score and Valuation Separation

Weights remain 85 quality points plus 15 income points. Do not map either score or Grade mechanically to risk-premium or discount-rate bands. The combined score includes price, and even the quality score is not a substitute for the price-independent business, capital, policy and evidence assessment in `buy-zone.md`. A lower income score can coexist with credible growth value; it does not waive an explicit investor cash-income minimum.

Keep `income_assessment` and its optional `required_yield_spread` separate: normalized N/P minus the independent required yields is a **price-sensitive** income comparison, not another quality score. A lower income score can coexist with credible growth value; it does not waive an explicit investor cash-income minimum.

Core income needs supported quality, safety, applicable evidence/action gates and the investor mandate. There is no automatic Score-to-Role mapping or quality-threshold-to-role rule. Holding fundamentals, safety and constraints fixed, a price decline changes entry attractiveness, not security quality or role.

## Structural Decline Overlay

If Fundamental Trend is `Structural Decline`, apply these limits after assessing the supported quality components and any complete unadjusted legacy score:

- Final legacy Grade cannot exceed C.
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

- Quality score /85 with component evidence or Not Assessed.
- Unadjusted legacy mixed score /100, when complete.
- Overlay-adjusted legacy Grade, when assessable.
- Final Portfolio Role.
- Structural Decline cap applied: Yes / No.
- Harvest / Managed Runoff Exception applied: Yes / No.
- Valuation mode: suspended / finite_life_harvest.
- Expected cash-harvest horizon when applicable.

## Legacy Score Bands

| Combined Score | Unadjusted Grade |
|---:|---|
| 85-100 | A |
| 70-84 | B |
| 55-69 | C |
| 40-54 | D |
| Below 40 | E |

Compute the Grade from the exact sum or both provisional endpoints, not an impression. Structural Decline applies the explicit C cap to both endpoints; otherwise final Grade follows the score. A range entirely within B supports B (provisional), not a forced null Grade. Do not silently apply additional pessimistic haircuts: financial weaknesses belong in their modules, evidence limitations in confidence/coverage, and failed entry conditions in the entry plan. Portfolio Role is selected separately.

## Transparent Rating Rules

Every required rating has a `rating_audit` record: `label`, `rule`, `supporting_evidence`, `source_refs`, `upgrade_trigger` and `downgrade_trigger`. The label must match the report. Explain the binding reason for the present rating and an observable condition that changes it; "conservative judgment" or "monitor risks" alone is not a rule or trigger.

| Rating | Decision rule |
|---|---|
| Dividend Quality | High at quality >= 68/85; Medium at 51-67; Low below 51. Apply to both quality-range endpoints: keep a matching label, otherwise Unclear with the label range. Missing data is not itself Low. These are descriptive bands, not entry gates. |
| Dividend Safety | Strong needs normalized aggregate coverage >= 1.5x, funded Bear/Base cash and verified capital access with resolved actual shortfalls. Acceptable needs >= 1.0x and a funded Base policy with bounded, disclosed stress. Weak means evidenced recurring impairment or unresolved funding stress; Unclear means the material cash/capital evidence cannot be established. A high yield cannot upgrade safety. |
| Withholding Efficiency | On a supported rate, High at <= 10%, Medium at > 10% and <= 20%, Low above 20%; Unclear when the rate or applicable basis is unsupported. These labels describe tax leakage, not dividend safety; show material fees separately. |
| Buyback Quality | Good for the first band, Neutral for the second, Poor for the third/fourth. In rubric 2, use Unclear when candidate bands cross these labels or the primary evidence is unknown, and state the possible labels in the audit. No program remains Not Applicable while documented per-share discipline is scored. |
| Three-Year Dividend Outlook | Grow or Decline when the funded Base year-3 net DPS is respectively more than 5% above or below year 1; otherwise Stable. High Uncertainty when that comparison is unsupported or a known intervening reset makes the endpoint misleading. Show the actual change and Bear path, not just the label. |
| Forecast Confidence | Use `business-fundamentals.md` by horizon. High requires corroborated drivers and cash/capital/policy/shares; bounded, reconciled analyst estimates can be Medium. Cyclicality or absent project-level ROIC alone does not force Low. Material unbounded assumptions produce Low or Not Forecastable, with the affected link named. |
| Fundamental Trend | Tie Structural Growth/Stable/Mature/Cyclical Recovery/Cyclical Peak/Structural Decline/Transformation/High Uncertainty to the operating history and five-year drivers. A price fall or high yield is not a trend classification. |
| Portfolio Role | Core income requires durable ordinary cash, Strong/Acceptable safety and no material evidence/entry veto; Cyclical income describes funded but cycle-linked cash; Opportunistic describes an evidenced non-core/event/runoff case. Watchlist is for a specified unresolved thesis/entry condition; Avoid is for evidenced incompatibility or impairment. Missing position size blocks sizing, not security-level research. |

The safety audit names its normalized coverage window and distinguishes historical evidence from a supported forward cash/capital assessment. A short history may support bounded proxy scoring or leave that module unknown without making a separately reconciled forward policy unsafe. Do not use missing history as an automatic action veto or substitute an unsupported forward improvement.

For qualitative labels the validator checks completeness, source-reference membership and agreement with displayed labels, not the truth of the evidence. State this limit; transparent reasoning is not mechanical proof of safety.

Historical comparisons must identify score type, framework version and evidence date. Do not compare an old mixed /100 score directly with price-independent quality /85, or silently reinterpret discretionary legacy points as rubric-2 results.

## Required Ratings

Always output:

- Quality Assessment: matching scorecard component points, quality /85 point or range and evidence coverage
- Current-price income fit / valuation and optional normalized-yield spread, separately from quality
- Combined score /100 and Grade point or range, with provisional status where applicable
- Portfolio Role Assessment: quality_safety_and_constraints, evidenced rationale, price_alone_changes_role false
- Dividend Quality: High / Medium / Low / Unclear
- Dividend Safety: Strong / Acceptable / Weak / Unclear
- Withholding Efficiency: High / Medium / Low / Unclear
- Buyback Quality: Good / Neutral / Poor / Not Applicable / Unclear (Unclear is new in schema 3.0)
- Three-Year Dividend Outlook: Grow / Stable / Decline / High Uncertainty
- Portfolio Role: Core income / Cyclical income / Opportunistic / Watchlist / Avoid
- Fundamental Trend: Structural Growth / Stable / Mature / Cyclical Recovery / Cyclical Peak / Structural Decline / Transformation / High Uncertainty
- Forecast Confidence: High / Medium / Low / Not Forecastable
- Structural Decline cap applied: Yes / No
- Harvest / Managed Runoff Exception applied: Yes / No
- Valuation mode: ordinary_yield_based / total_return_based / finite_life_harvest / suspended
- Holding review action and missing portfolio inputs, following `holding-review.md`
