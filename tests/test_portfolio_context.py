"""A reused portfolio objective must belong to the research date and scope."""
import copy
import unittest

from scripts.validate_analysis import validate_report
from test_analysis_contract import full_report
from test_income_audit import screen_report


def context():
    return {
        "source": "Fictional user's portfolio instruction dated 2025-12-01",
        "confirmed_on": "2025-12-01", "valid_until": "2026-06-30",
        "account_scope": "Fictional ordinary brokerage income portfolio",
        "investor_tax_basis": "Fictional after-withholding cash investor scenario",
        "income_currency": "HKD", "income_period": "Next full-year recurring cash",
        "applicability_confirmed": True,
        "applicability_evidence": "Fictional current request explicitly reuses the same portfolio and mandate.",
    }


class PortfolioContextTests(unittest.TestCase):
    def portfolio_screen(self):
        report = screen_report()
        report["screening_parameters"].update(target_basis="portfolio_target", portfolio_context=context())
        return report

    def test_dated_percentage_target_needs_no_holdings(self):
        self.assertEqual(validate_report(self.portfolio_screen()), [])

    def test_missing_or_unconfirmed_provenance_cannot_reuse_target(self):
        report = self.portfolio_screen()
        del report["screening_parameters"]["portfolio_context"]
        self.assertTrue(validate_report(report))
        report = self.portfolio_screen()
        report["screening_parameters"]["portfolio_context"]["applicability_confirmed"] = False
        self.assertTrue(validate_report(report))

    def test_expiry_is_checked_for_every_screen_date(self):
        report = self.portfolio_screen()
        later = copy.deepcopy(report["screen_results"][0])
        later.update(ticker="LATER", as_of_date="2026-07-01")
        report["screen_results"].append(later)
        self.assertTrue(any("expired" in error for error in validate_report(report)))

    def test_future_confirmation_and_reversed_validity_fail(self):
        report = self.portfolio_screen()
        report["screening_parameters"]["portfolio_context"]["confirmed_on"] = "2026-02-01"
        self.assertTrue(any("postdate" in error for error in validate_report(report)))
        report["screening_parameters"]["portfolio_context"]["valid_until"] = "2025-11-01"
        self.assertTrue(any("reversed" in error for error in validate_report(report)))

    def test_full_analysis_rejects_expired_target(self):
        report = full_report()
        report["income_assessment"]["target"].update(
            target_net_yield=.05, target_basis="portfolio_target", target_policy="preference", portfolio_context=context())
        report["income_assessment"].update(yield_fit="Pass", income_eligible=True)
        self.assertEqual(validate_report(report), [])
        report["income_assessment"]["target"]["portfolio_context"]["valid_until"] = "2025-12-31"
        self.assertTrue(any("expired" in error for error in validate_report(report)))

    def test_new_explicit_or_unassessed_target_does_not_inherit_context(self):
        self.assertEqual(validate_report(screen_report()), [])
        self.assertEqual(validate_report(screen_report(None)), [])
        report = screen_report()
        report["screening_parameters"]["portfolio_context"] = context()
        self.assertTrue(validate_report(report))

    def test_no_explicit_expiry_does_not_manufacture_a_calendar_limit(self):
        report = self.portfolio_screen()
        report["screening_parameters"]["portfolio_context"]["valid_until"] = None
        self.assertEqual(validate_report(report), [])
