"""Niri compositor and its configuration.

Replaces programs.niri plus the home-manager managed ~/.config/niri dotfiles.

The dms/outputs.kdl file is host specific (monitor layout), so each machine
passes its own source file for it. xwayland-satellite is started by niri
automatically when installed. The portals cover screencast (gnome) and file
dialogs (gtk) for the niri session.
"""

from decman import Directory, File, Module
from decman.plugins import pacman

from modules import HOME, USER, files_path


class Niri(Module):

    def __init__(self, outputs_kdl: str):
        super().__init__(name="niri")
        self._outputs_kdl = outputs_kdl

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "niri",
            "xwayland-satellite",
            "xdg-desktop-portal-gnome",
            "xdg-desktop-portal-gtk",
            "brightnessctl",  # used by the XF86MonBrightness binds
        }

    def directories(self) -> dict[str, Directory]:
        return {
            f"{HOME}/.config/niri": Directory(
                source_directory=files_path("niri"), owner=USER
            ),
        }

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.config/niri/dms/outputs.kdl": File(
                source_file=self._outputs_kdl, owner=USER
            ),
        }
