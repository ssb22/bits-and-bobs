#!/bin/sh

# FreeBSD setup script
# for Mac VirtualBox with screen magnification
# Silas S. Brown 2020-2021, public domain

# Tested on Mac OS 10.7.5, VirtualBox 4.3.4 & 4.3.40
# We install 2 Firefox profiles (one with CSS, one w/out)
# because old Mac OS X can't run latest browsers.

export User=ssb22

# Setup:
# https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.2/FreeBSD-12.2-RELEASE-amd64-bootonly.iso.xz
# 8G virtual hdd, 2G RAM (1G insufficient for Firefox on some websites)
# 3D acceleration = enabled
# shared clipboard = bidirectional
# NAT port forwarding = 22022 to 22
# Install / (Dvorak or whatever keymap) / Continue / hostname / deselect optional components / network (dhcp=y ipv6=n resolver=default) / mirror (e.g. UK2) / auto, entire disk, mbr, (if on SSD suggest delete swap and expand main partition) / root pwd / time zone / (no services, usrs) / reboot

# Then run:
# curl https://raw.githubusercontent.com/ssb22/bits-and-bobs/master/freebsd-setup.sh > freebsd-setup.sh && chmod +x freebsd-setup.sh && ./freebsd-setup.sh

# Notes on Zoom Cloud Meetings (does NOT work well) :
# with Virtualbox Oracle Extensions installed on 4.3.40,
# at runtime: menubar Devices / Webcams / (select one)
#  (do not just add the USB device on USB 2: that works
#   for audio but not for video, ditto in Debian 10 if
#   it's a device like 0ac8:3420),
#pkg install v4l-utils
#echo 'cuse_load="YES"' >> /boot/loader.conf
#echo 'webcamd_enable="YES"' >> /etc/rc.conf
#service webcamd start
# then in Firefox with no CSS, go to
# https://zoom.us/j/<meeting ID goes here>
# (tries to download Zoom client: scroll down to reveal
# a link to join from browser instead), CAPTCHA,
# (as of 2021-01) worked with both audio and video,
# BUT cpu (2.3GHz i5) cannot keep up with either
# (and the Firefox tab periodically crashes).
# Increase 1 CPU to 2 CPUs = no noticeable improvement.
# Native Zoom client on a separate Debian 10 VM (2 CPU,
# with 'apt install lxqt-panel' from minimum, ~3G HDD)
# managed to broadcast 4 to 5 frames/sec with no audio.
# Zoom say 2.5GHz hard-minimum (before virtualisation),
# and it's not documented what accelerations they use,
# so old i5 at 2.3GHz with virtualisation is not enough.

# TODO: how much of the install can we do from pkg only? or are /usr/ports really essential?  (rm after = save 1.7G)
# TODO: script to ssh in and start browser on a file/url via /mac ?

cd
cat > auto-ask-responses.txt <<EOF
inodes-ok|y
configure-firewall|n
latest-packages|n
update-system|n
disable-write-cache|n
build-from-source|n
desktop-selection|7
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
pkg install -y wget joe ncdu ca_root_nss desktop-installer bsdstats firefox fusefs-sshfs xclip py37-xlib
desktop-installer
pkg remove cabextract e2fsprogs exfat-utils fusefs-ntfs fusefs-simple-mtpfs libgphoto2 poppler-data py37-cairo py37-dbus py37-qt5-core py37-sip py37-tkinter pydbus-common pygobject3-common qscintilla2-qt5 tk86 webcamd zenity
pkg install virtualbox-ose-additions-legacy ; pkg remove virtualbox-ose-additions # (Mar2021 main package went to version 6; seems we need version 5 or older for VirtualBox version 4)
rm -rf /usr/ports/*/*/work /var/cache/pkg/*.txz

mkdir /mac
echo 10.0.2.2 mac >> /etc/hosts
mkdir -p .ssh
ssh-keygen -f .ssh/id_rsa -N ""
(echo Host mac;echo User $User) > .ssh/config
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
chmod +x /usr/local/share/desktop-installer/ICEWM/xinitrc
mkdir -p .config/autostart .icewm .config/fontconfig
cat > .config/fontconfig/fonts.conf <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
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
# firefox -CreateProfile is not available on FreeBSD version, but we can do it ourselves
mkdir -p .mozilla/firefox/25.CSS25/chrome
cd .mozilla/firefox/25.CSS25/chrome
ln -s 25.css userContent.css
cd
cat > .mozilla/firefox/25.CSS25/prefs.js <<EOF
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.newtabpage.enabled", false);
EOF
mkdir -p .mozilla/firefox/0.default
cat > .mozilla/firefox/0.default/prefs.js <<EOF
user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.newtabpage.enabled", false);
EOF
cat > .mozilla/firefox/profiles.ini <<EOF
[Profile1]
Name=CSS25
IsRelative=1
Path=25.CSS25

[Profile0]
Name=default
IsRelative=1
Path=0.default
Default=1
EOF
cat > .icewm/toolbar <<EOF
prog " 0 " - firefox -P default
prog " 25 " - firefox -P CSS25
prog " sh " - /usr/local/bin/xterm
EOF
echo 'WorkspaceNames=""' > .icewm/preferences # save taskbar space + accidental clicks; doesn't seem possible to disable workspaces altogether though

wget https://raw.githubusercontent.com/python-xlib/python-xlib/master/examples/xfixes-selection-notify.py
sed -ie "s/print('SetSelectionOwner.*/if not e.owner.get_wm_name()=='main': raise SystemExit/" xfixes-selection-notify.py
mv xfixes-selection-notify.py /usr/local/lib/xfsn.py
cat >.icewm/startup <<EOF
#!/bin/sh
sshfs mac:/ /mac
xrdb + .Xresources
setxkbmap dvorak
VBoxClient --clipboard # NOT -all (a kernel mismatch can stop mouse working after --vmsvga, which doesn't work anyway on our setup)
cd .mozilla/firefox/25.CSS25/chrome && wget -N http://ssb22.user.srcf.net/css/25.css ; cd
firefox -P CSS25 &
xsetroot -solid darkblue # .icewm/preferences DesktopBackgroundImage="" doesn't work ?

# Work around bug copying browser text to host clipboard
# - it seems host won't take it from CLIPBOARD set by browser, but will take it from CLIPBOARD set by xclip.
# So we watch for SetSelectionOwnerNotify on CLIPBOARD,
# and then copy PRIMARY (which should be the same) to
# CLIPBOARD via xclip.
# (Our patch to xfixes-selection-notify.py causes it to
# exit only if owner is not set by 'main' i.e. the host.
# This avoids an unwanted side-effect of reacting to any
# change in clipboard on the host side also, when vbox
# copies host to guest: if both plain text and another
# format like RTF are available on the host side, we
# probably don't want the vbox to take over as owner and
# make it plain-text only.)
while true ; do
  python3.7 /usr/local/lib/xfsn.py CLIPBOARD 2>/dev/null >/dev/null
  xclip -o | xclip -i -selection clipboard
done
EOF
chmod +x .icewm/startup
wget https://raw.githubusercontent.com/ssb22/config/master/.Xresources

echo "Use auto-update-system for FreeBSD 12 security patches" # until EOL of FreeBSD 12; may not have enough disk space to upgrade to 13, which requires reboots
