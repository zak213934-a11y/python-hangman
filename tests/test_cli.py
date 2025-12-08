"""CLI-level tests for the Hangman game entrypoint."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_quick_loss() -> None:
    """Run the game via ``python -m hangman`` and lose quickly with one attempt."""

    result = subprocess.run(
        [sys.executable, "-m", "hangman", "--attempts", "1"],
        input="z\n",
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Welcome to Hangman!" in result.stdout
    assert "Game over! The word was" in result.stdout


def test_cli_rejects_invalid_attempts() -> None:
    """Invalid attempts value should terminate with an error and message."""

    result = subprocess.run(
        [sys.executable, "-m", "hangman", "--attempts", "0"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "Allowed attempts must be positive." in result.stderr


def test_cli_missing_word_file(tmp_path: Path) -> None:
    """Missing word list file should produce an error and non-zero exit code."""

    missing_path = tmp_path / "missing.txt"
    result = subprocess.run(
        [sys.executable, "-m", "hangman", "--word-file", str(missing_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert str(missing_path) in result.stderr
