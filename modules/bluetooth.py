"""Bluetooth.

Replaces hardware.bluetooth from NixOS. powerOnBoot is covered by BlueZ's
default AutoEnable=true (/etc/bluetooth/main.conf).
"""

from decman import Module
from decman.plugins import pacman, systemd


class Bluetooth(Module):

    def __init__(self):
        super().__init__(name="bluetooth")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"bluez", "bluez-utils"}

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"bluetooth.service"}
