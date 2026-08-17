from importlib import import_module
from pathlib import Path

from pocketmen.spec import ATLAS_HEIGHT, ATLAS_WIDTH, CELL_HEIGHT, CELL_WIDTH, ROW_SPECS

SKILL_ROOT = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "pocketmen-with-you"


def test_bundled_skill_atlas_helpers_match_runtime(monkeypatch):
    monkeypatch.syspath_prepend(str(SKILL_ROOT))
    helper = import_module("scripts.atlas_helpers")

    assert (helper.ATLAS_WIDTH, helper.ATLAS_HEIGHT) == (ATLAS_WIDTH, ATLAS_HEIGHT)
    assert (helper.CELL_WIDTH, helper.CELL_HEIGHT) == (CELL_WIDTH, CELL_HEIGHT)
    assert helper.ROW_SPECS == ROW_SPECS


def test_bundled_skill_reference_docs_are_present():
    expected = {"motion-contract.md", "privacy-ip.md", "style-presets.md"}
    actual = {path.name for path in (SKILL_ROOT / "references").glob("*.md")}

    assert expected <= actual
