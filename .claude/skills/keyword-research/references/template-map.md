# Keyword Research Template Map

Source spreadsheet:
- Title: `Keyword research sheet - template`
- URL: `https://docs.google.com/spreadsheets/d/1VFC1VrBhyeLEa7xcSzw0_jyrUj8CMR5ZxjgApqFTi04/edit`

## Workbook tabs
- `Existing keywords`
- `Brainstorming`
- `Overview`
- `matching`
- `related`
- `questions`
- `{keyword} - SERP`
- `{keyword 2 - SERP}`

## Intended use
- `Existing keywords`: current rankings, historical terms, GSC terms, or known target terms
- `Brainstorming`: base phrases, modifiers, combinations, and flattened export-ready lists
- `Overview`: summary or overview-level keyword metrics
- `matching`: close matching variations
- `related`: adjacent and supporting terms
- `questions`: question-led opportunities
- SERP tabs: deeper competitor review for one or two focus keywords

## Brainstorming tab logic
The SOP references these formula patterns:
- modifier + base phrase
- base phrase + modifier
- flatten ranges to create export-ready keyword lists

Important notes from the SOP:
- the flatten output ranges may need extending if the brainstorm grid grows
- keep the template logic intact rather than replacing it with a plain dump of keywords

## Preferred copy workflow
When the user wants a fresh working copy:
1. Export the source spreadsheet workbook.
2. Import it back into Google Drive as a new Google Sheet.
3. Rename it clearly for the client/topic.
4. Update the copied workbook, not the master template.

This approach is preferred because it preserves workbook structure, formulas, and the tab layout better than rebuilding the sheet from scratch.

## Destination rule
Before creating or updating a sheet, confirm:
- existing sheet to update
- new copied template
- target Google Drive folder if a new copy is needed

## Ahrefs app notes
Verified working patterns in this environment:
- `keywords_explorer_volume_by_country`
- `keywords_explorer_volume_history`
- `keywords_explorer_related_terms` with `terms=also_rank_for`

Use valid `select` fields such as:
- `keyword`
- `volume`
- `difficulty`
- `intents`
- `cpc`
- `traffic_potential`

If a related-terms request fails, adjust the `terms` mode or `select` fields and retry.
