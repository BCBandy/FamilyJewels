import random
import pygame
from myMath import get_u
import values

class Peon(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/knight_small.png")
        self.rect = self.image.get_rect(center = [screen.get_width() + 20, random.randint(20, screen.get_height()-20)])
        self.tracker = random.randint(0,1)
        self.hitBoxes = [self.rect]
        self.speed = random.randint(1,4)
        self.hitPoints = 30 - self.speed*5 if not self.tracker else 30 - self.speed*5 + 15
        self.waitTime = 0
        self.direction = 'left'
        self.gold = None

    def waitASec(self, timer, item_sprites, interface):
        if self.waitTime == 0:
            self.waitTime = timer+1
        #gold grabbed
        elif self.waitTime < timer:
            self.direction = 'right'
            self.gold = Gold(self.rect.center)
            item_sprites.add(self.gold)
            interface.goldTotal -= self.gold.value
            return True
        return False
    def grabGold(self, timer, item_sprites, interface):
        if self.waitASec(timer, item_sprites, interface):
            pass

    def update(self, screen, timer, player, enemy_sprites, item_sprites, interface):
        #move peon toward player
        if self.tracker:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            toPlayer = get_u(dx, dy)
                        
            self.rect.centerx += toPlayer[0]*self.speed
            self.rect.centery += toPlayer[1]*self.speed
        #move linear
        elif self.direction == 'left':
            if self.rect.centerx > 20:
                self.rect.centerx -= self.speed
            else:
                self.grabGold(timer, item_sprites, interface)
        #return with gold
        elif self.direction == 'right':
            self.rect.centerx += self.speed+4
            self.gold.rect.center = self.rect.center

            
        #kill minion if dead or offscreen
        if self.hitPoints <= 0 or self.rect.centerx > screen.get_width()+30:
            self.kill()
        
class Gold(pygame.sprite.Sprite):
    def __init__(self, centerPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/coingold.png") if random.randint(0,1) else pygame.image.load("resources/images/coinsilver.png")
        self.rect = self.image.get_rect(center = centerPos)
        self.value = random.randint(25, 100)

