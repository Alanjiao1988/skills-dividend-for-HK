# Data and Evidence Conventions

Read this file in either mode before calculating yield. Screen Mode needs only the inputs used in its compact output; it does not require a full forecast.

## Comparable Inputs

- Record the research cut-off, exchange, price timestamp and currency, financial period, publication date, unit scale, and source. A filing published after the cut-off is unavailable to a historical analysis even if it describes an earlier year.
- Keep fiscal-year attributed dividends, trailing paid cash, declared future entitlements, and forecast dividends separate. Choose and label one trailing-event convention consistently; never add a proposed final dividend to paid TTM cash and call the result TTM.
- Separate ordinary, policy-variable, special, capital-return, and mandatory-share distributions. A repeated variable payout can be relevant income, but needs cycle normalization in Full Analysis. Do not annualize one quarter's unusually large payment without support.
- Convert dividend cash into the price currency before dividing. State FX direction, date, source, and whether the rate is the actual payment conversion or an estimate. For a total-return scenario, convert the initial price, each future distribution, and exit value into the investor's reporting currency using explicit assumptions.
- Adjust DPS and share counts consistently for splits, consolidations, bonus issues, rights issues, and ADR ratios. Current prices need current share units. Never divide historical DPS by a dividend-reinvestment-adjusted price series; that can double-count dividends. Historical entry yields use prices and information available at that date.
- Separate all-class company equity value from the market value of the listed share class. For A/H issuers, HK price times all A+H shares is a hypothetical H-price-equivalent value, not observed aggregate market capitalization. Match EPS, book value, shares, currency and numerator ownership in every valuation ratio.
- Null means unavailable, not zero. An omitted dividend announcement is not proof of zero DPS; a negative or zero profit denominator makes a conventional payout ratio not meaningful. Explain the economic loss and cash funding instead.

## Evidence and Arithmetic

Use official filings and issuer distribution notices for material inputs. Third-party data is a cross-check: two websites copying the same feed are not independent confirmation. A single authoritative disclosure can be used with its limitation stated; do not invent a second source. Reconcile conflicts in period, restatement, currency, corporate actions and distribution type before drawing a conclusion.

For each material derived result, preserve inputs, formula, units, and source references. Recompute yield, coverage, payout, share bridges, valuation boundaries and total returns with an available calculator or code. Cross-check statement subtotals and the model's cash roll-forward; arithmetic precision does not cure uncertain assumptions. Round prices and yield ranges to the quality of the evidence.

Missing critical dividend, tax, cash-access, refinancing, or share data produces an explicit unknown or range and affects confidence. It must not silently turn into 0% tax, full cash availability, clean veto status, or a favorable score. JSON required fields may contain null or empty histories with an explanation when data does not exist; do not fabricate five years of observations.

## Focused Normalization Audits

When the user asks to audit a proposed normalized DPS, N/B calculation or its action label, answer that focused question rather than inventing an 18-section company report. This is a supporting audit, not a new valuation mode. Ordinary Screen Mode does not calculate N or require this audit.

Use this compact output contract even when the answer must be concise: **arithmetic conclusion; evidence/action conclusion; the four-row evidence checklist below**. Do not stop at "a dividend bridge is needed." Include all four links, distinguish facts already supplied from missing evidence, and name the missing input and disclosure needed to resolve it. Do not mark every link missing merely because one fails.

| Evidence link | Specific input to assess | Where to verify it |
|---|---|---|
| Operating cash (`operating_cash`) | Volume/pricing, margins, working capital and cash conversion supporting normalized owner cash | Segment/operating disclosures, guidance and cash-flow notes; sector equivalent when applicable |
| Funding capacity (`funding_capacity`) | Maintenance/growth investment, debt/regulatory uses and remittability leading to recurring FAD | Capex commitments, maturities, capital/remittance and parent-cash disclosures |
| Payout policy (`payout_policy`) | Policy percentage or fixed DPS, its exact earnings/cash base and funding constraint | Dividend-policy announcement, results payout reconciliation or board declaration |
| Entitled shares (`entitled_shares`) | Installment record-date shares, cash election and scrip/dilution timing; not EPS weighted-average shares | Dividend entitlement/election notice, share-capital and treasury-share records |

For the actual answer, render `Link | Status / supplied evidence | Missing input / source to obtain | Consequence`. Every status is `supported`, `missing` or `conflicting`. Cite supplied evidence for supported/conflicting rows; a supported row has no invented gap. A missing disclosure means "not provided in this packet" when that is all that is known, not proof that the issuer does not publish it. An overall High label, an average or a generic "needs more evidence" sentence is not a substitute for this checklist.

Full Analysis uses the same checklist in Section 15. JSON with a `buy_zone` stores its four links in `buy_zone.normalization_evidence`; each contains `status`, `input_detail`, `source_refs`, `resolution_source` and `consequence`. References must match entries in `sources`; unsupported links name the disclosure needed, while supported links set `resolution_source` to null. An incomplete normalized comparison is diagnostic only. If an otherwise eligible growth model does not have a credible ordinary comparison, omit `buy_zone` rather than attach unsupported N/B to an eligible action. The validator checks completeness and declared consistency, not the truth or semantic adequacy of the prose.

## Entitlement and Implementation

For an entry decision, check the actual ex-date, approval status and election deadline. A buyer after ex-date does not receive that earlier entitlement. Dividend capture does not itself create an economic gain: the price normally reflects the entitlement loss, with market movements and taxes affecting the outcome. See [HKEX equity FAQ](https://www.hkex.com.hk/global/exchange/faq/products/securities/equity-securites?sc_lang=en) (checked 2026-09-05).

For buyback and dilution work, distinguish issued, outstanding, treasury, dividend-entitled, and EPS weighted-average diluted shares. Check cancellation, treasury retention and subsequent resale. HKEX introduced a treasury-share regime in June 2024; rights depend on domicile and the applicable arrangements, so a buyback is not automatically permanent cancellation. See [HKEX treasury-share guidance](https://www.hkex.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/Other-Resources/Listed-Issuers/LIR-Newsletter/newsletter_202405.pdf) (checked 2026-09-05).

Where a concrete purchase is discussed, disclose material bid/ask spread, turnover, lot size and entry/exit costs using current evidence. Keep commission, depositary fees, FX spread and withholding distinct. Screen Mode can flag these issues without inventing a trade size or portfolio allocation.

## Evaluating the Framework

Distinguish contract/arithmetic tests, evidence-routing case reviews and historical investment outcomes. A valid JSON report does not prove its sources or forecasts. An absence of actionable buys is a diagnostic question, not a target to repair by lowering rates or evidence standards.

First classify why each distinct security/date cannot support an entry: cash-income constraint, price, forecast confidence, funding/capital risk, veto, or missing information. Deduplicate report versions when reporting sample counts. Do not count an old report's recommendation as a result produced by the current skill.

Historical decision replay must freeze information by publication time, including financials, rates, tax/channel assumptions and corporate actions. Current N/B/required returns applied to old prices are a current-assumption historical-price sensitivity, not an investable historical backtest. Include failed/delisted cases where relevant, account for distributions and costs consistently, and keep parameter development separate from evaluation. Measure cash-income realization, dividend cuts, principal loss and total return alongside trigger rates; neither zero nor many buy signals establishes calibration. See [CFA Institute: Backtesting and Simulation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation).
