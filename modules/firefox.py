"""Firefox with enterprise policies.

Replaces programs.firefox from NixOS: Proton Pass force-installed,
"offer to save logins" disabled. The Arch firefox package reads
/etc/firefox/policies/policies.json.
"""

from decman import File, Module
from decman.plugins import pacman

from modules import files_path


class Firefox(Module):

    def __init__(self):
        super().__init__(name="firefox")

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"firefox"}

    def files(self) -> dict[str, File]:
        return {
            "/etc/firefox/policies/policies.json": File(
                source_file=files_path("firefox", "policies.json")
            ),
        }
