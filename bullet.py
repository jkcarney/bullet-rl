import random

import pygame
from pygame import Vector2
import constants
import numpy as np


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bounds_x, bounds_y):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = Vector2(0, 0)
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        img = pygame.image.load('15.png').convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()

    def is_out_of_bounds(self):
        return self.bounds_x + 10 < self.rect.centerx or self.rect.centerx < 0 - 10 or \
               self.bounds_y + 10 < self.rect.centery or self.rect.centery < 0 - 10

    def update(self):
        self.rect.x = self.rect.x + self.velocity.x
        self.rect.y = self.rect.y + self.velocity.y
        if self.is_out_of_bounds():
            self.kill()

    def set_starting_loc_and_vel(self):
        roll = random.random()
        # Start at x bounds zero; x-positive vector velocity
        if roll <= 0.25:
            self.rect.x = 0
            self.rect.y = random.randint(1, self.bounds_y)
            self.velocity = Vector2(random.randint(constants.SPEED_MIN, constants.SPEED_MAX),
                                    random.randint(-constants.SPEED_MAX, constants.SPEED_MAX))
        # Start at bounds_x; x-negative vector velocity
        elif 0.25 < roll <= 0.50:
            self.rect.x = self.bounds_x
            self.rect.y = random.randint(1, self.bounds_y)
            self.velocity = Vector2(-random.randint(constants.SPEED_MIN, constants.SPEED_MAX),
                                    random.randint(-constants.SPEED_MAX, constants.SPEED_MAX))
        # Start at y bounds zero; y-positive vector velocity
        elif 0.50 < roll <= 0.75:
            self.rect.x = random.randint(1, self.bounds_x)
            self.rect.y = 1
            self.velocity = Vector2(random.randint(-constants.SPEED_MAX, constants.SPEED_MAX),
                                    random.randint(constants.SPEED_MIN, constants.SPEED_MAX))
        # Start at bounds_y; y-negative vector velocity
        else:
            self.rect.x = random.randint(1, self.bounds_x)
            self.rect.y = self.bounds_y
            self.velocity = Vector2(random.randint(-constants.SPEED_MAX, constants.SPEED_MAX),
                                    -random.randint(constants.SPEED_MIN, constants.SPEED_MAX))
