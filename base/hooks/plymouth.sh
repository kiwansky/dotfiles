#!/bin/bash
set -euo pipefail

# Add plymouth module to mkinitcpio HOOKS array, right before encrypt
if ! grep -q 'HOOKS=.*plymouth' /etc/mkinitcpio.conf; then
    sudo sed -i 's/\(HOOKS=.*\)encrypt/\1plymouth encrypt/' /etc/mkinitcpio.conf
fi

# Append 'quiet splash' to all boot loader entries if not already present
for entry in /boot/loader/entries/*.conf; do
    if ! grep -q 'quiet splash' "$entry"; then
        sudo sed -i '/^options / s/$/ quiet splash/' "$entry"
    fi
done

# Set boot loader timeout to 0 for seamless boot
sudo sed -i 's/^timeout .*/timeout 0/' /boot/loader/loader.conf

# Regenerate initramfs
sudo mkinitcpio --allpresets
