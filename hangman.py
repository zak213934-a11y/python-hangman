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
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
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
