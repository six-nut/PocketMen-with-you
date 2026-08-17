# Benchmark protocol

PocketMen should measure progress against the *task*, not make vague claims of model parity.

## Benchmark tracks

1. Human → hero-chibi
2. Real pet → soft-real
3. Human + pet interaction
4. Original creature → capsule-creature

Each track uses 2–3 consented or synthetic references.

## Scores

Rate 1–5 per state for:

- identity fidelity;
- pose/action correctness;
- style consistency;
- fixed accessory preservation;
- anatomy quality;
- small-size readability;
- alpha/cutout quality.

Atlas-level checks:

- 1536×1872 exact size;
- correct row/frame contract;
- no cross-cell pixels;
- no clipped subject;
- unused cells transparent;
- GIF motion readable at Codex scale.

## Optional external baseline

A maintainer may compare the same references/prompts against a hosted frontier image editor such as GPT Image 2, but that baseline is optional and must never become a runtime dependency. Store only scores and consent-safe derived examples in the public repository.

## Release rule

Do not claim "equal to" or "better than" a proprietary image model without a reproducible benchmark. Prefer narrow statements such as "closes the gap for multi-reference Codex companion generation" and publish the benchmark inputs/criteria when possible.
