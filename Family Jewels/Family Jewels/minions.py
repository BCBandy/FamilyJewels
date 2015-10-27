import random
import pygame
from myMath import get_u
import values

class Peon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/knight_small.png")
        self.rect = self.image.get_rect(center = [values.screenx + 10, random.randint(10, values.screeny-10)])
        self.tracker = random.randint(0,1)
        self.hitBoxes = [self.rect]
        self.speed = random.randint(1,4)
        self.hitPoints = 30 - self.speed*5

    def update(self, screen, timer, player, enemy_sprites):
        #move peon toward player
        if self.tracker:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            toPlayer = get_u(dx, dy)
                        
            self.rect.centerx += toPlayer[0]*self.speed
            self.rect.centery += toPlayer[1]*self.speed
        #move left
        else:
            self.rect.centerx -= 10
            if self.rect.centerx <= 0:
                self.kill()
        #kill minion if dead
        if self.hitPoints <= 0:
            self.kill()
        
