# Visual Output Rules

Apply `report-language.md` to every reader-facing title, legend, table header and caption. The Chinese labels below are display text; JSON keys, enums, formula variables and official source names stay unchanged.

These analytical chart rules apply to Full Analysis. Screen Mode and Safety Review use their own compact outputs and do not require these charts or full-only records. All report modes use the single-file HTML delivery contract in `output-template.md` and the self-contained `templates/report.html` shell. `analysis-quality.md` defines the mandatory analytical records; charts and extra presentation detail are optional.

`output-template.md` decides what the reader sees. The main report carries at most three charts and five slim tables; everything else in this file is the **Audit Appendix** specification, used only when the user requests the appendix and always available as JSON records.

The main report communicates in this order:

1. The bottom-line judgment: current action and decisive reason, key numbers, and one status line with quality /85 and the combined score as points or provisional ranges with evidence coverage, and security role.
2. At most three visuals that each answer one of the four questions (finances, entry, outlook, risks), plus the staged entry card in Section 3.
3. Short bullets with numbers and judgments, not long-form explanation.

## 1. Output Capability Detection

- Use real charts when helpful, embedded as inline SVG or data images in the HTML; rendering capability does not make charts mandatory. Include a readable caption and an accessible data equivalent without duplicating the forecast cash-cost/DPS table.
- Otherwise use concise text conclusions plus slim audit tables inside the same HTML. `plain_text_fallback` describes the visualization, not a switch to a chat-only or Markdown deliverable.
- Do not fail because chart rendering is unavailable.
- Keep content static and readable with scripts disabled. Use the template's Clawpilot theme variables, table scroll containers and print styles; no remote chart libraries or separate asset files.

## 2. Main-Report Key Numbers

Use the Bottom Line table in `output-template.md` Section 1. Normalized yield must be derived from normalized business and cash-flow capacity. Quality /85, the combined /100 point/range with Grade/Grade range, coverage and portfolio role go in the one-line status beneath it, not in extra tables. A provisional recurring-income proxy must not be displayed as normalized yield.

The rules below govern every place a score appears: the status line in the main report and the full scorecard in appendix part A11.

Follow rubric 2 in `scoring.md`: missing one module produces an interval and coverage, not a blank overall score. Show `assessed`, `bounded` and `not_assessable` contributions distinctly; do not paint unknowns as zero-quality red bars, fill a midpoint, rescale available points, or rank incomparable research coverage as business quality. A chart must label its range as rubric bounds, not statistical confidence. Use the same overall status in the combined headline and detailed seven-module scorecard, including a stable provisional Grade when both endpoints agree; the separate quality-only status comes from its six non-income modules, not automatically from the overall status. Show quality-specific covered weight/85 as well as overall coverage. For zero covered weight, state insufficient evidence rather than a company score.

The three-stage decision card in main-report Section 3 references `entry_plan`; score colors and provisional points cannot imply a ready buy while material entry evidence is missing.

A falling quote cannot visually upgrade quality or security role; income-yield spreads remain price-sensitive. Preserve `quality_assessment` and its evidence links, reconciling its point/range with `scorecard.summary` rather than showing an independent legacy quality score. Missing chart or forecast preparation alone is not adverse issuer evidence for the 0-1 visibility band.

Render `quality_assessment.component_ranges`, `score_range` and `coverage_pct` even when nullable point fields cannot be shown. Label `range_kind: rubric_bounds` as scoring-rule bounds, not probability or statistical confidence; income-only uncertainty does not downgrade the quality-only evidence status.

## 3. Main-Report Charts

Use at most three charts, one per question, and only when rendering is available. Each chart replaces, rather than duplicates, the corresponding table or ladder line; the section's opening judgment serves as its caption. Provide an accessible text equivalent.

### 3.1 股息与覆盖历史图（第2节）

Stack base / ordinary DPS separately from special, supplemental or variable DPS by fiscal year, with sustainable coverage as a line and any actual-cash shortfall year highlighted. Label the coverage denominator. A normalized series must not hide an actual cash shortfall. Keep a separately labelled real-income trend in appendix A2 when supported; nominal DPS stability alone does not show purchasing-power preservation.

### 3.2 价格位置图（第3节）

Use the visual that matches `valuation_mode`:

- `ordinary_yield_based`: a Cash-Income Ladder using the four band names in `buy-zone.md`, with the current price marked. Caption it: no dividend growth is credited; this is not a complete estimate of intrinsic value.
- `total_return_based`: the Bear/Base/Bull Growth-Value Range with Base-supported starter/add and strict stress-discounted thresholds, valuation-review level and current price; show an ordinary income comparison separately when credible.
- `finite_life_harvest`: annual net distributions and the value range.
- `suspended`: no chart; state the reason in text.

Label any normalized yield band as uncertainty around central N. Cycle-state low/high DPS are separate economic states, not an uncertainty band or interchangeable forward Bear/Bull years.

For Structural Decline, show an ordinary cash-income ladder only as a secondary cross-check when specifically permitted by the finite-harvest exception in `buy-zone.md`. Ordinary ladder bands never produce action badges. A separately shown Strong Buy action needs the full independent action gates; a cash-income threshold or favorable chart color is insufficient.

### 3.3 股息展望图（第4节）

Historical DPS followed by five-year Bear/Base/Bull paths. Distinguish detailed years one to three from the extension; render unsupported years as gaps, not zeros.

Without rendering, the Section 2 and Section 4 tables and the Section 3 boundary line in `output-template.md` are the fallback; do not add text sparklines on top of them. The fuller business/FCF forecast chart, TTM-versus-normalized-versus-forecast yield comparison and growth R/g sensitivity visual belong to the appendix (A5, A6, A10).

## Appendix Tables

Sections 4 to 13 below specify the Audit Appendix. Use them only when the appendix is requested, following the part numbering A1-A13 in `output-template.md`. They also define the JSON records' display form.

## 4. Dividend Trajectory Tables

### Per-Share DPS Structure

| 财年 | 总每股股息 | 基础每股股息 | 特别／可变股息 | 每股股息同比 | 质量标签 | 说明 |
|---|---:|---:|---:|---:|---|---|

### Yield and Coverage

| 财年 | 按当前价股息率 | 按当年价股息率 | 派息率 | FCF／股息 | 覆盖率评价 | 说明 |
|---|---:|---:|---:|---:|---|---|

Quality Tag: Stable / Growing / Cyclical / One-off / Cut / Suspended / Event-driven / Peak-cycle.

Coverage Label: Strong / Adequate / Weak / Not Available.

## 5. Historical Cash-Flow Coverage Bridge

### Cash Generation

| 财年 | 披露FCF／行业代理 | 经常性股东FCF／代理 | 剩余成长／强制支出 | 经常性FAD | 实际全口径FCF | 证据 |
|---|---:|---:|---:|---:|---|---|

Show reported OCF/capex and the signed reconciliation in a separate slim table or ledger. Explicitly show whether each cash use is already included. For financial groups, replace industrial columns with the capital/remittance bridge rather than relabeling earnings as FCF.

### Cash Return and Funding

| 财年 | 现金股息 | 回购 | 股份发行 | 净债务变化 | FCF／股息 | 资金来源 |
|---|---:|---:|---:|---:|---:|---|

Funding Source: Operating FCF / Cash Balance / Asset Sale / Debt / Equity Issuance / Mixed.

Add Regulated Capital / Remittances for evidenced financial-sector funding. Show actual distribution capacity and actual coverage separately from recurring coverage. Give period completeness, declared-versus-paid reconciliation, and a specific reason for unavailable ratios.

## 6. Fundamental Forecast and Dividend Tables

Use `business-fundamentals.md` as the calculation source. Required records:

- Historical Operating Trend.
- Three-to-Five-Year Development Thesis and Milestones.
- Operating Driver Forecast.
- Financial Forecast.
- Owner FCF / Sector Proxy Build and Five-Year FAD Outlook.
- Single-Driver Sensitivity.
- Distributable-Cash Bridge.
- Share Count and Scrip / DRIP Assumptions.
- Dividend and Yield Runway.

### Dividend and Yield Runway

Precede the cash-cost/DPS table with a slim entitlement table: Year / Scenario, Policy-Indicated Entitlement, Modeled Entitlement, Cash-Settled Fraction, Settlement Adjustment, All-Cash Funding Gap. The two tables are complementary; do not copy the final DPS and cash cost into both.

| 年份／情景 | 可分配现金 | 派息政策／基数／比例 | 股息现金支出 | 推导每股股息 | 按当前价净股息率 | 资金缺口 |
|---|---|---:|---|---:|---:|---:|

Cover FY+1 through FY+5 for Bear/Base/Bull, including unavailable rows when evidence is missing. Keep policy-implied cash amounts, base amounts, policy adjustments and share-count reconciliation in a separate audit table; do not repeat the forecast Dividend Cash Cost or Derived DPS there.

For `analysis-quality.md` records, reference this runway by year/scenario instead of copying its DPS and cash cost into additional forecast tables. The separate cycle-state normalization ledger is not a second future runway.

## 7. Sensitivity Display Rules

Every sensitivity row must show `transient`, `persistent`, or `structural`.

- Transient: show affected-year DPS and yield; buy-zone change is `N/A`.
- Transient with growth DDM: separately show the discounted cash impact; terminal growth and N remain unchanged.
- Link that impact to `growth_cash_delta_audit`: dated baseline/revised net cash, unchanged R and PV deltas. Do not report an unauditable growth-value change.
- Persistent: show revised N basis or normalization adjustment before showing a boundary change.
- Structural: display `Rebuild required` instead of a numerical boundary change.

Text examples:

```text
暂时性（transient）：VLCC日租金一年内增加5,000 -> FY+1每股股息增加0.40 -> 长期买入边界不调整
持续性（persistent）：关税／费率永久上调5% -> 正常化N增加0.20 -> 高端收息要求边界（N/r_high）增加3.30
结构性（structural）：监管使某业务退出 -> 需要重建完整模型
```

## 8. Table Slimming Rules

- Main report: at most five tables, each at most six columns and eight rows; the section's opening judgment is the takeaway.
- Appendix: precede each table with a one-sentence takeaway; maximum 7 columns per table; split wider tables.
- Never print rows or columns that contain only N/A or Unknown; state the gap once instead.
- When withholding is 0%, state once that gross equals net rather than repeating columns.
- Separate TTM and normalized yield for cyclical stocks.
- Distinguish facts, guidance, consensus cross-checks, historical sensitivity, and analyst estimates.
- Label partial-year data and avoid unstated annualization.

## 9. Ordinary Cash-Income Tables

Use for ordinary valuation or a clearly labelled income-only comparison alongside eligible growth valuation. Do not let a growth comparison obscure an explicit income shortfall.

### Historical Price and Yield Context

| 指标 | 价格／水平 | 当前位置 | 说明 |
|---|---:|---:|---|

### Cash-Income Band Table

| 收息区间 | 价格范围 | 隐含净收益率 | 每股股息依据 | 证据／限制 |
|---|---:|---:|---|---|

默认使用这些中文区间名：低于要求现金收益率；正常化收入处于要求区间；正常化收入达到高端要求；压力情景收入达到高端要求。用户明确要求英文时使用 `buy-zone.md` 的对应英文名称。另列 N 依据、预测置信度和否决状态；`action_assessment.status`、`strong_buy_eligible` 及理由单独展示，不能由数学区间自动生成操作建议。

### Required Return Audit

| 基准／日期 | 币种／期限 | 税务／汇率依据 | 无风险回报锚 | 独立风险溢价区间 | 总回报要求 | 收息收益率要求 |
|---|---|---|---:|---:|---:|---:|

If shown, `required_yield_spread` compares normalized N/P with these independent required yields in percentage points. Label the spread **price-sensitive**, not price-independent quality.

### Normalization Provenance and Cycle-State Ledger

Use `analysis-quality.md` for required content. A compact presentation can split the record as follows:

| 驱动 | 期间／频率 | 单位 | 选取方法／数值 | 来源 | 联合假设／口径依据 |
|---|---|---|---|---|---|

| 周期状态／可估性 | 经营假设 | 股东现金 | 成长支出 | 强制支出 | 经常性FAD | 证据 |
|---|---|---:|---:|---:|---:|---|

| 周期状态 | 派息依据／基数／比例 | 分派权益 | 有权股数 | 该状态税前每股股息 | 对账／限制 |
|---|---|---:|---:|---:|---|

State the method, cycle/window rationale, shared units and the mid-state-to-net-N conversion once. Low/high can be Not estimable or Not applicable as defined in the canonical rules, with unavailable amounts, not fabricated zeros. Display optional N uncertainty bounds separately. Retain the four-link evidence checklist beside the ledger by reference; neither one replaces the other.

### Conditional Growth Valuation

| 情景 | 显式期股息现值 | 终值现值 | 总价值 | 终值占比 | 要求回报R／终值增长g | 证据 |
|---|---:|---:|---:|---:|---|---|

Then show the safety discount, entry limit, review-above threshold and a compact R/g sensitivity grid. Reference the funded DPS path rather than reprinting the entire runway. Entry and review levels are research parameters, not orders.

Show the first terminal-year owner-cash/reinvestment/capital funding ledger, quote-unit and share/ADR conversions, and full-period investor fees. The dated valuation multiplies already converted net DPS by its cash fraction; FX and fractions must not be applied twice. Keep a hard-income price ceiling separate from economic value.

## 10. Finite-Life Harvest Table

Use when `valuation_mode = finite_life_harvest`.

| 年份 | 预测净分派 | 折现因子 | 现值 | 关键假设 |
|---|---:|---:|---:|---|

Then show:

- Harvest horizon.
- Discount rate.
- Present value of forecast distributions.
- Residual value and percentage of total value.
- Finite-life value range.

## 11. Appendix Plain-Text Fallback

Use only inside the appendix when charts cannot render.

Render these text equivalents as semantic HTML inside the report, not as a replacement file format.

- Business and FCF trend: `Historical -> Bear | Base | Bull`.
- DPS path: `FY-4 -> FY0 -> FY+1 scenarios`.
- Yield stack: `TTM | normalized | Bear/Base/Bull`.
- Sensitivity: include type and whether N changes.
- Coverage labels by year.
- Development path: `FY+1 evidence | FY+3 capacity/cash | FY+5 durability | invalidation milestone`.
- Quality and role: `quality /85 point or range | income /15 point or range | exact/bounded/missing weights | quality/overall coverage | income fit | role rationale | combined /100 and Grade/range separately`.
- Scoring audit: `seven module statuses | inputs/periods | anchor bands | three checks | raw points | explicit caps | final points/bounds | sources/recovery`.
- Decision and rating audit: `current action/reason | starter/add/strict prices and conditions | price versus evidence wait | eight labels/rules/evidence/upgrade/downgrade triggers`.
- Real income: `matched cash/index dates | actual elapsed years | nominal/inflation/real CAGR | basket | limitations`.
- Economic FX: `generation -> remittance -> payout -> investor | FX-only / combined-Bear net-cash delta | limitations`.
- Controller and income drivers: `materiality / harm evidence | dominant cash transmission | portfolio inputs if concentration is quantified`.
- Valuation:
  - ordinary: `Current price | cash-income band | N/r_low | N/r_high | B/r_high | Veto`; use the band names above, with the no-growth/intrinsic-value limitation;
  - growth: `Income fit | scenario values | entry limit | review level | terminal dependence`;
  - finite-life: `Harvest horizon | PV distributions | residual | value range`;
  - suspended: `Buy zone suspended — reason`.

## 12. Holding Review

In the main report, holding review is at most one bullet in Section 3 (买点观点), and only when the user holds the stock or asks about holding, selling or switching. Place the compact `Trigger | Evidence | Review Level | Research Action | Missing Inputs | Next Check` table in appendix part A12, following `holding-review.md`; scoring and portfolio role are in A11. Distinguish a business/solvency red flag from a valuation-review signal. Do not display a specific trade size or a switch recommendation when the required portfolio/alternative information is absent.

Reuse `safety-review.md`'s baseline/new-disclosure and cash/capital deltas for event-driven checks within A12. No additional numbered report section is needed.

## 13. Real-Income and FX Audit Layouts

These are optional layouts for mandatory Full Analysis records, not extra analyses. Use null / unavailable with reasons when unsupported, and follow `analysis-quality.md` for calculation and action gates.

| 观察值 | 期末日期 | 恒定权益对应净现金 | 消费价格指数 | 币种／篮子／来源 |
|---|---|---:|---:|---|
| 起点 | | | | |
| 终点 | | | | |

State the exact elapsed years, nominal/inflation/real CAGR, precision-based tolerance and trend separately. Five observations do not mean five compounding intervals; missing inflation is not zero.

| 类型／年份 | Base现金路径引用 | 经营情景路径引用 | 基准→压力汇率 | 基准→压力净现金 | 现金变化 | 对冲／费用／证据 |
|---|---|---|---|---|---:|---|

Pair FX-only and combined-Bear at the same year. Reference the incremental economic-FX bridge, distinguishing fixed starting runway gross DPS from FX-driven cash/payout changes, which may be positive or negative. Show zero incremental delta for effects already in the runway. Retain the matching growth cash-flow conversion; do not repeat the entire forecast or visually imply a second FX multiplier.
