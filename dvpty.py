#!/usr/bin/env python3

# Run a shell in a pseudo terminal, remapping the
# input so you can type Dvorak on a terminal that
# won't let you change keyboard layout from QWERTY

# (c) 2022 Silas S. Brown, License: Apache 2

import sys

US_keyboard = "--US" in sys.argv
# set this if the keyboard you're using is
# US QWERTY, don't set it for UK QWERTY
# (controls whether to swap @ and " around)

do_control_keys = not "--nocontrol" in sys.argv
# map (or don't map) the control keys as well.
# WARNING: THIS BREAKS TAB COMPLETION, the Tab
# key will give you Ctrl-C instead (annoying).
# You'll have to think "Ctrl-I" (Ctrl-G) for Tab
# unless you also set tab_hack below.

tab_hack = "--tab-hack" in sys.argv
# if mapping the control keys, map Ctrl-G to
# Ctrl-C, and leave Ctrl-I as-is.  That means Tab
# will work, but you'll have to think "Ctrl-I"
# (Ctrl-G) when you want to press Ctrl-C.

import pty,os
from subprocess import getoutput
in_csi = False
From=b'qwertyuiop[]sdfghjkl;\'#~zxcvbn,./qwertyuiop{}sdfghjkl:zxcvbn<>?-=_+'
To=b"',.pyfgcrl/=oeuidhtns-\\|;qjkxbwvz\"<>pyfgcrl?+oeuidhtns:qjkxbwvz[]{}"
if US_keyboard:
    From += b"\""
    To   += b"_"
else: # UK keyboard
    From += b"\"@"
    To   += b"@_"
assert len(From)==len(To)
def convert(k):
    global in_csi
    if k==27: in_csi = True
    elif in_csi:
        in_csi = not (ord('A')<=k<=ord('Z') or ord('a')<=k<=ord('z')) ; return k
    if do_control_keys and 1 <= k < 27:
        if tab_hack:
            if k==9: return k
            elif k==7: return 3
        return max(1,convert(k+ord('a')-1)-(ord('a')-1))
    return dict(zip(From,To)).get(k,k)
def f(fd): return b''.join(convert(b).to_bytes(1,'big') for b in os.read(fd,1024)).replace("\u00a3".encode('utf-8'),b'#')
sys.exit(pty.spawn(["/bin/bash","-c","stty rows %s;stty columns %s;bash" % tuple(getoutput("stty size").split())],stdin_read=f))
