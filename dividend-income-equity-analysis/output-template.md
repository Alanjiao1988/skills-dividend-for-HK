# 中文报告输出模板

按 `report-language.md` 生成中文报告。下列英文说明用于定义计算与结构，不要求读者可见内容使用英文；机器字段与固定枚举保持原样。

This file is the single source of truth for **what the reader sees**: output modes, the six-section Full Analysis main report, its length budget and the on-request Audit Appendix. The other modules (screen, safety-review, analytical-quality, outlook, cash-flow, sector, valuation, scoring, visual and holding-review) define **what must be worked out**: the research, calculations, gates and JSON records. Do the full analysis, but report only what changes the reader's decision.

When another module says "show", "print", "display" or "include" for Full Analysis, it means: complete that work, keep it consistent with the report, store it in JSON when machine-readable output is requested, and place it in the Audit Appendix. It enters the main report only where this file puts it.

## 单文件 HTML 交付契约

- 报告默认交付一份真实的 `.html` 文件，使用 `templates/report.html` 作为外壳；不以聊天正文、代码块、Markdown附件、截图或指向外部资料的空壳网页代替完整报告。用户明确要求其他格式或只在聊天中回答时可覆盖。一般解释和不要求报告的局部审计不强制生成文件。
- 三种模式均使用同一外壳。Full Analysis 将下面的六节主报告按顺序写入静态正文，每节用唯一 `id` 的 `<section>` 和中文 `<h2>`；目录、页眉、免责声明不增加第七节。用户要求审计附录时，在第6节之后追加一个 `id="audit-appendix"` 的 `<section>`，标题为“审计附录”，只含相关的 A1–A13 子节（`<h3>`），并加入目录；未要求时不输出附录，只在第6节末尾用一行说明可按需提供。Screen 多标的结果合并在同一文件，保留筛选字段和限制；Safety Review 保留轻量现金／资本复检结构，不借HTML模板引入估值、评分或交易指令。
- 外壳占位符：`{{REPORT_TITLE}}` 用HTML转义后的中文标题替换全部出现位置；`{{REPORT_MODE}}` 仅为 `screen`、`full_analysis`、`safety_review`；`{{REPORT_METADATA}}` 为安全构造的公司／ticker／交易所、模式、数据截止日、报告生成时间、税务与币种假设、Schema 3.0／呈现版本 html-1 信息；`{{REPORT_NAV}}` 为指向真实章节ID的目录；`{{REPORT_BODY}}` 为完整静态语义HTML正文。解释性质的报告不增加机器模式，可省略模式属性。不得直接展示未替换的模板、示例公司、示意数字或空章节；缺失证据按既有规则明确写出限制。
- 正文、表格、证据链和来源直接存在于HTML中，不依赖JavaScript初始化或网络请求。使用语义化表格、列标题、可访问的图表说明和有效来源链接；来源链接可联网打开，但离线阅读报告本身不需要联网。图表可用内联SVG或内嵌图片，不能依赖外部脚本、CDN、字体、样式表、图片路径或同目录附件。无法画图时在HTML内保留文字与表格，不把文件降级为聊天输出。
- 使用外壳内嵌的 Clawpilot 明暗主题变量、字体与主题探测脚本；样式颜色使用 `var(--cp-*)`。保持移动端可读、宽表独立横向滚动、目录锚点和浏览器打印样式。不要用幻灯片翻页或仅交互可见的面板隐藏分析内容。核心结论、风险、缺失证据及来源始终可见；打印时不能丢失分析内容。
- 外部来源文本、公司名、表格值必须按HTML文本／属性上下文转义；链接只接受明确的 `https://`、`http://` 或文件内 `#` 锚点，不把 `javascript:`、源文件代码或外部网页HTML当作可执行内容。结构化JSON如嵌入，使用非执行 `application/json` 数据块并安全转义 `<` 等脚本终止字符；不得嵌入凭据、私有认证链接或原始券商身份资料。交互脚本仅做渐进增强，不加入网络调用或存储依赖。
- 新输出默认 Schema 3.0；2.3／2.4／2.5仅用于兼容旧记录，`presentation_revision: html-1` 仅标识外壳。`rendering.visual_mode` 描述图表能力而不是文件格式。有真实图表时用 `rich_charts`，仅静态文字／表格时仍用 `plain_text_fallback`。不新增 `html` 枚举，不因为HTML已生成就宣称数据核验通过。JSON并非默认额外文件；若确需结构化验证，使用授权工作目录内的中间记录并在交付后清理。JSON 始终承载完整分析记录，不受主报告篇幅预算影响。
- 用应用支持的文档／文件工具保存到用户指定位置或当前应用的默认文档位置，遵循文件权限和敏感数据约束，不写入技能安装目录、源码仓库或未授权的报告仓库。文件名包含可读的公司／报告主题与数据截止日；同名存在时加 `-2`、`-3`，只有明确更新指定文件时才覆盖。
- 交付前确认文件存在、UTF-8声明正确、没有遗留占位符、所有目录锚点有效、所选模式内容完整、正文可在无脚本情况下读取。能预览时检查明暗主题、窄屏表格和打印布局。聊天中提供简短中文摘要及实际文件链接／完整路径；不能写文件时明确说明阻碍和待操作步骤，不能声称已生成。推送按 `publishing.md` 单独处理，发布使用同一主报告，只有用户要求时才附审计附录。

## 主报告原则

1. **只回答四个问题。** 主报告回答：(a) 财务是否健康、分红是否由真实的经常性现金支付；(b) 现价是否是买点、什么价格开始成为买点；(c) 未来三至五年业务与股息走向；(d) 什么会打破论点、如何提前发现。不改变这四个答案的内容进入审计附录或省略。
2. **结论先行。** 每节以一句加粗判断开头，随后的数字和要点只作支撑，不复述判断。
3. **每个数字只出现一次。** 同一数字在主报告只出现在一处，其后章节按名称引用。
4. **通俗表述。** 主报告不出现 schema 字段名、公式、规则复述、方法说明或清单行；使用下方通俗标签。只在读者理解结论所必需时用一个分句解释方法。
5. **不打印占位行。** 不打印只有 N/A、Unknown 或“无法估计”的行或单元格；缺失输入集中写在第6节“数据缺口”一行，并说明其后果（例如“因此买点仅供参考”）。
6. **事实与估计紧凑区分。** 分析师估计标注 `（估）`，公司指引标注 `（指引）`；未标注的数字为已披露事实。第6节列出结论最依赖的少数假设。
7. **只写一次免责声明。** 研究而非建议、现金收益区间不计股息增长这两条限制在第6节写一次，不在每张表下重复。
8. **语言。** 遵循 `report-language.md`，默认简体中文；价格和股息总是注明币种、单位和截至日期。
9. **篇幅预算（Length budget）。** 主报告约 1,200–2,000 个汉字（不含表格）；最多五张表，每表最多六列、八行；可渲染时最多三张图。超出预算时删减解释和重复，绝不删减判断、关键数字和已命名的风险。
10. **分析不因呈现精简而减少。** `workflow.md` Steps 1–12、`analysis-quality.md` 的必需记录、评分与入场门槛全部照常完成；主报告只是其提炼，不是逐步记录。

### 主报告通俗标签

| 内部术语 | 主报告标签 |
|---|---|
| `ordinary_yield_based` | 收息定价 |
| `total_return_based` | 股息增长估值 |
| `finite_life_harvest` | 有限期现金回收 |
| `suspended` | 当前明确不买，列出解除事件与失效条件 |
| Recurring FAD | 可持续可分配现金 |
| N / B | 正常化股息 / 压力情景股息 |
| Value-Trap Veto Not triggered / Triggered / Unclear | 红利陷阱：未触发 / 已触发 / 存在未解除的风险约束（列具体事项） |
| Forecast Confidence High / Medium / Low / Not Forecastable | 预测可信度：高 / 中 / 低 / 无法预测 |
| `action_assessment` eligible / diagnostic_only / suspended | 可执行 / 仅供参考 / 暂停 |
| `entry_plan` 阶段 starter / add / strong_buy | 初始建仓 / 逐步增持 / 强力买入 |
| 阶段状态 ready / waiting_price / waiting_evidence / unavailable | 已就绪 / 等价格 / 等证据 / 暂不可用 |
| Cash-income bands | `buy-zone.md` 中的中文区间名称 |
| Sensitivity transient / persistent / structural | 暂时性 / 持续性 / 结构性 |

## 模式选择

### 轻量筛选（Screen）

When Screen Mode is triggered, follow `screen-mode.md` only. Do not produce the Full Analysis main report or Audit Appendix.

Required banner:

```text
模式：轻量筛选（Screen）
筛选税后股息率目标：x.x%／暂不评估（Not Assessed）
目标来源：用户明确要求／适用组合目标／暂不评估
目标政策：硬性最低要求／偏好／暂不评估
预测置信度：暂不评估（Not Assessed）
买入区间：暂不评估（Not Assessed）
本结果仅用于初步筛选，不构成完整投资分析。
```

For each ticker, output the compact screening fields, including:

- Paid TTM net yield and selected screening yield/basis/range (not normalized N).
- Screening net-yield target.
- Yield Fit: Pass / Below target / Unclear / Not Assessed.
- Yield Gap in percentage points or N/A.
- Documented dividend-growth path: Yes / No / Unclear.
- `Full Analysis Recommended: Yes / Watch / No`.

Do not infer a screening target from `buy-zone.md`. If no target is available, use `Not Assessed` and do not reject a stock solely because its yield appears low.

Screen output does not inherit the new full-only analytical records in `analysis-quality.md`.

### 股息安全性复检（Safety Review）

Follow `safety-review.md`, not the Full Analysis structure. Output identity/as-of date/sources, the dated baseline and new disclosure, comparable cash/capital deltas, cash-paid and full-cash-entitlement coverage/gaps, safety/decision, missing inputs and escalation/next review. The minimal schema 3.0 envelope is `mode: safety_review` plus `review`, with optional `controller_risk`; schema 2.4 remains a legacy-compatible envelope.

Without a comparable baseline use `not_comparable`; without current critical capacity use safety `Unclear`. No new N/B, five-year forecast, valuation, score, grade or trade size. Structural change or unresolved funding/veto means full reassessment, not automatic selling; `automatic_trade: false`.

### 局部审计（Focused Audit）

When the user asks to audit a proposed normalized DPS, N/B or its action label, use the compact four-link contract in `data-conventions.md`. It is not another mode and not a reason to fabricate the Full Analysis report.

### 完整分析（Full Analysis）

The main report has the six numbered sections below, in this order. The Audit Appendix follows only when requested. Integrate the conclusions of the required records in `analysis-quality.md` at the locations named in its placement table; their full records belong to the appendix and JSON.

Default Full Analysis machine output uses schema 3.0 and includes rubric-2 `scorecard.summary`, `rating_audit` and `entry_plan`. These must be fully worked out for every Full Analysis; the readable reasoning is shown in appendix parts A10–A11 when requested, and a JSON field alone does not replace that reasoning. Recover evidence before choosing an unavailable state. Missing one module does not cancel the report or the supported score interval; genuine cash, tax or capital gaps separately restrict entry.

## 1. 结论速览

最多三句：这家公司作为股息资产是什么、股息是否安全、现价能否买及原因。单一当前动作来自固定枚举：立即买入／分批建仓／等待到价／继续观察／回避，不得并列两个动作。先写当前行动及其决定性原因，而不是泛泛的风险声明。

| 现价（日期） | 税后股息率 TTM | 正常化税后股息率 | 3年股息覆盖 | 买点 | 当前位置 |
|---|---:|---:|---:|---|---|
| | | | | | |

- “买点”给出初始建仓、逐步增持、强力买入三档参考价与收入约束上限（`income-capped`）。资金门槛不通过、不能形成可执行买价时，写“当前明确不买”，同时给出具体等待价格或具体可观测解除事件及失效条件；降价本身不能解除现金、税务或资本缺口。不得连评分一起留空。
- “当前位置”是现金收入区间名称，或处于成长价值区间之上／之内／之下。
- 正常化收益率为有依据的不确定区间时写 `x–y%` 并注明口径；周期低／高状态不是可互换的 N。暂定的经常性收入代理不得显示为正常化收益率。

一行状态：

`行动：… ｜ 预测可信度：… ｜ 红利陷阱：… ｜ 质量：xx/85 ｜ 综合评分：xx/100（等级）｜ 组合角色：…`

- 评分全部模块有依据时写单点。存在有界或缺失模块时写暂定区间及覆盖度，例如 `质量：57-67/85 ｜ 综合评分：暂定 71-81/100（B，暂定；覆盖度 90%）`；两端评级不同时写评级范围。所有模块均无依据时仍展示质量区间／85、组合区间／100、等级区间与覆盖度 0%，明确这是未收窄的方法界限而非公司得零分，禁止中性补分或用其排序。
- 质量／85 取自 `scorecard.summary`，是价格独立的质量标题；综合 /100 与等级是次要信息，不能代替买入结论。股价下跌本身不提升质量或组合角色。
- 模块分、候选档位、覆盖权重和评级审计进入附录 A11。

## 2. 财务状况

**开篇判断：** 分红是否由经常性现金真实支付，资产负债或资本状况是否构成约束。

一张五年表（最近可比年份；不足五年按实际）：

| 财年 | 收入 / 行业核心指标 | 归母净利润 | 可持续可分配现金 | 每股股息 | 现金覆盖 |
|---|---:|---:|---:|---:|---:|

以上为默认列。最多六列，按证据选择（例如可持续与实际可分配现金出现背离时并列两者），宁可删列也不填 N/A。银行、保险、REIT、公用事业和控股公司改用 `sector-fcf-proxies.md` 的行业口径（资本生成、上缴现金、AFFO 等）。

然后三到五条要点，每条带数字和判断：

- **利润与现金质量：** 趋势、现金转化、剔除的一次性项目。
- **分红资金来源：** 三年累计覆盖、最差年度，以及任何缺口是否由负债、出售资产、以股代息或现金余额弥补。
- **资产负债与资本：** 杠杆或监管资本、再融资需求，必要时母公司上缴现金。
- **每股影响：** 期间增发或回购对股本的净影响。
- **投资者到手现金：** 预扣税率及依据、以股代息／DRIP 选择假设，一行写完；经济汇率敞口重要时在同一行说明方向和量级。
- **控股股东：** 仅当控股股东风险重要或存在未解决的潜在重大损害时加一行；控股股东资金需求本身不等于损害。

## 3. 买点观点

3.0 的 `decision` 必须回答三问：`can_buy_now` 是／否及 `reason`；`buy_conditions` 给具体数字或可观测事件（全部满足）；`invalidation_conditions` 给失效阈值或事件（任一触发）。价格条件注明报告估值币种，事件条件注明可查公告／指标、阈值、观察来源。禁止“补齐资金证据后”等空话。`reference_prices` 从已审计 `entry_plan` 投影，不能手填另一套买价；`price_status: blocked` 明确不买、空价格不是空结论，也不得隐藏已有可用参考价。

保留有限期现金回收例外：该模式只允许初始建仓参考价和收入约束上限，另两档明确“不适用”，不得为凑三档而发明强买或增持价格。普通收息和成长估值仍需三档数值。

**开篇判断：** 现价处于什么位置、什么价格开始有吸引力，用通俗语言写。

先用一两行给出估值边界：

- 收息定价：写出三个区间边界价格及现价所处的区间名称；可渲染时以现金收入阶梯图展示并标出现价（计入图表预算），完整价格阶梯表进入附录 A10。
- 股息增长估值：一行写 Bear / Base / Bull 价值、安全折扣后的入场上限、估值复评价位和终值占 Base 价值的比例；可信时另起一行写收息比较。成长价值不能豁免用户明确的最低现金收益要求。
- 有限期现金回收：回收期限、折现率（不低于 10%）和价值区间各一行。

然后是本节唯一的表，分阶段入场决策卡（取自 `entry_plan`，与 `buy-zone.md` Sections 5.2–5.3 一致）：

| 阶段 | 估值价格 | 收息约束后价格 | 相对现价 | 状态与条件 |
|---|---:|---:|---:|---|
| 初始建仓 | | | | |
| 逐步增持 | | | | |
| 强力买入 | | | | |

- 成长模型的 Base 支持试建仓价与严格压力折扣的 `entry_upper` 分开写，不能把强买价当成唯一可以买的价格。
- 某阶段证据缺失时在“状态与条件”写“等证据”及所需文件，不写投机性目标价；不打印只有占位的行。

最多四条要点：

- **要求回报：** 无风险锚加风险溢价得到要求税后收益率区间，一行写明日期和币种；说明用户明确的收入目标或“暂不评估”。
- **行动与条件：** 独立的行动状态（可执行 / 仅供参考 / 暂停）、为何可以或不可以强力买入、是在等价格还是等证据，以及会改变行动的具体证据或价格；同时点明 Bear 情景本金风险。
- **买点背后的证据缺口：** 若经营现金、资金能力、派息政策、有权股数四条链中有缺失或冲突，用一行点名；全部有据时省略。
- **持仓复评：** 仅当用户持有或询问持有、卖出、换仓时写：复评触发条件、价位和研究动作。不编造仓位。

估值暂停时：不写价格边界和入场卡价格；用不超过三条要点说明原因和重新估值的条件，并写明 `估值模式：暂停（suspended）`。结构性衰退且不满足有限期回收例外时，不输出普通收息阶梯、成长入场区间或强力买入。

## 4. 长期展望：业务与股息

**开篇判断：** 三至五年后每股现金和股息可能更高、持平还是更低，以及主要原因。

- **业务驱动：** 两到四条，每条写明驱动因素或业务分部、FY+3／FY+5 的方向及数字或区间、属于已承诺还是可选项目，以及证据；与 `analysis-quality.md` 的一两个收入驱动标签一致。
- **股息展望表：**

| 情景 | 核心假设 | FY+1 DPS | FY+3 DPS | FY+5 DPS | FY+1–3 覆盖 |
|---|---|---:|---:|---:|---:|
| 悲观 Bear | | | | | |
| 基准 Base | | | | | |
| 乐观 Bull | | | | | |

  无依据的远期单元格留空，并在第6节统一说明一次。
- **派息政策与股息增长：** 政策及其计算基数、预期 DPS 增长区间、派息余量或资金缺口，一到两行；有依据时用一个分句说明实际购买力（扣除通胀后的实际收入）趋势。

## 5. 风险点与跟踪信号

**开篇判断：** 红利陷阱结果（未触发 / 已触发 / 待确认）以及对股息最大的单一风险。

| 风险 | 早期信号（可观察指标 / 阈值） | 对股息的影响 | 性质 | 下次检查 |
|---|---|---|---|---|

- 三到五个公司特有风险，按对股息的影响排序。每项需要一个带阈值的可观察信号（阈值取自模型或披露）、量化或定向的股息影响，以及性质标签（暂时性 / 持续性 / 结构性）。
- 纳入所有被标记或待确认的红利陷阱项目（包括重大控股股东损害、无依据的重大经济汇率敞口）；已通过的项目省略。除非量化了对本股息的影响，不列市场波动、宏观不确定等泛泛风险。
- 必要时用一行写出确认 Base 情景的里程碑。

## 6. 数据来源与关键假设

- **数据截至：** 研究截止日、价格日期及来源。
- **主要来源：** 最多五个关键官方来源；完整清单进入附录 A13。
- **关键假设：** 结论最依赖的最多五个假设，逐项标注事实、指引或估计。
- **数据缺口：** 一行列出缺失的重要输入及其对可信度或买点的影响。
- **说明：** 一行：仅为研究，不构成个人投资或税务建议；现金收益区间未计入股息增长，不是完整的内在价值估计。

未要求附录时，以一行结束：可按需提供审计附录（现金流桥、五年逐年预测、敏感性、陷阱清单、估值与评分明细等）。

## Audit Appendix（审计附录，按需）

Output the appendix only when the user asks for detailed workings, full calculations, an audit trail, an appendix, score detail or the complete model. Otherwise end after Section 6 with the one-line offer above. JSON output (`schema.json`) always carries the full records regardless of what the report displays. Saving or publishing a report (`publishing.md`) uses the same main report; include the appendix only when requested.

When shown, the appendix uses these parts under a single `审计附录` heading (`id="audit-appendix"`), each following its canonical module and the appendix table rules in `visual-output-rules.md`. Include only the parts relevant to the question; do not print empty parts. A focused request (for example “只看评分明细”) prints only that part.

- **A1. 上市结构与股息税务：** domicile, listing venue, security type, dividend and reporting currencies, official and dividend-entitled share count; withholding rate, basis, broker-observed status and broker cash-line type (`withholding-notes.md`); scrip/DRIP availability, default election, all-cash assumption and tax/broker/fractional-share/dilution uncertainty. Identify the ultimate controller, or sourced absence of one, distinguishing the listed issuer's controlling parent from its subsidiaries.
- **A2. 股息轨迹：** per-share DPS structure and yearly yield/coverage tables with quality tags and a Dividend Pattern note (`visual-output-rules.md` Section 4). Show `real_income` separately: comparable net cash per constant split-adjusted entitlement, consumption basket/index, actual dates and elapsed years, nominal/inflation/exact real CAGR, tolerance and trend or the missing inputs; nominal stability is not real purchasing-power growth.
- **A3. 历史现金流覆盖桥：** reported FCF/proxy to Recurring Owner FCF and Recurring FAD and actual cash affordability, once-only deduction ledger, cash return and funding sources (recurring cash, cash balance, asset sales, debt, equity or mixed), three-year aggregate, five-year worst recurring and worst actual coverage with year; insufficient or comparability-limited histories.
- **A4. 资本配置与回购质量：** payout-policy type and exact earnings/cash/DPS calculation base, source and constraints; reinvestment, leverage, acquisitions, ordinary issuance, ATM, scrip/DRIP; true diluted-share change and whether buybacks create value, offset issuance, neutralize scrip or are debt-funded. The sourced `controller_risk` assessment and listed-company impact under `analysis-quality.md`, reused in A9 and A12; controller cash demand alone is not material harm or a veto.
- **A5. 业务展望明细：** dividend funding engine, historical operating trend with sector KPIs, Fundamental Trend, three to five core drivers, structural/cyclical/competitive/regulatory/capital-intensity factors, development-thesis table, segment baselines, FY+3/FY+5 outcomes, management delivery, project timing, dated invalidation milestones, sector proxy and holding-company overlay (`business-fundamentals.md`, `business-outlook.md`, `sector-fcf-proxies.md`). The one or two `income_drivers` tags and the economic currency-to-remittable-cash/payout/investor map; do not infer exposure solely from listing or reporting currency.
- **A6. 五年预测：** annual Bear/Base/Bull operating and FCF forecasts for FY+1 to FY+3 and supported FY+4/FY+5 extensions; working capital, maintenance/growth investment, owner claims, financing/capital needs, total/per-share cash outlook, cumulative FAD, cash-conversion timing and liquidity trough; FCF change decomposed by driver; unsupported years as null with reasons (`business-fundamentals.md` Sections 6 and 8). Include `fx_risk`'s paired FX-only and combined-Bear stress for the same supported year, or the gap and diagnostic restriction.
- **A7. 敏感性：** three to five single-driver rows, each typed transient/persistent/structural with its evidence basis. Transient: normalized high-end boundary change N/A, affected-year discounted cash impact shown separately in growth valuation. Persistent: recalculate normalized distributable cash and N first. Structural: `Rebuild required`. State local/nonlinear limitations.
- **A8. 分红预测推导与收益率路径：** Distributable-Cash Bridge, Recurring FAD versus total distribution capacity with separate exceptional uses and excess cash, deduction ledger, capital/remittance constraints, Share Count and Scrip/DRIP Assumptions, Forecast Confidence (`business-fundamentals.md` Section 7). Then the policy-entitlement table (Year / Scenario, Policy-Indicated Entitlement, Modeled Entitlement, Cash-Settled Fraction, Settlement Adjustment, All-Cash Funding Gap) and the single Dividend and Yield Runway from `visual-output-rules.md` Section 6, covering the same scenario-year keys as A6. Do not repeat Dividend Cash Cost or Derived DPS elsewhere.
- **A9. 红利陷阱清单：** every item from `workflow.md` Step 10 with status and evidence, including forecast DPS versus business and cash flow, normalized N basis, issuance and scrip dilution, Structural Decline without credible harvest logic, unsupported sector proxies or double deductions, growth relying on unfunded reinvestment or an unsupported terminal dividend, confirmed material controller harm (unresolved potential harm is an evidence gap, not presumed extraction) and material economic FX/remittance exposure without a supported cash-impact assessment. The checklist is a precondition for valuation.
- **A10. 估值与入场明细：** valuation mode and reason; the sourced risk-free anchor, currency/tenor/date/tax basis, price-independent premium range and required total return; explicit income target or Not Assessed. Ordinary mode: N and B values/basis/period/adjustments, DPS currency, normalization FX/fees, share/ADR entitlement and quote-unit conversion, r_low/r_high, optional `income_assessment.required_yield_spread`, the full cash-income band table and price ladder with the current price marked, historical price/yield context and veto status; caption that no dividend growth is credited. The four-row normalization evidence checklist from `data-conventions.md` and, whenever `buy_zone` is present, the `normalization_model` from `analysis-quality.md` (cycle/steady-state rationale and window, drivers, joint assumptions, perimeter adjustments, low/mid/high state ledger reconciled to N). Growth mode: dated dividend-path references to A8, reinvestment/ROIC or equity-retention/ROE or a supported direct bridge, horizon, transition, terminal DPS, bounded terminal growth, R-g spread, scenario PVs, terminal share, R/g sensitivity, safety discount, entry limit, review threshold, conditional hard-income price ceiling and terminal funding ledger. Finite-life mode: harvest horizon, annual net distributions, discount rate with 10% floor, residual value and basis, PV of distributions, value range and optional ordinary cross-check with r_low at least 10%. The complete `entry_plan`: three staged model and income-capped prices, signed distances, conditions, opportunity thesis, expectation gap, Bear/Base/Bull holding-period return table (entitled net cash, exit price, costs, cumulative return and basis, not annualized), principal-risk review, blockers and resolution sources, catalyst and invalidation conditions, and `action_assessment` shown independently of the cash-income band.
- **A11. 评分、评级与组合角色：** use `scoring.md` and show the complete seven-row scorecard (`模块／权重 | 输入／期间／证据类型 | 锚点档位／候选档位 | 检查／原始分 | 上限／最终分或区间 | 来源／缺口与恢复尝试`), not just module totals. Show `assessed`, `bounded` or `not_assessable` status and all three check results with specific evidence. Print the anchor band and `raw = band_floor + floor(band_width × met_checks / 3)`, then `final = min(raw, explicit_cap)` where a cap applies; evaluate candidate bands and unresolved checks at both bounded endpoints. Sum quality /85 and income /15 separately, then the combined /100 interval, with assessed subtotal/weight, bounded weight, missing weight and quality/overall coverage (for example 暂定综合评分 71-81/100；质量评分 57-67/85). Display a stable provisional Grade when both endpoints agree, otherwise the Grade range, and name the missing input that widens the range most. No imputed neutral points, rescaling, hidden discretion or repeated penalties; an unfinished forecast alone does not justify the lowest visibility band. For schema 3.0, keep `quality_assessment` with six-key `components`, nullable `score_85`, `evidence_and_limitations`, six-key `component_ranges`, `score_range = scorecard.summary.quality_range`, `coverage_pct = scorecard.summary.quality_coverage_pct`, `range_kind: rubric_bounds` and `price_independent: true`; a component point is its bound only when low equals high. Quality status is `assessed` only when all six quality modules are assessed with non-estimated evidence, `not_assessed` only when all six are `not_assessable`, otherwise `provisional`; estimated income evidence alone can make the overall score provisional without changing quality status. List Dividend Quality, Dividend Safety, Withholding Efficiency, Buyback Quality, Three-Year Dividend Outlook, Fundamental Trend, Forecast Confidence, Structural Decline cap, Harvest / Managed Runoff Exception and valuation mode, each with its `rating_audit` (label, decision rule, evidence/source, upgrade trigger, downgrade trigger). Structural Decline is the explicit Grade C cap. Then the Portfolio Role and `portfolio_role_assessment` with `basis: quality_safety_and_constraints`, rationale and `price_alone_changes_role: false`; a lower price alone changes neither quality /85 nor role, and a score or cash-income band is not an action recommendation.
- **A12. 持仓复评：** `holding-review.md` trigger table (thesis/cash/solvency triggers, valuation-review band, concentration/mandate constraints, research action, next evidence date), and for a proposed switch the named alternative, same-basis forward cash income/returns, taxes/fees/costs and documented improvement hurdle. A valuation band is not an automatic sell order; missing holdings or alternative information means no invented trade size or switch conclusion. When updating a prior assessment, embed the dated baseline/new-disclosure, cash/capital-change and escalation logic from `safety-review.md`; do not claim maintained or improved safety without a comparable baseline.
- **A13. 来源与数据质量：** the full source list (filings, announcements, operating statistics, guidance, broker records, price sources, cross-checks); missing, stale or restated data; every material forecast's source/date and confidence by horizon; unsupported later years; sector/cash reconciliation, payout basis, sensitivity types, scrip assumptions, N basis, rate/growth assumptions; whether future FCF/DPS is evidence-backed or illustrative; provenance and limitations of the `analysis-quality.md` records. A schema-valid record is not independent verification of the cited evidence.
