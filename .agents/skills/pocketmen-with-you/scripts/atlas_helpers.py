from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from .spec import ATLAS_HEIGHT, ATLAS_WIDTH, CELL_HEIGHT, CELL_WIDTH, COLUMNS, ROW_SPECS


def _nonzero_alpha(im: Image.Image) -> int:
    return sum(im.getchannel("A").histogram()[1:])


def _transparent_rgb_residue(im: Image.Image) -> int:
    raw = im.convert("RGBA").tobytes()
    return sum(
        1
        for i in range(0, len(raw), 4)
        if raw[i + 3] == 0 and (raw[i] or raw[i + 1] or raw[i + 2])
    )


def validate_atlas(path: str | Path, *, edge_margin: int = 1) -> dict[str, Any]:
    path = Path(path)
    errors: list[str] = []
    warnings: list[str] = []
    cells: list[dict[str, Any]] = []

    try:
        with Image.open(path) as src:
            source_format = src.format
            source_mode = src.mode
            image = src.convert("RGBA")
    except (OSError, ValueError) as exc:  # pragma: no cover - exercised by CLI
        return {"ok": False, "errors": [f"could not open atlas: {exc}"], "warnings": []}

    if image.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
        errors.append(f"expected {ATLAS_WIDTH}x{ATLAS_HEIGHT}, got {image.width}x{image.height}")
    if source_format not in {"PNG", "WEBP"}:
        errors.append(f"expected PNG or WebP, got {source_format}")
    if "A" not in source_mode:
        errors.append("atlas does not expose an alpha channel")

    if image.size == (ATLAS_WIDTH, ATLAS_HEIGHT):
        for row_index, (state, frame_count) in enumerate(ROW_SPECS):
            for col in range(COLUMNS):
                left, top = col * CELL_WIDTH, row_index * CELL_HEIGHT
                cell = image.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))
                used = col < frame_count
                nonzero = _nonzero_alpha(cell)
                info = {"state": state, "row": row_index, "column": col, "used": used, "nontransparent_pixels": nonzero}
                cells.append(info)
                if used and nonzero < 50:
                    errors.append(f"{state} frame {col + 1} is empty or too sparse")
                if not used and nonzero:
                    errors.append(f"unused cell {state} column {col + 1} is not transparent")
                if used and edge_margin > 0:
                    a = cell.getchannel("A")
                    bbox = a.getbbox()
                    if bbox:
                        l, t, r, b = bbox
                        if l <= edge_margin or t <= edge_margin or r >= CELL_WIDTH - edge_margin or b >= CELL_HEIGHT - edge_margin:
                            warnings.append(f"{state} frame {col + 1} touches or nearly touches a cell edge")

    residue = _transparent_rgb_residue(image)
    if residue:
        warnings.append(f"{residue} fully transparent pixels retain non-zero RGB values")

    return {
        "ok": not errors,
        "path": str(path),
        "format": source_format,
        "mode": source_mode,
        "size": list(image.size),
        "errors": errors,
        "warnings": warnings,
        "cells": cells,
        "transparent_rgb_residue": residue,
    }


def write_validation(result: dict[str, Any], output: str | Path) -> None:
    Path(output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def make_contact_sheet(atlas_path: str | Path, output: str | Path) -> None:
    with Image.open(atlas_path) as src:
        atlas = src.convert("RGBA")
    canvas = Image.new("RGBA", (ATLAS_WIDTH + 180, ATLAS_HEIGHT + 52), (248, 250, 253, 255))
    canvas.alpha_composite(atlas, (180, 52))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((180, 52, 180 + ATLAS_WIDTH - 1, 52 + ATLAS_HEIGHT - 1), outline=(160, 170, 185, 255), width=1)
    for c in range(COLUMNS + 1):
        x = 180 + c * CELL_WIDTH
        draw.line((x, 52, x, 52 + ATLAS_HEIGHT), fill=(190, 198, 210, 180), width=1)
    for r, (state, count) in enumerate(ROW_SPECS):
        y = 52 + r * CELL_HEIGHT
        draw.line((180, y, 180 + ATLAS_WIDTH, y), fill=(190, 198, 210, 180), width=1)
        draw.text((16, y + 8), f"{r}: {state}", fill=(25, 35, 50, 255))
        draw.text((16, y + 30), f"frames: {count}", fill=(90, 100, 116, 255))
    for c in range(COLUMNS):
        draw.text((180 + c * CELL_WIDTH + 8, 16), str(c + 1), fill=(25, 35, 50, 255))
    canvas.convert("RGB").save(output, quality=92)
