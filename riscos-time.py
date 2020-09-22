#!/usr/bin/env python
# (works on both Python 2 and Python 3)

# Sets the time on a RISC PC or a dual-boot Raspberry Pi.
# For use in offline environments when NTP is not available.
# Version 1.22 (c) 2007, 2014, 2017, 2019-20 Silas S. Brown.

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
# If you used NOOBS to install both RISC OS and Raspbian,
# you'll probably find the RISC OS FAT is on partition 5,
# so add this line to /etc/fstab:
# /dev/mmcblk0p5 /riscos-fat vfat defaults
# (then mkdir /riscos-fat and mount /riscos-fat )
# and put this line into /etc/default/fake-hwclock (changing /path-to) :
# if ! [ "$1" = "start" ]; then python /path-to/riscos-time.py; fi
# (use = not == as it'll be running under /bin/sh not /bin/bash)

# Then on RISC OS, create a file with the line:
# DIM b% 5 : OSCLI("LOAD $.!Boot.Loader.timecode "+STR$~b%) : SYS "Territory_SetTime",b%
# and save it as $.!Boot.Choices.Boot.Tasks.SetClock with type BASIC

# (if you wish, you can also create an Obey file in Tasks with
# WimpTask Resources:$.Apps.!Alarm
# or whatever to launch a time display at startup)

# After this, any boot into RISC OS should set the clock
# to the clock time that Raspbian last saved on shutdown.

# (TODO: script does not currently provide a way to save
# the clock when moving from RISC OS back into Raspbian)

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs

# ------------------------------------------------------

import time
def risc_time(extra_secs=0):
  try:
    long # Python 2
    offset = (long(0x33) << 32) + 0x6E93EBE4 # or on 2.2+, 0x336E93EBE4L
  except: # Python 3 drops long, and L is a syntax error
    offset = (0x33 << 32) + 0x6E93EBE4
  h = int((time.time()+extra_secs)*100) + offset # hundreths of a sec since 1900
  if time.localtime()[-1]: h += 360000 # BST/DST
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
  try: o=open(filesystem+'/timecode','w')
  except IOError: # maybe the shutdown process mounted it read-only
    os.system("umount "+filesystem+" 2>/dev/null ; mount "+filesystem+" -o rw")
    o=open(filesystem+'/timecode','w')
  try: buf = o.buffer # Python 3
  except: buf = o # Python 2
  buf.write((u'%c%c%c%c%c'.encode('utf-8')) % risc_time(30)) # (allows 30secs for the reboot)
