"""Desktop applications: Signal and Bambu Studio.

Replaces the home-manager packages signal-desktop and bambu-studio.
"""

from decman import Module
from decman.plugins import aur, pacman


class Apps(Module):

    def __init__(self):
        super().__init__(name="apps")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"signal-desktop"}

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"bambustudio-bin"}
