import json
from pathlib import Path

from pocketmen import __version__

ROOT = Path(__file__).resolve().parents[1]


def test_v030_release_configuration():
    config = json.loads((ROOT / "repo-config.json").read_text(encoding="utf-8"))
    required_topics = {"codex-skill", "local-ai", "flux2", "qwen-image", "image-editing"}

    assert __version__ == "0.3.0"
    assert config["owner"] == "six-nut"
    assert config["repo"] == "PocketMen-with-you"
    assert config["visibility"] == "public"
    assert config["release"] == "v0.3.0"
    assert len(config["topics"]) <= 20
    assert required_topics <= set(config["topics"])


def test_normal_runtime_has_no_api_key_or_hatch_pet_dependency():
    runtime_text = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "src" / "pocketmen").rglob("*.py")
    )

    assert "OPENAI_API_KEY" not in runtime_text
    assert "hatch-pet" not in runtime_text
