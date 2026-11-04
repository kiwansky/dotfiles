"""User accounts.

Replaces users.users."kyi" from the NixOS config.

Notes:
  - The "networkmanager" group does not exist on Arch; NetworkManager is
    controlled through polkit and wheel membership instead.
  - Set the password manually once: passwd kyi
"""

from decman.extras.users import User, UserManager

from modules import USER


def make_user_manager() -> UserManager:
    um = UserManager()
    um.add_user(
        User(
            username=USER,
            shell="/usr/bin/zsh",
            groups=("wheel", "input"),
        )
    )
    return um
