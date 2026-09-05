# Screen Mode

Screen Mode is a lightweight first-pass filter for one or more dividend stocks. Its purpose is to decide whether a company deserves Full Analysis. It must not be presented as a substitute for the full 18-section framework.

## 1. When to Trigger

Use Screen Mode when the user asks for:

- screening, quick screening, quick review, initial review, first-pass assessment, batch comparison, candidate-pool review, or whether a stock deserves deeper research;
- Chinese equivalents such as 筛选、快速评估、初步分析、批量比较、候选池、是否值得深入研究;
- analysis of multiple tickers where completing Full Analysis for every name would be impractical.

Use Full Analysis when the user asks for a complete analysis, a three-to-five-year business or FCF forecast, future dividend forecast, expected buy zone, holding review, detailed fundamentals, or an investment decision on a specific stock.

If the requested mode is ambiguous and there are multiple tickers, default to Screen Mode. If there is one ticker and the user asks for a detailed investment view, default to Full Analysis.

## 2. Screening Net-Yield Target

Screen Mode must not invent a dividend-yield objective.

Resolve the screening net-yield target in this order:

1. A minimum or target explicitly provided by the user for the current screen.
2. A previously established portfolio-level after-tax income target that is clearly applicable to the current screen.
3. `Not Assessed` when neither is available.

Always disclose:

```text
Screening net-yield target: x.x% / Not Assessed
Target basis: user_explicit / portfolio_target / not_assessed
Target policy: hard_minimum / preference / not_assessed
```

Rules:

- Use `hard_minimum` only when the user explicitly describes the target as a minimum, cutoff, exclusion rule, or mandatory requirement.
- Otherwise, an available target is a `preference`.
- Do not use the required-yield ranges in `buy-zone.md` as the user's screening target. Required return for a specific security and the investor's income-screen target are different concepts.
- Do not ask the user for a target when the screen can proceed responsibly without one. Use `Not Assessed` instead.

For each stock, calculate:

```text
Yield Fit = Pass, when TTM net yield >= screening net-yield target
Yield Fit = Below target, when TTM net yield < screening net-yield target
Yield Fit = Not Assessed, when no screening target is available

Yield Gap = TTM net yield - screening net-yield target
```

Express Yield Gap in percentage points. Use `N/A` when the target is Not Assessed.

## 3. Screen Mode Output

For each ticker, output only:

| Field | Required Output |
|---|---|
| Company / Ticker | Name and listing |
| As-of date / Price | Current verified price and date |
| TTM net yield | After withholding, with basis |
| Screening net-yield target | Target or Not Assessed |
| Yield Fit / Gap | Pass / Below target / Not Assessed; percentage-point gap or N/A |
| Documented dividend-growth path | Yes / No / Unclear |
| Five-year DPS pattern | Growing / Stable / Mildly cyclical / Volatile / Cut / Suspended / Insufficient data |
| Latest coverage | FCF / Dividend or sector-equivalent coverage |
| Balance-sheet alert | None / Watch / High risk / Insufficient data |
| Withholding efficiency | High / Medium / Low / Unclear |
| Fundamental Trend preliminary | Preliminary trend classification |
| Dividend-trap screen | Pass / Warning / Fail / Insufficient data |
| Full Analysis Recommended | Yes / Watch / No |
| Main reason | One concise reason |

For batch screening, use one row per company and keep comments concise. State the target, basis, and policy once above the batch table when the same target applies to all names.

## 4. Mandatory Limitations

Screen Mode must not output:

- a three-to-five-year fundamental or FCF forecast;
- Bear / Base / Bull DPS;
- normalized N or bear B;
- expected buy zone, target price, fair value, accumulation zone, or Strong Buy label;
- growth-based valuation, terminal growth, or trim/exit price thresholds;
- a full 100-point score or final Grade;
- High / Medium / Low Forecast Confidence.

Always state:

```text
Mode: Screen
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
This is a first-pass filter, not a full investment analysis.
```

## 5. Minimum Evidence

Use current official sources when available. At minimum verify:

- current or latest available price;
- latest declared or trailing dividend;
- five-year dividend pattern when available;
- latest annual or trailing cash-flow coverage, or a sector-equivalent capital-coverage metric;
- legal domicile and likely withholding treatment;
- latest leverage, regulatory-capital, solvency, or refinancing warning relevant to the sector;
- any recent dividend cut, suspension, major issuance, asset-sale-funded payout, or policy weakening;
- whether a claimed dividend-growth path is supported by policy, earnings, cash flow, or an established historical record.

If these inputs cannot be verified, mark the affected fields `Insufficient data` or `Unclear` rather than inferring a positive screen.

Use the appropriate metric and limitations in `sector-fcf-proxies.md` for the latest-coverage check; do not run its full forecast or force industrial FCF onto financial firms. OPAT, a solvency ratio or a low earnings payout alone is not verified cash coverage. Do not add historical CAGR to current yield and label the sum expected total return.

## 6. Triage Rules

Yield treatment must follow these rules before assigning Yes / Watch / No:

- If the target is `Not Assessed`, do not reject or downgrade a stock solely because its yield appears low.
- If Yield Fit is `Below target` and the target is a `preference`, yield alone cannot produce a `No`. Use `Watch` when a documented growth path, payout expansion, or other material question deserves Full Analysis.
- If Yield Fit is `Below target` and the target is a `hard_minimum`, use `No` unless the user explicitly permits exceptions.
- A documented growth path must be supported by evidence. A generic expectation that dividends may grow is not sufficient.

### Full Analysis Recommended: Yes

Use when all are broadly true:

- TTM net yield is relevant to the screen, or the target is Not Assessed;
- when a preference target exists, Yield Fit is Pass or a documented dividend-growth path could plausibly close the gap;
- dividend has not recently been cut or suspended without recovery evidence;
- latest coverage is adequate or better;
- no immediate balance-sheet or regulatory payout block is visible;
- the preliminary fundamental trend is not Structural Decline, unless a credible managed-runoff thesis may exist;
- the stock has enough information and liquidity for deeper analysis.

### Full Analysis Recommended: Watch

Use when:

- Yield Fit is Below target under a preference policy, but dividend growth or payout growth may justify deeper work;
- the target is Not Assessed and yield suitability therefore remains unresolved;
- yield or business quality is potentially attractive but one or more material questions remain;
- coverage is borderline, cyclical, or based on incomplete data;
- withholding or distribution classification is unclear;
- a recent cut, restructuring, acquisition, refinancing, or policy transition needs deeper work;
- Structural Decline may have a credible finite-life harvest case but is not yet demonstrated.

### Full Analysis Recommended: No

Use when any major condition is present without a credible exception:

- Yield Fit is Below target and the user explicitly set a hard minimum;
- dividend is suspended or likely to be cut;
- payout is clearly funded by debt, recurring issuance, or asset sales;
- normalized or latest coverage is materially below 1.0x with no recovery path;
- the balance sheet or regulatory capital position threatens distributions;
- Structural Decline has no credible harvest or managed-runoff case;
- the security structure, liquidity, or available evidence is unsuitable.

Do not use an unstated or inferred yield objective as the reason for `No`.

## 7. Screen Mode Does Not Reuse Full-Analysis Ratings

The preliminary Fundamental Trend is a screening signal only. Do not apply the final Structural Decline Grade cap, Portfolio Role, buy-zone framework, or Harvest / Managed Runoff Exception until Full Analysis is performed.

The only allowed decision label is:

```text
Full Analysis Recommended: Yes / Watch / No
```
