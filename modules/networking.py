"""NetworkManager, optionally with the desktop's static wired profile.

Replaces networking.networkmanager / networking.interfaces.eth0 from NixOS.
The static profile matches any wired interface instead of hardcoding "eth0",
since Arch uses predictable interface names (enp5s0, ...).
"""

from decman import File, Module
from decman.plugins import pacman, systemd

from modules import files_path


class Networking(Module):

    def __init__(self, static_wired: bool = False):
        super().__init__(name="networking")
        self._static_wired = static_wired

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"networkmanager"}

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"NetworkManager.service"}

    def files(self) -> dict[str, File]:
        if not self._static_wired:
            return {}
        return {
            "/etc/NetworkManager/system-connections/wired-static.nmconnection": File(
                source_file=files_path("networkmanager", "wired-static.nmconnection"),
                permissions=0o600,
            ),
        }
