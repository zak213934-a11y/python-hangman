# Python Hangman

A simple command-line Hangman game written in Python.

## Branching

All prior feature branches have been consolidated. The `main` branch now tracks
the up-to-date codebase and should be used for all future work.

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

After building, you can validate the archive in a clean environment by creating
a virtualenv with only Python installed and running the zipapp against a small
custom word list. This mirrors the release smoke tests captured in
`RELEASE_NOTES.md`.

## Testing

Run the unit tests with:

```bash
python -m pytest
```

## Publishing a release archive

Create a zip of the current `HEAD` revision with:

```bash
python publish_release.py v1.1.0
```

The script uses `git archive` to capture the repository state and writes the
result to `releases/hangman-v1.1.0.zip`. It refuses to run if there are
uncommitted changes unless you supply `--allow-dirty`. Use `--output-dir` to
change where the archive is stored. To publish a specific tag or branch instead
of `HEAD`, provide `--ref <git-ref>`.

After publishing, the script writes a `hangman-v1.1.0.zip.sha256` file in the
same directory with a ready-to-share SHA256 checksum for downstream
verification.

If you plan to lint or run the publishing workflow locally, install the dev
tooling first:

```bash
pip install -r requirements-dev.txt
```

## Release notes and validation

See `RELEASE_NOTES.md` for a summary of gameplay/CLI changes, packaging
updates, and the manual and automated validation performed (including tested
Python versions).
