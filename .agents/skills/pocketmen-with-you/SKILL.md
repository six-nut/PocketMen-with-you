---
name: pocketmen-with-you
description: Turn 2+ user reference images into a faithful animated Codex companion pet, including handsome chibi people, realistic affectionate animals, plush mascots, or original capsule creatures; orchestrate identity locking, style selection, the Codex 8x9 pet atlas, QA previews, validation, packaging, and local installation. Use when the user wants a custom Codex pet/companion from personal photos or character references. Do not use for ordinary image edits or when fewer than two reference images are available unless the user explicitly chooses to proceed with reduced identity fidelity.
---

# PocketMen with You

Create a high-fidelity Codex companion from **at least two** user-provided reference images. Treat the references as identity evidence, not merely inspiration.

## Non-negotiable rules

1. Require 2+ reference images by default. If there is only one, ask for a second angle/photo unless the user explicitly accepts reduced fidelity.
2. Never commit, publish, or copy raw personal reference images into a public repository or release asset without explicit permission.
3. Use the installed `$hatch-pet` skill as the Codex-pet backend whenever available. It owns image-generation delegation, deterministic frame extraction, atlas assembly, validation, motion previews and pet packaging.
4. Do not call an image API, image CLI, or paid external generator directly from this skill. Let `$hatch-pet` / `$imagegen` choose its built-in path. If a fallback requires API credentials or payment, stop and ask the user before it is used.
5. Never ask the user to paste an API key into chat.
6. Do not claim success until the final files exist and both deterministic and visual QA pass.

## Intake

From the references and user request, build an **identity lock** with only visible/stable traits:

- subject type: person / animal / original creature / mixed companion group;
- face or head shape;
- hair/fur/skin/material and stable markings;
- eye color and distinctive eye shape;
- body proportions and silhouette;
- fixed accessories (earrings, collar, watch, ribbon, backpack, etc.);
- personality cues that should affect pose, not identity;
- features that vary between photos and therefore must **not** be locked.

When a secondary companion is requested, define a physical interaction contract: foot-side, shoulder, lap, backpack, hand/paw contact, shared gaze, or another clear overlap. Avoid detached sticker-like companions.

## Style presets

Read `references/style-presets.md` and choose one:

- `hero-chibi`
- `soft-real`
- `plush`
- `capsule-creature`
- `auto`

For `capsule-creature`, use the project's original red/yellow companion-capsule language. Do not reproduce a trademarked capture-device design or protected franchise character unless the user has appropriate rights and the request is allowed.

## Canonical base

Before motion rows, create or approve one canonical base image. It is the identity source of truth for every row.

The base prompt must be concise and include:

- the locked visible traits;
- the selected style;
- compact full-body silhouette readable at 192×208;
- no text, watermark, scenery, detached shadow, soft glow, speed line, dust or UI;
- a plain/chroma-friendly background when the backend needs deterministic removal.

If the subject is a real animal and `soft-real` is selected, prioritize coat texture, eye color, ear shape, muzzle, body proportions and collar/markings over cute exaggeration.

## Motion contract

Read `references/motion-contract.md`. Keep identity and scale stable across all states.

Rows and valid frame counts:

1. `idle` — 6
2. `running-right` — 8
3. `running-left` — 8
4. `waving` — 4
5. `jumping` — 5
6. `failed` — 8
7. `waiting` — 6
8. `running` — 6, meaning Codex is actively working, **not** physical locomotion
9. `review` — 6

Directional rows must clearly face the correct direction and show alternating gait. Mirror `running-left` from an approved rightward row only when asymmetric identity cues remain valid.

## Backend orchestration

1. Check whether `$hatch-pet` is available.
2. If unavailable, tell the user to run `$skill-installer hatch-pet`, restart Codex, and resume. Do not silently install unrelated software.
3. Invoke `$hatch-pet` with:
   - all reference image paths;
   - pet name/display name;
   - identity lock as stable pet notes;
   - selected style preset;
   - the interaction contract for multiple subjects;
   - a request to produce the full Codex atlas, contact sheet, previews, validation and package.
4. Keep image-generation concurrency bounded. Generate `idle` and `running-right` early to check identity before spending effort on all rows.
5. If one row fails, repair that row only.

## QA gates

In addition to the backend's QA, reject the result if any of these occur:

- face/species/coat/eye/accessory identity drift;
- second companion disappears or floats without intended interaction;
- frame-to-frame size or baseline popping;
- wrong running direction or stagnant gait;
- `running` depicts physical running instead of a working state;
- clipping, cell-edge collisions, detached shadows, glows or motion trails;
- non-transparent unused cells;
- final atlas is not exactly 1536×1872.

For a finished atlas, optionally run this repository's independent validator:

```bash
python -m pocketmen.cli validate /absolute/path/to/spritesheet.webp --json-out /absolute/path/to/pocketmen-validation.json
```

## Packaging and installation

Final pet package:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

`pet.json` should contain a sanitized stable ID, display name, short description and `spritesheetPath: "spritesheet.webp"`.

After installation, tell the user to refresh Pets and wake the pet with `/pet` where supported.

## Final report

Report only after QA passes:

- pet ID and display name;
- style preset;
- package path;
- spritesheet path;
- validation result;
- contact-sheet path;
- preview directory;
- whether any external paid fallback was used;
- how to select/wake the pet.
