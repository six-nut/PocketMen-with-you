#!/usr/bin/env bash
set -euo pipefail
SKILL="${HOME}/.agents/skills/pocketmen-with-you"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$SKILL/SKILL.md" ]]; then
  SKILL="$ROOT/.agents/skills/pocketmen-with-you"
fi
python3 "$SKILL/scripts/setup_runtime.py" --skill-dir "$SKILL" --profile neural --download-model
