"""Scrip-year coverage basis, associate cash conversion and matching-currency risk-free checks."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dividend-income-equity-analysis"
sys.path.insert(0, str(SKILL))

from scripts.render_report import render_report  # noqa: E402
from scripts.validate_analysis import (  # noqa: E402
    associate_conversion_errors, scrip_coverage_errors, validate_report,
)


def cmport():
    path = next((ROOT / "validation-runs").glob("*/cmport-0144.analysis.json"))
    return json.loads(path.read_text(encoding="utf-8"))


def rows(report):
    return {row["fiscal_year"]: row for row in report["cash_flow_bridge"]}


class ScripCoverage(unittest.TestCase):
    def test_recorded_scrip_years_pass(self):
        report = cmport()
        self.assertEqual(scrip_coverage_errors(report), [])
        self.assertGreater(report["scrip_drip"]["historical_participation_rate"], 0)
        self.assertEqual(rows(report)["2022"]["scrip_settled_dividends"], 2651)

    def test_cash_paid_denominator_is_rejected_in_a_scrip_year(self):
        report = cmport()
        row = rows(report)["2022"]
        row["cash_dividends"] = row["cash_paid_dividends"]
        self.assertTrue(any("must be the full entitlement" in e for e in scrip_coverage_errors(report)))
        row["dividend_denominator_basis"] = "cash_paid"
        self.assertTrue(any("full_entitlement" in e for e in scrip_coverage_errors(report)))

    def test_scrip_history_needs_every_row_recorded(self):
        report = cmport()
        del rows(report)["2024"]["scrip_settled_dividends"]
        self.assertTrue(any("2024" in e and "scrip_settled_dividends" in e for e in scrip_coverage_errors(report)))

    def test_scrip_year_needs_cash_paid(self):
        report = cmport()
        rows(report)["2021"]["cash_paid_dividends"] = None
        self.assertTrue(any("cash_paid_dividends" in e for e in scrip_coverage_errors(report)))

    def test_no_scrip_history_needs_no_fields(self):
        example = json.loads((SKILL / "examples" / "ordinary.analysis.json").read_text(encoding="utf-8"))
        self.assertEqual(scrip_coverage_errors(example), [])

    def test_appendix_shows_scrip_columns(self):
        self.assertIn("<th scope=\"col\">以股代息</th>", render_report(cmport()))


class AssociateConversion(unittest.TestCase):
    def test_record_reconciles_and_renders(self):
        report = cmport()
        record = report["cash_flow_model"]["associate_cash_conversion"]
        self.assertEqual(associate_conversion_errors(report), [])
        self.assertAlmostEqual(record["aggregate_conversion"], 13419 / 32495)
        self.assertLessEqual(record["forecast_conversion"]["Base"], record["aggregate_conversion"])
        self.assertIn("联营及合营公司现金上缴率", render_report(report))

    def test_missing_record_is_rejected(self):
        report = cmport()
        del report["cash_flow_model"]["associate_cash_conversion"]
        self.assertTrue(any("needs cash_flow_model.associate_cash_conversion" in e for e in validate_report(report)))

    def test_best_year_cannot_become_base_without_evidence(self):
        report = cmport()
        forecast = report["cash_flow_model"]["associate_cash_conversion"]["forecast_conversion"]
        forecast["Base"] = 0.549
        self.assertTrue(any("multi-year aggregate" in e for e in associate_conversion_errors(report)))
        forecast["Bull"] = 0.60
        self.assertTrue(any("best historical year" in e for e in associate_conversion_errors(report)))
        report["cash_flow_model"]["associate_cash_conversion"]["above_history_evidence"] = "New associate payout policy."
        self.assertEqual(associate_conversion_errors(report), [])

    def test_ratios_are_recomputed(self):
        report = cmport()
        report["cash_flow_model"]["associate_cash_conversion"]["history"][4]["conversion"] = 0.7
        self.assertTrue(any("2025" in e for e in associate_conversion_errors(report)))

    def test_prior_year_timing(self):
        report = cmport()
        record = report["cash_flow_model"]["associate_cash_conversion"]
        record["timing_basis"] = "prior_year_profit"
        history = record["history"]
        history[0]["conversion"] = None
        for prev, row in zip(history, history[1:]):
            row["conversion"] = row["cash_dividends_received"] / prev["share_of_profit"]
        received = sum(row["cash_dividends_received"] for row in history[1:])
        record["aggregate_conversion"] = received / sum(row["share_of_profit"] for row in history[:-1])
        record["forecast_conversion"] = {"Bear": 0.25, "Base": 0.35, "Bull": 0.45}
        self.assertEqual(associate_conversion_errors(report), [])
        history[0]["conversion"] = 0.4
        self.assertTrue(any("must be null" in e for e in associate_conversion_errors(report)))

    def test_too_short_history_fails_schema(self):
        report = cmport()
        report["cash_flow_model"]["associate_cash_conversion"]["history"] = \
            report["cash_flow_model"]["associate_cash_conversion"]["history"][:2]
        self.assertTrue(validate_report(report))

    def test_other_profiles_need_no_record(self):
        report = cmport()
        report["economic_profile"]["cash_attribution"] = "wholly_owned"
        del report["cash_flow_model"]["associate_cash_conversion"]
        self.assertEqual(associate_conversion_errors(report), [])


class MatchingCurrencyBenchmark(unittest.TestCase):
    def test_hkd_valuation_uses_hkd_government_bond(self):
        returns = cmport()["return_requirements"]
        self.assertEqual(returns["benchmark_currency"], returns["valuation_currency"])
        self.assertIn("api.hkma.gov.hk", returns["benchmark_source"])

    def test_currency_mismatch_needs_a_basis(self):
        report = cmport()
        report["return_requirements"]["benchmark_currency"] = "USD"
        self.assertTrue(any("benchmark_currency_basis" in e for e in validate_report(report)))
        fixed = copy.deepcopy(report)
        fixed["return_requirements"]["benchmark_currency_basis"] = (
            "HKMA series unavailable on the analysis date; US 10-year used under the linked exchange rate.")
        self.assertFalse(any("benchmark_currency_basis" in e for e in validate_report(fixed)))


if __name__ == "__main__":
    unittest.main()
