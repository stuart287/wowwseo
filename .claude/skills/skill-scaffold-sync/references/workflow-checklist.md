# Workflow Checklist

## Standard Create Flow

1. Pick a lowercase-hyphenated skill name.
2. Scaffold both variants from the canonical `.agents` tree:

```bash
python3 .agents/skills/skill-scaffold-sync/scripts/sync_skill_tree.py scaffold <skill-name> --description "When and why the skill should trigger."
```

3. Edit the canonical files in `.agents/skills/<skill-name>`.
4. Sync the shared files into `.claude/skills/<skill-name>`:

```bash
python3 .agents/skills/skill-scaffold-sync/scripts/sync_skill_tree.py sync <skill-name> --delete
```

5. Verify parity before commit or PR:

```bash
python3 .agents/skills/skill-scaffold-sync/scripts/sync_skill_tree.py verify <skill-name>
```

## Standard Update Flow

1. Change the canonical `.agents/skills/<skill-name>` files only.
2. Re-run `sync`.
3. Re-run `verify`.

## Pre-PR Checks

- Confirm `SKILL.md` matches the current workflow.
- Confirm shared files exist in both trees.
- Confirm `verify` exits cleanly.
- If the skill uses `.agents/skills/<skill-name>/agents/openai.yaml`, remember that file is `.agents`-only and is not mirrored into `.claude`.
