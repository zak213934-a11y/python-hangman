# Remaining Tasks for Hangman Release

## Quality and gameplay validation
- [x] Run the automated test suite (`python -m pytest`) and resolve any failures, including CLI error text expectations. (Pass on Python 3.11 via `python -m pytest`.)
- [x] Perform manual playtests covering both win and loss paths, ensuring invalid guesses are rejected and remaining attempts decrement correctly. (Win/loss paths exercised; invalid numeric guess rejected.)
- [x] Verify CLI options still work: loading words from a custom file, enforcing positive attempt counts, and choosing secrets from the provided list. (Custom file paths honored; non-positive attempts rejected; secrets chosen from provided list.)
- [x] Confirm default word list still produces winnable rounds within the allotted attempts. (Deterministic selection with seeded RNG wins using default allowed attempts.)

## Packaging and distribution
- [x] Build the distributable zipapp (`python build_pyz.py`).
- [x] Smoke-test `dist/hangman.pyz` with default settings plus a custom word file/attempt limit. (Default flow exercised; custom word file + attempt cap validated.)
- [x] Validate the archive runs on a clean environment with only Python 3 installed (no dev dependencies). (Verified via fresh venv running `dist/hangman.pyz` against a custom word file on Python 3.11.)
- [x] Record the Python versions the artifact was tested against. (Tested on Python 3.11.)

## Release packaging workflow
- [x] Ensure the working tree is clean before publishing (or intentionally use `--allow-dirty`). (Verified clean working tree via `git status -sb`.)
- [x] Run `python publish_release.py <version>` to produce the release ZIP. (Published `releases/hangman-v1.0.0.zip` via `python publish_release.py v1.0.0`.)
- [x] Confirm the output lands in `releases/` (or the chosen directory) and matches the expected filename format `hangman-<version>.zip`. (Archive path: `releases/hangman-v1.0.0.zip`.)
- [x] Capture checksum (e.g., `sha256sum`) for the generated archive for later verification. (SHA256: `775ad1aedc02d1553db2aedde3a064650fa6e856537746f3b7e5485909757457`; now written automatically to `hangman-v1.0.0.zip.sha256`.)

## Documentation and communication
- [x] Update release notes or changelog with gameplay, option, and packaging changes included in the build. (Documented in `RELEASE_NOTES.md`, covering CLI validation, packaging workflows, and compatibility.)
- [x] Refresh README instructions if usage, options, or distribution steps change before the release. (Added clean-environment zipapp validation guidance, checksum recording, and release notes pointer.)
- [x] Note any manual validation performed and environments used, to aid future reproducibility. (Validation summary and Python 3.11 environment captured in `RELEASE_NOTES.md`.)

## Post-release verification
- [ ] Install and run the published artifact on at least one fresh machine to confirm packaging integrity.
- [ ] Monitor for crash or input-validation issues reported by early users and prepare a hotfix plan if needed.
