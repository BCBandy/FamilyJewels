import math, pygame
from pygame.locals import *
from myMath import get_u
from projectiles import Fireball

LEFT = 1

keys = [False, False, False, False]


class Player(pygame.sprite.Sprite):
    

    def __init__(self, playerPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/DragonAttack_small.png")
        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        self.shoot.set_volume(0.05)
        self.rect = self.image.get_rect(center = playerPos)
        self.hitBox = pygame.Rect(self.rect.centerx, self.rect.centery, 75, 75)
        self.flyTimer = 0
        self.flyDuration = 0.0
        self.flyAngle = 0.0
        self.hitPoints = 100

    def update(self, player, dragon, enemy_sprites, projectile_sprites):
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                self.shoot.play()
                mouse = pygame.mouse.get_pos()
                dx = mouse[0] - player.rect.centerx
                dy = mouse[1] - player.rect.centery

                angle = math.atan2(dy, dx)
                u = get_u(dx, dy)
                fireball = Fireball(angle, u, player)
                angle = angle / math.pi * 180

                img = fireball.image
                fireball.image = pygame.transform.rotate(img, -angle)
                projectile_sprites.add(fireball)
            # fly toward mouse on spacebar
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and 
                self.flyTimer <= 0):
                mouse = pygame.mouse.get_pos()
                dx = mouse[0] - self.rect.centerx
                dy = mouse[1] - self.rect.centery

                angle = math.atan2(-dy, dx)
                angle = angle / math.pi * 180

                self.flyAngle = angle
                self.flyTimer = 2
                self.flyDuration = .5
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
        # make player fly for duration
        if self.flyDuration <= .5 and self.flyDuration > 0:
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