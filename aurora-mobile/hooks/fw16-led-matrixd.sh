#!/bin/bash
set -euo pipefail

# Enable and start the fw16-led-matrixd service
sudo systemctl enable --now fw16-led-matrixd
