# explosion.py
# A figure walks around, if it walks into a bomb, it explodes

import pygame
from utils import load_png
from pygame.locals import *
pygame.init()


class character(pygame.sprite.Sprite):
    """can walk around"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('character.gif')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.speed = 10
        self.state = 'still'
        self.reinit

    def reinit(self):
        self.state = 'still'
        self.movepos = [0, 0]
        if self.side == 'left':
            self.rect.midleft = self.area.midleft
        if self.side == 'right':
            self.rect.midright = self.area.midright

    def update(self):

    def walk(self):


class bomb(pygame.sprite.Sprite):
    """explodes, as bombs are wont to do"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):

    def explode():

def main():


if __name__ == '__main__': main()