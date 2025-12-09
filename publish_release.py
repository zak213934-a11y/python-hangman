"""Utility to package the repository into a versioned release archive.

The script uses ``git archive`` to produce a zip file of the selected git
reference. By default it targets ``HEAD`` and writes to ``releases/``, but you
can override the location with ``--output-dir`` and choose any tag or branch via
``--ref``. It refuses to run if there are uncommitted changes unless
``--allow-dirty`` is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


def ensure_clean_worktree() -> None:
    """Raise ``RuntimeError`` if the working tree has uncommitted changes."""

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        raise RuntimeError(
            "Working tree is dirty; commit or stash changes before releasing."
        )


def create_release_archive(
    version: str, output_dir: Path, allow_dirty: bool, ref: str = "HEAD"
) -> Path:
    """Create a zip archive of the given repository revision.

    Args:
        version: Version label used in the archive filename (e.g. ``v1.2.3``).
        output_dir: Directory in which to place the archive.
        allow_dirty: If ``True``, skip the clean working tree check.
        ref: Git ref to archive (defaults to ``HEAD``).

    Returns:
        Path to the created archive.
    """

    if not allow_dirty:
        ensure_clean_worktree()

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"hangman-{version}.zip"

    subprocess.run(
        ["git", "archive", "--format", "zip", "-o", str(archive_path), ref],
        check=True,
    )

    return archive_path


def write_sha256_checksum(archive_path: Path) -> Path:
    """Compute and write a SHA256 checksum file for ``archive_path``.

    The checksum is written next to the archive using the ``<name>.sha256``
    format with ``sha256sum``-compatible contents.
    """

    digest = hashlib.sha256()
    with archive_path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            digest.update(chunk)

    checksum = digest.hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n")
    return checksum_path


def main() -> None:
    """Parse CLI arguments and create a release archive."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "version", help="Version label for the release archive (e.g. v1.0.0)"
    )
    parser.add_argument(
        "--ref",
        default="HEAD",
        help="Git ref to archive (default: HEAD)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("releases"),
        help="Directory where the release archive should be written (default: releases/)",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow creating a release even when the working tree has uncommitted changes.",
    )
    args = parser.parse_args()

    try:
        archive_path = create_release_archive(
            args.version, args.output_dir, args.allow_dirty, ref=args.ref
        )
        checksum_path = write_sha256_checksum(archive_path)
    except subprocess.CalledProcessError as err:
        print(f"Failed to archive git reference '{args.ref}': {err}", file=sys.stderr)
        raise SystemExit(1) from err
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1) from err

    print(f"Release archive created at {archive_path}")
    print(f"SHA256 checksum written to {checksum_path}")


if __name__ == "__main__":
    main()
