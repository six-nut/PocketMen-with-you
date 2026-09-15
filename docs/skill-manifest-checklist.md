# Codex plugin packaging decision

Date: 2026-09-15. Maintainer: six-nut. Design investigation for #5.

## Decision

Defer plugin distribution; retain the existing Skill and Python CLI for v0.3.
A plugin could improve discovery and versioned installation, but does not replace
Python runtime or GPU/model setup. Ship only after the three follow-ups below pass.
This is a proposed design, not an already available plugin.

The issue's original hatch-pet/imagegen delegation proposal is superseded by the
v0.3 architecture and AGENTS.md: use the bundled local engine, default
FLUX.2-klein-4B, optional Qwen-Image-Edit-2511, and deterministic fallback.
Normal generation remains independent of OPENAI_API_KEY.

## Proposed layout

```text
pocketmen-with-you/
  .codex-plugin/plugin.json
  skills/pocketmen-with-you/
    SKILL.md
    scripts/
    references/
    runtime/pocketmen/
  LICENSE
  NOTICE.md
```

The manifest is `.codex-plugin/plugin.json`, not `skill.json`. Its name is
`pocketmen-with-you`, version matches the Python release, author.name is `six-nut`,
license is MIT, and skills points to `./skills/`. Add the description and interface
metadata required by the target Codex validator. No MCP servers, connected apps
or install-time command hooks are needed.

Build from an explicit allowlist of tracked code and documentation. Generated
`pet.json` and `spritesheet.webp` are user outputs, not plugin files. Exclude
personal references, generated pets, prompts/logs, .venv, .env, credentials,
local Codex configuration and model caches. Reject symlinks and escaping paths;
Git ignore rules alone are not a packaging boundary.

## Lifecycle and tradeoffs

Keep dependency setup explicit and isolated. Core setup must not download neural
weights; document optional dependency/model downloads separately. Installing a
plugin must not automatically generate or install a pet. The current skill
installer replaces its destination and lacks transactional rollback; it cannot
be reused unchanged for this lifecycle.

Stage and validate upgrades before activation, retain the previous version and
runtime for rollback, and preserve user pets and external model caches. Match
plugin/Python versions to a Git tag; test activation through the Codex plugin
manager in a temporary profile. No published PyPI package is assumed.

Discovery and managed versions are useful, but another archive, runtime lifecycle
and client compatibility surface add maintenance and supply-chain work. Keep
one canonical runtime and derive the bundled skill copy during packaging.

## Independently reviewable follow-ups

1. **Builder/manifest:** implement the allowlisted archive builder; build twice
   from a clean checkout and compare member names and bytes. Run Codex's plugin
   validator; test rejection of private files, symlinks and escaping paths.
2. **Runtime lifecycle:** implement staging, version matching and rollback;
   test failed dependency setup and existing-install preservation in a temporary
   profile, with no changes to real user pets.
3. **Distribution acceptance:** run full pytest, Ruff, runtime/skill parity and
   no-key deterministic generation/package checks. Verify discovery in the app
   and document tested Codex versions before publishing a marketplace entry.

The build and test path is deterministic and offline with installed core
dependencies; app discovery remains a separate recorded acceptance check.
