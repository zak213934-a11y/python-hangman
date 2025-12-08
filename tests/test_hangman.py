"""Unit tests for the Hangman game logic."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from hangman import HangmanGame, choose_word, load_words_from_file


def test_hangman_game_win_flow() -> None:
    game = HangmanGame("code", allowed_attempts=6)
    for letter in "code":
        assert game.guess(letter) is True
    assert game.is_won()
    assert not game.is_lost()
    assert game.remaining_attempts == 6


def test_hangman_game_duplicate_guess_raises() -> None:
    game = HangmanGame("python", allowed_attempts=6)
    game.guess("p")
    with pytest.raises(ValueError):
        game.guess("p")
    game.guess("y")
    with pytest.raises(ValueError):
        game.guess("y")


def test_guess_requires_single_alpha_character() -> None:
    game = HangmanGame("test")
    for invalid in ("", "ab", "1", "!", "abc"):
        with pytest.raises(ValueError):
            game.guess(invalid)


def test_choose_word_uses_rng() -> None:
    rng = random.Random(123)
    word = choose_word(["alpha", "beta", "gamma"], rng)
    assert word == "alpha"


def test_load_words_from_file_filters_non_alpha(tmp_path: Path) -> None:
    content = "Alpha\nBeta\n123\n \nGamma!\n"
    word_file = tmp_path / "words.txt"
    word_file.write_text(content, encoding="utf-8")

    loaded = load_words_from_file(word_file)
    assert loaded == ["Alpha", "Beta"]


def test_load_words_from_file_requires_words(tmp_path: Path) -> None:
    word_file = tmp_path / "empty.txt"
    word_file.write_text("123\n!@#\n", encoding="utf-8")

    with pytest.raises(ValueError):
        load_words_from_file(word_file)
