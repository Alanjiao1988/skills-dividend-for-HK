# Portfolio Income Target Context

Read this module only when reusing an established portfolio income target or assessing an absolute-cash requirement. A current explicit user instruction takes precedence. Do not create a portfolio, request a full holdings export, or invent a minimum yield to complete a screen.

## Source and Applicability

`target_basis: portfolio_target` means a previously established user objective is being reused. Its source may be an identifiable earlier user message or a user-maintained file; persistent storage is optional. Keep the target percentage and hard-minimum/preference policy in the existing target fields.

Record `portfolio_context` inside `screening_parameters` in Screen Mode, or inside `income_assessment.target` in Full Analysis:

| Field | Required meaning |
|---|---|
| `source` | Locate the user instruction or maintained objective; an analyst's desired yield is not a source. |
| `confirmed_on` | Date on which the user established or last confirmed the objective. |
| `valid_until` | User-defined last applicable date, or null if none was specified. Do not invent an expiry period. |
| `account_scope` | Account or portfolio to which the instruction applies; do not infer account identity from a stock's exchange. |
| `investor_tax_basis` | Investor/channel and after-tax income convention attached to the objective. |
| `income_currency` | Three-letter income reporting currency. Convert compared cash consistently. |
| `income_period` | The requested measurement period, such as next full-year cash receipts. |
| `applicability_confirmed` | True only when the source and current task establish that the objective applies. |
| `applicability_evidence` | Explain that link and whether any subsequent instruction, mandate or investor change supersedes it. |

The confirmation date cannot be later than the analysis date. A stated expiry must not precede confirmation or the analysis date. A changed mandate, account, investor/channel, currency or income period requires reconsidering applicability even when `valid_until` is null. Calendar checks do not establish substantive applicability by themselves.

If applicability is unclear, expired or contradicted, use `target_basis: not_assessed`, null target and `target_policy: not_assessed`; explain the missing context and continue research that does not depend on it. Ask a focused question only if the user's requested decision needs that target. Do not downgrade a preference into a hard minimum or silently transfer one account's objective to another. A new current explicit target uses `user_explicit`; omit `portfolio_context` or set it to null.

## Inputs Proportional to the Decision

A percentage-yield screen does not require holdings, position sizes or account balances. Absolute annual cash income requires the relevant capital/holdings and receipt timing. Position sizing, concentration and switching decisions additionally use `holding-review.md`. Missing those inputs limits the affected conclusion rather than the whole research task.

## Contract Version

Schema 2.2 introduced provenance requirements only when `target_basis` is `portfolio_target`; 2.3 retains them and adds the normalization evidence and cash/action safeguards described in the root README. Existing `user_explicit` and `not_assessed` target shapes remain usable. When migrating a 2.1 or 2.2 report, supply genuine portfolio provenance if that source is used and reconcile the other 2.3 requirements before updating the version; if provenance is unavailable, reassess the target instead of manufacturing metadata.
