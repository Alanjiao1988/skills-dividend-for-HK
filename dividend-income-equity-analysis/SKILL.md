---
name: dividend-income-equity-analysis
description: 港股、美股和全球红利股分析技能。当用户要求红利分析、股息分析、股息率、派息分析、高息股、税后股息率、税后收益、公司基本面、盈利预测、未来分红预测、预期买入价、买入区间、dividend analysis、分红可持续性或红利陷阱检查时触发。默认投资者为 HK resident individual，普通券商账户，优先使用 IBKR 等券商实际流水。与 buffett-analysis 的护城河和再投资跑道分析、miao-ddm-strategy 的估值锚层级判定互补；本技能专注税后现金分红收入的基本面来源、净收益率、可持续性和红利买入区间。
---

# Dividend Income Equity Analysis Skill

## 技能定位

本技能用于分析上市公司的现金分红价值，重点关注公司业务和盈利的长期走势、税前股息率、净股息率、逐年股息变化、现金流覆盖、管理层资本分配、回购质量、未来三年基本面与分红跑道，以及基于历史价格和基本面推导的预期买入区间。

## 默认假设

- 投资者为 HK resident individual。
- 使用普通券商账户持有股票。
- 投资目标是中长期现金分红收入。
- 如果用户提供券商流水，券商实际扣税记录优先于理论分类。
- 本技能默认不处理内地个人港股通渠道，除非用户明确要求。

## 支撑文件读取规则

执行分析时按需读取同目录文件：

- `workflow.md`：完整研究流程、数据源和红利陷阱检查。数据源优先级以该文件为准。
- `business-fundamentals.md`：业务驱动、长期基本面趋势、行业化三年预测、可分配现金和 DPS 推导规则。完整分析必须读取。
- `visual-output-rules.md`：能力分层渲染、标准图、年度分红轨迹、基本面预测图、现金流覆盖桥、TTM vs normalized yield、三年分红跑道。完整分析必须读取。
- `buy-zone.md`：基于历史价格、历史股息率、基本面推导的 normalized / bear DPS、税后目标收益率和安全边际推导预期买入区间。涉及买入价、买入区间、目标入场价或估值锚时必须读取。
- `withholding-notes.md`：预扣税和券商实测扣税规则，是税务处理唯一权威源。
- `scoring.md`：100 分评分模型和评分锚点。
- `output-template.md`：最终输出唯一章节结构来源。完整分析必须严格按该文件的全部章节输出；缺少 Key Metrics at a Glance、Business Fundamentals and Long-Term Trend、Dividend Trajectory、Historical Cash-Flow Coverage Bridge、Three-Year Fundamental Forecast、Dividend Forecast Bridge、Three-Year Dividend Runway、Dividend Trap Checklist、Expected Buy Zone、Visual Summary 或 Required Ratings 视为输出不完整。
- `schema.json`：仅当用户要求结构化输出、JSON 输出或机器可读结果时使用。
- `examples/example-output-skeleton.md`：输出样例骨架。

## 执行原则

- 报价、派息、财务和经营数据必须注明 as-of date。
- 普通股息、特别股息、可变股息、REIT 分派和基金分派必须分开。
- 不得把一次性特别股息年化为持续收入。
- 必须识别真正为分红提供资金的业务和现金流来源。
- 必须分析至少五年的业务、利润、现金流和每股经济趋势；周期行业应尽量覆盖完整周期。
- 未来三年 DPS 不得作为独立假设直接输入。必须先预测业务驱动、盈利、OCF、Capex、FCF / 可分配现金，再结合债务、监管资本、必要再投资、派息政策和稀释后股数推导 DPS。
- Bear / Base / Bull 场景必须由明确的经营驱动变化产生，不得只对历史 DPS 做任意百分比调整。
- 必须用表格展示逐年 DPS、DPS YoY、历史股息率、派息率、现金流覆盖、基本面预测和 Dividend Forecast Bridge。
- 必须根据输出能力提供标准图或文本降级视图。
- 必须先检查红利陷阱，再基于基本面推导的 normalized net DPS、bear net DPS、目标税后收益率、历史股息率区间和安全边际推导预期买入区间。
- 不得把高 TTM 股息率、历史 DPS 平均值或 peak-cycle DPS 直接当作未来 DPS 和买入价依据。
- 如果无法从经营基本面负责任地预测未来分红，必须把 DPS 场景标注为 illustrative rather than evidence-backed，并降低 Forecast Confidence。
- 必须输出 `scoring.md` 要求的六项 Required Ratings，以及 Fundamental Trend 和 Forecast Confidence。
- 最终结论必须区分事实、假设和判断。

## 输出结构

完整分析的章节结构以 `output-template.md` 为唯一事实源，不要自行缩减、重排或用本文件重新定义章节列表。
