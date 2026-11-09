"""Validate research JSON structure and cross-field arithmetic, not market facts."""

import argparse
import json
import math
from datetime import date
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

if __package__:
    from .schema3_checks import validate_schema3
    from .decision_rules import validate_decision_framework
    from .local_checks import investor_cash_dps, validate_cash_events, validate_local_analysis, validate_safety_review
else:
    from schema3_checks import validate_schema3
    from decision_rules import validate_decision_framework
    from local_checks import investor_cash_dps, validate_cash_events, validate_local_analysis, validate_safety_review


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("Bear", "Base", "Bull")
SUPPORTED_WITHHOLDING_BASES = ("broker_observed", "company_announcement", "legal_structure")


def ordinary_boundaries(n, b, r_low, r_high, credit=0):
    """Ordinary income ladder; a gated growth credit lowers r_low/r_high but never the Bear strong-buy rate."""
    if not (0 <= b <= n and n > 0 and 0 < r_low < r_high and 0 <= credit):
        raise ValueError("Ordinary valuation requires 0 <= B <= N, N > 0 and 0 < r_low < r_high")
    strong = b / (r_high + credit)
    return {
        "too_expensive_above": n / r_low,
        "fair_lower": n / r_high,
        "fair_upper": n / r_low,
        "accumulation_lower": strong,
        "accumulation_upper": n / r_high,
        "strong_buy_at_or_below": strong,
    }

CREDIT_TRENDS = ("Structural Growth", "Stable", "Mature")
CREDIT_CAP = 0.03


def _cagr(start, end, years):
    return (end / start) ** (1 / years) - 1


def income_growth_credit_errors(report, runway, mode):
    """Gate the ordinary income growth credit (buy-zone.md Section 4.2A)."""
    errors = []
    returns = report["return_requirements"]
    credit = returns.get("income_growth_credit") or 0
    basis = returns.get("income_growth_credit_basis")
    tol = dict(rel_tol=1e-6, abs_tol=1e-6)

    def require(ok, message):
        if not ok:
            errors.append(f"Income growth credit: {message}")

    if basis is None:
        require(credit == 0, "a positive credit needs income_growth_credit_basis")
        return errors
    first, last = runway.get((1, "Base")), runway.get((5, "Base"))
    dps = [row and row.get("derived_dps") for row in (first, last)]
    if all(isinstance(value, (int, float)) and value > 0 for value in dps):
        require(math.isclose(basis["base_dps_cagr_fy1_fy5"], _cagr(dps[0], dps[1], 4), **tol),
                "Base FY1->FY5 DPS CAGR does not match the runway")
    else:
        require(credit == 0, "needs positive Base FY1 and FY5 runway DPS")
    require(math.isclose(basis["historical_cagr"], _cagr(basis["historical_start_value"], basis["historical_end_value"],
                                                          basis["historical_years"]), **tol),
            "historical CAGR does not match its start/end values")
    cap = max(0.0, min(CREDIT_CAP, basis["base_dps_cagr_fy1_fy5"], basis["historical_cagr"], basis["long_run_growth_bound"]))
    require(math.isclose(basis["credit_cap"], cap, **tol), "credit_cap must be min(3%, Base CAGR, historical CAGR, long-run bound)")
    gates = (mode == "ordinary_yield_based" and report["fundamental_trend"] in CREDIT_TRENDS
             and report["dividend_safety"] in ("Strong", "Acceptable")
             and report["forecast_confidence"] in ("High", "Medium")
             and report.get("value_trap_veto") == "Not triggered" and returns["status"] == "assessed")
    require(basis["gates_passed"] == (gates and cap > 0), "gates_passed disagrees with mode, trend, safety, confidence, veto or cap")
    if credit:
        require(gates, "only for ordinary_yield_based with Stable/Mature/Structural Growth trend, Strong/Acceptable "
                       "safety, High/Medium confidence and no value-trap veto")
        require(credit <= cap + 1e-12, "exceeds min(3%, Base CAGR, historical per-share growth, long-run bound)")
        if returns["status"] == "assessed":
            require(returns["required_total_return_low"] - credit > 0, "R_low - c must stay positive")
    return errors


def scrip_coverage_errors(report):
    """Scrip years must divide by the full entitlement, never the reduced cash paid (business-fundamentals.md)."""
    errors = []
    had_scrip = (report.get("scrip_drip", {}).get("historical_participation_rate") or 0) > 0
    history = sorted(report.get("cash_flow_bridge", []), key=lambda row: row["fiscal_year_end"])
    for row in history:
        label, in_year, next_year = row["fiscal_year"], row.get("entitlement_settled_in_year"), row.get("entitlement_settled_next_year")
        if had_scrip and (in_year is None or next_year is None):
            errors.append(f"{label}: scrip history needs entitlement_settled_in_year and entitlement_settled_next_year "
                          "(declared interim/final totals) to reconcile cash paid plus scrip across years")
        if in_year is not None and next_year is not None and row.get("dividend_denominator_basis") == "full_entitlement":
            if row["cash_dividends"] is not None and not math.isclose(in_year + next_year, row["cash_dividends"], rel_tol=1e-6, abs_tol=0.5):
                errors.append(f"{label}: full entitlement {row['cash_dividends']:g} must equal the declared "
                              f"in-year {in_year:g} plus next-year {next_year:g} parts")
    for prev, row in zip(history, history[1:]):
        in_year, carried = row.get("entitlement_settled_in_year"), prev.get("entitlement_settled_next_year")
        paid, scrip = row.get("cash_paid_dividends"), row.get("scrip_settled_dividends")
        if None in (in_year, carried, paid):
            continue
        settled, expected = paid + (scrip or 0), carried + in_year
        if expected > 0 and abs(settled - expected) > 0.02 * expected and row["evidence_status"] == "reported_reconciled" \
                and not row.get("settlement_reconciliation"):
            errors.append(f"{row['fiscal_year']}: cash paid plus scrip {settled:g} differs from prior final plus interim "
                          f"{expected:g} by more than 2%; explain it in settlement_reconciliation or do not mark the row reported_reconciled")
    for row in history:
        label, settled = row["fiscal_year"], row.get("scrip_settled_dividends")
        if had_scrip and settled is None:
            errors.append(f"{label}: scrip history (historical_participation_rate > 0) needs scrip_settled_dividends "
                          "on every bridge row, 0 for a year without scrip")
            continue
        if not settled:
            continue
        paid, div = row.get("cash_paid_dividends"), row["cash_dividends"]
        if row.get("dividend_denominator_basis") != "full_entitlement":
            errors.append(f"{label}: a scrip year must use dividend_denominator_basis full_entitlement")
        if paid is None:
            errors.append(f"{label}: a scrip year must record cash_paid_dividends")
        elif div is not None and div <= paid:
            errors.append(f"{label}: coverage denominator {div:g} must be the full entitlement, "
                          f"above the {paid:g} cash actually paid in a scrip year")
    return errors


def associate_conversion_errors(report):
    """Equity-accounted profit versus cash received from associates/JVs (economic-profile.md)."""
    profile = report.get("economic_profile")
    record = report.get("cash_flow_model", {}).get("associate_cash_conversion")
    if not profile or profile["cash_attribution"] != "material_jv_associates":
        return []
    if record is None:
        return ["Associate cash conversion: material_jv_associates needs cash_flow_model.associate_cash_conversion"]
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(f"Associate cash conversion: {message}")

    history = record["history"]
    years = [row["fiscal_year"] for row in history]
    require(years == sorted(set(years)), "history years must be unique and ascending")
    bridge_years = {row["fiscal_year"] for row in report.get("cash_flow_bridge", [])}
    require(set(years) <= bridge_years, "history years must come from the cash_flow_bridge periods")
    received, profits, ratios = [], [], []
    for index, row in enumerate(history):
        if record["timing_basis"] == "same_year":
            profit = row["share_of_profit"]
        else:
            profit = history[index - 1]["share_of_profit"] if index else None
        expected = row["cash_dividends_received"] / profit if profit is not None and profit > 0 else None
        if expected is None:
            require(row["conversion"] is None, f"{row['fiscal_year']}: conversion must be null without positive matching profit")
            continue
        require(row["conversion"] is not None and math.isclose(row["conversion"], expected, rel_tol=1e-6, abs_tol=1e-6),
                f"{row['fiscal_year']}: conversion should be {expected:.4f}")
        received.append(row["cash_dividends_received"])
        profits.append(profit)
        ratios.append(expected)
    require(len(ratios) >= 3, "needs at least three years with a computable conversion")
    aggregate = sum(received) / sum(profits) if ratios else None
    actual = record["aggregate_conversion"]
    require(actual is not None and aggregate is not None
            and math.isclose(actual, aggregate, rel_tol=1e-6, abs_tol=1e-6),
            f"aggregate_conversion should be {aggregate}")
    forecast = record["forecast_conversion"]
    evidence = record["above_history_evidence"]
    if evidence is not None:
        require(set(evidence["source_refs"]) <= set(report.get("sources", [])),
                "above_history_evidence source_refs must be entries of the report's sources")
    require(forecast["Bear"] <= forecast["Base"] <= forecast["Bull"], "forecast conversion must be ordered Bear <= Base <= Bull")
    if ratios and record["above_history_evidence"] is None:
        require(forecast["Base"] <= aggregate + 1e-9,
                f"Base {forecast['Base']:.1%} exceeds the {aggregate:.1%} multi-year aggregate without above_history_evidence")
        require(forecast["Bull"] <= max(ratios) + 1e-9,
                f"Bull {forecast['Bull']:.1%} exceeds the best historical year {max(ratios):.1%} without above_history_evidence")
    return errors


def distribution_capacity(owner_cash, growth_uses, mandatory_uses, exceptional_uses, excess_cash):
    if min(growth_uses, mandatory_uses, exceptional_uses, excess_cash) < 0:
        raise ValueError("Cash uses and excess cash must be nonnegative")
    recurring = owner_cash - growth_uses - mandatory_uses
    return recurring, recurring - exceptional_uses + excess_cash


def aggregate_coverage(cash, dividends):
    if len(cash) != len(dividends) or not cash:
        raise ValueError("Coverage needs matching, nonempty fiscal periods")
    if any(value is None for value in cash + dividends) or sum(dividends) <= 0:
        return None
    if any(value < 0 for value in dividends):
        raise ValueError("Cash dividends cannot be negative")
    return sum(cash) / sum(dividends)


def growth_present_value(cash_flows, required_return, terminal_growth, terminal_dps, terminal_time, finite=()):
    """Explicit PV and terminal PV. `finite` lists (cash_share, years) for assets whose share of the terminal
    dividend stops after `years` terminal years; the rest is a growing perpetuity."""
    if required_return <= 0 or terminal_growth <= -1 or required_return - terminal_growth < 0.02 - 1e-12:
        raise ValueError("Growth valuation requires positive R, g > -1 and R-g >= 0.02")
    if terminal_dps < 0 or terminal_time <= 0:
        raise ValueError("Invalid terminal cash or timing")
    times = [row["years_from_valuation"] for row in cash_flows]
    if not times or times != sorted(set(times)) or times[0] <= 0 or times[-1] > terminal_time:
        raise ValueError("Cash-flow times must increase and not extend beyond the terminal boundary")
    if any(row["net_dps"] < 0 for row in cash_flows):
        raise ValueError("Projected dividends cannot be negative")
    if any(not 0 < row["cash_fraction"] <= 1 for row in cash_flows):
        raise ValueError("Cash fractions must be in (0, 1]")
    explicit = sum(row["net_dps"] * row["cash_fraction"] * math.exp(-row["years_from_valuation"] * math.log1p(required_return)) for row in cash_flows)
    if any(share < 0 or years < 0 for share, years in finite) or sum(share for share, _ in finite) > 1 + 1e-9:
        raise ValueError("Finite terminal assets need nonnegative shares summing to at most 1")
    fade = (1 + terminal_growth) / (1 + required_return)
    remaining = 1 - sum(share * fade ** years for share, years in finite)
    terminal = terminal_dps / (required_return - terminal_growth) * remaining * math.exp(-terminal_time * math.log1p(required_return))
    return explicit, terminal


def terminal_finite_terms(report, growth, runway, horizon):
    """(cash_share, terminal years) per expiring asset, checked against economic_profile.finite_life_assets."""
    errors = []
    profile_assets = {row["name"]: row for row in report.get("economic_profile", {}).get("finite_life_assets", [])}
    records = growth.get("terminal_finite_assets") or []
    if not profile_assets:
        if records:
            errors.append("Growth: terminal_finite_assets without economic_profile.finite_life_assets")
        return [], errors
    if not records:
        return [], ["Growth: finite-life assets in economic_profile must enter the terminal value through "
                    "terminal_finite_assets, not only a lower perpetual growth rate"]
    names = [row["name"] for row in records]
    if sorted(names) != sorted(profile_assets):
        errors.append("Growth: terminal_finite_assets must list exactly the economic_profile finite-life assets")
    first = runway.get((min(horizon, 5), "Base"))
    base_year = None
    if first is not None and str(first["fiscal_year"]).isdigit():
        base_year = int(first["fiscal_year"]) + max(0, horizon - 5)
    if growth.get("terminal_base_fiscal_year") != base_year:
        errors.append(f"Growth: terminal_base_fiscal_year should be {base_year}, the last explicit/transition fiscal year")
    terms = []
    for row in records:
        source = profile_assets.get(row["name"])
        if source is None:
            continue
        if row["end_year"] != source["end_year"] or not math.isclose(row["cash_share"], source["operating_cash_share_pct"] / 100, abs_tol=1e-9):
            errors.append(f"Growth: terminal asset '{row['name']}' must match the profile end year and cash share")
        if row["treatment"] == "renewal_evidenced":
            if source["extension_evidence"] is None:
                errors.append(f"Growth: '{row['name']}' cannot stay in the perpetuity without profile extension_evidence")
            continue
        if base_year is not None:
            terms.append((row["cash_share"], max(0, row["end_year"] - base_year)))
    return terms, errors


@lru_cache(maxsize=1)
def schema_validator():
    schema_path = ROOT / "schema.json"
    if not schema_path.is_file():
        schema_path = ROOT / "dividend-income-equity-analysis" / "schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_report(report):
    errors = [f"{error.json_path}: {error.message}" for error in schema_validator().iter_errors(report)]
    if errors:
        return errors

    def require(condition, message):
        if not condition:
            errors.append(message)

    def same(actual, expected, label):
        if actual is None or expected is None:
            require(actual is expected, f"{label}: expected {expected}, got {actual}")
        else:
            require(math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-6),
                    f"{label}: expected {expected}, got {actual}")

    def finite_numbers(value, path="$"):
        if isinstance(value, dict):
            for key, item in value.items():
                finite_numbers(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                finite_numbers(item, f"{path}[{index}]")
        elif isinstance(value, (float, int)) and not isinstance(value, bool):
            require(math.isfinite(value), f"{path}: non-finite numbers are not allowed")

    finite_numbers(report)
    if errors:
        return errors
    errors.extend(validate_schema3(report))

    if report["mode"] == "safety_review":
        return errors + validate_safety_review(report)

    def portfolio_target_checks(params, as_of):
        if params["target_basis"] != "portfolio_target":
            return
        context = params["portfolio_context"]
        try:
            analysis_date = date.fromisoformat(as_of)
            confirmed = date.fromisoformat(context["confirmed_on"])
            expiry = date.fromisoformat(context["valid_until"]) if context["valid_until"] else None
        except (TypeError, ValueError):
            require(False, "Portfolio target requires valid analysis and context dates")
            return
        require(confirmed <= analysis_date, "Portfolio target confirmation cannot postdate the analysis")
        require(expiry is None or confirmed <= expiry, "Portfolio target validity interval is reversed")
        require(expiry is None or analysis_date <= expiry, "Portfolio target has expired; reassess the income target")

    if report["mode"] == "screen":
        params = report["screening_parameters"]
        for row in report["screen_results"]:
            portfolio_target_checks(params, row["as_of_date"])
            same(row["screening_net_yield_target"], params["target_net_yield"], "Screen target")
            target, net_yield = params["target_net_yield"], row["screening_yield_used"]
            low, high = row["screening_yield_range"]["low"], row["screening_yield_range"]["high"]
            require((low is None) == (high is None), "Screen yield range needs both endpoints or neither")
            if low is not None and high is not None:
                require(low <= high, "Screen yield range is reversed")
                if net_yield is not None:
                    require(low <= net_yield <= high, "Screen point yield lies outside its supported range")
            if target is None:
                fit = "Not Assessed"
            elif not row["screening_basis_usable"] or low is None or high is None:
                fit = "Unclear"
            else:
                fit = "Pass" if low >= target else "Below target" if high < target else "Unclear"
            require(row["yield_fit"] == fit, "Screen Yield Fit disagrees with the selected yield range and target")
            gap = (net_yield - target) * 100 if fit in ("Pass", "Below target") and net_yield is not None else None
            same(row["yield_gap_percentage_points"], gap, "Screen yield gap")
            if fit == "Below target" and params["target_policy"] == "hard_minimum":
                require(row["full_analysis_recommended"] == "No" or params.get("hard_minimum_exception_allowed", False),
                        "Screen hard minimum requires No unless the user permits an exception")
            if fit == "Unclear":
                require(row["full_analysis_recommended"] != "Yes", "Unclear screening income cannot receive Yes")
        return errors

    mode = report["valuation_mode"]
    action = report["action_assessment"]
    model = report["cash_flow_model"]
    units = model["cash_unit_scale"] / model["share_unit_scale"]
    kpi = report["key_metrics_at_a_glance"]
    for key in ("valuation_mode", "score_100", "grade", "portfolio_role"):
        require(kpi[key] == report[key], f"Key metrics disagree with top-level {key}")

    def ledger_checks(ledger, label):
        require(len({row["item"] for row in ledger}) == len(ledger), f"{label}: duplicate deduction item")
        for row in ledger:
            if not row["already_in_starting_metric"] and row["amount"] is not None:
                same(row["incremental_deduction"], row["amount"], f"{label}: {row['item']}")

    ledger_checks(model["deduction_ledger"], "Cash model")
    history = sorted(report["cash_flow_bridge"], key=lambda row: row["fiscal_year_end"])
    require(len({row["fiscal_year"] for row in history}) == len(history), "Duplicate historical fiscal year")
    require(len({row["fiscal_year_end"] for row in history}) == len(history), "Duplicate historical fiscal year end")
    require(all(row["fiscal_year_end"] <= report["as_of_date"] for row in history), "Historical fiscal periods cannot end after the analysis date")
    for row in history:
        label = row["fiscal_year"]
        div = row["cash_dividends"]
        require(div is None or div >= 0, f"{label}: negative cash dividend")
        recurring = aggregate_coverage([row["recurring_fad"]], [div])
        actual = aggregate_coverage([row["actual_distribution_capacity"]], [div])
        same(row["fcf_dividend_coverage"], recurring, f"{label} recurring coverage")
        same(row["actual_cash_coverage"], actual, f"{label} actual coverage")
        if row["evidence_status"] == "insufficient":
            require(row["recurring_fad"] is None, f"{label}: insufficient evidence cannot give precise FAD")

    errors.extend(scrip_coverage_errors(report))
    errors.extend(associate_conversion_errors(report))

    window = history[-5:]
    coverage = report["coverage_summary"]
    require(coverage["fiscal_years"] == [row["fiscal_year"] for row in window], "Coverage periods must match the latest history rows")
    require(coverage["years_available"] == len(window), "Coverage years_available disagrees with history")
    three_year = None
    if len(window) >= 3:
        three_year = aggregate_coverage([row["recurring_fad"] for row in window[-3:]],
                                        [row["cash_dividends"] for row in window[-3:]])
    same(coverage["three_year_recurring_coverage"], three_year, "Three-year aggregate coverage")
    recurring_rows = [row for row in window if row["fcf_dividend_coverage"] is not None]
    actual_rows = [row for row in window if row["actual_cash_coverage"] is not None]
    worst_recurring = min((row["fcf_dividend_coverage"] for row in recurring_rows), default=None)
    worst_actual = min((row["actual_cash_coverage"] for row in actual_rows), default=None)
    same(coverage["worst_available_recurring_coverage"], worst_recurring, "Worst available recurring coverage")
    same(coverage["five_year_worst_recurring_coverage"],
         worst_recurring if len(recurring_rows) == 5 else None, "Five-year worst recurring coverage")
    same(coverage["worst_actual_coverage"], worst_actual, "Worst actual coverage")
    for rows, field, ratio in ((recurring_rows, "worst_recurring_year", "fcf_dividend_coverage"),
                               (actual_rows, "worst_actual_year", "actual_cash_coverage")):
        expected_years = {row["fiscal_year"] for row in rows if row[ratio] == min(item[ratio] for item in rows)}
        require(coverage[field] in expected_years if rows else coverage[field] is None,
                f"{field}: year must identify an observed minimum")

    def indexed(rows, years, label):
        keys = [(row["forecast_year"], row["scenario"]) for row in rows]
        expected = {(year, scenario) for year in years for scenario in SCENARIOS}
        require(len(keys) == len(set(keys)) and set(keys) == expected,
                f"{label}: require exactly one row per year/scenario")
        return dict(zip(keys, rows))

    forecasts = indexed(report["three_year_fundamental_forecast"] + report["forecast_extension"], range(1, 6), "Forecast")
    bridges = indexed(report["dividend_forecast_bridge"], range(1, 6), "Distribution bridge")
    runway = indexed(report["dividend_and_yield_runway"], range(1, 6), "Dividend runway")
    if errors:
        return errors

    event_errors, mixed_cash_supported = validate_cash_events(report)
    errors.extend(event_errors)

    bridge_cash = ("fcf_or_capital_generation", "required_reinvestment", "mandatory_debt_or_regulatory_uses",
                   "recurring_fad", "exceptional_cash_uses", "excess_cash_used", "cash_available_for_distribution")
    runway_cash = ("cash_available_for_distribution", "dividend_cash_cost", "dividend_entitlement",
                  "cash_settled_fraction", "settlement_cash_adjustment", "derived_dps", "funding_gap", "all_cash_funding_gap")

    def settlement_checks(row, label):
        fields = ("dividend_entitlement", "cash_settled_fraction", "settlement_cash_adjustment",
                  "dividend_cash_cost", "dividend_entitled_shares")
        require(all(row[field] is not None for field in fields), f"{label}: incomplete dividend settlement")
        if any(row[field] is None for field in fields):
            return None
        same(row["dividend_cash_cost"], row["dividend_entitlement"] * row["cash_settled_fraction"]
             + row["settlement_cash_adjustment"], f"{label} issuer cash settlement")
        return row["dividend_entitlement"] * units / row["dividend_entitled_shares"]

    def policy_amount(component, forecast, shares, label):
        basis, reference = component["payout_calculation_basis"], component["payout_base_reference"]
        references = {
            "attributable_earnings": {"net_income_or_affo"},
            "issuer_defined_cash_flow": {"fcf_or_distributable_cash", "actual_all_in_fcf", "recurring_fad"},
            "recurring_fad": {"recurring_fad"},
            "fixed_dps": {"fixed_dps"},
            "discretionary": {"discretionary"},
        }
        require(reference in references.get(basis, set()), f"{label}: payout base reference is incompatible with policy basis")
        base, ratio = component["payout_base_amount"], component["payout_ratio"]
        adjustments = component["payout_base_adjustments"]
        require(len({row["item"] for row in adjustments}) == len(adjustments), f"{label}: duplicate payout-base adjustment")
        if basis in ("attributable_earnings", "issuer_defined_cash_flow", "recurring_fad"):
            amount = forecast.get(reference)
            require(amount is not None, f"{label}: missing forecast reference for payout base")
            if amount is not None:
                same(base, amount + sum(row["amount"] for row in adjustments), f"{label} payout base bridge")
            require(base is not None and ratio is not None and ratio >= 0, f"{label}: ratio policy needs base and nonnegative ratio")
            return max(0, base * ratio) if base is not None and ratio is not None and ratio >= 0 else None
        require(not adjustments, f"{label}: fixed/discretionary policy must state its direct base, not an unanchored adjustment")
        if basis == "fixed_dps":
            require(base is not None and base >= 0, f"{label}: missing fixed DPS")
            return base * shares / units if base is not None and base >= 0 else None
        if basis == "discretionary":
            require(base is not None and base >= 0, f"{label}: missing discretionary cash plan")
            return base if base is not None and base >= 0 else None
        return None

    for key, forecast in forecasts.items():
        bridge, dividend = bridges[key], runway[key]
        label = f"{key[0]} / {key[1]}"
        require(forecast["fiscal_year"] == bridge["fiscal_year"] == dividend["fiscal_year"], f"{label}: fiscal periods disagree")
        ledger_checks(bridge["deduction_ledger"], label)
        if forecast["estimate_status"] == "not_estimable":
            require(all(bridge[field] is None for field in bridge_cash), f"{label}: unavailable forecast cannot produce a cash bridge")
            require(all(dividend[field] is None for field in runway_cash), f"{label}: unavailable forecast cannot produce a dividend valuation")
            require(dividend["dps_source"] != "evidence_backed", f"{label}: missing cash cannot be evidence-backed DPS")
            continue
        require(all(bridge[field] is not None for field in bridge_cash), f"{label}: estimated cash bridge is incomplete")
        require(all(dividend[field] is not None for field in runway_cash), f"{label}: estimated dividend runway is incomplete")
        require(dividend["dividend_entitled_shares"] is not None, f"{label}: missing entitled shares")
        if any(bridge[field] is None for field in bridge_cash) or any(dividend[field] is None for field in runway_cash) or dividend["dividend_entitled_shares"] is None:
            continue
        if min(bridge[field] for field in ("required_reinvestment", "mandatory_debt_or_regulatory_uses", "exceptional_cash_uses", "excess_cash_used")) < 0:
            errors.append(f"{label}: negative cash uses")
            continue
        for category, field in (("growth", "required_reinvestment"), ("mandatory", "mandatory_debt_or_regulatory_uses"),
                                ("exceptional", "exceptional_cash_uses")):
            entries = [row for row in bridge["deduction_ledger"] if row["category"] == category]
            require(all(row["incremental_deduction"] is not None for row in entries), f"{label}: incomplete {category} deduction ledger")
            if all(row["incremental_deduction"] is not None for row in entries):
                same(bridge[field], sum(row["incremental_deduction"] for row in entries), f"{label} {category} ledger total")
        require(all(row["incremental_deduction"] == 0 for row in bridge["deduction_ledger"]
                    if row["category"] in ("maintenance", "owner_claims")), f"{label}: owner cash already includes maintenance and owner claims")
        owner = forecast["fcf_or_distributable_cash"]
        same(bridge["fcf_or_capital_generation"], owner, f"{label} owner cash / proxy")
        same(bridge["required_reinvestment"], forecast["remaining_growth_investment"], f"{label} growth investment")
        if model["sector_model"] in ("operating_company", "utility_infrastructure",
                                    "concession_infrastructure", "midstream_partnership"):
            inputs = [forecast[field] for field in ("normalized_ocf", "maintenance_capex", "other_owner_claims")]
            require(all(value is not None for value in inputs), f"{label}: missing operating owner-FCF inputs")
            if all(value is not None for value in inputs):
                same(owner, inputs[0] - inputs[1] - inputs[2], f"{label} Recurring Owner FCF")
            inflow = forecast["nonrecurring_operating_cash_inflow"]
            require(inflow is not None, f"{label}: state temporary operating cash inflows explicitly")
            if inflow is not None:
                actual_fcf = owner - bridge["required_reinvestment"] - bridge["exceptional_cash_uses"] + inflow
                same(forecast["actual_all_in_fcf"], actual_fcf, f"{label} actual all-in FCF")
        recurring, capacity = distribution_capacity(owner, bridge["required_reinvestment"],
                                                    bridge["mandatory_debt_or_regulatory_uses"],
                                                    bridge["exceptional_cash_uses"], bridge["excess_cash_used"])
        same(forecast["recurring_fad"], recurring, f"{label} forecast recurring FAD")
        same(bridge["recurring_fad"], recurring, f"{label} bridge recurring FAD")
        same(bridge["cash_available_for_distribution"], capacity, f"{label} total distribution capacity")
        same(dividend["cash_available_for_distribution"], capacity, f"{label} runway capacity")
        if dividend["dividend_installments"]:
            installments = dividend["dividend_installments"]
            dates = [item["record_date"] for item in installments]
            require(dates == sorted(dates), f"{label}: installments must follow entitlement dates")
            dps_values = []
            for item in installments:
                dps = settlement_checks(item, f"{label} {item['record_date']}")
                same(item["derived_dps"], dps, f"{label} installment DPS")
                dps_values.append(dps)
            if all(value is not None for value in dps_values):
                same(dividend["derived_dps"], sum(dps_values), f"{label} annual DPS")
            for field in ("dividend_cash_cost", "dividend_entitlement", "settlement_cash_adjustment"):
                if all(item[field] is not None for item in installments):
                    same(dividend[field], sum(item[field] for item in installments), f"{label} annual {field}")
        aggregate_dps = settlement_checks(dividend, label)
        if not dividend["dividend_installments"]:
            same(dividend["derived_dps"], aggregate_dps, f"{label} DPS")
        same(dividend["funding_gap"], max(0, dividend["dividend_cash_cost"] - capacity), f"{label} funding gap")
        same(dividend["all_cash_funding_gap"], max(0, dividend["dividend_entitlement"] - capacity), f"{label} all-cash funding gap")
        if mode == "ordinary_yield_based" and key[1] == "Base" and key[0] <= 3:
            require(dividend["funding_gap"] == 0 and dividend["all_cash_funding_gap"] == 0,
                    f"{label}: unresolved Base funding gap prevents ordinary valuation")
        policy = report["payout_policy"]
        require(dividend["payout_policy"] == policy["policy_type"], f"{label}: payout policy type disagrees with the documented policy")
        require(dividend["payout_calculation_basis"] == policy["calculation_basis"], f"{label}: payout calculation basis disagrees with the documented policy")
        if policy["policy_type"] == "base_variable":
            components = dividend["policy_components"]
            require(len(components) == 2 and {item["component"] for item in components} == {"base", "variable"},
                    f"{label}: base/variable policy needs both components")
            amounts = []
            for component in components:
                amount = policy_amount(component, forecast, dividend["dividend_entitled_shares"], label)
                same(component["policy_implied_dividend"], amount, f"{label} policy component")
                amounts.append(amount)
            if len(amounts) == 2 and all(amount is not None for amount in amounts):
                same(dividend["policy_implied_dividend"], sum(amounts), f"{label} base-plus-variable cash")
        else:
            require(not dividend["policy_components"], f"{label}: unexpected base/variable components")
            amount = policy_amount(dividend, forecast, dividend["dividend_entitled_shares"], label)
            same(dividend["policy_implied_dividend"], amount, f"{label} policy dividend")

    if errors:
        return errors

    cumulative = report["business_outlook"]["cumulative_fad"]
    require({row["scenario"] for row in cumulative} == set(SCENARIOS), "Cumulative FAD must cover each scenario once")
    for row in cumulative:
        for horizon, field in ((3, "three_year"), (5, "five_year")):
            values = [forecasts[(year, row["scenario"])]["recurring_fad"] for year in range(1, horizon + 1)]
            same(row[field], None if any(value is None for value in values) else sum(values), f"{row['scenario']} cumulative {horizon}-year FAD")

    returns = report["return_requirements"]
    if returns["status"] == "assessed":
        require(returns["benchmark_date"] <= report["as_of_date"], "Risk-free observation cannot postdate the analysis")
        require(returns["benchmark_currency"] == returns["valuation_currency"] or returns.get("benchmark_currency_basis"),
                "A risk-free benchmark in another currency needs benchmark_currency_basis "
                "(matching sovereign source tried, why not used, peg/hedge treatment)")
        same(returns["required_total_return_low"], returns["risk_free_rate"] + returns["risk_premium_low"], "Required return low")
        same(returns["required_total_return_high"], returns["risk_free_rate"] + returns["risk_premium_high"], "Required return high")
        require(returns["required_total_return_high"] > returns["required_total_return_low"], "Return range must be ordered and nonempty")
    income = report["income_assessment"]
    portfolio_target_checks(income["target"], report["as_of_date"])
    target, net_yield = income["target"]["target_net_yield"], income["forward_net_yield"]
    forward_dps, price = income["forward_net_dps"], report["price_used"]
    scrip = report["scrip_drip"]
    cash_assumption = scrip["investor_cash_yield_assumption"]
    cash_option = scrip["cash_election_available"]
    mandatory_stock = not mixed_cash_supported and (cash_assumption == "mandatory_shares" or cash_option == "No")
    plain_cash = (scrip["available"] == "No" and cash_option == "Not Applicable"
                  and cash_assumption == "not_applicable"
                  and scrip["default_election"] in ("cash", "none", "not_applicable"))
    cash_income_supported = (plain_cash or (cash_option == "Yes" and cash_assumption == "all_cash_election")
                             or mixed_cash_supported)
    tax_supported = (report["withholding_rate"] is not None
                     and report["withholding_basis"] in SUPPORTED_WITHHOLDING_BASES)

    if mandatory_stock:
        require(mode == "suspended", "Mandatory stock / no cash election requires suspended cash-dividend valuation")
        require(all(row["derived_dps"] in (None, 0) and row["dividend_entitlement"] in (None, 0)
                    and row["dividend_cash_cost"] in (None, 0) for row in runway.values()),
                "Mandatory stock distributions must be excluded from the cash-income runway")
    if not cash_income_supported:
        require(forward_dps in (None, 0), "No supported investor cash election can produce positive forward cash DPS")
        require(income["income_eligible"] is not True, "Unverified cash election cannot establish income eligibility")
    if not tax_supported:
        require(income["yield_fit"] != "Pass" and income["income_eligible"] is not True,
                "Unverified withholding cannot establish income eligibility")
    same(net_yield, forward_dps / price if forward_dps is not None and price is not None else None,
         "Forward cash yield")
    ceiling = None
    if income["target"]["target_policy"] == "hard_minimum" and target is not None and target > 0 and forward_dps is not None:
        ceiling = forward_dps / target
    same(income["income_price_ceiling"], ceiling, "Hard-income price ceiling")
    if target is not None and net_yield is not None:
        require(income["yield_fit"] == ("Pass" if net_yield >= target else "Below target"), "Full-analysis income fit disagrees with cash yield")
    elif net_yield is None:
        require(income["yield_fit"] == "Not Assessed" and income["income_eligible"] is None, "Missing cash yield cannot pass an income requirement")

    credit = returns.get("income_growth_credit") or 0
    errors.extend(income_growth_credit_errors(report, runway, mode))
    if "buy_zone" in report:
        zone = report["buy_zone"]
        if zone["normalized_net_dps_basis"] == "three_year_base_average":
            require(zone["dps_currency"] == model["financial_currency"], "Base-average source DPS currency must match the runway")
            values = [investor_cash_dps(runway[(year, "Base")], units) for year in range(1, 4)]
            require(all(value is not None for value in values) and report["withholding_rate"] is not None,
                    "Three-year Base-average N requires sourced DPS, withholding and currency conversion")
            if all(value is not None for value in values) and report["withholding_rate"] is not None:
                average = sum(values) / 3 * (1 - report["withholding_rate"])
                average *= zone["normalization_fx_rate"] * returns["shares_per_quoted_security"]
                average = (average - zone["normalization_cash_deductions"]) / returns["valuation_unit_scale"]
                same(zone["normalized_net_dps"], average, "Three-year Base-average N")
        try:
            boundaries = ordinary_boundaries(zone["normalized_net_dps"], zone["bear_net_dps"],
                                              zone["required_net_yield_low"], zone["required_net_yield_high"],
                                              credit if mode == "ordinary_yield_based" else 0)
        except ValueError as error:
            errors.append(str(error))
        else:
            for field, value in boundaries.items():
                same(zone["boundaries"][field], value, f"Ordinary {field}")
        if mode == "finite_life_harvest":
            require(zone["required_net_yield_low"] >= 0.1, "Harvest ordinary cross-check needs r_low >= 10%")
        else:
            label = "Growth-credited" if credit else "Zero-growth"
            same(zone["required_net_yield_low"], returns["required_total_return_low"] - credit, f"{label} income r_low")
            same(zone["required_net_yield_high"], returns["required_total_return_high"] - credit, f"{label} income r_high")

    if mode == "finite_life_harvest":
        harvest = report["finite_life_valuation"]
        require(returns["status"] == "assessed", "Finite-life valuation requires an independent return derivation")
        require(harvest["finite_life_value_low"] <= harvest["finite_life_value_high"], "Finite-life value range is reversed")
        cash_path = harvest["forecast_net_distributions"]
        horizon, rate = harvest["harvest_horizon_years"], harvest["discount_rate"]
        times = [row.get("years_from_valuation", index + 1) for index, row in enumerate(cash_path)]
        require(len(cash_path) == horizon, "Finite-life cash path must cover the full harvest horizon")
        require(times == sorted(set(times)) and times[0] > 0, "Finite-life cash times must be positive and increasing")
        total_pv = 0
        for row, when in zip(cash_path, times):
            amount = row.get("net_distribution")
            require(amount is not None and amount >= 0, "Finite-life distributions must be supported nonnegative cash")
            if amount is not None and amount >= 0:
                pv = amount * math.exp(-when * math.log1p(rate))
                same(row.get("present_value"), pv, "Finite-life distribution PV")
                total_pv += pv
        same(harvest["present_value_of_distributions"], total_pv, "Finite-life distribution PV total")
        residual_pv = harvest["residual_value"] * math.exp(-times[-1] * math.log1p(rate))
        if harvest.get("residual_value_share_of_total") is not None:
            same(harvest["residual_value_share_of_total"], residual_pv / (total_pv + residual_pv) if total_pv + residual_pv else None,
                 "Finite-life residual share")

    if "capital_return_valuation" in report:
        errors.extend(capital_return_errors(report))
    if "growth_valuation" in report:
        require(mode == "total_return_based", "Growth valuation cannot bypass the primary mode's eligibility gates")
        require(cash_income_supported and tax_supported, "Growth valuation requires supported cash election and withholding")
        growth = report["growth_valuation"]
        require(growth["terminal_growth_cap"] <= growth["long_run_nominal_growth_bound"], "Terminal cap exceeds the currency's evidenced long-run bound")
        scenarios = {row["scenario"]: row for row in growth["scenarios"]}
        require(set(scenarios) == set(SCENARIOS), "Growth valuation must include all three scenarios")
        for key, forecast in forecasts.items():
            require(forecast["estimate_status"] == "estimated", "Growth terminal value cannot bypass an unsupported five-year cash outlook")
            dividend = runway[key]
            require(dividend["dps_source"] == "evidence_backed",
                    f"{key}: illustrative DPS cannot enter growth value, including years after an early terminal boundary")
            if dividend["dividend_entitlement"] is not None and forecast["recurring_fad"] is not None:
                require(dividend["dividend_entitlement"] <= forecast["recurring_fad"] and dividend["funding_gap"] == 0 and dividend["all_cash_funding_gap"] == 0,
                        f"{key}: growth requires funded dividends throughout the five-year outlook")
        finite, finite_errors = terminal_finite_terms(report, growth, runway,
                                                      growth["explicit_horizon_years"] + growth["transition_years"])
        errors.extend(finite_errors)
        for row in growth["scenarios"]:
            label = f"Growth {row['scenario']}"
            path = row["forecast_cash_flows"]
            horizon = growth["explicit_horizon_years"] + growth["transition_years"]
            years = sorted({cash["forecast_year"] for cash in path})
            require(len(years) == horizon and all(year == index + 1 for index, year in enumerate(years)),
                    f"{label}: incomplete annual cash path")
            for year in years:
                fraction = sum(cash["cash_fraction"] for cash in path if cash["forecast_year"] == year)
                if year == 1:
                    require(fraction <= 1 + 1e-12, f"{label}: first-year cash entitlement counted more than once")
                else:
                    same(fraction, 1, f"{label} year {year} cash entitlement")
            require(row["terminal_growth"] <= growth["terminal_growth_cap"], f"{label}: terminal growth above cap")
            require(row["terminal_growth"] <= row["sustainable_terminal_growth_bound"], f"{label}: terminal growth above sustainable company bound")
            require(returns["status"] == "assessed", f"{label}: missing required return")
            if returns["status"] == "assessed":
                require(returns["required_total_return_low"] <= row["required_return"] <= returns["required_total_return_high"], f"{label}: R outside documented range")
            for cash in path:
                if cash["forecast_year"] <= 5:
                    key = (cash["forecast_year"], row["scenario"])
                    support, recurring = runway[key], forecasts[key]["recurring_fad"]
                else:
                    support = cash["transition_support"]
                    recurring = support["recurring_fad"]
                amount, shares = support["dividend_entitlement"], support["dividend_entitled_shares"]
                require(amount is not None and shares is not None and recurring is not None, f"{label}: missing funded cash support")
                if amount is not None and shares is not None and recurring is not None:
                    require(0 <= amount <= recurring, f"{label}: dividend is not funded by recurring FAD")
                    capacity = support["cash_available_for_distribution"]
                    require(capacity is not None and max(amount, support["dividend_cash_cost"]) <= capacity, f"{label}: dividend exceeds actual distribution capacity")
                    same(support["funding_gap"], 0, f"{label} unresolved funding gap")
                    settlement_checks(support, label)
                    if report["withholding_rate"] is None:
                        errors.append(f"{label}: missing withholding basis")
                    else:
                        net = investor_cash_dps(support, units) * (1 - report["withholding_rate"])
                        net *= cash["fx_to_valuation_currency"] * returns["shares_per_quoted_security"]
                        net = (net - cash["investor_cash_deductions"]) / returns["valuation_unit_scale"]
                        same(cash["net_dps"], net, f"{label}: cash path / runway reconciliation")
            try:
                explicit, terminal = growth_present_value(path, row["required_return"], row["terminal_growth"],
                                                          row["terminal_net_dps"], row["terminal_time_years"], finite)
            except ValueError as error:
                errors.append(f"{label}: {error}")
                continue
            same(row["present_value_of_dividends"], explicit, f"{label} explicit PV")
            same(row["present_value_of_terminal"], terminal, f"{label} terminal PV")
            same(row["total_value"], explicit + terminal, f"{label} value")
            same(row["terminal_value_share"], terminal / (explicit + terminal) if explicit + terminal > 0 else None, f"{label} terminal share")
            last_full_dps = sum(cash["net_dps"] * cash["cash_fraction"] for cash in path if cash["forecast_year"] == horizon)
            same(row["terminal_net_dps"], last_full_dps * (1 + row["terminal_growth"]), f"{label} first terminal-year DPS")
            funding = row["terminal_funding"]
            terminal_fad = funding["owner_cash_or_proxy"] - funding["remaining_growth_uses"] - funding["remaining_mandatory_uses"]
            same(funding["recurring_fad"], terminal_fad, f"{label} terminal recurring FAD")
            require(funding["dividend_entitlement"] <= terminal_fad and funding["dividend_cash_cost"] <= terminal_fad, f"{label}: terminal dividend is unfunded")
            settlement_checks(funding, label)
            if horizon < 5:
                next_key = (horizon + 1, row["scenario"])
                same(funding["recurring_fad"], forecasts[next_key]["recurring_fad"], f"{label} terminal / next forecast FAD")
                same(funding["dividend_cash_cost"], runway[next_key]["dividend_cash_cost"], f"{label} terminal / next forecast dividend")
                same(funding["dividend_entitlement"], runway[next_key]["dividend_entitlement"], f"{label} terminal / next forecast entitlement")
                same(funding["dividend_entitled_shares"], runway[next_key]["dividend_entitled_shares"], f"{label} terminal / next forecast shares")
                for year in range(horizon + 1, 6):
                    known_dps = investor_cash_dps(runway[(year, row["scenario"])], units)
                    if known_dps is None or report["withholding_rate"] is None:
                        continue  # Missing support is reported by the five-year and cash-path gates above.
                    known_net = known_dps * (1 - report["withholding_rate"])
                    known_net *= funding["fx_to_valuation_currency"] * returns["shares_per_quoted_security"]
                    known_net = (known_net - funding["investor_cash_deductions"]) / returns["valuation_unit_scale"]
                    expected_net = row["terminal_net_dps"] * (1 + row["terminal_growth"]) ** (year - horizon - 1)
                    same(known_net, expected_net,
                         f"{label} year {year} early terminal path; extend the explicit/transition horizon if the outlook changes")
            if report["withholding_rate"] is not None:
                terminal_dps = investor_cash_dps(funding, units)
                terminal_dps *= (1 - report["withholding_rate"]) * funding["fx_to_valuation_currency"] * returns["shares_per_quoted_security"]
                terminal_dps = (terminal_dps - funding["investor_cash_deductions"]) / returns["valuation_unit_scale"]
                same(row["terminal_net_dps"], terminal_dps, f"{label} funded terminal DPS")
            if row["terminal_value_share"] > 0.75:
                require(report["forecast_confidence"] != "High", f"{label}: high terminal dependence requires lower confidence")
        values = [row["total_value"] for row in growth["scenarios"]]
        same(growth["growth_value_low"], min(values), "Growth value low")
        same(growth["growth_value_high"], max(values), "Growth value high")
        if "Base" in scenarios:
            same(growth["base_case_value"], scenarios["Base"]["total_value"], "Base growth value")
        same(growth["entry_upper"], min(values) * (1 - growth["margin_of_safety"]), "Growth entry upper")
        same(growth["review_above"], max(values), "Growth review threshold")
        for sensitivity in growth["return_growth_sensitivity"]:
            rate, g = sensitivity["required_return"], sensitivity["terminal_growth"]
            status = "calculated"
            if rate - g < 0.02 - 1e-12:
                status = "invalid_spread"
            elif g > growth["terminal_growth_cap"] or ("Base" in scenarios and g > scenarios["Base"]["sustainable_terminal_growth_bound"]):
                status = "invalid_growth_cap"
            require(sensitivity["status"] == status, "R/g sensitivity status disagrees with spread/growth cap")
            if status != "calculated":
                require(sensitivity["value"] is None, "Invalid R/g sensitivity cannot have a value")
            elif "Base" in scenarios:
                base = scenarios["Base"]
                terminal_year = max(cash["forecast_year"] for cash in base["forecast_cash_flows"])
                terminal_dps = sum(cash["net_dps"] * cash["cash_fraction"] for cash in base["forecast_cash_flows"]
                                   if cash["forecast_year"] == terminal_year) * (1 + g)
                try:
                    explicit, terminal = growth_present_value(base["forecast_cash_flows"], rate, g,
                                                              terminal_dps, base["terminal_time_years"], finite)
                except ValueError as error:
                    errors.append(f"R/g sensitivity: {error}")
                else:
                    same(sensitivity["value"], explicit + terminal, "Base-path R/g sensitivity value")

    for sensitivity in report["driver_sensitivity"]:
        if sensitivity["sensitivity_type"] != "transient":
            continue
        audit, change = sensitivity["growth_cash_delta_audit"], sensitivity["growth_value_change"]
        if change is None:
            require(not audit, "Unassessed transient growth change cannot carry a calculated audit")
            continue
        require(mode == "total_return_based" and bool(audit), "Transient growth value needs an assessed DDM and dated cash audit")
        base = next((row for row in report.get("growth_valuation", {}).get("scenarios", []) if row["scenario"] == "Base"), None)
        if base is None:
            continue
        seen = set()
        for item in audit:
            key = (item["forecast_year"], item["years_from_valuation"])
            require(key not in seen, "Duplicate transient cash audit period")
            seen.add(key)
            matches = [cash for cash in base["forecast_cash_flows"]
                       if cash["forecast_year"] == item["forecast_year"] and math.isclose(cash["years_from_valuation"], item["years_from_valuation"])]
            require(len(matches) == 1, "Transient audit must reference a Base cash-flow period")
            if len(matches) == 1:
                same(item["baseline_net_cash"], matches[0]["net_dps"] * matches[0]["cash_fraction"], "Transient baseline net cash")
            same(item["required_return"], base["required_return"], "Transient unchanged required return")
            delta = item["revised_net_cash"] - item["baseline_net_cash"]
            same(item["delta_net_cash"], delta, "Transient net cash delta")
            same(item["present_value_change"], delta * math.exp(-item["years_from_valuation"] * math.log1p(item["required_return"])), "Transient cash PV delta")
        same(change, sum(item["present_value_change"] for item in audit), "Transient growth-value change")

    holding = report["holding_review"]
    local_errors, entry_limitations = validate_local_analysis(report)
    errors.extend(local_errors)
    normalization_gaps = []
    if not tax_supported:
        entry_limitations.append("Unverified withholding permits diagnostic only, not eligible entry")
    if not cash_income_supported:
        entry_limitations.append("Unverified investor cash election permits diagnostic only, not eligible entry")
    if report["forecast_confidence"] == "Not Forecastable":
        require(mode == "suspended", "Not Forecastable requires suspended valuation")
    elif report["forecast_confidence"] == "Low":
        entry_limitations.append("Low confidence cannot support eligible entry")
    if report["dividend_safety"] in ("Weak", "Unclear"):
        entry_limitations.append("Weak or unclear dividend safety cannot support eligible entry")
    if "buy_zone" in report:
        zone = report["buy_zone"]
        evidence = zone["normalization_evidence"]
        gaps = [link for link, record in evidence.items() if record["status"] != "supported"]
        normalization_gaps = gaps
        for link, record in evidence.items():
            require(all(reference in report["sources"] for reference in record["source_refs"]),
                    f"Normalization {link}: source_refs must identify declared report sources")
        if gaps:
            require(action["status"] != "eligible" and not action["strong_buy_eligible"]
                    and report["portfolio_role"] in ("Watchlist", "Avoid"),
                    f"Incomplete normalization evidence ({', '.join(gaps)}) is diagnostic only")
        if zone["normalized_net_dps_basis"] == "historical_fundamental_fallback" or zone["bear_net_dps_is_fallback"] or (mode == "ordinary_yield_based" and zone["bear_net_dps"] == 0):
            entry_limitations.append("Fallback N or zero Bear dividend is diagnostic only")
        if zone["normalized_net_dps_basis"] == "three_year_base_average":
            if any(runway[(year, "Base")]["dps_source"] != "evidence_backed" for year in range(1, 4)):
                require(bool(gaps), "Illustrative Base-average N must disclose a missing or conflicting evidence link")
                entry_limitations.append("Illustrative or unknown Base-average N is diagnostic only")
    if mode == "ordinary_yield_based":
        if any(runway[(year, scenario)]["dps_source"] != "evidence_backed"
               for year in range(1, 4) for scenario in ("Bear", "Base")):
            entry_limitations.append("Illustrative or fallback ordinary dividend sources are diagnostic only")
    non_income_limitations = entry_limitations.copy()
    price_only_income_shortfall = (
        report.get("schema_version") in ("2.5", "3.0")
        and not errors and not non_income_limitations and not normalization_gaps
        and mode in ("ordinary_yield_based", "total_return_based", "capital_return_based")
        and income["target"]["target_policy"] == "hard_minimum"
        and target is not None and target > 0
        and income["income_eligible"] is False and income["yield_fit"] == "Below target"
        and ceiling is not None and ceiling > 0 and price is not None and price > ceiling
        and report.get("entry_plan", {}).get("current_action") == "wait_for_price"
        and report.get("entry_plan", {}).get("risk_review", {}).get("status") == "pass"
        and report["value_trap_veto"] == "Not triggered"
    )
    if income["target"]["target_policy"] == "hard_minimum" and income["income_eligible"] is not True:
        entry_limitations.append("Eligible entry requires confirmed hard-income eligibility")
    for limitation in entry_limitations:
        require(action["status"] != "eligible" and not action["strong_buy_eligible"]
                and (price_only_income_shortfall or report["portfolio_role"] in ("Watchlist", "Avoid")),
                limitation)
    if action["status"] == "diagnostic_only":
        require(not action["strong_buy_eligible"]
                and (price_only_income_shortfall or report["portfolio_role"] in ("Watchlist", "Avoid")),
                "Diagnostic entry cannot be Strong Buy; only an evidenced price-only income shortfall preserves a security role")
    if action["strong_buy_eligible"]:
        require(income["income_eligible"] is not False, "Strong Buy cannot override income constraints")
        if income["target"]["target_policy"] == "hard_minimum":
            require(income["income_eligible"] is True, "Strong Buy requires confirmed hard-income eligibility")
        if mode == "ordinary_yield_based":
            require(price is not None and 0 < price <= report["buy_zone"]["boundaries"]["strong_buy_at_or_below"],
                    "Strong Buy price must meet the Bear income threshold")
        elif mode == "total_return_based":
            require(price is not None and price <= report["growth_valuation"]["entry_upper"],
                    "Strong Buy price must meet the growth entry threshold")
        elif mode == "capital_return_based":
            require(price is not None and price <= report["capital_return_valuation"]["entry_upper"],
                    "Strong Buy price must meet the capital-return entry threshold")
    if holding["action"] == "switch":
        switch = holding["switch_analysis"]
        require(switch["after_cost_advantage"] > switch["switching_hurdle"], "Switch benefit must exceed the documented after-cost hurdle")
    if "scorecard" in report:
        errors.extend(validate_decision_framework(
            report, tax_supported=tax_supported, cash_supported=cash_income_supported,
            evidence_limitations=non_income_limitations + normalization_gaps,
        ))
    return errors



def capital_return_errors(report):
    """Tangible-book residual-income value (buy-zone.md Section 7A)."""
    errors = []

    def require(condition, message):
        if not condition:
            errors.append("Capital-return valuation: " + message)

    def close(actual, expected, label):
        require(actual is not None and math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-9),
                f"{label}: expected {expected}, got {actual}")

    value = report["capital_return_valuation"]
    returns = report["return_requirements"]
    require(report["valuation_mode"] == "capital_return_based",
            "the record is only valid as the capital_return_based primary mode")
    require(returns["status"] == "assessed", "requires an assessed required return")
    if returns["status"] == "assessed":
        close(value["required_return_low"], returns["required_total_return_low"], "required_return_low")
        close(value["required_return_high"], returns["required_total_return_high"], "required_return_high")
    require(value["book_value_currency"] == returns["valuation_currency"], "book value must be in the valuation currency")
    g = value["long_run_growth"]
    require(g <= value["long_run_nominal_growth_bound"], "long-run growth above its documented bound")
    require(value["required_return_low"] - g >= 0.02 - 1e-12, "required return must exceed growth by at least 2 points")
    rows = {row["scenario"]: row for row in value["scenarios"]}
    require(set(rows) == {"Bear", "Base", "Bull"}, "needs Bear, Base and Bull exactly once")
    if set(rows) != {"Bear", "Base", "Bull"}:
        return errors
    rotes = [rows[s]["sustainable_return_on_tangible_equity"] for s in ("Bear", "Base", "Bull")]
    require(rotes == sorted(rotes), "returns on tangible equity must rise from Bear to Bull")
    bv = value["book_value_per_share"]
    for name, row in rows.items():
        rote = row["sustainable_return_on_tangible_equity"]
        close(row["value_at_required_high"], bv * (rote - g) / (value["required_return_high"] - g), f"{name} value at R_high")
        close(row["value_at_required_low"], bv * (rote - g) / (value["required_return_low"] - g), f"{name} value at R_low")
    low = min(row["value_at_required_high"] for row in rows.values())
    high = max(row["value_at_required_low"] for row in rows.values())
    close(value["value_low"], low, "value_low")
    close(value["value_high"], high, "value_high")
    close(value["base_case_value"], rows["Base"]["value_at_required_high"], "base_case_value")
    close(value["entry_upper"], low * (1 - value["margin_of_safety"]), "entry_upper")
    close(value["review_above"], high, "review_above")
    capacity = value.get("distribution_capacity")
    require(capacity is not None, "needs distribution_capacity linking the formula to forecast capital generation")
    if capacity is None:
        return errors
    forecasts = {(row["forecast_year"], row["scenario"]): row
                 for row in report["three_year_fundamental_forecast"] + report.get("forecast_extension", [])}
    runway = {(row["forecast_year"], row["scenario"]): row for row in report["dividend_and_yield_runway"]}
    caps = {row["scenario"]: row for row in capacity["scenarios"]}
    require(set(caps) == {"Bear", "Base", "Bull"}, "distribution_capacity needs Bear, Base and Bull exactly once")
    for name in set(caps) & set(rows):
        cap, rote = caps[name], rows[name]["sustainable_return_on_tangible_equity"]
        implied = (rote - g) / rote if rote > 0 else None
        if implied is None:
            require(False, f"{name}: sustainable RoTE must be positive")
            continue
        close(cap["implied_distribution_ratio"], implied, f"{name} implied distribution ratio")
        years = [forecasts.get((year, name)) for year in range(1, 6)]
        if not all(row and row["recurring_fad"] is not None and row["net_income_or_affo"] for row in years):
            require(False, f"{name}: needs five forecast years of earnings and capital generation")
            continue
        ratio = sum(row["recurring_fad"] for row in years) / sum(row["net_income_or_affo"] for row in years)
        close(cap["forecast_distributable_ratio"], ratio, f"{name} forecast distributable ratio")
        require(implied <= ratio + 1e-9,
                f"{name}: the formula assumes {implied:.0%} of earnings is returned but forecast capital generation "
                f"supports only {ratio:.0%}; lower RoTE or g, or show the capital")
        payout = runway.get((1, name), {}).get("payout_ratio")
        if payout is not None:
            close(cap["dividend_payout_ratio"], payout, f"{name} dividend payout ratio")
        close(cap["buyback_capacity_ratio"], ratio - cap["dividend_payout_ratio"], f"{name} buyback capacity ratio")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="A saved Screen, Safety Review or Full Analysis JSON file")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"Cannot read analysis JSON: {error}\n")
    errors = validate_report(report)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Analysis contract passed (source accuracy and investment judgment are not verified).")


if __name__ == "__main__":
    main()
