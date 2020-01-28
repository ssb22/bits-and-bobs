#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# Convert ASCII Portable Bitmap (.pbm) files to BBC Micro VDU 23 sequences
# Silas S. Brown - public domain - no warranty

screenWidth = 40 # text columns (e.g. Mode 4)
# (If using 20 or 80, might want to account for non-square pixels)

mode = "raw" # "basic" for VDU commands to paste into AUTO; "raw" to send bytes over link

import sys
if len(sys.argv)>1: pbmDat=open(sys.argv[1])
else:
  sys.stderr.write("pbmtobbc: reading from standard input\n")
  pbmDat=sys.stdin
if hasattr(pbmDat,"buffer"): _,pbmDat = pbmDat,pbmDat.buffer # Python 3
pbmDat = pbmDat.read()

newline = u"\n".encode('utf-8') # Python 2 or Python 3
def pullLine():
  global pbmDat
  ret,pbmDat = pbmDat[:pbmDat.index(newline)],pbmDat[pbmDat.index(newline)+1:]
  return ret

def B(s):
  """string to byte-string in
  Python 2 (including old versions that don't support b"")
  and Python 3"""
  if type(s)==type(u""): return s.encode('utf-8') # Python 3
  return s
def C(c):
  "chr(c) to byte-string in Python 2 or Python 3"
  c = chr(c)
  if type(c)==type(u""): return c.encode('latin1') # Python 3
  else: return c # Python 2
def O(c): # ord(c) in Python2/3
  if type(c)==str: return ord(c)
  else: return c

assert pullLine()==B("P1")
l = B("#")
while l.startswith(B("#")): l = pullLine()
width,height = l.split()
width,height = int(width),int(height)
pbmDat = pbmDat.replace(newline,B("")).replace(B("0"),B("w")).replace(B("1"),B("0")).replace(B("w"),B("1")) # collapse and invert
rows = []
while pbmDat:
    rows.append(pbmDat[:width])
    pbmDat = pbmDat[width:]
assert len(rows)==height
defs = [None]*32 ; nextDef = 0
for yStart in range(0,height,8):
    out = []
    for x in range(0,min(width,screenWidth*8),8):
        charDef = []
        for y in range(yStart,yStart+8):
          if y < height: charDef.append(int((rows[y][x:x+8]+B("000000"))[:8],2))
          else: charDef.append(0)
        if not any(charDef): # all 0 bits: just add a space
            out.append(B(' ')) ; continue
        charDef = B("").join(C(x) for x in charDef)
        if not charDef in defs:
           out.append(C(23)+C(nextDef+224)+charDef)
           defs[nextDef] = charDef
           nextDef += 1
           if nextDef>=len(defs): nextDef = 0
        out.append(C(224+defs.index(charDef)))
    out = B('').join(out)
    if not out.replace(B(' '),B('')): out = newline
    elif out[-1:]==B(' '): out = out.rstrip()+B('\r\n')
    # else exact fit for screenWidth
    if mode=="basic":
      o = []
      while out:
         o.append(B("V."+",".join(str(O(c)) for c in out[:59])+"\n"))
         out = out[59:]
      out = B("").join(o)
    if hasattr(sys.stdout,"buffer"): sys.stdout.buffer.write(out) # Python 3
    else: sys.stdout.write(out) # Python 2
