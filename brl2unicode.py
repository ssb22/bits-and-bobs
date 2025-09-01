#!/usr/bin/env python3
# translate ASCII Braille to Unicode Braille
# Silas Brown - public domain
import sys
print(sys.stdin.read().upper().translate(
    dict((ord(x),y)
         for x,y in zip(
                 " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)=",
                 list(range(0x2800,0x2840))))))
