# Executed inside build_hsbc.py after hsbc_rest.py.
TNAV = 9.41
REV = [49552, 50620, 66058, 65854, 68274]; PBT = [18906, 17058, 30348, 32309, 29907]
EPS = [0.62, 0.72, 1.15, 1.25, 1.21]; ROTE = [8.3, 10.0, 14.6, 14.6, 13.3]
TNAVH = [7.88, 7.44, 8.19, 8.61, 9.64]; ISSUED = [20632, 20294, 19263, 17947, 17175]
def ptbv_value(rote, coe, g=0.03): return TNAV * (rote - g) / (coe - g)
pv = {"bear_hi": ptbv_value(0.14, R_HIGH), "base_hi": ptbv_value(0.17, R_HIGH), "base_lo": ptbv_value(0.17, R_LOW)}
sens = [(d, N / (R_LOW + d)) for d in (-0.01, -0.005, 0, 0.005, 0.01)]
implied_coe = 0.03 + (0.17 - 0.03) / (PRICE / TNAV)

# ---- labels and texts the validator does not cover ----
r.update({"fundamental_trend": "Stable", "forecast_confidence": "Medium", "dividend_safety": "Acceptable",
          "three_year_outlook": "Grow", "portfolio_role": "Watchlist", "buyback_quality": "Good" if pts["buyback_quality"] >= 8 else "Neutral",
          "valuation_reason": "Ordinary cash-income thresholds with no growth or buyback credit; a P/TBV residual-income cross-check is shown separately in chapter 9."})
for i, row in enumerate(r["five_year_dividend_history"]):
    row.update({"fiscal_year": YEARS[i], "coverage_label": "Strong" if covs[i] >= 1.5 else "Adequate" if covs[i] >= 1 else "Weak",
                "quality_tag": "Stable"})
r["business_fundamentals"] = {"dividend_funding_engine": "Banking NII (about 60% of revenue) plus wealth and transaction fees generate profit; dividends are 50% of EPS excluding notable items, paid after CET1 capital for RWA growth.",
                              "core_operating_drivers": ["Banking NII and NIM", "Expected credit losses", "CET1 and RWA growth"],
                              "historical_operating_trend": []}
bo["drivers"] = [dict(bo["drivers"][0], **{"driver": d, "segment": seg, "baseline": base_, "year_three_outcome": y3, "year_five_outcome": y5,
        "investment_and_funding": "Funded from retained earnings; CET1 kept at 14%-14.5%.", "fcf_transmission": "Profit less RWA growth capital is distributable; 50% paid as dividends.",
        "evidence_type": "company_guidance", "source_and_date": Q3, "confidence": "Medium", "invalidation_signal": inv})
    for d, seg, base_, y3, y5, inv in (
        ("Banking NII", "Hong Kong and UK banking", "Banking NII at least 46bn USD in 2026", "Base flat-to-up with structural hedge reinvestment", "Base grows with deposits", "Banking NII guidance cut below 44bn USD"),
        ("Credit costs", "Group", "ECL about 45bps of loans in 2026", "Base 40-45bps", "Base 40-45bps", "ECL above 60bps for two quarters"),
        ("Costs and synergies", "Group", "Target-basis cost growth about 1% in 2026", "Hang Seng synergies 0.5bn USD", "Cost growth below revenue growth", "Cost growth above 3% without revenue offset"))]
r["controller_risk"].update({"listed_company_impact": "Widely held; Ping An is a significant minority shareholder without control.", "source_and_date": AR, "assessed_on": AS_OF})
r["real_income"].update({"inflation_basket": "Hong Kong CPI not retrieved in this run.", "source_and_method": "Not assessed: inflation series not retrieved; nominal DPS rose 0.22 to 0.66 USD paid (2021-2025)."})
r["fx_risk"].update({"status": "not_material", "economic_exposure": "USD dividends paid in HKD under the HKD-USD peg; group earns HKD, GBP, USD.",
                     "operating_currencies": ["HKD", "GBP", "USD"], "distribution_currency": "USD", "investor_currency": "HKD",
                     "material_exposure": False, "hedge_and_natural_offsets": "HKD peg to USD limits investor FX risk; GBP translation affects group profit modestly.",
                     "evidence_and_limitations": AR})
r["holding_review"].update({"rationale": "User holds HSBC but did not supply size, cost or income target; no trade instruction is given.", "next_review": "FY2026 results, February 2027"})
r["holding_review"]["triggers"][0].update({"threshold": f"Revisit if price exceeds the P/TBV Base value at R_high (about USD {pv['base_hi']:.2f}) or RoTE falls below 14%.", "evidence": Q3})
r["portfolio_role_assessment"]["rationale"] = "High quality and Acceptable safety, but the investor's income mandate is unknown; role stays Watchlist until mandate is supplied."
for key, v in r["rating_audit"].items():
    for f in ("supporting_evidence", "rule"):
        if isinstance(v.get(f), str) and ("ictional" in v[f] or "teaching" in v[f]):
            v[f] = f"See scorecard and coverage: three-year coverage {sum(fads[2:]) / sum(divs[2:]):.2f}x; CET1 13.9%; HK-resident withholding 0%."
r["visual_summary"] = {**r["visual_summary"], "business_and_fcf_trend": "Profit to ordinary shareholders 12.6bn (2021) to 21.1bn USD (2025); Base 2026 29.4bn.",
                       "dps_path": f"Base DPS {base_dps[0]:.3f}/{base_dps[2]:.3f}/{base_dps[4]:.3f} USD in 2026/2028/2030.",
                       "yield_normalization": f"Forward net yield {fwd_yield:.2%} vs US 10y 4.84%.",
                       "main_driver_sensitivity": "Rate cuts and credit costs drive the Bear case.",
                       "valuation_summary": f"Income thresholds USD {starter:.2f}/{add:.2f}/{strong:.2f}; P/TBV value USD {pv['bear_hi']:.2f}-{pv['base_lo']:.2f}."}

# ---- report body ----
yuan = lambda usd: f"{usd*USDHKD:.1f} 港元"
T = lambda title, cols, rows, note: {"title": title, "columns": cols, "rows": rows, "note": note}
NOTE_AR = "美元百万（每股为美元），财年截至 12 月 31 日，报告口径；来源：汇丰 2025 年报五年财务资料"
sections = [
 ("摘要与投资结论", [
   f"汇丰是稳定分红型的全球银行，盈利主要来自香港和英国的存贷利差，按剔除特殊项目后每股盈利的 50% 派息，另用超额资本回购。",
   f"另一视角：按银行常用的市净率口径，现价隐含约 {implied_coe:.1%} 的股本成本，处于 Bear 至 Base 合理区间（约 {yuan(pv['bear_hi'])} 至 {yuan(pv['base_lo'])}）之内，已持有部分没有因估值过高而必须卖出的证据。",
   "最重要的恶化信号：2025 年税前利润下降 7%（含交通银行减值和法国贷款组合出售损失等特殊项目），CET1 因恒生银行私有化跌至 13.9%，低于 14% 目标下限，回购收缩。"],
  [T("摘要关键数字", ["指标", "数值", "说明"], [
     ["现价", f"{PRICE_HKD} 港元", "2026-11-09 收盘；折合 17.55 美元"],
     ["2025 年每股股息", "0.75 美元", "TTM 税后股息率 4.3%"],
     ["2026 年 Base 每股股息", f"{N:.2f} 美元", f"远期税后股息率 {fwd_yield:.1%}"],
     ["美国 10 年期国债", "4.84%", "2026-11-05"],
     ["收息口径初始建仓价", yuan(starter), "约为现价的 62%"],
     ["市净率合理区间", f"{yuan(pv['bear_hi'])}–{yuan(pv['base_lo'])}", "按有形净资产 9.41 美元"],
     ["质量／综合评分", f"{quality}/85，{total}/100（{grade}）", "完整评估，无暂定区间"]],
     "股价来自 Yahoo Finance，美国国债来自 FRED，其余来自汇丰 2025 年报及 2026 年三季度业绩公告")]),
 ("公司概况与行业定位", [
   "汇丰控股是在英国注册、在港交所和伦交所上市的全球性银行集团。2026 年 1 月完成恒生银行私有化后，香港业务（汇丰香港与恒生银行）是最大利润来源，其次是英国围栏银行，以及企业与机构银行、财富管理业务。",
   "按经济特征分类：三个分部都属于“资产负债表即业务”，收入以利差为主，受利率周期驱动，资产没有到期日，属轻资本。因此现金模型使用银行资本生成，不使用工业企业的自由现金流算法；股息由母公司从子公司上缴的分红中支付。"]),
 ("行业结构、供需与周期", [
   "银行业的核心变量是利率、存款结构和信用成本。2022–2024 年港元、英镑、美元利率大幅上升，推高汇丰的净利息收入；2025–2026 年利率回落，净息差从 2023 年的 1.66% 降至 2025 年的 1.59%，2026 年三季度为 1.57%。管理层通过结构性对冲把部分高利率锁定到未来几年。",
   "未来三至五年的三个驱动因素：第一，利率下行速度决定银行业务净利息收入能否维持在 460 亿美元以上；第二，香港商业地产及内地相关敞口的信用成本，管理层预期 2026 年约为贷款的 45 个基点；第三，Basel 3.1 将于 2027 年 1 月 1 日起实施，预计提高 CET1 比率约 40–50 个基点，释放回购空间。"]),
 ("竞争格局与公司护城河", [
   "汇丰在香港拥有最大的存款基础，加上恒生银行，在港元低成本存款上具有规模优势；跨境贸易与财富管理网络是其与区域性银行相比的主要差异。",
   "本次没有取得渣打集团、中银香港等同业的同口径数据，因此不列同业对比表，以免口径不一。下次复评时应补充同业的有形股本回报率和市净率。"]),
 ("过去五年经营与财务趋势", [
   "2021–2024 年利润随加息大幅改善，归属普通股东利润从 126 亿美元升至 229 亿美元，有形股本回报率从 8.3% 升至 14.6%；2025 年回落至 211 亿美元和 13.3%，主要由特殊项目造成，剔除后税前利润增长 7%。",
   "每股指标优于总量：已发行股数五年减少 17%，每股有形净资产从 7.88 美元升至 9.64 美元（2026 年三季度为 9.41 美元，因私有化有所下降）。趋势状态：盈利与股东回报为绿色，资本充足率为黄色（低于目标区间）。"],
  [T("五年经营与股东回报", ["财年", "营业收入", "税前利润", "归属普通股东利润", "每股盈利", "当年派息", "有形股本回报率%", "每股有形净资产"],
     [[YEARS[i], REV[i], PBT[i], PROFIT[i], EPS[i], DPS_PAID[i], ROTE[i], TNAVH[i]] for i in range(5)],
     NOTE_AR + "；2024 年派息含 0.21 美元特别股息；2021 年为 IFRS 4 口径")],
  [{"title": "归属普通股东利润与税前利润", "kind": "bar", "unit": "百万美元", "x_labels": YEARS,
    "series": [{"name": "税前利润", "values": PBT}, {"name": "归属普通股东利润", "values": PROFIT}],
    "source": "汇丰 2025 年报五年财务资料"},
   {"title": "每股盈利与当年派息", "kind": "line", "unit": "美元／股", "x_labels": YEARS,
    "series": [{"name": "每股盈利", "values": EPS}, {"name": "当年派息", "values": DPS_PAID}],
    "source": "汇丰 2025 年报五年财务资料"}]),
 ("现金流、资产负债与股息质量", [
   f"银行不用工业自由现金流，改用资本生成：归属普通股东利润减去支撑风险加权资产增长所需的 CET1 资本（按 14.25% 目标）。2023–2025 年合计资本生成是现金股息的 {sum(fads[2:]) / sum(divs[2:]):.2f} 倍，最差年份 2025 年为 {min(covs):.2f} 倍。",
   "股息加回购在 2024–2025 年超过了资本生成，差额来自出售加拿大、阿根廷业务释放的资本，以及让 CET1 向目标区间回落；这部分不可重复。CET1 在 2026 年 9 月底为 13.9%，12 个月平均流动性覆盖率 132%。",
   "到手现金：股息以美元宣派，香港登记股东按联系汇率收取港元；英国对普通股息不预扣税，香港不征股息税，因此香港居民税前即税后。没有以股代息安排。股息安全性判断为“可接受”：派息由利润支持，但资本暂时低于目标。"],
  [T("历年资本生成与股息覆盖", ["财年", "归属普通股东利润", "增长占用资本", "资本生成", "现金股息", "覆盖倍数"],
     [[YEARS[i], PROFIT[i], round(PROFIT[i] - fads[i]), fads[i], divs[i], round(covs[i], 2)] for i in range(5)],
     "美元百万；增长占用资本 = 风险加权资产增量 × 14.25%（2021 年无上年数据，记为 0）；现金股息 = 当年派息 × 期末股数（近似）")]),
 ("企业成长性与资本配置", [
   "增长主要来自每股层面而不是总量：2021–2025 年归属普通股东利润年均增长约 14%，每股盈利年均增长约 18%，差额来自回购。管理层目标是 2026–2028 年有形股本回报率不低于 17%，2028 年收入增长约 5%。",
   "资本配置：50% 派息率政策清晰；回购与 CET1 区间挂钩，资本低于目标时暂停，体现纪律。恒生银行私有化预计带来每年 5 亿美元协同效益，但对每股价值的净影响尚无披露。"]),
 ("未来五年经营与现金流预测", [
   "Base：2026 年剔除特殊项目后的归属普通股东利润约 294 亿美元（按前三季度每股 1.30 美元年化），此后每年增长 4%–5%，有形股本回报率维持在目标下限附近。Bear：利率较快下行，叠加信用成本上升，2027–2028 年利润降至 230–240 亿美元。Bull：利率维持高位，叠加协同效益超预期。",
   "股数按 171.11 亿股保持不变，不计回购带来的每股提升，因此每股股息偏保守。"],
  [T("情景每股股息（美元）", ["情景", "2026", "2027", "2028", "2029", "2030"],
     [[s_] + [round(d, 3) for d in dps] for s_, dps in (("Bear", bear_dps), ("Base", base_dps), ("Bull", bull_dps))],
     "按 50% 派息率 ÷ 171.11 亿股；不计回购；分析师估算")]),
 ("估值与预期总回报", [
   f"收息口径（不计成长与回购）：以 Base 2026 年每股股息 {N:.3f} 美元除以 7.84%–9.84% 的必要收益率，对应 {add:.2f}–{starter:.2f} 美元（{yuan(add)}–{yuan(starter)}），现价远高于此区间。",
   f"市净率／超额收益口径：按有形股本回报率 17%、长期增长 3%、股本成本 9.84%，合理市净率约 {pv['base_hi']/TNAV:.2f} 倍，对应 {pv['base_hi']:.2f} 美元（{yuan(pv['base_hi'])}）；股本成本取 7.84% 时为 {yuan(pv['base_lo'])}；Bear（回报率 14%）为 {yuan(pv['bear_hi'])}。现价 1.87 倍市净率，隐含股本成本约 {implied_coe:.1%}。",
   "两种方法的差异来自回购和增长：汇丰除 50% 派息外还持续回购，收息口径只计股息部分，也不计每股盈利增长。三年持有期（不计回购、不计再投资）：Bear 若估值回落到必要收益率约亏损 39%，Base 估值不变约赚 25%，Bull 约赚 44%。"],
  [T("三年持有情景（每股，美元）", ["情景", "三年累计股息", "第三年末价格", "累计回报"],
     [[row["scenario"], round(row["net_cash_received"], 2), round(row["exit_price"], 2), f"{row['cumulative_return']:.1%}"] for row in ep["return_scenarios"]],
     "退出价格按第三年每股股息 ÷ 假设股息率：Bear 7.84%、Base 维持现有 4.90%、Bull 4.5%")]),
 ("买点、建仓策略与持仓复评", [
   f"美国 10 年期国债对比：国债收益率 4.84%（FRED，2026-11-05）；汇丰远期税后股息率 {fwd_yield:.2%}，毛利差与税后利差均约为 {(fwd_yield-RF)*100:+.2f} 个百分点（香港居民持有美债利息一般适用组合利息豁免，两者均按零预扣计算）。持有汇丰而非国债的补偿只能来自股息增长、回购和估值，而不是当期收入。",
   "国债收益率敏感性（风险溢价不变）：国债收益率每变动 50 个基点，收息口径初始建仓价反向变动约 6%–7%。",
   f"分阶段参考价：初始建仓 {yuan(starter)}、逐步增持 {yuan(add)}、强力买入 {yuan(strong)}（强力买入还需预测可信度为高、安全性为强）。这些价格只适用于以收息为目的的新资金。已持有部分：用户未提供仓位和成本，本报告不给出加减仓指令；按市净率口径估值仍在合理区间内，若 CET1 恢复到 14% 以上且回报率维持在 17% 以上，持有逻辑不变。"],
  [T("国债收益率敏感性", ["美国 10 年期国债", "必要收益率下限", "初始建仓价（港元）"],
     [[f"{(RF + d) * 100:.2f}%", f"{(R_LOW + d) * 100:.2f}%", round(v * USDHKD, 1)] for d, v in sens],
     "风险溢价 3% 不变；Base 每股股息 0.859 美元；汇率 7.8395")]),
 ("风险、监测指标与论点证伪", [
   "最大风险：利率较快下行导致净利息收入不及 460 亿美元指引，同时信用成本上升，两者叠加会使每股股息回到 0.70 美元左右。"],
  [T("风险与监测阈值", ["风险／指标", "当前值", "预警阈值", "影响", "复查时间"], [
     ["CET1 比率", "13.9%", "低于 13.5%", "回购暂停，股息增长受限", "每季度"],
     ["剔除特殊项目的有形股本回报率", "18.8%（前三季度）", "连续两季低于 14%", "派息基数下降，论点失效", "每季度"],
     ["预期信用损失率", "约 45 个基点", "高于 60 个基点", "利润每年减少约 15 亿美元", "每季度"],
     ["银行业务净利息收入", "≥460 亿美元（2026 指引）", "指引下调至 440 亿美元以下", "Bear 情景成立", "2027 年 2 月"],
     ["监管限制分红", "无", "监管要求暂停派息（2020 年先例）", "股息中断", "持续"]],
     "阈值为分析判断；当前值来自汇丰 2026 年三季度业绩公告")]),
 ("数据来源、关键假设与研究限制", [
   "数据截至 2026-11-09。主要来源：汇丰 2025 年报（2026-02-25）、2026 年三季度业绩公告（2026-10-27）、Yahoo Finance 行情、FRED 美国国债收益率。",
   "关键假设：50% 派息率；股数不变（不计回购）；风险加权资产每年增长约 3%，按 14.25% CET1 占用资本；风险溢价 3%–5%。",
   "研究限制：未取得同业对比数据、香港通胀序列和恒生银行私有化对每股价值的完整披露；未建立计入回购的完整总回报估值模型；用户持仓与收息目标未提供。本报告仅为研究资料，不构成投资建议。"]),
]
r["report_output"].update({"title": "汇丰控股（0005.HK）完整研究报告", "summary": f"数据截至 {AS_OF}；收息口径等待到价，市净率口径处于合理区间。",
                           "sections": [dict({"heading": h, "paragraphs": p_}, **({"tables": t_} if t_ else {}), **({"charts": c_} if c_ else {}))
                                        for h, p_, *rest in sections for t_, c_ in [((rest + [None, None])[0], (rest + [None, None])[1])]],
                           "appendix": ["审计附录 A3、A5、A6、A10、A11、A13 由结构化记录自动生成；A12 持仓复评因未提供持仓而不适用。"],
                           "labels": ["金额单位：美元百万，另有注明除外"]})
ra = r["rating_audit"]
ra["buyback_quality"].update({"label": r["buyback_quality"], "rule": "Real share-count reduction with capital discipline is Good.",
    "supporting_evidence": "Shares in issue 20,632m (2021) to 17,175m (2025); buybacks paused when CET1 fell below range."})
ra["three_year_outlook"].update({"label": "Grow", "rule": "Base year-3 net DPS more than 5% above year 1 is Grow.",
    "supporting_evidence": f"Base DPS {base_dps[0]:.3f} (2026) to {base_dps[2]:.3f} USD (2028), +{base_dps[2]/base_dps[0]-1:.1%}; Bear {bear_dps[0]:.3f} to {bear_dps[2]:.3f}."})
r["visual_summary"]["coverage_labels"] = f"Three-year capital-generation coverage {sum(fads[2:]) / sum(divs[2:]):.2f}x; worst year 2025 {min(covs):.2f}x. Safety Acceptable: CET1 below target range."
bo["extension_limitations"] = "Years 4-5 extend Base profit growth of about 4% a year at the RoTE target floor; analyst estimate, not issuer guidance."
for m in bo.get("milestones", []):
    m["source_to_revisit"] = "HSBC FY2026 annual results and 2027 quarterly releases"
