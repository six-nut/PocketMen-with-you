from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from pocketmen.pipeline import create_pet
from pocketmen.spec import ATLAS_HEIGHT, ATLAS_WIDTH


def _make_ref(path: Path, shift: int) -> None:
    im = Image.new("RGB", (420, 560), (238, 240, 244))
    d = ImageDraw.Draw(im)
    d.ellipse((100 + shift, 65, 320 + shift, 300), fill=(35, 40, 48))
    d.rounded_rectangle((125 + shift, 250, 295 + shift, 520), radius=45, fill=(43, 49, 60))
    d.ellipse((160 + shift, 150, 185 + shift, 182), fill=(238, 190, 45))
    d.ellipse((235 + shift, 150, 260 + shift, 182), fill=(238, 190, 45))
    im.save(path)


def test_local_create_without_openai_key(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = tmp_path / "a.png"
    b = tmp_path / "b.png"
    _make_ref(a, 0)
    _make_ref(b, 8)
    out = tmp_path / "out"
    summary = create_pet(
        [a, b],
        name="Demo Friend",
        output_dir=out,
        style="soft-real",
        engine="deterministic",
    )
    assert summary["ok"]
    assert summary["engine"] == "local-deterministic-motion-puppet"
    assert summary["api_key_required"] is False
    assert summary["hatch_pet_required"] is False
    assert summary["openai_imagegen_used"] is False
    atlas = Image.open(summary["spritesheet"])
    assert atlas.size == (ATLAS_WIDTH, ATLAS_HEIGHT)
    assert (out / "package" / "demo-friend" / "pet.json").is_file()
    assert (out / "run" / "qa" / "contact-sheet.png").is_file()
    assert len(list((out / "run" / "qa" / "previews").glob("*.gif"))) == 9


def test_neural_pipeline_path_can_package_with_stub(monkeypatch, tmp_path):
    from PIL import Image, ImageDraw

    from pocketmen import pipeline
    from pocketmen.spec import ROW_SPECS

    a = tmp_path / "a2.png"
    b = tmp_path / "b2.png"
    _make_ref(a, 10)
    _make_ref(b, 14)

    def fake_generate(*args, **kwargs):
        sprites = {}
        for state, _ in ROW_SPECS:
            im = Image.new("RGBA", (100, 130), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.ellipse((18, 8, 82, 122), fill=(25, 25, 25, 255))
            sprites[state] = im
        return sprites, {
            "backend": "fake-neural",
            "model_id": "test/fake",
            "model_license": "test",
            "generation_calls": 10,
            "state_failures": {},
        }

    monkeypatch.setattr(pipeline, "generate_state_sprites", fake_generate)
    summary = pipeline.create_pet(
        [a, b],
        name="Neural Stub",
        output_dir=tmp_path / "out-neural",
        engine="neural",
        backend="auto",
        quality="max",
        subject_type="animal",
    )
    assert summary["ok"] is True
    assert summary["engine"] == "neural-local:fake-neural"
    assert summary["api_key_required"] is False
    assert summary["hatch_pet_required"] is False
    assert summary["openai_imagegen_used"] is False


def test_neural_failure_falls_back_without_openai_key(monkeypatch, tmp_path):
    from pocketmen import pipeline

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    a = tmp_path / "fallback-a.png"
    b = tmp_path / "fallback-b.png"
    _make_ref(a, 2)
    _make_ref(b, 6)

    def fail_neural(*args, **kwargs):
        raise RuntimeError("local neural runtime unavailable")

    monkeypatch.setattr(pipeline, "generate_state_sprites", fail_neural)
    summary = pipeline.create_pet(
        [a, b],
        name="Fallback Friend",
        output_dir=tmp_path / "out-fallback",
        engine="neural",
        neural_fallback=True,
    )

    assert summary["ok"] is True
    assert summary["engine"] == "local-deterministic-motion-puppet"
    assert "local neural runtime unavailable" in summary["neural_fallback_reason"]
    assert summary["api_key_required"] is False
    assert summary["hatch_pet_required"] is False
    assert summary["openai_imagegen_used"] is False
