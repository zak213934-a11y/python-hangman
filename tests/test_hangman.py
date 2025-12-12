"""Unit tests for the Hangman game logic and helpers."""

from __future__ import annotations

import pytest

from hangman import DIFFICULTY_SETTINGS, HangmanGame, WordManager


def test_hangman_game_flow_tracks_state() -> None:
    """A sequence of guesses should advance win/loss state appropriately."""

    game = HangmanGame("code", difficulty="MEDIUM")
    assert game.remaining_attempts == DIFFICULTY_SETTINGS["MEDIUM"]["max_attempts"]

    assert game.guess("c") is True
    assert game.guess("x") is False
    assert "x" in game.wrong_guesses
    assert game.remaining_attempts == DIFFICULTY_SETTINGS["MEDIUM"]["max_attempts"] - 1

    assert game.guess("o") is True
    assert game.guess("d") is True
    assert game.guess("e") is True
    assert game.is_won()
    assert not game.is_lost()
    assert game.game_over()


def test_guess_rejects_invalid_letters() -> None:
    """Invalid inputs should not change guessed letters or attempts."""

    game = HangmanGame("python")

    for invalid in ("", "ab", "1", "!", "abc"):
        assert game.guess(invalid) is False

    assert not game.guessed_letters
    assert not game.wrong_guesses
    assert game.remaining_attempts == DIFFICULTY_SETTINGS["MEDIUM"]["max_attempts"]


def test_hints_reveal_letters_and_affect_score() -> None:
    """Using hints should reveal letters, increment hint counters, and reduce score."""

    game = HangmanGame("banana", difficulty="EASY")
    initial_score = game.score

    assert game.get_hint() is True
    assert game.hints_used == 1
    assert len(game.revealed_hints) == 1
    assert game.score < initial_score


def test_word_manager_respects_difficulty_lengths(monkeypatch: pytest.MonkeyPatch) -> None:
    """Words should be filtered into difficulty buckets by length."""

    mock_words = ["hat", "python", "encyclopedia", "keyboard", "loop"]

    class FakeCorpus:  # pylint: disable=too-few-public-methods
        """Minimal stand-in for the NLTK words corpus."""

        @staticmethod
        def words() -> list[str]:
            """Return a curated list of mock words."""

            return mock_words

    class FakeNltk:  # pylint: disable=too-few-public-methods
        """Minimal stand-in for the nltk package."""

        corpus = FakeCorpus()

        @staticmethod
        def download(_name: str, _quiet: bool = True) -> None:  # pragma: no cover - noop helper
            """Pretend to download the corpus without touching the network."""

            return None

    monkeypatch.setattr("hangman.NLTK_AVAILABLE", True)
    monkeypatch.setattr("hangman.nltk", FakeNltk)
    monkeypatch.setattr("hangman.nltk_words", FakeCorpus())

    manager = WordManager()

    for word in manager.word_cache["EASY"]:
        assert DIFFICULTY_SETTINGS["EASY"]["min_length"] <= len(word) <= DIFFICULTY_SETTINGS["EASY"]["max_length"]

    for word in manager.word_cache["HARD"]:
        assert DIFFICULTY_SETTINGS["HARD"]["min_length"] <= len(word) <= DIFFICULTY_SETTINGS["HARD"]["max_length"]


def test_score_awards_bonus_for_attempts_left() -> None:
    """Scores should scale with remaining attempts and difficulty."""

    game = HangmanGame("quiz", difficulty="HARD")
    game.guess("q")
    game.guess("u")
    game.guess("i")
    game.guess("z")

    expected_base = len("quiz") * 10
    attempts_bonus = game.remaining_attempts * 5
    hint_penalty = 0
    difficulty_multiplier = 2
    assert game.score == int((expected_base + attempts_bonus - hint_penalty) * difficulty_multiplier)
