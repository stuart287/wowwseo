---
name: mini-seo-audit-process
description: Run, populate, quality-assure, or improve a Mini SEO Audit from an approved framework and client source data. Use when Codex needs to collect Mini SEO Audit evidence, populate an existing Google Docs audit template, create the linked content strategy or worklog, repair incomplete/stale audit sections, or produce a final client-ready Mini SEO Audit.
---

# Mini SEO Audit Process

Use this workflow to turn approved client data into a complete, accurate Mini SEO Audit without damaging its template structure or leaving placeholders and stale reference content behind.

## Operating rules

- Treat the framework as structural authority and live client sources as factual authority.
- Build the data layer before writing recommendations. Do not infer missing numbers, claims, competitor facts, or delivery links.
- Use existing direct Google Docs edits only after locating the exact section and verifying its current context. Avoid global replacements for repeated placeholders.
- Keep recommendations specific, prioritised, implementable, and visibly tied to the evidence.
- Preserve document structure, tables, headings, links, and non-targeted content. Make a copy before a broad template adaptation.

## Workflow

### 1. Scope, budget and source map

1. Confirm the client, site/domain, target geography, approved competitors, delivery document, and the audit date.
2. Confirm the commercial envelope: 8 hours delivery time at R1,150/hour, total R9,200 unless the user states a different arrangement.
3. Locate the Mini SEO Audit framework, working audit, source Drive folder, reporting folder, proposed sitemap, competitor analysis sheet, and any linked content strategy/worklog document.
4. Create a coverage map: each audit section, its required data inputs, source sheet/tab, target report location, and final verification check. See [coverage map](references/coverage-map.md) and [source sheet map](references/source-sheet-map.md).
5. Label unavailable evidence as `TBD – source unavailable`; do not fill a template slot with a guess.

### 2. Collect evidence in the correct sheets before drafting

Populate or verify the audit evidence layer before report writing. Use the source sheet map to collect:

- crawl URLs, trailing slash behaviour, content word counts, and orphan-page checks;
- title, meta description, H1, Twitter/X card and OG-tag issue tabs;
- internal links, external links, and both anchor-text tabs;
- images, missing alt text, unique images, and unique alt text;
- competitor selection, competitor comparison, backlink exports, referring-domain exports, backlink/link intersects;
- keyword seed terms, existing rankings, keyword intersect, and bracketed keyword sheets for locations, core plumbing, emergency plumbing, drain/geyser/leak, electrical, HVAC/refrigeration, property types, trust/comparisons, and questions;
- proposed sitemap hierarchy for service, blog, about, project and contact recommendations.

For every data point retained in the audit, capture source, extraction date, scope, and caveat in the worklog or collection sheet. The Mini SEO Audit report should be written only after the necessary sheets are complete enough to support the recommendations.

### 3. Draft the audit narrative

For each section, write in this sequence:

1. evidence-led finding;
2. business or SEO implication;
3. prioritised recommendation with a clear action;
4. owner, dependency, or caveat where useful.

Make recommendations proportional to the data. Avoid generic filler, legacy-client facts, and advice that cannot be actioned.

### 4. Populate safely

1. Read the live target document and identify the exact body section, table cell, or paragraph.
2. Locate repeated placeholders by section anchor and instance, not by the first global match.
3. Replace the smallest confirmed range or use exact scoped replacements.
4. Re-read after every substantive/index-shifting update. Use live indexes only.
5. For stale template language, replace the complete relevant sentence/block after checking its surroundings; do not merely delete a marker.

### 5. Build the content strategy and worklog

Build the content strategy from the keyword brackets, keyword intersect, proposed sitemap, competitor analysis, and audit findings. It must distinguish:

- service/landing pages from blog/supporting content;
- new pages from optimisation of existing URLs;
- core Cape Town service pages from selective suburb/location pages;
- qualified service areas from services that need legal/operational confirmation;
- content topics that support service architecture from content ideas that are not worth publishing.

Create or update the worklog with source links, completed collection actions, open items, decisions, owner, and next step. Do not present planned collection as complete.

### 6. Validate and hand off

Run these checks before completion:

- Every required section is completed or explicitly marked unavailable.
- No `zzz`, `Zzz`, `{ClientName}`, placeholder links, unrelated client names, or reference-era brands remain in client-facing sections.
- Material figures and competitor claims reconcile with the data collection.
- Recommendations are evidence-linked and implementable.
- The content strategy and worklog links resolve and their content matches the audit.
- Every direct edit has been read back; confirm both new text is present and stale text is absent.
- Perform a final visual/layout check for table overflow, broken headings, and unreadable content.

## Prompt pack

Use [prompt pack](references/prompt-pack.md) for source collection, document population, content strategy, worklog creation, and final QA. Adapt only the bracketed input fields; keep the guardrails intact.

## Bundled templates and examples

Use [template and example assets](references/template-and-example-assets.md) when the user asks for the approved Mini Complete SEO Audit template, a completed example, or visual/layout guidance. The bundled PDF has also been rendered into page-level PNG images; use those images as the visual structure reference for headings, color-coded recommendation blocks, tables, page flow, and footer/page-number treatment.

## Timing

Plan the audit as an 8-hour delivery:

- 0:00–0:30 setup and source inventory
- 0:30–2:00 crawl/sitewide/on-page/link/image collection
- 2:00–4:00 keyword, competitor, backlink and sitemap review
- 4:00–5:15 content strategy and worklog
- 5:15–7:15 report writing and document population
- 7:15–8:00 QA, evidence reconciliation and handoff

## Failure recovery

- If a target range is ambiguous, stop the write and retrieve its local paragraph or table context.
- If a source conflicts with the framework, preserve the framework structure but disclose the factual conflict.
- If direct edits fail or a document changed unexpectedly, re-read the target, refresh indexes, and resume in smaller verified batches.
- If a required source is missing, record the gap and request it rather than manufacturing a conclusion.
