#!/bin/bash
set -euo pipefail
shopt -s nullglob

# Add plymouth module to mkinitcpio HOOKS array, right before encrypt
if ! grep -q 'HOOKS=.*plymouth' /etc/mkinitcpio.conf; then
    sudo sed -i 's/\(HOOKS=.*\)encrypt/\1plymouth encrypt/' /etc/mkinitcpio.conf
fi

# Append 'quiet splash' to any systemd-boot loader entries (traditional split initramfs)
for entry in /boot/loader/entries/*.conf; do
    if ! grep -q 'quiet splash' "$entry"; then
        sudo sed -i '/^options / s/$/ quiet splash/' "$entry"
    fi
done

# For unified kernel images, the cmdline is baked in at build time from
# /etc/kernel/cmdline + /etc/cmdline.d/*.conf. Drop in 'quiet splash' if any
# mkinitcpio preset is configured to build a UKI.
presets=(/etc/mkinitcpio.d/*.preset)
if (( ${#presets[@]} > 0 )) && grep -qE '^[[:space:]]*default_uki=' "${presets[@]}"; then
    dropin=/etc/cmdline.d/10-plymouth.conf
    if [[ ! -f $dropin ]] || ! grep -q 'quiet splash' "$dropin"; then
        sudo install -d -m 0755 /etc/cmdline.d
        echo 'quiet splash' | sudo tee -a "$dropin" >/dev/null
    fi
fi

# Set boot loader timeout to 0 for seamless boot (systemd-boot only)
if [[ -f /boot/loader/loader.conf ]]; then
    sudo sed -i 's/^timeout .*/timeout 0/' /boot/loader/loader.conf
fi

# Regenerate initramfs (and UKIs, for presets with default_uki=)
sudo mkinitcpio --allpresets
