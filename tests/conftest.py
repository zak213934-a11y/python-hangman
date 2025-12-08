"""Test configuration for importing the hangman module."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on sys.path when running pytest as an entrypoint script.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
