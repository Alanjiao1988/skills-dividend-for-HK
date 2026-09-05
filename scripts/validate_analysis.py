"""Validate research JSON structure and cross-field arithmetic, not market facts."""

import argparse
import json
import math
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("Bear", "Base", "Bull")


def ordinary_boundaries(n, b, r_low, r_high):
    if not (0 <= b <= n and n > 0 and 0 < r_low < r_high):
        raise ValueError("Ordinary valuation requires 0 <= B <= N, N > 0 and 0 < r_low < r_high")
    return {
        "too_expensive_above": n / r_low,
        "fair_lower": n / r_high,
        "fair_upper": n / r_low,
        "accumulation_lower": b / r_high,
        "accumulation_upper": n / r_high,
        "strong_buy_at_or_below": b / r_high,
    }


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


def growth_present_value(cash_flows, required_return, terminal_growth, terminal_dps, terminal_time):
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
    terminal = terminal_dps / (required_return - terminal_growth) * math.exp(-terminal_time * math.log1p(required_return))
    return explicit, terminal


@lru_cache(maxsize=1)
def schema_validator():
    schema_path = ROOT / "dividend-income-equity-analysis" / "schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
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

    if report["mode"] == "screen":
        params = report["screening_parameters"]
        for row in report["screen_results"]:
            same(row["screening_net_yield_target"], params["target_net_yield"], "Screen target")
            target, net_yield = params["target_net_yield"], row.get("ttm_net_yield")
            if target is not None and net_yield is not None:
                fit = "Pass" if net_yield >= target else "Below target"
                require(row["yield_fit"] == fit, "Screen Yield Fit disagrees with the supplied target")
                same(row["yield_gap_percentage_points"], (net_yield - target) * 100, "Screen yield gap")
        return errors

    mode = report["valuation_mode"]
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

    bridge_cash = ("fcf_or_capital_generation", "required_reinvestment", "mandatory_debt_or_regulatory_uses",
                   "recurring_fad", "exceptional_cash_uses", "excess_cash_used", "cash_available_for_distribution")
    runway_cash = ("cash_available_for_distribution", "dividend_cash_cost", "derived_dps", "funding_gap")

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
        if model["sector_model"] in ("operating_company", "utility_infrastructure"):
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
        same(dividend["derived_dps"], dividend["dividend_cash_cost"] * units / dividend["dividend_entitled_shares"], f"{label} DPS")
        same(dividend["funding_gap"], max(0, dividend["dividend_cash_cost"] - capacity), f"{label} funding gap")
        if mode == "ordinary_yield_based" and key[1] == "Base" and key[0] <= 3:
            require(dividend["funding_gap"] == 0, f"{label}: unresolved Base funding gap prevents ordinary valuation")
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

    cumulative = report["business_outlook"]["cumulative_fad"]
    require({row["scenario"] for row in cumulative} == set(SCENARIOS), "Cumulative FAD must cover each scenario once")
    for row in cumulative:
        for horizon, field in ((3, "three_year"), (5, "five_year")):
            values = [forecasts[(year, row["scenario"])]["recurring_fad"] for year in range(1, horizon + 1)]
            same(row[field], None if any(value is None for value in values) else sum(values), f"{row['scenario']} cumulative {horizon}-year FAD")

    returns = report["return_requirements"]
    if returns["status"] == "assessed":
        require(returns["benchmark_date"] <= report["as_of_date"], "Risk-free observation cannot postdate the analysis")
        same(returns["required_total_return_low"], returns["risk_free_rate"] + returns["risk_premium_low"], "Required return low")
        same(returns["required_total_return_high"], returns["risk_free_rate"] + returns["risk_premium_high"], "Required return high")
        require(returns["required_total_return_high"] > returns["required_total_return_low"], "Return range must be ordered and nonempty")
    income = report["income_assessment"]
    target, net_yield = income["target"]["target_net_yield"], income["forward_net_yield"]
    forward_dps, price = income["forward_net_dps"], report["price_used"]
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

    if "buy_zone" in report:
        zone = report["buy_zone"]
        if zone["normalized_net_dps_basis"] == "three_year_base_average":
            require(zone["dps_currency"] == model["financial_currency"], "Base-average source DPS currency must match the runway")
            values = [runway[(year, "Base")]["derived_dps"] for year in range(1, 4)]
            require(all(value is not None for value in values) and report["withholding_rate"] is not None,
                    "Three-year Base-average N requires sourced DPS, withholding and currency conversion")
            if all(value is not None for value in values) and report["withholding_rate"] is not None:
                average = sum(values) / 3 * (1 - report["withholding_rate"])
                average *= zone["normalization_fx_rate"] * returns["shares_per_quoted_security"]
                average = (average - zone["normalization_cash_deductions"]) / returns["valuation_unit_scale"]
                same(zone["normalized_net_dps"], average, "Three-year Base-average N")
        try:
            boundaries = ordinary_boundaries(zone["normalized_net_dps"], zone["bear_net_dps"],
                                              zone["required_net_yield_low"], zone["required_net_yield_high"])
        except ValueError as error:
            errors.append(str(error))
        else:
            for field, value in boundaries.items():
                same(zone["boundaries"][field], value, f"Ordinary {field}")
        if mode == "finite_life_harvest":
            require(zone["required_net_yield_low"] >= 0.1, "Harvest ordinary cross-check needs r_low >= 10%")
        else:
            same(zone["required_net_yield_low"], returns["required_total_return_low"], "Zero-growth income r_low")
            same(zone["required_net_yield_high"], returns["required_total_return_high"], "Zero-growth income r_high")

    if mode == "finite_life_harvest":
        harvest = report["finite_life_valuation"]
        require(returns["status"] == "assessed", "Finite-life valuation requires an independent return derivation")
        require(harvest["finite_life_value_low"] <= harvest["finite_life_value_high"], "Finite-life value range is reversed")

    if "growth_valuation" in report:
        require(mode == "total_return_based", "Growth valuation cannot bypass the primary mode's eligibility gates")
        growth = report["growth_valuation"]
        require(growth["terminal_growth_cap"] <= growth["long_run_nominal_growth_bound"], "Terminal cap exceeds the currency's evidenced long-run bound")
        scenarios = {row["scenario"]: row for row in growth["scenarios"]}
        require(set(scenarios) == set(SCENARIOS), "Growth valuation must include all three scenarios")
        for key, forecast in forecasts.items():
            require(forecast["estimate_status"] == "estimated", "Growth terminal value cannot bypass an unsupported five-year cash outlook")
            dividend = runway[key]
            if dividend["dividend_cash_cost"] is not None and forecast["recurring_fad"] is not None:
                require(dividend["dividend_cash_cost"] <= forecast["recurring_fad"] and dividend["funding_gap"] == 0,
                        f"{key}: growth requires funded dividends throughout the five-year outlook")
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
                    require(support["dps_source"] == "evidence_backed", f"{label}: illustrative DPS cannot enter growth value")
                else:
                    support = cash["transition_support"]
                    recurring = support["recurring_fad"]
                amount, shares = support["dividend_cash_cost"], support["dividend_entitled_shares"]
                require(amount is not None and shares is not None and recurring is not None, f"{label}: missing funded cash support")
                if amount is not None and shares is not None and recurring is not None:
                    require(0 <= amount <= recurring, f"{label}: dividend is not funded by recurring FAD")
                    capacity = support["cash_available_for_distribution"]
                    require(capacity is not None and amount <= capacity, f"{label}: dividend exceeds actual distribution capacity")
                    same(support["funding_gap"], 0, f"{label} unresolved funding gap")
                    if report["withholding_rate"] is None:
                        errors.append(f"{label}: missing withholding basis")
                    else:
                        net = amount * units / shares * (1 - report["withholding_rate"])
                        net *= cash["fx_to_valuation_currency"] * returns["shares_per_quoted_security"]
                        net = (net - cash["investor_cash_deductions"]) / returns["valuation_unit_scale"]
                        same(cash["net_dps"], net, f"{label}: cash path / runway reconciliation")
            try:
                explicit, terminal = growth_present_value(path, row["required_return"], row["terminal_growth"],
                                                          row["terminal_net_dps"], row["terminal_time_years"])
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
            require(funding["dividend_cash_cost"] <= terminal_fad, f"{label}: terminal dividend is unfunded")
            if horizon < 5:
                next_key = (horizon + 1, row["scenario"])
                same(funding["recurring_fad"], forecasts[next_key]["recurring_fad"], f"{label} terminal / next forecast FAD")
                same(funding["dividend_cash_cost"], runway[next_key]["dividend_cash_cost"], f"{label} terminal / next forecast dividend")
                same(funding["dividend_entitled_shares"], runway[next_key]["dividend_entitled_shares"], f"{label} terminal / next forecast shares")
            if report["withholding_rate"] is not None:
                terminal_dps = funding["dividend_cash_cost"] * units / funding["dividend_entitled_shares"]
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
                                                              terminal_dps, base["terminal_time_years"])
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
    if holding["action"] == "switch":
        switch = holding["switch_analysis"]
        require(switch["after_cost_advantage"] > switch["switching_hurdle"], "Switch benefit must exceed the documented after-cost hurdle")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="A saved Screen or Full Analysis JSON file")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"Cannot read analysis JSON: {error}\n")
    errors = validate_report(report)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Analysis contract passed (source accuracy and investment judgment are not verified).")


if __name__ == "__main__":
    main()
