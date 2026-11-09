"""Render validated schema 3.0 records as an offline, single-file HTML report."""
import argparse
import math
import html
import json
from pathlib import Path

if __package__:
    from .validate_analysis import validate_report
else:
    from validate_analysis import validate_report


SERIES_COLORS = ("var(--cp-accent)", "var(--cp-link)", "var(--cp-success)",
                 "var(--cp-warning)", "var(--cp-text-muted)")


def _cell(value):
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value) if 1800 <= value <= 2300 else f"{value:,}"  # years print without separators
    return str(value)


def span(low, high):
    return f"{low}" if low == high else f"{low}–{high}"


def render_table(table):
    """A chapter table; null cells show an explicit gap, never zero."""
    escape = html.escape
    head = "".join(f"<th scope=\"col\">{escape(col)}</th>" for col in table["columns"])

    def cell(value):
        text = _cell(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return f'<td class="numeric">{escape(text)}</td>'
        if len(text) <= 10 and " " not in text:
            return f'<td class="nowrap">{escape(text)}</td>'
        return f"<td>{escape(text)}</td>"

    body = "".join("<tr>" + "".join(cell(value) for value in row) + "</tr>" for row in table["rows"])
    return (f'<div class="table-scroll"><table><caption>{escape(table["title"])}</caption>'
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
            f'<p class="muted">口径与来源：{escape(table["note"])}</p>')


def render_chart(chart):
    """Static inline SVG line, grouped-bar or stacked-bar chart with one unit axis; nulls are gaps. Readable offline with scripts disabled."""
    escape = html.escape
    width, height, left, right, top, bottom = 640, 300, 64, 16, 16, 48
    labels, series = chart["x_labels"], chart["series"]
    values = [v for row in series for v in row["values"] if v is not None]
    if chart["kind"] == "stacked_bar":
        values += [sum(row["values"][i] or 0 for row in series) for i in range(len(labels))]
    low, high = min(0.0, min(values)), max(0.0, max(values))
    if high == low:
        high = low + 1.0
    raw_step = (high - low) / 4
    magnitude = 10 ** math.floor(math.log10(raw_step))
    tick = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw_step)
    low, high = math.floor(low / tick) * tick, math.ceil(high / tick) * tick
    plot_w, plot_h = width - left - right, height - top - bottom
    step = plot_w / len(labels)

    def y(value):
        return top + plot_h * (high - value) / (high - low)

    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(chart["title"])}">']
    for index in range(round((high - low) / tick) + 1):
        value = low + tick * index
        ty = y(value)
        parts.append(f'<line x1="{left}" x2="{width - right}" y1="{ty:.1f}" y2="{ty:.1f}" '
                     'style="stroke:var(--cp-border);stroke-width:1"/>')
        parts.append(f'<text x="{left - 6}" y="{ty + 4:.1f}" text-anchor="end" font-size="11" '
                     f'style="fill:var(--cp-text-muted)">{escape(_cell(round(value, 2)))}</text>')
    for index, label in enumerate(labels):
        cx = left + step * (index + 0.5)
        parts.append(f'<text x="{cx:.1f}" y="{height - bottom + 18}" text-anchor="middle" font-size="11" '
                     f'style="fill:var(--cp-text-muted)">{escape(label)}</text>')
    zero = y(0.0)
    bar_w = step * 0.7 / len(series)
    stack = [0.0] * len(labels)
    for number, row in enumerate(series):
        color = SERIES_COLORS[number % len(SERIES_COLORS)]
        if chart["kind"] == "stacked_bar":
            for index, value in enumerate(row["values"]):
                if value is None:
                    continue
                base, stack[index] = stack[index], stack[index] + value
                parts.append(f'<rect x="{left + step * (index + 0.2):.1f}" y="{y(stack[index]):.1f}" '
                             f'width="{step * 0.6:.1f}" height="{abs(y(base) - y(stack[index])):.1f}" '
                             f'style="fill:{color}"/>')
        elif chart["kind"] == "bar":
            for index, value in enumerate(row["values"]):
                if value is None:
                    continue
                bx = left + step * (index + 0.15) + bar_w * number
                parts.append(f'<rect x="{bx:.1f}" y="{min(y(value), zero):.1f}" width="{bar_w:.1f}" '
                             f'height="{abs(zero - y(value)):.1f}" style="fill:{color}"/>')
        else:
            segment = []
            for index, value in enumerate(row["values"] + [None]):
                if value is not None:
                    segment.append(f"{left + step * (index + 0.5):.1f},{y(value):.1f}")
                    continue
                if len(segment) > 1:
                    parts.append(f'<polyline points="{" ".join(segment)}" '
                                 f'style="fill:none;stroke:{color};stroke-width:2"/>')
                for point in segment:
                    px, py = point.split(",")
                    parts.append(f'<circle cx="{px}" cy="{py}" r="3" style="fill:{color}"/>')
                segment = []
    parts.append("</svg>")
    legend = "；".join(
        f'<span style="color:{SERIES_COLORS[n % len(SERIES_COLORS)]}">■</span> {escape(row["name"])}'
        for n, row in enumerate(series))
    data = "；".join(
        escape(row["name"]) + "：" + "，".join(
            f"{escape(label)} {escape(_cell(value))}" for label, value in zip(labels, row["values"]))
        for row in series)
    return (f"<figure>{''.join(parts)}<figcaption>{escape(chart['title'])}（单位：{escape(chart['unit'])}）"
            f"<br>{legend}<br>数据：{data}<br>来源：{escape(chart['source'])}</figcaption></figure>")


PROFILE_LABELS = {
    "regulated_or_contracted": "受监管／长约定价", "volume_times_price": "量×价",
    "commodity_linked": "商品／运价挂钩", "spread_income": "利差收入", "fee_or_aum": "管理费／交易费",
    "subscription_recurring": "订阅／经常性", "perpetual_going_concern": "持续经营",
    "finite_assets": "有限期资产", "stable": "稳定", "demand_cycle": "需求周期",
    "supply_cycle": "供给周期", "commodity_cycle": "商品周期", "rate_cycle": "利率周期",
    "operating": "经营型", "balance_sheet_spread": "资产负债表即业务", "asset_leasing": "资产租赁",
    "asset_light": "轻资产", "maintenance_heavy": "维护型重资产", "growth_heavy": "扩张型重资产",
    "ordinary_company": "普通公司股", "reit": "REIT", "us_publicly_traded_partnership": "美国上市合伙企业（MLP）",
    "business_trust_or_stapled": "商业信托／合订单位", "holding_parent": "控股母公司",
    "fund_or_etf": "基金／ETF", "wholly_owned": "基本全资", "material_minorities": "少数股东占比重大",
    "material_jv_associates": "依赖合营／联营分红",
}
STAGE_LABELS = {"starter": "初始建仓", "add": "逐步增持", "strong_buy": "强力买入"}
STATUS_LABELS = {"ready": "已就绪", "waiting_price": "等价格", "waiting_evidence": "等证据",
                 "unavailable": "不可用"}
MODULE_LABELS = {"net_yield": "净股息率", "dividend_stability": "股息稳定性", "cash_coverage": "现金覆盖",
                 "balance_sheet": "资产负债表", "capital_allocation": "资本配置",
                 "buyback_quality": "回购质量", "visibility": "可见度"}


def render_profile(profile):
    """Chapter 2 table of the seven economic dimensions (economic-profile.md)."""
    label = lambda key: PROFILE_LABELS.get(key, key)
    rows = [[row["name"], row["cash_share_pct"], label(row["revenue_engine"]), label(row["asset_life"]),
             label(row["cyclicality"]), label(row["balance_sheet_role"]), label(row["capital_intensity"])]
            for row in profile["segments"]]
    html_text = render_table({
        "title": "经济特征档案（分部）",
        "columns": ["分部", "现金占比%", "收入引擎", "资产寿命", "周期性", "资产负债表角色", "资本强度"],
        "rows": rows,
        "note": f"法律结构：{label(profile['legal_wrapper'])}；现金归属：{label(profile['cash_attribution'])}；"
                f"分类依据：{profile['classification_evidence']}"})
    if profile["finite_life_assets"]:
        html_text += render_table({
            "title": "有限期资产到期表",
            "columns": ["资产", "到期年", "经营现金占比%", "续期／补偿证据", "到期后处理"],
            "rows": [[row["name"], row["end_year"], row["operating_cash_share_pct"],
                      row["extension_evidence"], row["terminal_treatment"]]
                     for row in profile["finite_life_assets"]],
            "note": "逐项资产按剩余年限估值；单项到期不等于公司整体到期"})
    return html_text


def render_appendix(report):
    """Default audit appendix built from the structured records, so it cannot silently go missing."""
    parts = []
    if report.get("cash_flow_bridge"):
        bridge = report["cash_flow_bridge"]
        scrip = any(row.get("scrip_settled_dividends") for row in bridge)
        parts.append("<h3>A3 历史现金覆盖桥</h3>" + render_table({
            "title": "历年经常性与实际现金覆盖",
            "columns": ["财年", "经常性所有者现金", "经常性 FAD", "实际可分配",
                        "覆盖口径股息" if scrip else "现金股息", "经常性覆盖", "实际覆盖"]
                       + (["实付现金股息", "以股代息"] if scrip else []),
            "rows": [[row["fiscal_year"], row["recurring_owner_fcf_or_proxy"], row["recurring_fad"],
                      row["actual_distribution_capacity"], row["cash_dividends"],
                      row["fcf_dividend_coverage"], row["actual_cash_coverage"]]
                     + ([row.get("cash_paid_dividends"), row.get("scrip_settled_dividends")] if scrip else [])
                     for row in bridge],
            "note": f"{report['cash_flow_model']['financial_currency']}，单位："
                    f"{ {1: '元', 1e3: '千', 1e6: '百万', 1e9: '十亿'}.get(report['cash_flow_model']['cash_unit_scale'], report['cash_flow_model']['cash_unit_scale'])}；"
                    "来自 cash_flow_bridge"
                    + ("；有以股代息的年份按全部应派股息计算覆盖，实付现金只作对照" if scrip else "")}))
    if report.get("economic_profile"):
        profile = report["economic_profile"]
        parts.append("<h3>A5 业务与行业明细</h3>" + render_table({
            "title": "行业关键指标及因果依据", "columns": ["指标", "为何决定现金"],
            "rows": [[row["name"], row["why_causal"]] for row in profile["kpis"]],
            "note": "来自 economic_profile.kpis"}))
    if report.get("three_year_fundamental_forecast"):
        parts.append("<h3>A6 五年预测（前三年逐年）</h3>" + render_table({
            "title": "Bear／Base／Bull 逐年预测",
            "columns": ["财年", "情景", "收入", "经营现金", "维护投资", "所有者现金", "成长投资", "经常性 FAD"],
            "rows": [[row["fiscal_year"], row["scenario"], row["revenue_or_sector_income"],
                      row["normalized_ocf"], row["maintenance_capex"], row["fcf_or_distributable_cash"],
                      row["remaining_growth_investment"], row["recurring_fad"]]
                     for row in report["three_year_fundamental_forecast"]],
            "note": "来自 three_year_fundamental_forecast；null 表示该行业不适用或无法估计"}))
    if report.get("entry_plan"):
        currency = report["return_requirements"]["valuation_currency"]
        parts.append("<h3>A10 估值与买点复算</h3>" + render_table({
            "title": "分阶段买点",
            "columns": ["档位", "估值价格", "收入约束后价格", "相对现价%", "状态"],
            "rows": [[STAGE_LABELS.get(row["stage"], row["stage"]), row["valuation_price"],
                      row["effective_price"], row["gap_to_current_pct"],
                      STATUS_LABELS.get(row["status"], row["status"])]
                     for row in report["entry_plan"]["stages"]],
            "note": f"价格币种 {currency}；来自 entry_plan"}))
    if report.get("scorecard"):
        summary = report["scorecard"]["summary"]
        parts.append("<h3>A11 评分与组合角色</h3>" + render_table({
            "title": "评分模块区间",
            "columns": ["模块", "下限", "上限"],
            "rows": [[MODULE_LABELS.get(key, key), value["low"], value["high"]]
                     for key, value in summary["module_ranges"].items()],
            "note": f"评分规则 rubric 2；研究覆盖度 {summary['evidence_coverage_pct']}%"}))
    if report.get("sources"):
        parts.append("<h3>A13 来源与数据质量</h3><ol>" + "".join(
            f"<li>{html.escape(source)}</li>" for source in report["sources"]) + "</ol>")
    return "".join(parts)


def render_associate_conversion(record):
    """Equity-accounted associate/JV profit versus cash actually received (economic-profile.md)."""
    pct = lambda value: "—" if value is None else f"{value * 100:.1f}%"
    timing = {"same_year": "当年股息 ÷ 当年应占利润", "prior_year_profit": "当年股息 ÷ 上一年应占利润"}
    forecast = record["forecast_conversion"]
    amount = lambda value: f"{value:,.0f}"  # explicit, so 1800-2300 amounts are not printed as years
    rows = [[row["fiscal_year"], amount(row["share_of_profit"]), amount(row["cash_dividends_received"]),
             pct(row["conversion"])] for row in record["history"]]
    rows.append(["历史合计", "", "", pct(record["aggregate_conversion"])])
    rows.append(["预测 Bear／Base／Bull", "", "",
                 "／".join(pct(forecast[key]) for key in ("Bear", "Base", "Bull"))])
    note = f"{timing[record['timing_basis']]}。{record['explanation']}"
    if record["above_history_evidence"]:
        note += f" 高于历史的依据：{record['above_history_evidence']}"
    return "<h3>联营及合营公司现金上缴率</h3>" + render_table({
        "title": "应占利润与实际收到的现金股息",
        "columns": ["财年", "应占联营合营利润", "收到现金股息", "上缴率"], "rows": rows, "note": note})


def render_capital_distribution(value):
    """Capital-return formula versus forecast capital generation (buy-zone.md Section 7A)."""
    capacity = value["distribution_capacity"]
    pct = lambda number: f"{number * 100:.0f}%"
    rows = [[row["scenario"], pct(row["implied_distribution_ratio"]), pct(row["forecast_distributable_ratio"]),
             pct(row["dividend_payout_ratio"]), pct(row["buyback_capacity_ratio"])] for row in capacity["scenarios"]]
    return "<h3>资本回报能否兑现</h3>" + render_table({
        "title": "估值公式隐含的利润返还比例 vs 预测资本生成",
        "columns": ["情景", "公式隐含返还比例", "预测可分配比例（五年）", "股息派息率", "可用于回购"],
        "rows": rows,
        "note": f"隐含返还比例 =（有形股本回报率 − 长期增长）÷ 有形股本回报率；可分配比例 = 五年扣除风险资产增长所需资本后的可分配资本 ÷ 五年利润。"
                f"{capacity['growth_consistency']} 近期约束：{capacity['near_term_constraint']}"})


def render_growth_credit(returns):
    """Gated income growth credit test (buy-zone.md Section 4.2A)."""
    basis = returns["income_growth_credit_basis"]
    metric = {"dps": "每股股息", "recurring_eps": "每股经常性利润"}[basis["historical_metric"]]
    pct = lambda value: f"{value * 100:.2f}%"
    rows = [
        ["Base 情景每股股息年增长（预测第 1→5 年）", pct(basis["base_dps_cagr_fy1_fy5"])],
        [f"历史{metric}年增长（{basis['historical_start_period']}→{basis['historical_end_period']}）",
         pct(basis["historical_cagr"])],
        [f"长期名义增长上限（{basis['long_run_growth_bound_basis']}）", pct(basis["long_run_growth_bound"])],
        ["规则上限", "3.00%"],
        ["可抵扣上限（取以上最小值，不低于 0）", pct(basis["credit_cap"])],
        ["质量门槛", "通过" if basis["gates_passed"] else "未通过"],
        ["实际采用的增长抵扣", pct(returns["income_growth_credit"])],
    ]
    return "<h3>收息口径增长抵扣检验</h3>" + render_table({
        "title": "增长抵扣：起始与增持价按 N/(R−c)，强力买入仍按 B/R_high",
        "columns": ["检验项", "数值"], "rows": rows, "note": basis["explanation"]})


def render_report(report):
    errors = validate_report(report)
    if errors:
        raise ValueError("\n".join(errors))
    if report.get("schema_version") != "3.0":
        raise ValueError("Rendering requires an explicitly authored schema 3.0 report; no silent migration.")
    output = report["report_output"]
    if output["language"] != "zh-CN":
        raise ValueError("The bundled renderer supports zh-CN; use a localized template for the requested language.")
    escape = html.escape
    sections = []
    for index, section in enumerate(output["sections"], 1):
        body = "".join(f"<p>{escape(text)}</p>" for text in section["paragraphs"])
        body += "".join(render_table(table) for table in section.get("tables", []))
        body += "".join(render_chart(chart) for chart in section.get("charts", []))
        if index == 2 and report.get("economic_profile") and len(output["sections"]) == 12:
            body += render_profile(report["economic_profile"])
        if index == 1 and report["mode"] == "full_analysis":
            decision = report["decision"]
            score = report["scorecard"]["summary"]
            role = {"Core income": "核心收息", "Cyclical income": "周期收息",
                    "Opportunistic": "机会型", "Watchlist": "观察名单", "Avoid": "回避"}[report["portfolio_role"]]
            quality, combined = score["quality_range"], score["score_range"]
            headline = (
                f"当前动作：{decision['current_action']}；现价能否买："
                f"{'是' if decision['can_buy_now'] else '否'}。{decision['reason']}",
                f"质量评分：{span(quality['low'], quality['high'])}/85；"
                f"组合评分：{span(combined['low'], combined['high'])}/100；"
                f"等级：{span(score['grade_range']['worst'], score['grade_range']['best'])}；"
                f"研究覆盖度：{score['evidence_coverage_pct']}%；"
                f"质量覆盖度：{score['quality_coverage_pct']}%；组合角色：{role}。",
                f"红利陷阱结论：{decision['trap_conclusion']}",
                f"买点结论：{decision['entry_conclusion']}",
            )
            body = "".join(f"<p>{escape(text)}</p>" for text in headline) + body
        if report["mode"] == "full_analysis" and "买点" in section["heading"]:
            decision = report["decision"]
            for label, key in (("允许买入的条件（须同时满足）", "buy_conditions"),
                               ("结论失效条件（任一触发）", "invalidation_conditions")):
                body += f"<h3>{label}</h3><ul>"
                for condition in decision[key]:
                    if condition["kind"] == "event":
                        verb = "撤回" if condition["operator"] == "withdrawn" else "公告"
                        text = f"{condition['observable']}（{verb}即触发；跟踪来源：{condition['source_to_watch']}）"
                    else:
                        operator = {"<=": "≤", ">=": "≥"}.get(condition["operator"], condition["operator"])
                        threshold = condition["threshold"]
                        if isinstance(threshold, float):
                            threshold = f"{threshold:.2f}".rstrip("0").rstrip(".")
                        text = (f"{condition['observable']} {operator} {threshold} {condition['unit']}"
                                f"（跟踪来源：{condition['source_to_watch']}）")
                    body += f"<li>{escape(text)}</li>"
                body += "</ul>"
            if decision["price_status"] == "reference_prices":
                returns = report["return_requirements"]
                currency = returns["valuation_currency"]
                quote, rate = returns.get("quote_currency"), returns.get("quote_per_valuation_unit")
                extra = f"<th>折合 {escape(quote)}</th>" if quote and rate else ""
                body += f"<table><thead><tr><th>参考档位</th><th>价格</th>{extra}</tr></thead><tbody>"
                for key, label in (("starter", "初始建仓"), ("add", "逐步增持"),
                                   ("strong_buy", "强力买入"), ("income_capped_upper", "收入约束上限")):
                    value = decision["reference_prices"][key]
                    displayed = "不适用（有限期现金回收不增设档位）" if value is None else f"{value:.2f} {escape(currency)}"
                    quoted = (f"<td>{value * rate:.1f} {escape(quote)}</td>" if value is not None else "<td>—</td>") if extra else ""
                    body += f"<tr><td>{label}</td><td>{displayed}</td>{quoted}</tr>"
                body += "</tbody></table><p>参考价不替代资金、税务、资本与风险门槛；未就绪档位不可执行。</p>"
        capital = report.get("capital_return_valuation")
        if report["mode"] == "full_analysis" and "估值与预期总回报" in section["heading"] and capital \
                and capital.get("distribution_capacity"):
            body += render_capital_distribution(capital)
        conversion = report.get("cash_flow_model", {}).get("associate_cash_conversion")
        if report["mode"] == "full_analysis" and "现金流、资产负债" in section["heading"] and conversion:
            body += render_associate_conversion(conversion)
        credit_basis = report.get("return_requirements", {}).get("income_growth_credit_basis")
        if report["mode"] == "full_analysis" and "买点" in section["heading"] and credit_basis:
            body += render_growth_credit(report["return_requirements"])
        if index == len(output["sections"]):
            for record in report["evidence_recovery"]["records"]:
                body += f"<p>取数范围：{escape(record['reason'])}；影响：{escape(record['impact'])}</p><ul>"
                for attempt in record["attempts"]:
                    outcomes = {"found": "已取得", "not_found": "本次未找到", "inaccessible": "访问失败",
                                "not_applicable": "不适用", "not_provided": "用户未提供"}
                    body += (f"<li>{escape(attempt['source'])}（{escape(attempt['source_period'])}）："
                             f"{outcomes[attempt['outcome']]}。{escape(attempt['result'])}</li>")
                body += "</ul>"
                if record["estimate"] is not None:
                    estimate = record["estimate"]
                    body += (f"<p>有据估计：{estimate['low']}–{estimate['high']} {escape(estimate['unit'])}；"
                             f"{escape(estimate['derivation'])}；适用边界：{escape(estimate['applicability'])}</p>")
                elif record["resolution"] == "not_assessable":
                    body += f"<p>区间无法收窄的原因：{escape(record['estimate_failure_reason'])}</p>"
        sections.append(f'<section id="section-{index}"><h2>{index}. {escape(section["heading"])}</h2>{body}</section>')
    twelve = report["mode"] == "full_analysis" and len(output["sections"]) == 12
    appendix = "".join(f"<p>{escape(text)}</p>" for text in output["appendix"])
    if twelve:
        appendix += render_appendix(report)
    if appendix:
        sections.append(f'<section id="audit-appendix"><h2>审计附录</h2>{appendix}</section>')
    template = (Path(__file__).resolve().parents[1] / "templates" / "report.html").read_text(encoding="utf-8")
    values = {
        "REPORT_TITLE": escape(output["title"]),
        "REPORT_MODE": escape(report["mode"]),
        "REPORT_METADATA": f'<p>规则版本：3.0；{escape(output["summary"])}</p>',
        "REPORT_NAV": "<ol>" + "".join(
            f'<li><a href="#section-{index}">{escape(section["heading"])}</a></li>'
            for index, section in enumerate(output["sections"], 1))
            + ('<li><a href="#audit-appendix">审计附录</a></li>' if appendix else "") + "</ol>",
        "REPORT_BODY": "".join(sections),
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        result = render_report(json.loads(args.report.read_text(encoding="utf-8")))
        args.output.write_text(result, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Report rendering failed: {error}\n")


if __name__ == "__main__":
    main()
