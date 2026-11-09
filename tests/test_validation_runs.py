"""Real-company validation runs stay valid and exercise the profile-driven rules."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dividend-income-equity-analysis"
RUNS = ROOT / "validation-runs"
sys.path.insert(0, str(SKILL))

from scripts.render_report import render_report  # noqa: E402
from scripts.validate_analysis import validate_report  # noqa: E402


def load(name):
    return json.loads(next((RUNS).glob(f"*/{name}.analysis.json")).read_text(encoding="utf-8"))


class ValidationRuns(unittest.TestCase):
    def test_runs_validate_and_render(self):
        for name in ("hsbc-0005", "cmport-0144"):
            with self.subTest(run=name):
                report = load(name)
                self.assertEqual(validate_report(report), [])
                self.assertEqual(report["evidence_recovery"]["scope"], "live_research")
                self.assertIn("经济特征档案", render_report(report))

    def test_port_holding_company_rules(self):
        report = load("cmport-0144")
        self.assertEqual(report["economic_profile"]["cash_attribution"], "material_jv_associates")
        self.assertIn("有限期资产到期表", render_report(report))
        no_overlay = copy.deepcopy(report)
        no_overlay["cash_flow_model"]["overlays"] = []
        self.assertTrue(any("holding_company" in e for e in validate_report(no_overlay)))
        harvest = copy.deepcopy(report)
        harvest["valuation_mode"] = "finite_life_harvest"
        self.assertTrue(validate_report(harvest))
        bank_route = copy.deepcopy(report)
        bank_route["valuation_mode"] = "capital_return_based"
        self.assertTrue(validate_report(bank_route))

    def test_scrip_years_use_full_entitlement(self):
        report = load("cmport-0144")
        rows = {row["fiscal_year"]: row for row in report["cash_flow_bridge"]}
        # 2022 cash paid was 941m HKD; coverage must use the 0.82 HKD entitlement on 3,861m shares instead.
        self.assertEqual(rows["2022"]["cash_dividends"], round(0.82 * 3861.103481))


if __name__ == "__main__":
    unittest.main()
