#!/usr/bin/env python3
"""Scaffold, sync, and verify mirrored skill folders."""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
from pathlib import Path


SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
SHARED_ROOTS = ("references", "scripts", "assets")
CANONICAL_ONLY_FILES = {Path("agents/openai.yaml")}


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".agents/skills").is_dir() and (candidate / ".claude/skills").is_dir():
            return candidate
    raise RuntimeError("Could not find repo root containing both .agents/skills and .claude/skills")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
AGENTS_ROOT = REPO_ROOT / ".agents/skills"
CLAUDE_ROOT = REPO_ROOT / ".claude/skills"


def validate_skill_name(name: str) -> None:
    if not SKILL_NAME_RE.fullmatch(name):
        raise SystemExit(
            f"Invalid skill name '{name}'. Use lowercase letters, digits, and hyphens only."
        )


def canonical_dir(skill_name: str) -> Path:
    return AGENTS_ROOT / skill_name


def mirror_dir(skill_name: str) -> Path:
    return CLAUDE_ROOT / skill_name


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def skill_title(skill_name: str) -> str:
    return skill_name.replace("-", " ").title()


def scaffold_skill(args: argparse.Namespace) -> int:
    validate_skill_name(args.skill_name)
    source_dir = canonical_dir(args.skill_name)
    target_dir = mirror_dir(args.skill_name)

    if (source_dir.exists() or target_dir.exists()) and not args.force:
        raise SystemExit(
            f"Skill '{args.skill_name}' already exists. Use --force only if you intend to replace stub files."
        )

    display_name = args.display_name or skill_title(args.skill_name)
    description = args.description.strip()
    prompt = (
        args.default_prompt.strip()
        if args.default_prompt
        else f"Use ${args.skill_name} to {description[0].lower() + description[1:]}"
    )

    skill_md = f"""---
name: {args.skill_name}
description: {description}
---

# {display_name}

## Purpose

Describe what this skill should accomplish and when to use it.

## Inputs

- Add the required inputs here.
- Add optional context that improves the output.

## Core Workflow

1. Replace this scaffold with the real workflow.
2. Keep shared instructions in the canonical `.agents` tree.
3. Re-run the scaffold/sync helper after meaningful updates.

## References

- Add reference files under `references/` as the workflow grows.
"""

    openai_yaml = (
        "interface:\n"
        f'  display_name: "{display_name}"\n'
        f'  short_description: "{description}"\n'
        f'  default_prompt: "{prompt}"\n'
    )

    notes_md = f"""# {display_name} Notes

- Canonical source: `.agents/skills/{args.skill_name}`
- Mirror target: `.claude/skills/{args.skill_name}`
- Update the canonical files first, then run the sync helper.
"""

    for folder in (source_dir / "agents", source_dir / "references", source_dir / "scripts"):
        folder.mkdir(parents=True, exist_ok=True)

    write_text(source_dir / "SKILL.md", skill_md, overwrite=args.force)
    write_text(source_dir / "agents/openai.yaml", openai_yaml, overwrite=args.force)
    write_text(source_dir / "references/notes.md", notes_md, overwrite=args.force)

    sync_skill(args.skill_name, delete=args.delete)
    print(
        f"Scaffolded {args.skill_name} in {source_dir.relative_to(REPO_ROOT)} and "
        f"{target_dir.relative_to(REPO_ROOT)}"
    )
    return 0


def iter_shared_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    skill_md = source_dir / "SKILL.md"
    if skill_md.exists():
        files.append(skill_md)
    for root_name in SHARED_ROOTS:
        root = source_dir / root_name
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file():
                files.append(path)
    return files


def sync_skill(skill_name: str, *, delete: bool) -> list[Path]:
    validate_skill_name(skill_name)
    source_dir = canonical_dir(skill_name)
    target_dir = mirror_dir(skill_name)

    if not source_dir.is_dir():
        raise SystemExit(f"Canonical skill does not exist: {source_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    expected_relpaths: set[Path] = set()

    for source_file in iter_shared_files(source_dir):
        relpath = source_file.relative_to(source_dir)
        expected_relpaths.add(relpath)
        target_file = target_dir / relpath
        ensure_parent(target_file)
        shutil.copy2(source_file, target_file)
        copied.append(relpath)

    if delete:
        for target_file in sorted(path for path in target_dir.rglob("*") if path.is_file()):
            relpath = target_file.relative_to(target_dir)
            if relpath not in expected_relpaths:
                target_file.unlink()
        prune_empty_dirs(target_dir)

    return copied


def prune_empty_dirs(root: Path) -> None:
    for path in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            continue


def verify_skill(skill_name: str) -> list[str]:
    validate_skill_name(skill_name)
    source_dir = canonical_dir(skill_name)
    target_dir = mirror_dir(skill_name)
    issues: list[str] = []

    if not source_dir.is_dir():
        return [f"Missing canonical skill: {source_dir.relative_to(REPO_ROOT)}"]
    if not target_dir.is_dir():
        return [f"Missing mirror skill: {target_dir.relative_to(REPO_ROOT)}"]

    source_files = {path.relative_to(source_dir) for path in iter_shared_files(source_dir)}
    target_files = {
        path.relative_to(target_dir)
        for path in target_dir.rglob("*")
        if path.is_file() and path.relative_to(target_dir) not in CANONICAL_ONLY_FILES
    }

    missing_in_target = sorted(source_files - target_files)
    extra_in_target = sorted(target_files - source_files)

    for relpath in missing_in_target:
        issues.append(f"{skill_name}: missing mirrored file {relpath.as_posix()}")
    for relpath in extra_in_target:
        issues.append(f"{skill_name}: unexpected mirrored file {relpath.as_posix()}")

    for relpath in sorted(source_files & target_files):
        source_file = source_dir / relpath
        target_file = target_dir / relpath
        if not filecmp.cmp(source_file, target_file, shallow=False):
            issues.append(f"{skill_name}: content mismatch for {relpath.as_posix()}")

    return issues


def cmd_sync(args: argparse.Namespace) -> int:
    copied = sync_skill(args.skill_name, delete=args.delete)
    print(f"Synced {args.skill_name}: {len(copied)} shared file(s) copied")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    skill_names = args.skill_names or sorted(
        {path.name for path in AGENTS_ROOT.iterdir() if path.is_dir()}
        | {path.name for path in CLAUDE_ROOT.iterdir() if path.is_dir()}
    )

    all_issues: list[str] = []
    for skill_name in skill_names:
        validate_skill_name(skill_name)
        all_issues.extend(verify_skill(skill_name))

    if all_issues:
        for issue in all_issues:
            print(issue)
        print(f"Verification failed: {len(all_issues)} issue(s)")
        return 1

    print(f"Verification passed for {', '.join(skill_names)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold, sync, and verify mirrored skills across .agents and .claude trees."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold = subparsers.add_parser("scaffold", help="Create a new mirrored skill scaffold")
    scaffold.add_argument("skill_name")
    scaffold.add_argument("--description", required=True, help="Frontmatter description for the skill")
    scaffold.add_argument("--display-name", help="UI display name for agents/openai.yaml")
    scaffold.add_argument("--default-prompt", help="Default prompt for agents/openai.yaml")
    scaffold.add_argument("--delete", action="store_true", help="Delete stale mirror files during initial sync")
    scaffold.add_argument("--force", action="store_true", help="Allow overwriting stub files if they already exist")
    scaffold.set_defaults(func=scaffold_skill)

    sync = subparsers.add_parser("sync", help="Copy shared files from .agents into .claude")
    sync.add_argument("skill_name")
    sync.add_argument("--delete", action="store_true", help="Delete mirror files that no longer exist canonically")
    sync.set_defaults(func=cmd_sync)

    verify = subparsers.add_parser("verify", help="Check mirrored path and content parity")
    verify.add_argument("skill_names", nargs="*", help="Specific skill names to verify; defaults to all")
    verify.set_defaults(func=cmd_verify)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
