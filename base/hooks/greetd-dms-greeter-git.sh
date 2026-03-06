#!/bin/bash
set -euo pipefail

# Enable and sync the DMS greeter for greetd
dms greeter enable
dms greeter sync
