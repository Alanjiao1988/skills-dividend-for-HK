"""Capital-return valuation, metric/quote-currency conditions and template-residue checks.

Uses the reproducible HSBC validation run as a real-data regression fixture.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dividend-income-equity-analysis"
RUN = ROOT / "validation-runs" / "2026-11-09-hsbc-0005" / "hsbc-0005.analysis.json"
sys.path.insert(0, str(SKILL))

from scripts.decision_rules import stage_prices  # noqa: E402
from scripts.render_report import render_report  # noqa: E402
from scripts.validate_analysis import validate_report  # noqa: E402


def hsbc():
    return json.loads(RUN.read_text(encoding="utf-8"))


class CapitalDistributionLoop(unittest.TestCase):
    """The RoTE formula must be backed by forecast capital generation (ChatGPT review P1-02)."""

    def test_hsbc_capital_supports_the_formula(self):
        capacity = hsbc()["capital_return_valuation"]["distribution_capacity"]
        base = next(row for row in capacity["scenarios"] if row["scenario"] == "Base")
        self.assertAlmostEqual(base["implied_distribution_ratio"], (0.17 - 0.03) / 0.17)
        self.assertGreaterEqual(base["forecast_distributable_ratio"], base["implied_distribution_ratio"])
        self.assertIn("资本回报能否兑现", render_report(hsbc()))

    def test_formula_beyond_capital_generation_is_rejected(self):
        report = hsbc()
        value = report["capital_return_valuation"]
        for row in value["scenarios"]:
            if row["scenario"] == "Base":
                row["sustainable_return_on_tangible_equity"] = 0.30
        errors = validate_report(report)
        self.assertTrue(any("forecast capital generation supports only" in e for e in errors))

    def test_annual_path_reconciles(self):
        report = hsbc()
        path = report["capital_return_valuation"]["distribution_capacity"]["annual_path"]
        self.assertGreater(path[0]["target_gap_rebuild"], 0)      # 2026 rebuilds CET1 first
        self.assertLess(path[1]["target_gap_rebuild"], 0)         # Basel 3.1 release in 2027
        path[2]["buyback_capacity"] += 1000
        self.assertTrue(any("buyback capacity" in e for e in validate_report(report)))

    def test_capital_release_needs_a_documented_bridge(self):
        report = hsbc()
        capacity = report["capital_return_valuation"]["distribution_capacity"]
        row = capacity["annual_path"][2]
        row["target_gap_rebuild"] -= 20000            # invented release, arithmetic kept consistent
        row["buyback_capacity"] += 20000
        self.assertTrue(any("releases more capital" in e for e in validate_report(report)))
        wrong_year = hsbc()
        wrong_year["capital_return_valuation"]["distribution_capacity"]["annual_path"][0]["fiscal_year"] = "2031"
        self.assertTrue(any("must be fiscal year" in e for e in validate_report(wrong_year)))
        no_bridge = hsbc()
        del no_bridge["capital_return_valuation"]["distribution_capacity"]["capital_ratio_bridge"]
        self.assertTrue(any("capital_ratio_bridge" in e for e in validate_report(no_bridge)))

    def test_release_cannot_come_before_the_rule_takes_effect(self):
        report = hsbc()
        path = report["capital_return_valuation"]["distribution_capacity"]["annual_path"]
        release = path[1]["target_gap_rebuild"]            # move the 2027 Basel release into 2026, totals unchanged
        path[1]["target_gap_rebuild"] = 0; path[1]["buyback_capacity"] += release
        path[0]["target_gap_rebuild"] += release; path[0]["buyback_capacity"] -= release
        errors = validate_report(report)
        self.assertTrue(any("before the regulatory change" in e or "rebuilt" in e for e in errors))

    def test_appendix_rate_sensitivity(self):
        text = render_report(hsbc())
        self.assertIn("±50／±100 个基点", text)
        self.assertIn("单一驱动敏感性", text)

    def test_missing_capacity_is_rejected(self):
        report = hsbc()
        del report["capital_return_valuation"]["distribution_capacity"]
        self.assertTrue(any("distribution_capacity" in e for e in validate_report(report)))

    def test_bdc_cannot_use_the_bank_formula(self):
        report = hsbc()
        report["cash_flow_model"]["sector_model"] = "bdc"
        self.assertTrue(any("fits banks and insurers" in e for e in validate_report(report)))


class CapitalReturnValuation(unittest.TestCase):
    def test_real_bank_run_validates(self):
        report = hsbc()
        self.assertEqual(report["valuation_mode"], "capital_return_based")
        self.assertEqual(validate_report(report), [])

    def test_stage_prices_follow_tangible_book_formula(self):
        report = hsbc()
        value = report["capital_return_valuation"]
        starter, add, strong = stage_prices(report)
        self.assertAlmostEqual(starter, value["base_case_value"] * (1 - value["margin_of_safety"]))
        self.assertAlmostEqual(add, min(starter, value["value_low"]))
        self.assertAlmostEqual(strong, value["value_low"] * (1 - value["margin_of_safety"]))
        base = next(row for row in value["scenarios"] if row["scenario"] == "Base")
        expected = value["book_value_per_share"] * (base["sustainable_return_on_tangible_equity"] - value["long_run_growth"]) \
            / (value["required_return_high"] - value["long_run_growth"])
        self.assertAlmostEqual(base["value_at_required_high"], expected)

    def test_arithmetic_and_guardrails(self):
        report = hsbc()
        report["capital_return_valuation"]["scenarios"][1]["value_at_required_high"] += 1
        self.assertTrue(any("Base value at R_high" in e for e in validate_report(report)))
        report = hsbc()
        report["capital_return_valuation"]["long_run_growth"] = 0.065
        errors = validate_report(report)
        self.assertTrue(any("growth above its documented bound" in e or "exceed growth" in e for e in errors))
        report = hsbc()
        rows = report["capital_return_valuation"]["scenarios"]
        rows[0]["sustainable_return_on_tangible_equity"], rows[2]["sustainable_return_on_tangible_equity"] = 0.19, 0.14
        self.assertTrue(any("rise from Bear to Bull" in e for e in validate_report(report)))

    def test_only_for_balance_sheet_spread_businesses(self):
        report = hsbc()
        for row in report["economic_profile"]["segments"]:
            row["balance_sheet_role"] = "operating"
        report["cash_flow_model"]["sector_model"] = "operating_company"
        self.assertTrue(any("capital_return_based valuation is for balance-sheet spread" in e
                            for e in validate_report(report)))

    def test_record_requires_its_mode(self):
        report = hsbc()
        report["valuation_mode"] = "ordinary_yield_based"
        self.assertTrue(validate_report(report))

    def test_renders_capital_return_table(self):
        self.assertIn("资本回报口径估值", render_report(hsbc()))


class Conditions(unittest.TestCase):
    def test_metric_invalidation_condition(self):
        report = hsbc()
        metrics = [c for c in report["decision"]["invalidation_conditions"] if c["kind"] == "metric"]
        self.assertTrue(metrics)
        self.assertIn("CET1 比率 &lt; 13.5 %", render_report(report))
        metrics[0]["threshold"] = "低于目标"
        self.assertTrue(validate_report(report))

    def test_quote_currency_price_condition(self):
        report = hsbc()
        condition = report["decision"]["buy_conditions"][0]
        self.assertEqual(condition["unit"], "HKD")
        self.assertEqual(validate_report(report), [])
        undeclared = copy.deepcopy(report)
        undeclared["return_requirements"]["quote_currency"] = None
        self.assertTrue(any("quote currency" in e for e in validate_report(undeclared)))
        above = copy.deepcopy(report)
        above["decision"]["buy_conditions"][0]["threshold"] = 150.0  # HKD, above the 137.6 quote
        self.assertTrue(any("specific lower entry price" in e for e in validate_report(above)))


class TemplateResidue(unittest.TestCase):
    def test_live_research_rejects_example_text(self):
        report = hsbc()
        report["controller_risk"]["listed_company_impact"] = "Fictional widely held issuer."
        self.assertTrue(any("template example text" in e for e in validate_report(report)))

    def test_packet_examples_are_exempt(self):
        example = json.loads((SKILL / "examples" / "full-report.analysis.json").read_text(encoding="utf-8"))
        self.assertEqual(example["evidence_recovery"]["scope"], "provided_packet")
        self.assertEqual(validate_report(example), [])


if __name__ == "__main__":
    unittest.main()
