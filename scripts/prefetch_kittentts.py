"""
Prefetch KittenTTS model assets into the HF Hub cache for CI testing.

Mirrors the exact files downloaded by KittenTTS at runtime (config.json,
model file, voices file) without importing any KittenTTS internals.

Cache location is controlled by the HF_HUB_CACHE environment variable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from collections import deque
from huggingface_hub import hf_hub_download

REPO_ID = os.environ.get("KITTEN_TTS_MODEL", "KittenML/kitten-tts-micro-0.8")
SUPPORTED_TYPES = {"ONNX1", "ONNX2"}


def prefetch(repo_id: str) -> None:
    print(f"→ Prefetching {repo_id}")

    config_path = hf_hub_download(repo_id=repo_id, filename="config.json")
    config = json.loads(Path(config_path).read_text())

    model_type = config.get("type")
    if model_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported model type: {model_type!r} (expected one of {SUPPORTED_TYPES})")

    # Use deque(..., maxlen=0) to consume the generator and trigger side effects
    deque(
        (
            print(f"  ↓ {config[key]}") or hf_hub_download(repo_id=repo_id, filename=config[key])
            for key in ("model_file", "voices")
        ),
        maxlen=0
    )

    print("✓ Done")


if __name__ == "__main__":
    prefetch(REPO_ID)