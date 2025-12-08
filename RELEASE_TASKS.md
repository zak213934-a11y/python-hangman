# Remaining Tasks for Hangman Release

## Quality and gameplay validation
- Run the automated test suite (`python -m pytest`) and keep it green before tagging a release.
- Perform manual playtests covering both win and loss paths, ensuring invalid guesses are rejected and remaining attempts behave as expected.
- Verify CLI options still work: loading words from a custom file, enforcing positive attempt counts, and choosing secrets from the provided list.

## Packaging and distribution
- Build the distributable zipapp (`python build_pyz.py`) and smoke-test `dist/hangman.pyz` with default settings plus a custom word file/attempt limit.
- Confirm the generated archive runs on a clean environment with only Python 3 installed.

## Release packaging workflow
- Use `python publish_release.py <version>` to produce the release ZIP, ensuring the working tree is clean unless `--allow-dirty` is explicitly intended.
- Store the resulting archive in the desired output directory (default: `releases/`) and validate the expected filename format (`hangman-<version>.zip`).

## Documentation and communication
- Update release notes or changelog with gameplay, option, and packaging changes included in the build.
- Refresh README instructions if usage, options, or distribution steps change before the release.
