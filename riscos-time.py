#!/usr/bin/env python
# (works on both Python 2 and Python 3)

# Sets the time on a RISC PC or a dual-boot Raspberry Pi.
# For use in offline environments when NTP is not available.
# Version 1.32 (c) 2007, 2014, 2017, 2019-21 Silas S. Brown.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To set the time on a RISC PC
# ----------------------------
# Uncomment the following line and set it to the RISC PC's IP:
# risc_ip = "192.168.142.2"
# This script should then be run on another machine
# (any platform that supports Python 2 or 3) with a correct clock
# and the RISC PC should be running a Telnet server.

# To set the time on a dual-boot Raspberry Pi
# -------------------------------------------
# If you used NOOBS to install both RISC OS and Raspbian / Raspberry Pi OS,
# you'll probably find the RISC OS FAT is on partition 5 or 6,
# so add a line like this to /etc/fstab:
# /dev/mmcblk0p5 /riscos-fat vfat defaults
# (then mkdir /riscos-fat and mount /riscos-fat )
# and put this line into /etc/default/fake-hwclock (changing /path-to) :
# if ! [ "$1" = "start" ]; then python /path-to/riscos-time.py; fi
# (use = not == as it'll be running under /bin/sh not /bin/bash)

# On newer versions of Raspbian/PiOS, /etc/init.d/fake-hwclock is
# bypassed by /lib/systemd/system/fake-hwclock.service so you won't
# be able to add commands to /etc/default/fake-hwclock in this way,
# and adding directly to /sbin/fake-hwclock doesn't always work.
# You could create /etc/systemd/system/riscos-time.service with:
# 
# [Unit]
# Descrption=Set RISC OS time
# [Service]
# Type=oneshot
# RemainAfterExit=true
# ExecStop=/usr/local/riscos-time.py
# [Install]
# WantedBy=multi-user.target
# 
# and do "systemctl daemon-reload" and "systemctl enable riscos-time --now"

# Then on RISC OS, create a file with the line:
# DIM b% 5 : OSCLI("LOAD $.!Boot.Loader.timecode "+STR$~b%) : SYS "Territory_SetTime",b%
# and save it as $.!Boot.Choices.Boot.Tasks.SetClock with type BASIC
# (and enable auto DST changes in Alarm, otherwise you may get GMT only)

# If you're having FAT corruption issues, you might prefer to use
# the timestamp of the timecode file itself instead of its data.
# You can set the clock to the file timestamp from BASIC:
# DIM b% 5 : SYS "OS_File",5,"$.!Boot.Loader.timecode" TO r0%,r1%,r2%,r3% : b%?4=r2% AND &FF : !b%=r3% : SYS "Territory_SetTime",b%
# and then instead of this script, use a shell script with:
# touch -t "$(date +"%Y%m%d%H%M.%S" --date="+30 seconds")" /riscos-fat/timecode
# (after verifying /riscos-boot is mounted, and unmount afterwards)

# After this, any boot into RISC OS should set the clock
# to the clock time that Raspbian/PiOS last saved on shutdown.
# (But don't boot Raspbian/PiOS to set the time and immediately switch to
# RISC OS: Raspbian/PiOS's NTP process runs in the background and might
# not be complete by the time the login prompt shows, so some extra
# delay is needed before typing reboot and going into RISC OS.)

# If you wish, you can also create an Obey file in Tasks with
# WimpTask Resources:$.Apps.!Alarm
# or whatever to launch a time display at startup;
# you might also want to put other startup files here,
# e.g. if a small child will be using the machine and
# might press F12, Michael Borcherds' Ctrlf12 module:
# https://web.archive.org/web/20210128155544/http://www.borcherds.co.uk/binaries/ctrlf12.zip
# use lynx not wget for archive.org

# (TODO: script does not currently provide a way to save
# the clock when moving from RISC OS back into Raspbian/PiOS)

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

# ------------------------------------------------------

import time
def risc_time(extra_secs=0):
  try:
    long # Python 2
    offset = (long(0x33) << 32) + 0x6E9952EF # or on 2.2+, 0x336E9952EFL
  except: # Python 3 drops long, and L is a syntax error
    offset = (0x33 << 32) + 0x6E9952EF
  h = int((time.time()+extra_secs)*100) + offset # hundredths of a sec since 1900
  return (h&255, (h>>8)&255, (h>>16)&255, (h>>24)&255, (h>>32)&255)
try: risc_ip
except NameError: risc_ip=0
if risc_ip:
  import socket
  s=socket.socket()
  s.connect((risc_ip,23)) # (or whichever port you're running it on; 23 is default)
  def slowsend(bytestr):
    if type(bytestr)==type(u""): bytestr==bytestr.encode('utf-8') # Python 3
    for b in bytestr:
      s.send(b) ; s.recv(100)
  slowsend('basic\n')
  slowsend('SYS "Territory_SetTime",CHR$(%d)+CHR$(%d)+CHR$(%d)+CHR$(%d)+CHR$(%d)\n' % risc_time())
else: # Raspberry Pi dual-boot
  filesystem = "/riscos-fat"
  import sys,commands,os
  sys.stderr.write("Writing Territory_SetTime call to $.!Boot.Loader ("+filesystem+") timecode\n")
  try: o=open(filesystem+'/timecode','wb')
  except IOError: # maybe the shutdown process mounted it read-only
    os.system("umount "+filesystem+" 2>/dev/null ; mount "+filesystem+" -o rw")
    o=open(filesystem+'/timecode','wb')
  o.write((u'%c%c%c%c%c'.encode('latin1')) % risc_time(30)) # (allows 30secs for the reboot)
  o.close() ; os.system("umount "+filesystem+"||sync;sleep 3") # just in case (RPi SD card etc)
