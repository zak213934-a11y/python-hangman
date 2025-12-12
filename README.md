# Pygame Hangman

A graphical Hangman experience built with `pygame`, featuring difficulty levels, a hint system, and scoring. It also supports the NLTK words corpus for a large dictionary but gracefully falls back to a bundled list.

## Quick start
- Install dependencies (pygame is required for the GUI):
  ```bash
  pip install pygame
  # Optional: nltk for a larger word list
  pip install nltk
  python - <<'PY'
  import nltk
  nltk.download('words')
  PY
  ```
- Run the game: `python hangman.py`

## Features
- Three difficulty levels that adjust word length, attempts, and hint costs.
- Hint button reveals random letters (up to three hints per game) and affects score.
- Dynamic scoring that rewards remaining attempts and difficulty multipliers.
- Fallback word list when NLTK is unavailable.
- GUI ready for future sound effects and polish.

## Testing
The core game logic is independent of `pygame` so tests can run headless:
```bash
python -m pytest
```

## Distribution
Build a single-file zipapp when PyInstaller isn’t available:
```bash
python build_pyz.py
```
The archive is written to `dist/hangman.pyz`; run it with `python dist/hangman.pyz`.

## Release packaging
Create a versioned source archive:
```bash
python publish_release.py v1.1.0
```
The script emits `releases/hangman-v1.1.0.zip` (with a matching `.sha256`), refuses to run with uncommitted changes unless `--allow-dirty` is provided, and supports publishing specific refs via `--ref <git-ref>`. Use `--output-dir` to choose the destination.

## Dev setup
Install optional tooling (linters, publish helpers) with:
```bash
pip install -r requirements-dev.txt
```

## Release notes
For gameplay changes and validation details, see `RELEASE_NOTES.md`.
