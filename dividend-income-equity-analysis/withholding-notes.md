# Withholding Notes for Dividend Research

This file is the single source of truth for withholding assumptions in this skill. Other files should reference this file instead of repeating the same rules.

## Priority Rule

Use this order when estimating net dividend yield:

1. Actual broker cash statement for the same investor and same holding channel.
2. Company dividend announcement and tax note.
3. Legal domicile, listing structure, and issuer type.
4. Market-level default assumption.

Broker-observed withholding overrides theory. If IBKR or another broker cash statement shows withholding on a stock, future net-yield calculations should use the observed rate unless later evidence shows a change.

## Default Guide

- HK incorporated company: usually no local dividend withholding on ordinary dividends. Confirm issuer domicile and announcement.
- PRC H-share: usually mainland withholding applies. Many dividend announcements show 10% for HK individual holders. Verify issuer announcement and holding channel.
- Red-chip or mainland-controlled HK-listed issuer: do not assume zero withholding only because it trades in Hong Kong. Check domicile, profit source, dividend announcement, HKSCC or custodian wording, and broker cash statement.
- PRC-source dividend risk: if the issuer is controlled by a mainland parent, has material mainland-source profits, or has prior broker-observed withholding, mark the withholding basis as broker_observed or company_announcement where possible; otherwise mark as uncertain.
- HK REIT: for HK individual holders, distributions are often received without local withholding, but verify trust-level announcement, distribution composition, and broker handling.
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

## Required Output Fields

Every analysis must show:

- Withholding rate.
- Withholding basis: broker_observed, company_announcement, legal_structure, market_default, or unknown.
- Broker-observed withholding: Yes / No / Unknown.
- Evidence: broker record, company announcement, legal structure, or default assumption.

Always state uncertainty and use official announcements when available.
