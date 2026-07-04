# ChatGPT Custom GPT Instructions

This file is a setup guide, not the generated Custom GPT instruction payload.

To prevent drift from the Claude Skill source files, the full ChatGPT instruction payload is generated into:

```text
dist/chatgpt-custom-gpt-instructions.md
```

Regenerate it with:

```bash
bash build-gpt-instructions.sh
```

The generated file is built from:

```text
gpt-header.md
dividend-income-equity-analysis/SKILL.md
dividend-income-equity-analysis/workflow.md
dividend-income-equity-analysis/withholding-notes.md
dividend-income-equity-analysis/scoring.md
dividend-income-equity-analysis/visual-output-rules.md
dividend-income-equity-analysis/buy-zone.md
dividend-income-equity-analysis/output-template.md
```

For Custom GPT setup, the sustainable default is:

1. Paste the contents of `gpt-header.md` into the GPT Builder Instructions field.
2. Upload these files as Knowledge:

```text
dividend-income-equity-analysis/SKILL.md
dividend-income-equity-analysis/workflow.md
dividend-income-equity-analysis/withholding-notes.md
dividend-income-equity-analysis/scoring.md
dividend-income-equity-analysis/visual-output-rules.md
dividend-income-equity-analysis/buy-zone.md
dividend-income-equity-analysis/output-template.md
dividend-income-equity-analysis/schema.json
dividend-income-equity-analysis/examples/example-output-skeleton.md
```

Do not manually copy rules from the module files into this setup guide. Update the canonical module files and rerun the builder instead.

The generated full-instructions version in `dist/` is useful when you want a single pasteable instruction file. The header-plus-knowledge setup is usually better for avoiding drift and keeping each rule in one canonical place.
