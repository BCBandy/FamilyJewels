import pygame
from pygame.locals import *
import math
import random

def main():
    class Peon(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("resources/images/knight_small.png")
            self.rect = self.image.get_rect()
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("resources/images/DragonAttack_small.png")
            self.rect = self.image.get_rect(center = playerPos)
            self.hitBox = pygame.Rect(self.rect.centerx, self.rect.centery, 75, 75)
            self.flyTimer = 0
            self.flyDuration = 0.0
            self.flyAngle = 0.0
            self.hitPoints = 100

        def update(self):
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
                    shoot.play()
                    mouse = pygame.mouse.get_pos()
                    dx = mouse[0] - player.rect.centerx
                    dy = mouse[1] - player.rect.centery

                    angle = math.atan2(dy, dx)
                    u = get_u(dx, dy)
                    fireball = Fireball(angle, u)
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
                    
    class Fireball(pygame.sprite.Sprite):
        def __init__(self, angle, u):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("resources/images/flame_verysmall.png")
            self.rect = self.image.get_rect(center = [player.rect.centerx + u[0]*40, player.rect.centery + u[1]*40])
            self.angle = angle
            self.damage = 10

        def update(self):
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
                            enemy.image = king_knight_takedamage
                            enemy.hit_timer = timer

            #delete if fireball is off screen
            if (self.rect.x > 640 or self.rect.x < -64 or self.rect.y > 480 or self.rect.y < -64):
                all_sprites.remove(self)
                projectile_sprites.remove(self)
    class KingKnight(pygame.sprite.Sprite):
    
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = king_knight
            self.rect = self.image.get_rect(center = [screenx/1.1, screeny/2])
            self.hitPoints = 100
            self.hit_timer = 0
            self.head = self.getHead()
            self.chest = self.getChest()
            self.legs = self.getLegs()
            self.hitBoxes = [self.head, self.chest, self.legs]

        def getLegs(self):
            legs = pygame.Rect(self.rect.x+60, self.rect.y+110, 25, 40)
            return legs
        def getChest(self):
            chest = pygame.Rect(self.rect.x+50, self.rect.y+70, 40, 50)
            return chest
        def getHead(self):
            head = pygame.Rect(self.rect.x+70, self.rect.y+28, 2, 10)
            return head
        def update(self, screen):
        
            pygame.draw.rect(screen, (0,0,0), (5, 459, 506, 18))
            pygame.draw.rect(screen, (255,0,0), (8,462,500, 12))
            if self.hitPoints > 0:
                pygame.draw.rect(screen, (0,255,0), (8,462,self.hitPoints*5, 12))
            else:
                enemy_sprites.remove(self)
            #make kingknight flash red when hit
            if timer - self.hit_timer > .05:  
                self.image = king_knight
            #move kingknight toward player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            toPlayer = get_u(dx, dy)
                        
            self.rect.centerx += toPlayer[0]*3
            self.rect.centery += toPlayer[1]*3

            self.head = self.getHead()
            self.chest = self.getChest()
            self.legs = self.getLegs()
            self.hitBoxes = [self.head, self.chest, self.legs]

            
    # For finding point on line, returns u
    def get_u(dx, dy):
        return [dx/math.sqrt(dx**2 + dy**2), dy/math.sqrt(dx**2 + dy**2)]
    # 1 - Initialize the game
    pygame.init()
    #timer
    timer = 0
    #screen
    screenx = 640
    screeny = 480
    screen = pygame.display.set_mode((screenx, screeny))
    running = True
    #sprites lists
    player_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    #enemy data
    bossPos = [screenx/2, screeny/2]
    #player
    playerPos = [250, 250]
    player = Player()
    all_sprites.add(player)
    player_sprites.add(player)
    keys = [False, False, False, False]
    # 2 - Load resources
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    king_knight_takedamage = pygame.image.load("resources/images/king_knight_takedamage.png")
    smallFireball = pygame.image.load("resources/images/flame_verysmall.png")
    dragon = pygame.image.load("resources/images/DragonAttack_small.png")
    king_knight = pygame.image.load("resources/images/king_knight_medium.png")
    background = pygame.image.load("resources/images/rock_ground.jpg")

    clock = pygame.time.Clock()
    LEFT = 1
    king1 = 0
    while running:
        # Spawn king knight/enter battle    
        if int(timer) >= 1 and king1 == 0:
            king1 = 1
            kingKnight = KingKnight()
            all_sprites.add(kingKnight)
            enemy_sprites.add(kingKnight)



        screen.fill(0)
        # Draw background
        for x in range(screenx/background.get_width()+1):
            for y in range(screeny/background.get_height()+1):
                screen.blit(background,(x*100,y*100))

    
        # 5 - Draw screen and update sprites
        player.update()
        projectile_sprites.update()
        enemy_sprites.update(screen)

        enemy_sprites.draw(screen)
        projectile_sprites.draw(screen)
        player_sprites.draw(screen)   
        # Draw timer display
        seconds = clock.tick()/1000.0
        timer += seconds
        player.flyTimer -= seconds
        player.flyDuration -= seconds
        displayTimer = round(timer,1)

        gamefont = pygame.font.Font(None, 24)
        timertext = gamefont.render(str(displayTimer), 1, [0,0,0])
        screen.blit(timertext, [screenx-50, 5])
        # Draw player health
        pygame.draw.rect(screen, (0,0,0), (5, 5, 206, 18))
        pygame.draw.rect(screen, (255,0,0), (8,8,200, 12))
        if player.hitPoints:
            pygame.draw.rect(screen, (0,255,0), (8,8,player.hitPoints*2, 12))
        else:
            running = 0
            gameover(screen)
    
        pygame.display.flip()
        #limit to 30 frames per second
        clock.tick(30)
def gameover(screen):    
    gameover = pygame.image.load("resources/images/gameover.png")
    screen.blit(gameover,(0,0))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()
if __name__ == "__main__":
    main()