"""Gated income growth credit for the ordinary income ladder (buy-zone.md Section 4.2A)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dividend-income-equity-analysis"
sys.path.insert(0, str(SKILL))

from scripts.decision_rules import stage_prices  # noqa: E402
from scripts.validate_analysis import (  # noqa: E402
    income_growth_credit_errors, ordinary_boundaries, validate_report,
)


def ordinary():
    return json.loads((SKILL / "examples" / "ordinary.analysis.json").read_text(encoding="utf-8"))


def basis(base_cagr=0.03, hist_start=1.0, hist_end=1.2, years=5, bound=0.04, gates=True):
    hist = (hist_end / hist_start) ** (1 / years) - 1
    return {
        "base_dps_cagr_fy1_fy5": base_cagr, "historical_metric": "dps",
        "historical_start_period": "FY2020", "historical_end_period": "FY2025", "historical_years": years,
        "historical_start_value": hist_start, "historical_end_value": hist_end, "historical_cagr": hist,
        "long_run_growth_bound": bound, "long_run_growth_bound_basis": "2% inflation plus 2% real growth",
        "credit_cap": max(0.0, min(0.03, base_cagr, hist, bound)), "gates_passed": gates,
        "explanation": "test",
    }


def growing_runway(cagr=0.03):
    return {(year, "Base"): {"derived_dps": 1.0 * (1 + cagr) ** (year - 1)} for year in range(1, 6)}


def report_with(credit, record, **overrides):
    report = {"valuation_mode": "ordinary_yield_based", "fundamental_trend": "Stable",
              "dividend_safety": "Acceptable", "forecast_confidence": "Medium",
              "value_trap_veto": "Not triggered",
              "return_requirements": {"status": "assessed", "required_total_return_low": 0.08,
                                      "income_growth_credit": credit, "income_growth_credit_basis": record}}
    report.update(overrides)
    return report


class Boundaries(unittest.TestCase):
    def test_credit_lowers_starter_and_add_but_not_strong_buy(self):
        plain = ordinary_boundaries(4, 3.2, 0.08, 0.10)
        credited = ordinary_boundaries(4, 3.2, 0.06, 0.08, credit=0.02)
        self.assertAlmostEqual(credited["fair_upper"], 4 / 0.06)
        self.assertAlmostEqual(credited["accumulation_upper"], 4 / 0.08)
        self.assertAlmostEqual(credited["strong_buy_at_or_below"], plain["strong_buy_at_or_below"])
        self.assertAlmostEqual(credited["accumulation_lower"], 3.2 / 0.10)

    def test_stage_prices_keep_bear_price_without_credit(self):
        report = ordinary()
        report["return_requirements"]["income_growth_credit"] = 0.02
        report["buy_zone"]["required_net_yield_low"] = 0.06
        report["buy_zone"]["required_net_yield_high"] = 0.08
        starter, add, strong = stage_prices(report)
        self.assertAlmostEqual(starter, 4 / 0.06)
        self.assertAlmostEqual(add, 4 / 0.08)
        self.assertAlmostEqual(strong, 3.2 / 0.10)


class Gates(unittest.TestCase):
    def test_passing_case(self):
        self.assertEqual(income_growth_credit_errors(report_with(0.03, basis()), growing_runway(), "ordinary_yield_based"), [])

    def test_cap_is_the_smallest_evidence(self):
        record = basis(bound=0.02)
        errors = income_growth_credit_errors(report_with(0.03, record), growing_runway(), "ordinary_yield_based")
        self.assertTrue(any("exceeds" in e for e in errors))

    def test_falling_history_blocks_credit(self):
        record = basis(hist_start=1.0, hist_end=0.8, gates=False)
        self.assertEqual(record["credit_cap"], 0)
        errors = income_growth_credit_errors(report_with(0.01, record), growing_runway(), "ordinary_yield_based")
        self.assertTrue(errors)
        # Recording the failed test with no credit is valid.
        self.assertEqual(income_growth_credit_errors(report_with(0, record), growing_runway(), "ordinary_yield_based"), [])

    def test_base_cagr_must_match_runway(self):
        errors = income_growth_credit_errors(report_with(0.02, basis(base_cagr=0.03)), growing_runway(0.01),
                                             "ordinary_yield_based")
        self.assertTrue(any("runway" in e for e in errors))

    def test_quality_gates(self):
        for field, value in (("fundamental_trend", "Cyclical Peak"), ("dividend_safety", "Weak"),
                             ("forecast_confidence", "Low"), ("value_trap_veto", "Triggered")):
            report = report_with(0.02, basis(gates=False), **{field: value})
            errors = income_growth_credit_errors(report, growing_runway(), "ordinary_yield_based")
            self.assertTrue(any("only for ordinary_yield_based" in e for e in errors), field)

    def test_other_modes_get_no_credit(self):
        errors = income_growth_credit_errors(report_with(0.02, basis(gates=False)), growing_runway(), "finite_life_harvest")
        self.assertTrue(errors)

    def test_positive_credit_needs_a_record(self):
        errors = income_growth_credit_errors(report_with(0.02, None), growing_runway(), "ordinary_yield_based")
        self.assertTrue(any("needs income_growth_credit_basis" in e for e in errors))


class Integration(unittest.TestCase):
    def test_example_flat_dividend_cannot_take_credit(self):
        report = ordinary()
        returns = report["return_requirements"]
        returns["income_growth_credit"] = 0.01
        returns["income_growth_credit_basis"] = basis(base_cagr=0.0, gates=False)
        errors = validate_report(report)
        self.assertTrue(any("Income growth credit" in e for e in errors))

    def test_zone_rates_must_subtract_the_credit(self):
        report = ordinary()
        report["return_requirements"]["income_growth_credit"] = 0.0
        self.assertEqual(validate_report(report), [])
        bad = copy.deepcopy(report)
        bad["buy_zone"]["required_net_yield_low"] = 0.07
        self.assertTrue(any("income r_low" in e for e in validate_report(bad)))

    def test_schema_caps_credit_at_three_percent(self):
        report = ordinary()
        report["return_requirements"]["income_growth_credit"] = 0.04
        self.assertTrue(validate_report(report))


if __name__ == "__main__":
    unittest.main()
