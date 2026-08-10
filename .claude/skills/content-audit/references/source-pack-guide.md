# Content Audit Source Pack Guide

Use this guide when working with local content audit source packs.

## Standard Source Pack Shape

A strong Woww content audit pack can include:

- Completed audit report DOCX: report structure, tone, section order, examples, traffic-light usage, and recommendation style.
- Data folder: crawl exports for URLs, top folders, page titles, meta descriptions, OG/Twitter tags, H1s/H2s, images, content length, internal linking, anchor text, and external linking.
- Content Analysis workbook: page-level qualitative ratings for search intent, content depth, title/meta quality, heading quality, CTAs, trust signals, and recommendations.
- Keyword research folder: topic brackets with seed terms, overview, matching terms, questions, related terms, and SERP tabs where available.
- Existing keywords workbook: current rankings, branded/non-branded splits, country/market tabs, historical comparisons, and sometimes cannibalisation tabs.
- Keyword Cannibalisation workbook: URLs competing for the same keyword, traffic change, top keyword shifts, and consolidation signals.
- Keyword Intersect workbook: competitor domains, overlap summaries, missing keyword opportunities, and competitor gap evidence.
- Seed Term Brainstorming workbook: early keyword/category/theme ideation.
- Content strategy workbook, where present: downstream prioritisation and roadmap support after the audit identifies gaps.

## Local Example Packs

### Paradise Games - Content Audit

Use this as a local example for gaming, lottery, sportsbook, casino, and multi-product content audits.

Important files and folders:

- `Content Audit - Paradise Games.docx`
- `Data/`
- `Keyword Research Data/`
- `Paradise Games - Content Strategy.xlsx`

Observed report pattern:

- Introduction.
- Key / traffic-light interpretation.
- Keywords: existing keywords, keyword research, cannibalisation, traffic potential.
- On Page SEO: page titles, meta descriptions, OG/Twitter cards, H-tag structure, media/images/alt text.
- Links & Siloing: physical siloing, virtual siloing/internal linking, anchor text.
- On Page Content: correlation analysis, content length, content quality and search intent.
- Content Ideas: short-form evergreen, long-form articles, infographics, guest articles, list posts, how-to guides, roundups, optimisations and landing page ideas.
- Content promotion and outreach strategy.
- Summary and conclusion with areas for improvement.
- Appendices.

Observed source-data pattern:

- Data folder includes anchor text, content length, external linking, internal linking, OG/Twitter cards, top folders, URLs, H1s, images, metas, and titles.
- Keyword research brackets cover lotto results, lotto products, online casino, sportsbook, NBA betting, NFL betting, Premier League betting, casino providers, casino games, and competitors.
- Existing keywords workbook includes global, US, Bahamas, historical comparison, lost keywords, and cannibalisation-style sheets.
- Keyword Cannibalisation workbook includes traffic change, previous/current top keyword, and URL-level issue evidence.
- Keyword Intersect workbook includes competitor domains, overlap summary, intersect terms, and gap evidence.
- Content strategy workbook can be used after the audit to understand how findings become prioritised strategy rows.

### Content Audit - Pikeland Property Group

Use this as a local example for local SEO, property, service-area, lead-generation, and location-page content audits.

Important files and folders:

- `Content Audit - Pikeland Property Group.docx`
- `Data/`
- `Keyword Research/`

Observed report pattern:

- The completed report follows the same Woww content-audit structure as Paradise Games.
- Example pages include homepage, conversion page, location page, and blog post examples.
- The content ideas section separates short-form, long-form, list, how-to, roundup, landing page, and optimisation opportunities.

Observed source-data pattern:

- Data folder includes anchor text, content analysis, content length, external linking, H1s, H2s, internal linking, OG/Twitter cards, top folders, URLs, images, metas, and titles.
- Content Analysis workbook uses page-named sheets with columns such as Metric, Result, Additional comments, and Why this metric is important.
- Keyword research brackets cover locations, buyer services, as-is repairs, fast cash offers, property types/issues/situations, process actions, and cost/fees/net proceeds.
- Existing keywords, keyword cannibalisation, keyword intersect, and seed-term brainstorming workbooks support prioritised recommendations and content ideas.

## Evidence Workflow

1. Inventory the pack.
   - Identify the completed report, Data folder, keyword research folder, content analysis workbook, existing keyword workbook, cannibalisation workbook, intersect workbook, and strategy workbook if present.
   - Note the client, domain, market, audit date, and site sections covered.

2. Inspect workbook structure.
   - Read sheet names before loading data.
   - Identify header rows because some exports include repeated headers, filtered tabs, or example tabs.
   - Preserve market, product, folder, and keyword-bracket splits where they affect interpretation.

3. Establish source of truth.
   - Use crawl exports for URL counts, indexability, metadata, headings, images, links, status codes, and folder structure.
   - Use keyword research workbooks for opportunity validation, search demand, parent topics, questions, related terms, and SERP hints.
   - Use existing keyword workbooks for current rankings and current URL/topic fit.
   - Use cannibalisation workbooks for overlap and consolidation risk.
   - Use content analysis sheets for qualitative page examples, but validate sitewide conclusions against crawl and keyword data.
   - Use completed reports for structure, tone, section order, and example density, not as a substitute for current source data.

4. Analyse by section.
   - Keywords: existing rankings, keyword research, cannibalisation, traffic potential, topic gaps, and business fit.
   - On Page SEO: page titles, meta descriptions, OG/Twitter cards, H1/H2 structure, images, alt text, and media usefulness.
   - Links & Siloing: folder structure, internal links, orphan/low-inlink pages, anchor text, hub/support relationships, and external link quality.
   - On Page Content: correlation analysis, content length, search intent, content depth, trust signals, CTAs, freshness, and usefulness.
   - Content Ideas: short-form evergreen, long-form articles, infographics, guest articles, list posts, how-to guides, roundups, landing pages, and optimisations.
   - Promotion and outreach: link creator database, social promotion, PPC, partnerships, authority sites, and outreach when relevant.

5. Write evidence-led recommendations.
   - Lead with the finding.
   - State the evidence source.
   - Explain the SEO or business impact.
   - Give a specific action.
   - Assign severity/priority and likely owner when useful.

## Report Style Pattern

Completed Woww reports:

- Use a short introduction to define audit scope.
- Include a traffic-light key: green, orange, red, and blue recommendation.
- Use section-level findings supported by example URLs and tables.
- Avoid listing every issue from every export in the narrative.
- Move detailed evidence into appendices or source workbooks when necessary.
- Finish with grouped areas for improvement under Keywords, On Page SEO, Links, and Content.

## QA Checks

- Confirm every URL, count, and keyword comes from the correct client folder.
- Do not reuse example findings across clients.
- Do not recommend new content when an existing URL should be improved, consolidated, or internally linked.
- Do not use content length alone as the recommendation; identify missing information or intent gaps.
- Do not turn one qualitative content-analysis row into a sitewide conclusion without pattern evidence.
- Flag suspicious source data, stale exports, mismatched filenames, or copied template rows.
- Make every red/orange finding map to a concrete action.
