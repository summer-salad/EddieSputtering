import pygame
from pygame.locals import *
import random, math, sys, time

pygame.init()

Surface = pygame.display.set_mode((800,600))
lastTop = 0 
circlesSize = 10

Circles = []
class Circle:
    def __init__(self): #Setting up paraameters for blue circles
        #self.radius = int(random.random()*50) + 1
        self.radius = circlesSize
        self.x = random.randint(self.radius, 800-self.radius)
        self.y = random.randint(50+self.radius, 550-self.radius) #100 in the rand int so ball doesnt get stuck in the red bar, making a shower of red balls
        self.speedx = 0.5*(random.random()+1.0)
        self.speedy = 0.5*(random.random()+1.0)

Tcircles = [] #Setting up parameters for red circles
class Tcircle:
    def __init__(self):
        print (lastTop)
        self.radius = 5
        #self.x = random.randint(self.radius, 800-self.radius)
        self.x = (lastTop- (circlesSize/2)) #this makes it so that it spawns in at the exact point hwere the ball hit
        self.y = 50 #50 for spawn at bottom of red bar
        self.speedx = 0 #no horizontal movement 
        self.speedy = 0.5 #set movement speed, helpful for no midair grouping
for x in range(10):
    Circles.append(Circle())

def CircleCollide(C1,C2): #interactions between blue balls, math lol
    C1Speed = math.sqrt((C1.speedx**2)+(C1.speedy**2))
    XDiff = -(C1.x-C2.x)
    YDiff = -(C1.y-C2.y)
    if XDiff > 0:
        if YDiff > 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff < 0:
        if YDiff > 0:
            Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff == 0:
        if YDiff > 0:
            Angle = -90
        else:
            Angle = 90
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    elif YDiff == 0:
        if XDiff < 0:
            Angle = 0
        else:
            Angle = 180
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    C1.speedx = XSpeed
    C1.speedy = YSpeed
def Move(): #circles move
    for Circle in Circles:
        Circle.x += Circle.speedx
        Circle.y += Circle.speedy
    for Tcircle in Tcircles: #Red circles stop when they hit the green target
        Tcircle.y += Tcircle.speedy
        if Tcircle.y >= 550:
            Tcircle.speedy = 0
        for Tcircle2 in Tcircles:
            if Tcircle != Tcircle2:
                if math.sqrt(((Tcircle.x-Tcircle2.x)**2)+((Tcircle.y-Tcircle2.y)**2)) <= (Tcircle.radius+Tcircle2.radius):
                    Tcircle.speedy = 0
def CollisionDetect(): #turns balls around
    global lastTop #with this, we can alter lastTop
    for Circle in Circles:
        if Circle.x < Circle.radius or Circle.x > 800-Circle.radius:
            Circle.speedx *= -1 
        if Circle.y < Circle.radius+50: #red rectangle is hit
            Circle.speedy *= -1
            lastTop = int(Circle.x) #lastTop is changed
            Tcircles.append(Tcircle()) #adds another circle
        if Circle.y > 550-Circle.radius:
            Circle.speedy *= -1
    for Circle in Circles:
        for Circle2 in Circles:
            if Circle != Circle2:
                if math.sqrt(((Circle.x-Circle2.x)**2)+((Circle.y-Circle2.y)**2)) <= (Circle.radius+Circle2.radius):
                    CircleCollide(Circle,Circle2)
def Draw():
    Surface.fill((0,0,0))
    pygame.draw.rect(Surface, (150,0,0), (0, 0, 800, 50)) #draws red bar
    pygame.draw.rect(Surface, (0,150,0), (0,550, 800, 50)) #draws green bar
    for Circle in Circles:
        pygame.draw.circle(Surface,(0,0,150),(int(Circle.x),int(Circle.y)),Circle.radius) #draws individual blue circles
    for Tcircle in Tcircles:
        pygame.draw.circle(Surface,(150,0,0),(int(Tcircle.x),int(Tcircle.y)),Tcircle.radius) #draws individual red circles
    pygame.display.flip()

def GetInput():
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]: #if Esc is pressed, quit window
            pygame.quit(); sys.exit()
def main():
    while True:
        GetInput()
        Move()
        CollisionDetect()
        Draw()
        time.sleep(.005)


if __name__ == '__main__': main()  
