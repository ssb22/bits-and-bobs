#!/usr/bin/env python3

# Cleans up filenames from GraceNote database etc.
# (e.g. for migrating from Mac iTunes to GNU/Linux MiniDLNA)

# Use --pipe for pipe, or specify a FULL path to an iTunes-style
# collection to rename (in which case you'll also get
# MiniDLNA-compatible m3u playlists in the current directory)

# Silas S. Brown 2025 - public domain, no warranty.  All
# copyrighted CDs should've been legally read for use within the
# household only and the original physical copies still present.

def main():
    if '--pipe' in sys.argv:
        for l in sys.stdin: print(clean(l))
    elif len(sys.argv) > 1 and all(os.path.isdir(f) for f in sys.argv[1:]):
        for d in sys.argv[1:]: rename(d)
    else: print ("Unknown usage or directory not found")

def clean(l): return re.sub(' +',' ',re.sub('[.]+','.',re.sub("[^ -~]",'',unicodedata.normalize('NFD',l.strip().replace("_ "," ").replace(" _"," ").replace("_"," ").replace(", "," ").replace(" - "," ").replace(" & "," and ").replace(" ["," ").replace("]","").replace("#","").replace(". "," ").replace(" .",".")))))

def rename(d):
    d2 = clean(d)
    if not d==d2:
        print(f'Renaming "{d}" to "{d2}"')
        os.rename(d,d2)
    if not os.path.isdir(d2): return
    for i in os.listdir(d2): rename(d2+os.sep+i)
    dOnly = d2.split(os.sep)[-1]
    if any(i.endswith(".m4a") or i.endswith(".mp3") or i.endswith(".ogg") for i in os.listdir(d2)) and not os.path.exists(dOnly+".m3u"):
        print(f"Writing {dOnly+'.m3u'}")
        open(dOnly+".m3u","w").write("\n".join(d2+os.sep+i for i in os.listdir(d2))+"\n")

import sys, os, unicodedata, re
if __name__ == "__main__": main()
