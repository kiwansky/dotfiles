# Dotfiles deployment Makefile
# Deploys packages, configs, and hooks for base + host-specific layers.

USER := $(shell whoami)
HOST := $(shell cat /etc/hostname)

.PHONY: all deps pkgs aur update cfg hooks

# Default target: run all deployment steps in order.
all: deps pkgs aur cfg hooks

# --------------------------------------------------------------------------
# deps — Install required dependencies (paru) from the AUR manually.
# Clones, builds, installs, and cleans up.
# --------------------------------------------------------------------------
deps:
	@git submodule update --init --recursive
	@if ! command -v paru >/dev/null 2>&1; then \
		echo "Installing paru..."; \
		git clone https://aur.archlinux.org/paru.git /tmp/paru-build; \
		cd /tmp/paru-build && makepkg -sirc --noconfirm; \
		rm -rf /tmp/paru-build; \
		echo "paru installed."; \
	else \
		echo "paru already installed."; \
	fi

# --------------------------------------------------------------------------
# pkgs — Install official repo packages via pacman.
# Reads from base/packages and $(HOST)/packages, deduplicates, then installs.
# --------------------------------------------------------------------------
pkgs:
	@PKGS=""; \
	for f in base/packages $(HOST)/packages; do \
		[ -f "$$f" ] && PKGS="$$PKGS $$(cat "$$f")"; \
	done; \
	PKGS=$$(echo "$$PKGS" | tr ' ' '\n' | sed '/^$$/d' | sort -u | tr '\n' ' '); \
	if [ -n "$$PKGS" ]; then \
		echo "Installing packages: $$PKGS"; \
		sudo pacman -S --needed --noconfirm $$PKGS; \
	else \
		echo "No packages to install."; \
	fi

# --------------------------------------------------------------------------
# aur — Install AUR packages via paru.
# Reads from base/aur-packages and $(HOST)/aur-packages, deduplicates.
# --------------------------------------------------------------------------
aur:
	@PKGS=""; \
	for f in base/aur-packages $(HOST)/aur-packages; do \
		[ -f "$$f" ] && PKGS="$$PKGS $$(cat "$$f")"; \
	done; \
	PKGS=$$(echo "$$PKGS" | tr ' ' '\n' | sed '/^$$/d' | sort -u | tr '\n' ' '); \
	if [ -n "$$PKGS" ]; then \
		echo "Installing AUR packages: $$PKGS"; \
		paru -S --needed --skipreview $$PKGS; \
	else \
		echo "No AUR packages to install."; \
	fi

# --------------------------------------------------------------------------
# update — Update all installed packages (official repos + AUR) via paru.
# --------------------------------------------------------------------------
update:
	@echo "Updating all packages (official repos + AUR)..."
	@paru -Syu

# --------------------------------------------------------------------------
# cfg — Deploy config files to their absolute paths on the filesystem.
# - config/ mirrors /  (e.g. config/etc/pacman.conf -> /etc/pacman.conf)
# - {{USER}} in directory names is replaced with $(USER).
# - Files under /home/$(USER) are copied as the current user; others use sudo.
# - Base layer is applied first, then host layer overwrites where applicable.
# - .gitkeep and .clean files are skipped.
# - If a directory contains a .clean file, all existing files in the
#   corresponding host directory are removed before copying.
# --------------------------------------------------------------------------
cfg:
	@for layer in base $(HOST); do \
		CFG_DIR="$$layer/config"; \
		[ -d "$$CFG_DIR" ] || continue; \
		find "$$CFG_DIR" -name '.clean' | while read -r clean; do \
			CLEAN_DIR=$$(dirname "$$clean"); \
			REL=$${CLEAN_DIR#$$CFG_DIR/}; \
			TARGET_DIR="/$$REL"; \
			TARGET_DIR=$$(echo "$$TARGET_DIR" | sed 's|{{USER}}|$(USER)|g'); \
			case "$$TARGET_DIR" in \
				/home/$(USER)/*) \
					if [ -d "$$TARGET_DIR" ]; then \
						echo "Cleaning $$TARGET_DIR"; \
						find "$$TARGET_DIR" -mindepth 1 -depth -delete; \
					fi; \
					;; \
				*) \
					if [ -d "$$TARGET_DIR" ]; then \
						echo "Cleaning $$TARGET_DIR (sudo)"; \
						sudo find "$$TARGET_DIR" -mindepth 1 -depth -delete; \
					fi; \
					;; \
			esac; \
		done; \
		find "$$CFG_DIR" -type f ! -name '.gitkeep' ! -name '.clean' | while read -r src; do \
			REL=$${src#$$CFG_DIR/}; \
			TARGET="/$$REL"; \
			TARGET=$$(echo "$$TARGET" | sed 's|{{USER}}|$(USER)|g'); \
			DIR=$$(dirname "$$TARGET"); \
			case "$$TARGET" in \
				/home/$(USER)/*) \
					mkdir -p "$$DIR"; \
					cp "$$src" "$$TARGET"; \
					echo "$$src -> $$TARGET"; \
					;; \
				*) \
					sudo mkdir -p "$$DIR"; \
					sudo cp "$$src" "$$TARGET"; \
					echo "$$src -> $$TARGET (sudo)"; \
					;; \
			esac; \
		done; \
	done

# --------------------------------------------------------------------------
# hooks — Run hook scripts for every installed package.
# Collects all package names from both layers, deduplicates.
# For each package, runs base/hooks/<pkg>.sh then $(HOST)/hooks/<pkg>.sh.
# --------------------------------------------------------------------------
hooks:
	@PKGS=""; \
	for f in base/packages base/aur-packages $(HOST)/packages $(HOST)/aur-packages; do \
		[ -f "$$f" ] && PKGS="$$PKGS $$(cat "$$f")"; \
	done; \
	PKGS=$$(echo "$$PKGS" | tr ' ' '\n' | sed '/^$$/d' | sort -u); \
	for pkg in $$PKGS; do \
		for layer in base $(HOST); do \
			HOOK="$$layer/hooks/$$pkg.sh"; \
			if [ -f "$$HOOK" ]; then \
				echo "Running hook: $$HOOK"; \
				bash "$$HOOK" || echo "WARNING: $$HOOK failed with exit code $$?"; \
			fi; \
		done; \
	done
