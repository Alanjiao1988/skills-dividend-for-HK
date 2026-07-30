#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SCHEMA="dividend-income-equity-analysis/schema.json"
TEMPLATE="dividend-income-equity-analysis/output-template.md"
SKELETON="dividend-income-equity-analysis/examples/example-output-skeleton.md"
SCREEN_MODE="dividend-income-equity-analysis/screen-mode.md"
GENERATED="dist/chatgpt-custom-gpt-instructions.md"

python3 - <<'PY'
import json
from pathlib import Path

path = Path("dividend-income-equity-analysis/schema.json")
raw = path.read_text(encoding="utf-8")
schema = json.loads(raw)
line_count = len(raw.splitlines())
if line_count < 50:
    raise SystemExit(f"schema.json is valid but not maintainably formatted: only {line_count} lines")
if not raw.endswith("\n"):
    raise SystemExit("schema.json must end with a newline")

def require(condition, message):
    if not condition:
        raise SystemExit(message)

defs = schema.get("$defs", {})
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

require("screening_parameters" in schema.get("properties", {}), "top-level screening_parameters missing")
require("not_assessed" in param_props["target_basis"].get("enum", []), "target_basis missing not_assessed")
require("hard_minimum" in param_props["target_policy"].get("enum", []), "target_policy missing hard_minimum")
require("preference" in param_props["target_policy"].get("enum", []), "target_policy missing preference")
require("Not Assessed" in item_props["yield_fit"].get("enum", []), "yield_fit missing Not Assessed")

print(f"schema.json: valid and readable ({line_count} lines)")
print("screening-yield schema contract: present")
PY

bash build-gpt-instructions.sh >/dev/null

for module in \
  SKILL.md \
  screen-mode.md \
  workflow.md \
  business-fundamentals.md \
  withholding-notes.md \
  scoring.md \
  visual-output-rules.md \
  buy-zone.md \
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
grep -Fq 'Screening net-yield target' "$SCREEN_MODE"
grep -Fq 'Target policy: hard_minimum / preference / not_assessed' "$SCREEN_MODE"
grep -Fq 'do not reject or downgrade a stock solely because its yield appears low' "$SCREEN_MODE"
grep -Fq 'screen-mode.md' build-gpt-instructions.sh

echo "Skill validation passed"
