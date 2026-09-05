#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SCHEMA="dividend-income-equity-analysis/schema.json"
TEMPLATE="dividend-income-equity-analysis/output-template.md"
SKELETON="dividend-income-equity-analysis/examples/example-output-skeleton.md"
SCREEN_MODE="dividend-income-equity-analysis/screen-mode.md"
GENERATED="dist/chatgpt-custom-gpt-instructions.md"

if [[ -n "${PYTHON:-}" ]]; then
  PYTHON_BIN="$PYTHON"
elif command -v python >/dev/null 2>&1 && python -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  PYTHON_BIN="python3"
fi

if ! "$PYTHON_BIN" -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
  echo "Python 3.10+ is required; set PYTHON to a working interpreter." >&2
  exit 1
fi
if ! "$PYTHON_BIN" -c 'import jsonschema' >/dev/null 2>&1; then
  echo "Missing validation dependency. Run: $PYTHON_BIN -m pip install -r requirements-dev.txt" >&2
  exit 1
fi

"$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator

path = Path("dividend-income-equity-analysis/schema.json")
raw = path.read_text(encoding="utf-8")
schema = json.loads(raw)
Draft202012Validator.check_schema(schema)
line_count = len(raw.splitlines())
if line_count < 50:
    raise SystemExit(f"schema.json is valid but not maintainably formatted: only {line_count} lines")
if not raw.endswith("\n"):
    raise SystemExit("schema.json must end with a newline")

def require(condition, message):
    if not condition:
        raise SystemExit(message)

defs = schema.get("$defs", {})
props = schema.get("properties", {})
params = defs.get("screeningParameters", {})
item = defs.get("screenItem", {})
require(params, "schema missing $defs.screeningParameters")
require(item, "schema missing $defs.screenItem")

param_props = params.get("properties", {})
item_props = item.get("properties", {})
for key in ("target_net_yield", "target_basis", "target_policy"):
    require(key in param_props, f"screeningParameters missing {key}")
for key in (
    "screening_net_yield_target",
    "yield_fit",
    "yield_gap_percentage_points",
    "documented_dividend_growth_path",
):
    require(key in item_props, f"screenItem missing {key}")

require("screening_parameters" in props, "top-level screening_parameters missing")
require("not_assessed" in param_props["target_basis"].get("enum", []), "target_basis missing not_assessed")
require("hard_minimum" in param_props["target_policy"].get("enum", []), "target_policy missing hard_minimum")
require("preference" in param_props["target_policy"].get("enum", []), "target_policy missing preference")
require("Not Assessed" in item_props["yield_fit"].get("enum", []), "yield_fit missing Not Assessed")

restored_full_fields = (
    "key_metrics_at_a_glance",
    "dividend_snapshot",
    "five_year_dividend_history",
    "cash_flow_bridge",
    "scrip_drip",
    "rendering",
    "visual_summary",
)
for key in restored_full_fields:
    require(key in props, f"full-analysis schema field missing: {key}")

buy_zone_props = props.get("buy_zone", {}).get("properties", {})
require("too_expensive_zone" in buy_zone_props, "buy_zone missing too_expensive_zone")

full_required = None
for rule in schema.get("allOf", []):
    condition = rule.get("if", {})
    if condition.get("properties", {}).get("mode", {}).get("const") == "full_analysis":
        full_required = set(rule.get("then", {}).get("required", []))
        break
require(full_required is not None, "schema missing full_analysis conditional requirement")
for key in restored_full_fields:
    require(key in full_required, f"full_analysis does not require {key}")
require("sources" in full_required, "full_analysis does not require sources")
for key in (
    "cash_flow_model", "coverage_summary", "business_outlook", "forecast_extension",
    "payout_policy", "return_requirements", "growth_assessment", "income_assessment",
    "holding_review", "value_trap_veto", "score_limitations",
):
    require(key in props and key in full_required, f"full_analysis missing required contract: {key}")
require("total_return_based" in defs["valuationMode"]["enum"], "growth valuation mode missing")

def check_refs(node):
    if isinstance(node, dict):
        ref = node.get("$ref")
        if ref:
            require(ref.startswith("#/"), f"unexpected external schema reference: {ref}")
            target = schema
            for part in ref[2:].split("/"):
                require(part in target, f"unresolved schema reference: {ref}")
                target = target[part]
        for value in node.values():
            check_refs(value)
    elif isinstance(node, list):
        for value in node:
            check_refs(value)

check_refs(schema)

print(f"schema.json: valid and readable ({line_count} lines)")
print("screening-yield schema contract: present")
print("full-analysis historical and presentation contract: present")
PY

bash build-gpt-instructions.sh >/dev/null

for module in \
  SKILL.md \
  data-conventions.md \
  screen-mode.md \
  workflow.md \
  business-outlook.md \
  business-fundamentals.md \
  sector-fcf-proxies.md \
  withholding-notes.md \
  scoring.md \
  visual-output-rules.md \
  buy-zone.md \
  holding-review.md \
  output-template.md; do
  grep -Fq "# Module: $module" "$GENERATED" || {
    echo "Generated GPT instructions missing module: $module" >&2
    exit 1
  }
done

full_template_sections=$(grep -Ec '^## ([1-9]|1[0-8])\. ' "$TEMPLATE")
full_skeleton_sections=$(grep -Ec '^## ([1-9]|1[0-8])\. ' "$SKELETON")

if [[ "$full_template_sections" -ne 18 ]]; then
  echo "output-template.md must contain 18 numbered Full Analysis sections; found $full_template_sections" >&2
  exit 1
fi

if [[ "$full_skeleton_sections" -ne 18 ]]; then
  echo "example-output-skeleton.md must contain 18 numbered Full Analysis sections; found $full_skeleton_sections" >&2
  exit 1
fi

if grep -R -n -E 'B / r_low|"three_year_forecast"|Base-derived N|after-tax yield is plainly insufficient' dividend-income-equity-analysis; then
  echo "Stale rule detected" >&2
  exit 1
fi

grep -Fq 'sensitivity_type' "$SCHEMA"
grep -Fq 'finite_life_harvest' "$SCHEMA"
grep -Fq 'screening_parameters' "$SCHEMA"
grep -Fq 'yield_gap_percentage_points' "$SCHEMA"
grep -Fq 'five_year_dividend_history' "$SCHEMA"
grep -Fq 'cash_flow_bridge' "$SCHEMA"
grep -Fq 'too_expensive_zone' "$SCHEMA"
grep -Fq 'Screening net-yield target' "$SCREEN_MODE"
grep -Fq 'Target policy: hard_minimum / preference / not_assessed' "$SCREEN_MODE"
grep -Fq 'do not reject or downgrade a stock solely because its yield appears low' "$SCREEN_MODE"
grep -Fq 'screen-mode.md' build-gpt-instructions.sh

"$PYTHON_BIN" -m unittest discover -s tests -p 'test_*.py'

echo "Skill validation passed"
