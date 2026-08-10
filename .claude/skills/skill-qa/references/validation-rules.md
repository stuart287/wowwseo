# Skill QA Validation Rules

Use these rules when interpreting validator output or adjusting the skill QA workflow.

## Release Gate

A skill is release-ready only when the validator returns exit code `0` for the requested scope.

## Required Structure

Every `SKILL.md` should include:

1. YAML frontmatter bounded by `---`.
2. `name` and `description` fields in frontmatter.
3. A single top-level `#` heading near the start of the file.
4. At least one H2 section.

## Required H2 Sections

The validator currently requires these sections for `skill-qa` because it is an operational workflow skill:

- `## Purpose`
- `## Workflow`
- `## References`

All other skills are checked for a top-level heading plus at least one H2, but they are not forced onto a generic template.

## Link and Path Rules

- Relative markdown links must resolve from the markdown file that contains them.
- Backticked repo-local paths like `references/foo.md`, `scripts/bar.py`, or `agents/openai.yaml` must also resolve.
- HTTP, HTTPS, anchor-only, and absolute filesystem paths are ignored by the relative-path checks.

## Cross-Agent Parity

- Shared files under `.agents/skills/<skill>` and `.claude/skills/<skill>` should match exactly.
- The `agents/` subdirectory is agent-only and is excluded from parity checks.
- Missing files in either mirrored tree are release blockers unless the skill is intentionally single-platform.

## Warning Policy

Warnings are suitable for style drift or weak descriptions that do not block execution.
Errors should be used for anything that breaks discoverability, execution, or mirrored maintenance.
