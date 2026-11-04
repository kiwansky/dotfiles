"""Decman source for the desktop (Intel CPU, NVIDIA GPU, static wired IP).

Run with:
    sudo decman --source /home/kyi/Source/dotfiles/desktop.py
"""

import os
import sys

try:
    _here = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _here = os.getcwd()
if _here not in sys.path:
    sys.path.insert(0, _here)

import decman

from modules import files_path
from modules.apps import Apps
from modules.audio import Audio
from modules.base import Base
from modules.bluetooth import Bluetooth
from modules.devtools import DevTools
from modules.dux import DuxShell
from modules.firefox import Firefox
from modules.gaming import Gaming
from modules.ghostty import Ghostty
from modules.git import Git
from modules.greeter import Greeter
from modules.hardware.desktop import DesktopHardware
from modules.networking import Networking
from modules.niri import Niri
from modules.users import make_user_manager
from modules.zsh import Zsh

decman.modules += [
    # users first, so files owned by kyi can be installed on a fresh system
    make_user_manager(),
    Base(hostname="desktop"),
    DesktopHardware(),
    Networking(static_wired=True),
    Bluetooth(),
    Audio(),
    Zsh(),
    Niri(outputs_kdl=files_path("niri", "outputs-desktop.kdl")),
    DuxShell(),
    Greeter(),
    Ghostty(),
    Firefox(),
    Git(),
    Gaming(),
    DevTools(),
    Apps(),
]
