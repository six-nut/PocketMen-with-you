# Contributing to PocketMen with You

Thanks for helping make tiny companions better.

## Principles

1. Preserve identity before adding effects.
2. Keep visual changes reviewable with contact sheets or synthetic fixtures.
3. Never add API keys, private reference photos, or paid-generation credentials.
4. Avoid exact copies of protected characters, brand mascots, or trademarked capture-device designs.
5. Keep the Codex atlas contract deterministic and covered by tests.

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .[dev]
pytest -q
ruff check .
```

## Good first contributions

- New synthetic test fixtures for edge cases.
- Better animation QA heuristics.
- A new generic style preset that does not copy a living artist or protected franchise.
- Better docs or translations.
- Cross-platform installation improvements.

## Demo contributions

Public examples must use synthetic, owned, public-domain, or explicitly redistributable material.
Follow the [privacy-safe demo contribution guide](docs/demo-contributions.md) and include provenance,
license information, QA evidence, and deterministic validation output.

## Pull requests

Keep PRs focused. Include:

- what changed;
- why it helps pet fidelity or developer experience;
- tests run;
- before/after contact sheets for visual-pipeline changes.
