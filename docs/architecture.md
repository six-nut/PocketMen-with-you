# Architecture

## v0.3 overview

PocketMen is local-first and has two rendering tiers behind one CLI.

```text
references
   ↓
Codex visual Identity Lock
   ↓
hardware doctor
   ↓
engine selector
   ├─ neural-local
   │    ├─ FLUX.2 klein 4B (default)
   │    └─ Qwen Image Edit 2511 (Identity-Max)
   │         ↓
   │    canonical master
   │         ↓
   │    per-state semantic key poses
   │         ↓
   │    chroma extraction
   │         ↓
   │    micro-motion stabilizer
   │
   └─ deterministic fallback
        ├─ canonical cutout
        ├─ local style transform
        └─ deterministic motion
             ↓
        common atlas builder
             ↓
        validation / previews / package / install
```

## Separation of responsibilities

- `hardware.py`: detect local execution capability and recommend an engine.
- `prompts.py`: build structured identity/action/style prompts.
- `backends/`: local open-weight model adapters.
- `neural.py`: canonical/state generation and chroma extraction.
- `imageops.py`: deterministic reference processing.
- `styles.py`: deterministic style fallback.
- `motion.py`: temporal stabilization and sprite-cell rendering.
- `atlas.py`: contract validation and contact sheets.
- `pipeline.py`: engine orchestration, fallback, QA and packaging.

The atlas/package layer never depends on a particular neural model.
