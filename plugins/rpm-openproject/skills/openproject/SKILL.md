---
name: openproject
description: Reads and updates OpenProject work packages (tickets, features, tasks, bugs) on any OpenProject instance through its REST API v3. Lists sprints and boards, shows a ticket and its children, moves status, and adds comments. Never deletes. Use when the user mentions a ticket number like #363, asks what's queued or in the sprint, or wants a ticket's status or comments updated.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh config) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh projects) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh statuses) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh boards) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh wp *) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh children *) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh sprint *) Bash(${CLAUDE_SKILL_DIR}/scripts/openproject.sh get *)
license: MIT
metadata:
  sources: "OpenProject API v3 docs"
---

# OpenProject

Reach OpenProject only through the helper `${CLAUDE_SKILL_DIR}/scripts/openproject.sh` (outside Claude Code: `scripts/openproject.sh` in this skill's folder).
Don't hand-roll `curl` calls. The helper keeps the token out of argv, restricts paths to `/api/v3/`, and has no delete path.

## Setup

The helper reads `OPEN_PROJECT_BASE_URL`, `OPEN_PROJECT_ACCESS_TOKEN`, and optionally `OPEN_PROJECT_READONLY`. The first source that sets a variable wins:

1. variables already exported in the environment
2. the file named by `$OPEN_PROJECT_ENV_FILE`
3. `<project root>/.env.local`, for a per-project instance (must be gitignored)
4. `~/.config/openproject/env`, for your default instance across projects

```bash
OPEN_PROJECT_BASE_URL=https://openproject.example.com   # no trailing slash, no /api/v3
OPEN_PROJECT_ACCESS_TOKEN=...                           # My Account → Access tokens → API
OPEN_PROJECT_READONLY=false                             # true = every write fails closed
```

Run `openproject.sh config` to see which instance and files are in use. It prints the token redacted.
**Never** `cat` these files, echo the token, or put it in a command. If config is missing, tell the user which file to create. Don't ask them to paste the token into the chat.

## Commands

```bash
openproject.sh config                  # instance, sources, readonly (token redacted)
openproject.sh projects                # id, identifier, name
openproject.sh statuses                # status id -> name, closed flag
openproject.sh boards                  # boards and the sprint id each filters on
openproject.sh sprint 17 [status-id]   # work packages on a sprint
openproject.sh wp 363                  # one work package (full JSON)
openproject.sh children 363            # direct children of a feature
openproject.sh get /api/v3/<path>      # any GET
openproject.sh status 363 22           # move status (handles lockVersion)
openproject.sh comment 363 "text"      # add a comment
openproject.sh post|patch /api/v3/<path> <json|@file|->
```

Responses are raw JSON and mostly `_links`, so pull out only the fields you need with `python3 -c` or `jq`.
Status ids differ per instance. Run `statuses` first instead of guessing.

- Sprints and boards, a common trap: [references/sprints-and-boards.md](references/sprints-and-boards.md)
- Creating work packages and other writes: [references/writes.md](references/writes.md)

## Rules

Allowed without asking: any read, plus moving the status of, or commenting on, a ticket the user named.

Confirm the exact ticket list first:
- bulk status changes
- closing a parent feature
- anything on tickets the user didn't name
- creating work packages
- editing a subject or description

Never:
- **Delete.** The helper has no DELETE path. Don't work around it with raw `curl`. Tell the user to delete in the web UI.
- Change assignees, versions, or project membership unless asked.

Project conventions (which status means "ready for review", ticket ids in branch names or commits, plan docs) belong in the project's AGENTS.md or CLAUDE.md. Follow them when present.
