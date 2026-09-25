"""Keep price-only income restrictions distinct from an evidenced security role."""

import copy
import unittest

from scripts.validate_analysis import validate_report
from test_decision_rules import attach_entry_plan, attach_rating_audit
from test_local_extensions import scoring_fixture
from test_provisional_scoring import mark_unknown


def price_limited_report():
    report = scoring_fixture()
    report["income_assessment"].update(
        target={"target_net_yield": .12, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
        yield_fit="Below target", income_eligible=False, income_price_ceiling=4 / .12,
    )
    attach_entry_plan(report)
    report["portfolio_role"] = report["key_metrics_at_a_glance"]["portfolio_role"] = "Opportunistic"
    report["portfolio_role_assessment"]["rationale"] = (
        "Synthetic non-core opportunity; an otherwise funded thesis, independent of the current price ceiling."
    )
    attach_rating_audit(report)
    return report


class LocalEntryConsistencyTests(unittest.TestCase):
    def test_price_only_shortfall_retains_role_but_not_buy_permission(self):
        report = price_limited_report()
        before = copy.deepcopy(report)
        self.assertEqual(validate_report(report), [])
        self.assertEqual(report, before)
        self.assertEqual(report["portfolio_role"], "Opportunistic")
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_price")
        self.assertEqual(report["action_assessment"]["status"], "diagnostic_only")
        self.assertFalse(report["action_assessment"]["strong_buy_eligible"])
        self.assertAlmostEqual(report["entry_plan"]["stages"][0]["effective_price"], 4 / .12)

    def test_price_only_exception_does_not_authorize_entry(self):
        report = price_limited_report()
        report["action_assessment"]["status"] = "eligible"
        self.assertTrue(validate_report(report))
        report = price_limited_report()
        report["action_assessment"]["strong_buy_eligible"] = True
        self.assertTrue(validate_report(report))

    def test_unknown_tax_cannot_use_price_only_role_exception(self):
        report = price_limited_report()
        report["withholding_rate"] = None
        report["withholding_basis"] = "unknown"
        self.assertTrue(validate_report(report))

    def test_unresolved_capital_cannot_use_price_only_exception(self):
        report = price_limited_report()
        report["cash_flow_model"].update(evidence_status="insufficient", missing_inputs=["Unverified capital access"])
        self.assertTrue(validate_report(report))
        report = price_limited_report()
        report["controller_risk"].update(status="not_assessed", materiality="unknown", material_harm_confirmed=None)
        self.assertTrue(validate_report(report))

    def test_noncritical_missing_module_preserves_price_wait_and_range(self):
        report = price_limited_report()
        mark_unknown(report, "buyback_quality")
        self.assertEqual(validate_report(report), [])
        self.assertEqual(report["entry_plan"]["current_action"], "wait_for_price")
        self.assertEqual(report["portfolio_role"], "Opportunistic")
        self.assertEqual(report["scorecard"]["summary"]["evidence_coverage_pct"], 90)
        self.assertEqual(report["grade"], "B")

    def test_unknown_mandate_is_not_price_only(self):
        report = price_limited_report()
        report["income_assessment"]["income_eligible"] = None
        self.assertTrue(validate_report(report))


if __name__ == "__main__":
    unittest.main()
