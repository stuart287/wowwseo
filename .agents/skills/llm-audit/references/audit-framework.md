# LLM Audit Framework

## Evidence Priority

Use evidence in this order:

1. Current client source pack supplied by the user.
2. AI Audit Data Sheet or PEEC/source-domain sheets.
3. Existing AI Audit Master report for structure, tone, and previous conclusions.
4. Screenshots, raw prompt/chat exports, and platform-specific outputs.
5. Live checks or connected research tools, clearly dated.
6. Assumptions, clearly labelled and kept out of scored conclusions.

Never let a polished report paragraph override the underlying data sheet when they conflict. Flag the discrepancy and use the sheet as the data source unless the user confirms otherwise.

## Source Pack Inventory

Before analysing a source pack, identify:

- Client name, domain, audit date, markets, and platforms tested.
- AI Audit Data Sheet and its key tabs.
- Raw chat or prompt export workbook.
- PEEC/source-domain workbooks and their regions.
- Crawl/indexability, schema, metadata, sitemap, Common Crawl, performance, or technical retrieval evidence.
- Completed audit report document, if present.
- AI info page and llms.txt implementation drafts, if present.
- Screenshots or images mapped to specific audit sections.

Record any mismatch between folder name, filenames, workbook contents, and report contents. Use internal workbook/report content as the evidence authority and label the mismatch.

## Spreadsheet Handling

- Read sheet names first and inspect header rows before drawing conclusions.
- Keep market tabs and regional source-domain sheets separate unless the user explicitly requests consolidation.
- Use the AI Audit Data Sheet as the source of truth for scores, pass/fail checks, visibility tables, competitor counts, and recommendations.
- Use Chats from LLMs exports for prompt-level evidence: prompt text, model/platform, answer text, mentions, sources, citations, and content-in-chat flags.
- Use PEEC/source-domain sheets to identify which URLs/domains are retrieved, cited, classified as listicles/directories/UGC/corporate/competitor, and whether the client is mentioned.
- Use crawl exports for retrieval hygiene: indexability, status codes, titles, meta descriptions, H1s, schema items, and internal link depth.
- Do not average regions together when one market is materially stronger or weaker.

## Visual Evidence Handling

- Treat uploaded screenshots and reference images as supporting evidence and formatting guidance, not as a replacement for the underlying sheet or prompt export.
- For each screenshot you use, capture:
  - section
  - what the image shows
  - source file/folder/link
  - the claim it supports
- If a screenshot is intended to shape the Google Doc layout, reuse its section placement and visual logic where practical, but keep the written conclusion tied to the underlying evidence source.
- If the image quality is too poor to read confidently, say so and rely on the source sheet/export instead of guessing.

## Scoring Bands

- 0-5%: non-existent or practically invisible.
- 5-20%: low visibility.
- 20-50%: moderate visibility.
- 50-80%: high visibility.
- 80%+: excellent visibility.

When scores vary by region or prompt group, report the range and explain where the brand is strongest and weakest. Avoid averaging away meaningful regional differences.

## Core Judgements

AI visibility:
- Strong when the brand appears across broad, high-intent, non-branded prompts and is recommended with clear reasons.
- Weak when the brand only appears for explicit branded prompts, niche prompts, or after competitors/aggregators dominate the answer.
- Risky when the brand is mentioned but described inaccurately, generically, negatively, or with outdated facts.

Competitor analysis:
- Treat competitors mentioned by LLMs as "AI visibility competitors" even if they are not perfect business competitors.
- Separate company competitors from source competitors such as directories, review sites, forums, publications, roundups, Wikipedia, tourism boards, analyst sites, or software listings.
- Identify why competitors win: authority, reviews, directories, content depth, clearer positioning, category ownership, freshness, PR, backlinks, or UGC.

Brand alignment:
- Compare AI descriptions against the client's desired narrative.
- Look for missing differentiators, entity confusion, geography errors, old facts, weak proof points, hedging language, and competitor-adjacent framing.
- If the model says "likely", "may", or "appears to", treat that as a sign the source footprint may be thin or unclear.

Misinformation:
- Ordinary misinformation is wrong, stale, vague, or unsupported information.
- Malicious disinformation is coordinated or intentionally damaging falsehood.
- Criticism-led risk is not necessarily false. Handle it by recommending credible, current, evidence-backed counter-narrative and reputation monitoring.

Source footprint:
- Owned source footprint is strong when important pages are indexable, easy to crawl, internally linked, structured, current, and clearly describe entities, services, geographies, and proof points.
- Third-party footprint is strong when credible listicles, directories, industry sources, news, partner pages, reviews, UGC, and social/video profiles consistently mention or cite the client.
- Retrieval does not equal recommendation. A page can be retrieved without mentioning the client, and a brand can be mentioned without being cited as a trusted source.

Implementation assets:
- AI info pages clarify the entity and give AI/search systems a concise source of truth.
- llms.txt helps expose canonical context and key URLs, but it is a supporting asset only.
- Treat implementation assets as recommendations or completed actions, not as visibility evidence unless later prompt/source data shows improvement.

## Recommendation Patterns

Owned source of truth:
- Create or improve an AI Info Page with concise, factual descriptions of the brand, services, locations, entities, leadership, differentiators, FAQs, proof points, and canonical links.
- Add or improve llms.txt where useful, but do not treat it as a replacement for indexable HTML pages.
- Write answer-led service, product, destination, industry, comparison, and FAQ pages.
- Add schema only when the visible page content supports it.

Content:
- Publish comparison pages that clarify distinctions from top AI visibility competitors.
- Publish roundups where the client can credibly be included, especially if external roundups already influence prompt outputs.
- Publish original research, tools, templates, calculators, benchmark reports, datasets, case studies, or explainers that other sites and AI systems can cite.
- Refresh older posts with current dates, updated examples, and stronger internal links.

Authority:
- Build third-party mentions through PR, industry publications, associations, partners, directories, analyst sites, review platforms, podcasts, YouTube, and credible roundups.
- For regulated or high-reputation industries, keep outreach accurate, source-backed, and compliant.
- Use Wikipedia or Wikidata only when notability and sourcing requirements are realistically met.

Social, UGC, and reviews:
- Standardise descriptions, categories, links, visuals, and posting cadence across social profiles.
- Grow detailed reviews on relevant platforms, prioritising specificity over volume alone.
- Participate in Reddit, Quora, LinkedIn, YouTube, Medium, Substack, forums, or communities with useful, non-spammy contributions.

Technical retrieval:
- Confirm important pages are indexable, internally linked, in sitemaps, fast enough for crawlers, and not blocked by robots or server rules.
- Treat TTFB above 1s as a retrieval risk for some AI/search crawlers.
- Check Common Crawl presence where source-pack evidence or the audit scope calls for it.

AI info page:
- Build one factual page that names the brand, domain, services, markets, audiences, differentiators, proof points, official profiles, and canonical pages.
- Include guidance for AI assistants only when it is supported by visible, truthful, client-approved facts.
- Keep claims specific and verifiable.

llms.txt:
- Draft concise Markdown-style guidance with the canonical brand name, what the company does, priority URLs, markets, services, audiences, and official links.
- Do not overstate what llms.txt can do; pair it with indexable HTML, schema, internal links, and third-party source growth.

## Writing Rules

- Lead with the finding and make the implication obvious.
- Use examples sparingly: enough to prove the pattern, not every row from the export.
- Tie each recommendation to a visibility mechanism: retrieval, entity clarity, authority, sentiment, source diversity, freshness, or conversion.
- Keep advanced or risky tactics in a clearly labelled optional/education section and do not recommend manipulative tactics as the main plan.
- When visuals are available, place them with the section they support and add a short caption or lead-in that explains why the image matters.
