#!/usr/bin/env python3

"""Simple BBC Micro disassembler handling Micropower Chess computed jump
and inserting some comments about that Chess program's workings.

Silas S. Brown - public domain - no warranty

Micropower Chess is proprietary software.  To respect the
original author's copyright, this disassembler does NOT
contain or redistribute any game code or assets.

To use this tool, you must supply your own copy of the
original Micropower Chess binary: I am assuming anyone who
is interested in Micropower Chess will have a copy of it in
their legitimate collection of disks from the 1980s.

This program simply reads your local file and overlays my
original analytical comments for educational and historical study.

"""

chess_disk = "chess.ssd"
load_from_sector = 0x21
binary_size = 0x2280
loadTo = 0xE00 # loads at 1E00 but relocates to E00
entryPoint = 0x3000 # disk version's relocator (runs at 0x4000, then calls 1C00)

def main():
    data=open(chess_disk,"rb").read()[load_from_sector*256:load_from_sector*256+binary_size]
    mem = bytearray(loadTo+len(data))
    for i in range(len(data)): mem[loadTo+i] = data[i]
    lines = disasm(mem)
    with open("chess.asm","w") as f:
        for addr in sorted(lines.keys()):
            f.write(lines[addr] + "\n")
    print(f"Wrote {len(lines)} lines to chess.asm")

comments = {
    0x0E00:"tokenised BASIC CALL for tape version CHAIN to work",
    0x0E20:"start of pawn sprite",
    0x0E70:"start of knight sprite",
    0x0EC0:"start of bishop sprite",
    0x0F10:"start of rook sprite",
    0x0F60:"start of queen sprite",
    0x0FB0:"start of king sprite",
    0x1000:"additions table for bishop, rook and knight movement on a 10x10 board",
    0x1026:"material values, I think",
    0x102C:"initial back-rank pattern (shows piece IDs)",
    0x1034:"Space reserved for current board: 10x10 including $FF borders. This gets wiped and reinitialised on load, so they could have put a 100-byte secret message here if they wanted. As it is, they left a board with a few moves played: might have been used with the init bypassed during testing.",
    0x10AC:"memory reserved for attack/defence count",
    0x1115:"table of piece IDs to ASCII letters for analysis edit mode",
    0x19A0:"Demo data (Fischer-Spassky game 6).  This is overwritten by Replay data when a game is played.  First 2 bytes point to next free slot, then start and destination squares as 10*(rank+1)+file; for castling the king moves first and then rook after a byte 01.",
    0x1A50:"Space for more Replay moves if you have a game longer than the Fischer-Spassky",
    0x1A80:"Still space for more Replay moves; I think we periodically switch between 00 and FF blocks to protect against tape-read glitches (again they could have left a secret message here?) It goes right up to 1C00 giving you 303-ply (with castling counting as 2.5-ply); I saw display bugs if you go over ~260-ply with an unfinished game but not yet seen why in the code",
    0x1C00:"main entry point",
    0x1C03:"main menu jump point",
    0x1C1F:"Mode 1, set palette (second VDU19 is unnecessary), turn off cursor and print main menu",
    0x1C66:"p (play)",
    0x1C6A:"a (analysis)",
    0x1C71:"q (quit)",
    0x1C75:"so 'quit' means simulate a Ctrl-Break to wipe the code completely",
    0x1C78:"r (replay)",
    0x1C7F:"b (blitz)",
    0x1C81:"none of the above = go back and wait for another keystroke",
    0x1C83:"set blitz=True (any non-0 value, $62 in this case)",
    0x1C85:"main menu Play entry point",
    0x1C87:"set replay move pointer to $(19)A2 i.e. clear list",
    0x1C8A:"and a copy here",
    0x1C8D:"and the MSB",
    0x1C9F:"start with move number = 1",
    0x1CA6:"main play loop",
    0x1CA9:"check if user plays white ($80) or black (0)",
    0x1CAB:"if white, let user go first",
    0x1CBC:"increment move number",
    0x1CC1:"ask for destination coordinates",
    0x1CC3:"dash (-)",
    0x1CC6:"get keypress, lower-case and print",
    0x1CCB:"immediate return if lower than digits",
    0x1CCF:"or higher than capital letters",
    0x1CD1:"convert to lower case",
    0x1CD6:"and return it",
    0x1CD7:"get keypress intercept Escape",
    0x1CDA:"Escape pressed?",
    0x1CDC:"if not, return character we read",
    0x1CDE:"clear the Escape condition",
    0x1CE6:"check key while clock running",
    0x1CE8:"osbyte $81 = INKEY, 10 centiseconds (0.1s) doubles as the clock timer",
    0x1CF1:"handles Escape",
    0x1CF6:"handles normal keypresses",
    0x1CF8:"tenths of a second column",
    0x1D04:"are we in Blitz mode?",
    0x1D06:"if not, don't have to move at 10secs",
    0x1D08:"strip inside-user's-turn return address from stack",
    0x1D09:"so it goes back to play loop and takes another computer turn",
    0x1D29:"read text cursor position",
    0x1D2E:"save cursor position",
    0x1D41:"dot (.) to separate seconds from tenths",
    0x1D4C:"print last clock digit and restore cursor position",
    0x1D51:"position cursor",
    0x1D5E:"print space and two clock digits",
    0x1D63:"print next two clock digits",
    0x1D64:"we use the top of the function keys area at 0BDF for clock readout string",
    0x1D6A:"print next clock digit",
    0x1D71:"clear clock string",
    0x1D7C:"roll clock counter column to 0 and advance next col",
    0x1D82:"advance clock column",
    0x1D85:"make sure there's a digit there",
    0x1D95:"inline string print",
    0x1D96:"get return address",
    0x1D99:"and store it as string address",
    0x1D9F:"branch always taken as Y=0 on init",
    0x1DA8:"($37 has wrapped to 0 if we get here)",
    0x1DAA:"load next character (Y=0 throughout, 6502 just didn't have a version that doesn't use X or Y)",
    0x1DAC:"go back and write it if high bit not set",
    0x1DB0:"continue execution after the string",
    0x1DCB:"'w'",
    0x1DCF:"'b'",
    0x1DD1:"loop until we get 'w' or 'b'",
    0x1DD3:"user plays black",
    0x1DD7:"user plays white",
    0x1DD9:"store user's colour in $68",
    0x1DDB:"check for blitz",
    0x1DDF:"force level 1 (no time to calculate more in blitz)",
    0x1DF2:"Default level number is 2 unless",
    0x1DF4:"input is less than '7' and",
    0x1DF8:"greater than or equal to '1'",
    0x1DFE:"in which case use inputted level instead",
    0x1DFF:"6F holds the level number",
    0x1E02:"board setup",
    0x1E08:"so ($60,$61) -> $1034 (the 10x10 board with borders)",
    0x1E0A:"write 120 x FF bytes (erases the board and attack/defence counts)",
    0x1E15:"so ($60,$61) -> $102C (inital back-rank pattern)",
    0x1E1D:"to store this piece on Black's back rank",
    0x1E21:"and change its colour to White",
    0x1E23:"to be stored on White's back rank",
    0x1E27:"put a pawn in front of it as well",
    0x1E29:"for Black",
    0x1E2D:"and a White pawn",
    0x1E2F:"for White",
    0x1E33:"and set the intervening squares to empty",
    0x1E35:"on the 6th rank",
    0x1E39:"and the 5th rank",
    0x1E3D:"and the 4th rank",
    0x1E41:"and the 3rd rank",
    0x1E4E:"writes to $10CE, since ($60,$61) has had 8 increments since $102C so it's $1034 and we set Y to $9A",
    0x1E53:"to $10CF, now ($10CE,$10CF) -> $195F",
    0x1E58:"to $10D0",
    0x1E5D:"to $10D1, now ($10D0,$10D1) -> $185E",
    0x1E60:"clear screen and draw board",
    0x1E62:"CLS",
    0x1E65:"draw board",
    0x1E9E:"plot square",
    0x1EB2:"set square colour/position",
    0x1ED7:"($60, $61) -> screen memory location of square",
    0x1EDD:"draw piece on square",
    0x1EE4:"A is now $67*10",
    0x1EE5:"rank*10+file",
    0x1EE8:"read board square (skipping top border)",
    0x1EEF:"no piece to draw -> return",
    0x1EF1:"X is now the piece type",
    0x1EF2:"sprite addr MSB: we'll increment it at least once to 0E",
    0x1EF9:"each sprite is $50 bytes",
    0x1F02:"($62,$63) -> sprite",
    0x1F12:"jump if we need to flip the sprite's colour to black",
    0x1F18:"effectively a JMP (the OR won't ever be 0 as background squares are red and green)",
    0x1F20:"write to screen memory",
    0x1F34:"update clock",
    0x1F51:"call Your move",
    0x1F7B:"clear 5 lines and position cursor",
    0x1F86:"move cursor to line 12",
    0x1F8E:"erase a line",
    0x1FA2:"user's turn",
    0x1FA8:"delete (the take-back key)",
    0x2009:"validate user's move (?)",
    0x2075:"delay loop",
    0x2079:"shorter delay loop",
    0x20AB:"check for Check",
    0x20CA:"generate attacks for current piece",
    0x21AE:"generate legal moves",
    0x21F0:"check occupancy of one destination square",
    0x22C8:"make a move",
    0x2353:"generate moves for piece (?)",
    0x23F9:"append to move list",
    0x245A:"en-passant availability check (?)",
    0x24C7:"castling availability check (?)",
    0x254A:"take back a move",
    0x25E8:"record and display move (?)",
    0x2620:"show and list move (?)",
    0x2622:"beep",
    0x2647:"append bytes to replay data",
    0x2685:"convert square to coordinates",
    0x2691:"print coordinates",
    0x269F:"computer's turn",
    0x272D:"main menu Analysis entry point",
    0x27D6:"'y'",
    0x27E0:"CLS",
    0x27E8:"set move number to 2 (skips opening book)",
    0x27FF:"'w'",
    0x280C:"check if user plays white ($80) or black (0)",
    0x280E:"and do the opposite",
    0x283F:"handle user takeback",
    0x2890:"opening book",
    0x28EB:"save analysis board",
    0x2909:"calculate computer move",
    0x290B:"are we on move 1?",
    0x2936:"load the level number",
    0x2955:"iterative search-node entry point",
    0x2957:"($70 is ply depth from root)",
    0x2960:"compare searched depth with level",
    0x2962:"if at max ply, skip move ordering (no point sorting moves we won't recurse past)",
    0x2967:"walk ordered legal moves",
    0x296F:"'read next move record' loop",
    0x297A:"second byte of move record is 0 -> end of list",
    0x297C:"copy move to stack",
    0x298D:"depth vs level number check",
    0x298F:"non-leaf: don't need extra king-safety verify",
    0x2997:"0 = not putting ourselves in check",
    0x299F:"test if depth==level",
    0x29A5:"are we giving check?",
    0x29A9:"check for Check on the side about to move",
    0x29AC:"not a checking move: terminal leaf",
    0x29AE:"Check extension: search one more ply",
    0x29B0:"reuse legality flag already computed for interior nodes",
    0x29B4:"score 0 (own king in check) skip",
    0x29B9:"flip side to move ($69)",
    0x29BF:"is side to move now White?",
    0x29C3:"increment move number",
    0x29C5:"copy node forward, opening slot before it (?)",
    0x29D2:"handle stalemate/checkmate/backtrack",
    0x29D4:"if moves found, skip no-moves logic",
    0x29D6:"No moves. Was side to move in check?",
    0x29D8:"If yes, jump to checkmate",
    0x29DA:"stalemate scores 128/255",
    0x29DC:"(effectively a JMP)",
    0x29DE:"checkmate found at this move number",
    0x29E0:"record it",
    0x29E2:"and score 255/255",
    0x29E4:"(effectively a JMP)",
    0x29E6:"check if at root",
    0x29E8:"with move list exhausted,",
    0x29EC:"if so, tree search is finished",
    0x2A00:"load this node's score",
    0x2A02:"push the move score",
    0x2A05:"mark this node has moves (not mate)",
    0x2A0A:"compare score with parent's best",
    0x2A0C:"for pruning",
    0x2A20:"if we're at root",
    0x2A22:"(i.e. depth==1)",
    0x2A26:"then move we found is new best-so-far",
    0x2A28:"so keep it",
    0x2A2E:"check if best root move",
    0x2A31:"is a forced mate",
    0x2A35:"if found forced mate, shorten search horizon by 2 plies for rest of game (won't get here if level is 1)",
    0x2A37:"(Bug: if user undoes a move that let computer see mate, rest of game gets 2 fewer search plies)",
    0x2A39:"parity correct mate move number from side to play",
    0x2A3F:"it's mate one move sooner",
    0x2A48:"main menu Replay entry point",
    0x2ADB:"replay clear from-square (?)",
    0x2AF1:"check for Check and mates",
    0x2AF5:"earlier found mate at this move number",
    0x2AF8:"is it the current move number?",
    0x2AFA:"if not, no mate yet",
    0x2B05:"was it computer or user that won?",
    0x2B09:"looks like it was computer",
    0x2B63:"call check",
    0x2B6F:"call mate",
    0x2B7C:"unmake move in search",
    0x2B86:"undoing Black's move, decrement move number",
    0x2B8E:"decrement ply-depth counter",
    0x2BAD:"insertion-sort move list by static eval", # probably didn't do this deliberately: the address 2BAD can be read as "too bad" i.e. which ones look too bad to search first
    0x2C23:"evaluate candidate move",
    0x2C2B:"putting ourselves in check breaks the rules",
    0x2C2D:"and scores 0",
    0x2C2F:"(effectively a JMP to skip evaluating putting ourselves in check)",
    0x2C3A:"clear the attack map (?)",
    0x2C4B:"build the attack map (?)",
    0x2C4D:"attack count = 0 (?)",
    0x2C55:"pointer = piece list (?)",
    0x2D1D:"static evaluator",
    0x2D1F:"material = 0 (?)",
    0x2D21:"positional = 0 (?)",
    0x2D23:"best capture value = 0 (?)",
    0x2D25:"highest attack = 0 (?)",
    0x2D27:"second-highest attack = 0 (?)",
    0x2D29:"king-under-attack flag = 0 (?)",
    0x2D35:"load board[square] (?)",
    0x2D39:"skip borders (?)",
    0x2D3B:"end of board (?)",
    0x2D3E:"piece data (with colour/flags) (?)",
    0x2D42:"piece type (?)",
    0x2D46:"pawn: skip positional, go to material (?)",
    0x2D4A:"knight or bishop: development check (?)",
    0x2D4E:"king: safety check (?)",
    0x2D50:"move number",
    0x2D54:"if < 7 moves (each) played, be positional for rooks/queens (?)",
    0x2D56:"else skip to material (?)",
    0x2D5B:"bit 4 = has-moved flag (?)",
    0x2D5D:"king hasn't moved: no bonus (?)",
    0x2D5F:"+6 for castled king (?)",
    0x2D63:"colour (?)",
    0x2D65:"white: add the +6 (?)",
    0x2D67:"black: add -6 (will be negated) (?)",
    0x2D75:"bit 3 = has-moved flag (?)",
    0x2D77:"already moved: no penalty (?)",
    0x2D79:"-2 penalty for undeveloped piece (?)",
    0x2D7D:"colour (?)",
    0x2D7F:"white: add -2 (?)",
    0x2D81:"black: add +2 (becomes -2 after negation) (?)",
    0x2D85:"positional += bonus/penalty (?)",
    0x2D8F:"load attack count for this square (?)",
    0x2D93:"subtract defender count (?)",
    0x2D97:"adjust the positional score accordingly (?)",
    0x2DA7:"is static exchange evaluation 0 or non-0? (?)",
    0x2DA9:"checks if exchange evaluator said piece is safe or lost (?)",
    0x2DAB:"if non-0, piece hangs, decrement piece value by 1 (?)",
    0x2DDB:"piece value (1, 3, 3, 5, 9) (?)",
    0x2DDD:"check colour (?)",
    0x2DDF:"white: add normally (?)",
    0x2DE1:"black: negate (?)",
    0x2DE7:"material += value (?)",
    0x2DF7:"king under attack? (?)",
    0x2DFB:"if so, shift attack values (?)",
    0x2E03:"best capture value (?)",
    0x2E0C:"highest attack (?)",
    0x2E10:"second-highest attack (?)",
    0x2E17:"/ 2 (?)",
    0x2E19:"attack_score = ($77-1)/2 - ($75-1) (?)",
    0x2E25:"+ material (?)",
    0x2E28:"- best_so_far_material (?)",
    0x2E2A:"material_diff (?)",
    0x2E2E:"clamp to +/-30 (?)",
    0x2E31:"clamped_material_diff (?)",
    0x2E33:"positional (?)",
    0x2E36:"- best_so_far_positional (?)",
    0x2E38:"positional_diff (?)",
    0x2E3A:"king under attack? (?)",
    0x2E40:"if king attacked, positional_diff = 0 (?)",
    0x2E44:"clamp to +/-6 (?)",
    0x2E47:"clamped_positional_diff (?)",
    0x2E49:"material_diff (?)",
    0x2E4C:"*2 (?)",
    0x2E4D:"*4 (?)",
    0x2E4F:"+ positional_diff (?)",
    0x2E51:"colour (?)",
    0x2E53:"black: skip negation (?)",
    0x2E55:"white: negate (?)",
    0x2E5B:"+128 bias (make positive) (?)",
    0x2E5D:"final score (?)",
    0x2E61:"store in move record (?)",
    0x2E64:"static exchange evaluator",
    0x2E92:"load piece value (1,3,3,5,9,10) (?)",
    0x2E94:"double it: this is the 'prize' (?)",
    0x2E95:"store current attacker threshold (?)",
    0x2E97:"initial defender value (?)",
    0x2E99:"get cheapest attacker from attack map (?)",
    0x2E9C:"if someone can capture, continue (?)",
    0x2E9E:"nobody can capture: piece is safe, $62 stays 0 (?)",
    0x2EA8:"doubled piece value (?)",
    0x2EAA:"compare with attacker value (?)",
    0x2EAC:"piece value >= attacker, capture is safe (?)",
    0x2F64:"write 1-8 rank legends on vertical sides of board",
    0x2FCA:"print $61 at X,Y",
    0x2FCF:"effectively JMP oswrch",
    0x2FD1:"cursor to X,Y",
    0x2FDE:"write a-h file legend at row Y",
    0x2FE3:"'a'",
    0x2FF8:"possibly a programmer's signature (or 8x8 sprite?)",
    0x3000:"Start of Mode 1 screen memory after relocation. This is where the disk version added its relocator loop.",
    0x3002:"It starts by doing the equivalent of *TAPE",
    0x3004:"to disable the DFS/ADFS:",
    0x300F:"relocating to $E00",
    0x3013:"relocating from $1E00",
    0x3026:"stop before source address $4000 (relocated address $3000)",
    0x302A:"This code copies 48 bytes into the cassette workspace at 3B0.  Since this is never read by the Chess program, I assume whoever wrote the disk relocator thought they'd better restore the CFS state as well just in case.  Almost certainly unnecessary.",
    0x302C:"$3050 in our relocated addresses",
    0x302F:"cassette BPUT workspace",
    0x3033:"stop at 48 bytes",
    0x3037:"*FX200 (apparently to",
    0x3039:"reset Break and Escape to normal",
    0x303B:"in case the BASIC loader set them differently)",
    0x3040:"flush buffers",
    0x3048:"padding (the relocator author didn't sign like someone apparently did at 2FF8)",
    0x3050:"these 48 bytes are copied to 3B0 (unnecessarily I think, see above)",
    0xFFE0:"osrdch (read character)",
    0xFFEE:"oswrch (write character)",
    0xFFF4:"osbyte (*FX)",
}

OPCODES = {
    0x00:("BRK",0),0x01:("ORA",8),0x05:("ORA",1),0x06:("ASL",1),
    0x08:("PHP",0),0x09:("ORA",11),0x0A:("ASL",12),0x0D:("ORA",4),
    0x0E:("ASL",4),0x10:("BPL",10),0x11:("ORA",9),0x15:("ORA",2),
    0x16:("ASL",2),0x18:("CLC",0),0x19:("ORA",6),0x1D:("ORA",5),
    0x1E:("ASL",5),0x20:("JSR",4),0x24:("BIT",1),0x25:("AND",1),
    0x26:("ROL",1),0x28:("PLP",0),0x29:("AND",11),0x2A:("ROL",12),
    0x2C:("BIT",4),0x2D:("AND",4),0x2E:("ROL",4),0x30:("BMI",10),
    0x31:("AND",9),0x35:("AND",2),0x36:("ROL",2),0x38:("SEC",0),
    0x39:("AND",6),0x3D:("AND",5),0x3E:("ROL",5),0x40:("RTI",0),
    0x41:("EOR",8),0x45:("EOR",1),0x46:("LSR",1),0x48:("PHA",0),
    0x49:("EOR",11),0x4A:("LSR",12),0x4C:("JMP",4),0x4D:("EOR",4),
    0x4E:("LSR",4),0x50:("BVC",10),0x51:("EOR",9),0x55:("EOR",2),
    0x56:("LSR",2),0x58:("CLI",0),0x59:("EOR",6),0x5D:("EOR",5),
    0x5E:("LSR",5),0x60:("RTS",0),0x61:("ADC",8),0x65:("ADC",1),
    0x66:("ROR",1),0x68:("PLA",0),0x69:("ADC",11),0x6A:("ROR",12),
    0x6C:("JMP",7),0x6D:("ADC",4),0x6E:("ROR",4),0x70:("BVS",10),
    0x71:("ADC",9),0x75:("ADC",2),0x76:("ROR",2),0x78:("SEI",0),
    0x79:("ADC",6),0x7D:("ADC",5),0x7E:("ROR",5),0x81:("STA",8),
    0x84:("STY",1),0x85:("STA",1),0x86:("STX",1),0x88:("DEY",0),
    0x8A:("TXA",0),0x8C:("STY",4),0x8D:("STA",4),0x8E:("STX",4),
    0x90:("BCC",10),0x91:("STA",9),0x94:("STY",2),0x95:("STA",2),
    0x96:("STX",3),0x98:("TYA",0),0x99:("STA",6),0x9A:("TXS",0),
    0x9D:("STA",5),0xA0:("LDY",11),0xA1:("LDA",8),0xA2:("LDX",11),
    0xA4:("LDY",1),0xA5:("LDA",1),0xA6:("LDX",1),0xA8:("TAY",0),
    0xA9:("LDA",11),0xAA:("TAX",0),0xAC:("LDY",4),0xAD:("LDA",4),
    0xAE:("LDX",4),0xB0:("BCS",10),0xB1:("LDA",9),0xB4:("LDY",2),
    0xB5:("LDA",2),0xB6:("LDX",3),0xB8:("CLV",0),0xB9:("LDA",6),
    0xBA:("TSX",0),0xBC:("LDY",5),0xBD:("LDA",5),0xBE:("LDX",6),
    0xC0:("CPY",11),0xC1:("CMP",8),0xC4:("CPY",1),0xC5:("CMP",1),
    0xC6:("DEC",1),0xC8:("INY",0),0xC9:("CMP",11),0xCA:("DEX",0),
    0xCC:("CPY",4),0xCD:("CMP",4),0xCE:("DEC",4),0xD0:("BNE",10),
    0xD1:("CMP",9),0xD5:("CMP",2),0xD6:("DEC",2),0xD8:("CLD",0),
    0xD9:("CMP",6),0xDD:("CMP",5),0xDE:("DEC",5),0xE0:("CPX",11),
    0xE1:("SBC",8),0xE4:("CPX",1),0xE5:("SBC",1),0xE6:("INC",1),
    0xE8:("INX",0),0xE9:("SBC",11),0xEA:("NOP",0),0xEC:("CPX",4),
    0xED:("SBC",4),0xEE:("INC",4),0xF0:("BEQ",10),0xF1:("SBC",9),
    0xF5:("SBC",2),0xF6:("INC",2),0xF8:("SED",0),0xF9:("SBC",6),
    0xFD:("SBC",5),0xFE:("INC",5)
}

def format_operand(mem,addr,mode):
    if mode==1: return f"${mem[addr+1]:02X}",2 # ZP
    elif mode==2: return f"${mem[addr+1]:02X},X",2 # ZP,X
    elif mode==3: return f"${mem[addr+1]:02X},Y",2 # ZP,Y
    elif mode==4: return f"${mem[addr+2]:02X}{mem[addr+1]:02X}",3 # ABS
    elif mode==5: return f"${mem[addr+2]:02X}{mem[addr+1]:02X},X",3 # ABS,X
    elif mode==6: return f"${mem[addr+2]:02X}{mem[addr+1]:02X},Y",3 # ABS,Y
    elif mode==7: return f"(${mem[addr+2]:02X}{mem[addr+1]:02X})",3 # IND
    elif mode==8: return f"(${mem[addr+1]:02X},X)",2 # (ZP,X)
    elif mode==9: return f"(${mem[addr+1]:02X}),Y",2 # (ZP),Y
    elif mode==10: # Relative
        offset = mem[addr+1]
        if offset > 127: offset -= 256
        target = (addr + 2 + offset) & 0xFFFF
        return f"${target:04X}",2
    elif mode==11: return f"#${mem[addr+1]:02X}",2 # Immediate
    elif mode==12: return "A",1 # Accumulator
    else: return "",1 # mode 0 implied

def disasm(mem):
    queue = [entryPoint]
    visited = set()
    code_lines = {}
    while queue:
        addr = queue.pop(0)
        if addr in visited or addr >= len(mem): continue
        op = mem[addr]
        if op in OPCODES: name,mode = OPCODES[op]
        else:
            print("Warning: code ran into unrecognised opcode at",hex(addr))
            continue
        operand,length = format_operand(mem,addr,mode)
        for L in range(length): visited.add(addr+L)
        hex_bytes = " ".join(f"{mem[addr+i]:02X}" for i in range(length))
        code_lines[addr] = f"${addr:04X}: {hex_bytes:<10} {name} {operand}".rstrip()
        # Add targets to queue
        if name in ("JMP","JSR") and mode==4: # Absolute
            target = mem[addr+2] << 8 | mem[addr+1]
            if target < 0xFF00: queue.append(target)
            if target in comments:
                code_lines[addr] += " ; "+name+" "+comments[target]
            
            # Special case: JSR $1D95 is the inline string printer
            # The next bytes are string data until we find top bit set
            if target==0x1D95:
                string_start = addr + 3
                string_end = string_start
                while (mem[string_end] & 0x80)==0:
                    visited.add(string_end)
                    string_end += 1
                queue.append(string_end) # the terminator itself is the next instruction (will be 0xEA NOP if the actual next instruction is <128)
                code_lines[addr] += f' with data {repr(mem[string_start:string_end])[len("bytearray(b"):-1]}'
                if mem[string_end]==0xEA and string_end not in comments: comments[string_end]="terminator for data"
                continue
        elif name in ("BPL","BMI","BVC","BVS","BCC","BCS","BNE","BEQ"): # Relative
            offset = mem[addr+1]
            if offset > 127: offset -= 256
            target = (addr + 2 + offset) & 0xFFFF
            queue.append(target)
        if not name in ["JMP","RTS"]: queue.append(addr + length)
    for missed in range(loadTo,len(mem)):
        if not missed in visited:
            missedEnd = missed
            while not missedEnd in visited and missedEnd<len(mem) and not (missedEnd>missed and (missedEnd%16==0 or missedEnd in comments)):
                visited.add(missedEnd)
                missedEnd += 1
            code_lines[missed] = f"${missed:04X}: data {repr(mem[missed:missedEnd])[len("bytearray(b"):-1].replace(chr(0x22),chr(0x5c)+'x22')}" # the .replace here is to be nice to Emacs' syntax highlighter in the .asm
    for addr,comment in list(comments.items()):
        if addr in code_lines:
            code_lines[addr] += " ; "+comment
        else: assert addr >= 0xFF00, "comment for unknown address "+hex(addr)
    return code_lines

if __name__=="__main__": main()
