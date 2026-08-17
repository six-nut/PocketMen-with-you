from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from PIL import Image


@dataclass(frozen=True)
class BackendInfo:
    name: str
    model_id: str
    license: str
    local_only: bool = True


class NeuralBackend(ABC):
    info: BackendInfo

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def edit(
        self,
        images: Sequence[Image.Image],
        prompt: str,
        *,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int = 0,
        quality: str = "balanced",
    ) -> Image.Image:
        raise NotImplementedError

    def model_cached(self) -> bool:
        try:
            from huggingface_hub import try_to_load_from_cache

            return try_to_load_from_cache(self.info.model_id, "model_index.json") is not None
        except (ImportError, OSError, ValueError):
            return False
