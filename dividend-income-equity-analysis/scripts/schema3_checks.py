"""Schema 3.0 conclusions, retrieval provenance and reader-language checks."""
import math
import re

SOURCE_LADDER = (
    "issuer_filings", "group_disclosures", "announcements", "exchange_regulator",
    "official_series", "historical_comparables", "broker_records",
)
ACTION_LABELS = {
    "strong_buy": "立即买入", "buy": "立即买入", "accumulate": "分批建仓",
    "wait_for_price": "等待到价", "wait_for_evidence": "继续观察", "avoid": "回避",
}
HEADINGS = (
    "结论速览", "财务状况", "买点观点", "长期展望：业务与股息",
    "风险点与跟踪信号", "数据来源与关键假设",
)
PLACEHOLDERS = ("数据不足", "暂不给出", "暂不评估", "待确认", "不可评估",
                "Not Assessable", "cannot score")
GAP_VALUES = {
    "unknown", "not_assessable", "insufficient", "not_assessed", "unavailable",
    "Unclear", "Not Forecastable", "bounded", "missing", "conflicting", "Unknown",
}


def unresolved_paths(report):
    """Point to actual unresolved inputs, not legitimate null aggregate scalars."""
    paths = set()

    def visit(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                child = path + "/" + key.replace("~", "~0").replace("/", "~1")
                if key in ("decision", "report_output", "evidence_recovery"):
                    continue
                if isinstance(value, str) and value in GAP_VALUES:
                    paths.add(child)
                if key in ("missing_inputs", "missing_evidence") and value:
                    paths.add(child)
                visit(value, child)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(value, f"{path}/{index}")

    visit(report, "")
    return paths


def resolve_pointer(report, pointer):
    node = report
    for part in pointer[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def validate_schema3(report):
    if report.get("schema_version") != "3.0":
        return []
    errors = []

    def require(condition, message):
        if not condition:
            errors.append("Schema 3.0: " + message)

    research = report["evidence_recovery"]
    covered = set()
    cutoff = report.get("as_of_date")
    if cutoff is None and report.get("screen_results"):
        cutoff = min(row["as_of_date"] for row in report["screen_results"])
    for record in research["records"]:
        attempts = record["attempts"]
        order = [SOURCE_LADDER.index(row["category"]) for row in attempts]
        require(order == sorted(order) and set(order) == set(range(7)),
                "each gap needs the ordered seven-category retrieval ladder before estimation")
        for row in attempts:
            require(cutoff is None or row["attempted_on"] <= cutoff,
                    "retrieval dates cannot postdate the report cutoff")
            if row["outcome"] == "found":
                require(row["source"] in report.get("sources", []),
                        "successful retrievals must cite declared sources")
            if research["scope"] == "live_research" and row["outcome"] not in ("not_applicable", "not_provided"):
                require(bool(re.match(r"https?://", row["source"])),
                        "live retrieval attempts require the actual source URL")
            require(row["outcome"] != "not_provided" or row["category"] == "broker_records",
                    "not_provided is reserved for absent user broker records")
        if research["is_group_structure"]:
            group = [row for row in attempts if row["category"] == "group_disclosures"]
            require({"parent", "subsidiary"} <= {row["scope"] for row in group},
                    "group structures require separate parent and subsidiary disclosure attempts")
            require(all(row["outcome"] != "not_applicable" for row in group),
                    "parent/subsidiary retrieval cannot be waived for a group structure")
        for pointer in record["field_paths"]:
            require(pointer not in covered, "a gap field must have one unambiguous recovery record")
            try:
                resolve_pointer(report, pointer)
            except (KeyError, IndexError, TypeError, ValueError):
                require(False, f"recovery pointer does not identify a report field: {pointer}")
            require(not pointer.startswith(("/evidence_recovery", "/report_output", "/decision")),
                    "recovery must identify analytical inputs, not its own record or conclusion")
            covered.add(pointer)
        estimate = record["estimate"]
        if estimate is not None:
            require(estimate["low"] <= estimate["high"], "bounded estimate endpoints are reversed")
            require(all(ref in report.get("sources", []) for ref in estimate["source_refs"]),
                    "bounded estimate sources must be declared")
        if record["resolution"] in ("reported", "reconstructed"):
            require(any(row["outcome"] == "found" for row in attempts),
                    "recovered facts require at least one successful retrieval")
    for pointer in sorted(unresolved_paths(report) - covered):
        require(False, f"unresearched gap: {pointer}")

    output = report["report_output"]
    language = output["language"]
    require(language == "zh-CN" or output["user_requested_language"] == language,
            "non-Chinese output requires the user's explicit language override")
    require(output["user_requested_language"] is None or output["user_requested_language"] == language,
            "the requested and rendered language must agree")
    visible = [output["title"], output["summary"], *output["appendix"], *output["labels"]]
    for section in output["sections"]:
        visible.extend([section["heading"], *section["paragraphs"]])
    for record in research["records"]:
        visible.extend([record["reason"], record["impact"]])
        visible.extend(row["result"] for row in record["attempts"])
        if record["estimate"]:
            visible.extend([record["estimate"]["derivation"], record["estimate"]["applicability"]])
        if record["estimate_failure_reason"]:
            visible.append(record["estimate_failure_reason"])
    if report["mode"] == "full_analysis":
        decision = report["decision"]
        visible.extend([decision["reason"], decision["trap_conclusion"], decision["entry_conclusion"]])
        for condition in decision["buy_conditions"] + decision["invalidation_conditions"]:
            visible.append(condition["observable"])
        expected = ACTION_LABELS[report["entry_plan"]["current_action"]]
        require(decision["current_action"] == expected, "current action contradicts the audited entry gates")
        buying = expected in ("立即买入", "分批建仓")
        require(decision["can_buy_now"] == buying, "can_buy_now must match the single current action")
        for key in ("reason", "trap_conclusion", "entry_conclusion"):
            require(not any(word.lower() in decision[key].lower() for word in PLACEHOLDERS),
                    f"{key} must be a definite conclusion, not a placeholder")
        require(not any(word.lower() in output["summary"].lower() for word in PLACEHOLDERS),
                "publication summary must not replace the conclusion with a placeholder")
        conditions = decision["buy_conditions"]
        vague = ("补齐资金证据", "等待确认", "进一步研究", "数据完善", "资料齐全")
        for condition in conditions + decision["invalidation_conditions"]:
            require(not any(word in condition["observable"] for word in vague),
                    "conditions must identify a specific observable threshold or publication event")
            require(not any(word in str(condition["threshold"]) for word in PLACEHOLDERS),
                    "condition thresholds cannot be placeholders")
            if condition["kind"] == "price":
                require(condition["unit"] == report["return_requirements"]["valuation_currency"],
                        "price conditions must use the report's price currency")
        if expected == "等待到价":
            require(any(c["kind"] == "price" and c["operator"] in ("<", "<=")
                        and c["threshold"] < report["price_used"] for c in conditions),
                    "waiting for price needs a specific lower entry price")
        prices = decision["reference_prices"]
        stages = {row["stage"]: row for row in report["entry_plan"]["stages"]}
        if set(stages) != {"starter", "add", "strong_buy"}:
            require(False, "the decision requires each of the three entry stages exactly once")
            return errors
        if decision["price_status"] == "reference_prices":
            for stage in ("starter", "add", "strong_buy"):
                if report["valuation_mode"] == "finite_life_harvest" and stage != "starter":
                    require(prices[stage] is None and stages[stage]["valuation_price"] is None,
                            "finite-life harvest must not invent additional entry stages")
                    continue
                require(prices[stage] is not None and stages[stage]["valuation_price"] is not None
                        and math.isclose(prices[stage], stages[stage]["valuation_price"], rel_tol=1e-6),
                        f"{stage} reference price must equal the audited valuation ladder")
            cap = stages["starter"]["effective_price"]
            require(prices["income_capped_upper"] is not None and cap is not None
                    and math.isclose(prices["income_capped_upper"], cap, rel_tol=1e-6),
                    "income-capped upper must equal the effective starter price")
        else:
            require(not buying, "blocked prices cannot authorize a purchase")
            require(any(c["kind"] == "event" for c in conditions),
                    "blocked funding needs a concrete release event; a cheaper price alone cannot repair it")
            require(all(value is None for value in prices.values()),
                    "blocked prices must not fabricate an executable ladder")
            require(report["valuation_mode"] == "suspended"
                    or any(row["valuation_price"] is None or row["effective_price"] is None
                           for row in stages.values()),
                    "available reference prices must not be hidden behind a blocked label")
        if language == "zh-CN":
            require(tuple(row["heading"] for row in output["sections"]) == HEADINGS,
                    "Full Analysis must retain the six Chinese report sections")

    if language == "zh-CN":
        # Formal source names and fixed machine enums are exempt, not arbitrary prose.
        exempt = set(report.get("sources", []))
        for text in visible:
            if text in exempt:
                continue
            require(bool(re.search(r"[\u3400-\u9fff]", text)),
                    "reader-visible narrative must be Simplified Chinese")
            scrubbed = re.sub(r"https?://\S+|\b[A-Z][A-Z0-9./+-]*\b", "", text)
            for source in sorted(exempt, key=len, reverse=True):
                scrubbed = scrubbed.replace(source, "")
            require(not re.search(r"\b[a-zA-Z]{3,}\s+[a-zA-Z]{3,}\s+[a-zA-Z]{3,}\b", scrubbed),
                    "untranslated English prose is not allowed in reader-visible content")
    return errors
