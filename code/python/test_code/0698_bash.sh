# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T21:19:26.709000
# Context: ### Fixing Your Kubuntu Install and NVIDIA Driver Setup

Congrats on getting into Kubuntu 24.04! From the screenshot, your system is correctly detected as Kubuntu 24.04 with KDE Plasma 5.27.12, Kernel...

sudo pvcreate /dev/nvme0n1p3  # LVM partition
   sudo vgcreate kubuntu-vg /dev/nvme0n1p3
   sudo lvcreate -L 50G -n root kubuntu-vg
   sudo lvcreate -L 8G -n swap kubuntu-vg
   sudo lvcreate -l 100%FREE -n home kubuntu-vg
   sudo mkfs.ext4 /dev/kubuntu-vg/root
   sudo mkfs.ext4 /dev/kubuntu-vg/home
   sudo mkswap /dev/kubuntu-vg/swap
   sudo mkfs.ext4 /dev/nvme0n1p4  # New /boot partition (if created as p4)