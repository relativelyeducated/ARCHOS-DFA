# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T21:19:26.709000
# Context: ### Fixing Your Kubuntu Install and NVIDIA Driver Setup

Congrats on getting into Kubuntu 24.04! From the screenshot, your system is correctly detected as Kubuntu 24.04 with KDE Plasma 5.27.12, Kernel...

sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nouveau.conf"
   sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nouveau.conf"
   sudo update-initramfs -u