#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/install_skill.py" --source "$ROOT/.agents/skills/pocketmen-with-you"
