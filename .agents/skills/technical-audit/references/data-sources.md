# Technical Audit Data Sources

For bundled local examples, read `source-pack-guide.md` and inspect `source-packs/`.

## Crawl Exports

Use spreadsheet columns instead of manually scanning rows when possible.

### URLs

Common columns:

- `URL`
- `Title`
- `Content type`
- `HTTP status code`
- `Is in sitemap`
- `Is indexable page`
- `No. of all inlinks`
- `No. of href inlinks`
- `No. of redirect inlinks`
- `No. of canonical inlinks`
- `Depth`
- `Organic traffic`

Use for indexation, low-value pages, sitemap coverage, orphan-like patterns, depth, status code distribution, and architecture.

### 301 Redirects

Common columns:

- `URL`
- `HTTP status code`
- `Is in sitemap`
- `Is indexable page`
- `Is redirect loop`
- `Redirect URL`
- `Redirect chain URLs`
- `Redirect chain URLs codes`
- `No. of all inlinks`
- `No. of redirect inlinks`
- `First found at`

Use for redirect totals, redirect loops, redirects in sitemap, redirect chains, and URLs that internal links should point to directly.

### Pages With Internal Links to Redirects

Common columns:

- `Source URL`
- `Source HTTP status code`
- `Target URL`
- `Target HTTP status code`
- `Target no-crawl reason`
- `Anchor`
- `Alt attribute`
- `Is source noindex`
- `Is target canonical`
- `Is link self-referencing`

Use to identify internal links that should be updated to final destination URLs.

### 404 Errors

Common columns:

- `URL`
- `HTTP status code`
- `Organic traffic`
- `Depth`
- `Is in sitemap`
- `Is indexable page`
- `No. of all inlinks`
- `No. of href inlinks`
- `No. of canonical inlinks`
- `First found at`

Use for broken URL totals, 404s with traffic, 404s in sitemap, internally linked 404s, and priority examples.

### Pages With Internal Links to 404 Errors

Common columns:

- `Source URL`
- `Source HTTP status code`
- `Target URL`
- `Target HTTP status code`
- `Anchor`
- `Alt attribute`
- `Is source noindex`

Use to tell the client exactly where broken links live and what link text or image alt text is involved.

### Duplicate Content

Common columns:

- `URL`
- `Title`
- `Content type`
- `HTTP status code`
- `Is indexable page`
- `Canonical URL`
- `Canonical URL code`
- `Is canonical target canonical`
- `Is self-canonical`
- `No. of pages having the same content`
- `No. of all inlinks`

Use for duplicate body content, title duplication, non-canonical duplicates, canonical misconfiguration, and indexable duplicate groups.

### Internal Links to HTTP

Common columns:

- `Source URL`
- `Source HTTP status code`
- `Target URL`
- `Target HTTP status code`
- `Anchor`
- `Is source canonical`
- `Is source noindex`
- `Is target canonical`
- `Is target noindex`

Use to check whether HTTPS is forced and whether internal links still point to HTTP URLs.

### Orphan Pages

Common columns:

- `URL`
- `HTTP status code`
- `Is in sitemap`
- `No. of all inlinks`
- `No. of href inlinks`
- `No. of redirect inlinks`
- `No. of canonical inlinks`

Use to find pages discoverable in sitemap or external sources but not supported by internal linking.

### Current And Proposed Sitemap

Common columns:

- `level_1`
- `level_2`
- `level_3`
- `page_type`
- `page_name`
- `current_url`
- `proposed_url`
- `recommended_url_or_status`
- `seo_sitemap_status`
- `category`
- `notes`

Use for sitemap architecture, URL cleanup, recommended redirects/removals, new URL planning, and migration sitemap planning. Treat proposed sitemap files as planning evidence until implemented and crawled.

### PageSpeed Or Lighthouse

Common sections:

- Overview or score summary.
- Mobile and desktop scores.
- Core Web Vitals or Lighthouse metrics.
- LCP, FCP, CLS, INP/TBT, speed index, and server response time where available.
- Action items and notes.

Use for performance recommendations, migration benchmarking, and prioritising image, JavaScript, CSS, server, and template fixes.

### Migration Notes And Checklists

Common evidence:

- Domain/subdomain notes.
- Robots/noindex/canonical instructions.
- Redirect mapping or migration redirect tabs.
- Sitemap drafts.
- Backlink benchmarking.
- Performance benchmarking.
- Pre-launch and post-launch checklist items.

Use for migration planning and QA. Do not treat notes or checklists as proof that fixes are live.

## Google Sources

- GA4: users, new/returning users, countries, traffic sources, device split, engagement, speed where available.
- Google Search Console: impressions, clicks, average CTR, average position, indexing reports, sitemap status, mobile usability where available.
- GSC page indexing exports: `robots.txt`, `excluded by no-index tag`, `alternate page with proper canonical`, crawled/discovered not indexed, duplicate without user-selected canonical.

## Live Checks

- WHOIS or registrar lookup for domain age.
- Browser/curl checks for HTTP, HTTPS, www, non-www, and trailing slash variants.
- SSL checker or browser security panel.
- `robots.txt` and XML sitemap URLs.
- Google Rich Results Test or Schema validator.
- PageSpeed Insights or Lighthouse report.
- Safe Browsing, malware, or security-header checks where relevant.
- Manual CMS/plugin signals from source code, `/wp-admin`, generator tags, or known CMS paths.

## Local Source-Pack Patterns

Pikeland Property Group:
- Standard technical audit pack with URL crawl, redirects, 404s, internal links to redirects and 404s, duplicate content, internal HTTP links, orphan pages, redirect chains, and current/proposed sitemap workbook.
- Useful for local-service and property site audits.

Paradise Games:
- Technical audit plus migration pack with URL crawl, redirects, 404s, internal HTTP links, orphan pages, redirect chains, PageSpeed migration workbook, migration checklist, robots draft, migration notes, and sitemap drafts.
- Useful for gaming/iGaming, subdomain cleanup, migration planning, sitemap cleanup, noindex/canonical decisions, and post-launch QA.
- One internal-link-to-redirects file is named for PowerPlastics; verify the sheet content before treating it as Paradise evidence.

## Counting Guidance

- Count unique target URLs when describing how many broken or redirected URLs exist.
- Count source rows or source URLs when describing how many internal links need changing.
- For duplicated content, count duplicate groups and affected indexable URLs.
- For large exports, include the top examples by traffic, depth, sitemap inclusion, or volume of inlinks.
- For migration work, separate current crawl issue counts from planned redirect/sitemap/robots tasks.
