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


def test_skill_runtime_mirror_matches_package():
    project_root = Path(__file__).resolve().parents[1]
    package_root = project_root / "src" / "pocketmen"
    runtime_root = SKILL_ROOT / "runtime" / "pocketmen"
    package_files = {path.relative_to(package_root) for path in package_root.rglob("*.py")}
    runtime_files = {path.relative_to(runtime_root) for path in runtime_root.rglob("*.py")}

    assert runtime_files == package_files
    for relative in package_files:
        assert (runtime_root / relative).read_bytes() == (package_root / relative).read_bytes()
