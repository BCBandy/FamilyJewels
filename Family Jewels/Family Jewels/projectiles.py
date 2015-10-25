import math
import pygame
from pygame.locals import *
from boss import KingKnight


class Fireball(pygame.sprite.Sprite):
        def __init__(self, angle, u, player):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("resources/images/flame_verysmall.png")
            self.king_knight_takedamage = pygame.image.load("resources/images/king_knight_takedamage.png")
            self.rect = self.image.get_rect(center = [player.rect.centerx + u[0]*40, player.rect.centery + u[1]*40])
            self.angle = angle
            self.damage = 10

        def update(self, projectile_sprites, timer, enemy_sprites, all_sprites, kingKnight):
            #advance fireball
            self.rect.x += math.cos(self.angle)*10
            self.rect.y += math.sin(self.angle)*10

            #check for enemy collisions
            for enemy in enemy_sprites:
                for box in enemy.hitBoxes:
                    if (self.rect.colliderect(box)): 
                        # Damage kingKnight and delete fireball
                        kingKnight.hitPoints -= self.damage
                        projectile_sprites.remove(self)
                        #king kinght flash red if hit
                        if type(enemy) is KingKnight:
                            enemy.image = self.king_knight_takedamage
                            enemy.hit_timer = timer

            #delete if fireball is off screen
            if (self.rect.x > 640 or self.rect.x < -64 or self.rect.y > 480 or self.rect.y < -64):
                all_sprites.remove(self)
                projectile_sprites.remove(self)