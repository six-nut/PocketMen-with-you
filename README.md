<div align="center">
  <img src="assets/logo-512.png" width="132" alt="PocketMen with You companion capsule logo" />
  <h1>PocketMen with You</h1>
  <p><strong>Turn 2+ reference images into a high-fidelity animated Codex companion.</strong></p>
  <p>Handsome chibi people · gentle realistic pets · original capsule creatures · deterministic Codex pet packaging</p>

  [![CI](https://github.com/six-nut/PocketMen-with-you/actions/workflows/ci.yml/badge.svg)](https://github.com/six-nut/PocketMen-with-you/actions/workflows/ci.yml)
  [![MIT License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
  [![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](https://developers.openai.com/codex/build-skills)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
</div>

> **Upload at least two images. Describe the vibe. PocketMen turns the visual identity into a companion that can stay beside your Codex work.**

[中文说明](README.zh-CN.md) · [Quick start](#quick-start) · [How it works](#how-it-works) · [Contributing](CONTRIBUTING.md)

## Why PocketMen?

Custom Codex pets are delightful, but good results require more than one pretty image: identity has to stay stable across nine states, directional running must read correctly, unused atlas cells must be transparent, the final sheet must be exactly `1536 × 1872`, and visual QA must catch scale pops and identity drift.

PocketMen packages that workflow as a reusable Codex skill. It is deliberately **skill-first**: visual generation is delegated to Codex's installed image-generation workflow, while PocketMen adds reference-image intake, style presets, identity locks, companion-interaction rules, QA gates, and one-click pet installation.

## What you can make

| Mode | Best for | Goal |
|---|---|---|
| `hero-chibi` | people, creators, researchers, mascots | handsome + bouncy-cute, readable at pet size |
| `soft-real` | cats, dogs, small animals | preserve coat, eyes, proportions, collar/marks |
| `plush` | cozy mascots and objects | soft toy material, simple silhouette |
| `capsule-creature` | original fantasy companions | creature + **original red/yellow companion capsule**, not a copied franchise mark |
| `auto` | mixed inputs | let Codex infer the safest useful preset |

## Quick start

### Option A — open this repository in Codex

1. Clone or unzip this repository.
2. Start Codex from the repository root.
3. Upload **2 or more reference images**.
4. Ask:

```text
Use $pocketmen-with-you to create a companion from these references.
Style: auto.
Name: <your pet name>.
Keep the identity faithful and install it when QA passes.
```

Codex discovers repository skills from `.agents/skills`. If the skill is not listed immediately, restart Codex.

### Option B — install the skill for all repositories

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_skill.ps1
```

macOS / Linux:

```bash
bash scripts/install_skill.sh
```

This copies the skill to `~/.agents/skills/pocketmen-with-you`, the documented user-scope location for Codex skills.

## How it works

```text
2+ references
    │
    ▼
Identity lock ──► style preset ──► canonical base
                                   │
                                   ▼
                         9 Codex motion states
                                   │
                                   ▼
                       official hatch-pet backend
                                   │
                                   ▼
                      deterministic QA + previews
                                   │
                                   ▼
                 pet.json + spritesheet.webp
                                   │
                                   ▼
                 ${CODEX_HOME:-~/.codex}/pets/<id>
```

PocketMen does **not** call the OpenAI Image API directly. The skill tells Codex to use the installed `$hatch-pet` / `$imagegen` workflow. If that workflow needs an external paid fallback, it must stop and obtain user confirmation rather than exposing or silently using credentials.

## Codex atlas contract

PocketMen validates the current Codex pet atlas geometry:

- 8 columns × 9 rows
- 192 × 208 px cells
- final atlas: 1536 × 1872 px
- rows: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`
- unused cells must be fully transparent

The included local validator and tests do not generate images, so CI stays deterministic and does not need an API key.

## Companion-first design rules

PocketMen prioritizes what users notice at desktop-pet scale:

- **Identity before novelty.** Face, coat pattern, eyes, silhouette, accessories and proportions are locked first.
- **Interaction over stickers.** A second pet/companion should physically interact with the primary subject instead of floating as an unrelated decal.
- **Readable motion.** Running direction, jump height and waiting/review semantics must be visually distinct.
- **No detached VFX by default.** Glows, speed lines, floating symbols and shadows can break transparent sprite extraction.
- **Privacy by default.** Raw reference images are never intended for repository commits or release assets.

## Local CLI

Install development dependencies:

```bash
python -m pip install -e .[dev]
```

Validate an atlas:

```bash
pocketmen validate path/to/spritesheet.webp --json-out validation.json
```

Build a contact sheet:

```bash
pocketmen contact-sheet path/to/spritesheet.webp --output contact-sheet.png
```

Install a finished pet directory:

```bash
pocketmen install path/to/pet-package
```

## Repository bootstrap for `six-nut/PocketMen-with-you`

This source package ships with a safe GitHub bootstrapper. It checks GitHub CLI authentication, refuses to publish from the wrong account, never prints tokens, initializes Git if needed, creates the public repository, pushes `main`, adds topics and community labels, and can create `v0.1.0`.

Windows one-click:

```bat
PUBLISH_GITHUB.bat
```

Or:

```bash
python scripts/bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.1.0
```

GitHub does not expose the repository social-preview upload through the normal `gh repo` commands, so after publishing upload `assets/social-preview.png` in **Settings → Social preview**.

## Trademark & character policy

PocketMen is an independent open-source project and is not affiliated with Nintendo, The Pokémon Company, Game Freak, OpenAI, or GitHub. The bundled red/yellow **companion capsule** is an original project mark; the project intentionally does not ship an exact Poké Ball design or copyrighted franchise characters. Users are responsible for having the rights to reference images and characters they ask a model to transform.

## Security

- No API keys belong in this repository.
- CI performs no paid image generation.
- External generation fallbacks require explicit user confirmation.
- See [SECURITY.md](SECURITY.md) for responsible disclosure.

## Contributing

Small, visual, testable pull requests are welcome. Start with a `good first issue`, improve a style preset, add synthetic fixtures, or make a QA check more robust. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

MIT © 2026 six-nut and contributors.
