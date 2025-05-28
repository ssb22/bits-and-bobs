# Introductory Python from https://ssb22.user.srcf.net/game/ball.html
# (mostly-completed solution for demonstration purposes only)

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

pygame.init()
screenW, screenH = pygame.display.get_desktop_sizes()[0]
screenW,screenH = screenW*0.9, screenH*0.8
display = pygame.display.set_mode((screenW,screenH))

class ObjectDimension:
    def __init__(self, start, length, speed, controller):
        self.front = start
        self.back = start - length
        self.speed = speed
        self.controller = controller
    def touching(self, other):
        if other is self: return False
        return other.front >= self.front >= other.back or self.front >= other.front >= self.back
    def move(self, allObjectDimensions):
        self.front += self.speed
        self.back += self.speed
        touching = [b for b in allObjectDimensions
                    if self.touching(b)]
        if touching:
            for t in touching:
                self.controller.touched(t.controller)
                t.controller.touched(self.controller)
            self.front -= self.speed # bounce back
            self.back -= self.speed
            self.speed = - self.speed # and turn around

class GameObject:
    def __init__(self, x, y, height, width, speedX=0, speedY=0, colour=red):
        self.xDim = ObjectDimension(x, width, speedX, self)
        self.yDim = ObjectDimension(y, height, speedY, self)
        self.colour = colour
    def move(self, allObjects):
        self.xDim.move(
          o.xDim for o in allObjects if self.yDim.touching(o.yDim))
        self.yDim.move(
          o.yDim for o in allObjects if self.xDim.touching(o.xDim))
    def touched(self, otherObject): pass
    def draw(self):
        self.drawOrErase(self.colour)
    def erase(self):
        self.drawOrErase(black)
    def drawOrErase(self,colour):
        x,y = self.xDim.back,self.yDim.back
        pygame.draw.rect(display, colour, pygame.Rect(x, y, self.xDim.front-x, self.yDim.front-y))

class Goal(GameObject): pass

class Player(GameObject):
    def __init__(self, x, y, height, width, colour,
                 up=None, down=None, left=None, right=None,
                 speed = 0.002):
        GameObject.__init__(self, x, y, height, width, 0, 0, colour)
        self.up, self.down = up, down
        self.left, self.right = left, right
        self.speed = speed
        self.score = 0
    def check_keydown(self, scancode):
        if scancode==self.up:
            self.yDim.speed = -screenH*self.speed
        if scancode==self.down:
            self.yDim.speed = +screenH*self.speed
        if scancode==self.left:
            self.xDim.speed = -screenW*self.speed
        if scancode==self.right:
            self.xDim.speed = +screenW*self.speed
    def check_keyup(self, scancode):
        if scancode in [self.up, self.down, self.left, self.right]:
            self.xDim.speed = self.yDim.speed = 0
    def touched(self, otherObject):
        if type(otherObject)==Ball: otherObject.colour = self.colour
        otherObject.last_played_by = self

class Ball(GameObject):
    def __init__(self,*a,**k):
        GameObject.__init__(self,*a,**k)
        self.last_played_by = None
    def touched(self, otherObject):
        if self.last_played_by and type(otherObject)==Goal:
            self.last_played_by.score += 1
            otherObject.colour = self.colour
            pygame.display.set_caption(
                "-".join(f"{p.score}" for p in players))

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

balls = [
    Ball(screenW*0.5, screenH*0.5,
         screenH*0.02, screenH*0.02,
         screenW*0.001, screenH*0.0007)]
walls = [
    Goal(5, screenH, screenH, 5), # left
    Goal(screenW, 5, 5, screenW), # top
    Goal(screenW, screenH, screenH, 5), # right
    Goal(screenW, screenH, 5, screenW)] # bottom

everything = players + balls + walls
while True:
    for obj in everything:
        obj.erase()
        obj.move(everything)
        obj.draw()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for p in players:
                p.check_keydown(event.scancode)
        if event.type == pygame.KEYUP:
            for p in players:
                p.check_keyup(event.scancode)
        if event.type == pygame.QUIT:
            pygame.quit() ; break
    pygame.display.update()
    pygame.time.wait(1)
