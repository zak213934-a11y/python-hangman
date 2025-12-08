# Python Hangman

A simple command-line Hangman game written in Python.

## How to Play

1. Run `python hangman.py`.
2. Guess one letter at a time when prompted.
3. You win by revealing the secret word before running out of attempts.

## Options

- `--word-file PATH`: Provide a newline-delimited list of words to draw from.
- `--max-attempts N`: Override the number of allowed wrong guesses (default matches the hangman art).
- `--seed N`: Supply a seed for deterministic word selection when testing.

## Testing

Run the unit tests with:

```bash
python -m pytest
```
