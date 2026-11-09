# Sector Cash-Flow and Capital Proxies

This is the single source for sector routing and distributable-capacity evidence. Apply the definitions and once-only deduction ledger in `business-fundamentals.md`. A proxy is not GAAP/IFRS cash flow; name it, identify its reporting perimeter, reconcile it to disclosures, and label its confidence.

## 1. Model Selection and Evidence

Select `operating_company`, `bank`, `bdc`, `insurer`, `reit`, `mortgage_reit`, `utility_infrastructure`, `concession_infrastructure`, `midstream_partnership`, or `holding_company`. `concession_infrastructure` and `midstream_partnership` use the operating owner-FCF arithmetic (normalized OCF − maintenance − other owner claims) with the extra evidence below; `mortgage_reit` is a spread-income proxy like `bank` and `bdc`. Choose the model from the `economic_profile` built under `economic-profile.md`, not from an industry name: the dominant segment's balance-sheet role decides between operating owner-FCF models and spread/capital proxies, and `scripts/schema3_checks.py` rejects inconsistent pairs. An industry with no dedicated model uses `operating_company` with the profile-driven KPI set. Add `holding_company` as an overlay whenever the listed parent's dividend depends on subsidiary remittances. Mixed groups require segment-specific bridges plus the parent bridge, not a blended industrial FCF.

For every proxy record:

| Model / Metric | Reporting Perimeter | Starting Disclosure | Adjustments Not Already Included | Capital / Remittance Constraint | Evidence Status |
|---|---|---|---|---|---|

Evidence status is `reported_reconciled`, `estimated_reconciled`, or `insufficient`. Name every source, fiscal period, assumption, and missing input. Confidence cannot be High for a material estimated capital/remittance bridge. With `insufficient` evidence, do not print precise recurring coverage, treat payout safety as Unclear, and suspend valuation if the gap prevents credible N/B or a funded growth path.

The sector checklists identify what to investigate, not mandatory precise values for every score. Use disclosed aggregates/equivalents and bounded, reconciled estimates when granular splits are unavailable; explain why remaining detail is nonbinding or show its sensitivity. Historical receipts and coverage can be assessed independently of an unfinished future model. A material legal/capital/remittance gap is not an innocuous missing KPI.

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

Inspect NIM, deposit/wholesale funding mix, credit losses, NPLs, provision coverage, RWA, CET1, management target buffers, payout approvals and parent liquidity. Start with the reported capital-generation bridge, RWA sensitivity and target buffers when individual lines are aggregated. Future capital and remittances may be bounded analyst estimates; do not wait for five years of issuer projections. Separate earnings generation, OCI/valuation movements, regulatory deductions and capital issued externally.

- Retained earnings are not automatically free cash. CET1 **ratios** are constraints, not cash flow.
- Compute required capital against forecast RWA and a documented target including buffers; do not subtract the full existing required-capital stock from annual earnings.
- Excess capital is a stock and can support a separately identified capital release only once. It is not recurring FAD.
- Stress NIM compression, credit losses, funding costs and RWA inflation together where economically linked.

## 3. Business Development Companies (BDCs) and Private Credit

```text
Recurring cash interest and fee income (separate cash-pay from PIK)
- funding costs - operating expenses - base/incentive management fees - normalized credit losses - tax
-> recurring net investment income (NII)
-> NII/share and regular distribution coverage
+ separately identified realized gains / spillover income
-> supplemental or special distribution capacity (not assumed recurring)
```

Require NAV/share trend, portfolio fair-value marks, non-accruals at cost and fair value, PIK income share, first-lien/senior-secured mix, borrower/industry concentration, portfolio yield, debt/equity, statutory asset coverage, unsecured vs secured funding, maturity ladder, unfunded commitments, fee hurdles and incentive-fee catch-ups. Stress falling base rates, rising credit losses, non-accrual migration, valuation markdowns and funding spreads together where relevant.

- NII is not automatically cash received: isolate PIK and non-cash fee accretion from cash-pay interest.
- NAV is a stock measure, not distributable income. Do not infer dividend safety from stable NAV alone.
- Separate regular distributions from supplemental/special dividends and return-of-capital components; assess coverage using recurring NII after fees and cash credit losses.
- Model statutory asset coverage and lender covenants before assuming additional leverage or portfolio growth.
- Treat realized gains, fee waivers and one-off recoveries separately from recurring NII.

## 4. Insurers

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

## 5. REITs and Property Trusts

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

### 5.1 Mortgage REITs (`mortgage_reit`)

```text
Interest income on mortgage assets / loans (cash coupon; separate amortization of premiums and PIK)
- repo and other funding costs +/- realized hedge settlements
- operating and management expenses - normalized credit losses (commercial mREITs)
-> earnings available for distribution (EAD / core earnings), reconciled to disclosures
-> recurring FAD per share -> dividend coverage
```

Equity-REIT AFFO, occupancy and cap rates do not apply. Require net interest spread, hedge book and swap roll-off, leverage (debt/equity and repo concentration), duration gap, prepayment speed, book value per share trend, and for commercial mREITs non-accruals, risk ratings, CECL reserves and loan maturities. Core earnings that exclude hedge losses or rely on drop income must be reconciled to cash.

- A sustained decline in book value per share while the dividend is maintained is a red flag: the payout may be returning capital.
- Share issuance below book value dilutes existing holders; do not count it as funding for the dividend.
- Stress funding spread, curve shape, prepayment and credit losses together; a dividend yield above the spread-implied return on equity is not recurring.
- EAD/core earnings is a non-GAAP earnings measure, not cash. EAD coverage alone does not prove dividend safety: a mortgage REIT can cover its dividend and still be forced to sell assets.
- **Liquidity stress (mandatory):** repo maturity ladder and counterparty concentration, unencumbered cash and agency securities versus a margin call from a stated price shock (e.g. agency MBS −5% and spread +50 bp), and book value per share under the same shock.
- **Hedge roll-off:** net interest spread after swaps and caps that mature within two years are replaced at the current curve.
- Agency and commercial mREITs share the top-level formula but use different core stresses: agency — prepayment, spread widening, repo haircut and margin calls; commercial — non-accruals, loan maturities and extensions, CECL reserves, collateral values and warehouse-line covenants.

## 6. Utilities and Infrastructure

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

### 6.1 Toll Roads and Finite Concessions (`concession_infrastructure`)

```text
Traffic volume by vehicle class x toll tariff (after toll-free days / discounts)
- operating costs - cash tax - cash interest
-> normalized OCF
- resurfacing, major repair and safety capex (maintenance)
-> Recurring Owner FCF
- committed expansion / new-concession investment - scheduled debt amortization
-> recurring FAD
```

Record each concession in `economic_profile.finite_life_assets` with its end date and share of operating cash, and show the share expiring within ten years. **Value asset by asset:** each concession contributes cash only to its own end date unless an extension or compensation is legally evidenced; the company value is the sum of concession values plus cash, other operating assets, investments, committed new concessions with their own return evidence and a justified replacement assumption, minus debt. A single concession's expiry is not the company's expiry. Use `finite_life_harvest` in `buy-zone.md` only when the whole company is in an evidenced run-off (`company_level_runoff: true`: no new concessions, shrinking perimeter); a normally reinvesting toll-road company stays on the ordinary or growth route, with the expiry ladder reflected in its cash path and terminal assumptions. Test the dividend in the year after each material expiry. Separate cyclical resurfacing from expansion, and treat acquisitions of new concessions as growth investment with their own return evidence. Tariff reviews, policy toll-free periods and competing routes belong in the stress set.

### 6.2 Midstream Pipelines and MLPs (`midstream_partnership`)

```text
Issuer-disclosed DCF (start here; record its definition)
reconciled to the cash-flow statement:
  OCF (after working capital, cash interest and cash tax)
  - maintenance capex (issuer definition, tested against depreciation and asset age)
  - preferred, minority and general-partner/IDR claims (other owner claims)
  = Recurring Owner FCF; explain every reconciling item to issuer DCF
- growth capex not funded by new debt or new units - mandatory debt reduction
-> recurring FAD -> distribution coverage
```

Do not rebuild cash from segment margins and then deduct operating costs again: disclosed segment margins are usually already after direct operating costs. Adjusted EBITDA minus interest and tax is not OCF until working capital, non-cash adjustments and other cash obligations are reconciled. Show three coverage ratios: issuer DCF / distributions, owner FCF / distributions, and after self-funded growth capex; state the leverage target and whether growth is funded at that target.

Require take-or-pay and fee-based share, contract tenor, counterparty credit, throughput, maintenance versus growth capex definition, net debt/EBITDA target, IDRs or general-partner claims, and units outstanding. Management-defined DCF often excludes growth capex entirely: show coverage both before growth capex and after the portion not funded by debt or new units. The cash model is economic; the tax route is legal. Record `economic_profile.legal_wrapper` from the issuer's US federal tax classification: a C-corp midstream issuer (e.g. KMI, WMB, OKE) uses this cash model with the ordinary dividend route; an MLP uses it with the partnership route in `withholding-notes.md`. A 1099 or K-1 label is supporting evidence only.

## 7. Holding Companies and Financial Groups

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

## 8. Other Operating Companies

| Sector | Operating Drivers | Investment / Cash Risks |
|---|---|---|
| Telecom | Subscribers, churn, ARPU, enterprise mix | Spectrum, network replacement and growth capex, leases, collection |
| Energy / mining (incl. coal and metals) | Normalized commodity prices over a full cycle, long-term contract share, volumes, unit cash costs | Sustaining capex, reserve replacement, mine closure and decommissioning, royalties, price-cap or policy risk, project commitments |
| Aircraft / equipment lessors (`asset_leasing`) | Lease rate factor, utilization, lessee credit, funding spread, fleet age | Build an asset-cash model: lease cash − funding cost − opex − tax, then net fleet investment (deliveries − sale proceeds). Routine portfolio recycling at or near book value is part of recurring cash when it has a multi-year history and a stated sale programme; gains above book and opportunistic bulk sales are one-off. Stress residual values, funding spreads and lessee defaults |
| Business trusts / stapled securities | Trust-deed distributable income, trustee-manager adjustments, operating cash at the trust and company level | Keep three numbers separate: deed-defined distributable income, actual cash generated (OCF − capex − lease and debt service at both levels) and cash actually distributed. Long-term safety rests on the second, not the payout ratio of the first; add the `holding_company` overlay when cash is upstreamed and test refinancing at both levels |
| Shipping | Available days, charter/spot mix, normalized rates | Drydock, fleet renewal, debt amortization, vessel disposal versus recurring cash |
| Consumer / industrial / technology | Volume, price/mix, unit margins, customer retention | Working capital, capacity, maintenance, stock dilution, recurring software development |
| Pharmaceuticals | Product-level volume/net price, exclusivity expiry, launch uptake | Expensed R&D, licensing/milestones, royalties, manufacturing investment, litigation |

Use operating-company owner FCF definitions, not a fresh sector-specific cash formula. For pharmaceuticals, separate established products, approved launches and probability-sensitive pipeline; do not embed all pipeline success in Base. Model patent expiry, substitution and reinvestment before extrapolating terminal growth.

## 9. What Missing Evidence Means

Use the source-first recovery paths in `data-conventions.md`: a fully deducted total-capex cash proxy can avoid demanding an unavailable maintenance/growth split; disclosed parent receipts, costs and dated capital requirements can anchor a range instead of requiring management's exact future remittances. Any unquantified material cash restriction remains unresolved.

Keep financial profitability and independently supported scoring useful even if cash remittance remains unknown, but never label earnings "verified FCF". State the field, attempted recovery, next source, affected years and decision consequence. Apply `scoring.md` to retain point/range scores and evidence coverage; unknown recurring cash must not erase unrelated dividend-history or balance-sheet evidence. Do not infer comfortable coverage from accounting payout ratios, headline solvency or dividend growth alone.
