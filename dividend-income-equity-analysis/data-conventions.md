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

## Entitlement and Implementation

For an entry decision, check the actual ex-date, approval status and election deadline. A buyer after ex-date does not receive that earlier entitlement. Dividend capture does not itself create an economic gain: the price normally reflects the entitlement loss, with market movements and taxes affecting the outcome. See [HKEX equity FAQ](https://www.hkex.com.hk/global/exchange/faq/products/securities/equity-securites?sc_lang=en) (checked 2026-09-05).

For buyback and dilution work, distinguish issued, outstanding, treasury, dividend-entitled, and EPS weighted-average diluted shares. Check cancellation, treasury retention and subsequent resale. HKEX introduced a treasury-share regime in June 2024; rights depend on domicile and the applicable arrangements, so a buyback is not automatically permanent cancellation. See [HKEX treasury-share guidance](https://www.hkex.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/Other-Resources/Listed-Issuers/LIR-Newsletter/newsletter_202405.pdf) (checked 2026-09-05).

Where a concrete purchase is discussed, disclose material bid/ask spread, turnover, lot size and entry/exit costs using current evidence. Keep commission, depositary fees, FX spread and withholding distinct. Screen Mode can flag these issues without inventing a trade size or portfolio allocation.

## Evaluating the Framework

Distinguish contract/arithmetic tests, evidence-routing case reviews and historical investment outcomes. A valid JSON report does not prove its sources or forecasts. An absence of actionable buys is a diagnostic question, not a target to repair by lowering rates or evidence standards.

First classify why each distinct security/date cannot support an entry: cash-income constraint, price, forecast confidence, funding/capital risk, veto, or missing information. Deduplicate report versions when reporting sample counts. Do not count an old report's recommendation as a result produced by the current skill.

Historical decision replay must freeze information by publication time, including financials, rates, tax/channel assumptions and corporate actions. Current N/B/required returns applied to old prices are a current-assumption historical-price sensitivity, not an investable historical backtest. Include failed/delisted cases where relevant, account for distributions and costs consistently, and keep parameter development separate from evaluation. Measure cash-income realization, dividend cuts, principal loss and total return alongside trigger rates; neither zero nor many buy signals establishes calibration. See [CFA Institute: Backtesting and Simulation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation).
