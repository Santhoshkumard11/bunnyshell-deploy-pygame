import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.path = "./assets/images/background/sprites/"
        for i in range(1,9):
            self.sprites.append(pygame.image.load(self.path + f'{i}.png').convert_alpha())

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [0,0]

    def update(self):
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

pygame.init()
clock = pygame.time.Clock()