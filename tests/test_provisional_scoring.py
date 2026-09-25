"""Evidence-recovery contracts and pinned report-shape replays, not issuer re-ratings."""

import copy
import json
import unittest
from pathlib import Path

from scripts.decision_rules import SCORE_BANDS, buyback_rating, metric_band, module_cap, score_grade, summarize_scorecard
from scripts.validate_analysis import validate_report
from test_analysis_contract import EVIDENCE, full_report, unavailable_years
from test_local_extensions import attach_local_extensions, refresh_local_quality
from test_decision_rules import (
    attach_entry_plan,
    attach_rating_audit,
    latest_report,
    refresh_score_totals,
)


def score_row(report, name):
    return next(row for row in report["scorecard"]["modules"] if row["module"] == name)


def refresh_provisional(report):
    for row in report["scorecard"]["modules"]:
        if row["assessment"] == "bounded":
            row["cap"] = module_cap(report, row["module"])
    refresh_score_totals(report)
    card = report["scorecard"]
    summary = card["summary"] = summarize_scorecard(report)
    for field, key in (("quality_score_85", "quality_range"), ("income_score_15", "income_range")):
        interval = summary[key]
        card[field] = interval["low"] if interval["low"] == interval["high"] else None
    interval = summary["score_range"]
    total = interval["low"] if interval["low"] == interval["high"] else None
    raw_grades = [score_grade(interval[key]) for key in ("low", "high")]
    card["unadjusted_grade"] = raw_grades[0] if raw_grades[0] == raw_grades[1] else None
    grades, labels = summary["grade_range"], summary["quality_rating_range"]
    grade = grades["best"] if grades["worst"] == grades["best"] else None
    report["dividend_quality"] = labels["best"] if labels["worst"] == labels["best"] else "Unclear"
    if report["buyback_quality"] != "Not Applicable":
        report["buyback_quality"] = buyback_rating(score_row(report, "buyback_quality"))
    report.update(score_100=total, grade=grade)
    report["key_metrics_at_a_glance"].update(
        score_100=total, grade=grade, quality_score_85=card["quality_score_85"],
        score_status=summary["status"], score_range=copy.deepcopy(summary["score_range"]),
        quality_score_range=copy.deepcopy(summary["quality_range"]),
        score_coverage_pct=summary["evidence_coverage_pct"], grade_range=copy.deepcopy(grades),
    )
    attach_rating_audit(report)
    refresh_local_quality(report)


def provisional_report(**kwargs):
    """Pinned 2.5 compatibility record; test_schema3 explicitly adds the 3.0 contract."""
    report = latest_report(**kwargs)
    report["schema_version"] = "2.5"
    report["scorecard"]["rubric_version"] = "2"
    for row in report["scorecard"]["modules"]:
        row["evidence_basis"] = "reported"
    refresh_provisional(report)
    attach_local_extensions(report)
    return report


def mark_unknown(report, name):
    row = score_row(report, name)
    row.pop("bounds", None)
    row.pop("band_override", None)
    row.pop("adverse_evidence", None)
    row.update(
        assessment="not_assessable", evidence_basis="unknown", band=None, metric_value=None,
        raw_score=None, cap=None, final_score=None,
        missing_evidence=["The bounded synthetic packet cannot establish this primary band."],
        recovery={
            "attempt": "Inspect the supplied packet and attempt reconciliation; no issuer lookup is authorized.",
            "outcome": "not_in_packet",
            "next_source": "The dated issuer disclosure that resolves this module's primary input.",
        },
    )
    refresh_provisional(report)


def bound_module(report, name, bands, basis="qualitative", low=None, high=None):
    row = score_row(report, name)
    row.pop("recovery", None)
    row.pop("adverse_evidence", None)
    row.update(
        assessment="bounded", evidence_basis="estimated", band=None, metric_value=None,
        raw_score=None, final_score=None,
        bounds={
            "metric_basis": basis, "metric_low": low, "metric_high": high, "bands": bands,
            "derivation": "Synthetic disclosed anchors and reconciliation bound the input; no neutral imputation.",
            "limitations": "The stated range is a scoring proxy, not normalization or entry authorization.",
            "source_refs": [EVIDENCE],
        },
    )
    refresh_provisional(report)


def suspend_model(report):
    report.pop("buy_zone", None)
    report["valuation_mode"] = report["key_metrics_at_a_glance"]["valuation_mode"] = "suspended"
    report.update(forecast_confidence="Not Forecastable", value_trap_veto="Unclear", dividend_safety="Unclear")
    report["key_metrics_at_a_glance"]["normalized_net_yield"] = None
    report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None)
    attach_entry_plan(report, risk_status="not_assessed", evidence_ready=False)
    unavailable_years(report, 1)
    report["cash_flow_model"].update(
        evidence_status="insufficient", missing_inputs=["Unreconciled parent remittance and capital constraints"],
    )
    for row in report["cash_flow_bridge"]:
        row.update(recurring_owner_fcf_or_proxy=None, recurring_fad=None,
                   fcf_dividend_coverage=None, evidence_status="insufficient")
    report["coverage_summary"].update(
        three_year_recurring_coverage=None, five_year_worst_recurring_coverage=None,
        worst_available_recurring_coverage=None, worst_recurring_year=None,
    )
    mark_unknown(report, "net_yield")
    mark_unknown(report, "cash_coverage")
    for name, indexes in (("visibility", (0, 1)), ("balance_sheet", (1, 2)), ("capital_allocation", (1,))):
        for index in indexes:
            score_row(report, name)["checks"][index].update(status="unknown", source_refs=[])
    bound_module(report, "visibility", [2, 3])


def use_short_history(report):
    report["cash_flow_bridge"] = report["cash_flow_bridge"][-2:]
    report["coverage_summary"].update(
        fiscal_years=["2024", "2025"], years_available=2, three_year_recurring_coverage=None,
        five_year_worst_recurring_coverage=None, worst_available_recurring_coverage=2,
        worst_recurring_year="2024",
    )


class ProvisionalScoringTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_complete_scores_and_both_legacy_versions_remain_readable(self):
        self.assertValid(full_report())
        self.assertValid(latest_report())
        for growth in (False, True):
            report = provisional_report(growth=growth)
            self.assertValid(report)
            self.assertEqual(report["score_100"], 76)
            self.assertEqual(report["scorecard"]["summary"]["score_range"], {"low": 76, "high": 76})
            self.assertEqual(report["scorecard"]["summary"]["status"], "complete")
            self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_one_unknown_module_retains_numeric_range_and_stable_grade(self):
        report = provisional_report()
        mark_unknown(report, "buyback_quality")
        self.assertValid(report)
        card, summary = report["scorecard"], report["scorecard"]["summary"]
        self.assertEqual((card["assessed_points"], card["assessed_weight"]), (71, 90))
        self.assertEqual(summary["score_range"], {"low": 71, "high": 81})
        self.assertEqual(summary["quality_range"], {"low": 57, "high": 67})
        self.assertEqual(summary["quality_coverage_pct"], 88.24)
        self.assertEqual(summary["status"], "provisional")
        self.assertEqual((report["grade"], report["dividend_quality"]), ("B", "Medium"))
        self.assertIsNone(report["score_100"])
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_unknown_tax_retains_quality_but_not_an_entry_pass(self):
        report = provisional_report()
        report.update(withholding_rate=None, withholding_basis="unknown", withholding_efficiency="Unclear")
        report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None)
        mark_unknown(report, "net_yield")
        attach_entry_plan(report, risk_status="not_assessed", evidence_ready=False)
        self.assertValid(report)
        summary = report["scorecard"]["summary"]
        self.assertEqual(summary["score_range"], {"low": 62, "high": 77})
        self.assertEqual(summary["quality_range"], {"low": 62, "high": 62})
        self.assertEqual(summary["grade_range"], {"worst": "C", "best": "B"})
        self.assertEqual((summary["evidence_coverage_pct"], summary["quality_coverage_pct"]), (85, 100))
        self.assertEqual(report["scorecard"]["quality_score_85"], 62)
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")
        self.assertIsNone(report["grade"])

    def test_all_unknown_is_not_a_zero_or_neutral_company_score(self):
        report = provisional_report()
        for name in SCORE_BANDS:
            mark_unknown(report, name)
        self.assertValid(report)
        summary = report["scorecard"]["summary"]
        self.assertEqual(summary["status"], "insufficient")
        self.assertEqual(summary["score_range"], {"low": 0, "high": 100})
        self.assertEqual((summary["evidence_coverage_pct"], summary["missing_weight"]), (0, 100))
        self.assertIsNone(report["score_100"])
        self.assertEqual(report["dividend_quality"], "Unclear")

    def test_bounded_primary_band_uses_known_checks_and_possible_unknown_checks(self):
        report = provisional_report()
        bound_module(report, "buyback_quality", [2, 3])
        self.assertValid(report)
        summary = report["scorecard"]["summary"]
        self.assertEqual(summary["module_ranges"]["buyback_quality"], {"low": 2, "high": 7})
        self.assertEqual(summary["score_range"], {"low": 73, "high": 78})
        self.assertEqual((summary["bounded_weight"], summary["missing_weight"]), (10, 0))
        self.assertEqual(summary["evidence_coverage_pct"], 100)
        self.assertEqual(report["scorecard"]["assessed_weight"], 90)

    def test_estimated_point_keeps_score_but_exposes_provisional_status(self):
        report = provisional_report()
        score_row(report, "net_yield")["evidence_basis"] = "estimated"
        refresh_provisional(report)
        self.assertValid(report)
        self.assertEqual(report["score_100"], 76)
        self.assertEqual(report["scorecard"]["summary"]["status"], "provisional")

    def test_bounded_buyback_rating_does_not_pick_a_favorable_label(self):
        report = provisional_report()
        bound_module(report, "buyback_quality", [2, 3])
        self.assertValid(report)
        self.assertEqual(report["buyback_quality"], "Unclear")
        report["buyback_quality"] = report["rating_audit"]["buyback_quality"]["label"] = "Good"
        self.assertInvalid(report, "Buyback Quality disagrees")
        legacy = latest_report()
        legacy["buyback_quality"] = "Unclear"
        self.assertInvalid(legacy, "buyback_quality")

    def test_two_year_reconciled_proxy_can_score_without_fake_three_year_history(self):
        report = provisional_report()
        use_short_history(report)
        bound_module(report, "cash_coverage", [1], "reconciled_cash_proxy", 2.0, 2.3)
        row = score_row(report, "cash_coverage")
        row["period"] = "FY2024-FY2025 only, not three years"
        row["bounds"]["derivation"] = "(80+90)/(40+40)=2.125x; stipulated reconciled sensitivity spans 2.0-2.3x."
        self.assertValid(report)
        self.assertIsNone(report["coverage_summary"]["three_year_recurring_coverage"])
        self.assertEqual(row["cap"], 16)
        self.assertEqual(report["score_100"], 74)
        self.assertEqual(report["scorecard"]["summary"]["status"], "provisional")
        self.assertEqual(report["entry_plan"]["current_action"], "accumulate")

    def test_material_cash_gap_keeps_other_scores_and_preserves_suspension(self):
        report = provisional_report()
        suspend_model(report)
        self.assertValid(report)
        summary = report["scorecard"]["summary"]
        self.assertEqual(summary["evidence_coverage_pct"], 65)
        self.assertEqual(summary["missing_weight"], 35)
        self.assertEqual(summary["module_ranges"]["net_yield"], {"low": 0, "high": 9})
        self.assertEqual(summary["module_ranges"]["visibility"], {"low": 2, "high": 7})
        self.assertGreater(summary["score_range"]["low"], 0)
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")
        self.assertTrue(all(row["valuation_price"] is None for row in report["entry_plan"]["stages"]))

    def test_missing_future_rows_do_not_erase_reconciled_history(self):
        report = provisional_report()
        report.pop("buy_zone")
        report["valuation_mode"] = report["key_metrics_at_a_glance"]["valuation_mode"] = "suspended"
        report.update(forecast_confidence="Not Forecastable", dividend_safety="Unclear", value_trap_veto="Unclear")
        report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None)
        report["key_metrics_at_a_glance"]["normalized_net_yield"] = None
        attach_entry_plan(report, risk_status="not_assessed", evidence_ready=False)
        unavailable_years(report, 1)
        for name, indexes in (
            ("net_yield", (0, 1, 2)), ("cash_coverage", (0,)), ("visibility", (0, 1)),
            ("balance_sheet", (1, 2)), ("capital_allocation", (1,)),
        ):
            for index in indexes:
                score_row(report, name)["checks"][index].update(status="unknown", source_refs=[])
        score_row(report, "visibility")["evidence_basis"] = "estimated"
        bound_module(report, "net_yield", [1], "recurring_income_proxy", .1, .1)
        self.assertValid(report)
        self.assertEqual(report["coverage_summary"]["three_year_recurring_coverage"], 2)
        self.assertEqual(score_row(report, "cash_coverage")["final_score"], 17)
        self.assertEqual(report["score_100"], 67)
        self.assertEqual(report["scorecard"]["summary"]["status"], "provisional")
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")

    def test_recurring_income_proxy_is_not_normalization_or_buy_permission(self):
        report = provisional_report()
        suspend_model(report)
        for check in score_row(report, "net_yield")["checks"]:
            check.update(status="unknown", source_refs=[])
        bound_module(report, "net_yield", [3], "recurring_income_proxy", .035, .049)
        self.assertValid(report)
        summary = report["scorecard"]["summary"]
        self.assertEqual(summary["module_ranges"]["net_yield"], {"low": 6, "high": 9})
        self.assertEqual(summary["evidence_coverage_pct"], 80)
        self.assertNotIn("buy_zone", report)
        self.assertIsNone(report["key_metrics_at_a_glance"]["normalized_net_yield"])
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_evidence")
        report["withholding_basis"] = "unknown"
        self.assertInvalid(report, "Income bounds still require supported tax/cash")

    def test_material_capital_gap_cannot_be_relabelled_as_reconciled_coverage(self):
        report = provisional_report()
        suspend_model(report)
        for check in score_row(report, "cash_coverage")["checks"]:
            check.update(status="unknown", source_refs=[])
        bound_module(report, "cash_coverage", [1], "reconciled_cash_proxy", 1.5, 2)
        self.assertInvalid(report, "unresolved material cash/capital")

    def test_unfinished_model_does_not_justify_lowest_visibility_band(self):
        report = provisional_report()
        row = score_row(report, "visibility")
        row["band"] = 4
        refresh_provisional(report)
        self.assertInvalid(report, "adverse issuer evidence")
        row["adverse_evidence"] = {
            "condition": "structurally_unpredictable_cash", "detail": EVIDENCE, "source_refs": [EVIDENCE],
        }
        self.assertValid(report)
        row["adverse_evidence"]["condition"] = "unfinished_model"
        self.assertInvalid(report, "unfinished_model")

    def test_recovery_and_provenance_are_not_optional_or_faked(self):
        for field in ("recovery", "evidence_basis"):
            report = provisional_report()
            mark_unknown(report, "buyback_quality")
            del score_row(report, "buyback_quality")[field]
            self.assertInvalid(report, field)
        report = provisional_report()
        bound_module(report, "buyback_quality", [2, 3])
        score_row(report, "buyback_quality")["bounds"]["source_refs"] = ["Made-up source"]
        self.assertInvalid(report, "declared report sources")
        report = provisional_report()
        mark_unknown(report, "buyback_quality")
        score_row(report, "buyback_quality")["recovery"]["attempt"] = " "
        self.assertInvalid(report, "attempt")

    def test_range_cannot_be_replaced_with_midpoint_or_rescaled_total(self):
        for fake in (76, 79, 71):
            report = provisional_report()
            mark_unknown(report, "buyback_quality")
            report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = fake
            self.assertInvalid(report, "Combined score /100")

    def test_summary_ranges_coverage_status_and_grades_are_recomputed(self):
        for field, fake in (
            ("score_range", {"low": 80, "high": 71}),
            ("quality_range", {"low": 57, "high": 77}),
            ("grade_range", {"worst": "B", "best": "A"}),
            ("quality_rating_range", {"worst": "High", "best": "High"}),
            ("evidence_coverage_pct", 100), ("quality_coverage_pct", 100),
            ("bounded_weight", 10), ("missing_weight", 0), ("status", "complete"),
        ):
            with self.subTest(field=field):
                report = provisional_report()
                mark_unknown(report, "buyback_quality")
                report["scorecard"]["summary"][field] = fake
                self.assertInvalid(report, "Score summary must reconcile")
        report = provisional_report()
        mark_unknown(report, "buyback_quality")
        report["key_metrics_at_a_glance"]["score_range"]["high"] = 99
        self.assertInvalid(report, "Key metrics score_range")

    def test_bounded_metric_and_band_thresholds_cannot_drift(self):
        for name, pairs in (
            ("net_yield", ((.0199, 5), (.02, 4), (.035, 3), (.05, 2), (.07, 1))),
            ("cash_coverage", ((-.1, 4), (.7, 3), (1, 2), (1.5, 1))),
        ):
            for metric, band in pairs:
                self.assertEqual(metric_band(name, metric), band)
        for bands, low, high, message in (
            ([1], .04, .11, "bands disagree"),
            ([1, 2, 3], .11, .04, "ordered endpoints"),
            ([1, 2], .05, .08, "include the supplied normalized yield"),
            ([1, 3], .04, .11, "ordered and contiguous"),
        ):
            report = provisional_report()
            bound_module(report, "net_yield", bands, "normalized_net_yield", low, high)
            self.assertInvalid(report, message)
        report = provisional_report()
        bound_module(report, "buyback_quality", [2, 3])
        score_row(report, "buyback_quality")["bounds"]["bands"] = [5]
        self.assertInvalid(report, "invalid bounded anchor bands")

    def test_nonfinite_quantitative_scores_are_rejected_explicitly(self):
        for name in ("net_yield", "cash_coverage"):
            for value in (float("inf"), float("nan")):
                with self.assertRaises(ValueError):
                    metric_band(name, value)
        report = provisional_report()
        report["coverage_summary"]["three_year_recurring_coverage"] = float("inf")
        score_row(report, "cash_coverage")["metric_value"] = float("inf")
        self.assertInvalid(report, "non-finite numbers are not allowed")

    def test_proxy_caps_and_known_checks_cannot_be_overridden(self):
        report = provisional_report()
        use_short_history(report)
        bound_module(report, "cash_coverage", [1], "reconciled_cash_proxy", 2, 2.2)
        self.assertValid(report)
        score_row(report, "cash_coverage")["cap"] = 20
        self.assertInvalid(report, "explicit cap")
        refresh_provisional(report)
        score_row(report, "cash_coverage")["checks"][1]["status"] = "met"
        self.assertInvalid(report, "contradicts the supplied cash-funding")
        report = provisional_report()
        suspend_model(report)
        bound_module(report, "net_yield", [3], "recurring_income_proxy", .035, .04)
        self.assertInvalid(report, "without N/B must remain unknown")

    def test_proxies_cannot_cherry_pick_over_supported_standard_metrics(self):
        report = provisional_report()
        bound_module(report, "cash_coverage", [1], "reconciled_cash_proxy", 2, 2.2)
        self.assertInvalid(report, "standard aggregate")
        report = provisional_report()
        bound_module(report, "net_yield", [3], "recurring_income_proxy", .035, .049)
        self.assertInvalid(report, "supported normalization")

    def test_bounded_coverage_applies_named_override_before_points(self):
        report = provisional_report()
        row = score_row(report, "cash_coverage")
        row["band_override"] = {"rule": "peak_cycle_only", "evidence": EVIDENCE, "source_refs": [EVIDENCE]}
        bound_module(report, "cash_coverage", [3], "three_year_recurring_coverage", 1.6, 2.4)
        self.assertValid(report)
        self.assertEqual(report["scorecard"]["summary"]["module_ranges"]["cash_coverage"], {"low": 7, "high": 9})
        row["bounds"]["bands"] = [1]
        self.assertInvalid(report, "bounded bands disagree")

    def test_unknown_module_cannot_hide_an_unaudited_adverse_record(self):
        report = provisional_report()
        mark_unknown(report, "visibility")
        score_row(report, "visibility")["adverse_evidence"] = {
            "condition": "policy_failure", "detail": EVIDENCE, "source_refs": ["Not a declared source"],
        }
        self.assertInvalid(report, "declared report sources")
        self.assertInvalid(report, "belongs to an assessed")

    def test_new_contract_cannot_be_smuggled_into_legacy_or_omit_headline(self):
        for version in ("2.3", "2.4"):
            report = provisional_report()
            report["schema_version"] = version
            self.assertInvalid(report, "rubric_version")
        for field in ("score_status", "score_range", "quality_score_range", "score_coverage_pct", "grade_range"):
            report = provisional_report()
            del report["key_metrics_at_a_glance"][field]
            self.assertInvalid(report, field)
        report = latest_report()
        report["schema_version"] = "2.5"
        self.assertInvalid(report, "rubric_version")

    def test_unknown_ranges_honor_current_caps_and_price_independent_quality(self):
        report = provisional_report()
        mark_unknown(report, "net_yield")
        mark_unknown(report, "visibility")
        report["fundamental_trend"] = "Structural Decline"
        summary = summarize_scorecard(report)
        self.assertEqual(summary["module_ranges"]["visibility"], {"low": 0, "high": 4})
        self.assertGreaterEqual(summary["grade_range"]["best"], "C")
        cheaper = copy.deepcopy(report)
        cheaper["price_used"] = 10
        self.assertEqual(summarize_scorecard(cheaper)["quality_range"], summary["quality_range"])

    def test_bounded_points_span_only_possible_refinement_outcomes(self):
        report = provisional_report()
        row = score_row(report, "buyback_quality")
        bound_module(report, "buyback_quality", [2, 3])
        for met in range(4):
            for unknown in range(4 - met):
                statuses = ["met"] * met + ["unknown"] * unknown + ["not_met"] * (3 - met - unknown)
                for check, status in zip(row["checks"], statuses):
                    check["status"] = status
                interval = summarize_scorecard(report)["module_ranges"]["buyback_quality"]
                possible = [floor + (ceiling - floor) * completed // 3
                            for floor, ceiling in ((5, 7), (2, 4))
                            for completed in range(met, met + unknown + 1)]
                self.assertEqual(interval, {"low": min(possible), "high": max(possible)})


class ArchiveScoreObservationTests(unittest.TestCase):
    def test_five_pinned_reports_reproduce_partial_weight_loss_not_issuer_ratings(self):
        path = Path(__file__).parent / "fixtures" / "archive-score-observations.json"
        corpus = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(corpus["repository"], "Alanjiao1988/Dividendreport")
        self.assertEqual(corpus["source_commit"], "fe03757a49b09cf5edb2bd687aab42109bbbc1b6")
        self.assertEqual(len(corpus["cases"]), 5)
        for case in corpus["cases"]:
            with self.subTest(ticker=case["ticker"]):
                self.assertEqual(case["reported_total_status"], "Not assessed")
                self.assertEqual(set(case["unknown_modules"]), {"net_yield", "cash_coverage"})
                self.assertIn(case["as_of_date"], case["report_path"])
                self.assertTrue(case["visibility_reason"])
                report = provisional_report()
                report["forecast_confidence"] = "Not Forecastable"
                for name in case["unknown_modules"]:
                    mark_unknown(report, name)
                # Replay the archived subtotal only; these are not revalidated rubric-2 bands.
                for name, points in case["reported_quality_points"].items():
                    score_row(report, name)["final_score"] = points
                summary = summarize_scorecard(report)
                known = sum(case["reported_quality_points"].values())
                self.assertEqual(summary["quality_range"], {"low": known, "high": known + 20})
                self.assertEqual(summary["score_range"], {"low": known, "high": known + 29})
                self.assertEqual(summary["evidence_coverage_pct"], 65)
                self.assertEqual(summary["quality_coverage_pct"], 76.47)
                self.assertEqual(summary["status"], "provisional")


if __name__ == "__main__":
    unittest.main()
