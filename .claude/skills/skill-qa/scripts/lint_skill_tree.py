#!/usr/bin/env python3
"""Lint skill folders for required files, frontmatter, and mirrored path drift."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOTS = {
    ".agents": ROOT / ".agents" / "skills",
    ".claude": ROOT / ".claude" / "skills",
}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r"^(name|description):\s*(.+)$", re.MULTILINE)
TOP_HEADING_RE = re.compile(r"^#\s+.+$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")

REQUIRED_H2_BY_SKILL = {
    "skill-qa": {"Purpose", "Workflow", "References"},
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return {key: value.strip() for key, value in FIELD_RE.findall(match.group(1))}


def iter_skill_dirs(root: Path, skill_name: str | None) -> list[Path]:
    if skill_name:
        target = root / skill_name
        return [target] if target.exists() else []
    return sorted(path for path in root.iterdir() if path.is_dir())


def relative_files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
    }


def looks_like_local_path(candidate: str) -> bool:
    if not candidate or "\n" in candidate:
        return False
    if candidate.startswith(("http://", "https://", "/")):
        return False
    if any(char in candidate for char in "<>{}|*"):
        return False
    if candidate.endswith(("/", ".")):
        return False
    if " " in candidate:
        return False
    if candidate in {".agents", ".claude"}:
        return False
    if candidate.startswith((".agents/", ".claude/")):
        return True
    if candidate.startswith(("references/", "scripts/", "agents/")):
        return True
    suffix = Path(candidate).suffix
    return bool(suffix)


def resolve_candidate(skill_dir: Path, candidate: str) -> Path:
    if candidate.startswith((".agents/", ".claude/")):
        return (ROOT / candidate).resolve()
    root_reference = ROOT / candidate
    if candidate.startswith("references/") and root_reference.exists():
        return root_reference.resolve()
    return (skill_dir / candidate).resolve()


def check_links(skill_dir: Path, text: str) -> list[str]:
    errors: list[str] = []
    stripped = FENCED_BLOCK_RE.sub("", text)
    for candidate in INLINE_CODE_RE.findall(stripped):
        if not looks_like_local_path(candidate):
            continue
        path = resolve_candidate(skill_dir, candidate)
        if not path.exists():
            errors.append(f"broken local reference `{candidate}`")
    return errors


def lint_tree(skill_name: str | None) -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for label, root in SKILL_ROOTS.items():
        for skill_dir in iter_skill_dirs(root, skill_name):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                failures.append(f"{label}/{skill_dir.name}: missing SKILL.md")
                continue

            text = skill_file.read_text(encoding="utf-8")
            metadata = parse_frontmatter(text)
            if not metadata:
                failures.append(f"{label}/{skill_dir.name}: missing frontmatter")
            else:
                if metadata.get("name") != skill_dir.name:
                    failures.append(
                        f"{label}/{skill_dir.name}: frontmatter name `{metadata.get('name', '')}` does not match folder"
                    )
                if "description" not in metadata:
                    failures.append(f"{label}/{skill_dir.name}: missing frontmatter description")
            if not TOP_HEADING_RE.search(text):
                failures.append(f"{label}/{skill_dir.name}: missing top-level heading")
            h2_sections = {match.group(1).strip() for match in H2_RE.finditer(text)}
            if not h2_sections:
                failures.append(f"{label}/{skill_dir.name}: missing H2 sections")
            for section in sorted(REQUIRED_H2_BY_SKILL.get(skill_dir.name, set()) - h2_sections):
                failures.append(f"{label}/{skill_dir.name}: missing required section `## {section}`")

            for error in check_links(skill_dir, text):
                failures.append(f"{label}/{skill_dir.name}: {error}")

    agents_skills = {path.name for path in iter_skill_dirs(SKILL_ROOTS[".agents"], skill_name)}
    claude_skills = {path.name for path in iter_skill_dirs(SKILL_ROOTS[".claude"], skill_name)}

    for missing in sorted(agents_skills - claude_skills):
        failures.append(f"missing mirrored skill in .claude: {missing}")
    for missing in sorted(claude_skills - agents_skills):
        failures.append(f"missing mirrored skill in .agents: {missing}")

    for skill in sorted(agents_skills & claude_skills):
        agents_dir = SKILL_ROOTS[".agents"] / skill
        claude_dir = SKILL_ROOTS[".claude"] / skill
        agents_files = relative_files(agents_dir)
        claude_files = relative_files(claude_dir)
        only_agents = sorted(agents_files - claude_files)
        only_claude = sorted(claude_files - agents_files)
        if only_agents:
            warnings.append(f"{skill}: extra files in .agents: {', '.join(str(path) for path in only_agents)}")
        if only_claude:
            warnings.append(f"{skill}: extra files in .claude: {', '.join(str(path) for path in only_claude)}")
        if ("agents/openai.yaml" in {str(path) for path in only_agents}
                or "agents/openai.yaml" in {str(path) for path in only_claude}):
            failures.append(f"{skill}: mirrored trees disagree on agents/openai.yaml")

    for line in failures:
        print(f"ERROR: {line}")
    for line in warnings:
        print(f"WARN: {line}")

    if failures:
        return 1
    print("PASS: skill tree validation succeeded")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill")
    args = parser.parse_args()
    return lint_tree(args.skill)


if __name__ == "__main__":
    raise SystemExit(main())
