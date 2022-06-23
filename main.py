import pygame
import numpy
import sys
from player import Player
import constants


def mainloop():
    pygame.init()
    screen = pygame.display.set_mode(constants.SIZE)
    player = Player(constants.width, constants.height)  # spawn player
    player.rect.x = 0  # go to x
    player.rect.y = 0  # go to y
    player_list = pygame.sprite.Group()
    player_list.add(player)
    steps = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        screen.fill(constants.BLACK)
        player.update()
        player_list.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    mainloop()
