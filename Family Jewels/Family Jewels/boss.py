﻿import pygame
from myMath import get_u
import minions
import random
#from values import screenx,screeny

king_knight = pygame.image.load("resources/images/king_knight_medium.png")

class KingKnight(pygame.sprite.Sprite):
       
        def __init__(self, screen):
            pygame.sprite.Sprite.__init__(self)
            self.image = king_knight
            self.rect = self.image.get_rect(center = [screen.get_width()+40, random.randint(10, screen.get_height())])
            self.hitPoints = 100
            self.hit_timer = 0
            self.head = self.getHead()
            self.chest = self.getChest()
            self.legs = self.getLegs()
            self.hitBoxes = [self.head, self.chest, self.legs]
            self.largeFireballId = -1
            self.speed = random.randint(1,4)
            self.points = 15

        def getLegs(self):
            legs = pygame.Rect(self.rect.x+60, self.rect.y+110, 25, 40)
            return legs
        def getChest(self):
            chest = pygame.Rect(self.rect.x+50, self.rect.y+70, 40, 110)
            return chest
        def getHead(self):
            head = pygame.Rect(self.rect.x+70, self.rect.y+28, 2, 50)
            return head
        def update(self, screen, timer, player, enemy_sprites, item_sprites, interface):
        
            #hp bar
            pygame.draw.rect(screen, (0,0,0), (5, 459, 506, 18))
            pygame.draw.rect(screen, (255,0,0), (8,462,500, 12))
            if self.hitPoints > 0:
                pygame.draw.rect(screen, (0,255,0), (8,462,self.hitPoints*5, 12))
            else:
                #boss died, drop powerup
                if player.largeFireball == False:
                    item_sprites.add(minions.LargeFireball(self.rect.center))
                player.totalPoints += self.points
                enemy_sprites.remove(self)
            #make kingknight flash red when hit
            if timer - self.hit_timer > .05:  
                self.image = king_knight
            
            #move kingknight toward player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            toPlayer = get_u(dx, dy)
                        
            self.rect.centerx += toPlayer[0]*self.speed
            self.rect.centery += toPlayer[1]*self.speed

            self.head = self.getHead()
            self.chest = self.getChest()
            self.legs = self.getLegs()
            self.hitBoxes = [self.head, self.chest, self.legs]
            