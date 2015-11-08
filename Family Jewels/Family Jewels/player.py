import math, pygame, sys
from pygame.locals import *
from myMath import get_u
from projectiles import Fireball, SmallFireball
import projectiles
from values import *
import minions

LEFT = 1

keys = [False, False, False, False]


class Player(pygame.sprite.Sprite):
    

    def __init__(self, playerPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/DragonAttack_small.png")
        
        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        self.shootbig = pygame.mixer.Sound("resources/audio/explode.wav")
        self.shootbig.set_volume(.1)
        self.shoot.set_volume(0.05)
        self.rect = pygame.Rect(playerPos[0], playerPos[1], 50, 50)#self.image.get_rect(center = playerPos)
        self.hitBox = pygame.Rect(self.rect.centerx, self.rect.centery, 75, 75)
        self.flycd = 0
        self.rightclick_cd = 0
        self.flyDuration = 0.0
        self.flyAngle = 0.0
        self.hitPoints = 100
        self.largeFireball = False
        self.largeFireballId = 0
        self.totalPoints = 0
        self.pause = 0

    def update(self, player, dragon, enemy_sprites, projectile_sprites, item_sprites, screen, interface):
        # Change player angle
        mousePos = pygame.mouse.get_pos()
        playerRect = player.rect.center

        dx1 = mousePos[0] - playerRect[0]
        dy1 = mousePos[1] - playerRect[1]
        angle = math.atan2(-dy1, dx1)/math.pi*180

        playerRot = pygame.transform.rotozoom(dragon,angle, 1)
        player.image = playerRot
        player.rect = player.image.get_rect(center = player.rect.center)
        # 3 - Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # create fireball on left mouse event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse = pygame.mouse.get_pos()
                dx = mouse[0] - player.rect.centerx
                dy = mouse[1] - player.rect.centery

                angle = math.atan2(dy, dx)
                u = get_u(dx, dy)
                #small fireball
                if event.button == LEFT:
                    self.shoot.play()
                    fireball = SmallFireball(angle, u, player)
                    img = fireball.image
                    angle = angle / math.pi * 180
                    fireball.image = pygame.transform.rotate(img, -angle)
                    projectile_sprites.add(fireball)
                #large fireball
                if event.button == 3 and self.largeFireball == True and self.rightclick_cd <= 0:
                    self.rightclick_cd = 3
                    self.shootbig.play()
                    fireball = projectiles.BigFireball(angle, u, player)
                    self.largeFireballId += 1
                    img = fireball.image
                    angle = angle / math.pi * 180
                    fireball.image = pygame.transform.rotate(img, -angle)
                    projectile_sprites.add(fireball)
            # fly toward mouse on spacebar
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and 
                self.flycd <= 0):
                mouse = pygame.mouse.get_pos()
                dx = mouse[0] - self.rect.centerx
                dy = mouse[1] - self.rect.centery

                angle = math.atan2(-dy, dx)
                angle = angle / math.pi * 180

                self.flyAngle = angle
                self.flycd = 1
                self.flyDuration = .2
            # player movement
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True
            if event.type == pygame.KEYUP:                
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.pause == 0:
                    self.pause = 1
                else:
                    self.pause = 0
        # make player fly for duration
        if self.flyDuration <= .2 and self.flyDuration > 0:
            #self.rect.centerx += math.cos(self.flyAngle)*10
            #self.rect.centery += math.sin(self.flyAngle)*10
            u = get_u(dx1, dy1)
            self.rect.centerx += u[0]*18
            self.rect.centery += u[1]*18
        # move player
        if keys[0]:
            self.rect.centery -= 5
        elif keys[2]:
            self.rect.centery += 5
        if keys[1]:
            self.rect.centerx -= 5
        elif keys[3]:
            self.rect.centerx += 5

        self.hitBox.center = self.rect.center
        # Check for player vs enemy collisions
        for enemy in enemy_sprites:
            for box in enemy.hitBoxes:
                while self.hitBox.colliderect(box):
                    self.hitPoints -= 20
                    #push dragon away from enemy collision
                    if self.rect.centerx < box.centerx:
                        self.rect.centerx -= 50          
                    elif self.rect.centerx > box.centerx:
                        self.rect.centerx += 50
                    if self.rect.centery < box.centery:
                        self.rect.centery -= 50
                    elif self.rect.centery > box.centery:
                        self.rect.centery += 50
                    self.hitBox.center = self.rect.center 

        #check for item collisions
        for item in item_sprites:
            if self.hitBox.colliderect(item.rect):
                if hasattr(item, 'value'):
                    interface.goldTotal += item.value
                if type(item) == minions.LargeFireball:
                    self.largeFireball = True
                item.kill()

        