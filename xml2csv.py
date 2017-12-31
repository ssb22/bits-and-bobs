# Simple XML to "CSV" (actually tab-separated text)
# e.g. for https://ghr.nlm.nih.gov/download/ghr-summaries.xml
# Silas S. Brown 2017 - public domain

max_chars_per_cell = 80
# LibreOffice sc/source/ui/docshell/impex.cxx lcl_appendLineData
# uses SAL_MAX_UINT16 (previously STRING_MAXLEN, both 0xFFFF bytes)
# but LibreOffice 4.2 and 5.1.6 can give "maximum number
# of characters per cell" warnings in other circumstances
# even if the above is set quite low (TODO: find out why)

import sys
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
        data, dataRest = data[:max_chars_per_cell],data[max_chars_per_cell:]
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

curX=curY=0
for y,x in sorted(items.keys()):
    while y > curY:
        sys.stdout.write("\n")
        curY += 1 ; curX = 0
    while x > curX:
        sys.stdout.write("\t")
        curX += 1
    sys.stdout.write(' '.join(items[(y,x)].split()).encode('utf-8'))
