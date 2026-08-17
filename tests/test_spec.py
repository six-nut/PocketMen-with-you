from pocketmen.spec import ATLAS_HEIGHT, ATLAS_WIDTH, CELL_HEIGHT, CELL_WIDTH, ROW_SPECS


def test_geometry():
    assert (ATLAS_WIDTH, ATLAS_HEIGHT) == (1536, 1872)
    assert (CELL_WIDTH, CELL_HEIGHT) == (192, 208)
    assert [name for name, _ in ROW_SPECS] == [
        "idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running", "review"
    ]
    assert [n for _, n in ROW_SPECS] == [6, 8, 8, 4, 5, 8, 6, 6, 6]
