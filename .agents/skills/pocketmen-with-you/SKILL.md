---
name: pocketmen-with-you
description: Turn 2+ user reference images into a high-fidelity animated Codex companion using PocketMen's own local stack. Prefer the open-weight Neural Local Studio (FLUX.2 klein 4B; optional Qwen-Image-Edit-2511 Identity-Max) on compatible hardware; otherwise fall back to the deterministic local renderer. Never require hatch-pet or OPENAI_API_KEY for the normal workflow.
---

# PocketMen with You — Neural Local Studio

Create a Codex companion from **at least two** user-provided reference images. The normal workflow is self-contained and **must not invoke `$hatch-pet` or request `OPENAI_API_KEY`**.

## Product goal

The user should be able to upload 2+ images and get a polished, identity-consistent Codex companion with minimal setup. PocketMen should aim for hosted-image-editor-like quality **within this narrow companion-creation task**, while being honest that local open-weight models are not guaranteed to equal a proprietary frontier model on every visual task.

## Engine order

Use this decision order:

1. inspect the references visually and build an Identity Lock;
2. run PocketMen hardware doctor;
3. if compatible neural runtime/hardware is available, use `neural-local`;
4. if the neural runtime is missing but an NVIDIA GPU with roughly 13 GB+ VRAM is present, bootstrap the skill-local neural profile once, then retry;
5. if neural inference is unavailable or fails, fall back to the deterministic local renderer;
6. never route failure into hatch-pet or OpenAI API-key setup.

### Default neural backend

`flux2-klein-4b`

- open-weight local generation/editing;
- multi-reference editing;
- commercial-friendly Apache-2.0 weights;
- intended for consumer NVIDIA GPUs;
- preferred for most users.

### Identity-Max backend

`qwen-image-edit-2511`

Use only when the user prioritizes identity consistency over setup size/latency or when FLUX state outputs visibly drift. This backend is heavier and should not be silently installed unless needed.

### Deterministic fallback

`local-deterministic-motion-puppet`

Guaranteed no-model path. It preserves supplied pixels and produces a valid Codex atlas, but cannot invent unseen anatomy/poses at neural quality.

## First step: visual Identity Lock

Before running any command, inspect all supplied references and summarize only stable visible details.

Record:

- `subject_type`: `person`, `animal`, `creature`, `mascot`, or `auto`;
- face/head shape;
- hair/fur/material and stable markings;
- eye color and eye shape;
- silhouette/body proportions;
- fixed accessories (collar, earrings, glasses, watch, ribbon, backpack, etc.);
- stable outfit details when the user wants them locked;
- personality cues relevant to motion;
- any traits that vary between images and must **not** be locked.

Turn these into one concise `--identity-notes` string. This is important: the local neural backend sees image references, but explicit stable identity notes substantially reduce drift across animation states.

Do not infer sensitive identity attributes. Describe only visible appearance needed for rendering.

## Style choice

Allowed styles:

- `soft-real` — photo-faithful humans/animals; preserve fur/hair/eyes/markings/accessories;
- `hero-chibi` — premium 3D toy-like chibi, handsome/cute balance, roughly 2.7–3 heads tall;
- `plush` — premium collectible plush interpretation;
- `capsule-creature` — original PocketMen pocket-creature styling using PocketMen's own red/yellow Companion Capsule;
- `auto` — conservative; use `soft-real` unless the user clearly requests stylization.

For a real deceased or memorial pet, prioritize identity fidelity over cuteness and do not imply the digital pet is literally the deceased animal.

## Quality choice

- `draft`: one neural canonical master + deterministic nine-state motion;
- `balanced`: canonical master + state-specific neural key poses; recommended default;
- `max`: independently generate every state key pose; best for publication-quality showcases and important personal companions.

Use `max` when the user explicitly asks for maximum quality, ImageGen-like results, or very high fidelity.

## Runtime discovery

Resolve the installed skill directory first.

Runtime Python:

Windows:

```text
<skill-dir>\.venv\Scripts\python.exe
```

macOS/Linux:

```text
<skill-dir>/.venv/bin/python
```

If the virtual environment does not exist, run:

```bash
python <skill-dir>/scripts/setup_runtime.py --skill-dir <skill-dir> --profile core
```

## Hardware doctor

Run:

```bash
<python> <skill-dir>/scripts/create_local_pet.py doctor
```

If `recommended_engine` is `neural-local` but the neural dependencies are missing, run once:

```bash
python <skill-dir>/scripts/setup_runtime.py --skill-dir <skill-dir> --profile neural
```

The first real neural creation may download `black-forest-labs/FLUX.2-klein-4B` into the normal Hugging Face cache. This is a local model download, **not an OpenAI API call**, and no OpenAI key is required.

If the user explicitly requests Identity-Max, use:

```bash
python <skill-dir>/scripts/setup_runtime.py --skill-dir <skill-dir> --profile identity-max
```

## Creation command — default high-quality path

```bash
<python> <skill-dir>/scripts/create_local_pet.py create \
  --reference /absolute/path/ref1.jpg \
  --reference /absolute/path/ref2.jpg \
  --name "<display name>" \
  --pet-id "<stable-id>" \
  --subject-type <person|animal|creature|mascot|auto> \
  --identity-notes "<stable visible identity details>" \
  --style <soft-real|hero-chibi|plush|capsule-creature|auto> \
  --engine auto \
  --backend auto \
  --quality balanced \
  --output /absolute/path/to/output \
  --install
```

For maximum local quality:

```text
--engine neural --backend flux2-klein-4b --quality max
```

For identity-sensitive heavy mode:

```text
--engine neural --backend qwen-image-edit-2511 --quality max
```

Do not ask for API credentials if these fail. If neural fallback is allowed, PocketMen will use the deterministic path and report the reason.

## Neural rendering design

PocketMen owns the full pipeline:

1. choose a chroma color maximally separated from the references;
2. use 2–3 references as identity anchors;
3. generate a canonical master in the requested style;
4. generate semantically correct state-specific key poses from canonical + raw references;
5. use a strict structured prompt: purpose → subject → identity lock → action → style → composition → background → constraints;
6. render on a perfectly flat opaque chroma background;
7. remove only chroma-like pixels connected to the frame border, protecting same-colored eyes/accessories inside the subject;
8. use deterministic micro-motion between key poses to reduce identity flicker;
9. build, validate, preview and package the 8×9 Codex atlas.

## Motion contract

Rows and frame counts:

1. `idle` — 6
2. `running-right` — 8
3. `running-left` — 8
4. `waving` — 4
5. `jumping` — 5
6. `failed` — 8
7. `waiting` — 6
8. `running` — 6, meaning Codex is actively working, not physical locomotion
9. `review` — 6

The neural engine generates a true semantic key pose for each state in balanced/max modes. Deterministic transforms are reserved for subtle breathing, bounce, lean and timing—not for pretending a static cutout is a completely new pose.

For animals, `waving` should use a raised front paw with natural anatomy. For people, use a real hand wave. `running` should depict focused work with a compact plain laptop. `review` should depict inspection of a plain paper/blueprint. No readable brand logos or UI text.

## QA gates

Expected output:

```text
<output>/
  package/<pet-id>/
    pet.json
    spritesheet.webp
  run/final/
    spritesheet.webp
    validation.json
  run/qa/
    identity-lock.json
    neural-generation.json        # neural runs only
    neural-raw/*.png              # local QA artifacts
    neural-cutouts/*.png          # local QA artifacts
    contact-sheet.png
    review.json
    run-summary.json
    previews/*.gif
```

Before installation acceptance:

1. `validation.json` must report `ok: true`;
2. inspect `contact-sheet.png` visually;
3. inspect at least `idle`, `running-right`, `waving`, `jumping`, `running`, and `review` GIFs when available;
4. reject severe identity drift, wrong eye/fur/hair color, missing fixed accessories, extra limbs, extra subjects, bad cutout residue, crop, or action semantics mismatch;
5. if one state is visibly wrong in neural mode, rerun that creation with stronger identity notes or Identity-Max rather than switching to an OpenAI API fallback;
6. do not publish or commit raw personal reference images.

## Failure policy

### Neural dependency/model failure

- report the local error briefly;
- use deterministic fallback unless the user explicitly disabled it;
- never suggest `OPENAI_API_KEY` as the default recovery path.

### Out-of-memory

- keep CPU offload enabled;
- close other GPU-heavy apps;
- use `balanced` or `draft` quality;
- if still failing, use deterministic fallback.

### Identity drift

- strengthen `--identity-notes`;
- use the cleanest 2–3 references;
- use `qwen-image-edit-2511 --quality max` when the hardware can support it;
- regenerate only the pet creation, not unrelated repository assets.

## Independence rule

Normal PocketMen output must report:

```text
api_key_required: false
hatch_pet_required: false
openai_imagegen_used: false
```

Do not invoke `$hatch-pet`. Do not inspect or request `OPENAI_API_KEY`. Do not silently call an external paid image endpoint.

## Model licensing

PocketMen code is MIT. Model weights are downloaded separately and are not redistributed by this repository.

- FLUX.2 [klein] 4B: Apache-2.0.
- Qwen-Image-Edit-2511: Apache-2.0.
- Do not make FLUX.2 [dev] a default backend; its model license is non-commercial.

## Privacy

Raw reference images remain local. Do not copy them into Git commits, public releases, bug reports or example datasets without explicit user permission. Final pet packages should contain only the required install assets unless the user asks to retain QA files.

## Final report

Report:

- pet ID and display name;
- engine actually used;
- backend/model actually used;
- style and quality profile;
- hardware summary;
- package path and install path;
- validation result;
- contact sheet and preview paths;
- neural fallback reason, if any;
- `hatch_pet_required=false`;
- `api_key_required=false`;
- `openai_imagegen_used=false`.
