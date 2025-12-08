"""Utility to package the repository into a versioned release archive.

The script uses ``git archive`` to produce a zip file of the selected git
reference. It defaults to storing the archive under ``releases/`` and refuses to
run if there are uncommitted changes unless ``--allow-dirty`` is supplied.
"""

from __future__ import annotations

import argparse
import subprocess
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
        raise RuntimeError("Working tree is dirty; commit or stash changes before releasing.")


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


def main() -> None:
    """Parse CLI arguments and create a release archive."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Version label for the release archive (e.g. v1.0.0)")
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
    archive_path = create_release_archive(
        args.version, args.output_dir, args.allow_dirty, ref=args.ref
    )
    print(f"Release archive created at {archive_path}")


if __name__ == "__main__":
    main()
