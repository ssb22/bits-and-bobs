#!/bin/sh

# FreeBSD setup script
# for Mac VirtualBox with screen magnification
# Silas S. Brown 2020, public domain

# Tested on Mac OS 10.7.5, VirtualBox 4.3.4
# We install 2 browsers (one with CSS, one without)
# because old Mac OS X can't run latest browsers.

export User=ssb22

# Setup:
# https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-bootonly.iso.xz
# 8G virtual hdd, 2G RAM (1G insufficient for Firefox on some websites)
# 3D acceleration = enabled
# shared clipboard = bidirectional
# NAT port forwarding = 22022 to 22
# Install / (Dvorak or whatever keymap) / Continue / hostname / deselect optional components / network (dhcp=y ipv6=n resolver=default) / mirror (e.g. UK2) / auto, entire disk, mbr, (if on SSD suggest delete swap and expand main partition) / root pwd / time zone / (no services, usrs) / reboot

# curl https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/freebsd-setup.sh > freebsd-setup.sh && chmod +x freebsd-setup.sh && ./freebsd-setup.sh

# TODO: Firefox PDF export ?
# TODO: how much of the install can we do from pkg only? or are /usr/ports really essential?  (rm after = save 1.7G)
# TODO: ssh in and start browser on a file/url via /mac ?

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
pkg install -y wget subversion joe ncdu ca_root_nss desktop-installer bsdstats firefox otter-browser fusefs-sshfs xclip py37-xlib
# subversion might be needed for an 'svn clean' in /usr/ports if your Internet connection glitches during desktop-installer
desktop-installer
rm -rf /usr/ports/*/*/work /var/cache/pkg/*.txz

mkdir /mac
echo 10.0.2.2 mac >> /etc/hosts
mkdir -p .ssh
ssh-keygen -f .ssh/id_rsa -N ""
(echo Host mac;echo User $User) > .ssh/con
fig
cat .ssh/id_rsa.pub | ssh mac 'cat >> .ssh/authorized_keys'
ssh mac cat .ssh/id_rsa.pub > .ssh/authorized_keys
if ! ssh mac cat .ssh/config | grep 'Host freebsd'; then (echo;echo Host freebsd;echo User root;echo HostName localhost;echo Port 22022) | ssh mac 'cat >> .ssh/config'; fi
echo PermitRootLogin yes >> /etc/ssh/sshd_config
echo 'sshd_enable="YES"' >> /etc/rc.conf
ln -s /mac/Users/$User/Downloads

ln -s /usr/local/bin/bash /bin/bash

cat >> /usr/local/etc/slim.conf <<EOF
default_user root
auto_login yes
EOF
rm .xinitrc # save confusion (isn't used by slim)
mkdir -p .config/autostart .config/lxqt .config/fontconfig
cat > .config/fontconfig/fonts.conf <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<!-- created by lxqt-config-appearance (DO NOT EDIT!) -->
<fontconfig>
  <include ignore_missing="yes">conf.d</include>
  <match target="font">
    <edit name="antialias" mode="assign">
      <bool>false</bool>
    </edit>
  </match>
  <match target="font">
    <edit name="rgba" mode="assign">
      <const>rgb</const>
    </edit>
  </match>
  <match target="font">
    <edit name="lcdfilter" mode="assign">
      <const>lcddefault</const>
    </edit>
  </match>
  <match target="font">
    <edit name="hinting" mode="assign">
      <bool>true</bool>
    </edit>
  </match>
  <match target="font">
    <edit name="hintstyle" mode="assign">
      <const>hintslight</const>
    </edit>
  </match>
  <match target="font">
    <edit name="autohint" mode="assign">
      <bool>false</bool>
    </edit>
  </match>
  <match target="pattern">
    <edit name="dpi" mode="assign">
      <double>96</double>
    </edit>
  </match>
</fontconfig>
EOF
cat > .config/lxqt/panel.conf <<EOF
[quicklaunch]
apps\1\desktop=/usr/local/share/applications/firefox.desktop
apps\2\desktop=/usr/local/share/applications/otter-browser.desktop
apps\3\desktop=/usr/local/share/applications/qterminal.desktop
apps\size=3
EOF
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

wget https://raw.githubusercontent.com/python-xlib/python-xlib/master/examples/xfixes-selection-notify.py
sed -ie "s/print('SetSelectionOwner.*/raise SystemExit/" xfixes-selection-notify.py
mv xfixes-selection-notify.py /usr/local/lib/xfsn.py
cat >.x-start <<EOF
#!/bin/sh
sshfs mac:/ /mac
xrdb + .Xresources
setxkbmap dvorak
firefox &
otter-browser &
# Work around bug copying browser text to host clipboard:
while true ; do python3.7 /usr/local/lib/xfsn.py CLIPBOARD 2>/dev/null >/dev/null ; xclip -o | xclip -i -selection clipboard; done
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
[Search]
DefaultSearchEngine=google
EOF
# can't say [Backends] / Web=qtwebengine to get Chrome 80+
# instead of Webkit 602 (Safari 10 equivalent), as Chrome
# stops our user CSS from being applied.  We could do CSS
# in Firefox and non-CSS in Otter, but then would need to
# somehow get it to read a new user.js with
# user_pref("toolkit.legacyUserProfileCustomizations.stylesheets","false");
# could try firefox -CreateProfile CSS25 (but will have to find where it went via profiles.ini) , firefox -P CSS25
cat > .config/otter/keyboard/default.json <<EOF
// Title: Default
// Description: 
// Type: keyboard-profile
// Author: 
// Version: 

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
    {"action": "Copy","shortcuts": ["Ctrl+C"]},
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
