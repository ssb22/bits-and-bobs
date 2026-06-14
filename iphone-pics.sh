#!/bin/bash

# Move the camera roll off of an iPhone to make space
# (c) Silas S. Brown 2026, License: Apache 2
# (I did say "public domain no warranty" but apparently
# some corporate offices don't trust that.  Apache 2 lets
# them know I don't have a silly patent up my sleeve that
# I'd try to enforce, so their policy might accept it more
# easily if you need to use this at work.)

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
