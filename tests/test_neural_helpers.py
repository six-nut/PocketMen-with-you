import numpy as np
from PIL import Image, ImageDraw

from pocketmen.backends import make_backend
from pocketmen.motion import build_frames_from_sprites
from pocketmen.neural import remove_chroma
from pocketmen.prompts import canonical_prompt, state_prompt
from pocketmen.spec import ROW_SPECS


def test_prompt_compiler_keeps_identity_and_action():
    p = canonical_prompt(
        style="hero-chibi",
        subject_type="person",
        identity_notes="black hair, silver earrings",
        chroma_hex="#00FF46",
    )
    assert "silver earrings" in p
    assert "#00FF46" in p
    s = state_prompt(
        "waving",
        style="hero-chibi",
        subject_type="person",
        identity_notes="black hair, silver earrings",
        chroma_hex="#00FF46",
    )
    assert "waving" in s.lower()
    assert "silver earrings" in s


def test_remove_chroma_keeps_foreground():
    bg = (0, 255, 70)
    im = Image.new("RGB", (128, 128), bg)
    d = ImageDraw.Draw(im)
    d.ellipse((30, 20, 98, 112), fill=(25, 25, 25))
    out = remove_chroma(im, bg)
    assert out.mode == "RGBA"
    assert out.getchannel("A").getbbox() is not None
    arr = np.asarray(out.getchannel("A"))
    assert int(arr.max()) == 255


def test_state_specific_sprites_build_full_contract():
    sprites = {}
    for state, _ in ROW_SPECS:
        im = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((16, 8, 80, 120), fill=(30, 30, 30, 255))
        sprites[state] = im
    frames = build_frames_from_sprites(sprites)
    assert list(frames) == [s for s, _ in ROW_SPECS]
    assert [len(frames[s]) for s, _ in ROW_SPECS] == [n for _, n in ROW_SPECS]


def test_neural_backend_defaults_and_licenses():
    default = make_backend("auto")
    identity_max = make_backend("qwen-image-edit-2511")

    assert default.info.name == "flux2-klein-4b"
    assert default.info.model_id == "black-forest-labs/FLUX.2-klein-4B"
    assert default.info.license == "Apache-2.0"
    assert identity_max.info.name == "qwen-image-edit-2511"
    assert identity_max.info.model_id == "Qwen/Qwen-Image-Edit-2511"
    assert identity_max.info.license == "Apache-2.0"
