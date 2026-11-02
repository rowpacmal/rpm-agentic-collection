#!/usr/bin/env python3
"""PreToolUse guard for Bash commands (rpm-security plugin).

deny: catastrophic, almost never intended (wiping / or $HOME, mkfs, raw disk writes).
ask:  risky but sometimes legitimate; the user confirms in the permission prompt.

A developer guardrail, not a security boundary: it matches text, so it is easy to
bypass on purpose. Fails open on bad input so it never breaks a session.
"""

from __future__ import annotations

import json
import re
import shlex
import sys

PREFIXES = {"sudo", "doas", "env", "nohup", "time", "command", "exec", "xargs"}
DANGER_DIRS = re.compile(
    r"^(/|/\*|~|~/|~/\*|\$HOME|\$\{HOME\}|(\$HOME|\$\{HOME\})/\*?|\.\.|\.\./\*?"
    r"|/(bin|boot|dev|etc|home|lib\w*|opt|root|sbin|srv|sys|usr|var|Users|System|Applications)/?\*?)$"
)


def segments(command: str) -> list[str]:
    return [s for s in re.split(r"\|\||&&|[;|\n]", command) if s.strip()]


def command_tokens(segment: str) -> list[str]:
    try:
        tokens = shlex.split(segment)
    except ValueError:
        tokens = segment.split()
    while tokens and (tokens[0] in PREFIXES or "=" in tokens[0] or tokens[0].startswith("-")):
        tokens = tokens[1:]
    return tokens


ENV_FILE = re.compile(r"(^|/)\.env(\.[\w-]+)*$")
ENV_TEMPLATE = re.compile(r"\.(example|sample|template|dist|defaults)$")
READERS = {"cat", "less", "more", "head", "tail", "bat", "nl", "strings", "xxd", "od",
           "grep", "rg", "awk", "sed", "cut", "sort", "source", "."}


def check_env_read(segment: str) -> tuple[str, str] | None:
    tokens = command_tokens(segment)
    if not tokens or tokens[0].rsplit("/", 1)[-1] not in READERS:
        return None
    for tok in tokens[1:]:
        if ENV_FILE.search(tok) and not ENV_TEMPLATE.search(tok):
            return "ask", "prints a local env file, which may hold real secrets"
    return None


def check_rm(segment: str) -> tuple[str, str] | None:
    tokens = command_tokens(segment)
    if not tokens or tokens[0].rsplit("/", 1)[-1] != "rm":
        return None
    recursive = force = False
    targets: list[str] = []
    end_of_flags = False
    for tok in tokens[1:]:
        if end_of_flags or not tok.startswith("-") or tok == "-":
            targets.append(tok)
        elif tok == "--":
            end_of_flags = True
        elif tok.startswith("--"):
            recursive |= tok == "--recursive"
            force |= tok == "--force"
        else:
            recursive |= "r" in tok or "R" in tok
            force |= "f" in tok
    if recursive and any(DANGER_DIRS.match(t) for t in targets):
        return "deny", "recursive delete of /, home, a system dir, or a parent dir"
    if recursive and force:
        return "ask", "recursive force delete"
    return None


DENY: list[tuple[str, str]] = [
    (r"\bmkfs(\.\w+)?\b", "formatting a filesystem"),
    (r"\bdd\b[^;&|]*\bof=/dev/(sd|nvme|hd|disk|mmcblk)", "raw write to a disk device"),
    (r">\s*/dev/(sd|nvme|hd|disk|mmcblk)\w*", "redirect onto a disk device"),
    (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:", "fork bomb"),
    (r"\bchmod\s+(-[a-zA-Z]*R[a-zA-Z]*\s+)?[0-7]*777\s+/(\s|$)", "chmod 777 on /"),
]

ASK: list[tuple[str, str]] = [
    (r"\bgit\s+push\b[^;&|]*\s(--force(?!-with-lease|-if-includes)\b|-[a-zA-Z]*f\b)", "force push rewrites remote history"),
    (r"\bgit\s+push\b[^;&|]*\s(--delete\b|-d\b|:\S)", "deletes a remote branch or tag"),
    (r"\bgit\s+reset\s+[^;&|]*--hard\b", "git reset --hard discards uncommitted work"),
    (r"\bgit\s+clean\s+[^;&|]*-[a-zA-Z]*f", "git clean deletes untracked files"),
    (r"\bgit\s+(checkout|restore)\s+[^;&|]*(--\s+)?\.(\s|$)", "discards all local changes"),
    (r"\bgit\s+branch\s+[^;&|]*-D\b", "force-deletes a branch"),
    (r"\bgit\s+(filter-branch|filter-repo)\b", "rewrites history"),
    (r"\bgit\s+stash\s+(drop|clear)\b", "drops stashed work"),
    (r"\bsudo\b", "runs as root"),
    (r"\b(curl|wget)\b[^;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", "pipes a remote script into a shell"),
    (r"\b(eas)\s+(build|submit|update)\b", "uses EAS build or submit quota"),
    (r"\b(npm|pnpm|yarn|bun)\s+publish\b|\b(twine\s+upload|cargo\s+publish|gem\s+push)\b", "publishes a package"),
    (r"(?i)\b(DROP\s+(TABLE|DATABASE|SCHEMA)|TRUNCATE\s+TABLE)\b", "destructive SQL"),
    (r"\b(terraform|tofu)\s+(apply|destroy)\b|\bkubectl\s+delete\b", "changes live infrastructure"),
    (r"\bdocker\s+(system|volume)\s+prune\b|\bdocker\s+volume\s+rm\b", "deletes Docker volumes or data"),
    (r"\bdocker(-|\s+)compose\b[^;&|]*\bdown\b[^;&|]*\s(-v|--volumes)\b", "deletes Docker Compose volumes"),
]


def decide(command: str) -> tuple[str, str] | None:
    rm_results = [r for r in map(check_rm, segments(command)) if r]
    for result in rm_results:
        if result[0] == "deny":
            return result
    for pattern, reason in DENY:
        if re.search(pattern, command):
            return "deny", reason
    if rm_results:
        return rm_results[0]
    for pattern, reason in ASK:
        if re.search(pattern, command):
            return "ask", reason
    for result in map(check_env_read, segments(command)):
        if result:
            return result
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        command = payload.get("tool_input", {}).get("command", "")
    except Exception:
        return 0
    if not isinstance(command, str) or not command:
        return 0

    result = decide(command)
    if result is None:
        return 0
    decision, reason = result
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": f"rpm-security bash guard: {reason}.",
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
