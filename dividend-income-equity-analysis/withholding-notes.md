# Withholding Notes for Dividend Research

This file is the single source of truth for withholding assumptions in this skill. Other files should reference this file instead of repeating the same rules.

Official sources below were checked on **2026-09-05**. Recheck the relevant law and the latest issuer announcement for each analysis; these are dated reference points, not permanent ticker tax rates.

## Investor and Holding-Channel Assumptions

When no investor profile is supplied, use a **clearly labelled research scenario**: Hong Kong tax-resident individual, holding ordinary shares through a normal brokerage account outside Stock Connect, with valid tax documentation. This is not a finding about the user's residence. An HK broker, HK address, citizenship, and tax residence are different facts.

Use the user's stated residence, entity type, holding channel, and distribution election when available. Record whether shares are directly registered to the individual or held through HKSCC / another corporate nominee. A normal brokerage account does not imply direct registration or a particular withholding rate. If these details change the conclusion, show supported alternatives and mark the unresolved field `Unknown`; do not silently apply the HK scenario to a mainland resident, US taxpayer, company, partnership, or Stock Connect investor.

`Net yield` in this skill means **cash dividend yield after investor-level withholding, before other personal taxes and before fees unless explicitly deducted**. It is not automatically the investor's final worldwide after-tax return. Applicable residence-country tax, reclaim, credit, or special taxpayer status must be shown separately when known. Do not count a possible refund as immediate spendable income.

## Separate Tax Layers

Keep these layers distinct:

1. Tax on operating-company profits and remittances between subsidiaries and the listed parent: these affect distributable cash and coverage. Do not deduct them again from an already announced shareholder DPS.
2. Tax withheld when the listed issuer pays a registered holder or nominee: this may reduce cash reaching the beneficial investor, including when its legal label is enterprise income tax.
3. The beneficial investor's own tax liability, treaty relief, broker charges, and later refunds: these may differ from the initial withholding.

Mainland control or mainland operating profits alone do not establish shareholder-level PRC withholding. Check the listed issuer's tax residence, dividend source rules, registered-holder category, and announcement. Equally, HK incorporation alone does not establish a zero deduction through a nominee. Hong Kong IRD distinguishes taxation of the paying company's profits from tax on the dividend itself. [IRD DIPN 44, paragraphs 85-88](https://www.ird.gov.hk/eng/pdf/dipn44.pdf)

## Evidence and Reconciliation Rule

For **cash actually received**, start with the same investor's reconciled broker event. Match ticker / ISIN, share class, eligible quantity, gross entitlement, payment date, currency, dividend line, tax debit, charges, refunds, and corrections. Deduct fees separately; `1 - net cash / gross dividend` is not a withholding rate when fees or FX are mixed into net cash.

For **a declared or future dividend**, use this order:

1. Current applicable tax rules and issuer tax announcement matched to investor type and the actual custody / registration chain.
2. Current custodian or broker notice for that event, including documented relief or nominee treatment.
3. Prior reconciled ordinary-dividend events for the same investor and channel, as corroboration rather than a guarantee.
4. Legal-structure or market assumptions, explicitly labelled; use `unknown` when applicable treatment cannot be established.

A historical broker outcome does not override current law or a new announcement, and law alone may not explain the broker's initial cash deduction. Show an unresolved difference and the resulting cash-yield range instead of choosing whichever rate makes yield more attractive. Reconcile recoveries separately from initial withholding and state timing and recoverability.

### Payment in Lieu (PIL)

Confirm whether a statement line is a normal dividend, PIL / manufactured dividend / securities-lending substitute, or mixed. A PIL is evidence of cash and any withholding **on that substitute-payment event**, but cannot establish the ordinary dividend's tax treatment, exemption, or future rate. Separate ordinary and substitute portions when both occur.

Do not describe PIL as tax-free or as bypassing issuer tax. IBKR distinguishes PIL from ordinary dividends when shares are lent or pledged, and US dividend-equivalent rules can themselves impose withholding on substitute payments. Apply the relevant jurisdiction and investor rules, not US taxpayer examples to every holder. [IBKR PIL explanation](https://www.interactivebrokers.com/campus/glossary-terms/payment-in-lieu-of-dividends/), [IRS Publication 515, Dividend Equivalents](https://www.irs.gov/publications/p515)

## Default Guide: Conditional, Not Ticker-Wide Rates

| Structure | Starting point and required check |
|---|---|
| HK tax-resident ordinary company | Ordinary dividends generally have no Hong Kong local dividend tax. Verify issuer tax residence and any non-HK source or nominee deduction; HK listing or incorporation alone is insufficient. [IRD DIPN 44, paragraph 86](https://www.ird.gov.hk/eng/pdf/dipn44.pdf) |
| PRC H-share | Establish issuer tax residence, individual versus non-resident enterprise registration, nominee chain, and applicable treaty / announcement. A 10% case may apply, but is not a universal rate for all investors or channels. The Mainland-HK arrangement distinguishes qualifying corporate owners from other recipients, subject to applicable conditions. [IRD treaty rates](https://www.ird.gov.hk/eng/tax/dta_rates.htm), [IRD notes](https://www.ird.gov.hk/eng/tax/dta_notes.htm) |
| Red-chip / mainland-controlled offshore issuer | Check whether the listed entity is treated as a PRC tax-resident enterprise and what the dividend notice requires. Do not infer shareholder withholding solely from the parent's nationality or mainland profit share. |
| US ordinary corporation | Under the default HK individual scenario, ordinary US-source dividends commonly face 30% withholding absent an applicable exception. W-8BEN documents status and valid treaty claims; it does not itself create a reduced rate. The US-China treaty does not apply to Hong Kong. [IRS treaty claims](https://www.irs.gov/individuals/international-taxpayers/claiming-tax-treaty-benefits), [IRS Publication 901](https://www.irs.gov/publications/p901) |
| UK ordinary dividend / UK REIT | Distinguish ordinary dividends, normally paid without UK income-tax withholding, from REIT property income distributions, which have separate deduction and possible relief rules. [HMRC UK-REIT notes](https://assets.publishing.service.gov.uk/media/672346a93758e4604742aa51/uk-reit-dt-individual-notes.pdf), [HMRC distribution rules](https://www.gov.uk/hmrc-internal-manuals/investment-funds/ifm28005) |
| Singapore ordinary company | One-tier dividends from Singapore-resident companies are generally exempt for shareholders. SG listing alone does not establish this treatment; verify residence, one-tier status, and distribution type. [IRAS dividends](https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/what-is-taxable-what-is-not/dividends) |
| Offshore shipping issuer | Obtain current issuer tax disclosure for the actual domicile and payment. Do not assign zero withholding from a Marshall Islands, Bermuda, or Liberia label alone. Check source, distribution classification, broker deductions, and PIL separately. |
| ADR / depositary receipt | Check underlying issuer domicile, source-country tax, depositary ratio, fee per receipt, custody chain, and cash currency. US trading does not by itself make the dividend US-source. |
| HK REIT, other REIT, BDC, MLP, fund, trust, or partnership | Read the vehicle and distribution tax disclosures. Separate ordinary income, capital-gain distributions, return of capital, and non-cash distributions; no ordinary-company default applies automatically. |

### Worked Custody Example: China Mobile

China Mobile's 2026 interim dividend notice states that distributions to non-individual registered holders, including HKSCC and corporate nominees, suffer a 10% PRC enterprise-income-tax deduction. Natural persons entered directly on the shareholder register are treated differently: the company does not withhold PRC individual income tax on that dividend. Thus HK incorporation and an individual beneficial owner are insufficient to choose the cash withholding rate. Use the announcement as `company_announcement` evidence for the applicable channel; it does not verify an IBKR statement. [China Mobile announcement, 13 August 2026, page 3](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0813/2026081300300.pdf)

The same event is declared in RMB with an HKD cash option and specified exchange rate. Use the selected cash amount in the price currency and verify broker currency elections. Do not multiply an already converted HKD DPS by RMB/HKD again. [Updated dividend form, published 14 August 2026](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0814/2026081400069.pdf)

## Broker Observations: Evidence Must Travel with the Claim

No authenticated account statement is included in this repository. Earlier entries mentioning `0941.HK / China Mobile / IBKR` and `1919.HK / COSCO SHIPPING Holdings / IBKR` are **unverified historical leads**, not confirmed withholding observations or future-rate defaults. Do not output `Broker-observed withholding: Yes` from those entries.

Maintain an observation only in the current analysis or a user-supplied evidence record, with at least:

- investor tax-residence scenario, broker, holding channel, ticker / share class, and distribution date;
- ordinary dividend / PIL / mixed classification and eligible share quantity;
- gross entitlement, tax debit, fees, net cash, currency, and linked refund / reversal if any;
- effective observed rate, evidence reference, verification date, and scope of applicability.

Store a redacted reference, not an account number or private statement in a public skill. A prior ordinary-dividend observation supports that event and channel; revalidate before using it in a forecast. Absence of a supplied statement is `Unknown`, not evidence that no withholding occurred.

## Currency, Fees, and Uncertain Rates

- Express DPS and the unadjusted market price in the same currency and on the same share / receipt basis. Record dividend currency, cash currency, quote currency, conversion direction, FX date, source, and ADR ratio when applicable.
- For historical cash actually received, use actual paid amounts or documented payment-date conversion. For current-price comparison, label any common valuation-date FX translation as an estimate, not realized investor cash.
- Report withholding-only net yield separately from spendable yield after attributable broker / depositary fees and conversion costs. Fixed fees need a disclosed holding size; do not invent a universal fee percentage or assume unknown charges are zero.
- If no fee schedule or holding size is known, label the yield `before fees; fee impact unknown`. If the user sets a minimum on spendable income, an unbounded material fee cannot support a `Pass`.
- If multiple tax or FX outcomes are supported, calculate lower and upper net yields using identified scenarios. Explain each endpoint; do not invent a generic tax band. If no defensible bound exists, output `Unknown` instead of a point estimate.
- Keep withholding rates, fee rates, and FX separate. Do not deduct tax twice from a broker-net or issuer-net cash amount.

## Scrip Dividend and DRIP Treatment

A scrip dividend, elective share distribution, stock dividend, or DRIP is not automatically equivalent to cash available for spending.

Required checks:

- Whether cash, shares, or both are offered; default election, deadline, broker availability, charges, fractional-share treatment, and scrip reference price / discount.
- Whether withholding applies to a cash equivalent, shares, or another statutory amount; do not assume identical tax for cash and shares without evidence.
- Whether new shares are issued or existing market shares are purchased. Issuer scrip may dilute shareholders; a broker DRIP purchase of existing shares does not itself dilute the company.
- Expected participation, new-share issuance, and buyback cancellation when forecasting diluted share count; do not double-count dilution.

When an all-cash election is available, calculate headline cash yield using that election and disclose it. If the investor elects reinvestment, separate dividend and tax from the reinvestment purchase and actual cash retained. Mandatory stock distributions with no cash alternative are excluded from recurring cash-income yield. IBKR's DRIP guidance confirms that reinvestment can be net of tax and commission. [IBKR DRIP guidance](https://www.ibkrguides.com/kb/overview-of-drip.htm)

## Required Output Fields

Full Analysis must show these fields; Screen Mode may consolidate them in one linked evidence note and concise table fields:

- Investor residence / type / holding channel, and whether confirmed or assumed.
- Withholding rate or supported range; historical observed rate separately from declared / prospective treatment.
- Withholding basis: `broker_observed`, `company_announcement`, `legal_structure`, `market_default`, or `unknown`; attach current legal evidence where relevant.
- Broker-observed withholding: `Yes / No / Unknown`; `No` only when a reconciled relevant ordinary-dividend event shows zero deduction.
- Broker cash-line type when statements are used: `dividend`, `PIL`, `mixed`, or `unknown`.
- Evidence reference, dividend event / effective date, verification date, and unresolved conflicts.
- DPS / price currencies, FX convention and date, tax-exclusive fee assumptions, and fee-adjusted cash yield or `Unknown`.
- Scrip / DRIP availability: `Yes / No / Unknown`; cash-election assumption and tax, liquidity, or dilution uncertainty.

Always retain material uncertainty in yield and decisions. An assumed or historically observed rate is not a guarantee of future cash receipts.
