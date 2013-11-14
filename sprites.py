__author__ = 'Mike Mcmahon'

import pygame
from Color import *


class GameBase(object):
    def __init__(self):
        self._rect = self._x, self._y, self._width, self._width = 0, 0, 0, 0
        self._pos = self._x, self._y

    def get_pos(self):
        return self._pos

    def set_pos(self, point):
        self._pos = self._x, self._y = point

    def get_rect(self):
        return self._rect

    def set_rect(self, x, y, width, height):
        self._rect = self._x, self._y, self._width, self._width = x, y, width, height


class Citizen(GameBase):
    def __init__(self, x, y, width, height):
        self.set_rect(x, y, width, height)
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._alive_color = GREY
        self._dead_color = WHITE
        self._highlight_color = RED
        self._is_alive = False
        self._is_highlighted = False
        self._next_state = -1

    def highlight(self):
        self._is_highlighted = True

    def clear_highlight(self):
        self._is_highlighted = False

    def kill_next_generation(self):
        """
        The next time generate() is called we will kill this citizen
        @return:
        """
        self._next_state = 0

    def resurrect_next_generation(self):
        """
        THe next time generate() is called we will ressurect this citizen
        @return:
        """
        self._next_state = 1

    def will_die(self):
        """
        Checks if the next call to generate() will kill this citizen
        @return:
        """
        return True if self._next_state == 0 else False

    def will_resurrect(self):
        """
        Checks if the next call to generate() will resurrect this citizen
        @return:
        """
        return True if self._next_state == 1 else False

    def kill(self):
        """
        Kills this citizen
        @return:
        """
        self._is_alive = False
        pass

    def resurrect(self):
        """
        By the grace of the neighbor we are brought back to life!
        @return:
        """
        self._is_alive = True

    def is_alive(self):
        return self._is_alive

    def _fill_color(self):
        """
        Applies the specified color to the sprite
        """
        self._surface.fill(GREY)

        if self._is_alive:
            self._surface.fill(self._alive_color, (1, 1, 8, 8))
        elif self._is_highlighted:
            self._surface.fill(self._highlight_color, (1, 1, 8, 8))
        else:
            self._surface.fill(self._dead_color, (1, 1, 8, 8))

    def set_color(self, alive, dead, highlight):
        self._alive_color = alive
        self._dead_color = dead
        self._highlight_color = highlight

    def generate(self):
        """
        Applies the next state to the citizen
        @return:
        """
        self.kill() if self.will_die() else self.resurrect() if self.will_resurrect() else None

        # Reset the next state
        self._next_state = -1

    def blit_to(self, surface):
        """
        Blits to the surface and sets the rect to whatever is blit on that surface
        @param surface:
        """
        self._fill_color()
        self._rect = surface.blit(self._surface, (self._x, self._y))