# Executed inside build_hsbc.py (shares its globals).
S = [AR, Q3]
HK = lambda usd: round(usd * USDHKD, 1)
base_dps = [SCEN["Base"]["profit"][i] * PAYOUT / SHARES for i in range(5)]
bear_dps = [SCEN["Bear"]["profit"][i] * PAYOUT / SHARES for i in range(5)]
bull_dps = [SCEN["Bull"]["profit"][i] * PAYOUT / SHARES for i in range(5)]
fwd_yield = N / PRICE

# ---------------- economic profile ----------------
r["economic_profile"] = {
    "segments": [
        {"name": "香港业务（含恒生银行）", "cash_share_pct": 45, "revenue_engine": "spread_income",
         "asset_life": "perpetual_going_concern", "cyclicality": "rate_cycle",
         "cycle_window": "2021–2025 覆盖港元利率从近零升至约 5% 再回落的完整利率周期",
         "balance_sheet_role": "balance_sheet_spread", "capital_intensity": "asset_light"},
        {"name": "英国零售与商业银行", "cash_share_pct": 25, "revenue_engine": "spread_income",
         "asset_life": "perpetual_going_concern", "cyclicality": "rate_cycle",
         "cycle_window": "2021–2025 覆盖英镑基准利率从 0.1% 升至 5.25% 再回落",
         "balance_sheet_role": "balance_sheet_spread", "capital_intensity": "asset_light"},
        {"name": "企业与机构银行及财富管理", "cash_share_pct": 30, "revenue_engine": "fee_or_aum",
         "asset_life": "perpetual_going_concern", "cyclicality": "demand_cycle",
         "cycle_window": "2021–2025 覆盖贸易与资本市场一轮上下行",
         "balance_sheet_role": "balance_sheet_spread", "capital_intensity": "asset_light"},
    ],
    "legal_wrapper": "ordinary_company", "cash_attribution": "wholly_owned",
    "finite_life_assets": [], "company_level_runoff": False,
    "tax_route": {"distribution_regime": "ordinary_dividend", "exit_withholding_rate": None,
                  "exception_evidence": None, "refunds_excluded_from_cash": True},
    "kpis": [
        {"name": "银行业务净利息收入", "why_causal": "约占收入六成，随利率与存款结构变化，直接决定利润和资本生成"},
        {"name": "CET1 比率与风险加权资产", "why_causal": "资本低于 14% 目标下限时暂停回购，增长占用的资本先于股东回报扣除"},
        {"name": "预期信用损失率", "why_causal": "每上升 10 个基点约减少税前利润 10 亿美元，直接压低派息基数"},
        {"name": "剔除特殊项目的有形股本回报率", "why_causal": "50% 派息率按剔除特殊项目的每股盈利计算，回报率决定每股股息"},
    ],
    "classification_evidence": "2025 年报分部与净利息收入附注；2026 年三季度业绩公告。分部现金占比为按利润贡献的估算",
}

# ---------------- policy, requirements, income ----------------
r["payout_policy"].update({
    "policy_type": "earnings_linked", "calculation_basis": "attributable_earnings",
    "basis_definition": "50% dividend payout ratio target basis for 2026-2028, applied to EPS excluding material notable items and related impacts; quarterly interims of 0.10 USD with a larger fourth interim.",
    "reported_payout_ratio": 0.5,
    "source_and_date": Q3,
    "funding_constraint": f"Base FY2026: 50% x {SCEN['Base']['profit'][0]}m = {SCEN['Base']['profit'][0]*PAYOUT:.0f}m versus capacity {SCEN['Base']['profit'][0]-SCEN['Base']['growth_capital']}m after RWA growth capital."})
rr = r["return_requirements"]
rr.update({"quote_currency": "HKD", "quote_per_valuation_unit": USDHKD,
           "benchmark": "US 10-year Treasury constant maturity (DGS10)", "benchmark_source": UST,
           "benchmark_date": "2026-11-05", "benchmark_currency": "USD", "benchmark_tenor": "10 years", "benchmark_remaining_years": 10, "target_tenor_years": 10,
           "valuation_currency": "USD", "valuation_unit_scale": 1, "shares_per_quoted_security": 1,
           "tax_and_fx_basis": f"Dividends declared in USD; HK register paid in HKD under the peg. Quote HKD {PRICE_HKD} converted at USD/HKD {USDHKD} = USD {PRICE}. HK-resident individual: no UK withholding on ordinary dividends, no HK tax on dividends.",
           "risk_free_rate": RF, "risk_premium_low": 0.03, "risk_premium_high": 0.05,
           "required_total_return_low": R_LOW, "required_total_return_high": R_HIGH,
           "price_independent_risk_factors": ["3 points: diversified, well-capitalised global bank with a published payout policy. 5 points: rate-cycle NII sensitivity, China/Hong Kong credit and geopolitics, and a 2020 regulator-ordered dividend cancellation precedent. Neither depends on price or score."],
           "income_growth_credit": 0,
           "limitations": "Ordinary cash-income thresholds give no credit for buybacks or EPS growth; they are not a complete intrinsic value for a 17%+ RoTE bank. See the P/TBV cross-check in chapter 9."})
inc = r["income_assessment"]
inc.update({"forward_net_yield": fwd_yield, "forward_net_dps": N, "income_period": "FY2026 full year (Base)",
            "reason": f"No investor income target supplied. Base FY2026 net DPS {N:.4f} USD / price {PRICE} = {fwd_yield:.2%}."})

# ---------------- buy zone ----------------
bz = r["buy_zone"]
src = [Q3]
bz.update({"normalized_net_dps": N, "normalized_net_dps_basis": "mid_cycle",
           "normalized_net_dps_source_period": "FY2026 Base: 50% x 29,400m / 17,111m shares",
           "normalization_adjustments": [f"N={N:.4f} USD = Base FY2026 profit excl. notable items 29,400m x 50% / 17,111m shares; no buyback or special dividend credit."],
           "bear_net_dps": B, "bear_net_dps_source": f"Bear FY2027 profit 24,000m x 50% / 17,111m = {B:.4f} USD (rate cuts and ECL normalisation).",
           "bear_net_dps_is_fallback": False, "dps_currency": "USD", "normalization_fx_rate": 1,
           "normalization_fx_basis": "USD DPS compared with USD-converted quote; HKD peg.",
           "normalization_cash_deductions": 0, "required_net_yield_low": R_LOW, "required_net_yield_high": R_HIGH,
           "too_expensive_zone": f">{starter:.2f}", "fair_value_zone": f"({add:.2f}, {starter:.2f}]",
           "accumulation_zone": f"({strong:.2f}, {add:.2f}]", "strong_buy_zone": f"<={strong:.2f}",
           "boundaries": {"too_expensive_above": starter, "fair_lower": add, "fair_upper": starter,
                          "accumulation_lower": strong, "accumulation_upper": add, "strong_buy_at_or_below": strong}})
for key, text in (("operating_cash", "Bank proxy: 9M26 EPS excl. notable items 1.30 USD annualised to about 1.72; profit 29,400m."),
                  ("funding_capacity", "Capacity = profit - RWA growth capital 3,900m = 25,500m, covering the 14,700m dividend."),
                  ("payout_policy", "50% target-basis payout reaffirmed for 2026-2028 in the 3Q26 release."),
                  ("entitled_shares", "17,111m basic shares at 30 Sep 2026; cash dividend, no scrip; zero withholding for HK-resident individuals.")):
    bz["normalization_evidence"][key].update({"input_detail": text, "source_refs": src,
                                              "consequence": "Supports the Base normalized DPS for the ordinary income comparison."})
nm = bz["normalization_model"]
nm.update({"method": "steady_state", "cycle_applicability": "non_cyclical",
           "cycle_basis": "Rate-cycle bank; FY2026 Base uses management RoTE target and current-rate NII, not peak 2024 rates.",
           "series_sources": [AR], "joint_assumption_rationale": "Profit, RWA growth and payout taken from one Base scenario.",
           "perimeter_adjustments": "Excludes material notable items; Hang Seng Bank fully owned from 26 Jan 2026."})
nm["drivers"][0].update({"name": "Profit to ordinary shareholders", "unit": "USD m", "source": AR,
                         "selected_value": SCEN["Base"]["profit"][0], "observations": PROFIT})
mid = nm["cycle_states"]["mid"]
p0, g0 = SCEN["Base"]["profit"][0], SCEN["Base"]["growth_capital"]
mid.update({"operating_assumptions": "Base FY2026 bank capital proxy", "owner_cash": p0, "growth_uses": g0, "mandatory_uses": 0,
            "recurring_fad": p0 - g0, "earnings": p0, "payout_base": p0, "payout_ratio": PAYOUT,
            "dividend_entitlement": p0 * PAYOUT, "shares": SHARES, "gross_dps": N, "evidence": Q3})
for state in ("low", "high"):
    nm["cycle_states"][state].update({"operating_assumptions": "No separate cycle extreme modelled; Bear/Bull scenarios carry the range.", "evidence": Q3})

# ---------------- capital-return valuation (buy-zone.md 7A) ----------------
TNAV, G, MOS = 9.41, 0.03, 0.10
ROTES = {"Bear": 0.14, "Base": 0.17, "Bull": 0.19}
val = lambda rote, rr_: TNAV * (rote - G) / (rr_ - G)
crv_rows = [{"scenario": s_, "sustainable_return_on_tangible_equity": rote,
             "value_at_required_high": val(rote, R_HIGH), "value_at_required_low": val(rote, R_LOW),
             "evidence": {"Bear": "Bear forecast: faster rate cuts and ECL near 60bps cut RoTE to about 14%, below the 2021-2025 average.",
                          "Base": "Management target RoTE of 17% or better for 2026-2028; 9M26 annualised 18.8% excl. notable items.",
                          "Bull": "Rates stay higher and Hang Seng synergies exceed plan; 9M26 run-rate near 19%."}[s_]}
            for s_, rote in ROTES.items()]
v_low = min(row["value_at_required_high"] for row in crv_rows)
v_high = max(row["value_at_required_low"] for row in crv_rows)
v_base = crv_rows[1]["value_at_required_high"]
c_start = v_base * (1 - MOS); c_add = min(c_start, v_low); c_strong = v_low * (1 - MOS)
fc_rows = r["three_year_fundamental_forecast"] + r["forecast_extension"]
cap_rows = []
for s_, rote in ROTES.items():
    yrs = [row for row in fc_rows if row["scenario"] == s_]
    ratio = sum(row["recurring_fad"] for row in yrs) / sum(row["net_income_or_affo"] for row in yrs)
    cap_rows.append({"scenario": s_, "implied_distribution_ratio": (rote - G) / rote, "forecast_distributable_ratio": ratio,
                     "dividend_payout_ratio": PAYOUT, "buyback_capacity_ratio": ratio - PAYOUT})
# Base, year by year. CET1 was 13.9% against a 14.25% midpoint: rebuilding 0.35% of RWAs comes first in 2026;
# Basel 3.1 is expected to add about 45bps on 1 Jan 2027, releasing capital that year (3Q26 release).
GAP_2026 = (CET1_TARGET - 0.139) * RWA[-1]
RELEASE_2027 = -0.0045 * RWA[-1]
annual_path = []
for y in range(1, 6):
    p_ = SCEN["Base"]["profit"][y - 1]
    rebuild = GAP_2026 if y == 1 else RELEASE_2027 if y == 2 else 0
    annual_path.append({"fiscal_year": str(2025 + y), "earnings": p_, "growth_capital": SCEN["Base"]["growth_capital"],
                        "target_gap_rebuild": rebuild, "dividends": p_ * PAYOUT,
                        "buyback_capacity": p_ - SCEN["Base"]["growth_capital"] - rebuild - p_ * PAYOUT,
                        "note": {1: "2026 年先把资本充足率从 13.9% 补到 14.25%（按 2025 年末风险加权资产估算）。",
                                 2: "2027 年巴塞尔 3.1 生效，预计提高资本充足率约 0.45 个百分点。"}.get(y, "")})
r["valuation_mode"] = "capital_return_based"
r["capital_return_valuation"] = {
    "status": "assessed", "method": "tangible_book_residual_income", "book_value_per_share": TNAV,
    "book_value_date": "2026-09-30", "book_value_currency": "USD", "book_value_source": Q3,
    "long_run_growth": G, "long_run_nominal_growth_bound": 0.04,
    "long_run_growth_basis": "Long-run nominal growth of HSBC's main markets (HK, UK) about 3%-4%; 3% used, below R_low by 4.84 points.",
    "required_return_low": R_LOW, "required_return_high": R_HIGH, "margin_of_safety": MOS,
    "scenarios": crv_rows, "value_low": v_low, "value_high": v_high, "base_case_value": v_base,
    "entry_upper": v_low * (1 - MOS), "review_above": v_high,
    "shareholder_return_policy": "50% target-basis dividend payout for 2026-2028 plus buybacks when CET1 is within or above 14%-14.5%.",
    "capital_constraint": "CET1 13.9% at 30 Sep 2026, below the operating range; Basel 3.1 expected +40-50bps on 1 Jan 2027.",
    "distribution_capacity": {"scenarios": cap_rows, "annual_path": annual_path,
        "capital_ratio_bridge": {"current_ratio": 0.139, "target_ratio": CET1_TARGET, "risk_weighted_assets": RWA[-1],
                                 "regulatory_change_ratio": 0.0045, "source_refs": [Q3, AR]},
        "growth_consistency": (f"Base reserves {SCEN['Base']['growth_capital']}m a year of CET1 for RWA growth at the 14.25% target, "
                               f"about {SCEN['Base']['growth_capital'] / CET1_TARGET / RWA[-1]:.1%} of 2025 RWAs, close to the 3% long-run g. "
                               "Bear reserves less because loan growth slows."),
        "near_term_constraint": ("CET1 is 13.9%, below the 14%-14.5% range, so buybacks are paused until Basel 3.1 (+40-50bps, Jan 2027) "
                                 "restores headroom. The per-share forecast holds shares flat and credits no buybacks; the valuation "
                                 "counts the capacity above the 50% dividend, which is not yet being paid out.")},
    "price_independent": True}
print("capital-return", round(v_low, 2), round(v_base, 2), round(v_high, 2), "stages", round(c_start, 2), round(c_add, 2), round(c_strong, 2))

# ---------------- entry plan and decision ----------------
def pct(x): return (x / PRICE - 1) * 100
ep = r["entry_plan"]
ep.update({"current_action": "wait_for_price",
           "summary": f"At USD {PRICE} (HKD {PRICE_HKD}) the price is just above the capital-return starter price USD {c_start:.2f}; the income view (forward yield {fwd_yield:.1%}) is far stricter.",
           "opportunity_thesis": "HSBC is a high-quality capital-return story (17%+ RoTE, 50% payout plus buybacks), but buybacks and EPS growth are not credited by the ordinary income method.",
           "market_expectation_gap": f"Price implies P/TBV {PRICE/9.41:.2f}x on TNAV 9.41 USD; at a 17% sustained RoTE that implies about a 9% cost of equity, i.e. the market already prices sustained high returns."})
ep["stages"] = [
    {"stage": "starter", "valuation_price": c_start, "effective_price": c_start, "gap_to_current_pct": pct(c_start),
     "status": "waiting_price", "condition": f"Base value at R_high {v_base:.2f} x (1 - 10%) = USD {c_start:.2f} (HKD {HK(c_start)})."},
    {"stage": "add", "valuation_price": c_add, "effective_price": c_add, "gap_to_current_pct": pct(c_add),
     "status": "waiting_price", "condition": f"Bear value at R_high = USD {c_add:.2f} (HKD {HK(c_add)})."},
    {"stage": "strong_buy", "valuation_price": c_strong, "effective_price": c_strong, "gap_to_current_pct": pct(c_strong),
     "status": "waiting_evidence", "condition": f"Bear value x (1 - 10%) = USD {c_strong:.2f} (HKD {HK(c_strong)}), plus High confidence and Strong safety."}]
cash3 = {s: sum(d[:3]) for s, d in (("Bear", bear_dps), ("Base", base_dps), ("Bull", bull_dps))}
exits = {"Bear": bear_dps[2] / R_LOW, "Base": base_dps[2] / fwd_yield, "Bull": bull_dps[2] / 0.045}
basis = {"Bear": f"Exit at Bear FY2028 DPS / R_low {R_LOW:.2%}: re-rating to the required income yield.",
         "Base": f"Exit at Base FY2028 DPS / current forward yield {fwd_yield:.2%}: no re-rating.",
         "Bull": "Exit at Bull FY2028 DPS / 4.5% yield."}
ep["return_scenarios"] = [{"scenario": s, "horizon_years": 3, "net_cash_received": cash3[s],
                           "exit_price": exits[s], "costs": 0,
                           "cumulative_return": (cash3[s] + exits[s]) / PRICE - 1,
                           "basis": basis[s] + " No reinvestment, buybacks not credited, zero costs assumed.",
                           "source_refs": [Q3, PX]} for s in ("Bear", "Base", "Bull")]
ep["risk_review"].update({"rationale": f"Bear path loses {-(ep['return_scenarios'][0]['cumulative_return']):.0%} including three years of dividends if the market re-rates HSBC to a required income yield; Base relies on no de-rating.", "source_refs": [Q3, PX]})
ep["blockers"] = [{"scope": "price", "reason": f"Price is {pct(c_start):+.1f}% from the capital-return starter price.",
                   "resolution": f"Price at or below USD {c_start:.2f} (HKD {HK(c_start)}), or a higher evidenced sustainable RoTE.", "source_refs": [Q3, PX]},
                  {"scope": "position_sizing", "reason": "Existing holding size and cost basis not supplied.",
                   "resolution": "Provide holdings before any sizing or trimming discussion.", "source_refs": []}]
ep["catalysts"] = [{"event": "FY2026 results and fourth interim dividend", "check_date_or_period": "February 2027",
                    "confirmation": "FY2026 DPS near 0.86 USD and CET1 back within 14%-14.5% after Basel 3.1 benefit.",
                    "source_to_revisit": "HSBC annual results release", "if_missed": "Rebuild N and stage prices."}]
ep["invalidation_conditions"] = ["CET1 below 13.5% with buybacks and dividend constrained.",
                                 "RoTE excluding notable items below 14% for two consecutive quarters."]
r["action_assessment"].update({"status": "eligible", "strong_buy_eligible": False,
                               "reasons": ["Evidence supports the income comparison; the price does not meet the required income yield."],
                               "capital_risk_and_total_return_check": "See entry_plan.return_scenarios: Bear re-rating loses principal; dividends alone do not offset it."})
r["decision"].update({"current_action": "等待到价", "can_buy_now": False,
    "reason": f"按银行有形净资产估值，Base 价值打九折的初始建仓价约 {HK(c_start)} 港元，现价 {PRICE_HKD} 港元略高约 {abs(pct(c_start)):.1f}%；收息口径（远期股息率 {fwd_yield:.1%}，与美国国债持平）更为严格。新资金等待小幅回调，已持有部分估值仍在合理区间。",
    "buy_conditions": [{"kind": "price", "observable": "汇丰控股港股收盘价", "operator": "<=", "threshold": round(HK(c_start), 1), "unit": "HKD", "source_to_watch": "港交所实时报价"}],
    "invalidation_conditions": [{"kind": "event", "observable": "董事会下调 50% 派息率目标或暂停季度股息", "operator": "published", "threshold": "已公告", "unit": "公告事件", "source_to_watch": "汇丰业绩公告"},
                                {"kind": "metric", "observable": "CET1 比率", "operator": "<", "threshold": 13.5, "unit": "%", "source_to_watch": "汇丰季度业绩公告"},
                                {"kind": "metric", "observable": "剔除特殊项目的年化有形股本回报率（连续两季）", "operator": "<", "threshold": 14, "unit": "%", "source_to_watch": "汇丰季度业绩公告"}],
    "trap_conclusion": "未触发红利陷阱：股息由利润和资本生成覆盖，派息率政策清晰；主要风险是利率下行和信用成本。",
    "entry_conclusion": f"资本回报口径参考价：初始建仓 {HK(c_start)} 港元、逐步增持 {HK(c_add)} 港元、强力买入 {HK(c_strong)} 港元；收息口径初始建仓约 {HK(starter)} 港元，仅作对比。",
    "price_status": "reference_prices",
    "reference_prices": {"starter": c_start, "add": c_add, "strong_buy": c_strong, "income_capped_upper": c_start}})
# ---------------- business outlook cumulative FAD ----------------
for row in r["business_outlook"]["cumulative_fad"]:
    s_ = row["scenario"]; fad = [SCEN[s_]["profit"][i] - SCEN[s_]["growth_capital"] for i in range(5)]
    row.update({"three_year": sum(fad[:3]), "five_year": sum(fad),
                "limitations": "Sum of modeled bank capital-generation proxy after RWA growth capital; before dividends and buybacks."})
bo = r["business_outlook"]
bo.update({"data_cutoff": AS_OF,
           "competitive_position": "Largest Hong Kong deposit franchise (with Hang Seng Bank fully owned since Jan 2026), UK ring-fenced bank, global trade and wealth network.",
           "management_execution": "Management targets RoTE of 17% or better for 2026-2028, ~1% target-basis cost growth in 2026 and a 50% payout; 9M26 RoTE excl. notable items 18.8%."})

# ---------------- scorecard ----------------
def chk(n, status, ev): return {"check": n, "status": status, "evidence": ev, "source_refs": S}
spec = {
 "net_yield": (15, fwd_yield, 3, 6, 9, ["unknown", "not_met", "not_met"],
   [f"FY2026 DPS depends on the Q4 interim; 9M paid 0.30 USD against Base N {N:.3f}.", f"B/price {B/PRICE:.2%} is below r_high {R_HIGH:.2%}.", f"N/price {fwd_yield:.2%} is below R_low {R_LOW:.2%}."],
   f"N/price {fwd_yield:.2%} sits in the 3.5%-5% band."),
 "dividend_stability": (15, None, 1, 12, 15, ["met", "met", "not_met"],
   ["Quarterly/interim ordinary dividends paid every year 2021-2025.", "DPS paid rose from 0.22 to 0.66 USD (2021-2025), well above inflation.", "In 2020 the PRA request led HSBC to cancel the 4Q19 dividend; stability has not survived a regulatory stress."],
   "Ordinary DPS rose each year 2021-2025 with no cut inside the window."),
 "cash_coverage": (20, None, 1, 17, 20, ["met", "met", "not_met"],
   ["Bear, Base and Bull years 1-3 capital generation covers the 50% dividend.", f"Worst 2021-2025 coverage {min(covs):.2f}x (2025).", "CET1 13.9% is below the 14% operating floor; dividends plus buybacks exceeded the proxy in 2024-2025."],
   "Three-year capital-generation proxy / dividends is 1.59x."),
 "balance_sheet": (15, None, 2, 8, 11, ["met", "met", "met"],
   ["12-month average LCR 132% at 30 Sep 2026, above the 100% minimum.", "Bear profit keeps CET1 above regulatory minima with buybacks paused.", "No equity issuance needed; Basel 3.1 adds about 40-50bps CET1 on 1 Jan 2027."],
   "Well-capitalised but CET1 temporarily below the 14%-14.5% target after the Hang Seng privatisation."),
 "capital_allocation": (15, None, 1, 12, 15, ["met", "met", "unknown"],
   ["50% target-basis payout applied in 2023-2025 and reaffirmed for 2026-2028.", "Hang Seng privatisation targets 0.5bn USD annual synergies; disposals of Canada/Argentina/France simplified the group.", "Hang Seng privatisation premium and BoCom impairments: per-share outcome not yet evidenced."],
   "Clear published payout policy with buybacks tied to the CET1 range."),
 "buyback_quality": (10, None, 1, 8, 10, ["met", "unknown", "met"],
   ["Shares in issue fell from 20,632m (2021) to 17,175m (2025), net reduction after employee issuance.", "Buybacks executed at 1.0x-1.9x TNAV; no contemporaneous intrinsic-value test extracted.", "Buybacks paused when CET1 fell below the range, preserving capital."],
   "Real 17% share-count reduction since 2021."),
 "visibility": (10, None, 2, 5, 7, ["met", "met", "not_met"],
   ["Years 1-3 tie to 9M26 EPS, payout policy and RWA growth.", "Years 4-5 extend Base RoTE at the target floor with bounded Bear/Bull.", "Rate path and HK/China credit remain outside management control; not treated as corroborated."],
   "Moderate visibility: rate- and credit-sensitive earnings."),
}
mods, ranges = [], {}
for name, (w, metric, band, lo, hi, statuses, evs, why) in spec.items():
    k = statuses.count("met")
    raw = lo + ((hi - lo) * k) // 3
    mods.append({"module": name, "weight": w, "assessment": "assessed", "evidence_basis": "reconstructed",
                 "metric_value": metric if name != "cash_coverage" else sum(fads[2:]) / sum(divs[2:]),
                 "period": "FY2021-2025 and FY2026 Base at the 2026-11-09 quote", "band": band, "rationale": why,
                 "checks": [chk(i + 1, st, ev) for i, (st, ev) in enumerate(zip(statuses, evs))],
                 "raw_score": raw, "cap": w, "cap_reason": "No lower cap applies.", "final_score": raw,
                 "source_refs": S, "missing_evidence": [ev for st, ev in zip(statuses, evs) if st == "unknown"]})
    ranges[name] = {"low": raw, "high": raw}
pts = {m["module"]: m["final_score"] for m in mods}
quality = sum(v for k_, v in pts.items() if k_ != "net_yield"); income = pts["net_yield"]; total = quality + income
print("scores", pts, quality, income, total)
sc = r["scorecard"]
for old in sc["modules"]:
    pass
sc["modules"] = [dict(old, **new) for old, new in zip(sorted(sc["modules"], key=lambda m: list(spec).index(m["module"])), mods)]
sc.update({"quality_score_85": quality, "income_score_15": income, "assessed_points": total, "assessed_weight": 100})
sm = sc["summary"]
sm.update({"module_ranges": ranges, "score_range": {"low": total, "high": total},
           "quality_range": {"low": quality, "high": quality}, "income_range": {"low": income, "high": income}})
r["score_100"] = total
qa = r["quality_assessment"]
qa.update({"components": {k_: v for k_, v in pts.items() if k_ != "net_yield"}, "score_85": quality,
           "component_ranges": {k_: v for k_, v in ranges.items() if k_ != "net_yield"},
           "score_range": {"low": quality, "high": quality},
           "evidence_and_limitations": "Rubric-2 points reconstructed from HSBC AR2025 and 3Q26 release; unknown checks earn no bonus."})
km = r["key_metrics_at_a_glance"]
km.update({"ttm_net_yield": 0.75 / PRICE, "normalized_net_yield": fwd_yield, "quality_score_85": quality,
           "current_action": "wait_for_price", "score_range": {"low": total, "high": total},
           "quality_score_range": {"low": quality, "high": quality}, "score_100": total})
r["dividend_snapshot"].update({"ttm_dps": 0.75, "ttm_net_yield": 0.75 / PRICE, "normalized_net_dps": N})
for k_, v in r["rating_audit"].items():
    v["source_refs"] = S
r["score_limitations"] = f"Rubric-2 point score from public filings: quality {quality}/85 plus income {income}/15 = {total}/100. Unknown refinements earn no bonus."
r["income_drivers"] = [{"driver": "credit_losses_and_spreads", "exposure_direction": "higher_supports_income", "horizon": "One to three years",
                        "transmission": "Higher HKD/GBP/USD rates raise banking NII, profit and the 50%-of-EPS dividend.",
                        "evidence": Q3}]

# ---------------- evidence recovery ----------------
SUB = "https://www.about.hsbc.com.hk/hongkong-and-shanghai-banking-corporation-limited/results"
def attempts(results, sub=("inaccessible", "该网站不在本环境网络白名单内，未能取得香港上海汇丰银行年报")):
    cats = ["issuer_filings", "group_disclosures", "announcements", "exchange_regulator",
            "official_series", "historical_comparables", "broker_records"]
    rows = []
    for c, (src_, per, out, res) in zip(cats, results):
        scope = "investor" if c == "broker_records" else ("parent" if c == "group_disclosures" else "issuer")
        rows.append({"category": c, "scope": scope, "source": src_, "source_period": per,
                     "attempted_on": AS_OF, "outcome": out, "result": res})
        if c == "group_disclosures":
            rows.append({"category": c, "scope": "subsidiary", "source": SUB, "source_period": "2025 财年",
                         "attempted_on": AS_OF, "outcome": sub[0], "result": sub[1]})
    return rows
def find_paths(prefixes):
    out = []
    for i, m in enumerate(r["scorecard"]["modules"]):
        for j, c in enumerate(m["checks"]):
            if c["status"] == "unknown" and m["module"] in prefixes:
                out.append(f"/scorecard/modules/{i}/checks/{j}/status")
        if m["missing_evidence"] and m["module"] in prefixes:
            out.append(f"/scorecard/modules/{i}/missing_evidence")
    return out
co = lambda obs, src_: {"kind": "event", "observable": obs, "operator": "published", "threshold": "已公告", "unit": "公告事件", "source_to_watch": src_}
r["evidence_recovery"].update({"scope": "live_research", "scope_reason": "联网查阅汇丰 2025 年报、2026 年三季度业绩公告及行情数据", "is_group_structure": True})
inv_paths = ["/growth_assessment/growth_method", "/growth_assessment/status", "/holding_review/action",
             "/holding_review/missing_inputs", "/income_assessment/target/target_basis",
             "/income_assessment/target/target_policy", "/real_income/status"]
r["evidence_recovery"]["records"] = [
 {"field_paths": inv_paths,
  "reason": "用户未提供收息目标、持仓与成本；本次未做购买力（通胀）测算",
  "impact": "不判断收入匹配度、不给仓位建议；主估值为资本回报口径（有形净资产 × 回报率），收息口径作对照",
  "resolution": "not_assessable",
  "attempts": attempts([
    (AR, "2025 财年", "found", "公司披露不含投资者个人收息目标与持仓"),
    (AR, "2025 财年", "found", "母公司披露派息政策与资本目标，可用于后续成长估值"),
    (Q3, "2026 年前三季度", "found", "披露 2026–2028 年回报率与派息率目标"),
    ("https://www1.hkexnews.hk/search/titlesearch.xhtml", "截至 2026-11-09", "not_found", "无投资者个人信息"),
    (UST, "2026-11-05", "found", "取得美国 10 年期国债收益率，未取得香港通胀序列"),
    (AR, "2021–2025", "found", "五年历史数据可支持后续总回报模型"),
    ("用户券商记录", "未提供", "not_provided", "用户未提供持仓、成本与收息目标")],
    sub=("inaccessible", "该网站不在本环境网络白名单内，子公司披露也不含投资者个人信息")),
  "estimate": None, "estimate_failure_reason": "缺少用户输入；成长估值需逐年股息折现与终值资金证明，本次未完成",
  "closure_condition": co("用户提供持仓、成本及收息目标", "用户补充信息")},
 {"field_paths": find_paths({"net_yield"}),
  "reason": "2026 年第四次中期股息要到 2027 年 2 月年度业绩时才公布",
  "impact": "收息得分不计这一项加分；远期股息按 50% 派息率估算",
  "resolution": "not_assessable",
  "attempts": attempts([
    (Q3, "2026 年前三季度", "found", "已宣派前三次中期股息合计 0.30 美元，未公布第四次"),
    (AR, "2025 财年", "found", "2025 年第四次中期股息 0.45 美元，可作参考但不等于 2026 年"),
    ("https://www.hsbc.com/investors/results-and-announcements/all-reporting", "截至 2026-11-09", "not_found", "尚无 2026 年第四次中期股息公告"),
    ("https://www1.hkexnews.hk/search/titlesearch.xhtml", "截至 2026-11-09", "not_found", "无相关公告"),
    (UST, "2026-11-05", "not_applicable", "与股息金额无关"),
    (AR, "2023–2025 财年", "found", "历年第四次中期股息使全年派息率回到 50%"),
    ("用户券商记录", "未提供", "not_provided", "用户未提供持仓及收息记录")]),
  "estimate": None, "estimate_failure_reason": "第四次中期股息取决于全年剔除特殊项目后的每股盈利，公告前无法确定",
  "closure_condition": co("汇丰公布 2026 年第四次中期股息", "汇丰 2026 年度业绩公告")},
 {"field_paths": find_paths({"capital_allocation", "buyback_quality"}),
  "reason": "恒生银行私有化溢价与回购价格是否低于内在价值，缺少可核对的同期估值",
  "impact": "资本配置与回购质量不计这两项加分",
  "resolution": "not_assessable",
  "attempts": attempts([
    (AR, "2025 财年", "found", "披露私有化完成及协同目标 5 亿美元，未披露每股价值影响"),
    (Q3, "2026 年前三季度", "found", "披露协同进展，未量化每股回报"),
    ("https://www.hsbc.com/investors/results-and-announcements/all-reporting", "2025–2026", "not_found", "本环境未取得计划文件全文"),
    ("https://www1.hkexnews.hk/search/titlesearch.xhtml", "截至 2026-11-09", "inaccessible", "未能取得私有化计划文件"),
    ("https://fred.stlouisfed.org/", "不适用", "not_applicable", "无相关官方序列"),
    (AR, "2021–2025", "found", "回购价约为每股有形净资产 1.0–1.9 倍，无独立内在价值对比"),
    ("用户券商记录", "未提供", "not_provided", "与公司层面判断无关")]),
  "estimate": None, "estimate_failure_reason": "缺少私有化对每股盈利和资本的完整影响披露，无法有据收窄",
  "closure_condition": co("汇丰披露恒生银行私有化后协同效益与每股盈利影响", "汇丰年度业绩与投资者简报")},
]

grade = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 55 else "D" if total >= 40 else "E"
qlabel = "High" if quality >= 68 else "Medium" if quality >= 51 else "Low"
sm.update({"status": "complete", "grade_range": {"worst": grade, "best": grade},
           "quality_rating_range": {"worst": qlabel, "best": qlabel}})
qa["status"] = "assessed"
km.update({"score_status": "complete", "grade_range": {"worst": grade, "best": grade}, "grade": grade})
sc["unadjusted_grade"] = grade
r.update({"grade": grade, "dividend_quality": qlabel})
ra = r["rating_audit"]
ra["dividend_quality"].update({"label": qlabel, "rule": "Quality >= 68/85 is High; price excluded.",
    "supporting_evidence": "+".join(str(v) for k_, v in pts.items() if k_ != "net_yield") + f"={quality} quality points.",
    "upgrade_trigger": "Already High.", "downgrade_trigger": "Quality falls below 68, e.g. a dividend cut or CET1 shortfall."})
