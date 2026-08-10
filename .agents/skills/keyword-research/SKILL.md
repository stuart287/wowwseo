---
name: keyword-research
description: Creates Google Sheets keyword research outputs for blogs and landing pages using the connected Ahrefs app, a copied keyword research template, and a structured brainstorming-to-analysis workflow based on the team's SOP.
---

# Keyword Research

## PURPOSE
Produce a copied and updated keyword research template for a specific client, topic, or landing page using the team's Google Sheets template, the connected Ahrefs app, and the keyword research SOP.

## WHEN TO USE
- User asks for keyword research for a blog post, article, guide, service page, category page, or landing page
- User wants a keyword research template copied and filled in
- User wants Ahrefs-backed seed term expansion, search volume checks, intent checks, or related term discovery
- User provides a topic, client, market, brief, content strategy, or existing keyword context

DO NOT USE WHEN...
- User only wants a short list of title ideas with no research
- User asks for a full content draft rather than research
- User wants live SERP browsing and no Drive/Sheets output

## REQUIRED INPUTS
- Client or brand name
- Topic / page / core offer
- Target country or country code for Ahrefs and search intent checks
- Content type: blog post, landing page, or allow inference

## OPTIONAL BUT HIGH VALUE INPUTS
- Briefing materials, content audit, strategy notes, or existing page URL
- Existing keyword list, GSC data, or competitor URLs
- Preferred Google Drive folder or existing Google Sheet to update
- Secondary keyword ideas, exclusions, or business priorities
- Target audience and commercial goal

## REFERENCES
- SOP summary: `references/sop-summary.md`
- Template map: `references/template-map.md`

## CONNECTED TOOLS
- Google Drive tools for reading the SOP/template, creating or updating Sheets, exporting/importing a workbook copy, and writing results
- Ahrefs app tools for search volume, related terms, and volume history

## OUTPUTS
Preferred output:
1) A copied and updated Google Sheets keyword research workbook
2) A concise summary in chat covering:
- primary target keyword
- supporting keyword clusters
- intent notes
- notable difficulty or opportunity signals
- any gaps, exclusions, or follow-up recommendations

If a sheet cannot be created or updated, return:
1) the same summary in chat
2) a clearly structured table-ready block that can be pasted into the template manually

## WORKFLOW
1) Confirm the destination before researching.
   Always ask before drafting or filling the sheet:
   - Should I update an existing Google Sheet, create a fresh copy of the keyword research template, or return the research in chat only?
   - If creating a copy, which Google Drive folder should it live in?
   - If updating an existing sheet, ask for the sheet link if it has not been provided.

2) Confirm the research brief.
   Stop and ask if missing:
   - client/brand
   - topic or page
   - target country
   - content type or permission to infer it

3) Create or open the working sheet.
   - If the user wants a fresh template copy, use the Google Drive workflow in `references/template-map.md`.
   - Preserve the workbook structure and tab names from the source template.
   - Name the copied file clearly, for example: `Keyword Research - {Client} - {Topic}`.

4) Extract seed terms from the brief before using Ahrefs.
   Use the SOP rules:
   - pull base phrases from the main topic, products, services, or page angle
   - add singular/plural variants
   - add common synonyms
   - add spelling variants where relevant
   - add industry-recognized terminology
   - add intent-led modifiers such as informational, commercial, transactional, solution-focused, feature-focused, and comparison terms
   - note any negative terms or exclusions

5) Use the Brainstorming tab structure.
   - Populate base phrases and modifiers in the same logic as the template
   - Keep modifier + base phrase and base phrase + modifier patterns distinct
   - Preserve or extend the flatten formula ranges if the brainstorm area grows

6) Use the Ahrefs app for evidence-backed expansion.
   Preferred patterns:
   - Use `keywords_explorer_volume_by_country` to validate market fit and country-level demand for promising seeds
   - Use `keywords_explorer_related_terms` for expansion
   - Start with `terms=also_rank_for` for practical keyword expansion
   - Use `select` fields that actually exist in the app response, such as `keyword,volume,difficulty,intents,cpc,traffic_potential`
   - Use `keywords_explorer_volume_history` when seasonality or trend movement matters
   - If a related-terms request fails, adjust `terms` or `select` rather than abandoning Ahrefs

7) Apply intent and viability judgment.
   - Match keyword intent to the requested page type
   - Blogs usually prioritize informational or comparison intent
   - Landing pages usually prioritize commercial, transactional, service, and solution-led intent
   - Flag mismatches where the SERP intent conflicts with the requested content type
   - Prefer terms with realistic competition relative to the client's authority and goals

8) Populate the template with useful structure, not just raw exports.
   Update the most relevant tabs:
   - `Existing keywords`: current rankings, GSC terms, or provided legacy terms if available
   - `Brainstorming`: seed terms, modifiers, and formula-driven combinations
   - `Overview`: top validated focus terms and high-level metrics
   - `matching`: useful matching terms or close variants
   - `related`: related/supporting terms and topical adjacencies
   - `questions`: question-led keyword opportunities
   - SERP tabs: only when one or two focus keywords deserve deeper competitor review

9) Keep the output decision-oriented.
   The completed research should make it easy to decide:
   - primary keyword
   - secondary/supporting keywords
   - likely content angle
   - whether the topic is viable for the specified market

10) Final QA.
   - Ensure the workbook is a copy or confirmed target, not the master template
   - Ensure the country setting used in Ahrefs matches the brief
   - Ensure the selected keywords match the intended content type
   - Ensure branded, irrelevant, or off-intent terms are either excluded or clearly flagged
   - Ensure the summary in chat matches the sheet contents

## TEMPLATE COPY RULE
When the user asks for the output as a copied template:
- Prefer copying the full source workbook by exporting the template spreadsheet and re-importing it as a new Google Sheet so formulas and tab structure are preserved
- Then update the new copy rather than altering the master template
- If the user provides an existing working sheet instead, update that sheet directly

## OUTPUT FORMAT
Return this structure after the sheet work is complete:

```text
Keyword research sheet:
[Link or status]

Primary keyword:

Secondary/supporting keywords:
- ...

Intent notes:
- ...

Opportunity/risk notes:
- ...

Next recommendation:
- ...
```

## EDGE CASES
- If no destination folder or sheet is confirmed, ask before creating or editing files
- If Ahrefs returns sparse or noisy expansions, say so and fall back to the strongest validated terms
- If the topic spans multiple distinct intents, recommend splitting it into more than one page
- If the user wants the workbook filled from Ahrefs exports they already have, import those into the appropriate tabs instead of redoing everything from scratch
