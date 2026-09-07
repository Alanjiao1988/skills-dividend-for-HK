#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

usage() {
  echo "Usage: bash build-gpt-instructions.sh [--mode all|screen]"
}

MODE="all"
if [[ $# -eq 1 && ( "$1" == "--help" || "$1" == "-h" ) ]]; then
  usage
  exit 0
elif [[ $# -eq 2 && "$1" == "--mode" && ( "$2" == "all" || "$2" == "screen" ) ]]; then
  MODE="$2"
elif [[ $# -ne 0 ]]; then
  usage >&2
  exit 2
fi

SRC="dividend-income-equity-analysis"
OUT_DIR="dist"
OUT="$OUT_DIR/chatgpt-custom-gpt-instructions.md"

mkdir -p "$OUT_DIR"
if [[ "$MODE" == "screen" ]]; then
  OUT="$OUT_DIR/chatgpt-screen-instructions.md"
  MODULES=(data-conventions.md screen-mode.md withholding-notes.md)
  cat <<'EOF' > "$OUT"
# Screen-Only Dividend Research Instructions

Use this bundle only for first-pass screening, not forecasts, valuation or investment actions.
If the user requests Full Analysis, load the full canonical modules before proceeding.
Use the investor scenario and evidence rules below; do not invent a screening target.
EOF
else
  MODULES=(
    SKILL.md data-conventions.md screen-mode.md workflow.md
    business-outlook.md business-fundamentals.md sector-fcf-proxies.md
    withholding-notes.md scoring.md visual-output-rules.md buy-zone.md
    holding-review.md output-template.md
  )
  cat gpt-header.md > "$OUT"
fi

cat <<'EOF' >> "$OUT"

---

# Canonical Skill Modules

The sections below are generated from the canonical skill files. Do not edit this generated file directly. Edit the source files and rerun `./build-gpt-instructions.sh`.
EOF

for f in "${MODULES[@]}"; do
  echo -e "\n---\n\n# Module: $f\n" >> "$OUT"
  cat "$SRC/$f" >> "$OUT"
done

cat <<'EOF' >> "$OUT"

---

# Machine-Readable Schema Note

Use `dividend-income-equity-analysis/schema.json` when the user asks for JSON or machine-readable output. Upload it as a knowledge file rather than pasting the full schema into Custom GPT Instructions unless needed.
EOF

echo "Generated $OUT"
