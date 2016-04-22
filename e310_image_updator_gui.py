#!/usr/bin/env python

# Tool to help write new image for E310/312
# Scans connected drives and lists them to user
# Complete Tool Should:
#   * List drives to help user find memory card
#   * Format memory card
#   * Write image to memory card (dd)

import subprocess

# Get output of lsblk
lsblk = subprocess.Popen(['lsblk'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# Strip out lines that are 'disk' types (not partitions)
blockdevs = [line.strip() for line in lsblk.stdout if 'disk' in line]

returncode = lsblk.wait()

if returncode:
    print("Something happened!")

for devices in blockdevs:
    print devices


