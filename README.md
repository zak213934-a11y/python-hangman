# Python Hangman

A simple command-line Hangman game written in Python.

## How to Play

1. Run `python hangman.py`.
2. Guess one letter at a time when prompted.
3. You win by revealing the secret word before running out of attempts.

## Options

- `--word-file PATH`: Provide a newline-delimited list of words to draw from.
- `--attempts N`: Override the number of allowed wrong guesses (default matches the hangman art).

## Building a distributable zipapp

If network restrictions block installing PyInstaller, you can still ship a
single-file archive that runs on any machine with Python 3 installed:

```bash
python build_pyz.py
```

The build places `dist/hangman.pyz` alongside the project. Launch it with
`python dist/hangman.pyz [options]` and distribute that file to end users.
The `dist/` directory is gitignored, so generate the archive locally when
you need to ship it.

## Testing

Run the unit tests with:

```bash
python -m pytest
```

## Publishing a release archive

Create a zip of the current `HEAD` revision with:

```bash
python publish_release.py v1.0.0
```

The script uses `git archive` to capture the repository state and writes the
result to `releases/hangman-v1.0.0.zip`. It refuses to run if there are
uncommitted changes unless you supply `--allow-dirty`. Use `--output-dir` to
change where the archive is stored. To publish a specific tag or branch
instead of `HEAD`, provide `--ref <git-ref>`.
