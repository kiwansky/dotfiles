#!/bin/bash
set -euo pipefail

# Enable the dms user service
systemctl --user enable dms

# Set the profile image
dms ipc call profile setImage "$HOME/Pictures/profile.jpg"
