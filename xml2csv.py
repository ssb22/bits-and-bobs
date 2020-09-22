# Simple XML to CSV
# e.g. for https://ghr.nlm.nih.gov/download/ghr-summaries.xml
# Silas S. Brown 2017 - public domain - no warranty

# Bugs: may not correctly handle descriptions that mix
# tags with inline text on the same level.
# FOR EXPLORATORY USE ONLY.

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs

max_chars_per_cell = 80

# set max_chars_per_cell = None for unlimited,
# but note many spreadsheet programs will have problems

import sys, csv
from xml.parsers import expat

items = {}
cursorStack = [(0,0,0,0,0)] # x,y,curDir,maxX,maxY
def inc(x,y,curDir,xToSet,yToSet):
    if curDir: return x,yToSet
    else: return xToSet,y
def turn(curDir):
    if curDir==1: return 0
    else: return 1

def StartElementHandler(name,attrs):
    x,y,curDir,maxX,maxY = cursorStack[-1]
    items[(y,x)] = name
    childDir = turn(curDir)
    cursorStack.append(inc(x,y,childDir,x+1,y+1) + (childDir,x,y))
def EndElementHandler(name):
    _,_,_,cMaxX,cMaxY = cursorStack.pop()
    x,y,curDir,maxX,maxY = cursorStack.pop()
    cursorStack.append(inc(x,y,curDir,cMaxX+1,cMaxY+1) + (curDir,max(maxX,cMaxX),max(maxY,cMaxY)))
def CharacterDataHandler(data):
    x,y,curDir,maxX,maxY = cursorStack.pop()
    while data:
        data = items.get((y,x),"") + data.replace("\n"," ").replace("\r","")
        if max_chars_per_cell: data, dataRest = data[:max_chars_per_cell],data[max_chars_per_cell:]
        else: dataRest = ""
        if dataRest and len(data.split())>1 and data[-1].split() and dataRest[0].split(): data,dataRest = data.rsplit(None,1)[0],data.rsplit(None,1)[1]+dataRest # word wrap on spaces
        items[(y,x)] = data
        data = dataRest
        if data: y += 1
    cursorStack.append((x,y,curDir,max(x,maxX),max(y,maxY)))

parser = expat.ParserCreate()
parser.StartElementHandler = StartElementHandler
parser.EndElementHandler = EndElementHandler
parser.CharacterDataHandler = CharacterDataHandler
parser.Parse(sys.stdin.read(),1)

curX=curY=0 ; curRow = [""]
o = csv.writer(sys.stdout)
for y,x in sorted(items.keys()):
    while y > curY:
        o.writerow(curRow)
        curRow = [""]
        curY += 1 ; curX = 0
    while x > curX:
        curRow.append("")
        curX += 1
    curRow[-1] = ' '.join(items[(y,x)].split()).encode('utf-8')
o.writerow(curRow)
