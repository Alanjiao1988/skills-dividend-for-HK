"""Paired regressions for cash eligibility, evidence and early terminal paths."""

import unittest

from scripts.validate_analysis import ordinary_boundaries, validate_report
from test_analysis_contract import EVIDENCE, full_report, refresh_growth_pv


def strong_buy_report():
    report = full_report()
    report["price_used"] = 30
    report["income_assessment"]["forward_net_yield"] = 4 / 30
    report["forecast_confidence"] = "High"
    report["dividend_safety"] = "Strong"
    report["action_assessment"]["strong_buy_eligible"] = True
    return report


def early_terminal_report(horizon=3):
    report = full_report(growth=True)
    growth = report["growth_valuation"]
    growth["explicit_horizon_years"] = horizon
    for scenario in growth["scenarios"]:
        scenario["forecast_cash_flows"] = scenario["forecast_cash_flows"][:horizon]
        scenario["terminal_time_years"] = horizon
        scenario["terminal_net_dps"] = scenario["forecast_cash_flows"][-1]["net_dps"] * 1.02
        next_forecast = next(row for row in report["forecast_extension"]
                             if row["forecast_year"] == horizon + 1 and row["scenario"] == scenario["scenario"])
        next_dividend = next(row for row in report["dividend_and_yield_runway"]
                             if row["forecast_year"] == horizon + 1 and row["scenario"] == scenario["scenario"])
        funding = scenario["terminal_funding"]
        funding.update(owner_cash_or_proxy=next_forecast["fcf_or_distributable_cash"],
                       remaining_growth_uses=next_forecast["remaining_growth_investment"],
                       remaining_mandatory_uses=next_forecast["fcf_or_distributable_cash"]
                       - next_forecast["remaining_growth_investment"] - next_forecast["recurring_fad"],
                       recurring_fad=next_forecast["recurring_fad"])
        for key in ("dividend_entitlement", "dividend_cash_cost", "dividend_entitled_shares",
                    "cash_settled_fraction", "settlement_cash_adjustment"):
            funding[key] = next_dividend[key]
    refresh_growth_pv(report)
    return report


class EntryGateTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_supported_withholding_preserves_strong_buy(self):
        for basis in ("broker_observed", "company_announcement", "legal_structure"):
            with self.subTest(basis=basis):
                report = strong_buy_report()
                report["withholding_basis"] = basis
                self.assertValid(report)

    def test_unknown_or_assumed_withholding_cannot_support_entry(self):
        for rate, basis in ((None, "unknown"), (0, "unknown"), (None, "company_announcement"), (0, "market_default")):
            with self.subTest(rate=rate, basis=basis):
                report = strong_buy_report()
                report.update(withholding_rate=rate, withholding_basis=basis)
                self.assertInvalid(report, "Unverified withholding")
                report["action_assessment"].update(status="diagnostic_only", strong_buy_eligible=False)
                self.assertValid(report)
                report["portfolio_role"] = report["key_metrics_at_a_glance"]["portfolio_role"] = "Core income"
                self.assertInvalid(report, "Unverified withholding")

    def test_withholding_basis_cannot_be_omitted(self):
        report = full_report()
        del report["withholding_basis"]
        self.assertInvalid(report, "withholding_basis")

    def test_unverified_tax_cannot_pass_income_floor_in_diagnostic_report(self):
        report = full_report()
        report["withholding_basis"] = "unknown"
        report["action_assessment"]["status"] = "diagnostic_only"
        report["income_assessment"].update(
            target={"target_net_yield": 0.05, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
            yield_fit="Pass", income_eligible=True, income_price_ceiling=80,
        )
        self.assertInvalid(report, "Unverified withholding cannot establish income eligibility")
        report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None,
                                           income_price_ceiling=None, yield_fit="Not Assessed", income_eligible=None)
        self.assertValid(report)

    def test_growth_also_requires_supported_tax(self):
        report = full_report(growth=True)
        report["withholding_basis"] = "unknown"
        self.assertInvalid(report, "Growth valuation requires supported cash election and withholding")

    def test_mandatory_stock_cannot_pass_cash_floor_or_strong_buy(self):
        for growth in (False, True):
            with self.subTest(growth=growth):
                report = full_report(growth=True) if growth else strong_buy_report()
                report["scrip_drip"].update(available="Yes", cash_election_available="No",
                                           default_election="shares", investor_cash_yield_assumption="mandatory_shares",
                                           expected_participation_rate=1)
                for row in report["dividend_and_yield_runway"]:
                    row.update(cash_settled_fraction=0, dividend_cash_cost=0)
                self.assertInvalid(report, "requires suspended cash-dividend valuation")
                self.assertInvalid(report, "No supported investor cash election")

    def test_mandatory_stock_can_be_reported_as_suspended_without_cash(self):
        report = full_report()
        report.pop("buy_zone")
        report["valuation_mode"] = report["key_metrics_at_a_glance"]["valuation_mode"] = "suspended"
        report["action_assessment"]["status"] = "suspended"
        report["scrip_drip"].update(available="Yes", cash_election_available="No",
                                   default_election="shares", investor_cash_yield_assumption="mandatory_shares")
        for row in report["dividend_and_yield_runway"]:
            row.update(derived_dps=0, dividend_entitlement=0, dividend_cash_cost=0, cash_settled_fraction=0,
                       policy_adjustment_reason="Stock-only distribution excluded from cash income; see scrip evidence.")
        report["income_assessment"].update(
            target={"target_net_yield": 0.1, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
            forward_net_dps=0, forward_net_yield=0, income_price_ceiling=0,
            yield_fit="Below target", income_eligible=False,
        )
        self.assertValid(report)

    def test_no_cash_option_cannot_be_overridden_by_all_cash_label(self):
        report = full_report()
        report["scrip_drip"].update(available="Yes", cash_election_available="No")
        self.assertInvalid(report, "requires suspended cash-dividend valuation")

    def test_plain_cash_with_no_election_scheme_is_supported(self):
        report = strong_buy_report()
        report["scrip_drip"].update(cash_election_available="Not Applicable",
                                   investor_cash_yield_assumption="not_applicable",
                                   default_election="not_applicable")
        self.assertValid(report)

    def test_optional_scrip_keeps_cash_election_value(self):
        for growth in (False, True):
            with self.subTest(growth=growth):
                report = full_report(growth=growth)
                report["scrip_drip"].update(available="Yes", expected_participation_rate=0.4)
                for row in report["dividend_and_yield_runway"]:
                    row.update(cash_settled_fraction=0.6, dividend_cash_cost=row["dividend_entitlement"] * 0.6)
                self.assertValid(report)
                self.assertEqual(report["income_assessment"]["forward_net_dps"], 4)

    def test_unknown_cash_or_share_election_cannot_claim_spendable_income(self):
        for assumption, option in (("unknown", "Unknown"), ("share_election", "Yes")):
            with self.subTest(assumption=assumption):
                report = full_report()
                report["scrip_drip"].update(available="Yes", cash_election_available=option,
                                           investor_cash_yield_assumption=assumption)
                self.assertInvalid(report, "No supported investor cash election")
                report["income_assessment"].update(forward_net_dps=None, forward_net_yield=None)
                report["action_assessment"]["status"] = "diagnostic_only"
                self.assertValid(report)

    def test_non_evidenced_normalization_is_diagnostic_across_bases(self):
        for basis in ("three_year_base_average", "mid_cycle"):
            for source in ("illustrative", "historical_fallback", "unknown"):
                with self.subTest(basis=basis, source=source):
                    report = strong_buy_report()
                    report["buy_zone"]["normalized_net_dps_basis"] = basis
                    report["dividend_and_yield_runway"][1]["dps_source"] = source
                    self.assertInvalid(report, "diagnostic only")
                    report["action_assessment"].update(status="diagnostic_only", strong_buy_eligible=False)
                    report["buy_zone"]["normalization_evidence"]["operating_cash"].update(
                        status="missing", source_refs=[],
                        input_detail="No sourced volume/margin/working-capital path supports the illustrative DPS.",
                        resolution_source="Operating guidance and annual-report cash-flow reconciliation",
                        consequence="The Base-average N remains illustrative, not actionable.",
                    )
                    self.assertValid(report)

    def test_evidenced_base_average_can_remain_actionable(self):
        report = strong_buy_report()
        report["buy_zone"]["normalized_net_dps_basis"] = "three_year_base_average"
        self.assertValid(report)

    def test_hard_income_gate_is_shared_by_ordinary_and_growth_entry(self):
        for growth in (False, True):
            with self.subTest(growth=growth):
                report = full_report(growth=growth)
                report["income_assessment"].update(
                    target={"target_net_yield": 0.12, "target_basis": "user_explicit", "target_policy": "hard_minimum"},
                    yield_fit="Below target", income_eligible=False, income_price_ceiling=4 / 0.12,
                )
                self.assertInvalid(report, "confirmed hard-income eligibility")
                report["action_assessment"]["status"] = "diagnostic_only"
                self.assertValid(report)

    def test_steady_early_terminal_paths_are_supported(self):
        for horizon in (3, 4):
            with self.subTest(horizon=horizon):
                self.assertValid(early_terminal_report(horizon))

    def test_early_terminal_cannot_ignore_later_dividend_reset(self):
        report = early_terminal_report()
        self.assertValid(report)
        for row in report["dividend_and_yield_runway"]:
            if row["forecast_year"] == 5:
                for field in ("dividend_entitlement", "dividend_cash_cost", "derived_dps"):
                    row[field] *= 0.1
                row["policy_adjustment_reason"] = "Permanent board payout reset in FY2030."
        self.assertInvalid(report, "year 5 early terminal path")

    def test_early_terminal_checks_per_share_dilution(self):
        report = early_terminal_report()
        row = report["dividend_and_yield_runway"][-2]
        row["dividend_entitled_shares"] *= 2
        row["derived_dps"] /= 2
        self.assertInvalid(report, "year 5 early terminal path")

    def test_early_terminal_requires_evidenced_later_dividends(self):
        report = early_terminal_report()
        report["dividend_and_yield_runway"][-2]["dps_source"] = "illustrative"
        self.assertInvalid(report, "illustrative DPS cannot enter growth value")

    def test_early_terminal_uses_quote_unit_and_adr_conversion_once(self):
        report = early_terminal_report()
        report["return_requirements"].update(valuation_unit_scale=0.01, shares_per_quoted_security=2)
        report["price_used"] *= 200
        report["income_assessment"]["forward_net_dps"] *= 200
        report["buy_zone"].update(normalized_net_dps=800, bear_net_dps=640,
                                   boundaries=ordinary_boundaries(800, 640, 0.08, 0.1))
        for scenario in report["growth_valuation"]["scenarios"]:
            scenario["terminal_net_dps"] *= 200
            for cash in scenario["forecast_cash_flows"]:
                cash["net_dps"] *= 200
        refresh_growth_pv(report)
        self.assertValid(report)

    def test_explicit_transition_can_capture_permanent_payout_reset(self):
        report = full_report(growth=True)
        growth = report["growth_valuation"]
        original_value = growth["base_case_value"]
        growth.update(explicit_horizon_years=3, transition_years=2)
        for row in report["dividend_and_yield_runway"]:
            if row["forecast_year"] == 5:
                for field in ("dividend_entitlement", "dividend_cash_cost", "derived_dps"):
                    row[field] *= 0.1
                row["policy_adjustment_reason"] = EVIDENCE + " Permanent FY2030 payout reset."
        for scenario in growth["scenarios"]:
            scenario["forecast_cash_flows"][-1]["net_dps"] *= 0.1
            scenario["terminal_net_dps"] *= 0.1
            for field in ("dividend_entitlement", "dividend_cash_cost"):
                scenario["terminal_funding"][field] *= 0.1
        refresh_growth_pv(report)
        self.assertValid(report)
        self.assertLess(growth["base_case_value"], original_value)


if __name__ == "__main__":
    unittest.main()
