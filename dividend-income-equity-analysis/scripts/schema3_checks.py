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
FULL_HEADINGS = (
    "摘要与投资结论", "公司概况与行业定位", "行业结构、供需与周期",
    "竞争格局与公司护城河", "过去五年经营与财务趋势",
    "现金流、资产负债与股息质量", "企业成长性与资本配置",
    "未来五年经营与现金流预测", "估值与预期总回报",
    "买点、建仓策略与持仓复评", "风险、监测指标与论点证伪",
    "数据来源、关键假设与研究限制",
)
TWELVE_CHAPTER_REQUIRED_FROM = "2026-11-10"
SPREAD_MODELS = {"bank", "bdc", "mortgage_reit", "insurer"}
OPERATING_MODELS = {"operating_company", "utility_infrastructure",
                    "concession_infrastructure", "midstream_partnership"}
TEMPLATE_MARKERS = re.compile(r"[Ff]ictional|teaching (?:case|assumption|input|calculation)|worked-examples\.md|"
                              r"虚构|教学案例|教学假设|示例公司")
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


def economic_profile_errors(report):
    """Cross-dimension routing rules from economic-profile.md."""
    profile = report["economic_profile"]
    model = report["cash_flow_model"]
    sector, overlays = model["sector_model"], set(model["overlays"])
    segments = profile["segments"]
    errors = []

    def check(condition, message):
        if not condition:
            errors.append("economic_profile: " + message)

    total = sum(row["cash_share_pct"] for row in segments)
    check(95 <= total <= 105, f"segment cash shares must sum to about 100%, got {total:g}%")
    for row in segments:
        check(row["cyclicality"] == "stable" or row["cycle_window"] is not None,
              f"segment '{row['name']}' is cyclical and needs a cycle_window")
    for row in segments:
        check(row["revenue_engine"] != "spread_income" or row["balance_sheet_role"] == "balance_sheet_spread",
              f"segment '{row['name']}' earns spread_income, so its balance_sheet_role must be balance_sheet_spread")
        check(row["revenue_engine"] != "commodity_linked" or row["cyclicality"] != "stable",
              f"segment '{row['name']}' is commodity_linked and cannot be classed as stable")
    finite_segments = [row for row in segments if row["asset_life"] == "finite_assets"]
    for asset in profile["finite_life_assets"]:
        earliest = asset.get("earliest_end_year")
        check(earliest is None or earliest <= asset["end_year"],
              f"finite asset '{asset['name']}': earliest_end_year cannot be after end_year")
    check(bool(finite_segments) == bool(profile["finite_life_assets"]),
          "finite_assets segments and the finite_life_assets schedule must appear together")
    mode = report.get("valuation_mode")
    check(mode != "finite_life_harvest" or profile["company_level_runoff"],
          "finite_life_harvest needs an evidenced company-level run-off; finite assets alone are valued asset by asset")
    check(not profile["company_level_runoff"] or mode in ("finite_life_harvest", "suspended"),
          "a company-level run-off must use finite_life_harvest or be suspended")
    dominant = max(segments, key=lambda row: row["cash_share_pct"])
    spread = lambda row: row["balance_sheet_role"] == "balance_sheet_spread"
    other_side = [row for row in segments if spread(row) != spread(dominant)]
    material_side = sum(row["cash_share_pct"] for row in other_side) >= 20
    for row in other_side:
        if not material_side:   # materiality is judged for the whole other side, not segment by segment
            continue
        check(sector == "holding_company" or "holding_company" in overlays,
              f"material segment '{row['name']}' ({row['cash_share_pct']:g}%) runs on a different balance sheet from the "
              "dominant segment; use the holding_company model or overlay to add up segment cash at the parent")
        check(bool(row.get("capital_bridge")),
              f"material segment '{row['name']}' needs a capital_bridge: its own cash/capital generation, "
              "regulatory constraint and upstream route")
    if dominant["balance_sheet_role"] == "balance_sheet_spread":
        check(sector in SPREAD_MODELS or sector == "holding_company",
              "a balance-sheet spread business must use a spread/capital proxy, not industrial FCF")
    else:
        check(sector not in SPREAD_MODELS,
              "an operating or leasing business must not use a bank/BDC/insurer/mortgage-REIT proxy")
    check(mode != "capital_return_based" or dominant["balance_sheet_role"] == "balance_sheet_spread",
          "capital_return_based valuation is for balance-sheet spread businesses (banks, insurers, BDCs, mortgage REITs)")
    spread_share = sum(row["cash_share_pct"] for row in segments if spread(row))
    check(mode != "capital_return_based" or sector in ("bank", "insurer")
          or (sector == "holding_company" and spread_share >= 50),
          "capital_return_based (RoTE on tangible book) fits banks and insurers; BDCs and mortgage REITs use NAV and "
          "net investment income through their sector cash models")
    check(sector != "mortgage_reit" or profile["legal_wrapper"] == "reit",
          "mortgage_reit requires the reit legal wrapper")
    check(sector != "concession_infrastructure" or bool(finite_segments),
          "concession_infrastructure requires finite concession assets in the profile")
    check(profile["legal_wrapper"] != "fund_or_etf",
          "funds/ETFs are outside the issuer Full Analysis; use a fund method")
    if profile["cash_attribution"] == "material_jv_associates" or profile["legal_wrapper"] == "holding_parent":
        check(sector == "holding_company" or "holding_company" in overlays,
              "JV/associate or parent-level cash needs the holding_company model or overlay")
    tax = profile["tax_route"]
    check(tax["refunds_excluded_from_cash"], "possible tax refunds must stay out of spendable cash")
    is_ptp = profile["legal_wrapper"] == "us_publicly_traded_partnership"
    check(is_ptp == (tax["distribution_regime"] == "us_1446a"),
          "the §1446(a) distribution route applies to, and only to, US publicly traded partnerships")
    if is_ptp:
        rate = tax["exit_withholding_rate"]
        check(rate is not None, "a PTP must record §1446(f) exit withholding")
        check(rate is None or abs(rate - 0.10) < 1e-9 or tax["exception_evidence"] is not None,
              "§1446(f) exit withholding other than 10% needs documented exception evidence")
    return errors


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
        for table in section.get("tables", []):
            visible.extend([table["title"], table["note"]])
            require(all(len(row) == len(table["columns"]) for row in table["rows"]),
                    f"table '{table['title']}' rows must match its column count")
        for chart in section.get("charts", []):
            visible.extend([chart["title"], chart["source"]])
            require(all(len(row["values"]) == len(chart["x_labels"]) for row in chart["series"]),
                    f"chart '{chart['title']}' series must match its x labels")
            require(chart["kind"] != "stacked_bar" or all(
                        value is None or value >= 0 for row in chart["series"] for value in row["values"]),
                    f"stacked chart '{chart['title']}' components must be non-negative")
            require(any(value is not None for row in chart["series"] for value in row["values"]),
                    f"chart '{chart['title']}' needs at least one observed value")
    if "economic_profile" in report:
        profile = report["economic_profile"]
        visible.append(profile["classification_evidence"])
        visible.extend(row["name"] for row in profile["segments"])
        visible.extend(row["why_causal"] for row in profile["kpis"])
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
        returns = report["return_requirements"]
        price_units = {returns["valuation_currency"]: 1.0}
        if returns.get("quote_currency") and returns.get("quote_per_valuation_unit"):
            price_units[returns["quote_currency"]] = returns["quote_per_valuation_unit"]
        vague = ("补齐资金证据", "等待确认", "进一步研究", "数据完善", "资料齐全")
        for condition in conditions + decision["invalidation_conditions"]:
            require(not any(word in condition["observable"] for word in vague),
                    "conditions must identify a specific observable threshold or publication event")
            require(not any(word in str(condition["threshold"]) for word in PLACEHOLDERS),
                    "condition thresholds cannot be placeholders")
            if condition["kind"] == "price":
                require(condition["unit"] in price_units,
                        "price conditions must use the valuation currency or the declared quote currency")
        if expected == "等待到价":
            require(any(c["kind"] == "price" and c["operator"] in ("<", "<=") and c["unit"] in price_units
                        and c["threshold"] / price_units[c["unit"]] < report["price_used"] for c in conditions),
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
        headings = tuple(row["heading"] for row in output["sections"])
        if language == "zh-CN":
            require(headings in (HEADINGS, FULL_HEADINGS),
                    "Full Analysis must use the legacy six-section or complete twelve-chapter Chinese structure")
        contract = report.get("report_contract_version")
        # A declared twelve_chapter contract binds whatever the data date (backtests); legacy is archive-only.
        new_report = contract == "twelve_chapter" or str(report.get("as_of_date") or "") >= TWELVE_CHAPTER_REQUIRED_FROM
        if new_report and language == "zh-CN":
            require(headings == FULL_HEADINGS,
                    "reports dated from 2026-11-10 or declaring report_contract_version twelve_chapter must use the "
                    "twelve-chapter structure; six sections are archive-only")
        if new_report or headings == FULL_HEADINGS or "economic_profile" in report:
            require("economic_profile" in report,
                    "a twelve-chapter Full Analysis must record economic_profile (economic-profile.md)")
            if "economic_profile" in report:
                for message in economic_profile_errors(report):
                    require(False, message)

    if research["scope"] == "live_research":
        residue = []

        def scan(node, path):
            if isinstance(node, dict):
                for key, child in node.items():
                    scan(child, f"{path}/{key}")
            elif isinstance(node, list):
                for index, child in enumerate(node):
                    scan(child, f"{path}/{index}")
            elif isinstance(node, str) and TEMPLATE_MARKERS.search(node):
                residue.append(path)

        scan(report, "")
        require(not residue, "live research still contains template example text at "
                + ", ".join(residue[:5]) + (" ..." if len(residue) > 5 else ""))
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
