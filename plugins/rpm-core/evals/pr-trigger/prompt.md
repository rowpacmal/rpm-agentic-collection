---
description: Asking for a PR title and description should load the pull-request skill.
tags: [trigger, core3]
max_turns: 6
allowed_tools: [Skill, Read, Glob, Grep]
---

Write the PR title and description for my branch. It adds rate limiting (100 req/min per API key) to the public API, and I tested it with a new integration test. Just give me the text, don't push anything.
