"""Git and its user configuration.

Replaces home-manager programs.git. The config file is the same one that was
in /etc/nixos/.config/git/config.
"""

from decman import File, Module
from decman.plugins import pacman

from modules import HOME, USER, files_path


class Git(Module):

    def __init__(self):
        super().__init__(name="git")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"git"}

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.config/git/config": File(
                source_file=files_path("git", "config"), owner=USER
            ),
        }
