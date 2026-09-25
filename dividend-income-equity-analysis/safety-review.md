# Safety Review

Apply `report-language.md` in the standalone safety bundle as well: reader-facing reports use Chinese by default, while JSON keys/enums and source identifiers remain unchanged.

Use `mode: safety_review` in schema **3.0** for a light, read-only review of a new disclosure against a dated security-level cash/capital baseline. Existing 2.4/2.5 reviews remain readable without conversion. New 3.0 reviews include `evidence_recovery` and Chinese `report_output`, but never the Full Analysis `decision`, scorecard or entry plan. It answers **whether the evidence for dividend safety changed**, not what price to pay or how much to trade. It is distinct from Screen Mode, Full Analysis and a focused normalization audit.

This file is the canonical light-task contract. Use `data-conventions.md`, the cash/coverage definitions in `business-fundamentals.md`, `sector-fcf-proxies.md` and relevant withholding/settlement rules as supporting definitions only; reading them does not require their Full Analysis forecasts. The cross-task minimum matrix is in `analysis-quality.md`.

## 1. Scope and Minimal Inputs

Start from the new result, payout notice, refinancing/capital event or operating disclosure and the prior review/source actually available. A quarterly update does not automatically justify a new five-year forecast or terminal assumption.

The JSON envelope contains only:

```text
mode: safety_review
schema_version: "3.0"
company, ticker, exchange, as_of_date
sources[]
review
controller_risk: optional, when relevant
```

Do not add a new forecast, `buy_zone`, N/B, growth/finite-life valuation, price target, score, grade, portfolio role or sized trade. The optional controller record follows `analysis-quality.md` and `schema.json`; load its definition when needed without inheriting the other full-only records. No complete personal holdings export is required to assess a security's cash safety.

Record `previous_review_date` and `previous_reference` together; both are null if there is no usable sourced baseline. State `event_date`, `event_source`, the analysis cutoff and `period_basis`. Sources must be available by the cutoff; a prior safety label without its cash/capital basis is not a comparable baseline.

## 2. Comparable Cash and Capital Deltas

`review.metrics` must include all five named records below, even when values are unavailable. Each contains nullable `before`/`after`, `unit` and `source`; do not omit a metric key to hide a missing value:

| Metric | Required interpretation |
|---|---|
| `recurring_fad` | Owner cash/eligible sector capital proxy after remaining growth and mandatory uses, deducted once |
| `cash_dividends` | Policy-relevant cash-paid dividends for the matching period and owner perimeter |
| `actual_capacity` | Actual distribution capacity after exceptional cash uses and explicitly available excess cash; not gross consolidated cash |
| `liquidity` | Accessible liquidity after restrictions and committed uses, with scope/date identified |
| `capital_headroom` | **Signed surplus above the applicable disclosed minimum**: measured capital minus its regulatory/debt/covenant requirement, on matching units, date and perimeter; not a raw CET1 or solvency ratio |

Explain baseline/current financial periods, fiscal or rolling-period treatment, owner perimeter, currency, unit scales, restatements and payment timing. Reconcile like for like before attributing a change. Annual versus interim amounts, declared versus paid dividends, and different subsidiary cash perimeters are not directly comparable. Keep reported, estimated and missing quantities distinct:

- `reported_reconciled`: reported cash/capital data reconciles to the review measures.
- `estimated_reconciled`: explicit bounded estimates reconcile to operating, cash/capital and payout evidence; identify assumptions.
- `insufficient`: critical current cash/capital evidence cannot support the bridge; leave unsupported capacity figures null.

These are `cash_evidence_status` values, not safety ratings. OPAT, earnings, embedded value or a solvency percentage alone is **not insurer cash**. Use the sector's capital-generation/remittance bridge. Do not count restricted subsidiary cash, debt proceeds or asset-sale funding as recurring FAD.

For current-period values on one compatible unit and perimeter:

```text
recurring_coverage = metrics.recurring_fad.after / metrics.cash_dividends.after
actual_coverage = metrics.actual_capacity.after / metrics.cash_dividends.after
funding_gap = max(0, metrics.cash_dividends.after - metrics.actual_capacity.after)
```

Compute ratios only with supported numerators and a positive dividend denominator. Zero or missing dividends do not imply infinite coverage or a safety pass. Missing capacity makes the affected ratios/gap unavailable, not zero. A sourced zero cash payment can still be shown as a fact; explain what cannot be concluded from that period.

For scrip, record the same-period `full_cash_entitlement` and `entitlement_source` separately from actual cash paid. Compute `recurring_entitlement_coverage = recurring_fad / full_cash_entitlement` for a supported positive denominator and `all_cash_funding_gap = max(0, full_cash_entitlement - actual_capacity)`. For an ordinary all-cash payment the entitlement normally equals gross cash paid; reconcile timing and any settlement differences. Missing entitlement leaves these metrics null and safety Unclear, not implicitly all-cash. An unfunded cash option requires Weak/Unclear and full reassessment even when low actual cash settlement produces excellent cash-paid ratios.

Reduced issuer cash settlement must not manufacture safety. An investor's market DRIP is not issuer cash retention, and a mandatory stock-only distribution is excluded from cash entitlement/income. Reuse the tax and settlement classification once; a broker's historical deduction does not establish a future tax rate.

Show the material before/after cash, payout, liquidity and capital differences with explanations. A price decline or a higher quoted yield is not a cash-capital improvement.

## 3. Decision and Escalation

`dividend_safety` is `Strong`, `Acceptable`, `Weak` or `Unclear`. Justify it from cash support, actual affordability, liquidity, capital access and payout obligations, not a ratio alone. Missing current **critical capacity** requires `Unclear`; it is neither proof of distress nor evidence that safety is maintained.

A negative current `liquidity` or `capital_headroom` is a funding/capital-buffer breach **even when dividends are cash-covered**. Safety must be `Weak` when the breach is established, or `Unclear` when critical supporting evidence remains unresolved; it cannot be `Strong` or `Acceptable`. Set `requires_full_analysis: true` and identify the breached requirement and remediation evidence in `escalation_reasons`. A nonnegative buffer alone is not a safety pass. For capital ratios, compute the surplus in percentage points over the applicable disclosed minimum, rather than treating the raw ratio as headroom.

| `decision` | Minimum evidence |
|---|---|
| `maintained` | A comparable sourced baseline and current bridge support no material change in safety; state the remaining risks |
| `weakened` | Comparable evidence identifies deterioration and its cash/capital mechanism |
| `strengthened` | Comparable evidence demonstrates improved sustainable support, not just a transient release or higher market yield |
| `not_comparable` | No usable baseline, unmatched periods/perimeters or insufficient evidence to make a directional comparison |

If the baseline is absent or any of the five required metrics has `before: null`, set `decision: not_comparable`, even when a prior review date/reference is known. Do not say “unchanged,” “maintained,” “improved” or “weakened.” A current safety view can still be supported separately if current critical evidence is complete. Missing baseline alone does not prove a new failure or force a trade.

Assess `structural_change`, `veto_status` (`Not triggered` / `Triggered` / `Unclear`) and `requires_full_analysis`. Set `requires_full_analysis: true` and list specific `escalation_reasons` for a structural change, unresolved funding gap, negative liquidity/capital headroom, triggered/unresolved veto, or material cash/capital uncertainty requiring a rebuilt thesis or forecast. A changed payout regime, investment/funding model or remittance constraint cannot be dismissed as one-quarter noise.

Controller concern must run in the correct direction: the listed issuer may fund an unlisted controlling parent. Parent debt/refinancing needs, pledges, state/group ownership, high payout or coincident dates alone do not establish harm. A controller-driven veto needs confirmed material damage to the listed company's funding, necessary investment, liquidity or minority value. Unresolved potentially material harm needs evidence escalation, not a claim of proven extraction.

A supported transient timing update may remain light with `requires_full_analysis: false` when cash, capital and veto checks remain adequately supported; explain why it does not alter sustainable economics. Do not extrapolate five-year cash or a terminal reset from a single quarter. Route persistent/structural changes to the appropriate full reassessment rather than creating new N/B inside the light review.

Escalation is a **research requirement**, not an automatic sell. Set `automatic_trade: false`. Even a confirmed funding failure does not authorize orders, trade sizes or a personalized exit decision. Full Analysis can embed these dated safety checks in Audit Appendix part A12 under `holding-review.md`, without adding a report section.

## 4. Compact Output and Required Record

Use a short conclusion and this table; charts and a presentation appendix are optional:

| 现金／资本指标 | 复检前 | 复检后 | 单位／期间 | 来源／变化说明 |
|---|---:|---:|---|---|
| 经常性可分配现金（FAD） | | | | |
| 同期相关现金股息 | | | | |
| 实际可分配能力 | | | | |
| 可用流动性 | | | | |
| 资本安全余量 | | | | |

The `review` record includes:

```text
previous_review_date / previous_reference: sourced pair or both null
event_date / event_source:
period_basis:
cash_evidence_status: reported_reconciled / estimated_reconciled / insufficient
metrics: recurring_fad, cash_dividends, actual_capacity, liquidity, capital_headroom
recurring_coverage / actual_coverage / funding_gap: computed or null
full_cash_entitlement / entitlement_source:
recurring_entitlement_coverage / all_cash_funding_gap: computed or null
dividend_safety: Strong / Acceptable / Weak / Unclear
decision: maintained / weakened / strengthened / not_comparable
structural_change:
veto_status: Not triggered / Triggered / Unclear
requires_full_analysis:
escalation_reasons[]:
missing_inputs[]:
next_review:
automatic_trade: false
```

`missing_inputs` names the disclosure/metric needed and the conclusion it could change; do not just write “more research.” `next_review` specifies a sourced date or concrete event plus earlier escalation signals. When a future date is unknown, name the event/source to check rather than inventing a reporting date. No review date or escalation rule schedules an automatic trade.
