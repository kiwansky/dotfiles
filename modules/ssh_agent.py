"""SSH agent setup for user-specific systemd-based key management.

Enables ssh-agent.socket (user-level systemd socket) to automatically start
ssh-agent.service on demand. Configures ~/.ssh/config to add keys to the
agent on first use (AddKeysToAgent yes).
"""

from decman import File, Module

from modules import HOME, USER


class SshAgent(Module):

    def __init__(self):
        super().__init__(name="ssh-agent")

    def files(self) -> dict[str, File]:
        return {
            f"{HOME}/.ssh/config": File(
                content="Host *\n  AddKeysToAgent yes\n",
                owner=USER,
                permissions=0o600,
            ),
        }

    def on_enable(self, store):
        import os

        ssh_dir = f"{HOME}/.ssh"
        if os.path.isdir(ssh_dir):
            os.chmod(ssh_dir, 0o700)
