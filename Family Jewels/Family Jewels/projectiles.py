import math, random
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
            self.damage = random.randint(1, 3)

        def update(self, projectile_sprites, timer, enemy_sprites, all_sprites):
            #advance fireball
            self.rect.x += math.cos(self.angle)*10
            self.rect.y += math.sin(self.angle)*10

            #check for enemy collisions
            for enemy in enemy_sprites:
                for box in enemy.hitBoxes:
                    if (self.rect.colliderect(box)): 
                        projectile_sprites.remove(self)
                        #minion
                        enemy.hitPoints -= self.damage
                        #king kinght flash red if hit
                        if type(enemy) is KingKnight:
                            # Damage kingKnight and delete fireball
                            #kingKnight.hitPoints -= self.damage
                            enemy.image = self.king_knight_takedamage
                            enemy.hit_timer = timer

            #delete if fireball is off screen
            if (self.rect.x > 640 or self.rect.x < -64 or self.rect.y > 480 or self.rect.y < -64):
                all_sprites.remove(self)
                projectile_sprites.remove(self)