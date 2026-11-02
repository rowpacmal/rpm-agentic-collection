#!/usr/bin/env bash
# Read and write OpenProject work packages through its REST API v3 (rpm-openproject plugin).
#
# Configuration: OPEN_PROJECT_BASE_URL, OPEN_PROJECT_ACCESS_TOKEN, and optionally
# OPEN_PROJECT_READONLY. The first source that sets a variable wins:
#   1. the environment (already exported variables)
#   2. $OPEN_PROJECT_ENV_FILE, if set
#   3. <project root>/.env.local   (project root = git top level of the current dir)
#   4. ${XDG_CONFIG_HOME:-~/.config}/openproject/env   (a per-user default instance)
#
# The token is passed to curl over stdin, never on the command line, so it does
# not land in the process list or in shell history.
#
# Only GET, POST and PATCH exist here. There is deliberately no DELETE path:
# every destructive OpenProject API operation is an HTTP DELETE, so omitting the
# verb removes the capability rather than guarding it.
#
# Usage:
#   openproject.sh config                         # where config came from (token redacted)
#   openproject.sh projects                       # id, identifier, name
#   openproject.sh get    <path>                  # e.g. /api/v3/work_packages/363
#   openproject.sh post   <path> <json|@file|->
#   openproject.sh patch  <path> <json|@file|->
#   openproject.sh wp     <id>                    # one work package
#   openproject.sh children <id>                  # direct children of a work package
#   openproject.sh statuses                       # id -> name status list
#   openproject.sh boards                         # boards, with the sprint each one filters on
#   openproject.sh sprint <id> [status-id]        # work packages on a sprint board
#   openproject.sh status <id> <status-id>        # move a work package (handles lockVersion)
#   openproject.sh comment <id> <text>            # add a comment
#
# Set OPEN_PROJECT_READONLY=true to make every write fail closed.
set -euo pipefail

die() { printf '%s\n' "$*" >&2; exit 1; }

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
USER_ENV_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/openproject/env"
CONFIG_SOURCES=""

# Load KEY=value lines for our three variables only, without overriding values
# that are already set. Parsed, not sourced, so a config file can't run code.
load_env_file() {
  local file="$1" key value
  [ -f "$file" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line#export }"
    case "$line" in
      OPEN_PROJECT_BASE_URL=*|OPEN_PROJECT_ACCESS_TOKEN=*|OPEN_PROJECT_READONLY=*) ;;
      *) continue ;;
    esac
    key="${line%%=*}"
    value="${line#*=}"
    value="${value%$'\r'}"
    case "$value" in
      \"*\") value="${value#\"}"; value="${value%\"}" ;;
      \'*\') value="${value#\'}"; value="${value%\'}" ;;
    esac
    if [ -z "${!key:-}" ]; then
      printf -v "$key" '%s' "$value"
      export "$key"
    fi
  done < "$file"
  CONFIG_SOURCES="$CONFIG_SOURCES $file"
}

[ -n "${OPEN_PROJECT_ENV_FILE:-}" ] && load_env_file "$OPEN_PROJECT_ENV_FILE"
load_env_file "$PROJECT_ROOT/.env.local"
load_env_file "$USER_ENV_FILE"

[ -n "${OPEN_PROJECT_BASE_URL:-}" ] || die "OPEN_PROJECT_BASE_URL is not set. Add it to $PROJECT_ROOT/.env.local or $USER_ENV_FILE (see the openproject skill's Setup)."
[ -n "${OPEN_PROJECT_ACCESS_TOKEN:-}" ] || die "OPEN_PROJECT_ACCESS_TOKEN is not set. Add it to $PROJECT_ROOT/.env.local or $USER_ENV_FILE (see the openproject skill's Setup)."

BASE_URL="${OPEN_PROJECT_BASE_URL%/}"

# Refuse anything outside the v3 API surface, and refuse a path that tries to
# escape it with a scheme, a host, or traversal.
assert_api_path() {
  case "$1" in
    /api/v3/*) ;;
    *) die "Path must start with /api/v3/ (got: $1)" ;;
  esac
  case "$1" in
    *..*) die "Path must not contain '..' (got: $1)" ;;
    *//*) die "Path must not contain '//' (got: $1)" ;;
  esac
}

assert_writable() {
  case "${OPEN_PROJECT_READONLY:-false}" in
    true|TRUE|1|yes) die "OPEN_PROJECT_READONLY is set — refusing to $1." ;;
  esac
}

# Reads the body from a literal JSON string, @file, or - for stdin.
read_body() {
  case "$1" in
    -) cat ;;
    @*) cat "${1#@}" ;;
    *) printf '%s' "$1" ;;
  esac
}

# Percent-encodes an OpenProject filters array from name/value pairs.
encode_filters() {
  python3 -c 'import json,sys,urllib.parse
pairs = sys.argv[1:]
f = [{pairs[i]: {"operator": "=", "values": [pairs[i + 1]]}} for i in range(0, len(pairs), 2)]
print(urllib.parse.quote(json.dumps(f)))' "$@"
}

# curl with auth supplied via --config on stdin so the token never hits argv.
op_curl() {
  local method="$1" path="$2" body="${3-}"
  assert_api_path "$path"
  local args=(
    --silent --show-error --fail-with-body
    --request "$method"
    --header "Accept: application/json"
  )
  if [ -n "$body" ]; then
    args+=(--header "Content-Type: application/json" --data-binary "$body")
  fi
  printf 'url = "%s"\nuser = "apikey:%s"\n' "$BASE_URL$path" "$OPEN_PROJECT_ACCESS_TOKEN" \
    | curl "${args[@]}" --config -
}

json_get() { python3 -c 'import json,sys;d=json.load(sys.stdin);[d:=d[k] for k in sys.argv[1:]];print(d)' "$@"; }

cmd="${1:-}"
[ -n "$cmd" ] || die "Usage: openproject.sh <config|projects|get|post|patch|wp|children|statuses|boards|sprint|status|comment> ..."
shift

case "$cmd" in
  config)
    printf 'base url:  %s\n' "$BASE_URL"
    printf 'token:     set (%s chars, redacted)\n' "${#OPEN_PROJECT_ACCESS_TOKEN}"
    printf 'readonly:  %s\n' "${OPEN_PROJECT_READONLY:-false}"
    printf 'sources:  %s\n' "${CONFIG_SOURCES:- environment only}"
    ;;

  projects)
    op_curl GET "/api/v3/projects?pageSize=200" \
      | python3 -c 'import json,sys
for p in json.load(sys.stdin)["_embedded"]["elements"]:
    print("%5d  %-24s %s" % (p["id"], p["identifier"], p["name"]))'
    ;;

  get)
    [ $# -ge 1 ] || die "Usage: get <path>"
    op_curl GET "$1"
    ;;

  post)
    [ $# -ge 2 ] || die "Usage: post <path> <json|@file|->"
    assert_writable "POST $1"
    op_curl POST "$1" "$(read_body "$2")"
    ;;

  patch)
    [ $# -ge 2 ] || die "Usage: patch <path> <json|@file|->"
    assert_writable "PATCH $1"
    op_curl PATCH "$1" "$(read_body "$2")"
    ;;

  wp)
    [ $# -ge 1 ] || die "Usage: wp <id>"
    op_curl GET "/api/v3/work_packages/$1"
    ;;

  children)
    [ $# -ge 1 ] || die "Usage: children <id>"
    op_curl GET "/api/v3/work_packages?filters=%5B%7B%22parent%22%3A%7B%22operator%22%3A%22%3D%22%2C%22values%22%3A%5B%22$1%22%5D%7D%7D%5D&pageSize=100"
    ;;

  statuses)
    op_curl GET "/api/v3/statuses?pageSize=100" \
      | python3 -c 'import json,sys
for s in json.load(sys.stdin)["_embedded"]["elements"]:
    print("%4d  %s%s" % (s["id"], s["name"], "  (closed)" if s.get("isClosed") else ""))'
    ;;

  boards)
    op_curl GET "/api/v3/grids?pageSize=100" \
      | python3 -c 'import json,sys
for g in json.load(sys.stdin)["_embedded"]["elements"]:
    o = g.get("options") or {}
    if o.get("type") != "action":
        continue
    sprints = [v for f in o.get("filters", []) for v in f.get("sprint_id", {}).get("values", [])]
    cols = [w.get("options", {}).get("queryId") for w in g.get("widgets", [])]
    print("grid %-4s sprint %-4s %s" % (g["id"], ",".join(sprints) or "-", g.get("name")))
    print("          column queries: %s" % ", ".join(str(c) for c in cols if c))'
    ;;

  sprint)
    [ $# -ge 1 ] || die "Usage: sprint <sprint-id> [status-id]"
    if [ $# -ge 2 ]; then
      filters="$(encode_filters sprint "$1" status "$2")"
    else
      filters="$(encode_filters sprint "$1")"
    fi
    op_curl GET "/api/v3/work_packages?filters=$filters&pageSize=200" \
      | python3 -c 'import json,sys
d = json.load(sys.stdin)
print("total: %s" % d["total"])
for e in d["_embedded"]["elements"]:
    l = e["_links"]
    print("  #%-5s %-9s %-22s %-18s %s" % (
        e["id"], l["type"]["title"], l["status"]["title"],
        (l.get("assignee") or {}).get("title", "unassigned")[:18], e["subject"]))'
    ;;

  status)
    [ $# -ge 2 ] || die "Usage: status <work-package-id> <status-id>"
    assert_writable "change the status of work package $1"
    lock="$(op_curl GET "/api/v3/work_packages/$1" | json_get lockVersion)"
    op_curl PATCH "/api/v3/work_packages/$1" \
      "$(printf '{"lockVersion":%s,"_links":{"status":{"href":"/api/v3/statuses/%s"}}}' "$lock" "$2")"
    ;;

  comment)
    [ $# -ge 2 ] || die "Usage: comment <work-package-id> <text>"
    assert_writable "comment on work package $1"
    op_curl POST "/api/v3/work_packages/$1/activities" \
      "$(python3 -c 'import json,sys;print(json.dumps({"comment":{"raw":sys.argv[1]}}))' "$2")"
    ;;

  delete|DELETE|rm|destroy)
    die "This helper has no delete path. Destructive OpenProject operations are out of scope — do it in the web UI if you really mean it."
    ;;

  *)
    die "Unknown command: $cmd"
    ;;
esac
