"""kyi-nb hardware: AMD CPU + AMD GPU.

The AMD equivalent of kyi-ws's hardware module:
  - amd-ucode microcode
  - mesa/vulkan-radeon (plus lib32 for Steam) for the GPU; mesa includes the
    VAAPI video decode drivers (the separate libva-mesa-driver package was
    merged into mesa)
  - power-profiles-daemon for laptop power management; the Dux Shell battery
    widget integrates with it
"""

from decman import Module
from decman.plugins import pacman, systemd


class NotebookHardware(Module):

    def __init__(self):
        super().__init__(name="hardware-kyi-nb")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "amd-ucode",
            "mesa",
            "lib32-mesa",
            "vulkan-radeon",
            "lib32-vulkan-radeon",
            "power-profiles-daemon",
        }

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"power-profiles-daemon.service"}
