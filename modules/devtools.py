"""Development tools: Claude Code and opencode.

Replaces the home-manager packages claude-code and programs.opencode
(autoupdate false, model mistral/devstral-medium-latest).
"""

from decman import File, Module
from decman.plugins import aur

from modules import HOME, USER, files_path


class DevTools(Module):

    def __init__(self):
        super().__init__(name="devtools")

    @aur.packages
    def aur_packages(self) -> set[str]:
        return {"claude-code", "opencode-bin"}

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.config/opencode/opencode.json": File(
                source_file=files_path("opencode", "opencode.json"), owner=USER
            ),
        }
