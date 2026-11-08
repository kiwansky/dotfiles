"""Development tools: opencode, Ansible, proxmoxer.

Replaces the home-manager package programs.opencode
(autoupdate false, model mistral/devstral-medium-latest).
"""

from decman import File, Module
from decman.plugins import aur, pacman

from modules import HOME, USER, files_path


class DevTools(Module):

    def __init__(self):
        super().__init__(name="devtools")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {
            "ansible",
            "python-proxmoxer",  # Proxmox API client, used by the community.proxmox Ansible modules
        }

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"claude-code"}

