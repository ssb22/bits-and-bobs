#!/usr/bin/env expect --
# -*- mode: shell-script -*-

# Mac and Linux script to SSH to a host via Android adb
# with SOCKS port-forwarding and decent terminal settings
# (Linux users: remove the '--' on the first line above)

# Silas S. Brown 2014-2015, 2019, public domain, no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs

# Assumes ~/.ssh/known_hosts already has the host you're
# trying to connect to.  (If it doesn't, you might need to
# add code to recognise the fingerprint and answer yes.)

# You'll need to set the following:
# The path to your adb binary:
set ADB_PATH /usr/local/adt-bundle/sdk/platform-tools/adb
# The port number of the local SOCKS port to set up
# (10080 is the default port number for dsocks, which
# might be useful)
set SOCKS_PORT 10080

# --------------------------------------------------------

if {$argc == 0} {
  send_user "Syntax: $argv0 \[-l user\] host\n"
  send_user "(do not add a command)\n"
  exit 1
}

set timeout -1

# Read the user ID from 'whoami' for -l option.  If the
# user supplies a -l option as well, it'll override this.
spawn /usr/bin/whoami
expect -re "(.*)\r"
set USER "$expect_out(1,string)"

# Now start the ADB stuff:
send_user "Getting an ADB shell...\n"
spawn "$ADB_PATH" -d shell
expect {
  "device not found" {exit 1}
  "$ "
}
send_user "Sending known_hosts to Android...\n"
system "$ADB_PATH" -d push ~/.ssh/known_hosts /storage/emulated/legacy/known_hosts
send_user "Starting SSH...\n"
send "ssh -D $SOCKS_PORT -C -o UserKnownHostsFile=/storage/emulated/legacy/known_hosts -l $USER $argv \"/bin/bash -c 'echo waiting...;read'\"\r"
# (we do a 'read' rather than just have the prompt so that
# (1) it doesn't matter what the prompt is, (2) the local
# user is not confused by this non-interactive prompt)
expect assword:
stty -echo
expect_user -re "(.*)\n"
stty echo
set the_password "$expect_out(1,string)"
send_user "\nRemoving known_hosts from Android...\n"
system "$ADB_PATH" -d shell rm -f /storage/emulated/legacy/known_hosts
send_user "Sending password...\n"
send "$the_password\r"
expect "waiting..."
send_user "Completing the port forwarding...\n"
system "$ADB_PATH" -d forward tcp:$SOCKS_PORT tcp:$SOCKS_PORT
send_user "Spawning a local ssh...\n"
set old_id $spawn_id
spawn /bin/bash -c "ssh -o IdentityFile=/not/exist -o ProxyCommand='`which nc` -x localhost:$SOCKS_PORT %h %p' $argv"
# (using IdentityFile=/not/exist to force password so the following 'expect assword:' always works; could also use expect { ... } with some other string e.g. "Last login" as an alternative)
trap {
    set rows [stty rows]
    set cols [stty columns]
    stty rows $rows columns $cols < $spawn_out(slave,name)
} WINCH
expect assword:
send_user "(sending password)\n"
send_user "SOCKS port is localhost:$SOCKS_PORT; will be closed when this session exits"
send "$the_password\r"
interact
set spawn_id $old_id
send_user "Shutting down Android SSH connection...\n"
send "exit\r"
expect "$ "
system "$ADB_PATH" -d forward --remove tcp:$SOCKS_PORT
send "exit\r"
send_user "Finished\n"
