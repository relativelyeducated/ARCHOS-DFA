# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T18:57:16.944000
# Context: Ah, got it—thanks for clarifying! The Samsung 990 PRO is indeed a beast of an NVMe SSD, and the 2TB model has a **total raw capacity of ~1.818 TiB** (1,863,000,000,000 bytes, or 2,000,000,000,000 byte...

sudo cryptsetup luksFormat /dev/nvme0n1p3    # Set a strong passphrase (twice)
sudo cryptsetup luksOpen /dev/nvme0n1p3 cryptlvm  # Unlock it (enter passphrase)