"""Synthetic positive-entry and transparent-rating regressions, not backtests."""

import copy
import unittest

from scripts.decision_rules import SCORE_BANDS, module_cap, score_grade, score_points, stage_prices
from scripts.validate_analysis import ordinary_boundaries, validate_report
from test_analysis_contract import EVIDENCE, full_report, refresh_growth_pv
from test_income_audit import screen_report


def refresh_score_totals(report):
    card = report["scorecard"]
    rows = card["modules"]
    for row in rows:
        if row["assessment"] == "assessed":
            count = sum(check["status"] == "met" for check in row["checks"])
            row["raw_score"] = score_points(row["module"], row["band"], count)
            row["cap"] = module_cap(report, row["module"])
            row["final_score"] = min(row["raw_score"], row["cap"])
    quality = [row["final_score"] for row in rows if row["module"] != "net_yield"]
    card["quality_score_85"] = sum(quality) if None not in quality else None
    card["income_score_15"] = next(row["final_score"] for row in rows if row["module"] == "net_yield")
    assessed = [row for row in rows if row["final_score"] is not None]
    card["assessed_points"] = sum(row["final_score"] for row in assessed)
    card["assessed_weight"] = sum(row["weight"] for row in assessed)
    total = card["assessed_points"] if len(assessed) == 7 else None
    card["unadjusted_grade"] = score_grade(total)
    card["grade_cap"] = "C" if report["fundamental_trend"] == "Structural Decline" else None
    grade = card["unadjusted_grade"]
    if grade and card["grade_cap"]:
        grade = max(grade, card["grade_cap"])
    report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = total
    report["grade"] = report["key_metrics_at_a_glance"]["grade"] = grade
    q = card["quality_score_85"]
    report["key_metrics_at_a_glance"]["quality_score_85"] = q
    report["dividend_quality"] = "Unclear" if q is None else "High" if q >= 68 else "Medium" if q >= 51 else "Low"


def attach_scorecard(report):
    specs = {
        "net_yield": (1, (True, False, True)),
        "dividend_stability": (1, (True, None, None)),
        "cash_coverage": (1, (True, False, None)),
        "balance_sheet": (2, (True, None, True)),
        "capital_allocation": (2, (True, True, None)),
        "buyback_quality": (2, (True, None, None)),
        "visibility": (2, (True, True, None)),
    }
    modules = []
    for name, (band, checks) in specs.items():
        metric = None
        if name == "net_yield":
            zone, price = report["buy_zone"], report["price_used"]
            metric = zone["normalized_net_dps"] / price
            band = next((i for i, floor in enumerate((.07, .05, .035, .02), 1) if metric >= floor), 5)
            checks = (
                report["income_assessment"]["forward_net_dps"] >= zone["normalized_net_dps"],
                zone["bear_net_dps"] / price >= zone["required_net_yield_high"],
                metric >= report["return_requirements"]["required_total_return_low"],
            )
        if name == "cash_coverage":
            metric = report["coverage_summary"]["three_year_recurring_coverage"]
        modules.append({
            "module": name, "weight": SCORE_BANDS[name][0], "assessment": "assessed",
            "metric_value": metric, "period": "Synthetic FY2021-2030 evidence window",
            "band": band, "rationale": EVIDENCE,
            "checks": [{
                "check": i, "status": "unknown" if met is None else "met" if met else "not_met",
                "evidence": EVIDENCE, "source_refs": [] if met is None else [EVIDENCE],
            } for i, met in enumerate(checks, 1)],
            "raw_score": 0, "cap": SCORE_BANDS[name][0], "cap_reason": "Use the documented module cap once.",
            "final_score": 0, "source_refs": [EVIDENCE], "missing_evidence": [],
        })
    report["scorecard"] = {
        "rubric_version": "1", "modules": modules, "quality_score_85": 0, "income_score_15": 0,
        "assessed_points": 0, "assessed_weight": 0, "unadjusted_grade": None,
        "grade_cap": None, "grade_cap_reason": "No structural decline in this fixture.",
    }
    refresh_score_totals(report)


def attach_rating_audit(report):
    report["rating_audit"] = {
        field: {
            "label": report[field], "rule": "Apply the named rule in scoring.md, not the combined Grade.",
            "supporting_evidence": EVIDENCE, "source_refs": [EVIDENCE],
            "upgrade_trigger": "Next disclosed operating/cash record supports the next rating's conditions.",
            "downgrade_trigger": "Reconciled recurring cash fails the currently funded policy.",
        }
        for field in ("dividend_quality", "dividend_safety", "withholding_efficiency", "buyback_quality",
                      "three_year_outlook", "fundamental_trend", "forecast_confidence", "portfolio_role")
    }


def attach_entry_plan(report, risk_status="pass", evidence_ready=True):
    price, income, mode = report["price_used"], report["income_assessment"], report["valuation_mode"]
    hard = income["target"]["target_policy"] == "hard_minimum"
    ready = evidence_ready and risk_status == "pass" and mode != "suspended"
    if mode != "suspended":
        report["action_assessment"]["status"] = (
            "eligible" if ready and (not hard or income["income_eligible"] is True) else "diagnostic_only"
        )
    else:
        report["action_assessment"]["status"] = "suspended"
    prices = stage_prices(report)
    stages = []
    strong_profile = report["forecast_confidence"] == "High" and report["dividend_safety"] == "Strong"
    for name, value in zip(("starter", "add", "strong_buy"), prices):
        effective = value
        if value is not None and hard:
            effective = (None if income["income_eligible"] is None else
                         min(value, income["income_price_ceiling"]) if income["income_price_ceiling"] is not None else value)
        if value is None or value <= 0 or risk_status == "fail":
            state = "unavailable"
        elif not ready or effective is None or price is None or (name == "strong_buy" and not strong_profile):
            state = "waiting_evidence"
        else:
            state = "ready" if price <= effective else "waiting_price"
        stages.append({
            "stage": name, "valuation_price": value, "effective_price": effective,
            "gap_to_current_pct": None if effective is None or price is None else (effective / price - 1) * 100,
            "status": state, "condition": "Confirm funded cash, capital access and this stage's confidence/price.",
        })
    avoid = (risk_status == "fail" or report["dividend_safety"] == "Weak"
             or report["value_trap_veto"] == "Triggered"
             or (report["fundamental_trend"] == "Structural Decline" and mode != "finite_life_harvest"))
    if avoid:
        action = "avoid"
    elif stages[0]["status"] == "waiting_price":
        action = "wait_for_price"
    elif stages[0]["status"] != "ready":
        action = "wait_for_evidence"
    elif stages[2]["status"] == "ready":
        action = "strong_buy"
    elif stages[1]["status"] == "ready" and report["forecast_confidence"] == "High":
        action = "buy"
    else:
        action = "accumulate"
    returns = []
    for scenario in ("Bear", "Base", "Bull"):
        known = price is not None and risk_status != "not_assessed"
        path = [row for row in report["dividend_and_yield_runway"]
                if row["scenario"] == scenario and row["forecast_year"] <= 3]
        cash = sum(row["derived_dps"] for row in path)
        exit_price = path[-1]["derived_dps"] / (.1 if scenario == "Bear" else .08)
        returns.append({
            "scenario": scenario, "horizon_years": 3 if known else None,
            "net_cash_received": cash if known else None, "exit_price": exit_price if known else None,
            "costs": 0 if known else None,
            "cumulative_return": (cash + exit_price - price) / price if known else None,
            "basis": "Fictional runway cash; exit at a 10% Bear or 8% Base/Bull yield, no costs or reinvestment.",
            "source_refs": [EVIDENCE],
        })
    scope = {"wait_for_price": "price", "wait_for_evidence": "evidence", "avoid": "fundamentals"}.get(action)
    report["entry_plan"] = {
        "current_action": action, "summary": "Conditional synthetic entry, never an automatic trade.",
        "opportunity_thesis": "Supported net cash compensates for the stated operating and principal risks.",
        "market_expectation_gap": "Compare the price-implied normalized yield; no consensus expectations supplied.",
        "stages": stages, "return_scenarios": returns,
        "risk_review": {"status": risk_status, "rationale": EVIDENCE, "source_refs": [EVIDENCE]},
        "blockers": ([] if scope is None else [{
            "scope": scope, "reason": EVIDENCE, "resolution": "Recheck the named price or evidence gate.",
            "source_refs": [EVIDENCE],
        }]),
        "catalysts": [{
            "event": "Next ordinary cash declaration", "check_date_or_period": "Next scheduled results",
            "confirmation": "Cash generation continues to fund policy entitlement.",
            "source_to_revisit": "Issuer results and dividend notice",
            "if_missed": "Pause additions and rebuild the payout/funding bridge.",
        }],
        "invalidation_conditions": ["Unresolved funding gap or payout restriction requires a thesis rebuild."],
        "automatic_trade": False,
    }
    report["key_metrics_at_a_glance"]["current_action"] = action
    report["action_assessment"]["strong_buy_eligible"] = action == "strong_buy"


def latest_report(growth=False, price=40, confidence="Medium", safety="Acceptable"):
    report = full_report(growth)
    report.update(schema_version="2.4", price_used=price, forecast_confidence=confidence, dividend_safety=safety)
    if growth:
        for row in report["growth_valuation"]["scenarios"]:
            row["required_return"] = .09
        refresh_growth_pv(report)
    report["income_assessment"]["forward_net_yield"] = 4 / price
    report["key_metrics_at_a_glance"]["normalized_net_yield"] = 4 / price
    attach_scorecard(report)
    attach_rating_audit(report)
    attach_entry_plan(report)
    return report


def unassess_module(report, name):
    row = next(row for row in report["scorecard"]["modules"] if row["module"] == name)
    row.update(assessment="not_assessable", band=None, metric_value=None, raw_score=None, cap=None,
               final_score=None, missing_evidence=["The source needed to establish this band is unavailable."])
    refresh_score_totals(report)
    attach_rating_audit(report)


class DecisionRuleTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_latest_ordinary_and_growth_have_positive_medium_entry(self):
        for growth in (False, True):
            report = latest_report(growth)
            self.assertValid(report)
            self.assertEqual(report["entry_plan"]["current_action"], "accumulate")
            self.assertFalse(report["action_assessment"]["strong_buy_eligible"])
            self.assertEqual(report["scorecard"]["quality_score_85"], 62)
            self.assertEqual(report["score_100"], 76)

    def test_latest_requires_all_audits_but_legacy_still_reads(self):
        self.assertValid(full_report())
        for field in ("entry_plan", "scorecard", "rating_audit"):
            report = latest_report()
            del report[field]
            self.assertInvalid(report, field)
        report = full_report()
        report["schema_version"] = "2.4"
        self.assertInvalid(report, "scorecard")

    def test_screen_cannot_acquire_full_analysis_audits(self):
        for field in ("entry_plan", "scorecard", "rating_audit"):
            report = screen_report()
            report["schema_version"] = "2.4"
            report[field] = latest_report()[field]
            self.assertInvalid(report, "Additional properties")

    def test_fixed_band_refinements_and_grade_edges(self):
        self.assertEqual([score_points("cash_coverage", 2, n) for n in range(4)], [12, 13, 14, 16])
        self.assertEqual([score_points("net_yield", 1, n) for n in range(4)], [13, 13, 14, 15])
        self.assertEqual([score_grade(n) for n in (0, 39, 40, 54, 55, 69, 70, 84, 85, 100)],
                         ["E", "E", "D", "D", "C", "C", "B", "B", "A", "A"])
        for args in (("not-a-module", 1, 1), ("visibility", 5, 1), ("net_yield", 1, 4)):
            with self.assertRaises(ValueError):
                score_points(*args)

    def test_unsupported_total_and_grade_no_longer_pass(self):
        report = latest_report()
        report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = 99
        report["grade"] = report["key_metrics_at_a_glance"]["grade"] = "A"
        self.assertInvalid(report, "Combined score /100")
        self.assertInvalid(report, "Final Grade")

    def test_raw_points_caps_and_bands_are_recomputed(self):
        for field, value, fragment in (("raw_score", 15, "raw points"), ("cap", 12, "explicit cap"),
                                       ("band", 2, "band disagrees"), ("metric_value", .2, "Income score metric")):
            report = latest_report()
            report["scorecard"]["modules"][0][field] = value
            self.assertInvalid(report, fragment)

    def test_duplicate_modules_checks_and_weights_are_rejected(self):
        report = latest_report()
        report["scorecard"]["modules"][1] = copy.deepcopy(report["scorecard"]["modules"][0])
        self.assertInvalid(report, "each fixed module")
        report = latest_report()
        report["scorecard"]["modules"][0]["checks"][1]["check"] = 1
        self.assertInvalid(report, "each refinement check")
        report = latest_report()
        report["scorecard"]["modules"][0]["weight"] = 20
        self.assertInvalid(report, "weight must remain")

    def test_unknown_refinement_retains_supported_band_and_action(self):
        report = latest_report()
        row = report["scorecard"]["modules"][1]
        row["checks"][0].update(status="unknown", source_refs=[])
        refresh_score_totals(report)
        attach_rating_audit(report)
        self.assertValid(report)
        self.assertEqual(row["final_score"], 12)
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_partial_noncritical_score_does_not_create_an_entry_veto(self):
        report = latest_report()
        unassess_module(report, "buyback_quality")
        self.assertValid(report)
        self.assertIsNone(report["score_100"])
        self.assertIsNone(report["grade"])
        self.assertIsNone(report["scorecard"]["quality_score_85"])
        self.assertEqual(report["scorecard"]["assessed_weight"], 90)
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")
        report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = 79
        self.assertInvalid(report, "Combined score /100")

    def test_missing_tax_preserves_quality_but_blocks_entry(self):
        report = latest_report()
        report["withholding_basis"] = "unknown"
        report["withholding_efficiency"] = "Unclear"
        report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None)
        unassess_module(report, "net_yield")
        attach_entry_plan(report, risk_status="not_assessed", evidence_ready=False)
        self.assertValid(report)
        self.assertEqual(report["scorecard"]["quality_score_85"], 62)
        self.assertIsNone(report["scorecard"]["income_score_15"])
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")

    def test_price_change_cannot_upgrade_quality(self):
        original, cheaper = latest_report(), latest_report(price=30)
        self.assertValid(cheaper)
        self.assertEqual(original["scorecard"]["quality_score_85"], cheaper["scorecard"]["quality_score_85"])
        self.assertEqual(cheaper["scorecard"]["income_score_15"], 15)
        self.assertEqual(cheaper["entry_plan"]["current_action"], "accumulate")
        cheaper["scorecard"]["quality_score_85"] += 1
        self.assertInvalid(cheaper, "Quality score /85")

    def test_rating_labels_and_sources_cannot_drift(self):
        report = latest_report()
        report["rating_audit"]["dividend_safety"]["label"] = "Strong"
        self.assertInvalid(report, "rating audit label")
        report = latest_report()
        report["rating_audit"]["dividend_safety"]["source_refs"] = ["Invented source"]
        self.assertInvalid(report, "declared report sources")
        report = latest_report()
        report["rating_audit"]["dividend_safety"]["upgrade_trigger"] = "   "
        self.assertInvalid(report, "upgrade_trigger")

    def test_ordinary_price_stages_and_exact_boundaries(self):
        for price, confidence, safety, expected in (
            (50, "Medium", "Acceptable", "accumulate"),
            (50.001, "High", "Strong", "wait_for_price"),
            (40, "High", "Acceptable", "buy"),
            (32, "High", "Strong", "strong_buy"),
            (32.001, "High", "Strong", "buy"),
        ):
            with self.subTest(price=price, confidence=confidence):
                report = latest_report(price=price, confidence=confidence, safety=safety)
                self.assertValid(report)
                self.assertEqual(report["entry_plan"]["current_action"], expected)
                self.assertEqual([row["valuation_price"] for row in report["entry_plan"]["stages"]], [50, 40, 32])

    def test_growth_starter_is_not_the_strict_bear_threshold(self):
        report = latest_report(growth=True)
        stages = report["entry_plan"]["stages"]
        self.assertAlmostEqual(stages[0]["valuation_price"], 48.57142857142857)
        self.assertAlmostEqual(stages[1]["valuation_price"], 45.71428571428571)
        self.assertAlmostEqual(stages[2]["valuation_price"], 38.85714285714285)
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")
        self.assertGreater(report["price_used"], stages[2]["valuation_price"])
        expensive = latest_report(growth=True, price=49)
        self.assertValid(expensive)
        self.assertEqual(expensive["entry_plan"]["current_action"], "wait_for_price")

    def test_hard_income_shortfall_waits_for_price_not_perfect_evidence(self):
        for growth in (False, True):
            report = latest_report(growth)
            report["income_assessment"].update(
                target={"target_net_yield": .12, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
                income_eligible=False, yield_fit="Below target", income_price_ceiling=4 / .12,
            )
            attach_entry_plan(report)
            self.assertValid(report)
            self.assertEqual(report["entry_plan"]["current_action"], "wait_for_price")
            self.assertAlmostEqual(report["entry_plan"]["stages"][0]["effective_price"], 33.333333333333336)
            self.assertAlmostEqual(report["entry_plan"]["stages"][0]["gap_to_current_pct"], -16.666666666666664)

    def test_preference_does_not_change_entry_prices(self):
        report = latest_report()
        report["income_assessment"].update(
            target={"target_net_yield": .12, "target_basis": "user_explicit", "target_policy": "preference"},
            income_eligible=True, yield_fit="Below target",
        )
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["stages"][0]["effective_price"], 50)

    def test_generic_caution_cannot_override_met_conditions(self):
        report = latest_report()
        report["entry_plan"]["current_action"] = report["key_metrics_at_a_glance"]["current_action"] = "wait_for_evidence"
        self.assertInvalid(report, "Current action must be accumulate")
        report = latest_report()
        report["action_assessment"]["status"] = "diagnostic_only"
        self.assertInvalid(report, "not generic caution")

    def test_risk_review_and_return_arithmetic_are_not_optional(self):
        report = latest_report()
        report["entry_plan"]["return_scenarios"][0]["cumulative_return"] = .4
        self.assertInvalid(report, "Bear cumulative holding return")
        report = latest_report()
        report["entry_plan"]["return_scenarios"][0].update(net_cash_received=None, cumulative_return=None)
        self.assertInvalid(report, "quantified Bear/Base/Bull")
        report = latest_report()
        report["entry_plan"]["return_scenarios"][0]["horizon_years"] = 5
        self.assertInvalid(report, "same holding horizon")
        report = latest_report()
        attach_entry_plan(report, risk_status="not_assessed")
        report["entry_plan"]["return_scenarios"][0]["horizon_years"] = 3
        report["entry_plan"]["return_scenarios"][1]["horizon_years"] = 5
        self.assertInvalid(report, "same holding horizon")

    def test_unassessed_or_failed_risk_has_an_explicit_action(self):
        for status, expected in (("not_assessed", "wait_for_evidence"), ("fail", "avoid")):
            report = latest_report()
            attach_entry_plan(report, risk_status=status)
            self.assertValid(report)
            self.assertEqual(report["entry_plan"]["current_action"], expected)
            self.assertFalse(report["entry_plan"]["automatic_trade"])

    def test_low_confidence_and_normalization_gaps_still_block_entry(self):
        report = latest_report()
        report["forecast_confidence"] = "Low"
        refresh_score_totals(report)
        attach_rating_audit(report)
        attach_entry_plan(report, evidence_ready=False)
        self.assertValid(report)
        self.assertEqual(report["scorecard"]["income_score_15"], 9)
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")
        report = latest_report()
        report["buy_zone"]["normalization_evidence"]["operating_cash"].update(
            status="missing", source_refs=[], resolution_source="Operating and cash-flow disclosure",
        )
        unassess_module(report, "net_yield")
        attach_entry_plan(report, evidence_ready=False)
        self.assertValid(report)
        report["entry_plan"]["stages"][0]["status"] = "ready"
        self.assertInvalid(report, "readiness must be waiting_evidence")

    def test_stage_distances_and_monitoring_are_required(self):
        report = latest_report()
        report["entry_plan"]["stages"][0]["gap_to_current_pct"] = -25
        self.assertInvalid(report, "signed price distance")
        for key in ("catalysts", "invalidation_conditions"):
            report = latest_report()
            report["entry_plan"][key] = []
            self.assertInvalid(report, key)

    def test_suspended_veto_has_no_numerical_entry_ladder(self):
        report = latest_report()
        report.pop("buy_zone")
        report["valuation_mode"] = report["key_metrics_at_a_glance"]["valuation_mode"] = "suspended"
        report["value_trap_veto"] = "Triggered"
        unassess_module(report, "net_yield")
        attach_entry_plan(report, risk_status="not_assessed")
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["current_action"], "avoid")
        self.assertTrue(all(row["valuation_price"] is None for row in report["entry_plan"]["stages"]))
        report["entry_plan"]["stages"][0]["valuation_price"] = 10
        self.assertInvalid(report, "starter valuation price")

    def test_short_history_does_not_erase_supported_forward_entry(self):
        report = latest_report()
        report["cash_flow_bridge"] = report["cash_flow_bridge"][-2:]
        report["coverage_summary"].update(
            fiscal_years=["2024", "2025"], years_available=2, three_year_recurring_coverage=None,
            five_year_worst_recurring_coverage=None, worst_available_recurring_coverage=2,
            worst_recurring_year="2024",
        )
        unassess_module(report, "cash_coverage")
        report["rating_audit"]["dividend_safety"]["supporting_evidence"] = (
            "Historical three-year coverage is unavailable; safety uses the separately funded forward "
            "Base/Bear cash and capital bridge, not an invented historical series."
        )
        self.assertValid(report)
        self.assertIsNone(report["score_100"])
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_named_coverage_overrides_are_audited_not_hidden_penalties(self):
        report = latest_report()
        row = next(row for row in report["scorecard"]["modules"] if row["module"] == "cash_coverage")
        row["band_override"] = {"rule": "peak_cycle_only", "evidence": EVIDENCE, "source_refs": [EVIDENCE]}
        row["band"] = 3
        refresh_score_totals(report)
        attach_rating_audit(report)
        self.assertValid(report)
        self.assertEqual(row["final_score"], 7)
        row["band_override"]["source_refs"] = ["Undeclared cycle source"]
        self.assertInvalid(report, "declared report sources")
        report = latest_report()
        report["scorecard"]["modules"][0]["band_override"] = {
            "rule": "peak_cycle_only", "evidence": EVIDENCE, "source_refs": [EVIDENCE],
        }
        self.assertInvalid(report, "Only assessed cash coverage")

    def test_quantified_refinement_cannot_contradict_known_actual_shortfall(self):
        report = latest_report()
        row = next(row for row in report["scorecard"]["modules"] if row["module"] == "cash_coverage")
        row["checks"][1]["status"] = "met"
        refresh_score_totals(report)
        attach_rating_audit(report)
        self.assertInvalid(report, "Coverage check 2 contradicts")

    def test_normalization_gap_cannot_keep_high_income_points(self):
        report = latest_report()
        report["buy_zone"]["normalization_evidence"]["operating_cash"].update(
            status="missing", source_refs=[], resolution_source="Cash-flow disclosure",
        )
        attach_entry_plan(report, evidence_ready=False)
        self.assertInvalid(report, "Income points require supported normalization")

    def test_coincident_boundaries_and_zero_bear_are_not_clipped(self):
        report = latest_report(price=40, confidence="High", safety="Strong")
        report["buy_zone"].update(bear_net_dps=4, boundaries=ordinary_boundaries(4, 4, .08, .1))
        attach_scorecard(report)
        attach_rating_audit(report)
        attach_entry_plan(report)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["current_action"], "strong_buy")
        self.assertEqual(report["entry_plan"]["stages"][1]["effective_price"],
                         report["entry_plan"]["stages"][2]["effective_price"])
        report = latest_report()
        report["buy_zone"].update(bear_net_dps=0, boundaries=ordinary_boundaries(4, 0, .08, .1))
        attach_entry_plan(report, evidence_ready=False)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["stages"][2]["status"], "unavailable")
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")

    def test_zero_hard_floor_and_missing_hard_inputs_remain_distinct(self):
        report = latest_report()
        report["income_assessment"].update(
            target={"target_net_yield": 0, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
            yield_fit="Pass", income_eligible=True,
        )
        attach_entry_plan(report)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["stages"][0]["effective_price"], 50)
        report["income_assessment"].update(
            target={"target_net_yield": .05, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
            forward_net_dps=None, forward_net_yield=None, yield_fit="Not Assessed", income_eligible=None,
        )
        income_score = report["scorecard"]["modules"][0]
        income_score["checks"][0].update(status="unknown", source_refs=[])
        refresh_score_totals(report)
        attach_rating_audit(report)
        attach_entry_plan(report)
        self.assertValid(report)
        self.assertIsNone(report["entry_plan"]["stages"][0]["effective_price"])
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")

    def test_finite_harvest_retains_grade_cap_and_only_one_entry_stage(self):
        report = latest_report(price=20)
        report.update(valuation_mode="finite_life_harvest", fundamental_trend="Structural Decline",
                      structural_decline_cap_applied=True, harvest_managed_runoff_exception_applied=True,
                      portfolio_role="Opportunistic")
        report["key_metrics_at_a_glance"].update(valuation_mode="finite_life_harvest", portfolio_role="Opportunistic")
        report["buy_zone"].update(required_net_yield_low=.1, required_net_yield_high=.12,
                                  boundaries=ordinary_boundaries(4, 3.2, .1, .12))
        pv = sum(10 / 1.1 ** year for year in range(1, 4))
        report["finite_life_valuation"] = {
            "harvest_horizon_years": 3, "discount_rate": .1,
            "forecast_net_distributions": [
                {"year": str(year), "net_distribution": 10, "present_value": 10 / 1.1 ** year}
                for year in range(1, 4)
            ],
            "present_value_of_distributions": pv, "residual_value": 0, "residual_value_basis": EVIDENCE,
            "finite_life_value_low": pv - 1, "finite_life_value_high": pv + 1,
        }
        attach_scorecard(report)
        attach_rating_audit(report)
        attach_entry_plan(report)
        self.assertValid(report)
        self.assertEqual(report["scorecard"]["unadjusted_grade"], "B")
        self.assertEqual(report["grade"], "C")
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")
        self.assertEqual([row["valuation_price"] for row in report["entry_plan"]["stages"]][1:], [None, None])
        report["scorecard"]["grade_cap"] = None
        self.assertInvalid(report, "Grade C cap")

    def test_known_bear_cash_shortfall_cannot_appear_buy_ready(self):
        report = latest_report()
        forecast = report["three_year_fundamental_forecast"][0]
        bridge = report["dividend_forecast_bridge"][0]
        dividend = report["dividend_and_yield_runway"][0]
        forecast["actual_all_in_fcf"] -= 25
        bridge["exceptional_cash_uses"] += 25
        bridge["cash_available_for_distribution"] -= 25
        for item in bridge["deduction_ledger"]:
            if item["category"] == "exceptional":
                item["amount"] += 25
                item["incremental_deduction"] += 25
        dividend["cash_available_for_distribution"] -= 25
        dividend["funding_gap"] = dividend["all_cash_funding_gap"] = 1
        self.assertInvalid(report, "ordinary Bear/Base cash")
        self.assertInvalid(report, "Coverage check 1 contradicts")
        coverage = next(row for row in report["scorecard"]["modules"] if row["module"] == "cash_coverage")
        coverage["checks"][0]["status"] = "not_met"
        refresh_score_totals(report)
        attach_rating_audit(report)
        attach_entry_plan(report, evidence_ready=False)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")
        bridge["excess_cash_used"] = 1
        bridge["cash_available_for_distribution"] += 1
        dividend["cash_available_for_distribution"] += 1
        dividend["funding_gap"] = dividend["all_cash_funding_gap"] = 0
        coverage["checks"][0]["status"] = "met"
        refresh_score_totals(report)
        attach_rating_audit(report)
        attach_entry_plan(report)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_funded_ordinary_cash_smoothing_is_not_a_growth_only_gate(self):
        report = latest_report()
        forecast = report["three_year_fundamental_forecast"][0]
        bridge = report["dividend_forecast_bridge"][0]
        dividend = report["dividend_and_yield_runway"][0]
        forecast["operating_cash_flow"] -= 30
        forecast["normalized_ocf"] -= 30
        forecast["fcf_or_distributable_cash"] -= 30
        forecast["recurring_fad"] -= 30
        forecast["actual_all_in_fcf"] -= 30
        bridge["fcf_or_capital_generation"] -= 30
        bridge["recurring_fad"] -= 30
        bridge["excess_cash_used"] += 6
        bridge["cash_available_for_distribution"] -= 24
        dividend["cash_available_for_distribution"] -= 24
        cash = next(row for row in report["business_outlook"]["cumulative_fad"] if row["scenario"] == "Bear")
        cash["three_year"] -= 30
        cash["five_year"] -= 30
        self.assertLess(bridge["recurring_fad"], dividend["dividend_entitlement"])
        self.assertEqual(bridge["cash_available_for_distribution"], dividend["dividend_entitlement"])
        coverage = next(row for row in report["scorecard"]["modules"] if row["module"] == "cash_coverage")
        coverage["checks"][0]["status"] = "not_met"
        refresh_score_totals(report)
        attach_rating_audit(report)
        self.assertValid(report)
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")


if __name__ == "__main__":
    unittest.main()
