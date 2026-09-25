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
├── data-conventions.md
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

## Schema 3.0

新报告默认使用 **schema 3.0 / rubric 2**，简体中文、离线单文件 HTML，保留结论先行的六节结构。完整评分与本地扩展已纳入源码，不再依赖某台机器上的未提交安装。

- **确定性结论**：`decision` 必须给出单一动作（立即买入／分批建仓／等待到价／继续观察／回避）、现价能否买、具体买入条件及失效条件。正常输出三档参考价和收入约束上限；资金受限时明确不买及具体解除事件，不编造价格。
- **先取数**：`evidence_recovery` 逐缺口记录公司披露、集团两层、公告、交易所／监管、官方序列、历史回溯、券商流水，再记录有据区间或无法估计的具体原因。取数覆盖率不等于企业质量。
- **中文输出**：三个模式均有 `report_output`；正文、标题、附录与发布摘要默认简体中文，固定机器字段和正式来源名不翻译。轻量包也包含语言契约。

价格独立质量 **/85**、收入吸引力 **/15**、兼容组合总分 **/100**。一个分项不可评估只贡献 `[0, cap]` 方法区间，不取消其他评分，不填中性分、不重分配权重。没有可审计 N 时，支持的普通派息可使用上限 **9/15** 的当期收入代理，不能据此生成买价。

`schema.json` 的 **allOf[4] 与 allOf[18]** 均覆盖 `["2.5", "3.0"]`；相关必需字段、扩展及旧版排除分派也已同步。2.3／2.4／2.5 按原行为兼容，旧报告不自动迁移或重新评级。

独立安装目录保留完整运行脚本；仓库根目录 `scripts` 只是同一实现的入口，`tests` 与 fixtures 为仓库本地测试。`installation-manifest.json` 列明恢复的文件及位置。不得将真实报告或资料下载归档到技能源码。

## Analysis Modes

### Safety Review

使用 `safety-review.md` 对照旧基准与新披露核查现金和资本安全。不得生成新估值、评分、等级或交易指令；`automatic_trade` 始终为 false。

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

Runs the complete framework (business fundamentals, dividend capacity, sensitivity, dilution, valuation and scoring), then writes a short, conclusion-first report that answers four questions:

| Section | Answers |
|---|---|
| 1. Bottom Line | One-sentence verdict, key numbers table and action status line. |
| 2. Financial Condition | Is the dividend funded by real recurring cash? Five-year coverage table and balance-sheet constraints. |
| 3. Entry View | Where the price sits, at what price it becomes attractive, and the action with its conditions. |
| 4. Long-Term Business and Dividend Outlook | Three-to-five-year drivers and a Bear/Base/Bull FY+1/FY+3/FY+5 dividend table. |
| 5. Key Risks and Monitoring | Three to five company-specific risks with observable early signals and dividend impact. |
| 6. Sources and Key Assumptions | Cut-off date, key sources, key assumptions and data gaps, one line each. |

The main report has a length budget (about 1,200-2,000 Chinese characters excluding tables, at most five tables and three charts), states each number once, and omits placeholder rows, formulas and rule restatements. Cash-flow bridges, the five-year annual forecast, sensitivities, the full trap checklist, valuation audit, score detail and holding-review table go into an Audit Appendix that is produced only on request; JSON output always carries the full records. See [the example report](dividend-income-equity-analysis/examples/example-output-skeleton.md).

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

- Future DPS is derived from operating drivers, cash generation, reinvestment, payout policy, and dividend-entitled shares, with issuer cash settlement separated from the total dividend entitlement.
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

Generate the full reference bundle with:

```bash
bash build-gpt-instructions.sh
```

The generated output is:

```text
dist/chatgpt-custom-gpt-instructions.md
```

For lightweight screening, use `bash build-gpt-instructions.sh --mode screen` to generate `dist/chatgpt-screen-instructions.md`. It includes only data conventions, portfolio-target context, screening and withholding rules. Switch to the full canonical modules before Full Analysis; the Screen bundle cannot produce forecasts or valuations.

The root-level `chatgpt-custom-gpt-instructions.md` remains a setup guide. Prefer its header-plus-Knowledge setup and load modules by mode. The full export is not guaranteed to fit a host's Instructions field; do not truncate required rules to make it fit.

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
- six numbered Full Analysis report sections plus the on-request Audit Appendix in both template and example;
- all canonical modules included in generated GPT instructions;
- absence of selected stale rule strings;
- presence of Screen Mode, explicit screening-yield parameters, sensitivity classification, and finite-life valuation contracts.
- actual Draft 2020-12 schema validity, required new fields and local references;
- synthetic ordinary-boundary compatibility, three/five-year coverage, no double deduction, payout bases, missing sector evidence, growth eligibility/formulas, and Screen Mode isolation.
- paired regressions for unsupported tax, mandatory stock distributions, illustrative normalization and early-terminal contradictions, preserving ordinary cash, optional scrip and supported steady states;
- Screen bundle isolation and fixed evaluation-packet integrity.

验证以本地命令为准；本次升级不新增或启用 GitHub Actions，不需要市场数据凭据或模型 API 密钥。完整验收命令：

```text
python -B -m unittest discover -s tests -p "test_*.py"
pytest tests
```

To validate a saved machine-readable analysis without committing the report:

```text
python scripts\validate_analysis.py C:\path\outside-this-repo\analysis.json
```

The validator checks schema, year/scenario completeness and cross-field arithmetic, not source accuracy or investment merit. Keep numerical JSON values unrounded; presentation tables may round them.

Full Analysis uses `schema_version: "3.0"`. Historical presentation fields and `three_year_fundamental_forecast` are retained; `forecast_extension` contains years four and five. Version 2.3 combined portfolio-target provenance with the four-link normalization evidence checklist and cash/action gates; 2.5 added provisional rubric-2 scoring. Version 3.0 preserves these calculations and adds definite conclusions, retrieval records and Chinese presentation. Synthetic cases are not issuer backtests and do not prescribe valuations.

Do not automatically rewrite existing reports. A new 3.0 report needs genuine withholding and four-link normalization evidence where applicable, rubric-2 score intervals, `decision`, `evidence_recovery` and `report_output`. Screen and Safety Review require only their compact mode contracts plus recovery/presentation, never Full Analysis scores or trading instructions. Suspended Full Analysis still omits `buy_zone` but retains numeric score bounds and a definite no-buy conclusion. Legacy buy-zone keys retain cash-income labels, not intrinsic-value or action judgments.

Render a validated new record outside this repository:

```text
python dividend-income-equity-analysis\scripts\render_report.py C:\research\analysis.json C:\research\report.html
```

Eligible entry needs a stated numeric tax rate and a sourced basis, not `unknown` or `market_default`; unsupported inputs remain diagnostic. Illustrative ordinary DPS cannot become actionable through averaging or an all-supported evidence checklist. Stock-only distributions suspend cash-dividend valuation. Early terminal assumptions must reconcile with every remaining year through FY+5, including per-share dilution, using the disclosed terminal conversion assumptions. If future FX/fees or payouts require a different path, extend the explicit/transition horizon.

Focused normalization audits now use an explicit four-row evidence checklist instead of a generic request for more evidence. The machine contract enforces required links, nonblank records, declared source references and action consistency; whether the text is substantively specific and the underlying sources true still requires model/human evaluation.

## Model Evaluation Packets

`tests/fixtures/skill-evaluation-cases.json` contains eight fixed, fictional evidence packets with a 2026-01-01 cutoff, prompts, expected checks, forbidden claims and links to arithmetic regressions. They cover special payouts, tax ranges, insurer remittance gaps, mandatory/optional scrip, unknown tax, illustrative normalization and a known year-five payout reset.

`tests/fixtures/normalization-evidence-cases.json` adds two separately versioned transfer controls: a partial packet with known policy/shares but missing cash support, and a complete fictional Base cash/policy/share bridge. They check that the four-link audit neither hides missing inputs nor labels all supplied evidence missing. Keep development retests separate from the original eight-case baseline.

For actual model runs, follow the file's `run_protocol`: start fresh conversations, provide only the prompt and evidence packet with the relevant canonical modules, retain unedited responses outside this repo, and score each criterion using response excerpts. Never reveal the answer rubric to the model under evaluation. Record the model/version, skill commit and latency; a false cash-income Pass or unsupported Strong Buy is a case failure, not something to average away.

These focused rule-assessment packets are a first stage, not full issuer-report backtests. Packet-format checks and synthetic contract regressions do **not** run an LLM or measure its output accuracy. Live end-to-end report evaluation still needs dated, licensed/public disclosure snapshots, complete report generation and separate human review of source use and reasoning; no such run is claimed by this suite.
## Complete Examples and Publication

- [Worked assumptions and independent answers](dividend-income-equity-analysis/examples/worked-examples.md).
- [Ordinary analysis JSON](dividend-income-equity-analysis/examples/ordinary.analysis.json) and [growth analysis JSON](dividend-income-equity-analysis/examples/growth.analysis.json), both validated by the local entry point.
- [Portfolio target context](dividend-income-equity-analysis/portfolio-context.md) and [report publishing contract](dividend-income-equity-analysis/publishing.md).

Both generated bundle profiles identify their source commit, schema version, source dirty/clean status and deterministic build-input hash. Archives without a matching Git checkout report the commit as unknown. Local validation does not require a hosted CI service. Arithmetic checks and evidence-routing reviews do not establish investment performance; see `data-conventions.md` for point-in-time evaluation requirements.
