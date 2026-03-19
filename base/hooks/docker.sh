#!/bin/bash
set -euo pipefail

# Enable and start the docker service
sudo systemctl enable --now docker

# Add current user to the docker group
sudo usermod -aG docker "$USER"
