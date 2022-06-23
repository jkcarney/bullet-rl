import pygame
import constants


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bounds_x, bounds_y):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = (0, 0)
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        img = pygame.image.load('15.png').convert()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(constants.ALPHA)  # set alpha
        self.image = img
        self.rect = self.image.get_rect()
