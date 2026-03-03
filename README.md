# Kitten TTS 😻

<img width="607" height="255" alt="Screenshot 2026-02-18 at 8 33 04 PM" src="https://github.com/user-attachments/assets/f4646722-ba78-4b25-8a65-81bacee0d4f6" />



> **🎉 ANNOUNCEMENT:** New version of KittenTTS  is now available to download!

###  [Wanna hear samples? Try the model for free on Hugging Face Spaces by clicking this link](https://huggingface.co/spaces/KittenML/KittenTTS-Demo)



Kitten TTS is an open-source realistic text-to-speech model with just 15 million parameters, designed for lightweight deployment and high-quality voice synthesis.

*Currently in developer preview*

[Join our discord](https://discord.com/invite/VJ86W4SURW) 

[Our website](https://kittenml.com) 

[For custom support - fill this form ](https://docs.google.com/forms/d/e/1FAIpQLSc49erSr7jmh3H2yeqH4oZyRRuXm0ROuQdOgWguTzx6SMdUnQ/viewform?usp=preview)

Email the creators with any questions : info@stellonlabs.com


## Features

- **Ultra-lightweight**: Model size less than 25MB
- **CPU-optimized**: Runs without GPU on any device
- **High-quality voices**: Several premium voice options available
- **Fast inference**: Optimized for real-time speech synthesis


## Models

| Model | Params | Size | Link |
|-------|--------|------|------|
| kitten-tts-mini | 80M | 80MB | 🤗 [KittenML/kitten-tts-mini-0.8](https://huggingface.co/KittenML/kitten-tts-mini-0.8) |
| kitten-tts-micro | 40M | 41MB | 🤗 [KittenML/kitten-tts-micro-0.8](https://huggingface.co/KittenML/kitten-tts-micro-0.8) |
| kitten-tts-nano | 15M | 56MB | 🤗 [KittenML/kitten-tts-nano-0.8](https://huggingface.co/KittenML/kitten-tts-nano-0.8-fp32) |
| kitten-tts-nano-0.8-int8 | 15M | 25MB | 🤗 [KittenML/kitten-tts-nano-0.8-int8](https://huggingface.co/KittenML/kitten-tts-nano-0.8-int8) |

> Some users are facing minor issues with the kitten-tts-nano-int8  model. We are looking into it. Please report to us if you face any issues. 

## Demo Video


https://github.com/user-attachments/assets/d80120f2-c751-407e-a166-068dd1dd9e8d



## Quick Start

### Installation

```
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
```

### Development setup (uv)

This project is uv-first. To create a local environment and install dependencies:

```
uv sync
```

Run the example in the project environment:

```
uv run python example.py
```

If you update dependencies in `pyproject.toml`, re-lock and re-sync:

```
uv lock
uv sync
```

### Alternative setup (Poetry 2.x)

Poetry 2.x can use the PEP 621 `[project]` metadata in `pyproject.toml`:

```
poetry check
poetry install --only main
```

(For reproducibility, `uv.lock` is the primary lockfile. Poetry users can generate a `poetry.lock` locally if desired.)

### Alternative setup (Conda + uv pip)

If you prefer Conda, use Conda for Python/system libs and let uv install Python packages directly into the active Conda env.

```
# create env (mamba recommended; conda also works)
mamba env create -f environment.yml   # or: conda env create -f environment.yml
conda activate kittentts-312

# remove any existing .venv so uv uses the Conda env
rm -rf .venv

# install Python deps into the active Conda env
uv pip install --python $(which python) -r requirements.txt -e .

# run
python example.py
```

For development (with test tools):
```
uv pip install --python $(which python) -r requirements.txt -e . pytest ruff
pytest -q
```

Notes:
- On Linux, `libsndfile` (provided by the env) is required for `soundfile`. On macOS/Windows, wheels bundle it.
- The `--python $(which python)` flag ensures uv installs into the active Conda environment, not a new `.venv`.

 ### Basic Usage 

```
from kittentts import KittenTTS
m = KittenTTS("KittenML/kitten-tts-mini-0.8")

audio = m.generate("This high quality TTS model works without a GPU.", voice='Jasper' )

# available_voices : ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']

# Save the audio
import soundfile as sf
sf.write('output.wav', audio, 24000)

```





## System Requirements

Python 3.10–3.12 supported (3.12 recommended). We recommend using conda. 



## Checklist 

- [x] Release a preview model
- [ ] Release the fully trained model weights
- [ ] Release mobile SDK 
- [ ] Release web version 

