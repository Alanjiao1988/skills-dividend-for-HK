# Workflow

Use this workflow when reviewing dividend-paying listed companies.

Apply `report-language.md` before rendering any report, chart or publication summary. English rule names and code enums remain canonical identifiers, not a requirement to write reader-facing prose in English.

## Mode Selection

Read `data-conventions.md` and the selected mode's canonical rules before research begins. Screen Mode reads `screen-mode.md` and only the supporting rules needed for the compact screen, not the Full Analysis forecast modules or new analytical records.

Use Screen Mode for screening, quick review, candidate-pool work, batch comparison, or multiple tickers where the user asks which names deserve deeper research.

Use Safety Review for a disclosure-driven update to security-level dividend safety against a sourced prior cash/capital baseline. Use `safety-review.md`; missing baseline/current evidence is reported, not fabricated.

Use Full Analysis for detailed research, three-to-five-year business/FCF outlooks, future dividend forecasts, buy points, current entry readiness, complete scores/ratings, or holding and switching decisions. Explicit buy/score requests take priority over quick-review wording or a multiple-ticker default.

The machine modes are `screen`, `full_analysis` and `safety_review` in schema 3.0. A focused normalization audit remains a supporting task under `data-conventions.md`, not another mode. Follow the minimum task matrix in `analysis-quality.md`. All modes require the ordered retrieval log and Chinese `report_output`; only Full Analysis adds `decision`, numeric score bounds and staged prices. Before declaring any gap, actually follow the seven-source ladder and bounded-estimate step in `data-conventions.md`. Verify the final three answers and single action against `entry_plan`, not against a desired Grade.

Screen Mode and Safety Review end their analysis after their compact outputs, then use Common Report Delivery below. Neither silently continues into the Full Analysis steps below.

## Screen Mode Workflow

1. Verify ticker, listing, current price, and as-of date.
2. Separate paid TTM yield from the selected recurring-income screening measure, with distribution, withholding, FX and fee basis.
3. Resolve the screening net-yield target using this priority:
   - user-explicit target for the current screen;
   - clearly applicable portfolio-level target with provenance/validity from `portfolio-context.md`;
   - `Not Assessed` when neither is available.
4. Classify target policy as `hard_minimum`, `preference`, or `not_assessed`.
5. Calculate Yield Fit and Yield Gap:
   - Follow `screen-mode.md`: compare the selected screening yield or supported range with the target.
   - Pass when its lower bound meets the target; Below target when its upper bound is below it.
   - Unclear when the range straddles the target or material inputs are unusable; normally Watch.
   - Not Assessed / N/A when no target is available.
6. Check whether a claimed dividend-growth path is documented by policy, earnings, cash flow, or an established record.
7. Classify the five-year DPS pattern.
8. Check latest FCF / Dividend or sector-equivalent coverage.
9. Check leverage, regulatory-capital, solvency, or refinancing alerts.
10. Make a preliminary Fundamental Trend classification.
11. Run the abbreviated dividend-trap screen.
12. Output `Full Analysis Recommended: Yes / Watch / No`.

Do not use `buy-zone.md` required-yield ranges as the investor's screening target.

If the screening target is Not Assessed, do not reject or downgrade a stock solely because its yield appears low.

If the target is a preference and Yield Fit is Below target, yield alone cannot produce `No`. Use `Watch` when a documented growth path or another unresolved question deserves Full Analysis.

If the target is an explicit hard minimum and Yield Fit is Below target, use `No` unless the user explicitly permits exceptions.

Required limitations:

```text
模式：轻量筛选（Screen）
预测置信度：暂不评估（Not Assessed）
买入区间：暂不评估（Not Assessed）
不输出三至五年预测、N/B、成长估值、买入／减仓价格、强力买入标签或最终评分。
```

## Safety Review Workflow

1. Identify the new disclosure, its availability date, analysis cutoff and a dated prior review/source, or record the missing baseline.
2. Reconcile the comparable cash, payout, liquidity and capital deltas using sector-appropriate definitions; compute current coverage and funding gap only when supported.
3. State safety, directional decision or `not_comparable`, missing inputs and next review. A security-level review does not require a full holdings export.
4. Apply `safety-review.md` escalation rules for structural change, unresolved funding/veto or material uncertainty. Escalation means full reassessment, not a new valuation within this mode or an automatic sale.

The minimal `review` record has no forecast, N/B, score, grade, trade size or automatic trading. Purely transient, supported updates may remain light.

## Full Analysis Data Rules

Always record the data date.

Read `analysis-quality.md` for the required full-only records and their missing-data consequences. Complete them for every Full Analysis; their conclusions enter the six-section main report at the locations in `analysis-quality.md`, and the full records go to the Audit Appendix and JSON. Charts and additional presentation detail are optional, not substitutes for evidence.

- Price must include as-of date and exchange.
- Dividend history should come from official announcements or annual reports when available.
- Check dividend currency, record date, ex-date, payment date, special-dividend treatment, and scrip / DRIP terms.
- Distinguish reported facts, company guidance, consensus cross-checks, historical sensitivities, and analyst estimates.
- User broker statements are the priority source for actual cash received and actual withholding, subject to PIL classification.
- Use official share count from filings when available.
- Historical price inputs must identify period, frequency, source, and price type.

## Search Instructions

For HK-listed stocks, search HKEXnews and issuer materials for results, annual/interim reports, dividend and tax notes, scrip-election documents, operating statistics, guidance, cash flow, capex, share issuance, and buybacks.

For US-listed stocks, search SEC EDGAR and investor relations for 10-K, 10-Q, 8-K, proxy, operating KPIs, guidance, dividend declarations, DRIP terms, cash flow, share count, issuance, and buybacks.

For UK-listed stocks, search LSE RNS and investor relations for results, guidance, dividend and scrip terms, and buyback programmes.

Source order:

1. Official exchange announcements and filings.
2. Annual/interim reports, results, dividend documents, operating statistics, and guidance.
3. Company investor relations and management commentary.
4. User broker statement.
5. Third-party cross-checks.

Before returning an unavailable score or forecast, apply the recovery-first protocol in `data-conventions.md`. Attempt relevant official inputs and reconciled derivations, then bounded estimates. For a closed packet, respect that scope and say "not supplied", not "issuer does not disclose". A missing granular KPI is not automatically a whole-model failure; record its actual consequence.

## Step 1: Classification

Collect company, ticker, exchange, domicile, operating geography, listing structure, reporting currency, dividend currency, investor reporting currency, and security type.

Identify scrip dividend, stock dividend, elective share distribution, or DRIP.

Identify the ultimate controller and ownership source for `controller_risk`; a sourced absence of a controller is valid. Do not confuse an unlisted controlling parent with subsidiaries that remit cash to a listed holding company.

## Step 2: Dividend Treatment

Read `withholding-notes.md`.

Show gross DPS, withholding rate and basis, net DPS, gross and net yield, broker-observed status, and broker cash-line type.

For scrip / DRIP, state the cash-election assumption and tax, broker, fractional-share, and dilution uncertainty.

## Step 3: Business Fundamentals and Long-Term Trend

Read `business-outlook.md`, `business-fundamentals.md`, and `sector-fcf-proxies.md`.

Identify the dividend funding engine and build the historical operating baseline. Classify Fundamental Trend and select three to five core operating drivers.

Use `analysis-quality.md` for one or two income-driver tags, the economic currency-to-remittance/payout chain and the normalization window. The historical five-year overview does not establish a full cycle; explain the relevant supply, contract or capital cycle.

Track per-share effects from ordinary issuance, scrip / DRIP, and buyback offsets.

Select the sector model and any holding-company overlay. Build a five-year development thesis with segment/driver baselines, FY+3/FY+5 outcomes, competitive risks, investment/funding needs, and dated milestones that can invalidate the thesis. Separate disclosed facts, guidance and analyst assumptions.

## Step 4: Historical Dividend Record

Build the Dividend Snapshot and Dividend Trajectory. Separate recurring, special, variable, and one-off distributions.

Add the separate `real_income` purchasing-power assessment under `analysis-quality.md`, using comparable historical net cash and a relevant consumption basket. Missing inflation or baseline cash is unavailable, not zero; nominal stability and nominal valuation remain separate.

The coverage fields may be backfilled after Step 5.

## Step 5: Historical Cash-Flow Coverage

Reconcile reported FCF/sector capital generation to Recurring Owner FCF and Recurring FAD using the once-only deduction ledger. Preserve actual all-in FCF, exceptional obligations and parent/remittance constraints separately.

Calculate three-year aggregate recurring FAD / relevant cash dividends paid, five-year worst recurring coverage, and worst actual coverage. Do not average ratios, mix declared and paid dividends, or call OPAT cash flow. If a standard window is unavailable, retain the actual evidence window and test a reconciled cash-proxy range for provisional scoring. Do not require a completed five-year forecast before retaining independently reconciled historical coverage.

Return to Step 4 and complete coverage fields.

## Step 6: Capital Allocation and Buybacks

Review payout policy, reinvestment, leverage, acquisitions, issuance, ATM, scrip / DRIP, and shareholder returns.

Complete the controller-impact assessment in `analysis-quality.md`: evidence of listed-company transfers, guarantees or payout changes must connect to actual material harm before a controller veto is triggered. A parent's funding demand, ownership category or timing alone is not that connection.

Classify fixed/progressive, earnings-linked, cash-flow-linked, base/variable or discretionary policy and identify its exact calculation base before applying a payout ratio.

Assess true diluted-share-count change and whether buybacks create value or merely offset dilution.

## Step 7: Three-to-Five-Year Fundamental and FCF Forecast

Build Bear, Base, and Bull cases from explicit operating drivers. Derive sector income, profitability, working capital, normalized OCF, maintenance investment, owner cash, remaining growth/capital uses and recurring FAD. Model funding, interest and dilution; growth does not arrive before investment.

Provide detailed FY+1 to FY+3 rows and supported FY+4/FY+5 extensions. Unsupported years retain null values, Not estimable, and a specific reason. Show total and per-share cash trends, the FCF change decomposition, cumulative cash generation and liquidity/self-funding implications. A five-year qualitative outlook is required even when later numerical estimates are unavailable.

Do not apply arbitrary percentage haircuts directly to DPS.

Build one-driver-at-a-time sensitivity for three to five important drivers and classify every row:

- `transient`: temporary; update affected-year cash flow, DPS, and yield only; normalized high-end cash-yield boundary change (N/r_high) = N/A;
- `persistent`: expected to alter normalized economics; recalculate N before updating boundaries;
- `structural`: rebuild Fundamental Trend, forecast, scoring, veto, and valuation mode.

For growth DDM, transient cash changes affect dated present value only, not terminal growth or ordinary boundaries.

State the evidence basis and nonlinear limitations.

Complete `fx_risk` using the same forecast-year Base and Bear runway, with matched FX-only and combined-Bear stress under `analysis-quality.md`. Keep the joint scenarios coherent and reconcile any economic FX effect, tax, fees, hedge cash and growth cash-flow conversion once.

## Step 8: Dividend Forecast Bridge

Use `business-fundamentals.md` Section 2 for the single cash definition: Recurring FAD equals owner cash/proxy less remaining growth and mandatory uses; total distribution capacity additionally deducts exceptional cash uses and includes only explicitly available excess cash. Never deduct capex or capital needs twice.

Build the Distributable-Cash Bridge and Share Count and Scrip / DRIP Assumptions table.

Forecast diluted share count using ordinary issuance, scrip / DRIP participation, and buyback offsets.

Rate Forecast Confidence by horizon. Reconcile the cash model, source units, share units and dividend-entitled versus diluted shares.

## Step 9: Dividend and Yield Runway

Build the single Dividend and Yield Runway:

```text
Policy-Implied Dividend
= stated policy applied to its stated earnings / cash / DPS base

Modeled Dividend Entitlement
= policy-implied amount after explicitly justified funding/policy adjustments

Derived DPS per installment
= Modeled Dividend Entitlement / dividend-entitled share count

Forecast Dividend Cash Cost
= Modeled Dividend Entitlement x cash-settled fraction + settlement cash adjustment

Funding Gap
= max(0, Forecast Dividend Cash Cost - Total Distribution Capacity)

Net Yield at Current Price
= Derived DPS x (1 - withholding rate) / current price
```

Aggregate installment cash cost and DPS separately; use the entitlement and settlement rules in `business-fundamentals.md`. Do not create another table that repeats Dividend Cash Cost and Derived DPS.

Reconcile forecasts across all five year/scenario pairs. Unsupported cash or share inputs must not yield precise DPS, coverage or terminal values.

## Step 10: Dividend Trap Checklist

Check at least:

- high yield caused by price collapse;
- weak normalized coverage;
- payout above FCF;
- rising leverage or refinancing wall;
- debt-, asset-sale-, or equity-funded payout;
- issuance, ATM, or persistent scrip dilution concurrent with elevated payout;
- one-off or peak-cycle distributions treated as recurring;
- weaker policy language or regulatory payout pressure;
- FX mismatch;
- ineffective buybacks;
- forecast DPS inconsistent with business drivers, cash generation, payout policy, or share count;
- N retaining temporary premiums;
- recurring FAD inflated by duplicated add-backs, omitted growth investment, or excess-cash releases;
- sector earnings proxies without capital/remittance evidence;
- confirmed material controller-driven harm to the listed company's funding, necessary investment, liquidity or minority value, using `analysis-quality.md`;
- growth dividends assuming unfunded reinvestment, unbounded terminal growth or nonexistent cash conversion;
- Structural Decline without a credible finite-life harvest case.

Set Value-Trap Veto to Not triggered / Triggered / Unclear.

Do not treat unresolved material controller or FX evidence as a passed safety gate; follow the diagnostic/no-Strong-Buy/Core restrictions in `analysis-quality.md`, without asserting proven distress.

## Step 11: Valuation Mode and Entry Framework

Read `buy-zone.md`.

First establish a sourced, dated, currency/tax-consistent risk-free anchor, a price-independent risk-premium range and resulting required total return. Do not derive risk from the total score, which contains yield. Resolve any explicit cash-income target separately.

### Ordinary Dividend Asset

Use valuation mode `ordinary_yield_based` and deterministic N, B, r_low, and r_high boundaries.

Always state N value, N basis, source period, and normalization adjustments.

Include the canonical `normalization_model` next to the four-link evidence checklist whenever `buy_zone` exists. Reconcile the central sustainable state to N and distinguish cycle extremes, uncertainty bounds and future Bear/Bull forecasts. Unsupported central normalization cannot yield an actionable N.

### Eligible Dividend-Growth Asset

Use `total_return_based` only after the evidence gates in `buy-zone.md` pass. Discount the same funded annual dividend path, with a justified transition and bounded terminal growth. Display scenario values, R/g sensitivity, terminal dependence, the Base-supported starter price and separate strict stress-discounted threshold, plus the ordinary income comparison where credible. Do not force a stock into growth valuation to justify its current price.

### Structural Decline Without Exception

Use valuation mode `suspended`. Do not output ordinary cash-yield bands or actionable entry conclusions.

### Structural Decline With Harvest / Managed Runoff Exception

Use valuation mode `finite_life_harvest`.

Estimate the present value of finite annual after-tax distributions plus a conservative residual value. Use a discount-rate floor of 10%, state the harvest horizon, and do not assume a perpetual terminal dividend.

Ordinary yield-based zones may be shown only as a secondary cross-check with r_low at least 10%.

If the Value-Trap Veto is triggered, suspend ordinary and growth valuation output; growth cannot bypass the veto.

### Entry Decision Card

Complete `entry_plan` from `buy-zone.md` Sections 5.2-5.3 in every Full Analysis, even when numerical valuation is suspended. Calculate the three staged reference prices, hard-income caps and signed distances. Reconcile Bear/Base/Bull holding-period returns and a sourced principal-risk review; show opportunity, monitoring and thesis-invalidation evidence. Separate `wait_for_price` from `wait_for_evidence`. A bounded Medium forecast with otherwise supported entry conditions permits `accumulate`, not an automatic Watchlist-only answer.

Apply each limitation to its affected output. A noncritical missing score input or unknown personal position size is not a new financial veto. An actual cash/capital/tax gap remains a gate failure regardless of price.

## Step 12: Quality, Role, and Holding Review

Use `scoring.md` for the six-component quality total /85, separate current-price income fit and optional normalized-yield spreads. Retain the /100 mixed score and Grade only as labelled compatibility indicators. Complete `portfolio_role_assessment` from quality, safety and constraints, never a Score-to-Role table or price decline alone.

Read `holding-review.md`. Link business milestones, cash/solvency warnings, valuation-review levels and portfolio constraints to hold/review/trim/exit/switch or Not Assessed. A price threshold triggers review, not an order.

Within the full holding review, reuse `safety-review.md`'s dated baseline, cash/capital deltas and escalation discipline where relevant; do not add a report section.

Compare alternatives only with evidenced prospective cash income and risk-adjusted returns on the same currency/horizon basis, net of taxes, fees and switching costs. Without position size, constraints or an identified alternative, state the missing inputs rather than inventing a trade.

## Step 13: Auditable Scores, Ratings and Final Decision

Use `scoring.md` to recover evidence, select supported bands or bounded alternatives and evaluate the three fixed checks. Calculate points/ranges and explicit caps. Present quality /85 and income /15 before the combined /100 Grade, with exact/bounded/missing weights and the binding uncertainty. Missing one module must not cancel the aggregate display; never normalize a subtotal to 100 or fill an unknown module with neutral points. An unbuilt forecast is not by itself evidence for the lowest visibility band.

Complete the eight `rating_audit` records with matching labels, rules, dated sources and upgrade/downgrade triggers. Use stable provisional labels when the complete score interval supports them; otherwise show the label range. Reconcile the executive decision to `entry_plan`, not the Grade. Machine output uses schema 3.0 and rubric 2; the executive score/range/status must match `scorecard.summary`. Validate arithmetic and consistency, not source truth or investment merit.

## Step 14: Write the Report

Read `output-template.md`. Steps 1-13 are the work; the report is a distillation of it, not a transcript. Write the six-section main report: bottom line, financial condition, entry view (including the staged entry card), long-term business and dividend outlook, key risks and monitoring, sources and key assumptions. Keep within its length budget, keep every number consistent with the underlying model, and leave the bridges, ledgers, full forecasts, sensitivities, full trap checklist, valuation audit, full scorecard and rating audit and holding-review table to the Audit Appendix unless the user asks for it.

## Common Report Delivery

For every report request, including Screen and Safety Review, follow the single-file HTML contract in `output-template.md`. Read `templates/report.html`, fill the complete selected-mode content as static HTML, embed all styles and optional charts, and save one `.html` file. Full Analysis uses the six-section main report, with the Audit Appendix only on request; compact modes do not inherit full-only records. Ordinary conversational clarifications remain in chat unless a report is requested.

Validate any structured analysis with the existing schema/validator when needed, without making JSON a mandatory extra deliverable. Check the actual HTML file, resolved placeholders, table readability, source links and chapter anchors. A chart-free report still uses the HTML file with text/tables. Return its actual link/path plus a short Chinese summary, not the whole report in chat.

For archive publication, read `publishing.md` and verify HTML path, metadata and index-validator compatibility before any authorized push to `Alanjiao1988/Dividendreport`. Local generation is not publication; do not change the archive schema, enable hosted workflows or invent a live viewing URL.
