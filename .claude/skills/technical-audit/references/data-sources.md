# Technical Audit Data Sources

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

## Counting Guidance

- Count unique target URLs when describing how many broken or redirected URLs exist.
- Count source rows or source URLs when describing how many internal links need changing.
- For duplicated content, count duplicate groups and affected indexable URLs.
- For large exports, include the top examples by traffic, depth, sitemap inclusion, or volume of inlinks.
