#!/usr/bin/env python3
"""Lint every SKILL.md under plugins/ against the Agent Skills spec and Anthropic's authoring limits.

Stdlib only. Usage: python3 -I scripts/lint_skills.py [root]
Exit 1 on errors; warnings don't fail the run.
"""

from __future__ import annotations

import pathlib
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOP_KEY_RE = re.compile(r"^([A-Za-z][\w-]*):\s*(.*)$")
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
MAX_BODY_LINES = 500
MAX_LISTING_CHARS = 1536  # description + when_to_use, as truncated in Claude Code's skill listing


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        m = TOP_KEY_RE.match(line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip("\"'")
    return fields, "\n".join(lines[end + 1:])


def lint(skill_md: pathlib.Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    parsed = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if parsed is None:
        return ["frontmatter missing or not closed on line 1"], warnings
    fm, body = parsed
    folder = skill_md.parent.name

    name = fm.get("name", "")
    if not name:
        errors.append("missing name")
    else:
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"name '{name}': lowercase letters, digits, single hyphens, max 64")
        if name != folder:
            errors.append(f"name '{name}' doesn't match folder '{folder}'")
        if "claude" in name or "anthropic" in name:
            errors.append(f"name '{name}' uses a reserved word")

    desc = fm.get("description", "")
    if not desc:
        errors.append("missing description")
    else:
        if len(desc) > 1024:
            errors.append(f"description is {len(desc)} chars (max 1024)")
        if re.search(r"<[a-zA-Z/][^>]*>", desc):
            errors.append("description contains an XML tag")
        if "use when" not in desc.lower():
            warnings.append("description has no 'Use when ...' trigger")
        if re.match(r"(?i)^(i|you|we)\b", desc):
            warnings.append("description should be third person")
        if len(desc) + len(fm.get("when_to_use", "")) > MAX_LISTING_CHARS:
            warnings.append("description + when_to_use exceed the 1536-char listing cut")

    body_lines = body.count("\n") + 1
    if body_lines > MAX_BODY_LINES:
        errors.append(f"body is {body_lines} lines (max {MAX_BODY_LINES}); move detail to references/")

    for target in LINK_RE.findall(body):
        path = target.split("#", 1)[0]
        if path and not (skill_md.parent / path).exists():
            errors.append(f"broken relative link: {target}")
    return errors, warnings


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skills = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    names: dict[str, pathlib.Path] = {}
    failed = False
    for skill in skills:
        rel = skill.relative_to(root)
        errors, warnings = lint(skill)
        fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
        name = fm[0].get("name", "") if fm else ""
        if name in names:
            errors.append(f"duplicate skill name, also in {names[name]} (clashes in flat installs like npx skills)")
        names[name] = rel
        for e in errors:
            print(f"ERROR {rel}: {e}")
        for w in warnings:
            print(f"warn  {rel}: {w}")
        failed |= bool(errors)
    print(f"{len(skills)} skills checked, {'FAILED' if failed else 'ok'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
