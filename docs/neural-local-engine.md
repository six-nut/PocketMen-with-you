# Neural Local Engine

PocketMen v0.3 uses local open-weight image editing to close the quality gap for reference-driven Codex companions.

## Why a neural local engine

A deterministic renderer can preserve a reference cutout but cannot create genuinely new anatomy or poses. A local multi-reference image editor can use the original references plus a canonical master to create new state-specific key poses while preserving identity.

## Default backend

`black-forest-labs/FLUX.2-klein-4B`

- unified generation and editing;
- multi-reference editing;
- Apache-2.0 model license;
- consumer NVIDIA GPU target;
- four-step distilled inference.

PocketMen renders one canonical master and, in balanced/max mode, a semantic key pose for each Codex state. It then performs alpha extraction and deterministic micro-animation locally.

## Identity-Max backend

`Qwen/Qwen-Image-Edit-2511`

Use when identity drift is more important than runtime cost. PocketMen feeds the generated canonical image plus up to two original references into Qwen's multi-image editing pipeline.

## Prompt compiler

The prompt compiler is intentionally structured:

1. purpose;
2. subject;
3. explicit identity lock;
4. required action;
5. fixed style;
6. composition;
7. flat chroma background;
8. negative constraints.

This reduces ambiguity and keeps the model focused on changing the pose rather than redesigning the subject.

## Chroma-to-alpha pipeline

Neural models are asked to render against a flat opaque chroma background. PocketMen chooses a chroma color that is far from sampled reference colors. During extraction, only chroma-like pixels belonging to connected components that touch an image border are removed. This protects similarly colored eye/accessory pixels in the interior.

## Why key poses + micro-motion

Generating every animation frame independently would maximize motion freedom but often increases identity flicker. PocketMen instead generates state-level key poses and adds small deterministic transformations for breathing, bounce, lean and timing. The neural model is responsible for the difficult semantic pose; the deterministic layer stabilizes animation.

## Model cache

Models are downloaded into the normal Hugging Face cache. They are not redistributed in the PocketMen repository. Once cached, local generation can run without an OpenAI API key.
