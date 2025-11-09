# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T19:13:52.470000
# Context: The "volume out of range +512M" error in `fdisk` typically means that the starting sector or size you specified (+512M for the EFI partition) is outside the valid range for the disk, often due to a mi...

sudo fdisk /dev/nvme0n1