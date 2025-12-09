# Remaining Tasks for Hangman Release

## Quality and gameplay validation
- [ ] Run the automated test suite (`python -m pytest`) and resolve any failures, including CLI error text expectations.
- [ ] Perform manual playtests covering both win and loss paths, ensuring invalid guesses are rejected and remaining attempts decrement correctly.
- [ ] Verify CLI options still work: loading words from a custom file, enforcing positive attempt counts, and choosing secrets from the provided list.
- [ ] Confirm default word list still produces winnable rounds within the allotted attempts.

## Packaging and distribution
- [ ] Build the distributable zipapp (`python build_pyz.py`).
- [ ] Smoke-test `dist/hangman.pyz` with default settings plus a custom word file/attempt limit.
- [ ] Validate the archive runs on a clean environment with only Python 3 installed (no dev dependencies).
- [ ] Record the Python versions the artifact was tested against.

## Release packaging workflow
- [ ] Ensure the working tree is clean before publishing (or intentionally use `--allow-dirty`).
- [ ] Run `python publish_release.py <version>` to produce the release ZIP.
- [ ] Confirm the output lands in `releases/` (or the chosen directory) and matches the expected filename format `hangman-<version>.zip`.
- [ ] Capture checksum (e.g., `sha256sum`) for the generated archive for later verification.

## Documentation and communication
- [ ] Update release notes or changelog with gameplay, option, and packaging changes included in the build.
- [ ] Refresh README instructions if usage, options, or distribution steps change before the release.
- [ ] Note any manual validation performed and environments used, to aid future reproducibility.

## Post-release verification
- [ ] Install and run the published artifact on at least one fresh machine to confirm packaging integrity.
- [ ] Monitor for crash or input-validation issues reported by early users and prepare a hotfix plan if needed.
