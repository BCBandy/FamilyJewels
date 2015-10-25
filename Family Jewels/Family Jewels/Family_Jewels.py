import pygame
from pygame.locals import *
import random, math
from myMath import get_u
from boss import KingKnight
from player import Player
player = None

def main():
    
    
                    
    
    

            
    
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
    global player
    player = Player(playerPos)
    all_sprites.add(player)
    player_sprites.add(player)
    # 2 - Load resources
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    smallFireball = pygame.image.load("resources/images/flame_verysmall.png")
    dragon = pygame.image.load("resources/images/DragonAttack_small.png")
    background = pygame.image.load("resources/images/rock_ground.jpg")

    clock = pygame.time.Clock()
    LEFT = 1
    king1 = 0
    kingKnight = None
    while running:
        # Spawn king knight/enter battle    
        if int(timer) >= 1 and king1 == 0:
            king1 = 1
            kingKnight = KingKnight()
            all_sprites.add(kingKnight)
            enemy_sprites.add(kingKnight)

        screen.fill(0)
        # Draw background
        for x in range(int(screenx/background.get_width())+1):
            for y in range(int(screeny/background.get_height())+1):
                screen.blit(background,(x*100,y*100))

        # 5 - Draw screen and update sprites
        player.update(player, dragon, enemy_sprites, projectile_sprites)
        projectile_sprites.update(projectile_sprites, timer, enemy_sprites, all_sprites, kingKnight)
        enemy_sprites.update(screen, timer, player)

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