# Report Archive Publishing Contract

Read this module when the user requests saving, repairing or publishing reports in `Alanjiao1988/Dividendreport`. Ordinary analysis stays in the conversation unless saving/publication is requested. Existing authorization for a defined archive repair covers its necessary index and README updates; do not ask for the same permission again. An archive repair does not authorize refreshing historical investment conclusions.

## Canonical Records and Paths

The archive's `reports/index.schema.json` is the machine-readable index contract. Its `reports/index.json` remains an array, distinct from this skill's analysis `schema.json`. Validate a new structured analysis with `scripts/validate_analysis.py` in the skill repository before publishing; legacy Markdown reports are not automatically schema-2.2 analyses.

- Required index fields: `as_of_date`, `ticker`, `company`, `exchange`, `path`, `summary`, `score`, `portfolio_role`, `published_at`. Preserve their meanings and types from the archive schema.
- `as_of_date` is the research information cutoff; `published_at` is a timezone-bearing publication timestamp. Do not replace either with the repair date.
- Prefer the report's declared publication metadata. When restoring historical metadata, record its provenance; if the only evidence is the first-add Git commit, identify that fallback explicitly. Disclose conflicting timestamps. A declared timestamp is not independently verified publication evidence.
- Canonical HK stock tickers use at least four digits plus `.HK`, preserving valid five-digit codes. Normalize numeric aliases consistently in directory names, metadata and links. Do not apply HK zero-padding to US, UK or other tickers.
- Store reports under `reports/<ticker>/<YYYY-MM-DD>-<company-slug>-<ticker>.md`. For new slugs, retain readable Unicode letters/numbers and join name segments with hyphens; avoid whitespace and punctuation that needs special URL handling. Existing valid paths need not be renamed solely for cosmetic consistency.
- Preserve balanced parentheses in valid legacy paths, or encode link destinations correctly. Test the parsed destination rather than declaring punctuation itself a broken link.

## Summaries and Version Chains

Keep `summary` to at most 600 Unicode characters on one line, with no Markdown table delimiter. Summarize the original conclusion and key qualification; do not copy the whole analysis or add new market claims.

Recover missing or damaged prices, scores and roles from the original report or verifiable Git history. Never fill digits from memory or current market prices. For repaired or rewritten numeric summaries, retain the archive's `summary_evidence` records linking values to source excerpts. If the source is internally contradictory, disclose the conflict and omit the disputed number until it can be resolved; do not silently select the more favourable figure.

For each ticker, a newer report's `supersedes` points to the immediately prior report under the archive's documented date ordering. The first report has no predecessor. No self-links, cycles, cross-ticker predecessors or missing targets are allowed. Keep older reports accessible; an updated index is not permission to erase them.

The root README and each ticker's README are views of the canonical index. Regenerate them together with the archive's `scripts/render_index.py`; changes to a path or summary must reach every relevant view. Restoring a missing ticker README is part of completing its index entry.

## Local Verification and Publication

Run in the report repository:

```text
python -X utf8 scripts/validate_archive.py
python -X utf8 -m unittest discover -s tests -v
```

Run `python -X utf8 scripts/render_index.py` after editing the index, then rerun the read-only validator. Its checks cover schema, paths, metadata, version chains, generated views and documented numeric evidence; they do not independently verify the original research's economic facts. Review affected summaries against their source text.

Publish only the requested repository/branch and authorized changes. Preserve other contributors' work. For a pull request, state which historical records were repaired, where restored values came from, and what validation ran. Verify remote files/commit and PR status after publishing. Use the established local validation process; this workflow does not require a hosted CI service.
