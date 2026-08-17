from __future__ import annotations

import argparse
import os
import subprocess
import venv
from pathlib import Path


def _python(env_dir: Path) -> Path:
    return env_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an isolated PocketMen runtime")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--profile", choices=("core", "neural", "identity-max"), default="core")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--download-model", action="store_true")
    args = parser.parse_args()
    skill = Path(args.skill_dir).resolve()
    env_dir = skill / ".venv"
    if env_dir.exists() and args.force:
        import shutil

        shutil.rmtree(env_dir)
    if not env_dir.exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(env_dir)
    py = _python(env_dir)
    subprocess.check_call([str(py), "-m", "pip", "install", "--disable-pip-version-check", "-U", "pip", "wheel"])
    subprocess.check_call(
        [str(py), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(skill / "requirements-local.txt")]
    )
    if args.profile in ("neural", "identity-max"):
        req = skill / ("requirements-neural.txt" if args.profile == "neural" else "requirements-identity-max.txt")
        subprocess.check_call([str(py), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(req)])
    if args.download_model:
        model = "black-forest-labs/FLUX.2-klein-4B" if args.profile != "identity-max" else "Qwen/Qwen-Image-Edit-2511"
        subprocess.check_call(
            [
                str(py),
                "-c",
                "from huggingface_hub import snapshot_download; import sys; snapshot_download(sys.argv[1])",
                model,
            ]
        )
    print(py)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
