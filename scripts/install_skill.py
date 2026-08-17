from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(Path(__file__).resolve().parents[1] / ".agents" / "skills" / "pocketmen-with-you"))
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
    print("If Codex does not show the new skill immediately, restart Codex.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
