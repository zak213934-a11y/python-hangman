"""Simple command-line Hangman game with configurable options.

Run with ``python hangman.py`` and follow the prompts.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Iterable, Sequence

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    r"""
"""Simple command-line Hangman game.

Run with `python hangman.py` and follow the prompts.
"""

import random
from typing import Iterable, Set


HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
    """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
]

DEFAULT_WORDS = [
WORDS = [
    "python",
    "hangman",
    "algorithm",
    "developer",
    "function",
    "variable",
    "testing",
    "container",
    "terminal",
    "program",
]


class HangmanGame:
    """Encapsulates game state and logic for Hangman."""

    def __init__(self, secret_word: str, allowed_attempts: int | None = None) -> None:
        if not secret_word.isalpha():
            raise ValueError("Secret word must contain only alphabetic characters.")

        self.secret_word = secret_word.lower()
        self.allowed_attempts = (
            allowed_attempts if allowed_attempts is not None else len(HANGMAN_STAGES) - 1
        )
        if self.allowed_attempts <= 0:
            raise ValueError("Allowed attempts must be positive.")

        self.guessed_letters: set[str] = set()
        self.wrong_guesses: set[str] = set()

    @property
    def remaining_attempts(self) -> int:
        """Return how many attempts remain."""

        return self.allowed_attempts - len(self.wrong_guesses)

    def masked_word(self) -> str:
        """Return the secret word with unguessed letters masked."""

        return " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.secret_word
        )

    def guess(self, letter: str) -> bool:
        """Process a guess and return ``True`` when correct.

        Raises:
            ValueError: If the guess is invalid or already made.
        """

        self.secret_word = secret_word.lower()
        self.allowed_attempts = allowed_attempts if allowed_attempts is not None else len(HANGMAN_STAGES) - 1
        self.guessed_letters: Set[str] = set()
        self.wrong_guesses: Set[str] = set()

    @property
    def remaining_attempts(self) -> int:
        return self.allowed_attempts - len(self.wrong_guesses)

    def masked_word(self) -> str:
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.secret_word)

    def guess(self, letter: str) -> bool:
        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            raise ValueError("Guess must be a single alphabetic character.")

        if letter in self.guessed_letters or letter in self.wrong_guesses:
            raise ValueError(f"You already guessed '{letter}'.")

        if letter in self.secret_word:
            self.guessed_letters.add(letter)
            return True

        self.wrong_guesses.add(letter)
        return False

    def is_won(self) -> bool:
        """Return whether the player has won."""

        return all(letter in self.guessed_letters for letter in set(self.secret_word))

    def is_lost(self) -> bool:
        """Return whether the player has lost."""

        return self.remaining_attempts <= 0

    def game_over(self) -> bool:
        """Return whether the game has concluded."""

        return self.is_won() or self.is_lost()

    def stage_art(self) -> str:
        """Return the ASCII art for the current state."""

        return all(letter in self.guessed_letters for letter in set(self.secret_word))

    def is_lost(self) -> bool:
        return self.remaining_attempts <= 0

    def game_over(self) -> bool:
        return self.is_won() or self.is_lost()

    def stage_art(self) -> str:
        stage_index = min(len(self.wrong_guesses), len(HANGMAN_STAGES) - 1)
        return HANGMAN_STAGES[stage_index]


def choose_word(word_list: Iterable[str]) -> str:
    word_list = list(word_list)
    if not word_list:
        raise ValueError("Word list cannot be empty.")
    return random.choice(word_list)


def prompt_for_guess() -> str:
    while True:
        entry = input("Guess a letter: ").strip().lower()
        if len(entry) == 1 and entry.isalpha():
            return entry
        print("Please enter a single letter.")


def print_game_state(game: HangmanGame) -> None:
    print(game.stage_art())
    print(f"Word: {game.masked_word()}")
    if game.wrong_guesses:
        wrong = ", ".join(sorted(game.wrong_guesses))
        print(f"Wrong guesses: {wrong}")
    print(f"Remaining attempts: {game.remaining_attempts}\n")


def main() -> None:
    secret_word = choose_word(WORDS)
    game = HangmanGame(secret_word)

    print("Welcome to Hangman!\n")

    while not game.game_over():
        print_game_state(game)

        try:
            letter = prompt_for_guess()
            correct = game.guess(letter)
            if correct:
                print(f"Good job! '{letter}' is in the word.\n")
            else:
                print(f"Sorry, '{letter}' is not in the word.\n")
        except ValueError as err:
            print(f"{err}\n")
            continue

    print_game_state(game)
    if game.is_won():
        print(f"Congratulations! You guessed the word '{game.secret_word}'.")
    else:
        print(f"Game over! The word was '{game.secret_word}'.")


if __name__ == "__main__":
    main()
