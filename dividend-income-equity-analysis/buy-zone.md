# Buy Zone Rules

This file defines how to estimate expected buy prices for dividend-income analysis.

The goal is not to produce a guaranteed target price. The goal is to translate sustainable after-tax dividend capacity and risk into a disciplined entry framework.

## 1. Required Inputs

Required data:

- Current share price and as-of date.
- Trailing DPS.
- Normalized net DPS, N, using the documented normalization basis.
- Bear net DPS, B, derived from the Bear fundamental forecast.
- Bear, Base, and Bull forecast DPS for the next three years.
- Withholding rate and net DPS.
- Five-year or longer historical price and yield context when available.
- Sector, cycle, balance-sheet, FCF coverage, Forecast Confidence, and diluted share-count context.
- Fundamental Trend, Structural Decline overlay status, and Dividend Trap Checklist result.

Optional data:

- 52-week high and low.
- Three-year and five-year price medians.
- Drawdown from recent high.
- Relevant sector or market index context.
- Historical valuation multiples appropriate to the sector.

## 2. Core Buy-Price Formula

For ordinary sustainable dividend assets, use after-tax dividend income as the primary anchor:

```text
Net DPS = Gross DPS x (1 - withholding rate)
Buy Price = Net DPS / Required Net Yield
```

For normalized analysis:

```text
Normalized Buy Price = Normalized Net DPS / Required Net Yield
```

Do not use peak-cycle DPS as the normalized buy-price anchor unless the business is demonstrably capable of sustaining that DPS through a cycle.

## 3. Fundamental Source Requirement

Read `business-fundamentals.md` before setting N or B.

### N Source Priority

`N`, normalized net DPS, must represent mid-cycle or otherwise sustainable net dividend capacity. Use this priority:

1. `mid_cycle`: explicit mid-cycle distributable cash, payout policy, diluted share count, and withholding-derived net DPS.
2. `full_cycle_median`: full-cycle median distributable cash and payout-policy-derived net DPS.
3. `three_year_base_average`: average of three-year Base-case derived net DPS only when assumptions have returned to normal operating conditions.
4. `historical_fundamental_fallback`: fundamentally adjusted historical normalized DPS; this is a Lower Confidence fallback.

Always output:

```text
N value:
N basis: mid_cycle / full_cycle_median / three_year_base_average / historical_fundamental_fallback
N source period:
N normalization adjustments:
```

A near-term Base case is not automatically normalized. Temporary commodity, freight-rate, geopolitical, credit, regulatory, interest-rate, or pricing windfalls must be removed from N.

### B Source

- `B` must normally come from Bear-case distributable cash, payout policy, diluted share count, and withholding treatment.
- N and B must reconcile to operating drivers, profitability, cash generation, required reinvestment, balance-sheet constraints, and expected scrip / DRIP dilution.
- Do not choose N or B to justify a preferred target price.
- When Forecast Confidence is Not Forecastable, do not publish an ordinary buy zone.

## 4. Required Net Yield Selection

Choose required net yield from both historical yield and risk level.

| Dividend Profile | Required Net Yield Anchor |
|---|---:|
| Stable, regulated, low-volatility income | 4%-6% |
| Strong bank / telecom / utility with moderate growth | 5%-7% |
| Cyclical but financially strong dividend payer | 7%-10% |
| Formula-based variable dividend or commodity / shipping exposure | 8%-12% |
| Weak visibility, likely cut, or high leverage | Suspend ordinary buy zone; use special-situation framework |

Adjust required yield upward when:

- Dividend is cyclical or variable.
- Forecast Confidence is Low.
- Fundamental Trend is Cyclical Peak, Transformation, or High Uncertainty.
- FCF coverage is weak or peak-cycle-only.
- Balance sheet is stretched.
- Dividend depends on asset sales, debt, or equity issuance.
- Management has a discretionary or inconsistent payout policy.
- Regulatory, commodity, FX, refinancing, or execution risk is high.
- Persistent scrip / DRIP dilution is not credibly offset.

Adjust required yield downward only when:

- Dividend has long-term stability.
- Forecast Confidence is High.
- FCF coverage is strong on normalized basis.
- Balance sheet is conservative.
- Dividend policy is clear and credible.
- The company has durable reinvestment or buyback support.

## 5. Structural Decline Valuation Mode

A company classified as `Structural Decline` must not automatically use the ordinary perpetual-style N / required-yield framework.

### 5.1 No Harvest / Managed Runoff Exception

If the exception in `scoring.md` is not satisfied:

```text
Valuation mode: suspended
Ordinary buy zone: suspended
Reason: Structural Decline without a credible finite-life harvest case
```

Do not output Fair, Accumulation, or Strong Buy zones. A low share price or high current yield is not sufficient to override this rule.

### 5.2 Harvest / Managed Runoff Exception Satisfied

Use a finite-life cash-recovery framework as the primary valuation method:

```text
Finite-Life Cash Recovery Value
= sum(Net DPS_t / (1 + k)^t)
+ Residual Value_T / (1 + k)^T
```

Required inputs:

- explicit cash-harvest horizon, T;
- annual after-tax distribution path for each year;
- expected decline rate in distributable cash;
- discount rate, k;
- conservative residual or liquidation value;
- evidence that distributions do not depend on refinancing, uncertain asset-sale timing, or new equity issuance.

Rules:

- Use a discount-rate floor of 10%.
- A default range of 10%-15% may be used when risk is moderate; use a higher rate when cash recovery, residual value, or timing is uncertain.
- Do not assume a perpetual terminal dividend.
- Residual value may be zero when asset recovery is uncertain.
- State the cash-harvest horizon and percentage of value coming from the residual value.
- Ordinary N / r yield-based zones may be shown only as a secondary cross-check, with `r_low >= 10%`; they must not replace the finite-life calculation.
- Even when the exception applies, do not label the security Core income.

Required output:

```text
Valuation mode: finite_life_harvest
Harvest horizon:
Discount rate:
Present value of forecast net distributions:
Residual value and basis:
Finite-life value range:
Ordinary yield cross-check, if used:
```

## 6. Deterministic Ordinary Buy-Zone Boundaries

Use these rules only when valuation mode is `ordinary_yield_based`.

Definitions:

```text
N = normalized net DPS using the documented N basis
B = bear-case net DPS derived from the Bear fundamental forecast
r_low = lower bound of required net yield range
r_high = upper bound of required net yield range
P_current = current share price
```

Requirements:

- `r_low` and `r_high` are decimals.
- `r_high` must be greater than `r_low`.
- If B is unavailable, use a documented conservative fallback and label the buy zone Lower Confidence.
- B must be less than or equal to N.

Boundary formulas:

```text
Too expensive boundary = N / r_low
Fair lower boundary = N / r_high
Fair upper boundary = N / r_low
Accumulation lower boundary = B / r_high
Accumulation upper boundary = N / r_high
Strong buy boundary = B / r_high
```

These formulas create a monotonic boundary set:

```text
N / r_low >= N / r_high >= B / r_high
```

| Zone | Deterministic Boundary | Interpretation |
|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Normalized yield is below minimum required yield. |
| Fair value / hold | N / r_high < Price <= N / r_low | Yield is within the required range but margin of safety is limited. |
| Accumulation zone | B / r_high < Price <= N / r_high | Normalized yield is attractive and Bear yield approaches the high-end requirement. |
| Strong buy zone | Price <= B / r_high | Bear-case DPS still meets the high-end required yield. |

If B equals N, the accumulation zone is empty and Fair connects directly to Strong Buy.

If N, B, r_low, r_high, or the Dividend Forecast Bridge is not credible, output `buy zone cannot be responsibly estimated`.

## 7. Sensitivity and Boundary Revaluation

Use the sensitivity classification from `business-fundamentals.md`:

- `transient`: do not change N or ordinary buy-zone boundaries; Accumulation Upper-Bound Change must be `N/A`;
- `persistent`: recalculate normalized distributable cash and N before updating boundaries;
- `structural`: rebuild Fundamental Trend, the forecast, scoring, veto status, and valuation mode; do not mechanically update one boundary.

A temporary commodity-price, freight-rate, interest-rate, or geopolitical move must not raise the long-term buy zone.

## 8. Value-Trap Veto

Value trap is a veto condition, not a price band.

Major veto conditions include:

- Dividend likely to be cut or suspended.
- Normalized FCF / Dividend below 1.0x without a credible recovery path.
- Dividend funded by debt, equity issuance, or asset sales rather than recurring FCF.
- Balance-sheet stress or a near-term refinancing wall.
- Regulatory restrictions that block payout.
- Peak-cycle dividend used as recurring DPS.
- Equity issuance, ATM, or persistent scrip dilution concurrent with elevated payout.
- Forecast DPS cannot be reconciled to business drivers, distributable cash, payout policy, and diluted share count.
- N retains temporary cycle premiums and is therefore not normalized.

Required wording when triggered:

```text
Value-trap veto triggered: buy-zone output is suspended. High implied yield should not be treated as an entry signal until the following conditions are resolved: ...
```

## 9. Historical Yield and Price Cross-Checks

Historical yield and price are secondary checks. They must not override a deteriorating fundamental forecast or Structural Decline valuation mode.

### Historical Yield Band

| Period | DPS Used | Price Range | Gross Yield Range | Net Yield Range | Yield Percentile | Comment |
|---|---:|---:|---:|---:|---:|---|

### Historical Price Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|
| Current price | | | |
| 52-week high | | | |
| 52-week low | | | |
| 3-year median | | | |
| 5-year median | | | |
| Recent drawdown from high | | | |
| Relevant index / sector level | | | |

## 10. Ordinary Buy-Zone Table

Use only when valuation mode is `ordinary_yield_based` and the value-trap veto is not triggered.

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Below required range | Normalized DPS | Yield below required return | Avoid adding |
| Fair value / hold | N / r_high < Price <= N / r_low | Required range | Normalized DPS | Reasonable yield, limited MOS | Hold / small add only |
| Accumulation zone | B / r_high < Price <= N / r_high | Attractive normalized yield | Normalized + Bear DPS | Acceptable coverage | Gradual buy |
| Strong buy zone | Price <= B / r_high | Bear yield meets high-end requirement | Bear-derived DPS | Strong coverage and credible forecast | Higher-conviction buy |

Always output:

```text
Valuation mode: ordinary_yield_based / finite_life_harvest / suspended
N value and basis:
B value and source:
Forecast Confidence:
Value-trap veto:
```

## 11. Required Output Language

- Use `expected buy zone`, `income entry zone`, or `finite-life value range`, not guaranteed target price.
- State the valuation mode, N basis, DPS source, and risk assumptions.
- Never imply that a high yield alone is a buy signal.
- If the operating forecast is weak, label the result Lower Confidence.
- If data is insufficient, state what is missing rather than inventing precision.

## 12. Visual Output

For ordinary valuation, show Current Price, Fair, Accumulation, Strong Buy, N basis, Forecast Confidence, and veto status.

For Structural Decline with a harvest exception, replace the ordinary Buy-Zone Ladder with a Finite-Life Cash-Recovery summary showing forecast distributions, discount rate, residual value, and value range.

For Structural Decline without the exception, show:

```text
Buy-zone status: Suspended — Structural Decline without credible managed-runoff case
```

## 13. Relationship with DDM or Other Valuation Skills

This framework is not a full corporate DCF.

- Ordinary dividend assets use normalized net DPS and required yield.
- Structural Decline harvest cases use finite-life cash recovery.
- Use a dedicated DDM, DCF, moat, or reinvestment skill for broader intrinsic-value analysis.
- If valuation methods conflict, explain the conflict rather than forcing one answer.
