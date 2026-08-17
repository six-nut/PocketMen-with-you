# Backend modes

## `--engine auto`

Runs `pocketmen doctor`. On a compatible NVIDIA CUDA system (conservative threshold around 13 GB VRAM), tries the FLUX.2 klein neural-local backend. Otherwise uses deterministic local rendering.

## `--engine neural`

Forces a local neural backend. With `--backend auto`, this resolves to FLUX.2 klein 4B.

## `--backend flux2-klein-4b`

Default high-quality local backend. Best balance of licensing, consumer hardware, multi-reference editing and latency.

## `--backend qwen-image-edit-2511`

Heavy Identity-Max backend. Use when the user has sufficient hardware and state identity is more important than setup time.

## `--engine deterministic`

Never loads a neural model. Uses canonical cutout + deterministic style/motion. This is the universal fallback.

## Quality profiles

`draft`: 1 neural generation call (canonical only).

`balanced`: canonical + neural state key poses, with left-running derived from right-running to reduce drift.

`max`: canonical + an independent neural key pose for all nine states.
