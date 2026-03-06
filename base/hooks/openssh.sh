#!/bin/bash
set -euo pipefail

# Enable and start the sshd service
sudo systemctl enable --now sshd
