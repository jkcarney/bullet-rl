from typing import Tuple, Optional

import pygame
import gym
from gym.core import ActType, ObsType
from gym.spaces import Discrete, Box
from pygame import Vector2
import numpy as np
import sys
import math
from player import Player
from bullet import Bullet
import constants


class BulletHell(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array", "single_rgb_array"],
        "render_fps": 30
    }

    def __init__(self):
        pygame.init()
        self.stepcnt = 0
        self.screen = pygame.display.set_mode(constants.SIZE)
        self.player = Player(constants.width, constants.height)  # spawn player
        self.player.rect.x = constants.width // 2  # go to x
        self.player.rect.y = constants.height // 2  # go to y
        self.player_list = pygame.sprite.GroupSingle()
        self.player_list.add(self.player)

        self.timer = pygame.time.Clock()
        self.SPAWN_BULLET = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_BULLET, constants.BULLET_SPAWN_RATE)
        self.closest = None

        # 5 discrete actions; do nothing, up, down, left, right
        self.action_space = Discrete(5)
        # Observation space is an array of tuples (or 2d array), the closest bullet count bullets
        # position relative to the spaceship
        self.observation_space = Box(low=-constants.width,
                                     high=constants.width,
                                     shape=(constants.CLOSEST_BULLET_COUNT, 2))

        self.bullet_list = pygame.sprite.Group()
        for _ in range(constants.CLOSEST_BULLET_COUNT + 3):
            bullet = Bullet(constants.width, constants.height)
            self.bullet_list.add(bullet)
            bullet.set_starting_loc_and_vel()

        self.steps = 4

    # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Vector_formulation
    # Vector2.length((p - a) - Vector2.dot((p - a), v) * v)
    # p => Player's Current Location
    # a => Bullet Location
    # v => Bullet's Vector, -NORMALIZED-
    # This returns p's distance to the line formed by 'a' and 'v'. It has some rounding error but it's pretty close
    def observe(self):
        self.closest = self.player.get_closest_bullets(self.bullet_list, n=constants.CLOSEST_BULLET_COUNT)
        out = [x[2] for x in self.closest]
        # Pad out list to always fit 9,2
        while len(out) != constants.CLOSEST_BULLET_COUNT:
            out.append((-1, -1))

        # Do matrix subtraction to get relative coordinates
        return np.array([*out]) - np.array([self.player.rect.centerx, self.player.rect.centery])

    # noinspection PyUnresolvedReferences
    def step(self, action) -> Tuple[ObsType, float, bool, dict]:
        done = False
        reward = 0.1
        self.stepcnt += 1
        # We need to reassign self.player here. For some reason, when self.player is added to the sprite
        # group in init, the sprite added to the group and the sprite that is self.player differs.
        # I have no idea why this happens and why self.player doesn't function as a pointer to what lives in
        # self.player_list. WHATEVER.
        self.player = self.player_list.sprite

        # Do nothing
        if action == 0:
            self.player.control(0, 0)
        # Go up
        if action == 1:
            self.player.control(0, self.steps)
        # Go down
        if action == 2:
            self.player.control(0, -self.steps)
        # Go left
        if action == 3:
            self.player.control(-self.steps, 0)
        # Go right
        if action == 4:
            self.player.control(self.steps, 0)

        for event in pygame.event.get():
            if event.type == self.SPAWN_BULLET:
                bullet = Bullet(constants.width, constants.height)
                self.bullet_list.add(bullet)
                bullet.set_starting_loc_and_vel()

        self.player.update()
        self.bullet_list.update()
        self.timer.tick(self.metadata['render_fps'])

        self.player.zero()

        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.bullet_list, False)
        if len(blocks_hit_list) != 0:
            done = True
            reward = 0

        return self.observe(), reward, done, {}

    def redraw(self):
        self.screen.fill(constants.BLACK)
        self.bullet_list.draw(self.screen)
        self.player_list.draw(self.screen)
        for bullet, dis, _ in self.closest:
            pygame.draw.line(self.screen, 255, Vector2(self.player.rect.centerx, self.player.rect.centery),
                             Vector2(bullet.rect.centerx, bullet.rect.centery), width=1)
        pygame.display.flip()

    def reset(self, *, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None,):
        for b in self.bullet_list:
            b.kill()
        self.player_list.sprite.rect.x = constants.width // 2  # go to x
        self.player_list.sprite.rect.y = constants.height // 2  # go to y
        self.timer = pygame.time.Clock()
        for _ in range(5):
            bullet = Bullet(constants.width, constants.height)
            self.bullet_list.add(bullet)
            bullet.set_starting_loc_and_vel()
        return self.observe()

    def render(self, mode="human"):
        self.redraw()

    def close(self):
        pygame.display.quit()
        pygame.quit()


# fun lil code to draw lines teehee

# pygame.draw.line(self.screen, pygame.color.Color('deeppink'),
#                  Vector2(self.player.rect.centerx, self.player.rect.centery),
#                  Vector2(self.player.rect.centerx - math.cos(45 * math.pi / 180) * 100,
#                          self.player.rect.centery - math.sin(45 * math.pi / 180) * 100),
#                  width=3)
