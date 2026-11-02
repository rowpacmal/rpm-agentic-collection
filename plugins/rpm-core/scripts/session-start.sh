#!/usr/bin/env bash
# SessionStart hook: injects the coding-guidelines skill body as always-on context.
# Plain stdout from a SessionStart hook is added to Claude's context.
set -u
skill="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}/skills/coding-guidelines/SKILL.md"
[ -r "$skill" ] || exit 0

echo "<rpm-core-guidelines>"
echo "Always-on rules from the rpm-core plugin. Project instructions (CLAUDE.md, AGENTS.md) take precedence where they conflict."
# Strip the YAML frontmatter (everything up to the second '---' line).
awk 'f>=2 {print; next} /^---[[:space:]]*$/ {f++}' "$skill"
echo "</rpm-core-guidelines>"
