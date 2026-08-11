# LLM Audit References

This folder contains the operating materials for the `llm-audit` skill.

## Distilled References

- `audit-framework.md`: evidence hierarchy, scoring bands, judgement rules, recommendation patterns, and writing rules.
- `client-source-packs.md`: known Google Drive source packs and client-specific handling notes.
- `source-pack-guide.md`: local source-pack structure, workbook/doc handling rules, and patterns from the bundled examples.

## Local Source Packs

Use `source-packs/` when the task needs example audit files, workbook structures, report structure, AI info page structure, llms.txt structure, regional PEEC evidence, or raw prompt/chat exports.

- `Incubeta - AI Visibility Audit/`: local AI visibility audit example with data sheet, chat export, crawl export, completed report doc, AI info page, llms.txt draft, and regional PEEC source-domain workbooks for AU, DE, UAE, UK, and US.
- `Paradise Games AI LLM Audit/`: local folder supplied as a Paradise Games example pack, but its contained filenames are Incubeta-labelled. Verify the workbook/report contents before treating it as Paradise-specific evidence.

## Handling Rules

- Read this README before selecting local references.
- Use `source-pack-guide.md` before opening individual DOCX/XLSX files.
- Treat each source pack as confidential client evidence and never mix findings between clients.
- Inspect workbook sheet names and header rows before using data.
- Treat the AI Audit Data Sheet as the source of truth for scores and prompt outcomes.
- Treat completed audit documents as report-structure and style references, not as a replacement for the data sheet.
- Treat AI info pages and llms.txt files as implementation deliverables, not independent proof of visibility.
- Clearly label missing, stale, mismatched, or filename-conflicting evidence.
