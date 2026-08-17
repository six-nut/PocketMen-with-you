from __future__ import annotations

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from .imageops import enhance_soft_real, hero_chibi_warp, smooth_plush

STYLE_PRESETS = ("auto", "soft-real", "hero-chibi", "plush", "capsule-creature")


def apply_style(image: Image.Image, style: str) -> Image.Image:
    if style not in STYLE_PRESETS:
        raise ValueError(f"unknown style {style!r}; choose from {', '.join(STYLE_PRESETS)}")
    if style in {"auto", "soft-real"}:
        return enhance_soft_real(image)
    if style == "hero-chibi":
        return hero_chibi_warp(enhance_soft_real(image))
    if style == "plush":
        return smooth_plush(image)
    if style == "capsule-creature":
        base = smooth_plush(image)
        rgb = base.convert("RGB")
        rgb = ImageEnhance.Color(rgb).enhance(1.12)
        rgb = rgb.filter(ImageFilter.SMOOTH)
        out = rgb.convert("RGBA")
        out.putalpha(base.getchannel("A"))
        return out
    raise AssertionError(style)


def draw_companion_capsule(size: tuple[int, int]) -> Image.Image:
    """Draw PocketMen's original red/yellow companion capsule, not a third-party capture-ball mark."""
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = w // 2, int(h * 0.70)
    radius = int(min(w, h) * 0.19)
    box = (cx - radius, cy - radius, cx + radius, cy + radius)
    draw.ellipse(box, fill=(247, 199, 62, 235), outline=(31, 46, 72, 255), width=max(2, radius // 12))
    # Diagonal red panel, clipped approximately within the circular body.
    poly = [
        (cx - radius + 4, cy - radius // 2),
        (cx + radius // 2, cy - radius + 4),
        (cx + radius - 4, cy + radius // 3),
        (cx - radius // 3, cy + radius - 4),
    ]
    draw.polygon(poly, fill=(235, 67, 72, 235))
    band_w = max(4, radius // 7)
    draw.line((cx - radius * 0.72, cy + radius * 0.62, cx + radius * 0.68, cy - radius * 0.58), fill=(31, 46, 72, 255), width=band_w)
    core_r = max(5, radius // 4)
    draw.ellipse((cx - core_r, cy - core_r, cx + core_r, cy + core_r), fill=(255, 255, 255, 255), outline=(31, 46, 72, 255), width=max(2, core_r // 5))
    # tiny heart core
    hr = max(2, core_r // 3)
    draw.ellipse((cx - hr - 1, cy - hr, cx + 1, cy + 1), fill=(235, 67, 72, 255))
    draw.ellipse((cx - 1, cy - hr, cx + hr + 1, cy + 1), fill=(235, 67, 72, 255))
    draw.polygon([(cx - hr - 1, cy), (cx + hr + 1, cy), (cx, cy + hr + 2)], fill=(235, 67, 72, 255))
    return layer
