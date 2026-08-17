# Codex animation contract

PocketMen emits a 1536×1872 RGBA WebP atlas with 8 columns × 9 rows and 192×208 cells.

Rows:

1. idle — 6 frames
2. running-right — 8
3. running-left — 8
4. waving — 4
5. jumping — 5
6. failed — 8
7. waiting — 6
8. running — 6 (Codex actively working, not locomotion)
9. review — 6

In Neural Local Studio, each row is anchored by a semantic model-generated key pose and then receives subtle deterministic micro-motion. This is preferred over independently generating every frame because independent generations increase identity flicker.

Multiple companions are supported at the *reference/editor* level when a backend can combine them. They must remain a single compact visual unit inside each cell; no subject may cross cell boundaries.
