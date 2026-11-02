#!/usr/bin/env bash
# Copy the rpm project template into a project. Never overwrites existing files.
# Usage: scripts/init-project.sh <project-dir> [--design] [--testing]
#   --design   also enable the rpm-design plugin
#   --testing  also enable the rpm-testing plugin
set -euo pipefail

src="$(cd "$(dirname "$0")/../templates/project" && pwd)"
dest="${1:?usage: init-project.sh <project-dir> [--design] [--testing]}"
[ -d "$dest" ] || { echo "not a directory: $dest" >&2; exit 1; }

cd "$src"
find . -type f | while read -r f; do
  target="$dest/${f#./}"
  if [ -e "$target" ]; then
    echo "skip   ${f#./} (exists, merge by hand)"
  else
    mkdir -p "$(dirname "$target")"
    cp "$f" "$target"
    echo "create ${f#./}"
  fi
done

shift
for flag in "$@"; do
  case "$flag" in
    --design) plugin=rpm-design ;;
    --testing) plugin=rpm-testing ;;
    *) echo "unknown option: $flag" >&2; exit 1 ;;
  esac
  python3 -I - "$dest/.claude/settings.json" "$plugin" <<'PY'
import json, sys
path, plugin = sys.argv[1], sys.argv[2]
with open(path) as f:
    data = json.load(f)
data.setdefault("enabledPlugins", {})[f"{plugin}@rpm"] = True
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"enable {plugin}")
PY
done

echo "Next: fill in the TODOs in AGENTS.md, then commit."
