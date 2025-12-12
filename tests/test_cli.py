"""CLI-level smoke tests for the pygame Hangman entry point."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif("pygame" in sys.modules, reason="pygame installed; manual GUI testing preferred")
def test_module_requires_pygame_when_missing() -> None:
    """Running the module without pygame should exit with an informative error."""

    project_root = Path(__file__).resolve().parent.parent
    env = {**os.environ, "PYTHONPATH": str(project_root / "src")}

    result = subprocess.run(
        [sys.executable, "-m", "hangman"],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode != 0
    assert "pygame is required to run the GUI" in result.stderr
