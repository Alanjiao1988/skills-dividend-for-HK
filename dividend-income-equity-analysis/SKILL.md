---
name: dividend-income-equity-analysis
description: 港股、美股和全球红利股分析技能。当用户要求红利分析、股息分析、税后收益、公司基本面、未来3至5年发展展望、FCF自由现金流预测、盈利与分红预测、快速筛选、批量比较、买入区间、持仓复评、减仓退出或换仓研究、dividend analysis、分红可持续性或红利陷阱检查时触发。默认投资者为 HK resident individual，普通券商账户，优先使用 IBKR 等券商实际流水。本技能支持 Screen Mode 和 Full Analysis Mode。
---

# Dividend Income Equity Analysis Skill

## 技能定位

本技能用于分析上市公司的税后现金分红价值，连接未来三至五年业务发展、经常性股东现金流、行业资本约束、成长质量、派息政策、估值和持仓复评。收息适配与成长价值分别回答，不以成长抵消用户明确的最低现金收益要求。

## 默认假设

- 投资者为 HK resident individual。
- 使用普通券商账户。
- 投资目标是中长期现金分红收入与资本保护。
- 用户提供有效券商流水时，实际扣税记录优先于理论分类。
- 默认不处理内地个人港股通渠道，除非用户明确要求。
- 不预设 Screen Mode 的最低税后收益率。筛选目标只能来自用户明确要求或已明确建立且适用于本次筛选的组合目标；否则标记为 `Not Assessed`。

## 模式选择

- `Screen Mode`：筛选、快速评估、初步分析、批量比较、候选池或是否值得深入研究。
- `Full Analysis Mode`：完整分析、未来三至五年展望、FCF或分红预测、买入区间、详细基本面、持仓复评或具体投资决策。
- 多个 ticker 且用户未明确要求完整分析时，默认 Screen Mode。

Screen Mode 必须读取 `screen-mode.md`，且不得输出三至五年预测、N/B、成长估值、买入区间、减仓价格、Strong Buy 或最终评分。

Screen Mode 不得把 `buy-zone.md` 的标的必要收益率当作用户的筛选收益率目标，也不得凭空判断某个收益率“明显不足”。

## 支撑文件读取规则

- `screen-mode.md`：轻量筛选、筛选收益率目标、Yield Fit 和 Yes / Watch / No 的唯一规则源。
- `workflow.md`：模式路由、完整研究流程和数据源优先级。
- `business-outlook.md`：三至五年发展展望、竞争格局、增长项目、资本需求、情景假设与可证伪里程碑。
- `business-fundamentals.md`：Recurring Owner FCF → Recurring FAD、五年情景预测、派息计算基数、敏感性分类、scrip / DRIP 和 DPS 推导。
- `sector-fcf-proxies.md`：银行、保险、REIT、公用事业、控股公司等行业代理与资本／上缴现金证据的唯一规则源。
- `visual-output-rules.md`：Full Analysis 的图表和表格规则。
- `buy-zone.md`：独立必要回报推导、N/B收息区间、有条件的成长估值、Structural Decline及有限期现金回收。
- `holding-review.md`：持有、复评、减仓、退出、换仓的证据与组合约束；不自动交易。
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
- 必须形成五年业务发展展望，并提供前三年逐年Bear / Base / Bull预测及第四、五年的有依据延伸；不能预测的年份保留空值、原因和较低置信度，不机械外推CAGR。
- 未来 FCF 必须由业务量价、利润率、营运资金、维护与成长投资、融资／税务和股东现金权益推导；分别展示经常性与实际现金口径、总量与每股趋势、累计FAD及资金缺口。
- 先选择行业代理，金融机构不得把OPAT、净资产增长或偿付能力比率直接当作现金流；控股公司还须验证子公司可上缴及母公司可用现金。
- 每项Capex、利息、租赁、资本留存等只扣一次。实际现金义务不能因正常化而消失。
- 覆盖率以三年累计Recurring FAD除以同期现金股息，并展示五年最差年度及实际现金短缺；数据不足必须披露。
- 未来 DPS 必须由上述现金能力和正确的派息政策基数推导，盈利派息率不得直接乘FAD。派息承诺与资金约束冲突时须显示调整及缺口。
- Bear / Base / Bull 必须来自明确经营假设，不得直接对历史 DPS 做任意折扣。
- 对三到五个核心驱动做 one-driver-at-a-time 敏感性，并标注 transient / persistent / structural。
- Transient 不得改变 N 或普通收息边界，但须反映成长估值中受影响年度现金的现值；Persistent 必须先重估 N及可持续成长；Structural 必须重跑完整模型。
- Dividend Cash Cost 和 Derived DPS 只在 Dividend and Yield Runway 中展示一次。
- 先运行红利陷阱清单，再输出估值结果。
- N 必须遵循来源优先级，并输出 basis、来源期间和 normalization adjustments。
- 不得用高 TTM 收益率、未经调整的历史均值或近端周期高点 Base DPS 直接推导买入价。
- Fundamental Trend 为 Structural Decline 时，普通买入区间默认暂停。
- 只有满足 Harvest / Managed Runoff Exception 时，才使用有限期现金回收估值；折现率下限为 10%，不得假设永续分红。
- 必要回报必须打印币种／期限／税务一致的无风险锚、与价格独立的风险溢价和最终回报区间；不得用含股息率的总评分反推溢价。
- `total_return_based`仅在增长、再投资、资本、派息及终值均有依据时启用；先预测现金再折现，不把近端高增长永续化，也不预设某只股票必须变得便宜。
- 持仓复评使用前瞻收益和现金收入，不用成本收益率；估值偏贵触发复评而非机械卖出，缺少组合或替代品资料时不编造仓位与换仓结论。
- 无法负责任预测时，将 DPS 标注为 illustrative rather than evidence-backed，并降低 Forecast Confidence。
- 最终结论必须区分事实、假设和判断。

## 输出结构

输出模式和完整章节结构以 `output-template.md` 为唯一事实源。

## 报告保存与仓库边界

- 本仓库只维护可复用的分析规则、模板、schema 和工具，不用于归档具体公司的研究报告。
- 默认在对话中输出分析；只有用户明确要求保存或发布时，才生成报告文件。
- 临时报告、下载的披露资料、券商流水和生成的图表应放在会话工作区或用户指定的仓库外目录，不写入技能源码目录。
- 完整报告的独立归档仓库为 `Alanjiao1988/Dividendreport`，按 ticker 和数据基准日归档；发布前须获得用户明确授权并确认 company、ticker、exchange、as-of date。
- `output-template.md` 和 `examples/example-output-skeleton.md` 必须保持为可复用模板或占位示例，不得用真实公司报告覆盖。
