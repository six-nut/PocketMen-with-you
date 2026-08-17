from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Prepare PocketMen Neural Local Studio")
    p.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    p.add_argument("--identity-max", action="store_true")
    p.add_argument("--download-model", action="store_true")
    args = p.parse_args()
    setup = Path(__file__).with_name("setup_runtime.py")
    profile = "identity-max" if args.identity_max else "neural"
    cmd = [sys.executable, str(setup), "--skill-dir", args.skill_dir, "--profile", profile]
    if args.download_model:
        cmd.append("--download-model")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
