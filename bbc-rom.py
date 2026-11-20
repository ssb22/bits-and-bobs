#!/usr/bin/env python3
"""
Wrap a BBC Micro machine-code program in a 16K service ROM
(which relocates code to main RAM and runs it)

(c) 2026 Silas S. Brown, License: Apache 2

(I would say "public domain" but, just in case you somehow
need some of it at work, I want to reassure your legal dept I
don't have a silly patent up my sleeve, so Apache 2)

I think this idea was done in 1986 "Advanced ROM Manager" ROM
(*AUTOROM command, which also had a mode to do it for BASIC)

E.g. for Micropower Chess (Model B) 1982:
python3 bbc-rom.py Chess -o /usr/local/share/b-em/roms/general/chess.rom -l E00 -e 1C00 # or 1BD3 if using my sound patch
"""

import argparse,os,sys

ap = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('program')
ap.add_argument('-o', '--output',help='output .rom file (default is original filename + .rom)')
ap.add_argument('-n', '--name', help='star command (default is original filename in upper case)')
ap.add_argument('-l', '--load', help='load address, hex')
ap.add_argument('-e', '--exec', dest='execAddr', help='exec address, hex (default: load)')
ap.add_argument('--title', help='ROM title (default is original filename in original case)')
ap.add_argument('--version',default="",help='ROM version (default empty)')
ap.add_argument('--copyright',default="",help="ROM copyright string (default empty)")
ap.add_argument('--no-tape', action='store_true',
                help='do not issue *TAPE before relocating (use for utilities not touching E00 or on a Master)')

# 6502 operands
LDX,LDY,AND,ORA,INC,DEC=0xA2,0xA0,0x29,5,0xE6,0xC6
LDAabsx,LDAimm,LDAzp,LDAindY = 0xBD,0xA9,0xA5,0xB1
STAzp,STAindY = 0x85,0x91
CMPabsx,CMPimm = 0xDD,0xC9
JMP,JSR = 0x4C,0x20
INX,INY,TXA,TYA,TAX,TAY,PHA,PLA,RTS=0xE8,0xC8,0x8A,0x98,0xAA,0xA8,0x48,0x68,0x60
BEQ,BNE,BCC,BCS=0xF0,0xD0,0x90,0xB0

# BBC Micro memory map
RomBase, RomSize = 0x8000,0x4000
StarCmdPtr = 0xF2
SRC, DST, CNT = 0xA8, 0xAA, 0xAC # A8-AF = paged ROM temp use

def build(data, load, execAddr, command, title,
          version, copyright, tape=True):
  labels = {} ; L=lambda l:labels.get(l,0)
  for thePass in [1,2]:
    buf = bytearray() ; a=lambda *args:buf.extend(args)
    def w(v): return v.to_bytes(2,'little')
    def br(labelAddr):
        if labelAddr:
            offset = labelAddr - (RomBase+len(buf)+1)
            if not -128 <= offset <= 127: raise ValueError("Branch out of range")
            return offset & 0xFF
        else: return 0
    a(0,0,0) # no language entry
    a(JMP,*w(L('service')))
    a(0x82,L('copyrightPos'),0,*title.encode('ascii'),0,*version.encode('ascii'))
    labels['copyrightPos'] = len(buf)
    if not copyright.startswith("(C)"): copyright="(C)"+copyright # start with (C) is compulsory
    a(0, *copyright.encode('ascii'), 0)
    labels['service'] = RomBase+len(buf)
    a(CMPimm,4,BEQ),a(br(L('starCmd')),RTS)
    labels['starCmd'] = RomBase+len(buf)
    a(TXA,PHA,TYA,PHA,LDX,0)

    labels['cmp_loop'] = RomBase+len(buf)
    a(LDAabsx,*w(L('name')))
    a(BEQ),a(br(L('cmp_finish')))
    a(LDAindY,StarCmdPtr,CMPimm,0x61) # fold a-z to upper case
    a(BCC),a(br(L('cmp_it')))
    a(CMPimm,0x7B,BCS),a(br(L('cmp_it')))
    a(AND,0xDF)
    labels['cmp_it'] = RomBase+len(buf)
    a(CMPabsx,*w(L('name')),BNE),a(br(L('nomatch')))
    a(INX,INY,JMP,*w(L('cmp_loop')))
    labels['cmp_finish'] = RomBase+len(buf)
    a(LDAindY,StarCmdPtr)
    a(CMPimm,13,BEQ),a(br(L('matched')))
    a(CMPimm,32,BEQ),a(br(L('matched')))
    labels['nomatch']=RomBase+len(buf)
    a(PLA,TAY,PLA,TAX,LDAimm,4,RTS)
    labels['matched']=RomBase+len(buf)
    if tape: a(LDAimm,0x8C,LDX,0,LDY,0,JSR,*w(0xFFF4)) # *TAPE
    for zp, val in ((SRC, L('data')&0xFF), (SRC + 1, L('data')>>8),
                    (DST, load&0xFF), (DST + 1, load>>8),
                    (CNT, len(data)&0xFF), (CNT + 1, len(data)>>8)):
        a(LDAimm,val,STAzp, zp)

    a(LDY, 0)
    labels['copy'] = RomBase+len(buf)
    a(LDAindY,SRC,STAindY,DST,INC,SRC,BNE),a(br(L('s1')),INC,SRC+1)
    labels['s1'] = RomBase+len(buf)
    a(INC,DST,BNE),a(br(L('s2')),INC,DST+1)
    labels['s2'] = RomBase+len(buf)
    a(LDAzp,CNT,BNE),a(br(L('s3')),DEC,CNT+1)
    labels['s3'] = RomBase+len(buf)
    a(DEC,CNT,LDAzp,CNT,ORA,CNT+1,BNE),a(br(L('copy')))
    a(JSR, *w(execAddr))
    a(PLA,TAY,PLA,TAX,LDAimm,0,RTS) # A=0 command claimed

    labels['name'] = RomBase+len(buf)
    a(*command.encode('ascii'), 0)
    labels['data'] = RomBase+len(buf)
    overhead = len(buf)
    a(*data)
  if len(buf) > RomSize: raise ValueError("ROM bank overflow")
  return bytes(buf), overhead

def main():
    args = ap.parse_args()
    data = open(args.program, 'rb').read()
    load = int(args.load, 16) & 0xFFFF if args.load else None
    execAddr = int(args.execAddr, 16) & 0xFFFF if args.execAddr else None
    if load is None: ap.error('no load address: give -l')
    if execAddr is None: execAddr = load

    command = (args.name or os.path.splitext(os.path.basename(args.program))[0])
    if not command.isascii() or any(c <= ' ' for c in command): ap.error('command name must be printable ASCII without spaces')
    if not data: ap.error('empty program')
    if load + len(data) > 0x8000: ap.error(f'program would run past &7FFF (load &{load:04X} + {len(data)} bytes)')
    if not load <= execAddr < load + len(data):
        print(f'warning: exec &{execAddr:04X} is outside the program', file=sys.stderr)

    rom, overhead = build(data, load, execAddr, command.upper(),
                          args.title or command, args.version, args.copyright,tape=not args.no_tape)
    out = args.output or os.path.splitext(args.program)[0] + '.rom'
    with open(out, 'wb') as f: f.write(rom)
    print(f'wrote {out}: *{command} -> load &{load:04X}, exec &{execAddr:04X}, {len(data)} bytes (ROM overhead {overhead}, {RomSize - overhead - len(data)} spare)')

if __name__ == '__main__': main()
# ruff:noqa:E401,E701,E702,E731
