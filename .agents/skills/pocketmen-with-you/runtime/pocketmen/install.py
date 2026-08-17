from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .atlas import validate_atlas

PET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))


def install_pet(package_dir: str | Path) -> Path:
    package = Path(package_dir).expanduser().resolve()
    manifest_path = package / "pet.json"
    sprite_path = package / "spritesheet.webp"
    if not manifest_path.is_file() or not sprite_path.is_file():
        raise ValueError("pet package must contain pet.json and spritesheet.webp")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pet_id = manifest.get("id") or manifest.get("petId")
    if not isinstance(pet_id, str) or not PET_ID_RE.fullmatch(pet_id):
        raise ValueError("pet id must match [a-z0-9][a-z0-9._-]{0,63}")
    result = validate_atlas(sprite_path)
    if not result["ok"]:
        raise ValueError("spritesheet failed validation: " + "; ".join(result["errors"]))

    dest = codex_home() / "pets" / pet_id
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup = dest.with_name(dest.name + f".backup-{stamp}")
        shutil.copytree(dest, backup)
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_path, dest / "pet.json")
    shutil.copy2(sprite_path, dest / "spritesheet.webp")
    return dest
