#pong2.py
# A second attempt at pong from scratch

import sys, os, pygame, math, random
from pygame.locals import *
pygame.init()

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, xy, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.gif')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0


    def update(self):
        self.rect = self.calcnewpos()
        (angle, r) = self.vector

        if not self.area.contains(self.rect):
            tl = not self.area.collidepoint(self.rect.topleft)
            tr = not self.area.collidepoint(self.rect.topright)
            bl = not self.area.collidepoint(self.rect.bottomleft)
            br = not self.area.collidepoint(self.rect.bottomright)
            if (tl and tr) or (bl and br):
                angle = -angle
            if (tl and bl):
                #self.offcourt(player=2)
                angle = math.pi - angle
            if (tr and br): #self.offcourt(player=1)
                angle = math.pi - angle

        else:
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)

            # for avoiding collisions of ball with bat after hits
            if (self.rect.colliderect(player1.rect) == 1 or self.rect.colliderect(player2.rect)) and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit

        self.vector = (angle, r)

    def calcnewpos(self):
        (angle, r) = self.vector
        (dx, dy) = (r*math.cos(angle), r*math.sin(angle))
        return self.rect.move(dx, dy)

    #def offcourt(self):


class Bat(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('paddle.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 10
        self.state = 'still'
        self.reinit(side)

    def reinit(self, side):
        self.state = 'still'
        self.movepos = [0, 0]
        if self.side == 'left':
            self.rect.midleft = self.area.midleft
        if self.side == 'right':
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] = self.movepos[1] - self.speed
        self.state = 'moveup'

    def movedown(self):
        self.movepos[1] = self.movepos[1] + self.speed
        self.state = 'movedown'



def main():
    size = width, height = 640, 480
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Michael Pong')

    #Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(black)

    #Initialise players
    global player1
    global player2
    player1 = Bat('left')
    player2 = Bat('right')

    #Initialise ball
    speed = 13
    rand = ((0.1) * random.randint(5, 8))
    ball = Ball((0,0), (rand, speed))

    #Initialise sprites
    playersprites = pygame.sprite.RenderPlain((player1, player2))
    ballsprite = pygame.sprite.RenderPlain((ball))

    #Blit to the screen
    screen.blit(background, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    player1.moveup()
                if event.key == K_SEMICOLON:
                    player1.movedown()
                if event.key == K_UP:
                    player2.moveup()
                if event.key == K_DOWN:
                    player2.movedown()
            elif event.type == KEYUP:
                if event.key == K_a or event.key == K_z:
                    player1.movepos = [0,0]
                    player1.state = "still"
                if event.key == K_UP or event.key == K_DOWN:
                    player2.movepos = [0,0]
                    player2.state = "still"


        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)
        ballsprite.update()
        playersprites.update()
        ballsprite.draw(screen)
        playersprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()