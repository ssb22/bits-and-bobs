#!/bin/bash

# Move the camera roll off of an iPhone to make space
# Silas S. Brown 2026 - public domain - no warranty

set -e
ifuse /mnt
User="$(stat -c '%U' .)" # in case we're running as root
ThisBatch="$(pwd)/$(date +iphone-%Y-%m-%d)"
mkdir "$ThisBatch"
cd /mnt/DCIM
for D in *; do cd "$D" && for F in *; do mv -v "$F"  "$ThisBatch/$D-$F";done; cd ..; done
cd "$ThisBatch"
# We assume we have bash 4+ if we have ifuse
for F in *; do counter=1; D=$(date -r "$F" +%Y-%m-%d_%H-%M-%S 2>/dev/null); E="${F##*.}"; E="${E,,}"; N="${D}$(if ! [ $counter == 1 ] ; then printf '_%03d' $counter; fi).${E}"; while [ -e "$N" ]; do ((counter++)); N="${D}_$(printf '%03d' $counter).${E}"; done; mv -v "$F" "$N"; ((counter++)); done
chown -R "$User:$User" .
umount /mnt
