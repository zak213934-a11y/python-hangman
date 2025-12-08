"""Build a self-contained Hangman zipapp without external dependencies."""

from __future__ import annotations

import shutil
import tempfile
import zipapp
from pathlib import Path


def build_zipapp() -> Path:
    """Create ``dist/hangman.pyz`` from ``hangman.py``.

    The resulting file can be executed with ``python dist/hangman.pyz``
    on any machine with Python 3 installed.
    """

    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    dist_dir.mkdir(exist_ok=True)

    target = dist_dir / "hangman.pyz"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        shutil.copy(project_root / "hangman.py", tmp_path / "__main__.py")
        zipapp.create_archive(tmp_path, target, interpreter="/usr/bin/env python3")

    return target


if __name__ == "__main__":
    archive_path = build_zipapp()
    print(f"Created {archive_path}")
