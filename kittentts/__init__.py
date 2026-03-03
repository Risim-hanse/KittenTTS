from importlib.metadata import PackageNotFoundError, version

from kittentts.get_model import get_model, KittenTTS

try:
    __version__ = version("kittentts")
except PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "KittenML"
__description__ = "Ultra-lightweight text-to-speech model with just 15 million parameters"

__all__ = ["get_model", "KittenTTS"]
