from __future__ import annotations

from collections.abc import Sequence

from PIL import Image

from .base import BackendInfo, NeuralBackend


class QwenImageEdit2511Backend(NeuralBackend):
    info = BackendInfo(
        name="qwen-image-edit-2511",
        model_id="Qwen/Qwen-Image-Edit-2511",
        license="Apache-2.0",
    )

    def __init__(self, *, cpu_offload: bool = True):
        self.cpu_offload = cpu_offload
        self.pipe = None
        self.torch = None

    def load(self) -> None:
        if self.pipe is not None:
            return
        try:
            import torch
            from diffusers import DiffusionPipeline
        except Exception as exc:
            raise RuntimeError(
                "Qwen Image Edit 2511 requires the identity-max neural profile. "
                "Run setup_runtime.py --profile identity-max."
            ) from exc
        if not torch.cuda.is_available():
            raise RuntimeError("Qwen Image Edit 2511 automatic profile currently requires an NVIDIA CUDA GPU.")
        self.torch = torch
        self.pipe = DiffusionPipeline.from_pretrained(
            self.info.model_id,
            torch_dtype=torch.bfloat16,
        )
        if self.cpu_offload:
            self.pipe.enable_model_cpu_offload()
        else:
            self.pipe.to("cuda")
        self.pipe.set_progress_bar_config(disable=False)

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
        self.load()
        assert self.pipe is not None and self.torch is not None
        refs = [im.convert("RGB") for im in images][:3]
        steps = 40 if quality != "max" else 50
        result = self.pipe(
            image=refs,
            prompt=prompt,
            negative_prompt=negative_prompt or " ",
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            num_inference_steps=steps,
            generator=self.torch.Generator(device="cuda").manual_seed(seed),
            num_images_per_prompt=1,
        )
        return result.images[0]
