"""Steam with Proton GE and PlayStation controller support.

Replaces programs.steam (extraCompatPackages proton-ge-bin) and
boot.kernelModules = ["hid-playstation"] from NixOS.

Requires the [multilib] repository, which is enabled in the pacman.conf
managed by the base module. remotePlay.openFirewall has no equivalent here
because a default Arch install runs no firewall. The 32-bit Vulkan driver
comes from the hardware module of each machine.
"""

from decman import File, Module
from decman.plugins import aur, pacman


class Gaming(Module):

    def __init__(self):
        super().__init__(name="gaming")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"steam"}

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"proton-ge-custom-bin"}

    def files(self) -> dict[str, File]:
        return {
            "/etc/modules-load.d/hid-playstation.conf": File(
                content="hid_playstation\n"
            ),
        }
