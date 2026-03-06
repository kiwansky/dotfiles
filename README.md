# Dotfiles

A layered dotfiles system for Arch Linux that manages packages, AUR packages, configuration files, and post-install hooks across multiple machines.

## Requirements

- Minimal Arch Linux installation
- `git` installed
- `networkmanager` installed and configured

## How It Works

The repository uses a two-layer system:

1. **Base layer** (`base/`) -- Applied to every system.
2. **Host layer** (`<hostname>/`) -- Applied only when the machine's hostname matches the directory name. Detected automatically at runtime via `/etc/hostname`.

The base layer is always processed first. The host layer extends it, and host-specific config files overwrite base files at the same path.

## Directory Structure

```
dotfiles/
├── Makefile
├── base/
│   ├── packages
│   ├── aur-packages
│   ├── config/
│   │   ├── etc/
│   │   ├── home/
│   │   │   └── {{USER}}/
│   │   └── usr/
│   └── hooks/
│       ├── plymouth.sh
│       └── ...
└── <hostname>/
    ├── packages
    ├── aur-packages
    ├── config/
    └── hooks/
```

### Package Files

`packages` and `aur-packages` are plain text files with one package name per line. Packages from both layers are combined and deduplicated before installation.

### Configuration

The `config/` directory mirrors the root filesystem (`/`). Files are deployed to their corresponding absolute paths:

- `config/etc/pacman.conf` deploys to `/etc/pacman.conf`
- `config/home/{{USER}}/.zshrc` deploys to `/home/<your-username>/.zshrc`

The `{{USER}}` template variable is replaced with the current username at deploy time.

Files targeting `/home/$USER/` are copied as the current user. All other paths (e.g. `/etc/`, `/usr/`) are copied using `sudo`.

### Hooks

Hook scripts live in `hooks/` and are named `<package-name>.sh`. They run unconditionally for every listed package -- even if the package was already installed. Base hooks run before host hooks.

## Makefile Targets

| Target | Description |
|---|---|
| `make` | Runs all targets in order: deps, pkgs, aur, cfg, hooks |
| `make deps` | Initializes git submodules and installs paru from the AUR |
| `make pkgs` | Installs official repo packages via `pacman` |
| `make aur` | Installs AUR packages via `paru` |
| `make cfg` | Deploys configuration files to the filesystem |
| `make hooks` | Executes post-install hook scripts |

## Quick Start

```bash
git clone <repo-url> ~/dotfiles
cd ~/dotfiles
make
```

## Adding a New Host

1. Create a directory named after the machine's hostname (output of `cat /etc/hostname`).
2. Add any of the following files as needed: `packages`, `aur-packages`, `config/`, `hooks/`.
3. The host layer will be picked up automatically on the next run.
