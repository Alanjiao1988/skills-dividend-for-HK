---
name: dividend-income-equity-analysis
description: "研究港股、美股及其他上市股票的股息安全、现金流、成长性、估值与买入价格；适用于长期收息分析、行业比较、更新研究报告或按新财报复核派息安全。覆盖银行、保险、能源、港口和航运等不同经济模式。Full Analysis 生成完整十二章中文 HTML。Use for dividend sustainability, long-term income, company growth, valuation, entry prices, payout safety and earnings-based report updates. Do not use for unrelated programming, ordinary documents, general business research, or financial-term definitions alone. 不要用于无关编程、普通文档任务、一般商业研究或仅解释金融术语。"
metadata:
  source_repository: https://github.com/Alanjiao1988/skills-dividend-for-HK
  source_kind: canonical_repository
  upstream_synced_commit: 2811ffacc1679297e55bb1cf5383f8e5d3bc6a75
  report_structure: twelve_section_full_report
  schema_version: '3.0'
  scoring_rubric: '2'
  presentation_revision: html-2
  default_report_format: single_file_html
---

# Dividend Income Equity Analysis Skill

## 技能定位

报告输出默认遵循 `report-language.md`：标题、正文、表头、图表说明、结论和发布摘要使用简体中文；JSON 键／固定枚举、股票代码和正式来源名称保留原样。该规则覆盖所有模式和轻量指令包，除非用户明确要求其他语言。

用户要求生成或更新报告时，默认实际生成一份可独立打开的 `.html` 文件，而不是只在聊天中输出正文、HTML代码块或Markdown文件。使用 `output-template.md` 的“单文件 HTML 交付契约”和 `templates/report.html`；CSS、图表和正文内嵌，离线可读。简短追问、解释和局部审计仍可在聊天中回答，除非用户要求报告；用户明确指定其他格式或只在聊天中回答时可覆盖默认值。

本技能用于分析上市公司的税后现金分红价值，连接未来三至五年业务发展、经常性股东现金流、行业资本约束、成长质量、派息政策、估值和持仓复评。收息适配与成长价值分别回答，不以成长抵消用户明确的最低现金收益要求。

## 默认假设

- 投资者为 HK resident individual。
- 使用普通券商账户。
- 投资目标是中长期现金分红收入与资本保护。
- 用户可覆盖投资者身份和渠道。有效券商流水证明对应事件的实际现金与扣税；未来处理另按当前公告和托管链核实，不自动沿用历史税率。
- 默认不处理内地个人港股通渠道，除非用户明确要求。
- 不预设 Screen Mode 的最低税后收益率。筛选目标只能来自用户明确要求或已明确建立且适用于本次筛选的组合目标；否则标记为 `Not Assessed`。

## 工具与取数

参考文件及脚本路径相对于本 `SKILL.md` 所在技能目录，而非调用时的工作目录。根据当前环境实际可用的搜索、浏览或连接器查阅发行人和交易所等来源；不能联网或无法访问时明确记录数据缺口、来源日期及对结论的影响，不得编造实时价格、财报或来源。校验和渲染不需要 API Key；本技能不会执行交易或修改券商持仓。

## 模式选择

- `Screen Mode`：筛选、快速评估、初步分析、批量比较、候选池或是否值得深入研究。
- `Safety Review Mode`：只要求依据新财报、派息或资本事件，核对相对上次有来源复评的分红安全变化；采用 `safety-review.md` 的轻量只读流程。
- `Full Analysis Mode`：完整分析、未来三至五年展望、FCF或分红预测、买点、现在能否买、建仓／加仓价格、完整评分评级、详细基本面、持仓复评或具体投资决策。
- 买点、入场行动或完整评分请求优先于“快速”及多个 ticker 的默认筛选路由；不得用 Screen 的限制回避问题。多个 ticker 且未请求这些完整分析内容时，默认 Screen Mode。

Screen Mode 必须读取 `screen-mode.md`，且不得输出三至五年预测、N/B、成长估值、买入区间、减仓价格、Strong Buy 或最终评分；不继承 Full Analysis 新增的分析记录。

Screen Mode 不得把 `buy-zone.md` 的标的必要收益率当作用户的筛选收益率目标，也不得凭空判断某个收益率“明显不足”。

用户只要求核查现有 N/B、正常化股息或行动标签时，执行局部审计，不编造完整公司报告，也不新增估值模式。按 `data-conventions.md` 输出算术结论、证据／行动结论和四行证据清单；即使要求简短，也须区分经营现金、资金约束、派息政策、有权股数的已知与缺失证据，不能只写“需要股息桥”。

机器模式为 `screen`、`full_analysis`、`safety_review`；局部正常化审计不是第四种模式。各任务的最小工作量以 `analysis-quality.md` 的任务矩阵为准。

## 支撑文件读取规则

- `report-language.md`：所有模式共用的中文报告语言与机器字段保留规则。

- `data-conventions.md`：各模式按需使用的期间、币种、每股单位、公司行动、补数顺序、有据估计及缺口影响范围。
- `portfolio-context.md`：沿用此前组合目标时读取，核实来源、账户／税务／收入期间及有效性；百分比收益率筛选不要求完整持仓。
- `publishing.md`：用户要求保存、修复或发布归档报告时读取，定义报告索引、摘要、版本链和本地验证流程。
- `examples/calculation-checks.md`：维护计算及决策规则时使用的虚构验收案例。
- `examples/worked-examples.md` 及 `examples/ordinary.analysis.json`、`examples/growth.analysis.json`：需要完整结构化示例时读取，均为虚构公司，不提供真实市场建议。

- `full-analysis.md`：每次 Full Analysis 必须完整读取的执行原则与详细检查。
- `screen-mode.md`：轻量筛选、筛选收益率目标、Yield Fit 和 Yes / Watch / No 的唯一规则源。
- `safety-review.md`：轻量安全复评的基准／事件、现金资本变化、覆盖率、结论与升级条件的唯一规则源。
- `analysis-quality.md`：本机保留的正常化状态账本、控制人风险、独立质量／角色、实际购买力、经济汇率风险和收入驱动记录；质量字段须与 `scoring.md` 的统一评分及区间契约一致，不另设缺项取消总评规则。
- `workflow.md`：模式路由、完整研究流程和数据源优先级。
- `economic-profile.md`：七维经济特征档案（收入引擎、资产寿命、周期性、资产负债表角色、资本强度、法律／分派结构、现金归属），决定现金模型、估值处理、压力测试和税务路线；新行业无需新增规则。
- `industry-analysis.md`：行业结构、价值链、供需周期、竞争与同行比较；行业KPI表为速查参考，不是白名单。
- `historical-financial-trends.md`：强制五年财务与经营趋势、现金流恶化识别、异常归因和趋势状态。
- `business-outlook.md`：三至五年发展展望、竞争格局、增长项目、资本需求、情景假设与可证伪里程碑。
- `business-fundamentals.md`：Recurring Owner FCF → Recurring FAD、五年情景预测、派息计算基数、敏感性分类、scrip / DRIP 和 DPS 推导。
- `sector-fcf-proxies.md`：银行、保险、REIT、公用事业、控股公司等行业代理与资本／上缴现金证据的唯一规则源。
- `visual-output-rules.md`：Full Analysis 的图表和表格规则。
- `buy-zone.md`：含第 7A 节银行等资本回报型公司的有形净资产估值（`capital_return_based`）；独立必要回报、N/B收息区间、有条件的成长估值、试建仓／加仓／强买价格、当前行动、催化与失效条件、Structural Decline及有限期现金回收。
- `holding-review.md`：持有、复评、减仓、退出、换仓的证据与组合约束；不自动交易。
- `withholding-notes.md`：预扣税、PIL、scrip / DRIP 税务与现金收入规则。
- `scoring.md`：价格独立的质量／85、收入吸引力／15、逐项可复算评分、暂定区间／证据覆盖度、评级依据及 Structural Decline overlay。不以总分自动决定组合角色。
- `output-template.md`：读者可见内容的唯一事实源：单文件 HTML 交付、Screen／Safety Review 输出、Full Analysis 十二章完整报告、无固定篇幅限制和默认审计附录 A1–A13。
- `templates/report.html`：所有报告模式共用的单文件 HTML 外壳；按 `output-template.md` 填入实际内容，不交付占位模板。
- `schema.json`：默认 3.0 版 JSON，完整分析必须包含 rubric 2 的 `scorecard.summary`、`rating_audit`、`entry_plan` 及第1章状态行的评分区间；旧 2.3／2.4／2.5 按原契约兼容读取。
- `examples/example-output-skeleton.md`：Full Analysis 十二章完整报告示例骨架（篇幅与密度参考）。
- `scripts/decision_rules.py`、`scripts/validate_analysis.py`：已随本机技能安装的评分／分层买点计算和跨字段校验；路径相对于技能目录，不依赖源码仓库仍在原位置。

## Screen Mode 执行原则

- 筛选收益率目标优先使用用户本次明确提供的目标，其次使用明确适用的组合目标；否则为 `Not Assessed`。
- 只有用户明确说是最低要求、硬门槛或淘汰线时，目标政策才是 `hard_minimum`；其他目标均视为 `preference`。
- 没有目标时，Yield Fit 必须为 `Not Assessed`，不得仅因收益率看起来较低而判 `No`。
- 低于 preference 目标时，收益率本身不得单独导致 `No`；应结合有证据支持的股息增长路径决定 `Yes` 或 `Watch`。
- 低于用户明确的 hard minimum 时，除非用户允许例外，否则判 `No`。

## Safety Review 执行原则

- 按 `safety-review.md` 对照有日期和来源的旧基准与新披露，核对同期间、同权益范围的现金与资本变化；不要求完整个人持仓导出。
- 缺少可比基准不得声称“维持／改善”；缺少当前关键现金能力时安全性为 `Unclear`，说明缺失披露，不把未知当作困境或安全。
- 结构变化、未解决资金缺口或 veto 要求升级完整复评，不自动卖出；不生成新 N/B、五年预测、估值、评分、等级或交易仓位，`automatic_trade: false`。

## Full Analysis 执行原则

每次 Full Analysis 必须完整读取 `full-analysis.md` 及其中指定的参考文件；该文件保留全部研究步骤、验证、分层买点、暂定区间和禁止中性补分的要求，不因平台或上下文限制减少。必须保留 Schema 3.0、rubric 2、十二章正文、五年预测与 A1–A13 审计附录。

所有模式使用 `evidence_recovery` 记录逐项取数轨迹，使用 `report_output` 记录中文读者可见内容；Full Analysis 另需 `decision`。旧 2.3／2.4／2.5 记录不追溯新增字段。

## 输出结构

输出模式、单文件 HTML 交付方式和章节结构以 `output-template.md` 为唯一事实源。Full Analysis 默认采用完整十二章结构：摘要与投资结论、公司概况与行业定位、行业结构与周期、竞争格局、五年财务趋势、现金流与股息质量、成长性与资本配置、未来五年预测、估值与预期总回报、买点与建仓、风险与论点证伪、来源与研究限制。不得退化为六节摘要，也不得把核心行业分析、成长分析、财务趋势或买点分析隐藏到用户另行索取的附录。

报告不设固定字数、表格数量或图表数量上限；按公司复杂度呈现必要数据。表格和图表必须帮助读者核对关键数值，不能替代解释。所有核心判断在正文中可见，审计附录补充来源、公式、调整桥和敏感性。Screen 与 Safety Review 仍保持轻量，不继承 Full Analysis 的完整章节要求。

HTML 是交付格式，不是第四种分析模式；新报告使用 Schema 3.0、scoring rubric 2 和 `html-2` 呈现版本。行业模型必须按发行人实际业务动态选择，不得把 BTI 或任何单一行业作为默认模板；行业示例不是封闭白名单；旧 2.3／2.4／2.5 数据按原契约读取，不自动改写或重新评估。

本地校验：以技能目录为工作目录，运行 `python -B scripts/validate_analysis.py <分析JSON路径>`；渲染运行 `python -B scripts/render_report.py <分析JSON路径> <输出HTML路径>`。若缺依赖，在技能目录用 pip 安装 `requirements-dev.txt` 中的依赖。校验只能证明结构与算术一致，不能证明来源真实或投资安全；仓库级测试见项目 README。

## 报告保存与仓库边界

- 本仓库只维护可复用的分析规则、模板、schema 和工具，不用于归档具体公司的研究报告。
- 报告请求已包含本地 HTML 文件交付，不需要用户再次说“保存”；聊天只给简短摘要、实际文件链接及路径，不用长篇正文或代码块代替文件。默认只交付一份 HTML，不额外输出 Markdown、PDF、JSON 或资源文件夹；结构化 JSON 仅在明确请求或验证需要时生成，临时验证文件不作为额外交付物。
- 临时报告、下载的披露资料、券商流水和生成的图表应放在会话工作区或用户指定的仓库外目录，不写入技能源码目录。
- 完整报告的独立归档仓库仍为 `Alanjiao1988/Dividendreport`，按 ticker 和数据基准日归档。遵循 `publishing.md`，核对 company、ticker、exchange、as-of date、HTML兼容性与授权范围；生成本地文件不等于已经推送，不启用 GitHub Actions 或 GitHub Pages。
- `output-template.md`、`templates/report.html` 和 `examples/example-output-skeleton.md` 必须保持为可复用模板或占位示例，不得用真实公司报告覆盖。
