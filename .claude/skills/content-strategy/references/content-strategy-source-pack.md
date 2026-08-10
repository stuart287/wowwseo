# Content Strategy Source Pack

This reference distils the uploaded Content Strategy GPT / CustomGPT source pack into working rules for the skill. Use the original files in `source-documents/`, `templates/`, and `examples/` when exact source wording, workbook structure, or completed examples are needed.

## Source Authority

Use source materials in this order:

1. `source-documents/Master instruction set.docx`
2. `source-documents/Short SOP_ How to Use the Content Strategy Skill Pack _ CustomGPT.docx`
3. `source-documents/Content Idea Generation.docx`
4. `source-documents/Content Strategy Population.docx`
5. `templates/Content strategy + topic ideation template - make a copy (1).xlsx`
6. Example workbooks in `examples/`

The skill should behave as a content strategist and planner, not as a copywriter. It decides what content should be created or optimised, why it matters, how it should be prioritised, and how it should be tracked.

## Master Instruction Set

Core outputs must be:

- Commercially relevant.
- Search-intent aligned.
- Based on real SEO data wherever available.
- Easy to review and copy into the strategy template.
- Prioritised, not just brainstormed.

Always prioritise:

- Business relevance before raw search volume.
- SERP intent before preferred content format.
- Existing optimisation opportunities before duplicate net-new content.
- Clear assumptions and review notes when data is incomplete.

Task types:

- New content ideation: build ideas from client inputs, keyword research, topical maps, and competitor gaps.
- Optimisation opportunity finding: use Ahrefs rankings, GSC queries, content audits, and current URL performance.
- Refresh or decay recovery: identify pages losing traffic, rankings, or freshness.
- Cluster or hub expansion: group topics into pillars, support pages, and internal-link paths.
- Topic prioritisation: score existing ideas by intent, business fit, demand, difficulty, SERP reality, and effort.

## Short SOP

Use this skill when a team member needs:

- Topic ideas.
- Optimisation opportunities.
- Keyword-to-topic mapping.
- Cluster planning.
- Prioritised strategy tables.
- Strategy rows that can be copied into the workbook.
- Worklog-ready planning rows after strategy topics are approved.

Default output should be a table unless the user asks for narrative only. A good output is specific, cites the source data used, separates new content from optimisation, includes priority and funnel logic, and flags any assumptions.

Weak outputs usually list generic topics, overvalue search volume, ignore SERP intent, skip business fit, or omit missing-data caveats.

## Content Idea Generation

Use client inputs and Ahrefs when creating ideas from scratch:

- Extract products, services, features, use cases, buyer problems, buying triggers, and commercial priorities.
- Create brainstorm combinations using modifiers such as `best`, `top`, `price`, `cost`, `near me`, `South Africa`, `how to`, `vs`, `buy`, industry terms, location terms, and audience terms.
- Export Ahrefs Overview, Matching Terms, Questions, Related, and SERP data where available.
- Filter for intent match, relevant demand, traffic potential, achievable competition, and commercial relevance.
- Export SERP data for the strongest candidate keywords.

Use Google Search Console to find:

- Low CTR plus high impressions.
- Queries ranking without being properly covered in page copy.
- Queries with clicks but weak average position.
- New informational, commercial, or transactional topics implied by query data.

Use Ahrefs rankings to find:

- Quick wins in positions 4-10.
- Decaying top pages.
- Unintended rankings in positions 11-30.
- URL-level keyword clusters that justify supporting pages.
- Competitor content gaps.

Use Surfer:

- Topical Map for new sites, new niches, broad authority building, and pillar planning.
- Domain Map for established domains, adjacent expansion, gap discovery, and strengthening existing topical authority.

## Strategy Population

Populate rows only after the idea has a clear reason to exist. For each row:

- Write the content title as the likely H1 or page title.
- Assign the closest content type from the workbook options.
- Mark new content versus optimisation.
- Estimate difficulty from SERP competition, effort, content depth, backlinks, and client authority.
- Assign priority from intent, business relevance, demand, traffic potential, KD, SERP competitiveness, effort, and topical fit.
- Map funnel stage to TOFU, MOFU, BOFU, or evergreen based on the searcher's decision stage.
- Use a focused primary keyword rather than an overly broad parent term.
- Add related keywords only when they belong in the same page or article.
- Add top organic SERP results only; exclude ads, local packs, and unrelated SERP features unless the task is analysing those features.
- Add current URL/ranking data from Ahrefs and GSC when available.
- Add supporting blogs and landing pages after the topic is approved or when internal-link planning is part of the task.

Priority summary:

- High: strong business fit, correct intent, useful traffic potential or volume, feasible SERP, and clear cluster/internal-link value.
- Medium: relevant but less urgent, moderate demand or competition, or useful as supporting content.
- Low: weak commercial fit, SERP mismatch, low opportunity, high effort, or isolated topic.

## Workbook Pattern

Template workbook:

- `Ideas`: early topic ideation rows.
- `Strategy`: strategy summary rows with title, focus, keyword, SERP analysis, ranking, GSC, and support fields.
- `Worklog`: scheduling and delivery tracking.
- `Topics` or `New Topic Sheet Test`: detailed topic rows with Ahrefs-style fields.
- Keyword export tabs: Overview, Matching, Questions, Related, and similar Ahrefs exports.
- Timeline and TAM/traffic sheets can support planning but are not always populated.

Example workbooks:

- Incubeta shows roundup-led strategy, keyword brainstorm tabs, Ahrefs exports, URL exports, and filled roundup topic rows.
- Plum Plumbers shows local/service page strategy, page optimisation rows, worklog planning, client questions, URL suggestions, and delivery ownership.

When creating workbook-ready output, match the structure of the user's workbook if provided. If no workbook is provided, use the columns in `template-columns.md`.

## Worklog Rules

Suggest worklog rows when the user asks for scheduling, production planning, status tracking, or a strategy that is ready for implementation.

Worklog fields typically include:

- Month or planned date.
- Deliverable.
- Type.
- Status.
- Notes.
- Google Docs link.
- URL.
- Questions.
- Roles.

Use statuses such as planned, in progress, needs client review, uploaded, or published when they match the workbook.
