"""
author: Mike McMahon

created: 11/13/13

"""

import os


class GameState:
    IN_GAME = 0
    SETTINGS = 1
    EDITOR = 2

    def __init__(self):
        self.is_paused = True
        self.current_state = GameState.IN_GAME

    def pause(self):
        """
        For states that support pausing this will pause the state
        """
        self.is_paused = True

    def unpause(self):
        """
        For states the support pausing this will unpause the state
        """
        self.is_paused = False


def collect_gameboard(cells, rows, cols):
    collected = ''
    for row in range(rows):
        for col in range(cols):
            collected += '1' if cells[(cols * row) + col].is_cell_alive() else '0'
        collected += os.linesep
    return collected