#!/usr/bin/env bash
# Run every local check: skill lint, hook tests, and Claude Code's own validator.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -I scripts/lint_skills.py .
python3 -I -m unittest discover -s tests -q

if command -v claude >/dev/null 2>&1; then
  claude plugin validate .
  for p in plugins/*/; do claude plugin validate "$p"; done
else
  echo "claude CLI not found, skipping 'claude plugin validate'" >&2
fi
