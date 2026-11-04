"""Decman source for the notebook (AMD CPU and GPU, DHCP/Wi-Fi via NetworkManager).

Run with:
    sudo decman --source /home/kyi/Source/dotfiles/notebook.py
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
from modules.hardware.notebook import NotebookHardware
from modules.networking import Networking
from modules.niri import Niri
from modules.users import make_user_manager
from modules.zsh import Zsh

decman.modules += [
    # users first, so files owned by kyi can be installed on a fresh system
    make_user_manager(),
    Base(hostname="notebook"),
    NotebookHardware(),
    Networking(static_wired=False),
    Bluetooth(),
    Audio(),
    Zsh(),
    Niri(outputs_kdl=files_path("niri", "outputs-notebook.kdl")),
    DuxShell(),
    Greeter(),
    Ghostty(),
    Firefox(),
    Git(),
    Gaming(),  # remove this line if you don't want Steam on the notebook
    DevTools(),
    Apps(),
]
