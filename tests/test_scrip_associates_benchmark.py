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
        self.assertTrue(any("source_refs" in e for e in scrip_coverage_errors(report)))  # text alone no longer clears it
        row["settlement_reconciliation"] = {"amount": -100, "reason": "Entitlement on shares cancelled before payment.",
                                            "source_refs": [report["sources"][0]]}
        self.assertTrue(scrip_coverage_errors(report))   # the stated amount must equal the actual gap (-241)
        row["settlement_reconciliation"]["amount"] = -241
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


class ThirdReview(unittest.TestCase):
    """Fixes from the third external review."""

    def test_grouped_concession_uses_earliest_expiry(self):
        report = cmport()
        asset = next(a for a in report["economic_profile"]["finite_life_assets"] if a.get("earliest_end_year"))
        record = next(r for r in report["growth_valuation"]["terminal_finite_assets"] if r["name"] == asset["name"])
        self.assertEqual((asset["end_year"], asset["earliest_end_year"], record["end_year"]), (2049, 2035, 2035))
        record["end_year"] = 2049
        self.assertTrue(any("earliest expiry" in e for e in validate_report(report)))

    def test_cash_model_is_calibrated_on_five_years(self):
        report = cmport()
        bridge = {row["fiscal_year"]: row for row in report["cash_flow_bridge"]}
        base = next(r for r in report["three_year_fundamental_forecast"] if r["scenario"] == "Base" and r["forecast_year"] == 1)
        # Base non-associate cash margin is the FY2021-2025 aggregate, not the 2025 peak.
        margin = (42823 - 13419 - 7532 - 894) / 61073
        assoc = 0.36 * 4970
        self.assertAlmostEqual(base["normalized_ocf"], base["revenue_or_sector_income"] * margin + assoc, places=6)
        self.assertEqual(len(bridge), 5)

    def test_archive_without_new_fields_still_validates(self):
        report = cmport()
        del report["report_contract_version"]            # dated 2026-11-09, before the cutover
        report["report_output"]["sections"] = report["report_output"]["sections"]
        del report["cash_flow_model"]["associate_cash_conversion"]
        del report["return_requirements"]["benchmark_remaining_years"]
        for row in report["cash_flow_bridge"]:
            for key in ("cash_paid_dividends", "scrip_settled_dividends", "dividend_denominator_basis",
                        "entitlement_settled_in_year", "entitlement_settled_next_year", "settlement_reconciliation"):
                row.pop(key, None)
        self.assertEqual(validate_report(report), [])
        strict = cmport()
        del strict["cash_flow_model"]["associate_cash_conversion"]
        self.assertTrue(validate_report(strict))

    def test_tenor_fields_cannot_be_left_blank(self):
        report = cmport()
        report["return_requirements"]["benchmark_remaining_years"] = None
        self.assertTrue(any("benchmark_remaining_years" in e for e in validate_report(report)))

    def test_explicit_legacy_contract_beats_the_date(self):
        from scripts.validate_analysis import new_contract
        self.assertFalse(new_contract({"report_contract_version": "six_section_legacy", "as_of_date": "2027-01-01"}))
        self.assertTrue(new_contract({"report_contract_version": "twelve_chapter", "as_of_date": "2024-01-01"}))
        self.assertTrue(new_contract({"as_of_date": "2026-11-10"}))
        report = cmport()
        report["report_contract_version"] = "six_section_legacy"
        report["as_of_date"] = "2026-11-12"
        self.assertTrue(any("cannot declare" in e for e in validate_report(report)))   # creation rule for live research

    def test_tenor_and_freshness(self):
        report = cmport()
        report["return_requirements"]["benchmark_remaining_years"] = 5
        self.assertTrue(any("target tenor" in e for e in validate_report(report)))
        stale = cmport()
        stale["return_requirements"]["benchmark_date"] = "2026-08-01"
        self.assertTrue(any("days old" in e for e in validate_report(stale)))

    def test_appendix_slots_are_all_present(self):
        text = render_report(cmport())
        for number in range(1, 14):
            self.assertIn(f"<h3>A{number} ", text)
        self.assertNotIn("A14", text)
        self.assertIn("<h3>术语表</h3>", text)


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


class YearFormatting(unittest.TestCase):
    def test_amounts_keep_separators_and_year_columns_do_not(self):
        from scripts.render_report import render_table
        text = render_table({"title": "t", "columns": ["财年", "到期年", "联营股息"], "rows": [["2023", 2046, 2034]], "note": "n"})
        self.assertIn(">2046<", text)
        self.assertIn(">2,034<", text)
