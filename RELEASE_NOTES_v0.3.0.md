# PocketMen-with-you v0.3.0 — Neural Local Studio

This release replaces the v0.2 deterministic-only ceiling with a local open-weight neural studio while preserving the zero-OpenAI-API-key normal workflow.

## Highlights

- Local multi-reference generation/editing with FLUX.2 [klein] 4B (Apache-2.0) as the default neural backend on supported NVIDIA GPUs.
- Optional Qwen-Image-Edit-2511 (Apache-2.0) Identity-Max backend for heavier identity-sensitive editing.
- Reference ranking, identity-lock prompts, state-specific semantic key poses, chroma-to-alpha extraction, stable micro-motion, atlas assembly, GIF previews, QA, packaging, and Codex installation.
- Automatic hardware diagnosis and deterministic fallback when neural hardware/dependencies are unavailable.
- Normal PocketMen runs do not call hatch-pet, gpt-image, or OpenAI Image API and do not request `OPENAI_API_KEY`.

## Quality expectation

The goal is to approach hosted image-generation quality for the narrow PocketMen workflow (2+ references → one consistent desktop companion), not to claim general parity with proprietary frontier image models. Local quality depends on GPU, backend, reference quality, prompt/identity notes, and selected quality profile.

## Recommended modes

- `--engine auto --quality balanced`: best default.
- `--engine neural --backend flux2-klein-4b --quality max`: local high-fidelity mode on compatible NVIDIA hardware.
- `--engine neural --backend qwen-image-edit-2511 --quality max`: Identity-Max mode for machines capable of running the larger model.
- `--engine deterministic`: zero-model fallback.
