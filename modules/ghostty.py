"""Ghostty terminal.

Replaces home-manager programs.ghostty. Shell integration for zsh is
automatic in ghostty (it injects it when launching the shell), so only the
settings file is needed.
"""

from decman import File, Module
from decman.plugins import pacman

from modules import HOME, USER, files_path


class Ghostty(Module):

    def __init__(self):
        super().__init__(name="ghostty")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"ghostty"}

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.config/ghostty/config": File(
                source_file=files_path("ghostty", "config"), owner=USER
            ),
        }
