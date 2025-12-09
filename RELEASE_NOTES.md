# Hangman v1.1.0 Release Notes

## Gameplay and CLI updates
- Validates non-positive `--attempts` values with a clear error message while preserving backward compatibility for script and module invocations.
- Supports custom word lists via `--word-file` and continues to select secrets from the provided list without repeats in a single game.
- Confirms the default word list remains winnable within the allotted attempts using deterministic, seeded selection for verification.

## Packaging changes
- Provides a reproducible zipapp build via `python build_pyz.py`, producing `dist/hangman.pyz`.
- Adds a publishing workflow through `python publish_release.py <version>` that writes `releases/hangman-<version>.zip` and records a SHA256 checksum alongside the archive (`hangman-v1.1.0.zip` at commit time).

## Validation summary
- Automated tests: `python -m pytest` (Python 3.11).
- Manual gameplay checks on Python 3.11:
  - Win path using a custom word file with six attempts.
  - Loss path using a custom word file with three attempts, including invalid numeric guess rejection.
  - Default word list win with seeded RNG to confirm winnability.
- Packaging smoke tests:
  - `dist/hangman.pyz` executed with default settings and with custom word file/attempt limits.
  - `dist/hangman.pyz` run inside a clean virtual environment containing only Python 3.11.

## Compatibility
- Tested on Python 3.11 for gameplay, packaging, and publishing workflows.
