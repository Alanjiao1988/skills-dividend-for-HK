# Report Archive Publishing Contract

Apply `report-language.md`: report titles/body and index/README summaries use Chinese by default; retain metadata keys/enums, codes and official source names. Language changes must not alter historical conclusions or provenance.

Read this module when saving, repairing or publishing reports in `Alanjiao1988/Dividendreport`. Report requests default to one local self-contained HTML file under `output-template.md`; ordinary conversational clarifications stay in chat. The archive target remains `Alanjiao1988/Dividendreport`, but creating the local file is not a push. Publish only within the user's authorization and the application's outbound-confirmation policy. An archive repair does not authorize refreshing historical investment conclusions.

## Canonical Records and Paths

The archive's `reports/index.schema.json` is the machine-readable index contract. Its `reports/index.json` remains an array, distinct from this skill's analysis `schema.json`. Validate a new structured analysis with `scripts/validate_analysis.py` in this installed skill directory before publishing; legacy Markdown reports are not automatically current-schema analyses. Archive-specific scripts and files below belong to the separate report archive, not this installation.

- Required index fields: `as_of_date`, `ticker`, `company`, `exchange`, `path`, `summary`, `score`, `portfolio_role`, `published_at`, `ruleset`, `summary_provenance`, `summary_evidence`. Preserve their meanings and types from the archive schema.
- `ruleset` records the rules the report was produced under. New analyses from this skill use `ruleset: "3.0"` with `summary_provenance: "repaired_with_evidence"`. Before publishing, verify the archive schema and validator accept that ruleset; otherwise stop publication and identify the required archive migration. Never relabel a 3.0 report as 2.5, 2.4, 2.3 or 2.2 to bypass validation. Keep transcription evidence mandatory for new rulesets. Existing `2.5`, `2.4`, `2.3`, `2.2` and `pre-2.2` entries retain their original labels; do not retroactively call discretionary points audited rubric-2 scores. `pre-2.2` also predates the retired sector yield presets and five-year outlook requirement, so its yields, entry bands, roles and veto labels are historical records, not current results. Do not use historical no-entry frequency as threshold calibration. The archive's `MIGRATION.md` lists the historical differences.
- `summary_provenance` is `original_unverified` or `repaired_with_evidence`. The first keeps an author's original summary text and may carry an empty `summary_evidence`; that is a recorded exemption, not a verification claim. Never backfill evidence by matching a summary number to whatever report line happens to contain it: an automated match attaches figures to unrelated lines, and fabricated evidence is worse than an empty array. Backfill only from a line you have read and confirmed states that quantity.
- Every archived report body carries a `dividend-report-meta` comment block whose `ticker`, `company`, `exchange`, `as_of_date`, `published_at` and `ruleset` match the index, and whose `supersedes` is present with the same value when the index has one and absent when it does not. The block is required: without it a report silently skips every metadata cross-check.
- `as_of_date` is the research information cutoff; `published_at` is a timezone-bearing publication timestamp. Do not replace either with the repair date.
- Prefer the report's declared publication metadata. When restoring historical metadata, record its provenance; if the only evidence is the first-add Git commit, identify that fallback explicitly. Disclose conflicting timestamps. A declared timestamp is not independently verified publication evidence.
- Canonical HK stock tickers use at least four digits plus `.HK`, preserving valid five-digit codes. Normalize numeric aliases consistently in directory names, metadata and links. Do not apply HK zero-padding to US, UK or other tickers.
- New HTML reports use `reports/<ticker>/<YYYY-MM-DD>-<company-slug>-<ticker>.html` only after the compatibility gate below passes. Preserve existing `.md` report paths and historical records; do not bulk-convert or rename them. For new slugs, retain readable Unicode letters/numbers and join name segments with hyphens; avoid whitespace and punctuation that needs special URL handling. Existing valid paths need not be renamed solely for cosmetic consistency.
- Preserve balanced parentheses in valid legacy paths, or encode link destinations correctly. Test the parsed destination rather than declaring punctuation itself a broken link.

## Summaries and Version Chains

Keep `summary` to at most 600 Unicode characters on one line, with no Markdown table delimiter. Summarize the original conclusion and key qualification; do not copy the whole analysis or add new market claims.

Distinguish quality /85 from the compatibility score /100. The archive's existing `score` field retains its combined /100 meaning; do not replace it with quality points, an assessed subtotal, a range midpoint or a lower bound. For 3.0, preserve the report's point/range, provisional status, Grade/Grade range and covered weight in the index summary. Use a range in `score` only if the archive's live contract supports that representation; otherwise identify the needed format migration rather than silently dropping the usable score or falsifying a scalar. Updating this skill does not itself update the archive schema.

A summary may include the current action and binding price/evidence condition, but a provisional score or conditional starter stage is not Strong Buy. Reading archive reports to improve the skill does not authorize re-scoring, relabelling or overwriting them.

Recover missing or damaged prices, scores and roles from the original report or verifiable Git history. Never fill digits from memory or current market prices. For repaired or rewritten numeric summaries, retain the archive's `summary_evidence` records linking values to source excerpts. If the source is internally contradictory, disclose the conflict and omit the disputed number until it can be resolved; do not silently select the more favourable figure.

For each ticker, a newer report's `supersedes` points to the immediately prior report under the archive's documented date ordering. The first report has no predecessor. No self-links, cycles, cross-ticker predecessors or missing targets are allowed. Keep older reports accessible; an updated index is not permission to erase them.

The root README and each ticker's README are views of the canonical index. Regenerate them together with the archive's `scripts/render_index.py`; changes to a path or summary must reach every relevant view. Restoring a missing ticker README is part of completing its index entry.

## Local Verification and Publication

Before publishing HTML, confirm the archive's index schema, validator and README renderer accept `.html` paths, the `dividend-report-meta` HTML comment, ruleset 3.0 and traceable summary evidence from the rendered report text. Verify their actual behavior; changing a filename extension is not a migration. If any part is Markdown-only or incompatible, keep the completed HTML locally, identify the blocking file/contract and ask for authorization before changing that separate repository. Do not bypass validation, mislabel HTML as `.md`, silently create an extra Markdown report or downgrade its ruleset.

The HTML file remains the complete reader-facing report, with styles/charts inline and metadata consistent with the index. Index/README updates are archive maintenance, not additional report deliverables. Preserve chapter/source anchors and transcription evidence when encoding HTML text or generating archive summaries.

Run in the report repository:

```text
python -X utf8 scripts/validate_archive.py
python -X utf8 -m unittest discover -s tests -v
```

Run `python -X utf8 scripts/render_index.py` after editing the index, then rerun the read-only validator. Its checks cover schema, paths, metadata, version chains, generated views and documented numeric evidence; they do not independently verify the original research's economic facts. Review affected summaries against their source text.

Publish only the requested repository/branch and authorized changes. Preserve other contributors' work. For a pull request, state which historical records were repaired, where restored values came from, and what validation ran. Verify remote files/commit and PR status after publishing. Use the established local validation process; this workflow does not require a hosted CI service.

GitHub's file page may show HTML source rather than render the report. Label file/download links honestly; do not claim a live website or enable GitHub Pages, GitHub Actions or another hosting service without separate authorization.
