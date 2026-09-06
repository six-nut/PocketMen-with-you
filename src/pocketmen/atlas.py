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


def validate_atlas(
    path: str | Path,
    *,
    edge_margin: int = 1,
    motion_baseline_jump_px: int = 18,
    motion_scale_ratio: float = 0.18,
) -> dict[str, Any]:
    path = Path(path)
    errors: list[str] = []
    warnings: list[str] = []
    cells: list[dict[str, Any]] = []
    motion: dict[str, Any] = {}

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
            row_baselines: list[int] = []
            row_widths: list[int] = []
            row_heights: list[int] = []
            prev = None
            max_baseline_jump = 0
            max_scale_jump = 0.0
            for col in range(COLUMNS):
                left, top = col * CELL_WIDTH, row_index * CELL_HEIGHT
                cell = image.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))
                used = col < frame_count
                nonzero = _nonzero_alpha(cell)
                info: dict[str, Any] = {
                    "state": state,
                    "row": row_index,
                    "column": col,
                    "used": used,
                    "nontransparent_pixels": nonzero,
                }
                frame_bbox = cell.getchannel("A").getbbox() if used else None
                if frame_bbox:
                    l, t, r, b = frame_bbox
                    width = max(1, r - l)
                    height = max(1, b - t)
                    baseline = b
                    info.update(
                        {
                            "bbox": list(frame_bbox),
                            "frame_width": width,
                            "frame_height": height,
                            "baseline": baseline,
                        }
                    )
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

                    if frame_bbox:
                        row_baselines.append(baseline)
                        row_widths.append(width)
                        row_heights.append(height)
                        if prev is not None:
                            p_baseline, p_width, p_height = prev
                            baseline_jump = abs(baseline - p_baseline)
                            max_baseline_jump = max(max_baseline_jump, baseline_jump)
                            if baseline_jump > motion_baseline_jump_px:
                                warnings.append(
                                    f"{state} frame {col + 1} baseline jump is {baseline_jump}px from frame {col} "
                                    f"(threshold {motion_baseline_jump_px}px)"
                                )
                            scale_jump = max(
                                abs(width - p_width) / max(1, p_width),
                                abs(height - p_height) / max(1, p_height),
                            )
                            max_scale_jump = max(max_scale_jump, scale_jump)
                            if scale_jump > motion_scale_ratio:
                                warnings.append(
                                    f"{state} frame {col + 1} scale jump is {scale_jump:.2f} from frame {col} "
                                    f"(threshold {motion_scale_ratio:.2f})"
                                )
                        prev = (baseline, width, height)

            if row_baselines:
                motion[state] = {
                    "used_frames": len(row_baselines),
                    "baseline_span_px": max(row_baselines) - min(row_baselines),
                    "max_baseline_jump_px": max_baseline_jump,
                    "max_scale_jump_ratio": round(max_scale_jump, 4),
                }
            else:
                motion[state] = {
                    "used_frames": 0,
                    "baseline_span_px": 0,
                    "max_baseline_jump_px": 0,
                    "max_scale_jump_ratio": 0.0,
                }

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
        "motion_consistency": motion,
        "transparent_rgb_residue": residue,
        "motion_thresholds": {
            "baseline_jump_px": motion_baseline_jump_px,
            "scale_jump_ratio": motion_scale_ratio,
        },
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
