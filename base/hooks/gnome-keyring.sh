#!/bin/bash
set -euo pipefail

PAM_FILE="/etc/pam.d/greetd"
AUTH_LINE="auth       optional     pam_gnome_keyring.so"
SESSION_LINE="session    optional     pam_gnome_keyring.so auto_start"

# Add pam_gnome_keyring auth entry after the last existing auth line
if ! grep -q 'auth.*pam_gnome_keyring.so' "$PAM_FILE" 2>/dev/null; then
    # Find the last auth line number and insert after it
    last_auth=$(grep -n '^auth' "$PAM_FILE" | tail -1 | cut -d: -f1)
    sudo sed -i "${last_auth}a\\${AUTH_LINE}" "$PAM_FILE"
fi

# Add pam_gnome_keyring session entry after the last existing session line
if ! grep -q 'pam_gnome_keyring.so auto_start' "$PAM_FILE" 2>/dev/null; then
    # Find the last session line number and insert after it
    last_session=$(grep -n '^session' "$PAM_FILE" | tail -1 | cut -d: -f1)
    sudo sed -i "${last_session}a\\${SESSION_LINE}" "$PAM_FILE"
fi
