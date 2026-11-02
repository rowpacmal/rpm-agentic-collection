---
title: GitHub links
description: Read when looking for a source repo (skills, tools, MCP servers) or adding a new one. Repo, stars, what, and where we found it.
updated: 2026-11-02
---

# GitHub Links

Tracked GitHub repos for agentic coding: skills, tools, harnesses, references.
Stars checked via `gh api` on 2026-11-02.

**Source key**
- **chat**: shared directly in the team chat or added by hand
- **LI-design**: LinkedIn post "12 GitHub repos for polished UI" (Stanislav Beliaev), activity 7518668010459418624
- **LI-ctx**: LinkedIn post on `ctx` capability routing (André Lindenberg), activity 7467561625873698818
- **LI-codexsec**: LinkedIn post on the Codex Security CLI, including its "More Relevant Posts" section
- **fowler**: martinfowler.com article on SDD tools (Kiro, spec-kit, Tessl)
- **bun**: bun.com "Rewriting Bun in Rust" article
- **kg-pdf**: PDF linked from the @nicos_ai tweet (Karpathy loops, AgentHub, and knowledge graphs)
- **loop-zip**: `production-ai-app-ready` loop kit zips (v1 and v3) from Drive

## Mandatory

| Repo | ★ | What | Source |
|---|---|---|---|
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 228k | A single CLAUDE.md based on Karpathy's notes on LLM coding pitfalls | chat |

## Workflow, harness, methodology

| Repo | ★ | What | Source |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 311k | Agentic skills framework and dev methodology | chat |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 310k | Matt Pocock's skills for engineers | chat |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 295k | Harness optimization: skills, instincts, memory, security (formerly `everything-claude-code`) | chat, LI-codexsec |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 269k | Plugin-based agent harness (dev preview) | LI-codexsec |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 182k | Skill that pushes agents toward the simplest working solution | LI-codexsec |
| [github/spec-kit](https://github.com/github/spec-kit) | 145k | Spec-driven development toolkit | fowler, MS Learn |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 117k | Terse-output skill that claims to cut tokens by about 65%. Reference only, not in our distribution | chat |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 99k | Karpathy's autonomous experiment loop, the reference "ratchet loop" | kg-pdf |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 68k | Claude Code best practices | chat |
| [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) | 66k | Proxy that routes Claude Code and other harnesses to other providers (check ToS before use) | LI-codexsec |
| [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine) | 2.6k | Agents that learn from experience | chat |
| [AI-Builder-Club/skills](https://github.com/AI-Builder-Club/skills) | 1.3k | Codebase harness and loop engineer | chat |
| [stevesolun/ctx](https://github.com/stevesolun/ctx) | 589 | Picks a skill/agent/MCP bundle for a repo ("large catalog, small working set") | LI-ctx |
| [microsoft/Resource2Skill](https://github.com/microsoft/Resource2Skill) | 543 | Turns tutorials, articles, and code into executable skills | chat |
| [liza-mas/liza](https://github.com/liza-mas/liza) | 414 | Disciplined multi-agent coding system | chat |
| [RiyaParikh0112/vibe-coding-playbook](https://github.com/RiyaParikh0112/vibe-coding-playbook) | 381 | Vibe coding playbook (older; concepts still apply) | chat |
| [NickCrew/Claude-Cortex](https://github.com/NickCrew/Claude-Cortex/tree/main/skills/development-estimation) | 63 | `development-estimation` skill | chat |
| [plamen5rov/vibe-coding-playbook](https://github.com/plamen5rov/vibe-coding-playbook) | 25 | Vibe coding guide for Claude and OpenCode | chat |

## Memory and code knowledge graphs

| Repo | ★ | What | Source |
|---|---|---|---|
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 141k | Codebase as a queryable knowledge graph, with a `/graphify` skill (graphify.com) | chat |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | 30k | Persistent memory across agent sessions | LI-ctx, LI-codexsec |
| [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag) | 5.3k | Knowledge-graph RAG for monorepos | chat |

## Design and UI

| Repo | ★ | What | Source |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 187k | Official skills (frontend-design, web-artifacts, brand-guidelines, and more) | chat |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 144k | UI/UX rulebook skill, strong on accessibility | chat, LI-design |
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | 125k | DESIGN.md files based on brand design systems | LI-design |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 108k | Art direction, references, and a browser check | chat, LI-design |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | 105k | Local-first AI design workspace | LI-design |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 100k | Design commands and rules that catch AI-slop UI | LI-design |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | 53k | Skills for animation and UI detail | LI-design |
| [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | 51k | Animated React/Next components | LI-design |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 45k | Anti-AI-slop design skill with themes and checks | LI-design |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | 29k | Google's DESIGN.md spec plus a lint CLI (`npx @google/design.md lint`) | LI-design, DESIGN.md post |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | 18k | Official GSAP skills | LI-design |
| [oso95/scroll-world](https://github.com/oso95/scroll-world) | 11k | Skill for scroll-driven 3D landing pages | LI-design |
| [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev) | 6k | Transitions library and motion skill | chat |
| [DavidHDev/canvas-ui](https://github.com/DavidHDev/canvas-ui) | 5.3k | WebGL effects over live HTML | LI-design |

## Security and code review

| Repo | ★ | What | Source |
|---|---|---|---|
| [morluto/rea](https://github.com/morluto/rea) | 421k | Reverse-engineering MCP server | chat |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | 57k | Multi-phase security audit skill with independently verified, machine-readable findings (MIT) | chat |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 49k | Hybrid code review: deterministic pipelines plus an LLM | chat |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 44k | Router for reverse-engineering and pentest skills | LI-codexsec |
| [openai/codex-security](https://github.com/openai/codex-security) | 11k | Codex Security CLI/SDK: find, validate, and fix vulnerabilities (sends code to OpenAI) | LI-codexsec |
| [Kritt-ai/open-kritt](https://github.com/Kritt-ai/open-kritt) | 2.4k | Self-hosted multi-agent vulnerability research | chat |

## MCP servers

| Repo | ★ | What | Source |
|---|---|---|---|
| [upstash/context7](https://github.com/upstash/context7) | 64k | Up-to-date library docs for agents | loop-zip `.mcp.json` |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | 39k | Browser automation MCP | loop-zip `.mcp.json` |

## Local models and cost

| Repo | ★ | What | Source |
|---|---|---|---|
| [AlexsJones/llmfit](https://github.com/AlexsJones/llmfit) | 39k | Finds which models run on your hardware | chat |

## Reference and cookbooks

| Repo | ★ | What | Source |
|---|---|---|---|
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 54k | Includes the Knowledge Graph Construction cookbook | kg-pdf |

## Misc dev tools (from the Bun article)

| Repo | ★ | What | Source |
|---|---|---|---|
| [sharkdp/hyperfine](https://github.com/sharkdp/hyperfine) | 29k | CLI benchmarking | bun |
| [hatoo/oha](https://github.com/hatoo/oha) | 11k | HTTP load generator | bun |
| [googleprojectzero/fuzzilli](https://github.com/googleprojectzero/fuzzilli) | 2.4k | JS engine fuzzer | bun |

## Notes

- **AgentHub** (Karpathy, cited in kg-pdf): the original `karpathy/agenthub` repo is gone (404). Only unofficial mirrors remain, so it is not listed.
- **Not on GitHub**: Kiro (kiro.dev), Tessl, CodeRabbit, Penpot, motion.dev, GSAP core site.
- **Mentioned without a link**: "Concept Lab" design skill (comment on LI-design).
