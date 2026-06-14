#!/usr/bin/env python3
# translate ASCII Braille to Unicode Braille
# (c) Silas S. Brown, License: Apache 2
# (I did say "public domain no warranty" but apparently
# some corporate offices don't trust that.  Apache 2 lets
# them know I don't have a silly patent up my sleeve that
# I'd try to enforce, so their policy might accept it more
# easily if you need to use this at work.)
import sys
print(sys.stdin.read().upper().translate(
    dict((ord(x),y)
         for x,y in zip(
                 " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)=",
                 list(range(0x2800,0x2840))))))
