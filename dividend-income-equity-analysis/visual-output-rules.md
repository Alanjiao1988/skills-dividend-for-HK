# Visual Output Rules

These rules apply to Full Analysis. Screen Mode uses the compact output in `screen-mode.md` and does not require these charts.

The Full Analysis should communicate in this order:

1. Four key numbers.
2. Business, cash-flow, dividend, and valuation visuals.
3. Slim tables as the audit trail.
4. Long-form explanation.

## 1. Output Capability Detection

- Use real charts when inline chart, artifact, HTML, or interactive rendering is available.
- Otherwise use compact text visuals plus markdown tables.
- Do not fail because chart rendering is unavailable.

## 2. Key Metrics at a Glance

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| | | | |

Normalized yield must be derived from normalized business and cash-flow capacity.

## 3. Standard Charts

### 3.1 DPS Structure Chart

Stack base / ordinary DPS separately from special, supplemental, or variable DPS by fiscal year.

### 3.2 Yield Ladder

Show TTM net yield, normalized net-yield band, and Bear / Base / Bull forecast yields.

### 3.3 Coverage Chart

Show recurring FAD against the policy-relevant cash dividends paid, alongside actual cash affordability. Label the denominator. Highlight three-year aggregate coverage, five-year worst recurring coverage and the actual worst year; a normalized series must not hide an actual cash shortfall.

### 3.4 Fundamental Forecast Chart

Show historical actuals followed by five-year Bear/Base/Bull paths for a sector operating measure and recurring owner cash/FAD. Distinguish detailed years one to three from the extension; render unsupported years as gaps, not zeros. Show material investment/expiry/commissioning milestones.

### 3.5 Valuation Visual

Use the visual that matches `valuation_mode`:

- `ordinary_yield_based`: Buy-Zone Ladder with Current, Fair, Accumulation, Strong Buy, N basis, confidence, and veto.
- `total_return_based`: scenario Growth-Value Range, entry limit, valuation-review threshold, terminal-value share and R/g sensitivity; show an income entry comparison separately when credible.
- `finite_life_harvest`: Finite-Life Cash-Recovery summary with annual net distributions, discount rate, residual value, and value range.
- `suspended`: prominent status stating why ordinary buy-zone output is suspended.

Do not display a Structural Decline company as an ordinary Fair / Accumulation / Strong Buy ladder unless the ordinary framework is explicitly shown only as a secondary cross-check permitted by `buy-zone.md`.

## 4. Dividend Trajectory Tables

### Per-Share DPS Structure

| Fiscal Year | Total DPS | Base DPS | Special / Variable DPS | DPS YoY | Quality Tag | Notes |
|---|---:|---:|---:|---:|---|---|

### Yield and Coverage

| Fiscal Year | Yield at Current Price | Yield at Year Price | Payout Ratio | FCF / Dividend | Coverage Label | Comment |
|---|---:|---:|---:|---:|---|---|

Quality Tag: Stable / Growing / Cyclical / One-off / Cut / Suspended / Event-driven / Peak-cycle.

Coverage Label: Strong / Adequate / Weak / Not Available.

## 5. Historical Cash-Flow Coverage Bridge

### Cash Generation

| Fiscal Year | Reported FCF / Proxy | Recurring Owner FCF / Proxy | Remaining Growth / Mandatory Uses | Recurring FAD | Actual All-In FCF | Evidence |
|---|---:|---:|---:|---:|---|---|

Show reported OCF/capex and the signed reconciliation in a separate slim table or ledger. Explicitly show whether each cash use is already included. For financial groups, replace industrial columns with the capital/remittance bridge rather than relabeling earnings as FCF.

### Cash Return and Funding

| Fiscal Year | Cash Dividends | Buybacks | Share Issuance | Net Debt Change | FCF / Dividend | Funding Source |
|---|---:|---:|---:|---:|---:|---|

Funding Source: Operating FCF / Cash Balance / Asset Sale / Debt / Equity Issuance / Mixed.

Add Regulated Capital / Remittances for evidenced financial-sector funding. Show actual distribution capacity and actual coverage separately from recurring coverage. Give period completeness, declared-versus-paid reconciliation, and a specific reason for unavailable ratios.

## 6. Fundamental Forecast and Dividend Tables

Use `business-fundamentals.md` as the calculation source. Required records:

- Historical Operating Trend.
- Three-to-Five-Year Development Thesis and Milestones.
- Operating Driver Forecast.
- Financial Forecast.
- Owner FCF / Sector Proxy Build and Five-Year FAD Outlook.
- Single-Driver Sensitivity.
- Distributable-Cash Bridge.
- Share Count and Scrip / DRIP Assumptions.
- Dividend and Yield Runway.

### Dividend and Yield Runway

Precede the cash-cost/DPS table with a slim entitlement table: Year / Scenario, Policy-Indicated Entitlement, Modeled Entitlement, Cash-Settled Fraction, Settlement Adjustment, All-Cash Funding Gap. The two tables are complementary; do not copy the final DPS and cash cost into both.

| Year / Scenario | Cash Available for Distribution | Payout Policy / Basis / Ratio | Dividend Cash Cost | Derived DPS | Net Yield at Current Price | Funding Gap |
|---|---|---:|---|---:|---:|---:|

Cover FY+1 through FY+5 for Bear/Base/Bull, including unavailable rows when evidence is missing. Keep policy-implied cash amounts, base amounts, policy adjustments and share-count reconciliation in a separate audit table; do not repeat the forecast Dividend Cash Cost or Derived DPS there.

## 7. Sensitivity Display Rules

Every sensitivity row must show `transient`, `persistent`, or `structural`.

- Transient: show affected-year DPS and yield; buy-zone change is `N/A`.
- Transient with growth DDM: separately show the discounted cash impact; terminal growth and N remain unchanged.
- Link that impact to `growth_cash_delta_audit`: dated baseline/revised net cash, unchanged R and PV deltas. Do not report an unauditable growth-value change.
- Persistent: show revised N basis or normalization adjustment before showing a boundary change.
- Structural: display `Rebuild required` instead of a numerical boundary change.

Text examples:

```text
Transient: VLCC day rate +5,000 for one year -> FY+1 DPS +0.40 -> buy-zone boundary N/A
Persistent: tariff reset +5% -> normalized N +0.20 -> Accumulation upper bound +3.30
Structural: regulation removes business line -> full model rebuild required
```

## 8. Table Slimming Rules

- Precede every chart or table with a one-sentence takeaway.
- Maximum 7 columns per table; split wider tables.
- When withholding is 0%, state once that gross equals net rather than repeating columns.
- Separate TTM and normalized yield for cyclical stocks.
- Distinguish facts, guidance, consensus cross-checks, historical sensitivity, and analyst estimates.
- Label partial-year data and avoid unstated annualization.

## 9. Ordinary Buy-Zone Tables

Use for ordinary valuation or a clearly labelled income-only comparison alongside eligible growth valuation. Do not let a growth comparison obscure an explicit income shortfall.

### Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|

### Buy-Zone Table

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|

Also show N basis, Forecast Confidence, and Value-Trap Veto.

### Required Return Audit

| Benchmark / Date | Currency / Tenor | Tax / FX Basis | Risk-Free Anchor | Independent Premium Range | Total Return Range | Income Yield Range |
|---|---|---|---:|---:|---:|---:|

### Conditional Growth Valuation

| Scenario | PV of Explicit Dividends | PV of Terminal Value | Total Value | Terminal Share | R / Terminal g | Evidence |
|---|---:|---:|---:|---:|---|---|

Then show the safety discount, entry limit, review-above threshold and a compact R/g sensitivity grid. Reference the funded DPS path rather than reprinting the entire runway. Entry and review levels are research parameters, not orders.

Show the first terminal-year owner-cash/reinvestment/capital funding ledger, quote-unit and share/ADR conversions, and full-period investor fees. The dated valuation multiplies already converted net DPS by its cash fraction; FX and fractions must not be applied twice. Keep a hard-income price ceiling separate from economic value.

## 10. Finite-Life Harvest Table

Use when `valuation_mode = finite_life_harvest`.

| Year | Forecast Net Distribution | Discount Factor | Present Value | Key Assumption |
|---|---:|---:|---:|---|

Then show:

- Harvest horizon.
- Discount rate.
- Present value of forecast distributions.
- Residual value and percentage of total value.
- Finite-life value range.

## 11. Plain-Text Fallback

- Business and FCF trend: `Historical -> Bear | Base | Bull`.
- DPS path: `FY-4 -> FY0 -> FY+1 scenarios`.
- Yield stack: `TTM | normalized | Bear/Base/Bull`.
- Sensitivity: include type and whether N changes.
- Coverage labels by year.
- Development path: `FY+1 evidence | FY+3 capacity/cash | FY+5 durability | invalidation milestone`.
- Valuation:
  - ordinary: `Current | Fair | Accumulate | Strong Buy | Veto`;
  - growth: `Income fit | scenario values | entry limit | review level | terminal dependence`;
  - finite-life: `Harvest horizon | PV distributions | residual | value range`;
  - suspended: `Buy zone suspended — reason`.

## 12. Holding Review

Use a compact `Trigger | Evidence | Review Level | Research Action | Missing Inputs | Next Check` table, following `holding-review.md`. Distinguish a business/solvency red flag from a valuation-review signal. Do not display a specific trade size or a switch recommendation when the required portfolio/alternative information is absent.
