"""Build the HSBC (0005.HK) schema-3.0 Full Analysis from a few sourced inputs.

All derived numbers are computed here so the record stays internally consistent.
Units: USD millions for group cash/profit; shares in millions; per-share in USD.
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "dividend-income-equity-analysis"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "hsbc-0005.analysis.json"
r = json.loads((SKILL / "examples/full-report.analysis.json").read_text(encoding="utf-8"))

# ---------------- sourced inputs ----------------
AR = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2025/annual/pdfs/hsbc-holdings-plc/260225-annual-report-and-accounts-2025.pdf"
Q3 = "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2026/3q/pdfs/hsbc-holdings-plc/261027-3q-2026-earnings-release.pdf"
PX = "https://query1.finance.yahoo.com/v8/finance/chart/0005.HK"
UST = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"
SOURCES = [AR, Q3, PX, UST]
AS_OF = "2026-11-09"
PRICE_HKD, USDHKD = 137.60, 7.8395
PRICE = round(PRICE_HKD / USDHKD, 2)          # 17.55 USD per share
RF = 0.0484
SHARES = 17111                                  # basic outstanding, 30 Sep 2026 (3Q26 release)
CET1_TARGET = 0.1425                            # midpoint of 14%-14.5% operating range
YEARS = ["2021", "2022", "2023", "2024", "2025"]
PROFIT = [12607, 14346, 22432, 22917, 21102]    # attributable to ordinary shareholders (AR25)
RWA = [838263, 839720, 854114, 838254, 888647]  # year-end RWAs (AR25)
DPS_PAID = [0.22, 0.27, 0.53, 0.82, 0.66]       # paid in period incl. 2024 special 0.21 (AR25)
SHARES_HIST = [20073, 19739, 19006, 17918, 17140]

# Forecast: attributable profit excl. material notable items (USD m), revenue, RWA growth capital.
SCEN = {
    "Bear": {"profit": [28500, 24000, 23000, 23500, 24000], "revenue": [73000, 70000, 70000, 71000, 72000], "growth_capital": 1000},
    "Base": {"profit": [29400, 30600, 32100, 33400, 34700], "revenue": [75500, 77500, 80500, 83000, 85500], "growth_capital": 3900},
    "Bull": {"profit": [30000, 32500, 34500, 36000, 37500], "revenue": [76000, 80000, 84000, 87500, 91000], "growth_capital": 5000},
}
PAYOUT = 0.50
R_LOW, R_HIGH = RF + 0.03, RF + 0.05


def rnd(x, n=2):
    return round(x + 0.0, n)


# ---------------- history bridge ----------------
bridge = []
for i, fy in enumerate(YEARS):
    growth_cap = 0 if i == 0 else max(0, (RWA[i] - RWA[i - 1]) * CET1_TARGET)
    fad = PROFIT[i] - growth_cap
    div = DPS_PAID[i] * SHARES_HIST[i]
    row = copy.deepcopy(r["cash_flow_bridge"][i])
    row.update({"fiscal_year": fy, "fiscal_year_end": f"{fy}-12-31",
                "recurring_owner_fcf_or_proxy": PROFIT[i], "recurring_fad": rnd(fad, 0),
                "actual_all_in_fcf": rnd(fad, 0), "actual_distribution_capacity": rnd(fad, 0),
                "cash_dividends": rnd(div, 0),
                "fcf_dividend_coverage": rnd(fad, 0) / rnd(div, 0),
                "actual_cash_coverage": rnd(fad, 0) / rnd(div, 0),
                "evidence_status": "estimated_reconciled",
                "funding_source": "Regulated Capital / Remittances"})
    bridge.append(row)
r["cash_flow_bridge"] = bridge

# ---------------- forecasts ----------------
def forecast_row(template, fy, year, scen):
    s = SCEN[scen]
    p, rev, g = s["profit"][year - 1], s["revenue"][year - 1], s["growth_capital"]
    row = copy.deepcopy(template)
    row.update({"fiscal_year": fy, "forecast_year": year, "scenario": scen,
                "primary_driver_name": "Banking NII and RoTE",
                "primary_driver_assumption": f"{scen}: attributable profit excl. notable items {p}m; RWA growth capital {g}m at 14.25% CET1.",
                "revenue_or_sector_income": rev, "net_income_or_affo": p, "operating_cash_flow": None,
                "normalized_ocf": None, "maintenance_capex": None, "other_owner_claims": None,
                "remaining_growth_investment": g, "fcf_or_distributable_cash": p,
                "nonrecurring_operating_cash_inflow": None, "actual_all_in_fcf": p - g, "recurring_fad": p - g,
                "estimate_status": "estimated", "forecast_confidence": "Medium",
                "assumption_basis": "analyst_estimate",
                "evidence_and_limitations": "Bank capital proxy: profit to ordinary shareholders less CET1 capital consumed by RWA growth; anchored to 9M26 EPS excl. notable items 1.30 USD and management RoTE target of 17% or better for 2026-2028."})
    return row


tmpl = r["three_year_fundamental_forecast"][1]
r["three_year_fundamental_forecast"] = [forecast_row(tmpl, str(2025 + y), y, s)
                                        for y in (1, 2, 3) for s in ("Bear", "Base", "Bull")]
r["forecast_extension"] = [forecast_row(r["forecast_extension"][1], str(2025 + y), y, s)
                           for y in (4, 5) for s in ("Bear", "Base", "Bull")]

btmpl, rtmpl = r["dividend_forecast_bridge"][1], r["dividend_and_yield_runway"][1]
dfb, run = [], []
for y in (1, 2, 3, 4, 5):
    for s in ("Bear", "Base", "Bull"):
        p, g = SCEN[s]["profit"][y - 1], SCEN[s]["growth_capital"]
        b = copy.deepcopy(btmpl)
        b.update({"fiscal_year": str(2025 + y), "forecast_year": y, "scenario": s,
                  "fcf_or_capital_generation": p, "required_reinvestment": g,
                  "mandatory_debt_or_regulatory_uses": 0, "recurring_fad": p - g, "exceptional_cash_uses": 0,
                  "excess_cash_used": 0, "cash_available_for_distribution": p - g, "diluted_share_count": SHARES,
                  "deduction_ledger": [{"item": "RWA growth capital", "category": "growth", "amount": g,
                                        "already_in_starting_metric": False, "incremental_deduction": g,
                                        "evidence": "RWA growth x 14.25% CET1 target, deducted once from profit to ordinary shareholders."}],
                  "evidence_and_limitations": "Bank proxy: distributable capacity = ordinary profit - CET1 capital for RWA growth; AT1 coupons already excluded from ordinary profit; buybacks are discretionary and excluded."})
        dfb.append(b)
        div = p * PAYOUT
        q = copy.deepcopy(rtmpl)
        q.update({"fiscal_year": str(2025 + y), "forecast_year": y, "scenario": s,
                  "cash_available_for_distribution": p - g, "payout_base_amount": p, "payout_ratio": PAYOUT,
                  "policy_implied_dividend": div, "dividend_cash_cost": div, "dividend_entitlement": div,
                  "dividend_entitled_shares": SHARES,
                  "share_count_reconciliation": "17,111m basic shares outstanding at 30 Sep 2026 held flat; buybacks would raise DPS and are not credited.",
                  "derived_dps": rnd(div / SHARES, 6), "funding_gap": 0, "all_cash_funding_gap": 0,
                  "dps_source": "evidence_backed"})
        run.append(q)
r["dividend_forecast_bridge"], r["dividend_and_yield_runway"] = dfb, run

N = SCEN["Base"]["profit"][0] * PAYOUT / SHARES
B = SCEN["Bear"]["profit"][1] * PAYOUT / SHARES
starter, add, strong = N / R_LOW, N / R_HIGH, B / R_HIGH
print("N", N, "B", B, "R", R_LOW, R_HIGH, "prices", starter, add, strong, "price", PRICE, "yield", N / PRICE)



# @@EXTRA@@
# ---------------- identity, model, coverage ----------------
r.update({"company": "HSBC Holdings plc", "ticker": "0005.HK", "exchange": "Hong Kong Stock Exchange",
          "as_of_date": AS_OF, "price_used": PRICE, "withholding_rate": 0, "withholding_basis": "company_announcement",
          "sources": SOURCES})
cfm = r["cash_flow_model"]
cfm.update({"sector_model": "bank", "overlays": ["holding_company"],
            "starting_metric": "Profit attributable to ordinary shareholders (excl. material notable items in forecasts)",
            "owner_perimeter": "Ordinary shareholders of HSBC Holdings plc",
            "financial_currency": "USD", "cash_unit_scale": 1000000, "share_unit_scale": 1000000,
            "evidence_status": "estimated_reconciled",
            "proxy_reconciliation": "Capital generation proxy = profit to ordinary shareholders (after AT1 coupons and minorities) - CET1 capital consumed by RWA growth at the 14.25% target. FY2025: 21,102 - (888,647-838,254) x 14.25% = 13,921.",
            "capital_and_remittance_evidence": "Group CET1 13.9% at 30 Sep 2026 versus 14%-14.5% operating range; Basel 3.1 expected +40-50bps on 1 Jan 2027 (3Q26 release). Holding company relies on subsidiary dividends (HSBC UK ring-fenced bank, The Hongkong and Shanghai Banking Corporation); no specific remittance restriction disclosed.",
            "sources": [AR, Q3]})
cfm["deduction_ledger"] = [{"item": "RWA growth capital", "category": "growth", "amount": 3900, "already_in_starting_metric": False,
                            "incremental_deduction": 3900, "evidence": "Base FY2026 RWA growth about 3% x 14.25% CET1 target."}]
cfm["missing_inputs"] = []

fads = [row["recurring_fad"] for row in bridge]; divs = [row["cash_dividends"] for row in bridge]
covs = [f / d for f, d in zip(fads, divs)]
worst = min(range(5), key=lambda i: covs[i])
cs = r["coverage_summary"]
cs.update({"comparison_basis": "FY2021-2025 full years, USD millions; dividends = DPS paid in period x period-end basic shares (approximation; includes 2024 special 0.21). Buybacks excluded from the dividend denominator.",
           "fiscal_years": YEARS, "years_available": 5,
           "three_year_recurring_coverage": sum(fads[2:]) / sum(divs[2:]),
           "five_year_worst_recurring_coverage": covs[worst], "worst_available_recurring_coverage": covs[worst],
           "worst_recurring_year": YEARS[worst], "worst_actual_coverage": covs[worst], "worst_actual_year": YEARS[worst],
           "shortfall_funding_and_limitations": "No dividend-only shortfall. Dividends plus buybacks exceeded the capital-generation proxy in 2024-2025, funded by disposal capital releases (Canada, Argentina) and CET1 drawn toward target."})

exec((HERE / "hsbc_rest.py").read_text(encoding="utf-8"))
exec((HERE / "hsbc_report.py").read_text(encoding="utf-8"))
# @@END@@
json.dump(r, open(OUT, "w"), ensure_ascii=False, indent=2)

sys.path.insert(0, str(SKILL))
from scripts.validate_analysis import validate_report  # noqa: E402
from scripts.render_report import render_report  # noqa: E402
errors = validate_report(json.loads(OUT.read_text(encoding="utf-8")))
assert not errors, errors
(HERE / "hsbc-0005.html").write_text(render_report(json.loads(OUT.read_text(encoding="utf-8"))), encoding="utf-8")
print("validated and rendered")
