# dist

Generated files may be written here.

Generated files in this directory are ignored by Git; only this README is versioned. This directory is for instruction bundles, not investment reports.

Run from the repository root:

```bash
bash build-gpt-instructions.sh
```

This generates:

```text
dist/chatgpt-custom-gpt-instructions.md
```

For a Screen-only bundle, run `bash build-gpt-instructions.sh --mode screen`. This generates `dist/chatgpt-screen-instructions.md` with only data conventions, portfolio-target context, Screen Mode and withholding rules.

The full bundle is a reference export, not a guarantee that the text fits a host's Instructions field. Prefer the short GPT header plus canonical Knowledge files, loading modules by mode. Never use the Screen bundle for Full Analysis.

Do not edit generated files directly. Edit `gpt-header.md` or the canonical skill modules under `dividend-income-equity-analysis/`, then rerun the builder.

The bundle stamps its source Git commit, schema version, dirty/clean status and build-input SHA-256. An archive without its own matching Git checkout reports an unknown commit, never the identity of an enclosing repository. Rebuild after committing to produce a clean, attributable deliverable.

## Portable Agent Skill packages

Run `python scripts/skill_package.py build` and `python scripts/skill_package.py verify` to generate complete platform directories and ZIPs under `dist/agent-skills/`. The manifest records source commit, dirty status and per-file hashes. Generated packages are ignored by Git. Refer to the root README for installation, integrity checks and safe upgrades. They do not replace the Custom GPT bundles above.
