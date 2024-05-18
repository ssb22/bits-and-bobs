#!/usr/bin/env python2

# add \date{} to LaTeX letter from file's timestamp
# (in case you want to TeX it at a future date and have the
# letter's original date present in the printout or PDF,
# assuming the timestamp is the date originally printed)

import sys,os,time
if len(sys.argv)==1:
    sys.stderr.write("Please provide .tex filenames as arguments\n")
    sys.exit(1)
for fname in sys.argv[1:]:
    f = open(fname).read()
    if r"\date{" in f:
        sys.stderr.write(fname+r" already has \date{ so skipping"+"\n")
        continue
    if not r"\opening{" in f:
        sys.stderr.write(fname+r" has no \opening{ so skipping"+"\n")
        continue
    y,m,d = time.localtime(os.stat(fname).st_mtime)[:3]
    d=str(d)
    if d.endswith("3") and not d=="13": d+="rd"
    elif d.endswith("2") and not d=="12": d+="nd"
    elif d.endswith("1") and not d=="11": d+="st"
    else: d += "th"
    f = f.replace(r"\opening{",r"\date{"+d+" "+["","January","February","March","April","May","June","July","August","September","October","November","December"][m]+" "+str(y)+"}\n"+r"\opening{")
    open(fname,"w").write(f)
    sys.stderr.write("Done "+fname+"\n")
