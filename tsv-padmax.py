#!/usr/bin/env python3
"""'GitHub has a "fancy" TSV-data display but only
if all rows contain the same number of columns: a
 single row with an extra Notes column can stop
it.  This script pads all rows to the number of
columns of the longest row, as well as deleting
any completely-blank columns with blank headings.
(c) Silas S. Brown 2024, License: Apache 2."""
# (I did say "public domain no warranty" but apparently
# some corporate offices don't trust that.  Apache 2 lets
# them know I don't have a silly patent up my sleeve that
# I'd try to enforce, so their policy might accept it more
# easily if you need to use this at work.)

import sys
if len(sys.argv) < 2: print ("Need files")
for f in sys.argv[1:]:
    L = open(f).read().split('\n')
    cols = max(len(i.split('\t')) for i in L)
    L = ['\t'.join((i+'\t'*cols).split('\t')[:cols]) for i in L]
    for c in range(cols-1,-1,-1):
        if not any(i.split('\t')[c] for i in L):
            L = ['\t'.join(i.split('\t')[:c]+i.split('\t')[c+1:]) for i in L]
    if not L[-1].strip(): L[-1] = "" # trailing \n
    open(f,'w').write('\n'.join(L))
