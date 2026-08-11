# Woww Competitor Audit Method

## Purpose

Woww-style competitor audits compare the client against search and business competitors, with special attention to off-page SEO. The audit should help the client understand which competitors are winning, why they are visible, and which practical actions can close the gap.

The source examples use two layers:

- A spreadsheet with hundreds of data points and source tabs.
- A short Word-style narrative that explains the approach and summarizes the findings.

For bundled local examples, read `source-pack-guide.md` and inspect `source-packs/`.

## Source Pack Handling

Before analysing a source pack, identify:

- Completed report document.
- Choosing Competitors workbook.
- Competitor Analysis workbook.
- Backlinks workbook.
- Referring domains workbook.
- Link Intersect workbook.
- Raw Ahrefs CSV folder, if present.
- Competitor-specific compressed workbooks, if present.
- Client name, domain, geography, audit date, and product/service focus.

Use source evidence in this order:

1. Current source exports supplied by the user.
2. Cleaned comparison workbooks clearly derived from those exports.
3. Raw Ahrefs CSV/XLSX exports.
4. Completed audit report prose for structure and narrative style.
5. Live research, clearly dated.
6. Assumptions, clearly labelled.

If the report prose conflicts with source data, use the source data and flag the discrepancy.

When CSV files are present, detect encoding and delimiter before parsing. Ahrefs CSV exports may be UTF-16 and tab-delimited, despite using a CSV extension.

## Competitor Selection

Use a blended selection model:

- Client-nominated competitors: include when strategically important, even if they are not the strongest SEO competitors.
- Search competitors: domains ranking for target commercial and informational queries in the target geography.
- Ahrefs competitors: domains with keyword overlap, stronger DR, higher organic traffic, more ranking keywords, or stronger backlink profiles.
- Business-fit competitors: same geography, product/service category, buying intent, audience, and business model.

Do not choose competitors solely because they are famous or large. Explain when a selected SEO competitor differs from a real-world competitor.

Recommended fields for the `Choosing Competitors` workbook:

- Business Name
- URL
- Ecommerce or lead-gen
- Selection source: `By client`, `Woww`, `Client + Woww`, `SERP`, `Ahrefs`
- Notes explaining redirects, poor fit, special inclusion, or exclusion
- Ahrefs metrics from batch analysis: DR, Ahrefs Rank, organic keywords, top 3 keywords, top 10 keywords, backlinks, followed backlinks, dofollow referring domains

For large-market or local-service audits, keep separate:

- Key competitors for detailed comparison.
- Expanded competitor list.
- Expanded list with very large marketplaces or weak-fit domains removed.
- Real-world competitors that matter commercially but are weak SEO benchmarks.
- SEO competitors that dominate rankings but are not like-for-like businesses.

## Evidence Sources

Use these sources where available:

- Ahrefs Batch Analysis for high-level domain metrics.
- Ahrefs Site Explorer for backlinks, referring domains, top pages, anchors, organic keywords, and paid keywords.
- Ahrefs Link Intersect for domains linking to competitors but not the client.
- SERP checks for priority keywords and local-pack visibility.
- Google Business Profile checks for listing presence, reviews, photos, posts, services, locations, and completeness.
- Website review for blog/content cadence, service page coverage, product/category depth, resources, trust signals, and conversion routes.
- LinkedIn for employee count and company positioning when relevant.
- Social platforms for account presence, follower counts, cadence, engagement, and content themes.
- WHOIS/domain lookup or reliable SEO tools for domain age when needed.

If live web research is used, verify current pages and dates. If the user provides exports, prefer those over memory or stale notes.

## Spreadsheet Conventions

The main comparison sheet should have competitors as columns and audit dimensions as rows:

`Category | Item | Client | Competitor 1 | Competitor 2 | Competitor 3 | Competitor 4...`

Useful categories:

- Business
- Content
- Technical/UX observations, only where they affect competitive positioning
- Organic SEO
- Backlinks
- Local SEO
- Paid search
- Social media
- Opportunities

Keep raw exports or derived tabs separate:

- `Final List` or `Choosing Competitors`
- `raw data`
- `summary`
- `Referring Domains`
- `Backlinks`
- `Unique Anchor`
- `Link Intersect`
- `Organic Keywords Intersect`
- `Current Keyword Rankings`
- `Paid`
- `Top Pages`
- `Branded Volume`

Use consistent units and labels. Mark unknowns as `Not found` or `N/A`; do not leave important cells blank unless the blank means "not assessed".

If workbooks contain template-leftover tabs from another client, do not use those tabs as evidence. Note the mismatch and use the client-specific tabs only.

## Backlink And Referring Domain Review

Focus on quality, not just totals. Compare:

- Domain Rating distribution.
- Total referring domains.
- Dofollow referring domains.
- Total backlinks and followed backlinks.
- Domain traffic and keyword visibility of linking domains.
- Lost/new links where relevant.
- Anchor text quality and brand/naked URL/generic/commercial mix.
- Spam signals, low-traffic domains, obvious networks, irrelevant directories, and duplicated links.

Suggested rough value bands when estimating link equity:

- DR 70-100: very strong, but check traffic and relevance carefully.
- DR 40-70: strong link prospects.
- DR 30-40: moderate value.
- DR 10-30: lower value, still useful if relevant/local.
- DR 0-10: usually low value unless highly relevant.

Do not overstate link value from spammy high-DR domains with no traffic or obvious manipulation.

When a workbook includes backlink value estimates, treat them as rough prioritisation support only. Do not present calculated link value as exact commercial value unless the user explicitly asks for that model and its assumptions.

## Link Intersect Review

Prioritize domains that:

- Link to multiple competitors but not the client.
- Have meaningful DR and real organic traffic.
- Are locally or topically relevant.
- Look editorial, partner-based, directory-based, supplier/manufacturer-based, association-based, media-based, or resource-based.
- Can plausibly be acquired through outreach, listings, PR, sponsorship, supplier relationships, testimonials, or useful content.

Deprioritize obvious spam, expired domains, mass-generated pages, irrelevant foreign directories, and scraper sites.

For local-service audits, give extra weight to relevant local directories, chambers, BBB-style profiles, community organisations, regional publications, sponsorships, vendors, testimonials, and local resource pages.

For gaming/iGaming audits, separate mainstream SEO opportunities from compliance-sensitive, affiliate, casino, sportsbook, lottery, gaming-directory, and review-site opportunities. Flag legal or brand-risk review needs where relevant.

For each recommended opportunity, capture:

- Referring domain
- DR
- Traffic
- Which competitors are linked
- Why it matters
- Suggested acquisition route
- Priority

## Google Business Profile Review

Check whether each business has a visible Google Business Profile and compare:

- Profile completeness.
- Review count and average rating.
- Recency and quality of reviews.
- Photos and product/service details.
- Posts or updates.
- Branch/location coverage.
- NAP consistency where visible.

Recommendations should be practical: claim/verify listings, add services, improve photos, request reviews, respond to reviews, publish posts, and standardize branch details.

## Social And Content Review

Do not reduce social media to follower counts. Compare:

- Platform presence and relevance to the industry.
- Posting frequency and recency.
- Engagement relative to audience size.
- Content themes: educational, product-led, trust-building, offers, community, case studies.
- Whether content supports search demand and conversion.

For website content, compare:

- Blog/resource presence and freshness.
- Service/category page coverage.
- Product depth and buying information.
- FAQs, guides, case studies, galleries, calculators, downloads, or other useful assets.
- Internal linking to commercial pages.

## Completed Report Pattern

The local examples use a concise client-facing structure:

- Introduction.
- Key.
- Off Page SEO.
- Ahrefs definitions.
- Competitors and selection rationale.
- Backlinks.
- Google Business Profile / Google My Business.
- Detailed Competitor Analysis.
- Social Media.
- Summary and Conclusion.
- Areas for Improvement.
- References and resources.

The report should explain enough methodology for the client to trust the findings, but the detailed evidence should stay in the spreadsheet unless a table is needed to prove a pattern.

## Client Narrative Guidance

Keep the audit explanatory but decisive. Use short sections and avoid burying recommendations in tool jargon.

Good finding pattern:

`Observation -> Why it matters -> Evidence -> Recommendation`

Example:

`Competitor A has fewer backlinks overall but more relevant local referring domains. This matters because local and topical relevance can outperform raw backlink volume. Prioritize local directories, supplier pages, and association listings before broad link building.`

## Recommendation Checklist

Finish with prioritized actions. Cover the highest-relevance items from:

- Competitor selection caveat: explain the difference between SEO competitors and known business competitors.
- Backlink acquisition: link intersect prospects, industry directories, supplier/manufacturer listings, partner links, PR/news placements, associations, sponsorships.
- Link quality cleanup: monitor spam, ignore low-value noise, avoid risky paid links unless explicitly discussed.
- Content gaps: pages, guides, category coverage, FAQs, case studies, comparisons, top-pages opportunities.
- Local SEO: Google Business Profile improvements and review growth.
- Social/content support: cadence, channels, trust-building assets.
- Measurement: track DR/referring domains, target keyword rankings, organic traffic, local pack visibility, reviews, and acquired links.

## Quality Bar

Before finalizing:

- Every competitor has a stated reason for inclusion.
- Every major recommendation has supporting evidence.
- The audit distinguishes volume from quality.
- The document uses client-friendly language.
- Spreadsheet labels are consistent and understandable.
- Unknown data is labelled, not silently omitted.
- The final narrative tells the client what to do next, not just who is ahead.
- Template-leftover tabs are ignored or explicitly flagged.
- Raw CSV encoding/delimiter issues have not corrupted headers or columns.
