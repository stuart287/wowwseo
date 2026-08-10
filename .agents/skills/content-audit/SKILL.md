---
name: content-audit
description: Creates and reviews SEO content audits from crawl exports, keyword research, content analysis sheets, and client context. Use when asked to audit existing website content, assess on-page SEO quality, find content gaps, evaluate metadata/headings/images/internal links/content length/search intent, identify cannibalisation, or produce a content audit report with prioritised recommendations.
---

# Content Audit

## Purpose

Produce practical SEO content audits that evaluate whether existing content is indexable, discoverable, useful, search-intent aligned, and structured well enough to compete.

Use this skill for audit diagnosis and recommendations. Use `content-strategy` when the main task is turning findings into a prioritised publishing roadmap, and `seo-content-writer` when an approved item needs a full draft.

## Inputs

Required:
- Client/domain, target country or market, and business priorities.
- Crawl or page inventory data, ideally URLs, indexability, status codes, titles, meta descriptions, H1s, images/alt text, internal links, external links, folders, and content length.
- At least one performance or opportunity source: keyword research, current rankings, Google Search Console, Ahrefs, content analysis sheets, SERP review, or client priority pages.

Recommended:
- Existing content audit report or template to match.
- Page-level content analysis with qualitative ratings and comments.
- Keyword cannibalisation, existing keywords, keyword traffic potential, and content gap exports.
- Sitemap, top folders, URL structure, blog/category/product page lists, and known conversion pages.
- Brand tone, compliance limits, content ownership, and implementation constraints.

Ask only when missing context changes the audit materially, such as no domain, no crawl/page list, no target market, or no way to judge content performance/opportunity. Otherwise proceed with caveats and label assumptions.

## Core Workflow

1. Establish scope.
   - Confirm the site section, market, date of source data, and whether the audit covers all indexable pages, a blog, commercial pages, or a sample.
   - Identify whether the output should be a full report, findings summary, spreadsheet comments, page-level recommendations, or an implementation backlog.

2. Inventory the evidence.
   - Group available exports by theme: keywords, titles, metas, OG/Twitter tags, H1s/headings, images/alt text, URLs/folders, internal links, external links, content length, content analysis, and keyword gaps.
   - Prefer indexable 200-status URLs for SEO recommendations unless a non-indexable URL is important to a finding.
   - Note data gaps upfront instead of pretending every subsection has equal evidence.

3. Analyse keywords and search demand.
   - Identify existing rankings, missed keyword opportunities, keyword/topic gaps, traffic potential, and cannibalisation.
   - Flag pages ranking for unintended or weak-fit terms, multiple URLs competing for the same query, and important topics without a suitable landing page or article.
   - Separate business-critical BOFU opportunities from informational topics.

4. Analyse on-page SEO.
   - Page titles: check missing, duplicate, too short, too long, generic, keyword-poor, brand-suffix issues, and SERP rewrite risk.
   - Meta descriptions: check missing, duplicate, too short, too long, vague, boilerplate, and poor CTR motivation.
   - Social tags: check missing or duplicate OG/Twitter tags when social sharing matters.
   - Headings: check missing/multiple H1s, H1/title mismatch, weak keyword use, heading hierarchy, and scannability.
   - Images: check missing alt text, irrelevant alt text, oversized or decorative images, and opportunities to support product/service understanding.

5. Analyse links and siloing.
   - URL structure: review folder logic, physical siloing, clean slugs, duplicate paths, thin folders, and whether important pages sit in sensible sections.
   - Internal linking: identify orphan or low-inlink pages, high-value pages without enough support, weak contextual links, over-reliance on navigation links, and missing hub/spoke relationships.
   - Anchor text: check generic anchors, over-optimised anchors, mismatched anchors, and missed descriptive anchor opportunities.
   - External links: flag broken, irrelevant, excessive, or untrusted outbound links and opportunities to cite authoritative sources.

6. Analyse content quality.
   - Compare content length to intent and SERP expectations; do not recommend word count increases without explaining what information is missing.
   - Judge search intent match, topical completeness, expertise, originality, helpfulness, readability, trust signals, CTAs, freshness, and conversion support.
   - Categorise pages as keep, improve, consolidate, redirect, noindex, or remove when the evidence supports it.

7. Create content recommendations.
   - Recommend optimisation for existing URLs before net-new content when an existing page has rankings, impressions, backlinks, or topical fit.
   - Suggest new content for genuine gaps: short-form evergreen pieces, long-form guides, list posts, how-to guides, roundups, infographics, guest articles, and landing pages.
   - For each recommendation, state the target page or topic, why it matters, evidence, expected impact, and implementation priority.

8. Summarise actions.
   - End with prioritised improvements grouped by Keywords, On-page SEO, Links, and Content.
   - Distinguish quick fixes from strategic content work.
   - Include caveats, missing data, and recommended next exports where evidence is thin.

## Report Structure

Use this structure for a full audit unless the user provides a template:

```text
Introduction
Key
Keywords
  Existing Keywords
  Keyword Research
  Keyword Cannibalisation
  Keyword Traffic Potential
On Page SEO
  Page Titles
  Meta Descriptions
  OG Tags & Twitter Cards
  H-Tag Heading Structure
  Media, Images and Alt Text
Links & Siloing
  Physical Siloing & URL Structure
  Virtual Siloing & Linking
  Anchor Text
On Page Content
  Correlation Analysis
  Content Length
  Content Quality & Search Intent
Content Ideas
  Short Form Evergreen Content
  Long-form Articles
  Infographics
  Guest Articles
  List Posts
  How-to Guides
  Roundups
Content Promotion and Outreach Strategy
Summary and Conclusion
  Areas for Improvement
Appendices
```

Use the traffic-light key consistently:
- Green: done well or only trivial room for improvement.
- Orange: done poorly or clear room for improvement.
- Red: detrimental to SEO or effectively unimplemented.
- Blue: recommendation.

## Output Formats

For a findings summary, use:

```text
Finding | Severity | Evidence | Impact | Recommendation | Priority | Owner/Notes
```

For page-level recommendations, use:

```text
URL | Page type | Current issue | Evidence/source | Recommended action | Target keyword/topic | Priority | Notes
```

For report prose:
- Lead each section with the finding, then evidence, then recommendation.
- Quote or list only enough examples to prove the pattern.
- Avoid generic best-practice filler; tie every recommendation to the client's pages, keywords, or business goals.
- When metrics are unavailable, say what to export or verify next.

## References

- Read `references/source-data-map.md` when deciding how to use the common crawl, keyword, and content analysis exports.
- Read `references/audit-judgement-rules.md` for thresholds, severity guidance, and recommendation patterns.

## QA

- Confirm URLs, counts, and examples come from the correct client export.
- Do not mix evidence between different client reference folders.
- Check that recommendations are specific enough for a writer, SEO, or developer to act on.
- Make sure every red/orange issue has a corresponding action.
- Keep the audit qualitative where needed: search intent, usefulness, and content quality matter as much as spreadsheet thresholds.
