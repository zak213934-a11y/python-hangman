# path: scripts/publish_release.py
# WHY: This replaces the duplicated blocks reported by Pylint R0801.

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


def ensure_clean_worktree() -> None:
    """Fail if the working tree has uncommitted changes."""
    result = subprocess.run(  # nosec - trusted local git invocation
        ["git", "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        # WHY: Make failures explicit in CI.
        raise RuntimeError(
            "Working tree is dirty; commit or stash changes before releasing."
        )


def create_release_archive(
    version: str,
    output_dir: Path,
    allow_dirty: bool,
    ref: str = "HEAD",
) -> Path:
    """Create a zip archive of the given repository revision.

    Args:
        version: Version label (e.g. ``v1.2.3``).
        output_dir: Directory in which to place the archive.
        allow_dirty: If True, skip clean working tree check.
        ref: Git ref to archive (defaults to ``HEAD``).

    Returns:
        Path to the created archive.
    """
    if not allow_dirty:
        ensure_clean_worktree()

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"hangman-{version}.zip"

    # WHY: Use git-archive to produce a clean tree, excluding untracked files.
    subprocess.run(
        ["git", "archive", "--format", "zip", "-o", str(archive_path), ref],
        check=True,
    )
    return archive_path


def write_sha256_checksum(archive_path: Path) -> Path:
    """Compute and write a sha256 checksum file alongside ``archive_path``."""
    digest = hashlib.sha256()
    with archive_path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            digest.update(chunk)

    checksum = digest.hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n")
    return checksum_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args (isolated for testability)."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Version label for the release (e.g. v1.1.0)")
    parser.add_argument("--ref", default="HEAD", help="Git ref to archive (default: HEAD)")
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Create release archive and checksum from CLI."""
    args = parse_args(argv)
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
