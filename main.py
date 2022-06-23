import random

import pygame
from pygame import Vector2
import numpy as np
import sys
from player import Player
from bullet import Bullet
import constants


def mainloop():
    pygame.init()
    screen = pygame.display.set_mode(constants.SIZE)
    player = Player(constants.width, constants.height)  # spawn player
    player.rect.x = constants.width // 2  # go to x
    player.rect.y = constants.height // 2  # go to y
    player_list = pygame.sprite.Group()
    player_list.add(player)
    bg = pygame.image.load("bg.png")
    bg = pygame.transform.scale(bg, constants.SIZE)

    timer = pygame.time.Clock()
    SPAWN_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_BULLET, constants.BULLET_SPAWN_RATE)

    BULLET_VELOCITY_INCREASE = pygame.USEREVENT + 2
    pygame.time.set_timer(BULLET_VELOCITY_INCREASE, constants.BULLET_SPAWN_RATE)

    # Initial bullet spawning
    bullet_list = pygame.sprite.Group()
    for _ in range(5):
        bullet = Bullet(constants.width, constants.height)
        bullet_list.add(bullet)
        bullet.set_starting_loc_and_vel()

    steps = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWN_BULLET:
                bullet = Bullet(constants.width, constants.height)
                bullet_list.add(bullet)
                bullet.set_starting_loc_and_vel()

            # if event.type == BULLET_VELOCITY_INCREASE:
            #     constants.SPEED_MIN += constants.BULLET_SPEED_INCREASE_AMOUNT
            #     constants.SPEED_MAX += constants.BULLET_SPEED_INCREASE_AMOUNT

            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
                if event.key == pygame.K_LEFT:
                    player.control(-steps, 0)
                if event.key == pygame.K_RIGHT:
                    player.control(steps, 0)
                if event.key == pygame.K_UP:
                    player.control(0, -steps)
                if event.key == pygame.K_DOWN:
                    player.control(0, steps)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.control(steps, 0)
                if event.key == pygame.K_RIGHT:
                    player.control(-steps, 0)
                if event.key == pygame.K_UP:
                    player.control(0, steps)
                if event.key == pygame.K_DOWN:
                    player.control(0, -steps)

        blocks_hit_list = pygame.sprite.spritecollide(player, bullet_list, False)
        if len(blocks_hit_list) != 0:
            print('Collision')
            pygame.quit()
            sys.exit()

        screen.fill(constants.BLACK)
        player.update()
        bullet_list.update()
        bullet_list.draw(screen)
        player_list.draw(screen)
        pygame.display.flip()
        timer.tick(60)


if __name__ == "__main__":
    mainloop()
