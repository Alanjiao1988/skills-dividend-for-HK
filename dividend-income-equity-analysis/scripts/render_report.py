"""Render validated schema 3.0 records as an offline, single-file HTML report."""
import argparse
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
        return f"{value:,}"
    return str(value)


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
    """Static inline SVG line/bar chart; nulls are gaps. Readable offline with scripts disabled."""
    escape = html.escape
    width, height, left, right, top, bottom = 640, 300, 64, 16, 16, 48
    labels, series = chart["x_labels"], chart["series"]
    values = [v for row in series for v in row["values"] if v is not None]
    low, high = min(0.0, min(values)), max(0.0, max(values))
    if high == low:
        high = low + 1.0
    plot_w, plot_h = width - left - right, height - top - bottom
    step = plot_w / len(labels)

    def y(value):
        return top + plot_h * (high - value) / (high - low)

    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(chart["title"])}">']
    for tick in range(5):
        value = low + (high - low) * tick / 4
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
    for number, row in enumerate(series):
        color = SERIES_COLORS[number % len(SERIES_COLORS)]
        if chart["kind"] == "bar":
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
        if index == 1 and report["mode"] == "full_analysis":
            decision = report["decision"]
            score = report["scorecard"]["summary"]
            role = {"Core income": "核心收息", "Cyclical income": "周期收息",
                    "Opportunistic": "机会型", "Watchlist": "观察名单", "Avoid": "回避"}[report["portfolio_role"]]
            quality, combined = score["quality_range"], score["score_range"]
            headline = (
                f"当前动作：{decision['current_action']}；现价能否买："
                f"{'是' if decision['can_buy_now'] else '否'}。{decision['reason']}",
                f"质量评分：{quality['low']}–{quality['high']}/85；"
                f"组合评分：{combined['low']}–{combined['high']}/100；"
                f"等级区间：{score['grade_range']['worst']}–{score['grade_range']['best']}；"
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
                    operator = {"published": "披露", "withdrawn": "撤回"}.get(
                        condition["operator"], condition["operator"])
                    text = (f"{condition['observable']}：{operator} {condition['threshold']} "
                            f"{condition['unit']}；跟踪来源：{condition['source_to_watch']}")
                    body += f"<li>{escape(text)}</li>"
                body += "</ul>"
            if decision["price_status"] == "reference_prices":
                body += "<table><thead><tr><th>参考档位</th><th>价格</th></tr></thead><tbody>"
                for key, label in (("starter", "初始建仓"), ("add", "逐步增持"),
                                   ("strong_buy", "强力买入"), ("income_capped_upper", "收入约束上限")):
                    currency = report["return_requirements"]["valuation_currency"]
                    value = decision["reference_prices"][key]
                    displayed = "不适用（有限期现金回收不增设档位）" if value is None else f"{value:.2f} {escape(currency)}"
                    body += f"<tr><td>{label}</td><td>{displayed}</td></tr>"
                body += "</tbody></table><p>参考价不替代资金、税务、资本与风险门槛；未就绪档位不可执行。</p>"
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
    if output["appendix"]:
        sections.append('<section id="audit-appendix"><h2>审计附录</h2>' + "".join(
            f"<p>{escape(text)}</p>" for text in output["appendix"]) + "</section>")
    template = (Path(__file__).resolve().parents[1] / "templates" / "report.html").read_text(encoding="utf-8")
    values = {
        "REPORT_TITLE": escape(output["title"]),
        "REPORT_MODE": escape(report["mode"]),
        "REPORT_METADATA": f'<p>规则版本：3.0；{escape(output["summary"])}</p>',
        "REPORT_NAV": "<ol>" + "".join(
            f'<li><a href="#section-{index}">{escape(section["heading"])}</a></li>'
            for index, section in enumerate(output["sections"], 1))
            + ('<li><a href="#audit-appendix">审计附录</a></li>' if output["appendix"] else "") + "</ol>",
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
