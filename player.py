import pygame
from pygame import Vector2
import os
import constants
import heapq


class Player(pygame.sprite.Sprite):
    def __init__(self, bounds_x, bounds_y):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

        img = pygame.image.load('Ship_1.png').convert_alpha()
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

    def zero(self):
        self.movex = 0
        self.movey = 0

    def get_closest_bullets(self, bullet_list, n=10):
        l = []
        for b in bullet_list:
            distance = self.dis(Vector2(b.rect.centerx, b.rect.centery))
            # l.append((distance, b))
            l.append((b, distance, (b.rect.centerx, b.rect.centery)))
        l.sort(key=lambda e: e[1])
        return l[:n]

    def dis(self, other):
        pos = Vector2(self.rect.centerx, self.rect.centery)
        return pos.distance_to(other)
