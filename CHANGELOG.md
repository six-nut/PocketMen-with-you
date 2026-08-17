# Changelog

## 0.3.0 — Neural Local Studio

- Replaced the "local means only warps" ceiling with a true local open-weight generative path.
- Added **FLUX.2 [klein] 4B** as the default neural-local backend when compatible NVIDIA hardware is detected.
- Added optional **Qwen-Image-Edit-2511** Identity-Max backend for heavier multi-reference identity-sensitive editing.
- Added hardware detection, `pocketmen doctor`, auto backend selection, quality profiles, subject-aware prompt compilation and chroma-background extraction.
- Each Codex animation state can now receive its own model-generated semantic key pose; deterministic motion is only used for stable micro-animation between key poses.
- The normal neural path still requires **no OpenAI API key**, never invokes hatch-pet, and does not call OpenAI ImageGen.
- Added one-click neural runtime preparation scripts and explicit model/license documentation.
- Preserved deterministic fallback for CPU-only or low-VRAM machines.

## 0.2.0 — Local-first

- Removed the hard hatch-pet/ImageGen dependency.
- Added deterministic local foreground extraction, style transforms, motion synthesis, atlas assembly and validation.
