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

    def test_declared_parts_must_add_up(self):
        report = cmport()
        rows(report)["2023"]["entitlement_settled_next_year"] = 2000
        self.assertTrue(any("2023" in e and "declared" in e for e in scrip_coverage_errors(report)))

    def test_cross_year_settlement_reconciles(self):
        report = cmport()
        row = rows(report)["2022"]
        # 941 cash + 2,651 scrip = 2021 final 2,726 + 2022 interim 866
        self.assertEqual(row["cash_paid_dividends"] + row["scrip_settled_dividends"],
                         rows(report)["2021"]["entitlement_settled_next_year"] + row["entitlement_settled_in_year"])
        row["cash_paid_dividends"] = 700
        self.assertTrue(any("settlement_reconciliation" in e for e in scrip_coverage_errors(report)))
        row["settlement_reconciliation"] = "Test: entitlement on shares cancelled before payment."
        self.assertEqual(scrip_coverage_errors(report), [])

    def test_scrip_history_needs_declared_parts(self):
        report = cmport()
        rows(report)["2024"]["entitlement_settled_in_year"] = None
        self.assertTrue(any("entitlement_settled_in_year" in e for e in scrip_coverage_errors(report)))

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
        self.assertEqual(record["timing_basis"], "prior_year_profit")
        self.assertIsNone(record["history"][0]["conversion"])
        self.assertAlmostEqual(record["aggregate_conversion"], (2592 + 2034 + 2716 + 2730) / (7254 + 8112 + 5646 + 6513))
        self.assertLessEqual(record["forecast_conversion"]["Base"], record["aggregate_conversion"])
        self.assertIn("联营及合营公司现金上缴率", render_report(report))

    def test_missing_record_is_rejected(self):
        report = cmport()
        del report["cash_flow_model"]["associate_cash_conversion"]
        self.assertTrue(any("needs cash_flow_model.associate_cash_conversion" in e for e in validate_report(report)))

    def test_best_year_cannot_become_base_without_evidence(self):
        report = cmport()
        forecast = report["cash_flow_model"]["associate_cash_conversion"]["forecast_conversion"]
        forecast["Base"] = 0.42
        self.assertTrue(any("multi-year aggregate" in e for e in associate_conversion_errors(report)))
        forecast["Bull"] = 0.60
        self.assertTrue(any("best historical year" in e for e in associate_conversion_errors(report)))
        record = report["cash_flow_model"]["associate_cash_conversion"]
        record["above_history_evidence"] = {"evidence": "New associate payout policy.", "source_refs": ["not a report source"]}
        self.assertTrue(any("source_refs" in e for e in associate_conversion_errors(report)))
        record["above_history_evidence"]["source_refs"] = [report["sources"][0]]
        self.assertEqual(associate_conversion_errors(report), [])

    def test_ratios_are_recomputed(self):
        report = cmport()
        report["cash_flow_model"]["associate_cash_conversion"]["history"][4]["conversion"] = 0.7
        self.assertTrue(any("2025" in e for e in associate_conversion_errors(report)))

    def test_same_year_timing_inflates_2025(self):
        report = cmport()
        record = report["cash_flow_model"]["associate_cash_conversion"]
        record["history"][0]["conversion"] = 0.4
        self.assertTrue(any("must be null" in e for e in associate_conversion_errors(report)))
        record["timing_basis"] = "same_year"
        for row in record["history"]:
            row["conversion"] = row["cash_dividends_received"] / row["share_of_profit"]
        record["aggregate_conversion"] = (sum(row["cash_dividends_received"] for row in record["history"])
                                          / sum(row["share_of_profit"] for row in record["history"]))
        self.assertEqual(associate_conversion_errors(report), [])
        self.assertGreater(record["history"][4]["conversion"], 0.54)

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


class FiniteLifeTerminal(unittest.TestCase):
    def test_concessions_expire_in_the_terminal(self):
        from scripts.validate_analysis import growth_present_value
        report = cmport()
        growth = report["growth_valuation"]
        self.assertEqual(validate_report(report), [])
        self.assertEqual(growth["terminal_base_fiscal_year"], 2030)
        self.assertEqual({row["name"] for row in growth["terminal_finite_assets"]},
                         {row["name"] for row in report["economic_profile"]["finite_life_assets"]})
        base = next(row for row in growth["scenarios"] if row["scenario"] == "Base")
        _, perpetual = growth_present_value(base["forecast_cash_flows"], base["required_return"], base["terminal_growth"],
                                            base["terminal_net_dps"], base["terminal_time_years"])
        self.assertLess(base["present_value_of_terminal"], perpetual)

    def test_growth_haircut_alone_is_rejected(self):
        report = cmport()
        del report["growth_valuation"]["terminal_finite_assets"]
        self.assertTrue(any("terminal_finite_assets" in e for e in validate_report(report)))

    def test_assets_must_match_profile(self):
        report = cmport()
        report["growth_valuation"]["terminal_finite_assets"][0]["end_year"] = 2060
        self.assertTrue(any("profile end year" in e for e in validate_report(report)))
        renewed = cmport()
        renewed["growth_valuation"]["terminal_finite_assets"][0]["treatment"] = "renewal_evidenced"
        self.assertTrue(any("extension_evidence" in e for e in validate_report(renewed)))

    def test_terminal_value_recomputed(self):
        report = cmport()
        report["growth_valuation"]["scenarios"][1]["present_value_of_terminal"] *= 1.05
        self.assertTrue(any("terminal PV" in e for e in validate_report(report)))


class CurrencyRisk(unittest.TestCase):
    def test_rmb_exposure_is_stressed(self):
        fx = cmport()["fx_risk"]
        self.assertTrue(fx["material_exposure"])
        self.assertEqual({row["kind"] for row in fx["stress_rows"]}, {"fx_only", "combined_bear"})
        self.assertTrue(all(row["stressed_net_cash"] < row["base_net_cash"] for row in fx["stress_rows"]))


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
