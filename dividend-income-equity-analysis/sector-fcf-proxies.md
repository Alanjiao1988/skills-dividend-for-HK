# Sector Cash-Flow and Capital Proxies

This is the single source for sector routing and distributable-capacity evidence. Apply the definitions and once-only deduction ledger in `business-fundamentals.md`. A proxy is not GAAP/IFRS cash flow; name it, identify its reporting perimeter, reconcile it to disclosures, and label its confidence.

## 1. Model Selection and Evidence

Select `operating_company`, `bank`, `insurer`, `reit`, `utility_infrastructure`, or `holding_company`. Add `holding_company` as an overlay whenever the listed parent's dividend depends on subsidiary remittances. Mixed groups require segment-specific bridges plus the parent bridge, not a blended industrial FCF.

For every proxy record:

| Model / Metric | Reporting Perimeter | Starting Disclosure | Adjustments Not Already Included | Capital / Remittance Constraint | Evidence Status |
|---|---|---|---|---|---|

Evidence status is `reported_reconciled`, `estimated_reconciled`, or `insufficient`. Name every source, fiscal period, assumption, and missing input. Confidence cannot be High for a material estimated capital/remittance bridge. With `insufficient` evidence, do not print precise recurring coverage, treat payout safety as Unclear, and suspend valuation if the gap prevents credible N/B or a funded growth path.

## 2. Banks

```text
Loans / earning assets x net interest margin
+ fees and other recurring income
- operating costs - normalized credit losses - tax
-> attributable earnings
-> CET1 capital generation, reconciled to regulatory disclosures
- capital needed for forecast RWA growth
- required regulatory / management buffers not already deducted
-> distributable capital, subject to legal payout and parent cash availability
```

Require NIM, deposit/wholesale funding mix, credit losses, NPLs, provision coverage, RWA, CET1, management target buffers, payout approvals and parent liquidity. Separate earnings generation, OCI/valuation movements, regulatory deductions and capital issued externally.

- Retained earnings are not automatically free cash. CET1 **ratios** are constraints, not cash flow.
- Compute required capital against forecast RWA and a documented target including buffers; do not subtract the full existing required-capital stock from annual earnings.
- Excess capital is a stock and can support a separately identified capital release only once. It is not recurring FAD.
- Stress NIM compression, credit losses, funding costs and RWA inflation together where economically linked.

## 3. Insurers

```text
In-force run-off + new business economics + underwriting result
+ sustainable investment contribution
-> attributable operating earnings and separately disclosed capital generation
- new business strain / required solvency capital / locked capital, not already included
-> legally distributable subsidiary earnings and capital
-> remittances available to the listed parent
- parent costs / interest / debt and liquidity needs, not already included
-> recurring parent FAD
```

Prefer disclosed operating capital generation, free-surplus generation, remittances and parent cash records. Reconcile their definitions: a "free surplus" metric may already include new-business strain. Require legal-entity solvency measures, target buffers, regulatory dividend restrictions, parent liquidity, debt service and dividend receipts.

- OPAT is an earnings/payout-policy reference, **not cash or remittable capital**. CSM, embedded value, NBV and changes in net assets are not annual cash available to shareholders.
- No universal retention percentage such as `OPAT x 60%` is an insurer FCF formula. A retention estimate needs a capital/remittance reconciliation and scenario-specific stress; keep unsupported coverage unavailable.
- Do not count policyholder investment cash flows as shareholder FCF, or release existing solvency surplus as recurring income.
- Model liability guarantees and duration, reinvestment yields, asset/liability mismatch, surrender behavior, underwriting losses and equity/credit shocks. Investment marks can constrain solvency even when OPAT is smoothed.
- IFRS 17 or local-accounting restatements need comparable periods. A consolidated solvency surplus does not prove every subsidiary can remit.

## 4. REITs and Property Trusts

```text
Occupied area x cash rent + contractual escalation / rent reversion
- property operating costs - cash interest - owner costs
- recurring maintenance, tenant improvements and leasing commissions
-> recurring AFFO / owner cash, reconciled to reported FFO/AFFO
- remaining committed growth uses and mandatory financing needs
-> recurring FAD -> policy distribution / DPU
```

Remove non-cash fair-value gains, straight-line rent and other non-cash adjustments appropriately. AFFO is not standardized: inspect rather than assume maintenance, leasing costs and recurring incentives are deducted. Distinguish maintenance from acquisitions and redevelopment, and funded acquisitions from perpetual issuance assumptions.

Require occupancy, rent collection, WALE/expiry ladder, tenant concentration, cap rates as a valuation cross-check, LTV, covenant headroom, debt maturity and hedges. Test higher refinancing cost, vacancy and rights-issue/DRIP dilution. Tax distribution requirements do not create cash.

## 5. Utilities and Infrastructure

```text
Regulated asset base / contracted capacity and volume
x allowed return / tariff, with regulatory timing
- cash costs - tax - interest
-> normalized OCF
- maintenance and safety / environmental investment
-> Recurring Owner FCF
- remaining committed growth projects - mandatory debt uses
-> recurring FAD
```

Forecast project commissioning, regulatory lag, tariff resets, allowed versus earned return, collection delays, fuel pass-through and financing. An approved regulated-asset increase is not immediately available dividend cash.

Show both before-growth owner cash and **after-all-committed-investment** FAD. A utility may finance valuable growth externally; that requires an explicit debt/equity plan, interest, dilution and covenant stress. It does not make negative all-in FCF disappear. Distinguish project finance that cannot be upstreamed from parent funds.

## 6. Holding Companies and Financial Groups

```text
Recurring cash dividends / distributions actually remittable from subsidiaries
+ recurring parent operating cash
- parent cash costs, tax, interest and senior claims
- parent capital injections, mandatory debt uses and liquidity retention
-> recurring parent FAD
```

Use standalone parent cash statements and subsidiary dividend declarations/receipts where available. Align receipt timing with parent payout dates and ownership percentages.

- Do not add subsidiary operating FCF to the same subsidiary's upstream dividend.
- Consolidated profit, NAV, fair-value gains and investee earnings recognized by the equity method are not cash receipts.
- Unlisted holdings, cross-border withholding, trapped cash, local solvency and debt covenants can prevent remittance.
- Subsidiary stake sales are one-off capital releases; show them outside recurring FAD and reassess the future income base after disposal.
- For an insurance/banking group, use the appropriate regulated subsidiary models **and** this parent overlay. Never mechanically choose one and ignore the other.

## 7. Other Operating Companies

| Sector | Operating Drivers | Investment / Cash Risks |
|---|---|---|
| Telecom | Subscribers, churn, ARPU, enterprise mix | Spectrum, network replacement and growth capex, leases, collection |
| Energy / mining | Normalized commodity prices, volumes, unit costs | Sustaining capex, reserve replacement, decommissioning, royalties, project commitments |
| Shipping | Available days, charter/spot mix, normalized rates | Drydock, fleet renewal, debt amortization, vessel disposal versus recurring cash |
| Consumer / industrial / technology | Volume, price/mix, unit margins, customer retention | Working capital, capacity, maintenance, stock dilution, recurring software development |
| Pharmaceuticals | Product-level volume/net price, exclusivity expiry, launch uptake | Expensed R&D, licensing/milestones, royalties, manufacturing investment, litigation |

Use operating-company owner FCF definitions, not a fresh sector-specific cash formula. For pharmaceuticals, separate established products, approved launches and probability-sensitive pipeline; do not embed all pipeline success in Base. Model patent expiry, substitution and reinvestment before extrapolating terminal growth.

## 8. What Missing Evidence Means

Keep financial profitability analysis useful even if cash remittance is unknown, but never label that earnings estimate "verified FCF". State the unavailable field, document needed to resolve it, affected forecast years, and decision consequence. Do not infer comfortable coverage from a low accounting payout ratio, strong headline solvency, or historical dividend growth alone.
