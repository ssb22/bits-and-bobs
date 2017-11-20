#!/usr/bin/env python

"""Simple "call record" script for Skype using Clisk.
Silas S. Brown 2013, Public domain.

Must go in the same directory as clisk.  You can get
clisk from http://www.dlee.org/skype/clisk/ (correct as
of 2013).  You might want to set up a bash function, e.g.
if clisk and record-skype.py are in /usr/local/clisk251
then you can add the following to your bash profile:
record-skype () (cd /usr/local/clisk251;python record-skype.py "$*";)
"""

import sys,os,time

if sys.platform=="darwin": cmd="./clisk_mac"
elif sys.platform=="cygwin": cmd="./clisk_cygwin"
else: cmd="./clisk_linux"
if not os.path.exists(cmd):
    sys.stderr.write("Cannot find the clisk program.  Please put it in the current directory.\n")
    sys.exit(1)

cin,cout = os.popen4(cmd,bufsize=0)
counter = 0
def fn(): return "/tmp/word"+str(counter)+".wav"
while os.path.exists(fn()): counter += 1
raw_input("Press Enter to record "+fn()+": ")
cin.write("rec "+fn()+"\n") ; cin.flush()
t = time.time()
raw_input("Recording, press Enter to stop: ")
dur = time.time() - t
cin.write("off\n") ; cin.flush()
raw_input("Press Enter to play it back to the other party: ")
cin.write("snd "+fn()+"\n") ; cin.flush()
time.sleep(dur) # TODO: method of interrupting if dur is large?  (but this script is meant for short phrases)
cin.write("off\n") ; cin.flush()
print "Finished."
