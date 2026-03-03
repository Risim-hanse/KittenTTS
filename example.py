#!/usr/bin/env python3

from __future__ import annotations

from typing import Literal
import soundfile as sf
from kittentts import KittenTTS

Voice = Literal["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]
Model = Literal["mini", "micro", "nano"]

MODELS: dict[Model, str] = {
    "mini": "KittenML/kitten-tts-mini-0.8",    # 80M — best quality
    "micro": "KittenML/kitten-tts-micro-0.8",  # 40M — balanced
    "nano": "KittenML/kitten-tts-nano-0.8",    # 15M — fastest
}

# Configure here
model: Model = "micro"
voice: Voice = "Rosie"
text: str = "Kittens run and jump. They meow and purr. Happy little cats play."
output: str = "output.wav"

# Generate and save
tts = KittenTTS(MODELS[model])
audio = tts.generate(text=text, voice=voice)
sf.write(output, audio, 24000)

print(f"✓ Saved {output}")
