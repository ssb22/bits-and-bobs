# Python 2 script to rename/block MSN contacts in Skype 6
# Silas S. Brown 2013, Version 1.1, Public Domain, no warranty
# Usual disclaimers apply: don't blame me for any damage
# (I suggest you back up your data before trying this).
# Also, make sure to quit Skype before accessing its files!

# Tested on a Mac OS 10.7 machine running Skype 6.1.0.2295
# (and 6.2), and bringing contacts over from Adium 2.0
# (but this can easily be changed)

import os

# You can set blist_file to a blist.xml file used by a libpurple application
# such as Pidgin or Adium.  (This is optional.)
# The following is correct for Adium 2.0:
blist_file = os.environ["HOME"]+"/Library/Application Support/Adium 2.0/Users/Default/libpurple/blist.xml"

# The following dictionary will override blist_file (and
# will also be used if blist_file is missing)
ID2alias_override = {
    "test1@example.com" : "Test One",
    "test2@example.com" : "Test Two",
    }

# The following is a list of MSN emails you want to block.
# Adium block list will be added to these.
blocks = [
    "test1@example.com",
    "test2@example.com",
   ]

# ------------------------------------------------

import sqlite3, commands
import xml.etree.ElementTree as et

def walkXml(e):
    name=alias=None
    for c in e.getchildren():
        if c.tag=="name": name=c.text
        elif c.tag=="alias": alias=c.text
        elif c.tag=="block": blocks.append(c.text)
    if name and alias: yield (name,alias)
    else:
        for c in e.getchildren():
            for i in walkXml(c): yield i
try: blist = open(blist_file).read()
except: blist = None
if blist:
    print "Reading contacts from",blist_file
    name2alias = dict(walkXml(et.fromstring(blist)))
else:
    print "Cannot read",blist_file,"(skipping)"
    name2alias = {}
name2alias.update(ID2alias_override)

for db in commands.getoutput(r"find ~/Library/Application\ Support/Skype/*/main.db").split("\n"):
    print "Accessing database",db
    conn = sqlite3.connect(db)
    c=conn.cursor()
    c.execute("SELECT * FROM Contacts")
    changes = []
    for t in c.fetchall()[:]:
      if not len(t)==96: continue # skip (maybe wrong version, might need to print them up and check)
      mail = t[3]
      if mail:
        # TODO: t[49] isauthorized INTEGER, t[51] isblocked INTEGER
        if mail.startswith("1:"): mail=mail[2:]
        if mail in name2alias and (t[33]==t[36] or not t[36]) and not t[33]==t[36]==name2alias[mail]:
            print "Changing %s from %s to %s" % (mail,repr(t[33]),repr(name2alias[mail]))
            t=list(t)
            t[33]=t[36]=name2alias[mail] # TODO: omit t[36] if it was None? (if so, also change the last condition of the 'if' above)
            changes.append(tuple(t))
    print "Making",len(changes),"changes"
    if changes: c.executemany("INSERT OR REPLACE INTO Contacts VALUES ("+",".join(["?"]*len(changes[0]))+")", changes)
    else: print "Cannot find any changes to make. Perhaps they are already made, or do you have a different version of Skype?"
    print "Blocking %d emails" % len(blocks)
    c.executemany("UPDATE Contacts SET isblocked=1 WHERE skypename=?",[["1:"+b] for b in blocks])
    conn.commit() ; conn.close()

for db in commands.getoutput(r"find ~/Library/Application\ Support/Skype/*/eas.db").split("\n"):
    print "Accessing database",db
    conn = sqlite3.connect(db)
    c=conn.cursor()
    c.execute("SELECT * FROM properties")
    changes = []
    for t in c.fetchall()[:]:
      if not len(t)==3: continue # skip (maybe wrong version, might need to print them up and check)
      if t[1]=="_skypename" and t[2].startswith("1:") and t[2][2:] in name2alias:
          print "Changing",t[2][2:],"to",repr(name2alias[t[2][2:]]) # could print "from" but would need to get that from other loop iterations
          changes.append((t[0],'_FileAs',name2alias[t[2][2:]]))
    print "Making",len(changes),"changes"
    if changes: c.executemany("INSERT OR REPLACE INTO properties VALUES (?,?,?)", changes)
    else: print "Cannot find any changes to make. Perhaps they are already made, or do you have a different version of Skype?"
    conn.commit() ; conn.close()
