# LLM Audit Source Pack Guide

Use this reference when working with local AI visibility / LLM audit source packs.

## Standard Source Pack Shape

A strong Woww LLM audit pack can include:

- AI Audit Data Sheet: source of truth for onboarding, audit checks, platform visibility, brand narrative, socials, directories, competitor content, Ahrefs, authority, UGC, PR, content, performance, accessibility, schema, llms.txt, recommendations, and scoring.
- Chats from LLMs workbook: raw prompt outputs split by region or market, usually with prompt IDs, platform/model, user prompt, assistant answer, mentions, sources, content-in-chat flags, and citation counts.
- PEEC / Source Domains & URLs workbooks: regional source-domain and source-URL evidence, including retrieved domains, listicles, category pages, competitor pages, UGC, YouTube, social profiles, directories, and retrieval/citation rates.
- Crawl/indexability workbook: URL-level evidence for indexability, status code, titles, meta descriptions, H1s, schema items, inlinks, and retrieval hygiene.
- Completed audit report DOCX: report structure, tone, section order, data storytelling, and recommendation style.
- AI info page DOCX: source-of-truth implementation asset for entity clarity.
- llms.txt DOCX or text draft: crawl-friendly summary and canonical link guidance for AI/search systems.
- Screenshots or images, when supplied: visual support for specific sections, charts, prompt examples, SERP examples, or evidence panels.

## Local Example Packs

### Incubeta - AI Visibility Audit

Use this as the best local example for a multi-region B2B/service-company AI visibility audit.

Important files:

- `AI Audit Data Sheet - Incubeta.xlsx`
- `Chats from LLMs.xlsx`
- `Incubeta - AI Audit Report Document.docx`
- `Incubeta Crawl Pages - Meta titles, descriptions, h1s, schema items, indexability, status code.xlsx`
- `LLMs.txt/AI Info Page.docx`
- `LLMs.txt/New LLMs.txt for Incubeta.docx`
- `Source Domains & URLs/(AU) Source URLs & Domains - PEEC Incubeta.xlsx`
- `Source Domains & URLs/(DE) Source URLs & Domains - PEEC Incubeta.xlsx`
- `Source Domains & URLs/(UAE) Source URLs & Domains - PEEC Incubeta.xlsx`
- `Source Domains & URLs/(UK) Source URLs & Domains - PEEC Incubeta.xlsx`
- `Source Domains & URLs/(US) Source URLs & Domains - PEEC Incubeta.xlsx`

Observed workbook patterns:

- Data sheet tabs include onboarding, audit overview, brand narrative, socials, directories, competitor content, Ahrefs, authority, UGC, PR, content, performance, accessibility, schema, llms.txt, recommendations, LLM visibility, competitor visibility, brand visibility by region, competitor counts by region, and prompt visibility by region.
- Chat workbook sheets are split by market/region such as US, UK, AU, DE, and UAE.
- PEEC workbooks include `PEEC - Domains`, `PEEC - URLs - All`, `Title Contains Besttop`, and URL subsets for channels or domains such as YouTube, Instagram, Sortlist, Clutch.co, Semrush, Directive Consulting, Design Rush, TripAdvisor, Reddit, Pushgroup, and Top Developers.
- The crawl workbook provides technical retrieval evidence through status code, indexability, metadata, schema, and internal link columns.

Observed report pattern:

- The report opens with why AI visibility matters, how AI visibility works, and client-specific AI visibility goals.
- It then moves into audit findings, data sources, overall standing, competitors by region, prompt visibility, brand narrative, prioritised opportunities, performance tracking, website accessibility, website content, recommended next steps, measurement, working with Woww, bonus tactics, and credits.
- The report uses concrete prompt themes and regional visibility context, then turns evidence into prioritised implementation opportunities.

Observed implementation asset pattern:

- AI info pages include basic information, company positioning, core capabilities, solution areas, AI/search expertise, industries, markets, selected client experience, research/education, leadership/news, guidance for AI assistants, and official links.
- llms.txt drafts use concise Markdown-style sections for what the company does, core capabilities, AI/search expertise, important URLs, preferred brand description, audiences, markets, and guidance for AI systems.

### Paradise Games AI LLM Audit

The local folder name indicates a Paradise Games example pack, but the contained filenames are Incubeta-labelled. Before using it as Paradise-specific evidence:

- Open the data sheet and report document.
- Confirm the client name, domain, markets, prompt set, and report content.
- If the evidence is Incubeta-specific, use it only as a structure/style example.
- If the evidence is Paradise-specific but filenames are stale, note the filename mismatch and rely on internal workbook/report content.

## Evidence Workflow

1. Inventory the pack.
   - List files and folders.
   - Identify the data sheet, chats workbook, source-domain workbooks, crawl export, completed report, AI info page, and llms.txt file.
   - Note markets/regions covered.

2. Inspect workbook structure.
   - Read sheet names before loading data.
   - Identify header rows and region-specific tabs.
   - Preserve regional splits unless the user asks for a single executive summary.
   - Keep source-domain sheets separate from prompt visibility sheets.

3. Establish source of truth.
   - Use the AI Audit Data Sheet for scores and audit conclusions.
   - Use Chats from LLMs for raw prompt examples and platform-specific wording.
   - Use PEEC/source-domain sheets for retrieval, citation, source-domain, listicle, directory, UGC, and competitor-source evidence.
   - Use crawl workbooks for technical retrieval and indexability evidence.
   - Use completed reports for structure, tone, and layout guidance.

4. Analyse by section.
   - Visibility standing: score, region, platform, prompt group, and visibility band.
   - Competitors: brands mentioned, AI visibility competitors, source competitors, and why they are winning.
   - Brand narrative: accuracy, specificity, missing differentiators, geography, entity confusion, and sentiment.
   - Source footprint: domains and URLs AI systems retrieve or cite, especially listicles, directories, UGC, social, PR, and owned pages.
   - Technical retrieval: indexability, blocked pages, schema, sitemaps, llms.txt, AI info page, Common Crawl, and speed/TTFB where available.
   - Implementation opportunities: owned content, authority, social/reviews, UGC, PR, technical fixes, measurement.

5. Write evidence-led recommendations.
   - Lead with the finding.
   - State the evidence source.
   - Explain the visibility mechanism.
   - Give a specific action.
   - Assign priority, effort, and owner/channel when useful.

## AI Info Page Pattern

A recommended AI info page should include:

- Basic information.
- Company positioning.
- Core capabilities.
- Products, services, or solution areas.
- AI/search/answer-engine expertise where relevant.
- Industries served.
- Markets and regional presence.
- Notable clients, case studies, awards, credentials, or proof points.
- Research, educational content, news, and leadership pages.
- Guidance for AI assistants.
- Official canonical links.

Keep it factual, concise, and supported by visible site content. Do not add claims that the client cannot substantiate.

## llms.txt Pattern

A useful llms.txt draft should include:

- Canonical brand name.
- What the company does.
- Core capabilities.
- Priority service/category pages.
- Preferred factual brand description.
- Geographic markets.
- Audiences served.
- Official URLs and contact/about pages.
- AI/search guidance if relevant.

Use llms.txt as a supplementary retrieval aid. It does not replace indexable source-of-truth HTML pages, schema, third-party authority, or content quality.

## QA Checks

- Confirm client identity before using any score or finding.
- Keep regions separate unless combining them is explicitly requested.
- Do not treat source-domain retrieval as a brand mention unless the sheet says the brand was mentioned.
- Do not treat implementation docs as proof of improved visibility.
- Avoid copying client-specific conclusions from examples into a new audit.
- Flag filename/content mismatches.
- Cite the local file or workbook/sheet behind each major claim.
