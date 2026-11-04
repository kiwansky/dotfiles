"""greetd with the Dux greeter, polkit and GNOME keyring.

Replaces from NixOS:
  - services.displayManager.dms-greeter (compositor niri)
  - security.polkit.enable
  - services.gnome.gnome-keyring.enable (PAM unlock on login happens via the
    pam_gnome_keyring lines in /etc/pam.d/greetd)

After the first login you can run `dms-greeter sync` once to copy your DMS
theme and wallpaper to the login screen.
"""

from decman import File, Module
from decman.plugins import aur, pacman, systemd

from modules import files_path


class Greeter(Module):

    def __init__(self):
        super().__init__(name="greeter")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"greetd", "polkit", "gnome-keyring"}

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"dux-greeter-bin"}

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"greetd.service"}

    def files(self) -> dict[str, File]:
        return {
            "/etc/greetd/config.toml": File(
                source_file=files_path("greetd", "config.toml")
            ),
            "/etc/pam.d/greetd": File(source_file=files_path("greetd", "pam-greetd")),
        }
