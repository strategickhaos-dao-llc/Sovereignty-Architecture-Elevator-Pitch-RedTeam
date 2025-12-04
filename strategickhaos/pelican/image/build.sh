#!/usr/bin/env bash
set -e

# Sovereign Swarm Pelican Image Builder
# Creates bootable edge node image for ARM64 devices

IMG=swarm-pelican.img
SIZE=4G
WORK_DIR=work

echo "[*] Building Sovereign Swarm Pelican image..."

# Create work directory
mkdir -p ${WORK_DIR}/mnt

# Create sparse image file
echo "[*] Creating ${SIZE} image file..."
truncate -s ${SIZE} ${IMG}

# Create partitions
echo "[*] Creating partitions..."
parted -s ${IMG} mklabel gpt
parted -s ${IMG} mkpart primary fat32 1MiB 256MiB
parted -s ${IMG} mkpart primary ext4 256MiB 100%
parted -s ${IMG} set 1 boot on

# Setup loop device
LOOP=$(losetup --show -f -P ${IMG})
echo "[*] Loop device: ${LOOP}"

# Format partitions
mkfs.vfat -F 32 -n BOOT ${LOOP}p1
mkfs.ext4 -L ROOT ${LOOP}p2

# Mount partitions
mount ${LOOP}p2 ${WORK_DIR}/mnt
mkdir -p ${WORK_DIR}/mnt/boot
mount ${LOOP}p1 ${WORK_DIR}/mnt/boot

# Extract base system (placeholder - use debootstrap or pi-gen in production)
echo "[*] Installing base system..."
# debootstrap --arch=arm64 bookworm ${WORK_DIR}/mnt http://deb.debian.org/debian

# Copy cloud-init configuration
echo "[*] Installing cloud-init configuration..."
mkdir -p ${WORK_DIR}/mnt/etc/cloud/cloud.cfg.d
cp cloud-init.yaml ${WORK_DIR}/mnt/etc/cloud/cloud.cfg.d/99-swarm.cfg

# Copy systemd services
echo "[*] Installing systemd services..."
cp -r systemd/* ${WORK_DIR}/mnt/etc/systemd/system/

# Enable services
# systemctl --root=${WORK_DIR}/mnt enable swarmsgd wg-quick@wg0 syncthing

# Cleanup
echo "[*] Cleaning up..."
umount ${WORK_DIR}/mnt/boot
umount ${WORK_DIR}/mnt
losetup -d ${LOOP}

echo "[+] Pelican image built: ${IMG}"
echo "[+] Flash with: dd if=${IMG} of=/dev/sdX bs=4M status=progress"
