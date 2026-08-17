from pathlib import Path

from PIL import Image, ImageDraw

from pocketmen.atlas import validate_atlas
from pocketmen.spec import ATLAS_HEIGHT, ATLAS_WIDTH, CELL_HEIGHT, CELL_WIDTH, ROW_SPECS


def test_synthetic_atlas_passes(tmp_path: Path):
    atlas = Image.new("RGBA", (ATLAS_WIDTH, ATLAS_HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(atlas)
    for row, (_, count) in enumerate(ROW_SPECS):
        for col in range(count):
            x = col * CELL_WIDTH + 40
            y = row * CELL_HEIGHT + 40
            d.ellipse((x, y, x + 80, y + 100), fill=(40 + row * 10, 80, 140, 255))
    path = tmp_path / "atlas.png"
    atlas.save(path)
    result = validate_atlas(path)
    assert result["ok"], result


def test_unused_cell_must_be_transparent(tmp_path: Path):
    atlas = Image.new("RGBA", (ATLAS_WIDTH, ATLAS_HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(atlas)
    for row, (_, count) in enumerate(ROW_SPECS):
        for col in range(count):
            x = col * CELL_WIDTH + 40
            y = row * CELL_HEIGHT + 40
            d.rectangle((x, y, x + 50, y + 50), fill=(100, 120, 140, 255))
    # idle only uses 6 columns; poison column 8.
    d.rectangle((7 * CELL_WIDTH + 20, 20, 7 * CELL_WIDTH + 60, 60), fill=(255, 0, 0, 255))
    path = tmp_path / "bad.png"
    atlas.save(path)
    result = validate_atlas(path)
    assert not result["ok"]
    assert any("unused cell idle" in e for e in result["errors"])
