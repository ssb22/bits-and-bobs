
from https://ssb22.user.srcf.net/game/bchess.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/game/bchess.html) just in case)

# Solving Micropower Chess (1982)


I’m only an intermediate player (Elo perhaps 1500 if given enough time), but I did once checkmate some software that “Micro Power” released in 1982 for the then very new BBC Micro Model B (which it ran in screen mode 1)—and as this program *always* replied to a given sequence of moves in the same way (no random factor), any win against it can be repeated every time and therefore counts as having “weakly solved” that level. I first did this by lasting as long as I could with equal-material exchange, knowing that microcomputers of the time were more likely to play badly in the endgame, but it turns out there are considerably shorter solutions.

## Confusion about level numbers

MicroPower released *three* versions of Chess that ran on the BBC Micro:
1. a tape version in 1982, with 6 levels numbered 1 through 6;
2. a tape “Electron” version in 1983, with levels 1, 3, 5, 7 and 9 identical to the first 5 levels of the 1982 version, plus new ‘in-between’ levels that introduced randomness;
3. a BBC Micro *disk* version (which is what my school had)—this is the 6-level 1982 version plus a relocation loop, but they confused us by adding a loader that explains how level-numbering works **on the Electron version** (oops!) leading us to believe the highest level was 9 when it wasn’t.

This wouldn’t have been so bad if it weren’t for how the response to the “Level?” question is handled by the 1982 version—you’ll find the relevant 6502 code at RAM address `&1DF2` (or `&2DF2` before relocation)—if the key pressed does not fall between digits 1 and 6, it just **sets it to 2** without saying anything.

So if you read the loader instructions as I did, you’ll think “best play” is Level 9, but when you choose Level 9 *you will get Level 2* (equivalent to Level 3 on the Electron version).

## Long solution to Level 2

This was my first solution, in 89 moves (I could have checkmated on move 47 but then we wouldn’t have seen an empty-board endgame); the computer made striking mistakes on moves 45, 67 and 76. The program was set to control the Black pieces, and I thought I was playing “Level 9” as I didn’t know about the above level-numbering mix-up. (On the other hand, the *real* best-play levels are so slow they make only a few moves per day, and I doubt anyone would have let me run a computer for long enough to reach an endgame at *that* speed.)

Moves with discussion and screenshots:
1. `e2e4` `e7e5` These notes use the simplified algebraic notation that the BBC Micro Chess program accepts as move input. If you make a mistake, there is a one-move take-back facility—press Delete after the computer’s reply—but it does have bugs (it doesn’t decrement the move number, and strange things happen on move 1 as described below). Or you can start again and supply the same moves until the part you want to change (you can type up to 7 moves into the BBC’s 31-keystroke buffer while it’s processing). The program has a one-move “opening book”: it immediately responds `e5` if white first moves the `a`, `c` or `e` pawn, or `d5` if white makes any other move, and it opens with `e4` if itself playing white (the Electron version can also open with `d4`). There is a bug if you press Delete at this point: as white, you can repeat your move and *not* get the opening-book response (it’ll usually give you a knight’s move instead); as black, pressing Delete before making any moves can cause the computer to take back its e4 and let *you* move first, or cause stranger things to happen if this isn’t your first game in the session. But let’s accept the e5 and continue:
2. `g1f3` `b8c6`
3. `f1b5` `d8f6` I don’t usually bother putting a bishop there because black can just chase it around with pawns, but it’s supposed to be a good response to the knight (Ruy Lopez opening). The computer responded by getting its queen out a bit early (Frankfort Gunderam Var response)—if this queen move had been played on move 2 it *would* have been the Greco Defence, which Greco himself in 1620 suggested responding to by putting a bishop on e4, which in our case would mean 4. `b5c4` `f6g6`, 5. `e1g1` (O-O) `g6e4`, 6. `c4f7` `e8e7` (if the king were to take that bishop instead of moving, the white knight would then be able to fork king and queen), 7. `f1e1` (threatening the queen) `e4f4`, but then we’d run into problems because Greco’s 8. `e1e5` gets c6xe5—there wasn’t a knight on c6 in Greco’s version.
4. `b1c3` `a7a6` “putting the question to the bishop”
5. `b5c4` `b7b5` ditto. Now if `c4d5`, black responds with `b5b4` and threatens the c3 knight and it won’t be able to go to d5, so let’s put the knight on d5, threaten the queen and see where it goes.
6. `c3d5` `f6d6` probably to defend against the d5xc7 check that would have won the rook
7. `c4b3` `g8f6` I thought I might as well save that bishop for later. Black’s going in for a knight exchange makes sense so that its queen can become more mobile again; this also threatens to take the pawn on e4 which is not defended—it can do that first and *then* go back to f6 for the exchange, so I suppose I’d better defend e4 on my next move.
8. `d2d3` `f6d5` starting the knight exchange
9. `b3d5` `f8e7` ![bchess9.png](https://ssb22.user.srcf.net/game/bchess9.png) I supposed that taking it with the bishop gives me a slightly more interesting position than taking it with the pawn. The computer then prepared to castle, which makes sense to get out of what my bishop might be threatening.
10. `e1g1` `e8g8` we might as well both castle
11. `f3g5` `c8b7` I was ganging up on f7, and the computer un-pinned its c6 knight: if it moves now, it’ll leave a discovered attack on the bishop and the resulting exchange will leave a pawn undefended
12. `d1f3` `c6d4` I was still thinking about f7. Computer is threatening the exchange and the queen.
13. `d5f7` `g8h8` computer made the only sensible response
14. `f3h5` `h7h6` to avert my threatened checkmate on h7 and to threaten the knight
15. `g5f3` `d4c2` I no longer needed that knight to be on g5 to defend the bishop now the queen has that job; computer picked off a pawn that would have been defended by the queen before the queen was moved out
16. `a1b1` `g7g5` I just moved that rook out of the way of its attack
17. `c1g5` `e7g5` I just thought let’s try some more exchanges
18. `f3g5` `h8g7` so we swapped bishops and I’m no longer a pawn down; its h6 pawn is no longer pinned to the king, and now my g5 knight is in trouble and if I move it I won’t have enough pieces on f7 to save the bishop
19. `f7b3` `d6d3` to get my bishop out of the way and threaten its knight in exchange for mine; it defended. At this point 20. `f1d1` would have won the black queen (there’d be nowhere for it to go), but I wasn’t looking for exchanges *that* ambitious so I didn’t see it, and instead played:
20. `f2f3` `d3e3` ![bchess20.png](https://ssb22.user.srcf.net/game/bchess20.png) thinking I should defend e4 after my knight was gone. Then it checked me, basically to defend g5 after it takes the knight, otherwise I’d be able to take its g5 and e5 pawns while calling check, which it presumably values more than its knight on c2
21. `g1h1` `h6g5` took the knight as I thought
22. `b3c2` `e3d2` I might as well complete the exchange. Computer threatened the bishop again.
23. `b1c1` `f8h8` I might as well defend the bishop. Computer then threatened the queen.
24. `h5g4` `a8f8` I’m not sure what that rook move was supposed to prevent. I left my h2 pawn in potential trouble, but at least I’m defending g2.
25. `c2b3` `b7c6` I was leaving b2 vulnerable but covering the g8 area might be more useful. This computer response was presumably to put another defending piece on d7 to free up the black queen to take my newly-vulnerable b2; this also means advancing its a6 pawn to a4 would trap the bishop on the entire diagonal; if `a2a4` then `b5a4` `b3a4` `c6a4` loses a pawn.
26. `b3d5` `c6d5` ![bchess26.png](https://ssb22.user.srcf.net/game/bchess26.png) if I’m *going* to have an exchange that leaves me a pawn down, I’d rather have *this* one as it might leave a slightly better position
27. `e4d5` `d7d6` I was expecting its queen to take the undefended pawn on d5; it must have evaluated its queen being more useful where it was
28. `g4e6` `f8f7` to stop the white queen from doing too much damage in that corner (white’s move can be done seeing as black’s D pawn has advanced)
29. `c1b1` `d2f4` I was just defending. Computer threatens mate on h2.
30. `h1g1` `f4h2` it checks anyway just to get a pawn, leaves me only one legal move to make
31. `g1f2` `h2h4` another check: could be perpetual if I went back to g1; playing g3 would lose the pawn after h2+
32. `f2e3` `h4d4` check, leaves only one escape square
33. `e3e2` `d4c4` again this is danger of perpetual check
34. `e2d2` `f7f6` threatening the queen
35. `e6e7` `g7g6` my check was basically just to remove the queen from immediate danger
36. `d2e3` `f6f8` ![bchess36.png](https://ssb22.user.srcf.net/game/bchess36.png) My a2 and d5 pawns were forked and there’s not a lot I could do about it, but at least this meant Qxe5 wouldn’t be a check and I’d be able to respond by taking c7. I’m not sure why it responded as it did.
37. `a2a3` `f8e8` There wasn’t much hope for my a pawn, but I could take it out of the *immediate* line of fire. Computer responded by attacking the queen, but easily sidestepped:
38. `e7d7` `c4d4` (check, left me with only one legal move)
39. `e3e2` `d4c4` (are we going back to perpetual check?)
40. `e2e3` `c4d4` (yes it seems so)
41. `e3e2` `d4c4` (I don’t think the program implements any penalty for repetition, so *I’d* better be the one to do something else)
42. `e2f2` `c4c5` What’s the point of checking *there*? It could be a ‘horizon effect’—filling up the search tree with checks pushes back negative outcomes to beyond the number of moves being looked at.
43. `f2g3` `b5b4` it’s a pawn up so it can afford the exchange
44. `f1c1` `c5d5` I played a “waiting move”, albeit one forcing the queen to do something
45. `c1c7` `d5d3` ![bchess45.png](https://ssb22.user.srcf.net/game/bchess45.png) My 2 rooks on the first rank had been very useful up until now, but I’d rather have 2 pieces down the far end of the board for more checks etc. Computer responded by threatening the other rook now that I’ve moved one of them away, and also attacking the a3 square so it can open that file after exchanging its b pawn. This was a mistake on its part, because it gave me a mate in two (which I missed: I played the Qf7+ correctly on move 46 but then didn’t do the Rh1#); it could have averted this checkmate by leaving its queen where it was, perhaps playing Reg8 to also prevent Qg7+ Kf5 Rf7+ QxR QxQ# (or Ke6 Qf6#).
46. `d7f7` `g6h6` black king is forced to the edge, restricting the mobility of black’s h rook. I then had a mate in one (47. `b1h1` would be an immediate win), but I didn’t notice, so play continued:
47. `b1c1` `g5g4` I just thought I might as well move that rook out of trouble now. Too bad I was thinking too much about the c file to notice where *else* I could have put it—but on the other hand if I *had* ended the game at this point we wouldn’t have seen the computer’s two spectacular endgame mistakes later. Meanwhile, after the computer’s g4, if Kxg4 Qd4+ Kf5 then one of the two black rooks could attack the queen while pinning it against the king, so I didn’t do *that*, but again I missed the quick win with the white rook (Qg7+ Kh5 Rh1#) and instead played:
48. `g3h4` `d3g6` to parry my threat of Qg7# by offering a queen exchange; I’m a pawn down but I suppose I can still take it as I’ll win the pawn on g4 afterwards
49. `f7g6` `h6g6` discovered check from the rook
50. `h4g4` `b4a3` it’s exchanging those pawns also, but won’t be able to unblock the a file as easily as it could when its queen was on the board
51. `b2a3` `e8d8` now aiming to protect its d and e pawns?
52. `f3f4` `e5f4` it still exchanges that one
53. `g4f4` `d8f8` I’m not entirely sure why it’s checking *there*
54. `f4e4` `f8f2` obviously it values taking that pawn...
55. `c1c2` `f2c2` ...but when I offered a rook exchange instead, it accepted
56. `c7c2` `h8e8` again a check that’s buying it time?
57. `e4d5` `e8e3` looks like it’s given up on its d pawn and wants to clear the way for the a pawn
58. `d5d6` `e3d3` ![bchess58.png](https://ssb22.user.srcf.net/game/bchess58.png) check? why not just get on with taking a3?
59. `d6c5` `d3a3` Thought so. Modern 6-piece endgame tablebases say this position is drawn with perfect play on both sides, but we didn’t have those when I played this game. We do indeed draw if I play 60. `g2g4`, because play continues ...`g6g5` 61. `c2c4` (defending) `a3g3` (taking it and exchanging rooks would leave it with a king-and-pawn endgame, but the white king is positioned to easily capture the pawn resulting in a draw) 62. `c4a4` `a6a5` (for what it’s worth?) 63. `c5b5` `g3g4` 64. `a4a5` leaving king and rook versus king and rook, which is a theoretical draw, and although early microcomputer Chess programs were known for being poor at endgames until tablebases came along, MicroPower is easily able to keep up *this* draw, in some cases forcing exchange of rooks leaving two lone kings (e.g. 64 ...`g4h4` 65. `b5c6` `g5f6` 66. `a5a6` `h4h5` 67. `c6d7` `f6g7` 68. `a6a7` `h5h6` 69. `d7e8` `g7g8` 70. `a7e7` `h6h5` 71. `e7f7` `h5h6` 72. `e8e7` `h6h7` 73. `f7h7` `g8h7`)—it’s not programmed to declare the draw even then; it’ll just carry on moving its king around the board indefinitely. Or you can keep the rooks on the board and do 70. `e8d8` `h6h5` 71. `a7e7` `g8f8` 72. `e7d7` `h5h6` 73. `d8c8` `f8e8` 74. `d7c7` `h6b6` 75. `c7a7` `b6e6` 76. `c8b8` `e6e7` 77. `a7a1` `e8f7` 78. `a1f1` `f7g6` 79. `f1g1` `g6f5` 80. `b8c8` `f5f6` 81. `c8d8` `e7g7` 82. `g1f1` `f6e5` 83. `f1f8` `e5d6` 84. `f8f6` `d6e5` 85. `f6h6` `e5d4` 86. `h6d6` `d4c5` 87. `d6a6` `c5b5` 88. `a6a1` `b5c6` 89. `d8e8` `g7h7` and so on ad nauseam.
60. `c5b6` `a3a4`
61. `g2g3` `a4a3`
62. `c2g2` `g6g7`
63. `g3g4` `a3a4`
64. `g2g1` `g7f6` why? I’d just played a “waiting move” but I wasn’t expecting *that*
65. `g4g5` `f6g6` blocking
66. `g1g3` `a4a2` looks like we both played “waiting moves”
67. `g3g4` `g6f5` attacking the rook. This is a mistake, as I can sacrifice that rook for a guaranteed promotion. Modern tablebases agree: after this move, the result of perfect play changes from “draw” to “white mates in 36”.
68. `g5g6` `f5g4` ![bchess68.png](https://ssb22.user.srcf.net/game/bchess68.png)
69. `g6g7` `a2b2` check (I thought this was a horizon effect, but modern tablebases say it’s actually black’s best move and white mates in 34)
70. `b6a6` `b2a2` and modern tablebases say this position is drawn—that taking the pawn was a mistake that turned a “book win” into a “book draw” and I should instead have played Ka7 (playing the tablebases against a BBC emulator gives 70. `b6a7` `b2b8`? 71. `a7b8` `g4f5` 72. `g7g8` `f5f6` 73. `g8d5` `f6e7` 74. `b8c7` `e7f6` 75. `c7d7` `f6g7` 76. `d7e6` `g7f8` 77. `d5g5` `a6a5` 78. `g5g6` `a5a4` 79. `g6f7`# the poor BBC didn’t stand a chance, but I didn’t have the tablebases and stupidly did 70. `b6a6` instead)—but we’ll see it needs a better adversary than the 1982 BBC Micro to obtain a draw from this position. To begin with, the BBC has to keep me in check or I’m going to queen, but it can’t do so forever:
71. `a6b7` `a2b2` I covered the a8 square so it can’t go up there
72. `b7c7` `b2c2`
73. `c7d7` `c2d2`
74. `d7e7` `d2e2`
75. `e7f7` `e2f2`
76. `f7g6` `f2f6` and here we have the BBC’s second great mistake of this endgame. A desperate sacrifice of a rook for just a check? It would definitely have been better to save that rook. Did the minimax code ran out of memory or something? Four-piece tablebases agree: this computer’s move changes the evaluation from “draw” to “white mates in 9”. The most obvious way for it to save the draw would have been `f2g2` and `g4f3`—in either order—there are no two responses I can make to prevent its rook capturing my pawn or queen on the third move of that line; the best I can do is make it an exchange and we end up with two lone kings. Preferring `f2f6` to this seems like a search of 3-ply. Its Qd3 mistake on move 45 also suggests a 3-ply search, but it’s hard to see how some of its *other* moves were searched at only 3-ply. Perhaps it has a variable search depth (I’m not sure what would trigger it to search deeper), or it might be fixed at 3-ply but with extra evaluation heuristics to make it seem stronger in certain types of position (but not this one). We’d need some source code to know for sure.
77. `g6f6` `g4f3` ![bchess77.png](https://ssb22.user.srcf.net/game/bchess77.png)
78. `g7g8` `f3e4` It’s just as well I wanted a queen, as under-promotions are not supported by this program. Checkmate should be easy now, but I still have to *do* it. If this program doesn’t recognise a king-versus-king draw, I wouldn’t expect it to implement any resignation etiquette. Three-piece tablebases say my next play could have been Qd8 to mate in 7, but I was using a simpler heuristic so I called check instead:
79. `g8g4` `e4d5` and the tablebase says I could then have played Qb4 to mate in 5, but I didn’t see that, so once again I called check:
80. `g4e6` `d5d4`
81. `e6e5` `d4d3` and twice the tablebase figuratively tried to whisper back through time “c5 would have been quicker”, but I wasn’t listening,
82. `f6f5` `d3c4`
83. `f5e4` `c4b3` for once I played a move the tablebase says is best i.e. leads to the fastest mate
84. `e5d4` `b3c2`
85. `d4d3` `c2b2`
86. `e4d4` `b2c1` and I agreed with the tablebase again (pity about the in-between moves where I didn’t)
87. `d3e2` `c1b1` ![bchess87s.png](https://ssb22.user.srcf.net/game/bchess87s.png) I had to be careful here: if I had played Kc3 instead of this move, it would have been stalemate. Tablebases agree Qe2 led to the quickest mate from here, in 3 half-moves.
88. `d4c3` `b1c1`
89. `e2c2`# ![bchess89.png](https://ssb22.user.srcf.net/game/bchess89.png)

Same game in PGN:
* 1. e4 e5 2. Nf3 Nc6 3. Bb5 Qf6 4. Nc3 a6 5. Bc4 b5 6. Nd5 Qd6 7. Bb3 Nf6 8. d3 Nxd5 9. Bxd5 Be7 10. O-O O-O 11. Ng5 Bb7 12. Qf3 Nd4 13. Bxf7 Kh8 14. Qh5 h6 15. Nf3 Nxc2 16. Rb1 g5 17. Bxg5 Bxg5 18. Nxg5 Kg7 19. Bb3 Qxd3 20. f3 Qe3 21. Kh1 hxg5 22. Bxc2 Qd2 23. Rbc1 Rh8 24. Qg4 Raf8 25. Bb3 Bc6 26. Bd5 Bxd5 27. exd5 d6 28. Qe6 Rf7 29. Rb1 Qf4 30. Kg1 Qxh2 31. Kf2 Qh4 32. Ke3 Qd4 33. Ke2 Qc4 34. Kd2 Rf6 35. Qe7 Kg6 36. Ke3 Rff8 37. a3 Re8 38. Qd7 Qd4 39. Ke2 Qc4 40. Ke3 Qd4 41. Ke2 Qc4 42. Kf2 Qc5 43. Kg3 b4 44. Rfc1 Qxd5 45. Rxc7 Qd3 46. Qf7 Kh6 47. Rbc1 g4 48. Kh4 Qg6 49. Qxg6 Kxg6 50. Kxg4 bxa3 51. bxa3 Rd8 52. f4 exf4 53. Kxf4 Rdf8 54. Ke4 Rf2 55. R1c2 Rxc2 56. Rxc2 Re8 57. Kd5 Re3 58. Kxd6 Rd3 59. Kc5 Rxa3 60. Kb6 Ra4 61. g3 Ra3 62. Rg2 Kg7 63. g4 Ra4 64. Rg1 Kf6 65. g5 Kg6 66. Rg3 Ra2 67. Rg4 Kf5 68. g6 Kxg4 69. g7 Rb2 70. Kxa6 Ra2 71. Kb7 Rb2 72. Kc7 Rc2 73. Kd7 Rd2 74. Ke7 Re2 75. Kf7 Rf2 76. Kg6 Rf6 77. Kxf6 Kf3 78. g8=Q Ke4 79. Qg4 Kd5 80. Qe6 Kd4 81. Qe5 Kd3 82. Kf5 Kc4 83. Ke4 Kb3 84. Qd4 Kc2 85. Qd3 Kb2 86. Kd4 Kc1 87. Qe2 Kb1 88. Kc3 Kc1 89. Qc2#

In more modern times I tried a similar technique on Magnus Carlsen’s 2014 iOS app and narrowly beat “age 10” (which is different from Magnus’s real age 10: Tord Romstad set progress more ‘linear’ when tuning his Stockfish predecessor for the app)—it let me win an otherwise-drawn endgame by responding to move 78 inaccurately. These games are not usually reproducible as the engine adds a random factor, but here it is for reference:

Moves as PGN:
* 1. e4 c6 2. Nf3 d5 3. Bd3 dxe4 4. Bxe4 Nf6 5. Nc3 b5 6. Bd3 g6 7. O-O a5 8. Re1 Bg7 9. a4 b4 10. Ne4 Nd5 11. c3 f5 12. Nc5 Qd6 13. Nb3 O-O 14. c4 Nf4 15. Bc2 Nd3 16. Bxd3 Qxd3 17. c5 f4 18. Ne5 Bxe5 19. Rxe5 Re8 20. Qf3 Qxf3 21. gxf3 h6 22. d4 g5 23. Bd2 Kf7 24. Kg2 Ra7 25. Rae1 e6 26. Rd1 Rh8 27. Rde1 Kg8 28. Rd1 Kf7 29. Rde1 Rg8 30. Rd1 Nd7 31. Re4 h5 32. h3 Nf6 33. Re5 Nd7 34. Re4 Ra8 35. Rde1 Nf6 36. Re5 Nd5 37. Rd1 Ra7 38. Rde1 Rg6 39. Rd1 Bd7 40. Rde1 Ra8 41. h4 Kf6 42. hxg5+ Rxg5+ 43. Rxg5 Kxg5 44. Re5+ Kh6 45. Kh3 Kg6 46. Kh4 Ne7 47. Bxf4 Nf5+ 48. Kh3 Bc8 49. Nd2 Kf7 50. Ne4 Nxd4 51. Nd6+ Kg7 52. Nxc8 Rxc8 53. Rxh5 Nf5 54. Rg5+ Kf6 55. Kg2 Ra8 56. Kf1 Nd4 57. Kg2 Rh8 58. Kg3 Ne2+ 59. Kg4 Nxf4 60. Kxf4 Rh1 61. Rg8 Rh4+ 62. Ke3 Rc4 63. f4 Rxc5 64. Rc8 Rc2 65. b3 Rc1 66. Ke4 Rc3 67. Rf8+ Ke7 68. Rc8 Rxb3 69. Rxc6 Rb1 70. Ra6 Ra1 71. Rxa5 Ra2 72. f3 Kf7 73. Kd3 Kf6 74. Kc4 Ra3 75. Kxb4 Rxf3 76. Rc5 Rxf4+ 77. Kb5 Rf2 78. a5 Kg7 79. a6 Rb2+ 80. Ka5 Kf6 81. a7 Ra2+ 82. Kb6 Rxa7 83. Kxa7 Kg7 84. Re5 Kf7 85. Kb6 Kf6 86. Re1 Ke7 87. Kc5 Kd7 88. Kd4 Kd6 89. Ke4 Kc5 90. Ke5 Kc6 91. Kxe6 Kc5 92. Rd1 Kb4 93. Kd5 Kb3 94. Rc1 Ka3 95. Kc4 Kb2 96. Rc3 Ka1 97. Kb3 Kb1 98. Rc2 Ka1 99. Rc1# 1-0

## Fishing-Pole Trap

In the BBC Micro days I had no way of knowing about Brian Wall’s “fishing-pole trap” operated by black (open with knights and sacrifice one on g4 to expose white’s castled king)—I don’t think it was published before the 21<sup>st</sup> century (unless someone discovered it independently). Experimenting on an emulator shows the BBC Micro’s Level 2 *is* vulnerable to this trap and it reduces the game length to 14 moves, which is rather fewer than I originally took:

> **1.**  e4 e5 **2.**  Nc3 Nf6 **3.**  Nf3 Nc6 **4.**  Bc4 Bc5 **5.**  O-O Ng4? (setting the trap) **6.**  Na4 Bd6 **7.**  h3 h5? **8.**  hxg4?? (falling for the trap) hxg4 **9.**  Nh2?? (falling much further in) Qh4 **10.**  Bxf7+ Kxf7 **11.**  f3? g3 **12.**  Re1 Qxh2+ **13.**  Kf1 Nd4 **14.**  c3 Qh1#

This also works on the Electron version’s Level 3 *if* it starts with e4 not d4. It does not work on higher levels.

## Using modern engines

The shortest game I found against an *unassisted* modern engine was 16 moves, with MicroPower level 2 controlling the white pieces against 2002’s Sjeng 11 (the engine behind Apple Chess) in a mid-level mode:

Moves:

**1.**  e4 e5 **2.**  Nc3 Nf6 **3.**  Nf3 Nc6 **4.**  Bc4 Bc5 **5.**  O-O d6 **6.**  Ng5 O-O **7.**  Nxf7 Rxf7 **8.**  Bxf7 Kxf7 **9.**  Qe1 Nd4 **10.**  Qd1 (?) Bg4 **11.**  f3 Nxf3+ **12.**  Kh1 Nxh2 **13.**  Rxf6+ (??) Qxf6 **14.**  Qe1 Nf3 **15.**  gxf3 Qxf3+ **16.**  Kh2 Qh3#

Increasing the play-level of Sjeng (or using Don Dailey et al’s Komodo 9) or decreasing the play-level of the BBC Micro made the game 5 to 8 moves *longer* (although the modern engine still won of course).

I was able to reduce this to 14 moves as white by manually playing an unusual opening until the computer put its king in a risky place (misfired heuristic?), then letting a modern engine “do the honours” from move 8:

> **1.**  g3 d5 **2.**  Bh3 Be6 **3.**  Bxe6 fxe6 **4.**  Nf3 Nc6 **5.**  O-O Nf6 **6.**  d4 Kf7? **7.**  Ng5+ Kg6? **8.**  Qd3+ Ne4 **9.**  h4 e5 **10.**  h5+ Kxh5 **11.**  Qf3+ Kg6 **12.**  Qf7+ Kh6 **13.**  Nxe4+ g5 **14.**  Bxg5#

and then a couple of manual experiments shortened this still further, to a 12-move game that (oddly enough) gives discovered checkmate by ‘pawn to king 4’:

> **1.**  `g2g3` `d7d5` **2.**  `f1h3` `c8e6` **3.**  `h3e6` `f7e6` **4.**  `g1f3` `b8c6` **5.**  `h1g1` `g8f6` **6.**  `d2d4` `e8f7` **7.**  `f3g5`+ `f7g6` **8.**  `h2h4` `d8c8` **9.**  `h4h5`+ `g6h5` **10.**  `g3g4`+ `h5h4` **11.**  `g1h1`+ `h4g4` **12.**  `e2e4`#

![e4mate.png](https://ssb22.user.srcf.net/game/e4mate.png) This works on Level 2, but meets a different response on Level 1 that requires another half-dozen moves to win.

If the exact algorithm is known for a deterministic weaker engine then I suppose a stronger engine could be “tuned” to win faster by laying ‘traps’—non-best moves that result in this particular opponent making an even bigger mistake—by modifying the minimax algorithm in the stronger engine to prune out lines the weaker engine wouldn’t *choose* (e.g. never mind “10. g4 is not as good as Qd3 because the black king *could* go back to g6 and escape our forced mate in 4” if we know it’ll actually go to h4 and we mate in 3). This would probably amount to emulating the weaker engine (with its different static evaluator and search depth) at every candidate ‘opponent to move’ position *instead* of doing alpha-beta pruning (because alpha-beta pruning is not applicable to trees where there’s only ever one opponent move), but you might want to limit this “trap pruning” to upper levels of the tree (probably down to at most the difference between the two engines’ ply depths), and there’ll be places where the simulation of the weak engine can be optimised.

## Higher levels

Now we know I was actually playing Level 2 (not 9), I suppose for completeness I should also post solutions to the actual higher levels (I took some hints from modern engines to save time).

Moves:
* Level 3 (Electron level 5): 1. e2e4 e7e5, 2. d2d4 d8f6, 3. d4e5 f8b4+, 4. c2c3 f6e5, 5. c3b4 e5e4+, 6. d1e2 e4e2+, 7. f1e2 b8c6, 8. a2a3 g8f6, 9. g1f3 O-O, 10. e1g1 f8e8, 11. b1c3 d7d6, 12. c1g5 c8d7, 13. g5f6 g7f6, 14. f1e1 g8g7, 15. e2d3 a8c8, 16. e1e4 e8e4, 17. d3e4 f6f5, 18. e4d5 c8e8, 19. c3b5 e8e2, 20. a1b1 a7a6, 21. b5c7 f5f4, 22. g1f1 e2e7, 23. b1e1 e7e1+, 24. f1e1 g7f6, 25. e1d2 f6g7, 26. f3g5 f7f6, 27. g5e4 c6d4, 28. d5b7 f6f5, 29. e4d6 d4b5, 30. d6b5 a6b5, 31. b7a6 d7c6, 32. f2f3 g7f6, 33. a6b5 c6b5, 34. c7b5 f6e7, 35. b5d4 e7f6, 36. b4b5 f6e5, 37. b5b6 e5d4, 38. b6b7 d4c5, 39. b7b8 c5d5, 40. b8b6 h7h5, 41. b2b3 d5e5, 43. b6c6 h5h4, 43. h2h3 e5d4, 44. c6d6#
* Level 4 (Electron level 7): 1. e2e4 e7e5, 2. d2d4 e5d4, 3. c2c3 d8e7, 4. f1d3 b8c6, 5. g1f3 d7d5, 6. e1g1 d5e4, 7. d3e4 d4c3, 8. b1c3 g8f6, 9. e4c6 b7c6, 10. d1a4 a8b8, 11. f1e1 c8e6, 12. f3e5 e7b4, 13. a4c6 e8d8, 14. e5f7 e6f7 (oops I wasn’t paying attention, carried on anyway as the game was likely recoverable), 15. e1d1 f8d6, 16. c1g5 h7h6, 17. g5f6 g7f6, 18. c3e4 d8e7, 19. e4d6 c7d6, 20. c6c7 e7f8, 21. d1d6 b4b2, 22. a1d1 f8g7, 23. d6d7 b2a2, 24. c7g2 g7h7, 25. h2h4 h8c8, 26. g3f4 h7g7, 27. d7d3 a2e6(?), 28. d3e3 e6c6, 29. d1d6 c6c1+, 30. g1h2 c1c4, 31. f4f6 g7g8, 32. e3g3 g8f8, 33. d6d7 c4e6, 34. f6h8 f7g8 (still takes time because the engine *evaluates* every candidate move even when there’s only one option), 35. g3g8 e6g8, 36. h8f6 f8e8, 37. f6e7#
* Level 5 (Electron level 9): 1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. O-O Nxe4 5. d4 exd4 6. Re1 f5 7. Nxd4 Bc5 8. Rxe4+ fxe4 9. Qh5+ g6 10. Qxc5 Qe7 11. Qc3 Rf8 12. Bh6 Rf7 13. Bc4 g5 14. Nb5 d5 15. Bxd5 Rb8 16. Qh8+ Kd7 17. Bxf7 Qxf7 18. N1c3 a6 19. Rd1+ Ke6 20. Nxe4 Kf5 21. Nbd6+ cxd6 22. Nxd6+ Kg6 23. Nxf7 Kxf7 24. Rd6 Bf5 25. Qg7+ Ke8 26. Qf8#
* Level 6 (no Electron level): First 6 moves same as Level 5, then: 7. Nxd4 Qf6 8. Bxc6 dxc6 9. f3 c5 10. Nb5 Qb6 11. N1c3 c4+ 12. Be3 Qc6 13. fxe4 fxe4 14. Qh5+ Kd8 15. Bg5+ Be7 16. Bxe7+ Kxe7 17. Nd5+ Kf8 18. Rf1+ Qf6 19. Rxf6+ gxf6 20. Qh6+ Kf7 21. Qxf6+ Kg8 22. Ne7#

## Default “Replay” game

MicroPower’s “Replay” feature normally plays back the last-played game. The limit is 150 moves each (actually it’s 303 ply but castling counts as 2½ ply); Replay also has display bugs if you’ve played 130-odd moves and left the game unfinished.

If you choose Replay *before* any game has been played, it gives you a 41-move sample game that seems incomplete. Moves are stored in RAM at `&19A0` (relocated from `&29A0`, from file `CHESS` offset `BA0`, from disk-image offset `1FA0`); the first two bytes point to the next free slot, then start and destination squares are encoded as `10*(rank+1)+file` where `rank` and `file` start at 1; for castling the king’s move is coded first and then the rook’s after a byte `01`.

This turns out to be a copy of Fischer versus Spassky, Reykjavik world championships (Iceland), 7 January 1972 round 6. It’s “incomplete” because Spassky resigned after Fischer’s 41. Qf4—the computer doesn’t tell you this and just returns to the menu. (Modern engines tend to checkmate black within 7 moves, e.g. ...Qg8 42. Qe5 Rh7 43. e7 Qxg2+ 44. Kxg2 Rg7+ 45. Kf3 Kh7 46. Bd3+ Rg6 47. Rxg6 Rc8 48. Rg5#)

MicroPower documented the inclusion of the Fischer-Spassky game on the back cover of the 1982 *tape* release, but then it was removed for the 1983 “Electron” release (probably because extra code necessitated moving the Replay buffer to `&400` which is outside the program’s load-address range and they didn’t fancy writing a relocator), and when they later brought back the 1982 version for a *disk* release they apparently forgot it included a Fischer-Spassky game and didn’t mention it, making it a so-called “easter egg”. (At school I assumed it to be a pre-generated computer self-play and wondered why I could never get the same moves with the Play option.)

## Other differences with the Electron version

As already mentioned, the 1983 re-release “for the Acorn Electron” (although the BBC Micro can run either version) changed the level numbers—levels 1, 2, 3, 4 and 5 were renumbered 1, 3, 5, 7 and 9, with randomised intermediate levels added and the old Level 6 dropped—and the bundled copy of the Fischer-Spassky game was removed.

Other changes were:
1. The Electron version does not use the keyboard buffer, so when playing a deterministic level you cannot enter moves ahead of the computer as you can with the BBC Micro version. This is somewhat made up for by the added ability to continue from any point in a replay.
2. Support for under-promotion is added (the computer asks “Piece?” when you promote) although only queen promotions are included in the search. To demonstrate this without waiting for the computer too long, here’s a 42-move win against Level 1 that includes two promotions, behaving identically on both versions.

   Moves:

    **1.**  e4 e5 **2.**  d4 Nc6 **3.**  d5 Nd4 **4.**  c4 Nf6 **5.**  Nc3 Bd6 **6.**  f3 O-O **7.**  Ng1-e2 c5 **8.**  Nb5 Qd6 **9.**  Ne2xd4 cxd4 **10.**  Bd3 a6 **11.**  Nxd6 Qxd6 **12.**  a4 Re8 **13.**  O-O a5 **14.**  Bd2 Qb6 **15.**  b4 axb4 **16.**  Rb1 b3 **17.**  Rxb3 Qc5 **18.**  Rb5 Qa3 **19.**  Bc2 d3 **20.**  Bb3 Qd6 **21.**  c5 Qc7 **22.**  d6 Qc6 **23.**  Re1 Ra6 **24.**  Bg5 d2 **25.**  Re2 h6 **26.**  Bxf6 gxf6 **27.**  Bd5 Qxb5 **28.**  axb5 Ra1 (ah yes, I let it keep a pawn on d2 to get a 3-ply mistake like this) **29.**  Qxa1 Kg7 **30.**  c6 bxc6 **31.**  Bd5xc6 dxc6 **32.**  bxc6 Be6 **33.**  c7 Bc4 **34.**  Rxd2 h5 **35.**  d7 Rh8 **36.**  d8=Q Rxd8 **37.**  cxd8=Q Be6 **38.**  Qa1-a8 h4 **39.**  g4 Bc4 **40.**  g5 fxg5 **41.**  Qxg5+ Kh7 **42.**  Qa8-g8#

3. When the computer controls the white pieces, instead of always opening with `e4`, it now chooses at random between `d4` and `e4` (even on the odd-numbered levels that don’t otherwise involve randomness). The opening behaviour when *you* play white is unchanged (`e5` if you first move from `a`, `c` or `e`, `d5` otherwise).
4. The menu has fancier formatting, clocks are displayed for both players (not just the user), the “Replay” option prints a scrolling list of moves beside the board and you can continue from any point or save/load the moves, move ‘animations’ are slightly faster (with a slightly longer beep for “illegal move”) and colours are customisable.

The bugs associated with the Delete key are still present.

## Tube compatibility and other Chess software

The only Chess engine reviewed by Beebug was Martin Bryant’s *Colossus* in 1987 (plays at 12-ply with estimated 1850 Elo if given enough time, and has a monochrome Mode 4 display); this outperformed earlier engines but fewer schools had the disk. Colossus does not always make the same moves, so you won’t be able to “solve” a level with a single win as you can with MicroPower.

Tube compatibility is relevant if you have a “PiTubeDirect” ~140× speed second processor instead of a BBC emulator running at ~15× speed—although both options are now outpaced by Chris Evans’ “BeebJIT” which can achieve 5000+× speed on AMD64 (and has a mode to do so while keeping timers at normal speed, so you don’t have to toggle back to 1× to type as you do with older emulators).

MicroPower Chess is basically Tube-compatible but the chessboard is invisible: you see only the coordinates. Colossus however has more serious Tube problems. Acornsoft Chess (which Arthur Norman helped write) and Computer Concepts Chess (and its Superior re-release, both by David Thompson) have full Tube compatibility and don’t always make the same moves, while Bug-Byte Chess is fully Tube compatible and deterministic (although slow to update the screen)—but it’s less clear what counts as “solving” it as its search parameters may be configured in hundreds of ways (albeit none of them strong by modern standards)—however these programs all use low-resolution Mode 5 pieces that can be hard to tell apart, meaning that, in order to avoid making blunders due to misidentifying an opponent piece, you either have to get used to their odd pixel art or else keep track of the position separately, meaning there’s little advantage over MicroPower’s invisible board; perhaps the lack of Mode 1 graphics contributed to these programs’ being less popular with schools than MicroPower’s.

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Apple is a trademark of Apple Inc.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
