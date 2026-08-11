---
name: seo-content-writer
description: Writes Google Docs-friendly SEO posts (how-to, roundup, or ultimate guide) with metadata, URL slug, Surfer-term integration, and internal links selected from a provided sitemap sheet.
---

# SEO Content Writer (How-to / Roundup / Ultimate Guide)

## PURPOSE
Produce clean, human-first SEO content that matches the requested content type, includes metadata + URL slug, integrates Surfer/NLP terms naturally, uses a clear Google Docs heading structure, and includes an internal links plan based only on a user-provided sitemap sheet or pasted sitemap list.

## WHEN TO USE
- User asks for an SEO article in Google Docs-friendly formatting
- User wants a how-to, roundup list post, or ultimate guide
- User provides (or will provide) a sitemap sheet / post sitemap list for internal links
- User provides a primary keyword and (optionally) Surfer/NLP terms

DO NOT USE WHEN...
- User asks for short ad copy, emails, or social posts
- User asks for medical/legal advice content without sources and wants firm claims
- User asks for web browsing to verify facts (this skill is file/brief-driven)

## INPUTS
REQUIRED:
- Client: [CLIENT_NAME]
- Market/audience + English variant: [COUNTRY/AUDIENCE] / [ENGLISH_VARIANT]
- Tone notes: [tone]
- Topic: [TOPIC]
- Content type: [how-to | roundup | ultimate guide] OR allow auto-pick from brief
- Primary keyword: [PRIMARY_KEYWORD]
- Audience intent: [intent]
- CTA: [soft CTA near end, no hard sell]

OPTIONAL (HIGHLY RECOMMENDED):
- Surfer/NLP terms list: [PASTE TERMS]
- Word count target OR package tier: [budget | standard | premium] or [1000-2500]
- Sitemap sheet content for internal links (paste table) OR upload file and paste the relevant rows
- Internal link constraints (e.g., "must include service page + 2 blog posts")
- Image requirements (count, types, sizes) OR accept default image plan
- Google Docs destination preference: existing Google Doc, target Google Drive folder, or no upload

EXAMPLES:
See `references/brief-template.txt` and `references/sitemap-input-template.txt`
Example posts live in `references/examples/`, grouped by content type:
- `examples/how-to/`
- `examples/roundup/`
- `examples/ultimate-guide/`
Outline/template references live in `references/templates/`, grouped by content type:
- `templates/how-to/`
- `templates/roundup/`
- `templates/ultimate-guide/`

## OUTPUTS
Artifacts (single paste-ready output):
1) Metadata block:
- Meta title
- Meta description
- Focus keyphrase (primary keyword)
- Suggested URL slug (<= ~60 chars)
2) Internal links plan:
- 1 primary CTA internal link (from sitemap)
- 2-4 contextual internal links (from sitemap)
3) Full article in Google Docs-friendly formatting:
- Plain heading lines (no #)
- Heading hierarchy must map cleanly to Google Docs styles:
  - Article title = document title
  - Main sections = Heading 1
  - Subsections = Heading 2
  - Nested subsections only when needed = Heading 3
- Bullets use "• "
- Paragraphs 1-3 sentences
- Includes the correct structure for the selected content type
4) Image plan:
- In-article image blocks using `references/image-block-template.txt` (if images requested or default applied)

Success criteria:
- Content type matches brief (no blended formats)
- Headings have distinct purposes
- In ultimate guides, every Heading 2 section must contain body copy before the next heading appears
- Surfer terms are integrated naturally (or warning if missing)
- Internal links are chosen only from provided sitemap content
- Any example post consulted came from the matching content-type folder and was used for pattern reference only

## WORKFLOW
1) Identify content type.
   - If user specifies: follow it.
   - Else infer:
     - Roundup = comparing multiple options/providers/products ("best", "top", "compare").
     - How-to = step-based process ("how to", "steps", "SOP").
     - Ultimate guide = broad educational resource with chapters/subtopics.

2) Validate inputs.
   STOP AND ASK if missing: Topic, primary keyword, audience/market, content type (or permission to infer), CTA.
   If Surfer terms missing: proceed with a one-line warning in the output header.
   Before writing any draft, STOP AND ASK:
   - Should the output be uploaded to an existing Google Doc, a specific Google Drive folder, or returned in chat only?
   - If upload is requested but no destination is provided, ask for the Google Doc link/name or the Google Drive folder link/name before proceeding.
   Internal links:
   - If user demands internal links but no sitemap content is provided, STOP AND ASK for sitemap rows (use `references/sitemap-input-template.txt`).
   - If sitemap content is provided, proceed and select links per `references/internal-link-selection.md`.

3) Set word count target.
   - If tier provided:
     - budget: ~1000-1400
     - standard: ~1400-2000
     - premium: ~2000-2500
   - If explicit range provided, follow it.
   - If neither provided, aim ~1400-1800.

4) Draft the scaffold before drafting body copy.
   - Write all headings first.
   - Assign a single purpose to each section (avoid overlap).
   - Build a clean Google Docs outline with a single H1-equivalent title, H1 main sections, and H2/H3 subsections only where helpful.
   - If template references are available for the selected content type, consult the matching folder under `references/templates/`.
   - For roundup posts, use package tier to choose the closest matching template where available: budget, standard, or premium.
   - If example posts are available for the selected content type, consult only the matching folder under `references/examples/`:
     - How-to examples: `examples/how-to/`
     - Roundup examples: `examples/roundup/`
     - Ultimate guide examples: `examples/ultimate-guide/`
   - Use examples to understand structure, section rhythm, editorial depth, metadata style, and Google Docs formatting. Do not copy wording, client facts, links, pricing, product claims, or image prompts from examples.
   - When a `.docx` and `.pdf` exist for the same reference, use the `.docx` for readable text and the `.pdf` as the visual layout source.
   - Process PDFs visually by rendering pages to images before using them for layout, spacing, heading hierarchy, table/list rhythm, or page-break judgement. Do not rely on PDF text extraction for structure.

5) Write metadata + URL slug.
   - Meta title: keep within typical 25-60 chars; include primary keyword naturally.
   - Meta description: 100-140 chars; outcome + key subtopics + gentle CTA.
   - URL slug: short, lowercase, hyphenated, keyword-led, no stopword stuffing.

6) Build internal links plan (from sitemap only).
   - Select:
     - 1 CTA link (most commercially relevant page for the funnel stage)
     - 2-4 contextual links (definitions, supporting guides, adjacent topics)
   - Provide suggested anchors + placement notes.
   - Do not invent URLs not in the sitemap input.

7) Draft content by content type.

   A) HOW-TO (step-based)
   Required structure:
   - Title
   - Intro (outcome + who it's for + what it covers + soft CTA mention)
   - Before you start (prereqs/tools/decisions)
   - Steps (5-10 steps)
   - Tips / mistakes / decision help
   - FAQ (3-6 Qs if relevant or requested)
   - Summary + CTA

   B) ROUNDUP (comparison list)
   Required structure:
   - Title
   - Intro focused on selection and comparison
   - How we chose / what to look for (and price guide if relevant)
   - Categories (optional)
   - Listings in a consistent editorial structure:
     - Best for
     - Quick summary
     - Key details
     - Differentiators
     - Pricing note
     - How to get started
     - Verdict
   - FAQ (3-6 Qs)
   - Conclusion + CTA

   C) ULTIMATE GUIDE (chaptered educational)
   Required structure:
   - Title (guide-led framing)
   - Intro (why it matters + common challenge + what's inside + who it's for + CTA)
   - Chapters that progress: basics -> concepts -> deeper detail -> practical application -> decision support
   - Every Heading 2 chapter must include body paragraphs immediately under the heading; do not stack Heading 2s with no explanatory copy between them
   - FAQ (when relevant)
   - Conclusion + CTA

8) SEO / Surfer integration pass.
   - Place primary keyword in: title + intro + at least one major heading (natural).
   - Spread Surfer terms across high-value sections; rewrite sentences to avoid forced phrasing.
   - Avoid repeating the exact primary keyword phrase more than once per paragraph.

9) Image blocks (if required by brief or default image plan is enabled).
   - Insert image blocks at the most relevant sections using `references/image-block-template.txt`.
   - Default (if user requests images but gives no specifics):
     - 6 image blocks total (3 photorealistic, 3 infographic) + 1 duplicate (1200x630).
   - No logos/brands; no people unless requested.

10) Final QA.
   - Run `references/qa-checklist.md`.
   - Remove repetitive/robotic phrasing.
   - Tighten long sentences.
   - Ensure internal links match sitemap input exactly.
   - Ensure the heading levels are logically nested for easy paste/upload into Google Docs.
   - For ultimate guides, check every Heading 2 has at least one supporting paragraph or bullet block before the next heading.
   - Check that any example-informed structure came from the selected content type's example folder.

## OUTPUT FORMAT
Return exactly this order:

```text
Meta title:
Meta description:
Focus keyphrase:
Suggested URL:

Internal links plan:
1) CTA link: [Title] — [URL]
   Suggested anchor:
   Placement note:
2) Context link: ...
3) Context link: ...
4) Context link: ...
5) Context link: ...

[Optional warning if Surfer terms missing: "Surfer terms not provided; coverage kept natural."]

[If not yet confirmed, ask before drafting: "Do you want this uploaded to a specific Google Doc, a Google Drive folder, or should I return it here only?"]

Title: ...

Intro
...

[Article body with plain headings and "• " bullets, structured so headings can be applied in Google Docs as Title, Heading 1, Heading 2, and Heading 3]

[IMAGE BLOCK]
...
[/IMAGE BLOCK]

FAQ
Q:
A:

Conclusion
...
```

## DEPENDENCIES
- None required.
- If the user wants internal links: requires sitemap content pasted or uploaded + pasted rows.
- If internal link selection is needed, user must provide sitemap rows or a sitemap sheet; references live in this skill's `references/` folder.
- Content examples are optional reference material and live in `references/examples/` by content type. Use the matching folder only unless the user explicitly asks for cross-format inspiration.
- Template references are optional outline/layout material and live in `references/templates/` by content type. Prefer the matching package tier when one is provided.

## SAFETY & EDGE CASES
- Default to cautious wording for claims.
- If asked to include trademarks/logos in image prompts, refuse that part and offer a logo-free alternative.
- If the user requests citations but provides none and browsing is not allowed, STOP AND ASK for sources or permission to draft without citations.

## EXAMPLES
- Example 1 (How-to): user provides topic + keyword + steps intent + sitemap -> output metadata + internal links + step guide.
- Example 2 (Roundup): user provides list of options + selection criteria + sitemap -> output metadata + internal links + consistent listings.
- Example 3 (Ultimate guide): user provides topic + subtopics + sitemap -> output metadata + internal links + chaptered guide.
