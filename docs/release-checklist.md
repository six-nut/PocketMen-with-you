# Release checklist

- [ ] `PYTHONPATH=src pytest -q` passes.
- [ ] `python -m compileall -q src` passes.
- [ ] `ruff check .` passes in the release environment.
- [ ] Core/deterministic smoke test succeeds with `OPENAI_API_KEY` unset.
- [ ] `repo-config.json`, `pyproject.toml`, `CITATION.cff`, README and CHANGELOG say `v0.3.0`.
- [ ] Skill runtime mirror matches `src/pocketmen`.
- [ ] Neural dependencies remain optional imports in CI.
- [ ] No model weights are present in the repository/archive.
- [ ] No private reference images are present.
- [ ] Default neural backend license is documented as Apache-2.0.
- [ ] GitHub topics are lowercase, hyphenated and no more than 20.
- [ ] Social preview and logo render correctly.
