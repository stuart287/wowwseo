# Competitor Audit Source Pack Guide

Use this guide when working with local competitor audit source packs.

## Standard Source Pack Shape

A strong Woww competitor audit pack can include:

- Completed competitor audit report DOCX: report structure, tone, section order, explanation style, and recommendation density.
- Choosing Competitors workbook: final competitor list, selection source, notes, and raw/summary Ahrefs batch-analysis data.
- Competitor Analysis workbook: main comparison sheet with rows for business, content, SEO, backlinks, local/Google Business Profile, social, and opportunities.
- Backlinks workbook: backlink exports, referring-page data, URL/domain metrics, linked pages, anchors, and unique-anchor summaries.
- Referring domains workbook: referring-domain exports, spam flags, DR, dofollow domains, traffic, keywords, links to target, new/lost links, and sometimes backlink value estimates.
- Link Intersect workbook: domains linking to competitors but not the client, with DR, traffic, intersect count, and competitor columns.
- Raw Ahrefs CSV folder, where present: batch analysis, backlinks, content gap, link intersect, refdomains, common domains, and common keywords exports.
- Competitor-specific compressed workbooks, where present: more detailed ranking or silo comparisons for selected competitors.

## Local Example Packs

### Competitor Audit - Paradise Games

Use this as a local example for gaming, lottery, casino, sportsbook, iGaming, and multi-product competitor audits.

Important files:

- `Competitor Audit - Paradise Games.docx`
- `Choosing Competitors - Paradise Games.xlsx`
- `Competitor Analysis - Paradise Games.xlsx`
- `Backlinks - Paradise Games.xlsx`
- `Referring domains - Paradise Games.xlsx`
- `Link Intersect - Paradise Games.xlsx`
- `Bahamas_iGaming_Competitor_Audit_Comprehensive.xlsx`
- `Island_Game_Competitor_Audit_Compressed.xlsx`
- `Island_Luck_Competitor_Audit_Compressed.xlsx`

Observed report pattern:

- Introduction.
- Key.
- Off Page SEO.
- Ahrefs definitions and metric explanation.
- Competitors and selection rationale.
- Backlinks.
- Google My Business / Google Business Profile.
- Detailed competitor analysis.
- Social media.
- Summary and conclusion.
- Areas for improvement under Off Page, Competitors, and Social Media.
- References and resources.

Observed source-data pattern:

- Choosing Competitors workbook includes final list, global raw batch data, global summary, and Bahamas raw data.
- Competitor Analysis workbook uses a main comparison sheet with categories as rows and Paradise Games plus competitors as columns.
- Branded volume and competitor-specific tabs may support narrative comments.
- Link Intersect workbook contains a relevant client-specific tab plus a leftover Baobest/template tab. Use the Paradise Games tab for client evidence and flag template leftovers.
- Referring domains workbook includes backlink-value calculation tabs with and without low-traffic domains.
- Compressed competitor audit workbooks include profile/baseline, casino silo, sports silo, content/guides, local/authority, summary, and action-plan sheets.

### Competitor Audit - Pikeland Property Group

Use this as a local example for local SEO, property, home-buyer, service-area, and lead-generation competitor audits.

Important files:

- `Competitor Audit - Pikeland Property Group.docx`
- `Choosing Competitors - Pikelands Property Group.xlsx`
- `Competitor Analysis - Pikelands Property Group.xlsx`
- `Backlinks - Pikelands Property Group.xlsx`
- `Referring domains - Pikelands Property Group.xlsx`
- `Link Intersect - Pikelands Property Group.xlsx`
- `CSVs/`

Observed report pattern:

- The completed report follows the same Woww competitor-audit structure as Paradise Games.
- It explicitly distinguishes key competitors, expanded competitors, and expanded lists with very large marketplaces removed where needed.
- This is useful when a large domain such as Zillow or Opendoor is a real SERP competitor but not the best operational benchmark.

Observed source-data pattern:

- Choosing Competitors workbook includes final list, raw US batch data, and summary data.
- Competitor Analysis workbook includes a keyword summary comparison plus the main comparison sheet.
- Link Intersect workbook includes first-30,000 and filtered tabs, plus a leftover Baobest/template tab. Use the filtered or client-specific tabs for evidence.
- CSVs folder contains raw Ahrefs exports for batch analysis, backlinks, content gap, link intersect, referring domains, common domains, and common keywords.
- Raw CSV exports may be UTF-16/tab-delimited. Detect encoding before parsing and do not assume comma-delimited UTF-8.

## Evidence Workflow

1. Inventory the pack.
   - Identify the completed report, competitor selection workbook, competitor analysis workbook, backlinks workbook, referring domains workbook, link intersect workbook, raw CSV folder, and competitor-specific workbooks.
   - Note client, domain, target market, audit date, product/service focus, and competitors covered.

2. Inspect workbook and CSV structure.
   - Read sheet names before loading data.
   - Identify header rows because some workbooks include template tabs, filtered tabs, summaries, or repeated headers.
   - For CSVs, detect encoding and delimiter. Ahrefs exports may be UTF-16 with tabs.
   - Preserve geography, competitor-list, and filtered/unfiltered splits where they affect interpretation.

3. Establish source of truth.
   - Use Choosing Competitors for competitor selection rationale.
   - Use Competitor Analysis for the main client-facing comparison.
   - Use raw Ahrefs CSVs and source workbooks for evidence behind the summary.
   - Use backlinks and referring-domain workbooks for authority and link quality conclusions.
   - Use Link Intersect for link prospects and acquisition routes.
   - Use completed reports for structure, tone, section order, and example density, not as a substitute for current source data.

4. Analyse by section.
   - Competitor selection: client-nominated, Woww-selected, Ahrefs, SERP, real-world, and excluded competitors.
   - Off-page SEO: DR, UR, Ahrefs Rank, backlinks, referring domains, dofollow links, DR/traffic quality, anchors, and spam/low-value patterns.
   - Link intersect: domains linking to competitors but not the client, acquisition route, relevance, quality, and priority.
   - Google Business Profile: presence, reviews, rating, photos, services/products, posts, branches, and NAP consistency.
   - Detailed competitor analysis: business model, content, blog/resources, service/category coverage, UX/conversion, social, paid/search, and visible trust signals.
   - Social media: presence, follower counts, recency, cadence, engagement, and content themes.

5. Write evidence-led recommendations.
   - Lead with the finding.
   - State the evidence source.
   - Explain why it matters.
   - Give a specific action.
   - Assign priority and acquisition/implementation route where useful.

## Link Intersect Triage

Prioritise domains that:

- Link to multiple competitors but not the client.
- Have real organic traffic and sensible DR.
- Are topically or locally relevant.
- Are directories, associations, suppliers, partners, publications, industry roundups, local organisations, sponsorship opportunities, or credible review/listing sites.
- Have a plausible acquisition route.

Deprioritise:

- Zero-traffic SEO shops, scraper sites, obvious spam, irrelevant foreign directories, expired domains, mass-generated sites, and unrelated high-DR domains.
- Template-leftover tabs from other clients.
- Prospects where the client cannot credibly qualify or be listed.

## Report Style Pattern

Completed Woww reports:

- Explain off-page SEO in plain language before comparing metrics.
- Define Ahrefs metrics briefly.
- State why each selected competitor matters.
- Use spreadsheet evidence without dumping every export into the narrative.
- Keep the client-facing recommendation story focused even when the spreadsheet includes many competitors.
- Finish with grouped areas for improvement under Off Page, Competitors, and Social Media.

## QA Checks

- Confirm every competitor has a stated inclusion reason.
- Confirm every metric, backlink example, and link prospect comes from the correct client pack.
- Do not reuse example findings across clients.
- Do not confuse real-world competitors with SEO competitors.
- Do not treat backlink totals as quality without DR, traffic, relevance, and spam checks.
- Do not recommend link prospects from template-leftover tabs.
- Flag encoding, filename, template, or source-data issues before relying on them.
- Make every recommendation specific enough for SEO, PR, local, social, or content owners to act on.
