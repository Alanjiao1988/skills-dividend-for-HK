"""Cross-field checks for local analytical records; never rewrite an input report."""

import math
from datetime import date
from statistics import median


QUALITY_WEIGHTS = {
    "dividend_stability": 15, "cash_coverage": 20, "balance_sheet": 15,
    "capital_allocation": 15, "buyback_quality": 10, "visibility": 10,
}
SUPPORTED_TAX = ("broker_observed", "company_announcement", "legal_structure")


def _checks():
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def same(actual, expected, label):
        equal = (actual is expected if actual is None or expected is None else
                 math.isclose(actual, expected, rel_tol=1e-6, abs_tol=1e-6))
        require(equal, f"{label}: expected {expected}, got {actual}")

    return errors, require, same


def _controller(report, require):
    risk = report.get("controller_risk")
    if risk is None:
        return False
    require(risk["assessed_on"] <= report["as_of_date"],
            "Controller assessment cannot postdate the analysis")
    harm = risk["material_harm_confirmed"] is True
    if harm:
        require(risk["status"] == "triggered" and risk["materiality"] == "material",
                "Confirmed material controller harm requires a triggered material risk")
    if risk["status"] == "triggered":
        require(harm and risk["materiality"] == "material"
                and bool(risk["cash_demand_evidence"]) and bool(risk["channels"]),
                "Triggered controller risk needs confirmed material harm and its evidenced channel")
    if risk["status"] == "no_material_concern":
        require(risk["materiality"] == "not_material" and risk["material_harm_confirmed"] is False,
                "No material controller concern cannot stand for unknown or confirmed harm")
    if risk["status"] == "not_assessed":
        require(risk["materiality"] == "unknown" and risk["material_harm_confirmed"] is None,
                "Unassessed controller risk must retain unknown materiality and harm")
    return harm or risk["status"] == "triggered"


def validate_safety_review(report):
    errors, require, same = _checks()
    review = report["review"]
    metrics = review["metrics"]
    after = {name: record["after"] for name, record in metrics.items()}
    require(review["event_date"] <= report["as_of_date"],
            "Safety Review event cannot postdate the analysis")
    previous = review["previous_review_date"]
    if previous is not None:
        require(previous <= review["event_date"], "Safety Review dates are reversed")
    require((previous is None) == (review["previous_reference"] is None),
            "Safety Review comparison needs both the prior date and reference")
    cash, entitlement = after["cash_dividends"], review["full_cash_entitlement"]
    for name, value in (("cash dividends", cash), ("all-cash entitlement", entitlement)):
        require(value is None or value >= 0, f"Safety Review {name} cannot be negative")
    if cash is not None and entitlement is not None:
        require(entitlement >= cash, "Safety Review all-cash entitlement cannot understate settled dividends")
    cash_units = {metrics[name]["unit"] for name in
                  ("recurring_fad", "cash_dividends", "actual_capacity")}
    require(len(cash_units) == 1, "Safety Review cash coverage needs matching units and period")

    def ratio(numerator, denominator):
        return None if numerator is None or denominator is None or denominator <= 0 else numerator / denominator

    def gap(claim, capacity):
        return None if claim is None or capacity is None else max(0, claim - capacity)

    same(review["recurring_coverage"], ratio(after["recurring_fad"], cash), "Safety Review recurring coverage")
    same(review["actual_coverage"], ratio(after["actual_capacity"], cash), "Safety Review actual coverage")
    same(review["recurring_entitlement_coverage"], ratio(after["recurring_fad"], entitlement),
         "Safety Review recurring entitlement coverage")
    same(review["funding_gap"], gap(cash, after["actual_capacity"]), "Safety Review funding gap")
    same(review["all_cash_funding_gap"], gap(entitlement, after["actual_capacity"]),
         "Safety Review all-cash funding gap")
    missing = any(value is None for value in after.values()) or entitlement is None
    unsupported = review["cash_evidence_status"] == "insufficient"
    if previous is None or any(row["before"] is None for row in metrics.values()):
        require(review["decision"] == "not_comparable",
                "Safety Review missing prior baseline must remain not_comparable")
    negative_capital = any(after[name] is not None and after[name] < 0
                           for name in ("liquidity", "capital_headroom"))
    funding_deficit = any(review[name] is not None and review[name] > 0
                          for name in ("funding_gap", "all_cash_funding_gap"))
    recurring_deficit = (after["recurring_fad"] is not None and entitlement is not None
                         and entitlement > after["recurring_fad"])
    controller_harm = _controller(report, require)
    adverse = negative_capital or funding_deficit or recurring_deficit or controller_harm
    evidenced_adverse = negative_capital or controller_harm or (
        not unsupported and (funding_deficit or recurring_deficit))
    if missing or unsupported:
        require(bool(review["missing_inputs"]), "Safety Review incomplete cash/capital evidence needs missing_inputs")
        require(review["dividend_safety"] in ("Weak", "Unclear") if evidenced_adverse
                else review["dividend_safety"] == "Unclear",
                "Safety Review missing evidence alone requires Unclear, not an adverse safety rating")
        if not evidenced_adverse:
            require(review["decision"] == "not_comparable",
                    "Safety Review material current uncertainty without reliable adverse evidence is not_comparable")
        else:
            require(review["decision"] in ("weakened", "not_comparable"),
                    "Safety Review incomplete evidence cannot maintain or strengthen safety")
    if adverse:
        require(review["dividend_safety"] in ("Weak", "Unclear"),
                "Safety Review cash funding/capital/controller deficit cannot be Strong or Acceptable")
        require(review["decision"] not in ("maintained", "strengthened"),
                "Safety Review a material funding/capital deficit cannot maintain or strengthen safety")
    if controller_harm:
        require(review["veto_status"] == "Triggered", "Safety Review controller harm requires a triggered veto")
    if missing or unsupported or adverse or review["structural_change"] or review["veto_status"] != "Not triggered":
        require(review["requires_full_analysis"] and bool(review["escalation_reasons"]),
                "Safety Review material cash/capital uncertainty or structural/veto change requires explained escalation")
    if review["requires_full_analysis"]:
        require(bool(review["escalation_reasons"]), "Safety Review escalation needs a reason")
    elif review["escalation_reasons"]:
        require(False, "Safety Review escalation reasons cannot contradict requires_full_analysis")
    return errors


def validate_cash_events(report):
    errors, require, same = _checks()
    runway = report["dividend_and_yield_runway"]
    mixed = report["scrip_drip"]["investor_cash_yield_assumption"] == "cash_components_only"
    complete = True
    any_cash = False
    for scenario in ("Bear", "Base", "Bull"):
        issuer_start = None
        pending = []
        seen = set()
        for row in sorted((row for row in runway if row["scenario"] == scenario),
                          key=lambda row: row["forecast_year"]):
            events = row["dividend_installments"]
            audited = bool(events) and all("distribution_type" in event for event in events)
            if any("distribution_type" in event for event in events):
                require(audited, "Local cash events cannot mix audited and unaudited distributions")
            if not audited:
                complete = False
                if "investor_cash_dps" in row:
                    same(row["investor_cash_dps"], row["derived_dps"],
                         "Investor cash DPS without a dated event ledger")
                continue
            issuer_dps = investor_dps = 0
            calculable = True
            for event in events:
                when = event["record_date"]
                require(when not in seen, "Local cash events need unique record dates within each scenario")
                seen.add(when)
                kind = event["distribution_type"]
                if issuer_start is None:
                    issuer_start = event["dividend_entitled_shares"] - event["other_share_change"]
                matured = [item for item in pending if item["date"] <= when]
                expected_shares = issuer_start + sum(item["shares"] for item in matured)
                expected_shares += event["other_share_change"]
                same(event["dividend_entitled_shares"], expected_shares, "Dated issuer share reconciliation")
                issuer_start += event["other_share_change"]
                expected_factor = 1 + sum(item["investor_shares"] for item in matured)
                same(event["investor_share_factor"], expected_factor, "Dated investor share reconciliation")
                if kind == "mandatory_stock":
                    require(not event["cash_election_confirmed"],
                            "Mandatory-stock event cannot claim a cash election")
                    require(all(event[field] == 0 for field in
                                ("dividend_entitlement", "dividend_cash_cost", "derived_dps",
                                 "settlement_cash_adjustment")),
                            "Mandatory-stock event must be excluded from cash dividends and DPS")
                else:
                    require(event["cash_election_confirmed"],
                            "Cash/optional-scrip events need event-specific investor cash access")
                    if kind == "cash_dividend":
                        require(event["stock_shares_issued"] == 0 and event["investor_stock_ratio"] == 0,
                                "Cash-only event cannot silently issue stock")
                    else:
                        require(event["investor_stock_ratio"] == 0,
                                "Cash-election income cannot also count voluntary scrip shares")
                    any_cash |= event["investor_entitled"] and (event["derived_dps"] or 0) > 0
                if event["stock_shares_issued"] > 0 or event["investor_stock_ratio"] > 0:
                    require(event["shares_eligible_from"] is not None and event["shares_eligible_from"] > when,
                            "New stock must have a later documented dividend-entitlement date")
                    if event["shares_eligible_from"] is not None:
                        investor_shares = (event["investor_share_factor"] * event["investor_stock_ratio"]
                                           if event["investor_entitled"] else 0)
                        pending.append({"date": event["shares_eligible_from"],
                                        "shares": event["stock_shares_issued"], "investor_shares": investor_shares})
                else:
                    require(event["shares_eligible_from"] is None,
                            "An event without new shares cannot invent a stock-entitlement date")
                if event["derived_dps"] is None:
                    calculable = False
                else:
                    issuer_dps += event["derived_dps"]
                    if event["investor_entitled"]:
                        investor_dps += event["derived_dps"] * event["investor_share_factor"]
            if calculable:
                same(row["derived_dps"], issuer_dps, "Audited annual issuer cash DPS")
                require("investor_cash_dps" in row, "Audited cash events need explicit investor_cash_dps")
                if "investor_cash_dps" in row:
                    same(row["investor_cash_dps"], investor_dps, "Audited annual investor cash DPS")
            else:
                require(row.get("investor_cash_dps") is None,
                        "Incomplete event cash cannot produce investor cash DPS")
        growth = next((row for row in report.get("growth_valuation", {}).get("scenarios", [])
                       if row["scenario"] == scenario), None)
        if growth:
            supports = [cash["transition_support"] for cash in growth["forecast_cash_flows"]
                        if cash["forecast_year"] > 5]
            supports.append(growth["terminal_funding"])
            for support in supports:
                fields = ("record_date", "investor_share_factor", "other_share_change", "share_change_source")
                if pending or any(field in support for field in fields):
                    require(all(field in support for field in fields),
                            "Growth share adjustments require a dated investor/issuer share audit")
                    if not all(field in support for field in fields):
                        continue
                    when = support["record_date"]
                    require(not seen or when > max(seen),
                            "Growth transition/terminal share record must follow explicit cash events")
                    require(issuer_start is not None,
                            "Growth share-factor adjustments require an explicit event-ledger baseline")
                    if issuer_start is not None:
                        matured = [item for item in pending if item["date"] <= when]
                        same(support["investor_share_factor"],
                             1 + sum(item["investor_shares"] for item in matured),
                             "Growth dated investor share factor")
                        expected_shares = issuer_start + sum(item["shares"] for item in matured)
                        expected_shares += support["other_share_change"]
                        same(support["dividend_entitled_shares"], expected_shares,
                             "Growth dated issuer shares")
                        issuer_start += support["other_share_change"]
                    seen.add(when)
    if mixed:
        require(complete, "cash_components_only requires complete dated cash/stock event ledgers")
    return errors, mixed and complete and any_cash and not errors


def investor_cash_dps(support, units):
    if "investor_cash_dps" in support:
        return support["investor_cash_dps"]
    if "derived_dps" in support:
        return support["derived_dps"]
    amount, shares = support["dividend_entitlement"], support["dividend_entitled_shares"]
    if amount is None or shares is None:
        return None
    return amount * units / shares * support.get("investor_share_factor", 1)


def validate_local_analysis(report):
    errors, require, same = _checks()
    limitations = []
    quality = report.get("quality_assessment")
    current = report.get("schema_version") in ("2.5", "3.0")
    controller_harm = _controller(report, require)
    risk = report.get("controller_risk")
    if risk:
        if controller_harm:
            require(report["value_trap_veto"] == "Triggered",
                    "Confirmed material controller harm requires the full-analysis veto")
            limitations.append("Material controller harm blocks eligible entry")
        elif risk["materiality"] == "unknown" or risk["status"] == "not_assessed":
            limitations.append("Unresolved controller materiality blocks eligible entry")

    if quality:
        if current and "scorecard" in report:
            card = report["scorecard"]
            summary = card["summary"]
            modules = {row["module"]: row for row in card["modules"] if row["module"] != "net_yield"}
            if set(modules) == set(QUALITY_WEIGHTS):
                expected_status = (
                    "assessed" if all(row["assessment"] == "assessed"
                                      and row.get("evidence_basis") != "estimated" for row in modules.values())
                    else "not_assessed" if all(row["assessment"] == "not_assessable" for row in modules.values())
                    else "provisional"
                )
                require(quality["status"] == expected_status,
                        "Local quality status must expose bounded, missing or estimated quality evidence")
                for name in QUALITY_WEIGHTS:
                    interval = summary["module_ranges"][name]
                    require(quality["component_ranges"][name] == interval,
                            f"Local quality {name} range disagrees with the rubric")
                    point = interval["low"] if interval["low"] == interval["high"] else None
                    same(quality["components"][name], point, f"Local quality {name} point")
                require(quality["score_range"] == summary["quality_range"],
                        "Local quality range disagrees with the six unscaled rubric modules")
                same(quality["coverage_pct"], summary["quality_coverage_pct"], "Local quality evidence coverage")
                same(quality["score_85"], card["quality_score_85"], "Local quality /85")
        else:
            components = quality["components"]
            known = all(value is not None for value in components.values())
            require((quality["status"] == "assessed") == known,
                    "Legacy local quality assessment needs all six components or not_assessed")
            same(quality["score_85"], sum(components.values()) if known else None, "Legacy local quality /85")
        same(report["key_metrics_at_a_glance"]["quality_score_85"], quality["score_85"],
             "Local quality / key metrics")
        if report["portfolio_role"] == "Core income":
            supported_quality = quality["coverage_pct"] > 0 if current else quality["status"] == "assessed"
            require(supported_quality and report["dividend_safety"] in ("Strong", "Acceptable")
                    and report["forecast_confidence"] in ("High", "Medium")
                    and report["value_trap_veto"] == "Not triggered" and not controller_harm,
                    "Core income requires supported quality evidence, Strong/Acceptable safety and no unresolved veto")

    zone = report.get("buy_zone")
    normalization = zone.get("normalization_model") if zone else None
    tax_supported = report["withholding_rate"] is not None and report["withholding_basis"] in SUPPORTED_TAX
    if normalization:
        assessed = normalization["status"] == "assessed"
        states = normalization["cycle_states"]
        start, end = normalization["period_start"], normalization["period_end"]
        if assessed:
            require(normalization["method"] != "not_assessed" and start is not None and end is not None
                    and bool(normalization["series_sources"]) and bool(normalization["drivers"])
                    and states["mid"]["status"] == "estimated",
                    "Assessed normalization needs dated sourced drivers and an estimated operating mid-state")
            require(normalization["cycle_applicability"] != "unclear",
                    "Assessed normalization cannot leave cycle applicability unclear")
        else:
            require(normalization["method"] == "not_assessed",
                    "Unassessed normalization cannot name a completed normalization method")
            require(all(row["status"] != "estimated" for row in states.values()),
                    "Unassessed normalization cannot emit estimated operating states")
            limitations.append("Unassessed local normalization blocks eligible entry")
            if "scorecard" in report:
                module = next((row for row in report["scorecard"]["modules"]
                               if row["module"] == "net_yield"), None)
                if module:
                    require(module["assessment"] == "not_assessable"
                            or (module["assessment"] == "bounded"
                                and module["bounds"]["metric_basis"] == "recurring_income_proxy"),
                            "Unassessed local normalization cannot produce normalized-income point scores")
        if start is not None and end is not None:
            require(start <= end <= report["as_of_date"], "Normalization reference dates are reversed or forward-looking")
        if normalization["cycle_applicability"] == "cyclical":
            require(all(row["status"] != "not_applicable" for row in states.values()),
                    "Cyclical normalization extremes are estimated or not_estimable, never not_applicable")
            if assessed:
                require(normalization["method"] in ("cycle_distribution", "supply_demand_balance"),
                        "Cyclical normalization requires a documented cycle/balance method")
        full_cycle = (normalization["method"] == "cycle_distribution"
                      or zone["normalized_net_dps_basis"] == "full_cycle_median")
        if assessed and full_cycle:
            require(normalization["cycle_length_years"] is not None,
                    "Full-cycle normalization requires an evidenced cycle length")
            if start and end and normalization["cycle_length_years"]:
                years = (date.fromisoformat(end) - date.fromisoformat(start)).days / 365.25
                require(years + 0.01 >= normalization["cycle_length_years"],
                        "Full-cycle normalization reference window must cover the evidenced cycle")
        for driver in normalization["drivers"]:
            require(driver["series_start"] <= driver["series_end"] <= report["as_of_date"],
                    "Normalization driver dates are reversed or forward-looking")
            if driver["selection"] == "median":
                require(bool(driver["observations"]), "Normalization median requires the complete observed series")
                if driver["observations"]:
                    same(driver["selected_value"], median(driver["observations"]), "Normalization observed median")
        units = report["cash_flow_model"]["cash_unit_scale"] / report["cash_flow_model"]["share_unit_scale"]
        numeric = ("owner_cash", "growth_uses", "mandatory_uses", "recurring_fad", "earnings", "payout_base",
                   "payout_ratio", "dividend_entitlement", "shares", "gross_dps")
        for label, state in states.items():
            if state["status"] != "estimated":
                require(all(state[field] is None for field in numeric),
                        f"Normalization {label}: unavailable state cannot emit precise financial inputs")
                continue
            fields = ("owner_cash", "growth_uses", "mandatory_uses", "recurring_fad",
                      "payout_base", "dividend_entitlement", "shares", "gross_dps")
            require(all(state[field] is not None for field in fields),
                    f"Normalization {label}: estimated state needs a complete cash/payout/share bridge")
            if any(state[field] is None for field in fields):
                continue
            fad = state["owner_cash"] - state["growth_uses"] - state["mandatory_uses"]
            same(state["recurring_fad"], fad, f"Normalization {label} recurring FAD")
            basis, base, payout = state["payout_basis"], state["payout_base"], state["payout_ratio"]
            policy_dividend = None
            if basis in ("earnings", "recurring_fad", "stated_cash_flow"):
                require(payout is not None, f"Normalization {label}: ratio policy needs a payout ratio")
                if basis in ("earnings", "recurring_fad"):
                    same(base, state["earnings" if basis == "earnings" else "recurring_fad"],
                         f"Normalization {label} payout base")
                if payout is not None:
                    policy_dividend = max(0, base * payout)
            elif basis == "fixed_dps":
                policy_dividend = base * state["shares"] / units
            else:
                policy_dividend = base
            if policy_dividend is not None and not math.isclose(
                    state["dividend_entitlement"], policy_dividend, rel_tol=1e-6, abs_tol=1e-6):
                require(state["dividend_entitlement"] < policy_dividend,
                        f"Normalization {label}: entitlement cannot exceed the documented policy dividend")
                citations = set(report["sources"]) | set(normalization["series_sources"])
                citations.update(driver["source"] for driver in normalization["drivers"])
                require(bool(state["evidence"].strip()) and state["evidence"].strip() not in citations,
                        f"Normalization {label}: reduced payout needs an explicit adjustment explanation beyond a source citation")
            same(state["gross_dps"], state["dividend_entitlement"] * units / state["shares"],
                 f"Normalization {label} gross DPS")
            require(state["dividend_entitlement"] <= max(0, fad),
                    f"Normalization {label}: unfunded recurring dividend cannot establish normalized income")
            if label == "mid" and state["dividend_entitlement"] > fad:
                limitations.append("Unfunded central normalization blocks eligible entry")
        low, high = normalization["uncertainty_low"], normalization["uncertainty_high"]
        require((low is None) == (high is None), "Normalization uncertainty needs both endpoints or neither")
        if low is not None and high is not None:
            require(low <= zone["normalized_net_dps"] <= high,
                    "Normalization uncertainty must be ordered and contain N; it is not a low/high cycle band")
        mid = states["mid"]
        if assessed and mid["gross_dps"] is not None and tax_supported:
            returns = report["return_requirements"]
            net = (mid["gross_dps"] * (1 - report["withholding_rate"]) * zone["normalization_fx_rate"]
                   * returns["shares_per_quoted_security"] - zone["normalization_cash_deductions"])
            same(zone["normalized_net_dps"], net / returns["valuation_unit_scale"],
                 "Normalization operating mid-state net DPS")

    real = report.get("real_income")
    if real:
        fields = ("period_start", "period_end", "starting_net_cash", "ending_net_cash",
                  "starting_price_index", "ending_price_index", "nominal_cagr", "inflation_cagr", "real_cagr")
        if real["status"] == "assessed":
            require(real["currency"] is not None and all(real[field] is not None for field in fields),
                    "Assessed real income requires matching dated cash and price-index observations")
        years = None
        if real["period_end"] is not None:
            require(real["period_end"] <= report["as_of_date"], "Real-income period cannot postdate analysis")
        if real["period_start"] is not None and real["period_end"] is not None:
            start, end = date.fromisoformat(real["period_start"]), date.fromisoformat(real["period_end"])
            years = (end - start).days / 365.25
            require(years > 0, "Real-income period must be positive")
        nominal = inflation = growth = None
        if years is not None and years > 0:
            if (real["starting_net_cash"] is not None and real["starting_net_cash"] > 0
                    and real["ending_net_cash"] is not None):
                nominal = (real["ending_net_cash"] / real["starting_net_cash"]) ** (1 / years) - 1
            if real["starting_price_index"] is not None and real["ending_price_index"] is not None:
                inflation = (real["ending_price_index"] / real["starting_price_index"]) ** (1 / years) - 1
        if nominal is not None and inflation is not None:
            growth = (1 + nominal) / (1 + inflation) - 1
        same(real["nominal_cagr"], nominal, "Real-income nominal CAGR")
        same(real["inflation_cagr"], inflation, "Real-income inflation CAGR")
        same(real["real_cagr"], growth, "Real-income purchasing-power CAGR")
        if growth is None:
            require(real["status"] == "not_assessed" and real["trend"] == "Not Assessed",
                    "Unassessed real income cannot fabricate a CPI or purchasing-power trend")
        else:
            require(real["status"] == "assessed",
                    "Complete real-income observations must expose their calculated purchasing-power assessment")
            trend = ("Growing" if growth > real["flat_tolerance"] else
                     "Eroding" if growth < -real["flat_tolerance"] else "Flat")
            require(real["trend"] == trend, "Real-income trend disagrees with real CAGR and flat tolerance")

    fx = report.get("fx_risk")
    if fx:
        if fx["status"] == "not_material":
            require(fx["material_exposure"] is False,
                    "FX not_material needs an evidenced absence of material exposure, not unknown")
        elif fx["status"] == "not_assessed":
            require(fx["material_exposure"] is None and not fx["stress_rows"],
                    "Unassessed FX cannot imply no material exposure or calculated stresses")
        else:
            require(fx["material_exposure"] is not None and bool(fx["operating_currencies"])
                    and fx["distribution_currency"] is not None and fx["investor_currency"] is not None,
                    "Assessed FX requires economic exposure and cash-currency identification")
            if fx["material_exposure"]:
                require(bool(fx["stress_rows"]),
                        "Material FX exposure requires both FX-only and combined-Bear cash stresses")
                for year in {row["forecast_year"] for row in fx["stress_rows"]}:
                    kinds = {row["kind"] for row in fx["stress_rows"] if row["forecast_year"] == year}
                    require(kinds == {"fx_only", "combined_bear"},
                            f"Material FX exposure year {year} needs paired FX-only and combined-Bear cash stresses")
        rows = {(row["forecast_year"], row["scenario"]): row for row in report["dividend_and_yield_runway"]}
        keys = [(row["forecast_year"], row["kind"]) for row in fx["stress_rows"]]
        require(len(keys) == len(set(keys)), "Duplicate FX stress year/kind")
        for stress in fx["stress_rows"]:
            year, kind = stress["forecast_year"], stress["kind"]
            base = rows.get((year, "Base"))
            operating = rows.get((year, "Bear" if kind == "combined_bear" else "Base"))
            if base is not None and operating is not None:
                same(stress["base_gross_dps"], base.get("investor_cash_dps", base["derived_dps"]),
                     "FX base cash DPS / runway")
                same(stress["operating_gross_dps"], operating.get("investor_cash_dps", operating["derived_dps"]),
                     "FX operating cash DPS / runway")
            if stress["economic_fx_in_runway"]:
                same(stress["economic_gross_dps_delta"], 0, "FX economic effect already in runway")
            require(tax_supported, "FX net-cash stress requires supported withholding")
            if tax_supported:
                returns = report["return_requirements"]
                scale, shares = returns["valuation_unit_scale"], returns["shares_per_quoted_security"]
                factor = (1 - report["withholding_rate"]) * shares
                base_cash = (stress["base_gross_dps"] * factor * stress["base_fx"] - stress["investor_fees"]) / scale
                gross = stress["operating_gross_dps"] + stress["economic_gross_dps_delta"]
                require(gross >= 0, "FX stress cannot imply negative cash DPS")
                stressed = (gross * factor * stress["stressed_fx"] + stress["hedge_cash_adjustment"]
                            - stress["investor_fees"]) / scale
                same(stress["base_net_cash"], base_cash, "FX base net cash")
                same(stress["stressed_net_cash"], stressed, "FX stressed net cash")
                same(stress["delta_cash"], stressed - base_cash, "FX cash delta")
        if fx["material_exposure"] is None or (fx["material_exposure"] and not fx["stress_rows"]):
            limitations.append("Unresolved material FX cash exposure blocks eligible entry")

    income = report["income_assessment"]
    forward_fields = ("forecast_year", "forward_fx_rate", "forward_cash_deductions")
    if any(field in income for field in forward_fields):
        require(all(field in income for field in forward_fields), "Local forward-income bridge needs year, FX and cash deductions")
        if all(field in income for field in forward_fields) and tax_supported:
            row = next((row for row in report["dividend_and_yield_runway"]
                        if row["forecast_year"] == income["forecast_year"] and row["scenario"] == "Base"), None)
            if row:
                gross = row.get("investor_cash_dps", row["derived_dps"])
                if gross is not None:
                    returns = report["return_requirements"]
                    expected = (gross * (1 - report["withholding_rate"]) * income["forward_fx_rate"]
                                * returns["shares_per_quoted_security"] - income["forward_cash_deductions"])
                    same(income["forward_net_dps"], expected / returns["valuation_unit_scale"],
                         "Local forward net cash bridge")
    spread = income.get("required_yield_spread")
    if spread is not None:
        returns = report["return_requirements"]
        ready = zone is not None and report["price_used"] is not None and returns["status"] == "assessed"
        require(ready, "Required-yield spread needs N, a quote and independently assessed returns")
        if ready:
            net_yield = zone["normalized_net_dps"] / report["price_used"]
            same(spread["normalized_net_yield"], net_yield, "Local normalized yield spread")
            same(spread["vs_low_pp"], (net_yield - zone["required_net_yield_low"]) * 100,
                 "Local yield spread vs low")
            same(spread["vs_high_pp"], (net_yield - zone["required_net_yield_high"]) * 100,
                 "Local yield spread vs high")
    return errors, limitations
