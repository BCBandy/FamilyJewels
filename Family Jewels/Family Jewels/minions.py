class Peon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/images/knight_small.png")
        self.rect = self.image.get_rect()