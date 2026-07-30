# Visual Output Rules

This file defines the required visual and intuitive outputs for dividend analysis.

The goal is to make dividend reports readable in this order:

1. Four key numbers.
2. Standard charts when visualization is available.
3. Slim tables as data records.
4. Long-form explanation only after the reader sees the shape of the business, cash flow, dividend, and valuation story.

## 1. Output Capability Detection

Before producing visuals, detect output capability rather than platform name.

- If inline rich visualization is available, such as chart, artifact, HTML, or interactive rendering capability, use real charts for the standard visuals.
- If only plain-text or markdown output is available, downgrade gracefully to text visuals plus markdown tables.
- Do not fail just because chart rendering is unavailable.
- In rich-capable sessions, charts carry the main communication burden. Tables are the audit trail.
- In plain-text sessions, text visuals are the fallback communication layer.

## 2. Key Metrics at a Glance

Every full analysis must start with four action-relevant metrics before the long bullet summary.

If rich visualization or card-style layout is available, render these as four metric cards. If not, use a compact one-row markdown table.

| TTM Net Yield | Normalized Net Yield | Score / Grade | Portfolio Role |
|---:|---:|---:|---|
| | | | |

Rules:

- TTM Net Yield is the headline trailing yield after withholding.
- Normalized Net Yield is the more sustainable yield estimate derived from normalized business and cash-flow capacity.
- Score / Grade must match `scoring.md`.
- Portfolio Role must use the required rating vocabulary.
- If withholding treatment is the central thesis, add Withholding Efficiency as a fifth metric only when it improves clarity.

## 3. Standard Charts

These charts are required in full analysis when rich visualization is available. In plain-text environments, provide the text fallback in Section 9.

### 3.1 DPS Structure Chart

Use a stacked bar chart by fiscal year.

- Show base or ordinary DPS separately from special, supplemental, or variable DPS.
- Annotate partial years.
- Annotate non-operating special distributions.
- Purpose: show the dividend cycle shape at a glance.

### 3.2 Yield Ladder

Use a horizontal range or ladder-style chart on one axis.

Show:

- TTM net yield.
- Normalized net yield band.
- Bear, base, and bull net-yield ranges for each forecast year.

Rules:

- Emphasize TTM yield when it materially deviates from normalized yield.
- Purpose: show the gap between headline yield and sustainable yield.

### 3.3 Coverage Chart

Use paired bars by fiscal year.

Show:

- Recurring or normalized free cash flow.
- Total cash dividends.
- FCF / Dividend multiple as a label.

Purpose: show historical and forecast payment capacity and whether payout is funded by real cash flow.

### 3.4 Fundamental Forecast Chart

Show the operating and cash-flow path that supports the dividend forecast.

Preferred form:

- Historical actuals followed by Bear, Base, and Bull forecast ranges.
- Use one primary sector-appropriate operating measure, such as revenue, net interest income, AFFO, production, day rate, occupancy, or regulated asset base.
- Show FCF, distributable cash, or sector-equivalent capital generation as the dividend-capacity measure.
- Clearly separate actual and forecast periods.

Purpose: demonstrate that future DPS is grounded in business performance rather than extrapolated directly from historical dividends.

### 3.5 Buy-Zone Ladder

Use a horizontal ladder or band chart.

Show:

- Current price.
- Historical fair range if available.
- Fair / hold zone.
- Accumulation zone.
- Strong buy zone.
- Value-trap veto status, shown as Not triggered / Triggered / Unclear.

Purpose: translate fundamentally derived net DPS and historical price context into a disciplined income entry zone. Do not show value trap as a price band.

## 4. Dividend Trajectory Tables

Every full analysis must include year-by-year dividend trajectory data.

Apply the table slimming rules in Section 7 before choosing table layout.

### Per-share DPS Structure Table

| Fiscal Year | Total DPS | Base DPS | Special / Variable DPS | DPS YoY | Quality Tag | Notes |
|---|---:|---:|---:|---:|---|---|

### Yield and Coverage Table

| Fiscal Year | Yield at Current Price | Yield at Year Price | Payout Ratio | FCF / Dividend | Coverage Label | Comment |
|---|---:|---:|---:|---:|---|---|

Definitions:

- Yield at Current Price = that year's DPS divided by the current price used in the analysis.
- Yield at Year Price = that year's DPS divided by year-end price or average price for that year. If unavailable, mark N/A.
- DPS YoY must show the percentage change and direction.
- Quality Tag should be Stable, Growing, Cyclical, One-off, Cut, Suspended, Event-driven, or Peak-cycle.
- Coverage Label should be Strong, Adequate, Weak, or Not Available.

After the table, add a short paragraph called Dividend Pattern. State whether the stock is stable income, progressive income, formula-based variable income, cycle income, or one-off distribution.

## 5. Historical Cash-Flow Coverage Bridge

Every full analysis should include a funding bridge when data is available.

If the bridge exceeds seven columns, split it into two tables:

### Cash Generation Table

| Fiscal Year | Net Income | Operating Cash Flow | Capex | Free Cash Flow | FCF Quality | Comment |
|---|---:|---:|---:|---:|---|---|

### Cash Return and Funding Table

| Fiscal Year | Cash Dividends | Buybacks | Share Issuance | Net Debt Change | FCF / Dividend | Funding Source |
|---|---:|---:|---:|---:|---:|---|

If company-reported free cash flow is unavailable, calculate operating cash flow minus capex and clearly label it as estimated.

Funding Source should be Operating FCF, Cash Balance, Asset Sale, Debt, Equity Issuance, or Mixed.

## 6. Fundamental Forecast and Dividend Bridge Tables

Use `business-fundamentals.md` as the authoritative source for table structures and calculation logic.

The required data record includes:

- Historical Operating Trend.
- Operating Driver Forecast.
- Financial Forecast.
- Distributable-Cash Bridge.
- DPS Derivation.

When rich visualization is available, use the Fundamental Forecast Chart to communicate the result. Keep the tables as the audit trail.

## 7. Table Slimming Rules

- Every table and every chart must be preceded by a one-sentence takeaway telling the reader what to look for.
- Hard ceiling of 7 columns per table. If a table would exceed 7 columns, split it into smaller tables.
- If withholding is 0%, drop the Withholding, Net DPS, and Net Yield columns. State once above the relevant table: "Withholding 0% — gross equals net."
- If withholding is not 0%, use a compact tax table rather than repeating withholding columns in every historical row, unless year-by-year withholding differs.
- For cyclical stocks, separate TTM yield from normalized yield in all summaries.
- Historical facts, company guidance, consensus cross-checks, and analyst estimates must be visibly distinguished.
- Tables are the data record. Charts are the communication layer.
- Partial-year data must be labeled clearly as partial and must not be annualized unless the method is explicitly stated.

## 8. Buy-Zone Visual and Tables

Use `buy-zone.md` as the authoritative logic source.

### Historical Price and Yield Context

| Metric | Price / Level | Current Position | Comment |
|---|---:|---:|---|

### Buy-Zone Table

| Zone | Price Range | Implied Net Yield | DPS Basis | Condition Required | Action View |
|---|---:|---:|---|---|---|

Also show value-trap veto status separately:

```text
Value-trap veto: Not triggered / Triggered / Unclear
```

If rich visualization is available, also render the Buy-Zone Ladder. If unavailable, use the text fallback in Section 9.

## 9. Plain-Text Fallback Visuals

Use these when rich visualization is unavailable.

- Business and FCF trend: `Historical stable -> Base growth 3%-5% -> Bear decline 10% -> Bull growth 8%`.
- DPS path: `2022 1.42 -> 2023 6.29 -> 2024 5.77 -> 2025 2.93`.
- Yield stack: `TTM yield 10.7% | normalized 5%-7% | bear 2%-3% | base 4%-6%`.
- Coverage labels: `2023 Strong | 2024 Adequate | 2025 Adequate | 2026 Peak-cycle / Uncertain`.
- Buy-zone ladder: `Current 100 | Fair 90-100 | Accumulate 75-90 | Strong buy <75 | Veto: not triggered`.

Do not replace tables with text visuals. Use text visuals to make tables easier to understand when charts are unavailable.

## 10. Three-Year Dividend Runway

The forecast must include both per-share dividends and cash coverage.

If rich visualization is available, include the Yield Ladder and Fundamental Forecast Chart. Always keep a table as the data record.

| Fiscal Year | Scenario | DPS | Net Yield at Current Price | Estimated FCF | Dividend Cash Cost | FCF / Dividend |
|---|---|---:|---:|---:|---:|---:|

DPS must be derived from the Three-Year Fundamental Forecast and Dividend Forecast Bridge in `business-fundamentals.md`.

If more detail is needed, add a separate assumptions table with Balance Sheet Impact and Key Assumptions.
