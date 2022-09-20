from multiprocessing.util import info
from tkinter import W
from pygame_functions import *


screenSize(1000,800)
setBackgroundColour("grey")
centrex = 500
centrey = 400
setAutoUpdate(False)
infoLabel = makeLabel("text here",54,10,10,"white","Consolas","black")
showLabel(infoLabel)

class World():
    def __init__(self):
        self.blocks = [([300,400],[870,831]),([1113,375],[1329,759])]
        self.mapimage = makeSprite("map.png")
        self.mapwidth = 2000
        self.mapheight = 2000
        showSprite(self.mapimage)
        self.interactables = []

    def draw(self, player):
        # Draw the blocks
        moveSprite(self.mapimage,centrex-player.x, centrey-player.y)
        for block in self.blocks:
            topleftx = centrex + block[0][0]-player.x
            toplefty = centrey + block[0][1]-player.y
            drawRect(topleftx, toplefty, block[1][0]-block[0][0], block[1][1]-block[0][1], "black")
        #Draw Interactables
        for i in self.interactables:
            i.draw(player)

    def addInteractable(self,newInteractable):
        self.interactables.append(newInteractable)

    def removeInteractable(self,i):
        hideSprite(i.image)
        self.interactables.remove(i)
    
    def checkCollision(self,pointx, pointy):
        for b in self.blocks:
            if b[0][0] <= pointx <= b[1][0] and b[0][1] <= pointy <= b[1][1]:
                return True
        else:
            return False
    
    def checkInteractions(self,player):
        touched = []
        for b in self.interactables:
            if touching(player.sprite, b.image):
                touched.append(b)
        return touched

class Interactable():
    def __init__(self, x,y,image, world):
        self.x = x
        self.y = y
        self.image = makeSprite(image)
        self.world = world

    def draw(self,player):
        showSprite(self.image)
        moveSprite(self.image,centrex-player.x+self.x, centrey-player.y+self.y)

    def interact(self,player):
        changeLabel(infoLabel,"Got it!")
        self.world.removeInteractable(self)

class Player():
    def __init__(self):
        self.x = 200
        self.y = 200
        self.sprite = makeSprite("chef150.png",8)
    
    def update(self, world):
        newx = self.x
        newy = self.y
        if keyPressed("left"):
            newx=self.x-5
        if keyPressed("right"):
            newx=self.x+5
        if keyPressed("up"):
            newy=self.y-5
        if keyPressed("down"):
            newy=self.y+5
        # see if collided with blocks in world
        if not world.checkCollision(newx,newy):
            self.x = newx
            self.y = newy
        # see if colllided with interactable:
        for touched in world.checkInteractions(self):
            touched.interact(self)
            

    def draw(self):
        moveSprite(self.sprite,centrex,centrey, True)
        showSprite(self.sprite)

p = Player()
w = World()
w.addInteractable(Interactable(500,800,"chest.png",w))

while True:
    clearShapes()
    w.draw(p)
    p.update(w)
    p.draw()

    updateDisplay()
    tick(60)


endWait()
