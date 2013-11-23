"""
author: Family
date: 11/17/13
"""

import os


class ShapeSelect:
    def __init__(self):
        self.first = (-1, -1)
        self.last = (-1, -1)
        self.loaded = None

    def read_shape_data(self, shape):
        """
        Reads in the shape data and stores the rows, cols, and shape information
        @param shape:
        @return:
        """
        rows = 0
        cols = shape.find("!")
        for i in range(len(shape)):
            if shape[i] == "!":
                rows += 1
        self.loaded = rows, cols, shape

    def drop_shape(self, rows, cols, pos, sprites, highlight=False):
        """
        Display on the gameboard the shape, by either killing/resurrecting the shape (on drop) or a simple highlight
        with highlight=True
        @param rows:  the rows in the grid
        @param cols: the cols in the grid
        @param pos: the position of the current sprite
        @param sprites: the game sprites
        @param highlight: show as a highlight or activate/deactivate the cell
        @return:
        """
        x, y = pos

        shape_rows, shape_cols, shape_data = self.loaded
        shape_end_x = x + shape_cols
        shape_end_y = y + shape_rows
        x_range = [x for x in range(x, shape_end_x if shape_end_x <= cols else cols)]
        y_range = [y for y in range(y, shape_end_y if shape_end_y <= rows else rows)]

        for row in y_range:
            for col in x_range:
                index = (row * cols) + col
                shape_index = ((row - y_range[0]) * shape_cols) + (col - x_range[0])
                if shape_data.replace("!", "")[shape_index] == "0":
                    if highlight:
                        sprites[index].is_shape_selected = False
                    else:
                        sprites[index].kill()
                elif shape_data.replace("!", "")[shape_index] == "1":
                    if highlight:
                        sprites[index].is_shape_selected = True
                    else:
                        sprites[index].resurrect()

    def highlight_selected(self, cols, sprites):
        """
        Tries to draw the border around the selected region
        @param cols:
        @param sprites:
        @return:
        """
        x1, y1 = self.first
        x2, y2 = self.last

        # Clear the sprites
        for sprite in sprites:
            sprite.is_shape_selected = False

        if not x1 == -1:
            sprites[(x1 * cols) + y1].is_shape_selected = True
        if not x2 == -1:
            sprites[(x2 * cols) + y2].is_shape_selected = True

        if not x1 == -1 and not x2 == -1:
            max_x, min_x = (x1, x2) if x1 > x2 else (x2, x1)
            max_y, min_y = (y1, y2) if y1 > y2 else (y2, y1)

            # We can't use a generator because it will be consumed once iterated
            x_range = [x for x in range(min_x, max_x+1)]
            y_range = [y for y in range(min_y, max_y+1)]

            # Highlights the top-most wall
            for (x, y) in (((y, min_x) for y in y_range)):
                sprites[(y * cols) + x].is_shape_selected = True

            # Highlights the bottom-most wall
            for (x, y) in (((y, max_x) for y in y_range)):
                sprites[(y * cols) + x].is_shape_selected = True

            # Highlights the right-most wall
            for (x, y) in (((max_y, x) for x in x_range)):
                sprites[(y * cols) + x].is_shape_selected = True

            # Highlights the left-most wall
            for (x, y) in (((min_y, x) for x in x_range)):
                sprites[(y * cols) + x].is_shape_selected = True

    def get_selected(self, cols, sprites):
        """
        get the sprites within the selected region
        @param cols:
        @param sprites:
        @return:
        """
        x1, y1 = self.first
        x2, y2 = self.last

        # We absolutely must have both
        if x1 == -1 or x2 == -1:
            return None, 0, 0

        max_x, min_x = (x1, x2) if x1 > x2 else (x2, x1)
        max_y, min_y = (y1, y2) if y1 > y2 else (y2, y1)

        # We can't use a generator because it will be consumed once iterated
        x_range = [x for x in range(min_x, max_x+1)]
        y_range = [y for y in range(min_y, max_y+1)]

        dest_sprites = list()
        for x in x_range:
            for y in y_range:
                dest_sprites.append(sprites[(y * cols) + x])

        return dest_sprites, (max_x - min_x) + 1, (max_y - min_y) + 1

    def clear_first(self):
        """
        Clears the first clicked element when in select mode
        @return:
        """
        self.first = (-1, -1)

    def clear_last(self):
        """
        Clears the last clicked element when in select mode
        @return:
        """
        self.last = (-1, -1)

    def clear_loaded(self):
        """
        Clears the loaded shape
        @return:
        """
        self.loaded = None

    def clear_all(self):
        """
        Clears everything associated
        @return:
        """
        self.clear_first()
        self.clear_last()
        self.clear_loaded()


class GameState:
    def __init__(self):
        self.is_paused = True
        self.is_shape_select = False
        self.is_shape_load = False


def collect_gameboard(cells, rows, cols):
    collected = ''
    for row in range(rows):
        for col in range(cols):
            collected += '1' if cells[(cols * row) + col].is_cell_alive() else '0'
        collected += os.linesep
    return collected