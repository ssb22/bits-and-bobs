#!/bin/sh

# FreeBSD setup script
# for Mac VirtualBox with screen magnification
# Silas S. Brown 2020, public domain

# Setup:
# https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-bootonly.iso.xz
# 8G virtual hdd
# Install / (Dvorak or whatever keymap) / Continue / hostname / deselect optional components / network (dhcp=y ipv6=n resolver=default) / mirror (e.g. UK2) / auto, entire disk, mbr, (if on SSD suggest delete swap and expand main partition) / root pwd / time zone / (no services, usrs) / reboot

# curl https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/freebsd-setup.sh > freebsd-setup.sh && chmod +x freebsd-setup.sh && ./freebsd-setup.sh

# TODO: X11 Up arrow pops up screenshot dialogue
# TODO: copy FROM Firefox doesn't go to host
# TODO: Firefox profiles for no css / 0.css / 25.css ?
# TODO: Firefox PDF export ?
# TODO: how much of the install can we do from pkg only? or are /usr/ports really essential?

cd

# Don't do this: it corrupts vbox screen after X11 quits
# echo hw.vga.textmode=0 >> /boot/loader.conf
# echo "vidcontrol -f /usr/share/vt/fonts/terminus-b32.fnt" >> .login
# Not needed if have set at install:
# echo "kbdcontrol -l /usr/share/vt/keymaps/us.dvorak.kbd" >> .login

cat > auto-ask-responses.txt <<EOF
inodes-ok|y
configure-firewall|n
latest-packages|n
update-system|n
disable-write-cache|n
build-from-source|n
desktop-selection|11
install-wireless|n
guest-additions|y
use-moused|y
generate-xorg|y
swcursor|y
edit-xorg|n
forward-x11|y
forward-x11-trusted|n
accept-x11-forward|y
enable-slim|y
EOF
pkg install -y wget subversion joe ca_root_nss desktop-installer firefox
desktop-installer
ln -s /usr/local/bin/bash /bin/bash
# For Dvorak:
# IS needed even if have set at install:
# echo setxkbmap dvorak >> .xinitrc
# TODO: or use .Xmodmap
# TODO: what about SLiM login keyboard layout?
wget https://raw.githubusercontent.com/ssb22/config/master/.Xresources # although doesn't do much for lxqt
