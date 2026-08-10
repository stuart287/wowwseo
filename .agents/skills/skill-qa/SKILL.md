---
name: skill-qa
description: Validate skill folders before a PR by checking frontmatter, mirrored paths, required files, and broken local references.
---

# Skill QA

Use this skill when a skill has been added or changed in this repository and you want a repeatable pre-PR validation pass instead of manual spot checks.

## Purpose

Catch structural mistakes in skill folders before review.

## Inputs

Required:
- The skill name or the skill folder path to review.

Recommended:
- Whether the check should cover one skill or the whole tree.
- Whether mirrored `.agents` and `.claude` paths are expected to be identical.

## Workflow

1. Identify the target skill or decide to lint the whole tree.
2. Run `scripts/lint_skill_tree.py`.
3. Review failures in this order:
   - missing `SKILL.md`
   - invalid or missing frontmatter fields
   - missing mirrored files
   - broken relative references
   - missing `agents/openai.yaml` when the skill expects one
4. Fix the blockers before opening or updating the PR.
5. Summarize the remaining warnings separately from true blockers.

## Checks

- `SKILL.md` exists for every skill.
- Frontmatter includes `name` and `description`.
- The `name` field matches the folder name.
- Any referenced local files exist.
- Mirrored `.agents` and `.claude` skills have the same file paths unless deliberately excluded.
- `agents/openai.yaml` is structurally present when included in one mirrored tree.

## Commands

```bash
python3 .agents/skills/skill-qa/scripts/lint_skill_tree.py
python3 .agents/skills/skill-qa/scripts/lint_skill_tree.py --skill technical-audit
```

## Output Expectations

- A short error list for blockers.
- A warning list for drift that is documented but not fatal.
- A clear pass/fail result.

## References

- Read `references/validation-rules.md` before changing the release checks or relaxing a blocker.

## QA

- Treat missing mirrored files as a blocker unless the difference is documented.
- Re-run after fixes so the PR contains a clean validation result.
