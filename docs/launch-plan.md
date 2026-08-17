# Star-ready launch plan

Stars cannot be guaranteed; the goal is to make PocketMen easy to understand, trust, try, and contribute to.

## Before launch

- Run `VERIFY_PROJECT.bat` or `pytest -q && ruff check .`.
- Confirm no personal reference photos, generated private pets, `.env` files, or secrets are tracked.
- Keep the first release focused: **2+ images → identity lock → Codex pet → QA → install**.
- Upload `assets/social-preview.png` in GitHub repository settings.
- Pin a short demo issue showing a synthetic input → contact sheet → installed pet workflow.

## Launch page checklist

- Lead with the result in one sentence, not implementation details.
- Show the red/yellow original companion-capsule logo consistently.
- Keep the bilingual README.
- Include a 30–60 second screen capture when a redistributable demo pet is available.
- Use GitHub Topics so users can discover the project through Codex, agent-skill, desktop-pet and spritesheet searches.

## Community flywheel

- Label small deterministic QA tasks as `good first issue`.
- Ask contributors to use synthetic or redistributable references.
- Prefer issue templates that collect reproducible steps without private images.
- Publish changelog-backed releases instead of silent main-branch changes.
- Turn recurring quality failures into validator tests.

## Suggested first three issues

1. **Demo gallery infrastructure without private references** — create a manifest format for opt-in community demos.
2. **Motion-quality heuristics** — detect baseline jumps and frame-size popping more robustly.
3. **Plugin packaging** — package the mature standalone skill as an installable OpenAI plugin when distribution requirements justify it.
