# skills-dividend-for-HK

A claude.ai Skill for screening and analyzing dividend-income equities from the perspective of an HK resident individual using a normal brokerage account.

## Repository Scope

This is an investment-analysis **skill source repository**, not a company research-report archive.

| Path | Purpose |
|---|---|
| `dividend-income-equity-analysis/` | Canonical analysis rules, output templates, and machine-readable schema. |
| `dividend-income-equity-analysis/examples/` | Placeholder examples that demonstrate the output structure, not completed company reports. |
| `gpt-header.md`, `chatgpt-custom-gpt-instructions.md` | ChatGPT configuration and setup instructions. |
| `build-gpt-instructions.sh`, `validate-skill.sh` | Build and maintenance tools. |
| `scripts/validate_analysis.py`, `tests/`, `requirements-dev.txt` | JSON contract validation and synthetic framework regressions, not company reports. |
| `dist/` | Generated instruction bundles; only `dist/README.md` is versioned. |

Completed company reports belong in the separate [Alanjiao1988/Dividendreport](https://github.com/Alanjiao1988/Dividendreport) repository, organized by ticker and data as-of date.

Keep temporary reports, downloaded disclosures, broker statements, and generated charts in the session workspace or another user-designated location outside this repository. Save or publish reports only when explicitly requested; do not overwrite skill templates with analysis results.

The `.gitignore` rules exclude generated bundles and reserved report/output/scratch directories (`reports/`, `output/`, `outputs/`, `tmp/`, and `.tmp/`) as a safety net. Canonical templates, placeholder examples, and `schema.json` remain versioned.

## Skill Directory

```text
dividend-income-equity-analysis/
├── SKILL.md
├── screen-mode.md
├── workflow.md
├── business-outlook.md
├── business-fundamentals.md
├── sector-fcf-proxies.md
├── withholding-notes.md
├── scoring.md
├── visual-output-rules.md
├── buy-zone.md
├── holding-review.md
├── output-template.md
├── schema.json
└── examples/
    └── example-output-skeleton.md
```

## Analysis Modes

### Screen Mode

Use for quick screening, candidate pools, batch comparisons, and deciding which stocks deserve Full Analysis.

It outputs current after-tax yield, the applicable screening net-yield target, Yield Fit, Yield Gap, documented dividend-growth path, five-year DPS pattern, latest coverage, withholding efficiency, preliminary trend, trap screen, and:

```text
Full Analysis Recommended: Yes / Watch / No
```

Screening target priority:

1. User-explicit target for the current screen.
2. Clearly applicable portfolio-level target.
3. `Not Assessed` when neither is available.

A target is a `hard_minimum` only when the user explicitly defines it as mandatory. Otherwise it is a `preference`.

If no target is available, the Skill must not reject a stock solely because its yield appears low. Required-yield ranges in `buy-zone.md` are security-specific return requirements and are not substitutes for the investor's screening target.

Screen Mode does not output forecasts, N/B, buy zones, Strong Buy, or final scores.

### Full Analysis Mode

Uses the complete 18-section framework from business fundamentals through dividend capacity, sensitivity, dilution, valuation, and scoring.

### Three-to-Five-Year Outlook and FCF

Full Analysis now requires a five-year development thesis: competitive position, segment drivers, committed versus optional projects, investment/funding, management execution, and measurable milestones that can invalidate the thesis. Detailed annual Bear/Base/Bull forecasts cover the first three years, with supported year-four/five extensions; missing later-year evidence produces unavailable values and reasons, not an automatic growth-rate extrapolation.

The financial chain is:

```text
Operating drivers -> earnings / normalized operating cash
-> Recurring Owner FCF or sector capital proxy
-> remaining committed growth investment and mandatory uses
-> Recurring FAD -> actual-period distribution capacity
-> policy-specific payout -> funded DPS and per-share cash outlook
```

Reported cash, recurring capacity and actual exceptional obligations remain separate. Capex, leases, regulatory uses and other claims are deducted once. Banks, insurers, REITs, utilities and holding companies use explicit sector/capital/remittance bridges; OPAT is not insurer cash flow. Coverage uses three-year aggregate FAD / matching cash dividends plus five-year worst-year stress, not an average of annual ratios.

### Valuation and Holding Review

- `ordinary_yield_based`: retains the existing deterministic N/B income-entry formulas.
- `total_return_based`: conditionally discounts an evidenced, funded dividend-growth path with explicit transition, bounded terminal growth, scenario values and sensitivity. Income fit is shown separately.
- `finite_life_harvest`: retains finite cash recovery for qualifying managed-runoff cases.
- `suspended`: used when vetoes, structural decline without an exception, or material evidence gaps prevent responsible valuation.

Required returns disclose a dated, currency/tax-consistent risk-free anchor, price-independent risk premia and the resulting range. The total score cannot determine discount rates because it contains current dividend yield. A US 20-year Treasury can be a justified USD reference, not a universal hardcoded hurdle.

Holding reviews separate thesis failure, capital/cash stress, valuation, portfolio constraints and switching opportunity costs. Review levels are not automatic sell orders; missing holdings or alternative data must not produce invented trade sizes. Scoring weights, the trap precondition, sensitivity classification and ordinary N/B anchors are preserved.

## Core Rules

- Future DPS is derived from operating drivers, cash generation, reinvestment, payout policy, and diluted share count.
- Sensitivities are transient, persistent, or structural.
- Transient changes do not move normalized N or ordinary income boundaries; they still affect the dated cash-flow PV in a growth model.
- N follows the mid-cycle / full-cycle / normalized Base-average / historical-fallback priority.
- Dividend Cash Cost and Derived DPS appear once in the Dividend and Yield Runway.
- PIL is not withholding-rate evidence.
- Scrip / issuer-issued DRIP affects investor cash income and company-level dilution separately; secondary-market DRIP does not issue new shares.
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

Requires Python 3.10+, Bash (Git Bash on Windows), and `jsonschema`. If the dependency is missing, install the development requirements:

```text
python -m pip install -r requirements-dev.txt
```

Run the existing entry point:

```bash
bash validate-skill.sh
```

The validator checks:

- valid, multi-line, maintainable JSON schema formatting;
- 18 numbered Full Analysis sections in both template and example;
- all canonical modules included in generated GPT instructions;
- absence of selected stale rule strings;
- presence of Screen Mode, explicit screening-yield parameters, sensitivity classification, and finite-life valuation contracts.
- actual Draft 2020-12 schema validity, required new fields and local references;
- synthetic ordinary-boundary compatibility, three/five-year coverage, no double deduction, payout bases, missing sector evidence, growth eligibility/formulas, and Screen Mode isolation.

To validate a saved machine-readable analysis without committing the report:

```text
python scripts\validate_analysis.py C:\path\outside-this-repo\analysis.json
```

The validator checks schema, year/scenario completeness and cross-field arithmetic, not source accuracy or investment merit. Keep numerical JSON values unrounded; presentation tables may round them.

Full Analysis uses `schema_version: "2.0"` and requires the new audit records. Historical presentation fields and `three_year_fundamental_forecast` are retained; `forecast_extension` contains years four and five. Old Full Analysis JSON must supply the new records before it conforms to version 2.0. Synthetic cases are not BTI/GSK/Ping An backtests and do not prescribe their valuations.
