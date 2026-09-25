"""Synthetic local-extension regressions; never migrate or rerate an investor report."""

import copy
import json
from datetime import date
from pathlib import Path
import unittest

from scripts.local_checks import QUALITY_WEIGHTS, validate_local_analysis
from scripts.validate_analysis import schema_validator, validate_report


ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "dividend-income-equity-analysis").is_dir():
    ROOT /= "dividend-income-equity-analysis"
LOCAL_FIELDS = ("controller_risk", "quality_assessment", "portfolio_role_assessment",
                "real_income", "fx_risk", "income_drivers")


def fixture(name="ordinary", *, current=False):
    report = json.loads((ROOT / "examples" / f"{name}.analysis.json").read_text(encoding="utf-8"))
    if not current and report["schema_version"] == "3.0":
        # Preserve the original 2.5 regression surface, independently of new contracts.
        report["schema_version"] = "2.5"
        for field in ("decision", "report_output", "evidence_recovery"):
            report.pop(field, None)
    return report


def scoring_fixture():
    from test_analysis_contract import EVIDENCE
    report = fixture()
    report["sources"].append(EVIDENCE)
    return report


def refresh_local_quality(report):
    """Synchronize only synthetic local mirrors after a fixture scorecard mutation."""
    if report.get("schema_version") not in ("2.5", "3.0") or "quality_assessment" not in report:
        return
    summary = report["scorecard"]["summary"]
    modules = {row["module"]: row for row in report["scorecard"]["modules"]
               if row["module"] in QUALITY_WEIGHTS}
    status = ("assessed" if all(row["assessment"] == "assessed" and row.get("evidence_basis") != "estimated"
                               for row in modules.values())
              else "not_assessed" if all(row["assessment"] == "not_assessable" for row in modules.values())
              else "provisional")
    ranges = {name: copy.deepcopy(summary["module_ranges"][name]) for name in QUALITY_WEIGHTS}
    report["quality_assessment"].update(
        status=status,
        components={name: row["low"] if row["low"] == row["high"] else None for name, row in ranges.items()},
        score_85=report["scorecard"]["quality_score_85"],
        range_kind="rubric_bounds", component_ranges=ranges,
        score_range=copy.deepcopy(summary["quality_range"]), coverage_pct=summary["quality_coverage_pct"],
    )


def attach_local_extensions(report):
    """Add stipulated local evidence only when constructing a new synthetic 2.5 fixture."""
    template = fixture()
    for field in LOCAL_FIELDS:
        report.setdefault(field, copy.deepcopy(template[field]))
    if "buy_zone" in report:
        report["buy_zone"].setdefault("normalization_model", copy.deepcopy(template["buy_zone"]["normalization_model"]))
    if report["portfolio_role"] == "Core income":
        report["portfolio_role"] = report["key_metrics_at_a_glance"]["portfolio_role"] = "Watchlist"
        if "rating_audit" in report:
            report["rating_audit"]["portfolio_role"]["label"] = "Watchlist"
    refresh_local_quality(report)
    return report


class LocalExtensionTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment=None):
        errors = validate_report(report)
        self.assertTrue(errors)
        if fragment:
            self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_current_examples_are_valid_and_not_modified(self):
        for name in ("ordinary", "growth", "safety-review"):
            with self.subTest(name=name):
                report = fixture(name, current=True)
                before = copy.deepcopy(report)
                self.assertValid(report)
                self.assertEqual(report, before)

    def test_untouched_local_legacy_examples(self):
        for name in ("ordinary", "growth", "safety-review"):
            with self.subTest(name=name):
                report = fixture(name)
                report["schema_version"] = "2.4"
                for key in ("scorecard", "rating_audit", "entry_plan"):
                    report.pop(key, None)
                if "quality_assessment" in report:
                    report["quality_assessment"] = {
                        key: value for key, value in report["quality_assessment"].items()
                        if key in ("status", "components", "score_85", "price_independent", "evidence_and_limitations")
                    }
                    report["quality_assessment"]["status"] = "assessed"
                    for key in ("current_action", "score_status", "score_range", "quality_score_range",
                                "score_coverage_pct", "grade_range"):
                        report["key_metrics_at_a_glance"].pop(key, None)
                before = copy.deepcopy(report)
                raw = json.dumps(report, sort_keys=True)
                self.assertValid(report)
                self.assertEqual(report, before)
                self.assertEqual(json.dumps(report, sort_keys=True), raw)
                self.assertNotIn("scorecard", report)

    def test_current_full_requires_every_local_record(self):
        for name in LOCAL_FIELDS:
            report = fixture()
            del report[name]
            self.assertInvalid(report, name)
        report = fixture()
        del report["buy_zone"]["normalization_model"]
        self.assertInvalid(report, "normalization_model")

    def test_current_rubric_and_ranges_are_not_optional(self):
        report = fixture()
        report["scorecard"]["rubric_version"] = "1"
        self.assertInvalid(report, "rubric_version")
        for name in ("component_ranges", "score_range", "coverage_pct", "range_kind"):
            report = fixture()
            del report["quality_assessment"][name]
            self.assertInvalid(report, name)

    def test_local_quality_matches_scorecard_not_old_fixture_score(self):
        report = fixture()
        self.assertEqual(report["quality_assessment"]["score_85"], 62)
        self.assertEqual(report["score_100"], 76)
        report["quality_assessment"]["score_85"] = 61
        self.assertInvalid(report, "Local quality /85")

    def test_quality_component_mismatch_fails(self):
        report = fixture()
        report["quality_assessment"]["components"]["visibility"] += 1
        self.assertInvalid(report, "Local quality visibility point")

    def test_partial_quality_retains_ranges_without_a_midpoint(self):
        from test_provisional_scoring import mark_unknown
        report = scoring_fixture()
        mark_unknown(report, "buyback_quality")
        refresh_local_quality(report)
        self.assertValid(report)
        self.assertEqual(report["quality_assessment"]["status"], "provisional")
        self.assertEqual(report["quality_assessment"]["score_range"], {"low": 57, "high": 67})
        self.assertIsNone(report["quality_assessment"]["score_85"])
        self.assertIsNone(report["quality_assessment"]["components"]["buyback_quality"])
        report["quality_assessment"]["score_85"] = 62
        self.assertInvalid(report, "Local quality /85")

    def test_partial_quality_is_not_erased_by_one_missing_component(self):
        from test_provisional_scoring import mark_unknown
        report = scoring_fixture()
        mark_unknown(report, "visibility")
        refresh_local_quality(report)
        self.assertValid(report)
        report["quality_assessment"]["status"] = "not_assessed"
        self.assertInvalid(report, "Local quality status")

    def test_estimated_quality_point_is_provisional(self):
        from test_provisional_scoring import refresh_provisional
        report = scoring_fixture()
        row = next(row for row in report["scorecard"]["modules"] if row["module"] == "visibility")
        row["evidence_basis"] = "estimated"
        refresh_provisional(report)
        refresh_local_quality(report)
        self.assertValid(report)
        self.assertEqual(report["quality_assessment"]["status"], "provisional")
        self.assertEqual(report["quality_assessment"]["score_85"], 62)

    def test_bounded_component_ranges_cannot_rescale_quality(self):
        from test_provisional_scoring import bound_module
        report = scoring_fixture()
        bound_module(report, "buyback_quality", [2, 3])
        refresh_local_quality(report)
        self.assertValid(report)
        report["quality_assessment"]["component_ranges"]["buyback_quality"]["high"] += 1
        self.assertInvalid(report, "Local quality buyback_quality range")

    def test_unknown_model_does_not_force_adverse_visibility(self):
        from test_provisional_scoring import suspend_model
        report = scoring_fixture()
        suspend_model(report)
        refresh_local_quality(report)
        self.assertValid(report)
        self.assertEqual(report["quality_assessment"]["status"], "provisional")
        self.assertGreater(report["quality_assessment"]["coverage_pct"], 0)

    def test_local_quality_does_not_bypass_upstream_cash_arithmetic(self):
        report = fixture()
        report["dividend_forecast_bridge"][0]["recurring_fad"] += 1
        self.assertInvalid(report, "recurring FAD")

    def test_controller_harm_requires_veto_and_blocks_action(self):
        report = fixture()
        report["controller_risk"].update(status="triggered", materiality="material",
                                        material_harm_confirmed=True,
                                        cash_demand_evidence=["Synthetic dated transfer"],
                                        channels=["Related-party extraction"])
        self.assertInvalid(report, "controller harm")
        self.assertInvalid(report, "blocks eligible entry")

    def test_unknown_controller_materiality_is_not_no_risk(self):
        report = fixture()
        report["controller_risk"].update(status="not_assessed", materiality="unknown",
                                        material_harm_confirmed=None)
        self.assertInvalid(report, "Unresolved controller")

    def test_role_is_not_created_by_a_cheap_quote(self):
        report = fixture()
        report["portfolio_role_assessment"]["price_alone_changes_role"] = True
        self.assertInvalid(report, "price_alone_changes_role")
        report = fixture()
        report["portfolio_role_assessment"]["rationale"] = ""
        self.assertInvalid(report, "rationale")

    def test_core_role_has_no_invented_68_point_or_strong_only_cutoff(self):
        report = fixture()
        self.assertEqual(report["quality_assessment"]["score_85"], 62)
        self.assertEqual(report["dividend_safety"], "Acceptable")
        report["portfolio_role"] = report["key_metrics_at_a_glance"]["portfolio_role"] = "Core income"
        report["rating_audit"]["portfolio_role"]["label"] = "Core income"
        report["portfolio_role_assessment"]["rationale"] = (
            "Synthetic supported recurring cash and Acceptable safety justify this independent role judgment; "
            "the combined score and quote do not assign it."
        )
        self.assertValid(report)

    def test_required_yield_spread_uses_income_rates_not_total_return_rates(self):
        report = fixture()
        report["buy_zone"].update(required_net_yield_low=.09, required_net_yield_high=.11)
        report["return_requirements"].update(required_total_return_low=.12, required_total_return_high=.14)
        report["income_assessment"]["required_yield_spread"] = {
            "normalized_net_yield": .1, "vs_low_pp": 1, "vs_high_pp": -1,
        }
        self.assertEqual(validate_local_analysis(report), ([], []))
        report["income_assessment"]["required_yield_spread"]["vs_low_pp"] = -2
        errors, _ = validate_local_analysis(report)
        self.assertTrue(any("Local yield spread vs low" in error for error in errors))

    def test_normalization_state_arithmetic(self):
        report = fixture()
        report["buy_zone"]["normalization_model"]["cycle_states"]["mid"]["recurring_fad"] += 1
        self.assertInvalid(report, "Normalization mid recurring FAD")

    def test_normalization_median_uses_observed_series(self):
        report = fixture()
        driver = report["buy_zone"]["normalization_model"]["drivers"][0]
        driver.update(selection="median", observations=[60, 70, 100, 200, 220], selected_value=100)
        self.assertValid(report)
        driver["selected_value"] = 140
        self.assertInvalid(report, "observed median")

    def test_normalization_uncertainty_is_not_cycle_extremes(self):
        report = fixture()
        model = report["buy_zone"]["normalization_model"]
        model.update(uncertainty_low=3.8, uncertainty_high=4.2)
        self.assertValid(report)
        model["uncertainty_low"] = 4.5
        self.assertInvalid(report, "uncertainty")

    def cyclical_report(self):
        report = fixture()
        model = report["buy_zone"]["normalization_model"]
        model.update(
            cycle_applicability="cyclical", method="supply_demand_balance", cycle_length_years=None,
            cycle_basis="Synthetic supply/demand balance supports central cash; cycle length is not established.",
            period_start="2025-01-01", period_end="2025-12-31",
        )
        for name in ("low", "high"):
            model["cycle_states"][name].update(
                status="not_estimable",
                evidence="Extreme operating assumptions are unavailable; no invented low/high DPS.",
            )
        return report

    def test_cyclical_central_normalization_allows_missing_extremes(self):
        report = self.cyclical_report()
        self.assertValid(report)
        model = report["buy_zone"]["normalization_model"]
        model["cycle_length_years"] = 8
        self.assertValid(report)
        model["cycle_states"]["low"]["status"] = "not_applicable"
        self.assertInvalid(report, "never not_applicable")

    def test_full_cycle_claim_still_needs_full_cycle_observations(self):
        report = self.cyclical_report()
        model = report["buy_zone"]["normalization_model"]
        model.update(method="cycle_distribution", cycle_length_years=8)
        self.assertInvalid(report, "must cover the evidenced cycle")
        model["method"] = "supply_demand_balance"
        report["buy_zone"]["normalized_net_dps_basis"] = "full_cycle_median"
        self.assertInvalid(report, "must cover the evidenced cycle")

    def test_base_average_also_reconciles_the_central_operating_ledger(self):
        report = fixture()
        report["buy_zone"]["normalized_net_dps_basis"] = "three_year_base_average"
        self.assertValid(report)
        mid = report["buy_zone"]["normalization_model"]["cycle_states"]["mid"]
        mid.update(earnings=110, payout_base=110, dividend_entitlement=44, gross_dps=4.4)
        self.assertInvalid(report, "operating mid-state net DPS")

    def test_documented_funded_payout_adjustment_is_allowed(self):
        report = fixture()
        mid = report["buy_zone"]["normalization_model"]["cycle_states"]["mid"]
        mid.update(payout_ratio=.5, evidence="Payout adjustment: retain 10 of the policy-implied 50 for liquidity; pay a funded 40.")
        self.assertValid(report)
        mid["evidence"] = "董事会决定派发40而非政策对应的50，因为另有10需用于到期债务的流动性准备。"
        self.assertValid(report)
        mid["evidence"] = report["buy_zone"]["normalization_model"]["series_sources"][0]
        self.assertInvalid(report, "explicit adjustment explanation")

    def test_adverse_low_state_retains_negative_fad_with_zero_dividend(self):
        report = self.cyclical_report()
        model = report["buy_zone"]["normalization_model"]
        low = model["cycle_states"]["low"] = copy.deepcopy(model["cycle_states"]["mid"])
        low.update(owner_cash=10, growth_uses=20, mandatory_uses=5, recurring_fad=-15,
                   earnings=-20, payout_base=-20, dividend_entitlement=0, gross_dps=0,
                   evidence="Synthetic low state has a 15 cash shortfall and zero dividend; central funding remains supported.")
        self.assertValid(report)
        self.assertEqual(low["recurring_fad"], -15)
        low.update(dividend_entitlement=1, gross_dps=.1)
        self.assertInvalid(report, "unfunded recurring dividend")

    def test_central_funding_shortfall_still_blocks_actionable_normalization(self):
        report = fixture()
        mid = report["buy_zone"]["normalization_model"]["cycle_states"]["mid"]
        mid.update(owner_cash=30, recurring_fad=5)
        self.assertInvalid(report, "Unfunded central normalization blocks eligible entry")

    def test_unassessed_normalization_cannot_authorize_entry(self):
        report = fixture()
        model = report["buy_zone"]["normalization_model"]
        model.update(status="not_assessed", method="not_assessed")
        model["cycle_states"]["mid"] = copy.deepcopy(model["cycle_states"]["low"])
        self.assertInvalid(report, "normalization blocks eligible entry")

    def test_real_income_exact_geometric_cagr(self):
        report = fixture()
        real = report["real_income"]
        years = (date(2025, 12, 31) - date(2021, 12, 31)).days / 365.25
        nominal = (120 / 100) ** (1 / years) - 1
        inflation = (110 / 100) ** (1 / years) - 1
        growth = (1 + nominal) / (1 + inflation) - 1
        real.update(status="assessed", period_start="2021-12-31", period_end="2025-12-31",
                    starting_net_cash=100, ending_net_cash=120, starting_price_index=100,
                    ending_price_index=110, nominal_cagr=nominal, inflation_cagr=inflation,
                    real_cagr=growth, trend="Growing")
        self.assertValid(report)
        real["real_cagr"] = nominal - inflation
        self.assertInvalid(report, "purchasing-power CAGR")

    def test_unassessed_real_income_does_not_invent_flat(self):
        report = fixture()
        report["real_income"]["trend"] = "Flat"
        self.assertInvalid(report, "Unassessed real income")

    def test_missing_cpi_preserves_known_cash_dates_and_nominal_cagr(self):
        report = fixture()
        real = report["real_income"]
        real.update(period_start="2021-12-31", period_end="2025-12-31",
                    starting_net_cash=100, ending_net_cash=120,
                    nominal_cagr=1.2 ** .25 - 1)
        self.assertValid(report)
        self.assertEqual(real["status"], "not_assessed")
        self.assertIsNone(real["inflation_cagr"])
        self.assertIsNone(real["real_cagr"])
        real["nominal_cagr"] = 0
        self.assertInvalid(report, "nominal CAGR")

    def test_missing_cash_preserves_independently_calculable_inflation(self):
        report = fixture()
        real = report["real_income"]
        real.update(period_start="2021-12-31", period_end="2025-12-31",
                    starting_price_index=100, ending_price_index=110,
                    inflation_cagr=1.1 ** .25 - 1)
        self.assertValid(report)
        self.assertIsNone(real["nominal_cagr"])
        real["real_cagr"] = 0
        self.assertInvalid(report, "purchasing-power CAGR")

    def fx_report(self):
        report = fixture()
        risk = report["fx_risk"]
        risk.update(status="assessed", material_exposure=True)
        for kind, operating in (("fx_only", 4), ("combined_bear", 3.2)):
            stressed = operating * .9
            risk["stress_rows"].append({
                "kind": kind, "forecast_year": 1, "base_fx": 1, "stressed_fx": .9,
                "base_gross_dps": 4, "operating_gross_dps": operating,
                "economic_gross_dps_delta": 0, "economic_fx_in_runway": True,
                "economic_fx_bridge": "Synthetic economic FX already in the operating runway.",
                "hedge_cash_adjustment": 0, "investor_fees": 0, "base_net_cash": 4,
                "stressed_net_cash": stressed, "delta_cash": stressed - 4,
                "evidence": "Synthetic FX stress, not a live-market estimate.",
            })
        return report

    def test_fx_stresses_reconcile_and_do_not_double_count(self):
        report = self.fx_report()
        self.assertValid(report)
        report["fx_risk"]["stress_rows"][0]["economic_gross_dps_delta"] = .1
        self.assertInvalid(report, "already in runway")

    def test_material_fx_needs_joint_bear_stress(self):
        report = self.fx_report()
        report["fx_risk"]["stress_rows"].pop()
        self.assertInvalid(report, "combined-Bear")

    def test_fx_pairs_cannot_be_split_across_different_years(self):
        report = self.fx_report()
        report["fx_risk"]["stress_rows"][1]["forecast_year"] = 2
        self.assertInvalid(report, "year 1 needs paired")
        self.assertInvalid(report, "year 2 needs paired")

    def test_unknown_fx_is_not_immaterial_and_blocks_action(self):
        report = fixture()
        report["fx_risk"].update(status="not_assessed", material_exposure=None)
        self.assertInvalid(report, "Unresolved material FX")

    def test_safety_has_no_valuation_scoring_or_automatic_trade(self):
        for name, value in (("score_100", 80), ("scorecard", {}), ("buy_zone", {}),
                            ("valuation_mode", "suspended"), ("entry_plan", {})):
            report = fixture("safety-review")
            report[name] = value
            self.assertInvalid(report)
        report = fixture("safety-review")
        report["review"]["automatic_trade"] = True
        self.assertInvalid(report, "automatic_trade")

    def test_safety_legacy_copy_is_valid(self):
        report = fixture("safety-review")
        report["schema_version"] = "2.4"
        self.assertValid(report)

    def test_safety_scrip_does_not_hide_all_cash_gap(self):
        report = fixture("safety-review")
        review = report["review"]
        review.update(full_cash_entitlement=60, recurring_entitlement_coverage=1,
                      all_cash_funding_gap=5, dividend_safety="Weak", requires_full_analysis=True,
                      escalation_reasons=["Synthetic all-cash gap needs a full funding review."])
        self.assertValid(report)
        review["all_cash_funding_gap"] = 0
        self.assertInvalid(report, "all-cash funding gap")

    def test_safety_negative_capital_headroom_escalates(self):
        report = fixture("safety-review")
        report["review"]["metrics"]["capital_headroom"]["after"] = -.1
        self.assertInvalid(report, "deficit")
        review = report["review"]
        review.update(dividend_safety="Weak", requires_full_analysis=True,
                      escalation_reasons=["Capital headroom below the applicable minimum."])
        self.assertValid(report)

    def test_safety_missing_capital_is_not_safe(self):
        report = fixture("safety-review")
        report["review"]["metrics"]["capital_headroom"]["after"] = None
        self.assertInvalid(report, "missing_inputs")

    def incomplete_safety_report(self):
        report = fixture("safety-review")
        review = report["review"]
        review["metrics"]["capital_headroom"]["after"] = None
        review.update(
            dividend_safety="Unclear", decision="not_comparable", requires_full_analysis=True,
            missing_inputs=["Current capital headroom has not been reconciled."],
            escalation_reasons=["Material capital uncertainty needs a full capital and remittance review."],
        )
        return report

    def test_safety_material_uncertainty_is_unclear_and_escalates(self):
        report = self.incomplete_safety_report()
        self.assertValid(report)
        report["review"]["dividend_safety"] = "Weak"
        self.assertInvalid(report, "missing evidence alone")
        report = self.incomplete_safety_report()
        report["review"]["decision"] = "maintained"
        self.assertInvalid(report, "not_comparable")
        report = self.incomplete_safety_report()
        report["review"].update(requires_full_analysis=False, escalation_reasons=[])
        self.assertInvalid(report, "requires explained escalation")

    def test_safety_insufficient_current_evidence_cannot_preserve_safe_rating(self):
        report = fixture("safety-review")
        review = report["review"]
        review.update(cash_evidence_status="insufficient", dividend_safety="Unclear",
                      decision="not_comparable", requires_full_analysis=True,
                      missing_inputs=["Current cash perimeter is not reconciled."],
                      escalation_reasons=["Material current cash uncertainty requires a full review."])
        self.assertValid(report)
        review["decision"] = "weakened"
        self.assertInvalid(report, "not_comparable")

    def test_safety_evidenced_deficit_can_remain_weak_despite_other_missing_inputs(self):
        report = self.incomplete_safety_report()
        review = report["review"]
        review["metrics"]["actual_capacity"]["after"] = 35
        review.update(actual_coverage=.875, funding_gap=5, all_cash_funding_gap=5,
                      dividend_safety="Weak", decision="weakened")
        self.assertValid(report)

    def test_safety_nonfinite_numbers_are_rejected(self):
        report = fixture("safety-review")
        report["review"]["metrics"]["liquidity"]["after"] = float("inf")
        self.assertInvalid(report, "non-finite")

    def cash_event_report(self):
        report = fixture()
        report["scrip_drip"].update(available="Yes", cash_election_available="No",
                                   investor_cash_yield_assumption="cash_components_only")
        for row in report["dividend_and_yield_runway"]:
            event = {name: copy.deepcopy(row[name]) for name in (
                "dividend_entitled_shares", "dividend_entitlement", "cash_settled_fraction",
                "settlement_cash_adjustment", "dividend_cash_cost", "derived_dps",
            )}
            event.update(record_date=f"{row['fiscal_year']}-06-30", distribution_type="cash_dividend",
                         cash_election_confirmed=True, distribution_evidence="Synthetic separate cash event.",
                         investor_entitled=True, investor_share_factor=1, stock_shares_issued=0,
                         investor_stock_ratio=0, shares_eligible_from=None, other_share_change=0,
                         share_change_source="No other share changes in the synthetic cash event.")
            row["dividend_installments"] = [event]
            row["investor_cash_dps"] = row["derived_dps"]
        return report

    def test_separately_audited_cash_survives_stock_scheme_flag(self):
        self.assertValid(self.cash_event_report())

    def test_mandatory_stock_cannot_be_used_as_cash(self):
        report = self.cash_event_report()
        report["dividend_and_yield_runway"][0]["dividend_installments"][0]["distribution_type"] = "mandatory_stock"
        self.assertInvalid(report, "Mandatory-stock")

    def test_investor_share_factor_needs_dated_issuance(self):
        report = self.cash_event_report()
        report["dividend_and_yield_runway"][0]["dividend_installments"][0]["investor_share_factor"] = 2
        self.assertInvalid(report, "Dated investor share")

    def test_investor_cash_without_event_audit_cannot_exceed_issuer_cash(self):
        report = fixture()
        report["dividend_and_yield_runway"][0]["investor_cash_dps"] = 100
        self.assertInvalid(report, "without a dated event ledger")

    def test_schema_remains_valid_draft_2020_12(self):
        self.assertIsNotNone(schema_validator())


if __name__ == "__main__":
    unittest.main()
