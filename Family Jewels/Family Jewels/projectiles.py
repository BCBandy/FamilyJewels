import math, random
import pygame
from pygame.locals import *
from boss import KingKnight


class Fireball(pygame.sprite.Sprite):
        def __init__(self, angle, u, player):
            pygame.sprite.Sprite.__init__(self)
            #self.image = pygame.image.load("resources/images/flame_verysmall.png")
            #self.imageBig = pygame.image.load('resources/images/flame_big.png')
            #self.king_knight_takedamage = pygame.image.load("resources/images/king_knight_takedamage.png")
            #self.rect = self.image.get_rect(center = [player.rect.centerx + u[0]*40, player.rect.centery + u[1]*40])
            #self.angle = angle
            #self.hitBoxBig = pygame.Rect(0,0,50,50)
            #self.hitBox = pygame.Rect(0,0,10,10)
            #self.small = 1
            #self.damage = 1000#random.randint(1, 4)

        def advance(self, projectile_sprites, timer, enemy_sprites, all_sprites, screen, angle):
            #advance fireball
            self.rect.x += math.cos(angle)*10
            self.rect.y += math.sin(angle)*10
            self.hitBox.center = self.rect.center

        def delete(self, projectile_sprites, timer, enemy_sprites, all_sprites, screen):
            #delete if fireball is off screen
            if (self.rect.x > screen.get_width() or self.rect.x < -64 or self.rect.y > screen.get_height() or self.rect.y < -64):
                all_sprites.remove(self)
                projectile_sprites.remove(self)

class BigFireball(Fireball):
    def __init__(self, angle, u, player):
        pygame.sprite.Sprite.__init__(self)
        self.king_knight_takedamage = pygame.image.load("resources/images/king_knight_takedamage.png")
        self.image = pygame.image.load('resources/images/flame_big.png')
        self.rect =  self.image.get_rect(center = player.rect.center)#[player.rect.centerx + u[0]*40, player.rect.centery + u[1]*40])
        self.hitBox = pygame.Rect(0,0,100,100)
        self.angle = angle
        self.damage = 30
        self.largeFireballId = player.largeFireballId

    def update(self, projectile_sprites, timer, enemy_sprites, all_sprites, screen):
        super().advance(projectile_sprites, timer, enemy_sprites, all_sprites, screen, self.angle)
        
        #check for enemy collisions
        for enemy in enemy_sprites:
            for box in enemy.hitBoxes:
                if (self.hitBox.colliderect(box)): 
                    #projectile_sprites.remove(self)
                    #minion
                    if enemy.largeFireballId != self.largeFireballId:
                        enemy.hitPoints -= self.damage
                        enemy.largeFireballId = self.largeFireballId
                    #king kinght flash red if hit
                    if type(enemy) is KingKnight:
                        # Damage kingKnight and delete fireball
                        #kingKnight.hitPoints -= self.damage
                        enemy.image = self.king_knight_takedamage
                        enemy.hit_timer = timer

        super().delete(projectile_sprites, timer, enemy_sprites, all_sprites, screen)

class SmallFireball(Fireball):
    def __init__(self, angle, u, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/flame_verysmall.png")
        self.king_knight_takedamage = pygame.image.load("resources/images/king_knight_takedamage.png")
        self.rect = self.image.get_rect(center = [player.rect.centerx + u[0]*40, player.rect.centery + u[1]*40])
        self.hitBox = pygame.Rect(0,0,10,10)
        self.angle = angle
        self.damage = random.randint(1,4)

    def update(self, projectile_sprites, timer, enemy_sprites, all_sprites, screen):
        super().advance(projectile_sprites, timer, enemy_sprites, all_sprites, screen, self.angle)
        
        #check for enemy collisions
        for enemy in enemy_sprites:
            for box in enemy.hitBoxes:
                if (self.hitBox.colliderect(box)): 
                    projectile_sprites.remove(self)
                    #minion
                    enemy.hitPoints -= self.damage
                    #king kinght flash red if hit
                    if type(enemy) is KingKnight:
                        # Damage kingKnight and delete fireball
                        #kingKnight.hitPoints -= self.damage
                        enemy.image = self.king_knight_takedamage
                        enemy.hit_timer = timer

        super().delete(projectile_sprites, timer, enemy_sprites, all_sprites, screen)