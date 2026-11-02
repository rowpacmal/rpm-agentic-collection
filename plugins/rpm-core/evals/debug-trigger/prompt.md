---
description: A flaky failure should start with building a reproducible loop.
tags: [trigger, core2]
max_turns: 8
allowed_tools: [Skill, Read, Glob, Grep]
---

Our checkout test fails maybe 1 in 10 runs on CI with 'expected total 42.00, got 41.99'. Help me debug it.
