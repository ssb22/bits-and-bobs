#!/usr/bin/env python3
"""List the longest lines of code in the current
   directory, in a format that should work with
   Emacs M-x grep.
   Silas S. Brown 2024 - public domain"""

extensions = [".py", ".sh"]
min_line_length_to_list = 80 # (PEP 8 suggests max 79 for editors with no wrap)

import os
lines = []
def checkFiles(dirname="."):
    global lines
    for l in os.listdir(dirname):
        l = dirname+os.sep+l
        if os.path.isdir(l): checkFiles(l)
        elif any(l.endswith(e) for e in extensions): lines += [(len(line),f"{(l)[2:]}:{lNo+1}:{len(line.rstrip())}:{line.rstrip()}") for lNo,line in enumerate(open(l)) if len(line.rstrip()) >= min_line_length_to_list] # (like this one)
checkFiles(".")
print("\n".join(l[1] for l in reversed(sorted(lines))))
