#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

"""Simple "Buddy Pounce" script for Skype using Clisk.
Silas S. Brown 2013, Public domain, no warranty.

(Note: Only Skype 7 and below supported the API that Clisk used.
Microsoft's support for Skype 7 ended in November 2018 and I have
no idea if it can even connect to the Skype network anymore.)

Must go in the same directory as clisk.  You can get
clisk from http://www.dlee.org/skype/clisk/ (correct as
of 2013).  You might want to set up a bash function, e.g.
if you put clisk and pounce.py into /usr/local/clisk251
then you can add the following to your bash profile:
pounce () (cd /usr/local/clisk251;python pounce.py "$*";)

This script should be run with 1 argument, the full
display name of the Skype contact you want to watch for
(case sensitive).  You probably have to put it in quotes.

The script will read all status changes from clisk, and
will generate no output until the name you gave is
mentioned.  At that point a dialogue is displayed and the
script will then exit.

If you want the watch to persist across reboots etc then
you could add it to a login script or whatever, but you'd
then need to manually remove it when no longer required.
Note also that this script does not currently check the
status of a contact on startup; it reports status CHANGES.
"""

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs

import sys,os,Tkinter,tkMessageBox,thread,time

if not len(sys.argv)==2:
    sys.stderr.write("Syntax: pounce.py \"string to watch for\"\n")
    sys.exit(1)

if sys.platform=="darwin": cmd="./clisk_mac"
elif sys.platform=="cygwin": cmd="./clisk_cygwin"
else: cmd="./clisk_linux"
if not os.path.exists(cmd):
    sys.stderr.write("Cannot find the clisk program.  Please put it in the current directory.\n")
    sys.exit(1)

try: cin,cout = os.popen4(cmd,bufsize=0)
except: # Python 3
    import subprocess
    p = subprocess.Popen(cmd, shell=True, bufsize=0,
                         stdin=PIPE, stdout=PIPE, close_fds=True)
    cin,cout = p.stdin, p.stdout
cin.write("aa * w\n") ; cin.flush() # but do not close
def buffer_flushing_thread():
    # Need to do this because the standard libraries used
    # by clisk will probably have 4k output buffers.
    # Need to get output from Skype4PY not just clisk help
    
    # (could also just use "contacts" to list current
    # contacts and poll it for changes, but that doesn't
    # always report complete display names and all status
    # changes)
    
    while cin:
        # cin.write("calls\n"*128)
        cin.write("help watchEvent\n")
        cin.flush()
        time.sleep(3)
thread.start_new_thread(buffer_flushing_thread,())
for line in cout:
  if sys.argv[1] in line:
    print ("\a"+line.strip())
    cin.close() ; cin=None ; cout.close()
    window=Tkinter.Tk()
    window.attributes("-topmost", True)
    window.wm_withdraw()
    tkMessageBox.showinfo(title="Buddy Pounce", message=line)
    break
