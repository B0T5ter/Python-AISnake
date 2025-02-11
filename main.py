import pygame
import random
pygame.init()

width = 800
height = 500
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
run = True
timermaks = 20
timer = timermaks

glowaX = 1
glowaY = 0

class segment:
    def __init__(self, x, y,color, w = 50):
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.lastx = None
        self.lasty = None

segments = [segment(150,50, (0,200,0)),segment(100,50, (0,255,0)),segment(50,50, (0,255,0))]

def ruch():
    global timer
    global timermaks
    timer -= 1
    if timer <= 0:
        segments[0].lastx = segments[0].x
        segments[0].lasty = segments[0].y
        segments[0].x += glowaX*50
        segments[0].y += glowaY*50
        for x in range(1, len(segments)):
            segments[x].lastx = segments[x].x
            segments[x].lasty = segments[x].y
            segments[x].x = segments[x-1].lastx
            segments[x].y = segments[x-1].lasty
        timer = timermaks

def makingZbior():
    global width
    global height
    zbior = []
    for x in range(width//50):
        for y in range(height//50):
            zbior.append([x,y])
    return zbior
zbior = makingZbior()
def berryLocation(zbior):
    for x in segments:
        try:
            zbior.pop(zbior.index([x.x//50, x.y//50]))
        except:
            pass
    losowa = random.randint(0,len(zbior))
    return zbior[losowa][0], zbior[losowa][1]
x,y = berryLocation(zbior)
malinka = segment(x * 50,y* 50, (255,0,0))

while run:
    screen.fill('black')
    ruch()
    if segments[0].x == malinka.x and segments[0].y == malinka.y:
        x,y = berryLocation(zbior)
        malinka = segment(x * 50,y* 50, (255,0,0))
        print(x*50, y*50)
        segments.append(segment(segments[len(segments)-1].lastx,segments[len(segments)-1].lasty, (0,255,0)))
    pygame.draw.rect(screen, malinka.color, (malinka.x, malinka.y, malinka.w, malinka.w))

    for x in segments:
        pygame.draw.rect(screen, x.color, (x.x, x.y, x.w, x.w))

    for x in segments[1:]:
        if x.x == segments[0].x and x.y == segments[0].y:
            run = False
    if segments[0].x > width - 50 or segments[0].x < 0 or segments[0].y > height - 50 or segments[0].y < 0:
        run = False
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        glowaX = -1
        glowaY = 0
    elif key[pygame.K_s] == True:
        glowaX = 0
        glowaY = 1
    elif key[pygame.K_w] == True:
        glowaX = 0
        glowaY = -1
    elif key[pygame.K_d] == True:
        glowaX = 1
        glowaY = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    clock.tick(60)
pygame.quit()