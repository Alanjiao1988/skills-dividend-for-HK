# Visual Output Rules

These rules apply to Full Analysis. Screen Mode uses the compact output in `screen-mode.md` and does not require these charts.

`output-template.md` decides what the reader sees. The main report carries at most three charts and five slim tables; everything else in this file is the **Audit Appendix** specification, used only when the user requests the appendix and always available as JSON records.

The main report communicates in this order:

1. The bottom-line judgment and its key numbers.
2. At most three visuals that each answer one of the four questions (finances, entry, outlook, risks).
3. Short bullets with numbers and judgments, not long-form explanation.

## 1. Output Capability Detection

- Use real charts when inline chart, artifact, HTML, or interactive rendering is available.
- Otherwise use compact text visuals plus markdown tables.
- Do not fail because chart rendering is unavailable.

## 2. Main-Report Key Numbers

Use the Bottom Line table in `output-template.md` Section 1. Normalized yield must be derived from normalized business and cash-flow capacity. Score, grade and portfolio role go in the one-line status beneath it, not in extra tables.

## 3. Main-Report Charts

Use at most three charts, one per question, and only when rendering is available. Each chart replaces, rather than duplicates, the corresponding table; the section's opening judgment serves as its caption.

### 3.1 Dividend and Coverage History (Section 2)

Stack base / ordinary DPS separately from special, supplemental or variable DPS by fiscal year, with sustainable coverage as a line and any actual-cash shortfall year highlighted. Label the coverage denominator. A normalized series must not hide an actual cash shortfall.

### 3.2 Price Position (Section 3)

Use the visual that matches the valuation mode:

- Income-yield pricing: a Cash-Income Ladder using the four band names in `buy-zone.md`, with the current price marked.
- Dividend-growth valuation: the Bear/Base/Bull growth-value range with entry limit, review level and current price; show the income comparison separately when credible.
- Finite-life cash recovery: annual net distributions and the value range.
- Suspended: no chart; state the reason in text.

For Structural Decline, show an ordinary cash-income ladder only as a secondary cross-check when specifically permitted by the finite-harvest exception in `buy-zone.md`. Ordinary ladder bands never produce action badges. A separately shown Strong Buy action needs the full independent action gates; a cash-income threshold or favorable chart color is insufficient.

### 3.3 Dividend Outlook (Section 4)

Historical DPS followed by five-year Bear/Base/Bull paths. Distinguish detailed years one to three from the extension; render unsupported years as gaps, not zeros.

Without rendering, the Section 2, 3 and 4 tables in `output-template.md` are the fallback; do not add text sparklines on top of them.

## Appendix Tables

Sections 4 to 12 below specify the Audit Appendix. Use them only when the appendix is requested, following the part numbering A1-A13 in `output-template.md`. They also define the JSON records' display form.

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
Persistent: tariff reset +5% -> normalized N +0.20 -> normalized high-end cash-yield boundary (N/r_high) +3.30
Structural: regulation removes business line -> full model rebuild required
```

## 8. Table Slimming Rules

- Main report: at most five tables, each at most six columns and eight rows; the section's opening judgment is the takeaway.
- Appendix: precede each table with a one-sentence takeaway; maximum 7 columns per table; split wider tables.
- Never print rows or columns that contain only N/A or Unknown; state the gap once instead.
- When withholding is 0%, state once that gross equals net rather than repeating columns.
- Separate TTM and normalized yield for cyclical stocks.
- Distinguish facts, guidance, consensus cross-checks, historical sensitivity, and analyst estimates.
- Label partial-year data and avoid unstated annualization.

## 9. Ordinary Cash-Income Tables

Use for ordinary valuation or a clearly labelled income-only comparison alongside eligible growth valuation. Do not let a growth comparison obscure an explicit income shortfall.

### Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|

### Cash-Income Band Table

| Cash-Income Band | Price Range | Implied Net Yield | DPS Basis | Evidence / Limitation |
|---|---:|---:|---|---|

Use these exact band names (or the Chinese equivalents in `buy-zone.md`): Below required cash yield; Normalized income within required range; Normalized income meets high-end requirement; Bear income meets high-end requirement. Also show N basis, Forecast Confidence and Value-Trap Veto. A separate action line states `action_assessment.status`, `strong_buy_eligible` and the supporting reasons; do not populate an action column merely from these mathematical bands.

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

## 11. Appendix Plain-Text Fallback

Use only inside the appendix when charts cannot render.

- Business and FCF trend: `Historical -> Bear | Base | Bull`.
- DPS path: `FY-4 -> FY0 -> FY+1 scenarios`.
- Yield stack: `TTM | normalized | Bear/Base/Bull`.
- Sensitivity: include type and whether N changes.
- Coverage labels by year.
- Development path: `FY+1 evidence | FY+3 capacity/cash | FY+5 durability | invalidation milestone`.
- Valuation:
  - ordinary: `Current price | cash-income band | N/r_low | N/r_high | B/r_high | Veto`; use the band names above, with the no-growth/intrinsic-value limitation;
  - growth: `Income fit | scenario values | entry limit | review level | terminal dependence`;
  - finite-life: `Harvest horizon | PV distributions | residual | value range`;
  - suspended: `Buy zone suspended — reason`.

## 12. Holding Review

In the main report, holding review is at most one bullet in Section 3 (Entry View), and only when the user holds the stock or asks about holding, selling or switching. Place the compact `Trigger | Evidence | Review Level | Research Action | Missing Inputs | Next Check` table in appendix part A12, following `holding-review.md`; scoring and portfolio role are in A11. Distinguish a business/solvency red flag from a valuation-review signal. Do not display a specific trade size or a switch recommendation when the required portfolio/alternative information is absent.
