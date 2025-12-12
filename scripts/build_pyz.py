"""Build a self-contained Hangman zipapp without external dependencies."""

from __future__ import annotations

import zipapp
from pathlib import Path


def build_zipapp() -> Path:
    """Create ``dist/hangman.pyz`` from the ``src`` package layout.

    The resulting file can be executed with ``python dist/hangman.pyz``
    on any machine with Python 3 installed.
    """

    project_root = Path(__file__).resolve().parent.parent
    src_dir = project_root / "src"
    dist_dir = project_root / "dist"
    dist_dir.mkdir(exist_ok=True)

    target = dist_dir / "hangman.pyz"

    zipapp.create_archive(
        src_dir,
        target,
        interpreter="/usr/bin/env python3",
        main="hangman.__main__:main",
    )

    return target


if __name__ == "__main__":
    archive_path = build_zipapp()
    print(f"Created {archive_path}")
