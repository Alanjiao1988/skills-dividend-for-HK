#!/usr/bin/env bash
set -euo pipefail

SRC="dividend-income-equity-analysis"
OUT_DIR="dist"
OUT="$OUT_DIR/chatgpt-custom-gpt-instructions.md"

mkdir -p "$OUT_DIR"
cat gpt-header.md > "$OUT"

cat <<'EOF' >> "$OUT"

---

# Canonical Skill Modules

The sections below are generated from the canonical skill files. Do not edit this generated file directly. Edit the source files and rerun `./build-gpt-instructions.sh`.
EOF

for f in \
  SKILL.md \
  screen-mode.md \
  workflow.md \
  business-fundamentals.md \
  withholding-notes.md \
  scoring.md \
  visual-output-rules.md \
  buy-zone.md \
  output-template.md; do
  echo -e "\n---\n\n# Module: $f\n" >> "$OUT"
  cat "$SRC/$f" >> "$OUT"
done

cat <<'EOF' >> "$OUT"

---

# Machine-Readable Schema Note

Use `dividend-income-equity-analysis/schema.json` when the user asks for JSON or machine-readable output. Upload it as a knowledge file rather than pasting the full schema into Custom GPT Instructions unless needed.
EOF

echo "Generated $OUT"
