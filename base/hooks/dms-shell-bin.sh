#!/bin/bash
set -euo pipefail

# Enable the dms user service
systemctl --user enable dms

# Set the profile image
dms setImage "$HOME/Pictures/profile.jpg"
