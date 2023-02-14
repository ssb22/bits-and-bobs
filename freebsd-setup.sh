#!/bin/sh

# FreeBSD setup script
# for Mac VirtualBox with screen magnification
# Silas S. Brown 2020-2023, public domain

# Tested on Mac OS 10.7.5, VirtualBox 4.3.4
# We install 2 Firefox profiles (one with CSS, one w/out)
# because old Mac OS X can't run latest browsers.

export User=ssb22

# Setup source:
# https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.4/FreeBSD-12.4-RELEASE-amd64-bootonly.iso.xz

# Setup:
# type: FreeBSD (64-bit) (ensure to select 64-bit)
# 2G RAM (1G insufficient for Firefox on some websites)
# 16G virtual hdd (8G was doable in 12.2 but not 12.4)
# System/motherboard/enable I/O APIC
# General/Advanced shared clipboard = bidirectional
# Display: 3D acceleration = enabled
# Network/Advanced/port forwarding: host port 22022 to guest port 22 (leave IPs blank)
# Install / (Dvorak or whatever keymap) / Continue / hostname / deselect optional components / network (dhcp=y ipv6=n resolver=default) / mirror (e.g. UK2) / auto, entire disk, mbr, (if on SSD suggest delete swap and expand main partition) / root pwd / time zone / (no services, usrs) / reboot (rm disc)

# Then run:
# pkg install curl
# curl https://raw.githubusercontent.com/ssb22/bits-and-bobs/%6d%61%73%74%65%72/freebsd-setup.sh > freebsd-setup.sh && chmod +x freebsd-setup.sh && ./freebsd-setup.sh

cd
cat > auto-ask-responses.txt <<EOF
inodes-ok|y
configure-firewall|n
latest-packages|y
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
enable-slim|n
EOF
pkg install -y bsdstats ca_root_nss desktop-installer firefox fusefs-sshfs joe ncdu py39-xlib telegram-desktop wget xclip
desktop-installer
pkg remove cabextract
rm -rf /usr/ports/*/*/work /var/cache/pkg/*.txz

mkdir /mac
echo 10.0.2.2 mac >> /etc/hosts
mkdir -p .ssh
ssh-keygen -f .ssh/id_rsa -N ""
(echo Host mac;echo User $User) > .ssh/config
ssh mac 'cat >> .ssh/authorized_keys' < .ssh/id_rsa.pub
ssh mac cat .ssh/id_rsa.pub > .ssh/authorized_keys
if ! ssh mac cat .ssh/config | grep 'Host freebsd'; then (echo;echo Host freebsd;echo User root;echo HostName localhost;echo Port 22022) | ssh mac 'cat >> .ssh/config'; fi
echo PermitRootLogin yes >> /etc/ssh/sshd_config
echo 'sshd_enable="YES"' >> /etc/rc.conf
ln -s /mac/Users/$User/Downloads

ln -s /usr/local/bin/bash /bin/bash

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

wget https://raw.githubusercontent.com/python-xlib/python-xlib/%6d%61%73%74%65%72/examples/xfixes-selection-notify.py
sed -i '' "s/print('SetSelectionOwner.*/if not e.owner.get_wm_name()=='main': raise SystemExit/" xfixes-selection-notify.py
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
  python3.9 /usr/local/lib/xfsn.py CLIPBOARD 2>/dev/null >/dev/null
  xclip -o | xclip -i -selection clipboard
done
EOF
chmod +x .icewm/startup
wget https://raw.githubusercontent.com/ssb22/config/%6d%61%73%74%65%72/.Xresources

pkg remove xdm
rm -rf /usr/local/etc/X11/xdm/
echo "autologin: :al=root:tc=Pc:" >> /etc/gettytab
grep -v ^ttyv0 < /etc/ttys > n
mv n /etc/ttys
echo 'ttyv0 "/usr/libexec/getty autologin" xterm on secure' >> /etc/ttys
echo '[ "$tty" == ttyv0 ] && startx' >> .cshrc

sysrc vboxguest_enable="YES"
sysrc vboxservice_enable="YES"

echo "Use auto-update-system for security patches" # until EOL of FreeBSD 12
# If need more space for auto-update-system, do first:
# rm -rf .cache .mozilla/firefox/*/storage /boot.save /var/cache/pkg/* /usr/ports/*/*/work
