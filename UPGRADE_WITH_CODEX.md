# Upgrade existing repository to v0.3.0

For the repository `six-nut/PocketMen-with-you`:

1. preserve Git history and all user-created issues/releases;
2. replace the v0.2 source/skill files with the bundled v0.3 implementation;
3. keep PocketMen local-first and independent from hatch-pet;
4. add the Neural Local Studio backends and documentation;
5. do not commit model weights or private reference images;
6. run `PYTHONPATH=src pytest -q` and `python -m compileall -q src`;
7. run a deterministic smoke test with `OPENAI_API_KEY` unset;
8. if compatible local GPU hardware is present, run `pocketmen doctor`; do not fail the release if a large model cannot be downloaded in CI;
9. commit and push normally; do not force-push;
10. update repository topics to include `local-ai`, `flux2`, `qwen-image`, `image-editing`, `codex-skill`;
11. create release `v0.3.0` only after tests pass.

Release notes should clearly state that neural model weights are downloaded separately and keep their upstream licenses.
