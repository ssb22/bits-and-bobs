#!/bin/sh

# FreeBSD setup script
# for Mac VirtualBox with screen magnification
# Silas S. Brown 2020, public domain

# Setup:
# https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-bootonly.iso.xz
# 8G virtual hdd
# Install / (Dvorak or whatever keymap) / Continue / hostname / deselect optional components / network (dhcp=y ipv6=n resolver=default) / mirror (e.g. UK2) / auto, entire disk, mbr, (if on SSD suggest delete swap and expand main partition) / root pwd / time zone / (no services, usrs) / reboot

# curl https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/freebsd-setup.sh > freebsd-setup.sh && chmod +x freebsd-setup.sh && ./freebsd-setup.sh

# TODO: copy FROM Firefox doesn't go to host, unless go via featherpad or sthg
# TODO: Firefox PDF export ?
# TODO: how much of the install can we do from pkg only? or are /usr/ports really essential?

cd
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
cat >> /usr/local/etc/slim.conf <<EOF
default_user root
auto_login yes
EOF
rm .xinitrc # save confusion (isn't used by slim)
mkdir -p .config/autostart
cat > .config/autostart/script.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name="Random wallpaper"
GenericName="Random wallpaper"
Comment=""
Exec=/root/.x-start
Terminal=false
OnlyShowIn=GNOME
Type=Application
StartupNotify=false
X-GNOME-Autostart=true
EOF

# Work around "up arrow gives Print Screen" bug
# https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=244290
mkdir -p .config/lxqt
cat > .config/lxqt/globalkeyshortcuts.conf <<EOF
[Print.30]
Enabled=false
EOF

cat >/root/.x-start <<EOF
#!/bin/sh
xrdb + .Xresources
setxkbmap dvorak
firefox &
# firefox -P profile
firefox --profile .mozilla/firefox/css0.default &
firefox --profile .mozilla/firefox/css25.default &
firefox --profile .mozilla/firefox/nocss.default &
EOF
# TODO: do we really want the above, or would 'toggle / restart' scripts on the menus be better?  (latter would mean can't use Private Mode so history/autocomplete gets cluttered unless remember to clean up)
# how to set window titles?  (KDE has --caption)
# or use different browser (which would also have the advantage of not requiring the manual step below)
# 'pkg install konqueror' = 116 packages, 720 MB and it doesn't apply CSS files (thankfully 'pkg autoremove' works afterwards)
# 'pkg install midori' gets Midori 9 which doesn't have user-CSS functionality
# (might just need to set up Web Adjuster)
# 'pkg install otter-browser' ok
chmod +x /root/.x-start
wget https://raw.githubusercontent.com/ssb22/config/master/.Xresources
mkdir -p .mozilla/firefox/css0.default/chrome
mkdir -p .mozilla/firefox/css25.default/chrome
mkdir -p .mozilla/firefox/nocss.default
wget -O .mozilla/firefox/css0.default/chrome/userContent.css http://ssb22.user.srcf.net/css/0.css
wget -O .mozilla/firefox/css25.default/chrome/userContent.css http://ssb22.user.srcf.net/css/25.css

# This won't work: you have to do it by hand in about.config:
# mkdir -p .mozilla/firefox/css0.default/datareporting
# echo 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);' > .mozilla/firefox/css0.default/datareporting/session-state.json

echo 'sshd_enable="YES"' >> /etc/rc.conf
