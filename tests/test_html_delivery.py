"""Regression checks for the local HTML delivery adaptation."""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest


SKILL = Path(__file__).resolve().parents[1]
if (SKILL / "dividend-income-equity-analysis").is_dir():
    SKILL /= "dividend-income-equity-analysis"
TEMPLATE = SKILL / "templates" / "report.html"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class HtmlDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.template = TEMPLATE.read_text(encoding="utf-8")

    def test_template_has_only_documented_placeholders(self):
        placeholders = set(re.findall(r"\{\{([A-Z_]+)\}\}", self.template))
        self.assertEqual(placeholders, {
            "REPORT_TITLE", "REPORT_MODE", "REPORT_METADATA", "REPORT_NAV", "REPORT_BODY",
        })
        contract = (SKILL / "output-template.md").read_text(encoding="utf-8")
        for name in placeholders:
            self.assertIn("{{" + name + "}}", contract)

    def test_self_contained_shell_and_theme(self):
        document = Document(self.template)
        self.assertIn(("html", {
            "lang": "zh-CN", "data-report-mode": "{{REPORT_MODE}}",
            "data-ruleset": "3.0", "data-presentation": "html-2",
        }), document.tags)
        self.assertIn(("meta", {"charset": "UTF-8"}), document.tags)
        self.assertEqual(sum(tag == "script" for tag, _ in document.tags), 1)
        for tag, attrs in document.tags:
            self.assertNotIn(tag, {"iframe", "link", "object", "embed"})
            self.assertNotIn("src", attrs)
            self.assertFalse(any(name.startswith("on") for name in attrs))
        for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
                          "indexedDB", "document.cookie", "@import", "url(", "window.open"):
            self.assertNotIn(forbidden, self.template)
        for required in ('--cp-bg: #f7f4ef;', '--cp-bg: #3d3b3a;',
                         '--cp-accent: #b11f4b;', '--cp-accent: #fd8ea1;',
                         'get("scoutTheme")', 'var(--cp-bg)', '@media print',
                         '@media (max-width: 36rem)', '.table-scroll',
                         '"Segoe UI", Aptos, Calibri', 'table-header-group'):
            self.assertIn(required, self.template)

    def test_complete_static_content_and_anchors_for_all_modes(self):
        source = (SKILL / "output-template.md").read_text(encoding="utf-8")
        full_section = source.split("## 3. Full Analysis — Required Twelve Chapters", 1)[1].split(
            "## 4. Audit Appendix", 1)[0]
        full_headings = re.findall(r"^## ([0-9]+\. .+)$", full_section, re.M)
        self.assertEqual(len(full_headings), 12)
        self.assertEqual([int(title.split(".", 1)[0]) for title in full_headings],
                         list(range(1, 13)))
        self.assertEqual([title.split(". ", 1)[1] for title in full_headings], [
            "摘要与投资结论", "公司概况与行业定位", "行业结构、供需与周期",
            "竞争格局与公司护城河", "过去五年经营与财务趋势",
            "现金流、资产负债与股息质量", "企业成长性与资本配置",
            "未来五年经营与现金流预测", "估值与预期总回报",
            "买点、建仓策略与持仓复评", "风险、监测指标与论点证伪",
            "数据来源、关键假设与研究限制",
        ])
        for title in full_headings:
            self.assertRegex(title, r"[\u4e00-\u9fff]")
        headings_by_mode = {
            "full_analysis": full_headings,
            "screen": ["筛选摘要", "候选标的", "来源与限制"],
            "safety_review": ["基线与新披露", "现金与资本", "复检结论与来源"],
        }
        for mode, headings in headings_by_mode.items():
            with self.subTest(mode=mode):
                values = {
                    "REPORT_TITLE": html.escape("Fixture <issuer> & income"),
                    "REPORT_MODE": mode,
                    "REPORT_METADATA": "<p>Schema 3.0；虚构布局测试。</p>",
                    "REPORT_NAV": "<ol>" + "".join(
                        f'<li><a href="#section-{i}">{html.escape(title)}</a></li>'
                        for i, title in enumerate(headings, 1)
                    ) + "</ol>",
                    "REPORT_BODY": "".join(
                        f'<section id="section-{i}"><h2>{html.escape(title)}</h2>'
                        "<p>虚构测试文字，不含投资结论。</p></section>"
                        for i, title in enumerate(headings, 1)
                    ),
                }
                rendered = self.template
                for key, value in values.items():
                    rendered = rendered.replace("{{" + key + "}}", value)
                self.assertNotRegex(rendered, r"\{\{[A-Z_]+\}\}")
                without_script = re.sub(r"<script>.*?</script>", "", rendered, flags=re.S)
                document = Document(without_script)
                ids = [attrs["id"] for _, attrs in document.tags if "id" in attrs]
                self.assertEqual(len(ids), len(set(ids)))
                for tag, attrs in document.tags:
                    if tag == "a":
                        self.assertIn(attrs["href"][1:], ids)
                self.assertEqual(sum(tag == "section" for tag, _ in document.tags), len(headings))
                for title in headings:
                    self.assertIn(title, document.text)
                self.assertNotIn("issuer", [tag for tag, _ in document.tags])

    def test_schema_is_not_changed_to_a_presentation_mode(self):
        schema = json.loads((SKILL / "schema.json").read_text(encoding="utf-8"))
        version = schema["properties"]["schema_version"]
        self.assertEqual(version["enum"], ["2.3", "2.4", "2.5", "3.0"])
        self.assertEqual(version["default"], "3.0")
        self.assertNotIn("const", version)
        self.assertEqual(set(schema["properties"]["mode"]["enum"]),
                         {"screen", "full_analysis", "safety_review"})
        self.assertEqual(schema["properties"]["rendering"]["properties"]["visual_mode"]["enum"],
                         ["rich_charts", "plain_text_fallback"])

    def test_partial_scoring_contract_preserves_light_modes(self):
        safety = (SKILL / "safety-review.md").read_text(encoding="utf-8")
        self.assertIn("Do not add a new forecast", safety)
        self.assertIn("N/B", safety)
        self.assertIn("score, grade", safety)
        self.assertIn("automatic_trade: false", safety)
        self.assertNotIn("scorecard", safety)
        scoring = (SKILL / "scoring.md").read_text(encoding="utf-8")
        for required in ("scorecard.summary", "rating_audit", "assessed", "bounded",
                         "not_assessable", "71-81/100", "57-67/85",
                         "summary.quality_range", "range_kind: rubric_bounds"):
            self.assertIn(required, scoring)
        schema = (SKILL / "schema.json").read_text(encoding="utf-8")
        self.assertIn('"entry_plan"', schema)

    def test_twelve_chapter_report_includes_default_audit_appendix(self):
        source = (SKILL / "output-template.md").read_text(encoding="utf-8")
        self.assertIn("## 4. Audit Appendix（模型与证据明细）", source)
        appendix = source.split("## 4. Audit Appendix（模型与证据明细）", 1)[1]
        for part in range(1, 14):
            self.assertIn(f"- A{part} ", appendix)
        self.assertIn("默认组成部分", appendix)
        self.assertIn("report_output.sections", source)
        main = source.split("## 1. 摘要与投资结论", 1)[1].split("## 4. Audit Appendix", 1)[0]
        self.assertIn("初始建仓", main)
        self.assertIn("逐步增持", main)
        self.assertIn("覆盖度", main)
        self.assertIn("12 章", source)
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("report_structure: twelve_section_full_report", entry)
        self.assertIn("presentation_revision: html-2", entry)

    def test_owned_documents_have_no_merge_markers(self):
        for name in ("output-template.md", "visual-output-rules.md",
                     "examples/example-output-skeleton.md", "examples/worked-examples.md"):
            with self.subTest(name=name):
                source = (SKILL / name).read_text(encoding="utf-8")
                self.assertIsNone(re.search(
                    r"^(?:<<<<<<<|\|\|\|\|\|\|\||=======|>>>>>>>)", source, re.M))

    def test_entry_routes_to_html_and_preserves_publication_gate(self):
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("default_report_format: single_file_html", entry)
        self.assertIn("presentation_revision: html-2", entry)
        self.assertIn("templates/report.html", entry)
        self.assertNotIn("默认在对话中输出分析；只有用户明确要求保存或发布时", entry)
        publishing = (SKILL / "publishing.md").read_text(encoding="utf-8")
        self.assertIn("Alanjiao1988/Dividendreport", publishing)
        self.assertIn("<ticker>.html", publishing)
        self.assertIn("Markdown-only or incompatible", publishing)
        self.assertIn("keep the completed HTML locally", publishing)


if __name__ == "__main__":
    unittest.main()
