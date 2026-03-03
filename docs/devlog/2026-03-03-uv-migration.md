# Dev log: uv-first migration, packaging cleanup, and Python support

Date: 2026-03-03

## Why this file exists

This PR touched packaging, dependency management, and phonemization. This document records the rationale and the *practical* consequences so future changes (or cherry-picks) don’t require re-deriving context.

## Goals

- Make the repo uv-first (reproducible installs via `uv.lock`).
- Keep `pyproject.toml` as the single source of truth for deps + build config.
- Support a practical Python range for ML users (avoid bleeding edge).
- Keep phonemization stable and avoid heavyweight accidental deps.

## Key decisions

### Packaging: remove setuptools surface area

- Build backend is **hatchling**.
- `setup.py` and `MANIFEST.in` removed.
- Wheel + sdist inclusion is managed via hatch config in `pyproject.toml`.

Build verification command:

```bash
uv build --no-sources
```

### Lockfile strategy

- `uv.lock` is the canonical lockfile.
- Poetry is supported (reads PEP 621 metadata) but **`poetry.lock` is not tracked** to avoid dual-lock drift.

### Python support range

- Supported: **Python 3.10–3.12** (`requires-python = ">=3.10,<3.13"`).
- Rationale: wide enough for most users, but avoids early 3.13 ecosystem churn.

### onnxruntime: per-Python pinning (cp310 wheel gap)

Problem observed in matrix tests:
- `onnxruntime==1.24.x` has wheels for cp311/cp312 but **not** cp310.

Resolution:
- Environment markers in `pyproject.toml`:
  - `onnxruntime>=1.23.2,<1.24.0; python_version < '3.11'`
  - `onnxruntime>=1.24.0; python_version >= '3.11'`

### Phonemization and the `misaki[en]` dependency trap

We considered using `misaki.espeak.EspeakG2P` directly.

Findings:
- `misaki[en]` pulls `spacy-curated-transformers` → `torch` → often large CUDA wheels.
- G2P output strings differed from the existing `phonemizer` output; quality regressions were plausible even if audio sounded “fine”.

Final choice:
- Keep `phonemizer` as the runtime phonemizer.
- Avoid system espeak dependency by wiring phonemizer’s espeak wrapper to `espeakng_loader`:

```python
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import espeakng_loader

EspeakWrapper.set_library(espeakng_loader.get_library_path())
EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
```

## Tests added (baseline coverage)

- `tests/test_imports.py`: public import surface.
- `tests/test_metadata.py`: runtime Python in supported range.
- `tests/test_phonemizer.py`: phonemizer works with `espeakng_loader` (no system espeak).

## Compatibility verification performed

### uv

For each Python version 3.10 / 3.11 / 3.12:

- `uv sync -p <ver> --frozen`
- `uv run -p <ver> --frozen --no-sync pytest`

### Poetry

Using Poetry 2.3.x, for each Python version 3.10 / 3.11 / 3.12:

- `poetry check`
- `poetry env use <python>`
- `poetry install --only main --no-root`
- `poetry run python -c "import kittentts"`

## Commit history (PR base)

These commits were already present in the branch history while developing this PR:

- `45a464d36b6b55c13fa43614e3b4051b6a2310ff`
  - Switch packaging to hatchling; remove `setup.py` + `MANIFEST.in`.

- `664a9eb0a08075a740b52db97171f2d41728625b`
  - Wire `EspeakWrapper` to `espeakng_loader`.

Note: later changes in this PR (Python range, onnxruntime markers, tests, README updates, lock updates) are applied as a single change-set for the automation to commit.
