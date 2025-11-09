# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T21:37:57.414000
# Context: Awesome—thanks for the output! It’s 10:37 PM EDT on October 20, 2025, and the `cat /etc/os-release` result shows you’re actually running **Ubuntu 24.04.3 LTS (Noble Numbat)**, not Arch Linux as the ho...

lsblk  # Find USB (e.g., /dev/sdb1)
    sudo mkdir /mnt/usb && sudo mount /dev/sdb1 /mnt/usb  # Replace sdb1
    cd /mnt/usb