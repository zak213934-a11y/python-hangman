"""Simple command-line Hangman game with configurable options."""

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
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
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
            allowed_attempts
            if allowed_attempts is not None
            else len(HANGMAN_STAGES) - 1
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
            letter if letter in self.guessed_letters else "_"
            for letter in self.secret_word
        )

    def guess(self, letter: str) -> bool:
        """Process a guess and return ``True`` when correct.

        Raises:
            ValueError: If the guess is invalid or already made.
        """

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

        stage_index = min(len(self.wrong_guesses), len(HANGMAN_STAGES) - 1)
        return HANGMAN_STAGES[stage_index]


def choose_word(word_list: Iterable[str], rng: random.Random | None = None) -> str:
    """Choose a word from ``word_list`` using the provided ``rng`` if given."""

    words = list(word_list)
    if not words:
        raise ValueError("Word list cannot be empty.")

    chooser = rng if rng is not None else random
    return chooser.choice(words)


def load_words_from_file(path: Path | str) -> list[str]:
    """Load words from a file, returning only alphabetic entries.

    Raises:
        ValueError: If no valid words are found.
    """

    file_path = Path(path)
    lines = [
        line.strip() for line in file_path.read_text(encoding="utf-8").splitlines()
    ]
    words = [line for line in lines if line.isalpha()]

    if not words:
        raise ValueError("Word file does not contain any valid words.")

    return words


def prompt_for_guess() -> str:
    """Prompt the user for a single-letter guess."""

    while True:
        entry = input("Guess a letter: ").strip().lower()
        if len(entry) == 1 and entry.isalpha():
            return entry
        print("Please enter a single letter.")


def print_game_state(game: HangmanGame) -> None:
    """Print the current Hangman state to the console."""

    print(game.stage_art())
    print(f"Word: {game.masked_word()}")
    if game.wrong_guesses:
        wrong = ", ".join(sorted(game.wrong_guesses))
        print(f"Wrong guesses: {wrong}")
    print(f"Remaining attempts: {game.remaining_attempts}\n")


def main(argv: Sequence[str] | None = None) -> None:
    """Run the Hangman game using optional CLI arguments."""

    parser = argparse.ArgumentParser(description="Play a game of Hangman.")
    parser.add_argument(
        "--word-file",
        type=Path,
        help="Optional path to a file containing one word per line to use instead of defaults.",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=None,
        help="Number of incorrect attempts allowed (default: depends on hangman stages).",
    )
    args = parser.parse_args(argv)

    if args.word_file:
        words = load_words_from_file(args.word_file)
    else:
        words = DEFAULT_WORDS

    secret_word = choose_word(words)
    game = HangmanGame(secret_word, allowed_attempts=args.attempts)

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
