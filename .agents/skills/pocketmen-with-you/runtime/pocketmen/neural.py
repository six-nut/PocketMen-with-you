from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .backends import make_backend
from .imageops import choose_canonical
from .prompts import NEGATIVE_PROMPT, canonical_prompt, state_prompt
from .spec import ROW_SPECS

CHROMA_CANDIDATES = [
    (0, 255, 70),       # green
    (255, 0, 220),      # magenta
    (0, 230, 255),      # cyan
    (255, 235, 0),      # yellow
]


def _sample_reference_colors(paths: list[Path]) -> np.ndarray:
    colors = []
    for p in paths[:3]:
        im = Image.open(p).convert("RGB")
        im.thumbnail((160, 160))
        arr = np.asarray(im, dtype=np.float32).reshape(-1, 3)
        if len(arr) > 4000:
            arr = arr[:: max(1, len(arr) // 4000)]
        colors.append(arr)
    if not colors:
        return np.zeros((1, 3), dtype=np.float32)
    return np.concatenate(colors, axis=0)


def choose_chroma(paths: list[Path]) -> tuple[int, int, int]:
    pixels = _sample_reference_colors(paths)
    best = CHROMA_CANDIDATES[0]
    best_score = -1.0
    for c in CHROMA_CANDIDATES:
        d = np.linalg.norm(pixels - np.array(c, dtype=np.float32), axis=1)
        # A good chroma is far from both typical and nearest subject colors.
        score = float(np.percentile(d, 10) * 0.65 + np.median(d) * 0.35)
        if score > best_score:
            best_score, best = score, c
    return best


def chroma_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def remove_chroma(image: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    """Remove a flat model-generated chroma background with edge-connected flood fill.

    Only pixels chroma-like *and connected to an image border* are treated as background,
    which protects same-colored eyes/accessories inside the subject.
    """
    arr = np.asarray(image.convert("RGB"), dtype=np.uint8)
    target = np.array(rgb, dtype=np.int16)
    diff = np.linalg.norm(arr.astype(np.int16) - target, axis=2)
    candidate = (diff < 92).astype(np.uint8) * 255

    # Close small holes in the chroma region, then keep only border-connected components.
    kernel = np.ones((5, 5), np.uint8)
    candidate = cv2.morphologyEx(candidate, cv2.MORPH_CLOSE, kernel, iterations=2)
    _, labels, _, _ = cv2.connectedComponentsWithStats(candidate, connectivity=8)
    border_labels: set[int] = set()
    h, w = candidate.shape
    for edge in (labels[0, :], labels[h - 1, :], labels[:, 0], labels[:, w - 1]):
        border_labels.update(int(x) for x in np.unique(edge) if x != 0)
    bg = np.isin(labels, list(border_labels)).astype(np.uint8) * 255

    # Feather inward slightly for anti-aliased hair/fur edges.
    bg_soft = cv2.GaussianBlur(bg, (0, 0), sigmaX=1.15, sigmaY=1.15)
    alpha = 255 - bg_soft
    alpha[diff > 135] = 255

    rgba = np.dstack([arr, alpha.astype(np.uint8)])
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getchannel("A").getbbox()
    if bbox:
        out = out.crop(bbox)
    return out


def _save_debug(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def _identity_refs(ref_paths: list[Path], canonical_render: Image.Image) -> list[Image.Image]:
    # Canonical render leads; two raw references keep fine identity anchors.
    result = [canonical_render.convert("RGB")]
    for p in ref_paths[:2]:
        result.append(Image.open(p).convert("RGB"))
    return result[:3]


def generate_state_sprites(
    references: Iterable[str | Path],
    *,
    backend_name: str,
    style: str,
    subject_type: str,
    identity_notes: str | None,
    quality: str,
    seed: int,
    work_dir: str | Path,
    cpu_offload: bool = True,
) -> tuple[dict[str, Image.Image], dict]:
    refs = [Path(p).expanduser().resolve() for p in references]
    work = Path(work_dir)
    raw_dir = work / "neural-raw"
    cutout_dir = work / "neural-cutouts"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cutout_dir.mkdir(parents=True, exist_ok=True)

    backend = make_backend(backend_name, cpu_offload=cpu_offload)
    backend.load()
    chroma = choose_chroma(refs)
    bg = chroma_hex(chroma)

    _, ranked_candidates = choose_canonical(refs)
    ranked_paths = [c.path for c in ranked_candidates[:3]]
    raw_refs = [Image.open(p).convert("RGB") for p in ranked_paths]
    can_prompt = canonical_prompt(
        style=style,
        subject_type=subject_type,
        identity_notes=identity_notes,
        chroma_hex=bg,
    )
    canonical = backend.edit(
        raw_refs,
        can_prompt,
        negative_prompt=NEGATIVE_PROMPT,
        seed=seed,
        quality=quality,
    )
    _save_debug(canonical, raw_dir / "canonical.png")
    canonical_cut = remove_chroma(canonical, chroma)
    _save_debug(canonical_cut, cutout_dir / "canonical.png")

    state_sprites: dict[str, Image.Image] = {}
    refs_for_states = _identity_refs(ranked_paths, canonical)
    failures: dict[str, str] = {}
    generation_order = [state for state, _ in ROW_SPECS]
    if quality == "draft":
        for state in generation_order:
            state_sprites[state] = canonical_cut.copy()
            _save_debug(state_sprites[state], cutout_dir / f"{state}.png")
    for idx, state in enumerate(generation_order if quality != "draft" else []):
        # In balanced mode the left-running row is derived from the right-running
        # neural key pose to minimize both identity drift and compute.
        if state == "running-left" and quality != "max" and "running-right" in state_sprites:
            state_sprites[state] = state_sprites["running-right"].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            _save_debug(state_sprites[state], cutout_dir / f"{state}.png")
            continue
        prompt = state_prompt(
            state,
            style=style,
            subject_type=subject_type,
            identity_notes=identity_notes,
            chroma_hex=bg,
        )
        try:
            generated = backend.edit(
                refs_for_states,
                prompt,
                negative_prompt=NEGATIVE_PROMPT,
                seed=seed + 1009 * (idx + 1),
                quality=quality,
            )
            _save_debug(generated, raw_dir / f"{state}.png")
            cut = remove_chroma(generated, chroma)
            if cut.getchannel("A").getbbox() is None:
                raise RuntimeError("chroma extraction produced an empty subject")
            state_sprites[state] = cut
            _save_debug(cut, cutout_dir / f"{state}.png")
        except Exception as exc:  # noqa: BLE001 - backend-specific failures must reuse canonical art
            failures[state] = f"{type(exc).__name__}: {exc}"
            # A local generative row must never block atlas creation after the
            # expensive model is already loaded. Reuse canonical art as a safe row.
            state_sprites[state] = canonical_cut.copy()

    metadata = {
        "backend": backend.info.name,
        "model_id": backend.info.model_id,
        "model_license": backend.info.license,
        "quality": quality,
        "seed": seed,
        "chroma_rgb": list(chroma),
        "chroma_hex": bg,
        "state_failures": failures,
        "ranked_reference_filenames": [p.name for p in ranked_paths],
        "generation_calls": (
            1
            if quality == "draft"
            else 1 + sum(1 for s in generation_order if not (s == "running-left" and quality != "max"))
        ),
    }
    (work / "neural-generation.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return state_sprites, metadata
