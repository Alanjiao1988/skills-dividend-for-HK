"""Profile-driven routing: rules follow economic dimensions, not an industry list."""
import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "dividend-income-equity-analysis"
sys.path.insert(0, str(SKILL))

from scripts.render_report import render_report  # noqa: E402
from scripts.schema3_checks import economic_profile_errors  # noqa: E402
from scripts.validate_analysis import validate_report  # noqa: E402


def full():
    return json.loads((SKILL / "examples" / "full-report.analysis.json").read_text(encoding="utf-8"))


def segment(name, share, engine, life, cycle, role, intensity):
    return {"name": name, "cash_share_pct": share, "revenue_engine": engine, "asset_life": life,
            "cyclicality": cycle, "cycle_window": None if cycle == "stable" else "覆盖一个完整周期的年份",
            "balance_sheet_role": role, "capital_intensity": intensity}


def profile(segments, wrapper="ordinary_company", attribution="wholly_owned", finite=(), runoff=False,
            regime="ordinary_dividend", exit_rate=None, exception=None):
    return {
        "segments": segments, "legal_wrapper": wrapper, "cash_attribution": attribution,
        "finite_life_assets": [{"name": name, "end_year": year, "operating_cash_share_pct": share,
                                "extension_evidence": None, "terminal_treatment": "到期后不再贡献现金"}
                               for name, year, share in finite],
        "company_level_runoff": runoff,
        "tax_route": {"distribution_regime": regime, "exit_withholding_rate": exit_rate,
                      "exception_evidence": exception, "refunds_excluded_from_cash": True},
        "kpis": [{"name": f"指标{i}", "why_causal": "驱动现金"} for i in range(3)],
        "classification_evidence": "年报分部附注",
    }


def case(prof, sector="operating_company", overlays=(), mode="ordinary_yield_based"):
    return {"economic_profile": prof, "valuation_mode": mode,
            "cash_flow_model": {"sector_model": sector, "overlays": list(overlays)}}


class HoldingsClassifyWithoutNewRules(unittest.TestCase):
    """The user's real holdings route through dimensions; no industry row is needed."""

    def test_bank_hsbc_style(self):
        prof = profile([segment("银行业务", 100, "spread_income", "perpetual_going_concern",
                                "rate_cycle", "balance_sheet_spread", "asset_light")])
        self.assertEqual(economic_profile_errors(case(prof, "bank", ["holding_company"])), [])
        self.assertTrue(economic_profile_errors(case(prof, "operating_company")))

    def test_container_shipping_cosco_style(self):
        prof = profile([segment("集装箱航运", 85, "commodity_linked", "finite_assets", "supply_cycle",
                                "operating", "maintenance_heavy"),
                        segment("码头", 15, "volume_times_price", "finite_assets", "demand_cycle",
                                "operating", "growth_heavy")],
                       attribution="material_jv_associates", finite=[("船队", 2045, 85), ("码头特许权", 2050, 15)])
        self.assertEqual(economic_profile_errors(case(prof, "operating_company", ["holding_company"])), [])
        self.assertTrue(any("JV/associate" in e for e in economic_profile_errors(case(prof))))

    def test_port_concessions_china_merchants_style(self):
        prof = profile([segment("港口", 100, "volume_times_price", "finite_assets", "demand_cycle",
                                "operating", "growth_heavy")],
                       wrapper="holding_parent", attribution="material_jv_associates",
                       finite=[("港口A特许权", 2040, 30), ("港口B特许权", 2055, 70)])
        self.assertEqual(economic_profile_errors(case(prof, "holding_company")), [])

    def test_integrated_oil_chevron_style(self):
        prof = profile([segment("上游", 75, "commodity_linked", "finite_assets", "commodity_cycle",
                                "operating", "maintenance_heavy"),
                        segment("下游", 25, "volume_times_price", "perpetual_going_concern", "demand_cycle",
                                "operating", "maintenance_heavy")],
                       finite=[("已探明储量", 2036, 75)])
        self.assertEqual(economic_profile_errors(case(prof)), [])


class DimensionRules(unittest.TestCase):
    def test_finite_assets_do_not_force_company_runoff(self):
        prof = profile([segment("收费公路", 100, "regulated_or_contracted", "finite_assets", "stable",
                                "operating", "maintenance_heavy")], finite=[("路段A", 2035, 60), ("路段B", 2048, 40)])
        self.assertEqual(economic_profile_errors(case(prof, "concession_infrastructure")), [])
        errors = economic_profile_errors(case(prof, "concession_infrastructure", mode="finite_life_harvest"))
        self.assertTrue(any("company-level run-off" in e for e in errors))
        prof["company_level_runoff"] = True
        self.assertEqual(economic_profile_errors(case(prof, "concession_infrastructure", mode="finite_life_harvest")), [])

    def test_finite_segment_and_schedule_must_match(self):
        prof = profile([segment("矿山", 100, "commodity_linked", "finite_assets", "commodity_cycle",
                                "operating", "maintenance_heavy")])
        self.assertTrue(any("finite_life_assets" in e for e in economic_profile_errors(case(prof))))

    def test_concession_model_requires_finite_assets(self):
        prof = profile([segment("服务", 100, "volume_times_price", "perpetual_going_concern", "stable",
                                "operating", "asset_light")])
        self.assertTrue(economic_profile_errors(case(prof, "concession_infrastructure")))

    def test_cyclical_segment_needs_window_and_shares_sum(self):
        prof = profile([segment("油轮", 100, "commodity_linked", "perpetual_going_concern", "supply_cycle",
                                "operating", "maintenance_heavy")])
        prof["segments"][0]["cycle_window"] = None
        self.assertTrue(any("cycle_window" in e for e in economic_profile_errors(case(prof))))
        prof["segments"][0]["cycle_window"] = "十年"
        prof["segments"][0]["cash_share_pct"] = 70
        self.assertTrue(any("sum to about 100%" in e for e in economic_profile_errors(case(prof))))

    def test_mortgage_reit_needs_spread_role_and_reit_wrapper(self):
        spread = [segment("机构抵押贷款", 100, "spread_income", "perpetual_going_concern", "rate_cycle",
                          "balance_sheet_spread", "asset_light")]
        self.assertEqual(economic_profile_errors(case(profile(spread, wrapper="reit", regime="reit_distribution"),
                                                      "mortgage_reit")), [])
        self.assertTrue(economic_profile_errors(case(profile(spread), "mortgage_reit")))
        self.assertTrue(economic_profile_errors(case(profile(spread, wrapper="reit", regime="reit_distribution"),
                                                     "reit")))

    def test_leasing_cannot_use_bank_proxy(self):
        prof = profile([segment("飞机租赁", 100, "regulated_or_contracted", "finite_assets", "demand_cycle",
                                "asset_leasing", "growth_heavy")], finite=[("机队", 2045, 100)])
        self.assertEqual(economic_profile_errors(case(prof)), [])
        self.assertTrue(economic_profile_errors(case(prof, "bank")))

    def test_partnership_tax_route(self):
        pipe = [segment("管道", 100, "regulated_or_contracted", "perpetual_going_concern", "stable",
                        "operating", "growth_heavy")]
        ok = profile(pipe, wrapper="us_publicly_traded_partnership", regime="us_1446a", exit_rate=0.10)
        self.assertEqual(economic_profile_errors(case(ok, "midstream_partnership")), [])
        for kwargs in ({"exit_rate": None}, {"exit_rate": 0.0}):
            bad = profile(pipe, wrapper="us_publicly_traded_partnership", regime="us_1446a", **kwargs)
            self.assertTrue(economic_profile_errors(case(bad, "midstream_partnership")), kwargs)
        documented = profile(pipe, wrapper="us_publicly_traded_partnership", regime="us_1446a",
                             exit_rate=0.0, exception="券商确认适用例外的书面文件")
        self.assertEqual(economic_profile_errors(case(documented, "midstream_partnership")), [])
        # A C-corp pipeline uses the same cash model but the ordinary dividend route.
        self.assertEqual(economic_profile_errors(case(profile(pipe), "midstream_partnership")), [])
        self.assertTrue(economic_profile_errors(case(profile(pipe, regime="us_1446a"), "midstream_partnership")))

    def test_refunds_and_funds(self):
        prof = profile([segment("业务", 100, "volume_times_price", "perpetual_going_concern", "stable",
                                "operating", "asset_light")])
        prof["tax_route"]["refunds_excluded_from_cash"] = False
        self.assertTrue(economic_profile_errors(case(prof)))
        prof = profile(prof["segments"], wrapper="fund_or_etf")
        self.assertTrue(any("fund" in e for e in economic_profile_errors(case(prof))))


class ReportContract(unittest.TestCase):
    def test_twelve_chapter_report_requires_profile(self):
        report = full()
        self.assertEqual(validate_report(report), [])
        del report["economic_profile"]
        self.assertTrue(any("economic_profile" in e for e in validate_report(report)))

    def test_new_reports_must_be_twelve_chapters(self):
        legacy = json.loads((SKILL / "examples" / "ordinary.analysis.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_report(legacy), [])  # archived six-section record still reads
        legacy["as_of_date"] = "2026-12-01"
        self.assertTrue(any("twelve-chapter structure" in e for e in validate_report(legacy)))

    def test_profile_and_appendix_render_from_records(self):
        report = full()
        report["report_output"]["appendix"] = []
        html_text = render_report(report)
        chapter2 = re.search(r'<section id="section-2">(.*?)</section>', html_text, re.S).group(1)
        self.assertIn("经济特征档案", chapter2)
        appendix = re.search(r'<section id="audit-appendix">(.*?)</section>', html_text, re.S).group(1)
        for part in ("A3 ", "A5 ", "A6 ", "A10 ", "A11 ", "A13 "):
            self.assertIn(part, appendix)

    def test_finite_asset_schedule_renders(self):
        report = full()
        prof = report["economic_profile"]
        prof["segments"][0]["asset_life"] = "finite_assets"
        prof["finite_life_assets"] = [{"name": "码头维护特许合同", "end_year": 2034, "operating_cash_share_pct": 100,
                                       "extension_evidence": None, "terminal_treatment": "到期后按续约假设单独测试"}]
        self.assertEqual(validate_report(report), [])
        self.assertIn("有限期资产到期表", render_report(report))

    def test_industry_tables_are_quick_reference_not_rules(self):
        industry = (SKILL / "industry-analysis.md").read_text(encoding="utf-8")
        self.assertIn("Routing comes from `economic-profile.md`", industry)
        proxies = (SKILL / "sector-fcf-proxies.md").read_text(encoding="utf-8")
        self.assertNotIn("equity value ends at expiry", proxies)
        self.assertIn("A single concession's expiry is not the company's expiry", proxies)
        withholding = (SKILL / "withholding-notes.md").read_text(encoding="utf-8")
        self.assertIn("gross amount realized", withholding)
        self.assertNotIn("1099 share class follows", withholding)


if __name__ == "__main__":
    unittest.main()


class CrossDimensionConsistency(unittest.TestCase):
    """Mixed businesses and contradictory dimensions (ChatGPT review P1-04)."""

    def test_spread_income_must_sit_on_a_spread_balance_sheet(self):
        prof = profile([segment("贷款", 100, "spread_income", "perpetual_going_concern", "rate_cycle",
                                "operating", "asset_light")])
        self.assertTrue(any("spread_income" in e for e in economic_profile_errors(case(prof))))

    def test_commodity_cash_is_not_stable(self):
        prof = profile([segment("油田", 100, "commodity_linked", "perpetual_going_concern", "stable",
                                "operating", "maintenance_heavy")])
        self.assertTrue(any("commodity_linked" in e for e in economic_profile_errors(case(prof))))

    def test_material_finance_arm_needs_its_own_bridge(self):
        finance = segment("金融子公司", 49, "spread_income", "perpetual_going_concern", "rate_cycle",
                          "balance_sheet_spread", "asset_light")
        prof = profile([segment("制造", 51, "volume_times_price", "perpetual_going_concern", "demand_cycle",
                                "operating", "maintenance_heavy"), finance])
        errors = economic_profile_errors(case(prof))
        self.assertTrue(any("holding_company" in e for e in errors))
        self.assertTrue(any("capital_bridge" in e for e in errors))
        finance["capital_bridge"] = "金融子公司按 12% 资本充足率留存资本，剩余利润以股息上缴母公司。"
        self.assertEqual(economic_profile_errors(case(prof, overlays=["holding_company"])), [])

    def test_small_finance_arm_does_not_trigger(self):
        prof = profile([segment("制造", 90, "volume_times_price", "perpetual_going_concern", "demand_cycle",
                                "operating", "maintenance_heavy"),
                        segment("消费金融", 10, "spread_income", "perpetual_going_concern", "rate_cycle",
                                "balance_sheet_spread", "asset_light")])
        self.assertEqual(economic_profile_errors(case(prof)), [])


class AggregateMateriality(unittest.TestCase):
    def test_several_small_finance_arms_add_up(self):
        arms = [segment(f"金融{i}", 19, "spread_income", "perpetual_going_concern", "rate_cycle",
                        "balance_sheet_spread", "asset_light") for i in range(3)]
        prof = profile([segment("制造", 43, "volume_times_price", "perpetual_going_concern", "demand_cycle",
                                "operating", "maintenance_heavy")] + arms)
        self.assertTrue(any("capital_bridge" in e for e in economic_profile_errors(case(prof))))

    def test_financial_holding_group_may_use_capital_return(self):
        bank = segment("银行子公司", 80, "spread_income", "perpetual_going_concern", "rate_cycle",
                       "balance_sheet_spread", "asset_light")
        untyped = economic_profile_errors(case(profile([bank], wrapper="holding_parent"), "holding_company",
                                               mode="capital_return_based"))
        self.assertTrue(any("fits banks and insurers" in e for e in untyped))     # a spread arm must name its capital regime
        bank["spread_business_type"] = "bdc"
        wrapped_bdc = economic_profile_errors(case(profile([bank], wrapper="holding_parent"), "holding_company",
                                                   mode="capital_return_based"))
        self.assertTrue(any("fits banks and insurers" in e for e in wrapped_bdc))  # a BDC cannot hide in a holding company
        bank["spread_business_type"] = "bank"
        other = segment("资产管理", 20, "fee_or_aum", "perpetual_going_concern", "demand_cycle", "operating", "asset_light")
        other["capital_bridge"] = "轻资本业务，利润全额上缴。"
        prof = profile([bank, other], wrapper="holding_parent")
        errors = economic_profile_errors(case(prof, "holding_company", mode="capital_return_based"))
        self.assertFalse(any("fits banks and insurers" in e for e in errors))


class MixedCapitalRegimes(unittest.TestCase):
    def test_bank_majority_with_a_bdc_arm_cannot_use_group_rote(self):
        bank = segment("银行", 51, "spread_income", "perpetual_going_concern", "rate_cycle", "balance_sheet_spread", "asset_light")
        bdc = segment("BDC", 49, "spread_income", "perpetual_going_concern", "rate_cycle", "balance_sheet_spread", "asset_light")
        bank["spread_business_type"], bdc["spread_business_type"] = "bank", "bdc"
        errors = economic_profile_errors(case(profile([bank, bdc], wrapper="holding_parent"), "holding_company",
                                              mode="capital_return_based"))
        self.assertTrue(any("value each arm on its own model" in e for e in errors))
        bdc["spread_business_type"] = "insurer"
        errors = economic_profile_errors(case(profile([bank, bdc], wrapper="holding_parent"), "holding_company",
                                              mode="capital_return_based"))
        self.assertFalse(any("fits banks and insurers" in e for e in errors))


class FiniteShareReconciles(unittest.TestCase):
    def test_schedule_must_cover_the_finite_segments(self):
        prof = profile([segment("矿山", 40, "commodity_linked", "finite_assets", "commodity_cycle", "operating", "maintenance_heavy"),
                        segment("贸易", 60, "volume_times_price", "perpetual_going_concern", "demand_cycle", "operating", "asset_light")],
                       finite=[("一号矿", 2040, 10)])
        self.assertTrue(any("cover 10% of cash" in e for e in economic_profile_errors(case(prof))))
        prof["finite_life_assets"].append({"name": "未拆分矿权", "end_year": 2045, "earliest_end_year": 2033,
                                           "operating_cash_share_pct": 30, "extension_evidence": None,
                                           "terminal_treatment": "按最早到期年估值"})
        self.assertEqual(economic_profile_errors(case(prof)), [])


class ReportContractVersion(unittest.TestCase):
    def test_declared_twelve_chapter_binds_an_early_data_date(self):
        from scripts.schema3_checks import validate_schema3
        report = json.loads(next((ROOT / "validation-runs").glob("*/cmport-0144.analysis.json")).read_text(encoding="utf-8"))
        self.assertEqual(report["report_contract_version"], "twelve_chapter")
        report["as_of_date"] = "2024-06-30"
        report["report_output"]["sections"] = report["report_output"]["sections"][:6]
        self.assertTrue(any("twelve-chapter" in e for e in validate_schema3(report)))
