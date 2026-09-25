# Output Template

This file is the single source of truth for **what the reader sees**. The other modules define **what must be worked out**: the research, calculations, gates and JSON records. Do the full analysis, but report only what changes the reader's decision.

When another module says "show", "print", "display" or "include" for Full Analysis, it means: complete that work, keep it consistent with the report, store it in JSON when machine-readable output is requested, and place it in the Audit Appendix. It enters the main report only where this file puts it.

## Report Principles

1. **Answer four questions.** The main report exists to answer: (a) how healthy the finances are and whether real recurring cash funds the dividend; (b) whether the current price is a buy point, and at what price it becomes one; (c) where the business and the dividend are heading over three to five years; (d) what could break the thesis and how to spot it early. Anything that does not change one of those answers goes to the appendix or is omitted.
2. **Conclusion first.** Every section opens with one bold sentence stating its judgment. Supporting numbers and bullets follow; they do not restate the judgment.
3. **Each number once.** A figure appears in one place in the main report. Later sections refer to it by name rather than repeating it.
4. **Plain language.** No schema field names, formulas, rule restatements, method explanations or checklist rows in the main report. Use the plain labels below. Explain a method only when the reader needs it to interpret the result, and then in one clause.
5. **No placeholder rows.** Do not print rows or cells filled with N/A, Unknown or Not estimable. Collect missing inputs in the single "数据缺口 / Data gaps" line in Section 6 and state their consequence (for example, "so the buy point is indicative only").
6. **Facts versus estimates, compactly.** Mark analyst estimates with `（估）`/`(est.)` and company guidance with `（指引）`/`(guidance)`. Unmarked numbers are reported facts. Section 6 lists the few assumptions the conclusion depends on.
7. **One disclaimer.** State research-not-advice and the no-dividend-growth limitation of cash-income bands once, in Section 6. Do not add caveats beneath each table.
8. **Language.** Write in the user's language; default to Chinese for Chinese requests. Always give the currency, unit and as-of date for prices and dividends.
9. **Length budget.** Main report: about 1,200-2,000 Chinese characters (about 800-1,300 English words) excluding tables; at most five tables, each at most six columns and eight rows; at most three charts when rendering is available. When over budget, cut explanation and repetition, never the judgment, the key numbers or the named risks.

### Plain Labels for the Main Report

| Internal term | Main-report label |
|---|---|
| `ordinary_yield_based` | 收息定价 / income-yield pricing |
| `total_return_based` | 股息增长估值 / dividend-growth valuation |
| `finite_life_harvest` | 有限期现金回收 / finite-life cash recovery |
| `suspended` | 暂不给出买点 / no buy point given |
| Recurring FAD | 可持续可分配现金 / sustainable distributable cash |
| N / B | 正常化股息 / 压力情景股息 (normalized / stress-case dividend) |
| Value-Trap Veto Not triggered / Triggered / Unclear | 红利陷阱：未触发 / 已触发 / 待确认 |
| Forecast Confidence High / Medium / Low / Not Forecastable | 预测可信度：高 / 中 / 低 / 无法预测 |
| `action_assessment` eligible / diagnostic_only / suspended | 可执行 / 仅供参考 / 暂停 |
| Cash-income bands | The Chinese or English band names in `buy-zone.md` |
| Sensitivity transient / persistent / structural | 暂时性 / 持续性 / 结构性 |

## Screen Mode

When Screen Mode is triggered, follow `screen-mode.md` only. Do not produce the Full Analysis report.

Required banner:

```text
Mode: Screen
Screening net-yield target: x.x% / Not Assessed
Target basis: user_explicit / portfolio_target / not_assessed
Target policy: hard_minimum / preference / not_assessed
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
This is a first-pass filter, not a full investment analysis.
```

Output one comparison table with one row per ticker, then one line per ticker giving the main reason for its label. Do not write a per-ticker essay. The compact screening fields include:

- Paid TTM net yield and selected screening yield/basis/range (not normalized N).
- Screening net-yield target.
- Yield Fit: Pass / Below target / Unclear / Not Assessed.
- Yield Gap in percentage points or N/A.
- Documented dividend-growth path: Yes / No / Unclear.
- `Full Analysis Recommended: Yes / Watch / No`.

Do not infer a screening target from `buy-zone.md`. If no target is available, use `Not Assessed` and do not reject a stock solely because its yield appears low.

## Focused Audit

When the user only asks to check an existing N/B, normalized dividend or action label, follow `data-conventions.md`: arithmetic conclusion, evidence/action conclusion and the four-row evidence checklist. Do not produce the Full Analysis report.

## Full Analysis Mode

The main report has these six numbered sections, in this order. The Audit Appendix follows only when requested.

## 1. 结论速览 / Bottom Line

Three sentences at most: what this company is as a dividend asset, whether its dividend is safe, and what the current price means for the reader (buy gradually, wait for price X, observe only, or no buy point).

| 现价（日期） | 税后股息率 TTM | 正常化税后股息率 | 3年股息覆盖 | 买点 | 当前位置 |
|---|---:|---:|---:|---|---|
| | | | | | |

- "买点" is the price at or below which normalized income meets the high-end requirement (or the growth-valuation entry limit, or the finite-life value range). Write `暂不给出` with a two-word reason when valuation is suspended.
- "当前位置" is the cash-income band name, or above/within/below the growth-value range.

One status line: `行动：… ｜ 预测可信度：… ｜ 红利陷阱：… ｜ 评分：xx/100（等级）｜ 组合角色：…`

## 2. 财务状况 / Financial Condition

**Opening judgment:** whether recurring cash genuinely funds the dividend, and whether the balance sheet or capital position constrains it.

One five-year table (latest comparable years; fewer if fewer exist):

| 财年 | 收入 / 行业核心指标 | 归母净利润 | 可持续可分配现金 | 每股股息 | 现金覆盖 |
|---|---:|---:|---:|---:|---:|

These columns are the default. Keep at most six, choose the ones the evidence supports (for example actual versus sustainable distributable cash when they diverge), and drop a column rather than fill it with N/A. For banks, insurers, REITs, utilities and holding companies, use the sector measures from `sector-fcf-proxies.md` instead (for example capital generation, remittances, AFFO).

Then three to five bullets, each with numbers and a judgment:

- **Earnings and cash quality:** trend, cash conversion, one-off items excluded.
- **Dividend funding:** three-year aggregate coverage, the worst year, and whether any shortfall was met by debt, asset sales, scrip or cash balances.
- **Balance sheet and capital:** leverage or regulatory capital, refinancing needs, parent-company remittance where relevant.
- **Per-share effects:** net dilution or buyback effect on shares over the period.
- **Net cash to the investor:** withholding rate and basis, and any scrip/DRIP election assumption, in one line.

## 3. 买点观点 / Entry View

**Opening judgment:** where the current price stands and at what price the stock becomes attractive, in plain words.

For income-yield pricing, one price ladder:

| 价格区间 | 对应税后股息率 | 含义 |
|---|---:|---|
| > N / r_low | < r_low | 低于要求现金收益率 |
| N / r_high – N / r_low | r_low – r_high | 正常化收入处于要求区间 |
| B / r_high – N / r_high | ≥ r_high | 正常化收入达到高端要求 |
| ≤ B / r_high | 压力情景 ≥ r_high | 压力情景收入达到高端要求 |

Replace the formulas with the computed prices and mark the current price's row with `← 现价`. Then at most four bullets:

- **Required return:** risk-free anchor plus risk premium gives the required net yield range, in one line with date and currency.
- **Action and conditions:** the independent action status in plain words (可执行 / 仅供参考 / 暂停), why Strong Buy is or is not available, and the specific evidence or price that would change the action.
- **Evidence gaps behind the buy point:** name any of the four normalization links (operating cash, funding capacity, payout policy, entitled shares) that are missing or conflicting, in one line. Omit when all are supported.
- **Holding review:** only when the user holds the stock or asks about holding, selling or switching: the review trigger, the level and the research action. Do not invent position sizes.

For dividend-growth valuation, replace the ladder with one table: Bear / Base / Bull value, entry limit after the safety discount, valuation-review level and the terminal value's share of Base value. Add the separate income-yield comparison in one line when credible; growth value does not waive an explicit income minimum.

For finite-life cash recovery, state the harvest horizon, discount rate (at least 10%) and value range in one line each.

When valuation is suspended, give no price ladder: state the reason and the conditions that would reopen valuation in at most three bullets.

## 4. 长期展望：业务与股息 / Long-Term Business and Dividend Outlook

**Opening judgment:** whether per-share cash and the dividend are likely to be higher, flat or lower in three to five years, and the main reason.

- **Business drivers:** two to four bullets, each naming a driver or segment, its FY+3/FY+5 direction with a number or range, whether it is committed or optional, and the evidence.
- **Dividend outlook table:**

| 情景 | 核心假设 | FY+1 DPS | FY+3 DPS | FY+5 DPS | FY+1–3 覆盖 |
|---|---|---:|---:|---:|---:|
| 悲观 Bear | | | | | |
| 基准 Base | | | | | |
| 乐观 Bull | | | | | |

  Leave an unsupported later-year cell blank and explain it once in Section 6.
- **Payout policy and dividend growth:** policy and its calculation base, expected DPS growth range, and payout headroom or funding gap, in one or two lines.

## 5. 风险点与跟踪信号 / Key Risks and Monitoring

**Opening judgment:** the dividend-trap result (未触发 / 已触发 / 待确认) and the single largest risk to the dividend.

| 风险 | 早期信号（可观察指标 / 阈值） | 对股息的影响 | 性质 | 下次检查 |
|---|---|---|---|---|

- Three to five company-specific risks, ranked by their effect on the dividend. Each needs an observable signal with a threshold taken from the model or disclosures, a quantified or directional dividend impact, and a nature label (暂时性 / 持续性 / 结构性).
- Include every dividend-trap item that is flagged or unclear; omit items that passed. Exclude generic risks (market volatility, macro uncertainty) unless their effect on this dividend is quantified.
- Where useful, add one line naming the milestone that would confirm the Base case.

## 6. 数据来源与关键假设 / Sources and Key Assumptions

- **数据截至：** research cut-off and price date/source.
- **主要来源：** at most five key official sources; the full list belongs in the appendix.
- **关键假设：** at most five assumptions the conclusion depends on most, each marked as fact, guidance or estimate.
- **数据缺口：** one line listing missing material inputs and their consequence for confidence or the buy point.
- **说明：** one line: research, not personalized investment or tax advice; cash-income bands credit no dividend growth.

## Audit Appendix (on request)

Output the appendix only when the user asks for detailed workings, full calculations, an audit trail, an appendix or the complete model. Otherwise end after Section 6 with one line offering the appendix. JSON output (`schema.json`) always carries the full records regardless of what the report displays. Saving or publishing a report (`publishing.md`) uses the same main report; include the appendix only when requested.

When shown, the appendix uses these parts under a single `## Audit Appendix` heading, each following its canonical module and the appendix table rules in `visual-output-rules.md`. Include only the parts relevant to the question; do not print empty parts.

- **A1. Listing and dividend treatment:** domicile, security type, currencies, official and dividend-entitled share count, withholding basis, broker cash-line type, scrip/DRIP election, tax and dilution uncertainty (`withholding-notes.md`).
- **A2. Dividend trajectory:** per-share DPS structure and yearly yield/coverage tables with quality tags and a dividend-pattern note.
- **A3. Historical cash-flow coverage bridge:** reported FCF/proxy to Recurring Owner FCF and Recurring FAD, once-only deduction ledger, cash return and funding sources, three-year aggregate, five-year worst recurring and worst actual coverage.
- **A4. Capital allocation and buyback quality:** payout-policy type and exact calculation base, reinvestment, leverage, issuance, scrip/DRIP and whether buybacks create value.
- **A5. Business outlook detail:** development-thesis table, milestones, historical operating trend and sector model/holding-company overlay (`business-outlook.md`, `sector-fcf-proxies.md`).
- **A6. Five-year forecast:** annual Bear/Base/Bull operating and financial forecasts, FCF build and capital needs, FCF change decomposition, cumulative FAD and liquidity trough; unsupported years with reasons (`business-fundamentals.md` Section 6).
- **A7. Sensitivity:** three to five single-driver rows, each typed transient/persistent/structural, with the growth-model cash-PV audit where applicable.
- **A8. Dividend forecast bridge and runway:** distributable-cash bridge, share count and scrip/DRIP assumptions, policy-entitlement table and the single Dividend and Yield Runway. Do not repeat Dividend Cash Cost or Derived DPS.
- **A9. Dividend trap checklist:** every item from `workflow.md` Step 10 with status and evidence.
- **A10. Valuation detail:** valuation mode and reason, required-return audit, N/B values/basis/period/adjustments, DPS currency and unit conversion, the four-row normalization evidence checklist from `data-conventions.md`, cash-income band table and action assessment; growth scenario PVs, R/g sensitivity and terminal funding ledger; or the finite-life harvest table (`buy-zone.md`).
- **A11. Score and portfolio role:** module points from `scoring.md`, overlays, unadjusted score and adjusted grade, portfolio-role rationale.
- **A12. Holding review:** trigger table, constraints and switching comparison from `holding-review.md`.
- **A13. Sources and data quality:** the full source list, stale or restated data, forecast sources and confidence by horizon, and whether future FCF/DPS is evidence-backed or illustrative.
