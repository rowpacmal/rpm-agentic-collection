---
name: dependency-review
description: Reviews a dependency change before it lands. Checks the need, maintenance, license, size, install scripts and supply-chain risk, version compatibility with the framework (Expo SDK, React Native, Node), lockfile sync, patches, and duplicate versions across workspaces. Reports only, never edits. Use when adding, upgrading, or removing a package, when package.json, a lockfile, or another manifest changes, or when the user asks whether to use a library.
argument-hint: "[package | base ref]"
license: MIT
metadata:
  sources: "OpenSSF guidance"
---

# Dependency review

Report findings. Don't install, upgrade, or edit anything unless asked.

## Scope

Find what changed: `git diff <base> -- '*package.json' '*lock*' '*requirements*.txt' pyproject.toml Cargo.toml go.mod patches/ app.json app.config.*`.
For a proposed package that isn't installed yet, review it by name.

## Checks

**Need**
- Does the project or the standard library already do this? A few lines of code beat a new dependency for small jobs.
- Is it the right kind: a runtime dependency or a dev dependency?

**Health and trust** (`npm view <pkg> version time.modified license repository maintainers`, or the registry page)
- Maintained recently, with a real source repository.
- The license fits the project (watch for GPL/AGPL in proprietary apps).
- The name is exactly right. Typosquats and look-alike scopes are common.
- Install scripts (`preinstall`, `install`, `postinstall`) run code on every machine. Flag any new one.
- A new maintainer or a sudden major release in a tiny package deserves a second look.

**Fit**
- Compatible with the framework version. For Expo, versions must match the SDK: run `npx expo install --check`. For React Native native modules, check that the native config or config plugin is set up.
- Engines and peer dependencies match the project's Node, Python, or runtime version.
- Bundle or install size is reasonable for what it does, especially in mobile and web clients.

**Consistency**
- The lockfile is updated and in sync with the manifest (`npm ci` or the equivalent succeeds).
- The same package isn't pinned to different versions across workspaces without a reason (`npm ls <pkg>`, `pnpm why <pkg>`).
- Patched packages (`patches/`): a version bump needs the patch re-checked.
- Known vulnerabilities: `npm audit --omit=dev` (or `pnpm audit`, `pip-audit`, `cargo audit`). Report high and critical only, with the fix version.

## Report

One line per finding, most serious first:

```
[HIGH] expo-camera 16.1 needs Expo SDK 54; the project is on 53 (package.json:31). Fix: `npx expo install expo-camera`.
```

Severities: HIGH (breaks the build, security risk, license problem), MEDIUM (drift, size, maintenance worry), LOW (style or preference).
If nothing is wrong, say so in one line, and list what you checked.
