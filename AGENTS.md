# Repository instructions for Codex

## Project purpose

This repository is the source package for `six-nut/PocketMen-with-you`, a skill-first open-source workflow that turns 2+ reference images into a faithful animated Codex companion.

## When the user asks to publish/configure GitHub

1. Read `repo-config.json`, `README.md`, `SECURITY.md`, and `scripts/bootstrap_github.py`.
2. Run local checks before any remote write:
   - `python -m pip install -e .[dev]`
   - `pytest -q`
   - `ruff check .`
3. Check `gh --version` and `gh auth status`.
4. Verify the active GitHub account is exactly `six-nut`. If not, stop and ask the user to switch accounts; never print or request a token.
5. Verify the target repository `six-nut/PocketMen-with-you` does not already contain unrelated work. If it exists, inspect it and ask before overwriting or force-pushing. Never force-push by default.
6. If the repository is absent and checks pass, run:
   `python scripts/bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.1.0`
7. After publication, report the repository URL and CI status. Remind the user to upload `assets/social-preview.png` under GitHub Settings → Social preview; normal `gh repo` commands do not set that image.
8. Do not upload private reference photos, generated personal pet runs, `.env` files, API keys, GitHub tokens, or local Codex configuration.

## Development rules

- Keep the public project independent of protected franchise assets. Use the original red/yellow companion-capsule logo in `assets/`.
- The PocketMen skill must delegate normal pet generation to `$hatch-pet` / `$imagegen`; do not add a direct secret-bearing Image API call.
- Preserve Codex atlas geometry and state semantics in tests.
- Use synthetic fixtures in CI; CI must not spend image-generation credits.
