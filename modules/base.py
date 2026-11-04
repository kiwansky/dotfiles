"""Core system: base packages, pacman.conf, hostname, locale, console, time zone, sudo.

Replaces from the NixOS config:
  - time.timeZone, i18n.*, services.xserver.xkb (console side), networking.hostName
  - the implicit NixOS base system (bootloader packages, sudo-like access via wheel)
  - decman manages itself here (like nixos-rebuild being part of NixOS)
"""

from decman import File, Module, prg
from decman.plugins import aur, pacman, systemd

from modules import files_path


class Base(Module):

    def __init__(self, hostname: str):
        super().__init__(name="base")
        self._hostname = hostname

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "base",
            "base-devel",  # needed to build AUR packages
            "linux",
            "linux-firmware",
            "efibootmgr",
            "sudo",
            "man-db",
            "man-pages",
            "less",
            "nano",
            "openssl",  # was in environment.systemPackages
        }

    @aur.packages
    def aur_packages(self) -> set[str]:
        # decman manages itself
        return {"decman"}

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"systemd-timesyncd.service"}

    def files(self) -> dict[str, File]:
        return {
            "/etc/pacman.conf": File(source_file=files_path("pacman.conf")),
            "/etc/hostname": File(content=self._hostname + "\n"),
            "/etc/locale.conf": File(source_file=files_path("locale.conf")),
            "/etc/locale.gen": File(source_file=files_path("locale.gen")),
            "/etc/vconsole.conf": File(source_file=files_path("vconsole.conf")),
            "/etc/sudoers.d/10-wheel": File(
                source_file=files_path("sudoers-wheel"), permissions=0o440
            ),
        }

    def symlinks(self) -> dict[str, str]:
        # time.timeZone = "Europe/Berlin"
        return {"/etc/localtime": "/usr/share/zoneinfo/Europe/Berlin"}

    def on_enable(self, store):
        prg(["locale-gen"])

    def on_change(self, store):
        prg(["locale-gen"])
