"""Dux Shell (formerly DankMaterialShell / DMS) desktop shell.

Replaces programs.dms-shell and programs.dsearch from NixOS:
  - dux-shell ships /usr/bin/dms and the dms.service user unit
    (programs.dms-shell.systemd.enable)
  - dux-gop provides dgop (enableSystemMonitoring)
  - matugen provides dynamic theming (enableDynamicTheming)
  - dux-search-bin ships dsearch and the dsearch.service user unit, which is
    bound to graphical-session.target (programs.dsearch.systemd)

The fonts are the ones DMS expects for icons and UI (Material Symbols,
Inter, a nerd font), plus general Noto coverage.
"""

from decman import Module
from decman.plugins import aur, pacman, systemd

from modules import USER


class DuxShell(Module):

    def __init__(self):
        super().__init__(name="dux-shell")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "dux-shell",
            "dux-gop",
            "matugen",
            "quickshell",
            "wl-clipboard",
            "wtype",
            "ttf-material-symbols-variable",
            "inter-font",
            "ttf-jetbrains-mono-nerd",
            "noto-fonts",
            "noto-fonts-emoji",
        }

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"dux-search-bin"}

    @systemd.user_units
    def systemd_user_units(self) -> dict[str, set[str]]:
        return {USER: {"dms.service", "dsearch.service"}}
