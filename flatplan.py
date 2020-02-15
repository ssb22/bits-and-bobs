#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# flatplan 1.3 (c) 2016, 2020 Silas S. Brown.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is a program to draw an SVG diagram of a flat, using
# input that can be collected by a person with low vision and
# a centimetre tape measure.  Area and wall length are noted
# and squared-paper backing is also added.  You can also
# include the opening arcs of the internal doors.

# To measure the flat, start measuring at any wall, and trace
# your way around the entire flat until you come back to the
# same position.  This in effect means every room's length and
# width measurements will be taken TWICE, for error checking
# (if the line doesn't come back to the same spot, you made a
# mistake, which can also be manifest in the two ends of some
# door frame not matching up with each other).

# For best results, include protrusions of door frames, depth
# of windows, etc.  (Walls are much less likely to match up
# if door-frame protrusion is not taken into account.)

# The program assumes the flat is all on one level (hence "flat"),
# that it includes only right-angles, and that all walls are
# connected to the outside walls (no "islands").  This is
# probably valid for nearly all UK flats.

# As you go, imagine an ant (or similar) walking around the
# wall, and write the measurements as follows:

# number = walk that number of centimetres forward
# L = turn 90 degrees left
# R = turn 90 degrees right

# D<number> or E<number> = a door with specified width.
# This should be noted when the ant is at the door's hinge
# and is facing in the direction of the door's handle;
# D = door opens to the right, E = door opens to the lEft.
# The position of the ant is not changed.  If followed by
# more walking in the same direction (e.g. to get through the
# doorway), add a separator character (e.g. a colon) between
# the two numbers.

# If you like, you can ''.join([...]) a list of strings, which
# allows you to put comments on some of the measurements.

# Place your string into s below:

s = ''.join([
    "500",
    "R500",
    "R500",
    "R500"])

margin_cm = 100
include_area_summary = True
include_doors = True
include_grid_lines = True

# -------------------------------------------------------

xd=0;yd=-1 # start pointing up (SVG origin is top left)

curX = curY = oldX = oldY = 0
minX = minY = maxX = maxY = 0
lines = [] ; doors = []

def turnLeft(xd,yd):
    if yd: return yd,0
    else: return 0,-xd
def turnRight(xd,yd):
    if yd: return -yd,0
    else: return 0,xd

import re
for c in re.findall("[lr]|[de]?[0-9.]+",s.lower()):
    if c=='l': xd,yd = turnLeft(xd,yd)
    elif c=='r': xd,yd = turnRight(xd,yd)
    elif c[0] in 'de':
        radius = float(c[1:])
        handleX = curX + radius*xd
        handleY = curY + radius*yd
        if c[0]=='d': xd2,yd2 = turnRight(xd,yd)
        else: xd2,yd2 = turnLeft(xd,yd)
        openX = curX + radius*xd2
        openY = curY + radius*yd2
        if c[0]=='d': sweep = 1
        else: sweep = 0
        doors.append((handleX,handleY,radius,sweep,openX,openY,curX,curY))
    elif c:
        oldX,oldY = curX,curY
        curX += xd*float(c)
        curY += yd*float(c)
        minX = min(minX,curX)
        minY = min(minY,curY)
        maxX = max(maxX,curX)
        maxY = max(maxY,curY)
        lines.append((oldX,oldY,curX,curY))
minX-=margin_cm ; maxX+=margin_cm ; minY-=margin_cm ; maxY+=margin_cm

# help programs that display paper boundaries:
xOffset = -minX ; yOffset = -minY
minX += xOffset ; maxX += xOffset
minY += yOffset ; maxY += yOffset
try: xrange
except: xrange = range # Python 3
for i in xrange(len(lines)):
    a,b,c,d = lines[i]
    a += xOffset ; c += xOffset
    b += yOffset ; d += yOffset
    lines[i] = a,b,c,d
for i in xrange(len(doors)):
    a,b,r,s,c,d,e,f = doors[i]
    a += xOffset ; c += xOffset ; e += xOffset
    b += yOffset ; d += yOffset ; f += yOffset
    doors[i] = a,b,r,s,c,d,e,f

# area calculation (by flood-filling the outside and counting the rest) :
assert minX==minY==0
inside = [] ; totalLineLen = 0
for x in xrange(int(maxX)+1): inside.append([1]*(int(maxY)+1)) # don't say *int(maxX): it creates aliases of the same list
errorLine = lines[-1][-2:]+lines[0][:2] # completes the path in case of error
for a,b,c,d in lines+[errorLine]:
    if a>c: c,a = a,c
    if b>d: b,d = d,b
    for x in xrange(int(a),int(c)+1):
        for y in xrange(int(b),int(d)+1):
            inside[x][y] = 0
    totalLineLen += c-a + d-b
fillQ = [(0,0)]
while fillQ:
    x,y = fillQ[0] ; del fillQ[0]
    if inside[x][y]:
        inside[x][y] = 0
        if x>0: fillQ.append((x-1,y))
        if x<len(inside)-1: fillQ.append((x+1,y))
        if y>0: fillQ.append((x,y-1))
        if y<len(inside[0])-1: fillQ.append((x,y+1))
area = sum(sum(x) for x in inside) / 10000.0
totalLineLen /= 100.0
maxDP = 1 # max 1 decimal place
area = (u"%%.%dg m\u00b2" % (len(str(int(area)))+maxDP)) % area
if not type(u"")==type(""): area = area.encode('utf-8') # Python 2
area += (("; walls = %%.%dg m" % (len(str(int(totalLineLen)))+maxDP)) % totalLineLen)
a,b,c,d = errorLine
import math ; err = math.sqrt((c-a)*(c-a) + (d-b)*(d-b))
if err: area += (("; error = %%.%dg cm" % (len(str(int(err)))+maxDP)) % err)

# SVG:
print ("""<?xml version="1.0"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" width="%g" height="%g" viewbox="%g %g %g %g">""" % (maxX-minX,maxY-minY,minX,minY,maxX,maxY))

# grid lines:
def doGrid(colour,step):
    print ("""<g stroke="%s" stroke-dasharray="1,2">""" % colour)
    for x in xrange(int(minX),int(maxX),step):
        print ("""<line x1="%g" y1="%g" x2="%g" y2="%g" stroke-width="1" />""" % (x,minY,x,maxY))
    for y in xrange(int(minY),int(maxY),step):
        print ("""<line x1="%g" y1="%g" x2="%g" y2="%g" stroke-width="1" />""" % (minX,y,maxX,y))
    print ("</g>")
if include_grid_lines:
    doGrid("cyan",10) ; doGrid("red",100)

# the wall itself:
print ("""<g stroke="black">""")
for l in lines: print ("""<line x1="%g" y1="%g" x2="%g" y2="%g" stroke-width="1" />""" % l)
print ("</g>")

if include_doors:
    for x1,y1,r,sweep,x2,y2,cx,cy in doors: print ("""<path d="M%g,%g A%g,%g 0 0,%d %g,%g L%g,%g L%g,%g" fill="none" stroke="green" />""") % (x1,y1,r,r,sweep,x2,y2,cx,cy,x1,y1)

if include_area_summary:
    print ("""<text x="25" y="75" font-family="Verdana" font-size="30">Area = %s</text>""" % area)

print ("</svg>")
