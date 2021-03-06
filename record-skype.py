#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

"""Simple "call record" script for Skype using Clisk.
Silas S. Brown 2013, Public domain, no warranty.

(Note: Only Skype 7 and below supported the API that Clisk used.
Microsoft's support for Skype 7 ended in November 2018 and I have
no idea if it can even connect to the Skype network anymore.)

Must go in the same directory as clisk.  You can get
clisk from http://www.dlee.org/skype/clisk/ (correct as
of 2013).  You might want to set up a bash function, e.g.
if clisk and record-skype.py are in /usr/local/clisk251
then you can add the following to your bash profile:
record-skype () (cd /usr/local/clisk251;python record-skype.py "$*";)
"""

import sys,os,time
try: raw_input
except: raw_input = input # Python 3

if sys.platform=="darwin": cmd="./clisk_mac"
elif sys.platform=="cygwin": cmd="./clisk_cygwin"
else: cmd="./clisk_linux"
if not os.path.exists(cmd):
    sys.stderr.write("Cannot find the clisk program.  Please put it in the current directory.\n")
    sys.exit(1)
cmd += " > /dev/null"
cin = os.popen(cmd,'w')
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
print ("Finished.")
