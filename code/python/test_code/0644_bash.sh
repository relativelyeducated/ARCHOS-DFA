# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T18:57:16.944000
# Context: Ah, got it—thanks for clarifying! The Samsung 990 PRO is indeed a beast of an NVMe SSD, and the 2TB model has a **total raw capacity of ~1.818 TiB** (1,863,000,000,000 bytes, or 2,000,000,000,000 byte...

sudo vgcreate kubuntu-vg /dev/nvme0n1p3    # Volume Group (your full ~1.8TiB space)
sudo lvcreate -L 50G -n root kubuntu-vg   # Root LV: 50GB (plenty for system)
sudo lvcreate -L 8G  -n swap kubuntu-vg   # Swap LV: 8GB (adjust to your RAM size, e.g., 16G if 16GB RAM)
sudo lvcreate -l 100%FREE -n home kubuntu-vg # Home LV: All remaining (~1.74TiB—huge for files!)