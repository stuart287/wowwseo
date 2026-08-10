---
name: skill-scaffold-sync
description: Scaffold a new skill once, sync it into both `.agents/skills` and `.claude/skills`, and verify the mirrored file set before opening a PR.
---

# Skill Scaffold Sync

Use this skill when adding a new reusable skill to this repository and you need both agent variants created consistently without manual folder drift.

## Purpose

Create one canonical skill scaffold, mirror it into both skill trees, and verify that the mirrored paths stay in sync.

## Inputs

Required:
- Skill name in kebab-case.
- One-sentence description.
- Intended use case and primary workflow.

Recommended:
- Whether the skill needs `agents/openai.yaml`.
- Which references or scripts should ship with the skill.
- Example prompt for the default prompt field.

## Workflow

1. Confirm the skill name, purpose, and minimum file set.
2. Create the skill in `.agents/skills/<name>/`.
3. Mirror the same structure into `.claude/skills/<name>/`.
4. Add only the files that are genuinely part of the first release:
   - `SKILL.md`
   - optional `agents/openai.yaml`
   - `references/*`
   - optional `scripts/*`
5. Run `scripts/scaffold_skill.py --verify <name>` to confirm path parity between `.agents` and `.claude`.
6. If one tree intentionally differs, document the exception in the PR summary instead of leaving silent drift.

## Guardrails

- Prefer a minimal first scaffold over speculative folders.
- Keep shared references mirrored unless there is a deliberate platform-specific difference.
- Do not leave one variant half-created.
- If the skill depends on external templates or binaries, record where they come from and why they belong in the repo.

## Output Expectations

- A complete mirrored skill under both trees.
- A short verification summary listing missing or extra files, if any.
- Clear assumptions when a file exists in one tree only.

## Commands

- Create a new scaffold:

```bash
python3 .agents/skills/skill-scaffold-sync/scripts/scaffold_skill.py create \
  --name example-skill \
  --description "Describe what the skill does" \
  --prompt "Use $example-skill to help with ..."
```

- Verify mirrored file sets:

```bash
python3 .agents/skills/skill-scaffold-sync/scripts/scaffold_skill.py verify --name example-skill
```

## QA

- Confirm both trees contain the same relative paths.
- Confirm `SKILL.md` frontmatter matches the skill name and description.
- Confirm any `agents/openai.yaml` file has a usable display name and default prompt.
- Confirm referenced files actually exist.
