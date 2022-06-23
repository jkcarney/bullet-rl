import pygame
import os
import constants


class Player(pygame.sprite.Sprite):
    def __init__(self, bounds_x, bounds_y):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

        img = pygame.image.load('Ship_1.png').convert()
        img.convert_alpha()  # optimise alpha
        img.set_colorkey(constants.ALPHA)  # set alpha
        self.image = img
        self.rect = self.image.get_rect()

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x >= self.bounds_x - self.image.get_width():
            self.rect.x = self.bounds_x - self.image.get_width()
        elif self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= self.bounds_y - self.image.get_height():
            self.rect.y = self.bounds_y - self.image.get_height()
        elif self.rect.y <= 0:
            self.rect.y = 0

        print(f'{self.rect.x}, {self.rect.y}')
