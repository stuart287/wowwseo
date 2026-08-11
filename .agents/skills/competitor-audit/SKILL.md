---
name: competitor-audit
description: Create, review, or improve Woww-style SEO competitor audits, including competitor selection, Ahrefs/backlink analysis, link intersect opportunities, Google Business Profile checks, content/social comparisons, spreadsheet synthesis, and client-ready audit narratives.
---

# Competitor Audit

Use this skill when the user asks for a competitor audit, SEO competitor comparison, off-page audit, competitor backlink review, link intersect analysis, or a client-ready summary of competitor research.

## Core Output

A complete competitor audit usually has two deliverables:

1. A detailed spreadsheet comparing the client and selected competitors across business, content, SEO, backlink, local, social, and opportunity metrics.
2. A concise client-facing audit document that explains the method, summarizes the main findings, and turns the spreadsheet into priorities.

Do not invent metrics. Use only provided exports, connected tools, live research, or clearly labelled assumptions. If current Ahrefs or search data is needed and not provided, ask for exports or use available connected research tools.

## Document and Data Handling

Use the bundled references in this order:

1. Read `references/README.md` to identify which local reference or source pack applies.
2. Read `references/source-pack-guide.md` when working from DOCX/XLSX/CSV source packs or matching a completed Woww audit structure.
3. Read `references/woww-competitor-audit-method.md` for competitor selection, spreadsheet conventions, backlink/link-intersect judgement, Google Business Profile checks, social/content review, recommendation patterns, and QA.
4. Open source files in `references/source-packs/` only when the task needs workbook structure, example evidence, raw Ahrefs exports, completed report style, or client-specific audit pack handling.

When handling spreadsheets and CSVs:
- Inspect workbook sheet names, header rows, filtered tabs, template tabs, and example rows before analysing.
- Detect CSV encoding and delimiter before parsing. Ahrefs exports may be UTF-16 and tab-delimited.
- Treat competitor selection workbooks as the source of truth for why competitors were included.
- Treat competitor analysis workbooks as the main comparison evidence base.
- Treat backlinks, referring domains, link intersect, content gap, common-domain, and common-keyword exports as supporting evidence for specific findings.
- Keep client-nominated, Woww-selected, SERP, Ahrefs, and expanded competitor lists distinct when they affect the narrative.

When handling documents:
- Treat completed audit DOCX files as structure, tone, section order, evidence-density, and report-style examples unless the user is updating that exact report.
- Do not let polished report prose override source workbooks or raw exports when they conflict.
- Keep client evidence separate across all local source packs.
- Flag missing, stale, mismatched, duplicated, template-leftover, or suspicious source data before relying on it.

## Workflow

1. Confirm the audit scope: client name, domain, geography, product/service focus, known competitors, and whether the audit should prioritize SEO competitors, real-world competitors, or both.
   - If one of the bundled local source packs applies, read `references/source-pack-guide.md`, then open only the relevant local pack files.
2. Build the candidate competitor pool from client suggestions, SERP competitors, Ahrefs competing domains, organic keyword overlap, backlink profile strength, and local/business relevance.
3. Select usually 3 main competitors. If more are useful, keep the client-facing story focused and move the rest into the spreadsheet.
4. Gather evidence:
   - Ahrefs batch analysis or site explorer metrics.
   - Backlinks and referring domains exports.
   - Link intersect export.
   - Organic keyword intersections and ranking gaps when available.
   - Branded search volume and top pages when relevant.
   - Website content activity, blog cadence, service/category coverage, UX signals.
   - Google Business Profile presence, reviews, photos, posts, location coverage.
   - Social channels, follower counts, posting frequency, engagement, and channel quality.
5. Create or update the comparison spreadsheet before writing the narrative. Treat it as the evidence base.
6. Write the audit document in plain client language: what was compared, why each competitor matters, where the client is ahead/behind, and what to do next.
7. Verify that every recommendation is traceable to data in the spreadsheet, source exports, or cited live research.

## Spreadsheet Shape

Prefer a primary comparison sheet with rows like:

- `Business`: domain URL, product/service offerings, domain age, employee count, Google Business Profile.
- `Content`: blog URL, blog frequency, key content types, service/category page coverage, useful resources.
- `SEO`: DR, UR, Ahrefs rank, estimated organic traffic, organic keywords, top 3/top 10 keyword counts.
- `Backlinks`: referring domains, backlinks, dofollow links, high-quality referring domains, spam/low-value link notes, anchor text patterns.
- `Paid/Search`: paid keywords, paid SERP presence, branded search demand, visible SERP features.
- `Social`: profiles, follower counts, posting cadence, engagement, platform fit.
- `Opportunities`: link prospects, content gaps, local visibility gaps, partnership/directories, tactical recommendations.

Keep source exports in separate tabs when available. Name tabs plainly: `Choosing Competitors`, `Competitor Analysis`, `Referring Domains`, `Backlinks`, `Link Intersect`, `Keyword Gaps`, `Branded Volume`.

## Client Narrative Shape

Use the established Woww structure unless the user asks for a different format:

- Introduction: define the competitor audit and explain the selection approach.
- Key: explain any symbols, colour coding, or scoring used.
- Off Page SEO: explain why backlinks and referring domains matter.
- Ahrefs: briefly define AR, UR, and DR if the client may not know them.
- Competitors: list the selected competitors and why they were selected.
- Backlinks: summarize relative backlink/referring-domain strength, quality issues, and link opportunities.
- Google Business Profile: compare local profile completeness and review strength.
- Detailed Competitor Analysis: point to the spreadsheet and summarize the most important non-SEO comparisons.
- Recommendations: prioritize next steps by expected impact and effort.

## Reference Loading

Read `references/README.md` first when selecting bundled local references.

Read `references/source-pack-guide.md` when you need:

- Local source-pack structure and file routing.
- Completed audit report examples.
- Raw Ahrefs CSV handling.
- Paradise Games or Pikeland Property Group source-pack patterns.
- Link intersect triage examples and template-leftover handling.

Read `references/woww-competitor-audit-method.md` when you need:

- The exact data sources and spreadsheet conventions.
- How to interpret backlink/referring-domain exports.
- How to select competitors and avoid false comparisons.
- A client-ready recommendation checklist.

Use `references/source-packs/Competitor Audit - Paradise Games/` as the local gaming/iGaming competitor audit example.

Use `references/source-packs/Competitor Audit - Pikeland Property Group/` as the local local-service/property competitor audit example.
