
from https://ssb22.user.srcf.net/setup/ssh-android.html
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/setup/ssh-android.html) just in case)

# Desktop SSH via Android devices
These notes are old: they may still work, but I have not re-tested them on anything more recent than Android 4.4.

Some Android devices have “USB tether” functions that don’t work.  The following alternative method has two prerequisites:

1. You must have a working `adb` command (for example if you’ve installed the Android Developer Tools bundle)
2. The shell that `adb -d shell` gives you must contain an `ssh` command

Works on Android 4.4 but not on Android 4.1. If your device lacks one and you can’t install it, you might need to use an SSH app with port forwarding (such as ConnectBot or the paid version of JuiceSSH—you’ll now need an older APK of this for devices below Android 8) although you might still be able to adapt some of the script below.

## Advantages of SSH command over ADB
* No “rooting” of the Android device is required
* No “apps” need to be installed on the Android device
* You don’t even have to touch the Android device’s screen when starting a connection, so this process is fully scriptable from the desktop computer
* No root access required on the desktop either
* Should work from any platform that has adb (GNU/Linux, Mac, ...)
* The desktop’s network configuration can be left as-is (useful if it’s on a private LAN that’s awkward to reconfigure)
* The new Internet connection is not automatically visible to every program on your network that wants to “phone home”, so they won’t automatically use up all your bandwidth
  * and that means you can also regard the new connection as “not really tethering” (if your carrier says no tethering): you are simply using a larger keyboard and display to control the phone, with the same low bandwidth use as if you were directly typing into an SSH app on the phone (which is awkward for those of us with certain types of disability)
* Connectivity does not rely on Wi-Fi or Bluetooth (which can be unreliable in some environments, needs network reconfiguration and counts as tethering) 

## Disadvantages
1. The `ssh` command bundled with Android ignores the setting of HOME and is compiled to try and put its files in a `/data` directory which you can’t access on a non-rooted device
2. Although you can set SSH options to use files in (for example) `/storage/emulated/legacy`, those files are **readable by all apps**, some of which might be running in the background with “spy” functions.  Exposing the `known_hosts` file to them is relatively benign, but if you start putting *identity* files in that directory (even for a short time) you are taking a risk.
3. Although `adb -d shell` can take a command as a parameter, supplying one will cause the shell to become non-interactive.  So if you want to actually *type* into that SSH session, you have to run a shell *without* a default command, and type in all the settings each time.
4. `adb`’s limited terminal emulation might be a let-down when you want to run full-screen terminal applications

The above problems can be worked around by using `expect` and port forwarding.

## expect script
This [ssh-android expect script](ssh-android.sh) works around the above by doing the following:

1. Connects to an Android shell over ADB and issues an SSH command with the user and host you specify (user defaults to your login name) and password authentication.  This command is also set to start a SOCKS proxy.
2. Uses `adb` to extend this SOCKS tunnel over the USB connection onto a port on the local machine
3. Issues a *second* SSH command *outside* the `adb` shell, and sets it to go over the SOCKS connection.  The password you entered the first time is repeated by the script.
4. You may now interact with this second session using the full capabilities of your terminal (since it’s not inside `adb`), and/or tell other applications to connect through the SOCKS proxy
5. When this second SSH session finishes, the script shuts down the first

The script assumes that the host key is already in your `~/.ssh/known_hosts` file, but can be adapted if it isn’t.

Install it by saving it somewhere on your `PATH`, edit as necessary to set the path to `adb` and use `chmod +x` on it.  You’ll need `adb` and `expect` on the system (many Macs have `expect` already, and there are Linux packages in most distributions).

## Other use of the SOCKS proxy
Rather than using everything over SSH, you might wish to allow selected local programs to connect over the proxy while still not opening it to everything.

### HTTP proxy
In many cases it’s easier to use an HTTP proxy than a SOCKS proxy, so I suggest installing Privoxy and setting its `config` to `forward-socks5 / 127.0.0.1:10080 .` (you might also want to delete the `127.0.0.1` in `listen-address` to make it available to other machines on your local network, and if one of them sends too many requests you might then want `debug 1` so you can check `/var/log/privoxy/logfile.log` and add appropriate block patterns).  After restarting Privoxy, you can tell selected applications about it, e.g. for lynx, wget etc
`export http_proxy=http://localhost:8118/ ; export https_proxy=$http_proxy`
or for Subversion
`alias svn="svn --config-option servers:global:http-proxy-host=localhost --config-option servers:global:http-proxy-port=8118 --config-option servers:global:https-proxy-host=localhost --config-option servers:global:https-proxy-port=8118"`

Most graphical browsers can be set to use a proxy in their Advanced Settings, but beware their bandwidth use.  Turning off images can help.

Other Android devices (and iOS devices and probably some other mobiles) can be configured to use an HTTP proxy over WiFi if they have run out of their own mobile data allowances and it’s too awkward to transfer the physical SIM to them, but:

1. Not all applications on the device will use the proxy. ​The browser should, but messaging applications typically don’t—for those you’d need to intercept the traffic (see below)
2. Applications which do use the proxy might be less conservative about network usage when on Wi-Fi (see note about block patterns above)

### Other SOCKS forwarding
For other machines on the local network to access SOCKS directly (rather than via an HTTP proxy), you’ll need an additional port-forward because `adb` listens only to localhost.  For example (from the other machine) `ssh -L 10080:localhost:10080 192.168.0.1`

* For additional SSH connections: `alias ssh="ssh -o ProxyCommand='$(which nc) -x localhost:10080 %h %p'"` (and similarly for scp) 

Mac HomeBrew has dsocks (the file `/usr/local/bin/dsocks.sh` will need editing if you need to change the port, but default 10080 is also the default of ssh-android)
* Does **not** tunnel DNS, so you’ll need a separate low-bandwidth connection for DNS lookup unless you set relevant entries in /etc/hosts (which might be the best option if you only want to run your email program; just make sure to update your hosts file if the servers’ IPs change: you might want to use WebCheck for this)
* Works with some programs better than others: `mutt` and `python imapfix.py` worked for me, but not `alpine` or `brew`.  It depends whether they use libraries that `dsocks` can intercept. 

tsocks (GNU/Linux): to make DNS work over the tunnel, I suggest patching it as follows:

1. Download the source of tsocks 1.8beta5
2. Use `./configure --enable-socksdns --disable-hostnames` (should work on Raspberry Pi)
3. Edit `tsocks.c` and add the line `_res.options |= RES_USEVC;` at the start of the `connect()` function.  This is because `res_init` is not always called as the original programmer expected (I guess due to changes in Linux libraries since it was published), so we need to set the option here instead.
4. Optionally comment out the “call to connect received on completed request” message (which sometimes appears spuriously in the middle of lynx etc)
5. `make` and `sudo make install`
6. In `/etc/tsocks.conf` put

    local = 192.168.0.0/255.255.0.0
    local = 127.0.0.1/255.255.255.255
    server = 127.0.0.1
    server_port = 10080
    server_type = 5
    # make sure there's a newline at the end

and make sure your `/etc/resolv.conf` has public DNS servers (or ones that are operable from the machine you’re SSH-ing into)

7. Run with `LD_PRELOAD=/lib/libtsocks.so program-name`
8. Uninstall with `rm -f /lib/libtsocks* /usr/man/man*/tsocks.* /usr/bin/tsocks`

### Redirecting *all* traffic
Setting up a gateway machine to redirect *all* traffic would lose the advantage of not having the connection automatically visible to every program on your network (you might need to add blocking rules), and arguably *will* constitute “tethering”, unless perhaps you’re providing WiFi to only another phone or tablet that you could have put your SIM into.

Perhaps the easiest way to set things up on the gateway machine (Raspberry Pi or whatever) is to use `transocks_ev` with `iptables` and `pdnsd`.
* If compiling transocks_ev with gcc 4.x (and possibly other compilers), ensure the `getopt` line says `!= (char)EOF` not just `!= EOF` or it may hang on startup (this was fixed in Revision 7). You’ll probably need a package like `libevent-dev`.
* Run `pdnsd` with the `-mto` parameter to make its upstream queries TCP-only, and configure it with an upstream server that’s reachable from the SSH host e.g.

    server {
    label="whatever";
    ip=8.8.8.8, 8.8.4.4;
    proxy_only=on;
    timeout=4;
    uptest=none;
    }

(commenting out any other `server` block).  It’s also important to `set server_ip = 0.0.0.0` in the `global` section, since `iptables` redirection does not override “localhost-only” socket binding.

* The script will look something like this:
  1. If adb is not running on the gateway machine, make port 10080 available via `ssh -L 10080:localhost:10080 machine-running-adb &` as mentioned above
  2. `pdnsd -mto &`
  3. `transocks_ev -p 10079 -H 0.0.0.0 -s 10080 -S 127.0.0.1 -f &`
  4. `iptables -t nat -N TRANSOCKS || iptables -t nat -F TRANSOCKS #` creates a new chain called TRANSOCKS, or clears it
  5. `iptables -t nat -A TRANSOCKS -d 127.0.0.0/8 -j RETURN ; iptables -t nat -A TRANSOCKS -d 192.168.0.0/16 -j RETURN #` exceptions for the local network
  6. If you want to block certain destinations/ports at the IP level, do it *here* e.g. `iptables -t nat -A TRANSOCKS -d $bad_ip_range -p tcp -j REDIRECT --to-ports 65432 #` and make sure nothing’s listening on port 65432; this results in a REJECT (not normally available from the nat table)
  7. `iptables -t nat -A TRANSOCKS -p tcp -j REDIRECT --to-ports 10079 #` redirect all other TCP traffic to transocks_ev
  8. `iptables -t nat -A TRANSOCKS -p udp --dport 53 -j REDIRECT --to-ports 53 #` redirect all UDP DNS queries to pdnsd
  9. `iptables -t nat -A PREROUTING -j TRANSOCKS #` apply the TRANSOCKS rules to any Internet-bound packets from other machines on the local network
  10. `iptables -t nat -A OUTPUT -j TRANSOCKS #` and apply them for locally-generated packets (important for pdnsd’s upstream queries) 

## Copyright and Trademarks
All material © Silas S. Brown unless otherwise stated.
Android is a trademark of Google LLC.
Bluetooth is a registered trademark held by the Bluetooth Special Interest Group.
Linux is the registered trademark of Linus Torvalds in the U.S. and other countries.
Mac is a trademark of Apple Inc.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.
Wi-Fi is a trademark of the Wi-Fi Alliance.
Any other trademarks I mentioned without realising are trademarks of their respective holders.
