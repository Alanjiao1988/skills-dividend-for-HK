"""Twelve-chapter report: chapter tables/charts, single buy-point block and sector routing."""
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
from scripts.schema3_checks import FULL_HEADINGS  # noqa: E402
from scripts.validate_analysis import validate_report  # noqa: E402


def load_full():
    return json.loads((SKILL / "examples" / "full-report.analysis.json").read_text(encoding="utf-8"))


def section(html_text, index):
    return re.search(rf'<section id="section-{index}">(.*?)</section>', html_text, re.S).group(1)


class FullReportRenderingTests(unittest.TestCase):
    def test_example_is_valid_twelve_chapter_report(self):
        report = load_full()
        self.assertEqual(validate_report(report), [])
        headings = tuple(row["heading"] for row in report["report_output"]["sections"])
        self.assertEqual(headings, FULL_HEADINGS)

    def test_buy_point_block_appears_only_in_chapter_ten(self):
        html_text = render_report(load_full())
        for index in range(1, 13):
            body = section(html_text, index)
            expected = index == 10
            with self.subTest(chapter=index):
                self.assertEqual("允许买入的条件" in body, expected)
                self.assertEqual("参考档位" in body, expected)

    def test_legacy_six_section_report_keeps_buy_block_in_section_three(self):
        report = json.loads((SKILL / "examples" / "ordinary.analysis.json").read_text(encoding="utf-8"))
        html_text = render_report(report)
        self.assertIn("允许买入的条件", section(html_text, 3))
        self.assertNotIn("允许买入的条件", section(html_text, 2))

    def test_tables_and_charts_render_as_static_html(self):
        html_text = render_report(load_full())
        trends = section(html_text, 5)
        self.assertIn("<table>", trends)
        self.assertIn("<caption>五年现金与股息</caption>", trends)
        self.assertIn("<svg", trends)
        self.assertIn("数据：可持续可分配现金：2021 50", trends)
        self.assertNotIn("<script", trends)

    def test_null_cells_and_points_are_gaps_not_zero(self):
        report = load_full()
        chapter = report["report_output"]["sections"][4]
        chapter["tables"][0]["rows"][0][2] = None
        chapter["charts"][0]["kind"] = "line"
        chapter["charts"][0]["series"][1]["values"][2] = None
        self.assertEqual(validate_report(report), [])
        trends = section(render_report(report), 5)
        self.assertIn('<td class="nowrap">—</td>', trends)
        self.assertIn("2023 —", trends)
        self.assertGreaterEqual(trends.count("<polyline"), 4)

    def test_mismatched_table_or_chart_shape_is_rejected(self):
        report = load_full()
        report["report_output"]["sections"][4]["tables"][0]["rows"][0].append(1)
        self.assertTrue(any("column count" in error for error in validate_report(report)))
        report = load_full()
        report["report_output"]["sections"][4]["charts"][0]["series"][0]["values"].pop()
        self.assertTrue(any("x labels" in error for error in validate_report(report)))

    def test_table_requires_source_note(self):
        report = load_full()
        del report["report_output"]["sections"][4]["tables"][0]["note"]
        self.assertTrue(validate_report(report))


class SectorRoutingTests(unittest.TestCase):
    def test_new_sector_models_are_in_schema_and_proxies(self):
        schema = json.loads((SKILL / "schema.json").read_text(encoding="utf-8"))
        models = schema["$defs"]["cashFlowModel"]["properties"]["sector_model"]["enum"]
        proxies = (SKILL / "sector-fcf-proxies.md").read_text(encoding="utf-8")
        for model in ("bank", "bdc", "insurer", "reit", "mortgage_reit", "utility_infrastructure",
                      "concession_infrastructure", "midstream_partnership", "holding_company"):
            with self.subTest(model=model):
                self.assertIn(model, models)
                self.assertIn(f"`{model}`", proxies)

    def test_operating_style_models_use_owner_fcf_arithmetic(self):
        base = json.loads((SKILL / "examples" / "ordinary.analysis.json").read_text(encoding="utf-8"))
        self.assertEqual(base["cash_flow_model"]["sector_model"], "operating_company")
        for model in ("concession_infrastructure", "midstream_partnership"):
            report = copy.deepcopy(base)
            report["cash_flow_model"]["sector_model"] = model
            with self.subTest(model=model):
                self.assertEqual(validate_report(report), [])
                forecast = report["three_year_fundamental_forecast"][0]
                forecast["maintenance_capex"] += 1
                self.assertTrue(any("Recurring Owner FCF" in error for error in validate_report(report)))

    def test_playbooks_cover_common_income_sectors(self):
        industry = (SKILL / "industry-analysis.md").read_text(encoding="utf-8")
        for name in ("Toll roads", "Gas distribution", "Coal / metals mining", "Mortgage REITs",
                     "Midstream pipelines", "Business trusts", "Aircraft / equipment lessors"):
            with self.subTest(sector=name):
                self.assertIn(name, industry)
        self.assertEqual(industry.count("| Ports / terminals |"), 1)
        self.assertIn("For an industry not listed, derive a bespoke KPI set", industry)
        withholding = (SKILL / "withholding-notes.md").read_text(encoding="utf-8")
        self.assertIn("§1446(f)", withholding)

    def test_no_stale_six_section_or_appendix_on_request_rules(self):
        for name in ("visual-output-rules.md", "analysis-quality.md", "buy-zone.md",
                     "holding-review.md", "scoring.md", "data-conventions.md"):
            text = (SKILL / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertNotIn("six-section main report", text)
                self.assertNotIn("at most three charts", text)
                self.assertNotIn("main report's Section 3", text)
                self.assertNotIn("按需附录", text)


if __name__ == "__main__":
    unittest.main()
