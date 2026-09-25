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

if [[ -n "${PYTHON:-}" ]]; then
  PYTHON_BIN="$PYTHON"
elif command -v python >/dev/null 2>&1 && python -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" - "$MODE" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path.cwd().resolve()
src = Path("dividend-income-equity-analysis")
all_modules = (
    "SKILL.md", "data-conventions.md", "portfolio-context.md", "screen-mode.md",
    "workflow.md", "business-outlook.md", "business-fundamentals.md",
    "sector-fcf-proxies.md", "withholding-notes.md", "scoring.md",
    "visual-output-rules.md", "buy-zone.md", "holding-review.md",
    "publishing.md", "output-template.md", "analysis-quality.md",
    "report-language.md", "safety-review.md",
)
mode = sys.argv[1]
modules = all_modules if mode == "all" else (
    "data-conventions.md", "portfolio-context.md", "screen-mode.md", "withholding-notes.md",
    "report-language.md",
)
schema_path = src / "schema.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
schema_version = schema["properties"]["schema_version"]["default"]

def git(*args):
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, check=False,
        )
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None

# An archive can be nested inside an unrelated checkout. Attribute a commit
# only when this builder is at that checkout's exact root.
commit, source_status = "unknown", "unknown (no matching Git checkout)"
git_root = git("rev-parse", "--show-toplevel")
if git_root and Path(git_root.decode("utf-8").strip()).resolve() == root:
    head = git("rev-parse", "--verify", "HEAD")
    if head:
        commit = head.decode("ascii").strip()
    tracked = git("status", "--porcelain=v1", "-z", "--untracked-files=no")
    untracked = git(
        "ls-files", "--others", "--exclude-standard", "-z", "--",
        "README.md", "gpt-header.md", "build-gpt-instructions.sh",
        "validate-skill.sh", "requirements-dev.txt", "dist/README.md",
        "dividend-income-equity-analysis", "scripts", "tests",
    )
    if tracked is not None and untracked is not None:
        source_status = "dirty" if tracked or untracked else "clean"
    else:
        source_status = "unknown (Git status unavailable)"

# Hash only known build inputs. Normalize newlines so Windows Git checkout
# settings do not change an otherwise identical generated bundle.
inputs = [Path("build-gpt-instructions.sh"), Path("gpt-header.md"), schema_path]
inputs += [src / module for module in modules]
texts = {path: path.read_text(encoding="utf-8") for path in inputs}
fingerprint = hashlib.sha256()
for path in inputs:
    fingerprint.update(path.as_posix().encode("utf-8") + b"\0")
    fingerprint.update(texts[path].encode("utf-8") + b"\0")
header = texts[Path("gpt-header.md")] if mode == "all" else (
    "# Screen-Only Dividend Research Instructions\n\n"
    "Use this bundle only for first-pass screening, not forecasts, valuation or investment actions.\n"
    "If the user requests Full Analysis, load the full canonical modules before proceeding.\n"
    "Use the investor scenario and evidence rules below; do not invent a screening target.\n"
)
parts = [header, "\n---\n\n# Bundle Provenance\n\n",
         f"- Bundle profile: `{mode}`\n",
         f"- Source commit: `{commit}`\n",
         f"- Schema version: `{schema_version}`\n",
         f"- Source status: `{source_status}`\n",
         f"- Build-input SHA-256: `{fingerprint.hexdigest()}`\n\n",
         "The commit identifies the source checkout before any dirty edits. "
         "Dirty includes all tracked changes and untracked files in the skill, "
         "validation and documented build-source paths; generated bundles and "
         "ignored scratch files are excluded. A source archive has no verified "
         "Git commit. The input hash identifies this bundle's actual source content.\n",
         "\n---\n\n# Canonical Skill Modules\n\n",
         "The sections below are generated from the canonical skill files. "
         "Do not edit this generated file directly. Edit the source files and "
         "rerun `bash build-gpt-instructions.sh`.\n"]
for module in modules:
    parts += [f"\n---\n\n# Module: {module}\n\n", texts[src / module]]
parts += ["\n---\n\n# Machine-Readable Schema Note\n\n",
          "Use `dividend-income-equity-analysis/schema.json` when the user asks "
          "for JSON or machine-readable output. Upload it as a knowledge file "
          "rather than pasting the full schema into Custom GPT Instructions "
          "unless needed.\n"]
out = Path("dist") / ("chatgpt-custom-gpt-instructions.md" if mode == "all" else "chatgpt-screen-instructions.md")
out.parent.mkdir(exist_ok=True)
out.write_text("".join(parts), encoding="utf-8", newline="\n")
print(f"Generated {out.as_posix()}")
PY
