# Technical Audit Normalization Schema

Use this schema when converting crawl and Google exports into a common review layer before writing findings.

## Core Fields

- `source_file`: original file name.
- `sheet_name`: worksheet name for spreadsheet sources.
- `url`: canonical URL of the audited page or resource.
- `source_url`: page where a link or issue originates.
- `target_url`: destination URL for redirects, broken links, canonicals, or sitemap references.
- `status_code`: HTTP status when available.
- `issue_type`: normalized issue label such as `redirect`, `broken_link`, `orphan_page`, `duplicate_content`, `http_internal_link`.
- `severity_hint`: optional early severity label from the export or analyst.
- `notes`: free-text context preserved from the source file.

## Common Header Aliases

- `url`: `url`, `address`, `page`, `final url`, `page url`
- `source_url`: `source`, `source url`, `from`, `origin url`
- `target_url`: `destination`, `target`, `redirect url`, `to`, `final destination`
- `status_code`: `status code`, `status`, `http status`
- `notes`: `notes`, `comment`, `comments`, `details`

## Mapping Rules

1. Preserve the original file name in every normalized row.
2. Keep source and target URLs separate when an export provides both.
3. Do not force-fit unrelated columns into the schema; leave them unmapped and note the gap.
4. When multiple candidate headers exist, prefer the most specific match.
5. If a file has no clear URL column, treat it as review-only input and flag it for manual handling.

## Output

The normalization script should produce:

- `normalized_rows.csv`: one row per mapped record.
- `unmapped_files.csv`: files that could not be mapped confidently.
