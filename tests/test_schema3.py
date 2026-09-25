"""3.0 contract regressions. All retrieval records here are stipulated test packets."""
import copy
import json
import unittest
from pathlib import Path

from scripts.schema3_checks import ACTION_LABELS, HEADINGS, SOURCE_LADDER, unresolved_paths, validate_schema3
from scripts.render_report import render_report
from scripts.validate_analysis import schema_validator, validate_report
from test_provisional_scoring import (
    provisional_report, mark_unknown, suspend_model, bound_module, refresh_provisional,
)
from test_income_audit import screen_report


def event(observable="董事会公告现金分红已获批准并注明付款日"):
    return {"kind": "event", "observable": observable, "operator": "published",
            "threshold": "已公告", "unit": "公告事件", "source_to_watch": "公司公告与交易所披露"}


def attach_research(report):
    """Synthetic packet declaration, never a claim that live retrieval occurred."""
    paths = sorted(unresolved_paths(report))
    records = []
    if paths:
        records.append({
            "field_paths": paths, "reason": "虚构测试包未提供这些输入",
            "impact": "保留各分项的贡献区间；资金约束独立限制买入",
            "resolution": "not_assessable",
            "attempts": [{
                "category": category, "scope": "investor" if category == "broker_records" else "issuer",
                "source": "虚构封闭测试包（不是在线取数）", "source_period": "截至测试截止日",
                "attempted_on": report.get("as_of_date", "2026-01-01"),
                "outcome": "not_provided" if category == "broker_records" else "not_found",
                "result": "仅核对封闭测试包；该类资料未提供，未声称检索真实公司",
            } for category in SOURCE_LADDER],
            "estimate": None,
            "estimate_failure_reason": "虚构包未含经营与现金敏感性锚，无法有据收窄输入区间",
            "closure_condition": event(),
        })
    report["evidence_recovery"] = {
        "scope": "provided_packet", "scope_reason": "单元测试限定虚构输入，不进行真实公司研究",
        "is_group_structure": False, "records": records,
    }


def attach_schema3(report):
    report["schema_version"] = "3.0"
    headings = HEADINGS if report["mode"] == "full_analysis" else (
        ("筛选摘要", "候选标的", "来源与限制") if report["mode"] == "screen"
        else ("基线与新披露", "现金与资本", "复检结论与来源"))
    report["report_output"] = {
        "language": "zh-CN", "user_requested_language": None,
        "title": "虚构公司股息研究示例", "summary": "仅用于验证规则，不构成真实投资意见。",
        "sections": [{"heading": heading, "paragraphs": ["本节仅使用虚构测试包的已知事实与明确假设。"]}
                     for heading in headings],
        "appendix": [], "labels": ["金额单位：报告币种"],
    }
    if report["mode"] == "full_analysis":
        action = ACTION_LABELS[report["entry_plan"]["current_action"]]
        stages = {row["stage"]: row for row in report["entry_plan"]["stages"]}
        blocked = any(row["valuation_price"] is None or row["effective_price"] is None for row in stages.values())
        prices = {key: None if blocked else stages[key]["valuation_price"]
                  for key in ("starter", "add", "strong_buy")}
        prices["income_capped_upper"] = None if blocked else stages["starter"]["effective_price"]
        condition = event() if blocked else {
            "kind": "price", "observable": "市场成交价格不高于收入约束上限", "operator": "<=",
            "threshold": prices["income_capped_upper"], "unit": report["return_requirements"]["valuation_currency"],
            "source_to_watch": "交易所实时报价",
        }
        report["decision"] = {
            "current_action": action, "can_buy_now": action in ("立即买入", "分批建仓"),
            "reason": "已核对资金与风险门槛，按对应状态执行；不以价格下跌替代公司质量判断。",
            "buy_conditions": [condition],
            "invalidation_conditions": [event("董事会公告削减普通现金股息")],
            "trap_conclusion": "已识别现金与资本约束，保持对应风险限制，不将未知视为安全。",
            "entry_conclusion": "当前不买，等待指定公告解除资金限制。" if blocked else
                                "参考价已列示，执行前须同时通过资金、税务、资本与风险门槛。",
            "price_status": "blocked" if blocked else "reference_prices",
            "reference_prices": prices,
        }
    attach_research(report)
    return report


def current_report():
    return attach_schema3(provisional_report())


class Schema3Tests(unittest.TestCase):
    def assertInvalid(self, report, fragment=None):
        errors = validate_report(report)
        self.assertTrue(errors)
        if fragment:
            self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_default_and_both_critical_dispatches(self):
        schema = schema_validator().schema
        self.assertEqual(schema["properties"]["schema_version"]["default"], "3.0")
        self.assertEqual(schema["properties"]["schema_version"]["enum"], ["2.3", "2.4", "2.5", "3.0"])
        for index in (4, 18):
            self.assertEqual(schema["allOf"][index]["if"]["properties"]["schema_version"]["enum"], ["2.5", "3.0"])

    def test_current_complete_record_and_legacy_25_are_valid(self):
        self.assertEqual(validate_report(current_report()), [])
        legacy = provisional_report()
        self.assertEqual(validate_report(legacy), [])
        self.assertNotIn("evidence_recovery", legacy)

    def test_scorecard_cannot_disappear_under_30(self):
        for key in ("scorecard", "entry_plan", "rating_audit", "decision", "report_output", "evidence_recovery"):
            report = current_report()
            del report[key]
            self.assertInvalid(report, key)

    def test_rubric1_cannot_silently_dispatch_for_30(self):
        report = current_report()
        report["scorecard"]["rubric_version"] = "1"
        self.assertInvalid(report)

    def test_missing_module_keeps_numeric_quality_and_combined_bounds(self):
        report = provisional_report()
        mark_unknown(report, "buyback_quality")
        attach_schema3(report)
        self.assertEqual(validate_report(report), [])
        self.assertEqual(report["scorecard"]["summary"]["score_range"], {"low": 71, "high": 81})
        self.assertEqual(report["scorecard"]["summary"]["evidence_coverage_pct"], 90)
        self.assertIn("71–81/100", render_report(report))

    def test_zero_coverage_still_has_numeric_bounds_not_a_zero_company_score(self):
        report = provisional_report()
        for row in list(report["scorecard"]["modules"]):
            mark_unknown(report, row["module"])
        attach_schema3(report)
        self.assertEqual(validate_report(report), [])
        self.assertEqual(report["scorecard"]["summary"]["score_range"], {"low": 0, "high": 100})
        self.assertIsNone(report["score_100"])

    def test_score_range_and_coverage_must_match_actual_modules(self):
        for key in ("score_range", "evidence_coverage_pct"):
            report = current_report()
            if key == "score_range":
                report["scorecard"]["summary"][key]["high"] += 1
            else:
                report["scorecard"]["summary"][key] -= 1
            self.assertInvalid(report)

    def test_action_is_single_fixed_enum(self):
        for value in ("", "待确认", "立即买入 / 继续观察", None):
            report = current_report()
            report["decision"]["current_action"] = value
            self.assertInvalid(report)

    def test_three_answers_are_all_required(self):
        for key in ("can_buy_now", "reason", "buy_conditions", "invalidation_conditions"):
            report = current_report()
            del report["decision"][key]
            self.assertInvalid(report, key)

    def test_buy_answer_cannot_contradict_gate(self):
        report = current_report()
        report["decision"]["can_buy_now"] = False
        self.assertInvalid(report, "can_buy_now")

    def test_placeholders_do_not_count_as_final_conclusions(self):
        for key in ("reason", "trap_conclusion", "entry_conclusion"):
            report = current_report()
            report["decision"][key] = "数据不足，暂不给出，待确认"
            self.assertInvalid(report, "placeholder")

    def test_vague_release_is_rejected(self):
        report = current_report()
        report["decision"]["buy_conditions"] = [event("补齐资金证据后")]
        self.assertInvalid(report, "specific observable")

    def test_reference_prices_and_income_cap_are_recomputed(self):
        for key in ("starter", "add", "strong_buy", "income_capped_upper"):
            report = current_report()
            report["decision"]["reference_prices"][key] += 1
            self.assertInvalid(report, "price")

    def test_duplicate_stages_return_validation_error_not_exception(self):
        report = current_report()
        report["entry_plan"]["stages"][0] = copy.deepcopy(report["entry_plan"]["stages"][1])
        self.assertInvalid(report, "three entry stages")

    def test_finite_life_projection_does_not_invent_two_more_prices(self):
        report = current_report()
        report["valuation_mode"] = "finite_life_harvest"
        for row in report["entry_plan"]["stages"][1:]:
            row.update(valuation_price=None, effective_price=None)
            report["decision"]["reference_prices"][row["stage"]] = None
        self.assertEqual(validate_schema3(report), [])
        report["decision"]["reference_prices"]["strong_buy"] = 1
        self.assertTrue(any("finite-life" in error for error in validate_schema3(report)))

    def test_blocked_funding_produces_definite_no_buy_not_blank_scores(self):
        report = provisional_report()
        suspend_model(report)
        attach_schema3(report)
        self.assertEqual(validate_report(report), [])
        self.assertEqual(report["decision"]["current_action"], "继续观察")
        self.assertFalse(report["decision"]["can_buy_now"])
        self.assertIsInstance(report["scorecard"]["summary"]["quality_range"]["low"], int)

    def test_cheaper_price_alone_cannot_release_funding(self):
        report = provisional_report()
        suspend_model(report)
        attach_schema3(report)
        report["decision"]["buy_conditions"] = [{
            "kind": "price", "observable": "股价低于指定价格", "operator": "<=",
            "threshold": 1, "unit": report["return_requirements"]["valuation_currency"], "source_to_watch": "交易所报价",
        }]
        self.assertInvalid(report, "release event")

    def test_gap_requires_actual_ordered_attempts(self):
        for mutation in ("missing", "reverse", "empty"):
            report = current_report()
            attempts = report["evidence_recovery"]["records"][0]["attempts"]
            if mutation == "missing":
                attempts.pop(3)
            elif mutation == "reverse":
                attempts.reverse()
            else:
                attempts[0]["result"] = ""
            self.assertInvalid(report)

    def test_gap_cannot_be_hidden_by_empty_log(self):
        report = current_report()
        report["evidence_recovery"]["records"] = []
        self.assertInvalid(report, "unresearched gap")

    def test_group_needs_both_disclosure_levels(self):
        report = current_report()
        report["evidence_recovery"]["is_group_structure"] = True
        self.assertInvalid(report, "parent and subsidiary")
        attempts = report["evidence_recovery"]["records"][0]["attempts"]
        attempts[1]["scope"] = "parent"
        subsidiary = copy.deepcopy(attempts[1])
        subsidiary["scope"] = "subsidiary"
        attempts.insert(2, subsidiary)
        self.assertEqual(validate_report(report), [])

    def test_future_retrieval_is_not_point_in_time_evidence(self):
        report = current_report()
        report["evidence_recovery"]["records"][0]["attempts"][0]["attempted_on"] = "2099-01-01"
        self.assertInvalid(report, "postdate")

    def test_successful_retrieval_must_identify_declared_source(self):
        report = current_report()
        report["evidence_recovery"]["records"][0]["attempts"][0]["outcome"] = "found"
        self.assertInvalid(report, "declared sources")

    def test_live_attempt_cannot_be_a_generic_packet_claim(self):
        report = current_report()
        report["evidence_recovery"]["scope"] = "live_research"
        self.assertInvalid(report, "actual source URL")

    def test_publication_summary_cannot_hide_a_blank_conclusion(self):
        report = current_report()
        report["report_output"]["summary"] = "评分暂不评估，买点暂不给出。"
        self.assertInvalid(report, "publication summary")

    def test_appendix_has_a_working_navigation_anchor(self):
        report = current_report()
        report["report_output"]["appendix"] = ["本附录说明各分项计算与取数边界。"]
        output = render_report(report)
        self.assertIn('href="#audit-appendix"', output)
        self.assertIn('id="audit-appendix"', output)

    def test_not_assessable_requires_estimate_failure_explanation(self):
        report = current_report()
        report["evidence_recovery"]["records"][0]["estimate_failure_reason"] = None
        self.assertInvalid(report)

    def test_bounded_estimate_requires_basis_period_and_valid_endpoints(self):
        report = current_report()
        record = report["evidence_recovery"]["records"][0]
        record.update(resolution="bounded", estimate_failure_reason=None, estimate={
            "low": 1, "high": 2, "unit": "测试单位", "derivation": "虚构上下界重建",
            "source_period": "测试期间", "applicability": "仅适用于封闭测试包",
            "source_refs": [report["sources"][0]],
        })
        self.assertEqual(validate_report(report), [])
        record["estimate"]["high"] = 0
        self.assertInvalid(report, "reversed")

    def test_recovery_paths_must_resolve_and_not_duplicate(self):
        for bad in ("/nonexistent", "/evidence_recovery/scope"):
            report = current_report()
            report["evidence_recovery"]["records"][0]["field_paths"].append(bad)
            self.assertInvalid(report)
        report = current_report()
        paths = report["evidence_recovery"]["records"][0]["field_paths"]
        paths.append(paths[0])
        self.assertInvalid(report, "one unambiguous")

    def test_chinese_visible_content_and_appendix(self):
        for field in ("title", "summary", "appendix", "labels"):
            report = current_report()
            report["report_output"][field] = ["English only prose"] if field in ("appendix", "labels") else "English only prose"
            self.assertInvalid(report, "Chinese")

    def test_mixed_untranslated_paragraph_is_rejected(self):
        report = current_report()
        report["report_output"]["sections"][0]["paragraphs"] = ["结论：This company has strong cash generation."]
        self.assertInvalid(report, "untranslated")

    def test_language_override_must_be_explicit(self):
        report = current_report()
        report["report_output"]["language"] = "en-US"
        self.assertInvalid(report, "explicit language")
        report["report_output"]["user_requested_language"] = "en-US"
        self.assertEqual(validate_report(report), [])
        with self.assertRaisesRegex(ValueError, "localized template"):
            render_report(report)

    def test_current_examples_in_all_available_modes(self):
        root = Path(__file__).resolve().parents[1] / "dividend-income-equity-analysis"
        for path in (root / "examples").glob("*.analysis.json"):
            report = json.loads(path.read_text(encoding="utf-8"))
            if report["schema_version"] != "3.0":
                attach_schema3(report)
            self.assertEqual(validate_report(report), [], path.name)

    def test_screen_uses_chinese_and_recovery_without_full_analysis(self):
        report = attach_schema3(screen_report())
        self.assertEqual(validate_report(report), [])
        rendered = render_report(report)
        self.assertIn("筛选摘要", rendered)
        self.assertNotIn("质量评分：", rendered)
        report["report_output"]["sections"][0]["paragraphs"] = ["English only screening summary"]
        self.assertInvalid(report, "Chinese")

    def test_safety_review_language_is_enforced(self):
        root = Path(__file__).resolve().parents[1] / "dividend-income-equity-analysis"
        report = json.loads((root / "examples" / "safety-review.analysis.json").read_text(encoding="utf-8"))
        attach_schema3(report)
        report["report_output"]["summary"] = "English only safety summary"
        self.assertInvalid(report, "Chinese")

    def test_safety_review_never_gets_decisions_scores_or_valuation(self):
        root = Path(__file__).resolve().parents[1] / "dividend-income-equity-analysis"
        report = json.loads((root / "examples" / "safety-review.analysis.json").read_text(encoding="utf-8"))
        attach_schema3(report)
        self.assertEqual(validate_report(report), [])
        for key in ("decision", "scorecard", "buy_zone", "entry_plan"):
            changed = copy.deepcopy(report)
            changed[key] = current_report()[key]
            self.assertInvalid(changed)

    def test_html_is_static_chinese_and_escaped(self):
        report = current_report()
        report["report_output"]["title"] = "测试公司<script>标记</script>"
        output = render_report(report)
        self.assertIn("&lt;script&gt;", output)
        self.assertNotIn("{{", output)
        for label in ("当前动作", "研究覆盖度", "收入约束上限", "结论失效条件"):
            self.assertIn(label, output)
        self.assertNotIn("fetch(", output)


if __name__ == "__main__":
    unittest.main()
