#!/bin/bash
# Build script for NovaOS, a Debian-based Linux distribution.
#
# Run this on Debian 12 (or inside a debian:bookworm container) with internet
# access and root rights. It downloads several hundred MB of Debian packages.
#
#   apt-get update
#   apt-get install -y live-build debootstrap squashfs-tools xorriso \
#       syslinux syslinux-common isolinux syslinux-utils grub-efi-amd64-bin \
#       grub-pc-bin mtools dosfstools cpio zip
#   ./build.sh
#
# Output: novaos-1.0-amd64.iso (boots as a live system, BIOS and UEFI)

set -e

DIST="bookworm"          # Debian 12
ARCH="amd64"
ISO_NAME="novaos-1.0-${ARCH}.iso"

SUDO=""
if [ "$(id -u)" -ne 0 ]; then SUDO="sudo"; fi

echo "=== NovaOS build starting (Debian ${DIST}, ${ARCH}) ==="

if ! command -v lb >/dev/null 2>&1; then
    echo "ERROR: live-build is not installed. Run: apt-get install -y live-build debootstrap"
    exit 1
fi

# Clean leftovers from a previous build (keeps config/ intact)
$SUDO lb clean || true

$SUDO lb config \
    --distribution "${DIST}" \
    --archive-areas "main contrib non-free-firmware" \
    --architectures "${ARCH}" \
    --binary-images iso-hybrid \
    --debian-installer none \
    --iso-application "NovaOS" \
    --iso-publisher "NovaOS Project" \
    --iso-volume "NovaOS 1.0" \
    --bootappend-live "boot=live components quiet splash"

# 20-60+ minutes depending on connection and CPU
$SUDO lb build

if [ -f live-image-${ARCH}.hybrid.iso ]; then
    $SUDO mv live-image-${ARCH}.hybrid.iso "${ISO_NAME}"
    echo "=== Build complete: ${ISO_NAME} ==="
else
    echo "Build finished but the expected ISO was not found. Check the log above."
    exit 1
fi
