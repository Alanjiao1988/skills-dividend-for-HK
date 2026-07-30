# Screen Mode

Screen Mode is a lightweight first-pass filter for one or more dividend stocks. Its purpose is to decide whether a company deserves Full Analysis. It must not be presented as a substitute for the full 18-section framework.

## 1. When to Trigger

Use Screen Mode when the user asks for:

- screening, quick screening, quick review, initial review, first-pass assessment, batch comparison, candidate-pool review, or whether a stock deserves deeper research;
- Chinese equivalents such as 筛选、快速评估、初步分析、批量比较、候选池、是否值得深入研究;
- analysis of multiple tickers where completing Full Analysis for every name would be impractical.

Use Full Analysis when the user asks for a complete analysis, future dividend forecast, expected buy zone, detailed fundamentals, or an investment decision on a specific stock.

If the requested mode is ambiguous and there are multiple tickers, default to Screen Mode. If there is one ticker and the user asks for a detailed investment view, default to Full Analysis.

## 2. Screen Mode Output

For each ticker, output only:

| Field | Required Output |
|---|---|
| Company / Ticker | Name and listing |
| As-of date / Price | Current verified price and date |
| TTM net yield | After withholding, with basis |
| Five-year DPS pattern | Growing / Stable / Mildly cyclical / Volatile / Cut / Suspended / Insufficient data |
| Latest coverage | FCF / Dividend or sector-equivalent coverage |
| Balance-sheet alert | None / Watch / High risk / Insufficient data |
| Withholding efficiency | High / Medium / Low / Unclear |
| Fundamental Trend preliminary | Preliminary trend classification |
| Dividend-trap screen | Pass / Warning / Fail / Insufficient data |
| Full Analysis Recommended | Yes / Watch / No |
| Main reason | One concise reason |

For batch screening, use one row per company and keep comments concise.

## 3. Mandatory Limitations

Screen Mode must not output:

- a three-year fundamental forecast;
- Bear / Base / Bull DPS;
- normalized N or bear B;
- expected buy zone, target price, fair value, accumulation zone, or Strong Buy label;
- a full 100-point score or final Grade;
- High / Medium / Low Forecast Confidence.

Always state:

```text
Mode: Screen
Forecast Confidence: Not Assessed
Buy Zone: Not Assessed
This is a first-pass filter, not a full investment analysis.
```

## 4. Minimum Evidence

Use current official sources when available. At minimum verify:

- current or latest available price;
- latest declared or trailing dividend;
- five-year dividend pattern when available;
- latest annual or trailing cash-flow coverage, or a sector-equivalent capital-coverage metric;
- legal domicile and likely withholding treatment;
- latest leverage, regulatory-capital, solvency, or refinancing warning relevant to the sector;
- any recent dividend cut, suspension, major issuance, asset-sale-funded payout, or policy weakening.

If these inputs cannot be verified, mark the affected fields `Insufficient data` rather than inferring a positive screen.

## 5. Triage Rules

### Full Analysis Recommended: Yes

Use when all are broadly true:

- TTM net yield is potentially relevant after withholding;
- dividend has not recently been cut or suspended without recovery evidence;
- latest coverage is adequate or better;
- no immediate balance-sheet or regulatory payout block is visible;
- the preliminary fundamental trend is not Structural Decline, unless a credible managed-runoff thesis may exist;
- the stock has enough information and liquidity for deeper analysis.

### Full Analysis Recommended: Watch

Use when:

- yield or business quality is potentially attractive but one or more material questions remain;
- coverage is borderline, cyclical, or based on incomplete data;
- withholding or distribution classification is unclear;
- a recent cut, restructuring, acquisition, refinancing, or policy transition needs deeper work;
- Structural Decline may have a credible finite-life harvest case but is not yet demonstrated.

### Full Analysis Recommended: No

Use when any major condition is present without a credible exception:

- dividend is suspended or likely to be cut;
- payout is clearly funded by debt, recurring issuance, or asset sales;
- normalized or latest coverage is materially below 1.0x with no recovery path;
- the balance sheet or regulatory capital position threatens distributions;
- Structural Decline has no credible harvest or managed-runoff case;
- after-tax yield is plainly insufficient for the user's dividend objective;
- the security structure, liquidity, or available evidence is unsuitable.

## 6. Screen Mode Does Not Reuse Full-Analysis Ratings

The preliminary Fundamental Trend is a screening signal only. Do not apply the final Structural Decline Grade cap, Portfolio Role, buy-zone framework, or Harvest / Managed Runoff Exception until Full Analysis is performed.

The only allowed decision label is:

```text
Full Analysis Recommended: Yes / Watch / No
```
