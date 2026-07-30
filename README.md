# skills-dividend-for-HK

A claude.ai Skill for screening and analyzing dividend-income equities from the perspective of an HK resident individual using a normal brokerage account.

## Skill Directory

```text
dividend-income-equity-analysis/
├── SKILL.md
├── screen-mode.md
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

## Analysis Modes

### Screen Mode

Use for quick screening, candidate pools, batch comparisons, and deciding which stocks deserve Full Analysis.

It outputs current after-tax yield, five-year DPS pattern, latest coverage, withholding efficiency, preliminary trend, trap screen, and:

```text
Full Analysis Recommended: Yes / Watch / No
```

It does not output forecasts, N/B, buy zones, Strong Buy, or final scores.

### Full Analysis Mode

Uses the complete 18-section framework from business fundamentals through dividend capacity, sensitivity, dilution, valuation, and scoring.

## Core Rules

- Future DPS is derived from operating drivers, cash generation, reinvestment, payout policy, and diluted share count.
- Sensitivities are transient, persistent, or structural.
- Transient changes do not move normalized N or long-term buy-zone boundaries.
- N follows the mid-cycle / full-cycle / normalized Base-average / historical-fallback priority.
- Dividend Cash Cost and Derived DPS appear once in the Dividend and Yield Runway.
- PIL is not withholding-rate evidence.
- Scrip / DRIP affects investor cash income and company-level dilution separately.
- Structural Decline defaults to suspended ordinary buy-zone output.
- A credible managed-runoff case uses finite-life cash recovery with a discount-rate floor of 10%.
- The Dividend Trap Checklist is a precondition for valuation.

## ChatGPT Custom GPT Support

ChatGPT-specific files:

```text
gpt-header.md
build-gpt-instructions.sh
chatgpt-custom-gpt-instructions.md
dist/
```

Generate the single-file GPT instructions with:

```bash
bash build-gpt-instructions.sh
```

The generated output is:

```text
dist/chatgpt-custom-gpt-instructions.md
```

The root-level `chatgpt-custom-gpt-instructions.md` remains a setup guide.

## Validation

Run:

```bash
bash validate-skill.sh
```

The validator checks:

- valid, multi-line, maintainable JSON schema formatting;
- 18 numbered Full Analysis sections in both template and example;
- all canonical modules included in generated GPT instructions;
- absence of selected stale rule strings;
- presence of Screen Mode, sensitivity classification, and finite-life valuation contracts.
