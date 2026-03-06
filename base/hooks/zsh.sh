#!/bin/bash
set -euo pipefail

# Change the default shell to zsh for the current user
sudo chsh -s "$(which zsh)" "$USER"
