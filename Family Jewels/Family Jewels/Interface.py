import math, pygame, sys
from pygame.locals import *
import pygame.font
#from values import *

class Interface():

    def __init__(self, screen):
        self.goldTotal = 1000
        self.myFont = pygame.font.Font(None, 40)
        self.flygreen = pygame.image.load("resources/images/fly.png")
        self.flyred = pygame.image.load('resources/images/flyred.png')
        self.rightclick = pygame.image.load('resources/images/flame_token.png')
        self.rightclick_cd = pygame.image.load('resources/images/flame_tokencd.png')
        self.rightclickPos = (screen.get_width() - 250, 12)
        self.flyPos = (screen.get_width() - 350, 12)



    def update(self, player, screen):
        #print gold total
        scoreTxt = self.myFont.render('Gold: '+str(self.goldTotal), 1, (0,0,0))
        screen.blit(scoreTxt, (screen.get_width()-200, screen.get_height()-45))

        #cooldowns
        if(player.flycd <= 0):
            screen.blit(self.flygreen, self.flyPos)
        else:
            screen.blit(self.flyred, self.flyPos)

        if player.largeFireball:
            if player.rightclick_cd <= 0:
                screen.blit(self.rightclick, self.rightclickPos)
            else:
                screen.blit(self.rightclick_cd, self.rightclickPos)


