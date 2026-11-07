"""OpenSSH server, key-only logins.

Installs openssh and starts sshd.service at boot on both machines. The
drop-in files/ssh/10-key-only.conf turns off password logins, so only
public keys work. With ``authorized_keys`` set, the module also installs
that file as ~/.ssh/authorized_keys of the user, so the listed machines
can log in. The desktop uses files/ssh/authorized_keys, which holds the
notebook's public key.
"""

import os

from decman import File, Module, prg
from decman.plugins import pacman, systemd

from modules import HOME, USER, files_path


class Ssh(Module):

    def __init__(self, authorized_keys: str | None = None):
        super().__init__(name="ssh")
        self._authorized_keys = authorized_keys

    @pacman.packages
    def pacman_packages(self) -> set[str]:
        return {"openssh"}

    @systemd.units
    def systemd_units(self) -> set[str]:
        return {"sshd.service"}

    def files(self) -> dict[str, File]:
        files = {
            "/etc/ssh/sshd_config.d/10-key-only.conf": File(
                source_file=files_path("ssh", "10-key-only.conf")
            ),
        }
        if self._authorized_keys is not None:
            files[f"{HOME}/.ssh/authorized_keys"] = File(
                source_file=self._authorized_keys, owner=USER, permissions=0o600
            )
        return files

    def _reload_sshd(self):
        # Pick up a changed sshd config. Does nothing if sshd is not running.
        prg(["systemctl", "try-reload-or-restart", "sshd.service"])

    def on_enable(self, store):
        self._reload_sshd()

    def on_change(self, store):
        self._reload_sshd()

    def after_update(self, store):
        # decman creates a missing ~/.ssh with the umask default (0755).
        # sshd accepts that, but the directory should be private.
        ssh_dir = f"{HOME}/.ssh"
        if self._authorized_keys is not None and os.path.isdir(ssh_dir):
            os.chmod(ssh_dir, 0o700)
