from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image, ImageDraw

from .spec import CELL_HEIGHT, CELL_WIDTH, ROW_SPECS
from .styles import draw_companion_capsule


@dataclass(frozen=True)
class Motion:
    dx: float = 0.0
    dy: float = 0.0
    sx: float = 1.0
    sy: float = 1.0
    angle: float = 0.0
    flip: bool = False
    prop: str | None = None


def _phase(i: int, count: int) -> float:
    return 2.0 * math.pi * i / max(count, 1)


def motion_for(state: str, i: int, count: int) -> Motion:
    p = _phase(i, count)
    if state == "idle":
        return Motion(dy=-1.5 * math.sin(p), sx=1.0 + 0.012 * math.sin(p), sy=1.0 - 0.010 * math.sin(p), angle=0.8 * math.sin(p))
    if state == "running-right":
        return Motion(dy=-4.5 * abs(math.sin(p)), sx=1.0 + 0.035 * math.sin(p), sy=1.0 - 0.028 * math.sin(p), angle=2.8 * math.sin(p), flip=False)
    if state == "running-left":
        return Motion(dy=-4.5 * abs(math.sin(p)), sx=1.0 + 0.035 * math.sin(p), sy=1.0 - 0.028 * math.sin(p), angle=-2.8 * math.sin(p), flip=True)
    if state == "waving":
        seq = (-5.0, 4.0, -5.0, 4.0)
        return Motion(dx=2.0 * math.sin(p), dy=-2.0 * abs(math.sin(p)), angle=seq[i % len(seq)])
    if state == "jumping":
        lift = (2.0, -16.0, -28.0, -16.0, 2.0)[i % 5]
        squash = (0.96, 1.04, 1.08, 1.04, 0.96)[i % 5]
        return Motion(dy=lift, sx=1.0 / squash, sy=squash)
    if state == "failed":
        angles = (0.0, 5.0, 10.0, 15.0, 17.0, 12.0, 7.0, 2.0)
        dys = (0.0, 1.0, 4.0, 7.0, 9.0, 8.0, 5.0, 2.0)
        return Motion(dy=dys[i % 8], sx=1.0 + 0.02 * math.sin(p), sy=0.98 - 0.05 * abs(math.sin(p / 2.0)), angle=angles[i % 8])
    if state == "waiting":
        return Motion(dx=2.2 * math.sin(p), dy=-1.0 * math.cos(p), angle=2.5 * math.sin(p))
    if state == "running":
        return Motion(dy=-1.5 * abs(math.sin(p * 2.0)), angle=1.2 * math.sin(p), prop="laptop")
    if state == "review":
        return Motion(dx=1.0 * math.sin(p), dy=1.0 * math.cos(p), angle=-1.8 + 1.2 * math.sin(p), prop="paper")
    raise KeyError(state)


def _fit_sprite(sprite: Image.Image, max_w: int, max_h: int) -> Image.Image:
    src = sprite.convert("RGBA")
    bbox = src.getchannel("A").getbbox()
    if bbox:
        src = src.crop(bbox)
    scale = min(max_w / max(src.width, 1), max_h / max(src.height, 1), 1.0)
    if scale < 1.0:
        src = src.resize((max(1, round(src.width * scale)), max(1, round(src.height * scale))), Image.Resampling.LANCZOS)
    return src


def _transform(sprite: Image.Image, motion: Motion) -> Image.Image:
    src = sprite.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if motion.flip else sprite
    w = max(1, round(src.width * motion.sx))
    h = max(1, round(src.height * motion.sy))
    src = src.resize((w, h), Image.Resampling.LANCZOS)
    if motion.angle:
        src = src.rotate(motion.angle, resample=Image.Resampling.BICUBIC, expand=True)
    return src


def _draw_laptop(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    y = int(CELL_HEIGHT * 0.72)
    x1, x2 = int(CELL_WIDTH * 0.34), int(CELL_WIDTH * 0.70)
    h = int(CELL_HEIGHT * 0.18)
    draw.rounded_rectangle((x1, y - h, x2, y), radius=4, fill=(48, 56, 70, 245), outline=(18, 24, 34, 255), width=2)
    draw.polygon([(x1 - 8, y + 1), (x2 + 8, y + 1), (x2 + 16, y + 8), (x1 - 16, y + 8)], fill=(81, 90, 106, 245))


def _draw_paper(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    x1, y1 = int(CELL_WIDTH * 0.36), int(CELL_HEIGHT * 0.68)
    x2, y2 = int(CELL_WIDTH * 0.70), int(CELL_HEIGHT * 0.84)
    draw.rounded_rectangle((x1, y1, x2, y2), radius=4, fill=(248, 248, 244, 245), outline=(77, 86, 101, 255), width=2)
    for j in range(3):
        yy = y1 + 8 + j * 8
        draw.line((x1 + 9, yy, x2 - 9, yy), fill=(140, 148, 160, 220), width=2)


def render_frame(sprite: Image.Image, state: str, index: int, frame_count: int, *, capsule: bool = False) -> Image.Image:
    canvas = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    if capsule:
        canvas.alpha_composite(draw_companion_capsule(canvas.size))

    motion = motion_for(state, index, frame_count)
    subject = _fit_sprite(sprite, int(CELL_WIDTH * 0.70), int(CELL_HEIGHT * 0.74))
    subject = _transform(subject, motion)
    x = round((CELL_WIDTH - subject.width) / 2 + motion.dx)
    baseline = int(CELL_HEIGHT * 0.88)
    y = round(baseline - subject.height + motion.dy)
    x = max(3, min(CELL_WIDTH - subject.width - 3, x))
    y = max(3, min(CELL_HEIGHT - subject.height - 3, y))
    canvas.alpha_composite(subject, (x, y))

    # Props deliberately overlap the subject to read as an attached activity, not detached UI.
    if motion.prop == "laptop":
        _draw_laptop(canvas)
    elif motion.prop == "paper":
        _draw_paper(canvas)
    return canvas


def build_frames(sprite: Image.Image, *, capsule: bool = False) -> dict[str, list[Image.Image]]:
    result: dict[str, list[Image.Image]] = {}
    for state, count in ROW_SPECS:
        result[state] = [render_frame(sprite, state, i, count, capsule=capsule) for i in range(count)]
    return result


def build_frames_from_sprites(
    sprites: dict[str, Image.Image], *, capsule: bool = False, derive_left: bool = False
) -> dict[str, list[Image.Image]]:
    """Build micro-animation frames from state-specific neural key poses.

    The neural engine invents the semantically correct key pose; deterministic transforms
    add subtle temporal motion without forcing dozens of independent generations that
    would otherwise increase identity flicker.
    """
    result: dict[str, list[Image.Image]] = {}
    for state, count in ROW_SPECS:
        if state not in sprites:
            raise KeyError(f"missing state sprite: {state}")
        sprite = sprites[state]
        # Neural sprites already encode their facing direction. Avoid the legacy
        # running-left mirror unless the caller explicitly supplied a right-facing source.
        frames = []
        for i in range(count):
            motion = motion_for(state, i, count)
            if state == "running-left" and not derive_left:
                motion = Motion(
                    dx=motion.dx, dy=motion.dy, sx=motion.sx, sy=motion.sy,
                    angle=motion.angle, flip=False, prop=motion.prop
                )
            frames.append(_render_with_motion(sprite, motion, capsule=capsule))
        result[state] = frames
    return result


def _render_with_motion(sprite: Image.Image, motion: Motion, *, capsule: bool = False) -> Image.Image:
    canvas = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    if capsule:
        canvas.alpha_composite(draw_companion_capsule(canvas.size))
    subject = _fit_sprite(sprite, int(CELL_WIDTH * 0.70), int(CELL_HEIGHT * 0.74))
    subject = _transform(subject, motion)
    x = round((CELL_WIDTH - subject.width) / 2 + motion.dx)
    baseline = int(CELL_HEIGHT * 0.88)
    y = round(baseline - subject.height + motion.dy)
    x = max(3, min(CELL_WIDTH - subject.width - 3, x))
    y = max(3, min(CELL_HEIGHT - subject.height - 3, y))
    canvas.alpha_composite(subject, (x, y))
    if motion.prop == "laptop":
        _draw_laptop(canvas)
    elif motion.prop == "paper":
        _draw_paper(canvas)
    return canvas
