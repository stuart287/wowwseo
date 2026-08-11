---
name: technical-audit
description: Use when preparing, analysing, writing, or reviewing a Woww-style technical SEO audit using crawl exports, Google Analytics/Search Console data, Lighthouse/PageSpeed evidence, CMS checks, domain checks, redirects, 404s, indexation, structured data, mobile friendliness, security, and final DOCX/report recommendations.
---

# Technical SEO Audit

Use this skill to complete a technical SEO audit in the same style as the reference audits in:
`/Users/stuartmarsden/Documents/Auditing Reference Files/Technical Audit Reference Files`.

## Document and Data Handling

Use the bundled references in this order:

1. Read `references/README.md` to identify which local reference or source pack applies.
2. Read `references/source-pack-guide.md` when working from DOCX/XLSX source packs, migration files, sitemap drafts, PageSpeed workbooks, or completed Woww audit examples.
3. Read `references/report-structure.md` when drafting or checking an audit document.
4. Read `references/data-sources.md` when deciding which crawl exports, Google reports, migration docs, sitemap files, and live checks support each section.
5. Read `references/recommendation-style.md` when turning raw findings into client-facing wording.
6. Read `references/normalization-schema.md` when mapping crawl and Google export columns into the shared ingestion schema.

When handling spreadsheets and source files:
- Inspect workbook sheet names, header rows, filtered tabs, template tabs, and example rows before analysing.
- Treat crawl exports as the source of truth for status codes, indexability, redirects, broken URLs, internal links, sitemap inclusion, orphan pages, duplicate content, HTTP links, and depth.
- Treat migration notes, proposed sitemap docs, robots drafts, and checklists as planning/implementation evidence, not proof that the live site is fixed.
- Treat PageSpeed/Lighthouse workbooks as performance evidence and preserve mobile/desktop or migration benchmark context.
- Keep client evidence separate across all local source packs.
- Flag missing, stale, mismatched, duplicated, template-leftover, or suspicious source data before relying on it.

## Core Workflow

1. Confirm the client domain, target market, CMS, and available evidence files.
2. Inventory the audit folder before writing. Use `scripts/inventory_audit_sources.py <audit-folder>` when there are many `.xlsx`, `.csv`, `.docx`, `.pdf`, or `.html` files.
3. Normalize the available exports before writing findings. Use `scripts/normalize_audit_exports.py <audit-folder>` to map spreadsheet columns into the standard schema and generate review-ready CSV outputs.
4. Build findings from evidence first, then write recommendations. Do not guess counts, status codes, or affected URLs.
5. Use the Woww severity key throughout:
   - Green: done well or trivial improvement.
   - Orange: done poorly or room for improvement.
   - Red: detrimental to SEO or unimplemented.
   - Blue: recommendation.
6. Write each audit section in this order: short explanation, data collection sources, findings, recommendations.
7. Prioritise practical fixes over broad SEO theory. Recommendations should be clear enough for a developer, CMS editor, or SEO retainer team to act on.
8. End with a summary grouped by Domain, 301 Redirects and 404 Errors, Google, Technical SEO, and CMS.

## Reference Files

- Read `references/README.md` first when selecting bundled local references.
- Read `references/source-pack-guide.md` when using local source packs, migration files, sitemap drafts, PageSpeed workbooks, or completed audit DOCX examples.
- Read `references/report-structure.md` when drafting the audit document or checking whether sections are missing.
- Read `references/data-sources.md` when deciding which crawl exports, Google reports, and live checks support each section.
- Read `references/recommendation-style.md` when turning raw findings into client-facing wording.
- Read `references/normalization-schema.md` when mapping crawl and Google export columns into the shared ingestion schema.
- Use `references/source-packs/Technical Audit - Pikeland Property Group/` as the local standard technical audit example.
- Use `references/source-packs/Technical Audit - Paradise Games/` as the local technical plus migration audit example.

## Evidence Standards

- Cite the source file or live check used for every material finding.
- Pull representative examples for large issue sets instead of pasting every affected URL into the main report.
- Use totals, unique URL counts, source URL counts, and target URL counts where useful.
- Separate minor housekeeping from SEO-critical issues. A handful of intentional redirects is usually not urgent; indexable HTTP variants, broken internal links, redirect chains, duplicate indexable pages, and sitemap/indexation mismatches are higher priority.
- When data conflicts, call out the conflict and prefer the freshest crawl or primary Google source.

## Common Inputs

Expected crawl exports often include:

- `URLs - <Client>.xlsx`
- `301 redirects - <Client>.xlsx`
- `404 errors - <Client>.xlsx`
- `Pages with internal links to 301 redirects - <Client>.xlsx`
- `Pages with internal links to 404 errors - <Client>.xlsx`
- `Redirect Chains - <Client>.xlsx`
- `Duplicate content.xlsx`
- `Internal links to HTTP - <Client>.xlsx`
- `Orphan pages - <Client>.xlsx`
- Google Search Console indexing exports
- Lighthouse, PageSpeed, or mobile friendliness reports

Older `.xls` files are not normalized by the helper scripts. Convert them to `.xlsx` or `.csv` before running the ingestion step.

## Output Expectations

For a full audit, produce a report-ready draft with:

- A clear table-of-contents style outline.
- Findings and recommendations for every core section.
- Client-specific counts and examples from the provided evidence.
- A concise final "Areas for Improvement" summary.
- An appendix list of source files, tools, and checks used.

For a partial request, answer only the requested section but keep the same evidence-first style.

## Commands

```bash
python3 .agents/skills/technical-audit/scripts/inventory_audit_sources.py /path/to/audit-folder
python3 .agents/skills/technical-audit/scripts/normalize_audit_exports.py /path/to/audit-folder
```

## QA

- Confirm the inventory output matches the actual source files in the audit folder.
- Confirm normalized columns match the source headers before relying on the generated CSVs.
- Flag files that could not be mapped cleanly instead of forcing them into the wrong schema.
- Treat unsupported `.xls` files as a data-prep blocker until they are converted.
