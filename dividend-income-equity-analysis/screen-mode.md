# Screen Mode

Screen Mode is a lightweight first-pass filter for one or more dividend stocks. Its purpose is to decide whether a company deserves Full Analysis. It must not be presented as a substitute for the full 18-section framework.

## 1. When to Trigger

Use Screen Mode when the user asks for:

- screening, quick screening, quick review, initial review, first-pass assessment, batch comparison, candidate-pool review, or whether a stock deserves deeper research;
- Chinese equivalents such as 筛选、快速评估、初步分析、批量比较、候选池、是否值得深入研究;
- analysis of multiple tickers where completing Full Analysis for every name would be impractical.

Use Full Analysis when the user asks for a complete analysis, future dividend forecast, expected buy zone, detailed fundamentals, or an investment decision on a specific stock.

If the requested mode is ambiguous and there are multiple tickers, default to Screen Mode. If there is one ticker and the user asks for a detailed investment view, default to Full Analysis.

## 2. Screening Net-Yield Target

Read `data-conventions.md` for common input rules. Screen Mode must not invent a dividend-yield objective.

Resolve the screening net-yield target in this order:

1. A minimum or target explicitly provided by the user for the current screen.
2. A previously established portfolio-level after-tax income target that is clearly applicable to the current screen.
3. `Not Assessed` when neither is available.

Always disclose:

```text
Screening net-yield target: x.x% / Not Assessed
Target basis: user_explicit / portfolio_target / not_assessed
Target policy: hard_minimum / preference / not_assessed
Screening yield basis: dividend period + ordinary / recurring variable components + FX / tax / fee basis
```

Rules:

- Use `hard_minimum` only when the user explicitly describes the target as a minimum, cutoff, exclusion rule, or mandatory requirement. Record `hard_minimum_exception_allowed: true` only when the user explicitly permits exceptions; the default is false.
- Otherwise, an available target is a `preference`.
- Do not use the required-yield ranges in `buy-zone.md` as the user's screening target. Required return for a specific security and the investor's income-screen target are different concepts.
- Do not ask the user for a target when the screen can proceed responsibly without one. Use `Not Assessed` instead.
- If the user explicitly defines a yield basis, such as total TTM payouts including specials, follow it and label it. Still show the ordinary-income measure and repeatability warning. Do not silently reinterpret the user's cutoff.

### 2.1 Establish the Dividend Basis

Keep these measures distinct and bridge any material difference:

| Measure | Definition and use |
|---|---|
| TTM paid cash yield | Cash dividends with payment dates in the 12 months ending on the as-of date, divided by current unadjusted price. Show ordinary, variable / supplemental, special, and capital-return components separately. This is historical distribution evidence, not an entitlement available to a new buyer. |
| Latest FY ordinary cash yield | Interim plus final ordinary cash DPS attributed to the latest completed financial year, divided by current price. State the FY and whether final is proposed / approved / paid. Exclude special payouts and capital returns. Do not call a proposed final a paid dividend. |
| Screening net yield | Unless the user specifies another basis, use latest FY ordinary cash DPS, including variable payouts demonstrably made under a recurring policy, after applicable withholding. Where the issuer documents a current annual base plus recurring variable component, this can be used with period and assumptions disclosed. This is a screening proxy, not normalized N, a guaranteed floor, or a forecast. |

Do not mechanically set a cyclical stock's variable dividend to zero. Keep its historical amount visible, identify the base and variable components when disclosed, and explain the policy and coverage evidence. Conversely, an issuer's `ordinary` label does not make a disposal-funded or peak-cycle payout repeatable. If an ongoing-income target cannot be assessed without a full cycle forecast, use `Yield Fit: Unclear` and normally `Watch`; do not manufacture sustainable DPS in Screen Mode. A user-defined historical-payout screen may still be evaluated on that basis with a clear repeatability warning.

Additional rules:

- Never mix payment-date TTM with fiscal-year attribution, or add the same final dividend twice. Do not annualize a single interim / irregular payment without a documented fixed cadence and base amount; label any permitted base annualization.
- A recent cut or new payout policy takes precedence over an obsolete FY proxy. If the current annual equivalent cannot be established without a forecast, mark the screening basis `Unclear`.
- Use the same share class, split / consolidation basis, and currency for DPS and price. Use actual cash-election amounts or a dated, sourced FX conversion; never divide RMB DPS directly by an HKD quote. Apply a depositary ratio where relevant.
- Separate issuer distributions from user account cash history. Changes in holding size, PIL, reinvestment, and broker corrections do not change issuer DPS.
- Follow `withholding-notes.md` for investor profile, custody chain, event evidence, fees, and tax / FX uncertainty. Label withholding-only yield `before fees`; do not present it as spendable income after charges.
- State ex-dividend and payment dates for a material pending distribution. Buying on or after the ex-date does not confer that event's entitlement; historical yield is not dividend-capture profit. [HKEX equity FAQ](https://www.hkex.com.hk/global/exchange/faq/products/securities/equity-securites?sc_lang=en)

### 2.2 Yield Fit and Uncertainty

Let `Y_low` and `Y_high` be the lower and upper supported **screening net yields** on the same dividend, currency, tax, and fee basis as the target. A verified point estimate has equal endpoints. Calculate:

```text
Yield Fit = Pass, when Y_low >= screening net-yield target and the screening basis is usable
Yield Fit = Below target, when Y_high < screening net-yield target and the screening basis is usable
Yield Fit = Unclear, when the range crosses the target, material inputs cannot be bounded,
                      or the ongoing-income proxy is not usable
Yield Fit = Not Assessed, when no screening target is available

Yield Gap = screening net yield - screening net-yield target
```

Express Yield Gap in percentage points, with a range in the explanation when appropriate. Use `N/A` when the target is Not Assessed or yield cannot be bounded. In structured output, retain `ttm_net_yield` for the paid TTM measure; use `screening_yield_used`, `screening_yield_basis`, and `screening_yield_range` for the selected comparison, and use `null` for `yield_gap_percentage_points` when Yield Fit is Unclear or no point estimate exists. `screening_basis_usable` records whether the selected proxy and tax/fee basis can responsibly support a comparison; the validator uses it along with the supported endpoints. Yield values and range endpoints are decimals as specified in `schema.json`.

Unknown tax or fees do not mean zero deductions or a failed minimum. Show evidence-backed endpoints, not an invented generic tax band. If a spendable-income target includes fees, unknown material charges cannot support a Pass.

Synthetic example: price HKD 10; FY ordinary DPS HKD 0.60; special DPS HKD 0.40; supported ordinary-dividend withholding scenarios 0%-10%; fees excluded. Ordinary screening net yield is 5.4%-6.0%, while a 10% gross TTM paid yield including the special is not the recurring measure. Against a 5.8% minimum, Yield Fit is `Unclear` and triage normally `Watch`; against a 6.5% minimum it is `Below target` and triage `No`. These figures are illustrative, not market data.

## 3. Screen Mode Output

For each ticker, output only:

| Field | Required Output |
|---|---|
| Company / Ticker | Name and listing / share class |
| As-of date / Price | Verified unadjusted price, currency, market timestamp, and stale / suspended status if relevant |
| TTM paid net cash yield | After withholding; period and ordinary / variable / special / capital-return split |
| Latest FY ordinary / current policy yield | Net yield, FY / period, approval / payment status, and repeatability caveat |
| Screening net yield / Basis | Point or supported range; selected dividend, FX, tax, and fee basis |
| Screening net-yield target | Target or Not Assessed |
| Yield Fit / Gap | Pass / Below target / Unclear / Not Assessed; percentage-point gap / range or N/A |
| Documented dividend-growth path | Yes / No / Unclear |
| Five-year DPS pattern | Growing / Stable / Mildly cyclical / Volatile / Cut / Suspended / Insufficient data; ordinary separately from special |
| Latest coverage | FCF / cash dividend or sector-equivalent coverage, with aligned period and cash / accrual basis |
| Balance-sheet alert | None / Watch / High risk / Insufficient data |
| Withholding efficiency | Rate / range and evidence basis; unresolved nominee treatment or fees noted |
| Fundamental Trend preliminary | Preliminary trend classification |
| Dividend-trap screen | Pass / Warning / Fail / Insufficient data |
| Full Analysis Recommended | Yes / Watch / No |
| Main reason / Evidence | One concise reason and direct links to decisive sources |

For batch screening, use one row per company and keep comments concise. Related fields can share a cell. State the common target, investor scenario, basis, policy, and verification date once above the table; disclose exceptions per stock. Compact output does not permit omission of a material special payout, tax / FX uncertainty, stale price, or evidence gap.

## 4. Mandatory Limitations

Screen Mode must not output:

- a three-to-five-year fundamental or FCF forecast, growth valuation, or holding/trim/switch price;
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

## 5. Minimum Evidence

Use current official sources and show the analysis verification date. At minimum verify:

- current or latest available price, timestamp, currency, and whether trading is active;
- dividend-event ledger sufficient to reconcile TTM paid cash with latest FY ordinary DPS; include announcement, ex-date, payment date, approval status, currency, and payout type;
- five-year ordinary and special dividend patterns when available, adjusted for splits / consolidations;
- latest annual or trailing cash-flow coverage, or a sector-equivalent capital-coverage metric, with the same coverage period and no mixing of group cash with parent-only obligations;
- legal and tax domicile, investor scenario, and withholding treatment for the relevant holding channel;
- latest leverage, regulatory-capital, solvency, or refinancing warning relevant to the sector;
- any recent dividend cut, suspension, major issuance, asset-sale-funded payout, or policy weakening;
- whether a claimed dividend-growth path is supported by policy, earnings, cash flow, or an established historical record.

If these inputs cannot be verified, mark affected fields `Insufficient data`, `Unknown`, or `Unclear` rather than inferring a positive screen. A stale annual report does not displace a newer interim report, profit warning, or dividend announcement. Cite event-specific issuer filings directly. The market-date guidance above and tax references in `withholding-notes.md` were checked on **2026-09-05**; reverify facts for each live screen.

## 6. Triage Rules

Yield treatment must follow these rules before assigning Yes / Watch / No:

- If the target is `Not Assessed`, do not reject or downgrade a stock solely because its yield appears low or a target is missing.
- If Yield Fit is `Below target` and the target is a `preference`, yield alone cannot produce a `No`. Use `Watch` when a documented growth path, payout expansion, or other material question deserves Full Analysis.
- If Yield Fit is `Below target` and the target is a `hard_minimum`, use `No` unless the user explicitly permits exceptions.
- If Yield Fit is `Unclear`, do not claim that the minimum is passed or failed. Normally use `Watch`; independently verified fundamental hazards can still produce `No`.
- A documented growth path must be supported by evidence. A generic expectation that dividends may grow is not sufficient. Growth potential cannot override an explicit hard minimum without user-permitted exceptions.

### Full Analysis Recommended: Yes

Use when all are broadly true:

- when a hard minimum exists, Yield Fit is Pass;
- when a preference target exists, Yield Fit is Pass or a documented dividend-growth path could plausibly close the gap;
- a missing target alone causes no downgrade;
- ordinary / recurring-policy income is interpretable for screening, with no material unbounded tax or fee uncertainty;
- dividend has not recently been cut or suspended without recovery evidence;
- latest coverage is adequate or better;
- no immediate balance-sheet or regulatory payout block is visible;
- the preliminary fundamental trend is not Structural Decline, unless a credible managed-runoff thesis may exist;
- the stock has enough information and liquidity for deeper analysis.

### Full Analysis Recommended: Watch

Use when:

- Yield Fit is Below target under a preference policy, but dividend growth or payout growth may justify deeper work;
- Yield Fit is Unclear because tax / fees straddle the target or a cyclical / variable / recently cut dividend makes the default income proxy unreliable;
- yield or business quality is potentially attractive but one or more material questions remain;
- coverage is borderline, cyclical, or based on incomplete data;
- withholding or distribution classification is unclear;
- a recent cut, restructuring, acquisition, refinancing, or policy transition needs deeper work;
- Structural Decline may have a credible finite-life harvest case but is not yet demonstrated.

### Full Analysis Recommended: No

Use when any major condition is present without a credible exception:

- Yield Fit is Below target and the user explicitly set a hard minimum;
- dividend is suspended or concrete evidence supports an impending cut inconsistent with the screen's objective;
- payout relies on persistent unfunded borrowing, recurring issuance, or disposal of productive assets without a credible finite-life distribution case;
- latest coverage is materially inadequate on the appropriate sector metric with no recovery path; do not apply industrial FCF coverage mechanically to banks, insurers, or REITs;
- the balance sheet or regulatory capital position threatens distributions;
- Structural Decline has no credible harvest or managed-runoff case;
- the security structure, liquidity, or persistent lack of essential evidence makes deeper analysis unsuitable.

Do not use an unstated or inferred yield objective as the reason for `No`. A short-term working-capital swing, ordinary asset rotation, or one missing input does not by itself establish a dividend trap.

## 7. Screen Mode Does Not Reuse Full-Analysis Ratings

The preliminary Fundamental Trend is a screening signal only. Do not apply the final Structural Decline Grade cap, Portfolio Role, buy-zone framework, or Harvest / Managed Runoff Exception until Full Analysis is performed.

The only allowed decision label is:

```text
Full Analysis Recommended: Yes / Watch / No
```
