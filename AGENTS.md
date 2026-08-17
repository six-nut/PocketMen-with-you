# Repository instructions for Codex

## Project purpose

This repository is the source package for `six-nut/PocketMen-with-you`, a local-first Codex Skill and Python toolkit that turns 2+ reference images into animated Codex companions.

## Non-negotiable architecture

- Normal PocketMen runs must **not** require `$hatch-pet`.
- Normal PocketMen runs must **not** request, inspect, or require `OPENAI_API_KEY`.
- On compatible local hardware, prefer the bundled open-weight Neural Local Studio.
- Default neural backend: `black-forest-labs/FLUX.2-klein-4B`.
- Optional Identity-Max backend: `Qwen/Qwen-Image-Edit-2511`.
- Keep the deterministic Pillow/NumPy/OpenCV renderer as a universal fallback.
- Never silently call a paid remote image API.
- Never commit model weights or raw personal reference images.

## When the user asks to publish/configure GitHub

1. Read `repo-config.json`, `README.md`, `SECURITY.md`, `NOTICE.md`, `UPGRADE_WITH_CODEX.md`, and `scripts/bootstrap_github.py`.
2. Run local checks before any remote write:
   - `python -m pip install -e .[dev]`
   - `pytest -q`
   - `ruff check .`
   - `python -m compileall -q src`
3. Check `gh --version` and `gh auth status`.
4. Verify the active GitHub account is exactly `six-nut`. If not, stop; never print or request a token.
5. Verify `six-nut/PocketMen-with-you` does not contain unrelated work before writes. Never force-push by default.
6. If safe, run:
   `python scripts/bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.3.0`
7. Report repository URL and CI status. Remind the user to set `assets/social-preview.png` as GitHub Social preview if needed.
8. Do not upload private references, model caches, `.env`, API keys, GitHub tokens, or local Codex configuration.

## Development rules

- Keep the public project independent of protected franchise assets. Use the original red/yellow Companion Capsule in `assets/`.
- Preserve Codex atlas geometry and state semantics in tests.
- Use synthetic fixtures in CI; CI must not download multi-GB neural weights.
- Neural backends must remain optional imports so core tests run without Torch/Diffusers.
- Any backend claiming commercial friendliness must have its upstream model license documented.
- Changes to prompt/state semantics require tests and documentation updates.
