# Proven prompt pack

## Populate an audit from data collection

```text
Populate the Mini SEO Audit using only the supplied data-collection sources and the approved Mini SEO Audit framework.

Before editing, create a coverage map for every required audit section. Treat the framework as structural authority and the client data as factual authority. Do not invent figures, claims, competitor facts, or links. Preserve the existing Google Doc’s headings, tables, links, formatting, and non-targeted content.

For each section: state the evidence-led finding, explain the SEO/business implication, then give a prioritised and implementable recommendation. Replace placeholders only in their confirmed body sections: locate them using the surrounding section heading and paragraph/table context, never by the first global occurrence. Use small verified edit batches; re-read after every substantive write.

Also update/create the linked content strategy and worklog with the source links, evidence collected, decisions, open gaps, owner and next step. Finish with a readback QA: confirm all required content is present, all stale reference-client wording and placeholders are absent, all material figures reconcile to the source data, and the document remains readable.

Inputs:
- Client/site: [CLIENT + DOMAIN]
- Working audit: [GOOGLE DOC URL]
- Framework: [GOOGLE DOC URL]
- Data collection: [SHEET/FOLDER URLS]
- Approved competitors: [LIST]
- Content strategy/worklog: [URL OR CREATE]
```

## Content strategy

```text
Use the approved keyword research, sitemap and Mini SEO Audit findings to populate the content strategy. Produce a practical priority backlog—not generic ideas. For every item include: title/topic, primary keyword or demand signal, intent, format/page type, priority, supporting/target URL, internal-link destination, and promotion or outreach angle where appropriate. Only propose pages the client can credibly support; flag gaps as TBD. Re-read the completed document and confirm every required row/section is populated.
```

## Worklog

```text
Create/update the Mini SEO Audit worklog from the audit activity. Record sources consulted, data-collection work completed, document edits made, decisions, evidence gaps, owner and next action. Link each entry to the relevant audit or source document. Keep it factual and operational; do not present planned work as completed.
```

## Final QA / near-flawless execution prompt

```text
Act as the Mini SEO Audit delivery owner. Produce a client-ready audit and its linked content strategy/worklog from the supplied framework and evidence pack.

1) Ground the target: confirm client, domain, working document, framework, approved competitors, content-strategy/worklog destinations and audit date.
2) Inventory the framework section by section and build a coverage map with required evidence, destination and verification check.
3) Collect and reconcile the evidence before drafting. The framework controls structure; live client sources control facts. Mark genuinely unavailable evidence as TBD—never guess.
4) Draft every section as evidence → implication → prioritised action. Tie each recommendation to a verified finding, include dependencies/caveats where material, and avoid generic SEO filler.
5) Populate safely: inspect the current body section/table context; target placeholders by section anchor and instance; replace only confirmed ranges; make small batches; re-read after every write. Preserve all non-targeted structure and styling. When stale template prose exists, replace the whole relevant block with client-specific content rather than deleting a marker.
6) Build/update the content strategy with demand, intent, format, priority, target/internal-link URL and promotion angle; build/update the worklog with sources, work completed, decisions, gaps, owner and next action.
7) Complete a two-sided QA readback: prove the new required content is present AND prove placeholders, old-client names, stale competitor references and unsupported claims are absent. Reconcile material numbers to source data; verify linked outputs; inspect tables/headings for layout issues.

Do not declare completion until all coverage-map checks pass. Return a short handoff containing the audit URL, content strategy/worklog URL, evidence gaps, and the highest-priority actions.

Inputs: [CLIENT/DOMAIN] [WORKING AUDIT URL] [FRAMEWORK URL] [DATA SOURCES] [APPROVED COMPETITORS] [CONTENT STRATEGY/WORKLOG URLS]
```
