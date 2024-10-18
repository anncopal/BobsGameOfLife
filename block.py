import pygame

red = (255, 0, 0)


class Block (pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(red)
        self.rect = self.image.get_rect()
