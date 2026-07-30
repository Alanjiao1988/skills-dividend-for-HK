#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SCHEMA="dividend-income-equity-analysis/schema.json"
TEMPLATE="dividend-income-equity-analysis/output-template.md"
SKELETON="dividend-income-equity-analysis/examples/example-output-skeleton.md"
GENERATED="dist/chatgpt-custom-gpt-instructions.md"

python3 - <<'PY'
import json
from pathlib import Path

path = Path("dividend-income-equity-analysis/schema.json")
raw = path.read_text(encoding="utf-8")
data = json.loads(raw)
formatted = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
if raw != formatted:
    raise SystemExit("schema.json is valid but not canonical 2-space formatted JSON")
print("schema.json: valid and formatted")
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

if grep -R -n -E 'B / r_low|"three_year_forecast"|Base-derived N' dividend-income-equity-analysis; then
  echo "Stale rule detected" >&2
  exit 1
fi

grep -Fq 'sensitivity_type' "$SCHEMA"
grep -Fq 'finite_life_harvest' "$SCHEMA"
grep -Fq 'Full Analysis Recommended' dividend-income-equity-analysis/screen-mode.md

echo "Skill validation passed"
