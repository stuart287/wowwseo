---
name: content-strategy
description: Creates and reviews SEO content strategy plans, content idea backlogs, and strategy spreadsheet rows from client inputs, keyword research, Ahrefs SERP data, Google Search Console data, Surfer topic maps, and existing content audits. Use when asked to generate content ideas, populate a content strategy or ideation template, prioritise topics, classify funnel stage, distinguish new content from optimisations, or prepare strategy rows for review.
---

# Content Strategy

## Purpose

Create data-led SEO content strategies that turn client offerings, keyword research, SERP competitiveness, GSC performance, Ahrefs rankings, Surfer topical maps, and existing content into prioritised content ideas.

This skill is separate from `seo-content-writer`: use this skill to decide what should be created or optimised, why it matters, and how it should be prioritised. Use `seo-content-writer` only after an approved strategy item needs a full article or page draft.

Repository note: `Content Strategy Creator/` is a separate internal-link visualisation app. The content strategy skill's operating instructions, source documents, workbook templates, and examples live inside this skill folder under `references/`.

## Inputs

Required:
- Client/domain and target market or country.
- Business goals, core products/services, audience segments, and known priority pages.
- At least one source of opportunity data: keyword research, Ahrefs exports, GSC export, Surfer topical map, content audit, sitemap, or client topic list.

Recommended:
- Keyword research sheet with overview, matching terms, questions, related terms, and SERP exports.
- Content strategy template or existing strategy sheet.
- Current rankings and top-performing URLs from Ahrefs/GSC.
- Existing blog and landing page URLs for supporting content and internal linking.
- Competitor domains for content gap checks.

Stop and ask only when the missing input changes the strategic decision materially, such as no client/domain, no target market, no business goal, or no usable opportunity data. Otherwise proceed with caveats.

## Document and Data Handling

Use the bundled references in this order:

1. Read `references/README.md` to identify which reference file, template, or example applies to the task.
2. Read `references/content-strategy-source-pack.md` for the distilled rules from the uploaded source documents.
3. Read `references/content-strategy-framework.md` for the working strategy process.
4. Read `references/template-columns.md` when mapping outputs into workbook columns.
5. Open original files in `references/source-documents/`, `references/templates/`, or `references/examples/` only when the task needs source wording, exact workbook structure, examples, or spreadsheet-compatible output.

When handling spreadsheets:
- Inspect workbook sheet names, header rows, dropdown-style values, and existing example rows before mapping new data.
- Use the template workbook as the structure source; do not overwrite it.
- Use example workbooks to match level of detail, tone, priority logic, worklog rows, and how keyword/URL exports support strategy rows.
- Preserve formulas, hidden sheets, dropdowns, and formatting whenever editing or copying a workbook.
- Clearly label provisional rows when Ahrefs, GSC, Surfer, sitemap, or client data is missing.

When handling source documents:
- Treat the master instruction set as the highest-level operating authority.
- Use the short SOP for user/team-facing workflow expectations.
- Use the idea generation document for sourcing and qualifying topic ideas.
- Use the population document for spreadsheet field mapping, SERP handling, prioritisation, and review.

## Core Workflow

1. Establish the strategy scope.
   - Identify whether the task is net-new ideation, optimisation opportunity finding, topical map planning, spreadsheet population, prioritisation review, or delivery scheduling.
   - Note the target country/language and whether the output is for blogs, landing pages, guides, product/category pages, or a mix.

2. Generate or consolidate topic ideas.
   - From client inputs: extract product/service themes, audience needs, use cases, features, problems, buyer motivations, and conversion goals.
   - From keyword research: shortlist terms with intent match, meaningful volume or traffic potential, achievable KD, and relevant modifiers such as `best`, `buy`, `how to`, `vs`, `near me`, `price`, or location terms.
   - From GSC: find low-CTR/high-impression queries, ranking queries missing from page copy, queries with clicks but weak average position, and long-tail informational/commercial gaps.
   - From Ahrefs: identify quick wins at positions 4-10, declining top pages, unintended rankings at positions 11-30, URL-level keyword clusters, and competitor content gap opportunities.
   - From Surfer: use Topical Map for new sites/new territories and Domain Map for sites with existing rankings or topical authority.

3. Map each idea to search intent and content type.
   - Blog list/roundup: "best", "top", comparisons, venues/products/providers.
   - How-to guide: step-based educational intent.
   - Ultimate guide: broad topic requiring a chaptered pillar.
   - Landing page/product/category page: transactional or BOFU intent.
   - Optimisation: an existing URL already has impressions, rankings, or partial intent coverage.
   - If the SERP format disagrees with the planned type, reframe the keyword, change the content type, or deprioritise.

4. Populate strategy fields.
   - Content title: write the H1 or page title; include an alternative title only when useful.
   - Content type: choose the closest template type.
   - New/opt: mark as new creation or optimisation.
   - Funnel position: classify TOFU, MOFU, BOFU, or evergreen.
   - Description: summarise the angle, scope, audience, caveats, and strategic fit.
   - Primary keyword: choose the most focused viable keyword, not the broadest possible rank target.
   - Metrics: add KD, volume, traffic potential, global search volume, parent topic, parent KD/volume, and related keywords where available.
   - SERP data: include the top 10 organic URLs only, plus titles, DR, traffic, keywords, word count range, and backlinks when available.
   - Current performance: add current ranking URL/position and GSC clicks, impressions, CTR, average position, and top-performing URL when available.
   - Supporting content: add only the most relevant blog and landing page URLs after the topic is approved.

5. Prioritise.
   - High: clear intent match, strong business relevance, useful volume or traffic potential, beatable/underserved SERP, acceptable KD and effort, and cluster/internal-linking value.
   - Medium: relevant but less central, moderate demand or TP, moderate competition, or useful for future cluster support.
   - Low: weak business fit, poor intent match, low demand and low TP, high effort, isolated topic, or SERP mismatch.
   - Document reasoning when prioritising against surface metrics, such as low volume but strong BOFU value.

6. Estimate difficulty.
   - Low: aligned SERP, weaker competitors or thin/outdated results, modest effort, existing topical support.
   - Medium: mixed SERP strength, some content depth or SME input required, moderate KD/backlinks.
   - High: strong domains, high backlink/content quality bar, heavy original research, complex visuals/data, or uncertain intent.

7. QA and review.
   - Verify all metrics are copied from the correct keyword/location.
   - Check that top SERPs are organic results, including `Organic, Thumbnail` where relevant, not local packs/ads unless explicitly analysing SERP features.
   - Confirm each topic is business-aligned and not merely high volume.
   - Check there are no duplicate or overlapping ideas unless they have distinct intent.
   - Flag unclear assumptions for reviewer/client approval before production.

## Output Formats

For a strategy table, return rows with these columns when available:

```text
Content title | Alternative title | Content type | New/opt | Difficulty | Priority | Funnel position | Description | Primary keyword | KD | Volume | Traffic potential | Global Search Volume | Related keywords | Parent topic | Parent KD | Parent volume | Keyword research sheet | Link to SERP data | Top 10 SERPs | Titles | DR | Traffic | Keywords | Word count | Backlinks | Current URL | Current position | Clicks | Impressions | CTR | Average Position | Supporting blogs | Supporting landing pages | Review notes
```

For an ideation summary, group ideas by priority or funnel stage and include:
- Topic/title
- Target keyword and related keywords
- Content type and new/optimisation status
- Funnel stage
- Strategic rationale
- SERP/competition notes
- Recommended next action

## References

- Read `references/README.md` first when choosing which local materials to use.
- Read `references/content-strategy-source-pack.md` for a distilled summary of the uploaded source documents and workbook examples.
- Read `references/content-strategy-framework.md` for detailed source-derived rules on idea generation, spreadsheet population, prioritisation, worklog support, and QA.
- Read `references/template-columns.md` when mapping data into the strategy spreadsheet columns.
- Use `references/source-documents/` for the original DOCX instruction sources.
- Use `references/templates/` for blank/reusable strategy workbooks.
- Use `references/examples/` for completed strategy/worklog examples.

## Edge Cases

- If Ahrefs/GSC/Surfer data is unavailable, create a provisional strategy and label missing metrics clearly.
- If a keyword has high volume but weak business fit, downgrade unless the user provides a brand-awareness rationale.
- If a zero-volume keyword has BOFU value, existing impressions, or clear sales relevance, keep it as a strategic exception and explain why.
- If a content audit exists, use it before proposing net-new content so optimisations and cannibalisation risks are considered.
