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

For a Screen-only bundle, run `bash build-gpt-instructions.sh --mode screen`. This generates `dist/chatgpt-screen-instructions.md` with only data conventions, Screen Mode and withholding rules.

The full bundle is a reference export, not a guarantee that the text fits a host's Instructions field. Prefer the short GPT header plus canonical Knowledge files, loading modules by mode. Never use the Screen bundle for Full Analysis.

Do not edit generated files directly. Edit `gpt-header.md` or the canonical skill modules under `dividend-income-equity-analysis/`, then rerun the builder.
