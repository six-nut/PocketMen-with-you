# Architecture

PocketMen separates probabilistic visual generation from deterministic packaging.

1. **Codex skill layer** — reference intake, identity lock, style preset and interaction contract.
2. **Official pet backend** — `$hatch-pet` delegates visual generation to `$imagegen` and assembles the Codex atlas.
3. **PocketMen independent QA** — local validator checks geometry, alpha, used/unused cells and edge collisions.
4. **Packaging** — `pet.json + spritesheet.webp` are installed under the Codex pet directory.
5. **Open-source tooling** — tests use synthetic images only, making CI reproducible and secret-free.
