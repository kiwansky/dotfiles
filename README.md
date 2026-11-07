# dotfiles — Arch Linux with decman

This repository contains a declarative configuration for Arch Linux.
The tool [decman](https://github.com/kiviktnm/decman) applies the configuration.
The configuration is a conversion of the NixOS configuration from `/etc/nixos/`.

Two machines use the same modules. Each machine has its own entry point:

| Entry point   | Machine  | Hardware               | Network                            |
| ------------- | -------- | ---------------------- | ---------------------------------- |
| `kyi-ws.py`  | kyi-ws  | Intel CPU + NVIDIA GPU | Static wired IP (192.168.10.30/24) |
| `kyi-nb.py` | kyi-nb | AMD CPU + AMD GPU      | DHCP / Wi-Fi with NetworkManager   |

## Layout

```
kyi-ws.py / kyi-nb.py   decman sources (one for each machine)
modules/                   one Python module for each function; each module
                           keeps the packages, their config files, and their
                           services together
files/                     the config files / dotfiles
```

## The modules and the NixOS options that they replace

| Module              | Packages                                                     | NixOS equivalent                                                      |
| ------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------- |
| `base`              | base, linux, base-devel, sudo, … + `decman` (AUR)            | base system, `time.timeZone`, `i18n.*`, hostname, wheel sudo           |
| `users`             | —                                                            | `users.users.kyi` (zsh shell, wheel + input groups)                    |
| `networking`        | networkmanager                                               | `networking.networkmanager`, static `eth0` config (kyi-ws)            |
| `ssh`               | openssh                                                      | — (new: sshd at boot, key-only logins; kyi-ws gets `files/ssh/authorized_keys`) |
| `bluetooth`         | bluez, bluez-utils                                           | `hardware.bluetooth` (powerOnBoot = BlueZ AutoEnable default)          |
| `audio`             | pipewire(+pulse/alsa), wireplumber, playerctl                | the PipeWire stack for the niri binds (wpctl/playerctl)                |
| `zsh`               | zsh, zsh-completions, zsh-syntax-highlighting, oh-my-zsh-git | `programs.zsh` + home-manager zsh (theme lambda, hist 10000)           |
| `niri`              | niri, xwayland-satellite, portals, brightnessctl             | `programs.niri` + the `~/.config/niri` dotfiles                        |
| `dux-shell`         | dux-shell, dux-gop, matugen, dux-search-bin (AUR), fonts     | `programs.dms-shell` (+systemd, sysmon, theming), `programs.dsearch`   |
| `greeter`           | greetd, dux-greeter-bin (AUR), polkit, gnome-keyring         | `services.displayManager.dms-greeter`, `security.polkit`, gnome-keyring |
| `ghostty`           | ghostty                                                      | home-manager `programs.ghostty` (background-opacity 0.5)               |
| `firefox`           | firefox                                                      | `programs.firefox` policies (Proton Pass force-installed)              |
| `git`               | git                                                          | home-manager `programs.git` (`files/git/config`)                       |
| `gaming`            | steam, proton-ge-custom-bin (AUR)                            | `programs.steam` + `boot.kernelModules = [hid-playstation]`            |
| `devtools`          | ansible, python-proxmoxer, opencode-bin (AUR) | home-manager `programs.opencode`                         |
| `apps`              | signal-desktop, bambu-studio (AUR)                        | home-manager signal-desktop + bambu-studio                             |
| `hardware/kyi_ws`  | intel-ucode, nvidia-open(+utils, lib32), egl-wayland         | the kyi-ws `hardware-configuration.nix` (NVIDIA open, modeset, modules loaded at boot) |
| `hardware/kyi_nb` | amd-ucode, mesa/vulkan-radeon(+lib32), power-profiles-daemon | the AMD equivalent for kyi-nb                                    |

Note: The project *DankMaterialShell (DMS)* has the new name **Dux** (duxlabs).
The package `dux-shell` contains the `dms` binary and the `dms.service` user unit.
The greeter binary keeps the name `dms-greeter`.
Thus the configuration shows the two names.

## Install a new system (kyi-nb first)

1. Install a minimal Arch Linux. You can use archinstall. Obey these rules:
   - Select systemd-boot as the boot loader.
   - Make the user `kyi`. Add the user to the wheel group. Set a password.
   - Enable NetworkManager. Then the network is available after the boot.
   - Do not install more software. decman installs all other software.
2. Start the system. Log in as `kyi` on the TTY.

   Note: The login starts your systemd user instance. decman must have this
   instance to enable the `dms.service` and `dsearch.service` user units.
3. Clone this repository. Then install decman from the AUR:

   ```sh
   sudo pacman -S --needed git base-devel
   git clone <this-repo> ~/Source/dotfiles
   git clone https://aur.archlinux.org/decman.git /tmp/decman
   cd /tmp/decman && makepkg -si
   ```

4. Apply the configuration:

   ```sh
    sudo decman --source ~/Source/dotfiles/kyi-nb.py
   ```

   Note: For the runs that follow, the command `sudo decman` is sufficient.
5. Do a restart. greetd starts the Dux greeter. The greeter starts niri and
   the Dux Shell.
6. Optional: After the first login, do `dms-greeter sync` one time. This
   command copies your shell theme and wallpaper to the login screen.

For kyi-ws, do the same procedure with `kyi-ws.py`.

## Important data

- **CAUTION: decman removes the packages that are not in the configuration.**
  The pacman and AUR plugins make the set of installed packages the same as
  this configuration. decman removes the other packages or makes them
  dependencies. Do not install new software with `pacman -S`. Add the new
  software to a module. Examine the decman plan before each run continues.
- decman builds the AUR packages in a chroot in `/tmp/decman/build`. If
  `/tmp` is a tmpfs, make sure that `/tmp` has a minimum of 6 GB of free
  space.
- The installer prepares the boot loader (systemd-boot), the disk layout, and
  the initramfs. decman does not control these items.
- decman can enable the user units (`dms.service`, `dsearch.service`,
  pipewire) only when the systemd user instance of `kyi` operates. Run decman
  from a session in which `kyi` is logged in.
- The files `files/niri/dms/*.kdl` are copies of files that DMS made. These
  files also could not change on NixOS (read-only store symlinks). Each
  decman run writes these files again. Thus the changes from the DMS settings
  UI (for example, the dynamic theme colors or the display layout) are lost.
  If DMS must control these files: remove them from `files/niri/dms/` and
  remove the `outputs_kdl` file from `modules/niri.py`.
- sshd accepts only public keys (`files/ssh/10-key-only.conf` turns off
  password logins). `files/ssh/authorized_keys` holds the public keys that
  may log in to kyi-ws as `kyi` (currently kyi-nb's key). To allow
  another machine, append its public key to this file and run decman on kyi-ws. Do not lock yourself out: add the key before you remove another.
- The file `dms/outputs.kdl` contains the monitor layout. Each machine has
  its own version: `files/niri/outputs-kyi-ws.kdl` and
  `files/niri/outputs-kyi-nb.kdl`.

## Intentional differences from the NixOS configuration

- `environment.sessionVariables.XDG_CONFIG_HOME = "$HOME/.config"` — removed.
  This value is the XDG default.
- `programs.steam.remotePlay.openFirewall` — a standard Arch installation has
  no firewall. There are no ports to open.
- The line `spawn-at-startup "waybar"` stays in `files/niri/config.kdl` as it
  was. waybar is not installed (it was also not installed on NixOS). The
  command has no effect. You can remove the line.
- The hostnames are `kyi-ws` and `kyi-nb`, not `nixos`. A new hostname
  becomes effective after a restart.
- The static network profile is applicable to all wired interfaces, not only
  to `eth0`. Arch Linux uses predictable interface names.
