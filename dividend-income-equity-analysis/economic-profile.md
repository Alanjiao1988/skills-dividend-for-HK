# Economic Profile: Classify by Economics, Not by Industry List

This is the canonical routing module for every Full Analysis. It replaces industry enumeration as the source of analytical rules. An issuer is first described by **seven economic dimensions**; each dimension value triggers specific required analysis, cash model constraints, valuation treatment, stress tests and tax routing. The industry tables in `industry-analysis.md` are a **quick-reference** of typical profiles and KPIs, not a whitelist and not the source of rules. A new industry needs a correct profile, not a new rule file.

Read with `industry-analysis.md`, `historical-financial-trends.md`, `sector-fcf-proxies.md`, `business-fundamentals.md`, `buy-zone.md` and `withholding-notes.md`.

## 1. When and How to Build the Profile

- Build `economic_profile` before choosing KPIs, the `cash_flow_model.sector_model`, or the valuation route. Every twelve-chapter Full Analysis must record it (validated by `scripts/schema3_checks.py`).
- Profile **each material segment** separately (normally any segment above about 15% of operating cash, profit or capital). A diversified group is the sum of its segments plus the parent layer; a conglomerate label is not a profile.
- Classify from filings, segment notes, contracts, concession schedules, regulatory disclosures and the cash-flow statement. Where the evidence is ambiguous, pick the more conservative value and say why.
- Chapter 2 presents the profile table; Audit Appendix A5 carries the full record.

## 2. The Seven Dimensions

### D1. Revenue engine (`revenue_engine`, per segment)

| Value | Meaning | Triggered analysis |
|---|---|---|
| `regulated_or_contracted` | Price set by regulator, concession formula or long-term contract | Contract/tariff tenor, reset dates, counterparty credit, indexation, renewal risk |
| `volume_times_price` | Market volume and price/mix drive revenue | Separate volume, price, mix and FX; market share; elasticity |
| `commodity_linked` | Realized price follows a commodity or freight benchmark | Realized versus benchmark, hedges, cash breakeven, cycle-normalized price deck |
| `spread_income` | Earns the gap between asset yield and funding cost | Asset yield, funding cost, leverage, credit losses, rate sensitivity |
| `fee_or_aum` | Fee on assets, volumes or transactions | Fee rate, flows, market-level sensitivity, fee compression |
| `subscription_recurring` | Recurring contracted subscriptions or usage | Retention/churn, ARPU, cohort economics |

### D2. Asset life (`asset_life`, per segment)

| Value | Meaning | Triggered analysis |
|---|---|---|
| `perpetual_going_concern` | Assets are routinely replaced; no legal or physical end date drives value | Standard maintenance-versus-growth split |
| `finite_assets` | Material cash comes from assets with an end date: concessions, reserves, patents, vessels/aircraft, projects, trust terms | **Asset-level finite-life valuation** (Section 3.1); record each asset in `finite_life_assets` |

`finite_assets` describes assets, not the company. A company holding finite assets is valued as the sum of each asset's remaining-life cash flows **plus** cash, other assets, committed new projects and a justified replacement/extension assumption, minus debt. Only when the whole company is in an evidenced run-off (no reinvestment, contracting perimeter) set `company_level_runoff: true`; only then may `valuation_mode` be `finite_life_harvest` (Structural Decline exception in `buy-zone.md`).

### D3. Cyclicality (`cyclicality`, per segment)

| Value | Meaning | Triggered analysis |
|---|---|---|
| `stable` | Demand and margin vary little through cycles | Five-year history is usually sufficient |
| `demand_cycle` | Volumes follow GDP, trade, credit or capex cycles | Normalize over a full demand cycle |
| `supply_cycle` | Returns follow capacity additions/exits (shipping, semis, chemicals) | Orderbook/capacity data; never annualize a peak quarter or peak distribution |
| `commodity_cycle` | Returns follow a commodity price | Mid-cycle price deck with stated source; low-price stress |
| `rate_cycle` | Returns follow interest rates or curve shape | Rate-path scenarios, deposit/funding beta, hedge roll-off |

For any non-`stable` value record `cycle_window` (years and why that window spans a full cycle). A five-year window inside one up-cycle is not mid-cycle.

### D4. Balance-sheet role (`balance_sheet_role`, per segment)

| Value | Meaning | Required cash model |
|---|---|---|
| `operating` | The balance sheet funds operations; cash comes from operating margin | Operating owner FCF (`operating_company`, `utility_infrastructure`, `concession_infrastructure`, `midstream_partnership`) |
| `balance_sheet_spread` | The balance sheet **is** the business: banks, BDCs, mortgage REITs, insurers | Spread/capital proxy (`bank`, `bdc`, `mortgage_reit`, `insurer`); never industrial FCF. Funding liquidity, capital and book-value stress are mandatory. Valuation may use `capital_return_based` (`buy-zone.md` Section 7A) so buybacks and RoTE are priced |
| `asset_leasing` | Owns long-lived assets leased to others (aircraft, equipment, property) | `operating_company` or `reit`, plus funding-spread, residual-value and lessee-credit stress; asset sales split into routine recycling and one-off disposals |

### D5. Capital intensity (`capital_intensity`, per segment)

`asset_light`, `maintenance_heavy` (high sustaining capex, little growth) or `growth_heavy` (large expansion programme). Maintenance-heavy and growth-heavy segments must show the maintenance/growth split or a fully deducted total-capex proxy, and incremental return on growth investment.

### D6. Legal and distribution wrapper (`legal_wrapper`, issuer level)

| Value | Triggered rules |
|---|---|
| `ordinary_company` | Ordinary dividend route in `withholding-notes.md` |
| `reit` | Distribution requirement, AFFO/DPU basis, REIT withholding rules |
| `us_publicly_traded_partnership` | §1446(a) distribution withholding and §1446(f) transfer withholding (Section 3.3); K-1 and US filing; never treated as an ordinary US dividend |
| `business_trust_or_stapled` | Trust-deed distributable income versus trust and company cash; two-level debt test |
| `holding_parent` | Parent-only cash, subsidiary remittance and restrictions (`sector-fcf-proxies.md` holding-company overlay) |
| `fund_or_etf` | Out of scope for the issuer model; route to a fund method or state the limitation |

The economic model and the legal wrapper are independent: a midstream C-corp uses midstream operating KPIs with `ordinary_company` tax treatment; an MLP uses the same KPIs with the partnership tax route.

### D7. Cash attribution (`cash_attribution`, issuer level)

`wholly_owned`, `material_minorities` (minority holders take a material share of subsidiary cash) or `material_jv_associates` (material cash arrives only as dividends from joint ventures/associates). The latter two require the attributable share, the actual cash received from those entities and, for `material_jv_associates`, the `holding_company` overlay or model so that equity-accounted profit is never treated as parent cash.

`material_jv_associates` also requires `cash_flow_model.associate_cash_conversion`: at least three bridge years of equity-accounted share of profit and dividends received from associates/JVs, the conversion each year (`same_year`, or `prior_year_profit` when associates pay out of last year's earnings), the multi-year aggregate, and the conversion each forecast scenario assumes. Choose the timing deliberately: associates that pay out of last year's earnings (most listed Chinese associates pay mid-year on the prior year) need `prior_year_profit`, otherwise a year of falling profit looks like a jump in conversion. Base may not exceed the aggregate and no scenario may exceed the best historical year unless `above_history_evidence` gives the specific evidence (such as a new associate payout policy) with `source_refs` drawn from the report's sources; one good year is not a trend. The validator recomputes every ratio, and the report prints the table in Chapter 6.

## 3. Rules Triggered Across Dimensions

### 3.1 Finite-life assets

For each asset in `finite_life_assets` record name, end year, share of operating cash, extension or compensation evidence (or null) and residual/terminal treatment. Do not merge assets with materially different end dates into one entry dated at the latest expiry. Split them when the filings allow; when they do not, record `earliest_end_year` and the valuation runs the whole entry only to that year, with the later-expiry case shown as a sensitivity. Value each asset over its remaining life; an expiry without evidenced extension removes that asset's cash after the end year, not the company's. In the growth route this is done in the terminal value through `growth_valuation.terminal_finite_assets` (`buy-zone.md` Section 6.3); the validator rejects a growth valuation that only lowers the perpetual growth rate. Show the share of operating cash expiring within ten years and the replacement investment needed to hold distributions flat. Test the dividend for the year after each material expiry.

### 3.2 Balance-sheet spread businesses

Use earnings/capital proxies, not OCF. Mandatory stresses: funding cost and availability (deposits, repo, unsecured), credit losses, rate path, book value per share and regulatory or statutory capital. A dividend maintained while book value per share falls is presumed to include capital return until disproved.

### 3.2A Mixed balance sheets and contradictory dimensions

The dominant segment chooses the primary cash model, but it does not get to hide the others. When the segments on the other side of the spread/non-spread line together reach 20% of cash (several small finance arms add up), each of them (an industrial group with a finance arm, an insurer with an operating business) needs the `holding_company` model or overlay, so segment cash is added up at the parent, and a `capital_bridge` on that segment: its own cash or capital generation, the regulatory or solvency constraint, and how cash reaches the parent. Dimensions must also agree with each other: `spread_income` requires `balance_sheet_spread`, and `commodity_linked` cash cannot be classed `stable`. `scripts/schema3_checks.py` enforces both.

### 3.3 US publicly traded partnerships (`us_publicly_traded_partnership`)

Model distribution cash and exit cash separately; see `withholding-notes.md`. Record `tax_route.distribution_regime: us_1446a`, `tax_route.exit_withholding_rate` (normally 0.10 of gross amount realized unless a documented exception applies) and keep potential refunds out of spendable cash. The exit withholding enters the total-return and exit-cash calculation even when the economic gain is smaller or negative.

### 3.4 Cyclical segments

Normalize the dividend from mid-cycle segment cash over `cycle_window`; show trough-year coverage. Variable payout policies (percentage of earnings or cash) produce variable dividends: a normalized N must come from mid-cycle cash × policy, not the latest payment.

## 4. Choosing Industry KPIs Without a Whitelist

Record at least three `kpis`, each with `why_causal`: how the KPI moves revenue, margin, cash or capital. Start from the triggered analysis above, then use `industry-analysis.md` quick-reference rows when one fits. A KPI must explain most of the historical change in segment cash in Chapter 5; if it does not, choose another.

## 5. Worked Classifications (illustrative)

| Issuer | Segment profile(s) | Wrapper / attribution | What the profile forces |
|---|---|---|---|
| HSBC (0005) | spread_income · perpetual · rate_cycle · balance_sheet_spread · asset_light | ordinary_company · wholly_owned (holding_parent overlay for subsidiary remittance) | Bank capital proxy, CET1/payout limits, rate-path and credit-loss stress |
| COSCO Shipping Holdings (1919) | container: commodity_linked (freight) · finite_assets (vessels) · supply_cycle · operating · maintenance_heavy; terminals: volume_times_price · finite_assets (concessions) · demand_cycle · operating | ordinary_company · material_jv_associates | Full freight-cycle normalization, no peak annualization, vessel/concession schedule, JV cash received |
| China Merchants Port (0144) | volume_times_price · finite_assets (concessions) · demand_cycle · operating · growth_heavy | holding_parent · material_jv_associates | Concession-level remaining life, associate dividends versus equity-accounted profit, parent cash |
| Chevron (CVX) | upstream: commodity_linked · finite_assets (reserves) · commodity_cycle · operating · maintenance_heavy; downstream: volume_times_price · perpetual · demand_cycle · operating | ordinary_company · wholly_owned | Mid-cycle price deck, reserve life and replacement capex, low-price coverage |
| Toll-road company | regulated_or_contracted · finite_assets (concessions) · stable · operating · maintenance_heavy | ordinary_company · wholly_owned | Per-road remaining life plus new projects; not `finite_life_harvest` unless the company is in run-off |
| Mortgage REIT | spread_income · perpetual · rate_cycle · balance_sheet_spread | reit | EAD coverage, book value, repo and margin-call stress |
| MLP pipeline | regulated_or_contracted · perpetual · stable · operating · growth_heavy | us_publicly_traded_partnership | DCF coverage after self-funded growth, §1446(a)/(f) cash route |

Classifications are research judgments for each report date; re-check against current filings.
