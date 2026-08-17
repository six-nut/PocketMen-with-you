from __future__ import annotations

from .base import NeuralBackend
from .flux2_klein import Flux2KleinBackend
from .qwen_edit import QwenImageEdit2511Backend

BACKENDS = ("auto", "flux2-klein-4b", "qwen-image-edit-2511")


def make_backend(name: str, *, cpu_offload: bool = True) -> NeuralBackend:
    if name in ("auto", "flux2-klein-4b"):
        return Flux2KleinBackend(cpu_offload=cpu_offload)
    if name == "qwen-image-edit-2511":
        return QwenImageEdit2511Backend(cpu_offload=cpu_offload)
    raise ValueError(f"unknown neural backend {name!r}")


__all__ = ["BACKENDS", "NeuralBackend", "make_backend"]
