# 🎮 Pygame Hangman

A graphical Hangman game built with **Python + Pygame**, featuring difficulty levels, hints, and scoring. The core logic is importable without Pygame, so tests can run headless while the GUI stays interactive.

## Repository layout
- **User-facing**: `README.md`, `assets/` (drop screenshots/banners here).
- **Runtime code**: `src/hangman/` (game logic and GUI entrypoint).
- **Developer tools**: `scripts/` (packaging helpers), `tests/`, `requirements-dev.txt`, release notes/tasks.

## Quick start
1. Install runtime requirements:
   ```bash
   pip install pygame
   # Optional, larger dictionary
   pip install nltk
   python - <<'PY'
   import nltk
   nltk.download('words')
   PY
   ```
2. Run the game from the repo root:
   ```bash
   PYTHONPATH=src python -m hangman
   ```

## Testing
Install dev tools and run the test suite:
```bash
pip install -r requirements-dev.txt
PYTHONPATH=src pytest
```

## Packaging options
- **Zipapp**: build a single-file archive with
  ```bash
  python scripts/build_pyz.py
  python dist/hangman.pyz
  ```
- **Release archive**: create versioned zip + checksum (requires clean git state) with
  ```bash
  python scripts/publish_release.py v1.1.0
  ```

## Project structure
```text
.
├── assets/                # User-visible art/screenshots
├── src/hangman/           # Game package (importable as `hangman`)
├── scripts/               # Dev utilities (packaging/release)
├── tests/                 # Headless logic/CLI tests
├── requirements-dev.txt   # Optional dev dependencies
├── RELEASE_NOTES.md
└── RELEASE_TASKS.md
```

Happy hacking 🎉
