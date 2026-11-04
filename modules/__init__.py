"""Shared constants and helpers for all decman modules."""

from pathlib import Path

# Absolute path to the repository root, so modules work no matter
# which directory decman is invoked from.
REPO_ROOT = Path(__file__).resolve().parent.parent
FILES = REPO_ROOT / "files"

USER = "kyi"
HOME = f"/home/{USER}"


def files_path(*parts: str) -> str:
    """Absolute path to a file inside the repository's files/ directory."""
    return str(FILES.joinpath(*parts))
