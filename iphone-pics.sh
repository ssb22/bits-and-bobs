#!/bin/bash

# Move the camera roll off of an iPhone to make space
# Silas S. Brown 2026 - public domain - no warranty

set -e
ifuse /mnt
User="$(stat -c '%U' .)" # in case we're running as root
ThisBatch="$(pwd)/$(date +iphone-%Y-%m-%d)"
mkdir "$ThisBatch"
cd /mnt/DCIM
for Dir in *; do cd "$Dir"
# Move off, rename by timestamp, and lower-case extension
# (We assume we have bash 4+ if we have ifuse)
for File in *; do Date=$(date -r "$File" +%Y-%m-%d_%H-%M-%S 2>/dev/null)
Ext="${File##*.}"; Ext="${Ext,,}"
Dest="$ThisBatch/$Date.$Ext"; counter=1; while [ -e "$Dest" ]; do ((counter++)); Dest="$ThisBatch/$Date_$(printf '%03d' $counter).$Ext"; done
mv -v "$File" "$Dest"; done; cd ..; done
chown -R "$User:$User" "$ThisBatch"
umount /mnt
