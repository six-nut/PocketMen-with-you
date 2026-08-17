from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


@dataclass(frozen=True)
class CutoutCandidate:
    path: Path
    cutout: Image.Image
    score: float
    foreground_fraction: float
    edge_touch_fraction: float
    sharpness: float


def load_rgb(path: str | Path) -> Image.Image:
    with Image.open(path) as src:
        return ImageOps.exif_transpose(src).convert("RGB")


def _resize_for_processing(image: Image.Image, max_side: int = 800) -> tuple[Image.Image, float]:
    w, h = image.size
    scale = min(1.0, max_side / max(w, h))
    if scale == 1.0:
        return image.copy(), 1.0
    return image.resize((max(2, round(w * scale)), max(2, round(h * scale))), Image.Resampling.LANCZOS), scale


def _largest_useful_components(mask: np.ndarray) -> np.ndarray:
    binary = (mask > 0).astype(np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if count <= 1:
        return binary
    h, w = binary.shape
    cx, cy = w / 2.0, h / 2.0
    candidates: list[tuple[float, int]] = []
    largest = max(int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, count))
    for i in range(1, count):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area < max(64, largest * 0.08):
            continue
        px, py = centroids[i]
        dist = ((px - cx) / max(w, 1)) ** 2 + ((py - cy) / max(h, 1)) ** 2
        score = area * (1.0 - min(0.6, dist))
        candidates.append((score, i))
    if not candidates:
        idx = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        return (labels == idx).astype(np.uint8)
    candidates.sort(reverse=True)
    keep = [i for _, i in candidates[:3]]
    out = np.isin(labels, keep).astype(np.uint8)
    return out


def _grabcut_mask(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image, dtype=np.uint8)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    if min(w, h) < 24:
        raise ValueError("reference image is too small")

    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    border = max(2, round(min(w, h) * 0.025))
    mask[:border, :] = cv2.GC_BGD
    mask[-border:, :] = cv2.GC_BGD
    mask[:, :border] = cv2.GC_BGD
    mask[:, -border:] = cv2.GC_BGD

    # Give GrabCut a strong but not absolute center prior. This works well for portraits/pets
    # while still allowing the foreground to touch the image edge after refinement.
    x1, x2 = int(w * 0.18), int(w * 0.82)
    y1, y2 = int(h * 0.10), int(h * 0.90)
    mask[y1:y2, x1:x2] = cv2.GC_PR_FGD
    ix1, ix2 = int(w * 0.34), int(w * 0.66)
    iy1, iy2 = int(h * 0.25), int(h * 0.70)
    mask[iy1:iy2, ix1:ix2] = cv2.GC_FGD

    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bg_model, fg_model, 3, cv2.GC_INIT_WITH_MASK)
    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)

    kernel = np.ones((3, 3), np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=1)
    fg = _largest_useful_components(fg)
    return fg


def _fallback_center_mask(size: tuple[int, int]) -> np.ndarray:
    w, h = size
    mask = np.zeros((h, w), np.uint8)
    center = (w // 2, h // 2)
    axes = (max(3, int(w * 0.38)), max(3, int(h * 0.46)))
    cv2.ellipse(mask, center, axes, 0, 0, 360, 1, -1)
    return mask


def extract_foreground(path: str | Path, *, max_side: int = 800, feather: float = 1.7) -> CutoutCandidate:
    path = Path(path)
    original = load_rgb(path)
    work, _ = _resize_for_processing(original, max_side=max_side)
    try:
        binary = _grabcut_mask(work)
    except (ValueError, cv2.error):
        binary = _fallback_center_mask(work.size)

    h, w = binary.shape
    fg_fraction = float(binary.mean())
    if fg_fraction < 0.035 or fg_fraction > 0.94:
        binary = _fallback_center_mask(work.size)
        fg_fraction = float(binary.mean())

    alpha = (binary * 255).astype(np.uint8)
    sigma = max(0.0, float(feather))
    if sigma:
        k = max(3, round(sigma * 4) | 1)
        alpha = cv2.GaussianBlur(alpha, (k, k), sigmaX=sigma, sigmaY=sigma)
        alpha = np.where(alpha < 8, 0, alpha).astype(np.uint8)

    rgba = work.convert("RGBA")
    rgba.putalpha(Image.fromarray(alpha, mode="L"))
    bbox = rgba.getchannel("A").getbbox()
    if bbox:
        pad = max(2, round(min(work.size) * 0.015))
        l, t, r, b = bbox
        bbox = (max(0, l - pad), max(0, t - pad), min(work.width, r + pad), min(work.height, b + pad))
        rgba = rgba.crop(bbox)

    edge_band = max(1, round(min(w, h) * 0.025))
    edge_pixels = np.concatenate(
        [
            binary[:edge_band, :].ravel(),
            binary[-edge_band:, :].ravel(),
            binary[:, :edge_band].ravel(),
            binary[:, -edge_band:].ravel(),
        ]
    )
    edge_touch = float(edge_pixels.mean()) if edge_pixels.size else 0.0

    gray = cv2.cvtColor(np.asarray(work), cv2.COLOR_RGB2GRAY)
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    occupancy_score = 1.0 - min(1.0, abs(fg_fraction - 0.42) / 0.42)
    score = 0.55 * occupancy_score + 0.35 * min(1.0, sharpness / 450.0) + 0.10 * (1.0 - edge_touch)

    return CutoutCandidate(path, rgba, score, fg_fraction, edge_touch, sharpness)


def choose_canonical(references: Iterable[str | Path]) -> tuple[CutoutCandidate, list[CutoutCandidate]]:
    candidates = [extract_foreground(p) for p in references]
    if len(candidates) < 2:
        raise ValueError("PocketMen requires at least two reference images by default")
    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[0], candidates


def enhance_soft_real(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    rgb = Image.new("RGB", rgba.size, "white")
    rgb.paste(rgba.convert("RGB"), mask=rgba.getchannel("A"))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.04)
    rgb = ImageEnhance.Color(rgb).enhance(1.04)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.14)
    out = rgb.convert("RGBA")
    out.putalpha(rgba.getchannel("A"))
    return out


def smooth_plush(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB").filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.MedianFilter(3))
    rgb = ImageEnhance.Color(rgb).enhance(1.08)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    out = rgb.convert("RGBA")
    alpha = rgba.getchannel("A").filter(ImageFilter.GaussianBlur(0.65))
    out.putalpha(alpha)
    return out


def hero_chibi_warp(image: Image.Image) -> Image.Image:
    """A deterministic, identity-preserving chibi-ish proportion transform.

    It deliberately avoids hallucinating unseen clothing or facial details. The upper body/head
    is enlarged modestly and the lower body is compressed, so the result stays recognizably
    photographic rather than pretending to be full generative character art.
    """
    src = image.convert("RGBA")
    bbox = src.getchannel("A").getbbox()
    if not bbox:
        return src
    subject = src.crop(bbox)
    w, h = subject.size
    split = max(1, min(h - 1, int(h * 0.44)))
    top = subject.crop((0, 0, w, split))
    bottom = subject.crop((0, split, w, h))

    top_scale = 1.12
    bottom_scale_x = 0.92
    bottom_scale_y = 0.90
    top2 = top.resize((max(1, round(w * top_scale)), max(1, round(split * top_scale))), Image.Resampling.LANCZOS)
    bottom2 = bottom.resize(
        (max(1, round(w * bottom_scale_x)), max(1, round((h - split) * bottom_scale_y))),
        Image.Resampling.LANCZOS,
    )
    overlap = max(2, round(h * 0.025))
    out_w = max(top2.width, bottom2.width)
    out_h = top2.height + bottom2.height - overlap
    canvas = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    canvas.alpha_composite(top2, ((out_w - top2.width) // 2, 0))
    canvas.alpha_composite(bottom2, ((out_w - bottom2.width) // 2, top2.height - overlap))
    return canvas
