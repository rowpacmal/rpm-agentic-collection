#!/usr/bin/env python3
"""PreToolUse guard for Write/Edit (rpm-security plugin).

Asks before writing a high-confidence secret (private keys, cloud and API tokens) into a
file, and before any edit to a local env file (.env, .env.local, .envrc), which may hold
real secrets. Templates such as .env.example are allowed.
Patterns are deliberately narrow to avoid false positives on ordinary code.
A developer guardrail, not a secret scanner: run gitleaks or trufflehog in CI for that.
Fails open on bad input.
"""

from __future__ import annotations

import json
import re
import sys

PATTERNS: list[tuple[str, str]] = [
    (r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----", "private key"),
    (r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b", "AWS access key id"),
    (r"\bgh[pousr]_[A-Za-z0-9]{36,}\b", "GitHub token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{60,}\b", "GitHub fine-grained token"),
    (r"\bsk-ant-[A-Za-z0-9_-]{32,}", "Anthropic API key"),
    (r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}", "OpenAI API key"),
    (r"\b[sr]k_live_[A-Za-z0-9]{20,}\b", "Stripe live key"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{20,}", "Slack token"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "Google API key"),
]


ENV_FILE = re.compile(r"(^|/)\.env(rc|(\.[\w-]+)*)$")
ENV_TEMPLATE = re.compile(r"\.(example|sample|template|dist|defaults)$")


def is_env_file(path: str) -> bool:
    return bool(ENV_FILE.search(path)) and not ENV_TEMPLATE.search(path)


def written_text(tool_input: dict) -> str:
    parts = [tool_input.get("content"), tool_input.get("new_string")]
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict):
            parts.append(edit.get("new_string"))
    return "\n".join(p for p in parts if isinstance(p, str))


def find_secret(text: str) -> str | None:
    for pattern, label in PATTERNS:
        if re.search(pattern, text):
            return label
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        tool_input = payload.get("tool_input") or {}
        path = str(tool_input.get("file_path") or "a file")
        label = find_secret(written_text(tool_input))
    except Exception:
        return 0
    if is_env_file(path):
        reason = f"{path} is a local env file, which may hold real secrets. Confirm the edit, or change the .env.example template instead."
    elif label:
        reason = f"this writes what looks like a {label} into {path}. Prefer an environment variable or a gitignored .env file."
    else:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"rpm-security secret guard: {reason}",
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
