# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T19:03:17.481000
# Context: It sounds like you might have encountered an issue when running the `fdisk` command, and you're seeing just a `command` prompt or an error, which could mean the command didn't start properly or you’re...

sudo mkfs.fat -F32 /dev/nvme0n1p1    # EFI
sudo mkfs.ext4 /dev/nvme0n1p2        # Boot
sudo pvcreate /dev/nvme0n1p3         # LVM PV