# Technical Audit Report Structure

Use this structure for Woww-style technical SEO audits.

For bundled local examples, read `source-pack-guide.md` and inspect `source-packs/`.

## Opening

- Table of Contents
- Key:
  - Green: done well or trivial room for improvement.
  - Orange: done poorly or room for improvement.
  - Red: current state is detrimental to overall SEO or completely unimplemented.
  - Blue: recommendation.
- Introduction:
  - Position the audit as the technical/sitewide component of SEO.
  - Explain that the report covers domain setup, Google properties, technical SEO, and CMS-specific issues.

## Domain Properties

1. Domain Name and TLD
   - Classify as branded, partial match, or exact match.
   - Check whether the TLD matches the business and target market.
2. Domain Age and Ownership
   - Use WHOIS or domain lookup evidence.
   - Note creation date and any ownership concerns.
3. SSL Certificate and HTTPS/HTTP Issues
   - Check active certificate, forced HTTPS, HTTP variants, and internal links to HTTP.
   - Use `Internal links to HTTP` exports where available.
4. Preferred Domain and Trailing Slashes
   - Test all four common variants: `http://domain`, `http://www.domain`, `https://domain`, `https://www.domain`.
   - Check whether all variants resolve to one preferred version.
   - Check trailing slash consistency and whether duplicate variants remain indexable.

## 301 Redirects and 404 Errors

1. 301 Redirects
   - Use `301 redirects`, `Redirect Chains`, and `Pages with internal links to 301 redirects`.
   - Distinguish intentional redirects from unnecessary internal links to redirected URLs.
   - Flag redirect chains, loops, redirects in sitemap, and menu links pointing through redirects.
2. 404 Errors
   - Use `404 errors` and `Pages with internal links to 404 errors`.
   - Separate broken internal links, sitemap 404s, and externally discovered dead pages.
   - Recommend link replacement, content restoration, removal, or 301 redirects based on intent and traffic.
3. Functioning 404 Page
   - Confirm the site returns a real 404 HTTP status.
   - Check whether the page is helpful, branded, and navigable.

## Google Properties

1. Analytics
   - Confirm GA4 setup, tracking, and access where evidence is available.
2. Search Console
   - Confirm property access, sitemap submission, indexing data, and major coverage issues.
3. Google Algorithm
   - Note whether recent known updates overlap with traffic changes if data is provided.
4. Google Data Analysis
   - Include Total Users, New vs Returning Users, Users by Country, Source Type, Mobile vs Desktop, Site Speed, Bounce Rate, Time Spent per Session, Total Impressions vs Clicks, and Average CTR vs Average Position when data is available.

## Technical SEO

1. Low Value Pages, Indexing, and Robots.txt
   - Use `URLs`, low value sheets, orphan page sheets, GSC indexing exports, robots.txt, and live checks.
   - Flag indexable low-value URLs, important noindexed pages, orphan pages, and indexable pages missing from sitemap.
2. XML Sitemap
   - Check sitemap availability, freshness, indexable URLs, 3xx/4xx URLs, and missing important pages.
3. Duplicate Content and Canonicalisation
   - Use `Duplicate content.xlsx` and canonical columns in crawl exports.
   - Flag duplicate indexable pages, non-self-canonical pages, canonical chains, canonical targets that are not indexable, and duplicate HTTP/HTTPS or slash variants.
4. Structured Data and Rich Results
   - Test representative page templates with Rich Results Test or Schema validator evidence.
   - Flag missing, invalid, or template-inconsistent schema.
5. Mobile Friendliness
   - Use mobile friendliness reports, PageSpeed mobile data, and manual checks.
6. Speed Test and Performance
   - Use Lighthouse/PageSpeed evidence.
   - Highlight Core Web Vitals, image weight, render-blocking resources, unused JS/CSS, server response time, and mobile vs desktop differences.
7. Security Check and Malware Scan
   - Check HTTPS, malware warnings, mixed content, unsafe resources, and security headers when available.
8. Website Structure and Depth
   - Use crawl depth, internal link counts, orphan pages, and navigation patterns.
   - Flag important pages too deep in the architecture or isolated from internal linking.

## Migration And Sitemap Planning

Add this as a dedicated section when the source pack includes migration notes, proposed sitemap files, redirect mapping, robots drafts, or migration checklists.

1. Current vs Proposed Sitemap
   - Compare current URLs, proposed URLs, page type, category, and recommended status.
   - Treat proposed sitemap files as planning evidence until implementation is crawled.
2. Redirect Mapping
   - Check old URLs, new destinations, chain risk, 404 risk, and backlink/traffic-sensitive URLs.
3. Robots, Noindex, and Canonicals
   - Separate live robots evidence from draft instructions.
   - For subdomains, recommend noindex/canonical handling only where it matches the migration plan and can be implemented on that host.
4. Migration Benchmarks
   - Preserve ranking, traffic, backlink, indexation, and performance baselines.
5. Post-Launch QA
   - Crawl the migrated site, verify redirects, submit sitemap, check robots, check canonical tags, monitor GSC indexing, monitor 404s, and compare performance/traffic benchmarks.

## Content Management System

1. General CMS
   - Identify CMS and any technical constraints visible from the site.
2. Yoast or SEO Plugin
   - For WordPress, check whether an SEO plugin is present and configured.
3. Plugins
   - Note outdated, excessive, or risky plugins only when evidence is available.

## Close

- Summary and Conclusion
- Areas for Improvement:
  - Domain
  - 301 Redirects and 404 Errors
  - Google
  - Technical SEO
  - CMS
- Appendix: references and resources
