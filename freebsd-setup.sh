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
pkg install -y wget subversion joe ca_root_nss desktop-installer firefox otter-browser
desktop-installer
rm -rf /usr/ports/*/*/work /var/cache/pkg/*.txz

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
otter-browser &
EOF
chmod +x /root/.x-start
wget https://raw.githubusercontent.com/ssb22/config/master/.Xresources

wget http://ssb22.user.srcf.net/css/25.css
mkdir -p .config/otter/keyboard
cat > .config/otter/otter.conf <<EOF
[Browser]
HomePage=http://ssb22.user.srcf.net/
Migrations=keyboardAndMouseProfilesIniToJson, optionsRename, searchEnginesStorage, sessionsIniToJson
StartupBehavior=startHomePage
[Content]
UserStyleSheet=/root/25.css
EOF
cat > .config/otter/keyboard/default.json <<EOF
// Title: Default
// Description: Default configuration
// Type: keyboard-profile
// Take out 'space = fast forward',
// we want space to just page down
// TODO: BROKEN : results in NO shortcuts being read
[{"actions":[
    {"action": "NewTab", "shortcuts":["Ctrl+T"]},
    {"action": "NewTabPrivate","shortcuts":["Ctrl+Shift+P"]},
    {"action": "NewWindow","shortcuts":["Ctrl+N"]},
    {"action": "NewWindowPrivate","shortcuts": ["Ctrl+Shiftt+N"]},
    {"action": "Open","shortcuts": ["Ctrl+O"]},
    {"action": "Save","shortcuts": ["Ctrl+S"]},
    {"action": "CloseTab","shortcuts": ["Ctrl+W"]},
    {"action": "ReopenTab","shortcuts": ["Ctrl+Shift+T"]},
    {"action": "ReopenWindow","shortcuts": ["Ctrl+Shift+N"]},
    {"action": "FillPassword","shortcuts": ["Ctrl+Return"]},
    {"action": "Reload","shortcuts": ["Ctrl+R"]},
    {"action": "ReloadAndBypassCache","shortcuts": ["Ctrl+Shift+R"]},
    {"action": "Undo","shortcuts": ["Ctrl+Z"]},
    {"action": "Redo","shortcuts": ["Ctrl+Shift+Z"]},
    {"action": "Cut","shortcuts": ["Ctrl+X"]},
    {"action": "Paste","shortcuts": ["Ctrl+V"]},
    {"action": "Delete","shortcuts": ["Del"]},
    {"action": "SelectAll","shortcuts": ["Ctrl+A"]},
    {"action": "Find","shortcuts": ["Ctrl+F"]},
    {"action": "FindNext","shortcuts": ["Ctrl+G"]},
    {"action": "QuickFind","shortcuts": ["/"]},
    {"action": "ZoomIn","shortcuts": ["Ctrl++","Ctrl+="]},
    {"action": "ZoomOut","shortcuts": ["Ctrl+-"]},
    {"action": "ZoomOriginal","shortcuts": ["Ctrl+0"]},
    {"action": "Print","shortcuts": ["Ctrl+P"]},
    {"action": "Bookmarks","shortcuts": ["Ctrl+Shift+B"]},
    {"action": "ViewSource","shortcuts": ["Ctrl+U"]},
    {"action": "InspectPage","shortcuts": ["Ctrl+Shift+I"]},
    {"action": "FullScreen","shortcuts": ["F11"]},
    {"action": "History","shortcuts": ["Ctrl+H"]},
    {"action": "Exit","shortcuts": ["Ctrl+Q"]}],
  "context": "Generic"
 }
]
EOF

echo 'sshd_enable="YES"' >> /etc/rc.conf
