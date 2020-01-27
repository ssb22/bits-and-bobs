#!/usr/bin/env python2

# Convert ASCII Portable Bitmap (.pbm) files to BBC Micro VDU 23 sequences
# Silas S. Brown - public domain - no warranty

screenWidth = 40 # text columns (e.g. Mode 4)
# (If using 20 or 80, might want to account for non-square pixels)

mode = "raw" # "basic" for VDU commands to paste into AUTO; "raw" to send bytes over link

import sys
if len(sys.argv)>1: pbmDat=open(sys.argv[1]).read()
else:
  sys.stderr.write("pbmtobbc: reading from standard input\n")
  pbmDat=sys.stdin.read()

def pullLine():
  global pbmDat
  ret,pbmDat = pbmDat[:pbmDat.index("\n")],pbmDat[pbmDat.index("\n")+1:]
  return ret

assert pullLine()=="P1"
l = "#"
while l.startswith("#"): l = pullLine()
width,height = l.split()
width,height = int(width),int(height)
pbmDat = pbmDat.replace("\n","").replace("0","w").replace("1","0").replace("w","1")
rows = []
while pbmDat:
    rows.append(pbmDat[:width])
    pbmDat = pbmDat[width:]
assert len(rows)==height
defs = [None]*32 ; nextDef = 0
for yStart in range(0,height,8):
    out = []
    for x in range(0,min(width,screenWidth*8),8):
        charDef = [int(rows[y][x:x+8],2) for y in range(yStart,yStart+8)]
        if not any(charDef):
            out.append(' ') ; continue
        charDef = "".join(chr(x) for x in charDef)
        if not charDef in defs:
           out.append(chr(23)+chr(nextDef+224)+charDef)
           defs[nextDef] = charDef
           nextDef += 1
           if nextDef>=len(defs): nextDef = 0
        out.append(chr(224+defs.index(charDef)))
    out = ''.join(out)
    if not out.replace(' ',''): out = '\n'
    elif out[-1]==' ': out = out.rstrip()+'\r\n'
    # else exact fit for screenWidth
    if mode=="basic":
      o = []
      while out:
         o.append("V."+",".join(str(ord(c)) for c in out[:59])+"\n")
         out = out[59:]
      out = "".join(o)
    sys.stdout.write(out)
