
from https://ssb22.user.srcf.net/game/index.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/game/index.html) just in case)

# 以Python游戏介绍面向对象编程 Introducing OOP in Python games

## Why I wrote this in 2015
A 9-year-old boy with limited English said he’d written down for me some questions in Chinese about computer programming. I got as far as reading the first two and they meant something like “why do we have to write `def __init__` after `class`” and “why do we need `import`”. It turned out he was trying to work through a `pygame` example in one of those “how-to” books that gives you code without really explaining what it does (and it didn’t help that he’d loaded Python 3 while the book was using Python 2). Below is my attempt to explain in Chinese and simple English. Before we go anywhere near `pygame`, I’d like to show what classes and modules actually *do*, using a text adventure game as an example and trying not to “waffle” too much in between. I assume Python 3, and I recommend [Thonny 3](https://web.archive.org/web/20220220173712/https://thonny.org/) if you don’t already have a Python setup. Beware Thonny 4 contains a pro-Ukraine message which might get you in trouble in some countries.

* This repository's [helper.py](helper.py) can let your child run the below text adventure and similar text-based games on your Amazon Alexa devices, although a little setup is required.

## 房子冒险游戏一 House Adventure 1

想想一个冒险游戏，你站在一栋房子而可以向北、南、东或西走。我们用英文字母n=北、s=南、e=东、w=西。

Think of a game where you are in a house and can go north, south, east or west (we’ll write `n`, `s`, `e` and `w` for short).

请看看以下个程序 Look at this program:
```python
# Start on the landing 开始是楼梯平台
room = "landing"

# Repeat until we're shut down 再做直到关机
while True:

    # Describe the player's current room.
    # 描述玩家的当前房间
    if room == "bathroom": # 浴室
        print ("You are in a bathroom.")
        print ("You can go: n.")
    if room == "landing": # 楼梯平台
        print ("You are on a landing.")
        print ("You can go: s or e or w.")
    if room == "bedroom 1": # 卧室 1
        print ("You are in a bedroom.")
        print ("You can go: w.")
    if room == "bedroom 2": # 卧室 2
        print ("You are in a bedroom.")
        print ("You can go: e.")

    # Find out what the player wants to do
    # 问一问玩家的决定
    what = input("What now? ")

    # Depending on what the player typed,
    # go to a new room.
    # 按照玩家的决定，去新的房间
    if room=="bathroom" and what=="n":
        room = "landing"
    elif room=="landing" and what=="s":
        room = "bathroom"
    elif room=="landing" and what=="e":
        room = "bedroom 1"
    elif room=="landing" and what=="w":
        room = "bedroom 2"
    elif room=="bedroom 1" and what=="w":
        room = "landing"
    elif room=="bedroom 2" and what=="e":
        room = "landing"
    else: print ("You can't do that now.")
```
问题 Questions:
1. 在楼梯平台的北面，加第三个卧室。

Add a 3rd bedroom to the north of the landing.

应该写多少附加的程序线?

How many more lines did you have to write?

应该在多少地方改变程序?

In how many places did you need to change the program?

你是不是检查玩家的确能够进的去新卧室，而且也能够从新卧室出来?

Did you check it’s possible to go into *and back out from* the new bedroom?
2. 这个程序三次说“bedroom 1”。假设第二次你打错“badroom 1”(坏房间)而不是“bedroom 1”(卧室)，这个错在游戏里有什么后果?

In this program, “bedroom 1” is mentioned 3 times. What will happen if, on the second time, you accidentally type “badroom 1” instead of “bedroom 1”?
3. 假设你安装浴室时把南的s打错为v，这个错在游戏里有什么后果?

What will happen if you accidentally typed “v” instead of “s” when putting in the bathroom?
4. 假如一个朋友帮助你编写这个程序，但他没留意楼梯平台的南边已经有浴室。他试试在楼梯平台的南边加个橱柜房间。什么会发生?

Imagine your friend is helping you make this game, and he wants to put a cupboard to the south of the landing. He doesn’t notice there’s already a bathroom there. He adds his cupboard anyway. What will happen?
5. 游戏目前只有一位玩家，假设你想加其他玩家，想一想那样做是不是很难。

Think about how hard it would be to have more than 1 player in the game.
6. 假设你想加可带的物体，想一想那是不是更难。

Think about how hard it would be to put things in the rooms that you can pick up and carry.

## 房子冒险游戏二 House Adventure 2

以下是同一个游戏，但程序好一点。试试了解。

Here is the same game, but programmed a bit better. Try to understand it.
```python
class Room: # 房间类
    def __init__(new_room, description): # 新的房间, 描述
        # This is the set-up code for a new Room.
        # 这是新房间物体的开办程序
        new_room.description = description
        new_room.doors = {} # let's start with no doors
    def connect(this_room, direction, other_room):
        # This is code to add a door between two rooms.
        # 这是连同两个房间的程序
        assert not direction in this_room.doors
        assert not opposite(direction) in other_room.doors
        this_room.doors[direction] = other_room
        other_room.doors[opposite(direction)] = this_room
    def __str__(this_room):
        # This is code to describe a room.  We use the
        # special name __str__ so we can just 'print' the room.
        return this_room.description + "\n" + \
            "You can go: " + \
            " or ".join(this_room.doors)

def opposite(direction): # 计算方向的对面
    return {"n":"s", "s":"n",
            "e":"w", "w":"e"} [direction]

def init():
    # Some set-up code for the house map:
    # 房子地图的开办程序
    bathroom = Room("You are in a bathroom.")
    bedroom1 = Room("You are in a bedroom.")
    bedroom2 = Room("You are in a bedroom.")
    landing = Room("You are on a landing.")
    landing.connect('s', bathroom)
    landing.connect('e', bedroom1)
    landing.connect('w', bedroom2)
    return landing # (see start_room below)

class Player: # 玩家类
    def __init__(new_player, first_room):
        # This is the set-up code for a new Player.
        # 这是新家类物体的开办程序
        new_player.in_room = first_room
    def have_a_turn(this_player): # 轮流
        print (this_player.in_room) # 说目前的房间
        what = input("What now? ")
        if what in this_player.in_room.doors:
            this_player.in_room = this_player.in_room.doors[what]
        else: print ("You can't do that now.")

start_room = init()
player1 = Player (start_room)
while True:
    player1.have_a_turn()
```
问题 Questions:
1. 在楼梯平台的北面，再次加第三个卧室。

Add a 3rd bedroom to the north of the landing again.

**这次**应该写多少附加的程序线? 比上次多或少?

How many more lines did you have to write **this** time? Was it more or fewer than last time?

这次应该在多少地方改变程序? 比上次多或少?

In how many places did you need to change the program? Was it more or fewer?

要是你做一百房间大的公馆，你比较喜欢采用《房子冒险游戏1》或《房子冒险游戏2》的程序? 为什么?

If you’re making a very big house with 100 rooms, would you prefer to use House Adventure 1 or House Adventure 2? Why?
2. 假设有一次你打错”badroom 1”而不是”bedroom 1”，这个错这次有什么后果?

What happens **now** if you type `badroom1` instead of `bedroom1` on *one* of the two lines that say it?

你为什么现在更可能马上留意这个错误?

Why are you now more likely to notice the mistake?
3. 假设你连接浴室时把南的s打错为v，这个错这次有什么后果?

What happens **now** if you accidentally type “v” instead of “s” when connecting the bathroom?

你为什么现在更可能马上留意这个错误?

Why are you now more likely to notice the mistake?
4. 假如一个朋友试试在楼梯平台的南边连接个橱柜房间，这次有什么后果?

What happens **now** if your friend connects a cupboard to the south of the landing?
5. 电脑帮我们更快的留意我们哪里错了为什么是好事?

Why is it good if the computer can help us to notice our mistakes more quickly?
6. 修改程序所以有两个玩家。别忘记显示该谁做轮流。可以说player 1(玩家一)或player 2(玩家二)，或者可以提前求他们输入自己的名字而使用这个。

Change the program so there are 2 players. Don’t forget to print whose turn it is (player 1 or player 2). If you like, you can ask for their names at the start.

应该写多少附加的程序线? 觉得比上次容易吗?

How many extra lines did you have to write? Do you think it’s easier than it would have been last time?
7. (比较难) 修改程序所以房间有可带的物体。

(harder) Change the program so we can put ‘things’ in the rooms that can be moved around.

Hint: you might want to break up the task:
  1. where it says `new_room.doors = {}`, try adding `new_room.things = []` as well.
  2. 为了告诉玩家某个房间目前有什么可带的物体，`__str__`该有什么改变?

How does `__str__` need to change so it can tell you what things are in the room?
  3. 现在能在浴室加一块毛巾?

Can you now put a towel in the bathroom?
  4. 修改`have_a_turn`的程序，让玩家打`"get "` + 物体的名字，就会带。可能你得修改玩家类的`__init__`加个存货清单，开始是空白的。会不会查考怎样使用`append`(附加)和`remove`(排除)?

How does `have_a_turn` need to change so you can type `"get "` + the name of a thing to pick it up? You might want to change Player’s `__init__` so there’s a list of things the player is carrying. You might also want to look up how to use `append` and `remove` in lists.
  5. 也能修改`have_a_turn`的程序让玩家打`"drop "` + 物体名字，就放回房间吗?

Can you also change `have_a_turn` so you can type `"drop "` + the name of a thing you’re carrying to put it back into the room?

## 房子冒险游戏三 House Adventure 3

冒险游戏往往有玩家先得站在某个地方而带某个物体才能使用的那个特别词语。比如，可以有锁住的门，一般来说进不去，但如果玩家有钥匙，可以打`unlock door`(开锁+门)然后能进去。打`unlock door`需要先带钥匙而站在锁住门的房间。

Usually, in games like this, there are special words you can say only in certain places and only when you have certain things. For example, there might be a door that is locked. Normally you can’t go through it. But if you have a key, you can say `unlock door`, and after that you can go through it. You can say `unlock door` only if you have the key and you are in the room with the locked door.

在《房子冒险游戏二》的`have_a_turn`里也许写这样的程序:

In House Adventure 2, you could write something into `have_a_turn` like:
```python
if what=="unlock door" \
    and "key" in player.things \
    and player.in_room == landing \
    and not 'n' in landing.doors: # not already unlocked
        landing.connect('n', secret_room)
        print ("The door is now unlocked.")
```
可是，**我为什么不喜欢这样写?** (线索: 想一想修改《房子冒险游戏一》的程序很难。如果我为许多特别房间写许多特别规则，而把全都放在`have_a_turn`的程序，可不可以有类似难应付的复杂程序?)

but **why don’t I like this?** (Hint: think about how hard it was to change things in House Adventure 1. If I make many special rules about many special rooms, and put them all into `have_a_turn`, could I end up with a program that’s nearly as bad as House Adventure 1?)

那么，看看一下 Now, watch this:
```python
class Room:
    def __init__(new_room, description):
        # same as before 跟上次一样
        new_room.description = description
        new_room.doors = {}
        new_room.things = []
    def connect(this_room, direction, other_room):
        # same as before 跟上次一样
        assert not direction in this_room.doors
        assert not opposite(direction) in other_room.doors
        this_room.doors[direction] = other_room
        other_room.doors[opposite(direction)] = this_room
    def __str__(this_room):
        # same as before; I've done the "things" question
        # 跟上次一样; 我已经做了那个可带物体的问题
        things = " and ".join(this_room.things)
        if things: things = "\nThings here: " + things
        return this_room.description + "\n" + \
            "You can go: " + \
            " or ".join(this_room.doors) + things
    def special_action(this_room, player, action):
        # This is a new part of the program!
        # 这是新的。但一般房间类的程序只说“结果是‘不’”而已。
        return False

class Landing(Room):
    # This is new!  Landing is now a special type of Room.
    # 这也是新的。楼梯平台现在属于“平台类”，是个房间类的子范畴。
    def __init__(new_landing):
        Room.__init__(
            new_landing,
            "You are on a landing. The north door has a lock.")
    # Everything else is the same as for normal Rooms,
    # so we don't have to repeat it here.  But our new part:
    # 其他的都跟一般的房间类一样，不需要在子范畴重写。
    # 但以下是子范畴的新功能:
    def special_action(this_landing, player, action):
        if action=="unlock door":
            if 'n' in this_landing.doors: # 已经开锁了
                print ("The door is already unlocked.")
            elif not "key" in player.things: # 没带钥匙
                print ("You do not have the key.")
            else: # 否则我们可以开锁
                this_landing.connect('n', secret_room)
                print ("The door is now unlocked.")
                return True # 结果是‘是’

def opposite(direction):
    # same as before 跟上次一样
    return {"n":"s", "s":"n",
            "e":"w", "w":"e"} [direction]

def init():
    bathroom = Room("You are in a bathroom.")
    bathroom.things.append("towel")
    bedroom1 = Room("You are in a bedroom.")
    bedroom1.things.append("key")
    landing = Landing()
    landing.connect('s', bathroom)
    landing.connect('e', bedroom1)
    landing.connect('w', Room("You are in a bedroom."))
    global secret_room # so it can be used later 之后采用
    secret_room = Room("You are in the secret room.")
    return landing # as before 跟上次一样

class Player:
    def __init__(new_player, first_room):
        new_player.in_room = first_room
        new_player.things = []
    def have_a_turn(this_player):
        print (this_player.in_room)
        what = input("What now? ") ; print()
        if this_player.in_room.special_action(this_player, what):
            return
        # Again I've done the "things" question.  There are
        # several ways.  Here's one of them.
        # 我再次已经做了那个可带物体的问题。有不同的方法，这是一个:
        what = what.split(None,1)
        # Now what[0] is the first word, what[1] is the rest.
        # (Look up 'split' to see why.)
        if not what: print("You didn't say anything!")
        elif what[0]=="get":
            if len(what)==1:
                print ("You have to tell me what to get.")
            elif what[1] in this_player.in_room.things:
                this_player.in_room.things.remove(what[1])
                this_player.things.append(what[1])
                print ("Got it.")
            elif what[1] in this_player.things:
                print ("You already had that.")
            else: print (what[1]+" is not here.")
        elif what[0]=="drop":
            if len(what)==1:
                print ("You have to tell me what to drop.")
            elif what[1] in this_player.things:
                this_player.things.remove(what[1])
                this_player.in_room.things.append(what[1])
                print ("Dropped it.")
            else: print ("You are not carrying "+what[1]+".")
            # In Python 3.6+ you can do (f"You are not carrying {what[1]}.")
            # but that didn't exist when I wrote this in 2015
        elif what[0] in this_player.in_room.doors:
            this_player.in_room = this_player.in_room.doors[what[0]]
        else: print ("You can't do that now.")

start_room = init()
player1 = Player (start_room) # same as before 跟上次一样
while True:
    player1.have_a_turn()
```
问题 Questions:
1. 我为什么写`return False`和`return True`? (线索: 仔细留意`have_a_turn`程序怎样使用`special_action`的结果。)

Why did I say `return False` and `return True`? (Hint: look carefully at how `special_action` is used in `have_a_turn`.)
2. 要是你没带钥匙而试试开锁，游戏显示:

If you try to unlock the door when you don’t have the key, it says:
```python
You do not have the key.
You can't do that now.
```
修改程序所以说“你没有钥匙”之后不也说“你不会现在这样做”。(线索: 你只需要删除几个空白而已，只不过得选择正确的地方删除! 仔细想一想以上的问题。)

Change the program so it *doesn’t* say “You can’t do that now” after it has already said “You do not have the key”. (Hint: this can be done just by deleting some spaces before one of the lines of the program! Think carefully about question 1.)
3. 修改程序所以开锁后玩家能打`lock door`(把门锁上)。把门锁上需要玩家带钥匙、站在平台、而门已经开锁。 线索: 在房间类，试试写个`disconnect`(使分离)程序，这跟`connect`的程序类似但做`del this_room.doors[direction]`和`del other_room.doors[opposite(direction)]`(del是Python的delete短写，是删除的意思)。`disconnect`程序的`assert`(坚持)省察怎样从`connect`的版本改变?

Change the program so that, after the door is unlocked, you can lock it again by saying `lock door`. You can’t lock the door unless you’re standing there, you have the key, and the door is already unlocked. (Hint: you might want to make a `disconnect` that is like `connect` but does `del this_room.doors[direction]` and `del other_room.doors[opposite(direction)]`. How do the `assert`s change in `disconnect`?)
4. 《房子冒险游戏一》与《房子冒险游戏二》的程序都有个`bedroom2`，但《房子冒险游戏三》的程序看起来没说`bedroom2`但仍然有这个卧室在游戏里，怎么会? 能猜我为什么这样写程序呢?

What happened to `bedroom2` in this version? Can you guess why?
5. 加几个其他房间，并使用`special_action`(特别行动)的程序把一两个有意思的谜语放在一两个房间里。

Add some more rooms, and use `special_action` to put interesting puzzles into one or two of them.

## 模块 Modules

我们的游戏程序越来越大。让我们分割成两个文件免得同时编写太多程序。

Our game is getting quite big now. Let’s try splitting it into two files, so we don’t have so much to see at once.
1. 打开一个名叫`play.py`的空白文件，而把Player类的程序全都在这个新文件。

Make a file called `play.py`, and put the whole of `class Player` into this new file.
2. 在旧的文件，删除Player类的程序，反而写:

In the old file, delete the whole of `class Player`, and instead write:
```python
from play import Player
```
现在会看见Python的`import`(进口)关键词有什么成效呢?

**Now** do you see what `import` does?

假如你的`play.py`含有许多不同的功能(不只是玩家类的功能)，能够写以下进口全都功能:

If you had lots of things in `play.py`, you can import all of them at once by writing:
```python
from play import *
```
可是我比较喜欢整洁的程序，所以一般来说我写:

But I like to keep things tidy, so I usually write:
```python
import play
```
然后我得打`play.Player`而不只是`Player`, 但虽然那得打更多，但是后来很容易看那个功能是从哪里来的。

and then I have to say `play.Player` instead of just `Player`, which is more to type, but it’s easier to see where things came from later.

进口的最好使用是其他人能容许你使用他们程序的某些功能。那能够多多帮助你的程序。不需费事地“拷贝/粘贴”正确部分，只写“进口”而已才能开始写你使用他们所给你的功能的那个程序! (有时候能进口之前需要下载什么东西而正确的安装在电脑上。) 比如，某人写了`random`(随机)的模块，几乎所有的Python版本已经有，可以这样使用:

The best thing about `import` is, other people can let you use parts of *their* programs to help your program, and you don’t need to Copy/Paste: you just `import` the right part (as long as that part is on your computer and all set up). For example, someone wrote a module called `random` which is already included in Python, and it can do this:
```python
import random
print ("I will go "+random.choice(["n","s","e","w"]))
```
(我要去北/南/东/西，随机的选择。请留意英文choice(选择)的拼写不是choise。)

(Make sure to spell `choice` correctly!)

练习 Exercises:
1. 在你所修改的《房子冒险游戏二》或《房子冒险游戏三》版本，多修改所以第二个玩家是被电脑控制的而随机走路。(也许你可以写个`Player`类的子范畴，只个子范畴可以有不同的`have_a_turn`程序。请别忘记显示什么东西所以我们可以看那电脑所控制的玩家到底做什么。)

In your 2-player version of House Adventure 2 (or House Adventure 3), make it so that Player 2 is controlled by the computer and just walks about at random. (You might want to make a special version of `Player` with a different `have_a_turn`. Remember to put something on the screen so we can see what the computer player is doing.)
2. 试试加一个**每玩都不一样**的迷宫。连接迷宫的房间时得使用`random.choice`。每一个迷宫房间的描述都可以说“You are in a maze”(你在迷宫里)而已。会不会只写少数程序线但创造许多许多的迷宫房间?

Try to put a maze into the house that is **different every time**. Use `random.choice` when connecting up the rooms of the maze. Their descriptions can all say “You are in a maze” and nothing else. Can you make it so only a few lines makes many many rooms?

## pygame

现在希望你会了解`import pygame`的真正意思。对于`pygame.init()`, 那是Pygame程序的开始功能，是Pygame作家希望你先使用。是跟我们所写的`init()`开办我们的房子地图类似。如果你喜欢，你可以看看Pygame的程序，看看他们的`init`到底做什么，但你不需这样做才能使用他们所给你的功能。

You should now be able to understand what `import pygame` *means*. As for `pygame.init()`, that is a part of the Pygame program that the people who wrote Pygame want you to call before you use anything else, a bit like *we* made an `init()` to set up our house map. If you like, you can look at the Pygame program and see what their `init` actually *does*, but you don’t have to do this just to use it.

希望你也更明白为什么大多数的类有`__init__`的程序。而且，书籍经常使用`self`(自己)指出类的哪一个物体(比如哪一个房间或哪一个玩家)是正在运转的(要是你不知道哪一个正在运转，有两多房间或两多玩家怎么办?) 我们称它为`new_room`、`this_room`、`new_player`、`this_player`让你看出怎么运转，但你了解这样之后能够开始写`self`因为别人习惯在Python的编程语言这样写(但这是大家的习惯而不是百分之百必须的)。其他编程语言有其他名字，比如C++成它为`this`(这个)而电脑一般能够计算哪里应该加所以你不必一直写。但C++的其他方面有时候一点难。

You should also have a better idea of why most classes have `__init__`. The first thing that goes into the class’s programming is usually called `self` in the books, because it points out the thing (like the room or the player) that the program is now working on. (If you didn’t know this, how would you cope when there’s more than one thing of the same class, like more than one room or more than one player?) We called it `new_room`, `this_room`, `new_player` and `this_player` so you can see what’s happening more easily. When you understand this well, you can start writing `self` because that’s what people *usually* do in Python, but you don’t have to. (In other programming languages it’s called other things. For example, in C++ it’s called `this`, but you don’t always have to write it—the computer can usually figure out where to put it in *for* you. Other parts of C++ can be hard though.)

# 乒乓游戏 Bat-and-ball game
from https://ssb22.user.srcf.net/game/ball.html (also [mirrored on GitLab Pages](https://ssb22.gitlab.io/game/ball.html) just in case)

My previous post about a text adventure game is probably a better introduction than this one, but some youngsters’d rather write graphical action games so let’s make one of those too.

Again I assume Python 3, and this time you’ll need the Pygame library installed.

## 简单的乒乓游戏 Simple bat-and-ball game

我们写个简单的乒乓游戏，但我们会支持4个人一起玩（左边、右边、上边和下边各有一个玩家，如果人数不够，电脑可以代替一些玩家），面向对象编程会让这个任务变得更容易。如果我们愿意，还可以在屏幕上放多个球。

Let’s write a simple bat-and-ball game for multiple players. To be a bit different, as our rectangular screen has 4 edges, we might as well make it a 4-player version (if you don’t have 4 players, the computer can play some of them), with paddles (bats) on the left, right, top and bottom of the screen. The power of object-oriented programming will let us be flexible enough to do that. We can even have more than one ball on the screen if we want.

把任何东西放在显示器之前，我们应该先认识一点关于显示器怎样处理布局（直角座標）和颜色（红绿蓝模型）。别担心这其实不太难。

Before we put anything on the screen, we need to know a little bit about how screens do place (X-Y coordinates) and colour (RGB). Don’t worry, it’s not too hard.

## 座標 Coordinates

我们需要了解直角座標系（这是四年级的内容）：x是从左边缘的水平距离，y是从下边缘的垂直距离。通过设定x和y然后看看这两条线在哪里相交，我们可以确定屏幕上任何一个点的位置。不过，Pygame有点奇怪：它不遵循数学的一般规则，它的y是从上边缘的垂直距离。我认为这是Pygame设计师的一个错误决定，因为Pygame的图形与常规数学相反，容易让年轻的程序员感到困惑。（80年代的英国广播公司微型计算机系统在这方面做得更好：它的图形从左下角开始。）

We need to know about the Cartesian coordinate system (the UK National Curriculum currently introduces this in Year 4 i.e. age 9)—“x” is the horizontal distance from the left edge, and “y” is the vertical distance up from the bottom edge. We can put something at any place on a page or screen by setting the “x” and the “y” and finding where they meet. But Pygame is naughty—instead of following what mathematics *normally* does, *its* idea of “y” is the vertical distance *down* from the *top* edge. My personal opinion is this was an incredibly bad decision by the Pygame designers because it means Pygame graphics are done “backwards” from normal maths, confusing our young potential programmers. (The BBC Micro in the 1980s got this right: its graphics started at bottom left.)

这是另一件我不喜欢的Pygame事：它的x和y的数目有赖于你屏幕的点，但不同屏幕有不同的点大小，所以，如果你在一个电脑上写游戏，你也许在另一个电脑发觉那个游戏根本太小了，所以把游戏发给朋友不一定有好结果。所以，我们得使我们的游戏考察全显示器有多少点才会计算该用多少点。（再次，80年代的英国广播公司微型计算机系统这次更好：它的坐标数字一直是显示器的某某分数，不被显示器点的大小影响。）

And here’s another thing I don’t like about the Pygame coordinate design: the *number* in the “x” or the “y” is the number of *screen dots* (called “picture elements” or pixels), but that depends on your screen: some screens have smaller dots than others, so if you write a game on one computer, you might find it looks way too small on another—no good if you want to send it to a friend! So we have to make the game check how many dots there *are* on the screen before it can work out how many dots to use. (Again the BBC Micro in the 1980s was more helpful: its numbers were always fixed fractions of the distance across the screen, no matter what dot size was being used.)

这些问题我们不必太担心，因为我们可以使用面向对象编程。我们只需要告诉电脑“对象”如何行为，然后让电脑自己计算细节。有些人以为教孩子们面向对象编程太复杂了，最好只写简单的代码说显示器的哪个像素打开。那种方法一开始可能更快，但随着我们添加更多功能（比如更多玩家），代码会变得越来越难调整。面向对象编程最终会更简单。

We don’t have to worry *too* much about these things, because we have object orientation. Once we tell the computer how the objects work, it can calculate some of the details itself. Some people think teaching object orientation to children is too complicated, and it’s better to write simple code that just says which dot on the screen to light up. It’s true their way might be quicker at the beginning, but it will get harder to adjust the code when we want to do things like add more players. This way will be easier in the long run.

有些人以为我们即将说“每个长方形对象都有x和y和高度和宽度”但慢下来！后来我们得做碰撞侦测（避免裁剪），2D或3D碰撞侦测可能看来一点难，不过，面向对象编程能这里帮我们: 我们只应该写如何做1D的碰撞侦测，然后说有两个尺寸（后来能说有三个）。

Now, some people might think we’re about to say “every rectangular object has an ‘x’ and a ‘y’ and a height and a width” but hold on! Later on we’ll have to do collision detection between objects (so they can bounce off of each other instead of going right through each other, sometimes known as “clipping”), and doing collision detection in two dimensions (or even *three* dimensions later) looks a bit hard. But we have object orientation: we just need to write how to do collision detection in *one* dimension, and then say have two of them (or maybe three of them later).

## 5月划船比賽 The May Bumps

每年六月，剑桥大学在康河上举行年度划船比赛，叫做“五月撞船赛”。之所以叫“五月”，是因为它以前是在五月举行的，后来改到六月时似乎忘了改名。（这是程序员的一个常见坏习惯：用一个变量保存某样东西，给它起一个合适的名字，但后来修改了它保存的内容，却懒得改名，结果让自己或其他程序员感到困惑，因为他们必须记住这个变量名已经不对了。请不要这样做：如果你修改了变量的内容，记得改名，这样可以避免混乱。）不过，我想重点讨论的是，为什么这个比赛叫做“撞船赛”。

Every June, Cambridge has a rowing-boat race on the River Cam called the May Bumps. It’s called May because it used to be in May: maybe they forgot to change its name when it became June. (That’s a common bad habit of programmers: they have a variable that stores one thing, so they give it a good name for that thing, but then they change the thing that’s in it, but they’re too lazy to change the name, and later programmers get confused because you have to remember the name is wrong. Please don’t do this: if you’re changing what it is, change its name. It’s less confusing.) But what I want to focus on here is, why it’s called Bumps.

康河有时窄，划艇与船桨有时宽，所以一条船超过另一条船有时不容易。所以他们有个规则：如果你后面船的前端碰撞你船的后端，你的船就得退赛，让那条船过。

The River Cam gets a bit narrow, and the rowing boats with their oars get a bit wide, so it’s difficult for one boat to overtake another. So they have a rule that if the front of the boat behind you bumps into the back of your boat, then your boat must drop out and let that one pass.

让我们写一个程序来判断一条船是否即将撞上另一条船。我们需要知道每条船的前端在哪里（每条船的前端只需要一个数字：从起点到前端的距离），以及每条船的后端（船尾）在哪里。然后，我们可以判断一条船的前端是否撞上了另一条船的后端。

Let’s write some code that works out if one boat is about to bump into another boat. We need to know where each boat-front is (each of which requires only one number: the distance from the starting line to where the boat-front is now), and we need to know where each boat-back is. (They have words like “bows” and “stern” but let’s not get too worried about that now.) Then we can work out whether one boat-front is bumping into another boat-back.
```python
class Boat:
    def __init__(self):
        # This is how to make a new Boat 这是如何创建新船
        self.front = 10
        self.back = 0
    def is_bumping(self, otherBoat):
        if otherBoat is self: # if they're the same Boat as us 如果我们和他们是同一条船，
            return False # we're not bumping them (we ARE them) 我们不碰撞他们（我们就是他们）
        else: return otherBoat.front >= self.front >= otherBoat.back
```
暗示: 如果您打字是比较慢，你可以求Thonny的帮助。比如，第二次打`otherBoat`就压制控制键(Ctrl)而打空格键一次，然后在选项单可以开始打`otherBoat`的头几个字母，Thonny就自动找而拷贝。这也能减少错别字的或然率。

Hint: If you’re slow at typing, you can get Thonny to help you. When you’re about to type `otherBoat` for the *second* time, hold down Ctrl while pressing Space and a menu pops up: you can then start typing the first few letters, and you’ll find it there (because Thonny finds where you typed it the first time). You can use the same method to type other things for the second time, which also reduces the chance of spelling it differently by mistake.

此外，请留意Python的变量名称不可包括空白，所以如果变量名称得包含两词语多，我们习惯或者加下划线（比如is_bumping）或者用大写字母开始新词（比如otherBoat）。我不想烦恼你的英文老师，这只是写代码的惯例而不是写一般英文的惯例。

Notice also that in Python, space is not allowed in variable names, so if a name has two or more words, we usually start a new word by adding an underline or a capital letter instead of writing a space. I don’t want to annoy your English teacher: this is just something we do in code, not in normal English writing.

问题 Questions:
1. 解释那代码的`else:`部分，或者画图解。为什么应该考虑`otherBoat.front`而不只是`otherBoat.back`?

Explain the `else:` part of the above, or draw a picture. Why did we need to check `otherBoat.front` as well as `otherBoat.back`?
2. 如果我们不只摸前面的船但稍微推过它的后端，代码仍然能计算我们碰撞他们吗？为什么这在程序里可能有用？（暗示：电脑是数字的，也许我们应该以步骤搬动。）

If we don’t just touch the boat in front but push slightly into it, will the code still say we’re bumping them? Why might this be useful in a program? (Hint: the computer is digital and we might have to move in steps.)
3. 不是每一条船都有前端离开始线10单位而后端离开始线0单位。如果`__init__`行被修改为`def __init__(self, start, length):`（start是开始，length是长度），此后两行怎么修改使用这些？（暗示：船后端是从船前端和船长度计算的）

Not all boats will have their fronts 10 units away from the starting line and their backs 0 units away from the starting line. If the `__init__` line is changed to `def __init__(self, start, length):` how do the 2 lines after it need to change to use `start` and `length`? (Hint: the line that sets `back` needs to use *both* of these new things.)
4. 这个代码计算什么：

What does this code calculate: `self.is_bumping(otherBoat) or otherBoat.is_bumping(self)`

让我们现给每一条船一个速度（每个时间单位动多少距离单位），然后改变规则所以无论有任何碰撞，船就返回。

Let’s give each boat a speed (units travelled per unit of time), and change the rules so that if it bumps into anything it reverses.
```python
class Boat:
    def __init__(self, start, length, speed):
        self.front = start
        self.back = start - length
        self.speed = speed
    def touching(self, otherBoat):
        if otherBoat is self: return False
        return otherBoat.front >= self.front >= otherBoat.back or self.front >= otherBoat.front >= self.back
    def move(self, allBoats):
        self.front += self.speed
        self.back += self.speed
        if any(self.touching(b) for b in allBoats):
            self.front -= self.speed # bounce back
            self.back -= self.speed
            self.speed = - self.speed # and turn around

boats = [
    Boat(10, 5, 0.2),
    Boat(20, 7, -0.3)]
for timeUnit in range(100):
    for b in boats: b.move(boats)
    print (boats[0].front, boats[1].back)
```
问题 Questions:
1. 这个`touching`做什么?

What does `touching` do?
2. 为什么`move`需要知道所有船的列出？能现看我们为什么之前用了`id`？

Why does `move` need a list of *all* the boats? Can you now see why we checked `id` before?
3. 试试输入以上代码，包括后面的测试行。我们还没使用Pygame只显示船地位的数字。能不能从这些数字解释两条船发生了什么事？

Try out the above code, including the test lines at the end. We’re not using Pygame yet: it’s showing boat positions as just numbers. Can you explain from the numbers what happened to the two boats?

现在我们可以把`Boat`重命名为`ObjectDimension`（物体尺寸），删除测试行，而做二维碰撞侦测：

Now let’s rename our boats into “object dimensions” (and delete the test lines) and do 2D collision checking:
```python
class GameObject:
    def __init__(self, x, y, height, width, speedX=0, speedY=0):
        self.xDim = ObjectDimension(x, width, speedX)
        self.yDim = ObjectDimension(y, height, speedY)
    def move(self, allObjects):
        self.xDim.move(
          o.xDim for o in allObjects if self.yDim.touching(o.yDim))
        self.yDim.move(
          o.yDim for o in allObjects if self.xDim.touching(o.xDim))
```
问题 Questions:
1. GameObject的`move`为什么需要两个`if`部分？（暗示：我们不再在窄康河）

Why are the `if` parts required in GameObject’s `move`? (Hint: we’re not on the narrow river anymore.)
2. 目前的x和y指出物体的右下角落。为什么？如果我们想指出左下或左上或（更难）中间，该如何改变`ObjectDimension`？

At the moment, the x,y position points to the bottom right-hand corner of the object. Why? How should the `ObjectDimension` class change if we want to make it the bottom left, the top left, or (harder) the middle?
3. 这里所说的`=0`等于什么?（叫做“默认选项”）

What does the `=0` do here? (The fancy wording for it is “default value” but can you work out what that means? Hint: what happens if we *don’t* set a speed when we make a `GameObject`?)

## 颜色 Colours

现在我们几乎能把我们的物体放在显示器，但我们仍然应该知道如何具体规定他们的颜色。

We are now very close to drawing our objects on the screen, but before we do so, we need to know how to say which colour they are.

可见光是由极其微小的粒子组成的，这些粒子像波一样运动。为了让你了解这些波有多小，看看一把尺子。尺子上可能有厘米（1/100米）和毫米（1/1,000米）。你可能觉得毫米已经很小了，但光波的波长比毫米还要小1,500到2,500倍——如果把一个光波放大到一毫米那么大，你的30厘米长的尺子可以延伸到上海中心大厦的顶端，这比伦敦碎片塔的两倍还要高。然而，大多数人的眼睛都能分辨出不同波长的光（这就是为什么我说它是“介于”两个数字之间）——我们看到不同波长的光就是不同的颜色。

Visible light is made up of extremely tiny particles that behave like waves. To give you some idea how *small* those waves are, look at a ruler. It probably has centimetres (1/100 of a metre) and perhaps millimetres (1/1,000 of a metre). You may think a millimetre is small, but a light wave is *between 1,500 and 2,500 times smaller*—if you blew up a light wave to the size of a whole millimetre, your 30-centimetre ruler could stretch past the top of the Shanghai Tower, which is more than twice the height of the London Shard. And yet, most people’s eyes can tell that not all light is the *same* wavelength (that’s why I said it’s “between” two numbers)—we see different wavelengths as different colours.

我见过的每一台电视或显示器只能产生三种不同波长的光——红、绿和蓝。你可能还记得，上次看电视时，你看到的颜色远不止红、绿和蓝——如果它只能产生三种颜色，为什么我们能看到更多呢？

Every TV or monitor I ever saw can make *no more than three* different wavelengths—red, green and blue. You might remember last time you watched TV you saw many more colours than just red, green and blue—if it can make only three, why do we see more?

答案就在我们的眼睛里。人类有三种不同的感光细胞，叫做视锥细胞。（狗有两种，有些鱼有四种，有些科学家认为鸽子有五种，但他们仍在努力证明这一点。）人类的三种视锥细胞可以对任何光产生反应，但它们对特定波长的光更敏感：一种对红光最敏感，一种对绿光最敏感，另一种对蓝光最敏感。

The answer is in the back of our eyes. Humans have 3 different types of colour-sensitive cells called cone cells. (Dogs have 2 types, some fish have 4 types, and some scientists think pigeons have 5 types but they’re still working to prove it.) The 3 cones in humans can each start working for *any* light, but they work *more* for light close to a specific wavelength: one is most sensitive to red, another is most sensitive to green, and another is most sensitive to blue.

当一个视力正常的人看到橙光时，他们的红色视锥细胞和绿色视锥细胞都会开始工作，但由于橙色更接近红色而不是绿色，绿色视锥细胞的工作强度只有红色视锥细胞的64%左右。因此，如果我们给这个人100%的红光和64%的绿光，就可以让他们以为自己看到了橙色，因为这会使视锥细胞的工作比例与真实橙光相同。这就是电视或显示器“制造”橙色的方式：它将100%的红光和64%的绿光混合在一起，制造出一种“假”橙色，在大多数人眼中看起来就像真的一样。

When a normally-sighted human sees orange light, both their red-sensitive cone cells and their green-sensitive cone cells start working, but because orange is closer to red than to green, the green-sensitive cones are working only about 64% as hard as the red-sensitive cones. So we can trick the person into thinking they are seeing orange if we give them 100% red light plus 64% green light, because this makes the cones work in the same proportion as they would with real orange. That’s how a TV or monitor “makes” orange: it mixes 100% red with 64% green to make a “fake” orange that looks like the real thing to most people’s eyes.

这个“制造”有引号，因为结果不是真正橘黄色。有些人声称100%红色加64%绿色制造橘黄色，但这个制造只在视力正常的人脑里而已。猫猫、狗狗、鱼都有不同的颜色知觉，色盲人士也是。此外，我们如果用棱镜把电视的橘黄色分为部分，我们会看出它仍然是红色和绿色（真正的橘黄色不是这样）。电视机欺骗我们的脑筋以为不怎的在场的颜色真的来了!

Now I put quotes around “makes” because it’s not really true. Some people do say 100% red plus 64% green “makes orange”, but that happens only in the brain of a normally-sighted human. Cats, dogs and fish see differently, and people with colour blindness see differently. And if you use a prism to break the TV’s “orange” into parts, you’ll see that in reality it’s still red and green, unlike light from other sources. Your TV is tricking you into thinking you’re seeing colours that aren’t there!

在Pygame中设置颜色时，我们需要告诉Pygame要用多少红、绿和蓝来“制造”出电视或显示器上的颜色。我们通过给Pygame三个数字来实现这一点，0表示“没有这种颜色”，255表示“尽可能多的这种颜色”——最大值是255，因为这是计算机用来告诉图形电路使用哪种混合颜色的8位二进制代码中最大的数字。Pygame使用美式英语拼写，所以我们必须把“colour”写成“color”（作为一个英国人，我固执地在日常写作中加上U，只有在为美国计算机系统编写代码时才去掉U）。以下是一些颜色混合的例子，你可以尝试找到其他组合：

To set a colour in Pygame, we need to tell Pygame what *mixture* of red, green and blue we need to fake the colour on a TV or monitor. We do this by giving Pygame three numbers, with 0 meaning “none of this colour” and 255 meaning “as much as possible of this colour”—the highest is 255 because that’s the biggest number that can fit into 8 digits of the binary code that the computer uses to tell its graphics circuit what mixture to use. Pygame also uses American English spelling, so we have to write “colour” without the U (as a Brit I stubbornly continue to add the U in normal writing and drop it only when I *have* to for an American computer system). Here are some colour mixtures to get you started—you can experiment to find others:
```python
import pygame
red    = pygame.Color(255,   0,   0) # 红色
orange = pygame.Color(255, 163,   0) # 橙色
yellow = pygame.Color(255, 255,   0) # 黄色
green  = pygame.Color(  0, 255,   0) # 绿色
blue   = pygame.Color(  0,   0, 255) # 蓝色
cyan   = pygame.Color(  0, 255, 255) # 青色
pink   = pygame.Color(255, 200, 220) # 粉色
white  = pygame.Color(255, 255, 255) # 白色
black  = pygame.Color(  0,   0,   0) # 黑色
```
你知道吗？Python允许你使用中文变量名！例如，你可以写`红色 = pygame.Color(255, 0, 0)`而不是`red = pygame.Color(255, 0, 0)`。请选择最适合你的语言！

Did you know? Python allows you to use Chinese variable names if you prefer! For example, you can write `红色 = pygame.Color(255, 0, 0)` instead of `red = pygame.Color(255, 0, 0)`. Feel free to choose the language that works best for you!

问题 Questions:

（不好意思我还没做完这个翻译）

(Sorry I’ve not finished translating this yet)
1. Change the `__init__` part of the `GameObject` class, adding an extra parameter called `colour`, and say it’s set to `red` if not given. Make it set `self.colour = colour` to keep it for later.
2. Add a new method to the `GameObject` class called `draw` which will actually draw it on the screen. It can start with `def draw(self):` and one way to do it is `pygame.draw.rect(display, self.colour, pygame.Rect(self.xDim.back, self.yDim.back, self.xDim.front-self.xDim.back, self.yDim.front-self.yDim.back))` but if you’re clever you can make this a bit shorter (hint: can we set a temporary `x` and `y` first?)
3. Add a new method to the `GameObject` class called `erase` which is like `draw` but erases the object by drawing over it in black (we’ll need to do this before moving if we’re not clearing the whole screen every time unit). Can you combine `erase` and `draw` so they both call a common service method with only the “colour or black” part changed?

## Setting up the screen

We are now very close to putting something on screen. Here’s how to get Pygame to open a nearly full-screen window and read off its height and width in dots: we will use `*` which means multiply (times, usually written × but that’s hard to type so we use `*` in most programming languages), and we’ll multiply by a decimal fraction less than 1 to make it smaller, but not *too* much less than 1.0 because we still want the window to take *most* of the screen (we just want to leave *some* space for desktop things around the edges so it’s easier to quit if we get something wrong):
```python
pygame.init()
screenW, screenH = pygame.display.get_desktop_sizes()[0]
screenW,screenH = screenW*0.9, screenH*0.8
display = pygame.display.set_mode((screenW,screenH))
```
Then, after putting in the `ObjectDimension` class (renamed from `Boat`), and the `GameObject` class (with the extra `draw` and `erase` methods from the above question), we can set the starting positions:
```python
players = [
    GameObject(screenW*0.06, screenH*0.5,
               screenH*0.15, screenW*0.02,
               0, 0, yellow),
    GameObject(screenW*0.97, screenH*0.5,
               screenH*0.15, screenW*0.02,
               0, 0, blue),
    GameObject(screenW*0.5, screenH*0.97,
               screenH*0.02, screenW*0.15,
               0, 0, green)]
balls = [
    GameObject(screenW*0.5, screenH*0.5,
               screenH*0.02, screenH*0.02,
               screenW*0.001, screenH*0.0007)]
walls = [
    GameObject(1, screenH, screenH, 1), # left
    GameObject(screenW, 1, 1, screenW), # top
    GameObject(screenW, screenH, screenH, 1), # right
    GameObject(screenW, screenH, 1, screenW)] # bottom

everything = players + balls + walls
while True:
    for obj in everything:
        obj.erase()
        obj.move(everything)
        obj.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() ; break
    pygame.display.update()
    pygame.time.wait(1)
```
问题 Questions:
1. Can you make the ball white instead of red just by adding `,white` somewhere?
2. Add a fourth player. (Which side has not yet been used? Can we base the fourth player on the third player but with a different starting place?)
3. Add a second ball (start it in a different place)—look carefully at how commas work in lists
4. Why do we need the walls? (If you’re not sure, try taking them out and see what happens)
5. If you fancy it, make an extra obstacle in the middle of the playing area by adding to `walls`

## Moving the players’ bats

We now have one or more balls bouncing off the walls of the screen and bouncing off the bats (and even perhaps bouncing off each other)—we didn’t have to code for each of these bounces separately, because we have object orientation: we just wrote out how to handle *one* object and then had the computer do the same for all of them. But the bats still aren’t moving—we’ve not yet added any code to let the players control them.

There are ways of asking the computer to tell us when someone types something on the keyboard, but “typing” something is not what we’re interested in here. For one thing, some computers are set to different keyboard layouts—I often set mine to a layout called Dvorak that’s easier on my wrists when I’m typing fast, and you might be using a computer that can be switched into a Chinese input method where several keys have to be pressed to get one character: imagine what could happen if that gets accidentally switched on during a game. And for another thing, if this game is going to be for 2, 3 or even 4 players all crowding around one keyboard, they *won’t* manage to take it in turns to press one key at a time. So, this isn’t normal typing: we need to go to the more basic level of “which actual keys are being held down” (possibly several at once).

Pygame sends us “events” to tell us what’s happening. At the moment, we just check `if event.type == pygame.QUIT` to see if someone closed our window (which is very important to act on), but we can also check for `pygame.KEYDOWN` and `pygame.KEYUP` to find out when keys start to be pressed down, and when they spring back up (not being pressed down anymore).

When we get one of those, we need to find out which key it is, using special “key codes” or “scan codes” which can be different on different types of computer—but thankfully Pygame gives us some pre-set variables we can check against if we want to make sure our game will work on all the kinds of computer Pygame can work on.

(Scan codes are *very* flexible: you can even respond to keys like Ctrl and Shift, with the left-hand one being different from the right-hand one, if you want. Just remember to use the pre-set variables if you want to make sure your game works on other types of computer.)

When we set up the `players`, right now we’re just setting the starting position, height, width, speed (all 0) and colour. Let’s add four more things to each player: the keys to go up, down, left and right. Except two of the players can go *only* left and right, and the other two can go *only* up and down, so some of these things will be `None`. And we’re getting rather a *lot* of things in the settings list for each player, so it’ll be more readable if we add more `thing=` before each one to label what it is, which also helps us miss out stuff we don’t want (like the starting speed, or the keys to move in directions we can’t go):
```python
players = [
    Player(x=screenW*0.06, y=screenH*0.5,
           height=screenH*0.15, width=screenW*0.02,
           colour=yellow,
           up=pygame.KSCAN_W, down=pygame.KSCAN_S),
    
    Player(x=screenW*0.97, y=screenH*0.5,
           height=screenH*0.15, width=screenW*0.02,
           colour=blue,
           up=pygame.KSCAN_UP, down=pygame.KSCAN_DOWN),
    
    Player(x=screenW*0.5, y=screenH*0.97,
           height=screenH*0.02, width=screenW*0.15,
           colour=green,
           left=pygame.KSCAN_J, right=pygame.KSCAN_K),

    Player(x=screenW*0.5, y=screenH*0.06,
           height=screenH*0.02, width=screenW*0.15,
           colour=cyan,
           left=pygame.KSCAN_F1, right=pygame.KSCAN_F2)]
```
The player on the right uses the up and down arrow keys, the player on the left uses `W` and `S`, the player at the bottom uses `J` and `K` and pity the player at the top who has to crowd around and use `F1` and `F2`—feel free to change these if you have better suggestions: you can get a list of all Pygame scan codes by saying `print('\n'.join(sorted(k for k,v in pygame.__dict__.items() if k.startswith("KSCAN"))))`

If you run the above now, you’ll get an error, because we changed `GameObject` into `Player` but we haven’t yet said what a `Player` is. We need to say that a `Player` is a special kind of `GameObject` that doesn’t just sit there like a wall or bounce around by itself like a ball—it gets controlled by the keyboard:
```python
class Player(GameObject):
    def __init__(self, x, y, height, width, colour,
                 up=None, down=None, left=None, right=None):
        GameObject.__init__(self, x, y, height, width, 0, 0, colour)
        self.up, self.down = up, down
        self.left, self.right = left, right
    def check_keydown(self, scancode):
        if scancode==self.up:
            self.yDim.speed = -screenH*0.002
        if scancode==self.down:
            self.yDim.speed = +screenH*0.002
        if scancode==self.left:
            self.xDim.speed = -screenW*0.002
        if scancode==self.right:
            self.xDim.speed = +screenW*0.002
    def check_keyup(self, scancode):
        if scancode in [self.up, self.down, self.left, self.right]:
            self.xDim.speed = self.yDim.speed = 0
```
问题 Questions:
1. Will these bats move faster or slower than the ball? What do you need to change to change that?
2. I don’t like having to change the same number in 4 different places. Please fix the code so that it uses a variable that would need to be changed only once if we want to change the player speed.
3. The last line has *two* equals signs in different places: what does that do?

It’s not *quite* working yet because we still need to actually *call* our new `check_keydown` and `check_keyup` methods. Let’s change the event handler so it looks like this:
```python
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for p in players:
                p.check_keydown(event.scancode)
        if event.type == pygame.KEYUP:
            for p in players:
                p.check_keyup(event.scancode)
        if event.type == pygame.QUIT:
            pygame.quit() ; break
```
and you probably want to go and play it now so I won’t put more questions here. Don’t be surprised though if, when you try to run your bat into a wall, or even the ball or another bat, your bat might bounce off and start moving in the *other* direction until you release the key and press it again—that’s because we gave *every* `GameObject` the “bounce” logic, even the *players*, so your bats will bounce off of things as well. If this isn’t what we want, we can override the `move` method of `Player` (so it doesn’t just take the one from `GameObject` but does something *different*) but that can be for later.

You might like to try adding a basic “computer player” that just keeps moving its bat from end to end—you can do that by putting the right `speedX` or `speedY` value into the `GameObject.__init__` call and letting the bounce logic do the rest. You probably want to have a `class ComputerPlayer` that’s a special type of `Player` (hint: check how we made `Player` a special type of `GameObject`—can we do that kind of thing again?) and just give it a new version of `__init__` that puts in the speed. Doing it this way, you can even assign keys to the computer player so that it starts off being controlled by the computer but then a real person can take over by pressing its keys. Hopefully you’re starting to see the power of object orientation now—just imagine how much more complicated it would have been if we’d had to write separate code for *each* player, wall and ball!

## Keeping score

I wasn’t sure how score was supposed to work in a 4-player bat-and-ball game, so I asked a 10-year-old and his suggestion was “the last player to hit a ball scores whenever it hits any wall” so let’s code that.

(You see I get it that different people are well-practised at different things. I may have coded a network translator used by two enormous phone companies plus some stuff for the weather forecasts, but if the task is thinking up game rules, children are probably better than me at it.)

So we’ll want to keep track of which player last hit the ball. As there might be more than one ball, let’s say a ball can have a hidden label saying which player hit it.

Now, this might get *slightly* tricky because currently our actual “bounce” logic is in the `move` method of `ObjectDimension` (our old `Boat` class), and *that* thing doesn’t even “know” which `GameObject` it’s working for, let alone what thing it hit—it responds only to hitting *something*. But we can change it:
1. Change the constructor (the `__init__`) of `ObjectDimension` to add an extra item after `speed` called `controller`. (Don’t forget to say `self.controller = controller` below so it’s kept for later.)
2. In the `__init__` of `GameObject`, add `,self` after the `speedX` and `speedY` when constructing `self.xDim` and `self.yDim`. That’ll make sure the X and the Y dimensions of a `GameObject` are able to refer back to their ‘parent’ `GameObject` via their `self.controller`.
3. The line that starts `if any(self.touching` needs changing, because now we no longer just want to say “are we touching *any*thing” but we want to know *what* things are being touched. Try writing it like this:
```python
        touching = [b for b in allObjectDimensions
                    if self.touching(b)]
        if touching:
            for t in touching:
                self.controller.touched(t.controller)
                t.controller.touched(self.controller)
```
and then the `self.front -= self.speed` as before (*don’t* change the indentation of that part: it still goes inside the `if touching` block, *not* inside the `for t in touching` block).
4. In `class GameObject` add a method `def touched(self, otherObject): pass` (the `pass` means do nothing for now—we just want to make sure everything *has* a `touched` method, to stop Python from saying there’s no such method as `touched` when the `ObjectDimension` tries to call it on something).
5. Run the game to check it still works. (It still won’t do scoring, but we can at least check we didn’t just make a mistake that’s bad enough to crash it.)
6. In `class Player`, write:
```python
    def touched(self, otherObject):
        otherObject.last_played_by = self
```
—this will set `last_played_by` on *any* object a player touches (even another player or a wall), but that won’t really matter because we’ll check it only when it’s on a ball.
7. In the constructor (`__init__`) of `class Player`, put `self.score = 0` (that’ll make each player start with 0 points)
8. Before the `class Player`, write `class Goal(GameObject): pass` and nothing else. That just says we want `Goal` to be a special type of `GameObject`, but we don’t yet want to change any of the behaviour—we just want to be able to *recognise* if something is a goal when we hit it.
9. Go to the part that sets up `walls` and change the four main `GameObject`s (top, bottom, left and right) into `Goal`s. (If you added any extra walls in the middle, don’t change *those* into `Goal`s, just leave them as normal objects. And if you only want to play against one opponent, you might want to leave the top and bottom walls as normal objects so nobody scores by hitting those. Remember, a `Goal` is a special object that will cause the last person who hit the ball to score a point when the ball hits it—choose which objects are `Goal`s carefully.)
10. Make balls special—let me help you out with this one:
```python
class Ball(GameObject):
    def __init__(self,*a,**k):
        GameObject.__init__(self,*a,**k)
        self.last_played_by = None
    def touched(self, otherObject):
        if self.last_played_by and type(otherObject)==Goal:
            self.last_played_by.score += 1
            pygame.display.set_caption(
                "-".join(f"{p.score}" for p in players))
```
—don’t worry about the `*a,**k` stuff: it’s a Python shorthand that lets us pass all the details about the new ball back up to the underlying `GameObject` without our having to fret about what those details are. And the `set_caption` part takes the score from each player and joins them together to put onto the window title—which is easier than putting them onto the game screen, because to do *that* we’d first need to learn about *fonts*, and I’m trying to get you up and running quickly so let’s just use the window title as score for now. The window title does have the slight advantage that screen-reading software for blind people can read it out—we haven’t yet made this game actually playable by blind people without assistance, but at least you can start a reader for a blind friend to know the score if you want.
11. Don’t forget to go to the `balls` setup and change the `GameObject` there into a `Ball` (if you have more than one ball, do this for all of them)

Extra challenge: by adding just one more line of code in the right place, make it so that, whenever a player hits a ball, the colour of that ball changes to the colour of the player’s bat. (But do check that the other object really is a ball—we don’t want to paint the walls or the other players here! Look at how we used `type()`.)

Can you also add another one line to change a goal into the colour of the ball whenever a point is scored? (You might want to make the goals a bit thicker than 1 to see this more easily.)

Copyright and Trademarks:
All material © Silas S. Brown unless otherwise stated.
Python is a trademark of the Python Software Foundation.
Any other [trademarks](https://ssb22.user.srcf.net/trademarks.html) I mentioned without realising are trademarks of their respective holders.
