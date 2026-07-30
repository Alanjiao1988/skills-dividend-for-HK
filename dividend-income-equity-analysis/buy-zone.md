# Buy Zone Rules

This file defines how to estimate expected buy prices for dividend-income analysis.

The goal is not to produce a single target price. The goal is to translate dividend sustainability and historical valuation into a disciplined buy zone.

## 1. Required Inputs

Use the most current and reliable data available.

Required data:

- Current share price and as-of date.
- Trailing DPS.
- Normalized net DPS derived from the normalized fundamental forecast and Dividend Forecast Bridge.
- Bear net DPS derived from the Bear fundamental forecast and Dividend Forecast Bridge.
- Bear, Base, and Bull forecast DPS for the next three years.
- Withholding rate and net DPS.
- Five-year or longer historical price range when available.
- Historical year-end price, average price, or closing-price range.
- Historical gross and net dividend yield range.
- Historical dividend-yield percentiles when data is available.
- Sector, cycle, balance-sheet, FCF coverage, Forecast Confidence, and diluted share-count context.
- Dividend Trap Checklist result.

Optional data:

- 52-week high and low.
- Three-year and five-year price high / low / median.
- Drawdown from recent high.
- Market index level or sector index context when relevant.
- Historical valuation multiples such as P/E, P/B, EV/EBITDA, or P/FFO for REITs.

## 2. Core Buy-Price Formula

Use after-tax dividend income as the primary anchor:

```text
Net DPS = Gross DPS x (1 - withholding rate)
Buy Price = Net DPS / Required Net Yield
```

For normalized analysis:

```text
Normalized Buy Price = Normalized Net DPS / Required Net Yield
```

For scenario analysis:

```text
Bear Buy Price = Bear Net DPS / Required Bear Yield
Base Buy Price = Base Net DPS / Required Base Yield
Bull Buy Price = Bull Net DPS / Required Bull Yield
```

Do not use peak-cycle DPS as the base-case buy-price anchor unless the business is demonstrably capable of sustaining that DPS through a cycle.

## 3. Fundamental Source Requirement

Read `business-fundamentals.md` before setting N or B.

### N Source Priority

`N`, normalized net DPS, must represent mid-cycle or otherwise sustainable net dividend capacity. Use this source priority:

1. `mid_cycle`: explicit mid-cycle distributable cash, payout policy, diluted share count, and withholding-derived net DPS.
2. `full_cycle_median`: full-cycle median distributable cash, payout policy, diluted share count, and withholding-derived net DPS.
3. `three_year_base_average`: average of the three-year Base-case derived net DPS only when the Base assumptions have returned to normal operating conditions and do not retain temporary premiums or trough effects.
4. `historical_fundamental_fallback`: historical normalized DPS adjusted for current business fundamentals, payout policy, and diluted share count; this is a Lower Confidence fallback.

Always output:

```text
N basis: mid_cycle / full_cycle_median / three_year_base_average / historical_fundamental_fallback
N source period:
N normalization adjustments:
```

A near-term Base case is not automatically normalized. Do not use temporary commodity, freight-rate, geopolitical, credit, regulatory, interest-rate, or pricing windfalls in N without normalizing the underlying driver.

### B Source

- `B`, bear-case net DPS, must normally come from Bear-case distributable cash, payout policy, diluted share count, and withholding treatment.
- The operating assumptions used for N and B must reconcile to revenue or sector-equivalent income, profitability, cash generation, required reinvestment, balance-sheet constraints, and expected scrip / DRIP dilution.
- Do not select N or B by averaging historical DPS and then choosing a preferred target price.
- Historical DPS averages may be used only as a cross-check or fallback when a responsible operating forecast cannot be built.
- When a historical fallback is used, label the buy zone Lower Confidence and explain the missing operating inputs.
- When Forecast Confidence is Not Forecastable, do not publish an ordinary buy zone.

## 4. Required Net Yield Selection

Choose required net yield from both historical yield and risk level.

Default guide:

| Dividend Profile | Required Net Yield Anchor |
|---|---:|
| Stable, regulated, low-volatility income | 4%-6% |
| Strong bank / telecom / utility with moderate growth | 5%-7% |
| Cyclical but financially strong dividend payer | 7%-10% |
| Formula-based variable dividend or commodity / shipping exposure | 8%-12% |
| Weak visibility, possible cut, or high leverage | Do not set a normal buy price; use special-situation framework |

Adjust required yield upward when:

- Dividend is cyclical or variable.
- Forecast Confidence is Low.
- Fundamental Trend is Structural Decline, Cyclical Peak, Transformation, or High Uncertainty.
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

## 5. Deterministic Buy-Zone Boundary Rules

Use these boundary rules so the same inputs produce the same buy-zone output.

Definitions:

```text
N = normalized net DPS using the documented N basis
B = bear-case net DPS derived from the Bear fundamental forecast
r_low = lower bound of required net yield range
r_high = upper bound of required net yield range
P_current = current share price
```

Requirements:

- `r_low` and `r_high` must be expressed as decimals, e.g. 0.06 for 6%.
- `r_high` must be greater than `r_low`.
- Use normalized DPS for fair and accumulation zones.
- Use bear or conservative DPS for strong-buy safety-margin testing.
- If `B` is unavailable, use a conservative haircut to N only as a documented fallback and label the buy zone Lower Confidence.
- `B` must be less than or equal to `N`. If `B > N`, treat the inputs as invalid and explain the data problem.

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

Zone mapping:

| Zone | Deterministic Boundary | Interpretation |
|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Normalized yield is below minimum required yield. |
| Fair value / hold | N / r_high < Price <= N / r_low | Normalized yield is within required range but margin of safety is limited. |
| Accumulation zone | B / r_high < Price <= N / r_high | Normalized yield is attractive and bear-case yield is approaching the high-end required yield. |
| Strong buy zone | Price <= B / r_high | Bear-case DPS still meets the high-end required yield. |

If B equals N, the accumulation zone becomes empty because bear-case DPS equals normalized DPS. In that case, state that there is no separate accumulation band and let fair value connect directly to the strong-buy boundary.

If B is missing, r_low/r_high is missing, the Dividend Forecast Bridge cannot be reconciled, or the dividend inputs are not credible, output "buy zone cannot be responsibly estimated" and list missing or invalid inputs.

## 6. Value-Trap Veto

Value trap is not a price zone. It is a veto condition.

If any major value-trap condition is triggered, all buy zones are suspended until the condition is resolved or explicitly treated as a special situation.

Major veto conditions include:

- Dividend likely to be cut or suspended.
- Normalized FCF / Dividend below 1.0x without a credible recovery path.
- Dividend funded by debt, equity issuance, or asset sales rather than recurring FCF.
- Balance sheet stress or near-term refinancing wall.
- Regulatory restriction or policy change that blocks payout.
- Peak-cycle dividend being used as recurring DPS.
- Equity issuance, ATM, or persistent scrip dilution concurrent with elevated payout and unclear capital need.
- Forecast DPS cannot be reconciled to business drivers, distributable cash, payout policy, and diluted share count.
- Fundamental forecast shows declining distributable cash while the DPS assumption remains stable or growing without a credible funding source.
- N retains temporary cycle premiums and is therefore not normalized.

Required wording when triggered:

```text
Value-trap veto triggered: buy-zone output is suspended. High implied yield should not be treated as an entry signal until the following conditions are resolved: ...
```

## 7. Historical Yield Band Cross-Check

Build a historical yield band when data is available.

| Period | DPS Used | Price Range | Gross Yield Range | Net Yield Range | Yield Percentile | Comment |
|---|---:|---:|---:|---:|---:|---|

Use at least five years when possible. For cyclical sectors, include a full cycle if available.

Interpretation:

- Current yield below historical median: usually not attractive for pure dividend entry unless dividend growth is strong.
- Current yield near historical median: fair zone, not necessarily a margin-of-safety buy.
- Current yield in the top quartile of historical range: potentially attractive, but check whether the market is pricing in a dividend cut.
- Current yield far above history: either rare opportunity or dividend trap. Use FCF coverage and balance sheet to decide.

Historical yield bands are a cross-check. They must not override a deteriorating fundamental forecast.

## 8. Historical Price Context

Use historical price levels as a secondary anchor, not the primary anchor.

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|
| Current price | | | |
| 52-week high | | | |
| 52-week low | | | |
| 3-year median | | | |
| 5-year median | | | |
| Recent drawdown from high | | | |
| Relevant index / sector level | | | |

Historical price can show sentiment and cyclicality, but it does not determine dividend value by itself. A stock can be cheap versus history and still be unattractive if normalized DPS is falling.

## 9. Buy-Zone Table

Every full dividend analysis should include a buy-zone table unless the user explicitly asks not to.

Use this table after applying the value-trap veto.

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|
| Too expensive / avoid adding | Price > N / r_low | Below required range | Normalized DPS | Yield below required return | Avoid adding |
| Fair value / hold | N / r_high < Price <= N / r_low | Required range | Normalized DPS | Reasonable yield, limited MOS | Hold / small add only |
| Accumulation zone | B / r_high < Price <= N / r_high | Attractive normalized yield | Normalized + Bear DPS | Required yield met with acceptable coverage | Gradual buy |
| Strong buy zone | Price <= B / r_high | Bear-case yield meets high-end required yield | Bear-derived DPS | Strong coverage, balance sheet, and credible forecast required | Higher conviction buy |

Also output:

```text
N value:
N basis: mid_cycle / full_cycle_median / three_year_base_average / historical_fundamental_fallback
N source period and normalization adjustments:
B value and source:
Forecast Confidence: High / Medium / Low / Not Forecastable
Value-trap veto: Not triggered / Triggered / Unclear
```

## 10. Safety-Margin and Sensitivity Checks

Before stating a buy zone, check:

- Does the buy price still make sense using bear-case DPS?
- Does the implied yield rely on special or peak-cycle dividends?
- Is FCF / Dividend above 1.0x on normalized basis?
- Would buy price still be reasonable if payout ratio falls to policy floor?
- Is current price already above the fair value range implied by normalized net yield?
- Is the stock cheap because of a temporary cycle issue or because the dividend is likely to be cut?
- Are N and B traceable to operating drivers and distributable cash?
- Is diluted share count consistent with forecast issuance, scrip / DRIP, and buybacks?
- Does the single-driver sensitivity imply that a modest adverse move would materially reduce the accumulation upper boundary?

## 11. Required Output Language

Use disciplined language:

- Use "expected buy zone", "accumulation zone", or "income entry zone" rather than guaranteed target price.
- State the DPS basis, N basis, and forecast source used for each price range.
- Never imply that a high yield alone is a buy signal.
- If the operating forecast is weak, label the buy zone Lower Confidence.
- If data is insufficient, output "buy zone cannot be responsibly estimated" and list the missing inputs.

## 12. Visual Output

When rich visualization is available, add a Buy-Zone Ladder:

- Current price.
- Fair-value zone.
- Accumulation zone.
- Strong buy zone.
- N basis.
- Forecast Confidence.
- Value-trap veto status.

When rich visualization is unavailable, use a compact text fallback:

```text
Buy-zone ladder: Current 100 | Fair 90-100 | Accumulate 75-90 | Strong buy <75 | N basis: mid-cycle | Confidence: Medium | Veto: not triggered
```

## 13. Relationship with DDM or Other Valuation Skills

This buy-zone framework is not a full DDM valuation and should not replace a dedicated valuation model.

- This skill sets dividend-income entry zones using fundamentally derived net DPS, required yield, historical yield bands, and cash-flow safety.
- If the user asks for intrinsic value, DDM, moat, or reinvestment runway, use or reference the appropriate valuation skill.
- If dividend buy zone and DDM valuation conflict, explain the conflict rather than forcing one answer.
