# From: Kubuntu LVM Setup Guide
# Date: 2025-10-20T21:33:16.724000
# Context: Thanks for the update! It’s 10:32 PM EDT on October 20, 2025, and you’ve shared the output from `sudo apt upgrade -y` after running `sudo dpkg --configure -a`. This is great progress on stabilizing yo...

sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nouveau.conf"
    sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nouveau.conf"
    sudo update-initramfs -u
    sudo reboot