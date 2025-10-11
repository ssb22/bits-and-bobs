#!/bin/bash

# Script to set up an access point on a Raspberry Pi Zero W
# (a 2.4GHz-only device) with USB Ethernet, tested in PiOS 12
# - Silas S. Brown 2025, public domain, no warranty

set -e

if [ "$2" == "" ]; then echo "Syntax: sudo $0 AP-name password"; exit 1; fi

# Determine Ethernet device name.  May be eth0 or may be
# a "predictable" name using the MAC address if raspi-config
for N in /sys/class/net/en*; do export Eth="${N##*/}" ; done

# Read default gateway from our current settings (assumed OK)
# and current IP (assume it's static /24 and we want to keep)
GatewayIP=$(route -n|grep "G.* $Eth"|sed -e 's/[0.]*//' -e 's/ *//' -e 's/ .*//')
MyIP=$(ifconfig "$Eth"|grep 'inet '|sed -e 's/^ *inet //' -e 's/ .*//')

# Figure out a different /24 subnet for the Wi-Fi side.
WifiIP=$(echo $GatewayIP|python3 -c "import sys;ip=[int(i) for i in sys.stdin.read().split('.')];ip[-2]+=1;print('.'.join(str(i) for i in ip))")

# Make sure no network-manager is installed.  It messes up
# the Raspberry Pi way of doing things.  (It does NOT work to
# "nmcli device wifi hotspot ifname wlan0 ssid X password Y"
# as it may for quick setup on an Ubuntu24 laptop w.dnsmasq)
apt purge network-manager dnsmasq dhcpd bridge-utils
apt --purge autoremove

# The main work is done by wpa_supplicant:
cat > /etc/wpa_supplicant/wpa_supplicant-wlan0.conf <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB
network={
  ssid="$1"
  mode=2
  key_mgmt=WPA-PSK
  proto=RSN WPA
  psk="$2"
}
EOF

# Also set up hostapd for running the access point:
apt install hostapd
cat > /etc/hostapd/hostapd.conf <<EOF
ssid=$1
wpa_passphrase=$2
interface=wlan0
hw_mode=g
auth_algs=1
country_code=GB
ctrl_interface=/run/hostapd
ctrl_interface_group=0
accept_mac_file=/dev/null
deny_mac_file=/dev/null
driver=nl80211
ieee80211d=1
ieee80211n=1
ignore_broadcast_ssid=0
logger_stdout=-1
logger_stdout_level=3
logger_syslog=-1
logger_syslog_level=3
macaddr_acl=0
max_num_sta=30
rsn_pairwise=CCMP
wme_enabled=1
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
EOF

# Set up /etc/network/interfaces for ifup / ifdown
cat > /etc/network/interfaces <<EOF
iface $Eth inet static
  address $MyIP/24
  gateway $GatewayIP

iface wlan0 inet static
 address $WifiIP/24
 wpa-ssid $1
 wpa-psk $2
 mode ap
EOF

# Make sure we have some DNS servers available.  You may need
# to change this if Google's DNS server is not available in
# your country or organisation or time period or whatever.
# This is used by the package openresolv.
cat > /etc/resolvconf.conf <<EOF
resolv_conf=/etc/resolv.conf
name_servers=8.8.8.8
EOF

# and same with systemd
# - IPMasquerade tells it we want to do NAT
# - if you need to see active NAT connections, use
# sudo apt install tcpdump
# sudo tcpdump -i wlan0
cat > /etc/systemd/network/08-wlan0.network <<EOF
[Match]
Name=wlan0
[Network]
Address=$WifiIP/24
MulticastDNS=yes
DHCPServer=yes
IPMasquerade=yes
[DHCPServer]
DNS=8.8.8.8 1.1.1.1
EOF

# Tell the ISC DHCP server (if installed) to leave us alone,
# as DHCP for this interface is done separately above:
echo "denyinterfaces wlan0 $Eth" >> /etc/dhcp/dhcpd.conf

# Set an @reboot crontab to run ifup in case it doesn't come
# up by itself.  Needs to loop as cron happens before network
touch /var/spool/cron/crontabs/root
grep -v SHELL=/bin/bash < /var/spool/cron/crontabs/root | grep -v "@reboot while ! route" > n && mv n /var/spool/cron/crontabs/root
echo SHELL=/bin/bash >> /var/spool/cron/crontabs/root
echo "@reboot while ! route -n | grep $GatewayIP; do /usr/sbin/ifup $Eth; sleep 1; done" >> /var/spool/cron/crontabs/root

echo "All set.  Try rebooting."
