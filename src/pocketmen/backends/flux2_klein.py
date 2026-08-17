from __future__ import annotations

from collections.abc import Sequence

from PIL import Image

from .base import BackendInfo, NeuralBackend


class Flux2KleinBackend(NeuralBackend):
    info = BackendInfo(
        name="flux2-klein-4b",
        model_id="black-forest-labs/FLUX.2-klein-4B",
        license="Apache-2.0",
    )

    def __init__(self, *, cpu_offload: bool = True):
        self.cpu_offload = cpu_offload
        self.pipe = None
        self.torch = None
        self.device = "cuda"

    def load(self) -> None:
        if self.pipe is not None:
            return
        try:
            import torch
            from diffusers import DiffusionPipeline
        except Exception as exc:
            raise RuntimeError(
                "FLUX.2 klein backend requires the PocketMen neural runtime. "
                "Run PREPARE_NEURAL_ENGINE.bat or setup_runtime.py --profile neural."
            ) from exc
        if not torch.cuda.is_available():
            raise RuntimeError("FLUX.2 klein automatic profile currently requires an NVIDIA CUDA GPU.")
        self.torch = torch
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        self.pipe = DiffusionPipeline.from_pretrained(self.info.model_id, torch_dtype=dtype)
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
        refs = [im.convert("RGB") for im in images]
        kwargs = {
            "prompt": prompt,
            "height": height,
            "width": width,
            "guidance_scale": 1.0,
            "num_inference_steps": 4,
            "generator": self.torch.Generator(device="cuda").manual_seed(seed),
        }
        if refs:
            kwargs["image"] = refs if len(refs) > 1 else refs[0]
        # Distilled Klein is optimized for four steps; 'max' spends quality budget
        # on better reference selection and a repair pass rather than extra steps.
        return self.pipe(**kwargs).images[0]
