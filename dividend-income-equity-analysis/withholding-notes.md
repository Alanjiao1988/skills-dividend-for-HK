# Withholding Notes for Dividend Research

This file is the single source of truth for withholding assumptions in this skill. Other files should reference this file instead of repeating the same rules.

## Priority Rule

Use this order when estimating net dividend yield:

1. Actual broker cash statement for the same investor and same holding channel.
2. Company dividend announcement and tax note.
3. Legal domicile, listing structure, and issuer type.
4. Market-level default assumption.

Broker-observed withholding overrides theory only when the broker record is a true dividend record.

Before registering an observed withholding rate, confirm the broker cash statement line is a dividend, not a payment in lieu, manufactured dividend, stock-loan substitute payment, or other securities-lending substitute payment.

Payment-in-lieu records do not constitute withholding observations. They show that cash was received for that event, but they may bypass or distort issuer-level dividend withholding. Use PIL lines only as cash-flow evidence, not as withholding-rate evidence.

If broker records include both normal dividend lines and PIL lines for the same issuer, calculate withholding treatment from the normal dividend line where available and separately disclose PIL treatment.

## Scrip Dividend and DRIP Treatment

A scrip dividend, elective share distribution, stock dividend, or DRIP is not automatically equivalent to a cash dividend for investor cash-income analysis.

Required checks:

- Whether the issuer offers cash, shares, or both.
- Whether cash or shares is the default election.
- Scrip reference price, discount, and election deadline.
- Broker handling, fees, withholding, and fractional-share treatment.
- Whether tax or withholding is calculated on the cash equivalent, shares received, or another statutory amount.
- Historical participation rate and resulting company-level dilution.
- Whether buybacks offset the additional shares.

Default analysis rule:

- When an all-cash election is available, calculate headline gross and net cash yield using the all-cash election.
- Separately disclose the dilution from shareholders who elect scrip / DRIP and include expected dilution in forecast share count.
- If the investor elects shares, distinguish nominal DPS from actual cash income received.
- Do not assume cash-election and share-election tax treatment are identical without official or broker evidence.
- For mandatory stock dividends with no cash alternative, do not present the distribution as recurring cash income.

## Default Guide

- HK incorporated company: usually no local dividend withholding on ordinary dividends. Confirm issuer domicile and announcement.
- PRC H-share: usually mainland withholding applies. Many dividend announcements show 10% for HK individual holders. Verify issuer announcement and holding channel.
- Red-chip or mainland-controlled HK-listed issuer: do not assume zero withholding only because it trades in Hong Kong. Check domicile, profit source, dividend announcement, HKSCC or custodian wording, and broker cash statement.
- PRC-source dividend risk: if the issuer is controlled by a mainland parent, has material mainland-source profits, or has prior valid broker-observed withholding, mark the withholding basis as broker_observed or company_announcement where possible; otherwise mark as uncertain.
- Offshore shipowner or shipping issuer domiciled in Marshall Islands, Bermuda, Liberia, or similar offshore shipping jurisdictions: often favorable or 0% issuer-level withholding for non-resident holders, but verify legal domicile, source rules, broker treatment, and whether the cash entry is dividend or PIL.
- HK REIT: for HK individual holders, distributions are often received without local withholding, but verify trust-level announcement, distribution composition, broker handling, and DRIP treatment.
- US ordinary share: commonly 30% US withholding for HK residents. W-8BEN confirms non-US status but usually does not reduce ordinary US share dividend withholding for HK residents.
- ADR: check underlying issuer domicile, source-country withholding, depositary fee, and broker handling.
- REIT, BDC, MLP, fund, trust, and partnership structures outside HK: analyze separately.
- UK and Singapore ordinary shares often have favorable withholding outcomes, but verify issuer structure and broker handling.
- Stock Connect boundary: this skill defaults to an HK resident using a normal broker. It does not analyze mainland personal investors using Stock Connect unless the user explicitly asks.

## User Observed Withholding Register

| Ticker | Company | Broker | Observed status | Default future treatment |
|---|---|---|---|---|
| 0941.HK | China Mobile | IBKR | withholding observed | Use observed withholding rate unless later evidence changes |
| 1919.HK | COSCO SHIPPING Holdings | IBKR | withholding observed | Use observed withholding rate unless later evidence changes |

Only add a new ticker to this register when the observed broker line is confirmed as a normal dividend line. Do not add PIL-only observations as withholding evidence.

## Required Output Fields

Every analysis must show:

- Withholding rate.
- Withholding basis: broker_observed, company_announcement, legal_structure, market_default, or unknown.
- Broker-observed withholding: Yes / No / Unknown.
- Broker cash-line type when user statements are used: dividend, PIL, mixed, or unknown.
- Evidence: broker record, company announcement, legal structure, or default assumption.
- Scrip / DRIP availability: Yes / No / Unknown.
- Cash-election assumption used for yield calculation.
- Scrip / DRIP tax and dilution uncertainty when relevant.

Always state uncertainty and use official announcements when available.
