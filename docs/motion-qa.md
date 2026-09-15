# Motion QA

`pocketmen validate atlas.webp --json-out validation.json` reports cell-local
alpha bounding boxes, width, height, center and baseline (exclusive bottom edge).
Adjacent nonempty used frames include signed `baseline_delta_px` and a
`scale_jump_ratio`: the larger absolute width/height change divided by the
previous frame's corresponding dimension. Empty cells interrupt comparisons.
Per-state summaries report baseline span and maximum adjacent jumps.

Defaults warn above 18 pixels of baseline movement or 0.18 relative size change.
The `jumping` state allows 58 pixels of baseline movement to accommodate intentional
flight. These are heuristics; inspect the GIF previews for visual quality.
Warnings identify the state and one-based frame numbers and do not fail structural
validation. First and last frames are not compared as a loop seam.

Tune `--motion-baseline-jump-px`, `--motion-scale-ratio`, and
`--motion-jumping-baseline-px` on the validate command. Python callers may pass
the equivalent underscore-named keyword arguments to `validate_atlas`.
Motion analysis remains enabled when the Python `edge_margin` is zero.

Tests use synthetic images only; no model downloads, network services or API keys
are needed. Geometry and unused-cell checks retain the v0.3 atlas contract.
