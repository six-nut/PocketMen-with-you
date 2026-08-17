from __future__ import annotations

import json
import re
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from .atlas import make_contact_sheet, validate_atlas, write_validation
from .hardware import detect_hardware
from .imageops import choose_canonical
from .motion import build_frames, build_frames_from_sprites
from .neural import generate_state_sprites
from .spec import ATLAS_HEIGHT, ATLAS_WIDTH, CELL_HEIGHT, CELL_WIDTH, ROW_SPECS
from .styles import STYLE_PRESETS, apply_style

PET_ID_RE = re.compile(r"[^a-z0-9._-]+")
ENGINE_CHOICES = ("auto", "neural", "deterministic")
QUALITY_CHOICES = ("draft", "balanced", "max")
SUBJECT_TYPES = ("auto", "person", "animal", "creature", "mascot")


def slugify(value: str) -> str:
    v = value.strip().lower().replace(" ", "-")
    v = PET_ID_RE.sub("-", v).strip("-._")
    return (v or "pocketmen-pet")[:64]


def auto_style(canonical: Image.Image) -> str:
    # Conservative by design: if we cannot prove the subject is a person, preserve the photo.
    return "soft-real"


def compose_atlas(frames: dict[str, list[Image.Image]], output: str | Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    atlas = Image.new("RGBA", (ATLAS_WIDTH, ATLAS_HEIGHT), (0, 0, 0, 0))
    for row, (state, expected) in enumerate(ROW_SPECS):
        row_frames = frames[state]
        if len(row_frames) != expected:
            raise ValueError(f"{state}: expected {expected} frames, got {len(row_frames)}")
        for col, frame in enumerate(row_frames):
            atlas.alpha_composite(frame.convert("RGBA"), (col * CELL_WIDTH, row * CELL_HEIGHT))
    atlas.save(output, format="WEBP", lossless=True, method=3)
    return output


def render_previews(frames: dict[str, list[Image.Image]], output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for state, row_frames in frames.items():
        prepared = []
        for frame in row_frames:
            bg = Image.new("RGB", frame.size, (246, 247, 250))
            bg.paste(frame.convert("RGB"), mask=frame.getchannel("A"))
            prepared.append(bg)
        prepared[0].save(
            output_dir / f"{state}.gif",
            save_all=True,
            append_images=prepared[1:],
            duration=105 if state.startswith("running-") else 150,
            loop=0,
            optimize=False,
        )
    return output_dir


def _cell_metrics(frames: dict[str, list[Image.Image]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for state, row_frames in frames.items():
        areas = []
        baselines = []
        for im in row_frames:
            bbox = im.getchannel("A").getbbox()
            if bbox:
                areas.append((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))
                baselines.append(bbox[3])
        if areas:
            area_ratio = max(areas) / max(1, min(areas))
            baseline_span = max(baselines) - min(baselines)
        else:
            area_ratio = 999.0
            baseline_span = 999
        metrics[state] = {
            "bbox_area_ratio": round(area_ratio, 4),
            "baseline_span_px": baseline_span,
            "frames": len(row_frames),
            "ok": area_ratio < 1.85 and baseline_span < 58,
        }
    return metrics


def _choose_engine(engine: str) -> tuple[str, dict[str, Any]]:
    hw = detect_hardware().to_dict()
    if engine == "deterministic":
        return "deterministic", hw
    if engine == "neural":
        return "neural", hw
    return ("neural" if hw["recommended_engine"] == "neural-local" else "deterministic"), hw


def _make_deterministic_frames(
    refs: list[Path],
    *,
    style: str,
    preferred_reference: str | Path | None,
) -> tuple[dict[str, list[Image.Image]], dict[str, Any]]:
    canonical, candidates = choose_canonical(refs)
    if preferred_reference is not None:
        preferred = Path(preferred_reference).expanduser().resolve()
        match = next((c for c in candidates if c.path == preferred), None)
        if match is None:
            raise ValueError("preferred reference must also be supplied through --reference")
        canonical = match
    chosen_style = auto_style(canonical.cutout) if style == "auto" else style
    sprite = apply_style(canonical.cutout, chosen_style)
    frames = build_frames(sprite, capsule=chosen_style == "capsule-creature")
    identity = {
        "reference_count": len(refs),
        "reference_filenames": [p.name for p in refs],
        "canonical_reference": canonical.path.name,
        "style_requested": style,
        "style_used": chosen_style,
        "candidates": [
            {
                "filename": c.path.name,
                "score": round(c.score, 5),
                "foreground_fraction": round(c.foreground_fraction, 5),
                "edge_touch_fraction": round(c.edge_touch_fraction, 5),
                "sharpness": round(c.sharpness, 3),
            }
            for c in candidates
        ],
    }
    return frames, identity


def create_pet(
    references: Iterable[str | Path],
    *,
    name: str,
    output_dir: str | Path,
    pet_id: str | None = None,
    style: str = "auto",
    description: str | None = None,
    preferred_reference: str | Path | None = None,
    engine: str = "auto",
    backend: str = "auto",
    quality: str = "balanced",
    subject_type: str = "auto",
    identity_notes: str | None = None,
    seed: int = 42,
    cpu_offload: bool = True,
    neural_fallback: bool = True,
) -> dict[str, Any]:
    refs = [Path(p).expanduser().resolve() for p in references]
    if len(refs) < 2:
        raise ValueError("at least two reference images are required")
    for p in refs:
        if not p.is_file():
            raise FileNotFoundError(p)
    if style not in STYLE_PRESETS:
        raise ValueError(f"unknown style {style!r}")
    if engine not in ENGINE_CHOICES:
        raise ValueError(f"unknown engine {engine!r}")
    if quality not in QUALITY_CHOICES:
        raise ValueError(f"unknown quality {quality!r}")
    if subject_type not in SUBJECT_TYPES:
        raise ValueError(f"unknown subject type {subject_type!r}")

    output_dir = Path(output_dir).expanduser().resolve()
    run_dir = output_dir / "run"
    final_dir = run_dir / "final"
    qa_dir = run_dir / "qa"
    package_dir = output_dir / "package" / slugify(pet_id or name)
    for d in (final_dir, qa_dir, package_dir):
        d.mkdir(parents=True, exist_ok=True)

    selected_engine, hardware = _choose_engine(engine)
    chosen_style = style if style != "auto" else "soft-real"
    engine_error: str | None = None
    neural_metadata: dict[str, Any] | None = None

    if selected_engine == "neural":
        try:
            state_sprites, neural_metadata = generate_state_sprites(
                refs,
                backend_name=backend,
                style=chosen_style,
                subject_type=subject_type,
                identity_notes=identity_notes,
                quality=quality,
                seed=seed,
                work_dir=qa_dir,
                cpu_offload=cpu_offload,
            )
            frames = build_frames_from_sprites(
                state_sprites,
                capsule=chosen_style == "capsule-creature",
                derive_left=False,
            )
            identity = {
                "reference_count": len(refs),
                "reference_filenames": [p.name for p in refs],
                "style_requested": style,
                "style_used": chosen_style,
                "subject_type": subject_type,
                "identity_notes": identity_notes or "",
                "neural": neural_metadata,
            }
            engine_used = f"neural-local:{neural_metadata['backend']}"
        except Exception as exc:
            if engine == "neural" and not neural_fallback:
                raise
            engine_error = f"{type(exc).__name__}: {exc}"
            frames, identity = _make_deterministic_frames(
                refs,
                style=style,
                preferred_reference=preferred_reference,
            )
            chosen_style = identity["style_used"]
            engine_used = "local-deterministic-motion-puppet"
    else:
        frames, identity = _make_deterministic_frames(
            refs,
            style=style,
            preferred_reference=preferred_reference,
        )
        chosen_style = identity["style_used"]
        engine_used = "local-deterministic-motion-puppet"

    atlas_path = compose_atlas(frames, final_dir / "spritesheet.webp")
    validation = validate_atlas(atlas_path, edge_margin=2)
    write_validation(validation, final_dir / "validation.json")
    contact_sheet = qa_dir / "contact-sheet.png"
    make_contact_sheet(atlas_path, contact_sheet)
    preview_dir = render_previews(frames, qa_dir / "previews")

    metrics = _cell_metrics(frames)
    review = {
        "engine": engine_used,
        "ok": validation["ok"] and all(v["ok"] for v in metrics.values()),
        "engine_error": engine_error,
        "hardware": hardware,
        "rows": metrics,
        "note": (
            "Neural-local mode uses open-weight multi-reference image editing to invent semantically correct key poses, "
            "then deterministic micro-motion for stable animation. It does not call OpenAI ImageGen. "
            "Deterministic fallback remains available when hardware/dependencies are insufficient."
        ),
    }
    (qa_dir / "review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    (qa_dir / "identity-lock.json").write_text(json.dumps(identity, ensure_ascii=False, indent=2), encoding="utf-8")

    final_id = slugify(pet_id or name)
    manifest = {
        "id": final_id,
        "displayName": name,
        "description": description or f"PocketMen companion created from {len(refs)} reference images.",
        "spritesheetPath": "spritesheet.webp",
    }
    (package_dir / "pet.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    import shutil

    shutil.copy2(atlas_path, package_dir / "spritesheet.webp")

    summary = {
        "ok": bool(validation["ok"] and review["ok"]),
        "engine_requested": engine,
        "engine": engine_used,
        "backend_requested": backend,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pet_id": final_id,
        "display_name": name,
        "style": chosen_style,
        "subject_type": subject_type,
        "quality": quality,
        "reference_count": len(refs),
        "api_key_required": False,
        "hatch_pet_required": False,
        "openai_imagegen_used": False,
        "hardware": hardware,
        "neural_metadata": neural_metadata,
        "neural_fallback_reason": engine_error,
        "spritesheet": str(package_dir / "spritesheet.webp"),
        "pet_json": str(package_dir / "pet.json"),
        "validation": str(final_dir / "validation.json"),
        "contact_sheet": str(contact_sheet),
        "preview_dir": str(preview_dir),
        "review": str(qa_dir / "review.json"),
    }
    (qa_dir / "run-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
