#!/usr/bin/env python3
"""Validate skill structure, references, and cross-agent parity."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
AGENTS_ROOT = REPO_ROOT / ".agents" / "skills"
CLAUDE_ROOT = REPO_ROOT / ".claude" / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
TOP_HEADING_RE = re.compile(r"^#\s+.+$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_PATH_RE = re.compile(r"`((?:references|scripts|agents|\.agents|\.claude|[^`\s/][^`\n]*/)[^`\n]*)`")

SKILL_QA_REQUIRED_H2 = {"Purpose", "Workflow", "References"}
FRONTMATTER_KEYS = {"name", "description"}
IGNORED_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


@dataclass
class Finding:
    level: str
    skill: str
    source: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate skills under .agents/skills and .claude/skills."
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Optional list of skill folder names to validate. Defaults to all mirrored skills.",
    )
    return parser.parse_args()


def iter_skill_names(selected: list[str]) -> list[str]:
    names = {path.name for path in AGENTS_ROOT.iterdir() if path.is_dir()}
    names.update(path.name for path in CLAUDE_ROOT.iterdir() if path.is_dir())
    if selected:
        return sorted(dict.fromkeys(selected))
    return sorted(names)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def path_display(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def resolve_relative_targets(markdown_path: Path, text: str) -> list[tuple[str, Path]]:
    targets: list[tuple[str, Path]] = []

    for raw_target in MARKDOWN_LINK_RE.findall(text):
        target = raw_target.strip()
        if not target or "://" in target or target.startswith(("#", "mailto:", "/")):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0].strip()
        if not clean:
            continue
        targets.append((clean, (markdown_path.parent / clean).resolve()))

    for raw_target in CODE_PATH_RE.findall(text):
        target = raw_target.strip()
        if not target or target.startswith("/"):
            continue
        if target.endswith(tuple(IGNORED_SUFFIXES)):
            continue
        targets.append((target, (markdown_path.parent / target).resolve()))

    return targets


def validate_skill_markdown(skill_name: str, tree_root: Path, findings: list[Finding]) -> None:
    skill_dir = tree_root / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        findings.append(Finding("ERROR", skill_name, path_display(skill_dir), "Missing SKILL.md"))
        return

    text = skill_md.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    source = path_display(skill_md)

    if frontmatter is None:
        findings.append(Finding("ERROR", skill_name, source, "Missing YAML frontmatter"))
    else:
        missing = sorted(FRONTMATTER_KEYS - frontmatter.keys())
        for key in missing:
            findings.append(Finding("ERROR", skill_name, source, f"Frontmatter missing `{key}`"))
        if frontmatter.get("name") and frontmatter["name"] != skill_name:
            findings.append(
                Finding(
                    "ERROR",
                    skill_name,
                    source,
                    f"Frontmatter name `{frontmatter['name']}` does not match folder `{skill_name}`",
                )
            )
        description = frontmatter.get("description", "")
        if description and len(description.split()) < 8:
            findings.append(Finding("WARN", skill_name, source, "Description is unusually short"))

    if not TOP_HEADING_RE.search(text):
        findings.append(Finding("ERROR", skill_name, source, "Missing top-level `#` heading"))

    h2_sections = {match.group(1).strip() for match in H2_RE.finditer(text)}
    if not h2_sections:
        findings.append(Finding("ERROR", skill_name, source, "Missing `##` sections"))

    if skill_name == "skill-qa":
        for section in sorted(SKILL_QA_REQUIRED_H2 - h2_sections):
            findings.append(Finding("ERROR", skill_name, source, f"Missing required section `## {section}`"))

    for raw_target, resolved in resolve_relative_targets(skill_md, text):
        try:
            resolved.relative_to(REPO_ROOT)
        except ValueError:
            findings.append(
                Finding("ERROR", skill_name, source, f"Relative path escapes repo root: `{raw_target}`")
            )
            continue
        if not resolved.exists():
            findings.append(Finding("ERROR", skill_name, source, f"Broken relative path: `{raw_target}`"))


def validate_agent_metadata(skill_name: str, findings: list[Finding]) -> None:
    skill_dir = AGENTS_ROOT / skill_name
    if not skill_dir.exists():
        return
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        findings.append(
            Finding("ERROR", skill_name, path_display(skill_dir), "Missing `agents/openai.yaml` in .agents skill")
        )


def shared_files(skill_dir: Path) -> set[Path]:
    files: set[Path] = set()
    for path in skill_dir.rglob("*"):
        if path.is_file():
            rel = path.relative_to(skill_dir)
            if rel.parts and rel.parts[0] == "agents":
                continue
            files.add(rel)
    return files


def validate_parity(skill_name: str, findings: list[Finding]) -> None:
    agent_dir = AGENTS_ROOT / skill_name
    claude_dir = CLAUDE_ROOT / skill_name

    if not agent_dir.exists():
        findings.append(
            Finding("ERROR", skill_name, str(agent_dir.relative_to(REPO_ROOT)), "Missing mirrored .agents skill")
        )
        return
    if not claude_dir.exists():
        findings.append(
            Finding("ERROR", skill_name, str(claude_dir.relative_to(REPO_ROOT)), "Missing mirrored .claude skill")
        )
        return

    agent_files = shared_files(agent_dir)
    claude_files = shared_files(claude_dir)

    for rel in sorted(agent_files - claude_files):
        findings.append(Finding("ERROR", skill_name, path_display(agent_dir / rel), "Missing mirrored file in .claude"))
    for rel in sorted(claude_files - agent_files):
        findings.append(Finding("ERROR", skill_name, path_display(claude_dir / rel), "Missing mirrored file in .agents"))

    for rel in sorted(agent_files & claude_files):
        agent_text = (agent_dir / rel).read_text(encoding="utf-8")
        claude_text = (claude_dir / rel).read_text(encoding="utf-8")
        if agent_text != claude_text:
            findings.append(
                Finding(
                    "ERROR",
                    skill_name,
                    path_display(agent_dir / rel),
                    f"Shared file content differs from .claude counterpart `{path_display(claude_dir / rel)}`",
                )
            )


def print_findings(findings: list[Finding], checked: list[str]) -> int:
    exit_code = 0
    if not findings:
        print(f"OK: validated {len(checked)} skill(s) with no issues")
        return exit_code

    order = {"ERROR": 0, "WARN": 1}
    for finding in sorted(findings, key=lambda item: (order[item.level], item.skill, item.source, item.message)):
        print(f"{finding.level} [{finding.skill}] {finding.source}: {finding.message}")
        if finding.level == "ERROR":
            exit_code = 1
    if exit_code == 0:
        print(f"OK: validated {len(checked)} skill(s) with warnings only")
    return exit_code


def main() -> int:
    args = parse_args()
    checked = iter_skill_names(args.skills)
    findings: list[Finding] = []

    for skill_name in checked:
        validate_parity(skill_name, findings)
        validate_skill_markdown(skill_name, AGENTS_ROOT, findings)
        validate_skill_markdown(skill_name, CLAUDE_ROOT, findings)
        validate_agent_metadata(skill_name, findings)

    return print_findings(findings, checked)


if __name__ == "__main__":
    raise SystemExit(main())
