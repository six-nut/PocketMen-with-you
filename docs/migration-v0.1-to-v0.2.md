# Migrating from v0.1 to v0.2

## The symptom v0.2 fixes

v0.1 could stop with a message equivalent to:

> Built-in image generation failed repeatedly. Configure `OPENAI_API_KEY` or approve CLI/API fallback.

That happened because v0.1 delegated the visual stage to hatch-pet/imagegen. The atlas utilities were local, but the actual pose artwork was not.

## v0.2 behavior

v0.2 removes hatch-pet as a hard dependency. The default skill command invokes the bundled Local Engine and therefore always has a no-key path.

If a user explicitly requests Studio-quality generative art, built-in image generation may still be attempted. A transport failure falls back to local mode; it is not treated as a reason to ask for an API key.

## Reinstall the global skill

From the repository root:

- Windows: `INSTALL_SKILL.bat`
- macOS/Linux: `bash scripts/install_skill.sh`

Restart Codex if it does not refresh the skill immediately.
