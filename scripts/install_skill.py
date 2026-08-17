from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _detect_vram_gb() -> float | None:
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        cp = subprocess.run(
            [exe, "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            check=True,
            capture_output=True,
            text=True,
            timeout=8,
        )
        return float(cp.stdout.strip().splitlines()[0]) / 1024.0
    except (IndexError, OSError, subprocess.SubprocessError, ValueError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        default=str(Path(__file__).resolve().parents[1] / ".agents" / "skills" / "pocketmen-with-you"),
    )
    parser.add_argument("--no-runtime", action="store_true")
    parser.add_argument("--profile", choices=("auto", "core", "neural", "identity-max"), default="auto")
    args = parser.parse_args()
    src = Path(args.source).resolve()
    if not (src / "SKILL.md").is_file():
        raise SystemExit(f"SKILL.md not found under {src}")
    dest_root = Path.home() / ".agents" / "skills"
    dest = dest_root / "pocketmen-with-you"
    dest_root.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    print(f"Installed PocketMen skill to: {dest}")

    if not args.no_runtime:
        profile = args.profile
        if profile == "auto":
            vram = _detect_vram_gb()
            profile = "neural" if (vram is not None and vram >= 12.5) else "core"
            print(f"Auto runtime profile: {profile} (detected VRAM: {vram if vram is not None else 'n/a'} GB)")
        setup = dest / "scripts" / "setup_runtime.py"
        subprocess.check_call([sys.executable, str(setup), "--skill-dir", str(dest), "--profile", profile])
    else:
        print("Runtime setup skipped. Run scripts/setup_runtime.py before the first creation.")

    print("PocketMen v0.3 uses a local open-weight neural engine when supported and never requires OPENAI_API_KEY.")
    print("The first neural creation downloads model weights to the normal Hugging Face cache.")
    print("If Codex does not show the new skill immediately, restart Codex.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
