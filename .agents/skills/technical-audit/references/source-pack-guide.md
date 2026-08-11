# Technical Audit Source Pack Guide

Use this guide when working with local technical SEO audit source packs.

## Standard Source Pack Shape

A strong Woww technical audit pack can include:

- Completed technical audit report DOCX: report structure, tone, section order, table density, and recommendation style.
- URLs workbook: crawl inventory, status codes, sitemap inclusion, indexability, inlinks, depth, low-value pages, trailing slash variants, and indexable pages missing from sitemap.
- 301/302 redirects workbooks: redirected URLs, redirect destination, chain URLs/codes, loops, sitemap inclusion, and internal links pointing at redirected URLs.
- 404 workbooks: broken target URLs, internal link sources, anchors, image alt text, sitemap inclusion, organic traffic, and depth.
- Duplicate content workbook: duplicate groups, risk level, affected URLs, canonical evidence, and crawl examples.
- Internal links to HTTP workbook: HTTP target URLs, source pages, anchors, and HTTPS hygiene.
- Orphan pages workbook: indexable pages with no internal support and pages missing from sitemap.
- Current/proposed sitemap files: URL architecture, recommended URL/status, page type, category, and sitemap inclusion planning.
- PageSpeed/Lighthouse workbook: mobile/desktop performance summaries, Core Web Vitals, action items, and migration benchmarks.
- Migration notes/checklists: robots, noindex, canonical, redirects, sitemap, benchmarking, post-launch QA, and stakeholder tasks.

## Local Example Packs

### Technical Audit - Pikeland Property Group

Use this as a local example for a standard technical audit on a local/property/service-area website.

Important files:

- Technical Audit - Pikeland Property Group.docx
- URLs - Pikeland Property Group.xlsx
- 301 redirects - Pikeland Property Group.xlsx
- 404 errors - Pikeland Property Group.xlsx
- Pages with internal links to 302 redirects - Pikeland Property Group.xlsx
- Pages with internal links to 404 errors - Pikeland Property Group.xlsx
- Redirects & Redirect Chains - Pikeland Property Group.xlsx
- Duplicate content.xlsx
- Internal links to HTTP - Pikeland Property Group.xlsx
- Orphan pages - Pikeland Property Group.xlsx
- Current and Proposed Sitemap.xlsx

Observed source-data pattern:

- URLs workbook includes data, trailing-slash variants, low-value pages, orphan pages, indexable pages missing from sitemap, content-word analysis, and trailing-slash review sheets.
- Redirects and redirect chains workbook includes redirected URLs and links-to-redirects tabs.
- 404 workbook includes broken URL inventory plus internal link source tabs.
- Current and Proposed Sitemap workbook separates current architecture from recommended future sitemap rows.
- Duplicate content workbook uses risk level, duplicate risk, affected URLs, and crawl evidence fields.

### Technical Audit - Paradise Games

Use this as a local example for a technical audit with migration planning, sitemap cleanup, robots/noindex/canonical decisions, and PageSpeed migration benchmarking.

Important files:

- Paradise Games - Technical Audit.docx
- URLs - Paradise Games.xlsx
- 301 redirects - Paradise Games.xlsx
- 404 errors - Paradise Games.xlsx
- Pages with internal links to 302 redirects - PowerPlastics.xlsx
- Pages with internal links to 404 errors - Paradise Games.xlsx
- Redirects & Redirect Chains - Paradise Games.xlsx
- Internal links to HTTP - Paradise Games.xlsx
- Orphan pages - Paradise Games.xlsx
- PageSpeed Audit - Migration.xlsx
- Website Migration Checklist/Domain Migration Checklist.xlsx
- Notes - Migration.docx
- WIP - PG Games - Robots.txt.docx
- Provisional Sitemap Paradise Games.docx
- Sitemap - Same URLs.docx
- Paradise Games Sitemap - v2.0 Proposed.docx

Observed source-data pattern:

- URL workbook includes data, old crawl sheet, indexable pages missing from sitemap, low-value URLs, orphan pages, and trailing-slash sheets.
- Migration notes discuss subdomains, noindex handling, canonical tags for classic/sports subdomains, and URL cleanup.
- Robots draft lists disallowed areas and sitemap location.
- Sitemap drafts are XML-style DOCX files and should be treated as planning/proposed implementation assets.
- PageSpeed workbook includes overview and action-item sheets with migration performance context.
- Migration checklist includes phases, checklist, backlink benchmarking, performance benchmarking, and migration redirect tabs.
- One file is named as PowerPlastics but sits in the Paradise pack; verify internal sheet content before using it as Paradise-specific evidence and flag the filename mismatch.

## Evidence Workflow

1. Inventory the pack.
   - Run the inventory script for large folders.
   - Identify completed report, URL crawl, redirects, 404s, internal links to redirects/404s, duplicate content, HTTP links, orphan pages, sitemap docs, PageSpeed evidence, migration notes, robots drafts, and checklists.
   - Note client, domain, market, CMS, audit date, and whether the task is a standard audit, migration audit, sitemap review, or partial section.

2. Inspect workbook structure.
   - Read sheet names before loading data.
   - Identify header rows because some workbooks include template tabs, filtered tabs, summary tabs, or repeated headers.
   - Preserve source URL, target URL, redirect URL, canonical URL, status code, inlink, sitemap, indexability, and depth fields separately.

3. Establish source of truth.
   - Use crawl exports for status codes, indexability, redirects, broken URLs, internal links, sitemap inclusion, orphan pages, duplicate content, HTTP links, and crawl depth.
   - Use Google/Search Console/Analytics exports only when present for traffic, impressions, clicks, indexing, and device/performance context.
   - Use PageSpeed/Lighthouse workbooks for speed and Core Web Vitals context.
   - Use migration notes, robots drafts, sitemap drafts, and checklists as planning evidence, not crawl evidence.
   - Use completed reports for structure, tone, and example density, not as a substitute for current source data.

4. Analyse by section.
   - Domain properties: domain/TLD, age, SSL/HTTPS, preferred domain, trailing slashes.
   - Redirects and 404s: redirects, internal links to redirects, redirect chains, loops, broken URLs, internal links to 404s, and functioning 404 page.
   - Google properties: Analytics, Search Console, algorithm context, users, sources, devices, speed, engagement, impressions, clicks, CTR, and average position where available.
   - Technical SEO: low-value pages, robots/noindex, XML sitemap, duplicate content, canonicals, schema, mobile friendliness, speed, security, architecture, and depth.
   - CMS: CMS identification, SEO plugin setup, plugin risk, and implementation constraints when evidence exists.
   - Migration: benchmark current state, map redirects, clean URLs, update robots/noindex/canonicals, submit sitemap, check post-launch crawl/indexing, and monitor performance.

5. Write evidence-led recommendations.
   - Lead with the finding.
   - State the evidence source and count.
   - Explain why it matters.
   - Give a specific action.
   - Assign severity and likely owner when useful.

## Migration Handling

For migration audits:

- Separate current-state crawl issues from planned migration tasks.
- Verify redirect mappings before recommending launch.
- Preserve benchmark data for traffic, rankings, backlinks, PageSpeed, and indexation.
- Treat sitemap drafts as proposed architecture until implemented and crawled.
- Treat robots/noindex/canonical notes as implementation instructions that still need post-launch verification.
- Add post-launch QA: crawl new site, check redirects, check sitemap, check robots, check canonicals, check GSC indexing, monitor 404s, and compare analytics/ranking benchmarks.

## Report Style Pattern

Completed Woww reports:

- Use a table-of-contents opening.
- Include the green/orange/red/blue key.
- Group sections under Domain Properties, 301 Redirects and 404 Errors, Google Properties, Technical SEO, CMS, Summary and Conclusion, Areas for Improvement, and Appendices.
- Explain each technical concept briefly, then move to client-specific evidence and recommendations.
- Use representative examples for large issue sets rather than dumping every row into the narrative.

## QA Checks

- Confirm every count, status code, and example comes from the correct client pack.
- Do not reuse example findings across clients.
- Do not treat proposed sitemap/robots/migration docs as proof of implementation.
- Do not treat a planning note as current crawl evidence.
- Flag filename/client mismatches before relying on a file.
- Confirm normalized columns match source headers before relying on generated CSVs.
- Make every red/orange issue map to a concrete action.
