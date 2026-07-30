# skills-dividend-for-HK

A claude.ai Skill for dividend-income stock analysis from the perspective of an HK resident individual using a normal brokerage account.

## Skill Directory

Upload or package this directory as the skill:

```text
dividend-income-equity-analysis/
```

Expected in-skill structure:

```text
dividend-income-equity-analysis/
├── SKILL.md
├── workflow.md
├── business-fundamentals.md
├── withholding-notes.md
├── scoring.md
├── visual-output-rules.md
├── buy-zone.md
├── output-template.md
├── schema.json
└── examples/
    └── example-output-skeleton.md
```

## ChatGPT Custom GPT Support

ChatGPT-specific files are kept outside the skill directory:

```text
gpt-header.md
build-gpt-instructions.sh
chatgpt-custom-gpt-instructions.md
dist/
```

Use `gpt-header.md` as the Custom GPT instruction header and upload the canonical skill files as Knowledge.

To generate a single pasteable Custom GPT instruction file:

```bash
bash build-gpt-instructions.sh
```

The generated output is written to:

```text
dist/chatgpt-custom-gpt-instructions.md
```

The root-level `chatgpt-custom-gpt-instructions.md` is a setup guide and should not be overwritten by the builder.

Do not hand-copy skill rules into the ChatGPT file; update canonical modules under `dividend-income-equity-analysis/` and regenerate.

## Focus

The skill focuses on:

- Business fundamentals and the economic engine that funds dividends.
- Historical operating, earnings, cash-flow, and per-share trends.
- Sector-specific Bear / Base / Bull fundamental forecasts.
- Dividend Forecast Bridge from distributable cash to derived DPS.
- Gross and net dividend yield.
- TTM yield versus fundamentally normalized yield.
- Five-year dividend history and dividend trajectory.
- Withholding treatment and broker-observed dividend cash flow.
- Payment-in-lieu versus true dividend cash-line identification.
- Management capital allocation and buyback quality.
- Historical and forecast financial coverage and dividend safety.
- Three-year evidence-backed dividend runway.
- Expected buy zone using Base-derived normalized net DPS, Bear-derived net DPS, required net yield, historical prices, and historical yield bands.
- Dividend-trap detection.

## Key Rules

- Broker-observed withholding has priority over theoretical classification only when the broker record is a true dividend line.
- Payment-in-lieu records do not constitute withholding-rate evidence.
- TTM yield must be separated from normalized yield.
- Future DPS must be derived from business drivers, earnings or sector-equivalent profitability, cash generation, required reinvestment, payout policy, and diluted share count.
- Bear / Base / Bull scenarios must be driven by explicit operating assumptions, not arbitrary DPS haircuts.
- Run the dividend-trap checklist before treating any buy-zone output as actionable.
- Buy-zone N and B inputs must normally come from the Base and Bear Dividend Forecast Bridge.
- Buy-zone analysis must use deterministic monotonic boundaries from `buy-zone.md`.
- Strong buy boundary uses Bear-derived net DPS divided by the high end of the required yield range: `B / r_high`.
- Buy-zone analysis must not use peak-cycle DPS as the base-case anchor unless that DPS is demonstrably sustainable.
