"""PipeWire audio stack.

On NixOS this came with the desktop defaults; the niri config's volume and
media binds rely on wpctl (WirePlumber) and playerctl.
"""

from decman import Module
from decman.plugins import pacman, systemd

from modules import USER


class Audio(Module):

    def __init__(self):
        super().__init__(name="audio")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "pipewire",
            "pipewire-alsa",
            "pipewire-pulse",
            "wireplumber",
            "playerctl",
        }

    @systemd.user_units
    def systemd_user_units(self) -> dict[str, set[str]]:
        return {
            USER: {
                "pipewire.socket",
                "pipewire-pulse.socket",
                "wireplumber.service",
            }
        }
