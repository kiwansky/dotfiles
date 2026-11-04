"""Zsh with oh-my-zsh (theme: lambda) and syntax highlighting.

Replaces programs.zsh (system) and the home-manager programs.zsh block:
enableCompletion (oh-my-zsh runs compinit), syntaxHighlighting,
history.size 10000, oh-my-zsh theme "lambda".
"""

from decman import File, Module
from decman.plugins import aur, pacman

from modules import HOME, USER, files_path


class Zsh(Module):

    def __init__(self):
        super().__init__(name="zsh")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"zsh", "zsh-completions", "zsh-syntax-highlighting"}

    @aur.packages
    def aur_packages(self) -> set[str]:
        # installs to /usr/share/oh-my-zsh
        return {"oh-my-zsh-git"}

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.zshrc": File(source_file=files_path("zsh", "zshrc"), owner=USER),
        }
