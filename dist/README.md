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

Do not edit generated files directly. Edit `gpt-header.md` or the canonical skill modules under `dividend-income-equity-analysis/`, then rerun the builder.

The bundle stamps its source Git commit, schema version, dirty/clean status and build-input SHA-256. An archive without its own matching Git checkout reports an unknown commit, never the identity of an enclosing repository. Rebuild after committing to produce a clean, attributable deliverable.
