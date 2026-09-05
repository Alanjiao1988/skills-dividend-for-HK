import copy
import math
import unittest
from pathlib import Path

from scripts.validate_analysis import (
    aggregate_coverage,
    distribution_capacity,
    growth_present_value,
    ordinary_boundaries,
    schema_validator,
    validate_report,
)


EVIDENCE = "Synthetic invariant fixture; not market data or a company recommendation."


def full_report(growth=False):
    history = []
    for index, year in enumerate(range(2021, 2026)):
        recurring = 50 + index * 10
        actual = [45, 55, 65, 75, 35][index]
        history.append({
            "fiscal_year": str(year), "fiscal_year_end": f"{year}-12-31", "recurring_owner_fcf_or_proxy": recurring + 10,
            "recurring_fad": recurring, "actual_all_in_fcf": actual,
            "actual_distribution_capacity": actual, "cash_dividends": 40,
            "fcf_dividend_coverage": recurring / 40, "actual_cash_coverage": actual / 40,
            "evidence_status": "reported_reconciled", "funding_source": "Operating FCF",
        })
    forecasts, bridges, runway = [], [], []
    for year in range(1, 6):
        for scenario, scale in (("Bear", 0.8), ("Base", 1), ("Bull", 1.2)):
            scale *= 1.02 ** (year - 1) if growth else 1
            shared = {"fiscal_year": str(2025 + year), "forecast_year": year, "scenario": scenario}
            forecasts.append({
                **shared, "primary_driver_name": "Volume", "primary_driver_assumption": EVIDENCE,
                "revenue_or_sector_income": 500 * scale, "net_income_or_affo": 100 * scale,
                "operating_cash_flow": 130 * scale, "normalized_ocf": 130 * scale,
                "maintenance_capex": 20 * scale, "other_owner_claims": 10 * scale,
                "remaining_growth_investment": 20 * scale, "fcf_or_distributable_cash": 100 * scale,
                "nonrecurring_operating_cash_inflow": 0,
                "actual_all_in_fcf": 75 * scale, "recurring_fad": 75 * scale,
                "estimate_status": "estimated", "forecast_confidence": "Medium",
                "assumption_basis": "analyst_estimate", "evidence_and_limitations": EVIDENCE,
            })
            bridges.append({
                **shared, "fcf_or_capital_generation": 100 * scale,
                "required_reinvestment": 20 * scale, "mandatory_debt_or_regulatory_uses": 5 * scale,
                "recurring_fad": 75 * scale, "exceptional_cash_uses": 5 * scale, "excess_cash_used": 0,
                "cash_available_for_distribution": 70 * scale, "diluted_share_count": 10,
                "deduction_ledger": [
                    {"item": "Growth", "category": "growth", "amount": 20 * scale, "already_in_starting_metric": False,
                     "incremental_deduction": 20 * scale, "evidence": EVIDENCE},
                    {"item": "Maintenance already in owner cash", "category": "maintenance", "amount": 20 * scale,
                     "already_in_starting_metric": True, "incremental_deduction": 0, "evidence": EVIDENCE},
                    {"item": "Mandatory", "category": "mandatory", "amount": 5 * scale,
                     "already_in_starting_metric": False, "incremental_deduction": 5 * scale, "evidence": EVIDENCE},
                    {"item": "Exceptional", "category": "exceptional", "amount": 5 * scale,
                     "already_in_starting_metric": False, "incremental_deduction": 5 * scale, "evidence": EVIDENCE},
                ],
                "forecast_confidence": "Medium", "evidence_and_limitations": EVIDENCE,
            })
            runway.append({
                **shared, "cash_available_for_distribution": 70 * scale,
                "payout_policy": "earnings_linked", "payout_calculation_basis": "attributable_earnings",
                "payout_base_reference": "net_income_or_affo", "payout_base_adjustments": [], "policy_components": [],
                "payout_base_amount": 100 * scale, "payout_ratio": 0.4,
                "policy_implied_dividend": 40 * scale, "policy_adjustment_reason": "No adjustment needed.",
                "dividend_cash_cost": 40 * scale, "dividend_entitled_shares": 10,
                "share_count_reconciliation": EVIDENCE, "derived_dps": 4 * scale,
                "funding_gap": 0, "dps_source": "evidence_backed",
            })
    mode = "total_return_based" if growth else "ordinary_yield_based"
    cumulative = [{
        "scenario": scenario,
        "three_year": sum(row["recurring_fad"] for row in forecasts if row["scenario"] == scenario and row["forecast_year"] <= 3),
        "five_year": sum(row["recurring_fad"] for row in forecasts if row["scenario"] == scenario),
        "limitations": EVIDENCE,
    } for scenario in ("Bear", "Base", "Bull")]
    report = {
        "schema_version": "2.0", "mode": "full_analysis", "company": "Synthetic",
        "ticker": "EXAMPLE", "exchange": "Example", "as_of_date": "2026-01-01", "price_used": 40,
        "withholding_rate": 0,
        "key_metrics_at_a_glance": {
            "ttm_net_yield": 0.1, "normalized_net_yield": 0.1, "score_100": 75,
            "grade": "B", "portfolio_role": "Watchlist", "valuation_mode": mode,
        },
        "dividend_snapshot": {
            "ttm_dps": 4, "ttm_net_yield": 0.1, "normalized_net_dps": 4,
            "coverage_status": "Strong", "history_coverage_years": 5,
        },
        "five_year_dividend_history": [
            {"fiscal_year": str(year), "coverage_label": "Strong", "quality_tag": "Stable"}
            for year in range(2021, 2026)
        ],
        "cash_flow_bridge": history,
        "cash_flow_model": {
            "sector_model": "operating_company", "overlays": [], "starting_metric": "Reported OCF",
            "owner_perimeter": "Ordinary parent owners", "financial_currency": "USD",
            "cash_unit_scale": 1000000, "share_unit_scale": 1000000,
            "evidence_status": "reported_reconciled", "proxy_reconciliation": EVIDENCE,
            "capital_and_remittance_evidence": EVIDENCE, "deduction_ledger": [],
            "missing_inputs": [], "sources": [EVIDENCE],
        },
        "coverage_summary": {
            "dividend_basis": "ordinary_cash_paid", "comparison_basis": EVIDENCE,
            "fiscal_years": [str(year) for year in range(2021, 2026)], "years_available": 5,
            "three_year_recurring_coverage": 2, "five_year_worst_recurring_coverage": 1.25,
            "worst_available_recurring_coverage": 1.25, "worst_recurring_year": "2021",
            "worst_actual_coverage": 0.875, "worst_actual_year": "2025",
            "shortfall_funding_and_limitations": "Exceptional cash use remained a real liquidity cost.",
        },
        "business_outlook": {
            "horizon_years": 5, "data_cutoff": "2026-01-01", "competitive_position": EVIDENCE,
            "management_execution": EVIDENCE,
            "drivers": [{
                "driver": driver, "segment": "Example", "baseline": EVIDENCE,
                "year_three_outcome": EVIDENCE, "year_five_outcome": EVIDENCE,
                "investment_and_funding": EVIDENCE, "fcf_transmission": EVIDENCE,
                "evidence_type": "analyst_estimate", "source_and_date": EVIDENCE,
                "confidence": "Medium", "invalidation_signal": EVIDENCE,
            } for driver in ("Volume", "Margin", "Maintenance")],
            "scenario_theses": dict.fromkeys(("Bear", "Base", "Bull"), EVIDENCE),
            "fcf_change_decomposition": EVIDENCE, "per_share_cash_outlook": EVIDENCE,
            "liquidity_and_self_funding": EVIDENCE, "cumulative_fad": cumulative,
            "extension_limitations": EVIDENCE,
            "milestones": [{
                "event": "Capacity starts", "due_period": "2027",
                "observable_threshold": EVIDENCE, "source_to_revisit": EVIDENCE,
                "fcf_implication": EVIDENCE, "action_if_missed": "Rebuild if structural.",
            }],
        },
        "payout_policy": {
            "policy_type": "earnings_linked", "calculation_basis": "attributable_earnings",
            "basis_definition": EVIDENCE, "reported_payout_ratio": 0.4,
            "source_and_date": EVIDENCE, "funding_constraint": EVIDENCE,
        },
        "return_requirements": {
            "status": "assessed", "benchmark": "Synthetic benchmark", "benchmark_source": EVIDENCE,
            "benchmark_date": "2026-01-01", "benchmark_currency": "USD", "benchmark_tenor": "20 years",
            "valuation_currency": "USD", "valuation_unit_scale": 1, "shares_per_quoted_security": 1,
            "tax_and_fx_basis": EVIDENCE, "rate_basis": "nominal",
            "risk_free_rate": 0.04, "risk_premium_low": 0.04, "risk_premium_high": 0.06,
            "required_total_return_low": 0.08, "required_total_return_high": 0.10,
            "price_independent_risk_factors": [EVIDENCE], "price_independent": True,
            "income_growth_credit": 0, "limitations": EVIDENCE,
        },
        "income_assessment": {
            "target": {"target_net_yield": None, "target_basis": "not_assessed", "target_policy": "not_assessed"},
            "forward_net_yield": 0.1, "forward_net_dps": 4, "income_period": "FY2026 full year",
            "income_price_ceiling": None, "yield_fit": "Not Assessed", "income_eligible": None, "reason": EVIDENCE,
        },
        "growth_assessment": {
            "status": "eligible" if growth else "not_assessed", "funded_dividend_path": growth,
            "reinvestment_to_dps_reconciled": growth, "capital_remittance_verified": growth,
            "credible_terminal_state": growth,
            "growth_method": "direct_operating_to_dps" if growth else "not_assessed",
            "evidence_and_reason": EVIDENCE,
        },
        "holding_review": {
            "action": "not_assessed", "rationale": EVIDENCE, "portfolio_inputs_available": False,
            "position_change_fraction": None, "missing_inputs": ["Holdings"], "next_review": "Next results",
            "automatic_trade": False, "switch_analysis": None,
            "triggers": [{"category": "valuation", "threshold": "Review, not an order.",
                          "evidence": EVIDENCE, "research_action": "review"}],
        },
        "scrip_drip": {
            "available": "No", "cash_election_available": "Yes", "default_election": "cash",
            "historical_participation_rate": 0, "expected_participation_rate": 0,
            "expected_dilution_rate": 0, "buyback_offset_rate": 0, "net_unoffset_dilution_rate": 0,
            "investor_cash_yield_assumption": "all_cash_election",
        },
        "fundamental_trend": "Stable", "forecast_confidence": "Medium", "valuation_mode": mode,
        "value_trap_veto": "Not triggered", "valuation_reason": EVIDENCE,
        "structural_decline_cap_applied": False, "harvest_managed_runoff_exception_applied": False,
        "business_fundamentals": {
            "dividend_funding_engine": EVIDENCE,
            "core_operating_drivers": ["Volume", "Margin", "Maintenance"], "historical_operating_trend": [],
        },
        "three_year_fundamental_forecast": forecasts[:9], "forecast_extension": forecasts[9:],
        "driver_sensitivity": [{
            "driver_name": "One-year cash loss", "driver_change": "-1", "sensitivity_type": "transient",
            "n_reestimated": False, "revised_n": None, "accumulation_upper_bound_change": None,
            "growth_value_change": None, "growth_cash_delta_audit": [],
            "boundary_effect": "N/A", "sensitivity_basis": "calculated",
        }],
        "dividend_forecast_bridge": bridges, "dividend_and_yield_runway": runway,
        "buy_zone": {
            "normalized_net_dps": 4, "normalized_net_dps_basis": "mid_cycle",
            "normalized_net_dps_source_period": "Explicit normalized model",
            "normalization_adjustments": [EVIDENCE], "bear_net_dps": 3.2, "bear_net_dps_source": EVIDENCE,
            "dps_currency": "USD", "normalization_fx_rate": 1, "normalization_fx_basis": EVIDENCE,
            "normalization_cash_deductions": 0,
            "required_net_yield_low": 0.08, "required_net_yield_high": 0.10,
            "too_expensive_zone": ">50", "fair_value_zone": "(40, 50]",
            "accumulation_zone": "(32, 40]", "strong_buy_zone": "<=32",
            "value_trap_veto": "Not triggered", "boundaries": ordinary_boundaries(4, 3.2, 0.08, 0.10),
        },
        "rendering": {"rich_visualization_available": False, "visual_mode": "plain_text_fallback", "charts_required": []},
        "visual_summary": dict.fromkeys(("business_and_fcf_trend", "dps_path", "yield_normalization",
                                         "main_driver_sensitivity", "valuation_summary", "coverage_labels"), EVIDENCE),
        "score_100": 75, "score_limitations": EVIDENCE, "grade": "B",
        "dividend_quality": "Medium", "dividend_safety": "Acceptable", "withholding_efficiency": "High",
        "buyback_quality": "Neutral", "three_year_outlook": "Stable", "portfolio_role": "Watchlist",
        "sources": [EVIDENCE],
    }
    if growth:
        attach_growth_values(report)
    return report


def attach_growth_values(report):
    rows = []
    for scenario, rate in (("Bear", 0.10), ("Base", 0.09), ("Bull", 0.08)):
        path = [{
            "forecast_year": row["forecast_year"], "years_from_valuation": row["forecast_year"],
            "net_dps": row["derived_dps"], "cash_fraction": 1, "fx_to_valuation_currency": 1,
            "investor_cash_deductions": 0,
            "cash_timing_and_fx_evidence": EVIDENCE,
        } for row in report["dividend_and_yield_runway"] if row["scenario"] == scenario]
        terminal_dps = path[-1]["net_dps"] * 1.02
        terminal_scale = terminal_dps / 4
        explicit, terminal = growth_present_value(path, rate, 0.02, terminal_dps, 5)
        rows.append({
            "scenario": scenario, "required_return": rate, "required_return_basis": EVIDENCE,
            "terminal_growth": 0.02, "sustainable_terminal_growth_bound": 0.03,
            "terminal_net_dps": terminal_dps, "terminal_time_years": 5,
            "terminal_funding_and_fade_evidence": EVIDENCE, "forecast_cash_flows": path,
            "terminal_funding": {
                "owner_cash_or_proxy": 100 * terminal_scale, "remaining_growth_uses": 20 * terminal_scale,
                "remaining_mandatory_uses": 5 * terminal_scale, "recurring_fad": 75 * terminal_scale,
                "dividend_cash_cost": 40 * terminal_scale, "dividend_entitled_shares": 10,
                "fx_to_valuation_currency": 1, "investor_cash_deductions": 0,
            },
            "present_value_of_dividends": explicit, "present_value_of_terminal": terminal,
            "total_value": explicit + terminal, "terminal_value_share": terminal / (explicit + terminal),
        })
    values = [row["total_value"] for row in rows]
    base = rows[1]
    sensitivity = []
    for rate in (0.08, 0.09, 0.10):
        explicit, terminal = growth_present_value(base["forecast_cash_flows"], rate, 0.02, base["terminal_net_dps"], 5)
        sensitivity.append({"required_return": rate, "terminal_growth": 0.02,
                            "value": explicit + terminal, "status": "calculated", "basis": EVIDENCE})
    report["growth_valuation"] = {
        "explicit_horizon_years": 5, "transition_years": 0, "terminal_growth_cap": 0.03,
        "long_run_nominal_growth_bound": 0.04, "growth_cap_evidence": EVIDENCE,
        "minimum_return_growth_spread": 0.02, "scenarios": rows,
        "growth_value_low": min(values), "growth_value_high": max(values), "base_case_value": base["total_value"],
        "margin_of_safety": 0.15, "margin_of_safety_basis": EVIDENCE,
        "entry_upper": min(values) * 0.85, "review_above": max(values),
        "terminal_dependence_warning": "Explicit terminal-share disclosure; no automatic confidence upgrade.",
        "return_growth_sensitivity": sensitivity,
    }


def unavailable_years(report, first_year):
    for row in report["three_year_fundamental_forecast"] + report["forecast_extension"]:
        if row["forecast_year"] >= first_year:
            row.update(dict.fromkeys(("normalized_ocf", "maintenance_capex", "other_owner_claims",
                                      "remaining_growth_investment", "nonrecurring_operating_cash_inflow", "fcf_or_distributable_cash",
                                      "actual_all_in_fcf", "recurring_fad")))
            row.update(estimate_status="not_estimable", forecast_confidence="Not Forecastable",
                       evidence_and_limitations="Capital/remittance evidence missing.")
    for row in report["dividend_forecast_bridge"]:
        if row["forecast_year"] >= first_year:
            row.update(dict.fromkeys(("fcf_or_capital_generation", "required_reinvestment",
                                      "mandatory_debt_or_regulatory_uses", "recurring_fad", "exceptional_cash_uses",
                                      "excess_cash_used", "cash_available_for_distribution")))
    for row in report["dividend_and_yield_runway"]:
        if row["forecast_year"] >= first_year:
            row.update(dict.fromkeys(("cash_available_for_distribution", "dividend_cash_cost", "derived_dps", "funding_gap")))
            row["dps_source"] = "unknown"
    for row in report["business_outlook"]["cumulative_fad"]:
        if first_year <= 3:
            row["three_year"] = None
        row["five_year"] = None


def refresh_growth_pv(report):
    growth = report["growth_valuation"]
    for row in growth["scenarios"]:
        explicit, terminal = growth_present_value(row["forecast_cash_flows"], row["required_return"],
                                                  row["terminal_growth"], row["terminal_net_dps"], row["terminal_time_years"])
        row.update(present_value_of_dividends=explicit, present_value_of_terminal=terminal,
                   total_value=explicit + terminal, terminal_value_share=terminal / (explicit + terminal))
    values = [row["total_value"] for row in growth["scenarios"]]
    base = next(row for row in growth["scenarios"] if row["scenario"] == "Base")
    growth.update(growth_value_low=min(values), growth_value_high=max(values), base_case_value=base["total_value"],
                  entry_upper=min(values) * (1 - growth["margin_of_safety"]), review_above=max(values))
    for row in growth["return_growth_sensitivity"]:
        explicit, terminal = growth_present_value(base["forecast_cash_flows"], row["required_return"],
                                                  row["terminal_growth"], base["terminal_net_dps"], base["terminal_time_years"])
        row["value"] = explicit + terminal


class AnalysisContractTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_synthetic_ordinary_and_growth_reports(self):
        self.assertValid(full_report())
        self.assertValid(full_report(growth=True))

    def test_ordinary_arithmetic_preserves_legacy_boundaries(self):
        self.assertEqual(ordinary_boundaries(4, 3, 0.05, 0.08), {
            "too_expensive_above": 80, "fair_lower": 50, "fair_upper": 80,
            "accumulation_lower": 37.5, "accumulation_upper": 50, "strong_buy_at_or_below": 37.5,
        })
        boundaries = ordinary_boundaries(4, 4, 0.05, 0.08)
        self.assertEqual(boundaries["accumulation_lower"], boundaries["accumulation_upper"])
        for args in ((4, 5, 0.05, 0.08), (4, 3, 0.08, 0.05), (0, 0, 0.05, 0.08)):
            with self.assertRaises(ValueError):
                ordinary_boundaries(*args)

    def test_price_and_score_do_not_change_return_inputs_or_boundaries(self):
        report = full_report()
        original = copy.deepcopy(report["buy_zone"]["boundaries"])
        report["price_used"] = 80
        report["income_assessment"]["forward_net_yield"] = 0.05
        report["key_metrics_at_a_glance"].update(ttm_net_yield=0.05, normalized_net_yield=0.05)
        report["dividend_snapshot"]["ttm_net_yield"] = 0.05
        report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = 60
        report["grade"] = report["key_metrics_at_a_glance"]["grade"] = "C"
        self.assertValid(report)
        self.assertEqual(report["buy_zone"]["boundaries"], original)

    def test_recurring_and_actual_capacity_stay_separate(self):
        self.assertEqual(distribution_capacity(100, 20, 5, 50, 10), (75, 35))
        self.assertEqual(distribution_capacity(10, 20, 5, 0, 0), (-15, -15))
        with self.assertRaises(ValueError):
            distribution_capacity(100, -1, 0, 0, 0)

    def test_aggregate_coverage_not_mean_of_ratios(self):
        ratio = aggregate_coverage([100, 100, 100], [10, 100, 100])
        self.assertAlmostEqual(ratio, 300 / 210)
        self.assertNotAlmostEqual(ratio, (10 + 1 + 1) / 3)
        self.assertIsNone(aggregate_coverage([100], [0]))
        self.assertIsNone(aggregate_coverage([None], [10]))

    def test_duplicate_deduction_rejected(self):
        report = full_report()
        report["dividend_forecast_bridge"][0]["deduction_ledger"][1]["incremental_deduction"] = 16
        self.assertInvalid(report, "0 was expected")

    def test_cash_and_policy_reconciliation(self):
        report = full_report()
        report["dividend_forecast_bridge"][0]["recurring_fad"] += 1
        self.assertInvalid(report, "bridge recurring FAD")
        report = full_report()
        row = report["dividend_and_yield_runway"][0]
        row["policy_implied_dividend"] = row["cash_available_for_distribution"] * row["payout_ratio"]
        self.assertInvalid(report, "policy dividend")
        report = full_report()
        row = report["dividend_and_yield_runway"][0]
        row.update(payout_calculation_basis="recurring_fad", payout_base_reference="recurring_fad",
                   payout_base_amount=60, policy_implied_dividend=24)
        self.assertInvalid(report, "payout calculation basis")
        report = full_report()
        report["dividend_and_yield_runway"][0]["payout_base_amount"] = 60
        self.assertInvalid(report, "payout base bridge")

    def test_ledger_totals_must_match_cash_deductions(self):
        report = full_report()
        report["dividend_forecast_bridge"][0]["required_reinvestment"] = 0
        self.assertInvalid(report, "growth ledger total")
        report = full_report()
        row = report["dividend_forecast_bridge"][0]["deduction_ledger"][0]
        row.update(already_in_starting_metric=True, incremental_deduction=0)
        self.assertInvalid(report, "growth ledger total")

    def test_actual_fcf_and_temporary_inflows_are_not_recurring_fad(self):
        report = full_report()
        row = report["three_year_fundamental_forecast"][0]
        row["actual_all_in_fcf"] += 10
        self.assertInvalid(report, "actual all-in FCF")
        row["nonrecurring_operating_cash_inflow"] = 10
        self.assertValid(report)
        self.assertEqual(row["recurring_fad"], 60)

    def test_coverage_uses_dates_not_array_order(self):
        report = full_report()
        report["cash_flow_bridge"].reverse()
        self.assertValid(report)
        report["coverage_summary"]["three_year_recurring_coverage"] = 1.5
        self.assertInvalid(report, "Three-year aggregate coverage")

    def test_base_average_n_must_match_forecast(self):
        report = full_report()
        zone = report["buy_zone"]
        zone["normalized_net_dps_basis"] = "three_year_base_average"
        self.assertValid(report)
        zone["normalized_net_dps"] = 40
        zone["boundaries"] = ordinary_boundaries(40, 3.2, 0.08, 0.1)
        self.assertInvalid(report, "Three-year Base-average N")

    def test_five_year_scenario_completeness(self):
        report = full_report()
        report["forecast_extension"][0]["scenario"] = "Base"
        self.assertInvalid(report, "exactly one row")
        report = full_report()
        report["forecast_extension"].pop()
        self.assertInvalid(report, "too short")

    def test_unavailable_extension_is_not_a_false_forecast(self):
        report = full_report()
        unavailable_years(report, 4)
        self.assertValid(report)
        report["forecast_extension"][0]["recurring_fad"] = 100
        self.assertInvalid(report, "None was expected")

    def test_insurer_without_capital_remittance_cannot_invent_fcf(self):
        report = full_report()
        report["cash_flow_model"].update(
            sector_model="insurer", overlays=["holding_company"], starting_metric="OPAT, earnings only",
            evidence_status="insufficient", missing_inputs=["Parent remittances and new-business capital strain"],
        )
        self.assertInvalid(report, "suspended")
        unavailable_years(report, 1)
        report.pop("buy_zone")
        report["valuation_mode"] = report["key_metrics_at_a_glance"]["valuation_mode"] = "suspended"
        report["forecast_confidence"] = "Not Forecastable"
        report["score_100"] = report["key_metrics_at_a_glance"]["score_100"] = None
        report["grade"] = report["key_metrics_at_a_glance"]["grade"] = None
        for row in report["cash_flow_bridge"]:
            row.update(recurring_owner_fcf_or_proxy=None, recurring_fad=None,
                       fcf_dividend_coverage=None, evidence_status="insufficient")
        report["coverage_summary"].update(
            three_year_recurring_coverage=None, five_year_worst_recurring_coverage=None,
            worst_available_recurring_coverage=None, worst_recurring_year=None,
        )
        self.assertValid(report)

    def test_growth_formula_uses_next_dividend_and_dated_cash(self):
        path = [{"years_from_valuation": year, "net_dps": 10, "cash_fraction": 1} for year in range(1, 6)]
        explicit, terminal = growth_present_value(path, 0.1, 0, 10, 5)
        self.assertAlmostEqual(explicit + terminal, 100)
        growing = [{"years_from_valuation": year, "net_dps": 10 * 1.02 ** year, "cash_fraction": 1} for year in range(1, 6)]
        values = growth_present_value(growing, 0.1, 0.02, 10 * 1.02 ** 6, 5)
        self.assertAlmostEqual(sum(values), 10.2 / (0.1 - 0.02))
        path[1]["net_dps"] += 3
        changed = growth_present_value(path, 0.1, 0, 10, 5)
        self.assertAlmostEqual(sum(changed) - 100, 3 / 1.1 ** 2)

    def test_stub_cash_fraction_is_applied_once(self):
        report = full_report(growth=True)
        base = report["growth_valuation"]["scenarios"][1]
        original = base["total_value"]
        base["forecast_cash_flows"][0]["cash_fraction"] = 0.5
        refresh_growth_pv(report)
        self.assertAlmostEqual(original - base["total_value"], 2 / 1.09)
        self.assertValid(report)

    def test_multiple_cash_dates_reconcile_to_annual_entitlement(self):
        report = full_report(growth=True)
        base = report["growth_valuation"]["scenarios"][1]
        first = base["forecast_cash_flows"][0]
        earlier = {**first, "cash_fraction": 0.4, "years_from_valuation": 0.5}
        first["cash_fraction"] = 0.6
        base["forecast_cash_flows"].insert(0, earlier)
        refresh_growth_pv(report)
        self.assertValid(report)
        earlier["cash_fraction"] = 0.5
        self.assertInvalid(report, "cash entitlement counted more than once")

    def test_pence_quotes_convert_values_without_changing_yield(self):
        report = full_report(growth=True)
        report["cash_flow_model"]["financial_currency"] = "GBP"
        report["return_requirements"].update(benchmark_currency="GBP", valuation_currency="GBP", valuation_unit_scale=0.01)
        report["buy_zone"].update(dps_currency="GBP", normalized_net_dps=400, bear_net_dps=320,
                                   boundaries=ordinary_boundaries(400, 320, 0.08, 0.1))
        report["price_used"] *= 100
        report["income_assessment"]["forward_net_dps"] *= 100
        for row in report["growth_valuation"]["scenarios"]:
            row["terminal_net_dps"] *= 100
            for cash in row["forecast_cash_flows"]:
                cash["net_dps"] *= 100
        refresh_growth_pv(report)
        self.assertValid(report)

    def test_adr_entitlement_and_recurring_fees(self):
        report = full_report(growth=True)
        report["return_requirements"]["shares_per_quoted_security"] = 2
        report["price_used"] = 80
        report["income_assessment"].update(forward_net_dps=7.8, forward_net_yield=7.8 / 80)
        report["buy_zone"].update(normalized_net_dps=7.8, bear_net_dps=6.24, normalization_cash_deductions=0.2,
                                   boundaries=ordinary_boundaries(7.8, 6.24, 0.08, 0.1))
        for row in report["growth_valuation"]["scenarios"]:
            for cash in row["forecast_cash_flows"]:
                fee = cash["net_dps"] * 0.05
                cash.update(investor_cash_deductions=fee, net_dps=cash["net_dps"] * 2 - fee)
            fee = row["terminal_net_dps"] * 0.05
            row["terminal_funding"]["investor_cash_deductions"] = fee
            row["terminal_net_dps"] = row["terminal_net_dps"] * 2 - fee
        refresh_growth_pv(report)
        self.assertValid(report)
        report["growth_valuation"]["scenarios"][0]["forecast_cash_flows"][0]["investor_cash_deductions"] = 0
        self.assertInvalid(report, "cash path / runway reconciliation")

    def test_transient_growth_cash_delta_has_a_reconciled_audit(self):
        report = full_report(growth=True)
        sensitivity = report["driver_sensitivity"][0]
        delta = -1 / 1.09
        sensitivity.update(growth_value_change=delta, growth_cash_delta_audit=[{
            "forecast_year": 1, "cash_timing": "End of FY2026", "years_from_valuation": 1,
            "baseline_net_cash": 4, "revised_net_cash": 3, "delta_net_cash": -1,
            "required_return": 0.09, "present_value_change": delta, "evidence": EVIDENCE,
        }])
        self.assertValid(report)
        sensitivity["growth_value_change"] = 0
        self.assertInvalid(report, "Transient growth-value change")

    def test_growth_gates_and_terminal_spread(self):
        for rate, growth in ((0.03, 0.03), (0.02, 0.03), (0.04, 0.03)):
            with self.assertRaises(ValueError):
                growth_present_value([{"years_from_valuation": 1, "net_dps": 1}], rate, growth, 1, 1)
        report = full_report(growth=True)
        report["growth_assessment"]["capital_remittance_verified"] = False
        self.assertInvalid(report, "True was expected")
        report = full_report(growth=True)
        report["growth_valuation"]["terminal_growth_cap"] = 0.04
        self.assertInvalid(report, "greater than the maximum")
        report = full_report(growth=True)
        report["growth_valuation"]["scenarios"][0]["terminal_net_dps"] *= 1.2
        self.assertInvalid(report, "terminal-year DPS")

    def test_growth_does_not_bypass_trap_or_structural_decline(self):
        report = full_report(growth=True)
        report["value_trap_veto"] = "Triggered"
        self.assertInvalid(report, "suspended")
        report = full_report(growth=True)
        report["fundamental_trend"] = "Structural Decline"
        self.assertInvalid(report, "finite_life_harvest")

    def test_terminal_funding_and_sensitivity_must_reconcile(self):
        report = full_report(growth=True)
        report["growth_valuation"]["scenarios"][0]["terminal_funding"]["remaining_growth_uses"] += 100
        self.assertInvalid(report, "terminal dividend is unfunded")
        report = full_report(growth=True)
        report["growth_valuation"]["return_growth_sensitivity"][0]["value"] += 1
        self.assertInvalid(report, "sensitivity value")

    def test_growth_path_cannot_ignore_exceptional_cash_shortfall(self):
        report = full_report(growth=True)
        bridge = report["dividend_forecast_bridge"][0]
        bridge.update(exceptional_cash_uses=80, cash_available_for_distribution=-20)
        bridge["deduction_ledger"][-1].update(amount=80, incremental_deduction=80)
        report["dividend_and_yield_runway"][0].update(cash_available_for_distribution=-20, funding_gap=52)
        self.assertInvalid(report, "actual distribution capacity")

    def test_short_growth_horizon_cannot_hide_missing_later_years(self):
        report = full_report(growth=True)
        unavailable_years(report, 4)
        growth = report["growth_valuation"]
        growth["explicit_horizon_years"] = 3
        for row in growth["scenarios"]:
            row["forecast_cash_flows"] = row["forecast_cash_flows"][:3]
            row["terminal_time_years"] = 3
        self.assertInvalid(report, "unsupported five-year cash outlook")

    def test_ordinary_base_cash_gap_must_be_resolved(self):
        report = full_report()
        bridge = report["dividend_forecast_bridge"][1]
        bridge.update(exceptional_cash_uses=100, cash_available_for_distribution=-25)
        bridge["deduction_ledger"][-1].update(amount=100, incremental_deduction=100)
        report["dividend_and_yield_runway"][1].update(cash_available_for_distribution=-25, funding_gap=65)
        self.assertInvalid(report, "unresolved Base funding gap")

    def test_negative_cash_dividends_are_validation_errors(self):
        report = full_report()
        report["cash_flow_bridge"][0]["cash_dividends"] = -1
        self.assertInvalid(report, "less than the minimum")

    def test_growth_does_not_override_hard_income_floor(self):
        report = full_report(growth=True)
        income = report["income_assessment"]
        income["target"] = {"target_net_yield": 0.12, "target_basis": "user_explicit", "target_policy": "hard_minimum"}
        income.update(yield_fit="Below target", income_eligible=False, income_price_ceiling=4 / 0.12)
        self.assertValid(report)
        income["income_eligible"] = True
        self.assertInvalid(report, "False was expected")

    def test_transient_cannot_move_normalized_ordinary_boundary(self):
        report = full_report()
        report["driver_sensitivity"][0]["accumulation_upper_bound_change"] = 3
        self.assertInvalid(report, "None was expected")

    def test_no_portfolio_no_sized_trade_or_switch(self):
        report = full_report()
        report["holding_review"]["position_change_fraction"] = 0.2
        self.assertInvalid(report, "None was expected")
        report = full_report()
        report["holding_review"]["action"] = "switch"
        self.assertInvalid(report, "True was expected")

    def test_switch_needs_positive_after_cost_advantage(self):
        report = full_report()
        holding = report["holding_review"]
        holding.update(action="switch", portfolio_inputs_available=True, missing_inputs=[])
        holding["switch_analysis"] = {
            "alternative": "Synthetic alternative", "currency_and_horizon": "USD, five years",
            "current_forward_cash_income": 100, "alternative_forward_cash_income": 105,
            "cost_and_tax_assumptions": EVIDENCE, "after_cost_advantage": 0.02,
            "switching_hurdle": 0.03, "hurdle_basis": EVIDENCE, "income_constraint_met": True,
            "risk_comparison_supported": True, "evidence": EVIDENCE,
        }
        self.assertInvalid(report, "Switch benefit")
        holding["switch_analysis"]["after_cost_advantage"] = 0.04
        self.assertValid(report)

    def test_finite_life_floor_and_structural_overlay_survive(self):
        report = full_report()
        report.pop("buy_zone")
        report.update(valuation_mode="finite_life_harvest", fundamental_trend="Structural Decline",
                      structural_decline_cap_applied=True, harvest_managed_runoff_exception_applied=True,
                      grade="C", portfolio_role="Opportunistic")
        report["key_metrics_at_a_glance"].update(valuation_mode="finite_life_harvest", grade="C",
                                                  portfolio_role="Opportunistic")
        pv = sum(10 / 1.1 ** year for year in range(1, 4))
        report["finite_life_valuation"] = {
            "harvest_horizon_years": 3, "discount_rate": 0.1,
            "forecast_net_distributions": [{"year": str(year), "net_distribution": 10,
                                          "present_value": 10 / 1.1 ** year} for year in range(1, 4)],
            "present_value_of_distributions": pv, "residual_value": 0, "residual_value_basis": EVIDENCE,
            "finite_life_value_low": pv - 1, "finite_life_value_high": pv + 1,
        }
        self.assertValid(report)
        report["finite_life_valuation"]["discount_rate"] = 0.09
        self.assertInvalid(report, "less than the minimum")

    def test_screen_stays_lightweight(self):
        report = {
            "mode": "screen",
            "screening_parameters": {"target_net_yield": None, "target_basis": "not_assessed", "target_policy": "not_assessed"},
            "screen_results": [{
                "company": "Synthetic", "ticker": "EXAMPLE", "exchange": "Example", "as_of_date": "2026-01-01",
                "screening_net_yield_target": None, "yield_fit": "Not Assessed", "yield_gap_percentage_points": None,
                "documented_dividend_growth_path": "Unclear", "five_year_dps_pattern": "Insufficient data",
                "latest_coverage": "Insufficient data", "balance_sheet_alert": "Insufficient data",
                "withholding_efficiency": "Unclear", "preliminary_fundamental_trend": "Unknown",
                "dividend_trap_screen": "Insufficient data", "full_analysis_recommended": "Watch",
                "main_reason": "Need evidence", "forecast_confidence": "Not Assessed", "buy_zone": "Not Assessed",
            }],
        }
        self.assertValid(report)
        full = full_report(growth=True)
        for field in ("forecast_extension", "growth_valuation", "holding_review", "return_requirements",
                      "dividend_and_yield_runway", "key_metrics_at_a_glance"):
            candidate = copy.deepcopy(report)
            candidate[field] = full[field]
            self.assertTrue(validate_report(candidate), f"Screen leaked {field}")

    def test_nonfinite_numbers_rejected(self):
        report = full_report()
        report["price_used"] = math.nan
        self.assertInvalid(report, "non-finite")

    def test_schema_and_document_contracts(self):
        self.assertIsNotNone(schema_validator())
        root = Path(__file__).resolve().parents[1]
        skill = root / "dividend-income-equity-analysis"
        business = (skill / "business-fundamentals.md").read_text(encoding="utf-8")
        self.assertIn("Three-Year Recurring Coverage = sum(Recurring FAD for 3 years) / sum(Relevant Cash Dividends for 3 years)", business)
        self.assertIn("Deduct an item exactly once", business)
        self.assertIn("earnings_linked", business)
        for path in (skill / "output-template.md", skill / "examples" / "example-output-skeleton.md"):
            text = path.read_text(encoding="utf-8")
            sections = [line for line in text.splitlines() if line.startswith("## ") and line[3:4].isdigit()]
            self.assertEqual(len(sections), 18)


if __name__ == "__main__":
    unittest.main()
