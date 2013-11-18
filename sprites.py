import os
from pygame.rect import Rect
from pygame.sprite import Sprite
import colors

__author__ = 'Mike Mcmahon'

import pygame
import font
from colors import *


class GameBase(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self._x, self._y, self._width, self._height = 0, 0, 0, 0
        self.rect = Rect(self._x, self._y, self._width, self._height)
        self.image = None
        self.pos = self._x, self._y

    def get_pos(self):
        return self.pos

    def set_pos(self, *point):
        self.pos = self._x, self._y = point
        self.set_rect(self._x, self._y, self._width, self._height)

    def get_rect(self):
        return self.rect

    def set_rect(self, x, y, width, height):
        self._x, self._y, self._width, self._height = x, y, width, height
        self.rect = Rect(self._x, self._y, self._width, self._height)


class Cell(GameBase):
    def __init__(self, x, y, width, height):
        GameBase.__init__(self)
        self.set_rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alive_color = GREY
        self.dead_color = WHITE
        self.highlight_color = RED
        self.neighbor_highlight = YELLOW
        self.is_neighbor_highlighted = False
        self.cell_alive = False
        self.is_highlighted = False
        self.next_state = -1
        self._fill_color()
        self._neighbors = list()

    def add_neighbor(self, neighbor):
        if neighbor not in self._neighbors:
            self._neighbors.append(neighbor)

    def living_neighbors(self):
        """
        returns the count of neighbors that are alive
        """
        count = 0
        for neighbor in self._neighbors:
            if neighbor.is_cell_alive():
                count += 1

        return count

    def highlight(self):
        """
        Highlights the given cell and all surrounding neighbors
        """
        for neighbor in self._neighbors:
            neighbor.is_neighbor_highlighted = True

        self.is_highlighted = True

    def clear_highlight(self, force=False):
        """
        Clears the highlight on the cell
        @param force:
        True if we want to clear out the highlight for surrounding neighbors.
        """
        if force:
            for neighbor in self._neighbors:
                neighbor.is_neighbor_highlighted = False

        self.is_highlighted = False

    def kill_next_generation(self):
        """
        The next time generate() is called we will kill this cell
        @return:
        """
        self.next_state = 0

    def resurrect_next_generation(self):
        """
        THe next time generate() is called we will ressurect this cell
        @return:
        """
        self.next_state = 1

    def will_die(self):
        """
        Checks if the next call to generate() will kill this cell
        @return:
        """
        return True if self.next_state == 0 else False

    def will_resurrect(self):
        """
        Checks if the next call to generate() will resurrect this cell
        @return:
        """
        return True if self.next_state == 1 else False

    def kill(self):
        """
        Kills this cell
        @return:
        """
        self.cell_alive = False
        pass

    def resurrect(self):
        """
        By the grace of the neighbor we are brought back to life!
        @return:
        """
        self.cell_alive = True

    def is_cell_alive(self):
        """
        Gets the health of the cell
        @return:
        True = Alive
        False = Dead
        """
        return self.cell_alive

    def update(self, *args):
        # Terrible and dirty way to do the update...whatevz
        paused, do_generate, repaint = args

        if not paused and not do_generate:
            living = self.living_neighbors()
            if self.is_cell_alive():
                if living < 2:
                    self.kill_next_generation()
                if 2 <= living <= 3:
                    # Keep alive
                    pass
                if living > 3:
                    self.kill_next_generation()
            else:
                if living == 3:
                    self.resurrect_next_generation()

        if do_generate:
            self.generate()

        if repaint:
            self._fill_color()

    def _fill_color(self):
        """
        Applies the specified color to the sprite
        """
        self.image.fill(GREY)

        if self.cell_alive:
            self.image.fill(self.alive_color, (1, 1, 8, 8))
        elif self.is_highlighted:
            self.image.fill(self.highlight_color, (1, 1, 8, 8))
        elif self.is_neighbor_highlighted:
            self.image.fill(self.neighbor_highlight, (1, 1, 8, 8))
        else:
            self.image.fill(self.dead_color, (1, 1, 8, 8))

    def set_color(self, alive, dead, highlight):
        self.alive_color = alive
        self.dead_color = dead
        self.highlight_color = highlight

    def generate(self):
        """
        Applies the next state to the cell
        @return:
        """
        self.kill() if self.will_die() else self.resurrect() if self.will_resurrect() else None

        # Reset the next state
        self.next_state = -1


class GameButton(GameBase):

    def __init__(self, font_renderer, label="", icon_path=""):
        GameBase.__init__(self)
        self.label = None
        self.icon_path = None
        self._show_icon = False
        self.pos = self._x, self._y = 0, 0
        self.font_renderer = font_renderer
        self._show_label = True
        self.label_width, self.label_height = (0, 0)
        self._padding = 2

        self.set_label(label)
        self.set_icon(icon_path)

    def set_label(self, label):
        self.label = label
        self.label_width, self.label_height = self.font_renderer.size(self.label)

    def set_icon(self, icon):
        self.icon_path = icon
        # TODO - this is a terrible way to check if we should show the image
        self._show_icon = True if len(self.icon_path) > 0 else False

    def get_width(self):
        """
        Gets the width of this object (including the icon width if an icon is specified
        @return:
        """
        icon_width = (self.label_height + self._padding) if self._show_icon else 0
        return self._padding + icon_width + self.label_width + self._padding

    def get_height(self):
        """
        Gets the height of this object
        @return:
        """
        return self.label_height + self._padding

    def show_label(self):
        self._show_label = True

    def hide_label(self):
        self._show_label = False

    def _paint(self):
        if self._show_label:
            font_surface = font.create_label(self.font_renderer, self.label, BLACK)

        if self._show_icon:
            image_path = os.path.join("assets", self.icon_path)
            image_width, image_height = (self.label_height - (self._padding * 2)), (self.label_height - (self._padding * 2))
            image_surface = pygame.image.load(image_path)
            image_surface = pygame.transform.smoothscale(image_surface, (image_width, image_height))

        display_width = self.get_width()
        display_height = self.get_height()
        display_surface = pygame.Surface(
            (display_width,
             display_height)
        )
        display_surface.fill(BLACK)
        colors.fill_gradient(
            display_surface,
            WHITE,
            GREY,
            rect=Rect(
                1,
                1,
                display_width - 3,
                display_height - 2),
            forward=True
        )

        display_surface.blit(image_surface, (self._padding, self._padding))
        display_surface.blit(font_surface, (self._padding + image_width, self._padding)) if self._show_label else None

        self.image = display_surface
        self.set_rect(self._x, self._y, self.image.get_width(), self.image.get_height())

    def update(self, *args):
        if len(args) > 0:
            label, icon = args[0]
            self.set_label(label)
            self.set_icon(icon)
        self._paint()