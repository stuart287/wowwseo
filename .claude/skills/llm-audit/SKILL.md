---
name: llm-audit
description: Create, review, or improve Woww-style LLM and AI visibility audits using client Drive source packs, AI audit data sheets, PEEC/source-domain exports, prompt visibility evidence, brand narrative checks, competitor mention analysis, and client-ready recommendations.
---

# LLM Audit

Use this skill when the user asks for an LLM audit, AI visibility audit, generative engine optimisation audit, LLMO/GEO review, AI search visibility report, prompt visibility analysis, PEEC audit, or recommendations to improve how AI tools describe and recommend a brand.

## Core Output

A complete LLM audit usually has two deliverables:

1. An evidence base: AI audit data sheet, prompt/chat exports, PEEC or source-domain sheets, screenshots, client onboarding answers, and relevant third-party/source checks.
2. A client-facing audit document that explains the AI visibility context, reports current visibility and competitors, diagnoses brand narrative accuracy, identifies misinformation risk, and turns the evidence into prioritised actions.

Do not invent visibility percentages, prompt results, competitor counts, sentiment, screenshots, source domains, or platform coverage. Use the provided Drive source pack, connected tools, live research, or clearly labelled assumptions.

## Inputs

Required:
- Client name, domain, market or region, and the output format requested.
- A source pack or equivalent exports with prompt results, AI visibility scores, competitor/entity mentions, and source domains.
- Client positioning: desired brand narrative, priority topics, target audience, business outcomes, and known competitors.

Recommended:
- Existing AI audit master doc to match.
- AI Audit Data Sheet with visibility, prompt, competitor, sentiment, and platform tabs.
- PEEC or Source Domains & URLs sheet.
- Prompt chat exports or screenshots from PEEC, Ahrefs, Perplexity, ChatGPT, Gemini, Google AI Overviews, Claude, or other tested platforms.
- Section-specific reference images or screenshots that show the exact charts, tables, SERP snapshots, prompt outputs, or evidence panels the final Google Doc should reflect.
- Evidence for website crawlability, Common Crawl inclusion, site speed/TTFB, schema, llms.txt, socials, reviews, directories, PR, UGC, and third-party roundups.

Ask only when missing context changes the audit materially, such as no client/domain, no prompt evidence, or no source pack. Otherwise proceed with caveats and label missing evidence.

## Document and Data Handling

Use the bundled references in this order:

1. Read `references/README.md` to identify which local reference or source pack applies.
2. Read `references/source-pack-guide.md` when working from DOCX/XLSX source packs or matching a completed audit structure.
3. Read `references/client-source-packs.md` when using a known Google Drive source pack.
4. Read `references/audit-framework.md` for judgement rules, evidence priority, scoring bands, recommendation patterns, and writing rules.
5. Open source files in `references/source-packs/` only when the task needs workbook structure, example evidence, report style, AI info page structure, or llms.txt structure.

When handling spreadsheets:
- Inspect workbook sheet names, header rows, regions, and platform/prompt tabs before analysing.
- Treat the AI Audit Data Sheet as the source of truth for scores, prompt outcomes, competitor counts, and audit conclusions.
- Treat Chats from LLMs exports as raw prompt evidence and quote/summarise only the rows needed to prove a pattern.
- Treat PEEC/source-domain workbooks as retrieval and citation evidence; do not confuse source retrieval with brand visibility unless the sheet shows a brand mention.
- Preserve regional splits such as US, UK, AU, DE, UAE, SADC, EU, or other market tabs.

When handling documents:
- Treat completed audit report DOCX files as structure, tone, and layout examples unless the user is updating that exact report.
- Treat AI info pages and llms.txt drafts as implementation deliverables, not proof that visibility has improved.
- Flag filename/client mismatches before relying on a local source pack for client-specific evidence.
- Keep client findings separate across all examples and source packs.

## Core Workflow

1. Establish scope.
   - Confirm the client, market, audit date, platforms tested, regions tested, and whether the work is a new audit, a review, a rewrite, a spreadsheet update, or a findings summary.
   - If one of the known source packs applies, read `references/client-source-packs.md` and open only that client's relevant Drive files.
   - If one of the bundled local source packs applies, read `references/source-pack-guide.md`, then open only the relevant local pack files.

2. Inventory evidence.
   - Separate evidence into client goals, prompt results, competitor/entity mentions, brand-description outputs, source domains, screenshots, website checks, social/review profiles, third-party sources, existing report prose, and section-specific reference images.
   - Treat the data sheet as the source of truth for scores and prompt outcomes. Treat the master doc as the style and narrative reference.
   - Do not mix evidence between client folders.
   - When screenshots or reference images are provided, note which audit section each image belongs to and what claim, table, or narrative point it is meant to support.

3. Analyse AI visibility.
   - Report overall visibility by platform, prompt group, market, and region where available.
   - Classify standing with the standard bands: 0-5% non-existent/practically invisible, 5-20% low, 20-50% moderate, 50-80% high, 80%+ excellent.
   - Explain whether the brand appears consistently, only in branded prompts, only in niche prompts, or is mostly omitted from broad commercial/research prompts.

4. Analyse competitors and share of voice.
   - Identify the brands, publications, directories, forums, review sites, and aggregators that AI tools mention instead of or alongside the client.
   - Distinguish real-world competitors from AI visibility competitors, source domains, and authority hubs.
   - Use competitor mentions to explain what AI systems currently trust: stronger content footprint, clearer entity signals, more third-party citations, better reviews, more UGC, or fresher PR.

5. Analyse brand alignment.
   - Compare how AI tools describe the brand against the client's preferred positioning.
   - Flag missing differentiators, vague phrasing, wrong locations, outdated facts, competitor-adjacent framing, similarly named entity confusion, unsupported claims, and sentiment drift.
   - State whether AI broadly understands the brand, partially understands it, or rewrites the narrative in a risky way.

6. Analyse misinformation and reputation risk.
   - Separate ordinary misinformation from malicious or criticism-led disinformation.
   - Trace risky claims to source domains, reviews, old pages, news coverage, forums, or prompt outputs where evidence exists.
   - Recommend correction, removal, response, new source-of-truth content, or monitoring depending on severity and controllability.

7. Diagnose improvement levers.
   - Owned content: source-of-truth page, AI info page, llms.txt, service/category pages, comparison pages, roundups, guides, FAQs, schema, freshness, internal links, and answer-led content structure.
   - Authority: digital PR, third-party roundups, directories, citations, partner profiles, Wikipedia/Wikidata where appropriate, analyst/media coverage, backlinks, and Common Crawl inclusion.
   - Social and UGC: LinkedIn, YouTube, Google Business Profile, X, Facebook, Instagram, TikTok, Reddit, Quora, Medium, Substack, reviews, forums, and community Q&A.
   - Technical retrieval: crawlability, robots, sitemap, indexation, TTFB below 1s, Core Web Vitals, server errors, blocked AI/search crawlers, JavaScript rendering, and structured data.

8. Write the audit narrative.
   - Lead each section with the finding, then the evidence, then the recommendation.
   - Keep the tone client-ready, practical, and confident. Avoid generic AI search filler unless it helps the client understand why the action matters.
   - Reuse the established Woww report shape unless the user provides a different template.
   - If section screenshots or reference images are available, use them to improve layout fidelity and evidence clarity in the final Google Doc. Place each image near the section it supports and introduce it with a short evidence-led sentence or caption.

## Report Structure

Use this structure for a full client-facing audit unless a template is provided:

```text
Client Name AI Visibility Audit - by Woww
Why AI Visibility Is Important for Your Business
How AI Visibility / LLM Visibility Works
AI Visibility Goals for Your Business
Audit Findings: Enhancing Your LLM Visibility
  Audit Scoresheet / Data Sources
  Overall AI Visibility Standing
  Visibility Band Explanation
  Top Competitors
  How Your Brand Shows Up
  Misinformation & Malicious Disinformation
A Path Forward for Your Business
  Top Prioritised Opportunities
  Socials and Profile Standardisation
  Reviews, Directories, Citations, and Third-Party Trust
  UGC, Community, and Parasite SEO Opportunities
  PR, Roundups, and Authority Building
  AI-Friendly Content, Schema, and Source-of-Truth Assets
  Technical Retrieval, Common Crawl, llms.txt, and SEO Foundations
Recommended Next Steps
Measurement & Continuous Improvement
Working with Woww Moving Forward
Bonus / Advanced Tactics, if appropriate
Credits, if required
```

## Output Formats

For a findings summary, use:

```text
Finding | Evidence | Impact | Recommendation | Priority | Source
```

For an implementation backlog, use:

```text
Action | Channel | Evidence | Expected AI visibility impact | Effort | Priority | Owner/Notes
```

For a prompt visibility summary, use:

```text
Prompt group | Market/platform | Client visibility | Main competitors | Sentiment/narrative | Evidence source | Recommendation
```

For a visual evidence register, use:

```text
Section | Image/screenshot reference | What it shows | Source pack/file | Intended use in final doc
```

## References

- Read `references/README.md` first when selecting bundled local references.
- Read `references/source-pack-guide.md` when using local source packs, workbook examples, report DOCX examples, AI info pages, or llms.txt examples.
- Read `references/client-source-packs.md` when using the Travelit, Travel.co.za, Pan African Resources, CyberPro, Karingani, or Paradise Games source packs.
- Read `references/audit-framework.md` for evidence handling, scoring bands, report judgement rules, and recommendation patterns.
- Use `references/source-packs/Incubeta - AI Visibility Audit/` as the main local multi-region AI visibility audit example.
- Use `references/source-packs/Paradise Games AI LLM Audit/` only after checking the internal client identity because its copied filenames are Incubeta-labelled.

## QA

- Verify every score, percentage, prompt count, competitor claim, and example comes from the correct client source pack.
- Do not copy private client findings into a different client's audit.
- Preserve regional splits where the data has them, especially Karingani's SADC, US, and EU packs.
- Mark missing source data explicitly and recommend the next export or check.
- Make every recommendation specific enough for a writer, SEO, PR, social, or developer to act on.
- If visuals are used, make sure each screenshot is section-matched, accurately described, and not used to imply evidence that the underlying sheet or prompt export does not support.
