from __future__ import annotations

import json
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class HardwareProfile:
    platform: str
    python: str
    cuda_available: bool
    cuda_device: str | None
    vram_gb: float | None
    mps_available: bool
    recommended_engine: str
    recommended_backend: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def _nvidia_smi() -> tuple[str | None, float | None]:
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None, None
    try:
        cp = subprocess.run(
            [
                exe,
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=8,
        )
        line = cp.stdout.strip().splitlines()[0]
        name, mib = [x.strip() for x in line.rsplit(",", 1)]
        return name, round(float(mib) / 1024.0, 2)
    except (IndexError, OSError, subprocess.SubprocessError, ValueError):
        return None, None


def detect_hardware() -> HardwareProfile:
    device_name, vram = _nvidia_smi()
    cuda = bool(device_name)
    mps = False
    try:
        import torch
    except (ImportError, OSError):
        torch = None

    if torch is not None:
        try:
            if torch.cuda.is_available():
                cuda = True
                device_name = torch.cuda.get_device_name(0)
                vram = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
            mps = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
        except (AssertionError, RuntimeError):
            mps = False

    # FLUX.2 klein 4B's official model card reports ~13 GB VRAM. We use a
    # conservative automatic threshold; explicit users can still try CPU offload.
    if cuda and vram is not None and vram >= 12.5:
        engine = "neural-local"
        backend = "flux2-klein-4b"
        reason = "NVIDIA GPU has enough VRAM for the commercial-friendly local neural backend."
    elif mps:
        engine = "deterministic"
        backend = "deterministic"
        reason = "Apple MPS detected; deterministic mode is the safe default until a validated MPS neural profile is installed."
    else:
        engine = "deterministic"
        backend = "deterministic"
        reason = "No >=12.5 GB NVIDIA CUDA device detected; use deterministic mode or explicitly enable CPU-offloaded neural inference."

    return HardwareProfile(
        platform=platform.platform(),
        python=platform.python_version(),
        cuda_available=cuda,
        cuda_device=device_name,
        vram_gb=vram,
        mps_available=mps,
        recommended_engine=engine,
        recommended_backend=backend,
        reason=reason,
    )


def doctor_json() -> str:
    return json.dumps(detect_hardware().to_dict(), ensure_ascii=False, indent=2)
