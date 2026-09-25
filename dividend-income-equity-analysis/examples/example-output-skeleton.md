# 中文报告示例骨架

读者可见的报告遵循 `report-language.md`。本文件保留少量英文维护说明，实际报告须使用中文正文、表头、图例和结论；固定枚举、代码和正式来源名称不翻译。

This shows the target length and density of a schema-3.0, rubric-2 Full Analysis main report. It uses the fictional Fictional Harbor Services case from `worked-examples.md` (assumptions A1-A8, cut-off 2026-01-01) and matches `ordinary.analysis.json`. It contains no market facts and no recommendation. Screen Mode uses `screen-mode.md`; a light disclosure update uses `safety-review.md` without new N/B, valuation, scores, grades or trade size. Full-only analytical records follow `analysis-quality.md`: they are always completed, their conclusions appear at the locations below, and the full records go to the Audit Appendix and JSON.

本文件是内容结构的维护用Markdown示例，不是默认交付格式。生成报告时按 `output-template.md` 的单文件HTML契约，将完成的六节主报告填入 `templates/report.html`；不要交付此示例或额外Markdown副本。

Teaching display only, for a provisional score: with 71 known points across 90 weight and only buyback quality missing, the status line reads `质量：57-67/85 ｜ 综合评分：暂定 71-81/100（B，暂定；覆盖度 90%）`. Only when no module has covered evidence after recovery may it state insufficient evidence, coverage 0%; that is not a 0/100 quality judgment. When entry evidence is missing, the Section 3 card shows `等证据` with the specific documents needed instead of prices.

---

# Fictional Harbor Services（FICTIONAL-O）红利分析

## 1. 结论速览

**一家现金流稳定、分红覆盖充足的维护服务公司；股息安全性可接受。现价 40 美元已进入“正常化收入达到高端要求”区间的上沿，可逐步增持，但不满足强力买入条件：预测可信度只有“中”。**

| 现价（日期） | 税后股息率 TTM | 正常化税后股息率 | 3年股息覆盖 | 买点 | 当前位置 |
|---|---:|---:|---:|---|---|
| 40 美元（2026-01-01） | 10.0% | 10.0% | 2.0x | ≤ 40 美元；≤ 32 美元时压力情景仍达标 | 正常化收入达到高端要求 |

行动：逐步增持 ｜ 预测可信度：中 ｜ 红利陷阱：未触发 ｜ 质量：62/85 ｜ 综合评分：76/100（B，暂定：含估计输入；覆盖度 100%）｜ 组合角色：观察名单（未提供持仓）

## 2. 财务状况

**分红由经常性现金支付：近三年可持续可分配现金是股息的 2.0 倍，唯一的实际缺口来自 2025 年一次性现金支出。**

| 财年 | 可持续可分配现金（百万美元） | 实际可分配现金 | 现金股息 | 可持续覆盖 | 实际覆盖 |
|---|---:|---:|---:|---:|---:|
| 2021 | 50 | 45 | 40 | 1.25x | 1.13x |
| 2022 | 60 | 55 | 40 | 1.50x | 1.38x |
| 2023 | 70 | 65 | 40 | 1.75x | 1.63x |
| 2024 | 80 | 75 | 40 | 2.00x | 1.88x |
| 2025 | 90 | 35 | 40 | 2.25x | 0.88x |

- **现金质量：** FY+1 基准经营现金 130（估）扣维护 20、其他股东权益 10 后，所有者自由现金流 100；再扣成长投资 20、强制性用途 5，可持续可分配现金 75（覆盖见第 4 节）。
- **分红资金：** 2025 年实际现金 35 低于股息 40，差额 5 由既有现金支付；属一次性支出，不是经常性缺口。
- **资产负债：** 现金 25、负债 50、EBITDA 100，五年内无再融资压力。
- **股本：** 无增发、无回购、无以股代息，每股数据不受稀释。
- **到手现金：** 按假设 A4 零预扣税、零费用，税前即税后；美元收入、美元报价，无汇率换算。

## 3. 买点观点

**现价 40 美元恰好对应 10% 税后股息率，达到要求区间的高端；跌至 32 美元以下时，即使压力情景股息也能满足 10% 要求。**

收息定价边界：50 美元以上低于要求现金收益率；40–50 美元正常化收入处于要求区间；32–40 美元正常化收入达到高端要求（← 现价）；32 美元及以下压力情景收入也达到高端要求。

| 阶段 | 估值价格 | 收息约束后价格 | 相对现价 | 状态与条件 |
|---|---:|---:|---:|---|
| 初始建仓 | 50 美元 | 50 美元 | +25% | 已就绪：维持有资金支持的基准现金路径 |
| 逐步增持 | 40 美元 | 40 美元 | 0% | 已就绪：现价达标；可信度“中”限于分批 |
| 强力买入 | 32 美元 | 32 美元 | −20% | 等价格＋等证据：还需可信度“高”、安全性“强” |

- **要求回报：** 无风险锚 4% + 风险溢价 4%–6% = 要求税后股息率 8%–10%（假设 A5，美元，2026-01-01）；未提供用户最低收入目标（暂不评估）。
- **行动与条件：** 可执行，逐步增持。强力买入同时需要价格跌至 32 美元以下、预测可信度升至“高”、股息安全性升至“强”。若股价回到 32 美元，账面回撤 20%；10% 现金收益不等于保证的总回报。

## 4. 长期展望：业务与股息

**未来五年每股现金和股息大致持平：业务靠续约合同，无扩张假设，派息率 40% 不变。**

- **服务量：** 基准情景下 FY+3／FY+5 收入维持 500（估）；悲观／乐观分别为基准的 80%／120%。仅续约现有合同，没有新市场假设。
- **现金转化：** 经营现金约为收入的 26%（估），成长投资 20／年由自由现金流内部支付，不增发、不加杠杆。

| 情景 | 核心假设 | FY+1 DPS | FY+3 DPS | FY+5 DPS | FY+1–3 覆盖 |
|---|---|---:|---:|---:|---:|
| 悲观 Bear | 经营水平为基准 80% | 3.2 | 3.2 | 3.2 | 1.9x |
| 基准 Base | 维持现有合同 | 4.0 | 4.0 | 4.0 | 1.9x |
| 乐观 Bull | 经营水平为基准 120% | 4.8 | 4.8 | 4.8 | 1.9x |

- **派息政策：** 归母净利润的 40%（假设 A3）。三个情景的股息都低于可分配现金，约 1.9 倍覆盖，没有资金缺口；股息增长只能来自利润增长，而非提高派息率。名义股息持平意味着实际购买力随通胀下降。

## 5. 风险点与跟踪信号

**红利陷阱未触发；最大风险是服务量或现金转化持续低于计划，这会直接压低以利润为基数的股息。**

| 风险 | 早期信号（可观察指标 / 阈值） | 对股息的影响 | 性质 | 下次检查 |
|---|---|---|---|---|
| 服务量下滑 | 服务量或经营现金转化低于计划 10% 以上 | 每低 10%，股息约降 0.4 美元 | 持续性 | 下期业绩 |
| 扩产延误 | 已承诺产能推迟超过一年 | 成长投资挤占现金，需重建模型 | 持续性 | 项目公告 |
| 派息政策改变 | 董事会下调 40% 派息率 | 按新比例同步下调 | 结构性 | 下次派息公告 |
| 一次性现金支出重现 | 实际可分配现金再次低于股息 | 动用存量现金，削弱安全垫 | 暂时性 | 下期现金流量表 |

## 6. 数据来源与关键假设

- **数据截至：** 2026-01-01；价格 40 美元为教学假设。
- **主要来源：** `worked-examples.md` 假设 A1–A8（虚构，无外部披露）。
- **关键假设：** 40% 利润派息率（假设）；零预扣税（假设）；要求回报 8%–10%（假设）；经营水平按情景平移，无时间增长（估）。
- **数据缺口：** 无真实的历史收入与利润序列；无持仓信息，因此不作持仓复评或仓位建议。
- **说明：** 仅为研究示例，不构成个人投资或税务建议；现金收益区间未计入股息增长，不是完整的内在价值估计。

需要完整计算过程（现金流桥、五年逐年预测、敏感性、陷阱清单、估值与入场审计、评分与评级明细）时，可要求输出审计附录。

---

## 审计附录位置说明

When the user asks for the appendix, append one `审计附录` section after Section 6 with only the relevant parts A1-A13 listed in `output-template.md`. The complete machine-readable records for this case are in `ordinary.analysis.json`; the growth-valuation variant is in `growth.analysis.json`.
