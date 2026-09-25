# Data and Evidence Conventions

Read the relevant definitions in this file for all three modes before calculating yield or comparable cash changes. Screen Mode and Safety Review need only their compact-contract inputs; they do not inherit a full forecast.

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

## Recover Inputs Before Declaring Insufficiency

When the user requests research rather than an audit of a closed packet, obtaining public inputs is part of the task. Schema 3.0 requires the ordered retrieval ladder below before declaring a gap. One authoritative source can resolve an input; no extra source is required after resolution. Remaining gaps require all applicable routes, an evidence-bounded estimate attempt, and a structured recovery record.

### 3.0 取数阶梯与缺口记录

按次序检查并记录实际结果：a 公司年报、中报、季度／业务回顾、附注及管理层讨论（`issuer_filings`）；b 子公司与控股层分别披露（`group_disclosures`，集团必须分别记录 `parent` 和 `subsidiary`）；c 公司公告、分红日历、董事会／股东会决议、回购与配售（`announcements`）；d 交易所与监管披露（`exchange_regulator`）；e 官方与监管序列锚点（`official_series`）；f 往年同科目与同类披露回溯（`historical_comparables`）；g 用户提供的券商现金及扣税记录（`broker_records`）；h 有据估计，或解释为什么连区间也不能成立。

`evidence_recovery.records` 每条含实际字段的 JSON Pointer 列表 `field_paths`、原因与影响范围、按序 `attempts`（类别、层级、文件／URL、期间、尝试日期、结果），以及最终处置。访问失败写 `inaccessible`，未提供券商流水写 `not_provided`，不得把“没拿到”写成“公司不披露”。不适用也必须具体说明；集团的两层披露不能标不适用。真实研究使用 `live_research`；只有用户明确限定封闭材料的任务才能用 `provided_packet`，不得用此模式规避取数。

`resolution: bounded` 必须有 `estimate` 的上下界、单位、推导、来源期间、来源引用与适用边界。只有无法建立有据估计时才用 `not_assessable`，写清 `estimate_failure_reason` 和具体 `closure_condition`。所有未解决输入均须对应日志；已恢复值保留原取数轨迹。评分区间并不冒充经营或现金预测区间。

报告第6节简述查阅轨迹及最大剩余约束；完整日志进入结构化记录和按需附录。研究覆盖度不是公司质量；模型未完成不是公司可见性差。真实的现金、税务、资本缺口仍然限制买入，不得填中性分、取区间中点、套行业均值、移除权重或放大剩余权重。

Before saying "cannot assess", identify the actual gap and its smallest affected output. Distinguish unavailable research tools, not found after a named lookup, absent from the supplied packet, and a genuine unreconciled material constraint. An incomplete calculation is unfinished work, not proof that the company cannot be evaluated. Try the relevant filing/notes and a defensible reconstruction before stopping; do not invent successful searches or bypass access restrictions.

| Missing detail | Useful recovery or bounded assumption | Boundary that remains |
|---|---|---|
| Maintenance/growth capex split | Use disclosed total cash capex as a conservative after-investment proxy, with a once-only ledger and appropriate range | Do not add back unidentified growth or deduct the same investment again |
| Exact future shares, record dates or repurchases | Start with latest reconciled entitled/outstanding shares, announced corporate actions and sourced dilution; explicitly model no discretionary future buybacks plus sensitivity | Historical entitlements still need actual event counts; an assumed future count is not a future register |
| Future scrip participation | Model the full cash-equivalent entitlement and an explicit all-cash issuer stress case, then a sourced participation sensitivity if useful | This is a scenario assumption, not a factual claim of 100% future elections or a guaranteed cash-saving program |
| A future board decision or policy renewal | Use the current declared policy/base, explain continuation and reset scenarios, test cash capacity | No invented permanent payout promise; a policy percentage still applies only to its correct base |
| Exact annual working capital, financing or cash buffer | Anchor ranges in comparable history, commitments, maturity ladders, actual parent cash and disclosed capital/liquidity targets | Do not silently assume zero uses, unlimited refinancing or unrestricted upstream cash |
| A third/fifth comparable historical year | Retain the actual window and independently supported modules; use a labelled bounded cash proxy where reconciled | Do not fabricate years, mix periods or call a two-year ratio the three-year aggregate |
| Broker fees, personal holdings or income target | Show sourced issuer/tax cash on an explicitly before-fee basis; omit personal sizing/mandate conclusions | Unknown fees are not zero realized costs; no target means no target-fit judgment, not no company score |

Preserve known operating/earnings facts even if a downstream FAD/DPS amount remains unknown. Public guidance can anchor an analyst range; a later-year gap does not automatically invalidate earlier-year evidence or historical quality. `cash_flow_model.evidence_status` describes the selected cash bridge, not whether every future spreadsheet cell has been completed; use individual forecast statuses for missing forecast years.

Missing evidence may affect only a refinement check, one module's possible points, normalization, a future cash horizon, entry eligibility or position sizing. State which. Use `scoring.md` for provisional score ranges and coverage rather than propagating any gap into a blank overall score. Material tax, owner entitlement, cash access and capital constraints still block conclusions that actually require them.

## Focused Normalization Audits

When the user asks to audit a proposed normalized DPS, N/B calculation or its action label, answer that focused question rather than inventing a Full Analysis company report. This is a supporting audit, not a new valuation mode. Ordinary Screen Mode does not calculate N or require this audit.

Use this compact output contract even when the answer must be concise: **arithmetic conclusion; evidence/action conclusion; the four-row evidence checklist below**. Do not stop at "a dividend bridge is needed." Include all four links, distinguish facts already supplied from missing evidence, and name the missing input and disclosure needed to resolve it. Do not mark every link missing merely because one fails.

| Evidence link | Specific input to assess | Where to verify it |
|---|---|---|
| Operating cash (`operating_cash`) | Volume/pricing, margins, working capital and cash conversion supporting normalized owner cash | Segment/operating disclosures, guidance and cash-flow notes; sector equivalent when applicable |
| Funding capacity (`funding_capacity`) | Maintenance/growth investment, debt/regulatory uses and remittability leading to recurring FAD | Capex commitments, maturities, capital/remittance and parent-cash disclosures |
| Payout policy (`payout_policy`) | Policy percentage or fixed DPS, its exact earnings/cash base and funding constraint | Dividend-policy announcement, results payout reconciliation or board declaration |
| Entitled shares (`entitled_shares`) | Installment record-date shares, cash election and scrip/dilution timing; not EPS weighted-average shares | Dividend entitlement/election notice, share-capital and treasury-share records |

For the actual answer, apply `report-language.md` and render `证据环节 | 状态／已提供证据 | 缺失输入／待获取来源 | 影响` by default. Every machine status remains `supported`, `missing` or `conflicting`; reader-facing Chinese labels may include the unchanged enum in parentheses. Cite supplied evidence for supported/conflicting rows; a supported row has no invented gap. A missing disclosure means "not provided in this packet" when that is all that is known, not proof that the issuer does not publish it. An overall High label, an average or a generic "needs more evidence" sentence is not a substitute for this checklist.

For future links, `supported` may rest on an explicit, sourced and reconciled analyst range, not just a future issuer announcement. Mark facts versus assumptions and stress the range. Do not leave the share or policy link permanently missing solely because future registers or board resolutions do not yet exist; unresolved legal entitlement or material cash access is a different, genuine gap.

Full Analysis completes the same checklist and shows it in Audit Appendix part A10; the main report's Entry View names only the links that are missing or conflicting. JSON with a `buy_zone` stores its four links in `buy_zone.normalization_evidence`; each contains `status`, `input_detail`, `source_refs`, `resolution_source` and `consequence`. References must match entries in `sources`; unsupported links name the disclosure needed, while supported links set `resolution_source` to null. An incomplete normalized comparison is diagnostic only. If an otherwise eligible growth model does not have a credible ordinary comparison, omit `buy_zone` rather than attach unsupported N/B to an eligible action. The validator checks completeness and declared consistency, not the truth or semantic adequacy of the prose.

## Entitlement and Implementation

For an entry decision, check the actual ex-date, approval status and election deadline. A buyer after ex-date does not receive that earlier entitlement. Dividend capture does not itself create an economic gain: the price normally reflects the entitlement loss, with market movements and taxes affecting the outcome. See [HKEX equity FAQ](https://www.hkex.com.hk/global/exchange/faq/products/securities/equity-securites?sc_lang=en) (checked 2026-09-05).

For buyback and dilution work, distinguish issued, outstanding, treasury, dividend-entitled, and EPS weighted-average diluted shares. Check cancellation, treasury retention and subsequent resale. HKEX introduced a treasury-share regime in June 2024; rights depend on domicile and the applicable arrangements, so a buyback is not automatically permanent cancellation. See [HKEX treasury-share guidance](https://www.hkex.com.hk/-/media/HKEX-Market/Listing/Rules-and-Guidance/Other-Resources/Listed-Issuers/LIR-Newsletter/newsletter_202405.pdf) (checked 2026-09-05).

Where a concrete purchase is discussed, disclose material bid/ask spread, turnover, lot size and entry/exit costs using current evidence. Keep commission, depositary fees, FX spread and withholding distinct. Screen Mode can flag these issues without inventing a trade size or portfolio allocation.

## Evaluating the Framework

Distinguish contract/arithmetic tests, evidence-routing case reviews and historical investment outcomes. A valid JSON report does not prove its sources or forecasts. An absence of actionable buys is a diagnostic question, not a target to repair by lowering rates or evidence standards.

First classify why each distinct security/date cannot support an entry: cash-income constraint, price, forecast confidence, funding/capital risk, veto, or missing information. Deduplicate report versions when reporting sample counts. Do not count an old report's recommendation as a result produced by the current skill.

Historical decision replay must freeze information by publication time, including financials, rates, tax/channel assumptions and corporate actions. Current N/B/required returns applied to old prices are a current-assumption historical-price sensitivity, not an investable historical backtest. Include failed/delisted cases where relevant, account for distributions and costs consistently, and keep parameter development separate from evaluation. Measure cash-income realization, dividend cuts, principal loss and total return alongside trigger rates; neither zero nor many buy signals establishes calibration. See [CFA Institute: Backtesting and Simulation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation).
