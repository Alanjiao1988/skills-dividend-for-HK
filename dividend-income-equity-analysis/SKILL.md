---
name: dividend-income-equity-analysis
description: 港股、美股和全球红利股分析技能。当用户要求红利分析、股息分析、股息率、派息分析、高息股、税后股息率、税后收益、公司基本面、盈利预测、未来分红预测、快速筛选、批量比较、预期买入价、买入区间、dividend analysis、分红可持续性或红利陷阱检查时触发。默认投资者为 HK resident individual，普通券商账户，优先使用 IBKR 等券商实际流水。本技能支持 Screen Mode 和 Full Analysis Mode。
---

# Dividend Income Equity Analysis Skill

## 技能定位

本技能用于分析上市公司的税后现金分红价值，覆盖业务与盈利趋势、现金流覆盖、预扣税、资本分配、稀释、未来分红能力、敏感性和入场估值。

## 默认假设

- 投资者为 HK resident individual。
- 使用普通券商账户。
- 投资目标是中长期现金分红收入与资本保护。
- 用户提供有效券商流水时，实际扣税记录优先于理论分类。
- 默认不处理内地个人港股通渠道，除非用户明确要求。
- 不预设 Screen Mode 的最低税后收益率。筛选目标只能来自用户明确要求或已明确建立且适用于本次筛选的组合目标；否则标记为 `Not Assessed`。

## 模式选择

- `Screen Mode`：筛选、快速评估、初步分析、批量比较、候选池或是否值得深入研究。
- `Full Analysis Mode`：完整分析、未来分红预测、买入区间、详细基本面或具体投资决策。
- 多个 ticker 且用户未明确要求完整分析时，默认 Screen Mode。

Screen Mode 必须读取 `screen-mode.md`，且不得输出三年预测、N/B、买入区间、Strong Buy 或最终评分。

Screen Mode 不得把 `buy-zone.md` 的标的必要收益率当作用户的筛选收益率目标，也不得凭空判断某个收益率“明显不足”。

## 支撑文件读取规则

- `screen-mode.md`：轻量筛选、筛选收益率目标、Yield Fit 和 Yes / Watch / No 的唯一规则源。
- `workflow.md`：模式路由、完整研究流程和数据源优先级。
- `business-fundamentals.md`：业务驱动、长期趋势、三年预测、敏感性分类、可分配现金、scrip / DRIP 和 DPS 推导。
- `visual-output-rules.md`：Full Analysis 的图表和表格规则。
- `buy-zone.md`：N/B、普通买入区间、Structural Decline 估值模式和有限期现金回收。
- `withholding-notes.md`：预扣税、PIL、scrip / DRIP 税务与现金收入规则。
- `scoring.md`：100 分评分和 Structural Decline overlay。
- `output-template.md`：模式输出和 Full Analysis 的 18 节结构。
- `schema.json`：JSON 或机器可读输出。
- `examples/example-output-skeleton.md`：Full Analysis 示例骨架。

## Screen Mode 执行原则

- 筛选收益率目标优先使用用户本次明确提供的目标，其次使用明确适用的组合目标；否则为 `Not Assessed`。
- 只有用户明确说是最低要求、硬门槛或淘汰线时，目标政策才是 `hard_minimum`；其他目标均视为 `preference`。
- 没有目标时，Yield Fit 必须为 `Not Assessed`，不得仅因收益率看起来较低而判 `No`。
- 低于 preference 目标时，收益率本身不得单独导致 `No`；应结合有证据支持的股息增长路径决定 `Yes` 或 `Watch`。
- 低于用户明确的 hard minimum 时，除非用户允许例外，否则判 `No`。

## Full Analysis 执行原则

- 报价、派息、财务和经营数据必须注明 as-of date。
- 普通、特别、可变、一次性、REIT 和基金分派必须分开。
- 必须识别真正为分红提供资金的业务与现金流。
- 至少分析五年的业务、利润、现金流和每股经济趋势；周期行业尽量覆盖完整周期。
- 未来 DPS 必须由业务驱动、盈利、OCF、Capex、可分配现金、强制用途、派息政策、scrip / DRIP 和稀释后股数推导。
- Bear / Base / Bull 必须来自明确经营假设，不得直接对历史 DPS 做任意折扣。
- 对三到五个核心驱动做 one-driver-at-a-time 敏感性，并标注 transient / persistent / structural。
- Transient 不得改变 N 或长期买入边界；Persistent 必须先重估 N；Structural 必须重跑完整模型。
- Dividend Cash Cost 和 Derived DPS 只在 Dividend and Yield Runway 中展示一次。
- 先运行红利陷阱清单，再输出估值结果。
- N 必须遵循来源优先级，并输出 basis、来源期间和 normalization adjustments。
- 不得用高 TTM 收益率、未经调整的历史均值或近端周期高点 Base DPS 直接推导买入价。
- Fundamental Trend 为 Structural Decline 时，普通买入区间默认暂停。
- 只有满足 Harvest / Managed Runoff Exception 时，才使用有限期现金回收估值；折现率下限为 10%，不得假设永续分红。
- 无法负责任预测时，将 DPS 标注为 illustrative rather than evidence-backed，并降低 Forecast Confidence。
- 最终结论必须区分事实、假设和判断。

## 输出结构

输出模式和完整章节结构以 `output-template.md` 为唯一事实源。
