# Parity Rules

## Canonical Source

- Canonical tree: `.agents/skills/<skill-name>`
- Mirror tree: `.claude/skills/<skill-name>`

## Files That Must Match

These paths are treated as shared and should be copied from `.agents` into `.claude`:

- `SKILL.md`
- `references/**`
- `scripts/**`
- `assets/**`

Verification compares file presence and file contents for the shared paths.

## Files That Stay Agent-Specific

- `.agents/skills/<skill-name>/agents/openai.yaml`

That file configures the OpenAI/Codex skill picker UI and is intentionally not required in `.claude`.

## Merge Guidance

- Make edits in the canonical `.agents` tree first.
- Re-run sync instead of manually copying files.
- Use `sync --delete` when files were removed or renamed in the canonical source.
- Run `verify` before opening a PR so missing mirrored paths are caught early.
