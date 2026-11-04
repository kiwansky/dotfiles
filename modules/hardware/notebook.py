"""Notebook hardware: AMD CPU + AMD GPU.

The AMD equivalent of the desktop's hardware module:
  - amd-ucode microcode
  - mesa/vulkan-radeon (plus lib32 for Steam) for the GPU
  - libva-mesa-driver for hardware video decode
  - power-profiles-daemon for laptop power management; the Dux Shell battery
    widget integrates with it
"""

from decman import Module
from decman.plugins import pacman, systemd


class NotebookHardware(Module):

    def __init__(self):
        super().__init__(name="hardware-notebook")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "amd-ucode",
            "mesa",
            "lib32-mesa",
            "vulkan-radeon",
            "lib32-vulkan-radeon",
            "libva-mesa-driver",
            "power-profiles-daemon",
        }

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"power-profiles-daemon.service"}
