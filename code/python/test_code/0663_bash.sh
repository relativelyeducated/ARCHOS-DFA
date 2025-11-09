# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T19:05:00.971000
# Context: It seems like you’re back at the `fdisk` prompt after running `sudo fdisk /dev/nvme0n1`, and you’ve asked for "command options." Based on your previous message, you’ve already seen the help menu, whic...

sudo mkfs.fat -F32 /dev/nvme0n1p1    # Format EFI
sudo mkfs.ext4 /dev/nvme0n1p2        # Format Boot
sudo pvcreate /dev/nvme0n1p3         # Prep LVM Physical Volume