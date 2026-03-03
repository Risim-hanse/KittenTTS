from __future__ import annotations

import numpy as np
import onnxruntime as ort
import soundfile as sf
import re
import phonemizer
import espeakng_loader
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from .preprocess import TextPreprocessor, normalize_symbol_spacing


def ensure_punctuation(text):
    """Ensure text ends with punctuation. If not, add a comma."""
    text = text.strip()
    if not text:
        return text
    if text[-1] not in '.!?,;:':
        text = text + ','
    return text


def chunk_text(text, max_len=400):
    """Split text into chunks for processing long texts."""
    
    sentences = re.split(r'[.!?]+', text)
    chunks = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        if len(sentence) <= max_len:
            chunks.append(ensure_punctuation(sentence))
        else:
            # Split long sentences by words
            words = sentence.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 <= max_len:
                    temp_chunk += " " + word if temp_chunk else word
                else:
                    if temp_chunk:
                        chunks.append(ensure_punctuation(temp_chunk.strip()))
                    temp_chunk = word
            if temp_chunk:
                chunks.append(ensure_punctuation(temp_chunk.strip()))
    
    return chunks


class CharTokenizer:
    PAD = "$"
    PUNCTUATION = ';:,.!?¡¿—…"«»"" '  # includes space
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    LETTERS_IPA = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"
    
    def __init__(self, *, skip_unknown: bool = True):
        self.symbols = list(self.PAD + self.PUNCTUATION + self.LETTERS + self.LETTERS_IPA)
        self.char2id = {ch: i for i, ch in enumerate(self.symbols)}
        self.skip_unknown = skip_unknown

    def __call__(self, text: str) -> list[int]:
        if self.skip_unknown:
            return [i for i in map(self.char2id.get, text) if i is not None]
        # will raise if any char is missing
        return [self.char2id[ch] for ch in text]


class KittenTTS_1_Onnx:
    def __init__(self, model_path="kitten_tts_nano_preview.onnx", voices_path="voices.npz", speed_priors={}, voice_aliases={}):
        """Initialize KittenTTS with model and voice data.
        
        Args:
            model_path: Path to the ONNX model file
            voices_path: Path to the voices NPZ file
        """
        self.model_path = model_path
        self.voices = np.load(voices_path) 
        self.session = ort.InferenceSession(model_path)

        EspeakWrapper.set_library(espeakng_loader.get_library_path())
        EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        self.phonemizer = phonemizer.backend.EspeakBackend(
            language="en-us", preserve_punctuation=True, with_stress=True
        )
        self.tokenizer = CharTokenizer()
        self.speed_priors = speed_priors
        
        # Available voices
        self.available_voices = [
            'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f', 
            'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'
        ]
        self.all_voice_names = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']
        self.voice_aliases = voice_aliases

        self.preprocessor = TextPreprocessor(remove_punctuation=False)
    
    def _prepare_inputs(self, text: str, voice: str, speed: float = 1.0) -> dict:
        """Prepare ONNX model inputs from text and voice parameters."""
        if voice in self.voice_aliases:
            voice = self.voice_aliases[voice]

        if voice not in self.available_voices:
            raise ValueError(f"Voice '{voice}' not available. Choose from: {self.available_voices}")
        
        if voice in self.speed_priors:
            speed = speed * self.speed_priors[voice]
        
        # Preprocess text and convert to phonemes
        phonemes_list = self.phonemizer.phonemize([text])
        phonemes_str = normalize_symbol_spacing(phonemes_list[0])
        # Convert phonemes to token IDs
        token_ids = self.tokenizer(phonemes_str)
        token_ids = [0, *token_ids, 10, 0]  # add start and end tokens

        input_ids = np.array([token_ids], dtype=np.int64)
        ref_id = min(len(text), self.voices[voice].shape[0] - 1)
        ref_s = self.voices[voice][ref_id:ref_id+1]
        
        return {
            "input_ids": input_ids,
            "style": ref_s,
            "speed": np.array([speed], dtype=np.float32),
        }
    
    def generate(self, text: str, voice: str = "expr-voice-5-m", speed: float = 1.0, clean_text: bool=True) -> np.ndarray:
        out_chunks = []
        if clean_text:
            text = self.preprocessor(text)
        for text_chunk in chunk_text(text):
            out_chunks.append(self.generate_single_chunk(text_chunk, voice, speed))
        return np.concatenate(out_chunks, axis=-1)

    def generate_single_chunk(self, text: str, voice: str = "expr-voice-5-m", speed: float = 1.0) -> np.ndarray:
        """Synthesize speech from text.
        
        Args:
            text: Input text to synthesize
            voice: Voice to use for synthesis
            speed: Speech speed (1.0 = normal)
            
        Returns:
            Audio data as numpy array
        """
        onnx_inputs = self._prepare_inputs(text, voice, speed)
        
        outputs = self.session.run(None, onnx_inputs)
        
        # Trim audio
        audio = outputs[0][..., :-5000]

        return audio
    
    def generate_to_file(self, text: str, output_path: str, voice: str = "expr-voice-5-m", 
                          speed: float = 1.0, sample_rate: int = 24000, clean_text: bool=True) -> None:
        """Synthesize speech and save to file.
        
        Args:
            text: Input text to synthesize
            output_path: Path to save the audio file
            voice: Voice to use for synthesis
            speed: Speech speed (1.0 = normal)
            sample_rate: Audio sample rate
            clean_text: If true, it will cleanup the text. Eg. replace numbers with words.
        """
        audio = self.generate(text, voice, speed, clean_text=clean_text)
        sf.write(output_path, audio, sample_rate)
        print(f"Audio saved to {output_path}")

