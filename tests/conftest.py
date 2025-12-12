"""Test configuration for importing the hangman module."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root and ``src`` are on sys.path when running pytest as an entrypoint script.
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
for path in (SRC_DIR, ROOT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
