# ChatGPT Custom GPT Instructions

This file is a setup guide, not the generated payload.

Generate the full payload into:

```text
dist/chatgpt-custom-gpt-instructions.md
```

Run:

```bash
bash build-gpt-instructions.sh
```

The generated file includes:

```text
gpt-header.md
dividend-income-equity-analysis/SKILL.md
dividend-income-equity-analysis/screen-mode.md
dividend-income-equity-analysis/workflow.md
dividend-income-equity-analysis/business-outlook.md
dividend-income-equity-analysis/business-fundamentals.md
dividend-income-equity-analysis/sector-fcf-proxies.md
dividend-income-equity-analysis/withholding-notes.md
dividend-income-equity-analysis/scoring.md
dividend-income-equity-analysis/visual-output-rules.md
dividend-income-equity-analysis/buy-zone.md
dividend-income-equity-analysis/holding-review.md
dividend-income-equity-analysis/output-template.md
```

Recommended Custom GPT setup:

1. Paste `gpt-header.md` into the Instructions field.
2. Upload the canonical skill files, including `screen-mode.md`, `schema.json`, and the example skeleton, as Knowledge.
3. After changing canonical modules, run:

```bash
bash validate-skill.sh
```

Do not manually copy module rules into this setup guide. The header-plus-knowledge configuration is preferred for avoiding drift; the generated file is available when a single pasteable payload is needed.
