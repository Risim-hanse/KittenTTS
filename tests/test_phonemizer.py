import espeakng_loader
import phonemizer
from phonemizer.backend.espeak.wrapper import EspeakWrapper


def test_phonemizer_uses_espeakng_loader():
    EspeakWrapper.set_library(espeakng_loader.get_library_path())
    EspeakWrapper.set_data_path(espeakng_loader.get_data_path())

    backend = phonemizer.backend.EspeakBackend(
        language="en-us", preserve_punctuation=True, with_stress=True
    )
    phonemes = backend.phonemize(["Hello world!"])[0]

    assert isinstance(phonemes, str)
    assert phonemes.strip()
