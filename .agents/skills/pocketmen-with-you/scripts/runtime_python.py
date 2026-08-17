from __future__ import annotations

import os
import sys
from pathlib import Path

skill = Path(__file__).resolve().parents[1]
if os.name == "nt":
    py = skill / ".venv" / "Scripts" / "python.exe"
else:
    py = skill / ".venv" / "bin" / "python"
print(py if py.exists() else Path(sys.executable))
