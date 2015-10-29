import math, pygame, sys
from pygame.locals import *
import pygame.font
#from values import *

class Interface():
    def __init__(self):
        self.goldTotal = 1000
        self.myFont = pygame.font.Font(None, 40)


    def update(self, player, screen):
        #print gold total
        scoreTxt = self.myFont.render('Gold: '+str(self.goldTotal), 1, (0,0,0))
        screen.blit(scoreTxt, (screen.get_width()-200, screen.get_height()-45))