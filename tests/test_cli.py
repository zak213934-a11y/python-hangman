"""CLI-level smoke tests for the pygame Hangman entry point."""

from __future__ import annotations

import subprocess
import sys

import pytest


@pytest.mark.skipif("pygame" in sys.modules, reason="pygame installed; manual GUI testing preferred")
def test_module_requires_pygame_when_missing() -> None:
    """Running the module without pygame should exit with an informative error."""

    result = subprocess.run(
        [sys.executable, "-m", "hangman"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "pygame is required to run the GUI" in result.stderr
