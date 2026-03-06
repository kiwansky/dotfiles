#!/bin/bash
set -euo pipefail

# Enable the dms user service
systemctl --user enable dms
