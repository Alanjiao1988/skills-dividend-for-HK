"""Build the China Merchants Port (0144.HK) schema-3.0 Full Analysis from sourced inputs.

Units: HKD millions for group cash/profit; shares in millions; per-share in HKD.
All derived numbers are computed here so the record stays internally consistent.
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "dividend-income-equity-analysis"
OUT = HERE / "cmport-0144.analysis.json"
r = json.loads((SKILL / "examples/full-report.analysis.json").read_text(encoding="utf-8"))

# ---------------- sourced inputs ----------------
HX = "https://www1.hkexnews.hk/listedco/listconews/sehk/"
AR25 = HX + "2026/0427/2026042701104.pdf"      # Annual Report 2025
AR23 = HX + "2024/0425/2024042501060.pdf"      # Annual Report 2023
AR22 = HX + "2023/0427/2023042701103.pdf"      # Annual Report 2022
IR26 = HX + "2026/0924/2026092400588.pdf"      # 2026 Interim Report
DIV26 = HX + "2026/0828/2026082800273.pdf"     # 2026 interim cash dividend announcement
PX = "https://query1.finance.yahoo.com/v8/finance/chart/0144.HK"
UST = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"
SOURCES = [AR25, AR23, AR22, IR26, DIV26, PX, UST]
S = [AR25, IR26]
AS_OF = "2026-11-09"
PRICE = 16.72                     # HKD, 2026-11-09
RF = 0.0484                       # US 10y via HKD peg (HK government bond yield not retrieved)
SHARES = 4198.009186              # millions, unchanged since 2024
YEARS = ["2021", "2022", "2023", "2024", "2025"]
REV = [11850, 12545, 11482, 11842, 13354]
PROFIT = [8144, 7781, 6233, 7919, 6457]          # attributable to equity holders
EPS = [2.199, 2.015, 1.532, 1.886, 1.538]
DPS = [0.940, 0.820, 0.700, 0.886, 0.739]
WSHARES = [3703.860052, 3861.103481, 4068.060286, 4198.009186, 4198.009186]
OCF = [8785, 8781, 7238, 8547, 9472]             # includes dividends from associates/JVs
ASSOC_DIV = [3347, 2592, 2034, 2716, 2730]
CAPEX = [1834, 1514, 1309, 1199, 873]
INTEREST = [1522, 1686, 1700, 1431, 1193]
LEASE = [103, 79, 96, 150, 466]
NCI_DIV = [386, 687, 434, 1884, 1216]
PERP = [223, 224, 225, 60, 60]
CASH_DIV_PAID = [1194, 941, 1248, 3065, 3719]    # cash actually paid; scrip shares issued 2021-2023
ASSOC_PROFIT_2025 = 4970
TEMPLATE_TWO = r["three_year_fundamental_forecast"][1]

SCEN = {
    "Bear": {"profit": [6650, 5900, 5700, 5800, 5900], "revenue": [13800, 13000, 12800, 13000, 13200], "growth": 300},
    "Base": {"profit": [6850, 7050, 7250, 7400, 7550], "revenue": [14300, 14800, 15300, 15700, 16100], "growth": 600},
    "Bull": {"profit": [7000, 7450, 7850, 8150, 8450], "revenue": [14600, 15500, 16300, 17000, 17700], "growth": 900},
}
PAYOUT = 0.48
OCF_K, CLAIMS_K, MAINT = 1.137, 0.20, 500.0
R_LOW, R_HIGH = RF + 0.04, RF + 0.06

# ---------------- history bridge (full cash-equivalent entitlement) ----------------
owner = [OCF[i] - INTEREST[i] - LEASE[i] - CAPEX[i] - NCI_DIV[i] - PERP[i] for i in range(5)]
entitle = [round(DPS[i] * WSHARES[i]) for i in range(5)]
covs = [owner[i] / entitle[i] for i in range(5)]
bridge = []
for i, fy in enumerate(YEARS):
    row = copy.deepcopy(r["cash_flow_bridge"][i])
    row.update({"fiscal_year": fy, "fiscal_year_end": f"{fy}-12-31", "recurring_owner_fcf_or_proxy": owner[i] + CAPEX[i],
                "recurring_fad": owner[i], "actual_all_in_fcf": owner[i], "actual_distribution_capacity": owner[i],
                "cash_dividends": entitle[i], "fcf_dividend_coverage": owner[i] / entitle[i],
                "actual_cash_coverage": owner[i] / entitle[i], "evidence_status": "reported_reconciled",
                "funding_source": "Mixed" if fy in ("2021", "2022", "2023") else "Operating FCF"})
    bridge.append(row)
r["cash_flow_bridge"] = bridge

# ---------------- forecasts ----------------
def fc(template, fy, year, s_):
    p_ = SCEN[s_]["profit"][year - 1]
    nocf = p_ * OCF_K
    claims = p_ * CLAIMS_K
    own = nocf - MAINT - claims
    g = SCEN[s_]["growth"]
    row = copy.deepcopy(template)
    row.update({"fiscal_year": fy, "forecast_year": year, "scenario": s_,
                "primary_driver_name": "Container throughput and associate dividends",
                "primary_driver_assumption": f"{s_}: attributable profit {p_}m HKD; normalized OCF after interest and leases = 1.137 x profit; minority and perpetual claims 20% of profit.",
                "revenue_or_sector_income": SCEN[s_]["revenue"][year - 1], "net_income_or_affo": p_,
                "operating_cash_flow": nocf, "normalized_ocf": nocf, "maintenance_capex": MAINT, "other_owner_claims": claims,
                "remaining_growth_investment": g, "fcf_or_distributable_cash": own, "nonrecurring_operating_cash_inflow": 0,
                "actual_all_in_fcf": own - g, "recurring_fad": own - g, "estimate_status": "estimated",
                "forecast_confidence": "Medium", "assumption_basis": "analyst_estimate",
                "evidence_and_limitations": "Ratios calibrated to FY2025 (OCF 9,472 less interest 1,193 and leases 466) and 1H26 profit 3,832m; associate dividend conversion assumed near the 2025 level of 55%."})
    return row


r["three_year_fundamental_forecast"] = [fc(TEMPLATE_TWO, str(2025 + y), y, s_) for y in (1, 2, 3) for s_ in ("Bear", "Base", "Bull")]
r["forecast_extension"] = [fc(r["forecast_extension"][1], str(2025 + y), y, s_) for y in (4, 5) for s_ in ("Bear", "Base", "Bull")]
fc_map = {(row["forecast_year"], row["scenario"]): row for row in r["three_year_fundamental_forecast"] + r["forecast_extension"]}

btmpl, rtmpl = r["dividend_forecast_bridge"][1], r["dividend_and_yield_runway"][1]
dfb, run = [], []
for y in range(1, 6):
    for s_ in ("Bear", "Base", "Bull"):
        f = fc_map[(y, s_)]
        own, g = f["fcf_or_distributable_cash"], f["remaining_growth_investment"]
        b = copy.deepcopy(btmpl)
        b.update({"fiscal_year": str(2025 + y), "forecast_year": y, "scenario": s_,
                  "fcf_or_capital_generation": own, "required_reinvestment": g, "mandatory_debt_or_regulatory_uses": 0,
                  "recurring_fad": own - g, "exceptional_cash_uses": 0, "excess_cash_used": 0,
                  "cash_available_for_distribution": own - g, "diluted_share_count": SHARES,
                  "deduction_ledger": [
                      {"item": "Growth capex (overseas terminals, smart port)", "category": "growth", "amount": g,
                       "already_in_starting_metric": False, "incremental_deduction": g,
                       "evidence": "Growth capex beyond 500m HKD maintenance; deducted once after owner cash."},
                      {"item": "Maintenance already in owner cash", "category": "maintenance", "amount": MAINT,
                       "already_in_starting_metric": True, "incremental_deduction": 0,
                       "evidence": "Maintenance capex deducted inside owner cash; not deducted again."}],
                  "evidence_and_limitations": "Operating owner cash after interest, leases, minority and perpetual claims; associate dividends included only as cash received."})
        dfb.append(b)
        div = f["net_income_or_affo"] * PAYOUT
        q = copy.deepcopy(rtmpl)
        q.update({"fiscal_year": str(2025 + y), "forecast_year": y, "scenario": s_,
                  "cash_available_for_distribution": own - g, "payout_base_amount": f["net_income_or_affo"],
                  "payout_ratio": PAYOUT, "policy_implied_dividend": div, "dividend_cash_cost": div,
                  "dividend_entitlement": div, "dividend_entitled_shares": SHARES,
                  "share_count_reconciliation": "4,198.0m shares unchanged since 2024; scrip dividend not offered for the 2025 final or 2026 interim.",
                  "derived_dps": div / SHARES, "funding_gap": 0, "all_cash_funding_gap": 0, "dps_source": "evidence_backed"})
        run.append(q)
r["dividend_forecast_bridge"], r["dividend_and_yield_runway"] = dfb, run

dps = {s_: [SCEN[s_]["profit"][i] * PAYOUT / SHARES for i in range(5)] for s_ in SCEN}
N, B = dps["Base"][0], dps["Bear"][1]
starter, add, strong = N / R_LOW, N / R_HIGH, B / R_HIGH
fwd = N / PRICE
pct = lambda x: (x / PRICE - 1) * 100

# ---------------- identity, model, coverage ----------------
r.update({"company": "China Merchants Port Holdings Company Limited", "ticker": "0144.HK",
          "exchange": "Hong Kong Stock Exchange", "as_of_date": AS_OF, "price_used": PRICE,
          "withholding_rate": 0, "withholding_basis": "company_announcement", "sources": SOURCES})
cfm = r["cash_flow_model"]
cfm.update({"sector_model": "operating_company", "overlays": ["holding_company"],
            "starting_metric": "Consolidated OCF (includes dividends received from associates and JVs) after cash interest and lease payments",
            "owner_perimeter": "Equity holders of China Merchants Port Holdings",
            "financial_currency": "HKD", "cash_unit_scale": 1000000, "share_unit_scale": 1000000,
            "evidence_status": "reported_reconciled",
            "proxy_reconciliation": "FY2025: OCF 9,472 - interest 1,193 - leases 466 - capex 873 - minority dividends 1,216 - perpetual 60 = 5,664 HKD m owner cash after all capex.",
            "capital_and_remittance_evidence": f"Associates and JVs contributed {ASSOC_PROFIT_2025}m of 2025 profit but paid only 2,730m in cash dividends (55%); parent cash depends on these remittances plus consolidated terminals in Shenzhen, Hong Kong and overseas.",
            "sources": S, "missing_inputs": []})
cfm["deduction_ledger"] = copy.deepcopy(dfb[1]["deduction_ledger"])
cs = r["coverage_summary"]
cs.update({"dividend_basis": "ordinary_cash_paid",
           "comparison_basis": "FY2021-2025, HKD millions; dividend = full cash-equivalent entitlement (DPS x weighted shares) because 2021-2023 dividends were partly settled in scrip.",
           "fiscal_years": YEARS, "years_available": 5,
           "three_year_recurring_coverage": sum(owner[2:]) / sum(entitle[2:]),
           "five_year_worst_recurring_coverage": min(covs), "worst_available_recurring_coverage": min(covs),
           "worst_recurring_year": YEARS[covs.index(min(covs))], "worst_actual_coverage": min(covs),
           "worst_actual_year": YEARS[covs.index(min(covs))],
           "shortfall_funding_and_limitations": "No entitlement shortfall; 2021-2023 cash outflow was reduced by scrip issuance (weighted shares +13%), which is dilution, not extra cash capacity."})

# ---------------- economic profile ----------------
r["economic_profile"] = {
    "segments": [
        {"name": "珠三角及香港控股码头与其他内地业务", "cash_share_pct": 21, "revenue_engine": "volume_times_price",
         "asset_life": "perpetual_going_concern", "cyclicality": "demand_cycle",
         "cycle_window": "2021–2025 覆盖疫情后外贸高峰、2023 年回落与 2024–2025 年恢复", "balance_sheet_role": "operating",
         "capital_intensity": "maintenance_heavy"},
        {"name": "上港集团等联营码头（长三角、渤海）", "cash_share_pct": 45, "revenue_engine": "volume_times_price",
         "asset_life": "perpetual_going_concern", "cyclicality": "demand_cycle",
         "cycle_window": "2021–2025 覆盖一轮外贸量价周期", "balance_sheet_role": "operating",
         "capital_intensity": "maintenance_heavy"},
        {"name": "海外特许经营码头", "cash_share_pct": 34, "revenue_engine": "volume_times_price",
         "asset_life": "finite_assets", "cyclicality": "demand_cycle",
         "cycle_window": "2021–2025 覆盖红海绕航与全球贸易调整", "balance_sheet_role": "operating",
         "capital_intensity": "growth_heavy"}],
    "legal_wrapper": "holding_parent", "cash_attribution": "material_jv_associates",
    "finite_life_assets": [
        {"name": "斯里兰卡 CICT 与多哥 LCT 码头特许权", "end_year": 2046, "operating_cash_share_pct": 15,
         "extension_evidence": None, "terminal_treatment": "到期后不再计入现金；估值按剩余约 20 年逐项计算"},
        {"name": "巴西 TCP 码头特许权", "end_year": 2048, "operating_cash_share_pct": 12,
         "extension_evidence": None, "terminal_treatment": "特许经营安排允许运营至 2048 年，之后不计现金"},
        {"name": "印尼码头及其他海外特许权", "end_year": 2049, "operating_cash_share_pct": 7,
         "extension_evidence": None, "terminal_treatment": "首个特许权 2035 年到期，需单独测试到期次年股息"}],
    "company_level_runoff": False,
    "tax_route": {"distribution_regime": "ordinary_dividend", "exit_withholding_rate": None,
                  "exception_evidence": None, "refunds_excluded_from_cash": True},
    "kpis": [
        {"name": "集装箱吞吐量（权益口径）", "why_causal": "量价决定码头收入，占收入九成以上；2026 年上半年吞吐量 7,821 万标箱，同比增 4.5%"},
        {"name": "联营及合营公司现金分红 ÷ 应占利润", "why_causal": "约四分之三的利润来自联营合营，实际只有约 55% 以现金上缴，决定母公司可派现金"},
        {"name": "净有息负债与利息支出", "why_causal": "利息约占经营现金流的 13%，直接从股东现金中扣除"},
        {"name": "少数股东分红", "why_causal": "控股码头的少数股东每年取走 4–19 亿港元，波动大，影响可分配现金"}],
    "classification_evidence": "2025 年报分部资料（附注 5）、现金流量表及特许经营权附注；分部现金占比按 2025 年分部归属利润估算，海外特许权占比为分析估算",
}

# ---------------- policy, requirements, income ----------------
r["payout_policy"].update({
    "policy_type": "earnings_linked", "calculation_basis": "attributable_earnings",
    "basis_definition": "Board discretion under the 2018 dividend policy; recent payout of attributable profit: 2023 46%, 2024 47%, 2025 48.1%. Model uses 48%.",
    "reported_payout_ratio": 0.481, "source_and_date": AR25,
    "funding_constraint": f"Base FY2026: 48% x 6,850m = {6850 * PAYOUT:.0f}m versus capacity {fc_map[(1, 'Base')]['recurring_fad']:.0f}m."})
rr = r["return_requirements"]
rr.update({"benchmark": "US 10-year Treasury (DGS10) as the HKD anchor under the linked exchange rate", "benchmark_source": UST,
           "benchmark_date": "2026-11-05", "benchmark_currency": "USD", "benchmark_tenor": "10 years",
           "valuation_currency": "HKD", "valuation_unit_scale": 1, "shares_per_quoted_security": 1, "quote_currency": None,
           "quote_per_valuation_unit": None,
           "tax_and_fx_basis": "HKD dividends on an HKD quote; Hong Kong-incorporated issuer, no withholding (2026 interim announcement), no HK dividend tax.",
           "risk_free_rate": RF, "risk_premium_low": 0.04, "risk_premium_high": 0.06,
           "required_total_return_low": R_LOW, "required_total_return_high": R_HIGH,
           "price_independent_risk_factors": ["4 points: diversified port portfolio with long-lived assets. 6 points: reliance on associate dividends, emerging-market concessions, trade-war volume risk and controlling-shareholder priorities. Neither depends on price or score."],
           "income_growth_credit": 0,
           "limitations": "HK government bond yield not retrieved; US 10-year used through the HKD peg. No growth credit in the income thresholds."})
inc = r["income_assessment"]
inc.update({"forward_net_yield": fwd, "forward_net_dps": N, "income_period": "FY2026 full year (Base)",
            "reason": f"No investor income target supplied. Base FY2026 DPS {N:.3f} HKD / price {PRICE} = {fwd:.2%}."})

# ---------------- buy zone (primary: ordinary income) ----------------
bz = r["buy_zone"]
bz.update({"normalized_net_dps": N, "normalized_net_dps_source_period": "FY2026 Base: 48% x 6,850m / 4,198.0m shares",
           "normalization_adjustments": [f"N={N:.4f} HKD from Base FY2026 profit; no growth credit, no special dividend."],
           "bear_net_dps": B, "bear_net_dps_source": f"Bear FY2027 profit 5,900m x 48% / 4,198.0m = {B:.4f} HKD.",
           "dps_currency": "HKD", "normalization_fx_basis": "HKD dividends and HKD quote.",
           "required_net_yield_low": R_LOW, "required_net_yield_high": R_HIGH,
           "too_expensive_zone": f">{starter:.2f}", "fair_value_zone": f"({add:.2f}, {starter:.2f}]",
           "accumulation_zone": f"({strong:.2f}, {add:.2f}]", "strong_buy_zone": f"<={strong:.2f}",
           "boundaries": {"too_expensive_above": starter, "fair_lower": add, "fair_upper": starter,
                          "accumulation_lower": strong, "accumulation_upper": add, "strong_buy_at_or_below": strong}})
for key, text in (("operating_cash", "FY2025 OCF 9,472 reconciled to owner cash 5,664 after interest, leases, capex, minority and perpetual claims."),
                  ("funding_capacity", "Base FY2026 recurring FAD covers the 48% dividend about 1.7x."),
                  ("payout_policy", "Discretionary policy; payout 46%-48% in 2023-2025."),
                  ("entitled_shares", "4,198.0m shares; 2026 interim paid in cash with no scrip; no withholding.")):
    bz["normalization_evidence"][key].update({"input_detail": text, "source_refs": S,
                                              "consequence": "Supports the Base normalized DPS for the income thresholds."})
nm = bz["normalization_model"]
nm.update({"cycle_basis": "Port volumes follow trade cycles; FY2026 Base uses 1H26 run-rate, not the 2021 peak.",
           "series_sources": [AR25], "joint_assumption_rationale": "Profit, cash conversion and payout from one Base scenario.",
           "perimeter_adjustments": "Same perimeter; no major acquisitions or disposals in 2025-2026."})
nm["drivers"][0].update({"name": "Profit attributable to equity holders", "unit": "HKD m", "source": AR25,
                         "selected_value": SCEN["Base"]["profit"][0], "observations": PROFIT})
f1 = fc_map[(1, "Base")]
nm["cycle_states"]["mid"].update({"operating_assumptions": "Base FY2026", "owner_cash": f1["fcf_or_distributable_cash"],
    "growth_uses": f1["remaining_growth_investment"], "mandatory_uses": 0, "recurring_fad": f1["recurring_fad"],
    "earnings": f1["net_income_or_affo"], "payout_base": f1["net_income_or_affo"], "payout_ratio": PAYOUT,
    "dividend_entitlement": f1["net_income_or_affo"] * PAYOUT, "shares": SHARES, "gross_dps": N, "evidence": IR26})
for st in ("low", "high"):
    nm["cycle_states"][st].update({"operating_assumptions": "No separate cycle extreme; Bear/Bull carry the range.", "evidence": IR26})

# ---------------- gated income growth credit test (buy-zone.md 4.2A) ----------------
base_cagr = (dps["Base"][4] / dps["Base"][0]) ** 0.25 - 1
hist_cagr = (DPS[4] / DPS[0]) ** 0.25 - 1
LONG_RUN = 0.04
credit_cap = max(0.0, min(0.03, base_cagr, hist_cagr, LONG_RUN))
rr["income_growth_credit_basis"] = {
    "base_dps_cagr_fy1_fy5": base_cagr, "historical_metric": "dps",
    "historical_start_period": "FY2021", "historical_end_period": "FY2025", "historical_years": 4,
    "historical_start_value": DPS[0], "historical_end_value": DPS[4], "historical_cagr": hist_cagr,
    "long_run_growth_bound": LONG_RUN,
    "long_run_growth_bound_basis": "中国与全球名义增长约 4%（2% 通胀 + 2% 实际增长）",
    "credit_cap": credit_cap, "gates_passed": False,
    "explanation": f"每股股息 2021→2025 年由 {DPS[0]} 降至 {DPS[4]} 港元（年均 {hist_cagr:.1%}，含以股代息摊薄），"
                   f"历史证据不支持增长抵扣；Base 预测 {base_cagr:.1%} 的增长只进入成长股息折现模型，不进入收息口径。"
                   "本报告主估值为成长股息折现，收息口径仅作对照，按规则也不适用抵扣。"}

# ---------------- growth dividend-discount model (primary) ----------------
R_MID = (R_LOW + R_HIGH) / 2
MOS = 0.15
G_TERM = {"Bear": 0.0, "Base": 0.015, "Bull": 0.025}
G_BOUND = {"Bear": 0.01, "Base": 0.02, "Bull": 0.025}
INTERIM_PAID = 0.25               # FY2026 interim, paid in cash before the valuation date
TIMES = [0.65, 1.4, 2.4, 3.4, 4.4]  # FY2026 final Jul-2027; later years weight Oct interim and Jul final
run_map = {(q["forecast_year"], q["scenario"]): q for q in run}


def pv(path, rate, g, tdps, ttime):
    explicit = sum(c["net_dps"] * c["cash_fraction"] / (1 + rate) ** c["years_from_valuation"] for c in path)
    return explicit, tdps / (rate - g) / (1 + rate) ** ttime


TIMING_NOTE = ("估值日 2026-11-09；2026 年中期 0.25 港元已现金派付，第 1 年只计末期部分（2027 年 7 月）；"
               "此后每年按 10 月中期与次年 7 月末期加权计时；港元收款，无预扣税和费用")
gscen = []
for s_ in ("Bear", "Base", "Bull"):
    path = []
    for y in range(1, 6):
        d = run_map[(y, s_)]["derived_dps"]
        path.append({"forecast_year": y, "years_from_valuation": TIMES[y - 1], "net_dps": d,
                     "cash_fraction": (d - INTERIM_PAID) / d if y == 1 else 1, "fx_to_valuation_currency": 1,
                     "investor_cash_deductions": 0, "cash_timing_and_fx_evidence": TIMING_NOTE})
    g = G_TERM[s_]
    f5, q5 = fc_map[(5, s_)], run_map[(5, s_)]
    tdps = q5["derived_dps"] * (1 + g)
    explicit, terminal = pv(path, R_MID, g, tdps, TIMES[-1])
    own6, gro6 = f5["fcf_or_distributable_cash"] * (1 + g), f5["remaining_growth_investment"] * (1 + g)
    gscen.append({
        "scenario": s_, "required_return": R_MID,
        "required_return_basis": f"所有情景统一用必要回报区间中点 {R_MID:.2%}（无风险 4.84% + 风险溢价 5%），不在 Bear 情景重复加风险折价。",
        "terminal_growth": g, "sustainable_terminal_growth_bound": G_BOUND[s_], "terminal_net_dps": tdps,
        "terminal_time_years": TIMES[-1],
        "terminal_funding_and_fade_evidence": (
            f"第 6 年起按 {g:.1%} 永续增长：吞吐量长期增长约 2%–3%，但约 34% 的现金来自 2035–2049 年到期的海外特许权，"
            "无续期证据，因此永续增长下调约 1 个百分点；第 6 年股东现金与成长投资同比例增长，派息率 48%、股数不变。"),
        "terminal_funding": {"owner_cash_or_proxy": own6, "remaining_growth_uses": gro6, "remaining_mandatory_uses": 0,
                             "recurring_fad": own6 - gro6, "dividend_cash_cost": q5["dividend_entitlement"] * (1 + g),
                             "dividend_entitlement": q5["dividend_entitlement"] * (1 + g), "cash_settled_fraction": 1,
                             "settlement_cash_adjustment": 0, "dividend_entitled_shares": SHARES,
                             "fx_to_valuation_currency": 1, "investor_cash_deductions": 0},
        "forecast_cash_flows": path, "present_value_of_dividends": explicit, "present_value_of_terminal": terminal,
        "total_value": explicit + terminal, "terminal_value_share": terminal / (explicit + terminal)})
gv_vals = {row["scenario"]: row["total_value"] for row in gscen}
g_low, g_high = min(gv_vals.values()), max(gv_vals.values())
base_path = gscen[1]["forecast_cash_flows"]
g_sens = []
for rate in (R_LOW, R_MID, R_HIGH):
    for g in (0.01, 0.015, 0.02, 0.025):
        ok = g <= G_BOUND["Base"]
        val = sum(pv(base_path, rate, g, run_map[(5, "Base")]["derived_dps"] * (1 + g), TIMES[-1])) if ok else None
        g_sens.append({"required_return": rate, "terminal_growth": g, "value": val,
                       "status": "calculated" if ok else "invalid_growth_cap",
                       "basis": "Base 现金路径不变，只改变折现率与永续增长；超过 Base 可持续增长上限 2% 的组合不计算。"})
r["growth_valuation"] = {
    "explicit_horizon_years": 5, "transition_years": 0, "terminal_growth_cap": 0.03, "long_run_nominal_growth_bound": LONG_RUN,
    "growth_cap_evidence": "港元／人民币现金对应的长期名义增长约 4%；码头行业成熟、海外特许权有期限，终值增长上限取 3%，各情景另设更低的公司上限。",
    "minimum_return_growth_spread": 0.02, "scenarios": gscen,
    "growth_value_low": g_low, "growth_value_high": g_high, "base_case_value": gv_vals["Base"],
    "margin_of_safety": MOS,
    "margin_of_safety_basis": "15%：联营现金上缴率、贸易摩擦与特许权续期均为有界估计，安全边际不替代缺失证据。",
    "entry_upper": g_low * (1 - MOS), "review_above": g_high,
    "terminal_dependence_warning": "约 64%–73% 的价值来自第 5 年之后的永续部分，结论对永续增长和折现率敏感，见敏感性表。",
    "return_growth_sensitivity": g_sens}
r["growth_assessment"] = {
    "status": "eligible", "funded_dividend_path": True, "reinvestment_to_dps_reconciled": True,
    "capital_remittance_verified": True, "credible_terminal_state": True, "growth_method": "direct_operating_to_dps",
    "evidence_and_reason": ("三种情景五年股息均由经常性可分配现金覆盖（Base 约 1.7 倍）；成长投资每年 3–9 亿港元对应吞吐量 2%–4% 增长，"
                            "按 48% 派息率直接转化为每股股息，股数不变；联营现金上缴率按 2025 年 55% 的有界估计；"
                            "终值已为海外特许权到期下调增长。预测可信度为中等，不支持强力买入。")}

def market_implied(g):
    lo, hi = g + 0.02, 0.2
    for _ in range(80):
        m = (lo + hi) / 2
        v = sum(pv(base_path, m, g, run_map[(5, "Base")]["derived_dps"] * (1 + g), TIMES[-1]))
        lo, hi = (m, hi) if v > PRICE else (lo, m)
    return m
implied = {g: market_implied(g) for g in (0.015, 0.02)}

inc_starter, inc_add, inc_strong = starter, add, strong          # income comparison (no credit)
starter = gv_vals["Base"] * (1 - MOS)
add = min(starter, g_low)
strong = g_low * (1 - MOS)
r["valuation_mode"] = "total_return_based"
r["valuation_reason"] = ("Operating port holding company with evidenced, funded modest growth: a five-year dividend-discount model "
                         "with a fading terminal sets the stages; the no-credit income ladder is kept as a comparison.")

# ---------------- entry plan and decision ----------------
ep = r["entry_plan"]
ep.update({"current_action": "wait_for_price",
           "summary": f"At HKD {PRICE} the forward yield is {fwd:.1%}, below the US 10-year Treasury; the Base dividend-discount value is HKD {gv_vals['Base']:.2f} at a {R_MID:.2%} required return, and the price implies only about {implied[0.015]:.1%}-{implied[0.02]:.1%}.",
           "opportunity_thesis": "Stable port cash with modest growth, but associate cash conversion and the low yield leave no income margin of safety.",
           "market_expectation_gap": f"Price is 0.64x book value (26.3 HKD/share) and about {PRICE / 1.538:.1f}x 2025 EPS; the market discounts associate cash conversion and geopolitical risk."})
ep["stages"] = [
    {"stage": "starter", "valuation_price": starter, "effective_price": starter, "gap_to_current_pct": pct(starter),
     "status": "waiting_price", "condition": f"Base DDM value {gv_vals['Base']:.2f} x (1 - {MOS:.0%}) = HKD {starter:.2f}."},
    {"stage": "add", "valuation_price": add, "effective_price": add, "gap_to_current_pct": pct(add),
     "status": "waiting_price", "condition": f"Lowest scenario (Bear) DDM value = HKD {add:.2f}."},
    {"stage": "strong_buy", "valuation_price": strong, "effective_price": strong, "gap_to_current_pct": pct(strong),
     "status": "waiting_evidence", "condition": f"Bear DDM value x (1 - {MOS:.0%}) = HKD {strong:.2f}, plus High confidence and Strong safety."}]
cash3 = {s_: sum(dps[s_][:3]) for s_ in SCEN}
exits = {"Bear": dps["Bear"][2] / R_LOW, "Base": dps["Base"][2] / fwd, "Bull": dps["Bull"][2] / 0.045}
ep["return_scenarios"] = [{"scenario": s_, "horizon_years": 3, "net_cash_received": cash3[s_], "exit_price": exits[s_],
                           "costs": 0, "cumulative_return": (cash3[s_] + exits[s_]) / PRICE - 1,
                           "basis": {"Bear": f"Exit at Bear FY2028 DPS / R_low {R_LOW:.2%}.", "Base": f"Exit at Base FY2028 DPS / current yield {fwd:.2%}.",
                                     "Bull": "Exit at Bull FY2028 DPS / 4.5%."}[s_] + " No reinvestment or costs.",
                           "source_refs": [IR26, PX]} for s_ in ("Bear", "Base", "Bull")]
ep["risk_review"].update({"rationale": f"Bear re-rating to the required yield loses {-ep['return_scenarios'][0]['cumulative_return']:.0%} including three years of dividends.", "source_refs": [IR26, PX]})
ep["blockers"] = [{"scope": "price", "reason": f"Price {PRICE} is above the Base DDM starter HKD {starter:.2f}; implied return about {implied[0.015]:.1%} versus required {R_LOW:.2%}-{R_HIGH:.2%}.",
                   "resolution": f"Price at or below HKD {starter:.2f}, or evidence of materially higher sustainable dividends.", "source_refs": [IR26, PX]},
                  {"scope": "position_sizing", "reason": "Existing holding size and cost not supplied.",
                   "resolution": "Provide holdings before any sizing discussion.", "source_refs": []}]
ep["catalysts"] = [{"event": "FY2026 results and final dividend", "check_date_or_period": "March 2027",
                    "confirmation": "Full-year DPS near 0.78 HKD and associate cash dividends at least 55% of their profits.",
                    "source_to_revisit": "HKEXnews results announcement", "if_missed": "Rebuild N and stage prices."}]
ep["invalidation_conditions"] = ["Associate/JV cash dividends below 40% of their attributable profit.",
                                 "Reintroduction of a scrip dividend or a payout ratio below 40%."]
r["action_assessment"].update({"status": "eligible", "strong_buy_eligible": False,
                               "reasons": ["Evidence supports a funded growth DDM; price is above every stage."],
                               "capital_risk_and_total_return_check": "See entry_plan.return_scenarios."})
r["decision"].update({"current_action": "等待到价", "can_buy_now": False,
    "reason": f"计入股息增长后（成长股息折现模型），Base 情景每股价值约 {gv_vals['Base']:.2f} 港元，现价 {PRICE} 港元高出约 {(PRICE / gv_vals['Base'] - 1):.0%}；按现价买入的预期年回报只有约 {implied[0.015]:.1%}–{implied[0.02]:.1%}，低于 8.84%–10.84% 的必要回报。远期股息率约 {fwd:.1%}，也低于美国 10 年期国债 4.84%。",
    "buy_conditions": [{"kind": "price", "observable": "招商局港口收盘价", "operator": "<=", "threshold": round(starter, 2), "unit": "HKD", "source_to_watch": "港交所实时报价"}],
    "invalidation_conditions": [
        {"kind": "metric", "observable": "联营及合营公司现金分红占应占利润比例", "operator": "<", "threshold": 40, "unit": "%", "source_to_watch": "年报现金流量表与分部资料"},
        {"kind": "event", "observable": "公司恢复以股代息或派息率降至 40% 以下", "operator": "published", "threshold": "已公告", "unit": "公告事件", "source_to_watch": "港交所派息公告"}],
    "trap_conclusion": "未触发红利陷阱：股息有经营现金覆盖；需警惕联营公司现金上缴率和以股代息历史。",
    "entry_conclusion": f"成长股息折现口径参考价：初始建仓 {starter:.2f} 港元、逐步增持 {add:.2f} 港元、强力买入 {strong:.2f} 港元；收息口径（不计增长）对照为 {inc_starter:.2f}／{inc_add:.2f}／{inc_strong:.2f} 港元。两种方法结论一致，现价高出较多。",
    "price_status": "reference_prices",
    "reference_prices": {"starter": starter, "add": add, "strong_buy": strong, "income_capped_upper": starter}})

# ---------------- scorecard ----------------
def chk(n, st, ev): return {"check": n, "status": st, "evidence": ev, "source_refs": S}
spec = {
 "net_yield": (15, fwd, 3, 6, 9, ["unknown", "not_met", "not_met"],
   ["FY2026 final dividend not yet declared; interim 0.25 paid.", f"B/price {B / PRICE:.2%} below r_high {R_HIGH:.2%}.", f"N/price {fwd:.2%} below R_low {R_LOW:.2%}."],
   f"N/price {fwd:.2%} sits in the 3.5%-5% band."),
 "dividend_stability": (15, None, 2, 8, 11, ["met", "not_met", "not_met"],
   ["Interim and final dividends paid every year 2021-2025.", "DPS fell from 0.94 (2021) to 0.739 HKD (2025).", "2021-2023 dividends were partly settled in scrip, an extraordinary funding aid."],
   "DPS follows earnings at a 41%-48% payout with mild cyclicality."),
 "cash_coverage": (20, None, 2, 12, 16, ["met", "met", "met"],
   ["Bear, Base and Bull years 1-3 FAD cover the 48% dividend.", f"Worst 2021-2025 entitlement coverage {min(covs):.2f}x ({YEARS[covs.index(min(covs))]}).", "Cash 11,695m at end-2025 exceeds a year of dividends."],
   f"Three-year owner cash / full entitlement is {sum(owner[2:]) / sum(entitle[2:]):.2f}x."),
 "balance_sheet": (15, None, 1, 12, 15, ["met", "met", "not_met"],
   ["Debt due within one year 21,716m versus undrawn facilities 27,628m plus cash 11,695m at end-2025.", "Net interest-bearing debt 21,675m at mid-2026, about 17% of equity.", "Net current liabilities 7,403m; relies on rolling bank loans (22,740m drawn in 2025)."],
   "Low leverage relative to equity."),
 "capital_allocation": (15, None, 2, 8, 11, ["met", "unknown", "not_met"],
   ["Payout of 46%-48% consistent with stated discretion.", "Returns on new overseas investments not disclosed per project.", "Scrip issuance 2021-2023 diluted shares by about 13%."],
   "Reasonable but discretionary policy."),
 "buyback_quality": (10, None, 3, 2, 4, ["met", "not_met", "met"],
   ["Share count reconciles: 3,704m (2021) to 4,198m (2024-2025) via scrip.", "No buybacks; scrip issued well below book value.", "No capital return strains the investment plan."],
   "No buybacks; past scrip dilution."),
 "visibility": (10, None, 2, 5, 7, ["met", "met", "not_met"],
   ["Years 1-3 tie to 1H26 profit and FY2025 cash ratios.", "Years 4-5 bounded Bear/Bull extensions.", "Associate dividend conversion swung 45%-80% in 2021-2025."],
   "Moderate visibility: trade volumes and associate payouts."),
}
mods, ranges = [], {}
order = list(spec)
for name, (w, metric, band, lo, hi, sts, evs, why) in spec.items():
    k = sts.count("met")
    raw = lo + ((hi - lo) * k) // 3
    mods.append({"module": name, "weight": w, "assessment": "assessed", "evidence_basis": "reconstructed",
                 "metric_value": metric if name != "cash_coverage" else sum(owner[2:]) / sum(entitle[2:]),
                 "period": "FY2021-2025 and FY2026 Base at the 2026-11-09 quote", "band": band, "rationale": why,
                 "checks": [chk(i + 1, st, ev) for i, (st, ev) in enumerate(zip(sts, evs))],
                 "raw_score": raw, "cap": w, "cap_reason": "No lower cap applies.", "final_score": raw,
                 "source_refs": S, "missing_evidence": [ev for st, ev in zip(sts, evs) if st == "unknown"]})
    ranges[name] = {"low": raw, "high": raw}
pts = {m["module"]: m["final_score"] for m in mods}
quality = sum(v for k_, v in pts.items() if k_ != "net_yield"); income = pts["net_yield"]; total = quality + income
grade = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 55 else "D" if total >= 40 else "E"
qlabel = "High" if quality >= 68 else "Medium" if quality >= 51 else "Low"
print("scores", pts, quality, income, total, grade)
sc = r["scorecard"]
sc["modules"] = [dict(old, **new) for old, new in zip(sorted(sc["modules"], key=lambda m: order.index(m["module"])), mods)]
sc.update({"quality_score_85": quality, "income_score_15": income, "assessed_points": total, "assessed_weight": 100, "unadjusted_grade": grade})
sm = sc["summary"]
sm.update({"status": "complete", "module_ranges": ranges, "score_range": {"low": total, "high": total},
           "quality_range": {"low": quality, "high": quality}, "income_range": {"low": income, "high": income},
           "grade_range": {"worst": grade, "best": grade}, "quality_rating_range": {"worst": qlabel, "best": qlabel}})
qa = r["quality_assessment"]
qa.update({"status": "assessed", "components": {k_: v for k_, v in pts.items() if k_ != "net_yield"}, "score_85": quality,
           "component_ranges": {k_: v for k_, v in ranges.items() if k_ != "net_yield"}, "score_range": {"low": quality, "high": quality},
           "evidence_and_limitations": "Rubric-2 points reconstructed from CMPort annual reports 2022-2025 and the 2026 interim report."})
ttm_dps = 0.489 + 0.25
r["key_metrics_at_a_glance"].update({"ttm_net_yield": ttm_dps / PRICE, "normalized_net_yield": fwd, "quality_score_85": quality,
    "current_action": "wait_for_price", "score_status": "complete", "score_range": {"low": total, "high": total},
    "quality_score_range": {"low": quality, "high": quality}, "grade_range": {"worst": grade, "best": grade},
    "score_100": total, "grade": grade, "valuation_mode": "total_return_based"})
r["dividend_snapshot"].update({"ttm_dps": ttm_dps, "ttm_net_yield": ttm_dps / PRICE, "normalized_net_dps": N})
three_y = "Grow" if dps["Base"][2] > dps["Base"][0] * 1.05 else "Decline" if dps["Base"][2] < dps["Base"][0] * 0.95 else "Stable"
bbq = "Poor" if pts["buyback_quality"] <= 4 else "Neutral"
r.update({"score_100": total, "grade": grade, "dividend_quality": qlabel, "dividend_safety": "Acceptable",
          "three_year_outlook": three_y, "buyback_quality": bbq, "fundamental_trend": "Stable", "forecast_confidence": "Medium",
          "portfolio_role": "Watchlist",
          "score_limitations": f"Rubric-2 point score from public filings: quality {quality}/85 plus income {income}/15 = {total}/100."})
ra = r["rating_audit"]
for k_, v in ra.items():
    v["source_refs"] = S
ra["dividend_quality"].update({"label": qlabel, "rule": "Quality 51-67/85 is Medium; price excluded.",
    "supporting_evidence": "+".join(str(v) for k_, v in pts.items() if k_ != "net_yield") + f"={quality}.",
    "upgrade_trigger": "Quality reaches 68, e.g. stable DPS and higher associate cash conversion.", "downgrade_trigger": "Quality below 51."})
ra["dividend_safety"].update({"label": "Acceptable", "rule": "Aggregate >= 1.0x with a funded Base policy.",
    "supporting_evidence": f"Three-year entitlement coverage {sum(owner[2:]) / sum(entitle[2:]):.2f}x; worst {min(covs):.2f}x."})
ra["withholding_efficiency"].update({"supporting_evidence": "2026 interim cash dividend announcement: withholding not applicable."})
ra["buyback_quality"].update({"label": bbq, "rule": "Scrip dilution without offsetting buybacks.",
    "supporting_evidence": "Weighted shares 3,704m (2021) to 4,198m (2024); no buybacks."})
ra["three_year_outlook"].update({"label": three_y, "rule": "Base year-3 DPS vs year 1 with a 5% band.",
    "supporting_evidence": f"Base DPS {dps['Base'][0]:.3f} to {dps['Base'][2]:.3f} HKD; Bear {dps['Bear'][0]:.3f} to {dps['Bear'][2]:.3f}."})
for k_ in ("fundamental_trend", "forecast_confidence", "portfolio_role"):
    for fld in ("supporting_evidence", "rule"):
        ra[k_][fld] = {"fundamental_trend": "Throughput growing about 4%-5% a year; profit flat-to-up excluding 2021 peak.",
                       "forecast_confidence": "Bounded analyst estimates reconciled to 2025 cash ratios and 1H26 profit.",
                       "portfolio_role": "Medium quality, Acceptable safety; income mandate unknown."}[k_]
r["income_drivers"] = [{"driver": "contracted_volumes", "exposure_direction": "higher_supports_income", "horizon": "One to three years",
                        "transmission": "Throughput drives terminal revenue and associate profits, then cash dividends to the parent.", "evidence": IR26}]

# ---------------- evidence recovery ----------------
SUB = "https://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId=600018"
def attempts(rows, sub=("inaccessible", "上港集团（600018）年报在上交所网站，不在本环境网络白名单内")):
    cats = ["issuer_filings", "group_disclosures", "announcements", "exchange_regulator",
            "official_series", "historical_comparables", "broker_records"]
    out = []
    for c, (src_, per, outc, res) in zip(cats, rows):
        scope = "investor" if c == "broker_records" else ("parent" if c == "group_disclosures" else "issuer")
        out.append({"category": c, "scope": scope, "source": src_, "source_period": per, "attempted_on": AS_OF,
                    "outcome": outc, "result": res})
        if c == "group_disclosures":
            out.append({"category": c, "scope": "subsidiary", "source": SUB, "source_period": "2025 财年",
                        "attempted_on": AS_OF, "outcome": sub[0], "result": sub[1]})
    return out
def paths(mods_):
    out = []
    for i, m in enumerate(r["scorecard"]["modules"]):
        if m["module"] in mods_:
            out += [f"/scorecard/modules/{i}/checks/{j}/status" for j, c in enumerate(m["checks"]) if c["status"] == "unknown"]
            if m["missing_evidence"]:
                out.append(f"/scorecard/modules/{i}/missing_evidence")
    return out
co = lambda obs, src_: {"kind": "event", "observable": obs, "operator": "published", "threshold": "已公告", "unit": "公告事件", "source_to_watch": src_}
LIST = "https://www1.hkexnews.hk/search/titlesearch.xhtml"
r["evidence_recovery"].update({"scope": "live_research", "scope_reason": "联网查阅招商局港口 2021–2025 年报、2026 年中报、派息公告及行情", "is_group_structure": True})
r["evidence_recovery"]["records"] = [
 {"field_paths": ["/holding_review/action",
                  "/holding_review/missing_inputs", "/income_assessment/target/target_basis",
                  "/income_assessment/target/target_policy", "/real_income/status"],
  "reason": "用户未提供收息目标、持仓与成本；未做通胀测算",
  "impact": "不判断收入匹配度、不给仓位建议；不评估实际购买力",
  "resolution": "not_assessable",
  "attempts": attempts([
    (AR25, "2025 财年", "found", "公司披露不含投资者个人信息"),
    (AR25, "2025 财年", "found", "母公司披露派息政策与分部资料"),
    (DIV26, "2026 年中期", "found", "确认中期股息为现金，无以股代息"),
    (LIST, "截至 2026-11-09", "not_found", "无投资者个人信息"),
    (UST, "2026-11-05", "found", "取得美国 10 年期国债收益率，未取得香港通胀与港债收益率"),
    (AR23, "2022–2023 财年", "found", "历史现金流可支持后续成长模型"),
    ("用户券商记录", "未提供", "not_provided", "用户未提供持仓、成本与收息目标")]),
  "estimate": None, "estimate_failure_reason": "缺少用户输入与香港通胀序列，无法收窄",
  "closure_condition": co("用户提供持仓、成本及收息目标", "用户补充信息")},
 {"field_paths": paths({"net_yield", "capital_allocation"}),
  "reason": "2026 年末期股息尚未宣派；海外新项目的单项投资回报未披露",
  "impact": "这两项不计加分；远期股息按 48% 派息率估算",
  "resolution": "not_assessable",
  "attempts": attempts([
    (IR26, "2026 年上半年", "found", "中期股息 0.25 港元；未披露末期股息与项目回报"),
    (AR25, "2025 财年", "found", "母公司披露分部利润，未披露单项目回报"),
    (DIV26, "2026 年中期", "found", "仅含中期股息"),
    (LIST, "截至 2026-11-09", "not_found", "无末期股息公告"),
    ("https://fred.stlouisfed.org/", "不适用", "not_applicable", "无相关官方序列"),
    (AR22, "2021–2022 财年", "found", "历年派息率 40%–48%，末期股息随全年利润决定"),
    ("用户券商记录", "未提供", "not_provided", "与公司层面判断无关")]),
  "estimate": None, "estimate_failure_reason": "末期股息取决于全年利润与董事会决定，公告前无法确定；项目回报未披露",
  "closure_condition": co("招商局港口公布 2026 年末期股息", "港交所派息公告")}]

# ---------------- residual texts ----------------
bo = r["business_outlook"]
for row in bo["cumulative_fad"]:
    fad = [fc_map[(y, row["scenario"])]["recurring_fad"] for y in range(1, 6)]
    row.update({"three_year": sum(fad[:3]), "five_year": sum(fad), "limitations": "Sum of modeled recurring FAD before dividends."})
bo.update({"data_cutoff": AS_OF,
           "competitive_position": "Largest port operator in the Pearl River Delta (West Shenzhen), major associate stakes in SIPG and Ningbo-Zhoushan, and overseas terminals in Sri Lanka, Brazil, Togo, Turkey and others.",
           "management_execution": "Throughput grew 3.8% in 2025 and 4.5% in 1H26; payout 46%-48% since 2023; scrip discontinued from the 2024 final.",
           "extension_limitations": "Years 4-5 extend Base profit growth of about 2% a year; analyst estimate.",
           "drivers": [dict(bo["drivers"][0], **{"driver": d, "segment": sg, "baseline": bl, "year_three_outcome": y3, "year_five_outcome": y5,
                "investment_and_funding": "Funded from operating cash; growth capex 300-900m HKD a year.",
                "fcf_transmission": "Throughput and tariffs drive terminal profit; associate profits reach the parent only as cash dividends.",
                "evidence_type": "reported_fact", "source_and_date": IR26, "confidence": "Medium", "invalidation_signal": inv})
                for d, sg, bl, y3, y5, inv in (
                  ("Throughput", "Group ports", "78.21m TEU in 1H26, +4.5%", "Base +3%-4% a year", "Base +2%-3% a year", "Two consecutive halves of throughput decline"),
                  ("Associate cash conversion", "SIPG and other associates", "2,730m HKD received vs 4,970m profit in 2025", "Base about 55%", "Base about 55%", "Below 40% for a full year"),
                  ("Interest cost", "Group", "Interest paid 1,193m HKD in 2025", "Base stable", "Base stable", "Net debt above 30% of equity"))]})
for m in bo.get("milestones", []):
    m["source_to_revisit"] = "CMPort FY2026 annual results on HKEXnews"
r["business_fundamentals"] = {"dividend_funding_engine": "Consolidated terminal cash (West Shenzhen, Hong Kong, overseas) plus cash dividends from associates such as SIPG fund the parent; minority holders and interest take a large share first.",
                              "core_operating_drivers": ["Container throughput", "Associate cash dividends", "Interest and minority claims"],
                              "historical_operating_trend": []}
r["controller_risk"].update({"status": "no_material_concern", "listed_company_impact": "China Merchants Group controls the company through China Merchants Port Group; the 2021-2023 scrip dividend schemes settled most dividends in new shares, retaining cash in the listed company.",
                             "source_and_date": AR25, "assessed_on": AS_OF})
r["real_income"].update({"currency": "HKD", "inflation_basket": "Hong Kong CPI not retrieved in this run.", "source_and_method": "Not assessed: inflation series not retrieved; nominal DPS fell from 0.94 to 0.739 HKD (2021-2025)."})
r["fx_risk"].update({"status": "not_material", "economic_exposure": "HKD dividends; group earns RMB, HKD, USD and EUR-linked tariffs.",
                     "operating_currencies": ["CNY", "HKD", "USD"], "distribution_currency": "HKD", "investor_currency": "HKD",
                     "material_exposure": False, "hedge_and_natural_offsets": "RMB translation affects reported profit; dividends declared in HKD.",
                     "evidence_and_limitations": AR25})
r["holding_review"].update({"rationale": "User holds the stock but did not supply size, cost or income target; no trade instruction is given.", "next_review": "FY2026 results, March 2027"})
r["holding_review"]["triggers"][0].update({"threshold": "Revisit if associate cash conversion falls below 40% or scrip is reintroduced.", "evidence": AR25})
r["portfolio_role_assessment"]["rationale"] = "Medium quality and Acceptable safety; income mandate unknown, so the role stays Watchlist."
for k_, v in r["rating_audit"].items():
    for fld in ("supporting_evidence", "rule", "upgrade_trigger", "downgrade_trigger"):
        if isinstance(v.get(fld), str) and ("ictional" in v[fld] or "teaching" in v[fld] or "Already in the highest" in v[fld]):
            v[fld] = "Reassess at the next annual results with updated cash, payout and share-count evidence."
r["visual_summary"] = {**r["visual_summary"],
    "business_and_fcf_trend": f"Owner cash after all capex {owner[0]}-{owner[4]}m HKD (2021-2025); Base FY2026 FAD {fc_map[(1, 'Base')]['recurring_fad']:.0f}m.",
    "dps_path": f"Base DPS {dps['Base'][0]:.3f}/{dps['Base'][2]:.3f}/{dps['Base'][4]:.3f} HKD in 2026/2028/2030.",
    "yield_normalization": f"Forward yield {fwd:.2%} vs US 10y 4.84%.",
    "main_driver_sensitivity": "Associate cash conversion and throughput drive the Bear case.",
    "valuation_summary": f"DDM stages HKD {starter:.2f}/{add:.2f}/{strong:.2f}; income comparison {inc_starter:.2f}/{inc_add:.2f}/{inc_strong:.2f}; price 0.64x book.",
    "coverage_labels": f"Three-year entitlement coverage {sum(owner[2:]) / sum(entitle[2:]):.2f}x; worst {min(covs):.2f}x."}
for i, row in enumerate(r["five_year_dividend_history"]):
    row.update({"fiscal_year": YEARS[i], "coverage_label": "Strong" if covs[i] >= 1.5 else "Adequate" if covs[i] >= 1 else "Weak",
                "quality_tag": "Stable"})
r["driver_sensitivity"][0].update({"driver_name": "One-year associate dividend shortfall",
    "driver_change": "Associate cash dividends 30% lower for one year; later years unchanged."})

# ---------------- report body ----------------
T = lambda title, cols, rows, note: {"title": title, "columns": cols, "rows": rows, "note": note}
NOTE = "港币百万（每股为港元），财年截至 12 月 31 日；来源：招商局港口 2022、2023、2025 年报"
bv = 110403 / SHARES
sections = [
 ("摘要与投资结论", [
   "招商局港口是周期／稳定之间的港口控股公司：盈利来自珠三角控股码头、上港集团等联营码头和海外特许经营码头，股息按归属利润约 48% 派发。",
   f"主估值采用成长股息折现模型（逐年折现五年股息，再加逐步放缓的永续部分）：Base 情景每股价值约 {gv_vals['Base']:.2f} 港元（Bear {gv_vals['Bear']:.2f}，Bull {gv_vals['Bull']:.2f}），初始建仓约 {starter:.2f} 港元；不计增长的收息口径对照为 {inc_starter:.2f} 港元，两者接近。现价 {PRICE} 港元隐含的预期年回报只有约 {implied[0.015]:.1%}–{implied[0.02]:.1%}，比美国 10 年期国债只高约 {(implied[0.015] - RF) * 100:.1f}–{(implied[0.02] - RF) * 100:.1f} 个百分点，新资金动作“等待到价”。",
   f"最重要的结构性特点：2025 年约 {ASSOC_PROFIT_2025 / 6457:.0%} 的归属利润来自联营及合营公司，但当年只收到 {2730 / ASSOC_PROFIT_2025:.0%} 的现金分红；2021–2023 年股息部分以股代息，股数增加约 13%。"],
  [T("摘要关键数字", ["指标", "数值", "说明"], [
     ["现价", f"{PRICE} 港元", "2026-11-09 收盘"],
     ["2025 年每股股息", "0.739 港元", f"TTM 股息率 {ttm_dps / PRICE:.1%}，派息率 48.1%"],
     ["2026 年 Base 每股股息", f"{N:.3f} 港元", f"远期股息率 {fwd:.1%}"],
     ["美国 10 年期国债", "4.84%", "2026-11-05；联系汇率下作港元无风险锚"],
     ["成长折现 Base 每股价值", f"{gv_vals['Base']:.2f} 港元", f"必要回报 {R_MID:.2%}，永续增长 1.5%"],
     ["初始建仓价（成长口径）", f"{starter:.2f} 港元", f"较现价 {pct(starter):+.0f}%；收息口径对照 {inc_starter:.2f}"],
     ["现价隐含年回报", f"{implied[0.015]:.1%}–{implied[0.02]:.1%}", "Base 现金路径，永续增长 1.5%–2%"],
     ["三年股息覆盖（全部应派）", f"{sum(owner[2:]) / sum(entitle[2:]):.2f} 倍", "2023–2025，扣除全部资本开支后"],
     ["质量／综合评分", f"{quality}/85，{total}/100（{grade}）", "完整评估"]],
     "股价来自 Yahoo Finance，国债来自 FRED，其余来自招商局港口年报与 2026 年中报")]),
 ("公司概况与行业定位", [
   "招商局港口在港交所上市，控股股东为招商局集团。业务包括：深圳西部港区（蛇口、赤湾、妈湾）及香港码头等控股港口；上港集团、宁波舟山港等联营权益；斯里兰卡、巴西、多哥、土耳其、印尼等海外码头；以及保税物流。",
   "按经济特征分类：三块业务都是“量×价”的经营型码头，随外贸周期波动；海外码头是有到期日的特许经营权，需要逐项按剩余年限估值，但这不等于公司整体到期；公司属控股母公司，大量利润来自联营合营，必须看实际收到的现金分红。"]),
 ("行业结构、供需与周期", [
   "港口需求跟随全球及中国外贸集装箱量。2026 年上半年亚洲港口吞吐量同比增 5%，集团吞吐量 7,821 万标箱，同比增 4.5%；红海绕航改变了航线结构，中东港口量大幅下降。",
   "未来三至五年的三个驱动因素：第一，中美贸易摩擦与关税对华南出口量的影响；第二，上港集团等联营公司的派息政策（决定现金上缴率）；第三，海外码头（斯里兰卡、巴西）在区域航线重组中的份额。港口资本开支周期长，新增产能有限，费率总体稳定。"]),
 ("竞争格局与公司护城河", [
   "护城河来自稀缺的深水泊位和长期土地使用权或特许经营权，以及在深圳西部港区的领先份额；海外码头多位于“一带一路”枢纽港。",
   "本次未取得中远海运港口、和记港口信托等同业的同口径数据，不列对比表；下次复评应补充同业的市净率、股息率和联营现金转化率。"]),
 ("过去五年经营与财务趋势", [
   "收入从 2021 年的 118.5 亿港元增至 2025 年的 133.5 亿港元，但归属利润从 81.4 亿港元降至 64.6 亿港元，每股盈利从 2.199 港元降至 1.538 港元，部分原因是以股代息增加了股数（约 13%）。",
   "恶化信号：每股盈利五年下降 30%，属于持续性下降，主要来自联营公司利润回落和股数摊薄，不是单年事件；2026 年上半年利润同比增 6.9%，出现企稳迹象。趋势状态：每股盈利与每股股息为黄色，现金生成为绿色。"],
  [T("五年经营与股东回报", ["财年", "收入", "归属利润", "每股盈利", "每股股息", "加权股数（百万）", "联营合营现金分红"],
     [[YEARS[i], REV[i], PROFIT[i], EPS[i], DPS[i], round(WSHARES[i], 1), ASSOC_DIV[i]] for i in range(5)],
     NOTE)],
  [{"title": "每股盈利与每股股息", "kind": "line", "unit": "港元／股", "x_labels": YEARS,
    "series": [{"name": "每股盈利", "values": EPS}, {"name": "每股股息", "values": DPS}],
    "source": "招商局港口 2025 年报五年财务摘要"}]),
 ("现金流、资产负债与股息质量", [
   f"股东可分配现金 = 经营现金流（已含联营合营分红）− 利息 − 租赁 − 全部资本开支 − 少数股东分红 − 永续债分派。2023–2025 年合计覆盖全部应派股息 {sum(owner[2:]) / sum(entitle[2:]):.2f} 倍，最差年份 {YEARS[covs.index(min(covs))]} 年为 {min(covs):.2f} 倍（当年少数股东分红高达 18.8 亿港元）。",
   "这里按“全部应派股息”计算，而不是实际付出的现金：2021–2023 年股东可选择以股代息，大部分股息以新股支付，实际现金派息只有 9–12 亿港元，若按现金计算覆盖率会被高估到 3–4 倍。2025 年末期和 2026 年中期均为纯现金派息。",
   "资产负债：2026 年 6 月末净有息负债 216.8 亿港元，约为权益的 17%；但存在 74 亿港元净流动负债，一年内到期债务 217 亿港元，依赖 276 亿港元未动用额度滚动。香港注册公司，派息不预扣税。股息安全性判断为“可接受”。"],
  [T("历年股东现金与股息覆盖", ["财年", "经营现金流", "资本开支", "利息与租赁", "少数股东与永续", "股东可分配现金", "全部应派股息", "覆盖倍数", "实付现金股息"],
     [[YEARS[i], OCF[i], CAPEX[i], INTEREST[i] + LEASE[i], NCI_DIV[i] + PERP[i], owner[i], entitle[i], round(covs[i], 2), CASH_DIV_PAID[i]] for i in range(5)],
     "港币百万；全部应派股息 = 每股股息 × 加权股数；实付现金股息较低的年份为以股代息")],
  [{"title": "股东可分配现金与全部应派股息", "kind": "bar", "unit": "港币百万", "x_labels": YEARS,
    "series": [{"name": "股东可分配现金", "values": owner}, {"name": "全部应派股息", "values": entitle}, {"name": "实付现金股息", "values": CASH_DIV_PAID}],
    "source": "招商局港口 2022、2023、2025 年报现金流量表"}]),
 ("企业成长性与资本配置", [
   "增长来自吞吐量（每年约 3%–5%）和海外项目，但过去五年没有转化为每股增长：每股盈利下降 30%，每股股息下降 21%。资本开支已从 2021 年的 18.3 亿港元降到 2025 年的 8.7 亿港元，自由现金改善。",
   "资本配置：派息率稳定在 46%–48%；以股代息在 2024 年后停止，是对小股东有利的变化；没有回购。海外新项目的单项回报未披露，无法判断再投资是否创造每股价值。"]),
 ("未来五年经营与现金流预测", [
   "Base：2026 年归属利润约 68.5 亿港元（上半年 38.3 亿，下半年按去年同期增长 5%），此后每年增长约 2%–3%。Bear：贸易摩擦导致吞吐量下滑、联营分红减少，2027–2028 年利润降至 57–59 亿港元。Bull：吞吐量和联营派息超预期。",
   "派息率按 48%，股数不变。现金比例按 2025 年校准：扣除利息租赁后的经营现金约为利润的 1.14 倍，少数股东与永续债约占利润的 20%。"],
  [T("情景每股股息（港元）", ["情景", "2026", "2027", "2028", "2029", "2030"],
     [[s_] + [round(d, 3) for d in dps[s_]] for s_ in ("Bear", "Base", "Bull")],
     "按 48% 派息率 ÷ 41.98 亿股；分析师估算")]),
 ("估值与预期总回报", [
   f"主估值：成长股息折现模型。逐年折现 2026–2030 年预测股息（2026 年中期 0.25 港元已派，只计末期），第 6 年起按永续增长计算终值。必要回报统一取 {R_MID:.2%}（区间中点），安全边际 15%。Bear／Base／Bull 每股价值 {gv_vals['Bear']:.2f}／{gv_vals['Base']:.2f}／{gv_vals['Bull']:.2f} 港元。",
   "永续增长为何只取 0%／1.5%／2.5%：吞吐量长期增长约 2%–3%，但约 34% 的现金来自 2035–2049 年到期的海外特许权，没有续期证据，所以把永续增长下调约 1 个百分点。约三分之二的价值来自第 5 年之后，结论对折现率和永续增长较敏感，见下表。",
   f"反推：要让现价 {PRICE} 港元成立，在 Base 现金路径和 1.5%–2% 永续增长下，投资者只要求约 {implied[0.015]:.1%}–{implied[0.02]:.1%} 的年回报，即比美国国债高约 {(implied[0.015] - RF) * 100:.1f}–{(implied[0.02] - RF) * 100:.1f} 个百分点。本报告认为联营现金上缴、地缘与特许权风险需要 4–6 个百分点补偿，所以现价偏贵。",
   f"收息口径对照（不计增长）：Base 2026 年每股股息 {N:.3f} 港元 ÷ 8.84%–10.84%，对应 {inc_add:.2f}–{inc_starter:.2f} 港元；与成长口径接近，说明结论不取决于方法选择。增长抵扣检验未通过（每股股息 2021–2025 年年均 {hist_cagr:.1%}），收息口径不计抵扣。",
   f"对照指标：每股账面净资产约 {bv:.1f} 港元，现价约 {PRICE / bv:.2f} 倍市净率；2025 年市盈率约 {PRICE / 1.538:.1f} 倍。低市净率反映市场对联营公司现金上缴、海外特许权到期和地缘风险的折价。",
   "三年持有情景（不计再投资）：Bear 若估值回落到必要收益率约亏损 {:.0%}，Base 估值不变约赚 {:.0%}，Bull 约赚 {:.0%}。".format(
       -ep["return_scenarios"][0]["cumulative_return"], ep["return_scenarios"][1]["cumulative_return"], ep["return_scenarios"][2]["cumulative_return"])],
  [T("成长股息折现模型（每股，港元）", ["情景", "永续增长", "五年股息现值", "终值现值", "每股价值", "终值占比"],
     [[row["scenario"], f"{row['terminal_growth']:.1%}", round(row["present_value_of_dividends"], 2), round(row["present_value_of_terminal"], 2),
       round(row["total_value"], 2), f"{row['terminal_value_share']:.0%}"] for row in gscen],
     f"必要回报 {R_MID:.2%}；股息来自五年预测（48% 派息率、股数不变）；终值资金由第 6 年经常性可分配现金覆盖"),
   T("Base 每股价值对折现率与永续增长的敏感性（港元）", ["必要回报", "永续 1.0%", "永续 1.5%", "永续 2.0%"],
     [[f"{rate:.2%}"] + [round(next(x["value"] for x in g_sens if x["required_return"] == rate and x["terminal_growth"] == g), 2)
                         for g in (0.01, 0.015, 0.02)] for rate in (R_LOW, R_MID, R_HIGH)],
     "Base 现金路径不变；永续增长超过 2%（Base 可持续上限）不计算"),
   T("三年持有情景（每股，港元）", ["情景", "三年累计股息", "第三年末价格", "累计回报"],
     [[row["scenario"], round(row["net_cash_received"], 2), round(row["exit_price"], 2), f"{row['cumulative_return']:.1%}"] for row in ep["return_scenarios"]],
     "退出价格 = 第三年每股股息 ÷ 假设股息率（Bear 8.84%、Base 维持现有、Bull 4.5%）")]),
 ("买点、建仓策略与持仓复评", [
   f"美国 10 年期国债对比：国债 4.84%，招商局港口远期股息率 {fwd:.2%}，利差约 {(fwd - RF) * 100:+.2f} 个百分点，即持有港口股的当期收入还不如国债。补偿只能来自股息增长和估值修复。",
   f"分阶段参考价（成长口径）：初始建仓 = Base 价值 × 85% = {starter:.2f} 港元；逐步增持 = 最低情景价值 = {add:.2f} 港元；强力买入 = 最低情景价值 × 85% = {strong:.2f} 港元。收息口径对照：{inc_starter:.2f}／{inc_add:.2f}／{inc_strong:.2f} 港元。已持有部分：用户未提供仓位和成本，本报告不给出加减仓指令；若联营现金上缴率维持在 55% 以上且不恢复以股代息，持有逻辑不变。"],
  [T("两种方法的分阶段参考价（港元）", ["档位", "成长股息折现", "收息口径（不计增长）", "较现价"],
     [[lab, f"{a:.2f}", f"{b:.2f}", f"{pct(a):+.0f}%"] for lab, a, b in
      (("初始建仓", starter, inc_starter), ("逐步增持", add, inc_add), ("强力买入", strong, inc_strong))],
     "较现价按成长口径计算；成长口径为主估值"),
   T("国债收益率敏感性", ["美国 10 年期国债", "必要回报（中点）", "Base 每股价值（港元）", "初始建仓价（港元）"],
     [[f"{(RF + d) * 100:.2f}%", f"{(R_MID + d) * 100:.2f}%", round(v, 2), round(v * (1 - MOS), 2)]
      for d, v in [(d, sum(pv(base_path, R_MID + d, 0.015, run_map[(5, "Base")]["derived_dps"] * 1.015, TIMES[-1]))) for d in (-0.01, -0.005, 0, 0.005, 0.01)]],
     "风险溢价 5% 不变；Base 现金路径，永续增长 1.5%")]),
 ("风险、监测指标与论点证伪", [
   "最大风险：联营公司（尤其上港集团）减少现金分红，或控股股东恢复以股代息，会直接降低小股东可收到的现金。"],
  [T("风险与监测阈值", ["风险／指标", "当前值", "预警阈值", "影响", "复查时间"], [
     ["联营合营现金分红 ÷ 应占利润", "约 55%（2025）", "低于 40%", "母公司可派现金减少约 7 亿港元", "年报"],
     ["集装箱吞吐量增速", "+4.5%（2026 上半年）", "连续两个半年下降", "Bear 情景成立", "半年报"],
     ["以股代息", "已停止", "重新推出", "小股东被摊薄", "派息公告"],
     ["一年内到期债务 ÷ 未动用额度", "217 亿 ÷ 276 亿", "未动用额度低于到期债务", "再融资风险", "年报"],
     ["海外特许权到期", "首个 2035 年（印尼）", "无续期安排且贡献超过 10%", "到期次年股息下降", "持续"]],
     "阈值为分析判断；当前值来自招商局港口 2025 年报与 2026 年中报")]),
 ("数据来源、关键假设与研究限制", [
   "数据截至 2026-11-09。来源：招商局港口 2022、2023、2025 年报，2026 年中报及中期派息公告（均来自港交所披露易），Yahoo Finance 行情，FRED 美国国债收益率。",
   "关键假设：派息率 48%；股数不变；成长模型必要回报 9.84%、永续增长 0%／1.5%／2.5%、安全边际 15%；扣除利息租赁后的经营现金约为利润 1.14 倍；少数股东与永续债约占利润 20%；风险溢价 4%–6%；以美国国债作港元无风险锚。",
   "研究限制：未取得上港集团年报（上交所网站不在本环境白名单内）、同业数据、香港通胀与港债收益率；海外特许权的现金占比为估算；成长模型的永续增长与联营现金上缴率为有界估计；用户持仓与收息目标未提供。本报告仅为研究资料，不构成投资建议。"]),
]
r["report_output"].update({"title": "招商局港口（0144.HK）完整研究报告",
    "summary": f"数据截至 {AS_OF}；成长股息折现口径初始建仓约 {starter:.2f} 港元（收息口径对照 {inc_starter:.2f}），现价 {PRICE} 港元，等待到价。",
    "sections": [dict({"heading": h, "paragraphs": p_}, **({"tables": rest[0]} if len(rest) > 0 and rest[0] else {}),
                      **({"charts": rest[1]} if len(rest) > 1 and rest[1] else {})) for h, p_, *rest in sections],
    "appendix": ["审计附录 A3、A5、A6、A10、A11、A13 由结构化记录自动生成；A12 持仓复评因未提供持仓而不适用。"],
    "labels": ["金额单位：港币百万，另有注明除外"]})

# @@TAIL@@
json.dump(r, open(OUT, "w"), ensure_ascii=False, indent=2)
sys.path.insert(0, str(SKILL))
from scripts.validate_analysis import validate_report  # noqa: E402
errors = validate_report(r)
print(len(errors)); print("\n".join(e[:260] for e in errors[:40]))
if not errors:
    from scripts.render_report import render_report  # noqa: E402
    (HERE / "cmport-0144.html").write_text(render_report(r), encoding="utf-8")
    print("validated and rendered")
