# Python Hangman

A lightweight command-line Hangman game with configurable word sources and attempt limits.

## Quick start
- Run the game: `python hangman.py`
- Guess one letter at a time; win by revealing the word before attempts run out.

## Options
- `--word-file PATH`: use a newline-delimited list of candidate words.
- `--attempts N`: set the number of allowed wrong guesses (default matches the included ASCII art).

## Distribution
Build a single-file zipapp when PyInstaller isn’t available:
```bash
python build_pyz.py
```
The archive is written to `dist/hangman.pyz`; run it with `python dist/hangman.pyz [options]`. The `dist/` directory is gitignored, so generate it locally as needed.

## Testing
Run unit tests with:
```bash
python -m pytest
```

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
For gameplay/CLI changes and validation details (including tested Python versions), see `RELEASE_NOTES.md`.
