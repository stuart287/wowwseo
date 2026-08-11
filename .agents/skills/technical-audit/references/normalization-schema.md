# Technical Audit Normalization Schema

Use this schema when converting crawl and Google exports into a common review layer before writing findings.

For bundled local examples, read `source-pack-guide.md` and inspect `source-packs/`.

## Core Fields

- `source_file`: original file name.
- `sheet_name`: worksheet name for spreadsheet sources.
- `url`: canonical URL of the audited page or resource.
- `source_url`: page where a link or issue originates.
- `target_url`: destination URL for redirects, broken links, canonicals, or sitemap references.
- `redirect_url`: destination URL from redirect exports.
- `canonical_url`: canonical target from duplicate/canonical exports.
- `proposed_url`: proposed replacement URL from sitemap or migration planning files.
- `status_code`: HTTP status when available.
- `issue_type`: normalized issue label such as `redirect`, `broken_link`, `orphan_page`, `duplicate_content`, `http_internal_link`.
- `is_indexable`: whether the URL is indexable in the source crawl.
- `is_in_sitemap`: whether the URL appears in the XML sitemap or sitemap export.
- `depth`: crawl depth when available.
- `severity_hint`: optional early severity label from the export or analyst.
- `notes`: free-text context preserved from the source file.

## Common Header Aliases

- `url`: `url`, `address`, `page`, `final url`, `page url`
- `source_url`: `source`, `source url`, `from`, `origin url`
- `target_url`: `destination`, `target`, `redirect url`, `to`, `final destination`
- `redirect_url`: `redirect url`, `final redirect url`, `redirect destination`
- `canonical_url`: `canonical url`, `canonical`, `canonical target`
- `proposed_url`: `proposed url`, `recommended url`, `recommended_url_or_status`, `proposed_url`
- `status_code`: `status code`, `status`, `http status`
- `is_indexable`: `is indexable page`, `indexable`, `is indexable`
- `is_in_sitemap`: `is in sitemap`, `in sitemap`, `seo_sitemap_status`
- `depth`: `depth`, `crawl depth`
- `notes`: `notes`, `comment`, `comments`, `details`

## Mapping Rules

1. Preserve the original file name in every normalized row.
2. Keep source and target URLs separate when an export provides both.
3. Do not force-fit unrelated columns into the schema; leave them unmapped and note the gap.
4. When multiple candidate headers exist, prefer the most specific match.
5. If a file has no clear URL column, treat it as review-only input and flag it for manual handling.
6. Treat proposed sitemap, robots, migration notes, and checklist files as planning rows unless they are confirmed by crawl/live evidence.
7. Preserve filename/client mismatches in `notes` rather than silently normalizing them away.

## Output

The normalization script should produce:

- `normalized_rows.csv`: one row per mapped record.
- `unmapped_files.csv`: files that could not be mapped confidently.
