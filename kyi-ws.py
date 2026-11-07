"""Decman source for kyi-ws (Intel CPU, NVIDIA GPU, static wired IP).

Run with:
    sudo decman --source /home/kyi/Source/dotfiles/kyi-ws.py
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

# Enable user-level systemd units (ssh-agent.socket)
decman.systemd.enabled_user_units.setdefault("kyi", set()).update({"ssh-agent.socket"})
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
from modules.hardware.kyi_ws import DesktopHardware
from modules.networking import Networking
from modules.niri import Niri
from modules.ssh import Ssh
from modules.ssh_agent import SshAgent
from modules.users import make_user_manager
from modules.zsh import Zsh

decman.modules += [
    # users first, so files owned by kyi can be installed on a fresh system
    make_user_manager(),
    Base(hostname="kyi-ws"),
    DesktopHardware(),
    Networking(static_wired=True),
    Ssh(authorized_keys=files_path("ssh", "authorized_keys")),  # kyi-nb key
    SshAgent(),
    Bluetooth(),
    Audio(),
    Zsh(),
    Niri(outputs_kdl=files_path("niri", "outputs-kyi-ws.kdl")),
    DuxShell(),
    Greeter(),
    Ghostty(),
    Firefox(),
    Git(),
    Gaming(),
    DevTools(),
    Apps(),
]
