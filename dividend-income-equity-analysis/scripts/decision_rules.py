"""Auditable scoring and staged-entry checks; source truth remains a research task."""

import math


SCORE_BANDS = {
    "net_yield": (15, ((13, 15), (10, 12), (6, 9), (3, 5), (0, 2))),
    "dividend_stability": (15, ((12, 15), (8, 11), (4, 7), (0, 3))),
    "cash_coverage": (20, ((17, 20), (12, 16), (6, 11), (0, 5))),
    "balance_sheet": (15, ((12, 15), (8, 11), (4, 7), (0, 3))),
    "capital_allocation": (15, ((12, 15), (8, 11), (4, 7), (0, 3))),
    "buyback_quality": (10, ((8, 10), (5, 7), (2, 4), (0, 1))),
    "visibility": (10, ((8, 10), (5, 7), (2, 4), (0, 1))),
}
STAGES = ("starter", "add", "strong_buy")
SCENARIOS = ("Bear", "Base", "Bull")


def score_points(module, band, met_checks):
    if module not in SCORE_BANDS:
        raise ValueError(f"Unknown score module: {module}")
    bands = SCORE_BANDS[module][1]
    if not 1 <= band <= len(bands) or not 0 <= met_checks <= 3:
        raise ValueError("Invalid score band or refinement-check count")
    low, high = bands[band - 1]
    return low + (high - low) * met_checks // 3


def score_grade(score):
    if score is None:
        return None
    if not 0 <= score <= 100:
        raise ValueError("Combined score must be between 0 and 100")
    for floor, grade in ((85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "E")):
        if score >= floor:
            return grade


def metric_band(module, value):
    thresholds = {
        "net_yield": (.07, .05, .035, .02),
        "cash_coverage": (1.5, 1, .7),
    }
    if module not in thresholds or not math.isfinite(value):
        raise ValueError("A quantitative score needs a known module and a finite metric")
    floors = thresholds[module]
    return next((index for index, floor in enumerate(floors, 1) if value >= floor), len(floors) + 1)


def quality_rating(score):
    return "High" if score >= 68 else "Medium" if score >= 51 else "Low"


def point_from_range(interval):
    return interval["low"] if interval["low"] == interval["high"] else None


def buyback_rating(row):
    if row["assessment"] == "not_assessable":
        return "Unclear"
    bands = row["bounds"]["bands"] if row["assessment"] == "bounded" else [row["band"]]
    labels = {"Good" if band == 1 else "Neutral" if band == 2 else "Poor" for band in bands}
    return labels.pop() if len(labels) == 1 else "Unclear"


def module_cap(report, module):
    cap = SCORE_BANDS[module][0]
    row = next((row for row in report.get("scorecard", {}).get("modules", [])
                if row["module"] == module), {})
    basis = row.get("bounds", {}).get("metric_basis")
    if module == "net_yield":
        zone = report.get("buy_zone", {})
        if (report["forecast_confidence"] in ("Low", "Not Forecastable")
                or zone.get("normalized_net_dps_basis") == "historical_fundamental_fallback"
                or zone.get("bear_net_dps_is_fallback", False)
                or basis == "recurring_income_proxy"):
            cap = min(cap, 9)
        if report["dividend_safety"] == "Weak" or report["value_trap_veto"] == "Triggered":
            cap = min(cap, 5)
    if module == "cash_coverage" and basis == "reconciled_cash_proxy":
        cap = min(cap, 16)
    if module == "visibility":
        if (report["fundamental_trend"] == "Structural Decline"
                or any(row["dps_source"] == "illustrative"
                       for row in report["dividend_and_yield_runway"])):
            cap = min(cap, 4)
    return cap


def summarize_scorecard(report):
    """Rubric bounds at current caps, not probabilities or rescaled partial points."""
    modules = {row["module"]: row for row in report["scorecard"]["modules"]}
    if set(modules) != set(SCORE_BANDS) or len(report["scorecard"]["modules"]) != len(SCORE_BANDS):
        raise ValueError("A score summary needs each fixed module exactly once")
    ranges = {}
    exact_weight = bounded_weight = quality_weight = 0
    estimated = False
    for name, row in modules.items():
        weight = SCORE_BANDS[name][0]
        cap = module_cap(report, name)
        if row["assessment"] == "assessed":
            low = high = row["final_score"]
            exact_weight += weight
            estimated |= row.get("evidence_basis") == "estimated"
        elif row["assessment"] == "bounded":
            bands = row["bounds"]["bands"]
            met = sum(check["status"] == "met" for check in row["checks"])
            unknown = sum(check["status"] == "unknown" for check in row["checks"])
            low = min(min(score_points(name, band, met), cap) for band in bands)
            high = max(min(score_points(name, band, met + unknown), cap) for band in bands)
            bounded_weight += weight
        elif row["assessment"] == "not_assessable":
            low, high = 0, cap
        else:
            raise ValueError(f"Unknown module assessment: {row['assessment']}")
        ranges[name] = {"low": low, "high": high}
        if name != "net_yield" and row["assessment"] != "not_assessable":
            quality_weight += weight
    covered = exact_weight + bounded_weight
    quality = {edge: sum(row[edge] for name, row in ranges.items() if name != "net_yield")
               for edge in ("low", "high")}
    income = ranges["net_yield"]
    total = {edge: quality[edge] + income[edge] for edge in ("low", "high")}
    grade_cap = "C" if report["fundamental_trend"] == "Structural Decline" else "A"
    return {
        "status": ("insufficient" if covered == 0 else "complete"
                   if exact_weight == 100 and not estimated else "provisional"),
        "range_kind": "rubric_bounds",
        "module_ranges": ranges,
        "score_range": total,
        "quality_range": quality,
        "income_range": income,
        "grade_range": {
            "worst": max(score_grade(total["low"]), grade_cap),
            "best": max(score_grade(total["high"]), grade_cap),
        },
        "quality_rating_range": {
            "worst": quality_rating(quality["low"]),
            "best": quality_rating(quality["high"]),
        },
        "bounded_weight": bounded_weight,
        "missing_weight": 100 - covered,
        "evidence_coverage_pct": covered,
        "quality_coverage_pct": round(quality_weight / 85 * 100, 2),
        "income_coverage_pct": 0 if modules["net_yield"]["assessment"] == "not_assessable" else 100,
    }


def stage_prices(report):
    mode = report["valuation_mode"]
    if mode == "ordinary_yield_based":
        zone = report["buy_zone"]
        return (
            zone["normalized_net_dps"] / zone["required_net_yield_low"],
            zone["normalized_net_dps"] / zone["required_net_yield_high"],
            zone["bear_net_dps"] / zone["required_net_yield_high"],
        )
    if mode == "total_return_based":
        growth = report["growth_valuation"]
        starter = growth["base_case_value"] * (1 - growth["margin_of_safety"])
        return starter, min(starter, growth["growth_value_low"]), growth["entry_upper"]
    if mode == "finite_life_harvest":
        return report["finite_life_valuation"]["finite_life_value_low"], None, None
    if mode == "suspended":
        return None, None, None
    raise ValueError(f"Unknown valuation mode: {mode}")


def forward_funding_status(report, *, scenarios=SCENARIOS, include_recurring=False):
    bridges = {(row["forecast_year"], row["scenario"]): row for row in report["dividend_forecast_bridge"]}
    rows = [row for row in report["dividend_and_yield_runway"]
            if row["forecast_year"] <= 3 and row["scenario"] in scenarios]
    missing = len(rows) != 3 * len(scenarios)
    for row in rows:
        capacity, entitlement, cost = (row["cash_available_for_distribution"],
                                       row["dividend_entitlement"], row["dividend_cash_cost"])
        comparisons = [(entitlement, capacity), (cost, capacity)]
        if include_recurring:
            bridge = bridges.get((row["forecast_year"], row["scenario"]))
            comparisons.append((entitlement, bridge["recurring_fad"] if bridge else None))
        for claim, cash in comparisons:
            if claim is None or cash is None:
                missing = True
            elif claim > cash and not math.isclose(claim, cash, rel_tol=1e-6, abs_tol=1e-6):
                return False
    return None if missing else True


def validate_decision_framework(report, *, tax_supported, cash_supported, evidence_limitations):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def same(actual, expected, label):
        equal = (actual is expected if actual is None or expected is None
                 else math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-6))
        require(equal, f"{label}: expected {expected}, got {actual}")

    def refs(record, label):
        require(all(source in report["sources"] for source in record["source_refs"]),
                f"{label}: source_refs must identify declared report sources")

    card = report["scorecard"]
    provisional_rubric = card["rubric_version"] == "2"
    modules = {row["module"]: row for row in card["modules"]}
    require(set(modules) == set(SCORE_BANDS), "Scorecard must contain each fixed module exactly once")
    if len(modules) != len(SCORE_BANDS):
        return errors

    price = report["price_used"]
    zone = report.get("buy_zone")
    coverage = report["coverage_summary"]["three_year_recurring_coverage"]
    normalized_yield = zone["normalized_net_dps"] / price if zone and price else None
    normalization_supported = zone and all(
        record["status"] == "supported" for record in zone["normalization_evidence"].values()
    )
    if zone and price:
        same(report["key_metrics_at_a_glance"]["normalized_net_yield"], normalized_yield,
             "Key metrics normalized yield")
    for name, row in modules.items():
        weight, bands = SCORE_BANDS[name]
        require(row["weight"] == weight, f"{name}: weight must remain {weight}")
        refs(row, name)
        checks = {check["check"]: check for check in row["checks"]}
        require(set(checks) == {1, 2, 3}, f"{name}: each refinement check is required exactly once")
        for check in row["checks"]:
            refs(check, f"{name} check {check['check']}")
        if "adverse_evidence" in row:
            refs(row["adverse_evidence"], f"{name} adverse evidence")
            require(name == "visibility" and row["assessment"] == "assessed" and row["band"] == 4,
                    "The adverse-visibility record belongs to an assessed lowest-band visibility score")
        override = row.get("band_override")
        if override:
            require(name == "cash_coverage" and row["assessment"] in ("assessed", "bounded"),
                    "Only assessed cash coverage (or rubric-2 bounded coverage) permits a named funding/peak band override")
            refs(override, "Coverage band override")
        if row["assessment"] == "not_assessable":
            continue
        bounded = row["assessment"] == "bounded"
        if not bounded and not 1 <= row["band"] <= len(bands):
            require(False, f"{name}: invalid anchor band")
            continue
        if bounded:
            bounds = row["bounds"]
            refs(bounds, f"{name} bounds")
            candidates = bounds["bands"]
            valid_bands = all(1 <= band <= len(bands) for band in candidates)
            require(valid_bands, f"{name}: invalid bounded anchor bands")
            if not valid_bands:
                continue
            require(candidates == list(range(min(candidates), max(candidates) + 1)),
                    f"{name}: candidate bands must be ordered and contiguous")
            basis = bounds["metric_basis"]
            low, high = bounds["metric_low"], bounds["metric_high"]
            if name in ("net_yield", "cash_coverage"):
                valid_range = (low is not None and high is not None
                               and math.isfinite(low) and math.isfinite(high) and low <= high)
                require(valid_range, f"{name}: bounded metric needs finite, ordered endpoints")
                if valid_range:
                    expected = list(range(metric_band(name, high), metric_band(name, low) + 1))
                    if override:
                        worst = 3 if override["rule"] == "peak_cycle_only" else 4
                        expected = sorted({max(band, worst) for band in expected})
                    require(candidates == expected, f"{name}: bounded bands disagree with metric endpoints")
                if name == "net_yield":
                    require(basis in ("normalized_net_yield", "recurring_income_proxy"),
                            "Income bounds need a normalized or explicitly provisional recurring-income basis")
                    require(tax_supported and cash_supported and price is not None and price > 0,
                            "Income bounds still require supported tax/cash and current-price evidence")
                    if basis == "normalized_net_yield":
                        require(bool(normalization_supported) and normalized_yield is not None
                                and report["dividend_safety"] != "Unclear",
                                "Normalized income bounds require the normalization and safety bridge")
                        if valid_range and normalized_yield is not None:
                            require(low <= normalized_yield <= high,
                                    "Income bounds must include the supplied normalized yield")
                    elif basis == "recurring_income_proxy":
                        require(not (normalization_supported and normalized_yield is not None
                                     and report["dividend_safety"] != "Unclear"),
                                "Use supported normalization before a provisional income proxy")
                else:
                    require(basis in ("three_year_recurring_coverage", "reconciled_cash_proxy"),
                            "Coverage bounds need the aggregate or a reconciled cash proxy")
                    require(report["cash_flow_model"]["evidence_status"] != "insufficient",
                            "Coverage bounds cannot replace unresolved material cash/capital evidence")
                    if basis == "three_year_recurring_coverage":
                        require(coverage is not None, "Aggregate coverage bounds need a supported aggregate")
                        if valid_range and coverage is not None:
                            require(low <= coverage <= high,
                                    "Coverage bounds must include the supplied aggregate")
                    elif basis == "reconciled_cash_proxy":
                        require(coverage is None,
                                "Use the supported standard aggregate before a provisional coverage proxy")
            else:
                require(basis == "qualitative" and low is None and high is None,
                        f"{name}: qualitative bounds must not invent a numeric metric")
        metric = row["metric_value"]
        if name == "net_yield":
            if not bounded:
                require(normalized_yield is not None and normalization_supported and tax_supported and cash_supported
                        and report["dividend_safety"] != "Unclear",
                        "Income points require supported normalization, tax/cash and safety evidence")
                same(metric, normalized_yield, "Income score metric")
                if metric is not None:
                    require(math.isfinite(metric), "Income score metric must be finite")
                    if math.isfinite(metric):
                        require(row["band"] == metric_band(name, metric),
                                "Income score band disagrees with normalized yield")
            if zone and normalized_yield is not None and set(checks) == {1, 2, 3}:
                required_low = report["return_requirements"]["required_total_return_low"]
                expected_checks = {
                    1: (None if report["income_assessment"]["forward_net_dps"] is None
                        else report["income_assessment"]["forward_net_dps"] >= zone["normalized_net_dps"]),
                    2: zone["bear_net_dps"] / price >= zone["required_net_yield_high"],
                    3: None if required_low is None else normalized_yield >= required_low,
                }
                for number, result in expected_checks.items():
                    if result is None:
                        require(checks[number]["status"] == "unknown",
                                f"Income check {number}: missing input must remain unknown")
                    elif checks[number]["status"] != "unknown":
                        require((checks[number]["status"] == "met") == result,
                                f"Income check {number}: status contradicts the supplied cash/yield inputs")
            elif provisional_rubric:
                require(all(check["status"] == "unknown" for check in row["checks"]),
                        "Income checks without N/B must remain unknown; a proxy is not normalization")
        elif name == "cash_coverage":
            if not bounded:
                require(coverage is not None, "Coverage points require the normalized aggregate, not a TTM proxy")
                same(metric, coverage, "Coverage score metric")
                if coverage is not None:
                    require(math.isfinite(coverage), "Coverage score metric must be finite")
                if coverage is not None and math.isfinite(coverage):
                    expected_band = metric_band(name, coverage)
                    if override:
                        expected_band = max(expected_band, 3 if override["rule"] == "peak_cycle_only" else 4)
                    require(row["band"] == expected_band, "Coverage score band disagrees with aggregate coverage")
            history = sorted(report["cash_flow_bridge"], key=lambda item: item["fiscal_year_end"])[-5:]
            actual = [item["actual_cash_coverage"] for item in history]
            worst_actual_passes = (False if any(value is not None and value < 1 for value in actual)
                                   else True if len(actual) == 5 and all(value is not None for value in actual) else None)
            if set(checks) == {1, 2, 3}:
                for number, result in ((1, forward_funding_status(report, include_recurring=True)),
                                       (2, worst_actual_passes)):
                    if result is None:
                        require(checks[number]["status"] == "unknown",
                                f"Coverage check {number}: missing evidence must remain unknown")
                    elif checks[number]["status"] != "unknown":
                        require((checks[number]["status"] == "met") == result,
                                f"Coverage check {number} contradicts the supplied cash-funding record")
        else:
            require(metric is None, f"{name}: qualitative bands do not use an invented numeric metric")
        if provisional_rubric and name == "visibility" and not bounded and row["band"] == 4:
            require("adverse_evidence" in row,
                    "Lowest visibility band needs adverse issuer evidence, not an unfinished research model")
        if bounded:
            same(row["cap"], module_cap(report, name), f"{name} explicit cap")
            continue
        met = sum(check["status"] == "met" for check in row["checks"])
        raw = score_points(name, row["band"], met)
        cap = module_cap(report, name)
        same(row["raw_score"], raw, f"{name} raw points")
        same(row["cap"], cap, f"{name} explicit cap")
        same(row["final_score"], min(raw, cap), f"{name} final points")

    assessed = [row for row in modules.values() if row["final_score"] is not None]
    points = sum(row["final_score"] for row in assessed)
    same(card["assessed_points"], points, "Assessed points")
    same(card["assessed_weight"], sum(SCORE_BANDS[row["module"]][0] for row in assessed), "Assessed weight")
    quality_rows = [row for name, row in modules.items() if name != "net_yield"]
    quality = (sum(row["final_score"] for row in quality_rows)
               if all(row["final_score"] is not None for row in quality_rows) else None)
    income = modules["net_yield"]["final_score"]
    total = points if len(assessed) == 7 else None
    summary = summarize_scorecard(report) if provisional_rubric and not errors else None
    if summary is not None:
        quality = point_from_range(summary["quality_range"])
        income = point_from_range(summary["income_range"])
        total = point_from_range(summary["score_range"])
    same(card["quality_score_85"], quality, "Quality score /85")
    same(card["income_score_15"], income, "Income score /15")
    same(report["key_metrics_at_a_glance"]["quality_score_85"], quality, "Key metrics quality score")
    same(report["score_100"], total, "Combined score /100")
    if total is not None and total > 100:
        require(False, "Combined module points exceed 100")
        return errors
    raw_grade = score_grade(total)
    if summary is not None:
        require(card["summary"] == summary, "Score summary must reconcile ranges, caps, coverage and ratings")
        edges = summary["score_range"]
        raw_grade = score_grade(edges["low"]) if score_grade(edges["low"]) == score_grade(edges["high"]) else None
        headline = report["key_metrics_at_a_glance"]
        for field, expected in {
            "score_status": summary["status"], "score_range": summary["score_range"],
            "quality_score_range": summary["quality_range"],
            "score_coverage_pct": summary["evidence_coverage_pct"], "grade_range": summary["grade_range"],
        }.items():
            require(headline[field] == expected, f"Key metrics {field} disagrees with the score summary")
    require(card["unadjusted_grade"] == raw_grade, "Unadjusted Grade must follow the supported combined score bounds")
    grade_cap = "C" if report["fundamental_trend"] == "Structural Decline" else None
    require(card["grade_cap"] == grade_cap, "Only the documented Structural Decline Grade C cap applies")
    final_grade = max(raw_grade, grade_cap) if raw_grade and grade_cap else raw_grade
    if summary is not None:
        grades = summary["grade_range"]
        final_grade = grades["best"] if grades["best"] == grades["worst"] else None
    require(report["grade"] == final_grade, "Final Grade disagrees with the score and explicit cap")
    quality_label = "Unclear" if quality is None else quality_rating(quality)
    if summary is not None:
        labels = summary["quality_rating_range"]
        quality_label = labels["best"] if labels["best"] == labels["worst"] else "Unclear"
    require(report["dividend_quality"] == quality_label, "Dividend Quality must follow the price-independent /85 score")

    for field, record in report["rating_audit"].items():
        require(record["label"] == report[field], f"{field}: rating audit label disagrees with the report")
        refs(record, field)
    expected_tax_rating = ("Unclear" if not tax_supported else "High" if report["withholding_rate"] <= .1
                           else "Medium" if report["withholding_rate"] <= .2 else "Low")
    require(report["withholding_efficiency"] == expected_tax_rating,
            "Withholding Efficiency disagrees with the supported tax rate")
    if report["value_trap_veto"] != "Not triggered":
        require(report["portfolio_role"] != "Core income", "An unresolved or triggered veto prevents Core income")
    buyback = modules["buyback_quality"]
    if report["buyback_quality"] != "Not Applicable" and (
            provisional_rubric or buyback["assessment"] == "assessed"):
        expected = buyback_rating(buyback)
        require(report["buyback_quality"] == expected, "Buyback Quality disagrees with the evidenced score band")

    plan = report["entry_plan"]
    risk = plan["risk_review"]
    refs(risk, "Entry risk review")
    scenarios = {row["scenario"]: row for row in plan["return_scenarios"]}
    require(set(scenarios) == set(SCENARIOS), "Entry return scenarios must include Bear/Base/Bull exactly once")
    complete_returns = True
    horizons = set()
    for row in plan["return_scenarios"]:
        refs(row, f"Entry {row['scenario']} return")
        if row["horizon_years"] is not None:
            horizons.add(row["horizon_years"])
        fields = (row["horizon_years"], row["net_cash_received"], row["exit_price"], row["costs"], price)
        known = all(value is not None for value in fields)
        complete_returns = complete_returns and known
        if known:
            require(bool(row["source_refs"]), "Calculated holding returns need source references and an exit basis")
            expected = (row["net_cash_received"] + row["exit_price"] - row["costs"] - price) / price
        else:
            expected = None
        same(row["cumulative_return"], expected, f"{row['scenario']} cumulative holding return")
    require(len(horizons) <= 1, "Entry return scenarios must use the same holding horizon")
    if risk["status"] == "pass":
        require(complete_returns and len(scenarios) == 3, "Entry risk pass requires quantified Bear/Base/Bull holding returns")

    for blocker in plan["blockers"]:
        refs(blocker, "Entry blocker")
    mode = report["valuation_mode"]
    income = report["income_assessment"]
    hard = income["target"]["target_policy"] == "hard_minimum"
    income_unknown = hard and income["income_eligible"] is None
    hard_failed = hard and income["income_eligible"] is not True
    ordinary_funded = mode != "ordinary_yield_based" or forward_funding_status(
        report, scenarios=("Bear", "Base")
    ) is True
    if not ordinary_funded:
        require(report["action_assessment"]["status"] != "eligible",
                "Unfunded or unknown ordinary Bear/Base cash cannot support eligible entry")
    evidence_ready = not evidence_limitations and ordinary_funded and mode != "suspended" and risk["status"] == "pass"
    action_gate_ready = evidence_ready and not hard_failed
    if mode != "suspended":
        require((report["action_assessment"]["status"] == "eligible") == action_gate_ready,
                "Action eligibility must reflect named evidence, risk and income gates, not generic caution")

    stages = {row["stage"]: row for row in plan["stages"]}
    require(set(stages) == set(STAGES), "Entry plan must contain starter/add/strong_buy exactly once")
    if len(stages) != 3:
        return errors
    strong_profile = (report["forecast_confidence"] == "High" and report["dividend_safety"] == "Strong"
                      and mode in ("ordinary_yield_based", "total_return_based"))
    expected_states = {}
    for stage, valuation_price in zip(STAGES, stage_prices(report)):
        row = stages[stage]
        effective = valuation_price
        if hard and valuation_price is not None:
            if income_unknown:
                effective = None
            elif income["income_price_ceiling"] is not None:
                effective = min(valuation_price, income["income_price_ceiling"])
        same(row["valuation_price"], valuation_price, f"{stage} valuation price")
        same(row["effective_price"], effective, f"{stage} income-capped price")
        gap = (effective / price - 1) * 100 if effective is not None and price is not None else None
        same(row["gap_to_current_pct"], gap, f"{stage} signed price distance")
        if valuation_price is None or valuation_price <= 0 or risk["status"] == "fail":
            state = "unavailable"
        elif (not evidence_ready or effective is None or price is None
              or (stage == "strong_buy" and not strong_profile)):
            state = "waiting_evidence"
        else:
            state = "ready" if price <= effective else "waiting_price"
        expected_states[stage] = state
        require(row["status"] == state, f"{stage}: readiness must be {state}, not {row['status']}")

    avoid = (report["value_trap_veto"] == "Triggered" or report["dividend_safety"] == "Weak"
             or risk["status"] == "fail"
             or (report["fundamental_trend"] == "Structural Decline" and mode != "finite_life_harvest"))
    if avoid:
        expected_action = "avoid"
    elif expected_states["starter"] == "waiting_price":
        expected_action = "wait_for_price"
    elif expected_states["starter"] != "ready":
        expected_action = "wait_for_evidence"
    elif expected_states["strong_buy"] == "ready":
        expected_action = "strong_buy"
    elif (expected_states["add"] == "ready" and report["forecast_confidence"] == "High"
          and mode in ("ordinary_yield_based", "total_return_based")):
        expected_action = "buy"
    else:
        expected_action = "accumulate"
    require(plan["current_action"] == expected_action,
            f"Current action must be {expected_action}, not {plan['current_action']}")
    require(report["key_metrics_at_a_glance"]["current_action"] == plan["current_action"],
            "Key metrics action disagrees with the entry plan")
    require(report["action_assessment"]["strong_buy_eligible"] == (expected_action == "strong_buy"),
            "Strong Buy eligibility disagrees with price, confidence and entry gates")
    scopes = {row["scope"] for row in plan["blockers"]}
    if expected_action == "wait_for_price":
        require(bool(scopes & {"price", "income"}), "Waiting for price needs a price/income blocker and resolution")
    if expected_action == "wait_for_evidence":
        require(bool(scopes & {"evidence", "confidence", "income"}),
                "Waiting for evidence needs a material evidence/confidence/income blocker")
    if expected_action == "avoid":
        require("fundamentals" in scopes, "Avoid needs a documented fundamental/risk blocker, not a hidden downgrade")
    return errors
